import {c2Crc32c} from './c2-kms-request-signing.mjs';

// SOURCE ONLY, not wired to any handler or Cloud Run deployment.
// KMS REST signing port for ONE synthetic private Gateway probe. All network,
// workload identity and credential sources MUST be bound by the trusted Cloud
// Run host. No ambient fetch, ADC in browser, JSON key, impersonation or retry.
// Actual Cloud Run serviceAccount identity and image/Invoker provenance must
// be independently confirmed. Durable consume-once budget MUST be atomic across
// host instances; local Map/flag is not an acceptable hosted implementation. A returned "principal" is not attestation.
const KEY_VERSION='projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1';
const GATEWAY='oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
const GATEWAY_UID='107238619872767759560';
const ENDPOINT='https://cloudkms.googleapis.com/v1/'+KEY_VERSION+':asymmetricSign';
const fail=()=>{throw Error('C2_KMS_GATEWAY_PROBE_UNAVAILABLE');};
const canonical=(v,size)=>typeof v==='string'&&v.length>0&&
  /^[A-Za-z0-9+/]+={0,2}$/.test(v)&&(()=>{const b=Buffer.from(v,'base64');return b.length===size&&b.toString('base64')===v;})();
const uintcrc=v=>typeof v==='string'&&/^(0|[1-9][0-9]{0,9})$/.test(v)&&Number(v)<=4294967295;

// This provider deliberately does NOT supply getKeyVersionStatus, which is
// separately required by createC2KmsRequestSigning and is not authorized by
// roles/cloudkms.signer. Do NOT fabricate ENABLED or viewPublicKey privileges.
export function createC2H2GatewayKmsSyntheticTransport({enabled=false,
  expectedGatewayEmail=GATEWAY,expectedGatewayUid=GATEWAY_UID,
  keyVersion=KEY_VERSION,getTrustedWorkloadCredential,fetchKms,consumeDurableSignBudget,now=Date.now}={}){
  const ready=enabled===true&&expectedGatewayEmail===GATEWAY&&
    expectedGatewayUid===GATEWAY_UID&&keyVersion===KEY_VERSION&&
    [getTrustedWorkloadCredential,fetchKms,consumeDurableSignBudget,now].every(x=>typeof x==='function');
  let attempted=false;
  return Object.freeze({ready,expectedPrincipal:GATEWAY,
    keyVersion:KEY_VERSION,signEndpoint:ENDPOINT,
    async asymmetricSign(payload,{signal,retry=false}={}){
      if(!ready||attempted||retry!==false||signal?.aborted)fail();
      attempted=true; // one attempt BEFORE credentials or KMS; never retry
      try{
        if(payload?.name!==KEY_VERSION||
           !canonical(payload?.digest?.sha256,32)||
           !uintcrc(payload?.digestCrc32c)||
           c2Crc32c(Buffer.from(payload.digest.sha256,'base64'))!==
             payload.digestCrc32c||
           Object.keys(payload).sort().join(',')!=='digest,digestCrc32c,name'||
           Object.keys(payload.digest).join(',')!=='sha256')fail();
        const t=now();
        if(!Number.isSafeInteger(t)||t<0)fail();
        // Cross-instance atomic budget is mandatory: a per-process attempted
        // flag cannot restrict a scaled Cloud Run deployment to ONE KMS sign.
        // Host supplies a durable transactional consume-once implementation.
        const budget=await consumeDurableSignBudget(Object.freeze({
          purpose:'oldx.h2.single-synthetic-sign.v1',
          projectId:'oldx-staging',gatewayUid:GATEWAY_UID,
          keyVersion:KEY_VERSION,maxSigns:1,
        }),{signal});
        if(signal?.aborted||budget?.allowed!==true)fail();
        // A host-provided trusted workload credential source must obtain the
        // token using the *attached Gateway runtime identity* (not Owner WSL).
        // Host identity must separately be verified via Cloud Run config/IAM.
        const credential=await getTrustedWorkloadCredential({signal,forPrincipal:GATEWAY});
        if(signal?.aborted||credential?.principal!==GATEWAY||
           credential?.uid!==GATEWAY_UID||
           credential?.source!=='cloud-run-metadata'||
           typeof credential?.accessToken!=='string'||
           !/^[A-Za-z0-9._~+-]{40,4096}$/.test(credential.accessToken)||
           !Number.isSafeInteger(credential?.expiresAtMs)||
           credential.expiresAtMs<=now()+3000||
           credential.expiresAtMs>now()+3600000)fail();

        const response=await fetchKms(ENDPOINT,{
          method:'POST',redirect:'error',cache:'no-store',
          headers:{authorization:'Bearer '+credential.accessToken,
                   accept:'application/json','content-type':'application/json'},
          body:JSON.stringify({digest:payload.digest,
                               digestCrc32c:payload.digestCrc32c}),
          signal,
        });
        if(signal?.aborted||response?.status!==200||
           !/^application\/json(?:\s*;|$)/i.test(response.headers?.get?.('content-type')??''))fail();
        const raw=await response.text();
        if(signal?.aborted||typeof raw!=='string'||raw.length>4096)fail();
        const v=JSON.parse(raw);
        if(v?.name!==KEY_VERSION||v?.protectionLevel!=='SOFTWARE'||
           v?.verifiedDigestCrc32c!==true||!canonical(v?.signature,256)||
           !uintcrc(v?.signatureCrc32c)||
           c2Crc32c(Buffer.from(v.signature,'base64'))!==v.signatureCrc32c)fail();
        // Caller createC2KmsRequestSigning independently verifies RSA-SHA256
        // with pinned public SPKI SHA256; this port does NOT claim that result.
        return Object.freeze({name:v.name,signature:v.signature,
          signatureCrc32c:v.signatureCrc32c,
          verifiedDigestCrc32c:true});
      }catch{fail();}
    },
  });
}
