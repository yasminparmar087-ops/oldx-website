import {createC2StagingRunBudget} from '../../scripts/c2-staging-run-budget.mjs';
import {createStagingMarketplaceBinding} from '../../scripts/staging-marketplace-context.mjs';
import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash,generateKeyPairSync,sign,privateEncrypt,constants} from 'node:crypto';
import {createC2EnabledReleaseControl} from '../../scripts/c2-enabled-release-control.mjs';
import {createC2EnabledProductBackend,createStep05Backend} from '../../functions/staging-marketplace/secure-product-pipeline.mjs';
import {createC2WebsiteMediator,createC2PrivateGatewayHost} from '../../functions/staging-marketplace/c2-website-mediation.mjs';
import {createC2CloudRunMetadataIdentity} from '../../scripts/c2-cloud-run-metadata-identity.mjs';
import {createC2KmsRequestSigning,c2Crc32c} from '../../scripts/c2-kms-request-signing.mjs';
import {createStagingMandatoryPhotoPolicy} from '../../scripts/mandatory-photo-policy.mjs';
import {createStagingAtomicPhotoPublication} from '../../scripts/firebase-atomic-photo-publication.mjs';
import {createFirebaseMarketplaceHttpIntegration} from '../../features/marketplace/firebase-integration.mjs';
import {createProductIntegration} from '../../features/marketplace/product-integration.mjs';
import {prepareC2SyntheticCleanupManifest,reconcileC2SyntheticCleanup} from '../../scripts/c2-synthetic-cleanup-manifest.mjs';
import {STAGING_MARKETPLACE_COLLECTIONS as c,STAGING_MEDIA_COLLECTIONS as m} from '../../scripts/staging-marketplace-context.mjs';
import {fakeFirestoreSdk} from './fake-firestore-sdk.mjs';
const google=generateKeyPairSync('rsa',{modulusLength:2048}),intent=generateKeyPairSync('rsa',{modulusLength:2048});
const site='https://website.invalid',gw='https://gateway.region.run.app',url='https://backend.region.run.app';
const sa=n=>n+'-runtime@oldx-staging.iam.gserviceaccount.com';
const issuer='https://accounts.google.com',wa='urn:oldx:synthetic:website',ga='urn:oldx:synthetic:gateway';
const baseTime=1800000000000,seller='synthetic-c2-batch-seller',buyer='synthetic-c2-batch-buyer';
const profile={title:'ગુજરાતી हिन्दी English',description:'Synthetic',category:'cars',locationLabel:'Sample',basePrice:1,isSold:false,storeId:null,photos:[]};
const contract=()=>({v:1,purpose:'oldx.c2.enabled-product.synthetic.v1',runId:'batch',projectId:'oldx-staging',databaseId:'(default)',
 startsAtMs:baseTime-100,expiresAtMs:baseTime+600000,principals:{mediator:sa('website'),gateway:sa('gateway'),backend:sa('backend')},
 images:Object.fromEntries(['mediator','gateway','backend'].map((k,i)=>[k,'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/synthetic-'+k+'@sha256:'+String(i+1).repeat(64)])),
 evidence:Object.fromEntries(['identity','iam','media','cleanup','security','rollback'].map(k=>[k,'a'.repeat(64)])),
 limits:{maxRequests:20,maxActors:2,maxProducts:1,maxPhotos:1},actors:{seller,buyer},managedPhotoId:'synthetic_photo_1234567890'});
