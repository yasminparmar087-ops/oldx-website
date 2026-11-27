import {createC2H2GatewayHostSource} from './c2-h2-gateway-host-source.mjs';
import {createC2H2GatewayMetadataAccessToken} from
  '../../scripts/c2-h2-cloud-run-gateway-access-token.mjs';
import {C2_H2_GATEWAY_IDENTITY,C2_H2_GATEWAY_UID} from
  '../../scripts/c2-h2-private-gateway-signing-composition.mjs';

// SOURCE ONLY, never registered as an HTTP route. This is a binder for a
// future independently verified private Cloud Run Gateway revision, not proof
// of its identity, public endpoint authorization or deployed image provenance.
// No SDK/credential/network action occurs on import or factory construction.
//
// getTrustedKeyVersionStatus MUST be independently sourced (Gateway signer
// role cannot read version metadata), and consumeDurableSignBudget MUST be a
// real cross-instance atomic transaction, NOT an in-memory callback.
const denied=()=>Object.freeze({
  ready:false,
  async fetch(){return Response.json({ok:false,error:{
    code:'H2_GATEWAY_NOT_AUTHORIZED'}},{status:503,headers:{
    'cache-control':'private, no-store'}});},
});
export function createC2H2MetadataBoundPrivateGatewayHostSource({
  enabled=false,hostOptions,fetchMetadata,now=Date.now,
}={}){
  if(enabled!==true||!hostOptions||
     Object.getPrototypeOf(hostOptions)!==Object.prototype||
     Reflect.ownKeys(hostOptions).includes('getTrustedWorkloadCredential')||
     hostOptions.runtimeServiceAccount!==C2_H2_GATEWAY_IDENTITY||
     hostOptions.runtimeServiceAccountUid!==C2_H2_GATEWAY_UID||
     typeof fetchMetadata!=='function'||typeof now!=='function')return denied();

  const metadata=createC2H2GatewayMetadataAccessToken({
    enabled:true,
    serviceAccount:C2_H2_GATEWAY_IDENTITY,
    serviceAccountUid:C2_H2_GATEWAY_UID,
    fetchMetadata,now,
  });
  if(!metadata.ready)return denied();
  // Do not fall back to caller-provided credentials, ADC or Owner WSL OAuth.
  // Source host will remain disabled if KMS PEM, trusted key state, real
  // transactional sign budget, Cloud Run identity/Invoker ports are absent.
  const host=createC2H2GatewayHostSource({
    ...hostOptions,enabled:true,now,
    getTrustedWorkloadCredential:metadata.getTrustedWorkloadCredential,
  });
  return Object.freeze({ready:host.ready,fetch:request=>host.fetch(request)});
}
