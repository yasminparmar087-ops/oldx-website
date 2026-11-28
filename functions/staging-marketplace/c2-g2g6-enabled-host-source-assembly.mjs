import {createC2CloudRunMetadataIdentity} from '../../scripts/c2-cloud-run-metadata-identity.mjs';
import {requireC2EnabledReleaseControl} from '../../scripts/c2-enabled-release-control.mjs';
import {createC2EnabledProductBackend} from './secure-product-pipeline.mjs';
import {createC2WebsiteMediator} from './c2-website-mediation.mjs';
import {createC2WebsiteNodeHandler} from './c2-website-node-http.mjs';
import {createC2H2MetadataBoundPrivateGatewayHostSource} from './c2-h2-gateway-runtime-credential-source.mjs';

// SOURCE-ONLY integration of EXISTING trusted factories. No listener or
// deployment, no ambient credentials/SDK, no KMS/Firestore on import/create.
// A 'sourceComposed' value is NOT proof of runtime IAM, deployed image,
// approval, trusted KeyVersion reader, durable quota or a hosted HTTP result.
// Unlike the previously deployed immutable H2U OFF handler, this is a NEW
// separate potential future revision, never a mutation of H2U's container.
const PROJ='oldx-staging';
const MED='oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com';
const MED_UID='100779414920484819274';
const GATE='oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
const GATE_UID='107238619872767759560';
const BACK='oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com';
const BACK_UID='106984791114720194680';
const oldOffDigests=new Set([
 '576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e',
 '612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a',
 '4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2',
]);
const plain=v=>v!==null&&typeof v==='object'&&
  !Array.isArray(v)&&Object.getPrototypeOf(v)===Object.prototype;
const image=v=>typeof v==='string'&&
  /^asia-south1-docker\.pkg\.dev\/oldx-staging\/oldx-staging-images\/[a-z0-9][a-z0-9_-]{0,80}@sha256:[a-f0-9]{64}$/.test(v)&&
  !oldOffDigests.has(v.slice(-64));
const role=(x,email,uid)=>data(x)&&x.principal===email&&x.uid===uid&&image(x.image);
// Prevent getter-backed browser/config objects or incomplete host ports from
// making a source assembly appear ready. Callbacks remain host-owned and must
// still be verified by independently approved runtime bindings.
const data=v=>plain(v)&&Reflect.ownKeys(v).every(k=>
  typeof k==='string'&&Object.hasOwn(Object.getOwnPropertyDescriptor(v,k),'value'));
const funcs=(obj,names)=>data(obj)&&names.every(k=>typeof obj[k]==='function');
const gatewayPorts=[
  'fetchKms','consumeDurableSignBudget','getTrustedKeyVersionStatus',
];
const webPorts=[
  'getGatewayInvokerCredential','getWebsiteAttestation',
  'consumeGuestAdmission','fetchPrivateGateway',
];
const gatewayHopPorts=[
  'getInvokerCredential','getGatewayAttestation','fetchBackend',
];
const offFetch=async()=>Response.json({ok:false,error:{code:'C2_G2_G6_NOT_AUTHORIZED'}},{
  status:503,headers:{'cache-control':'private, no-store','x-content-type-options':'nosniff'}});
const off=()=>Object.freeze({
  sourceComposed:false,
  reason:'MISSING_TRUSTED_HOST_OR_RELEASE_BOUNDARY',
  websiteHandler:createC2WebsiteNodeHandler(),
  gateway:Object.freeze({ready:false,fetch:offFetch}),
  backend:Object.freeze({fetch:offFetch}),
});

