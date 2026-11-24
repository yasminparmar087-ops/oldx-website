import test from 'node:test';
import assert from 'node:assert/strict';
import {generateKeyPairSync,sign,constants,createHash} from 'node:crypto';
import {fakeFirestoreSdk} from './fake-firestore-sdk.mjs';
import {createStep05Gateway,createStep05Backend} from '../../functions/staging-marketplace/secure-product-pipeline.mjs';
import {createFirebaseMarketplaceHttpIntegration} from '../../features/marketplace/firebase-integration.mjs';
import {createMarketplaceHttpTransport} from '../../features/marketplace/http-transport.mjs';
import {createMarketplacePublicClient} from '../../features/marketplace/public-read-client.mjs';
import {createProductIntegration} from '../../features/marketplace/product-integration.mjs';
import {createMarketplaceRequestProofSigner,createMarketplaceRequestProofVerifier,MARKETPLACE_REQUEST_PROOF_HEADER as proofHeader} from '../../scripts/marketplace-gateway-request-proof.mjs';
import {createProofBoundGatewayHop,createProofBoundBackendHop} from '../../scripts/marketplace-proof-bound-hop.mjs';
import {consumeAtomicMarketplaceReplayNonce} from '../../scripts/staging-marketplace-replay-nonce.mjs';
import {STAGING_MARKETPLACE_COLLECTIONS as c,STAGING_MEDIA_COLLECTIONS as m} from '../../scripts/staging-marketplace-context.mjs';
const identityKey=generateKeyPairSync('rsa',{modulusLength:2048}),intentKey=generateKeyPairSync('rsa',{modulusLength:2048});
const base='https://private-staging.invalid',site='https://ui-staging.invalid',principal='gateway-only@oldx-staging.iam.gserviceaccount.com',issuer='https://accounts.google.com',subject='123456789012345678901',assertionAudience='urn:oldx:test:attestation';
const clock=1800000000000,now=()=>clock,path=op=>'/api/staging/marketplace/'+op;
const profile={title:'ગુજરાતી हिन्दी',description:'Synthetic',category:'cars',locationLabel:'Sample',basePrice:1,isSold:false,storeId:null,photos:[]};
function assertion(patch={}){
 const b64=v=>Buffer.from(JSON.stringify(v)).toString('base64url'),input=b64({alg:'RS256',kid:'google-fixture',typ:'JWT'})+'.'+b64({iss:issuer,aud:assertionAudience,sub:subject,email:principal,email_verified:true,iat:clock/1000,exp:clock/1000+3600,...patch});
 return input+'.'+sign('RSA-SHA256',Buffer.from(input),{key:identityKey.privateKey,padding:constants.RSA_PKCS1_PADDING}).toString('base64url');
}
function fixture({guestLimit=20,actorLimit=30,media=true}={}){
 const f=fakeFirestoreSdk();let revoked=false,identityPatch={},wrongSigner=false,lose=false,mutate=null,waitReply=null,captureOnly=false,keyCalls=0,authCalls=0;
 const wire=[];
 function collection(name){
  const constraints=[];let fields;
  const query={doc:id=>({...f.sdk.doc(f.db,name,id),get:async()=>{const s=await f.sdk.getDocFromServer(f.sdk.doc(f.db,name,id));return {exists:s.exists(),data:s.data};}}),select(...v){fields=v;return query;},where(...v){constraints.push(f.sdk.where(...v));return query;},orderBy(...v){constraints.push(f.sdk.orderBy(...v));return query;},startAfter(v){constraints.push(f.sdk.startAfter(v));return query;},limit(v){constraints.push(f.sdk.limit(v));return query;},async get(){
   const s=await f.sdk.getDocsFromServer(f.sdk.query(f.sdk.collection(f.db,name),...constraints));
   return {docs:s.docs.map(d=>({id:d.id,data:()=>Object.fromEntries(Object.entries(d.data()).filter(([k])=>!fields||fields.includes(k)))}))};
  }};return query;
 }
 const adminFirestore={projectId:'oldx-staging',databaseId:'(default)',collection,runTransaction:(work,opts)=>f.sdk.runTransaction(f.db,tx=>work({get:async ref=>{const s=await tx.get(ref);return {exists:s.exists(),data:s.data};},set:(...a)=>tx.set(...a),delete:(...a)=>tx.delete(...a)}),opts)};
 const adminAuth={app:{options:{projectId:'oldx-staging'}},verifyIdToken:async(token,checkRevoked)=>{
  authCalls++;assert.equal(checkRevoked,true);if(revoked||!['seller.test.token','buyer.test.token'].includes(token))throw Error('Revoked/invalid synthetic user');
  const uid=token.split('.')[0];return {uid,sub:uid,aud:'oldx-staging',iss:'https://securetoken.google.com/oldx-staging',iat:clock/1000,exp:clock/1000+3600};
 }};
 for(const uid of ['seller','buyer'])f.seed(c.actors,uid,{uid,canWrite:true,canPublish:true,suspended:false});
 f.seed(c.generations,'current',{value:0});f.seed(m.generations,'current',{value:0});
 const googleIdentity={identityType:'google-service-account',issuer,attestationAudience:assertionAudience,expectedSubject:subject,fetchRequest:async(url,init)=>{
  keyCalls++;assert.equal(url,'https://www.googleapis.com/oauth2/v3/certs');assert.equal(init.redirect,'error');
  return Response.json({keys:[{...identityKey.publicKey.export({format:'jwk'}),alg:'RS256',kid:'google-fixture',use:'sig'}]},{headers:{'cache-control':'max-age=300'}});
 }};
 const backendOptions={enabled:true,audience:base,gatewayServiceAccount:principal,googleIdentity,
  requestVerification:{resolvePublicKey:({kid})=>kid==='intent-fixture'?intentKey.publicKey:null},runtimeOptions:{projectId:'oldx-staging',deploymentEnvironment:'preview',adminFirestore,adminAuth,FieldValue:{serverTimestamp:f.sdk.serverTimestamp},ratePolicy:{windowMs:60000,actorLimit,globalLimit:100}},guestPolicy:{windowMs:60000,guestLimit,globalLimit:100},cursorKey:new Uint8Array(32).fill(44),now};
 if(!media)backendOptions.runtimeOptions.createMediaBindings=()=>null;
 const backend=createStep05Backend(backendOptions);
 const gatewayOptions={enabled:true,backendOrigin:base,gatewayServiceAccount:principal,allowedOrigins:[site],attestationAudience:assertionAudience,now,
  getInvokerCredential:()=>({type:'cloud-run-iam-id-token',token:'iam.transport.signature',principal,audience:base,expiresAtMs:clock+60000}),
  getGatewayAttestation:()=>({token:assertion(identityPatch),principal,audience:assertionAudience,expiresAtMs:clock+60000}),
  requestSigning:{kid:'intent-fixture',signMessage:bytes=>sign('RSA-SHA256',bytes,{key:wrongSigner?identityKey.privateKey:intentKey.privateKey,padding:constants.RSA_PKCS1_PADDING})},
  fetchBackend:async(url,init)=>{
   const h=new Headers(init.headers);assert.equal(h.get('x-serverless-authorization'),'Bearer iam.transport.signature');h.set('x-serverless-authorization','Bearer iam.payload.');
   const item={url,headers:h,body:new Uint8Array(init.body)};wire.push(item);
   if(captureOnly)return Response.json({ok:false,error:{code:'UNAVAILABLE'}},{status:503});
   if(mutate)mutate(item);
   const response=await backend.fetch(new Request(url,{method:'POST',headers:item.headers,body:item.body}));
   if(lose&&url.endsWith('/save')){lose=false;throw Error('Lost committed response');}
   if(waitReply)await waitReply;
   return response;
  }};
 const gateway=createStep05Gateway(gatewayOptions);
 const browserFetch=(url,init)=>gateway.fetch(new Request(url,{...init,headers:{...init.headers,origin:site}}));
 const transport=createMarketplaceHttpTransport({enabled:true,origin:site,fetchRequest:browserFetch});
 const reads=createMarketplacePublicClient({enabled:true,sendRead:transport.sendRead});
 let observer,session,n=0;const user=uid=>({uid,getIdToken:async()=>uid+'.test.token'});
 const auth={app:{options:{projectId:'oldx-staging'}},currentUser:user('seller'),onIdTokenChanged:fn=>{observer=fn;return ()=>{};}};
 const bridge=createFirebaseMarketplaceHttpIntegration({enabled:true,auth,origin:site,fetchRequest:browserFetch,makeSessionId:()=> 'session-'+(++n),onSession:s=>session=s});
 observer(auth.currentUser);
 let reqNo=0;const ui=createProductIntegration({enabled:true,ports:bridge.product,makeRequestId:()=> 'integrated-'+(++reqNo)});ui.setSession(session);
 const send=(op,body,token='seller.test.token',extra={})=>gateway.fetch(new Request(site+path(op),{method:'POST',headers:{origin:site,'content-type':'application/json',...(token?{authorization:'Bearer '+token}:{}),...extra},body:typeof body==='string'?body:JSON.stringify(body)}));
 const seedPublic=id=>{
  const {photos,...fields}=profile,row={id,kind:'product',revision:1,...fields};
  f.seed(c.publicViews,'product_'+id,row);f.seed(c.privateRecords,'product_'+id,{id,kind:'product',revision:1,ownerUid:'seller',published:true,publicationRevision:1,publicProfile:row,profile,privateContact:'never-public'});
 };
 return {f,wire,backend,backendOptions,gateway,gatewayOptions,transport,reads,ui,bridge,auth,send,seedPublic,
  revoke:()=>revoked=true,badIdentity:()=>identityPatch={sub:'999'},badSigner:()=>wrongSigner=true,
  lose:()=>lose=true,mutate:fn=>mutate=fn,capture:()=>captureOnly=true,hold:p=>waitReply=p,
  async switch(uid){auth.currentUser=uid?user(uid):null;observer(auth.currentUser);ui.setSession(session);},
  get keyCalls(){return keyCalls;},get authCalls(){return authCalls;}};
}
const save={kind:'product',id:null,expectedRevision:0,publication:'draft',profile,requestId:'same-save'};
test('complete source pipeline saves/reloads/edits/withdraws/archives while publication stays OFF',async()=>{
 const x=fixture();await x.ui.save(profile);assert.equal(x.ui.snapshot().command.status,'saved');const id=x.ui.snapshot().owner.id;
 await x.ui.loadOwner(id);assert.equal(x.ui.snapshot().statuses.owner,'ready');
 await x.ui.save({...profile,title:'Edited ગુજરાતી'});assert.equal(x.ui.snapshot().owner.revision,2);
 assert.equal((await x.reads.detail({kind:'product',id})).ok,false);
 await x.ui.save(profile,'publish');assert.equal(x.ui.snapshot().command.status,'unavailable');assert.equal(x.f.get(c.privateRecords,'product_'+id).published,false);
 await x.ui.save(profile,'withdraw');assert.equal(x.ui.snapshot().command.status,'saved');
 await x.ui.archive();assert.equal(x.ui.snapshot().command.status,'saved');assert.equal(x.f.get(c.privateRecords,'product_'+id).archived,true);
 assert.equal(x.keyCalls,1);assert.ok(x.wire.every(w=>w.headers.has(proofHeader)));
 const missing=fixture({media:false});await missing.ui.save(profile);const own=missing.ui.snapshot().owner;
 await missing.ui.archive();assert.equal(missing.ui.snapshot().command.status,'unavailable');assert.notEqual(missing.f.get(c.privateRecords,'product_'+own.id).archived,true);
});
test('lost commit acknowledgement retries identical requestId with fresh proof/nonce and creates one Product',async()=>{
 const x=fixture();x.lose();await x.ui.save(profile);assert.equal(x.ui.snapshot().command.status,'unknown');
 await x.ui.retry();assert.equal(x.ui.snapshot().command.status,'saved');
 assert.deepEqual(x.wire[0].body,x.wire[1].body);assert.notEqual(x.wire[0].headers.get(proofHeader),x.wire[1].headers.get(proofHeader));
 assert.equal([...x.f.snapshot()].filter(([k])=>k.startsWith(c.privateRecords+'/')).length,1);
 const snap=x.f.snapshot(),w=x.wire[0];assert.equal((await x.backend.fetch(new Request(w.url,{method:'POST',headers:w.headers,body:w.body}))).status,403);assert.deepEqual(x.f.snapshot(),snap);
});
test('two backend instances share native-shaped atomic replay storage, accepting a signed attempt once',async()=>{
 const x=fixture();x.capture();await x.send('save',save);const w=x.wire[0],other=createStep05Backend(x.backendOptions);
 const response=await Promise.all([x.backend,other].map(b=>b.fetch(new Request(w.url,{method:'POST',headers:w.headers,body:w.body}))));
 assert.deepEqual(response.map(r=>r.status).sort(),[200,403]);assert.equal([...x.f.snapshot()].filter(([k])=>k.startsWith(c.privateRecords+'/')).length,1);
});
test('cryptographic identity/intent, revoked user and exact-byte binding deny BEFORE any store write',async()=>{
 for(const scenario of ['identity','intent','revoked','bytes']){
  const x=fixture(),snap=x.f.snapshot();
  if(scenario==='identity')x.badIdentity();if(scenario==='intent')x.badSigner();if(scenario==='revoked')x.revoke();
  if(scenario==='bytes')x.mutate(w=>{w.body=Buffer.concat([w.body,Buffer.from(' ')]);});
  assert.equal((await x.send('save',save)).status,403,scenario);assert.deepEqual(x.f.snapshot(),snap);
  if(scenario==='identity'||scenario==='intent')assert.equal(x.authCalls,0);
 }
 const x=fixture(),snap=x.f.snapshot();
 for(const extra of [{[proofHeader]:'forged.proof'},{'x-oldx-gateway-attestation':assertion()},{'x-serverless-authorization':'Bearer iam.transport.signature'}])assert.equal((await x.send('save',save,'seller.test.token',extra)).status,403);
 assert.equal((await x.send('save',save,null)).status,401);assert.deepEqual(x.f.snapshot(),snap);assert.equal(x.wire.length,0);
});
test('public guest DTOs, signed cursors and aggregate quota traverse the authenticated proof pipeline',async()=>{
 const x=fixture();x.seedPublic('a');x.seedPublic('b');
 const input={kind:'product',limit:1,category:'cars',storeId:null,cursor:null},first=await x.reads.list(input);
 assert.equal(first.ok,true);assert.equal(first.items[0].id,'a');assert.ok(first.nextCursor);
 assert.equal((await x.reads.list({...input,cursor:first.nextCursor})).items[0].id,'b');
 assert.equal((await x.reads.list({...input,category:'',cursor:first.nextCursor})).code,'CURSOR_INVALID');
 assert.doesNotMatch(JSON.stringify(first),/ownerUid|privateContact|never-public|photos/);
 const y=fixture({guestLimit:1});assert.equal((await y.reads.list(input)).ok,true);assert.equal((await y.reads.list(input)).code,'RATE_LIMITED');
 assert.ok(y.wire.every(w=>w.headers.get('authorization')===null));
 const seller=fixture({actorLimit:1});const r=await seller.send('save',save);assert.equal(r.status,200);const id=(await r.json()).id;
 assert.equal((await seller.send('save',{...save,id,expectedRevision:1,requestId:'rate-edit'})).status,429);assert.equal(seller.f.get(c.privateRecords,'product_'+id).revision,1);
});
test('account switch/logout discard late responses and cross-owner commands never change Product',async()=>{
 const x=fixture();await x.ui.save(profile);const id=x.ui.snapshot().owner.id,before=x.f.get(c.privateRecords,'product_'+id);
 await x.switch('buyer');await x.ui.loadOwner(id);assert.equal(x.ui.snapshot().owner,null);
 const r=await x.send('save',{...save,id,expectedRevision:1,requestId:'foreign'},'buyer.test.token');assert.equal(r.status,403);assert.deepEqual(x.f.get(c.privateRecords,'product_'+id),before);
 await x.switch('seller');let release;x.hold(new Promise(r=>release=r));
 const start=x.wire.length,pending=x.ui.loadOwner(id);while(x.wire.length===start)await new Promise(r=>setTimeout(r,0));
 await x.switch(null);release();await pending;assert.equal(x.ui.snapshot().owner,null);assert.equal(x.ui.snapshot().authenticated,false);
 const count=x.wire.length;await x.ui.save(profile);assert.equal(x.wire.length,count);
});
test('missing signing/durable storage/Google-key dependencies and default OFF never contact providers',async()=>{
 const x=fixture(),request=new Request(base+path('list'),{method:'POST',body:'{}'});
 assert.equal((await createStep05Backend().fetch(request)).status,503);
 for(const patch of [{requestVerification:{}},{googleIdentity:{}},{runtimeOptions:{}},{cursorKey:null}]){
  assert.equal((await createStep05Backend({...x.backendOptions,...patch}).fetch(request)).status,503);
 }
 assert.equal((await createStep05Gateway().fetch(request)).status,503);
 assert.equal((await createStep05Gateway({...x.gatewayOptions,requestSigning:{}}).fetch(request)).status,503);
 assert.equal(x.keyCalls,0);assert.equal(x.f.commits,0);
});

