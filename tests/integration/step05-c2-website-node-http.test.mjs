import test from 'node:test';
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {once} from 'node:events';
import {createC2WebsiteNodeHandler} from '../../functions/staging-marketplace/c2-website-node-http.mjs';
const host='https://mediator-stage.invalid',site='https://oldx-stage.invalid';
async function onLoopback(handler,fn){
 const server=createServer(handler);
 server.listen(0,'127.0.0.1');await once(server,'listening');
 const address='http://127.0.0.1:'+server.address().port;
 try{await fn(address);}finally{server.closeAllConnections();await new Promise(ok=>server.close(ok));}
}
const options={enabled:true,websiteOrigin:host,allowedOrigins:[host,site]};
const at=(origin=site)=>({'origin':origin,'content-type':'application/json'});

test('G1 server adapter is default-OFF, no mediator call or side effect',async()=>{
 let called=0;
 await onLoopback(createC2WebsiteNodeHandler({websiteOrigin:host,allowedOrigins:[host,site],
  mediator:{fetch:()=>{called++;return Response.json({ok:true});}}}),async(base)=>{
   const r=await fetch(base+'/api/staging/marketplace/list',{method:'POST',headers:at(),body:'{}'});
   assert.equal(r.status,503);assert.equal(called,0);
  });
});

test('G1 fixed HTTPS website origin and Firebase auth are passed to trusted mediator; Host spoof ignored',async()=>{
 const seen=[];
 const handler=createC2WebsiteNodeHandler({...options,mediator:{fetch:async r=>{
  seen.push({url:r.url,authorization:r.headers.get('authorization'),origin:r.headers.get('origin'),body:await r.text(),forwarded:r.headers.get('x-forwarded-host')});
  return Response.json({ok:true},{headers:{'access-control-allow-origin':site}});
 }}});
 await onLoopback(handler,async(base)=>{
  const r=await fetch(base+'/api/staging/marketplace/save',{method:'POST',headers:{...at(),'authorization':'Bearer firebase-fixture','x-forwarded-host':'malicious.invalid'},body:'{"kind":"product"}'});
  assert.equal(r.status,200);assert.equal(r.headers.get('access-control-allow-origin'),site);
 });
 assert.deepEqual(seen,[{url:host+'/api/staging/marketplace/save',authorization:'Bearer firebase-fixture',origin:site,body:'{"kind":"product"}',forwarded:null}]);
});

test('G1 public guest/list cap, forbidden headers, method, exact paths and invalid origins fail before mediator',async()=>{
 let calls=0;
 const handler=createC2WebsiteNodeHandler({...options,mediator:{fetch:()=>{calls++;return Response.json({ok:true});}}});
 await onLoopback(handler,async(base)=>{
  const cases=[
   {path:'/api/staging/marketplace/list',method:'POST',headers:at(),body:'x'.repeat(4097),status:413},
   {path:'/api/staging/marketplace/list?x=1',method:'POST',headers:at(),body:'{}',status:404},
   {path:'/api/staging/marketplace/save',method:'GET',headers:at(),status:405},
   {path:'/api/staging/marketplace/save',method:'POST',headers:{...at(),cookie:'x=1'},body:'{}',status:403},
   {path:'/api/staging/marketplace/save',method:'POST',headers:{...at(),'x-serverless-authorization':'Bearer fake'},body:'{}',status:403},
   {path:'/api/staging/marketplace/save',method:'POST',headers:{...at(),'x-oldx-gateway-request-proof':'forged'},body:'{}',status:403},
   {path:'/api/staging/marketplace/save',method:'POST',headers:at('https://evil.invalid'),body:'{}',status:403},
  ];
  for(const c of cases){const {path,status,...init}=c;const r=await fetch(base+path,init);assert.equal(r.status,status,path);}
 });
 assert.equal(calls,0);
});

test('G1 CORS preflight safely delegates without calling Google IAM or guest quota provider',async()=>{
 const seen=[];
 const handler=createC2WebsiteNodeHandler({...options,mediator:{fetch:request=>{
  seen.push({method:request.method,url:request.url,preflight:request.headers.get('access-control-request-method')});
  return new Response(null,{status:204,headers:{'access-control-allow-origin':site,'access-control-allow-methods':'POST','vary':'Origin'}});
 }}});
 await onLoopback(handler,async(base)=>{
  const r=await fetch(base+'/api/staging/marketplace/list',{method:'OPTIONS',headers:{origin:site,'access-control-request-method':'POST'}});
  assert.equal(r.status,204);assert.equal(r.headers.get('access-control-allow-origin'),site);
  assert.equal(r.headers.get('access-control-allow-methods'),'POST');
 });
 assert.deepEqual(seen,[{method:'OPTIONS',url:host+'/api/staging/marketplace/list',preflight:'POST'}]);
});
