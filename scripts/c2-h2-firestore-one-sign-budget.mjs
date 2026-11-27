import {createHash} from 'node:crypto';
import {requireStagingMarketplaceBinding,STAGING_RATE_COLLECTION} from './staging-marketplace-context.mjs';
import {copyRecord} from './isolated-firestore-context.mjs';

// H2S SOURCE ONLY. A dedicated, permanent, cross-instance one-sign tombstone.
// This is NOT the C2 Product request budget. It reuses only the authenticated
// Firestore transaction wrapper/allowed rate collection; no SDK/app initialization,
// Cloud calls, IAM changes, TTL policy or server listener. Default OFF.
//
// Critical: the document ID is constant for this Gateway + KeyVersion, NOT
// derived from a caller run ID, nonce or approval hash. Rotating those inputs
// must NEVER reset the one-sign quota. Do NOT delete this record for cleanup.
// No expiresAtMs / TTL timestamp is written: a TTL cleanup would reset quota.
// The future Cloud Run host must separately verify owner approval, image,
// Gateway workload identity, Firestore permissions and the trusted KMS status.
const PROJECT='oldx-staging';
const GATEWAY_UID='107238619872767759560';
const VERSION='projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1';
const PURPOSE='oldx.h2.single-synthetic-sign.v1';
const DIGEST=/^[0-9a-f]{64}$/;
const fail=()=>{throw Error('C2_H2_ONE_SIGN_BUDGET_UNAVAILABLE');};
const recordId=createHash('sha256').update(JSON.stringify([
  'oldx-h2s-permanent-global-single-sign-tombstone-v1',
  PROJECT,GATEWAY_UID,VERSION,
])).digest('hex');
const time=t=>Number.isSafeInteger(t)&&t>=0;
const denied=Object.freeze({allowed:false});

export function createC2H2OneSignFirestoreBudget({
  enabled=false,binding,approvedPlanSha256,syntheticNonceSha256,
  validFromMs,validUntilMs,now=Date.now,
}={}){
  if(enabled!==true)return async()=>denied;
  // These digest pins are matching constraints, NOT proof of Owner signature.
  // An independently approved, signed release control must authorize the host.
  if(!DIGEST.test(approvedPlanSha256)||!DIGEST.test(syntheticNonceSha256)||
     approvedPlanSha256===syntheticNonceSha256||
     !time(validFromMs)||!time(validUntilMs)||
     validUntilMs<=validFromMs||validUntilMs-validFromMs>120000||
     typeof now!=='function')fail();
  let b;
  try{b=requireStagingMarketplaceBinding(binding);}catch{fail();}
  const ref=b.sdk.doc(b.db,STAGING_RATE_COLLECTION,recordId);
  const check=(signal)=>{
    const t=now();
    if(signal?.aborted||!time(t)||t<validFromMs||t>=validUntilMs)fail();
    return t;
  };
  return async (input,{signal}={})=>{
    const data=copyRecord(input,[
      'purpose','projectId','gatewayUid','keyVersion','maxSigns',
    ]);
    if(!data||data.purpose!==PURPOSE||data.projectId!==PROJECT||
       data.gatewayUid!==GATEWAY_UID||data.keyVersion!==VERSION||
       data.maxSigns!==1||signal?.aborted)return denied;
    try{
      check(signal);
      // Existing trusted Native Admin transaction adapter retries conflicts at
      // most three times. The transaction reads the immutable global marker,
      // then sets it only when truly missing. No in-process Map/lease or reset.
      const result=await b.sdk.runTransaction(b.db,async tx=>{
        const at=check(signal);
        const previous=await tx.get(ref);
        check(signal);
        if(previous.exists())return denied;
        tx.set(ref,{
          purpose:PURPOSE,projectId:PROJECT,gatewayUid:GATEWAY_UID,
          keyVersion:VERSION,consumed:true,consumedAtMs:at,
          approvedPlanSha256,syntheticNonceSha256,
          // Deliberately NO expiresAtMs/TTL field in this permanent tombstone.
          signingWindowEndMs:validUntilMs,
        });
        check(signal);
        return {allowed:true};
      },{maxAttempts:3});
      return result?.allowed===true?Object.freeze({allowed:true}):denied;
    }catch{fail();} // Ambiguous Firestore transaction => NO KMS request.
  };
}

// Informational only; cannot be overridden by runId, approval hash or nonce.
export const C2_H2_SIGN_BUDGET_SCOPE=Object.freeze({
  projectId:PROJECT,gatewayUid:GATEWAY_UID,keyVersion:VERSION,
  purpose:PURPOSE,maxSigns:1,collection:STAGING_RATE_COLLECTION,
  globalRecordId:recordId,
});
