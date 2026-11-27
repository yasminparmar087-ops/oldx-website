import test from 'node:test';
import assert from 'node:assert/strict';
import {
  createC2H2IndependentKmsVersionStatus,c2H2VersionMetadataMatches,
  H2S_VERSION,H2S_ALGORITHM,H2S_VERSION_URL,H2S_PUBLIC_URL,
} from './c2-h2-independent-kms-version-status.mjs';

// NEW H2S KeyVersion status tests. No real Cloud KMS or access tokens.
// H2N pinned real public PEM is private WSL evidence and is NOT fabricated:
// successful full metadata+SPKI approval cannot be claimed by these mocks.
const AT=1800000000000;
const metadata=()=>({
  name:H2S_VERSION,state:'ENABLED',algorithm:H2S_ALGORITHM,
  protectionLevel:'SOFTWARE',
});
function build(overrides={}){
  const calls={v:0,p:0};
  const obj=createC2H2IndependentKmsVersionStatus({
    enabled:true,validFromMs:AT-1000,validUntilMs:AT+30000,now:()=>AT,
    readExactVersion:async ({name,url})=>{
      calls.v++;assert.equal(name,H2S_VERSION);assert.equal(url,H2S_VERSION_URL);
      return metadata();
    },
    readExactPublicKey:async ({name,url})=>{
      calls.p++;assert.equal(name,H2S_VERSION);assert.equal(url,H2S_PUBLIC_URL);
      return {algorithm:H2S_ALGORITHM,pem:'INVALID',pemCrc32c:'0'};
    },
    ...overrides,
  });
  return {calls,obj};
}
test('NEW H2S status: default OFF, invalid time and name never read',async()=>{
  let reads=0;
  const off=createC2H2IndependentKmsVersionStatus({
    readExactVersion:async()=>{reads++;return metadata();},
    readExactPublicKey:async()=>{reads++;return {};},
  });
  assert.equal(off.ready,false);
  await assert.rejects(()=>off.getTrustedKeyVersionStatus({name:H2S_VERSION}),/UNVERIFIED/);
  assert.equal(reads,0);
  const wrong=build();
  await assert.rejects(()=>wrong.obj.getTrustedKeyVersionStatus({
    name:'projects/other',
  }),/UNVERIFIED/);
  assert.deepEqual(wrong.calls,{v:0,p:0});
  const expired=createC2H2IndependentKmsVersionStatus({
    enabled:true,validFromMs:AT-1000,validUntilMs:AT,
    now:()=>AT,readExactVersion:async()=>{reads++;return metadata();},
    readExactPublicKey:async()=>{reads++;return {};},
  });
  assert.equal(expired.ready,true);
  await assert.rejects(()=>expired.getTrustedKeyVersionStatus({
    name:H2S_VERSION,
  }),/UNVERIFIED/);
  assert.equal(reads,0);
});
test('NEW H2S status: exact version metadata accepts pinned policy, rejects drift',async()=>{
  assert.equal(c2H2VersionMetadataMatches(metadata()),true);
  for(const patch of [
    {state:'DISABLED'},
    {algorithm:'RSA_SIGN_PSS_2048_SHA256'},
    {protectionLevel:'HSM'},
    {name:'projects/oldx-staging/other'},
  ]){
    assert.equal(c2H2VersionMetadataMatches({...metadata(),...patch}),false);
    const f=build({readExactVersion:async()=>({...metadata(),...patch})});
    await assert.rejects(()=>f.obj.getTrustedKeyVersionStatus({
      name:H2S_VERSION,
    }),/UNVERIFIED/);
    assert.equal(f.calls.p,0);
  }
});
test('NEW H2S status: wrong public PEM/CRC fails closed; no caching or repeat',async()=>{
  const f=build();
  assert.equal(f.obj.ready,true);
  await assert.rejects(()=>f.obj.getTrustedKeyVersionStatus({
    name:H2S_VERSION,
  }),/UNVERIFIED/);
  assert.deepEqual(f.calls,{v:1,p:1});
  await assert.rejects(()=>f.obj.getTrustedKeyVersionStatus({
    name:H2S_VERSION,
  }),/UNVERIFIED/);
  assert.deepEqual(f.calls,{v:1,p:1});
  const badChecksum=build({readExactPublicKey:async()=>({
    algorithm:H2S_ALGORITHM,
    pem:'-----BEGIN PUBLIC KEY-----\nINVALID\n-----END PUBLIC KEY-----\n',
    pemCrc32c:'4294967296',
  })});
  await assert.rejects(()=>badChecksum.obj.getTrustedKeyVersionStatus({
    name:H2S_VERSION,
  }),/UNVERIFIED/);
  const aborted=build();
  await assert.rejects(()=>aborted.obj.getTrustedKeyVersionStatus({
    name:H2S_VERSION,signal:AbortSignal.abort(),
  }),/UNVERIFIED/);
  assert.deepEqual(aborted.calls,{v:0,p:0});
});
