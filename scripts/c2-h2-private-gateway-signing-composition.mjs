import {requireC2H2LifecycleStageLedger} from './c2-h2-lifecycle-stage-ledger.mjs';
import {createHash,createPublicKey} from 'node:crypto';
import {requireC2H2MultiSignLifecyclePolicy} from './c2-h2-lifecycle-signing-status-contract.mjs';
import {parseMarketplaceCanonicalProofPayload} from './marketplace-gateway-request-proof.mjs';
import {c2LifecycleBoundary} from './c2-h2-lifecycle-boundary.mjs';
import {createC2KmsRequestSigning} from './c2-kms-request-signing.mjs';
import {createC2H2GatewayKmsSyntheticTransport} from './c2-h2-gateway-kms-synthetic-transport.mjs';

// SERVER-ONLY, H2S SOURCE COMPOSITION. No Cloud Run listener, runtime auth,
// user-controlled configuration, HTTP client, SDK initialization or side effect.
// Only trusted host providers may be injected. No public route is registered.
// This prepares the requestSigning option of createC2PrivateGatewayHost.
// Cloud Run's attached service identity, revision/image/Invoker and audiences
// MUST be independently verified outside this module before any enabled use.
export const C2_H2_GATEWAY_IDENTITY='oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
export const C2_H2_GATEWAY_UID='107238619872767759560';
export const C2_H2_KMS_KEY_VERSION='projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1';
export const C2_H2_KMS_SPKI_SHA256='69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba';
export const C2_H2_KMS_KID='oldx_c2_h2_kms_1';
const ALGORITHM='RSA_SIGN_PKCS1_2048_SHA256';
const fail=()=>{throw Error('C2_H2_SIGNING_UNAVAILABLE');};
const safeTime=n=>Number.isSafeInteger(n)&&n>=0;

// A trusted independent status provider is mandatory. This module does NOT
// derive key state from the signing role, a KMS sign response, or a user field.
// In particular roles/cloudkms.signer does NOT authorize getVersion/publicKey.
// The prior H2N public PEM remains a trusted *host-side* secret-free input;
// compare its DER SPKI SHA-256 to the pinned fingerprint before enabling.
//
// All three ports below must come from the trusted private Gateway host:
//   - getTrustedWorkloadCredential: Cloud Run metadata-issued Gateway identity
//   - fetchKms: bounded Google KMS HTTPS transport
//   - consumeDurableSignBudget: real atomic, cross-instance one-shot ledger
// And getTrustedKeyVersionStatus must be separately verified by a principal
// with valid metadata-read authority. No fake status or widened IAM permitted.
export function createC2H2PrivateGatewaySigning({
  enabled=false,runtimeServiceAccount,runtimeServiceAccountUid,publicKeyPem,
  validFromMs,validUntilMs,getTrustedWorkloadCredential,fetchKms,
  consumeDurableSignBudget,getTrustedKeyVersionStatus,now=Date.now,
}={}){
  const approvedWindow=enabled===true&&
    runtimeServiceAccount===C2_H2_GATEWAY_IDENTITY&&
    runtimeServiceAccountUid===C2_H2_GATEWAY_UID&&
    safeTime(validFromMs)&&safeTime(validUntilMs)&&
    validUntilMs>validFromMs&&validUntilMs-validFromMs<=120000&&
    typeof now==='function'&&
    [getTrustedWorkloadCredential,fetchKms,consumeDurableSignBudget,
     getTrustedKeyVersionStatus].every(fn=>typeof fn==='function');

  const transport=createC2H2GatewayKmsSyntheticTransport({
    enabled:approvedWindow,expectedGatewayEmail:runtimeServiceAccount,
    expectedGatewayUid:runtimeServiceAccountUid,
    keyVersion:C2_H2_KMS_KEY_VERSION,getTrustedWorkloadCredential,
    fetchKms,consumeDurableSignBudget,now,
  });
  const signing=createC2KmsRequestSigning({
    enabled:approvedWindow&&transport.ready,
    kid:C2_H2_KMS_KID,keyVersion:C2_H2_KMS_KEY_VERSION,
    algorithm:ALGORITHM,publicKeyPem,
    publicKeySha256:C2_H2_KMS_SPKI_SHA256,
    validFromMs,validUntilMs,
    asymmetricSign:transport.asymmetricSign,
    getKeyVersionStatus:getTrustedKeyVersionStatus,
    now,
  });
  const ready=approvedWindow&&transport.ready&&signing.ready;
  const requestSigning=ready?Object.freeze({
    kid:C2_H2_KMS_KID,
    async signMessage(bytes,{kid,signal}={}){
      if(kid!==C2_H2_KMS_KID||signal?.aborted)fail();
      try{return await signing.signMessage(bytes,{kid,signal});}
      catch{fail();}
    },
  }):Object.freeze({});
  return Object.freeze({
    ready,
    requestSigning,
    runtimeServiceAccount:ready?C2_H2_GATEWAY_IDENTITY:null,
    keyVersion:ready?C2_H2_KMS_KEY_VERSION:null,
  });
}

