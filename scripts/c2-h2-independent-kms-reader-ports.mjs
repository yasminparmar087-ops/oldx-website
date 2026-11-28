import {H2S_VERSION,H2S_VERSION_URL,H2S_PUBLIC_URL} from './c2-h2-independent-kms-version-status.mjs';
import {c2LifecycleBoundary} from './c2-h2-lifecycle-boundary.mjs';
import {parseBoundedJson} from './bounded-json.mjs';
const gate='oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
const fail=()=>{throw Error('C2_INDEPENDENT_READER_UNAVAILABLE');};
// Source-only authenticated GET transport, not a claim that a reader SA exists
// or has IAM. Credential/authority providers are SERVER trust boundaries.
// Existing H2S verifier independently checks actual version/PEM/CRC/SPKI.
export function createC2H2IndependentKmsReaderPorts({enabled=false,readerPrincipal,
  readerUid,getReaderCredential,verifyReaderAuthority,consumeDurableReadBudget,
  fetchReader,now=Date.now}={}) {
  const ready=enabled===true&&typeof readerPrincipal==='string'&&
    /^[a-z][a-z0-9-]{4,28}[a-z0-9]@oldx-staging\.iam\.gserviceaccount\.com$/.test(readerPrincipal)&&
    ![gate,'oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com',
      'oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com'].includes(readerPrincipal)&&
    !['107238619872767759560','100779414920484819274','106984791114720194680'].includes(readerUid)&&
    typeof readerUid==='string'&&/^\d{1,32}$/.test(readerUid)&&
    [getReaderCredential,verifyReaderAuthority,consumeDurableReadBudget,fetchReader,now].every(x=>typeof x==='function');
  async function read(input,expected) {
    if(!ready||input?.name!==H2S_VERSION||input?.url!==expected)fail();
    try{return await c2LifecycleBoundary(async signal=>{
      const at=now();if(!Number.isSafeInteger(at))fail();
      const authority=await verifyReaderAuthority({principal:readerPrincipal,uid:readerUid,
        keyVersion:H2S_VERSION,operation:'GET',url:expected},{signal});
      if(authority?.authorized!==true||authority.principal!==readerPrincipal||
         authority.uid!==readerUid||authority.keyVersion!==H2S_VERSION||
         !Number.isSafeInteger(authority.expiresAtMs)||authority.expiresAtMs<=now())fail();
      const budget=await consumeDurableReadBudget({keyVersion:H2S_VERSION,url:expected},{signal});
      if(budget?.allowed!==true||signal.aborted)fail();
      const credential=await getReaderCredential({principal:readerPrincipal,uid:readerUid},{signal});
      if(credential?.principal!==readerPrincipal||credential.uid!==readerUid||
         credential.source!=='cloud-run-metadata'||typeof credential.accessToken!=='string'||
         !/^[A-Za-z0-9._~-]{40,4096}$/.test(credential.accessToken)||
         !Number.isSafeInteger(credential.expiresAtMs)||credential.expiresAtMs<=now()+1000||
         credential.expiresAtMs>now()+3600000||authority.expiresAtMs<=now()||signal.aborted)fail();
      const response=await fetchReader(expected,{method:'GET',headers:{Authorization:'Bearer '+credential.accessToken,
        Accept:'application/json'},redirect:'error',credentials:'omit',cache:'no-store',signal});
      if(!(response instanceof Response)||response.status!==200||response.redirected||
         response.url&&response.url!==expected||!/^application\/json(?:;|$)/i.test(response.headers.get('content-type')??'')||
         !response.body)fail();
      const reader=response.body.getReader(),chunks=[];let size=0;
      try{for(;;){const {done,value}=await reader.read();if(done)break;
        size+=value.byteLength;if(size>16384)fail();chunks.push(value);}}
      finally{void reader.cancel().catch(()=>{});}
      if(signal.aborted||authority.expiresAtMs<=now())fail();
      const result=parseBoundedJson(Buffer.concat(chunks),{maxBytes:16384});
      if(!result.ok)fail();return result.value;
    },{signal:input.signal,timeoutMs:600});}catch{fail();}
  }
  return Object.freeze({ready,
    readExactVersion:input=>read(input,H2S_VERSION_URL),
    readExactPublicKey:input=>read(input,H2S_PUBLIC_URL)});
}
