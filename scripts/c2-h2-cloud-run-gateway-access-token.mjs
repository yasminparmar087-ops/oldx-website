// OLDX Step05 H2S — FUTURE private Cloud Run Gateway only, SOURCE/DEFAULT OFF.
// OAuth access-token provider for Cloud KMS asymmetricSign; NOT the existing
// Cloud Run IAM audience-bound ID-token provider. No network at import time,
// ambient fetch, ADC, SA JSON key, Owner token or impersonation. The injected
// host transport MUST use the actual Cloud Run instance metadata server.
// Metadata email is checked; pinned UID is a known control-plane mapping, NOT
// a cryptographic UID assertion from the access token. The actual deployed
// revision/attached SA UID/Invoker/image must be independently verified.
const EMAIL='oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
const UID='107238619872767759560';
const BASE='http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/';
const EMAIL_URL=BASE+'email';
const TOKEN_URL=BASE+'token';
const fail=()=>{throw Error('C2_H2_WORKLOAD_CREDENTIAL_UNAVAILABLE');};
const time=v=>Number.isSafeInteger(v)&&v>=0;
const TOKEN_PATTERN=/^[A-Za-z0-9._~+-]{40,4096}$/;

async function boundedRead(response,expected,maxBytes,wait,signal){
  if(signal.aborted||!(response instanceof Response)||response.status!==200||
     !response.ok||response.redirected||
     (response.url&&response.url!==expected)||
     response.headers.get('Metadata-Flavor')!=='Google'||
     !response.body)fail();
  const size=response.headers.get('content-length');
  if(size!==null&&(!/^[0-9]{1,6}$/.test(size)||Number(size)>maxBytes))fail();
  const reader=response.body.getReader();
  let bytes=0;const chunks=[];
  try{
    for(;;){
      if(signal.aborted)fail();
      const {done,value}=await wait(()=>reader.read());
      if(done)break;
      bytes+=value.byteLength;
      if(bytes>maxBytes)fail();
      chunks.push(Buffer.from(value));
    }
  }finally{void reader.cancel().catch(()=>{});}
  if(signal.aborted)fail();
  try{return new TextDecoder('utf-8',{fatal:true}).decode(Buffer.concat(chunks,bytes));}
  catch{fail();}
}

// One credential acquisition for ONE synthetic signing attempt; no hidden
// refresh or retry. If a signing request is denied, token is never reused.
export function createC2H2GatewayMetadataAccessToken({
  enabled=false,serviceAccount,serviceAccountUid,fetchMetadata,now=Date.now,
}={}){
  const ready=enabled===true&&serviceAccount===EMAIL&&
    serviceAccountUid===UID&&typeof fetchMetadata==='function'&&
    typeof now==='function';
  let attempted=false;
  return Object.freeze({
    ready,
    async getTrustedWorkloadCredential({signal,forPrincipal}={}){
      if(!ready||attempted||signal?.aborted||forPrincipal!==EMAIL)fail();
      attempted=true;
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
      const timer=setTimeout(abort,1500);
      try{
        const start=now();
        if(!time(start)||controller.signal.aborted)fail();
        const fetchOne=async(url,maxBytes)=>{
          if(url!==EMAIL_URL&&url!==TOKEN_URL)fail();
          const res=await wait(()=>fetchMetadata(url,{
            method:'GET',headers:{'Metadata-Flavor':'Google'},
            redirect:'error',cache:'no-store',credentials:'omit',
            signal:controller.signal,
          }));
          return boundedRead(res,url,maxBytes,wait,controller.signal);
        };
        const observedEmail=(await fetchOne(EMAIL_URL,320)).trim();
        if(observedEmail!==EMAIL||controller.signal.aborted)fail();
        const raw=await fetchOne(TOKEN_URL,8192);
        const item=JSON.parse(raw);
        if(!item||Object.getPrototypeOf(item)!==Object.prototype||
           Reflect.ownKeys(item).sort().join(',')!==
             'access_token,expires_in,token_type'||
           item.token_type!=='Bearer'||!TOKEN_PATTERN.test(item.access_token)||
           !Number.isSafeInteger(item.expires_in)||item.expires_in<10||
           item.expires_in>3600)fail();
        const at=now();
        const expiresAtMs=at+item.expires_in*1000;
        if(controller.signal.aborted||!time(at)||at<start||
           at-start>1500||!time(expiresAtMs)||
           expiresAtMs<=at+3000||expiresAtMs>at+3600000)fail();
        return Object.freeze({
          principal:EMAIL,uid:UID,source:'cloud-run-metadata',
          accessToken:item.access_token,expiresAtMs,
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
