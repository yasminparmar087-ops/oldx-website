import {MARKETPLACE_REQUEST_PROOF_HEADER} from './marketplace-gateway-request-proof.mjs';

// New inactive composition ports. These wrap (but never replace) the existing
// attested gateway fetchBackend / private backend fetch contracts.
const IDENTITY_HEADER='x-oldx-gateway-attestation';
const routes=new Set(['save','owner','archive','list','detail'].map(op=>'/api/staging/marketplace/'+op));
const signedProof=value=>typeof value==='string'&&value.length<=2048&&/^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(value);
const googleHop=value=>typeof value==='string'&&value.length<=8199&&/^Bearer [A-Za-z0-9_.-]+$/.test(value);
const id=value=>typeof value==='string'&&/^[a-z][a-z0-9-]{4,28}[a-z0-9]@oldx-staging\.iam\.gserviceaccount\.com$/.test(value);
function origin(value){try{const u=new URL(value);return u.protocol==='https:'&&!u.username&&!u.password&&u.pathname==='/'&&!u.search&&!u.hash&&u.origin===value;}catch{return false;}}
function pathFor(url,base){try{const u=new URL(url);return u.origin===base&&!u.search&&!u.hash&&routes.has(u.pathname)?u.pathname:null;}catch{return null;}}
const error=(status,code)=>Response.json({ok:false,error:{code}},{status,headers:{'cache-control':'private, no-store','x-content-type-options':'nosniff'}});
function context(parent,ms){
 const controller=new AbortController(),abort=()=>controller.abort();
 parent?.addEventListener('abort',abort,{once:true});if(parent?.aborted)abort();
 const timer=setTimeout(abort,ms);
 return {signal:controller.signal,close(){clearTimeout(timer);parent?.removeEventListener('abort',abort);}};
}
async function readBounded(stream,max,signal){
 if(signal.aborted)throw Error('Stopped');
 if(!stream)return new Uint8Array();
 const reader=stream.getReader(),chunks=[];let size=0;
 const stopped=new Promise((_,reject)=>{signal.addEventListener('abort',()=>reject(Error('Stopped')),{once:true});if(signal.aborted)reject(Error('Stopped'));});stopped.catch(()=>{});
 try{
  while(true){const {done,value}=await Promise.race([reader.read(),stopped]);if(done)break;
   size+=value.byteLength;if(size>max)throw Error('Oversize');chunks.push(value);}
  const result=new Uint8Array(size);let offset=0;
  for(const chunk of chunks){result.set(chunk,offset);offset+=chunk.byteLength;}return result;
 }finally{void reader.cancel().catch(()=>{});}
}

// Supply this function as the fetchBackend port of createAttestedMarketplaceGateway.
// The gateway already strips caller headers and obtains separate valid IAM and
// signed identity assertions; this hop adds server-signed request binding.
export function createProofBoundGatewayHop({enabled=false,backendOrigin,signRequestProof,fetchBackend,timeoutMs=5000}={}){
 const ready=enabled===true&&origin(backendOrigin)&&typeof signRequestProof==='function'&&typeof fetchBackend==='function'&&Number.isInteger(timeoutMs)&&timeoutMs>=1&&timeoutMs<=5000;
 return async(url,init={})=>{
  if(!ready)throw Error('Proof hop unavailable');
  const path=pathFor(url,backendOrigin),headers=new Headers(init.headers);
  if(!path||init.method!=='POST'||!(init.body instanceof Uint8Array)||init.body.byteLength>(path.endsWith('/list')||path.endsWith('/detail')?4096:32768)||headers.has(MARKETPLACE_REQUEST_PROOF_HEADER)||headers.has('origin')||headers.has('cookie')||!googleHop(headers.get('x-serverless-authorization'))||!/^[-\w]+\.[-\w]+\.[-\w]+$/.test(headers.get(IDENTITY_HEADER)??''))throw Error('Proof hop invalid request');
  const ctx=context(init.signal,timeoutMs);
  try{
   const proof=await signRequestProof({method:'POST',path,body:init.body,authorization:headers.get('authorization'),attestationToken:headers.get(IDENTITY_HEADER),signal:ctx.signal});
   if(!signedProof(proof)||ctx.signal.aborted)throw Error('Signing failed');
   headers.set(MARKETPLACE_REQUEST_PROOF_HEADER,proof);
   const response=await fetchBackend(url,{...init,headers,signal:ctx.signal,redirect:'error',credentials:'omit',cache:'no-store'});
   if(!(response instanceof Response)||response.redirected||response.status<200||response.status>=600)throw Error('Backend response failed');
   const body=await readBounded(response.body,65536,ctx.signal);
   const decoded=new TextDecoder('utf-8',{fatal:true}).decode(body);
   if(decoded.includes(proof))throw Error('Proof echoed');
   // Never propagate upstream response headers or credential echoes directly.
   return new Response(body,{status:response.status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'private, no-store','x-content-type-options':'nosniff'}});
  }finally{ctx.close();}
 };
}

