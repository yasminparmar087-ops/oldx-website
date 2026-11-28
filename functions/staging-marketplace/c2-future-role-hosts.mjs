import {requireC2H2LifecycleProofKeyResolver} from '../../scripts/c2-h2-private-gateway-signing-composition.mjs';
import {createC2G2G6MetadataBoundHostSourceAssembly} from './c2-g2g6-enabled-host-source-assembly.mjs';
// Source factories only: no HTTP listener, environment activation or deployment.
// Each actual workload gets its own server-only config/transport/identity.
// Existing deployed H2U OFF server and packaging are completely untouched.
const unavailable=()=>Response.json({ok:false,error:{code:'FUTURE_HOST_OFF'}},{status:503});
function roleHost(role,options={}) {
  if(options.enabled!==true)return Object.freeze({ready:false,fetch:async()=>unavailable()});
  // An enabled multi-sign host must also enforce its same durable policy at
  // the backend; neither website routing nor signing alone is authorization.
  const host=options.gatewayHostOptions,verification=options.backendOptions?.requestVerification;
  if(!host?.lifecycleRequestSigning||!verification?.lifecyclePolicy||!verification?.lifecycleLedger)
    return Object.freeze({ready:false,fetch:async()=>unavailable()});
  try{requireC2H2LifecycleProofKeyResolver(verification.resolvePublicKey,verification.lifecyclePolicy);}
  catch{return Object.freeze({ready:false,fetch:async()=>unavailable()});}
  const assembly=createC2G2G6MetadataBoundHostSourceAssembly(options);
  if(assembly.sourceComposed!==true)return Object.freeze({ready:false,fetch:async()=>unavailable()});
  if(role==='mediator')return Object.freeze({ready:true,nodeHandler:assembly.websiteHandler});
  return Object.freeze({ready:true,fetch:request=>assembly[role].fetch(request)});
}
export const createC2FutureMediatorHost=options=>roleHost('mediator',options);
export const createC2FutureGatewayHost=options=>roleHost('gateway',options);
export const createC2FutureBackendHost=options=>roleHost('backend',options);
