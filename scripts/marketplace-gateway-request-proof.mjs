import {createHash, randomBytes, verify, constants, KeyObject} from 'node:crypto';

// Inactive, server-only request-binding contract. A signed gateway identity
// token is still a bearer token: ONLY this separate signed intent + an atomic,
// cross-instance consumeNonce port can reject replays of a particular request.
export const MARKETPLACE_REQUEST_PROOF_HEADER='x-oldx-gateway-request-proof';
const purpose='oldx.marketplace.request.v1';
const exactRoutes=new Set(['save','owner','archive','list','detail'].map(x=>'/api/staging/marketplace/'+x));
const b64=v=>Buffer.from(v).toString('base64url');
const hex=v=>createHash('sha256').update(v).digest('hex');
const identifier=v=>typeof v==='string'&&/^[A-Za-z0-9_-]{1,100}$/.test(v);
const number=v=>Number.isSafeInteger(v)&&v>=0;
const bodyBytes=v=>v instanceof Uint8Array&&v.byteLength<=32768;
const validPath=(path,body)=>typeof path==='string'&&exactRoutes.has(path)&&body.byteLength<=(['/api/staging/marketplace/list','/api/staging/marketplace/detail'].includes(path)?4096:32768);
const allowedKeys=['v','kid','method','path','bodyHash','authHash','attestationHash','nonce','issuedAtMs','expiresAtMs'];
const validatePayload=p=>p&&Object.getPrototypeOf(p)===Object.prototype&&Object.keys(p).join(',')===allowedKeys.join(',')&&p.v===purpose&&identifier(p.kid)&&p.method==='POST'&&typeof p.path==='string'&&exactRoutes.has(p.path)&&[p.bodyHash,p.authHash,p.attestationHash].every(s=>typeof s==='string'&&/^[0-9a-f]{64}$/.test(s))&&typeof p.nonce==='string'&&/^[A-Za-z0-9_-]{22}$/.test(p.nonce)&&number(p.issuedAtMs)&&number(p.expiresAtMs)&&p.expiresAtMs>p.issuedAtMs&&p.expiresAtMs-p.issuedAtMs<=30000;
const attestation=s=>typeof s==='string'&&s.length>=20&&s.length<=8192&&/^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(s);
const authorization=v=>v===null||typeof v==='string'&&v.length<=8199&&/^Bearer [A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(v);
const message=payload=>Buffer.from(JSON.stringify(payload),'utf8');
const pubkey=k=>k instanceof KeyObject&&k.type==='public'&&k.asymmetricKeyType==='rsa'&&Number.isInteger(k.asymmetricKeyDetails?.modulusLength)&&k.asymmetricKeyDetails.modulusLength>=2048&&k.asymmetricKeyDetails.modulusLength<=4096&&k.asymmetricKeyDetails.publicExponent===65537n;
const stopped=signal=>signal?.aborted===true;
async function bounded(operation,signal,ms){
 const ctl=new AbortController(),abort=()=>ctl.abort();
 signal?.addEventListener('abort',abort,{once:true});if(stopped(signal))abort();
 const timeout=setTimeout(abort,ms);
 try{
  if(stopped(ctl.signal))return null;
  const timeoutResult=new Promise((_,reject)=>{ctl.signal.addEventListener('abort',()=>reject(Error('Proof stopped')),{once:true});if(stopped(ctl.signal))reject(Error('Stopped'));});
  timeoutResult.catch(()=>{});
  return await Promise.race([Promise.resolve().then(()=>operation(ctl.signal)),timeoutResult]);
 }catch{return null;}
 finally{clearTimeout(timeout);signal?.removeEventListener('abort',abort);}
}

// signMessage is a trusted server-side signer. Never accept a private key or
// signature from the browser. A keyless provider for it is NOT selected here.
export function createMarketplaceRequestProofSigner({enabled=false,kid,signMessage,now=Date.now,random=randomBytes,lifeMs=15000,timeoutMs=1000}={}){
 if(enabled!==true||!identifier(kid)||typeof signMessage!=='function'||typeof now!=='function'||typeof random!=='function'||!Number.isInteger(lifeMs)||lifeMs<1000||lifeMs>30000||!Number.isInteger(timeoutMs)||timeoutMs<1||timeoutMs>1000)return null;
 return async({method,path,body,authorization:auth=null,attestationToken,signal}={})=>{
  try{
   if(method!=='POST'||!bodyBytes(body)||!validPath(path,body)||!authorization(auth)||!attestation(attestationToken)||stopped(signal))return null;
   const clock=now();if(!number(clock)||!number(clock+lifeMs))return null;
   const nonceBytes=random(16);if(!(nonceBytes instanceof Uint8Array)||nonceBytes.length!==16)return null;
   const nonce=b64(nonceBytes);
   const payload={v:purpose,kid,method:'POST',path,bodyHash:hex(body),authHash:hex(auth??''),attestationHash:hex(attestationToken),nonce,issuedAtMs:clock,expiresAtMs:clock+lifeMs};
   const bytes=message(payload);
   const signature=await bounded(sig=>signMessage(bytes,{signal:sig,kid}),signal,timeoutMs);
   if(!(signature instanceof Uint8Array)||signature.length<256||signature.length>512||stopped(signal)||!number(now())||now()>=payload.expiresAtMs)return null;
   const proof=b64(bytes)+'.'+b64(signature);
   return proof.length<=2048?proof:null;
  }catch{return null;}
 };
}

// Verifier MUST be called only after independent cryptographic gateway identity
// attestation and Cloud Run IAM checks, before the marketplace operation starts.
// consumeNonce must be transactional/durable across instances; in-memory maps
// are suitable ONLY for local synthetic tests, never a hosted binding.
export function createMarketplaceRequestProofVerifier({enabled=false,resolvePublicKey,consumeNonce,authorizeBeforeNonce,now=Date.now,maxAgeMs=15000,skewMs=2000,timeoutMs=1000}={}){
 if(enabled!==true||typeof resolvePublicKey!=='function'||typeof consumeNonce!=='function'||authorizeBeforeNonce!==undefined&&typeof authorizeBeforeNonce!=='function'||typeof now!=='function'||!Number.isInteger(maxAgeMs)||maxAgeMs<1000||maxAgeMs>30000||!Number.isInteger(skewMs)||skewMs<0||skewMs>3000||!Number.isInteger(timeoutMs)||timeoutMs<1||timeoutMs>1000)return null;
 return async({proof,method,path,body,authorization:auth=null,attestationToken,signal}={})=>{
  try{
   if(method!=='POST'||typeof proof!=='string'||proof.length>2048||!bodyBytes(body)||!validPath(path,body)||!authorization(auth)||!attestation(attestationToken)||stopped(signal))return false;
   const parts=proof.split('.');if(parts.length!==2||!parts.every(s=>/^[A-Za-z0-9_-]+$/.test(s)))return false;
   const payloadBytes=Buffer.from(parts[0],'base64url'),signature=Buffer.from(parts[1],'base64url');
   if(payloadBytes.length>768||payloadBytes.toString('base64url')!==parts[0]||signature.length<256||signature.length>512||signature.toString('base64url')!==parts[1])return false;
   const data=new TextDecoder('utf-8',{fatal:true}).decode(payloadBytes);
   const payload=JSON.parse(data);if(!validatePayload(payload)||JSON.stringify(payload)!==data||payload.path!==path||payload.bodyHash!==hex(body)||payload.authHash!==hex(auth??'')||payload.attestationHash!==hex(attestationToken))return false;
   const clock=now();if(!number(clock)||payload.issuedAtMs>clock+skewMs||clock-payload.issuedAtMs>maxAgeMs||payload.expiresAtMs<=clock)return false;
   const key=await bounded(sig=>resolvePublicKey({kid:payload.kid,signal:sig}),signal,timeoutMs);
   if(!pubkey(key)||signature.length!==Math.ceil(key.asymmetricKeyDetails.modulusLength/8)||!verify('RSA-SHA256',payloadBytes,{key,padding:constants.RSA_PKCS1_PADDING},signature)||stopped(signal))return false;
   const fresh=()=>{const t=now();return number(t)&&payload.issuedAtMs<=t+skewMs&&t-payload.issuedAtMs<=maxAgeMs&&payload.expiresAtMs>t;};
   if(!fresh())return false;
   // Optional trusted authentication gate AFTER signature, BEFORE nonce writes.
   // Pass immutable strings only, not mutable body/proof objects.
   if(authorizeBeforeNonce!==undefined&&await bounded(sig=>authorizeBeforeNonce({method,path,authorization:auth,bodyHash:payload.bodyHash,authHash:payload.authHash,proofSha256:hex(payloadBytes)},{signal:sig}),signal,timeoutMs)!==true)return false;
   if(!fresh()||stopped(signal))return false;
   // Never persist the raw nonce, signed header, Firebase bearer, body or ID JWT.
   const nonceHash=hex(JSON.stringify([purpose,payload.kid,payload.nonce]));
   const decision=await bounded(sig=>consumeNonce({nonceHash,expiresAtMs:payload.expiresAtMs,signal:sig}),signal,timeoutMs);
   return decision?.allowed===true&&!stopped(signal)&&fresh();
  }catch{return false;}
 };
}

// Pure canonical payload parser shared by the FUTURE durable signing gate.
// Parsing is never identity/authentication; the existing verifier still checks
// the actual RSA signature, request bindings and transactional nonce.
export function parseMarketplaceCanonicalProofPayload(bytes) {
  try {
    if(!(bytes instanceof Uint8Array)||bytes.byteLength<1||bytes.byteLength>768)return null;
    const text=new TextDecoder('utf-8',{fatal:true}).decode(bytes),p=JSON.parse(text);
    return validatePayload(p)&&JSON.stringify(p)===text?Object.freeze(p):null;
  }catch{return null;}
}
