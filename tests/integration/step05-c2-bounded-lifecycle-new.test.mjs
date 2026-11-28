import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash,generateKeyPairSync,sign,constants} from 'node:crypto';
import {createServer} from 'node:http';
import {once} from 'node:events';
import {createC2H2MultiSignLifecyclePolicy,C2_H2_LIFECYCLE_REVIEW_SCOPE as scope} from '../../scripts/c2-h2-lifecycle-signing-status-contract.mjs';
import {createC2H2LifecycleApprovalVerifier} from '../../scripts/c2-h2-lifecycle-approval.mjs';
import {createC2H2LifecycleStageLedger} from '../../scripts/c2-h2-lifecycle-stage-ledger.mjs';
import {createStagingMarketplaceBinding} from '../../scripts/staging-marketplace-context.mjs';
import {createC2H2LifecycleKmsStatus} from '../../scripts/c2-h2-lifecycle-kms-status.mjs';
import {createC2H2IndependentKmsReaderPorts} from '../../scripts/c2-h2-independent-kms-reader-ports.mjs';
import {H2S_VERSION,H2S_VERSION_URL,H2S_PUBLIC_URL} from '../../scripts/c2-h2-independent-kms-version-status.mjs';
import {c2Crc32c} from '../../scripts/c2-kms-request-signing.mjs';
import {createC2G2G6MetadataBoundHostSourceAssembly} from '../../functions/staging-marketplace/c2-g2g6-enabled-host-source-assembly.mjs';
import {createC2H2LifecycleProofKeyResolver,createC2H2LifecycleRequestSigning} from '../../scripts/c2-h2-private-gateway-signing-composition.mjs';
import {createMarketplaceRequestProofSigner,createMarketplaceRequestProofVerifier,parseMarketplaceCanonicalProofPayload} from '../../scripts/marketplace-gateway-request-proof.mjs';
import {createGatewayAttestationVerifier} from '../../scripts/gateway-attestation.mjs';
import {createC2LifecycleStageController} from '../../functions/staging-marketplace/c2-lifecycle-stage-controller.mjs';
import {createC2FutureMediatorHost,createC2FutureGatewayHost,createC2FutureBackendHost} from '../../functions/staging-marketplace/c2-future-role-hosts.mjs';
import {prepareC2SyntheticCleanupManifest,reconcileC2SyntheticCleanup} from '../../scripts/c2-synthetic-cleanup-manifest.mjs';
import {lifecycleHttpFixture,profile,seller,buyer,site,baseTime} from './step05-lifecycle-http-fixture.mjs';
const sha=x=>createHash('sha256').update(x).digest('hex');
const h=x=>sha(JSON.stringify(x));
const approvalKey=generateKeyPairSync('rsa',{modulusLength:2048});
const proposal=()=>({v:1,purpose:scope.purpose,projectId:scope.projectId,databaseId:scope.databaseId,
 runId:'batch',gatewayEmail:scope.gatewayEmail,gatewayUid:scope.gatewayUid,keyVersion:scope.keyVersion,
 keyPublicSpkiSha256:scope.keyPublicSpkiSha256,mode:'one-server-held-kms-grant',signAttempts:1,
 startsAtMs:baseTime-100,expiresAtMs:baseTime+600000,actors:{seller,buyer},approvalSha256:h('approval'),
 runNonceSha256:h('run'),phaseNonceSha256:Object.fromEntries(scope.phases.map(x=>[x,h(x)])),
 phases:[...scope.phases],limits:{maxRequests:20,maxActors:2,maxProducts:1,maxPhotos:1},
 grantServerOnly:true,legacyOneSignTombstoneImmutable:true,durableStageLedgerRequired:true});
const policy=()=>createC2H2MultiSignLifecyclePolicy({enabled:true,proposal:proposal(),
 mode:'bounded-per-request-multisign-v1',maxSignAttempts:6});
