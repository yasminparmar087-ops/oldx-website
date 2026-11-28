import {requireFourRoleProtocol} from '../functions/staging-marketplace/four-role/protocol.mjs';
import {requireC2H2LifecycleApprovalVerifier} from './c2-h2-lifecycle-approval.mjs';
import {c2LifecycleBoundary} from './c2-h2-lifecycle-boundary.mjs';
import {createHash} from 'node:crypto';
import {requireC2H2MultiSignLifecyclePolicy} from './c2-h2-lifecycle-signing-status-contract.mjs';
import {requireStagingMarketplaceBinding,STAGING_RATE_COLLECTION} from './staging-marketplace-context.mjs';
import {copyRecord} from './isolated-firestore-context.mjs';
const ledgers=new WeakMap();
export function requireC2H2LifecycleStageLedger(value,policy){
  if(ledgers.get(value)!==policy)throw Error('C2_LIFECYCLE_LEDGER_UNVERIFIED');return value;
}
const hash=x=>createHash('sha256').update(JSON.stringify(x)).digest('hex');
const hex=x=>typeof x==='string'&&/^[a-f0-9]{64}$/.test(x);
const deny=()=>Object.freeze({allowed:false});
const fail=()=>{throw Error('C2_LIFECYCLE_LEDGER_UNAVAILABLE');};
// A separate, permanently retained global record. NO TTL, delete, run-ID reset,
// grant rotation or automatic retry. The legacy ONE-sign record is untouched.
// Requires separately approved multi-sign authority; config hashes are not consent.
export function createC2H2LifecycleStageLedger({enabled=false,binding,policy,
  verifyLifecycleApproval,now=Date.now}={}) {
  if(enabled!==true)return Object.freeze({ready:false,reserve:async()=>deny(),claimSign:async()=>deny(),claimBackend:async()=>deny(),consumeStatusRead:async()=>deny(),finish:async()=>deny()});
  const p=requireC2H2MultiSignLifecyclePolicy(policy),b=requireStagingMarketplaceBinding(binding);
  requireC2H2LifecycleApprovalVerifier(verifyLifecycleApproval,p);
  if(typeof now!=='function')fail();
  const policyDigest=hash(p);
  const id=hash(['oldx.c2.permanent.multisign.lifecycle.v1',p.gatewayUid,p.keyVersion]);
  const ref=b.sdk.doc(b.db,STAGING_RATE_COLLECTION,id);
  const fresh=signal=>{const at=now();if(signal?.aborted||!Number.isSafeInteger(at)||
    at<p.startsAtMs||at>=p.expiresAtMs)fail();return at;};
  // Approval port must verify independent signatures/authority for THIS policy;
  // not a browser boolean, callback-shape check or the old single-sign consent.
  async function approve(signal) {
    fresh(signal);
    const proof=await c2LifecycleBoundary(sig=>verifyLifecycleApproval({policyDigest,policy:p},{signal:sig}),{signal});
    fresh(signal);
    if(proof?.authorized!==true||proof.policyDigest!==policyDigest||
       proof.mode!==p.mode||proof.maxSignAttempts!==6||
       proof.expiresAtMs!==p.expiresAtMs)fail();
  }
  const transaction=(work,signal)=>c2LifecycleBoundary(sig=>b.sdk.runTransaction(b.db,tx=>work(tx,sig),{maxAttempts:3}),{signal});
  const result=Object.freeze({ready:true,policyDigest,recordId:id,
    async reserve(input,{signal}={}) {
      const r=copyRecord(input,['phase','actor','nonceSha256','requestSha256','sessionSha256','authSha256']);
      const index=p.phases.findIndex(s=>s.phase===r?.phase),stage=p.phases[index];
      if(!r||!stage||stage.actor!==r.actor||stage.nonceSha256!==r.nonceSha256||
         !hex(r.requestSha256)||!hex(r.sessionSha256)||!hex(r.authSha256))return deny();
      try {
        await approve(signal);
        return await transaction(async (tx,txSignal)=>{
          const at=fresh(txSignal),snap=await tx.get(ref);fresh(txSignal);
          const old=snap.exists()?snap.data():null;
          if(old&&(old.policyDigest!==policyDigest||old.state!=='READY'||
             old.nextStage!==index||old.signAttempts>=6||old.requests>=20)||
             !old&&index!==0)return deny();
          const reservation=hash([policyDigest,index,r.nonceSha256,r.requestSha256,r.sessionSha256]);
          tx.set(ref,{v:1,policyDigest,keyVersion:p.keyVersion,gatewayUid:p.gatewayUid,
            state:'PENDING',nextStage:index,signAttempts:(old?.signAttempts??0)+1,
            requests:(old?.requests??0)+1,statusReads:old?.statusReads??0,reservation,
            requestSha256:r.requestSha256,sessionSha256:r.sessionSha256,authSha256:r.authSha256,
            consumedAtMs:at,windowEndMs:p.expiresAtMs});
          // Reservation commits BEFORE any signer/network/mutation operation.
          // Conflict retries only re-evaluate this pure transaction.
          return Object.freeze({allowed:true,reservation});
        },signal);
      }catch{fail();} // An ambiguous transaction never licenses dispatch.
    },
    async claimSign(input,{signal}={}) {
      const r=copyRecord(input,['reservation','proofSha256','bodyHash','authHash','path']);
      if(!r||![r.reservation,r.proofSha256,r.bodyHash,r.authHash].every(hex))return deny();
      try {
        await approve(signal);
        return await transaction(async (tx,txSignal)=>{
          fresh(txSignal);const snap=await tx.get(ref);fresh(txSignal);
          if(!snap.exists())return deny();
          const old=snap.data();
          const op=['save','save','list','detail','save','save'][old.nextStage];
          if(old.policyDigest!==policyDigest||old.state!=='PENDING'||old.signingClaimed===true||
             old.reservation!==r.reservation||old.requestSha256!==r.bodyHash||
             old.authSha256!==r.authHash||r.path!=='/api/staging/marketplace/'+op)return deny();
          tx.set(ref,{...old,signingClaimed:true,proofSha256:r.proofSha256});
          return Object.freeze({allowed:true});
        },signal);
      }catch{fail();}
    },
    async claimBackend(input,{signal}={}) {
      const r=copyRecord(input,['proofSha256','bodyHash','authHash','path']);
      if(!r||![r.proofSha256,r.bodyHash,r.authHash].every(hex))return deny();
      try {
        await approve(signal);
        return await transaction(async(tx,txSignal)=>{
          fresh(txSignal);const snap=await tx.get(ref);fresh(txSignal);
          if(!snap.exists())return deny();
          const old=snap.data(),op=['save','save','list','detail','save','save'][old.nextStage];
          if(old.policyDigest!==policyDigest||old.state!=='PENDING'||
             old.signingClaimed!==true||old.backendClaimed===true||
             old.proofSha256!==r.proofSha256||old.requestSha256!==r.bodyHash||
             old.authSha256!==r.authHash||r.path!=='/api/staging/marketplace/'+op)return deny();
          tx.set(ref,{...old,backendClaimed:true});
          return Object.freeze({allowed:true});
        },signal);
      }catch{fail();}
    },
    async consumeStatusRead(input,{signal}={}) {
      const r=copyRecord(input,['reservation','operation']);
      const operations=['sign-version','sign-public','verify-version','verify-public'];
      const slot=operations.indexOf(r?.operation);
      if(!r||!hex(r.reservation)||slot<0)return deny();
      try {
        await approve(signal);
        return await transaction(async(tx,txSignal)=>{
          fresh(txSignal);const snap=await tx.get(ref);fresh(txSignal);
          if(!snap.exists())return deny();
          const old=snap.data(),reads=old.statusOperations??[];
          if(old.policyDigest!==policyDigest||old.state!=='PENDING'||
             old.reservation!==r.reservation||old.signingClaimed!==true||
             reads.includes(r.operation)||slot%2===1&&!reads.includes(operations[slot-1])||
             (old.statusReads??0)>=24)return deny();
          tx.set(ref,{...old,statusReads:(old.statusReads??0)+1,
            statusOperations:[...reads,r.operation]});
          return Object.freeze({allowed:true});
        },signal);
      }catch{fail();}
    },
    async finish(input,{signal}={}) {
      const r=copyRecord(input,['reservation','outcome','responseSha256']);
      if(!r||!hex(r.reservation)||!hex(r.responseSha256)||
         !['CONFIRMED','UNKNOWN'].includes(r.outcome))return deny();
      try {
        fresh(signal);
        return await transaction(async (tx,txSignal)=>{
          fresh(txSignal);const snap=await tx.get(ref);fresh(txSignal);
          if(!snap.exists())return deny();
          const old=snap.data();
          if(old.policyDigest!==policyDigest||old.state!=='PENDING'||
             old.reservation!==r.reservation)return deny();
          const done=r.outcome==='CONFIRMED'&&old.signingClaimed===true&&old.backendClaimed===true,next=old.nextStage+1;
          tx.set(ref,{...old,state:done?(next===6?'COMPLETE':'READY'):'UNKNOWN',
            nextStage:done?next:old.nextStage,responseSha256:r.responseSha256});
          return Object.freeze({allowed:done||r.outcome==='UNKNOWN'});
        },signal);
      }catch{fail();}
    },
  });
  ledgers.set(result,p);return result;
}