// Wrap an existing independently authenticated private backend. The injected
// verifyAttestation MUST be the actual signed gateway-attestation verifier, NOT
// a user-controlled verified:true callback. Existing Cloud Run IAM enforcement
// and the wrapped backend's Firebase/ownership checks are distinct requirements.
export function createProofBoundBackendHop({enabled=false,audience,gatewayServiceAccount,verifyAttestation,verifyRequestProof,backend,now=Date.now,timeoutMs=5000}={}){
 const ready=enabled===true&&origin(audience)&&id(gatewayServiceAccount)&&typeof verifyAttestation==='function'&&typeof verifyRequestProof==='function'&&typeof backend?.fetch==='function'&&typeof now==='function'&&Number.isInteger(timeoutMs)&&timeoutMs>=1&&timeoutMs<=5000;
 return Object.freeze({async fetch(request){
  if(!ready)return error(503,'ENFORCEMENT_UNAVAILABLE');
  if(!(request instanceof Request))return error(400,'INVALID_REQUEST');
  const path=pathFor(request.url,audience);
  if(!path)return error(404,'NOT_FOUND');
  if(request.method!=='POST')return error(405,'METHOD_NOT_ALLOWED');
  if(request.headers.has('origin')||request.headers.has('cookie')||!googleHop(request.headers.get('x-serverless-authorization'))||!signedProof(request.headers.get(MARKETPLACE_REQUEST_PROOF_HEADER)))return error(403,'DENIED');
  const ctx=context(request.signal,timeoutMs);
  try{
   const identity=await verifyAttestation(request,{audience,signal:ctx.signal});
   if(identity?.verified!==true||identity.principal!==gatewayServiceAccount||identity.audience!==audience||!Number.isSafeInteger(identity.expiresAtMs)||identity.expiresAtMs<=now()||ctx.signal.aborted)return error(403,'DENIED');
   const data=await readBounded(request.body,path.endsWith('/list')||path.endsWith('/detail')?4096:32768,ctx.signal);
   const allowed=await verifyRequestProof({proof:request.headers.get(MARKETPLACE_REQUEST_PROOF_HEADER),method:'POST',path,body:data,authorization:request.headers.get('authorization'),attestationToken:request.headers.get(IDENTITY_HEADER),signal:ctx.signal});
   if(allowed!==true||ctx.signal.aborted)return error(403,'DENIED');
   const headers=new Headers(request.headers);headers.delete(MARKETPLACE_REQUEST_PROOF_HEADER);
   const safe=new Request(request.url,{method:'POST',headers,body:data,signal:ctx.signal});
   return await backend.fetch(safe);
  }catch{return error(503,'ENFORCEMENT_UNAVAILABLE');}
  finally{ctx.close();}
 }});
}