function approval(p,patch={}) {
 const payload=Buffer.from(JSON.stringify({v:1,purpose:'oldx.c2.independent.multisign.approval.v1',
 policyDigest:h(p),mode:p.mode,maxSignAttempts:6,startsAtMs:p.startsAtMs,expiresAtMs:p.expiresAtMs}));
 return createC2H2LifecycleApprovalVerifier({enabled:true,policy:p,
 publicKeyPem:approvalKey.publicKey.export({type:'spki',format:'pem'}),
 publicKeySha256:sha(approvalKey.publicKey.export({type:'spki',format:'der'})),
 envelope:{payload:payload.toString('base64url'),signature:sign('RSA-SHA256',payload,approvalKey.privateKey).toString('base64url')},
 now:()=>baseTime,...patch});
}
function state({p=policy(),verify=approval(p)}={}) {
 // Existing SDK-shaped serialized atomic transaction double, NEVER deployable.
 const fixture=lifecycleHttpFixture({wire:()=>{throw Error('No network in unit test');}});
 const binding=createStagingMarketplaceBinding(fixture.options.runtimeOptions);
 const make=()=>createC2H2LifecycleStageLedger({enabled:true,binding,policy:p,verifyLifecycleApproval:verify,now:()=>baseTime});
 return {p,fixture,binding,make,ledger:make()};
}
const input=(p,i=0)=>({phase:p.phases[i].phase,actor:p.phases[i].actor,nonceSha256:p.phases[i].nonceSha256,
 requestSha256:h('body'),sessionSha256:h('session'),authSha256:sha('Bearer seller.test.token')});
const claim=(r,extra={})=>({reservation:r.reservation,proofSha256:h('proof'),bodyHash:h('body'),
 authHash:sha('Bearer seller.test.token'),path:'/api/staging/marketplace/save',...extra});

