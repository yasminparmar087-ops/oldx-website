import test from 'node:test';
import assert from 'node:assert/strict';
import {once} from 'node:events';
import {request} from 'node:http';
import {readFile} from 'node:fs/promises';
import {createHash,generateKeyPairSync,privateEncrypt,constants} from 'node:crypto';
import {createC2OffMediatorServer,listenC2OffMediator,drainC2OffMediator} from '../../functions/staging-marketplace/c2-mediator-off-server.mjs';
import {createC2KmsRequestSigning,c2Crc32c} from '../../scripts/c2-kms-request-signing.mjs';
import {createMarketplaceRequestProofSigner,createMarketplaceRequestProofVerifier} from '../../scripts/marketplace-gateway-request-proof.mjs';
import {prepareC2SyntheticCleanupManifest} from '../../scripts/c2-synthetic-cleanup-manifest.mjs';
async function fixture(run){
 const server=createC2OffMediatorServer();server.listen(0,'127.0.0.1');await once(server,'listening');
 const call=(path,options={})=>new Promise((resolve,reject)=>{
  const req=request({host:'127.0.0.1',port:server.address().port,path,method:options.method??'GET',headers:options.headers},res=>{
   let body='';res.on('data',x=>body+=x);res.on('end',()=>resolve({status:res.statusCode,headers:res.headers,body}));
  });req.on('error',reject);req.end(options.body);
 });
 try{await run(call,server);}finally{if(server.listening)await drainC2OffMediator(server);}
}
test('NEW H1 compiled-OFF server health, exact routes, headers and no activation',async()=>{
 await fixture(async call=>{
  assert.equal((await call('/health')).status,200);
  assert.equal((await call('/health',{method:'HEAD'})).body,'');
  for(const op of ['save','owner','archive','list','detail']){
   const r=await call('/api/staging/marketplace/'+op,{method:'POST'});
   assert.equal(r.status,503);assert.equal(r.headers['access-control-allow-origin'],undefined);
   assert.equal(r.headers['cache-control'],'private, no-store');assert.ok(r.body.length<200);
  }
  for(const path of ['/healthz','/health?x=1','/api/staging/marketplace/list?x=1','/api/staging/marketplace/%6cist','https://evil.invalid/health'])assert.equal((await call(path)).status,404);
  assert.equal((await call('/api/staging/marketplace/list')).status,405);
  assert.equal((await call('/health',{headers:{authorization:'Bearer NEVER_LEAK_THIS'}})).status,403);
  const denied=await call('/api/staging/marketplace/list',{method:'POST',headers:{origin:'https://evil.invalid','x-oldx-gateway-request-proof':'NEVER_LEAK_THIS'}});
  assert.equal(denied.status,403);assert.ok(!denied.body.includes('NEVER_LEAK_THIS'));
 });
});
test('NEW H1 request limits, explicit bind validation and shutdown',async()=>{
 await fixture(async(call,server)=>{
  assert.equal((await call('/api/staging/marketplace/list',{method:'POST',headers:{'content-length':'4097'}})).status,413);
  assert.equal((await call('/api/staging/marketplace/save',{method:'POST',headers:{'content-length':'32769'}})).status,413);
  const invalid=createC2OffMediatorServer();
  await assert.rejects(listenC2OffMediator(invalid,{port:'bad'}),/C2_BIND_DENIED/);
  assert.equal(server.requestTimeout,5000);assert.equal(server.headersTimeout,5000);
  assert.equal(server.maxRequestsPerSocket,1);
  await drainC2OffMediator(server);assert.equal(server.listening,false);
 });
});
test('NEW H1 immutable packaging contains only OFF server and no provider code',async()=>{
 const base=new URL('../../functions/staging-marketplace/',import.meta.url);
 const docker=await readFile(new URL('Dockerfile.c2-mediator-off',base),'utf8');
 const ignore=await readFile(new URL('Dockerfile.c2-mediator-off.dockerignore',base),'utf8');
 const server=await readFile(new URL('c2-mediator-off-server.mjs',base),'utf8');
 assert.match(docker,/FROM --platform=linux\/amd64 gcr\.io\/distroless\/nodejs24-debian13:nonroot@sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec/);
 assert.equal((docker.match(/^COPY /gm)||[]).length,1);
 assert.match(docker,/USER 65532:65532/);assert.match(docker,/STOPSIGNAL SIGTERM/);
 assert.ok(!/^(RUN|ARG|ADD) /m.test(docker));assert.ok(!server.includes('enabled=true'));
 assert.deepEqual([...server.matchAll(/from '([^']+)'/g)].map(x=>x[1]),['node:http','node:events','node:path','node:url']);
 assert.equal(ignore.trimEnd(),'**\n!functions/\n!functions/staging-marketplace/\n!functions/staging-marketplace/c2-mediator-off-server.mjs');
 assert.match(server,/process\.on\('SIGTERM',stop\)/);
});
const pair=generateKeyPairSync('rsa',{modulusLength:2048});
const keyVersion='projects/oldx-staging/locations/asia-south1/keyRings/SYNTHETIC/cryptoKeys/intent/cryptoKeyVersions/1';
const algorithm='RSA_SIGN_PKCS1_2048_SHA256',kid='synthetic-intent-v1';
const fingerprint=createHash('sha256').update(pair.publicKey.export({type:'spki',format:'der'})).digest('hex');
let clock=1700000000000;
const messageAttestation='aaaa.bbbb.cccccccccccccccccccccc';
const args={method:'POST',path:'/api/staging/marketplace/owner',body:Buffer.from('{}'),authorization:'Bearer aaaa.bbbb.cccc',attestationToken:messageAttestation};
function kms(overrides={}){
 let calls=0;const transcript=[];
 const config={enabled:true,kid,keyVersion,algorithm,
  publicKeyPem:pair.publicKey.export({type:'spki',format:'pem'}),publicKeySha256:fingerprint,
  validFromMs:clock-100,validUntilMs:clock+60000,now:()=>clock,
  getKeyVersionStatus:async()=>({name:keyVersion,state:'ENABLED',algorithm,publicKeySha256:fingerprint}),
  asymmetricSign:async(input,options)=>{
   calls++;transcript.push(input);assert.equal(options.retry,false);
   const digest=Buffer.from(input.digest.sha256,'base64');
   assert.equal(input.digestCrc32c,c2Crc32c(digest));assert.equal(input.data,undefined);
   // KMS PKCS1 SHA256 signs the supplied digest as DigestInfo, no second hash.
   const info=Buffer.concat([Buffer.from('3031300d060960864801650304020105000420','hex'),digest]);
   const signature=privateEncrypt({key:pair.privateKey,padding:constants.RSA_PKCS1_PADDING},info);
   return {name:keyVersion,verifiedDigestCrc32c:true,signature:signature.toString('base64'),signatureCrc32c:c2Crc32c(signature)};
  },...overrides};
 return {config,provider:createC2KmsRequestSigning(config),count:()=>calls,transcript};
}
test('NEW KMS exact canonical bytes sign once through existing intent verifier',async()=>{
 assert.equal(c2Crc32c(Buffer.from('123456789')),'3808858755');
 const f=kms();assert.equal(f.provider.ready,true);
 const signer=createMarketplaceRequestProofSigner({enabled:true,kid,signMessage:f.provider.signMessage,now:()=>clock,random:()=>Buffer.alloc(16,1)});
 let consumes=0;
 const verifier=createMarketplaceRequestProofVerifier({enabled:true,resolvePublicKey:f.provider.resolvePublicKey,consumeNonce:async()=>({allowed:++consumes===1}),now:()=>clock});
 const proof=await signer(args);assert.equal(typeof proof,'string');
 assert.equal(await verifier({...args,proof}),true);
 assert.equal(await verifier({...args,proof}),false);
 assert.equal(f.count(),1);
 const canonical=Buffer.from(proof.split('.')[0],'base64url');
 assert.equal(f.transcript[0].digest.sha256,createHash('sha256').update(canonical).digest('base64'));
});
test('NEW KMS inactive, unknown, rotated, disabled, expired or invalid key fail closed',async()=>{
 for(const override of [{enabled:false},{keyVersion:keyVersion.replace('oldx-staging','production')},{algorithm:'RSA_SIGN_PSS_2048_SHA256'},{publicKeySha256:'0'.repeat(64)},{validUntilMs:clock-1}]){
  const f=kms(override);await assert.rejects(f.provider.signMessage(Buffer.from('{}'),{kid}),/C2_SIGNING_UNAVAILABLE/);assert.equal(f.count(),0);
 }
 for(const state of ['DISABLED','DESTROYED','PENDING_GENERATION']){
  const f=kms({getKeyVersionStatus:async()=>({name:keyVersion,state,algorithm,publicKeySha256:fingerprint})});
  await assert.rejects(f.provider.resolvePublicKey({kid}),/C2_SIGNING_UNAVAILABLE/);assert.equal(f.count(),0);
 }
 const f=kms();await assert.rejects(f.provider.resolvePublicKey({kid:'rotated'}));
 const stop=new AbortController();stop.abort();await assert.rejects(f.provider.signMessage(Buffer.from('{}'),{kid,signal:stop.signal}));assert.equal(f.count(),0);
 const rotated=kms({getKeyVersionStatus:async()=>({name:keyVersion.replace('/1','/2'),state:'ENABLED',algorithm,publicKeySha256:fingerprint})});
 await assert.rejects(rotated.provider.resolvePublicKey({kid}));
});
test('NEW KMS response integrity, wrong signature and uncooperative provider timeout denied',async()=>{
 const base=kms();
 for(const patch of [{name:keyVersion+'/wrong'},{verifiedDigestCrc32c:false},{signatureCrc32c:'0'},{signature:Buffer.alloc(256).toString('base64'),signatureCrc32c:c2Crc32c(Buffer.alloc(256))}]){
  const f=kms({asymmetricSign:async(...x)=>({...await base.config.asymmetricSign(...x),...patch})});
  await assert.rejects(f.provider.signMessage(Buffer.from('{}'),{kid}),/C2_SIGNING_UNAVAILABLE/);
 }
 const hang=kms({getKeyVersionStatus:()=>new Promise(()=>{})});
 await assert.rejects(hang.provider.resolvePublicKey({kid}),/C2_SIGNING_UNAVAILABLE/);assert.equal(hang.count(),0);
});
test('NEW cleanup hard caps one Product and one photo without deleting shared records',()=>{
 const config={enabled:true,projectId:'oldx-staging',databaseId:'(default)',runId:'batch',actors:['synthetic-c2-batch-seller']};
 const row=path=>({path,ownerUid:config.actors[0],runId:'batch',updateTime:'2026-11-25T00:00:00Z'});
 assert.equal(prepareC2SyntheticCleanupManifest({...config,records:[row('marketplacePrivate_v1/product_one'),row('marketplacePublic_v1/product_one')]}).decision,'DRAFT_ONLY');
 for(const records of [
  [row('marketplacePrivate_v1/product_one'),row('marketplacePrivate_v1/product_two')],
  [row('marketplaceMediaAssets_v1/photo_one'),row('marketplaceMediaAssets_v1/photo_two')]]){
  const result=prepareC2SyntheticCleanupManifest({...config,records});assert.equal(result.reason,'SYNTHETIC_OBJECT_CAP');assert.equal(result.authorized,false);
 }
});


// Regression for a newly found timeout gap: AbortSignal alone cannot bound a
// trusted injected provider which ignores cancellation. No old adapter suite rerun.
test('NEW H2 HTTP adapter bounds an uncooperative mediator without leaking response',async()=>{
 const {createC2WebsiteNodeHandler}=await import('../../functions/staging-marketplace/c2-website-node-http.mjs');
 const {createServer}=await import('node:http');
 const origin='https://website.invalid';
 const server=createServer(createC2WebsiteNodeHandler({enabled:true,websiteOrigin:origin,allowedOrigins:[origin],timeoutMs:25,mediator:{fetch:()=>new Promise(()=>{})}}));
 server.listen(0,'127.0.0.1');await once(server,'listening');
 try{
  const result=await new Promise((resolve,reject)=>{
   const req=request({host:'127.0.0.1',port:server.address().port,path:'/api/staging/marketplace/owner',method:'POST',headers:{origin,'content-type':'application/json'}},res=>{
    let body='';res.on('data',x=>body+=x);res.on('end',()=>resolve({status:res.statusCode,body}));
   });req.setTimeout(1000,()=>req.destroy(Error('TEST_TIMEOUT')));req.on('error',reject);req.end('{}');
  });assert.equal(result.status,503);assert.ok(result.body.includes('ENFORCEMENT_UNAVAILABLE'));
 }finally{server.closeAllConnections();await new Promise(ok=>server.close(ok));}
});
