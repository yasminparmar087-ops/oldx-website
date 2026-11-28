import test from 'node:test';
import assert from 'node:assert/strict';
import {createC2EnabledReleaseControl} from '../../scripts/c2-enabled-release-control.mjs';
import {createC2G2G6EnabledHostSourceAssembly} from
  '../../functions/staging-marketplace/c2-g2g6-enabled-host-source-assembly.mjs';

const img=(name,digit)=>'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/'+
  name+'@sha256:'+digit.repeat(64);
const MED='oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com';
const GATE='oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
const BACK='oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com';
const time=1800000000000;
const facts=()=>({
  mediator:{principal:MED,uid:'100779414920484819274',image:img('mediator', '3')},
  gateway:{principal:GATE,uid:'107238619872767759560',image:img('gateway','4')},
  backend:{principal:BACK,uid:'106984791114720194680',image:img('backend','5')},
});
const contract=()=>({
  v:1,purpose:'oldx.c2.enabled-product.synthetic.v1',runId:'host',
  projectId:'oldx-staging',databaseId:'(default)',
  startsAtMs:time-100,expiresAtMs:time+300000,
  principals:{mediator:MED,gateway:GATE,backend:BACK},
  images:{mediator:img('mediator','3'),gateway:img('gateway','4'),backend:img('backend','5')},
  evidence:Object.fromEntries(['identity','iam','media','cleanup','security','rollback']
    .map(n=>[n,'a'.repeat(64)])),
  limits:{maxRequests:20,maxActors:2,maxProducts:1,maxPhotos:1},
  actors:{seller:'synthetic-c2-host-seller',buyer:'synthetic-c2-host-buyer'},
  managedPhotoId:'synthetic_photo_1234567890',
});
function args(patch={}){
  return {
    enabled:true,hostFacts:facts(),now:()=>time,
    websiteOptions:{websiteOrigin:'https://seller.example',
      mediatorPrincipal:MED,privateGatewayOrigin:'https://gateway.example',
      allowedOrigins:['https://seller.example'],
      mediationAudience:'urn:oldx:website'},
    gatewayHostOptions:{runtimeServiceAccount:GATE,
      runtimeServiceAccountUid:'107238619872767759560',
      runtimeImage:img('gateway','4'),
      mediatorPrincipal:MED,privateGatewayOrigin:'https://gateway.example',
      allowedOrigins:['https://seller.example'],
      gatewayOptions:{gatewayServiceAccount:GATE,
        attestationAudience:'urn:oldx:gateway'}},
    backendOptions:{runtimeOptions:{createMediaBindings:()=>({})}},
    fetchGatewayMetadata:()=>{throw Error('MUST_NOT_FETCH_METADATA_DURING_CONSTRUCTION');},
    ...patch,
  };
}

test('NEW G2-G6 source host defaults OFF with no product, IAM or network work',async()=>{
  const host=createC2G2G6EnabledHostSourceAssembly();
  assert.equal(host.sourceComposed,false);
  assert.equal(host.reason,'MISSING_TRUSTED_HOST_OR_RELEASE_BOUNDARY');
  const req=new Request('https://gateway.example/api/staging/marketplace/save',{
    method:'POST',body:'{}'});
  for(const h of [host.gateway,host.backend]){
    const res=await h.fetch(req);
    assert.equal(res.status,503);
    assert.equal(res.headers.get('cache-control'),'private, no-store');
    assert.equal((await res.json()).error.code,'C2_G2_G6_NOT_AUTHORIZED');
  }
});
test('NEW G2-G6 cannot substitute a forged release control for the WeakSet authority',()=>{
  const result=createC2G2G6EnabledHostSourceAssembly(
    args({releaseControl:{ready:true,runtimePrincipal:BACK,
      runtimeImage:img('backend','5')}}));
  assert.equal(result.sourceComposed,false);
});
test('NEW G2-G6 release control alone cannot authorize missing key status/KMS/host ports',()=>{
  let approvals=0,budgets=0;
  const release=createC2EnabledReleaseControl({
    enabled:true,contract:contract(),now:()=>time,
    verifyApproval:async()=>{approvals++;return {authorized:true};},
    consumeRunBudget:async()=>{budgets++;return {allowed:true};},
  });
  assert.equal(release.ready,true);
  const result=createC2G2G6EnabledHostSourceAssembly(
    args({releaseControl:release}));
  assert.equal(result.sourceComposed,false); // independent PEM, trusted KMS and host identity absent
  assert.equal(approvals,0);
  assert.equal(budgets,0);
});
test('NEW G2-G6 rejects original OFF digest and principal UID drift without side effects',()=>{
  const override=facts();
  override.gateway.image='asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/'+
    'oldx-c2-h2-gateway-off@sha256:'+
    '4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2';
  assert.equal(createC2G2G6EnabledHostSourceAssembly(
    args({hostFacts:override})).sourceComposed,false);
  const mutated=facts();mutated.backend.uid='000';
  assert.equal(createC2G2G6EnabledHostSourceAssembly(
    args({hostFacts:mutated})).sourceComposed,false);
});

