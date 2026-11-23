import test from 'node:test';
import assert from 'node:assert/strict';
import {createMarketplaceGateway,createTrustedMarketplaceBackend,createStagingMarketplaceTrustedHost} from '../../functions/staging-marketplace/trusted-host.mjs';
const audience='https://private-staging.invalid',site='https://oldx-staging-ui.invalid',principal='gateway-only@oldx-staging.iam.gserviceaccount.com';
const now=()=>100000,iam='gateway.iam.token',firebase='seller.firebase.token',path=op=>'/api/staging/marketplace/'+op;
const request=(op,headers={},body='{}',method='POST')=>new Request(site+path(op),{method,headers:{origin:site,'content-type':'application/json',...headers},...(method==='POST'?{body}:{} )});
function fixture(overrides={}){
 const calls=[];let credentials=0;
 const runtime={async handle(route,r){calls.push({route,headers:r.headers,body:JSON.parse(r.body)});return {status:200,body:{ok:true,operation:route.split('/').at(-1)}};}};
 const backend=createTrustedMarketplaceBackend({enabled:true,audience,gatewayServiceAccount:principal,verifyInvoker:async req=>({verified:req.headers.get('x-serverless-authorization')==='Bearer '+iam,principal,audience,expiresAtMs:200000}),commandRuntime:runtime,publicRuntime:runtime,now});
 const options={enabled:true,backendOrigin:audience,gatewayServiceAccount:principal,allowedOrigins:[site],now,getInvokerCredential:async()=>{credentials++;return {type:'cloud-run-iam-id-token',token:iam,principal,audience,expiresAtMs:200000};},fetchBackend:(url,init)=>backend.fetch(new Request(url,init)),...overrides};
 return {calls,backend,options,gateway:createMarketplaceGateway(options),get credentials(){return credentials;}};
}
test('server gateway keeps invoker token separate from Firebase, backend strips hop token from runtimes',async()=>{
 const x=fixture(),r=await x.gateway.fetch(request('save',{authorization:'Bearer '+firebase},'{"requestId":"same-retry"}'));
 assert.equal(r.status,200);assert.equal(r.headers.get('access-control-allow-origin'),site);
 assert.equal(r.headers.has('x-serverless-authorization'),false);assert.doesNotMatch(await r.text(),/gateway\.iam\.token/);
 assert.equal(x.calls[0].headers.authorization,'Bearer '+firebase);assert.equal(x.calls[0].headers['x-serverless-authorization'],undefined);
 assert.equal(x.calls[0].body.requestId,'same-retry');
 assert.equal((await x.gateway.fetch(request('detail'))).status,200);assert.equal(x.calls[1].headers.authorization,undefined);
});
test('guest cannot mutate or submit IAM credentials; backend requires independent trusted invoker proof',async()=>{
 const x=fixture();
 assert.equal((await x.gateway.fetch(request('save'))).status,401);
 assert.equal((await x.gateway.fetch(request('detail',{authorization:'Bearer '+firebase}))).status,403);
 assert.equal((await x.gateway.fetch(request('save',{authorization:'Bearer '+firebase,'x-serverless-authorization':'Bearer '+iam}))).status,403);
 assert.equal(x.credentials,0);assert.equal(x.calls.length,0);
 const backendRequest=(headers={})=>new Request(audience+path('save'),{method:'POST',headers:{'content-type':'application/json',authorization:'Bearer '+firebase,...headers},body:'{}'});
 assert.equal((await x.backend.fetch(backendRequest())).status,403);
 assert.equal((await x.backend.fetch(backendRequest({'x-serverless-authorization':'Bearer '+firebase}))).status,403);
 assert.equal((await x.backend.fetch(backendRequest({'x-serverless-authorization':'Bearer '+iam,authorization:'Bearer '+iam}))).status,401);
 assert.equal((await x.backend.fetch(backendRequest({'x-serverless-authorization':'Bearer '+iam,origin:site}))).status,403);
 assert.equal(x.calls.length,0);
});
test('CORS denies unknown/missing origin, forbidden preflight headers and all default/missing dependencies',async()=>{
 const x=fixture();
 assert.equal((await x.gateway.fetch(new Request('http://insecure.invalid'+path('list'),{method:'POST',headers:{origin:site,'content-type':'application/json'},body:'{}'}))).status,403);
 assert.equal((await x.gateway.fetch(request('list',{origin:'https://unknown.invalid'}))).status,403);
 const noOrigin=request('list');noOrigin.headers.delete('origin');assert.equal((await x.gateway.fetch(noOrigin)).status,403);
 const p=await x.gateway.fetch(request('save',{'access-control-request-method':'POST','access-control-request-headers':'authorization, content-type'},'', 'OPTIONS'));
 assert.equal(p.status,204);assert.equal(p.headers.has('access-control-allow-credentials'),false);
 assert.equal((await x.gateway.fetch(request('save',{'access-control-request-method':'POST','access-control-request-headers':'x-serverless-authorization'},'','OPTIONS'))).status,403);
 for(const patch of [{enabled:false},{allowedOrigins:[]},{allowedOrigins:['*']},{getInvokerCredential:null},{fetchBackend:null},{backendOrigin:'http://private.invalid'}]){
  assert.equal((await createMarketplaceGateway({...x.options,...patch}).fetch(request('list'))).status,503);
 }
 assert.equal((await createMarketplaceGateway().fetch(request('list'))).status,503);
 assert.equal((await createTrustedMarketplaceBackend().fetch(request('list'))).status,503);
 assert.equal((await createStagingMarketplaceTrustedHost().fetch(request('list'))).status,503);
 assert.equal(x.credentials,0);
});
test('credential audience/type/expiry/identity errors stop before private dispatch',async()=>{
 for(const patch of [{audience:site},{type:'firebase-id-token'},{principal:'wrong'},{expiresAtMs:100001},{token:firebase}]){
  let sends=0;const x=fixture({getInvokerCredential:()=>({type:'cloud-run-iam-id-token',token:iam,principal,audience,expiresAtMs:200000,...patch}),fetchBackend:()=>{sends++;}});
  assert.equal((await x.gateway.fetch(request('save',{authorization:'Bearer '+firebase}))).status,503);assert.equal(sends,0);
 }
});
test('bounded deadline, cancellation, oversize and lost mutation replies are safe with same-request recovery',async()=>{
 const x=fixture({timeoutMs:15,fetchBackend:()=>new Promise(()=>{})});
 const r=await x.gateway.fetch(request('save',{authorization:'Bearer '+firebase},'{"requestId":"retry-unchanged"}'));
 assert.equal(r.status,202);assert.equal((await r.json()).error.code,'OUTCOME_UNKNOWN');
 const read=await x.gateway.fetch(request('detail'));assert.equal(read.status,503);
 const pre=fixture({timeoutMs:15,getInvokerCredential:()=>new Promise(()=>{})});
 assert.equal((await pre.gateway.fetch(request('save',{authorization:'Bearer '+firebase}))).status,503);
 const c=new AbortController();c.abort();const q=request('detail');
 assert.equal((await fixture().gateway.fetch(new Request(q,{signal:c.signal}))).status,503);
 const big=fixture();assert.equal((await big.gateway.fetch(request('detail',{},JSON.stringify({large:'x'.repeat(4100)})))).status,503);assert.equal(big.credentials,0);
});
test('gateway strips backend headers and refuses invoker-token echoes or oversize responses',async()=>{
 const echo=fixture({fetchBackend:()=>Response.json({secret:iam},{headers:{'x-serverless-authorization':iam,'set-cookie':'private'}})});
 const response=await echo.gateway.fetch(request('detail'));assert.equal(response.status,503);assert.doesNotMatch(await response.text(),/gateway\.iam\.token/);assert.equal(response.headers.has('set-cookie'),false);
 const large=fixture({fetchBackend:()=>new Response('x'.repeat(65537),{headers:{'content-type':'application/json'}})});
 assert.equal((await large.gateway.fetch(request('detail'))).status,503);
});

test('existing Node listener binds fixed audience and preserves independent backend auth',async()=>{
 const {createTrustedMarketplaceListener}=await import('../../functions/staging-marketplace/trusted-host.mjs');
 const {createServer}=await import('node:http'),{once}=await import('node:events');
 const x=fixture(),server=createServer(createTrustedMarketplaceListener({enabled:true,audience,backend:x.backend}));
 server.listen(0,'127.0.0.1');await once(server,'listening');
 try{
  const local='http://127.0.0.1:'+server.address().port;
  const r=await fetch(local+path('save'),{method:'POST',headers:{'content-type':'application/json','x-serverless-authorization':'Bearer '+iam,authorization:'Bearer '+firebase,'x-forwarded-host':'forged.invalid'},body:'{}'});
  assert.equal(r.status,200);assert.equal(x.calls[0].headers.authorization,'Bearer '+firebase);
  assert.equal(x.calls[0].headers['x-forwarded-host'],undefined);
  assert.equal((await fetch(local+path('save'),{method:'POST',headers:{'content-type':'application/json',authorization:'Bearer '+firebase},body:'{}'})).status,403);
 }finally{await new Promise(resolve=>server.close(resolve));}
});
