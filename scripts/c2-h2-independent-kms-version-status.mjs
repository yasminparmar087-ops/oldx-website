import {createHash,createPublicKey} from 'node:crypto';
import {c2Crc32c} from './c2-kms-request-signing.mjs';

// H2S SOURCE ONLY — no credentials, network, IAM, Cloud Run or listener.
// This verifies raw KMS REST GET version + GET publicKey responses obtained by
// an INDEPENDENT, trusted status reader; NOT by Gateway's signer-only SA.
// H2N historical proof is a PIN, not proof of the key's present state.
// The reading identity, IAM, TLS/endpoint, private deployment and approval
// MUST be verified separately before supplying the two callback providers.
export const H2S_VERSION='projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1';
export const H2S_ALGORITHM='RSA_SIGN_PKCS1_2048_SHA256';
export const H2S_SPKI_SHA256='69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba';
export const H2S_VERSION_URL='https://cloudkms.googleapis.com/v1/'+H2S_VERSION;
export const H2S_PUBLIC_URL=H2S_VERSION_URL+'/publicKey';
const fail=()=>{throw Error('C2_H2_KEY_STATUS_UNVERIFIED');};
const time=n=>Number.isSafeInteger(n)&&n>=0;
const plain=x=>x&&typeof x==='object'&&!Array.isArray(x)&&
  Object.getPrototypeOf(x)===Object.prototype;
const crc=x=>typeof x==='string'&&/^(0|[1-9][0-9]{0,9})$/.test(x)&&
  Number(x)<=4294967295;
function validVersion(v){
  return plain(v)&&v.name===H2S_VERSION&&v.state==='ENABLED'&&
    v.algorithm===H2S_ALGORITHM&&v.protectionLevel==='SOFTWARE';
}
function validPublic(p){
  if(!plain(p)||p.algorithm!==H2S_ALGORITHM||
     (p.name!==undefined&&p.name!==H2S_VERSION)||
     (p.protectionLevel!==undefined&&p.protectionLevel!=='SOFTWARE')||
     typeof p.pem!=='string'||p.pem.length>8192||
     !p.pem.startsWith('-----BEGIN PUBLIC KEY-----\n')||
     !p.pem.trimEnd().endsWith('-----END PUBLIC KEY-----')||
     !crc(p.pemCrc32c)||c2Crc32c(Buffer.from(p.pem,'utf8'))!==p.pemCrc32c)return false;
  try{
    const pub=createPublicKey(p.pem);
    if(pub.type!=='public'||pub.asymmetricKeyType!=='rsa'||
       pub.asymmetricKeyDetails?.modulusLength!==2048||
       pub.asymmetricKeyDetails?.publicExponent!==65537n)return false;
    const der=pub.export({format:'der',type:'spki'});
    return createHash('sha256').update(der).digest('hex')===H2S_SPKI_SHA256;
  }catch{return false;}
}

// Both operations are bounded and validated. No local caching: each instance
// may call once; a consumed result does not authorize another invocation.
// All failure paths stop, without calling sign, allocating an IAM role or
// replacing the original H2N evidence.
export function createC2H2IndependentKmsVersionStatus({
  enabled=false,readExactVersion,readExactPublicKey,
  validFromMs,validUntilMs,now=Date.now,
}={}){
  const ready=enabled===true&&
    typeof readExactVersion==='function'&&
    typeof readExactPublicKey==='function'&&typeof now==='function'&&
    time(validFromMs)&&time(validUntilMs)&&validUntilMs>validFromMs&&
    validUntilMs-validFromMs<=120000;
  let consumed=false;
  return Object.freeze({
    ready,
    async getTrustedKeyVersionStatus({name,signal}={}){
      if(!ready||consumed||name!==H2S_VERSION||signal?.aborted)fail();
      consumed=true;
      const controller=new AbortController();
      const abort=()=>controller.abort();
      signal?.addEventListener('abort',abort,{once:true});
      if(signal?.aborted)abort();
      const stopped=new Promise((_,reject)=>{
        controller.signal.addEventListener('abort',()=>reject(Error('stopped')),{once:true});
        if(controller.signal.aborted)reject(Error('stopped'));
      });
      stopped.catch(()=>{});
      const wait=fn=>Promise.race([
        Promise.resolve().then(()=>{if(controller.signal.aborted)fail();return fn();}),
        stopped,
      ]);
      const timer=setTimeout(abort,600);
      const check=()=>{
        const t=now();
        if(!time(t)||t<validFromMs||t>=validUntilMs||controller.signal.aborted)fail();
      };
      try{
        check();
        const v=await wait(()=>readExactVersion({
          name:H2S_VERSION,url:H2S_VERSION_URL,signal:controller.signal,
        }));
        check();
        if(!validVersion(v))fail();
        const p=await wait(()=>readExactPublicKey({
          name:H2S_VERSION,url:H2S_PUBLIC_URL,signal:controller.signal,
        }));
        check();
        if(!validPublic(p))fail();
        return Object.freeze({
          name:H2S_VERSION,state:'ENABLED',algorithm:H2S_ALGORITHM,
          publicKeySha256:H2S_SPKI_SHA256,
        });
      }catch{fail();}
      finally{
        clearTimeout(timer);
        signal?.removeEventListener('abort',abort);
        controller.abort();
      }
    },
  });
}

// A small pure predicate lets focused tests validate the metadata half without
// misrepresenting unprovided H2N public PEM as a live status read.
export function c2H2VersionMetadataMatches(value){
  return validVersion(value);
}
