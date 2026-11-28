import {AsyncLocalStorage} from 'node:async_hooks';
import {createC2H2MultiSignLifecyclePolicy} from '../../../scripts/c2-h2-lifecycle-signing-status-contract.mjs';
import {createC2H2LifecycleApprovalVerifier} from '../../../scripts/c2-h2-lifecycle-approval.mjs';
import {createC2H2LifecycleStageLedger,createC2H2RemoteLifecycleStageLedger} from '../../../scripts/c2-h2-lifecycle-stage-ledger.mjs';
import {createStagingMarketplaceBinding} from '../../../scripts/staging-marketplace-context.mjs';
import {createC2EnabledReleaseControl} from '../../../scripts/c2-enabled-release-control.mjs';
import {createC2StagingRunBudget} from '../../../scripts/c2-staging-run-budget.mjs';
import {createStagingMarketplaceGuestRate} from '../../../scripts/staging-marketplace-guest-rate.mjs';
import {createC2H2LifecycleRequestSigning,createC2H2LifecycleProofKeyResolver} from '../../../scripts/c2-h2-private-gateway-signing-composition.mjs';
import {createC2EnabledProductBackend} from '../secure-product-pipeline.mjs';
import {createC2WebsiteMediator,createC2PrivateGatewayHost} from '../c2-website-mediation.mjs';
import {createC2LifecycleStageController} from '../c2-lifecycle-stage-controller.mjs';
import {createC2CloudRunMetadataIdentity} from '../../../scripts/c2-cloud-run-metadata-identity.mjs';
import {createFourRoleReaderHost} from './reader-host.mjs';
import {createBackendLedgerRpc} from './ledger-rpc.mjs';
import {createRemoteReaderStatus} from './remote-status.mjs';
import {createLifecycleKmsTransport} from './kms-transport.mjs';
import {createFirebaseNativeBindings} from './firebase-native.mjs';
import {ROLES,sha,requireFourRoleAuthority} from './contract.mjs';
import {createFourRoleProtocol,readBytes} from './protocol.mjs';
const wa='urn:oldx:h2ah:mediator',ga='urn:oldx:h2ah:gateway';
const off=()=>Object.freeze({ready:false,fetch:async()=>new Response(null,{status:503}),close:async()=>{}});
// Four separate processes. Only Backend constructs native Firestore. Gateway
// signs, Reader reads, Mediator verifies user sessions. ALS stores request-local
// context ONLY: every quota/replay/sign stage lives durably on Backend.
export async function createFourRoleRuntime({enabled=false,role,authority,configuration,
 fetchMetadata,fetchGoogleKeys,fetchPrivate,fetchKms,sdkLoader,cursorKey,now=Date.now}={}){
 if(enabled!==true)return off();
 let native;
 try{
 requireFourRoleAuthority(authority);
 if(!ROLES[role])return off();
 const signed=authority.configuration,facts=signed.roles;
 const policy=createC2H2MultiSignLifecyclePolicy({enabled:true,proposal:configuration.proposal,
 mode:'bounded-per-request-multisign-v1',maxSignAttempts:6});
 if(policy.activationAllowed!==false||!policy.maxSignAttempts||
 sha(JSON.stringify(policy))!==signed.policyDigest)throw Error('POLICY');
 const protocol=createFourRoleProtocol({enabled:true,role,authority,fetchMetadata,fetchGoogleKeys,fetchPrivate,now});
 if(!protocol)throw Error('PROTOCOL');
 await protocol.ownRuntimeEvidence();
 const scope=new AsyncLocalStorage(),current=()=>scope.getStore();
 const identity=(target,aud)=>createC2CloudRunMetadataIdentity({enabled:true,serviceAccount:ROLES[role].principal,
 expectedSubject:ROLES[role].uid,invokerAudience:facts[target].origin,assertionAudience:aud,fetchMetadata,now});
 let ledger,backendRpc,guest;
 if(role==='mediator'||role==='backend')
 native=await createFirebaseNativeBindings({protocol,fetchMetadata,sdkLoader,now});
 if(role==='backend'){
 const binding=createStagingMarketplaceBinding({projectId:'oldx-staging',deploymentEnvironment:'preview',...native});
 const a=configuration.lifecycleApproval;
 if(a?.publicKeySha256!==signed.lifecycleApprovalKeySha256)throw Error('APPROVAL_PIN');
 const verifyLifecycleApproval=createC2H2LifecycleApprovalVerifier({enabled:true,policy,...a,now});
 ledger=createC2H2LifecycleStageLedger({enabled:true,binding,policy,verifyLifecycleApproval,now});
 guest=createStagingMarketplaceGuestRate({enabled:true,binding,policy:{windowMs:600000,guestLimit:20,globalLimit:20},now});
 backendRpc=createBackendLedgerRpc({policy,ledger,protocol,guestAdmission:guest,now});
 }else ledger=createC2H2RemoteLifecycleStageLedger({enabled:true,policy,protocol});
 if(role==='reader'){
 const reader=createFourRoleReaderHost({enabled:true,authority,policy,ledger,protocol,fetchMetadata,fetchKms,now});
 return Object.freeze({...reader,origin:facts.reader.origin,isBound:()=>authority.fresh(),close:async()=>{}});
 }
 if(role==='backend'){
 let budget;
 const release=createC2EnabledReleaseControl({enabled:true,contract:configuration.releaseContract,now,
 verifyApproval:async(_c,{contractDigest})=>({authorized:authority.fresh()&&contractDigest===signed.releaseDigest,
 contractDigest,expiresAtMs:policy.expiresAtMs}),
 consumeRunBudget:(input,context)=>budget(input,context)});
 if(!release.ready||release.contractDigest!==signed.releaseDigest||configuration.releaseContract.expiresAtMs!==policy.expiresAtMs||
 !['mediator','gateway','backend'].every(r=>release.hostBindings.images[r]===facts[r].image&&
 release.hostBindings.principals[r]===facts[r].principal))throw Error('RELEASE');
 const binding=createStagingMarketplaceBinding({projectId:'oldx-staging',deploymentEnvironment:'preview',...native});
 budget=createC2StagingRunBudget({enabled:true,binding,runId:policy.runId,contractDigest:release.contractDigest,
 maxRequests:20,expiresAtMs:policy.expiresAtMs,now});
 const resolvePublicKey=createC2H2LifecycleProofKeyResolver({enabled:true,policy,publicKeyPem:configuration.kmsPublicKeyPem,
 getTrustedKeyVersionStatus:createRemoteReaderStatus({protocol,getStageContext:current}),now});
 if(!resolvePublicKey||!(cursorKey instanceof Uint8Array)||cursorKey.length!==32)throw Error('BACKEND_KEY');
 const backend=createC2EnabledProductBackend({enabled:true,releaseControl:release,runtimeServiceAccount:ROLES.backend.principal,
 runtimeImage:facts.backend.image,audience:facts.backend.origin,gatewayServiceAccount:ROLES.gateway.principal,
 googleIdentity:{identityType:'google-service-account',issuer:'https://accounts.google.com',attestationAudience:ga,
 expectedSubject:ROLES.gateway.uid,fetchRequest:fetchGoogleKeys},
 requestVerification:{resolvePublicKey,lifecyclePolicy:policy,lifecycleLedger:ledger},
 runtimeOptions:{...native,projectId:'oldx-staging',deploymentEnvironment:'preview',
 ratePolicy:{windowMs:600000,actorLimit:20,globalLimit:20}},
 guestPolicy:{windowMs:600000,guestLimit:20,globalLimit:20},cursorKey,now});
 return Object.freeze({ready:true,origin:facts[role].origin,isBound:()=>authority.fresh(),close:native.close,async fetch(request){
 if(new URL(request.url).pathname==='/internal/ledger')return backendRpc(request);
 try{const ctx=await protocol.receive(request,{fromRoles:['gateway'],path:new URL(request.url).pathname});
 return scope.run(ctx,()=>backend.fetch(new Request(request.url,{method:'POST',headers:request.headers,body:ctx.body,signal:request.signal})));
 }catch{return new Response(null,{status:403});}
 }});
 }
 if(role==='gateway'){
 const signing=createC2H2LifecycleRequestSigning({enabled:true,policy,ledger,getStageContext:current,
 publicKeyPem:configuration.kmsPublicKeyPem,getTrustedKeyVersionStatus:createRemoteReaderStatus({protocol,getStageContext:current}),
 asymmetricSign:createLifecycleKmsTransport({protocol,fetchMetadata,fetchKms,now}),now});
 if(!signing.ready)throw Error('SIGNER');
 const id=identity('backend',ga);
 const gateway=createC2PrivateGatewayHost({enabled:true,privateGatewayOrigin:facts.gateway.origin,
 mediatorPrincipal:ROLES.mediator.principal,allowedOrigins:[facts.mediator.origin],
 websiteIdentity:{identityType:'google-service-account',issuer:'https://accounts.google.com',
 attestationAudience:wa,expectedSubject:ROLES.mediator.uid,fetchRequest:fetchGoogleKeys},
 gatewayOptions:{backendOrigin:facts.backend.origin,gatewayServiceAccount:ROLES.gateway.principal,
 attestationAudience:ga,getInvokerCredential:id.getInvokerCredential,getGatewayAttestation:id.getWebsiteAttestation,
 requestSigning:signing,fetchBackend:(url,init)=>protocol.send('backend',new URL(url).pathname,init.body,
 {...current(),operation:new URL(url).pathname.split('/').at(-1),headers:init.headers,signal:init.signal})},now});
 return Object.freeze({ready:true,origin:facts.gateway.origin,isBound:()=>authority.fresh(),close:async()=>{},async fetch(request){
 try{const ctx=await protocol.receive(request,{fromRoles:['mediator'],path:new URL(request.url).pathname});
 return scope.run(ctx,()=>gateway.fetch(new Request(request.url,{method:'POST',headers:request.headers,body:ctx.body,signal:request.signal})));
 }catch{return new Response(null,{status:403});}
 }});
 }
 const id=identity('gateway',wa);
 const mediator=createC2WebsiteMediator({enabled:true,websiteOrigin:facts.mediator.origin,allowedOrigins:[facts.mediator.origin],
 privateGatewayOrigin:facts.gateway.origin,mediatorPrincipal:ROLES.mediator.principal,mediationAudience:wa,
 getGatewayInvokerCredential:id.getInvokerCredential,getWebsiteAttestation:id.getWebsiteAttestation,
 consumeGuestAdmission:async(input,{signal})=>{
 const ctx=current(),response=await protocol.send('backend','/internal/ledger',
 Buffer.from(JSON.stringify({...input,reservation:ctx.reservation})),{...ctx,operation:'consumeGuest',signal});
 if(response.status!==200)throw Error('GUEST_BUDGET');return response.json();
 },
 fetchPrivateGateway:(url,init)=>protocol.send('gateway',new URL(url).pathname,init.body,
 {...current(),operation:new URL(url).pathname.split('/').at(-1),headers:init.headers,signal:init.signal}),now});
 return Object.freeze({ready:true,origin:facts.mediator.origin,isBound:()=>authority.fresh(),close:native.close,async fetch(request){
 // Private bounded synthetic acceptance surface, NOT a public browser IAM
 // endpoint. User Firebase auth is consumed here; guest backend auth stays empty.
 try{
 const token=request.headers.get('authorization')?.replace(/^Bearer /,'');
 const claims=await native.adminAuth.verifyIdToken(token,true);
 const bytes=await readBytes(request,32768),body=JSON.parse(bytes.toString('utf8'));
 const op=new URL(request.url).pathname.split('/').at(-1);
 const phase=op==='list'?'buyer-list':op==='detail'?'buyer-detail':op==='save'?
 body.id===null?'seller-save':body.publication==='publish'?'seller-publish':
 body.publication==='withdraw'?'seller-withdraw':'seller-edit':null;
 const session={uid:claims.uid,sessionId:sha(token)},headers=new Headers(request.headers);
 headers.set('origin',facts.mediator.origin);if(op==='list'||op==='detail')headers.delete('authorization');
 // Never carry caller-selected internal context into the trusted dispatch.
 for(const key of headers.keys())if(key.startsWith('x-oldx-'))return new Response(null,{status:403});
 // Cloud Run may forward a signature-stripped IAM header. Discard it; the
 // external platform enforces IAM and Firebase independently verifies actors.
 headers.delete('x-serverless-authorization');
 const controller=createC2LifecycleStageController({enabled:true,policy,ledger,adminAuth:native.adminAuth,
 websiteOrigin:facts.mediator.origin,getCurrentSession:()=>session,now,
 dispatch:(clean,ctx)=>scope.run(ctx,()=>mediator.fetch(clean))});
 return controller.execute({phase,sessionToken:token,sessionId:session.sessionId,
 request:new Request(request.url,{method:'POST',headers,body:bytes,signal:request.signal})});
 }catch{return new Response(null,{status:403});}
 }});
 }catch{await native?.close?.();return off();}
}
