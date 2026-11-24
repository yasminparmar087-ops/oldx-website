import test from 'node:test';
import assert from 'node:assert/strict';
import {generateKeyPairSync,KeyObject} from 'node:crypto';
import {createGoogleGatewayPublicKeyResolver,GOOGLE_GATEWAY_JWKS_URL} from '../../scripts/google-gateway-public-keys.mjs';
const issuer='https://accounts.google.com', rsa=generateKeyPairSync('rsa',{modulusLength:2048});
const jwk=rsa.publicKey.export({format:'jwk'});
const goodKey={kty:'RSA',alg:'RS256',use:'sig',kid:'trusted-1',n:jwk.n,e:jwk.e};
const reply=(data={keys:[goodKey]},headers={})=>new Response(JSON.stringify(data),{status:200,headers:{'content-type':'application/json','cache-control':'public, max-age=120',...headers}});

test('explicit default OFF; fixed Google HTTPS endpoint, no attacker-selected URL',async()=>{
 assert.equal(createGoogleGatewayPublicKeyResolver(),null);
 let called=0;
 const resolver=createGoogleGatewayPublicKeyResolver({enabled:true,issuer,fetchRequest:(url,init)=>{called++;assert.equal(url,GOOGLE_GATEWAY_JWKS_URL);assert.equal(init.redirect,'error');assert.equal(init.credentials,'omit');return reply();}});
 assert.equal(await resolver({issuer:'https://attacker.invalid',kid:'trusted-1'}),null);
 assert.equal(await resolver({issuer,kid:'bad kid'}),null);
 assert.equal(called,0);
 assert.ok((await resolver({issuer,kid:'trusted-1'})) instanceof KeyObject);
 assert.equal(called,1);
});
test('cache preserves fresh keys, rotation on missing kid and hard expiry; no stale fallback',async()=>{
 let clock=200000,calls=0;
 const second=generateKeyPairSync('rsa',{modulusLength:2048}).publicKey.export({format:'jwk'});
 const resolver=createGoogleGatewayPublicKeyResolver({enabled:true,issuer,now:()=>clock,minimumRefreshMs:1000,fetchRequest:()=>{calls++;if(calls===3)throw Error('offline');return reply({keys:[calls===1?goodKey:{...goodKey,kid:'rotated',n:second.n,e:second.e}]});}});
 assert.ok(await resolver({issuer,kid:'trusted-1'}));
 assert.ok(await resolver({issuer,kid:'trusted-1'}));assert.equal(calls,1);
 assert.equal(await resolver({issuer,kid:'rotated'}),null);assert.equal(calls,1);
 clock+=1200;assert.ok(await resolver({issuer,kid:'rotated'}));assert.equal(calls,2);
 clock+=120001;assert.equal(await resolver({issuer,kid:'rotated'}),null);assert.equal(calls,3);
});
test('malformed, duplicate, wrong and oversized keys fail closed',async()=>{
 const cases=[{keys:[]},{keys:[goodKey,goodKey]},{keys:[{...goodKey,alg:'HS256'}]},{keys:[{...goodKey,kty:'EC'}]},{keys:[{...goodKey,e:'AQAC'}]}];
 for(const data of cases){const fn=createGoogleGatewayPublicKeyResolver({enabled:true,issuer,fetchRequest:()=>reply(data)});assert.equal(await fn({issuer,kid:'trusted-1'}),null);}
 const big=createGoogleGatewayPublicKeyResolver({enabled:true,issuer,fetchRequest:()=>new Response('x'.repeat(40000),{headers:{'content-type':'application/json','cache-control':'max-age=120'}})});
 assert.equal(await big({issuer,kid:'trusted-1'}),null);
});
test('timeout, abort, throttled failures and untrusted cache policy cause denial',async()=>{
 const absent=createGoogleGatewayPublicKeyResolver({enabled:true,issuer,timeoutMs:10,fetchRequest:()=>new Promise(()=>{})});
 assert.equal(await absent({issuer,kid:'trusted-1'}),null);
 const controller=new AbortController();controller.abort();
 const denied=createGoogleGatewayPublicKeyResolver({enabled:true,issuer,fetchRequest:()=>reply()});
 assert.equal(await denied({issuer,kid:'trusted-1',signal:controller.signal}),null);
 let failCalls=0,clock=10000;
 const throttled=createGoogleGatewayPublicKeyResolver({enabled:true,issuer,now:()=>clock,minimumRefreshMs:1000,fetchRequest:()=>{failCalls++;throw Error('offline');}});
 assert.equal(await throttled({issuer,kid:'trusted-1'}),null);
 assert.equal(await throttled({issuer,kid:'trusted-1'}),null);assert.equal(failCalls,1);
 clock+=1001;assert.equal(await throttled({issuer,kid:'trusted-1'}),null);assert.equal(failCalls,2);
 const noTtl=createGoogleGatewayPublicKeyResolver({enabled:true,issuer,fetchRequest:()=>reply(undefined,{'cache-control':'public'})});
 assert.equal(await noTtl({issuer,kid:'trusted-1'}),null);
});