test('NEW future multi-sign policy and all three role factories stay default OFF',async()=>{
 assert.equal(createC2H2MultiSignLifecyclePolicy().activationAllowed,false);
 assert.equal(policy().activationAllowed,false);assert.equal(policy().maxSignAttempts,6);
 assert.equal(createC2H2MultiSignLifecyclePolicy({enabled:true,proposal:proposal(),mode:'one-grant',maxSignAttempts:1}).reviewReady,false);
 assert.equal(createC2H2LifecycleRequestSigning().ready,false);
 for(const factory of [createC2FutureMediatorHost,createC2FutureGatewayHost,createC2FutureBackendHost])
 assert.equal((await factory().fetch()).status,503);
 assert.equal((await createC2LifecycleStageController().execute()).status,503);
});
test('NEW server-held independent approval checks actual RSA signature, policy digest, pin and expiry',async()=>{
 const p=policy(),good=approval(p),args={policyDigest:h(p),policy:p};
 assert.equal((await good(args)).authorized,true);
 assert.equal((await good({...args,policyDigest:h('different')})).authorized,false);
 assert.equal((await approval(p,{publicKeySha256:h('wrong')})(args)).authorized,false);
 assert.equal((await approval(p,{now:()=>p.expiresAtMs})(args)).authorized,false);
 const fake=approval(p,{envelope:{payload:Buffer.from('{}').toString('base64url'),signature:Buffer.alloc(256).toString('base64url')}});
 assert.equal((await fake(args)).authorized,false);
});
test('NEW durable global stage ledger serializes two instances, one signature claim and ordered completion',async()=>{
 const s=state();try {
 const [a,b]=await Promise.all([s.ledger.reserve(input(s.p)),s.make().reserve(input(s.p))]);
 assert.equal([a,b].filter(x=>x.allowed).length,1);
 const r=a.allowed?a:b;
 assert.equal((await s.make().claimSign(claim(r,{bodyHash:h('wrong')}))).allowed,false);
 assert.equal((await s.ledger.claimSign(claim(r))).allowed,true);
 assert.equal((await s.make().claimSign(claim(r))).allowed,false);
 const backendClaim={proofSha256:h('proof'),bodyHash:h('body'),authHash:sha('Bearer seller.test.token'),path:'/api/staging/marketplace/save'};
 assert.equal((await s.make().claimBackend({...backendClaim,proofSha256:h('tampered')})).allowed,false);
 assert.equal((await s.make().claimBackend(backendClaim)).allowed,true);
 assert.equal((await s.ledger.claimBackend(backendClaim)).allowed,false);
 assert.equal((await s.ledger.finish({reservation:r.reservation,outcome:'CONFIRMED',responseSha256:h('200')})).allowed,true);
 assert.equal((await s.make().reserve(input(s.p))).allowed,false);
 assert.equal((await s.make().reserve(input(s.p,2))).allowed,false);
 const changed=proposal();changed.runId='rotated';changed.actors={seller:'synthetic-c2-rotated-seller',buyer:'synthetic-c2-rotated-buyer'};
 const p2=createC2H2MultiSignLifecyclePolicy({enabled:true,proposal:changed,mode:s.p.mode,maxSignAttempts:6});
 const other=createC2H2LifecycleStageLedger({enabled:true,binding:s.binding,policy:p2,verifyLifecycleApproval:approval(p2),now:()=>baseTime});
 assert.equal(other.recordId,s.ledger.recordId);
 assert.equal((await other.reserve(input(p2))).allowed,false);
 const row=s.fixture.f.get('marketplaceRateLimits_v1',s.ledger.recordId);
 assert.equal(row.signAttempts,1);assert.equal('expiresAtMs' in row,false);
 }finally{s.fixture.integration.destroy();}
});
test('NEW ambiguous transaction or signing outcome never permits retry across instances',async()=>{
 const s=state();try{
 s.fixture.f.failCommit=true;
 await assert.rejects(s.ledger.reserve(input(s.p)),/LEDGER_UNAVAILABLE/);
 s.fixture.f.failCommit=false;
 const r=await s.ledger.reserve(input(s.p));assert.equal(r.allowed,true);
 assert.equal((await s.ledger.claimSign(claim(r))).allowed,true);
 assert.equal((await s.ledger.finish({reservation:r.reservation,outcome:'UNKNOWN',responseSha256:h('lost-KMS')})).allowed,true);
 assert.equal((await s.make().reserve(input(s.p))).allowed,false);
 assert.equal((await s.make().claimSign(claim(r))).allowed,false);
 }finally{s.fixture.integration.destroy();}
});
test('NEW ledger rejects wrong actor/nonce and forged approval providers',async()=>{
 const s=state();try{
 for(const patch of [{actor:buyer},{nonceSha256:h('foreign')},{authSha256:'bad'}])
 assert.equal((await s.ledger.reserve({...input(s.p),...patch})).allowed,false);
 for(const verify of [async()=>({authorized:true}),()=>new Promise(()=>{})])
 assert.throws(()=>createC2H2LifecycleStageLedger({enabled:true,binding:s.binding,
 policy:s.p,verifyLifecycleApproval:verify}),/APPROVAL_UNVERIFIED/);
 assert.equal(s.fixture.f.commits,0);
 }finally{s.fixture.integration.destroy();}
});
test('NEW canonical proof retains real per-request RSA binding and rejects tamper, replay, account switch',async()=>{
 const key=generateKeyPairSync('rsa',{modulusLength:2048}),used=new Set();
 const signer=createMarketplaceRequestProofSigner({enabled:true,kid:'new-local',now:()=>baseTime,
 signMessage:bytes=>sign('RSA-SHA256',bytes,key.privateKey)});
 const verifier=createMarketplaceRequestProofVerifier({enabled:true,now:()=>baseTime,
 resolvePublicKey:()=>key.publicKey,authorizeBeforeNonce:async info=>{
 assert.equal(info.proofSha256,sha(bytes));assert.equal(info.bodyHash,sha(args.body));return true;
 },consumeNonce:async({nonceHash})=>{
 if(used.has(nonceHash))return {allowed:false};used.add(nonceHash);return {allowed:true};}});
 const args={method:'POST',path:'/api/staging/marketplace/save',body:Buffer.from('{}'),
 authorization:'Bearer seller.test.token',attestationToken:'aaaa.bbbb.cccccccccccccccccccccc'};
 const proof=await signer(args),bytes=Buffer.from(proof.split('.')[0],'base64url');
 assert.equal(parseMarketplaceCanonicalProofPayload(bytes).bodyHash,sha(args.body));
 assert.equal(parseMarketplaceCanonicalProofPayload(Buffer.concat([bytes,Buffer.from(' ')])),null);
 assert.equal(await verifier({...args,proof,authorization:'Bearer buyer.test.token'}),false);
 assert.equal(await verifier({...args,proof,body:Buffer.from('{"tamper":true}')}),false);
 assert.equal(await verifier({...args,proof}),true);assert.equal(await verifier({...args,proof}),false);
 const bits=proof.split('.');bits[1]=Buffer.alloc(256).toString('base64url');
 assert.equal(await verifier({...args,proof:bits.join('.')}),false);
});
test('NEW signed workload assertion rejects wrong audience even with a valid local RSA signature',async()=>{
 const key=generateKeyPairSync('rsa',{modulusLength:2048});
 const mint=aud=>{const enc=x=>Buffer.from(JSON.stringify(x)).toString('base64url');
 const data=enc({alg:'RS256',kid:'test'})+'.'+enc({iss:'https://accounts.google.com',aud,
 sub:scope.gatewayUid,email:scope.gatewayEmail,email_verified:true,iat:baseTime/1000,exp:baseTime/1000+3600});
 return data+'.'+sign('RSA-SHA256',Buffer.from(data),key.privateKey).toString('base64url');};
 const audience='https://backend.region.run.app',a='urn:oldx:new:test';
 const verifier=createGatewayAttestationVerifier({enabled:true,identityType:'google-service-account',
 issuer:'https://accounts.google.com',attestationAudience:a,iamAudience:audience,
 expectedPrincipal:scope.gatewayEmail,expectedSubject:scope.gatewayUid,resolvePublicKey:()=>key.publicKey,now:()=>baseTime});
 for(const [aud,allowed] of [[a,true],['urn:foreign',false]]) {
 const result=await verifier(new Request(audience,{headers:{'x-oldx-gateway-attestation':mint(aud)}}),{audience});
 assert.equal(result?.verified===true,allowed);
 }
});
test('NEW independent reader uses only exact bounded GETs, separate authority and durable budget',async()=>{
 const principal='independent-reader@oldx-staging.iam.gserviceaccount.com',uid='333';
 let calls=0,budgets=0;
 const options={enabled:true,readerPrincipal:principal,readerUid:uid,now:()=>baseTime,
 verifyReaderAuthority:async()=>({authorized:true,principal,uid,keyVersion:H2S_VERSION,expiresAtMs:baseTime+10000}),
 consumeDurableReadBudget:async()=>({allowed:++budgets<=2}),
 getReaderCredential:async()=>({principal,uid,source:'cloud-run-metadata',accessToken:'a'.repeat(80),expiresAtMs:baseTime+30000}),
 fetchReader:async(url,init)=>{calls++;assert.ok([H2S_VERSION_URL,H2S_PUBLIC_URL].includes(url));
 assert.equal(init.method,'GET');assert.equal(init.redirect,'error');assert.equal(init.credentials,'omit');
 return Response.json({name:H2S_VERSION,state:'DISABLED'});}};
 const x=createC2H2IndependentKmsReaderPorts(options);assert.equal(x.ready,true);
 assert.equal((await x.readExactVersion({name:H2S_VERSION,url:H2S_VERSION_URL})).state,'DISABLED');
 await x.readExactPublicKey({name:H2S_VERSION,url:H2S_PUBLIC_URL});
 await assert.rejects(x.readExactVersion({name:H2S_VERSION,url:H2S_VERSION_URL}));
 await assert.rejects(x.readExactVersion({name:H2S_VERSION,url:'https://attacker.invalid'}));
 assert.equal(calls,2);
 assert.equal(createC2H2IndependentKmsReaderPorts({...options,readerPrincipal:scope.gatewayEmail}).ready,false);
 assert.equal(createC2H2IndependentKmsReaderPorts({...options,readerUid:scope.gatewayUid}).ready,false);
 const denied=createC2H2IndependentKmsReaderPorts({...options,verifyReaderAuthority:async()=>({authorized:false})});
 await assert.rejects(denied.readExactVersion({name:H2S_VERSION,url:H2S_VERSION_URL}));assert.equal(calls,2);
 const fail=createC2H2IndependentKmsReaderPorts({...options,consumeDurableReadBudget:async()=>({allowed:true}),
 fetchReader:async()=>{calls++;return new Response('',{status:403});}});
 await assert.rejects(fail.readExactVersion({name:H2S_VERSION,url:H2S_VERSION_URL}));assert.equal(calls,3);
});
async function httpWires() {
 const servers=new Map(),counts=new Map();
 return {counts,async wire(origin,target,request) {
 if(!servers.has(origin)){
 const server=createServer(async(req,res)=>{try{
 const chunks=[];for await(const c of req)chunks.push(c);
 const out=await target.fetch(new Request(origin+req.url,{method:req.method,headers:req.headers,
 body:Buffer.concat(chunks),duplex:'half'}));
 res.writeHead(out.status,Object.fromEntries(out.headers));res.end(Buffer.from(await out.arrayBuffer()));
 }catch{res.writeHead(500);res.end();}});
 server.listen(0,'127.0.0.1');await once(server,'listening');servers.set(origin,server);
 }
 counts.set(origin,(counts.get(origin)??0)+1);
 const server=servers.get(origin);
 return fetch('http://127.0.0.1:'+server.address().port+new URL(request.url).pathname,{
 method:request.method,headers:request.headers,body:await request.arrayBuffer(),signal:request.signal,redirect:'error'});
 },async close(){for(const s of servers.values()){s.closeAllConnections();await new Promise(r=>s.close(r));}}};
}
test('NEW six-stage Seller-Buyer journey uses three real localhost HTTP hops, crypto proofs and atomic stage ledger',async()=>{
 const wires=await httpWires(),p=policy(),durable=state({p});let ledger=durable.ledger,active,current={uid:seller,sessionId:'seller-session'},signs=0;
 const f=lifecycleHttpFixture({wire:wires.wire,lifecycle:{policy:p,ledger},onSign:async(bytes)=>{
 const proof=parseMarketplaceCanonicalProofPayload(bytes);assert.ok(proof);
 assert.equal((await ledger.claimSign({reservation:active,proofSha256:sha(bytes),bodyHash:proof.bodyHash,
 authHash:proof.authHash,path:proof.path})).allowed,true);signs++;
 }});
 const binding=createStagingMarketplaceBinding(f.options.runtimeOptions);

 const controller=createC2LifecycleStageController({enabled:true,policy:p,ledger,adminAuth:f.adminAuth,
 websiteOrigin:site,getCurrentSession:()=>current,now:f.now,dispatch:(request,ctx)=>{
 active=ctx.reservation;return wires.wire(site,f.mediator,request);
 }});
 const id='c2_batch_product';
 const body=(i,photo)=>i===2?{kind:'product',limit:1,category:'',storeId:null,cursor:null}:
 i===3?{kind:'product',id}:{kind:'product',requestId:'lifecycle_'+i,id:i===0?null:id,
 expectedRevision:i===0?0:i===1?1:i===4?2:3,
 publication:i===1?'publish':i===5?'withdraw':'draft',profile:photo??profile};
 try {
 assert.equal(controller.ready,true);let photo;
 for(let i=0;i<6;i++){
 if(i===1)photo=f.attach(id);
 current={uid:i===2||i===3?buyer:seller,sessionId:i===2||i===3?'buyer-session':'seller-session'};
 const token=current.uid+'.synthetic.token',pub=i===2||i===3;
 const request=new Request(site+'/api/staging/marketplace/'+(i===2?'list':i===3?'detail':'save'),
 {method:'POST',headers:{origin:site,'content-type':'application/json',...pub?{}:{authorization:'Bearer '+token}},body:JSON.stringify(body(i,photo))});
 const response=await controller.execute({phase:p.phases[i].phase,sessionToken:token,sessionId:current.sessionId,request});
 assert.equal(response.status,200,JSON.stringify(f.trace));const result=await response.json();assert.equal(result.ok,true,JSON.stringify(result));
 if(i===2)assert.doesNotMatch(JSON.stringify(result),/ownerUid|privateContact|processedDigest/);
 }
 assert.equal(signs,6);assert.equal(wires.counts.size,3);
 assert.ok([...wires.counts.values()].every(x=>x===6));
 const row=durable.fixture.f.get('marketplaceRateLimits_v1',ledger.recordId);assert.equal(row.state,'COMPLETE');assert.equal(row.signAttempts,6);
 assert.equal(f.f.get('marketplacePublic_v1','product_'+id),null);
 // Completion cannot be replayed from a fresh ledger object.
 const again=durable.make();
 assert.equal((await again.reserve(input(p))).allowed,false);
 }finally{f.integration.destroy();durable.fixture.integration.destroy();await wires.close();}
});
test('NEW stage controller refuses wrong actor, account switch, image ownership and missing durable authority',async()=>{
 const s=state();let dispatched=0,current={uid:buyer,sessionId:'session'},clock=baseTime;
 const controller=createC2LifecycleStageController({enabled:true,policy:s.p,ledger:s.ledger,adminAuth:s.fixture.adminAuth,
 websiteOrigin:site,getCurrentSession:()=>current,now:()=>clock,dispatch:()=>{dispatched++;throw Error('must not run');}});
 const make=()=>new Request(site+'/api/staging/marketplace/save',{method:'POST',
 headers:{origin:site,'content-type':'application/json',authorization:'Bearer '+seller+'.synthetic.token'},
 body:JSON.stringify({kind:'product',id:null,publication:'draft'})});
 try {
 assert.equal((await controller.execute({phase:'seller-save',sessionToken:seller+'.synthetic.token',sessionId:'session',request:make()})).status,403);
 current={uid:seller,sessionId:'session'};const old=s.fixture.adminAuth.verifyIdToken;
 s.fixture.adminAuth.verifyIdToken=async(...args)=>{current={uid:buyer,sessionId:'other'};return old(...args);};
 assert.equal((await controller.execute({phase:'seller-save',sessionToken:seller+'.synthetic.token',sessionId:'session',request:make()})).status,403);
 clock=s.p.expiresAtMs;assert.equal((await controller.execute({phase:'seller-save',sessionToken:seller+'.synthetic.token',sessionId:'session',request:make()})).status,503);
 assert.equal(dispatched,0);assert.equal(s.fixture.f.commits,0);
 const fakePolicy=Object.freeze({...s.p});
 assert.throws(()=>createC2H2LifecycleStageLedger({enabled:true,binding:s.binding,policy:fakePolicy,verifyLifecycleApproval:approval(s.p)}));
 // Actual pin cannot be replaced by generated test PEM to unlock production signer.
 assert.equal(createC2H2LifecycleRequestSigning({enabled:true,policy:s.p,ledger:s.ledger,getStageContext:()=>({}),
 publicKeyPem:approvalKey.publicKey.export({type:'spki',format:'pem'}),getTrustedKeyVersionStatus:()=>{throw Error('must not run');},
 asymmetricSign:()=>{throw Error('must not run');}}).ready,false);
 }finally{s.fixture.integration.destroy();}
});
test('NEW release photo-owner guard, quota and cleanup revision drift stay enforced',async()=>{
 const wires=await httpWires(),f=lifecycleHttpFixture({wire:wires.wire});
 try {
 f.login(seller);await f.model.save(profile);const id=f.model.snapshot().owner.id;
 const photo=f.attach(id);f.f.seed('marketplaceMediaAssets_v1','synthetic_photo_1234567890',{
 ...f.f.get('marketplaceMediaAssets_v1','synthetic_photo_1234567890'),ownerUid:buyer});
 await f.model.save(photo,'publish');assert.notEqual(f.model.snapshot().command.status,'saved');
 f.denyBudget();await f.model.loadOwner(id);assert.equal(f.model.snapshot().owner,null);
 const manifest=prepareC2SyntheticCleanupManifest({enabled:true,projectId:'oldx-staging',databaseId:'(default)',
 runId:'batch',actors:[seller],records:[{path:'marketplacePrivate_v1/product_'+id,ownerUid:seller,runId:'batch',updateTime:'2026-11-28T00:00:00Z'}]});
 assert.equal(reconcileC2SyntheticCleanup({enabled:true,manifest,readbacks:[{...manifest.records[0],
 updateTime:'2026-11-28T00:00:01Z',exists:true,dependencies:[]}]}).decision,'STOP');
 }finally{f.integration.destroy();await wires.close();}
});

