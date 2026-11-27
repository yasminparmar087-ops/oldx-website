import test from 'node:test';
import assert from 'node:assert/strict';
import {createStagingMarketplaceBinding} from './staging-marketplace-context.mjs';
import {createC2H2OneSignFirestoreBudget,C2_H2_SIGN_BUDGET_SCOPE as S} from './c2-h2-firestore-one-sign-budget.mjs';
import {fakeFirestoreSdk} from '../tests/integration/fake-firestore-sdk.mjs';

// NEW H2S budget-only tests; fake native Firestore SDK, no Firebase/Google,
// network, Cloud Run, KMS sign, IAM or previously completed tests.
const NOW=1800000000000;
const options={approvedPlanSha256:'a'.repeat(64),
  syntheticNonceSha256:'b'.repeat(64),
  validFromMs:NOW-2000,validUntilMs:NOW+30000,
  now:()=>NOW,
};
const input=()=>({purpose:S.purpose,projectId:S.projectId,
  gatewayUid:S.gatewayUid,keyVersion:S.keyVersion,maxSigns:1});
function nativeFixture(){
  const f=fakeFirestoreSdk();
  const db={
    projectId:'oldx-staging',databaseId:'(default)',
    collection:name=>({doc:id=>f.sdk.doc(f.db,name,id)}),
    runTransaction:(work,settings)=>f.sdk.runTransaction(f.db,async tx=>{
      return work(Object.freeze({
        get:async ref=>{const snap=await tx.get(ref);return {
          exists:snap.exists(),data:()=>snap.data(),
        };},
        set:(...args)=>tx.set(...args),
        delete:(...args)=>tx.delete(...args),
      }));
    },settings),
  };
  const binding=createStagingMarketplaceBinding({
    adminFirestore:db,FieldValue:{serverTimestamp:f.sdk.serverTimestamp},
    projectId:'oldx-staging',deploymentEnvironment:'preview',
  });
  return {f,binding};
}

test('NEW H2S one-sign budget default OFF, invalid approval and input never write',async()=>{
  const off=createC2H2OneSignFirestoreBudget();
  assert.deepEqual(await off(input()),{allowed:false});
  const {f,binding}=nativeFixture();
  assert.throws(()=>createC2H2OneSignFirestoreBudget({
    enabled:true,binding,...options,approvedPlanSha256:'wrong',
  }),/UNAVAILABLE/);
  const budget=createC2H2OneSignFirestoreBudget({enabled:true,binding,...options});
  assert.deepEqual(await budget({...input(),maxSigns:2}),{allowed:false});
  assert.deepEqual(await budget({...input(),projectId:'other'}),{allowed:false});
  assert.deepEqual(await budget(input(),{signal:AbortSignal.abort()}),{allowed:false});
  assert.equal(f.calls,0);
  assert.equal(f.commits,0);
});

test('NEW H2S one-sign Firestore transaction allows one across independent instances',async()=>{
  const {f,binding}=nativeFixture();
  const a=createC2H2OneSignFirestoreBudget({enabled:true,binding,...options});
  const b=createC2H2OneSignFirestoreBudget({
    enabled:true,binding,...options,
    // A different nonce/approval CANNOT reset the global tombstone.
    approvedPlanSha256:'c'.repeat(64),syntheticNonceSha256:'d'.repeat(64),
  });
  const results=await Promise.all([a(input()),b(input()),a(input())]);
  assert.equal(results.filter(x=>x.allowed===true).length,1);
  assert.equal(results.filter(x=>x.allowed===false).length,2);
  assert.equal(f.commits,1);
  const record=f.get(S.collection,S.globalRecordId);
  assert.equal(record.consumed,true);
  assert.equal(record.gatewayUid,S.gatewayUid);
  assert.equal(record.keyVersion,S.keyVersion);
  assert.equal(record.maxSigns,undefined);
  assert.ok(!Object.hasOwn(record,'expiresAtMs'));
  assert.equal(Object.values(f.snapshot()).length,1);
});

test('NEW H2S one-sign budget fails closed on transaction failure, window and expired tombstone',async()=>{
  const {f,binding}=nativeFixture();
  const budget=createC2H2OneSignFirestoreBudget({enabled:true,binding,...options});
  f.failCommit=true;
  await assert.rejects(()=>budget(input()),/UNAVAILABLE/);
  assert.equal(f.commits,0);
  f.failCommit=false;
  assert.deepEqual(await budget(input()),{allowed:true});
  assert.deepEqual(await budget(input()),{allowed:false});
  assert.equal(f.commits,1);

  // Once consumed, no new grants/nonce or artificial later window can reset.
  const later=createC2H2OneSignFirestoreBudget({
    enabled:true,binding,approvedPlanSha256:'e'.repeat(64),
    syntheticNonceSha256:'f'.repeat(64),
    validFromMs:NOW+100000,validUntilMs:NOW+120000,
    now:()=>NOW+101000,
  });
  assert.deepEqual(await later(input()),{allowed:false});
  assert.equal(f.commits,1);
  const expired=createC2H2OneSignFirestoreBudget({
    enabled:true,binding,...options,now:()=>NOW+50000,
  });
  await assert.rejects(()=>expired(input()),/UNAVAILABLE/);
  assert.equal(f.commits,1);
});
