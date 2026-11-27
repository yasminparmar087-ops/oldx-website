import {createC2PrivateGatewayHost} from './c2-website-mediation.mjs';
import {createC2H2PrivateGatewaySigning,
  C2_H2_GATEWAY_IDENTITY,C2_H2_GATEWAY_UID} from
  '../../scripts/c2-h2-private-gateway-signing-composition.mjs';

// SOURCE-ONLY, DEFAULT OFF. This factory creates no Cloud Run deployment,
// no HTTP listener, no Firebase SDK app and no public route. Never use a
// browser-provided config. Successful shape checks below are NOT Cloud Run IAM
// or image provenance verification; Owner must separately inspect actual
// service/revision/Invoker, workload SA UID and immutable image digest.
const MEDIATOR='oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com';
const hostUnavailable=()=>Object.freeze({
  ready:false,
  async fetch(){return Response.json({ok:false,error:{
    code:'H2_GATEWAY_NOT_AUTHORIZED'}},{status:503,headers:{
    'cache-control':'private, no-store'}});},
});
const exactOrigin=v=>{try{const u=new URL(v);return u.protocol==='https:'&&u.origin===v&&!u.username&&!u.password&&!u.search&&!u.hash&&u.pathname==='/';}catch{return false;}};
const audience=v=>typeof v==='string'&&v.length>=1&&v.length<=512&&
  !/[\s\u0000-\u001f\u007f]/.test(v);
const origins=v=>Array.isArray(v)&&v.length>0&&v.length<=8&&v.every(exactOrigin);
const hostImage=s=>typeof s==='string'&&
  /^asia-south1-docker\.pkg\.dev\/oldx-staging\/oldx-staging-images\/[a-z0-9][a-z0-9_-]{0,80}@sha256:[a-f0-9]{64}$/.test(s)&&
  !['576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e',
    '612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a'].some(v=>s.endsWith(v));

// This composes the EXISTING private gateway host; no product publication is
// activated here. Provider callbacks are injected by a separately approved
// trusted server deployment and MUST NOT be substituted with Owner credentials
// or an in-memory one-sign ledger. The signer stays off without a real SPKI
// PEM, independently trusted version status, metadata credential and budget.
export function createC2H2GatewayHostSource({
  enabled=false,runtimeServiceAccount,runtimeServiceAccountUid,runtimeImage,
  privateGatewayOrigin,mediatorPrincipal,websiteIdentity,allowedOrigins,
  gatewayOptions={},publicKeyPem,validFromMs,validUntilMs,
  getTrustedWorkloadCredential,fetchKms,consumeDurableSignBudget,
  getTrustedKeyVersionStatus,now=Date.now,
}={}){
  if(enabled!==true||runtimeServiceAccount!==C2_H2_GATEWAY_IDENTITY||
     runtimeServiceAccountUid!==C2_H2_GATEWAY_UID||
     !gatewayOptions||typeof gatewayOptions!=='object'||Array.isArray(gatewayOptions)||
     !hostImage(runtimeImage)||mediatorPrincipal!==MEDIATOR||
     !exactOrigin(privateGatewayOrigin)||!origins(allowedOrigins)||
     !exactOrigin(gatewayOptions?.backendOrigin)||
     gatewayOptions.backendOrigin===privateGatewayOrigin||
     !audience(gatewayOptions?.attestationAudience)||
     gatewayOptions.attestationAudience===gatewayOptions.backendOrigin||
     gatewayOptions.attestationAudience===websiteIdentity?.attestationAudience||
     websiteIdentity?.identityType!=='google-service-account'||
     websiteIdentity?.expectedPrincipal!==undefined&&
       websiteIdentity.expectedPrincipal!==MEDIATOR||
     websiteIdentity?.expectedSubject!=='100779414920484819274'||
     !audience(websiteIdentity?.attestationAudience)||
     !['https://accounts.google.com','accounts.google.com'].includes(websiteIdentity?.issuer)||
     typeof websiteIdentity?.fetchRequest!=='function'||
     [gatewayOptions?.getInvokerCredential,gatewayOptions?.getGatewayAttestation,
       gatewayOptions?.fetchBackend].some(v=>typeof v!=='function')||
     gatewayOptions?.gatewayServiceAccount!==C2_H2_GATEWAY_IDENTITY)
    return hostUnavailable();
  const signer=createC2H2PrivateGatewaySigning({
    enabled:true,runtimeServiceAccount,runtimeServiceAccountUid,
    publicKeyPem,validFromMs,validUntilMs,
    getTrustedWorkloadCredential,fetchKms,consumeDurableSignBudget,
    getTrustedKeyVersionStatus,now,
  });
  if(!signer.ready)return hostUnavailable();
  // Private request mediation, Google IAM audience + signed identity checks
  // still come from the EXISTING createC2PrivateGatewayHost source.
  const host=createC2PrivateGatewayHost({
    enabled:true,privateGatewayOrigin,mediatorPrincipal,
    websiteIdentity,allowedOrigins,now,
    gatewayOptions:{...gatewayOptions,requestSigning:signer.requestSigning},
  });
  // This is source composition readiness, not deployment/IAM readiness.
  return Object.freeze({ready:true,fetch:request=>host.fetch(request)});
}
