import {requireC2H2MultiSignLifecyclePolicy} from '../../scripts/c2-h2-lifecycle-signing-status-contract.mjs';
import {requireC2H2LifecycleStageLedger} from '../../scripts/c2-h2-lifecycle-stage-ledger.mjs';
import {requireC2EnabledReleaseControl} from '../../scripts/c2-enabled-release-control.mjs';
import {createAttestedMarketplaceGateway,createTrustedMarketplaceBackend} from './trusted-host.mjs';
import {createStagingMarketplaceRuntime} from './runtime.mjs';
import {createSecureStagingMarketplacePublicRuntime} from './public-runtime.mjs';
import {createGoogleGatewayPublicKeyResolver} from '../../scripts/google-gateway-public-keys.mjs';
import {createGatewayAttestationVerifier} from '../../scripts/gateway-attestation.mjs';
import {createMarketplaceRequestProofSigner,createMarketplaceRequestProofVerifier} from '../../scripts/marketplace-gateway-request-proof.mjs';
import {createProofBoundGatewayHop,createProofBoundBackendHop} from '../../scripts/marketplace-proof-bound-hop.mjs';
import {createStagingMarketplaceBinding} from '../../scripts/staging-marketplace-context.mjs';
import {createStagingMarketplaceReplayNonce} from '../../scripts/staging-marketplace-replay-nonce.mjs';
import {createStagingMarketplaceEnforcement} from '../../scripts/provider-enforcement-adapters.mjs';
import {createStagingMarketplaceRate} from '../../scripts/staging-marketplace-rate.mjs';
import {createStagingMarketplaceGuestRate} from '../../scripts/staging-marketplace-guest-rate.mjs';
import {createMarketplacePublicCursor} from '../../scripts/marketplace-public-cursor.mjs';
import {createStagingMarketplaceMedia} from '../../scripts/staging-marketplace-media.mjs';
// Source-only factories, no listener, environment, SDK init, token mint or fetch.
// Trusted host explicitly supplies all providers. Browser controls NONE of them.
export function createStep05Gateway({enabled=false,requestSigning={},fetchBackend,now=Date.now,...options}={}){
 if(enabled!==true||typeof fetchBackend!=='function')return createAttestedMarketplaceGateway();
 const signer=createMarketplaceRequestProofSigner({...requestSigning,enabled:true,now});
 if(typeof signer!=='function')return createAttestedMarketplaceGateway();
 const hop=createProofBoundGatewayHop({enabled:true,backendOrigin:options.backendOrigin,signRequestProof:signer,fetchBackend});
 return createAttestedMarketplaceGateway({...options,enabled:true,now,fetchBackend:hop});
}
function composeStep05Backend({enabled=false,audience,gatewayServiceAccount,googleIdentity={},requestVerification={},runtimeOptions={},guestPolicy,cursorKey,nonceRetentionMs=300000,now=Date.now}={},publicationEnabled=false){
 const off=()=>createTrustedMarketplaceBackend();
 if(enabled!==true)return off();
 try{
  const options={...runtimeOptions,now};
  if(options.adminAuth?.app?.options?.projectId!=='oldx-staging'||typeof options.adminAuth.verifyIdToken!=='function')return off();
  const binding=createStagingMarketplaceBinding(options);
  // Validate quota/cursor configuration without any reads or writes.
  createStagingMarketplaceRate({binding,policy:options.ratePolicy,now});
  createStagingMarketplaceGuestRate({enabled:true,binding,policy:guestPolicy,now});
  createMarketplacePublicCursor({key:cursorKey,now});
  const googleKeys=createGoogleGatewayPublicKeyResolver({enabled:true,issuer:googleIdentity.issuer,fetchRequest:googleIdentity.fetchRequest,now});
  if(typeof googleKeys!=='function'||typeof requestVerification.resolvePublicKey!=='function')return off();
  // Google OAuth keys verify ONLY the identity assertion. The independent
  // request signer MUST supply its matching public keys through the other port.
  const verifyIdentity=createGatewayAttestationVerifier({...googleIdentity,enabled:true,
   resolvePublicKey:googleKeys,iamAudience:audience,expectedPrincipal:gatewayServiceAccount,now});
  if(typeof verifyIdentity!=='function')return off();
  const consumeNonce=createStagingMarketplaceReplayNonce({enabled:true,binding,retentionMs:nonceRetentionMs,now});
  const auth=createStagingMarketplaceEnforcement({enabled:true,adminAuth:options.adminAuth,now});
  let lifecycleLedger=null;
  if(requestVerification.lifecycleLedger!==undefined||requestVerification.lifecyclePolicy!==undefined){
    const policy=requireC2H2MultiSignLifecyclePolicy(requestVerification.lifecyclePolicy);
    lifecycleLedger=requireC2H2LifecycleStageLedger(requestVerification.lifecycleLedger,policy);
  }
  const authorizeBeforeNonce=async({path,authorization,bodyHash,authHash,proofSha256},{signal})=>{
   const guest=path.endsWith('/list')||path.endsWith('/detail');
   if(guest&&authorization!==null)return false;
   if(!guest){
     if(typeof authorization!=='string'||!authorization.startsWith('Bearer '))return false;
     try{if(!await auth.verifyFirebaseToken(authorization.slice(7),{checkRevoked:true,signal}))return false;}catch{return false;}
   }
   // AFTER independently verified identity, canonical RSA proof and Firebase
   // auth; BEFORE nonce or Product writes. Never accepts a browser grant.
   if(lifecycleLedger)return (await lifecycleLedger.claimBackend({path,bodyHash,authHash,proofSha256},{signal}))?.allowed===true;
   return true;
  };
  const proof=createMarketplaceRequestProofVerifier({...requestVerification,enabled:true,consumeNonce,authorizeBeforeNonce,now});
  if(typeof proof!=='function')return off();
  const commandRuntime=createStagingMarketplaceRuntime({...options,enabled:true,publicationEnabled,
   createMediaBindings:options.createMediaBindings??(b=>createStagingMarketplaceMedia({enabled:true,binding:b}))});
  const publicRuntime=createSecureStagingMarketplacePublicRuntime({...options,enabled:true,guestPolicy,cursorKey});
  const inner=createTrustedMarketplaceBackend({enabled:true,audience,gatewayServiceAccount,
   verifyInvoker:verifyIdentity,commandRuntime,publicRuntime,now});
  return createProofBoundBackendHop({enabled:true,audience,gatewayServiceAccount,verifyAttestation:verifyIdentity,verifyRequestProof:proof,backend:inner,now});
 }catch{return off();}
}

