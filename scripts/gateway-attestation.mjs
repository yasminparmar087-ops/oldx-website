import {verify,constants,KeyObject} from 'node:crypto';
import {parseBoundedJson} from './bounded-json.mjs';
export const GATEWAY_ATTESTATION_HEADER='x-oldx-gateway-attestation';
const id=v=>typeof v==='string'&&/^[A-Za-z0-9_-]{1,128}$/.test(v);
const principal=v=>typeof v==='string'&&/^[a-z][a-z0-9-]{4,28}[a-z0-9]@oldx-staging\.iam\.gserviceaccount\.com$/.test(v);
const audience=v=>typeof v==='string'&&v.length>0&&v.length<=512&&!/[\s\u0000-\u001f\u007f]/.test(v);
const integer=v=>Number.isSafeInteger(v)&&v>=0&&Number.isSafeInteger(v*1000);
function json(part,maxBytes){
 if(!/^[A-Za-z0-9_-]+$/.test(part))return null;
 const bytes=Buffer.from(part,'base64url');
 if(bytes.length>maxBytes||bytes.toString('base64url')!==part)return null;
 const parsed=parseBoundedJson(bytes,{maxBytes});return parsed.ok?parsed.value:null;
}
// Pure server-only verifier. No keys generated/stored, URLs fetched, SDK/env or
// credentials loaded. Resolver must return ONE trusted public RSA KeyObject for
// configured issuer+kid, with bounded refresh/cache/rotation in the future host.
// Only the explicitly configured Google service-account identity profile exists.
// Numeric immutable sub AND verified email must match; sub is never email.
export function createGatewayAttestationVerifier({enabled=false,identityType,issuer,attestationAudience,iamAudience,expectedPrincipal,expectedSubject,resolvePublicKey,now=Date.now,maxAgeSeconds=60,clockSkewSeconds=5,keyTimeoutMs=1000}={}){
 if(enabled!==true||identityType!=='google-service-account'||!['https://accounts.google.com','accounts.google.com'].includes(issuer)||!audience(attestationAudience)||!audience(iamAudience)||attestationAudience===iamAudience||!principal(expectedPrincipal)||typeof expectedSubject!=='string'||!/^[0-9]{1,32}$/.test(expectedSubject)||typeof resolvePublicKey!=='function'||typeof now!=='function'||!Number.isInteger(maxAgeSeconds)||maxAgeSeconds<1||maxAgeSeconds>120||!Number.isInteger(clockSkewSeconds)||clockSkewSeconds<0||clockSkewSeconds>10||!Number.isInteger(keyTimeoutMs)||keyTimeoutMs<1||keyTimeoutMs>1000)return null;
 return async(request,{audience:backendAudience,signal}={})=>{
  let timer,abort,controller;
  try{
   if(!(request instanceof Request)||backendAudience!==iamAudience||signal?.aborted)return null;
   const token=request.headers.get(GATEWAY_ATTESTATION_HEADER);
   if(typeof token!=='string'||token.length>8192)return null;
   const parts=token.split('.');if(parts.length!==3)return null;
   const header=json(parts[0],1024);
   if(!header||header.alg!=='RS256'||!id(header.kid)||Object.keys(header).some(k=>!['alg','kid','typ'].includes(k))||header.typ!==undefined&&header.typ!=='JWT')return null;
   // Key selection uses ONLY configured issuer and bounded kid; never jku/x5u.
   const signature=Buffer.from(parts[2],'base64url');
   if(!/^[A-Za-z0-9_-]+$/.test(parts[2])||signature.length<256||signature.length>512||signature.toString('base64url')!==parts[2])return null;
   controller=new AbortController();abort=()=>controller.abort();signal?.addEventListener('abort',abort,{once:true});if(signal?.aborted)abort();
   const stopped=new Promise((_,reject)=>{controller.signal.addEventListener('abort',()=>reject(Error('Key resolution stopped')),{once:true});if(controller.signal.aborted)reject(Error('Stopped'));});
   timer=setTimeout(abort,keyTimeoutMs);
   const key=await Promise.race([Promise.resolve().then(()=>{if(controller.signal.aborted)throw Error('Stopped');return resolvePublicKey({issuer,kid:header.kid,signal:controller.signal});}),stopped]);
   if(controller.signal.aborted||signal?.aborted||!(key instanceof KeyObject)||key.type!=='public'||key.asymmetricKeyType!=='rsa')return null;
   const bits=key.asymmetricKeyDetails?.modulusLength;
   if(!Number.isInteger(bits)||bits<2048||bits>4096||key.asymmetricKeyDetails?.publicExponent!==65537n||signature.length!==Math.ceil(bits/8))return null;
   if(!verify('RSA-SHA256',Buffer.from(parts[0]+'.'+parts[1]),{key,padding:constants.RSA_PKCS1_PADDING},signature))return null;
   // Claims are parsed/trusted ONLY after signature verification.
   const claims=json(parts[1],6144),clock=now();
   if(!claims||!integer(clock)||signal?.aborted||controller.signal.aborted)return null;
   const seconds=clock/1000;
   if(claims.iss!==issuer||claims.aud!==attestationAudience||claims.sub!==expectedSubject||claims.email!==expectedPrincipal||claims.email_verified!==true||![claims.iat,claims.exp].every(integer)||claims.exp<=claims.iat||claims.exp-claims.iat>3600||claims.iat>seconds+clockSkewSeconds||seconds-claims.iat>maxAgeSeconds||claims.nbf!==undefined&&(!integer(claims.nbf)||claims.nbf>seconds+clockSkewSeconds||claims.nbf>=claims.exp))return null;
   // Bound replay acceptance by age even if provider's ID token lasts an hour.
   const expiresAtMs=Math.min(claims.exp,claims.iat+maxAgeSeconds)*1000;
   if(!Number.isSafeInteger(expiresAtMs)||clock>=expiresAtMs)return null;
   return Object.freeze({verified:true,principal:expectedPrincipal,audience:iamAudience,expiresAtMs,assertionAudience:attestationAudience,issuer,subject:expectedSubject});
  }catch{return null;}
  finally{if(timer!==undefined)clearTimeout(timer);if(abort)signal?.removeEventListener('abort',abort);}
 };
}
// Signed bearer assertions can be replayed during this short window. They do not
// prove IAM policy, request-body binding or one-time use. Require TLS/private IAM,
// existing mutation requestId+revision+quotas, and an approved replay threat review.
