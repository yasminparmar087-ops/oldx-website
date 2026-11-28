import {requireC2H2LifecycleStageLedger} from './c2-h2-lifecycle-stage-ledger.mjs';
import {requireC2H2MultiSignLifecyclePolicy} from './c2-h2-lifecycle-signing-status-contract.mjs';
import {createC2H2IndependentKmsReaderPorts} from './c2-h2-independent-kms-reader-ports.mjs';
import {H2S_VERSION,H2S_VERSION_URL,H2S_PUBLIC_URL,H2S_ALGORITHM,H2S_SPKI_SHA256,
  c2H2VersionMetadataMatches,c2H2PublicKeyMatches} from './c2-h2-independent-kms-version-status.mjs';
import {c2LifecycleBoundary} from './c2-h2-lifecycle-boundary.mjs';
const fail=()=>{throw Error('C2_LIFECYCLE_STATUS_BLOCKED');};
// DIFFERENT future scope: max FOUR exact GETs per reserved stage (sign/verify
// version+public). Durable global ledger caps total24; not a repeated legacy
// one-shot read, cached ENABLED value, or signer SA metadata permission.
export function createC2H2LifecycleKmsStatus({enabled=false,policy,ledger,
  readerOptions,getStageContext,now=Date.now}={}) {
  const off=Object.freeze({ready:false,getTrustedKeyVersionStatus:async()=>fail()});
  if(enabled!==true)return off;
  let p;try{p=requireC2H2MultiSignLifecyclePolicy(policy);requireC2H2LifecycleStageLedger(ledger,p);}catch{return off;}
  if(ledger?.ready!==true||typeof ledger.consumeStatusRead!=='function'||
     typeof getStageContext!=='function'||typeof now!=='function'||
     !readerOptions||Object.getPrototypeOf(readerOptions)!==Object.prototype||
     !Reflect.ownKeys(readerOptions).every(k=>typeof k==='string'&&
       Object.hasOwn(Object.getOwnPropertyDescriptor(readerOptions,k),'value'))||
     Object.hasOwn(readerOptions,'consumeDurableReadBudget'))return off;
  if(!createC2H2IndependentKmsReaderPorts({...readerOptions,enabled:true,now,
    consumeDurableReadBudget:async()=>({allowed:false})}).ready)return off;
  const fresh=signal=>{const t=now();if(signal.aborted||!Number.isSafeInteger(t)||
    t<p.startsAtMs||t>=p.expiresAtMs)fail();};
  return Object.freeze({ready:true,async getTrustedKeyVersionStatus({name,signal}={}) {
    if(name!==H2S_VERSION)fail();
    return c2LifecycleBoundary(async sig=>{
      fresh(sig);const context=await getStageContext({signal:sig});
      if(!['sign','verify'].includes(context?.usage)||typeof context.reservation!=='string')fail();
      // Snapshot server request context once. No shared mutable per-process slot.
      const {usage,reservation}=context;
      const ports=createC2H2IndependentKmsReaderPorts({...readerOptions,enabled:true,now,
        consumeDurableReadBudget:({url},{signal:readSignal})=>{
          const kind=url===H2S_VERSION_URL?'version':url===H2S_PUBLIC_URL?'public':null;
          if(!kind)fail();return ledger.consumeStatusRead({reservation,
            operation:usage+'-'+kind},{signal:readSignal});
        }});
      if(!ports.ready)fail();
      const version=await ports.readExactVersion({name,url:H2S_VERSION_URL,signal:sig});
      fresh(sig);if(!c2H2VersionMetadataMatches(version))fail();
      const pub=await ports.readExactPublicKey({name,url:H2S_PUBLIC_URL,signal:sig});
      fresh(sig);if(!c2H2PublicKeyMatches(pub))fail();
      return Object.freeze({name,state:'ENABLED',algorithm:H2S_ALGORITHM,publicKeySha256:H2S_SPKI_SHA256});
    },{signal,timeoutMs:600});
  }});
}
