import test from 'node:test';
import assert from 'node:assert/strict';
import {fakeFirestoreSdk} from './fake-firestore-sdk.mjs';
import {createStagingMarketplaceRuntime} from '../../functions/staging-marketplace/runtime.mjs';
import {createStagingMarketplacePublicRuntime} from '../../functions/staging-marketplace/public-runtime.mjs';
import {createMarketplaceFetchHandler} from '../../functions/staging-marketplace/vercel-handler.mjs';
import {createMarketplaceHttpTransport} from '../../features/marketplace/http-transport.mjs';
import {createAuthenticatedMarketplaceCommands} from '../../features/marketplace/authenticated-command-client.mjs';
import {createMarketplacePublicClient} from '../../features/marketplace/public-read-client.mjs';
import {createProductIntegration} from '../../features/marketplace/product-integration.mjs';
import {createStagingMarketplaceMedia} from '../../scripts/staging-marketplace-media.mjs';
import {createStagingMarketplaceBinding,STAGING_MARKETPLACE_COLLECTIONS as c} from '../../scripts/staging-marketplace-context.mjs';
const profile={title:'ગુજરાતી हिन्दी Product',description:'Synthetic only',category:'cars',locationLabel:'Sample',basePrice:10,isSold:false,storeId:null,photos:[]};
const path=op=>'/api/staging/marketplace/'+op;
function fixture(){
 const f=fakeFirestoreSdk();let uid='seller',lost=false,rate=true,hold=null;
 const nativeDoc=(name,id)=>({...f.sdk.doc(f.db,name,id),get:async()=>{const snap=await f.sdk.getDocFromServer(f.sdk.doc(f.db,name,id));return {exists:snap.exists(),data:snap.data};}});
 function collection(name){
  const constraints=[];let fields;
  const q={doc:id=>nativeDoc(name,id),select(...v){fields=v;return q;},where(field,op,value){constraints.push(f.sdk.where(field,op,value));return q;},orderBy(...args){constraints.push(f.sdk.orderBy(...args));return q;},startAfter(v){constraints.push(f.sdk.startAfter(v));return q;},limit(v){constraints.push(f.sdk.limit(v));return q;},async get(){
   const snap=await f.sdk.getDocsFromServer(f.sdk.query(f.sdk.collection(f.db,name),...constraints));
   return {docs:snap.docs.map(d=>({id:d.id,data:()=>Object.fromEntries(Object.entries(d.data()).filter(([k])=>!fields||fields.includes(k)))}))};
  }};return q;
 }
 const adminFirestore={projectId:'oldx-staging',databaseId:'(default)',collection,runTransaction:(work,opts)=>f.sdk.runTransaction(f.db,tx=>work({get:async ref=>{const snap=await tx.get(ref);return {exists:snap.exists(),data:snap.data};},set:(...args)=>tx.set(...args),delete:(...args)=>tx.delete(...args)}),opts)};
 const adminAuth={app:{options:{projectId:'oldx-staging'}},verifyIdToken:async(token,revoked)=>{assert.equal(revoked,true);if(token!==uid+'.test.token')throw Error('Invalid token');const now=Math.floor(Date.now()/1000);return {uid,sub:uid,aud:'oldx-staging',iss:'https://securetoken.google.com/oldx-staging',iat:now,exp:now+3600};}};
 for(const actor of ['seller','buyer'])f.seed(c.actors,actor,{uid:actor,canWrite:true,canPublish:true,suspended:false});
 f.seed(c.generations,'current',{value:0});
 const options={enabled:true,projectId:'oldx-staging',deploymentEnvironment:'preview',adminFirestore,adminAuth,FieldValue:{serverTimestamp:f.sdk.serverTimestamp},ratePolicy:{windowMs:60000,actorLimit:50,globalLimit:100},publicationEnabled:true,createMediaBindings:b=>createStagingMarketplaceMedia({enabled:true,binding:b})};
 const runtime=createStagingMarketplaceRuntime(options),cursors=new Map();
 const publicOptions={...options,consumeRateLimit:()=>({allowed:rate}),readCursor:key=>cursors.get(key),issueCursor:value=>{const key='cursor-'+cursors.size;cursors.set(key,value);return key;}};
 const publicRuntime=createStagingMarketplacePublicRuntime(publicOptions);
 const handlers=Object.fromEntries(['save','owner','archive','list','detail'].map(operation=>[operation,createMarketplaceFetchHandler({operation,options:{enabled:true},loadRuntime:async()=>['list','detail'].includes(operation)?publicRuntime:runtime})]));
 const calls=[];
 const transport=createMarketplaceHttpTransport({enabled:true,origin:'https://oldx-staging.invalid',fetchRequest:async(url,init)=>{
  calls.push({operation:url.split('/').at(-1),body:JSON.parse(init.body),headers:init.headers});
  const response=await handlers[url.split('/').at(-1)].fetch(new Request(url,init));
  if(lost&&url.endsWith('/save')){lost=false;throw Error('Lost committed response');}
  if(hold)await hold;
  return response;
 }});
 const commands=createAuthenticatedMarketplaceCommands({enabled:true,getToken:scope=>({...scope,token:uid+'.test.token'}),sendCommand:transport.sendCommand});
 const reads=createMarketplacePublicClient({enabled:true,sendRead:transport.sendRead});
 let n=0;const ui=createProductIntegration({enabled:true,ports:{...commands,...reads},makeRequestId:()=> 'step05-'+(++n)});ui.setSession({uid,sessionId:'session-seller'});
 const approve=async id=>{
  const binding=createStagingMarketplaceBinding(options),m=binding.mediaCollections,media=createStagingMarketplaceMedia({enabled:true,binding,authenticate:()=>({uid:'seller'})});
  const imageId='native_photo_12345678901234567890',digest='b'.repeat(64);
  f.seed(m.assets,imageId,{imageId,kind:'product',parentId:id,ownerUid:'seller',service:null,parentRevision:2,revision:0,state:'quarantined',references:[],processedDigest:digest,processed:{contentType:'image/webp',byteSize:100,width:10,height:10,metadataStripped:true,contentScanned:true}});
  assert.equal((await media.references.apply({requestId:'photo-ref',kind:'product',parentId:id,expectedParentRevision:2,expectedPhotoRevision:0,imageIds:[imageId],service:null})).ok,true);
  f.seed(m.generations,'current',{value:0});f.seed(m.permissions,'seller',{uid:'seller',canModerate:false,canRelease:true,suspended:false});f.seed(m.permissions,'reviewer',{uid:'reviewer',canModerate:true,canRelease:false,suspended:false});
  f.seed(m.reviews,imageId,{imageId,ownerUid:'seller',moderatorUid:'reviewer',decision:'approved',assetRevision:1,processedDigest:digest,revision:1});
  return {...profile,photos:[{kind:'managed',imageId}]};
 };
 return {f,ui,commands,reads,runtime,options,publicOptions,transport,calls,approve,handlers,
  other(){uid='buyer';},lose(){lost=true;},rateOff(){rate=false;},hold(p){hold=p;}};
}
test('inactive public runtime/transport/handler never accesses injected dependencies',async()=>{
 let calls=0;
 const transport=createMarketplaceHttpTransport({origin:'https://oldx-staging.invalid',fetchRequest:()=>{calls++;}});
 assert.equal((await transport.sendRead('list',{})).status,503);
 const runtime=createStagingMarketplacePublicRuntime({consumeRateLimit:()=>{calls++;}});
 assert.equal((await runtime.handle(path('detail'),{})).status,503);
 const handler=createMarketplaceFetchHandler({operation:'list',loadRuntime:()=>{calls++;}});
 assert.equal((await handler.fetch(new Request('https://oldx-staging.invalid'+path('list'),{method:'POST'}))).status,503);assert.equal(calls,0);
});
test('actual source chain saves/edits/reloads/publishes/discovers/withdraws/archives with photo safeguards',async()=>{
 const x=fixture();await x.ui.save(profile);let owner=x.ui.snapshot().owner;assert.ok(owner);const id=owner.id;
 assert.equal((await x.reads.detail({kind:'product',id})).ok,false);
 await x.ui.loadOwner(id);assert.equal(x.ui.snapshot().statuses.owner,'ready');
 await x.ui.save({...profile,title:'Edited ગુજરાતી'});assert.equal(x.ui.snapshot().owner.revision,2);
 // Publication enabled only inside this synthetic test, with real media policy.
 const photoProfile=await x.approve(id);await x.ui.save(photoProfile,'publish');
 assert.equal(x.ui.snapshot().command.status,'saved');assert.equal(x.f.get(c.privateRecords,'product_'+id).published,true);
 const listed=await x.reads.list({kind:'product',limit:12,category:'',storeId:null,cursor:null});assert.equal(listed.items[0].id,id);
 assert.equal(JSON.stringify(listed).includes('ownerUid'),false);assert.equal(JSON.stringify(listed).includes('photos'),false);
 assert.equal((await x.reads.detail({kind:'product',id})).ok,true);
 assert.equal(x.calls.filter(c=>['list','detail'].includes(c.operation)).every(c=>!Object.hasOwn(c.headers,'authorization')),true);
 await x.ui.save(photoProfile,'withdraw');assert.equal(x.ui.snapshot().command.status,'saved');
 assert.equal((await x.reads.detail({kind:'product',id})).ok,false);
 assert.deepEqual((await x.reads.list({kind:'product',limit:12,category:'',storeId:null,cursor:null})).items,[]);
 await x.ui.archive();assert.equal(x.ui.snapshot().command.status,'saved');assert.equal(x.f.get(c.privateRecords,'product_'+id).archived,true);
 x.ui.clear();assert.equal(x.ui.snapshot().owner,null);
 // All records are memory-only: discard fixture; no hosted cleanup/deletion.
});
test('committed lost response retries same request; logout/account switch deny stale owner work',async()=>{
 const x=fixture();x.lose();await x.ui.save(profile);assert.equal(x.ui.snapshot().command.status,'unknown');
 await x.ui.retry();assert.equal(x.ui.snapshot().command.status,'saved');
 assert.deepEqual(x.calls[0].body,x.calls[1].body);
 const id=x.ui.snapshot().owner.id;assert.equal([...x.f.snapshot()].filter(([k])=>k.startsWith(c.privateRecords+'/')).length,1);

 const guest=await x.handlers.save.fetch(new Request('https://oldx-staging.invalid'+path('save'),{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({kind:'product',id:null,expectedRevision:0,publication:'draft',profile,requestId:'guest'})}));
 assert.equal(guest.status,401);
 x.other();x.ui.setSession({uid:'buyer',sessionId:'session-buyer'});await x.ui.loadOwner(id);assert.equal(x.ui.snapshot().owner,null);
 assert.equal((await x.commands.save({id,expectedRevision:1,publication:'draft',profile,requestId:'foreign'},{session:{uid:'buyer',sessionId:'session-buyer'}})).code,'DENIED');
 x.ui.setSession(null);await x.ui.save(profile);assert.equal(x.ui.snapshot().command.status,'denied');
});
test('public composition rejects missing enforcement/wrong project and bounds guest quota',async()=>{
 const x=fixture(),input={method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({kind:'product',limit:12,category:'',storeId:null,cursor:null})};
 for(const patch of [{consumeRateLimit:null},{readCursor:null},{projectId:'oldx-1c983'},{deploymentEnvironment:'production'}]){
  assert.equal((await createStagingMarketplacePublicRuntime({...x.publicOptions,...patch}).handle(path('list'),input)).status,503);
 }
 x.rateOff();assert.equal((await x.reads.list(JSON.parse(input.body))).code,'RATE_LIMITED');
 assert.equal((await x.runtime.handle(path('list'),input)).status,404);
 assert.equal((await createStagingMarketplacePublicRuntime(x.publicOptions).handle(path('save'),input)).status,404);
});
test('transport rejects unsafe origin, credential/response contamination and oversized streams',async()=>{
 let calls=0;
 for(const origin of ['http://oldx-staging.invalid','https://user:pass@oldx-staging.invalid','https://oldx-staging.invalid/extra']){
  const t=createMarketplaceHttpTransport({enabled:true,origin,fetchRequest:()=>{calls++;}});assert.equal((await t.sendRead('list',{})).status,503);
 }
 const t=createMarketplaceHttpTransport({enabled:true,origin:'https://oldx-staging.invalid',fetchRequest:()=>{calls++;return Response.json({});}});
 assert.equal((await t.sendCommand('save',{},{})).status,401);assert.equal((await t.sendRead('list',{large:'x'.repeat(5000)})).status,413);assert.equal(calls,0);
 let cancelled=false;
 const big=createMarketplaceHttpTransport({enabled:true,origin:'https://oldx-staging.invalid',fetchRequest:()=>new Response(new ReadableStream({pull(c){c.enqueue(new Uint8Array(32768));},cancel(){cancelled=true;}}),{headers:{'content-type':'application/json'}})});
 await assert.rejects(big.sendRead('list',{}));assert.equal(cancelled,true);
 const bad=createMarketplaceHttpTransport({enabled:true,origin:'https://oldx-staging.invalid',fetchRequest:()=>Response.json({ok:true,profile:{id:'p',ownerUid:'secret'}})});
 assert.equal((await createMarketplacePublicClient({enabled:true,sendRead:bad.sendRead}).detail({kind:'product',id:'p'})).ok,false);
});

