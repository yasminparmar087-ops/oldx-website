import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {
  parseC2H2UCloudRunPort,
  createC2H2UPrivateOffRequestHandler,
  createC2H2UPrivateOffHttpServer,
} from '../functions/staging-marketplace/c2-h2u-private-off-http.mjs';

// NEW H2U-only tests. No listener, Docker, network, Cloud, KMS, Firestore,
// old H2S tests or credentials are used.
const handle=createC2H2UPrivateOffRequestHandler();
const simulate=(method,url,headers={})=>{
  let code,values,body;
  const request={method,url,headers};
  const response={
    writeHead(status,h){code=status;values=h;},
    end(chunk){body=JSON.parse(chunk);},
  };
  handle(request,response);
  return {code,values,body};
};

test('NEW H2U OFF-only health and known Product paths have safe exact responses',()=>{
  const health=simulate('GET','/healthz');
  assert.equal(health.code,200);
  assert.deepEqual(health.body,{
    ok:true,service:'oldx-c2-private-gateway',mode:'OFF',
  });
  assert.equal(health.values['cache-control'],'private, no-store');
  assert.equal(health.values['connection'],'close');
  for(const op of ['save','owner','archive','list','detail']){
    for(const method of ['GET','POST']){
      const result=simulate(method,'/api/staging/marketplace/'+op);
      assert.equal(result.code,503);
      assert.equal(result.body.error.code,'H2_GATEWAY_DISABLED');
    }
  }
});

test('NEW H2U OFF-only rejects query, unknown URLs and fake enabled headers',()=>{
  for(const url of [
    '/healthz?mode=ON','/api/staging/marketplace/save?enabled=1',
    '/api/staging/marketplace/SAVE','/api/staging/marketplace/unknown',
    'http://example.com/healthz','/api/staging/marketplace/save/..',
  ]){
    const result=simulate('GET',url);
    assert.equal(result.code,404);
  }
  for(const header of [
    {'x-oldx-enable':'true'},
    {'authorization':'Bearer owner'},
    {'x-serverless-authorization':'Bearer fake'},
    {'x-oldx-gateway-nonce':'forced'},
  ]){
    const r=simulate('POST','/api/staging/marketplace/save',header);
    assert.equal(r.code,503);
    assert.equal(r.body.error.code,'H2_GATEWAY_DISABLED');
  }
  assert.equal(simulate('HEAD','/healthz').code,404);
  assert.equal(simulate('GET','/'.repeat(2050)).code,400);
});

test('NEW H2U parse Cloud Run PORT and ensure server never autostarts',()=>{
  assert.equal(parseC2H2UCloudRunPort('8080'),8080);
  assert.equal(parseC2H2UCloudRunPort('65535'),65535);
  for(const v of [undefined,null,8080,'0','65536','08080','-2',
    '8080\n','8080;ENABLE','true','443.0','999999']){
    assert.throws(()=>parseC2H2UCloudRunPort(v),/H2U_INVALID_CLOUD_RUN_PORT/);
  }
  const server=createC2H2UPrivateOffHttpServer();
  assert.equal(server.listening,false);
  assert.equal(server.requestTimeout,10000);
  assert.equal(server.headersTimeout,5000);
  assert.equal(server.maxRequestsPerSocket,16);
  const entry=readFileSync(
    new URL('./c2-h2u-cloud-run-private-off-main.mjs',import.meta.url),
    'utf8');
  assert.match(entry,/createC2H2GatewayHostSource\(\)/);
  assert.match(entry,/h2s\.ready!==false/);
  assert.match(entry,/OLDX_H2U_MODE!=='OFF'/);
  assert.doesNotMatch(entry,/createC2H2GatewayHostSource\(\{[^}]*enabled:\s*true/);
});