// Existing contract/deployed callers ALWAYS remain publication-OFF.
export const createStep05Backend=options=>composeStep05Backend(options,false);
// Future H2 SOURCE composition only; no SDK/listener/env or operational approval.
// Real host must independently verify runtime SA/IAM and bind trusted providers.
export function createC2EnabledProductBackend({enabled=false,releaseControl,runtimeServiceAccount,runtimeImage,...options}={}){
 const off=()=>createTrustedMarketplaceBackend();
 if(enabled!==true)return off();
 try{
  const control=requireC2EnabledReleaseControl(releaseControl);
  if(runtimeServiceAccount!==control.runtimePrincipal||runtimeImage!==control.runtimeImage||typeof options.runtimeOptions?.createMediaBindings!=='function')return off();
  if(options.requestVerification?.lifecyclePolicy!==undefined){
    const policy=requireC2H2MultiSignLifecyclePolicy(options.requestVerification.lifecyclePolicy);
    requireC2H2LifecycleStageLedger(options.requestVerification.lifecycleLedger,policy);
    if(control.productId!=='c2_'+policy.runId+'_product'||
       !policy.phases.every(stage=>control.isActorAllowed(stage.actor)))return off();
  }
  const original=options.runtimeOptions.adminAuth;
  if(typeof original?.verifyIdToken!=='function')return off();
  const adminAuth={app:original.app,async verifyIdToken(...args){
   const claims=await original.verifyIdToken(...args);
   if(!control.isActorAllowed(claims?.uid))throw Error('C2_ACTOR_SCOPE_DENIED');
   return claims;
  }};
  return control.wrap(composeStep05Backend({...options,enabled:true,runtimeOptions:{...options.runtimeOptions,
   adminAuth,allocateId:()=>control.productId,productScopeId:control.productId}},true));
 }catch{return off();}
}