function fixture(){
 const f=fakeFirestoreSdk();let clock=baseTime,revoked=false,expired=false,budgetAllowed=true,approvalAllowed=true,lose=false,sessionNo=0,tokenWait=null,tokenStarted=null;
 const now=()=>clock;
 const collection=name=>{
  const constraints=[];let fields;
  const q={doc:id=>({...f.sdk.doc(f.db,name,id),get:async()=>{const r=await f.sdk.getDocFromServer(f.sdk.doc(f.db,name,id));return {exists:r.exists(),data:r.data};}}),
   select(...v){fields=v;return q;},where(...v){constraints.push(f.sdk.where(...v));return q;},orderBy(...v){constraints.push(f.sdk.orderBy(...v));return q;},
   startAfter(v){constraints.push(f.sdk.startAfter(v));return q;},limit(v){constraints.push(f.sdk.limit(v));return q;},
   async get(){const r=await f.sdk.getDocsFromServer(f.sdk.query(f.sdk.collection(f.db,name),...constraints));return {docs:r.docs.map(d=>({id:d.id,data:()=>Object.fromEntries(Object.entries(d.data()).filter(([k])=>!fields||fields.includes(k)))}))};}};
  return q;
 };
 const db={projectId:'oldx-staging',databaseId:'(default)',collection,runTransaction:(work,opts)=>f.sdk.runTransaction(f.db,tx=>work({
  get:async ref=>{const s=await tx.get(ref);return {exists:s.exists(),data:s.data};},set:(...x)=>tx.set(...x),delete:(...x)=>tx.delete(...x)}),opts)};
 const adminAuth={app:{options:{projectId:'oldx-staging'}},verifyIdToken:async(token,checkRevoked)=>{
  assert.equal(checkRevoked,true);if(revoked)throw Error('Revoked');const uid=token.split('.')[0];
  if(![seller,buyer].includes(uid))throw Error('Denied');return {uid,sub:uid,aud:'oldx-staging',iss:'https://securetoken.google.com/oldx-staging',iat:clock/1000-1,exp:expired?clock/1000-1:clock/1000+3600};
 }};
 for(const uid of [seller,buyer])f.seed(c.actors,uid,{uid,canWrite:true,canPublish:true,suspended:false});
 f.seed(c.generations,'current',{value:0});f.seed(m.generations,'current',{value:0});
 const runtimeOptions={projectId:'oldx-staging',deploymentEnvironment:'preview',adminFirestore:db,adminAuth,FieldValue:{serverTimestamp:f.sdk.serverTimestamp},
  ratePolicy:{windowMs:60000,actorLimit:80,globalLimit:100},createMediaBindings:b=>({photoPolicy:createStagingMandatoryPhotoPolicy({enabled:true,binding:b}),atomicPhotos:createStagingAtomicPhotoPublication({enabled:true,binding:b})})};
 const jwt=(email,sub,aud)=>{
  const enc=v=>Buffer.from(JSON.stringify(v)).toString('base64url');
  const bytes=enc({alg:'RS256',kid:'synthetic-google'})+'.'+enc({iss:issuer,aud,email,sub,email_verified:true,iat:clock/1000,exp:clock/1000+3600});
  return bytes+'.'+sign('RSA-SHA256',Buffer.from(bytes),{key:google.privateKey,padding:constants.RSA_PKCS1_PADDING}).toString('base64url');
 };
 const keys=()=>Response.json({keys:[{...google.publicKey.export({format:'jwk'}),alg:'RS256',kid:'synthetic-google',use:'sig'}]},{headers:{'cache-control':'max-age=300'}});
 const identity=(email,sub,invokerAudience,assertionAudience)=>createC2CloudRunMetadataIdentity({enabled:true,serviceAccount:email,invokerAudience,assertionAudience,now,
  fetchMetadata:async path=>new Response(jwt(email,sub,new URL(path).searchParams.get('audience')),{headers:{'Metadata-Flavor':'Google'}})});
 const webId=identity(sa('website'),'111',gw,wa),gateId=identity(sa('gateway'),'222',url,ga);
 const name='projects/oldx-staging/locations/asia-south1/keyRings/synthetic/cryptoKeys/intent/cryptoKeyVersions/1';
 const algorithm='RSA_SIGN_PKCS1_2048_SHA256',pin=createHash('sha256').update(intent.publicKey.export({type:'spki',format:'der'})).digest('hex');
 const kms=createC2KmsRequestSigning({enabled:true,kid:'synthetic-intent',keyVersion:name,algorithm,
  publicKeyPem:intent.publicKey.export({type:'spki',format:'pem'}),publicKeySha256:pin,validFromMs:clock-10,validUntilMs:clock+600000,now,
  getKeyVersionStatus:async()=>({name,state:'ENABLED',algorithm,publicKeySha256:pin}),
  asymmetricSign:async req=>{
   const digest=Buffer.from(req.digest.sha256,'base64');assert.equal(req.digestCrc32c,c2Crc32c(digest));
   const sig=privateEncrypt({key:intent.privateKey,padding:constants.RSA_PKCS1_PADDING},Buffer.concat([Buffer.from('3031300d060960864801650304020105000420','hex'),digest]));
   return {name,verifiedDigestCrc32c:true,signature:sig.toString('base64'),signatureCrc32c:c2Crc32c(sig)};
  }});
 let admitted=0;
 const release=createC2EnabledReleaseControl({enabled:true,contract:contract(),now,
  verifyApproval:async(_c,{contractDigest})=>({authorized:approvalAllowed,contractDigest,expiresAtMs:baseTime+600000}),
  consumeRunBudget:async()=>({allowed:budgetAllowed&&++admitted<=20})}); // IN-MEMORY TEST DOUBLE, not durable host proof.
 const options={audience:url,gatewayServiceAccount:sa('gateway'),googleIdentity:{identityType:'google-service-account',issuer,attestationAudience:ga,expectedSubject:'222',fetchRequest:keys},
  requestVerification:{resolvePublicKey:kms.resolvePublicKey},runtimeOptions,guestPolicy:{windowMs:60000,guestLimit:40,globalLimit:80},cursorKey:new Uint8Array(32).fill(33),now};
 const backend=createC2EnabledProductBackend({...options,enabled:true,releaseControl:release,runtimeServiceAccount:sa('backend'),runtimeImage:contract().images.backend});
 let backendTarget=backend;
 const wires=[],trace=[];
 const gatewayOptions={backendOrigin:url,gatewayServiceAccount:sa('gateway'),attestationAudience:ga,
  getInvokerCredential:gateId.getInvokerCredential,getGatewayAttestation:gateId.getWebsiteAttestation,
  requestSigning:{kid:'synthetic-intent',signMessage:kms.signMessage},
  fetchBackend:async(path,init)=>{const headers=new Headers(init.headers);headers.set('x-serverless-authorization','Bearer synthetic.payload.');
   const request=new Request(path,{...init,headers});wires.push(request.clone());const result=await backendTarget.fetch(request);trace.push({hop:'backend',status:result.status,body:await result.clone().text()});return result;}};
 const host=createC2PrivateGatewayHost({enabled:true,privateGatewayOrigin:gw,mediatorPrincipal:sa('website'),
  websiteIdentity:{identityType:'google-service-account',issuer,attestationAudience:wa,expectedSubject:'111',fetchRequest:keys},allowedOrigins:[site],gatewayOptions,now});
 const mediator=createC2WebsiteMediator({enabled:true,websiteOrigin:site,allowedOrigins:[site],privateGatewayOrigin:gw,
  mediatorPrincipal:sa('website'),mediationAudience:wa,getGatewayInvokerCredential:webId.getInvokerCredential,getWebsiteAttestation:webId.getWebsiteAttestation,
  consumeGuestAdmission:()=>({allowed:true}),now,fetchPrivateGateway:(path,init)=>{const headers=new Headers(init.headers);headers.set('x-serverless-authorization','Bearer synthetic.payload.');return host.fetch(new Request(path,{...init,headers})).then(async result=>{trace.push({hop:'gateway',status:result.status,body:await result.clone().text()});return result;});}});
 let listener;
 const auth={app:{options:{projectId:'oldx-staging'}},currentUser:null,onIdTokenChanged(fn){listener=fn;return ()=>{};}};
 let scope;
 const integration=createFirebaseMarketplaceHttpIntegration({enabled:true,auth,origin:site,makeSessionId:()=> 'session_'+(++sessionNo),
  onSession:s=>{scope=s;},fetchRequest:async(path,init)=>{
   const headers=new Headers(init.headers);headers.set('origin',site);
   const result=await mediator.fetch(new Request(path,{...init,headers}));
   trace.push({hop:'website',status:result.status,body:await result.clone().text()});if(lose&&path.endsWith('/save')&&result.status===200){lose=false;throw Error('Lost response');}return result;
  }});
 // Reuse existing model instead of mounting/rewriting Step06 UI.
 const model2=createProductIntegration({enabled:true,ports:integration.product,makeRequestId:()=> 'request_'+(++sessionNo)});
 // The actual UI-host session fanout is supplied by existing onSession contract.
 const login=uid=>{const user={uid,getIdToken:async()=>{if(tokenWait){tokenStarted?.();return tokenWait;}return uid+'.synthetic.token';}};auth.currentUser=user;listener(user);model2.setSession(scope);};
 const attach=id=>{
  const scopeId=createHash('sha256').update(JSON.stringify(['product',id,null])).digest('hex'),imageId='synthetic_photo_1234567890';
  f.seed(m.permissions,seller,{uid:seller,canRelease:true,suspended:false});
  f.seed(m.permissions,'moderator',{uid:'moderator',canModerate:true,suspended:false});
  f.seed(m.associations,scopeId,{kind:'product',parentId:id,ownerUid:seller,service:null,parentRevision:1,visibility:'private',photoRevision:1,imageIds:[imageId]});
  f.seed(m.assets,imageId,{imageId,ownerUid:seller,kind:'product',parentId:id,service:null,parentRevision:1,revision:1,state:'attached',references:[scopeId],
   processedDigest:'b'.repeat(64),processed:{metadataStripped:true,contentScanned:true,contentType:'image/webp',byteSize:100,width:10,height:10}});
  f.seed(m.reviews,imageId,{imageId,ownerUid:seller,decision:'approved',assetRevision:1,processedDigest:'b'.repeat(64),revision:1,moderatorUid:'moderator'});
  return {...profile,photos:[{kind:'managed',imageId}]};
 };
 return {useLegacy(){backendTarget=createStep05Backend({...options,enabled:true,runtimeOptions:{...runtimeOptions,publicationEnabled:true}});},f,trace,options,release,backend,model:model2,integration,login,attach,gatewayOptions,wires,
  holdToken(){let start,release;const started=new Promise(r=>start=r);tokenWait=new Promise(r=>release=r);tokenStarted=start;return {started,release(){release(seller+'.synthetic.token');tokenWait=null;tokenStarted=null;}};},
  revoke:()=>revoked=true,expire:()=>expired=true,time:v=>clock=v,denyBudget:()=>budgetAllowed=false,denyApproval:()=>approvalAllowed=false,lose:()=>lose=true};
}
test('NEW enabled-source lifecycle reuses real crypto/media and existing Firebase Product model',async()=>{
 const f=fixture();f.login(seller);
 await f.model.save(profile);let state=f.model.snapshot();assert.equal(state.command.status,'saved',JSON.stringify(f.trace));const id=state.owner.id;
 await f.model.loadOwner(id);
 await f.model.save(profile,'publish');assert.equal(f.model.snapshot().command.status,'photosUnavailable');
 const photo=f.attach(id);await f.model.save(photo,'publish');assert.equal(f.model.snapshot().command.status,'saved');
 assert.equal(f.f.get(c.privateRecords,'product_'+id).published,true);
 await f.integration.product.list({kind:'product',limit:1,category:'',storeId:null,cursor:null}).then(r=>{assert.equal(r.ok,true);assert.equal(r.items[0].id,id);assert.equal('ownerUid' in r.items[0],false);});
 await f.model.openProduct(id);assert.equal(f.model.snapshot().detail.id,id);
 await f.model.save({...photo,title:'Edited ગુજરાતી'},'draft');assert.equal(f.model.snapshot().command.status,'saved');
 await f.model.save({...photo,title:'Edited ગુજરાતી'},'withdraw');assert.equal(f.model.snapshot().command.status,'saved');
 assert.equal(f.f.get(c.publicViews,'product_'+id),null);
 await f.model.openProduct(id);assert.equal(f.model.snapshot().detail,null);
 assert.ok(f.f.get(m.assets,'synthetic_photo_1234567890').publicRelease===null);
 f.integration.destroy();
});
test('NEW enabled composition denies foreign owner, expiry, revoked user and changed database',async()=>{
 const f=fixture();f.login(seller);await f.model.save(profile);const id=f.model.snapshot().owner.id;
 f.login(buyer);await f.model.loadOwner(id);assert.equal(f.model.snapshot().owner,null);
 await f.model.save({...profile,title:'foreign'},'draft'); // New buyer draft cannot change seller ID.
 assert.equal(f.f.get(c.privateRecords,'product_'+id).ownerUid,seller);
 assert.equal([...f.f.snapshot().keys()].filter(p=>p.startsWith(c.privateRecords+'/')).length,1);
 f.revoke();f.model.startDraft();await f.model.save(profile);assert.equal(f.model.snapshot().command.status,'denied');
 const bad=createC2EnabledProductBackend({...f.options,enabled:true,releaseControl:f.release,runtimeServiceAccount:sa('backend'),runtimeImage:contract().images.backend,
  runtimeOptions:{...f.options.runtimeOptions,adminFirestore:{...f.options.runtimeOptions.adminFirestore,databaseId:'other'}}});
 assert.equal((await bad.fetch(new Request(url+'/api/staging/marketplace/owner',{method:'POST',body:JSON.stringify({kind:'product'})}))).status,503);
 const off=createStep05Backend({...f.options,enabled:true});
 // Existing public factory is STILL hard publication-OFF (code assertion in separate group).
 assert.equal(typeof off.fetch,'function');f.integration.destroy();
});
test('NEW same-request recovery, signature tamper/replay and release budget fail closed',async()=>{
 const f=fixture();f.login(seller);f.lose();await f.model.save(profile);assert.equal(f.model.snapshot().command.status,'unknown');
 const requestId=f.model.pendingReceipt().requestId;await f.model.retry();assert.equal(f.model.snapshot().command.status,'saved');
 assert.equal([...f.f.snapshot().keys()].filter(p=>p.startsWith(c.privateRecords+'/')).length,1);
 assert.equal(f.model.pendingReceipt(),null);assert.ok(requestId);
 const replay=f.wires[0];assert.equal((await f.backend.fetch(replay.clone())).status,403);
 const tampered=await replay.clone().json();tampered.profile.title='tampered';
 const changed=new Request(replay.url,{method:'POST',headers:replay.headers,body:JSON.stringify(tampered)});assert.equal((await f.backend.fetch(changed)).status,403);
 f.denyBudget();await f.model.loadOwner(f.model.snapshot().owner.id);assert.equal(f.model.snapshot().owner,null);
 f.integration.destroy();
});
test('NEW release scope snapshots, H1 evidence rejection, expiry and missing-provider OFF',async()=>{
 const c1=contract();const now=()=>baseTime;
 const verifyApproval=async(_,{contractDigest})=>({authorized:true,contractDigest,expiresAtMs:c1.expiresAtMs});
 const control=createC2EnabledReleaseControl({enabled:true,contract:c1,now,verifyApproval,consumeRunBudget:()=>({allowed:true})});
 c1.principals.backend=sa('attacker');c1.images.backend='mutable:tag';
 assert.equal(control.runtimePrincipal,sa('backend'));
 const req=()=>new Request(url+'/api/staging/marketplace/owner',{method:'POST',body:JSON.stringify({kind:'product'})});
 assert.equal((await control.wrap({fetch:()=>Response.json({ok:true})}).fetch(req())).status,200);
 for(const patch of [{purpose:'oldx.private.off'},{databaseId:'foreign'},{expiresAtMs:baseTime-101},{images:{...contract().images,backend:'gcr.io/base:tag'}}]){
  const ctl=createC2EnabledReleaseControl({enabled:true,contract:{...contract(),...patch},now,verifyApproval,consumeRunBudget:()=>({allowed:true})});
  assert.equal(ctl.ready,false);
 }
 assert.equal(createC2EnabledReleaseControl({enabled:true,contract:contract()}).ready,false);
 assert.equal((await createC2EnabledProductBackend().fetch(req())).status,503);
 const f=fixture();f.denyApproval();assert.equal((await f.backend.fetch(req())).status,503);
 f.time(baseTime+600001);assert.equal((await f.backend.fetch(req())).status,503);
 f.integration.destroy();
});
test('NEW metadata cancellation bounds providers and streaming bodies ignoring AbortSignal',async()=>{
 const opts={enabled:true,serviceAccount:sa('website'),invokerAudience:gw,assertionAudience:wa};
 const stalled=createC2CloudRunMetadataIdentity({...opts,fetchMetadata:()=>new Promise(()=>{})});
 await assert.rejects(stalled.getInvokerCredential({audience:gw}),/C2_IDENTITY_UNAVAILABLE/);
 let canceled=false;
 const stream=createC2CloudRunMetadataIdentity({...opts,fetchMetadata:()=>new Response(new ReadableStream({start(){},cancel(){canceled=true;}}),{headers:{'Metadata-Flavor':'Google'}})});
 await assert.rejects(stream.getInvokerCredential({audience:gw}),/C2_IDENTITY_UNAVAILABLE/);assert.equal(canceled,true);
});
test('NEW cleanup reconciliation captures exact versions, partial failures and shared/foreign STOP',()=>{
 const input={enabled:true,projectId:'oldx-staging',databaseId:'(default)',runId:'batch',actors:['synthetic-c2-batch-seller'],records:[
  {path:'marketplacePrivate_v1/product_one',ownerUid:'synthetic-c2-batch-seller',runId:'batch',updateTime:'2026-11-26T00:00:00Z'}]};
 const manifest=prepareC2SyntheticCleanupManifest(input),row=manifest.records[0];
 const readbacks=[{...row,exists:true,dependencies:[]}];
 assert.equal(reconcileC2SyntheticCleanup({enabled:true,manifest,readbacks}).decision,'DRAFT_READY');
 assert.equal(reconcileC2SyntheticCleanup({enabled:true,manifest,readbacks,results:[{path:row.path,updateTime:row.updateTime,status:'UNKNOWN'}]}).decision,'PARTIAL_STOP');
 assert.equal(reconcileC2SyntheticCleanup({enabled:true,manifest,readbacks:[{...readbacks[0],dependencies:['foreign']}]}).decision,'STOP');
 assert.equal(reconcileC2SyntheticCleanup({enabled:true,manifest,readbacks:[{...readbacks[0],updateTime:'new'}]}).decision,'STOP');
 const done=reconcileC2SyntheticCleanup({enabled:true,manifest,readbacks:[{...readbacks[0],exists:false}],results:[{path:row.path,updateTime:row.updateTime,status:'DELETED_CONFIRMED'}]});
 assert.equal(done.decision,'DRAFT_COMPLETE');assert.equal(done.authorized,false);
});

