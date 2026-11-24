import test from 'node:test';
import assert from 'node:assert/strict';
import {createC2CloudRunMetadataIdentity} from '../../scripts/c2-cloud-run-metadata-identity.mjs';

const serviceAccount='mediation-test@oldx-staging.iam.gserviceaccount.com';
const invokerAudience='https://oldx-step05-gateway-38472235077.asia-south1.run.app';
const assertionAudience='urn:oldx:staging:website-identity';
const clock = 1795565700000;
const enc = x => Buffer.from(JSON.stringify(x)).toString('base64url');
const token = (aud, overrides={}) =>
  enc({alg:'RS256',kid:'fixture'}) + '.' + enc({iss:'https://accounts.google.com',aud,email:serviceAccount,
    email_verified:true,sub:'12345678901234',iat:Math.floor(clock/1000)-1,exp:Math.floor(clock/1000)+3590,...overrides}) + '.signature';
const good = (aud, overrides={}) => new Response(token(aud,overrides),{status:200,headers:{'Metadata-Flavor':'Google'}});

test('C2 identity provider is completely inert OFF and has no implicit metadata fetch', async()=>{
  let count=0;
  const p=createC2CloudRunMetadataIdentity({serviceAccount,invokerAudience,assertionAudience,
    fetchMetadata:async()=>{count++;return good(invokerAudience);},now:()=>clock});
  assert.equal(p.ready,false);
  await assert.rejects(p.getInvokerCredential({audience:invokerAudience}),/C2_IDENTITY_UNAVAILABLE/);
  await assert.rejects(p.getWebsiteAttestation({audience:assertionAudience}),/C2_IDENTITY_UNAVAILABLE/);
  assert.equal(count,0);
});

test('separate exact Cloud Run IAM and website attestation audiences use bounded Google metadata token shapes',async()=>{
  const seen=[];
  const p=createC2CloudRunMetadataIdentity({enabled:true,serviceAccount,invokerAudience,assertionAudience,
    now:()=>clock,fetchMetadata:async(url,opt)=>{
      seen.push({url,opt});
      assert.equal(opt.method,'GET');assert.equal(opt.headers['Metadata-Flavor'],'Google');
      assert.equal(opt.redirect,'error'); assert.equal(opt.credentials,'omit');
      const audience=new URL(url).searchParams.get('audience');
      assert.equal(new URL(url).hostname,'metadata.google.internal');
      assert.equal(new URL(url).searchParams.get('format'),'full');
      return good(audience);
    }});
  assert.equal(p.ready,true);
  const iam=await p.getInvokerCredential({audience:invokerAudience});
  const signed=await p.getWebsiteAttestation({audience:assertionAudience});
  assert.equal(iam.type,'cloud-run-iam-id-token');
  assert.equal(iam.principal,serviceAccount);
  assert.equal(iam.audience,invokerAudience);
  assert.equal(signed.audience,assertionAudience);
  assert.notEqual(iam.token,signed.token);
  assert.equal(seen.length,2);
  assert.ok(Object.isFrozen(iam));
});

test('wrong audience and absent host binding fail closed before any transport',async()=>{
  let called=0;
  const fn=async()=>{called++;return good(invokerAudience);};
  const notReady=createC2CloudRunMetadataIdentity({enabled:true,serviceAccount,invokerAudience,
    assertionAudience:invokerAudience,fetchMetadata:fn,now:()=>clock});
  assert.equal(notReady.ready,false);
  const ready=createC2CloudRunMetadataIdentity({enabled:true,serviceAccount,invokerAudience,
    assertionAudience,fetchMetadata:fn,now:()=>clock});
  await assert.rejects(ready.getInvokerCredential({audience:'https://evil.invalid'}),/C2_IDENTITY_UNAVAILABLE/);
  await assert.rejects(ready.getWebsiteAttestation({audience:invokerAudience}),/C2_IDENTITY_UNAVAILABLE/);
  await assert.rejects(ready.getInvokerCredential({audience:invokerAudience,signal:AbortSignal.abort()}),/C2_IDENTITY_UNAVAILABLE/);
  assert.equal(called,0);
});

test('untrusted metadata response, malformed tokens, claims drift and stale token deny without leakage',async()=>{
  const variants=[
    ()=>new Response('not-a-jwt',{status:200,headers:{'Metadata-Flavor':'Google'}}),
    ()=>new Response(token(invokerAudience),{status:200}),
    ()=>new Response('',{status:403,headers:{'Metadata-Flavor':'Google'}}),
    ()=>good(invokerAudience,{aud:'https://evil.invalid'}),
    ()=>good(invokerAudience,{email:'foreign@oldx-staging.iam.gserviceaccount.com'}),
    ()=>good(invokerAudience,{iat:Math.floor(clock/1000)-500}),
    ()=>good(invokerAudience,{exp:Math.floor(clock/1000)+1}),
    ()=>new Response('x'.repeat(9000),{status:200,headers:{'Metadata-Flavor':'Google'}})
  ];
  for(const variant of variants){
    const p=createC2CloudRunMetadataIdentity({enabled:true,serviceAccount,invokerAudience,
      assertionAudience,now:()=>clock,fetchMetadata:async()=>variant()});
    await assert.rejects(p.getInvokerCredential({audience:invokerAudience}),/C2_IDENTITY_UNAVAILABLE/);
  }
});
