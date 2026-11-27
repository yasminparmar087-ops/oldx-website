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
