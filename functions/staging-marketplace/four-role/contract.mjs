import {createHash,createPublicKey,verify,constants} from 'node:crypto';
export const ROLES=Object.freeze({
 mediator:Object.freeze({principal:'oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com',uid:'100779414920484819274',imageName:'oldx-c2-mediator-h2ah'}),
 gateway:Object.freeze({principal:'oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com',uid:'107238619872767759560',imageName:'oldx-c2-gateway-h2ah'}),
 backend:Object.freeze({principal:'oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com',uid:'106984791114720194680',imageName:'oldx-c2-backend-h2ah'}),
 reader:Object.freeze({principal:'oldx-c2-kms-reader@oldx-staging.iam.gserviceaccount.com',uid:'107336955065718475994',imageName:'oldx-c2-kms-reader'}),
});
export const sha=value=>createHash('sha256').update(value).digest('hex');
export const data=x=>x!==null&&typeof x==='object'&&Object.getPrototypeOf(x)===Object.prototype&&
 Reflect.ownKeys(x).every(k=>typeof k==='string'&&Object.hasOwn(Object.getOwnPropertyDescriptor(x,k),'value'));
export function canonical(x){
 if(x===null||typeof x==='string'||typeof x==='boolean'||Number.isSafeInteger(x))return JSON.stringify(x);
 if(Array.isArray(x))return '['+x.map(canonical).join(',')+']';
 if(!data(x))throw Error('H2AH_INVALID_RECORD');
 return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}';
}
const freeze=x=>{if(x&&typeof x==='object'){Object.values(x).forEach(freeze);Object.freeze(x);}return x;};
export const runOrigin=x=>{try{const u=new URL(x);return u.origin===x&&u.protocol==='https:'&&
 /^[-a-z0-9]+\.[-a-z0-9]+\.run\.app$/.test(u.hostname)&&!u.username&&!u.password;}catch{return false;}};
const old=new Set(['576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e',
 '612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a',
 '4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2']);
const authorities=new WeakSet();
// External controller attestation must come from independently trusted operator
// custody, after actual source/image/attachment/IAM/network readback. Config and
// K_REVISION alone cannot prove any of those facts. No deployment is performed.
export function createFourRoleAuthority({enabled=false,configuration,envelope,
 controllerPublicKeyPem,controllerSpkiSha256,now=Date.now}={}){
 if(enabled!==true)return null;
 try{
 const c=JSON.parse(canonical(configuration)),clock=now();
 if(c.v!==1||c.purpose!=='oldx.h2ah.four-private-hosts.v1'||c.projectId!=='oldx-staging'||
 c.databaseId!=='(default)'||!/^[a-f0-9]{40}$/.test(c.sourceRevision)||
 !/^[a-f0-9]{64}$/.test(c.policyDigest)||!/^[a-f0-9]{64}$/.test(c.releaseDigest)||
 !/^[a-f0-9]{64}$/.test(c.lifecycleApprovalKeySha256)||!Number.isSafeInteger(clock)||
 !Number.isSafeInteger(c.startsAtMs)||!Number.isSafeInteger(c.expiresAtMs)||
 c.startsAtMs>clock||c.expiresAtMs<=clock||c.expiresAtMs-c.startsAtMs>1200000||
 c.network?.ingress!=='internal'||c.network.vpcEgress!=='all-traffic'||
 c.network.privateGoogleAccess!==true||
 !/^projects\/oldx-staging\/global\/networks\/[a-z][a-z0-9-]{0,62}$/.test(c.network.vpc)||
 !/^projects\/oldx-staging\/regions\/asia-south1\/subnetworks\/[a-z][a-z0-9-]{0,62}$/.test(c.network.subnet)||
 !data(c.roles)||Object.keys(c.roles).sort().join(',')!=='backend,gateway,mediator,reader')return null;
 for(const [role,pin]of Object.entries(ROLES)){
 const r=c.roles[role],prefix='asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/'+pin.imageName+'@sha256:';
 if(!data(r)||r.principal!==pin.principal||r.uid!==pin.uid||!runOrigin(r.origin)||
 typeof r.image!=='string'||!r.image.startsWith(prefix)||!/^[a-f0-9]{64}$/.test(r.image.slice(prefix.length))||
 old.has(r.image.slice(-64))||!/^[a-z0-9][a-z0-9-]{0,80}$/.test(r.revision)||
 !/^[a-f0-9]{64}$/.test(r.attachmentEvidenceSha256))return null;
 }
 if(new Set(Object.values(c.roles).map(r=>r.image)).size!==4||
 new Set(Object.values(c.roles).map(r=>r.origin)).size!==4)return null;
 const key=createPublicKey(controllerPublicKeyPem),bits=key.asymmetricKeyDetails?.modulusLength;
 if(key.asymmetricKeyType!=='rsa'||bits<2048||bits>4096||key.asymmetricKeyDetails?.publicExponent!==65537n||
 sha(key.export({type:'spki',format:'der'}))!==controllerSpkiSha256)return null;
 const bytes=Buffer.from(canonical(c)),signature=Buffer.from(envelope?.signature??'','base64url');
 if(envelope?.payload!==bytes.toString('base64url')||signature.length!==bits/8||
 signature.toString('base64url')!==envelope.signature||
 !verify('RSA-SHA256',bytes,{key,padding:constants.RSA_PKCS1_PADDING},signature))return null;
 const value=Object.freeze({configuration:freeze(c),digest:sha(bytes),
 fresh(){const t=now();return Number.isSafeInteger(t)&&t>=c.startsAtMs&&t<c.expiresAtMs;}});
 authorities.add(value);return value;
 }catch{return null;}
}
export function requireFourRoleAuthority(value){
 if(!authorities.has(value)||!value.fresh())throw Error('H2AH_RUNTIME_AUTHORITY_UNAVAILABLE');return value;
}
