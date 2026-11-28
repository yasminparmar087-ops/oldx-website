import test from 'node:test';
import assert from 'node:assert/strict';
import {proposeC2H2DedicatedReaderKeyPolicy as plan,C2_H2_READER_EMAIL as reader,C2_H2_READER_KEY as key} from '../../scripts/c2-h2-kms-reader-key-policy.mjs';
const signer='serviceAccount:oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
const props=()=>({enabled:true,readerUid:'123456789012345678901',readerDisabled:false,
 preimage:{version:1,etag:'BwYAAAABAA==',bindings:[{role:'roles/cloudkms.signer',members:[signer]}]}});
test('NEW reader source defaults OFF and performs no Cloud action',()=>{
 const p=plan();assert.equal(p.reviewReady,false);assert.equal(p.cloudWriteAuthorized,false);
});
test('NEW exactly two read-only key bindings preserve signer without scope drift',()=>{
 const p=plan(props());assert.equal(p.reviewReady,true);assert.equal(p.cloudWriteAuthorized,false);
 assert.equal(p.intent.cryptoKey,key);assert.equal(p.intent.readerEmail,reader);
 assert.deepEqual(p.intent.keyPolicy.bindings.map(x=>x.role),['roles/cloudkms.signer','roles/cloudkms.viewer','roles/cloudkms.publicKeyViewer']);
 assert.deepEqual(p.intent.keyPolicy.bindings.map(x=>x.members),[[signer],['serviceAccount:'+reader],['serviceAccount:'+reader]]);
 assert.equal(Object.isFrozen(p.intent.keyPolicy),true);
});
test('NEW unknown reader UID, disabled identity or changed SA rejected',()=>{
 for(const change of [{readerUid:'UNKNOWN'},{readerDisabled:true},{readerDisabled:undefined},{readerEmail:'oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com'}])
 assert.equal(plan({...props(),...change}).reviewReady,false);
});
test('NEW custom/conditional/owner roles in preimage or stale etag reject without replacing IAM',()=>{
 for(const mutate of [
 p=>p.preimage.bindings.push({role:'roles/owner',members:['user:owner@example.com']}),
 p=>p.preimage.bindings[0].condition={title:'condition',expression:'true'},
 p=>p.preimage.bindings[0].members=['allUsers'],
 p=>p.preimage.etag='',p=>p.preimage.version=3,
 ]){const p=props();mutate(p);assert.equal(plan(p).reviewReady,false);}
});
test('NEW getter-backed policy cannot be accessed during review',()=>{
 let called=0;const p=props();Object.defineProperty(p.preimage,'bindings',{get(){called++;throw Error('unexpected')}});
 assert.equal(plan(p).reviewReady,false);assert.equal(called,0);
});
