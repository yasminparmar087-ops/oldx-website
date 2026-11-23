import {createHash} from 'node:crypto';
import {requireStagingMarketplaceBinding,STAGING_RATE_COLLECTION} from './staging-marketplace-context.mjs';
import {consumeAtomicRate} from './atomic-rate.mjs';
// Independently enforced anonymous POOL, not per-person identity/fairness.
// Both counters live in one Firestore transaction, shared across all instances.
// No IP, forwarded header, caller UID, process counters or new provider.
export function createStagingMarketplaceGuestRate({enabled=false,binding,policy,now=Date.now}={}){
 if(enabled!==true)return async()=>({allowed:false});
 const b=requireStagingMarketplaceBinding(binding);
 if(!policy||!['windowMs','guestLimit','globalLimit'].every(k=>Number.isSafeInteger(policy[k])&&policy[k]>0)||policy.windowMs<1000||policy.windowMs>600000||policy.guestLimit>policy.globalLimit||policy.globalLimit>1000000)throw Error('Guest quota unavailable');
 const {windowMs,guestLimit,globalLimit}=policy;
 return async(input,context)=>{
  if(!['marketplace.public.list','marketplace.public.detail'].includes(input?.operation))throw Error('Guest operation denied');
  const clock=now();
  if(!Number.isSafeInteger(clock)||clock<0||!Number.isSafeInteger(clock+2*windowMs)||context?.signal?.aborted||!Number.isSafeInteger(context?.deadlineAt)||clock>=context.deadlineAt)throw Error('Guest quota stopped');
  const bucket=Math.floor(clock/windowMs),key=scope=>createHash('sha256').update(JSON.stringify(['marketplace-guest-v1',scope,bucket])).digest('hex');
  return consumeAtomicRate({sdk:b.sdk,db:b.db,actorRef:b.sdk.doc(b.db,STAGING_RATE_COLLECTION,key('anonymous-pool')),globalRef:b.sdk.doc(b.db,STAGING_RATE_COLLECTION,key('global')),actorLimit:guestLimit,globalLimit,expiresAtMs:(bucket+2)*windowMs,context,now});
 };
}