test('NEW lifecycle status GET attempts are durable per stage, ordered and never reset by new providers',async()=>{
 const s=state();try{
 const r=await s.ledger.reserve(input(s.p));await s.ledger.claimSign(claim(r));
 const read=(op,ledger=s.ledger)=>ledger.consumeStatusRead({reservation:r.reservation,operation:op});
 assert.equal((await read('sign-public')).allowed,false);
 const pair=await Promise.all([read('sign-version'),read('sign-version',s.make())]);
 assert.equal(pair.filter(x=>x.allowed).length,1);
 assert.equal((await read('sign-public')).allowed,true);
 assert.equal((await read('verify-version')).allowed,true);
 assert.equal((await read('verify-public')).allowed,true);
 for(const op of ['sign-version','sign-public','verify-version','verify-public'])
 assert.equal((await read(op,s.make())).allowed,false);
 assert.equal(s.fixture.f.get('marketplaceRateLimits_v1',s.ledger.recordId).statusReads,4);
 assert.equal(createC2H2LifecycleKmsStatus().ready,false);
 }finally{s.fixture.integration.destroy();}
});
test('NEW changed release exposes immutable identity/image bindings for all three hosts',()=>{
 const f=lifecycleHttpFixture({wire:()=>{throw Error('must not run');}});
 try {
 assert.equal(f.release.hostBindings.principals.backend,f.release.runtimePrincipal);
 assert.equal(f.release.hostBindings.images.backend,f.release.runtimeImage);
 assert.equal(Object.keys(f.release.hostBindings.images).length,3);
 assert.throws(()=>{f.release.hostBindings.images.mediator='wrong';});
 }finally{f.integration.destroy();}
});
test('NEW unknown HTTP mutation result remains quarantined and cannot be retried by another instance',async()=>{
 const s=state();let calls=0;
 const controller=createC2LifecycleStageController({enabled:true,policy:s.p,ledger:s.ledger,adminAuth:s.fixture.adminAuth,
 websiteOrigin:site,getCurrentSession:()=>({uid:seller,sessionId:'fixed'}),now:()=>baseTime,
 dispatch:async()=>{calls++;throw Error('AMBIGUOUS_MUTATION');}});
 const make=()=>({phase:'seller-save',sessionToken:seller+'.synthetic.token',sessionId:'fixed',
 request:new Request(site+'/api/staging/marketplace/save',{method:'POST',headers:{origin:site,'content-type':'application/json',
 authorization:'Bearer '+seller+'.synthetic.token'},body:JSON.stringify({kind:'product',id:null,publication:'draft'})})});
 try {
 assert.equal((await controller.execute(make())).status,202);
 assert.equal((await controller.execute(make())).status,409);assert.equal(calls,1);
 assert.equal(s.fixture.f.get('marketplaceRateLimits_v1',s.ledger.recordId).state,'PENDING');
 }finally{s.fixture.integration.destroy();}
});