test('offline cancellation and account switch discard late HTTP mutation acknowledgements',async()=>{
 const x=fixture();let release;x.hold(new Promise(r=>release=r));
 const pending=x.ui.save(profile);while(x.calls.length===0)await new Promise(r=>setTimeout(r,0));
 x.ui.setOnline(false);assert.equal(x.ui.snapshot().command.status,'unknown');
 x.other();x.ui.setSession({uid:'buyer',sessionId:'new-session'});release();await pending;
 assert.equal(x.ui.snapshot().owner,null);assert.equal(x.ui.snapshot().command.canRetry,false);
 x.ui.setOnline(true);assert.equal(x.ui.snapshot().authenticated,true);
});


test('opt-in Firebase composition wires HTTP ports while default OFF never observes Auth or sends',async()=>{
 const {createFirebaseMarketplaceHttpIntegration:make}=await import('../../features/marketplace/firebase-integration.mjs');
 let observer,scope,calls=0;const user={uid:'seller',getIdToken:async()=> 'seller.test.token'};
 const auth={app:{options:{projectId:'oldx-staging'}},currentUser:user,onIdTokenChanged:fn=>{observer=fn;return ()=>{};}};
 const config={auth,origin:'https://oldx-staging.invalid',makeSessionId:()=> 'factory-session',onSession:v=>scope=v,
  fetchRequest:async(url,init)=>{calls++;assert.equal(init.headers.authorization,'Bearer seller.test.token');assert.equal(JSON.parse(init.body).kind,'product');return Response.json({ok:true,status:'saved',id:'factory-product',revision:1,generation:0});}};
 const disabled=make(config);assert.equal(observer,undefined);
 await disabled.product.save({},{});assert.equal(calls,0);disabled.destroy();
 const bridge=make({...config,enabled:true});observer(user);
 const ui=createProductIntegration({enabled:true,ports:bridge.product,makeRequestId:()=> 'factory-request'});
 ui.setSession(scope);await ui.save(profile);assert.equal(ui.snapshot().owner.id,'factory-product');assert.equal(calls,1);
 observer(null);ui.setSession(scope);await ui.save(profile);assert.equal(ui.snapshot().command.status,'denied');assert.equal(calls,1);bridge.destroy();
});
