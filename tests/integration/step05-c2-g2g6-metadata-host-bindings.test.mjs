import test from 'node:test';
import assert from 'node:assert/strict';
import {createC2CloudRunMetadataIdentity} from '../../scripts/c2-cloud-run-metadata-identity.mjs';
import {createC2G2G6MetadataBoundHostSourceAssembly} from '../../functions/staging-marketplace/c2-g2g6-enabled-host-source-assembly.mjs';
const time=1800000000000;
const med='oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com';
const gate='oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
const medUid='100779414920484819274',gateUid='107238619872767759560';
const origin='https://gateway-abc.asia-south1.run.app';
const assertion='urn:oldx:c2:website';
const jwt=claims=>[JSON.stringify({alg:'RS256',kid:'offline-shape-only'}),
 JSON.stringify({iss:'https://accounts.google.com',email:med,email_verified:true,
 sub:medUid,aud:origin,iat:time/1000,exp:time/1000+3600,...claims}),'NOT_A_REAL_SIGNATURE']
 .map(x=>Buffer.from(x).toString('base64url')).join('.');
const response=token=>new Response(token,{headers:{'Metadata-Flavor':'Google'}});
const options=()=>({enabled:true,serviceAccount:med,expectedSubject:medUid,
 invokerAudience:origin,assertionAudience:assertion,now:()=>time});
test('new role binding is OFF by default and rejects invalid numeric UID without calls',async()=>{
 let calls=0;const fetchMetadata=()=>{calls++;throw Error('unexpected');};
 for(const opts of [{...options(),enabled:false},{...options(),expectedSubject:'email'}]){
 const x=createC2CloudRunMetadataIdentity({...opts,fetchMetadata});
 assert.equal(x.ready,false);
 await assert.rejects(x.getInvokerCredential({audience:origin}),/UNAVAILABLE/);
 } assert.equal(calls,0);
});
test('new pinned role uses two distinct exact metadata audiences and short assertion lease',async()=>{
 const calls=[];
 const x=createC2CloudRunMetadataIdentity({...options(),fetchMetadata:async(url,init)=>{
 calls.push({url,init});return response(jwt({aud:new URL(url).searchParams.get('audience')}));
 }});
 const iam=await x.getInvokerCredential({audience:origin});
 const proof=await x.getWebsiteAttestation({audience:assertion});
 assert.equal(iam.type,'cloud-run-iam-id-token');
 assert.equal(iam.audience,origin);assert.equal(proof.audience,assertion);
 assert.equal(iam.expiresAtMs,time+3600000);assert.equal(proof.expiresAtMs,time+60000);
 assert.notEqual(iam.token,proof.token);
 for(const {url,init} of calls){
 assert.equal(new URL(url).origin,'http://metadata.google.internal');
 assert.equal(new URL(url).pathname,'/computeMetadata/v1/instance/service-accounts/default/identity');
 assert.equal(init.method,'GET');assert.equal(init.redirect,'error');
 assert.equal(init.credentials,'omit');assert.equal(init.headers['Metadata-Flavor'],'Google');
 assert.equal(Object.hasOwn(init.headers,'Authorization'),false);
 } assert.equal(calls.length,2);
 // These unsigned fixtures prove transport/shape only, never independent authentication.
});
test('new role pin denies same email with wrong UID, other workload and stripped JWT',async()=>{
 for(const token of [jwt({sub:gateUid}),jwt({email:gate,sub:gateUid}),jwt({}).split('.').slice(0,2).join('.')+'.']){
 const x=createC2CloudRunMetadataIdentity({...options(),fetchMetadata:async()=>response(token)});
 await assert.rejects(x.getInvokerCredential({audience:origin}),/UNAVAILABLE/);
 }
});
test('new two role adapters keep gateway identity separate and refuse arbitrary audience before fetch',async()=>{
 let calls=0;
 const x=createC2CloudRunMetadataIdentity({...options(),serviceAccount:gate,expectedSubject:gateUid,
 fetchMetadata:async()=>{calls++;return response(jwt({email:gate,sub:gateUid}));}});
 await assert.rejects(x.getInvokerCredential({audience:'https://attacker.example'}),/UNAVAILABLE/);
 assert.equal(calls,0);
 const item=await x.getInvokerCredential({audience:origin});
 assert.equal(item.principal,gate);assert.equal(calls,1);
});
test('new assembly wrapper is OFF and accessor config never executes',async()=>{
 let calls=0;const config={enabled:true};
 Object.defineProperty(config,'websiteOptions',{get(){calls++;throw Error('unexpected');}});
 for(const x of [createC2G2G6MetadataBoundHostSourceAssembly(),
 createC2G2G6MetadataBoundHostSourceAssembly(config)]){
 assert.equal(x.sourceComposed,false);assert.equal((await x.gateway.fetch()).status,503);
 }assert.equal(calls,0);
});
test('new wrapper rejects competing identity callbacks and UID/audience drift without network',()=>{
 let calls=0;const fetchMetadata=()=>{calls++;throw Error('unexpected');};
 const make=()=>({enabled:true,websiteOptions:{privateGatewayOrigin:origin,mediationAudience:assertion},
 gatewayHostOptions:{websiteIdentity:{expectedSubject:medUid,attestationAudience:assertion},
 gatewayOptions:{backendOrigin:'https://backend-abc.asia-south1.run.app',attestationAudience:'urn:oldx:c2:gateway'}},
 backendOptions:{googleIdentity:{expectedSubject:gateUid,attestationAudience:'urn:oldx:c2:gateway'}},
 metadataIdentityOptions:{fetchMediatorMetadata:fetchMetadata,fetchGatewayMetadata:fetchMetadata}});
 for(const change of [
 x=>{x.websiteOptions.getWebsiteAttestation=undefined;},
 x=>{x.gatewayHostOptions.gatewayOptions.getInvokerCredential=fetchMetadata;},
 x=>{x.gatewayHostOptions.websiteIdentity.expectedSubject=gateUid;},
 x=>{x.backendOptions.googleIdentity.attestationAudience=assertion;},
 x=>{x.gatewayHostOptions.gatewayOptions.backendOrigin='https://attacker.example';},
 x=>{}
 ]){
 const x=make();change(x);
 assert.equal(createC2G2G6MetadataBoundHostSourceAssembly(x).sourceComposed,false);
 }assert.equal(calls,0);
});