test('request proof rechecks expiry after slow key/auth/nonce work, and rejects invalid UTF8 bytes',async()=>{
 let time=clock,consumes=0;const snapshot=()=>time;
 const input={method:'POST',path:path('save'),body:Buffer.from('{}'),authorization:'Bearer seller.test.token',attestationToken:assertion()};
 const signer=createMarketplaceRequestProofSigner({enabled:true,kid:'intent-fixture',now:snapshot,signMessage:bytes=>sign('RSA-SHA256',bytes,{key:intentKey.privateKey,padding:constants.RSA_PKCS1_PADDING})});
 const proof=await signer(input);
 const v=createMarketplaceRequestProofVerifier({enabled:true,now:snapshot,resolvePublicKey:()=>{time+=20000;return intentKey.publicKey;},consumeNonce:()=>{consumes++;return {allowed:true};}});
 assert.equal(await v({...input,proof}),false);assert.equal(consumes,0);
 time=clock;
 const after=createMarketplaceRequestProofVerifier({enabled:true,now:snapshot,resolvePublicKey:()=>intentKey.publicKey,consumeNonce:()=>{time+=20000;return {allowed:true};}});
 assert.equal(await after({...input,proof}),false);
 // Valid signature on non-UTF8 bytes must not reach key/nonce auth dispatch.
 const payload=Buffer.from([123,34,120,34,58,34,0xff,34,125]);
 const bad=payload.toString('base64url')+'.'+sign('RSA-SHA256',payload,{key:intentKey.privateKey,padding:constants.RSA_PKCS1_PADDING}).toString('base64url');
 assert.equal(await after({...input,proof:bad}),false);
 time=clock;
 const long=createMarketplaceRequestProofSigner({enabled:true,kid:'k'.repeat(100),now:snapshot,signMessage:bytes=>sign('RSA-SHA256',bytes,{key:intentKey.privateKey,padding:constants.RSA_PKCS1_PADDING})});
 const longProof=await long(input);assert.ok(longProof);
 const longVerifier=createMarketplaceRequestProofVerifier({enabled:true,now:snapshot,resolvePublicKey:({kid})=>kid==='k'.repeat(100)?intentKey.publicKey:null,consumeNonce:()=>({allowed:true})});
 assert.equal(await longVerifier({...input,proof:longProof}),true);

});
test('hop deadlines stop noncooperative providers and dispatched mutation failure stays OUTCOME_UNKNOWN',async()=>{
 const h={'content-type':'application/json','x-serverless-authorization':'Bearer iam.payload.','x-oldx-gateway-attestation':assertion(),[proofHeader]:'signed.proof',authorization:'Bearer seller.test.token'};
 const request=()=>new Request(base+path('save'),{method:'POST',headers:h,body:'{}'});
 const options={enabled:true,audience:base,gatewayServiceAccount:principal,now,timeoutMs:10,verifyAttestation:()=>({verified:true,audience:base,principal,expiresAtMs:clock+60000}),verifyRequestProof:()=>true,backend:{fetch:()=>{throw Error('lost result');}}};
 assert.equal((await createProofBoundBackendHop(options).fetch(request())).status,202);
 assert.equal((await createProofBoundBackendHop({...options,verifyAttestation:()=>new Promise(()=>{})}).fetch(request())).status,503);
 const hop=createProofBoundGatewayHop({enabled:true,backendOrigin:base,timeoutMs:10,signRequestProof:()=>new Promise(()=>{}),fetchBackend:()=>assert.fail('must not dispatch')});
 const init={method:'POST',headers:{...h},body:Buffer.from('{}')};delete init.headers[proofHeader];
 await assert.rejects(hop(base+path('save'),init));
});
test('proof echo decoding and malformed nonce snapshots fail closed',async()=>{
 const signer=createMarketplaceRequestProofSigner({enabled:true,kid:'intent-fixture',now,signMessage:bytes=>sign('RSA-SHA256',bytes,{key:intentKey.privateKey,padding:constants.RSA_PKCS1_PADDING})});
 const hop=createProofBoundGatewayHop({enabled:true,backendOrigin:base,signRequestProof:signer,fetchBackend:(_url,init)=>{
  const proof=init.headers.get(proofHeader),escaped='\\u'+proof.charCodeAt(0).toString(16).padStart(4,'0')+proof.slice(1);
  return new Response('{"echo":"'+escaped+'"}',{headers:{'content-type':'application/json'}});
 }});
 await assert.rejects(hop(base+path('save'),{method:'POST',headers:{'x-serverless-authorization':'Bearer iam.payload.','x-oldx-gateway-attestation':assertion(),authorization:'Bearer seller.test.token'},body:Buffer.from('{}')}));
 await assert.rejects(consumeAtomicMarketplaceReplayNonce({sdk:{runTransaction:(_db,fn)=>fn({get:()=>({exists:()=>undefined}),set:()=>assert.fail('must not write')})},db:{},nonceRef:{path:'test/nonces'},expiresAtMs:clock+10000,now}));
});
