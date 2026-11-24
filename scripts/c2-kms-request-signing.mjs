import {createHash,createPublicKey,verify,constants} from 'node:crypto';
// INACTIVE trusted server adapter. Transport is injected, never SDK/ADC/global fetch.
// REST-shaped KMS asymmetricSign contract; application intent key, NOT Google OAuth key.
export function c2Crc32c(bytes){
 let crc=0xffffffff;
 for(const byte of bytes){crc^=byte;for(let i=0;i<8;i++)crc=(crc>>>1)^((crc&1)?0x82f63b78:0);}
 return String((crc^0xffffffff)>>>0);
}
const denied=()=>{throw Error('C2_SIGNING_UNAVAILABLE');};
const int=x=>Number.isSafeInteger(x)&&x>=0;
export function createC2KmsRequestSigning({enabled=false,kid,keyVersion,algorithm,publicKeyPem,
 publicKeySha256,validFromMs,validUntilMs,asymmetricSign,getKeyVersionStatus,now=Date.now}={}){
 let publicKey=null;
 const bits={RSA_SIGN_PKCS1_2048_SHA256:2048,RSA_SIGN_PKCS1_3072_SHA256:3072,RSA_SIGN_PKCS1_4096_SHA256:4096};
 let ready=enabled===true&&typeof kid==='string'&&/^[A-Za-z0-9_-]{1,100}$/.test(kid)&&
  typeof keyVersion==='string'&&new RegExp('^projects/oldx-staging/locations/asia-south1/keyRings/[A-Za-z0-9_-]{1,63}/cryptoKeys/[A-Za-z0-9_-]{1,63}/cryptoKeyVersions/[1-9][0-9]{0,9}$').test(keyVersion)&&
  Object.hasOwn(bits,algorithm)&&typeof publicKeyPem==='string'&&publicKeyPem.length<=8192&&
  /^-----BEGIN PUBLIC KEY-----/.test(publicKeyPem)&&typeof publicKeySha256==='string'&&/^[a-f0-9]{64}$/.test(publicKeySha256)&&
  int(validFromMs)&&int(validUntilMs)&&validUntilMs>validFromMs&&validUntilMs-validFromMs<=86400000&&
  [asymmetricSign,getKeyVersionStatus,now].every(x=>typeof x==='function');
 try{
  if(ready){
   publicKey=createPublicKey(publicKeyPem);
   ready=publicKey.type==='public'&&publicKey.asymmetricKeyType==='rsa'&&
    publicKey.asymmetricKeyDetails.modulusLength===bits[algorithm]&&publicKey.asymmetricKeyDetails.publicExponent===65537n&&
    createHash('sha256').update(publicKey.export({format:'der',type:'spki'})).digest('hex')===publicKeySha256;
  }
 }catch{ready=false;}
 const fresh=()=>{const t=now();return int(t)&&t>=validFromMs&&t<validUntilMs;};
 async function run(selected,signal,operation){
  if(!ready||selected!==kid||signal?.aborted||!fresh())denied();
  const ctl=new AbortController(),abort=()=>ctl.abort();
  signal?.addEventListener('abort',abort,{once:true});if(signal?.aborted)abort();
  const timer=setTimeout(abort,750);
  const stopped=new Promise((_,reject)=>{ctl.signal.addEventListener('abort',()=>reject(Error('STOP')),{once:true});if(ctl.signal.aborted)reject(Error('STOP'));});
  try{
   return await Promise.race([(async()=>{
    if(ctl.signal.aborted)denied();
    const state=await getKeyVersionStatus({name:keyVersion,signal:ctl.signal});
    if(ctl.signal.aborted||!fresh()||state?.name!==keyVersion||state.state!=='ENABLED'||state.algorithm!==algorithm||state.publicKeySha256!==publicKeySha256)denied();
    const value=await operation(ctl.signal);
    if(ctl.signal.aborted||!fresh())denied();
    return value;
   })(),stopped]);
  }catch{denied();}
  finally{clearTimeout(timer);signal?.removeEventListener('abort',abort);}
 }
 return Object.freeze({ready,
  async signMessage(bytes,{kid:selected,signal}={}){
   if(!(bytes instanceof Uint8Array)||bytes.byteLength<1||bytes.byteLength>768)denied();
   // Snapshot canonical proof bytes before any asynchronous provider call.
   const message=Buffer.from(bytes),digest=createHash('sha256').update(message).digest();
   return run(selected,signal,async sig=>{
    const response=await asymmetricSign({name:keyVersion,digest:{sha256:digest.toString('base64')},
     digestCrc32c:c2Crc32c(digest)},{signal:sig,retry:false});
    if(response?.name!==keyVersion||response.verifiedDigestCrc32c!==true||typeof response.signature!=='string'||response.signature.length>684)denied();
    const signature=Buffer.from(response.signature,'base64');
    if(signature.toString('base64')!==response.signature||signature.length!==bits[algorithm]/8||
     response.signatureCrc32c!==c2Crc32c(signature)||
     !verify('RSA-SHA256',message,{key:publicKey,padding:constants.RSA_PKCS1_PADDING},signature))denied();
    return signature;
   });
  },
  async resolvePublicKey({kid:selected,signal}={}){return run(selected,signal,async()=>publicKey);}
 });
}

