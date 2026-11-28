import test from 'node:test';
import assert from 'node:assert/strict';
import {C2_H2_LIFECYCLE_REVIEW_SCOPE as scope,
  createC2H2LifecycleSigningStatusContract as build} from '../../scripts/c2-h2-lifecycle-signing-status-contract.mjs';
const ops=scope.phases;
const dig=(s)=>s.repeat(64);
const base=()=>({v:1,purpose:scope.purpose,projectId:scope.projectId,
  databaseId:scope.databaseId,runId:'test1',gatewayEmail:scope.gatewayEmail,
  gatewayUid:scope.gatewayUid,keyVersion:scope.keyVersion,
  keyPublicSpkiSha256:scope.keyPublicSpkiSha256,
  mode:'one-server-held-kms-grant',signAttempts:1,startsAtMs:1800000000000,
  expiresAtMs:1800000600000,
  actors:{seller:'synthetic-c2-test1-seller',buyer:'synthetic-c2-test1-buyer'},
  approvalSha256:dig('a'),runNonceSha256:dig('b'),
  phaseNonceSha256:Object.fromEntries(ops.map((x,i)=>[x,dig(String(i+1))])),
  phases:[...ops],limits:{maxRequests:20,maxActors:2,maxProducts:1,maxPhotos:1},
  grantServerOnly:true,legacyOneSignTombstoneImmutable:true,durableStageLedgerRequired:true});
test('NEW lifecycle review OFF by default and cannot sign, query KMS or approve Cloud',()=>{
  const r=build({proposal:base()});assert.equal(r.reviewReady,false);
  assert.equal(r.activationAllowed,false);
  assert.equal('signMessage' in r,false);
  assert.equal('fetchKms' in r,false);
});
test('NEW review permits scoped proposal but NEVER activates signed lifecycle',()=>{
  const p=base(),r=build({enabled:true,proposal:p});
  assert.equal(r.reviewReady,true);assert.equal(r.activationAllowed,false);
  assert.equal(r.scope.phases.length,6);
  assert.equal(r.scope.phases.filter(x=>x.actor===p.actors.buyer).length,2);
  assert.equal(r.scope.phases.every(x=>x.maxSuccessfulCommits===1),true);
  assert.ok(r.mandatoryGates.includes('INDEPENDENT_APPROVAL_AND_UNSPENT_PERMANENT_TOMBSTONE'));
});
test('NEW actor, stage nonce, ordering, time window, run id fail closed',()=>{
  const p=base(),r=build({enabled:true,proposal:p});const phase='buyer-detail';
  const req={runId:p.runId,phase,actor:p.actors.buyer,
    nonceSha256:p.phaseNonceSha256[phase],atMs:p.startsAtMs+1};
  assert.equal(r.matchesDeclaredStage(req),true);
  for(const changed of [
    {runId:'else'},{phase:'seller-delete'},{actor:p.actors.seller},
    {nonceSha256:p.phaseNonceSha256['buyer-list']},
    {atMs:p.expiresAtMs},{atMs:p.startsAtMs-1},
  ])assert.equal(r.matchesDeclaredStage({...req,...changed}),false);
  assert.equal(r.activationAllowed,false);
});
test('NEW tampered one-sign budget, ledger or timeout invalidates proposal',()=>{
  for(const patch of [
    {signAttempts:2},{mode:'unlimited-signing'},{legacyOneSignTombstoneImmutable:false},
    {grantServerOnly:false},{durableStageLedgerRequired:false},
    {expiresAtMs:1800000000000+1200001},{keyVersion:scope.keyVersion.replace('/1','/2')},
    {gatewayUid:'bad'},
  ])assert.equal(build({enabled:true,proposal:{...base(),...patch}}).reviewReady,false);
});
test('NEW unique immutable stages and signed digests required',()=>{
  let p=base();p.phaseNonceSha256['seller-edit']=p.phaseNonceSha256['seller-save'];
  assert.equal(build({enabled:true,proposal:p}).reviewReady,false);
  p=base();p.phases.reverse();
  assert.equal(build({enabled:true,proposal:p}).reviewReady,false);
  p=base();p.actors.buyer=p.actors.seller;
  assert.equal(build({enabled:true,proposal:p}).reviewReady,false);
});
test('NEW accessors rejected without invoking getters or host callbacks',()=>{
  let invoked=0;const p=base();Object.defineProperty(p,'actors',{get(){invoked++;throw Error('no');}});
  assert.equal(build({enabled:true,proposal:p}).reviewReady,false);
  assert.equal(invoked,0);
  const p2=base();Object.defineProperty(p2.phaseNonceSha256,'seller-save',{
    get(){invoked++;throw Error('no');}});
  assert.equal(build({enabled:true,proposal:p2}).reviewReady,false);
  assert.equal(invoked,0);
});

test('NEW candidate accessors do not execute and do not authorize a phase',()=>{
  let invoked=0;const p=base(),r=build({enabled:true,proposal:p});
  const cand={runId:p.runId,phase:'seller-save',actor:p.actors.seller,
    nonceSha256:p.phaseNonceSha256['seller-save'],atMs:p.startsAtMs+1};
  Object.defineProperty(cand,'actor',{get(){invoked++;throw Error('untrusted');}});
  assert.equal(r.matchesDeclaredStage(cand),false);assert.equal(invoked,0);
});