test('NEW independent lifecycle status refuses substituted PEM and cannot renew its consumed GET budget',async()=>{
 const s=state();let calls=0;
 try {
 const r=await s.ledger.reserve(input(s.p));await s.ledger.claimSign(claim(r));
 const principal='independent-reader@oldx-staging.iam.gserviceaccount.com',uid='333';
 const pem=approvalKey.publicKey.export({type:'spki',format:'pem'});
 const readerOptions={readerPrincipal:principal,readerUid:uid,
 verifyReaderAuthority:async()=>({authorized:true,principal,uid,keyVersion:H2S_VERSION,expiresAtMs:baseTime+60000}),
 getReaderCredential:async()=>({principal,uid,source:'cloud-run-metadata',accessToken:'a'.repeat(80),expiresAtMs:baseTime+30000}),
 fetchReader:async url=>{calls++;return Response.json(url===H2S_VERSION_URL?
 {name:H2S_VERSION,state:'ENABLED',algorithm:'RSA_SIGN_PKCS1_2048_SHA256',protectionLevel:'SOFTWARE'}:
 {name:H2S_VERSION,pem,pemCrc32c:c2Crc32c(Buffer.from(pem)),algorithm:'RSA_SIGN_PKCS1_2048_SHA256'});}};
 const make=()=>createC2H2LifecycleKmsStatus({enabled:true,policy:s.p,ledger:s.make(),readerOptions,
 getStageContext:()=>({usage:'sign',reservation:r.reservation}),now:()=>baseTime});
 await assert.rejects(make().getTrustedKeyVersionStatus({name:H2S_VERSION}));
 assert.equal(calls,2); // Wrong local PEM cannot match actual historical pin.
 await assert.rejects(make().getTrustedKeyVersionStatus({name:H2S_VERSION}));
 assert.equal(calls,2); // New provider cannot reset the shared read budget.
 }finally{s.fixture.integration.destroy();}
});
test('NEW assembly rejects nested getter host facts and forged lifecycle signer without executing providers',()=>{
 let calls=0;
 const facts={mediator:{},gateway:{},backend:{}};
 Object.defineProperty(facts.mediator,'principal',{get(){calls++;return 'forged';}});
 const result=createC2G2G6MetadataBoundHostSourceAssembly({enabled:true,hostFacts:facts,
 websiteOptions:{},gatewayHostOptions:{websiteIdentity:{},gatewayOptions:{},lifecycleRequestSigning:{ready:true}},
 backendOptions:{googleIdentity:{}},metadataIdentityOptions:{}});
 assert.equal(result.sourceComposed,false);assert.equal(calls,0);
});