const lifecycleSigners=new WeakSet();
export function requireC2H2LifecycleRequestSigning(value){
  if(!lifecycleSigners.has(value))throw Error('C2_LIFECYCLE_SIGNING_BLOCKED');return value;
}
// Separate FUTURE bounded multi-sign source provider. Never calls/recreates the
// legacy one-sign transport. Missing actual pin/status/authority stays BLOCKED.
// getStageContext is server request context, not a browser capability/header.
export function createC2H2LifecycleRequestSigning({enabled=false,policy,ledger,
  getStageContext,publicKeyPem,getTrustedKeyVersionStatus,asymmetricSign,
  now=Date.now}={}) {
  const off=Object.freeze({ready:false});
  if(enabled!==true)return off;
  let p;try{p=requireC2H2MultiSignLifecyclePolicy(policy);requireC2H2LifecycleStageLedger(ledger,p);}catch{return off;}
  if(ledger?.ready!==true||typeof ledger.claimSign!=='function'||
     [getStageContext,getTrustedKeyVersionStatus,asymmetricSign,now].some(x=>typeof x!=='function'))return off;
  const signing=createC2KmsRequestSigning({enabled:true,kid:C2_H2_KMS_KID,
    keyVersion:p.keyVersion,algorithm:'RSA_SIGN_PKCS1_2048_SHA256',publicKeyPem,
    publicKeySha256:p.keyPublicSpkiSha256,validFromMs:p.startsAtMs,validUntilMs:p.expiresAtMs,
    getKeyVersionStatus:getTrustedKeyVersionStatus,asymmetricSign,now});
  if(!signing.ready)return off;
  const result=Object.freeze({ready:true,kid:C2_H2_KMS_KID,
    async signMessage(bytes,{kid,signal}={}) {
      const snapshot=Buffer.from(bytes),proof=parseMarketplaceCanonicalProofPayload(snapshot);
      if(!proof||proof.kid!==C2_H2_KMS_KID||kid!==C2_H2_KMS_KID)throw Error('C2_LIFECYCLE_SIGNING_BLOCKED');
      return c2LifecycleBoundary(async sig=>{
        const ctx=await getStageContext({signal:sig});
        const claim=await ledger.claimSign({reservation:ctx?.reservation,
          proofSha256:createHash('sha256').update(snapshot).digest('hex'),
          bodyHash:proof.bodyHash,authHash:proof.authHash,path:proof.path},{signal:sig});
        if(claim?.allowed!==true||sig.aborted)throw Error('C2_LIFECYCLE_SIGNING_BLOCKED');
        // Durable attempt claimed BEFORE any status/sign call. Ambiguous result
        // consumes it; no repeat on another process or with a new provider.
        return signing.signMessage(snapshot,{kid,signal:sig});
      },{signal,timeoutMs:1000});
    }});
  lifecycleSigners.add(result);return result;
}

const lifecycleProofKeys=new WeakMap();
export function requireC2H2LifecycleProofKeyResolver(value,policy){
  if(lifecycleProofKeys.get(value)!==policy)throw Error('C2_LIFECYCLE_PROOF_KEY_BLOCKED');return value;
}
// BACKEND-only verification key provider. NO KMS signing port/credential.
// Separate independently authenticated status transport must use usage=verify.
export function createC2H2LifecycleProofKeyResolver({enabled=false,policy,publicKeyPem,
  getTrustedKeyVersionStatus,now=Date.now}={}) {
  if(enabled!==true)return null;
  let p,key;
  try{
    p=requireC2H2MultiSignLifecyclePolicy(policy);key=createPublicKey(publicKeyPem);
    if(key.type!=='public'||key.asymmetricKeyType!=='rsa'||
       key.asymmetricKeyDetails?.modulusLength!==2048||
       key.asymmetricKeyDetails?.publicExponent!==65537n||
       createHash('sha256').update(key.export({type:'spki',format:'der'})).digest('hex')!==p.keyPublicSpkiSha256||
       typeof getTrustedKeyVersionStatus!=='function'||typeof now!=='function')return null;
  }catch{return null;}
  const result=async({kid,signal}={})=>c2LifecycleBoundary(async sig=>{
    const fresh=()=>{const t=now();if(sig.aborted||!Number.isSafeInteger(t)||
      t<p.startsAtMs||t>=p.expiresAtMs)throw Error('C2_LIFECYCLE_PROOF_KEY_BLOCKED');};
    fresh();if(kid!==C2_H2_KMS_KID)throw Error('C2_LIFECYCLE_PROOF_KEY_BLOCKED');
    const status=await getTrustedKeyVersionStatus({name:p.keyVersion,signal:sig});fresh();
    if(status?.name!==p.keyVersion||status.state!=='ENABLED'||
       status.algorithm!=='RSA_SIGN_PKCS1_2048_SHA256'||
       status.publicKeySha256!==p.keyPublicSpkiSha256)throw Error('C2_LIFECYCLE_PROOF_KEY_BLOCKED');
    return key;
  },{signal,timeoutMs:600});
  lifecycleProofKeys.set(result,p);return result;
}