test('NEW trusted gateway configuration snapshot cannot redirect tokens or replace signer after construction',async()=>{
 const f=fixture();let leaked=false;
 f.gatewayOptions.backendOrigin='https://attacker.invalid';
 f.gatewayOptions.requestSigning.kid='attacker';
 f.gatewayOptions.fetchBackend=()=>{leaked=true;throw Error('Must not run');};
 f.login(seller);await f.model.save(profile);
 assert.equal(f.model.snapshot().command.status,'saved');assert.equal(leaked,false);
 assert.ok(f.wires.every(r=>new URL(r.url).origin===url));
 f.integration.destroy();
});
test('NEW Firebase account switch during token wait cannot write or resurrect old Product scope',async()=>{
 const f=fixture();f.login(seller);const hold=f.holdToken();
 const work=f.model.save(profile);await hold.started;
 f.login(buyer);hold.release();await work;
 assert.equal(f.model.snapshot().owner,null);
 assert.equal([...f.f.snapshot().keys()].filter(p=>p.startsWith(c.privateRecords+'/')).length,0);
 f.expire();await f.model.save(profile);assert.equal(f.model.snapshot().command.status,'denied');
 f.integration.destroy();
});

test('NEW single-product release scope never reads or mutates an unrelated Product ID',async()=>{
 const f=fixture();f.login(seller);await f.model.save(profile);
 const before=f.f.calls;
 await f.model.loadOwner('unrelated');
 assert.equal(f.model.snapshot().owner,null);assert.equal(f.f.calls,before);
 const response=await f.integration.product.detail({kind:'product',id:'unrelated'});
 assert.equal(response.ok,false);assert.equal(f.f.calls,before);
 const wrongImage=createC2EnabledProductBackend({...f.options,enabled:true,releaseControl:f.release,runtimeServiceAccount:sa('backend'),runtimeImage:'mutable:tag'});
 assert.equal((await wrongImage.fetch(new Request(url+'/api/staging/marketplace/owner',{method:'POST',body:'{"kind":"product"}'}))).status,503);
 f.integration.destroy();
});

