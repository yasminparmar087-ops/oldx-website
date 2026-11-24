import {createHash} from 'node:crypto';
import {requireStagingMarketplaceBinding,STAGING_RATE_COLLECTION} from './staging-marketplace-context.mjs';
const hex64=value=>typeof value==='string'&&/^[0-9a-f]{64}$/.test(value);
const validTime=value=>Number.isSafeInteger(value)&&value>=0;

// Standalone transaction core with no SDK initialization. Atomic, durable
// consume-once semantics are required; process memory is not suitable in host.
export async function consumeAtomicMarketplaceReplayNonce({sdk,db,nonceRef,expiresAtMs,signal,now=Date.now,retentionMs=300000}={}){
 const check=()=>{const time=now();if(signal?.aborted||!validTime(time)||time>=expiresAtMs)throw Error('Replay nonce deadline');};
 const clock=now();
 if(typeof sdk?.runTransaction!=='function'||typeof nonceRef?.path!=='string'||!validTime(clock)||!validTime(expiresAtMs)||expiresAtMs<=clock||expiresAtMs-clock>30000||!validTime(retentionMs)||retentionMs<30000||retentionMs>86400000||!validTime(expiresAtMs+retentionMs))throw Error('Replay nonce configuration denied');
 check();
 return sdk.runTransaction(db,async tx=>{
  check();const snapshot=await tx.get(nonceRef);check();
  if(typeof snapshot?.exists!=='function')throw Error('Replay snapshot unavailable');
  const exists=snapshot.exists();if(typeof exists!=='boolean')throw Error('Replay snapshot unavailable');
  if(exists)return {allowed:false};
  tx.set(nonceRef,{count:1,expiresAtMs:expiresAtMs+retentionMs});
  check();return {allowed:true};
 },{maxAttempts:3});
}

// Host is source-only and disabled by default; enabling a real nonce write
// requires finite all-provider cost, TTL/cleanup and exact owner approval.
// Expiry metadata does NOT configure Firestore TTL automatically.
export function createStagingMarketplaceReplayNonce({enabled=false,binding,now=Date.now,retentionMs=300000}={}){
 if(enabled!==true)return async()=>({allowed:false});
 const b=requireStagingMarketplaceBinding(binding);
 if(typeof now!=='function'||!validTime(retentionMs)||retentionMs<30000||retentionMs>86400000)throw Error('Replay adapter unavailable');
 return async({nonceHash,expiresAtMs,signal}={})=>{
  if(!hex64(nonceHash))throw Error('Replay nonce invalid');
  const name=createHash('sha256').update(JSON.stringify(['oldx-marketplace-request-replay-v1',nonceHash])).digest('hex');
  const nonceRef=b.sdk.doc(b.db,STAGING_RATE_COLLECTION,name);
  return consumeAtomicMarketplaceReplayNonce({sdk:b.sdk,db:b.db,nonceRef,expiresAtMs,signal,now,retentionMs});
 };
}
