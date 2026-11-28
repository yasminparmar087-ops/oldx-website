import test from 'node:test';
import assert from 'node:assert/strict';
import {createC2H2AGReaderMetadataSource as create,
 createC2H2AGReaderSourcePorts as compose,
 C2_H2AG_READER_UID as UID,C2_H2AG_READER_EMAIL as EMAIL}
 from '../../scripts/c2-h2ag-reader-metadata-source.mjs';
const at=1800000000000;
const img='asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-kms-reader@sha256:'+'a'.repeat(64);
const evidence={principal:EMAIL,uid:UID,image:img,expiresAtMs:at+60000};
const meta='http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/';
const token='A'.repeat(100);
const reply=v=>new Response(v,{headers:{'Metadata-Flavor':'Google'}});
const choices=()=>({enabled:true,readerEmail:EMAIL,readerUid:UID,readerImage:img,
 verifyRuntimeBinding:async()=>evidence,
 fetchMetadata:async url=>reply(url===meta+'email'?EMAIL:
   JSON.stringify({access_token:token,token_type:'Bearer',expires_in:1800})),
 now:()=>at});
test('NEW reader is OFF without verified source/runtime binding',async()=>{
 const a=create();assert.equal(a.ready,false);
 await assert.rejects(a.getReaderCredential({principal:EMAIL,uid:UID}),/NOT_VERIFIED/);
});
test('NEW actual H2AG UID and dedicated image are non-substitutable',()=>{
 for(const changed of [{readerUid:'107238619872767759560'},
   {readerEmail:'oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com'},
   {readerImage:'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-kms-reader@sha256:'+'g'.repeat(64)},
   {verifyRuntimeBinding:null}])assert.equal(create({...choices(),...changed}).ready,false);
});
test('NEW reader uses only OWN metadata identity and bounded OAuth credential',async()=>{
 const calls=[];const c=choices();c.fetchMetadata=async(url,init)=>{
   calls.push([url,init]);return reply(url===meta+'email'?EMAIL:
     JSON.stringify({access_token:token,token_type:'Bearer',expires_in:1800}));
 };
 const r=await create(c).getReaderCredential({principal:EMAIL,uid:UID});
 assert.equal(r.uid,UID);assert.equal(r.principal,EMAIL);
 assert.equal(r.source,'cloud-run-metadata');assert.equal(r.expiresAtMs,at+60000);
 assert.equal(r.accessToken,token);
 assert.equal(calls.length,2);
 assert.deepEqual(calls.map(([url])=>url),[meta+'email',meta+'token']);
 assert.equal(calls.every(([url,opts])=>opts.method==='GET'&&opts.redirect==='error'&&
   opts.credentials==='omit'&&opts.headers['Metadata-Flavor']==='Google'&&
   !Object.hasOwn(opts.headers,'Authorization')),true);
});
test('NEW unverified runtime evidence denies before reading metadata',async()=>{
 let calls=0;
 const c=choices();c.verifyRuntimeBinding=async()=>({...evidence,uid:'different'});
 c.fetchMetadata=()=>{calls++;throw Error('NEVER');};
 await assert.rejects(create(c).getReaderCredential({principal:EMAIL,uid:UID}),/NOT_VERIFIED/);
 assert.equal(calls,0);
});
test('NEW metadata email mismatch and malformed OAuth never authorize reader',async()=>{
 for(const bad of ['wrong-email','missing-token','wrong-body']){
  const c=choices();
  c.fetchMetadata=async url=>reply(url===meta+'email'?
    bad==='wrong-email'?'oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com':EMAIL:
    bad==='missing-token'?'{}':JSON.stringify({access_token:'wrong',expires_in:1000,token_type:'Bearer'}));
  await assert.rejects(create(c).getReaderCredential({principal:EMAIL,uid:UID}),/NOT_VERIFIED/);
 }
});
test('NEW reader source compose default OFF and caller cannot override identity',()=>{
 assert.equal(compose().ready,false);
 assert.equal(compose({enabled:true,metadataOptions:{...choices(),enabled:false},
   verifyReaderAuthority:()=>{},consumeDurableReadBudget:()=>{},fetchReader:()=>{}}).ready,false);
});