test('NEW C2 media ownership and legacy-publication OFF stay closed under new composition',async()=>{
 const f=fixture();f.login(seller);await f.model.save(profile);const id=f.model.snapshot().owner.id;
 const photo=f.attach(id),asset=f.f.get(m.assets,'synthetic_photo_1234567890');
 f.f.seed(m.assets,'synthetic_photo_1234567890',{...asset,ownerUid:buyer});
 await f.model.save(photo,'publish');assert.equal(f.model.snapshot().command.status,'photosUnavailable');
 assert.equal(f.f.get(c.privateRecords,'product_'+id).published,false);assert.equal(f.f.get(c.publicViews,'product_'+id),null);
 f.f.seed(m.assets,'synthetic_photo_1234567890',asset);f.useLegacy();
 await f.model.save(photo,'publish');assert.equal(f.model.snapshot().command.status,'unavailable');
 assert.equal(f.f.get(c.privateRecords,'product_'+id).published,false);f.integration.destroy();
});

test('NEW durable run budget reuses native atomic counters across two provider instances',async()=>{
 const f=fixture(),binding=createStagingMarketplaceBinding(f.options.runtimeOptions);
 const config={enabled:true,binding,runId:'budget',contractDigest:'b'.repeat(64),maxRequests:2,expiresAtMs:baseTime+10000,now:()=>baseTime};
 const a=createC2StagingRunBudget(config),b=createC2StagingRunBudget(config);
 const input={runId:'budget',operation:'save',projectId:'oldx-staging',databaseId:'(default)',expiresAtMs:baseTime+10000,limits:{maxRequests:2,maxActors:2,maxProducts:1,maxPhotos:1}};
 assert.equal((await a(input)).allowed,true);assert.equal((await b(input)).allowed,true);assert.equal((await a(input)).allowed,false);
 const freshGrant=createC2StagingRunBudget({...config,contractDigest:'c'.repeat(64)});
 assert.equal((await freshGrant(input)).allowed,false);
 assert.equal((await b({...input,databaseId:'foreign'})).allowed,false);
 assert.equal((await createC2StagingRunBudget()(input)).allowed,false);
 f.integration.destroy();
});
