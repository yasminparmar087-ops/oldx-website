import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fakeFirestoreSdk} from './fake-firestore-sdk.mjs';
import {createStagingMarketplaceBinding,STAGING_RATE_COLLECTION} from '../../scripts/staging-marketplace-context.mjs';
import {createStagingMarketplaceGuestRate} from '../../scripts/staging-marketplace-guest-rate.mjs';
import {createSecureStagingMarketplacePublicRuntime} from '../../functions/staging-marketplace/public-runtime.mjs';
function fixture(){
 const f=fakeFirestoreSdk(),now=()=>120000;
 const adminFirestore={projectId:'oldx-staging',databaseId:'(default)',collection:name=>({doc:id=>f.sdk.doc(f.db,name,id)}),runTransaction:(work,opts)=>f.sdk.runTransaction(f.db,tx=>work({get:async ref=>{const s=await tx.get(ref);return {exists:s.exists(),data:s.data};},set:(...args)=>tx.set(...args),delete:(...args)=>tx.delete(...args)}),opts)};
 const options={projectId:'oldx-staging',deploymentEnvironment:'preview',adminFirestore,FieldValue:{serverTimestamp:f.sdk.serverTimestamp}};
 const binding=createStagingMarketplaceBinding(options),context={signal:new AbortController().signal,deadlineAt:125000};
 return {f,options,binding,context,now,policy:{windowMs:60000,guestLimit:3,globalLimit:5}};
}
const input={operation:'marketplace.public.list'};
test('concurrent instances consume one anonymous pool atomically without trusting caller identity',async()=>{
 const x=fixture(),a=createStagingMarketplaceGuestRate({...x,enabled:true}),b=createStagingMarketplaceGuestRate({...x,enabled:true});
 const results=await Promise.all(Array.from({length:12},(_,i)=>(i%2?a:b)({...input,actorUid:'forged-'+i,ip:'untrusted'},x.context)));
 assert.equal(results.filter(r=>r.allowed).length,3);assert.equal(x.f.commits,3);
 const records=[...x.f.snapshot()];assert.equal(records.length,2);
 for(const [path,value]of records){assert.ok(path.startsWith(STAGING_RATE_COLLECTION+'/'));assert.deepEqual(Object.keys(value).sort(),['count','expiresAtMs']);assert.equal(value.count,3);}
 assert.doesNotMatch(JSON.stringify(records),/forged|untrusted/);
});
test('global counter is checked in the same transaction and failed commit does not partially consume',async()=>{
 const x=fixture(),key=createHash('sha256').update(JSON.stringify(['marketplace-guest-v1','global',2])).digest('hex');
 x.f.seed(STAGING_RATE_COLLECTION,key,{count:4,expiresAtMs:240000});
 const q=createStagingMarketplaceGuestRate({...x,enabled:true});
 assert.equal((await q(input,x.context)).allowed,true);assert.equal((await q(input,x.context)).allowed,false);
 const y=fixture();y.f.failCommit=true;await assert.rejects(createStagingMarketplaceGuestRate({...y,enabled:true})(input,y.context));
 assert.equal(y.f.snapshot().size,0);
});
test('disabled, expired, cancelled, invalid policy/operation and corrupt counters fail closed',async()=>{
 assert.deepEqual(await createStagingMarketplaceGuestRate()(),{allowed:false});
 const x=fixture(),q=createStagingMarketplaceGuestRate({...x,enabled:true});
 await assert.rejects(q(input,{...x.context,deadlineAt:120000}));
 await assert.rejects(q(input,{...x.context,signal:AbortSignal.abort()}));
 await assert.rejects(q({operation:'marketplace.save'},x.context));
 assert.throws(()=>createStagingMarketplaceGuestRate({...x,enabled:true,policy:{...x.policy,guestLimit:6}}));
 const key=createHash('sha256').update(JSON.stringify(['marketplace-guest-v1','anonymous-pool',2])).digest('hex');
 x.f.seed(STAGING_RATE_COLLECTION,key,{count:-1});
 assert.equal((await q(input,x.context)).allowed,false);assert.equal(x.f.commits,0);
});
test('secure public composition refuses missing key/quota and propagates a safe quota failure',async()=>{
 const x=fixture(),req={method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({kind:'product',id:'synthetic'})};
 for(const patch of [{},{enabled:true},{enabled:true,guestPolicy:x.policy},{enabled:true,cursorKey:new Uint8Array(32).fill(7)}]){
  const r=createSecureStagingMarketplacePublicRuntime({...x.options,...patch});
  assert.equal((await r.handle('/api/staging/marketplace/detail',req)).status,503);
 }
 x.f.failCommit=true;
 const r=createSecureStagingMarketplacePublicRuntime({...x.options,enabled:true,guestPolicy:x.policy,cursorKey:new Uint8Array(32).fill(7),now:x.now});
 assert.equal((await r.handle('/api/staging/marketplace/detail',req)).status,503);assert.equal(x.f.commits,0);
});

test('secure native-shaped public composition serves only published DTOs under shared quota',async()=>{
 const {STAGING_MARKETPLACE_COLLECTIONS:c}=await import('../../scripts/staging-marketplace-context.mjs');
 const x=fixture(),row={id:'p',kind:'product',revision:1,title:'ગુજરાતી हिन्दी',description:'Synthetic',category:'cars',locationLabel:'Sample',basePrice:1,isSold:false,storeId:null};
 x.f.seed(c.actors,'seller',{uid:'seller',canWrite:true,suspended:false});
 x.f.seed(c.publicViews,'product_p',row);x.f.seed(c.privateRecords,'product_p',{id:'p',kind:'product',ownerUid:'seller',published:true,publicationRevision:1,publicProfile:row,privateContact:'never-public'});
 const runtime=createSecureStagingMarketplacePublicRuntime({...x.options,enabled:true,guestPolicy:x.policy,cursorKey:new Uint8Array(32).fill(7),now:x.now});
 const req={method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({kind:'product',id:'p'})};
 for(let i=0;i<3;i++){const r=await runtime.handle('/api/staging/marketplace/detail',req);assert.equal(r.status,200);assert.deepEqual(r.body.profile,row);assert.doesNotMatch(JSON.stringify(r.body),/ownerUid|never-public/);}
 assert.equal((await runtime.handle('/api/staging/marketplace/detail',req)).status,429);
});