test('NEW reader deadline bounds a transport ignoring cancellation without retry',async()=>{
 let calls=0;const principal='independent-reader@oldx-staging.iam.gserviceaccount.com',uid='333';
 const reader=createC2H2IndependentKmsReaderPorts({enabled:true,readerPrincipal:principal,readerUid:uid,now:()=>baseTime,
 verifyReaderAuthority:async()=>({authorized:true,principal,uid,keyVersion:H2S_VERSION,expiresAtMs:baseTime+60000}),
 consumeDurableReadBudget:async()=>({allowed:true}),
 getReaderCredential:async()=>({principal,uid,source:'cloud-run-metadata',accessToken:'a'.repeat(80),expiresAtMs:baseTime+30000}),
 fetchReader:()=>{calls++;return new Promise(()=>{});}});
 await assert.rejects(reader.readExactVersion({name:H2S_VERSION,url:H2S_VERSION_URL}),/READER_UNAVAILABLE/);
 assert.equal(calls,1);
});

test('NEW backend key resolver is OFF without the actual pin and never acquires signing credentials',()=>{
 let calls=0;assert.equal(createC2H2LifecycleProofKeyResolver(),null);
 assert.equal(createC2H2LifecycleProofKeyResolver({enabled:true,policy:policy(),
 publicKeyPem:approvalKey.publicKey.export({type:'spki',format:'pem'}),
 getTrustedKeyVersionStatus:()=>{calls++;throw Error('must not run');}}),null);
 assert.equal(calls,0);
});