// Role-separated remote proxy. Only a branded, independently authorized private
// Google-identity protocol may cross processes. This is NOT an in-memory ledger
// or arbitrary callback facade; all operations commit on Backend's native ledger.
export function createC2H2RemoteLifecycleStageLedger({enabled=false,policy,protocol}={}){
 if(enabled!==true)return null;
 const p=requireC2H2MultiSignLifecyclePolicy(policy),policyDigest=hash(p);
 requireFourRoleProtocol(protocol,{policyDigest});
 const call=operation=>async(input,{signal}={})=>{
 const bytes=Buffer.from(JSON.stringify(input));
 const response=await protocol.send('backend','/internal/ledger',bytes,{operation,
 reservation:input?.reservation??hash(['reserve',policyDigest,input?.phase,input?.requestSha256]),signal});
 if(response.status!==200)fail();
 const result=await response.json();
 if(result?.allowed!==true&&result?.allowed!==false)fail();
 if(result.allowed&&operation==='reserve'&&!hex(result.reservation))fail();
 return Object.freeze({allowed:result.allowed,...result.reservation?{reservation:result.reservation}:{}});
 };
 const result=Object.freeze({ready:true,policyDigest,reserve:call('reserve'),claimSign:call('claimSign'),
 claimBackend:call('claimBackend'),consumeStatusRead:call('consumeStatusRead'),finish:call('finish')});
 ledgers.set(result,p);return result;
}
