// BAJUTO/OLDX Step05 H2AH: SOURCE-ONLY separate private reader workload.
// This is NOT an HTTP server/deployment, and cannot impersonate another SA.
// The attached Cloud Run reader identity, revision and immutable child image
// MUST be verified by an independent host controller before reading metadata.
// Never use Gateway signer/Owner creds, local ADC, SA JSON keys, or global fetch.
// The existing permanent cross-instance stage ledger MUST separately authorize
// every KMS GET (at most 24 slots per separately approved synthetic run).
import {createC2H2IndependentKmsReaderPorts} from './c2-h2-independent-kms-reader-ports.mjs';
export const C2_H2AG_READER_EMAIL='oldx-c2-kms-reader@oldx-staging.iam.gserviceaccount.com';
export const C2_H2AG_READER_UID='107336955065718475994';
const BASE='http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/';
const EMAIL_URL=BASE+'email';
const TOKEN_URL=BASE+'token';
const IMAGE=/^asia-south1-docker\.pkg\.dev\/oldx-staging\/oldx-staging-images\/oldx-c2-kms-reader@sha256:[0-9a-f]{64}$/;
const deny=()=>{throw Error('C2_H2AG_READER_RUNTIME_NOT_VERIFIED');};
const int=x=>Number.isSafeInteger(x)&&x>=0;
const plain=x=>x!==null&&typeof x==='object'&&!Array.isArray(x)&&Object.getPrototypeOf(x)===Object.prototype&&
  Reflect.ownKeys(x).every(k=>typeof k==='string'&&Object.hasOwn(Object.getOwnPropertyDescriptor(x,k),'value'));
const credentialPattern=/^[A-Za-z0-9._~+\-]{40,4096}$/;

async function boundedText(response,url,limit,signal,abort){
  if(signal.aborted||!(response instanceof Response)||response.status!==200||
     !response.ok||response.redirected||(response.url&&response.url!==url)||
     response.headers.get('Metadata-Flavor')!=='Google'||!response.body)deny();
  const cl=response.headers.get('content-length');
  if(cl!==null&&(!/^\d{1,6}$/.test(cl)||Number(cl)>limit))deny();
  const reader=response.body.getReader(),chunks=[];let length=0;
  try{for(;;){
    if(signal.aborted)deny();
    const part=await abort(()=>reader.read());
    if(part.done)break;
    length+=part.value.byteLength;
    if(length>limit)deny();
    chunks.push(part.value);
  }}finally{void reader.cancel().catch(()=>{});}
  if(signal.aborted)deny();
  try{
    const bytes=new Uint8Array(length);let offset=0;
    for(const item of chunks){bytes.set(item,offset);offset+=item.byteLength;}
    return new TextDecoder('utf-8',{fatal:true}).decode(bytes);
  }catch{deny();}
}

