import test from 'node:test';
import assert from 'node:assert/strict';
import {createC2H2GatewayMetadataAccessToken} from './c2-h2-cloud-run-gateway-access-token.mjs';
import {createC2H2MetadataBoundPrivateGatewayHostSource} from '../functions/staging-marketplace/c2-h2-gateway-runtime-credential-source.mjs';

// NEW H2S credential-port tests only. Synthetic metadata Responses; no Google
// metadata server, network, IAM, SA JSON keys or previous tests invoked.
const EMAIL='oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com';
const UID='107238619872767759560';
const NOW=1795800000000;
const BASE='http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/';
const token='ya29.'+'A'.repeat(110);
function response(body,{status=200,metadataFlavor='Google'}={}){
  return new Response(body,{status,headers:
    metadataFlavor?{'Metadata-Flavor':metadataFlavor}:{}});
}
function fixture(overrides={}){
  const seen=[];
  const fetchMetadata=async(url,opt)=>{
    seen.push({url,opt});
    assert.equal(opt.method,'GET');
    assert.equal(opt.redirect,'error');
    assert.equal(opt.cache,'no-store');
    assert.equal(opt.credentials,'omit');
    assert.equal(opt.headers['Metadata-Flavor'],'Google');
    if(url===BASE+'email')return response(EMAIL+'\n');
    if(url===BASE+'token')return response(JSON.stringify({
      access_token:token,expires_in:120,token_type:'Bearer',
    }));
    throw Error('UNEXPECTED_URL');
  };
  const adapter=createC2H2GatewayMetadataAccessToken({
    enabled:true,serviceAccount:EMAIL,serviceAccountUid:UID,
    now:()=>NOW,fetchMetadata,...overrides,
  });
  return {adapter,seen};
}

test('NEW H2S credential port default OFF never fetches metadata',async()=>{
  let calls=0;
  const api=createC2H2GatewayMetadataAccessToken({
    serviceAccount:EMAIL,serviceAccountUid:UID,
    fetchMetadata:async()=>{calls++;throw Error('NETWORK_CALLED');},
  });
  assert.equal(api.ready,false);
  await assert.rejects(()=>api.getTrustedWorkloadCredential({forPrincipal:EMAIL}),
    /C2_H2_WORKLOAD_CREDENTIAL_UNAVAILABLE/);
  assert.equal(calls,0);
  const wrongUID=createC2H2GatewayMetadataAccessToken({
    enabled:true,serviceAccount:EMAIL,serviceAccountUid:'unverified',
    fetchMetadata:async()=>{calls++;throw Error('NETWORK_CALLED');},
  });
  assert.equal(wrongUID.ready,false);
  assert.equal(calls,0);
  const host=createC2H2MetadataBoundPrivateGatewayHostSource({
    enabled:true,fetchMetadata:async()=>{calls++;throw Error('NETWORK_CALLED');},
    hostOptions:{
      runtimeServiceAccount:EMAIL,runtimeServiceAccountUid:UID,
    },
  });
  assert.equal(host.ready,false);
  assert.equal((await host.fetch(new Request('https://gateway.example.test/'))).status,503);
  assert.equal(calls,0);
  // Caller cannot smuggle an alternate credential source or getters into host.
  const overridden=createC2H2MetadataBoundPrivateGatewayHostSource({
    enabled:true,fetchMetadata:async()=>{calls++;throw Error('NETWORK_CALLED');},
    hostOptions:{
      runtimeServiceAccount:EMAIL,runtimeServiceAccountUid:UID,
      getTrustedWorkloadCredential:async()=>({accessToken:'FAKE'}),
    },
  });
  assert.equal(overridden.ready,false);
  assert.equal(calls,0);
  const accessors=Object.defineProperty({runtimeServiceAccount:EMAIL,
    runtimeServiceAccountUid:UID},'runtimeImage',{
      enumerable:true,get(){throw Error('GETTER_CALLED');},
    });
  assert.equal(createC2H2MetadataBoundPrivateGatewayHostSource({
    enabled:true,hostOptions:accessors,fetchMetadata:async()=>{},
  }).ready,false);
});

test('NEW H2S credential port exact email and OAuth token, single fetch pair',async()=>{
  const {adapter,seen}=fixture();
  assert.equal(adapter.ready,true);
  const result=await adapter.getTrustedWorkloadCredential({forPrincipal:EMAIL});
  assert.equal(result.principal,EMAIL);
  assert.equal(result.uid,UID);
  assert.equal(result.source,'cloud-run-metadata');
  assert.equal(result.accessToken,token);
  assert.equal(result.expiresAtMs,NOW+120000);
  assert.equal(seen.length,2);
  assert.equal(seen[0].url,BASE+'email');
  assert.equal(seen[1].url,BASE+'token');
  assert.ok(Object.isFrozen(result));
  await assert.rejects(()=>adapter.getTrustedWorkloadCredential({forPrincipal:EMAIL}),
    /C2_H2_WORKLOAD_CREDENTIAL_UNAVAILABLE/);
  assert.equal(seen.length,2);
});

test('NEW H2S credential port rejects wrong identity before OAuth, malformed token and invalid metadata',async()=>{
  let tokenCalls=0;
  const noEmail=fixture({fetchMetadata:async url=>{
    if(url===BASE+'email')return response('other@oldx-staging.iam.gserviceaccount.com');
    tokenCalls++;return response('{}');
  }});
  await assert.rejects(()=>noEmail.adapter.getTrustedWorkloadCredential({forPrincipal:EMAIL}),
    /C2_H2_WORKLOAD_CREDENTIAL_UNAVAILABLE/);
  assert.equal(tokenCalls,0);

  const cases=[
    ()=>response(JSON.stringify({access_token:token,expires_in:120,token_type:'ID'})),
    ()=>response(JSON.stringify({access_token:'short',expires_in:120,token_type:'Bearer'})),
    ()=>response(JSON.stringify({access_token:token,expires_in:1,token_type:'Bearer'})),
    ()=>response(JSON.stringify({access_token:token,expires_in:120,token_type:'Bearer',principal:EMAIL})),
    ()=>response(JSON.stringify({access_token:token,expires_in:120,token_type:'Bearer'}),{metadataFlavor:null}),
    ()=>response('BAD_REQUEST',{status:403}),
  ];
  for(const bad of cases){
    const {adapter}=fixture({fetchMetadata:async(url)=>{
      if(url===BASE+'email')return response(EMAIL);
      return bad();
    }});
    await assert.rejects(()=>adapter.getTrustedWorkloadCredential({forPrincipal:EMAIL}),
      /C2_H2_WORKLOAD_CREDENTIAL_UNAVAILABLE/);
  }
  const preAborted=fixture();
  await assert.rejects(()=>preAborted.adapter.getTrustedWorkloadCredential({
    forPrincipal:EMAIL,signal:AbortSignal.abort(),
  }),/C2_H2_WORKLOAD_CREDENTIAL_UNAVAILABLE/);
  assert.equal(preAborted.seen.length,0);
  const wrongPrincipal=fixture();
  await assert.rejects(()=>wrongPrincipal.adapter.getTrustedWorkloadCredential({
    forPrincipal:'owner@invalid.example',
  }),/C2_H2_WORKLOAD_CREDENTIAL_UNAVAILABLE/);
  assert.equal(wrongPrincipal.seen.length,0);
});
