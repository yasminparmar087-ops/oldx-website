import {createHash,createPublicKey,verify,constants} from 'node:crypto';
import {requireC2H2MultiSignLifecyclePolicy} from './c2-h2-lifecycle-signing-status-contract.mjs';
import {copyRecord} from './isolated-firestore-context.mjs';
const approvedVerifiers=new WeakMap();
export function requireC2H2LifecycleApprovalVerifier(value,policy){
  if(approvedVerifiers.get(value)!==policy)throw Error('C2_LIFECYCLE_APPROVAL_UNVERIFIED');return value;
}
const sha=x=>createHash('sha256').update(x).digest('hex');
// A server-held independent APPROVAL of policy, not a replacement for fresh
// per-request Gateway signatures or Firebase authentication. Public-key pin and
// envelope must arrive through separately verified operator custody, not HTTP.
export function createC2H2LifecycleApprovalVerifier({enabled=false,policy,
  publicKeyPem,publicKeySha256,envelope,now=Date.now}={}) {
  const off=async()=>({authorized:false});if(enabled!==true)return off;
  let p,key,payload,signature,policyDigest;
  try {
    p=requireC2H2MultiSignLifecyclePolicy(policy);
    key=createPublicKey(publicKeyPem);
    const bits=key.asymmetricKeyDetails?.modulusLength;
    if(key.type!=='public'||key.asymmetricKeyType!=='rsa'||bits<2048||bits>4096||
       key.asymmetricKeyDetails?.publicExponent!==65537n||
       sha(key.export({type:'spki',format:'der'}))!==publicKeySha256)return off;
    const e=copyRecord(envelope,['payload','signature']);
    if(!e||typeof e.payload!=='string'||e.payload.length>2048||
       typeof e.signature!=='string'||e.signature.length>684)return off;
    payload=Buffer.from(e.payload,'base64url');signature=Buffer.from(e.signature,'base64url');
    if(payload.toString('base64url')!==e.payload||signature.toString('base64url')!==e.signature||
       signature.length!==bits/8)return off;
    policyDigest=sha(JSON.stringify(p));
    const exact={v:1,purpose:'oldx.c2.independent.multisign.approval.v1',policyDigest,
      mode:p.mode,maxSignAttempts:6,startsAtMs:p.startsAtMs,expiresAtMs:p.expiresAtMs};
    if(!payload.equals(Buffer.from(JSON.stringify(exact)))||
       !verify('RSA-SHA256',payload,{key,padding:constants.RSA_PKCS1_PADDING},signature))return off;
  }catch{return off;}
  const result=async(input,{signal}={})=>{
    const at=now();
    if(signal?.aborted||!Number.isSafeInteger(at)||at<p.startsAtMs||at>=p.expiresAtMs||
       input?.policyDigest!==policyDigest||input?.policy!==p)return {authorized:false};
    return Object.freeze({authorized:true,policyDigest,mode:p.mode,
      maxSignAttempts:6,expiresAtMs:p.expiresAtMs});
  };
  approvedVerifiers.set(result,p);return result;
}
