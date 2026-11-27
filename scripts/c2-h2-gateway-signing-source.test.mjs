import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {c2Crc32c} from './c2-kms-request-signing.mjs';
import {createC2H2GatewayKmsSyntheticTransport} from './c2-h2-gateway-kms-synthetic-transport.mjs';
import {createC2H2GatewayHostSource} from '../functions/staging-marketplace/c2-h2-gateway-host-source.mjs';
import {createC2H2PrivateGatewaySigning,C2_H2_GATEWAY_IDENTITY,
  C2_H2_GATEWAY_UID,C2_H2_KMS_KEY_VERSION,C2_H2_KMS_SPKI_SHA256} from
  './c2-h2-private-gateway-signing-composition.mjs';

// New focused source-only H2S cases. All HTTP/credential/ledger providers
// are injected local mocks. No credentials, Google Cloud calls or IAM changes.
const NOW=100_000;
const DIGEST=createHash('sha256').update('OLDX-SYNTHETIC-ONLY').digest();
const SIGNATURE=Buffer.alloc(256,42);
const makePayload=()=>({
  name:C2_H2_KMS_KEY_VERSION,
  digest:{sha256:DIGEST.toString('base64')},
  digestCrc32c:c2Crc32c(DIGEST),
});
function createMock(overrides={}){
  const calls={budget:0,metadata:0,kms:0};
  const options={
    enabled:true,now:()=>NOW,
    consumeDurableSignBudget:async ({projectId,keyVersion,gatewayUid,maxSigns})=>{
      calls.budget++;
      assert.equal(projectId,'oldx-staging');
      assert.equal(keyVersion,C2_H2_KMS_KEY_VERSION);
      assert.equal(gatewayUid,C2_H2_GATEWAY_UID);
      assert.equal(maxSigns,1);
      return {allowed:true};
    },
    getTrustedWorkloadCredential:async ({forPrincipal})=>{
      calls.metadata++;
      assert.equal(forPrincipal,C2_H2_GATEWAY_IDENTITY);
      return {principal:C2_H2_GATEWAY_IDENTITY,uid:C2_H2_GATEWAY_UID,
        source:'cloud-run-metadata',accessToken:'A'.repeat(120),
        expiresAtMs:NOW+60_000};
    },
    fetchKms:async (url,options)=>{
      calls.kms++;
      assert.equal(url,'https://cloudkms.googleapis.com/v1/'+
        C2_H2_KMS_KEY_VERSION+':asymmetricSign');
      assert.equal(options.method,'POST');
      assert.equal(options.redirect,'error');
      assert.equal(options.cache,'no-store');
      assert.equal(options.headers.authorization,'Bearer '+'A'.repeat(120));
      const body=JSON.parse(options.body);
      assert.deepEqual(Object.keys(body).sort(),['digest','digestCrc32c']);
      assert.deepEqual(body.digest,{sha256:DIGEST.toString('base64')});
      return Response.json({
        name:C2_H2_KMS_KEY_VERSION,protectionLevel:'SOFTWARE',
        verifiedDigestCrc32c:true,
        signature:SIGNATURE.toString('base64'),
        signatureCrc32c:c2Crc32c(SIGNATURE),
      });
    },
    ...overrides,
  };
  return {calls,port:createC2H2GatewayKmsSyntheticTransport(options)};
}

