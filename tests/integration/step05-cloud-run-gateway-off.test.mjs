import test from 'node:test';
import assert from 'node:assert/strict';
import {once} from 'node:events';
import {createStep05OffGatewayServer,listenStep05OffGateway,drainStep05OffGateway} from '../../functions/staging-marketplace/cloud-run-gateway-off-server.mjs';

async function withServer(fn){
 const server=createStep05OffGatewayServer();server.listen(0,'127.0.0.1');await once(server,'listening');
 try{return await fn('http://127.0.0.1:'+server.address().port);}finally{await drainStep05OffGateway(server);}
}
test('C1A health is process-only and independent of all product/identity providers',async()=>withServer(async base=>{
 for(const path of ['/healthz','/health']){
  const get=await fetch(base+path);assert.equal(get.status,200);
  assert.deepEqual(await get.json(),{ok:true});
  assert.equal(get.headers.get('cache-control'),'private, no-store');
  const head=await fetch(base+path,{method:'HEAD'});assert.equal(head.status,200);assert.equal(await head.text(),'');
 }
 assert.equal((await fetch(base+'/healthz',{method:'POST'})).status,405);
}));
test('ALL API endpoints default OFF even with activation headers, fake signed tokens and POST bodies',async()=>withServer(async base=>{
 for(const path of ['/api','/api/','/api/staging/marketplace/save','/api/staging/marketplace/list','/api/staging/marketplace/owner','/api/secret']){
  const resp=await fetch(base+path,{method:'POST',headers:{authorization:'Bearer forged.id.token','x-serverless-authorization':'Bearer fake.cloud.token','x-oldx-gateway-attestation':'fake.token.signature','content-type':'application/json'},body:JSON.stringify({activate:true})});
  assert.equal(resp.status,503,path);assert.equal((await resp.json()).error.code,'ENFORCEMENT_UNAVAILABLE');
 }
 assert.equal((await fetch(base+'/api/staging/marketplace/owner',{method:'GET'})).status,503);
}));
test('unknown and malformed URLs fail closed; no request headers or private server source echoed',async()=>withServer(async base=>{
 for(const path of ['/', '/admin','/healthz?debug=true','/api%2fsecret','/server.mjs','/package.json']){
  const resp=await fetch(base+path);assert.equal(resp.status,404,path);
  const str=await resp.text();assert.equal(str.includes('forged'),false);
  assert.equal(str.includes('import {'),false);
  assert.equal(resp.headers.get('set-cookie'),null);
 }
 const denied=await fetch(base+'/api?token=private');assert.equal(denied.status,503);
}));
test('invalid ports/hosts fail before listen and shutdown drains cleanly',async()=>{
 for(const port of ['0','65536','abc','-1','8080x']){
  const server=createStep05OffGatewayServer();await assert.rejects(()=>listenStep05OffGateway(server,{port}));
  assert.equal(server.listening,false);
 }
 const server=createStep05OffGatewayServer();await assert.rejects(()=>listenStep05OffGateway(server,{port:8080,host:'example.org'}));
 assert.equal(server.listening,false);
 const active=createStep05OffGatewayServer();active.listen(0,'127.0.0.1');await once(active,'listening');await drainStep05OffGateway(active);assert.equal(active.listening,false);
});