export function createC2H2AGReaderMetadataSource({enabled=false,
 readerEmail,readerUid,readerImage,verifyRuntimeBinding,
 fetchMetadata,now=Date.now}={}){
 const ready=enabled===true&&readerEmail===C2_H2AG_READER_EMAIL&&
   readerUid===C2_H2AG_READER_UID&&typeof readerImage==='string'&&IMAGE.test(readerImage)&&
   typeof verifyRuntimeBinding==='function'&&typeof fetchMetadata==='function'&&
   typeof now==='function';
 return Object.freeze({ready,readerEmail:C2_H2AG_READER_EMAIL,readerUid:C2_H2AG_READER_UID,
 async getReaderCredential({principal,uid},{signal}={}){
   if(!ready||principal!==C2_H2AG_READER_EMAIL||uid!==C2_H2AG_READER_UID||signal?.aborted)deny();
   const ctl=new AbortController(),cancel=()=>ctl.abort();
   signal?.addEventListener('abort',cancel,{once:true});
   if(signal?.aborted)cancel();
   const stopped=new Promise((_,reject)=>{
     ctl.signal.addEventListener('abort',()=>reject(Error('ABORT')),{once:true});
     if(ctl.signal.aborted)reject(Error('ABORT'));
   });stopped.catch(()=>{});
   const timer=setTimeout(cancel,1200);
   const abort=fn=>Promise.race([Promise.resolve().then(()=>{
     if(ctl.signal.aborted)deny();return fn();
   }),stopped]);
   try{
     const start=now();if(!int(start)||ctl.signal.aborted)deny();
     const evidence=await abort(()=>verifyRuntimeBinding({
       principal:C2_H2AG_READER_EMAIL,uid:C2_H2AG_READER_UID,image:readerImage,
     },{signal:ctl.signal}));
     if(!plain(evidence)||Reflect.ownKeys(evidence).length!==4||
        evidence.principal!==C2_H2AG_READER_EMAIL||evidence.uid!==C2_H2AG_READER_UID||
        evidence.image!==readerImage||!int(evidence.expiresAtMs)||
        evidence.expiresAtMs<=now()+1500||ctl.signal.aborted)deny();
     const fetchOne=async(url,limit)=>boundedText(await abort(()=>fetchMetadata(url,{
       method:'GET',headers:{'Metadata-Flavor':'Google'},redirect:'error',
       cache:'no-store',credentials:'omit',signal:ctl.signal,
     })),url,limit,ctl.signal,abort);
     if((await fetchOne(EMAIL_URL,320)).trim()!==C2_H2AG_READER_EMAIL)deny();
     const parsed=JSON.parse(await fetchOne(TOKEN_URL,8192));
     if(!plain(parsed)||Reflect.ownKeys(parsed).sort().join(',')!==
       'access_token,expires_in,token_type'||parsed.token_type!=='Bearer'||
       !credentialPattern.test(parsed.access_token)||
       !Number.isSafeInteger(parsed.expires_in)||parsed.expires_in<10||parsed.expires_in>3600)deny();
     const at=now(),expiresAtMs=at+parsed.expires_in*1000;
     if(!int(at)||at<start||at-start>1200||!int(expiresAtMs)||
       expiresAtMs<=at+3000||expiresAtMs>at+3600000||
       ctl.signal.aborted||evidence.expiresAtMs<=at)deny();
     return Object.freeze({source:'cloud-run-metadata',principal:C2_H2AG_READER_EMAIL,
       uid:C2_H2AG_READER_UID,accessToken:parsed.access_token,expiresAtMs:
         Math.min(expiresAtMs,evidence.expiresAtMs)});
   }catch{deny();}
   finally{clearTimeout(timer);signal?.removeEventListener('abort',cancel);ctl.abort();}
 }});
}

// Composer for existing exact KMS read adapter; NO listener or KMS request on
// import/construction. The trusted host MUST separately prove IAM Invoker,
// cryptographic Gateway/Backend caller identity, stage ledger and IAM/key roles.
export function createC2H2AGReaderSourcePorts({enabled=false,
  metadataOptions,verifyReaderAuthority,consumeDurableReadBudget,fetchReader,now=Date.now}={}){
 const off=Object.freeze({ready:false,readExactVersion:async()=>deny(),
   readExactPublicKey:async()=>deny()});
 if(enabled!==true||!plain(metadataOptions)||
    metadataOptions.enabled!==undefined||typeof verifyReaderAuthority!=='function'||
    typeof consumeDurableReadBudget!=='function'||typeof fetchReader!=='function')return off;
 const identity=createC2H2AGReaderMetadataSource({...metadataOptions,enabled:true,now});
 if(!identity.ready)return off;
 const provider=createC2H2IndependentKmsReaderPorts({enabled:true,
   readerPrincipal:C2_H2AG_READER_EMAIL,readerUid:C2_H2AG_READER_UID,
   getReaderCredential:identity.getReaderCredential,verifyReaderAuthority,
   consumeDurableReadBudget,fetchReader,now});
 return provider.ready?provider:off;
}