test('NEW G2-G6 fully shaped host ports still fail closed without pinned KMS public key; no source providers fire',()=>{
  let calls=0;
  const forbidden=()=>{calls++;throw Error('NO_LIVE_HOST_CALL_IN_SOURCE_TEST');};
  const release=createC2EnabledReleaseControl({
    enabled:true,contract:contract(),now:()=>time,
    verifyApproval:forbidden,consumeRunBudget:forbidden,
  });
  assert.equal(release.ready,true);
  const a=args({releaseControl:release,fetchGatewayMetadata:forbidden});
  a.websiteOptions={
    ...a.websiteOptions,
    getGatewayInvokerCredential:forbidden,
    getWebsiteAttestation:forbidden,
    consumeGuestAdmission:forbidden,fetchPrivateGateway:forbidden,
  };
  a.gatewayHostOptions={
    ...a.gatewayHostOptions,
    websiteIdentity:{identityType:'google-service-account',
      issuer:'https://accounts.google.com',
      expectedSubject:'100779414920484819274',
      attestationAudience:'urn:oldx:website',
      fetchRequest:forbidden},
    gatewayOptions:{...a.gatewayHostOptions.gatewayOptions,
      backendOrigin:'https://backend.example',
      getInvokerCredential:forbidden,
      getGatewayAttestation:forbidden,fetchBackend:forbidden},
    fetchKms:forbidden,consumeDurableSignBudget:forbidden,
    getTrustedKeyVersionStatus:forbidden,
  };
  a.backendOptions={
    ...a.backendOptions,audience:'https://backend.example',
    gatewayServiceAccount:GATE,
    googleIdentity:{issuer:'https://accounts.google.com',
      fetchRequest:forbidden},
    requestVerification:{resolvePublicKey:forbidden},
    runtimeOptions:{...a.backendOptions.runtimeOptions,
      projectId:'oldx-staging',
      adminAuth:{app:{options:{projectId:'oldx-staging'}},
        verifyIdToken:forbidden},
      adminFirestore:{runTransaction:forbidden}},
  };
  const result=createC2G2G6EnabledHostSourceAssembly(a);
  assert.equal(result.sourceComposed,false);
  assert.equal(calls,0);
});

test('NEW G2-G6 host rejects mismatched backend/Gateway identities and HTTP origin before any provider invocation',()=>{
  let called=0;
  const forbidden=()=>{called++;throw Error('MUST_NOT_CALL_PROVIDER');};
  const a=args();
  a.gatewayHostOptions.gatewayOptions={
    ...a.gatewayHostOptions.gatewayOptions,backendOrigin:'https://backend.one'};
  a.backendOptions={
    ...a.backendOptions,
    audience:'https://backend.two',
    gatewayServiceAccount:GATE,
  };
  const result=createC2G2G6EnabledHostSourceAssembly({
    ...a,fetchGatewayMetadata:forbidden,
  });
  assert.equal(result.sourceComposed,false);
  assert.equal(called,0);
});