// Bind three *distinct* host processes' existing factories behind the same
// APPROVED synthetic release control. A caller MUST provide real, separately
// validated runtime metadata and restricted privileged callback ports;
// injected strings are not a substitute for such live validation.
// A successful source composition never turns on existing Cloud Run services.
export function createC2G2G6EnabledHostSourceAssembly({
  enabled=false,releaseControl,hostFacts,
  websiteOptions,gatewayHostOptions,backendOptions,
  fetchGatewayMetadata,now=Date.now,
}={}){
  if(enabled!==true||!data(hostFacts)||Object.keys(hostFacts).sort().join(',')!=='backend,gateway,mediator'||!data(websiteOptions)||
      !data(gatewayHostOptions)||!data(backendOptions)||
      !role(hostFacts.mediator,MED,MED_UID)||
      !role(hostFacts.gateway,GATE,GATE_UID)||
      !role(hostFacts.backend,BACK,BACK_UID)||
      new Set(Object.values(hostFacts).map(x=>x?.image)).size!==3||
      typeof fetchGatewayMetadata!=='function'||typeof now!=='function'||
      !funcs(websiteOptions,webPorts)||
      !funcs(gatewayHostOptions,gatewayHostOptions.lifecycleRequestSigning===undefined?gatewayPorts:[])||
      !funcs(gatewayHostOptions.gatewayOptions,gatewayHopPorts)||
      !data(gatewayHostOptions.websiteIdentity)||
      typeof gatewayHostOptions.websiteIdentity.fetchRequest!=='function'||
      !data(backendOptions.runtimeOptions)||
      !data(backendOptions.googleIdentity)||
      typeof backendOptions.googleIdentity.fetchRequest!=='function'||
      !data(backendOptions.requestVerification)||
      typeof backendOptions.requestVerification.resolvePublicKey!=='function'||
      typeof backendOptions.runtimeOptions?.adminAuth?.verifyIdToken!=='function'||
      typeof backendOptions.runtimeOptions?.adminFirestore?.runTransaction!=='function'||
      typeof backendOptions.runtimeOptions?.createMediaBindings!=='function'||
      typeof backendOptions.verifyApproval==='function'||
      backendOptions.runtimeServiceAccount!==undefined||
      backendOptions.runtimeImage!==undefined||
      backendOptions.releaseControl!==undefined||
      gatewayHostOptions.enabled!==undefined||
      websiteOptions.enabled!==undefined)return off();
  let control;
  try{control=requireC2EnabledReleaseControl(releaseControl);}
  catch{return off();}
  if(!control.hostBindings||!['mediator','gateway','backend'].every(role=>
      control.hostBindings.principals[role]===hostFacts[role].principal&&
      control.hostBindings.images[role]===hostFacts[role].image)||
      control.runtimePrincipal!==BACK||control.runtimeImage!==hostFacts.backend.image||
      gatewayHostOptions.runtimeServiceAccount!==GATE||
      gatewayHostOptions.runtimeServiceAccountUid!==GATE_UID||
      gatewayHostOptions.runtimeImage!==hostFacts.gateway.image||
      gatewayHostOptions.gatewayOptions?.gatewayServiceAccount!==GATE||
      gatewayHostOptions.mediatorPrincipal!==MED||
      websiteOptions.mediatorPrincipal!==MED||
      websiteOptions.privateGatewayOrigin!==gatewayHostOptions.privateGatewayOrigin||
      !Array.isArray(websiteOptions.allowedOrigins)||
      JSON.stringify(websiteOptions.allowedOrigins)!==
        JSON.stringify(gatewayHostOptions.allowedOrigins)||
      websiteOptions.websiteOrigin===websiteOptions.privateGatewayOrigin||
      websiteOptions.mediationAudience===gatewayHostOptions.gatewayOptions?.attestationAudience||
      gatewayHostOptions.gatewayOptions?.backendOrigin!==backendOptions.audience||
      backendOptions.gatewayServiceAccount!==GATE||
      backendOptions.googleIdentity?.expectedPrincipal!==undefined&&
        backendOptions.googleIdentity.expectedPrincipal!==GATE||
      backendOptions.runtimeOptions?.projectId!=='oldx-staging')
    return off();

  // The real release control still verifies independent approval and consumes
  // a durable run budget per backend operation. Neither is evaluated here.
  const backend=createC2EnabledProductBackend({
    ...backendOptions,enabled:true,releaseControl:control,
    runtimeServiceAccount:BACK,runtimeImage:hostFacts.backend.image,
  });
  const gateway=createC2H2MetadataBoundPrivateGatewayHostSource({
    enabled:true,hostOptions:gatewayHostOptions,
    fetchMetadata:fetchGatewayMetadata,now,
  });
  if(gateway.ready!==true)return off();
  // Keep the actual IAM hop via host-provided fetchPrivateGateway; NEVER
  // replace it with an in-process gateway.fetch shortcut in deployed code.
  if(typeof websiteOptions.fetchPrivateGateway!=='function'||
      typeof websiteOptions.consumeGuestAdmission!=='function')return off();
  const mediator=createC2WebsiteMediator({
    ...websiteOptions,enabled:true,now,
  });
  const websiteHandler=createC2WebsiteNodeHandler({
    enabled:true,websiteOrigin:websiteOptions.websiteOrigin,
    allowedOrigins:websiteOptions.allowedOrigins,
    mediator,timeoutMs:5000,
  });
  return Object.freeze({
    sourceComposed:true,
    reason:'SOURCE_ONLY_AWAITING_INDEPENDENT_HOSTED_GATES',
    websiteHandler,gateway,backend,
  });
}
// Trusted SERVER CONFIG only. Separate metadata transports belong to the two
// actual workload processes, never browser input or an in-process IAM shortcut.
// Metadata shape/UID checks are consistency checks, NOT signature verification.
// The existing downstream Google RS256 verification and Cloud Run IAM remain
// mandatory. This binds identity ports only; durable budgets, KMS status, real
// Firebase/media SDKs, immutable provenance and release approval stay required.
export function createC2G2G6MetadataBoundHostSourceAssembly(options={}) {
  if(!data(options)||options.enabled!==true||
     !data(options.websiteOptions)||!data(options.gatewayHostOptions)||
     !data(options.gatewayHostOptions.gatewayOptions)||
     !data(options.gatewayHostOptions.websiteIdentity)||
     !data(options.backendOptions)||!data(options.backendOptions.googleIdentity)||
     !data(options.metadataIdentityOptions))return off();
  const {websiteOptions:web,gatewayHostOptions:host,backendOptions:back,
    metadataIdentityOptions:metadata}=options;
  const hop=host.gatewayOptions;
  // Reject competing credential providers, including undefined-valued keys:
  // one role must have exactly one explicit metadata source.
  if(['getGatewayInvokerCredential','getWebsiteAttestation'].some(k=>Object.hasOwn(web,k))||
     ['getInvokerCredential','getGatewayAttestation'].some(k=>Object.hasOwn(hop,k))||
     typeof metadata.fetchMediatorMetadata!=='function'||
     typeof metadata.fetchGatewayMetadata!=='function'||
     Object.hasOwn(options,'fetchGatewayMetadata')||
     web.mediationAudience!==host.websiteIdentity.attestationAudience||
     host.websiteIdentity.expectedSubject!==MED_UID||
     back.googleIdentity.expectedSubject!==GATE_UID||
     back.googleIdentity.attestationAudience!==hop.attestationAudience)
    return off();
  const now=options.now??Date.now;
  const mediator=createC2CloudRunMetadataIdentity({
    enabled:true,serviceAccount:MED,expectedSubject:MED_UID,
    invokerAudience:web.privateGatewayOrigin,assertionAudience:web.mediationAudience,
    fetchMetadata:metadata.fetchMediatorMetadata,now,
  });
  const gateway=createC2CloudRunMetadataIdentity({
    enabled:true,serviceAccount:GATE,expectedSubject:GATE_UID,
    invokerAudience:hop.backendOrigin,assertionAudience:hop.attestationAudience,
    fetchMetadata:metadata.fetchGatewayMetadata,now,
  });
  if(!mediator.ready||!gateway.ready)return off();
  return createC2G2G6EnabledHostSourceAssembly({
    ...options,fetchGatewayMetadata:metadata.fetchGatewayMetadata,
    websiteOptions:{...web,
      getGatewayInvokerCredential:mediator.getInvokerCredential,
      getWebsiteAttestation:mediator.getWebsiteAttestation},
    gatewayHostOptions:{...host,gatewayOptions:{...hop,
      getInvokerCredential:gateway.getInvokerCredential,
      getGatewayAttestation:gateway.getWebsiteAttestation}},
  });
}
