import {createPublicKey, KeyObject} from 'node:crypto';

// A fixed Google-owned JWKS endpoint, never chosen by a JWT header, caller,
// environment variable or arbitrary URL. The injected transport is SERVER-ONLY.
export const GOOGLE_GATEWAY_JWKS_URL='https://www.googleapis.com/oauth2/v3/certs';
const validKid=value=>typeof value==='string'&&/^[A-Za-z0-9_-]{1,128}$/.test(value);
const positiveTime=value=>Number.isSafeInteger(value)&&value>=0;
const expiryMs=cacheControl=>{
 if(typeof cacheControl!=='string')return null;
 const matches=[...cacheControl.matchAll(/(?:^|,)\s*max-age\s*=\s*(\d+)\s*(?=,|$)/gi)];
 if(matches.length!==1)return null;
 const age=Number(matches[0][1]);
 return Number.isSafeInteger(age)&&age>=1&&age<=86400?Math.min(age*1000,3600000):null;
};
async function boundedJson(response,signal){
 if(!(response instanceof Response)||!response.ok||response.status!==200||response.redirected||response.url&&response.url!==GOOGLE_GATEWAY_JWKS_URL||!/^application\/json(?:\s*;|\s*$)/i.test(response.headers.get('content-type')??''))throw Error('Google keys response denied');
 const len=response.headers.get('content-length');
 if(len!==null&&(!/^\d+$/.test(len)||Number(len)>32768))throw Error('Google keys size denied');
 const reader=response.body?.getReader();if(!reader)throw Error('Google keys body missing');
 const chunks=[];let size=0;
 const rejectOnAbort=()=>{};
 let abortReader;
 const aborted=new Promise((_,reject)=>{abortReader=()=>reject(Error('Stopped'));signal.addEventListener('abort',abortReader,{once:true});if(signal.aborted)abortReader();});
 aborted.catch(rejectOnAbort);
 try{
  while(true){
   if(signal.aborted)throw Error('Stopped');
   const {done,value}=await Promise.race([reader.read(),aborted]);
   if(done)break;
   size+=value.byteLength;
   if(size>32768)throw Error('Google keys too large');
   chunks.push(value);
  }
 }finally{signal.removeEventListener('abort',abortReader);void reader.cancel().catch(()=>{});}
 const all=Buffer.concat(chunks.map(v=>Buffer.from(v)),size);
 const data=JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(all));
 if(!data||Object.getPrototypeOf(data)!==Object.prototype||Object.keys(data).length!==1||!Array.isArray(data.keys)||data.keys.length<1||data.keys.length>16)throw Error('Invalid Google JWKS');
 const keys=new Map();
 for(const item of data.keys){
  if(!item||Object.getPrototypeOf(item)!==Object.prototype||!validKid(item.kid)||keys.has(item.kid)||item.kty!=='RSA'||item.alg!=='RS256'||item.use!==undefined&&item.use!=='sig'||typeof item.n!=='string'||typeof item.e!=='string'||!/^[A-Za-z0-9_-]{256,1024}$/.test(item.n)||item.e!=='AQAB')throw Error('Invalid RSA JWK');
  const key=createPublicKey({key:{kty:'RSA',n:item.n,e:item.e},format:'jwk'});
  if(!(key instanceof KeyObject)||key.type!=='public'||key.asymmetricKeyType!=='rsa'||key.asymmetricKeyDetails?.publicExponent!==65537n||key.asymmetricKeyDetails?.modulusLength<2048||key.asymmetricKeyDetails?.modulusLength>4096)throw Error('Invalid RSA key');
  keys.set(item.kid,key);
 }
 return keys;
}

// Offline-injectable, NO automatic network call until an explicitly enabled
// verifier resolves a kid. Cached keys expire; failed refreshes never extend
// their lifetime. Unknown kids are rate-bounded and never accepted by fallback.
export function createGoogleGatewayPublicKeyResolver({enabled=false,issuer,fetchRequest,now=Date.now,timeoutMs=1000,minimumRefreshMs=30000}={}){
 if(enabled!==true||!['https://accounts.google.com','accounts.google.com'].includes(issuer)||typeof fetchRequest!=='function'||typeof now!=='function'||!Number.isInteger(timeoutMs)||timeoutMs<1||timeoutMs>1000||!Number.isInteger(minimumRefreshMs)||minimumRefreshMs<1000||minimumRefreshMs>60000)return null;
 let cache=new Map(),cacheExpiresAt=0,pending=null,lastAttemptAt=-Infinity;
 async function refresh(signal){
  const controller=new AbortController();
  const abort=()=>controller.abort();
  signal?.addEventListener('abort',abort,{once:true});
  if(signal?.aborted)abort();
  const timer=setTimeout(abort,timeoutMs);
  try{
   if(controller.signal.aborted)throw Error('Stopped');
   const response=await Promise.race([
    Promise.resolve().then(()=>fetchRequest(GOOGLE_GATEWAY_JWKS_URL,{method:'GET',redirect:'error',cache:'no-store',credentials:'omit',headers:{accept:'application/json'},signal:controller.signal})),
    new Promise((_,reject)=>controller.signal.addEventListener('abort',()=>reject(Error('Stopped')),{once:true}))
   ]);
   const keys=await boundedJson(response,controller.signal);
   const ttl=expiryMs(response.headers.get('cache-control'));
   const clock=now();
   if(ttl===null||!positiveTime(clock)||!Number.isSafeInteger(clock+ttl)||controller.signal.aborted)throw Error('Google keys cache policy denied');
   cache=keys;cacheExpiresAt=clock+ttl;
  }finally{clearTimeout(timer);signal?.removeEventListener('abort',abort);}
 }
 return async({issuer:requestedIssuer,kid,signal}={})=>{
  try{
   const clock=now();
   if(requestedIssuer!==issuer||!validKid(kid)||!positiveTime(clock)||signal?.aborted)return null;
   if(clock<cacheExpiresAt&&cache.has(kid))return cache.get(kid);
   if(!pending){
    // Throttle even when a previous fetch failed (no cache), preventing an
    // unauthenticated burst from triggering unbounded public-key downloads.
    if(clock-lastAttemptAt<minimumRefreshMs)return null;
    lastAttemptAt=clock;
    const promise=refresh(signal);
    pending=promise;
    void promise.finally(()=>{if(pending===promise)pending=null;}).catch(()=>{});
   }
   await pending;
   return !signal?.aborted&&now()<cacheExpiresAt?cache.get(kid)??null:null;
  }catch{return null;}
 };
}
