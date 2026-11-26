import {createMarketplaceGateway} from './trusted-host.mjs';
import {createStep05Gateway} from './secure-product-pipeline.mjs';
import {createGoogleGatewayPublicKeyResolver} from '../../scripts/google-gateway-public-keys.mjs';
import {createGatewayAttestationVerifier,GATEWAY_ATTESTATION_HEADER} from '../../scripts/gateway-attestation.mjs';
import {MARKETPLACE_REQUEST_PROOF_HEADER} from '../../scripts/marketplace-gateway-request-proof.mjs';
export const MEDIATED_ORIGIN_HEADER='x-oldx-mediated-website-origin';
const privileged=['x-serverless-authorization',GATEWAY_ATTESTATION_HEADER,MARKETPLACE_REQUEST_PROOF_HEADER,MEDIATED_ORIGIN_HEADER,'x-oldx-gateway-nonce'];
const principal=v=>typeof v==='string'&&/^[a-z][a-z0-9-]{4,28}[a-z0-9]@oldx-staging\.iam\.gserviceaccount\.com$/.test(v);
const origin=v=>{try{const u=new URL(v);return u.origin===v&&u.protocol==='https:'&&!u.username&&!u.password&&!u.search&&!u.hash&&u.pathname==='/';}catch{return false;}};
const audience=v=>typeof v==='string'&&v.length>0&&v.length<=512&&!/[\s\u0000-\u001f\u007f]/.test(v);
const origins=v=>Array.isArray(v)&&v.length>0&&v.length<=8&&v.every(origin);
const operation=request=>{const u=new URL(request.url),op=u.pathname.split('/').at(-1);return !u.search&&!u.hash&&['save','owner','archive','list','detail'].includes(op)&&u.pathname==='/api/staging/marketplace/'+op?op:null;};
const fail=(status=503,code='ENFORCEMENT_UNAVAILABLE')=>Response.json({ok:false,error:{code}},{status,headers:{'cache-control':'private, no-store','x-content-type-options':'nosniff'}});
const unknown=()=>Response.json({ok:false,error:{code:'OUTCOME_UNKNOWN'},retrySameRequest:true},{status:202,headers:{'cache-control':'private, no-store'}});
function deadline(parent){
 const controller=new AbortController(),abort=()=>controller.abort();let stop;
 const stopped=new Promise((_,reject)=>{stop=()=>{abort();reject(Error('Stopped'));};});stopped.catch(()=>{});
 parent.addEventListener('abort',stop,{once:true});if(parent.aborted)stop();
 const timer=setTimeout(stop,5000);
 return {signal:controller.signal,run:fn=>Promise.race([Promise.resolve().then(()=>{if(controller.signal.aborted)throw Error('Stopped');return fn();}),stopped]),close(){clearTimeout(timer);parent.removeEventListener('abort',stop);}};
}
// Browser -> existing trusted website server -> IAM-private Gateway. This module
// creates no public endpoint. Origin is ONLY CORS/routing, never user identity.
// Guest admission is a required durable/independently enforced server quota port;
// receives no raw IP/forwarded identity. Missing provider blocks ALL mediation.
export function createC2WebsiteMediator({enabled=false,websiteOrigin,allowedOrigins,privateGatewayOrigin,mediatorPrincipal,mediationAudience,getGatewayInvokerCredential,getWebsiteAttestation,consumeGuestAdmission,fetchPrivateGateway,now=Date.now}={}){
 allowedOrigins=origins(allowedOrigins)?Object.freeze([...allowedOrigins]):[];
 const ready=enabled===true&&origin(websiteOrigin)&&origins(allowedOrigins)&&allowedOrigins.includes(websiteOrigin)&&origin(privateGatewayOrigin)&&privateGatewayOrigin!==websiteOrigin&&principal(mediatorPrincipal)&&audience(mediationAudience)&&mediationAudience!==privateGatewayOrigin&&[getGatewayInvokerCredential,getWebsiteAttestation,consumeGuestAdmission,fetchPrivateGateway,now].every(v=>typeof v==='function');
 return Object.freeze({async fetch(request){
  if(!ready)return fail();
  if(!(request instanceof Request))return fail(400,'INVALID_REQUEST');
  const op=operation(request),caller=request.headers.get('origin');
  if(new URL(request.url).origin!==websiteOrigin||!allowedOrigins.includes(caller))return fail(403,'DENIED');
  if(!op)return fail(404,'NOT_FOUND');
  if(privileged.some(h=>request.headers.has(h))||request.headers.has('cookie'))return fail(403,'DENIED');
  if(request.method==='POST'&&(!/^application\/json(?:;\s*charset=utf-8)?$/i.test(request.headers.get('content-type')??'')||request.headers.has('content-encoding')&&request.headers.get('content-encoding')!=='identity'))return fail(415,'UNSUPPORTED_MEDIA_TYPE');
  const ctx=deadline(request.signal);let dispatched=false;
  try{
   if(request.method==='POST'&&['list','detail'].includes(op)){
    if(request.headers.has('authorization'))return fail(403,'DENIED');
    const time=now();if(!Number.isSafeInteger(time)||time<0)return fail();
    const quota=await ctx.run(()=>consumeGuestAdmission({operation:'marketplace.public.'+op},{signal:ctx.signal,deadlineAt:time+5000}));
    if(typeof quota?.allowed!=='boolean')return fail();
    if(!quota.allowed)return fail(429,'RATE_LIMITED');
   }
   const gateway=createMarketplaceGateway({enabled:true,backendOrigin:privateGatewayOrigin,gatewayServiceAccount:mediatorPrincipal,allowedOrigins,attestationAudience:mediationAudience,now,
    getInvokerCredential:getGatewayInvokerCredential,getGatewayAttestation:getWebsiteAttestation,
    fetchBackend:(url,init)=>{dispatched=true;return fetchPrivateGateway(url,{...init,headers:{...init.headers,[MEDIATED_ORIGIN_HEADER]:caller}});}});
   return await ctx.run(()=>gateway.fetch(new Request(request,{signal:ctx.signal})));
  }catch{return dispatched&&['save','archive'].includes(op)?unknown():fail();}
  finally{ctx.close();}
 }});
}
// Separate private Gateway app contract. Actual Cloud Run IAM enforcement is an
// EXTERNAL prerequisite. Full independently signed website identity is verified;
// stripped IAM bytes and the mediated-origin header NEVER establish principal.
export function createC2PrivateGatewayHost({enabled=false,privateGatewayOrigin,mediatorPrincipal,websiteIdentity={},allowedOrigins,gatewayOptions={},now=Date.now}={}){
 gatewayOptions=gatewayOptions&&typeof gatewayOptions==='object'?Object.freeze({...gatewayOptions,requestSigning:Object.freeze({...gatewayOptions.requestSigning})}):{};
 websiteIdentity=websiteIdentity&&typeof websiteIdentity==='object'?Object.freeze({...websiteIdentity}):{};
 allowedOrigins=origins(allowedOrigins)?Object.freeze([...allowedOrigins]):[];
 const keys=createGoogleGatewayPublicKeyResolver({enabled:enabled===true,issuer:websiteIdentity?.issuer,fetchRequest:websiteIdentity?.fetchRequest,now});
 const verify=createGatewayAttestationVerifier({...websiteIdentity,enabled:enabled===true,iamAudience:privateGatewayOrigin,expectedPrincipal:mediatorPrincipal,resolvePublicKey:keys,now});
 const ready=enabled===true&&origin(privateGatewayOrigin)&&principal(mediatorPrincipal)&&origins(allowedOrigins)&&typeof verify==='function'&&
  origin(gatewayOptions.backendOrigin)&&gatewayOptions.backendOrigin!==privateGatewayOrigin&&principal(gatewayOptions.gatewayServiceAccount)&&gatewayOptions.gatewayServiceAccount!==mediatorPrincipal&&
  audience(gatewayOptions.attestationAudience)&&gatewayOptions.attestationAudience!==gatewayOptions.backendOrigin&&gatewayOptions.attestationAudience!==websiteIdentity.attestationAudience&&
  [gatewayOptions.getInvokerCredential,gatewayOptions.getGatewayAttestation,gatewayOptions.fetchBackend,gatewayOptions.requestSigning?.signMessage,now].every(v=>typeof v==='function')&&/^[A-Za-z0-9_-]{1,100}$/.test(gatewayOptions.requestSigning?.kid??'');

 return Object.freeze({async fetch(request){
  if(!ready)return fail();
  if(!(request instanceof Request))return fail(400,'INVALID_REQUEST');
  const op=operation(request);
  if(new URL(request.url).origin!==privateGatewayOrigin||!op)return fail(404,'NOT_FOUND');
  if(request.method!=='POST')return fail(405,'METHOD_NOT_ALLOWED');
  const caller=request.headers.get(MEDIATED_ORIGIN_HEADER),iam=request.headers.get('x-serverless-authorization');
  if(!allowedOrigins.includes(caller)||request.headers.has('origin')||request.headers.has('cookie')||request.headers.has(MARKETPLACE_REQUEST_PROOF_HEADER)||request.headers.has('x-oldx-gateway-nonce')||typeof iam!=='string'||iam.length>8199||!/^Bearer [A-Za-z0-9_.-]+$/.test(iam))return fail(403,'DENIED');
  const ctx=deadline(request.signal);let dispatched=false;
  try{
   const proof=await ctx.run(()=>verify(request,{audience:privateGatewayOrigin,signal:ctx.signal}));
   if(proof?.verified!==true||proof.principal!==mediatorPrincipal||proof.audience!==privateGatewayOrigin)return fail(403,'DENIED');
   // Whitelist ONLY Firebase user authorization + JSON metadata + verified
   // website route origin. No original IAM, identity, nonce or forwarded fields.
   const headers=new Headers({'origin':caller,'content-type':request.headers.get('content-type')??''});
   for(const key of ['authorization','content-length','content-encoding'])if(request.headers.has(key))headers.set(key,request.headers.get(key));
   const clean=new Request(request.url,{method:'POST',headers,body:request.body,duplex:'half',signal:ctx.signal});
   const gateway=createStep05Gateway({...gatewayOptions,enabled:true,allowedOrigins,now,fetchBackend:(url,init)=>{
    const fresh=now();if(ctx.signal.aborted||!Number.isSafeInteger(fresh)||fresh>=proof.expiresAtMs)throw Error('Website identity expired');
    return gatewayOptions.fetchBackend(url,init);
   }});
   return await ctx.run(()=>{dispatched=true;return gateway.fetch(clean);});
  }catch{return dispatched&&['save','archive'].includes(op)?unknown():fail();}
  finally{ctx.close();}
 }});
}
