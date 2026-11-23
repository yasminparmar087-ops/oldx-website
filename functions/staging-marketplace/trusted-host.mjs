import {createCloudRunMarketplaceListener} from './cloud-run-http.mjs';
import {createMarketplaceFetchHandler} from './vercel-handler.mjs';
import {createStagingMarketplaceRuntime} from './runtime.mjs';
import {createSecureStagingMarketplacePublicRuntime} from './public-runtime.mjs';
const commands=new Set(['save','owner','archive']),reads=new Set(['list','detail']);
const jwt=v=>typeof v==='string'&&v.length<=8192&&/^[-\w]+\.[-\w]+\.[-\w]+$/.test(v);
const origin=v=>{try{const u=new URL(v);return u.protocol==='https:'&&!u.username&&!u.password&&u.pathname==='/'&&!u.search&&!u.hash?u.origin:null;}catch{return null;}};
const route=url=>{try{const u=new URL(url),op=u.pathname.split('/').at(-1);return !u.search&&!u.hash&&u.pathname==='/api/staging/marketplace/'+op&&(commands.has(op)||reads.has(op))?op:null;}catch{return null;}};
const fail=(status=503,code='ENFORCEMENT_UNAVAILABLE')=>Response.json({ok:false,error:{code}},{status,headers:{'cache-control':'private, no-store','x-content-type-options':'nosniff'}});
const identity=v=>typeof v==='string'&&/^[a-z][a-z0-9-]{4,28}[a-z0-9]@oldx-staging\.iam\.gserviceaccount\.com$/.test(v);
function deadline(signal,timeoutMs){
 const controller=new AbortController(),abort=()=>controller.abort();
 const stopped=new Promise((_,reject)=>{controller.signal.addEventListener('abort',()=>reject(Error('Stopped')),{once:true});});
 // Attach rejection handling even if no operation has begun.
 stopped.catch(()=>{});
 signal?.addEventListener('abort',abort,{once:true});if(signal?.aborted)abort();
 const timer=setTimeout(abort,timeoutMs);
 return {signal:controller.signal,run:task=>Promise.race([Promise.resolve().then(()=>{if(controller.signal.aborted)throw Error('Stopped');return task();}),stopped]),
  close(){clearTimeout(timer);signal?.removeEventListener('abort',abort);}};
}
async function bytes(stream,max,ctx){
 if(!stream)return new Uint8Array();
 const reader=stream.getReader(),chunks=[];let size=0;
 try{while(true){const {done,value}=await ctx.run(()=>reader.read());if(done)break;size+=value.byteLength;if(size>max)throw Error('Oversize');chunks.push(value);}}
 finally{void reader.cancel().catch(()=>{});}
 const data=new Uint8Array(size);let at=0;for(const v of chunks){data.set(v,at);at+=v.byteLength;}return data;
}
// Private backend contract. verifyInvoker MUST use independently authenticated
// platform/cryptographic evidence, not parse caller-supplied claims/headers.
// No SDK loading/token minting/HTTP calls; no active entrypoint or port.
export function createTrustedMarketplaceBackend({enabled=false,audience,gatewayServiceAccount,verifyInvoker,commandRuntime,publicRuntime,timeoutMs=5000,now=Date.now}={}){
 const base=origin(audience),ready=enabled===true&&base===audience&&identity(gatewayServiceAccount)&&typeof verifyInvoker==='function'&&typeof commandRuntime?.handle==='function'&&typeof publicRuntime?.handle==='function'&&Number.isInteger(timeoutMs)&&timeoutMs>=1&&timeoutMs<=5000;
 return Object.freeze({async fetch(request){
  if(!ready)return fail();
  if(!(request instanceof Request))return fail(400,'INVALID_REQUEST');
  const op=route(request.url);
  if(!op||new URL(request.url).origin!==base)return fail(404,'NOT_FOUND');
  if(request.method!=='POST')return fail(405,'METHOD_NOT_ALLOWED');
  // Browser origin/CORS belongs to gateway; backend accepts server-only hops.
  if(request.headers.has('origin')||request.headers.has('cookie'))return fail(403,'DENIED');
  const ctx=deadline(request.signal,timeoutMs);let attempted=false;
  try{
   const proof=await ctx.run(()=>verifyInvoker(request,{audience:base,signal:ctx.signal}));
   const clock=now();
   if(!Number.isSafeInteger(clock)||clock<0||proof?.audience!==base||proof?.principal!==gatewayServiceAccount||proof?.verified!==true||!Number.isSafeInteger(proof.expiresAtMs)||proof.expiresAtMs<=clock)return fail(403,'DENIED');
   const firebase=request.headers.get('authorization'),iam=request.headers.get('x-serverless-authorization');
   if(!iam?.startsWith('Bearer ')||!jwt(iam.slice(7)))return fail(403,'DENIED');
   if(commands.has(op)&&(!firebase?.startsWith('Bearer ')||!jwt(firebase.slice(7))||firebase===iam))return fail(401,'AUTH_REQUIRED');
   if(reads.has(op)&&firebase!==null)return fail(403,'DENIED');
   // Remove privileged hop credential before passing to Firebase/runtime code.
   const headers=new Headers({'content-type':request.headers.get('content-type')??''});
   for(const key of ['content-length','content-encoding'])if(request.headers.has(key))headers.set(key,request.headers.get(key));
   if(firebase)headers.set('authorization',firebase);
   const body=await bytes(request.body,commands.has(op)?32768:4096,ctx);
   const clean=new Request(request.url,{method:'POST',headers,body,signal:ctx.signal});
   const runtime=commands.has(op)?commandRuntime:publicRuntime;
   const handler=createMarketplaceFetchHandler({operation:op,options:{enabled:true},loadRuntime:async()=>runtime});
   return await ctx.run(()=>{attempted=true;return handler.fetch(clean);});
  }catch{return attempted&&commands.has(op)?Response.json({ok:false,error:{code:'OUTCOME_UNKNOWN'},retrySameRequest:true},{status:202}):fail();}
  finally{ctx.close();}
 }});
}
// Optional trusted composition from existing runtime dependencies only.
// Publication remains FALSE even if runtimeOptions contains an activation value.
export function createStagingMarketplaceTrustedHost({enabled=false,runtimeOptions={},guestPolicy,cursorKey,...trust}={}){
 if(enabled!==true)return createTrustedMarketplaceBackend();
 const commandRuntime=createStagingMarketplaceRuntime({...runtimeOptions,enabled:true,publicationEnabled:false});
 const publicRuntime=createSecureStagingMarketplacePublicRuntime({...runtimeOptions,enabled:true,guestPolicy,cursorKey});
 return createTrustedMarketplaceBackend({...trust,enabled:true,commandRuntime,publicRuntime});
}
// Browser -> trusted gateway -> private Cloud Run. IAM token is acquired only
// from server DI; NEVER accepted from browser or returned in response headers.
// Origin list and backend/audience must be supplied from separately approved
// trusted configuration. No permissive defaults, wildcard or automatic lookup.
export function createMarketplaceGateway({enabled=false,backendOrigin,gatewayServiceAccount,allowedOrigins=[],getInvokerCredential,fetchBackend,timeoutMs=5000,now=Date.now}={}){
 const base=origin(backendOrigin),origins=new Set(Array.isArray(allowedOrigins)?allowedOrigins:[]);
 const ready=enabled===true&&base===backendOrigin&&identity(gatewayServiceAccount)&&Array.isArray(allowedOrigins)&&allowedOrigins.length>0&&allowedOrigins.length<=8&&allowedOrigins.every(v=>origin(v)===v)&&typeof getInvokerCredential==='function'&&typeof fetchBackend==='function'&&Number.isInteger(timeoutMs)&&timeoutMs>=1&&timeoutMs<=5000;
 const cors=(response,allowed)=>{
  const headers=new Headers({'content-type':'application/json; charset=utf-8','cache-control':'private, no-store','x-content-type-options':'nosniff','vary':'Origin','access-control-allow-origin':allowed});
  return new Response(response.body,{status:response.status,headers});
 };
 return Object.freeze({async fetch(request){
  if(!ready)return fail();
  if(!(request instanceof Request))return fail(400,'INVALID_REQUEST');
  if(new URL(request.url).protocol!=='https:')return fail(403,'DENIED');
  const caller=request.headers.get('origin');
  if(!origins.has(caller))return fail(403,'DENIED');
  const op=route(request.url);
  if(!op)return cors(fail(404,'NOT_FOUND'),caller);
  if(request.method==='OPTIONS'){
   const names=(request.headers.get('access-control-request-headers')??'').toLowerCase().split(',').map(v=>v.trim()).filter(Boolean);
   if(request.headers.get('access-control-request-method')!=='POST'||names.some(v=>!['content-type',...(commands.has(op)?['authorization']:[])].includes(v)))return cors(fail(403,'DENIED'),caller);
   return new Response(null,{status:204,headers:{'access-control-allow-origin':caller,'access-control-allow-methods':'POST','access-control-allow-headers':commands.has(op)?'content-type, authorization':'content-type','vary':'Origin, Access-Control-Request-Method, Access-Control-Request-Headers','cache-control':'no-store'}});
  }
  if(request.method!=='POST')return cors(fail(405,'METHOD_NOT_ALLOWED'),caller);
  if(request.headers.has('x-serverless-authorization')||request.headers.has('cookie'))return cors(fail(403,'DENIED'),caller);
  const firebase=request.headers.get('authorization');
  if(commands.has(op)&&(!firebase?.startsWith('Bearer ')||!jwt(firebase.slice(7))))return cors(fail(401,'AUTH_REQUIRED'),caller);
  if(reads.has(op)&&firebase!==null)return cors(fail(403,'DENIED'),caller);
  if(!/^application\/json(?:;\s*charset=utf-8)?$/i.test(request.headers.get('content-type')??'')||request.headers.has('content-encoding')&&request.headers.get('content-encoding')!=='identity')return cors(fail(415,'UNSUPPORTED_MEDIA_TYPE'),caller);
  const ctx=deadline(request.signal,timeoutMs);let dispatched=false;
  try{
   const body=await bytes(request.body,commands.has(op)?32768:4096,ctx);
   const credential=await ctx.run(()=>getInvokerCredential({audience:base,signal:ctx.signal}));
   const clock=now();
   if(!Number.isSafeInteger(clock)||credential?.type!=='cloud-run-iam-id-token'||credential?.audience!==base||credential?.principal!==gatewayServiceAccount||!jwt(credential?.token)||credential.token===firebase?.slice(7)||!Number.isSafeInteger(credential.expiresAtMs)||credential.expiresAtMs<=clock+timeoutMs||credential.expiresAtMs>clock+3600000)throw Error('Invoker unavailable');
   const headers={'content-type':'application/json','x-serverless-authorization':'Bearer '+credential.token,...(firebase?{authorization:firebase}:{})};
   const response=await ctx.run(()=>{dispatched=true;return fetchBackend(base+'/api/staging/marketplace/'+op,{method:'POST',headers,body,signal:ctx.signal,redirect:'error',credentials:'omit',cache:'no-store'});});
   if(!(response instanceof Response)||response.redirected||response.status<200||response.status>=600||!/^application\/json(?:;\s*charset=utf-8)?$/i.test(response.headers.get('content-type')??''))throw Error('Backend unavailable');
   const data=await bytes(response.body,65536,ctx);
   const text=new TextDecoder('utf-8',{fatal:true}).decode(data),decoded=JSON.parse(text);
   if(JSON.stringify(decoded).includes(credential.token))throw Error('Credential echo denied');
   return cors(new Response(data,{status:response.status}),caller);
  }catch{
   return cors(dispatched&&commands.has(op)?Response.json({ok:false,error:{code:'OUTCOME_UNKNOWN'},retrySameRequest:true},{status:202}):fail(),caller);
  }finally{ctx.close();}
 }});
}


// Bridge existing Node listener's synthetic URL to a trusted fixed audience.
// Never derives backend audience from Host/X-Forwarded-* headers; opens no port.
export function createTrustedMarketplaceListener({enabled=false,audience,backend}={}){
 const ready=enabled===true&&origin(audience)===audience&&typeof backend?.fetch==='function';
 const handlers=Object.fromEntries([...commands,...reads].map(op=>[op,{fetch(request){
  return backend.fetch(new Request(audience+'/api/staging/marketplace/'+op,{
   method:'POST',headers:request.headers,body:request.body,duplex:'half',signal:request.signal
  }));
 }}]));
 return createCloudRunMarketplaceListener({enabled:ready,handlers});
}
