import test from 'node:test';
import assert from 'node:assert/strict';
import {consumeAtomicMarketplaceReplayNonce,createStagingMarketplaceReplayNonce} from '../../scripts/staging-marketplace-replay-nonce.mjs';
const nonceRef={path:'marketplaceRateLimits_v1/noncetest'};
function database(){
 const docs=new Map();let chain=Promise.resolve(),transactions=0;
 const sdk={async runTransaction(_db,callback,opts){
  assert.equal(opts.maxAttempts,3);transactions++;
  let release;const tail=new Promise(resolve=>release=resolve);const prev=chain;chain=chain.then(()=>tail);
  await prev;
  try{
   const changes=new Map();const tx={
    async get(ref){return {exists:()=>docs.has(ref.path),data:()=>docs.get(ref.path)};},
    set(ref,value){changes.set(ref.path,value);}
   };
   const result=await callback(tx);
   for(const [key,val] of changes)docs.set(key,val);
   return result;
  }finally{release();}
 }};
 return {sdk,docs,get transactions(){return transactions;}};
}
test('two competing transaction consumers cannot accept the same nonce twice',async()=>{
 const d=database(),now=()=>1000,params={sdk:d.sdk,db:d,nonceRef,expiresAtMs:16000,now,retentionMs:30000};
 const [a,b]=await Promise.all([consumeAtomicMarketplaceReplayNonce(params),consumeAtomicMarketplaceReplayNonce(params)]);
 assert.equal([a.allowed,b.allowed].filter(Boolean).length,1);
 assert.equal(d.transactions,2);
 assert.deepEqual(d.docs.get(nonceRef.path),{count:1,expiresAtMs:46000});
 const third=await consumeAtomicMarketplaceReplayNonce(params);assert.equal(third.allowed,false);
});
test('invalid expiry, aborted requests and failed storage never grant nonce access',async()=>{
 const d=database(),base={sdk:d.sdk,db:d,nonceRef,now:()=>1000};
 await assert.rejects(()=>consumeAtomicMarketplaceReplayNonce({...base,expiresAtMs:1000}));
 await assert.rejects(()=>consumeAtomicMarketplaceReplayNonce({...base,expiresAtMs:50000}));
 const signal=new AbortController();signal.abort();
 await assert.rejects(()=>consumeAtomicMarketplaceReplayNonce({...base,expiresAtMs:5000,signal:signal.signal}));
 const broken={runTransaction:async()=>{throw Error('commit failed');}};
 await assert.rejects(()=>consumeAtomicMarketplaceReplayNonce({...base,sdk:broken,expiresAtMs:5000}));
 assert.equal(d.docs.size,0);
 assert.deepEqual(await createStagingMarketplaceReplayNonce()(),{allowed:false});
});
