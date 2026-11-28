// SOURCE-ONLY review of a possible ONE-KMS-SIGNED, server-held lifecycle grant.
// NOT a signing service, live KMS-status reader, IAM grant, authorization or
// replay ledger. Existing permanent one-sign tombstone MUST NEVER be reset.
// In particular a proposal cannot prove that the one-sign tombstone is unused.
const KEY='projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1';
const SPKI='69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba';
const GATE='oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
const UID='107238619872767759560';
const OPS=Object.freeze([
  'seller-save','seller-publish','buyer-list','buyer-detail','seller-edit','seller-withdraw'
]);
const hex=x=>typeof x==='string'&&/^[a-f0-9]{64}$/.test(x)&&x!=='0'.repeat(64);
const time=x=>Number.isSafeInteger(x)&&x>=0;
const own=(v,keys)=>{
  if(v===null||typeof v!=='object'||Array.isArray(v)||Object.getPrototypeOf(v)!==Object.prototype)return false;
  const all=Reflect.ownKeys(v);
  return all.length===keys.length&&all.every(k=>typeof k==='string'&&keys.includes(k)&&
    Object.hasOwn(Object.getOwnPropertyDescriptor(v,k),'value'));
};
const denied=Object.freeze({reviewReady:false,activationAllowed:false,reason:'LIFECYCLE_CONTRACT_UNAVAILABLE'});
export const C2_H2_LIFECYCLE_REVIEW_SCOPE=Object.freeze({
  purpose:'oldx.c2.synthetic.lifecycle-run-grant.v1',projectId:'oldx-staging',databaseId:'(default)',
  keyVersion:KEY,keyPublicSpkiSha256:SPKI,gatewayEmail:GATE,gatewayUid:UID,
  maxKmsSignAttempts:1,maxRequests:20,maxActors:2,maxProducts:1,maxPhotos:1,
  maxDurationMs:1200000,phaseCount:OPS.length,phases:OPS,
  legacyOneSignTombstoneMustRemain:true,requiresIndependentUnspentTombstoneProof:true,
  requiresIndependentKmsStatusAndPublicKeyReader:true,
  requiresSignedServerOnlyGrantVerification:true,
  requiresPerActionFirebaseAuthAndAtomicReplayLedger:true,
});
const PROPOSAL_KEYS=['v','purpose','projectId','databaseId','runId','gatewayEmail',
  'gatewayUid','keyVersion','keyPublicSpkiSha256','mode','signAttempts',
  'startsAtMs','expiresAtMs','actors','approvalSha256','runNonceSha256',
  'phaseNonceSha256','phases','limits','grantServerOnly',
  'legacyOneSignTombstoneImmutable','durableStageLedgerRequired'];
// This is only a deterministic, side-effect-free source proposal validator.
// reviewReady NEVER means ready to activate or safe to dispatch a request.
export function createC2H2LifecycleSigningStatusContract({enabled=false,proposal}={}){
  if(enabled!==true||!own(proposal,PROPOSAL_KEYS))return denied;
  const p=proposal;
  const names=OPS;
  const actorKeys=['seller','buyer'];
  const limits=['maxRequests','maxActors','maxProducts','maxPhotos'];
  const fixed=C2_H2_LIFECYCLE_REVIEW_SCOPE;
  if(p.v!==1||p.purpose!==fixed.purpose||p.projectId!==fixed.projectId||
     p.databaseId!==fixed.databaseId||p.gatewayEmail!==GATE||p.gatewayUid!==UID||
     p.keyVersion!==KEY||p.keyPublicSpkiSha256!==SPKI||p.mode!=='one-server-held-kms-grant'||
     p.signAttempts!==1||p.grantServerOnly!==true||
     p.legacyOneSignTombstoneImmutable!==true||p.durableStageLedgerRequired!==true||
     typeof p.runId!=='string'||!(/^[A-Za-z0-9_-]{1,30}$/).test(p.runId)||
     !time(p.startsAtMs)||!time(p.expiresAtMs)||
     p.expiresAtMs<=p.startsAtMs||p.expiresAtMs-p.startsAtMs>fixed.maxDurationMs||
     !own(p.actors,actorKeys)||
     p.actors.seller!=='synthetic-c2-'+p.runId+'-seller'||
     p.actors.buyer!=='synthetic-c2-'+p.runId+'-buyer'||
     !hex(p.approvalSha256)||!hex(p.runNonceSha256)||
     p.approvalSha256===p.runNonceSha256||
     !Array.isArray(p.phases)||p.phases.length!==names.length||
     p.phases.some((v,i)=>v!==names[i])||
     !own(p.phaseNonceSha256,names)||!names.every(n=>hex(p.phaseNonceSha256[n]))||
     !own(p.limits,limits)||p.limits.maxRequests!==20||p.limits.maxActors!==2||
     p.limits.maxProducts!==1||p.limits.maxPhotos!==1)return denied;
  const nonces=[p.approvalSha256,p.runNonceSha256,...names.map(n=>p.phaseNonceSha256[n])];
  if(new Set(nonces).size!==nonces.length)return denied;
  const stages=Object.freeze(names.map(n=>Object.freeze({
    phase:n,actor:n.startsWith('buyer-')?p.actors.buyer:p.actors.seller,
    nonceSha256:p.phaseNonceSha256[n],maxSuccessfulCommits:1,
  })));
  const snapshot=Object.freeze({
    runId:p.runId,startsAtMs:p.startsAtMs,expiresAtMs:p.expiresAtMs,
    gatewayEmail:GATE,gatewayUid:UID,keyVersion:KEY,keyPublicSpkiSha256:SPKI,
    approvalSha256:p.approvalSha256,runNonceSha256:p.runNonceSha256,
    phases:stages,limits:Object.freeze({...p.limits}),
  });
  // This stage prefilter ONLY checks declared shape; it is NOT Firebase auth,
  // a cryptographic grant verification, nor Firestore replay consumption.
  const matchesDeclaredStage=candidate=>{
    if(!own(candidate,['runId','phase','actor','nonceSha256','atMs']))return false;
    const {runId,phase,actor,nonceSha256,atMs}=candidate;
    if(runId!==snapshot.runId||!time(atMs)||atMs<snapshot.startsAtMs||
       atMs>=snapshot.expiresAtMs)return false;
    const stage=stages.find(s=>s.phase===phase);
    return !!stage&&stage.actor===actor&&stage.nonceSha256===nonceSha256;
  };
  return Object.freeze({reviewReady:true,activationAllowed:false,
    reason:'SOURCE_REVIEW_ONLY_UNSPENT_TOMBSTONE_AND_HOSTED_GATES_UNVERIFIED',
    scope:snapshot,matchesDeclaredStage,
    mandatoryGates:Object.freeze([
      'INDEPENDENT_APPROVAL_AND_UNSPENT_PERMANENT_TOMBSTONE',
      'TRUSTED_KMS_VERSION_STATE_AND_PUBLIC_SPKI_READER',
      'SERVER_HELD_SIGNED_GRANT_CRYPTOGRAPHIC_VERIFICATION',
      'FIREBASE_ACTOR_FOR_EVERY_PHASE_AND_ATOMIC_STAGE_NONCE_REPLAY_LEDGER',
      'DURABLE_RUN_QUOTA_MEDIA_CLEANUP_AND_VERIFIED_HOSTED_IAM_IMAGE',
    ]),
  });
}