test('H2S: default OFF and composition rejects missing real trust providers',async()=>{
  const off=createC2H2GatewayKmsSyntheticTransport();
  assert.equal(off.ready,false);
  await assert.rejects(()=>off.asymmetricSign(makePayload()),/UNAVAILABLE/);
  const noLedger=createC2H2GatewayKmsSyntheticTransport({
    enabled:true,fetchKms:async()=>{throw Error('SHOULD_NOT_RUN');},
    getTrustedWorkloadCredential:async()=>({}),now:()=>NOW,
  });
  assert.equal(noLedger.ready,false);
  const composed=createC2H2PrivateGatewaySigning({
    enabled:true,runtimeServiceAccount:C2_H2_GATEWAY_IDENTITY,
    runtimeServiceAccountUid:C2_H2_GATEWAY_UID,
    publicKeyPem:'-----BEGIN PUBLIC KEY-----\ninvalid\n-----END PUBLIC KEY-----',
    validFromMs:NOW,validUntilMs:NOW+30_000,
    now:()=>NOW,
    getTrustedWorkloadCredential:async()=>({}),
    fetchKms:async()=>{throw Error('SHOULD_NOT_RUN');},
    consumeDurableSignBudget:async()=>({allowed:true}),
    getTrustedKeyVersionStatus:async()=>({
      name:C2_H2_KMS_KEY_VERSION,state:'ENABLED',
      algorithm:'RSA_SIGN_PKCS1_2048_SHA256',
      publicKeySha256:C2_H2_KMS_SPKI_SHA256,
    }),
  });
  assert.equal(composed.ready,false);
  assert.deepEqual(composed.requestSigning,{});
  assert.equal(composed.runtimeServiceAccount,null);
  const host=createC2H2GatewayHostSource({enabled:true,
    runtimeServiceAccount:C2_H2_GATEWAY_IDENTITY,
    runtimeServiceAccountUid:C2_H2_GATEWAY_UID,
    runtimeImage:'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/c2-h2-gateway@sha256:'+'a'.repeat(64),
    mediatorPrincipal:'oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com',
    privateGatewayOrigin:'https://gateway.example.test',
    gatewayOptions:{gatewayServiceAccount:C2_H2_GATEWAY_IDENTITY},
  });
  assert.equal(host.ready,false);
  const response=await host.fetch(new Request('https://gateway.example.test/api/staging/marketplace/list',{method:'POST'}));
  assert.equal(response.status,503);
  const nullOptions=createC2H2GatewayHostSource({
    enabled:true,runtimeServiceAccount:C2_H2_GATEWAY_IDENTITY,
    runtimeServiceAccountUid:C2_H2_GATEWAY_UID,
    gatewayOptions:null,
  });
  assert.equal(nullOptions.ready,false);
});

test('H2S: valid synthetic digest and CRC reaches one mocked KMS transport only',async()=>{
  const {port,calls}=createMock();
  assert.equal(port.ready,true);
  const result=await port.asymmetricSign(makePayload());
  assert.equal(result.name,C2_H2_KMS_KEY_VERSION);
  assert.equal(result.verifiedDigestCrc32c,true);
  assert.equal(result.signatureCrc32c,c2Crc32c(SIGNATURE));
  assert.deepEqual(calls,{budget:1,metadata:1,kms:1});
  await assert.rejects(()=>port.asymmetricSign(makePayload()),/UNAVAILABLE/);
  assert.deepEqual(calls,{budget:1,metadata:1,kms:1});
});

test('H2S: reject bad checksum, denied durable budget and mutated KMS signature',async()=>{
  const bad=createMock();
  await assert.rejects(()=>bad.port.asymmetricSign({
    ...makePayload(),digestCrc32c:'0',
  }),/UNAVAILABLE/);
  assert.deepEqual(bad.calls,{budget:0,metadata:0,kms:0});
  const denied=createMock({
    consumeDurableSignBudget:async()=>({allowed:false}),
  });
  await assert.rejects(()=>denied.port.asymmetricSign(makePayload()),/UNAVAILABLE/);
  assert.equal(denied.calls.metadata,0);
  assert.equal(denied.calls.kms,0);
  const tampered=createMock({
    fetchKms:async()=>Response.json({
      name:C2_H2_KMS_KEY_VERSION,protectionLevel:'SOFTWARE',
      verifiedDigestCrc32c:true,signature:SIGNATURE.toString('base64'),
      signatureCrc32c:'0',
    }),
  });
  await assert.rejects(()=>tampered.port.asymmetricSign(makePayload()),/UNAVAILABLE/);
});
