import {createHash} from 'node:crypto';
import {requireStagingMarketplaceBinding,STAGING_RATE_COLLECTION} from './staging-marketplace-context.mjs';
import {consumeAtomicRate} from './atomic-rate.mjs';
import {copyRecord} from './isolated-firestore-context.mjs';
// Disabled by default; reuses native transaction budget core, not process memory.
// No SDK initialization, TTL policy, reset, cleanup, credentials or cloud calls.
export function createC2StagingRunBudget({enabled=false,binding,runId,contractDigest,maxRequests,expiresAtMs,now=Date.now}={}){
 const off=async()=>({allowed:false});
 if(enabled!==true)return off;
 const b=requireStagingMarketplaceBinding(binding);
 if(typeof runId!=='string'||!/^[A-Za-z0-9_-]{1,30}$/.test(runId)||typeof contractDigest!=='string'||!/^[a-f0-9]{64}$/.test(contractDigest)||
  !Number.isSafeInteger(maxRequests)||maxRequests<1||maxRequests>20||!Number.isSafeInteger(expiresAtMs)||typeof now!=='function')throw Error('C2_BUDGET_UNAVAILABLE');
 const id=parts=>createHash('sha256').update(JSON.stringify(parts)).digest('hex');
 const contractKey=id(['oldx-c2-contract-budget-v1',runId,contractDigest]),runKey=id(['oldx-c2-run-budget-v1',runId]);
 return async(input,context={})=>{
  const r=copyRecord(input,['runId','operation','projectId','databaseId','limits','expiresAtMs']);
  const limits=copyRecord(r?.limits,['maxRequests','maxActors','maxProducts','maxPhotos']);
  const clock=now();
  if(!r||r.runId!==runId||r.projectId!=='oldx-staging'||r.databaseId!=='(default)'||r.expiresAtMs!==expiresAtMs||
   !['save','owner','archive','list','detail'].includes(r.operation)||!limits||limits.maxRequests!==maxRequests||limits.maxActors!==2||limits.maxProducts!==1||limits.maxPhotos!==1||
   context.signal?.aborted||!Number.isSafeInteger(clock)||clock<0||expiresAtMs<=clock||expiresAtMs-clock>1200000)return {allowed:false};
  // A different grant cannot reset the common run counter. Unique run IDs and
  // exact hash/retention evidence still require trusted host/owner custody.
  return consumeAtomicRate({sdk:b.sdk,db:b.db,
   actorRef:b.sdk.doc(b.db,STAGING_RATE_COLLECTION,contractKey),globalRef:b.sdk.doc(b.db,STAGING_RATE_COLLECTION,runKey),
   actorLimit:maxRequests,globalLimit:maxRequests,expiresAtMs,
   context:{signal:context.signal,deadlineAt:Math.min(clock+1000,expiresAtMs)},now});
 };
}
