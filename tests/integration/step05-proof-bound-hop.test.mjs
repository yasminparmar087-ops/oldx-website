import test from 'node:test';
import assert from 'node:assert/strict';
import {generateKeyPairSync,sign,verify,constants} from 'node:crypto';
import {createMarketplaceRequestProofSigner,createMarketplaceRequestProofVerifier,MARKETPLACE_REQUEST_PROOF_HEADER} from '../../scripts/marketplace-gateway-request-proof.mjs';
import {createProofBoundGatewayHop,createProofBoundBackendHop} from '../../scripts/marketplace-proof-bound-hop.mjs';
const key=generateKeyPairSync('rsa',{modulusLength:2048});
const idKey=generateKeyPairSync('rsa',{modulusLength:2048});
const root='https://private-staging.invalid', principal='gateway-only@oldx-staging.iam.gserviceaccount.com';
const path='/api/staging/marketplace/owner',firebase='Bearer seller.firebase.token',time=1000000,now=()=>time;
const body=new TextEncoder().encode('{"kind":"product","id":"p","requestId":"same-retry"}');
const makeToken=()=>{
 const enc=x=>Buffer.from(JSON.stringify(x)).toString('base64url');
 const input=enc({alg:'RS256',kid:'test'})+'.'+enc({iss:'https://accounts.google.com',aud:'urn:test:gateway',email:principal,exp:2000,iat:1000});
 return input+'.'+sign('RSA-SHA256',Buffer.from(input),{key:idKey.privateKey,padding:constants.RSA_PKCS1_PADDING}).toString('base64url');
};
const token=makeToken();
async function verifyIdentity(request,{audience}){
 const jwt=request.headers.get('x-oldx-gateway-attestation')??'',p=jwt.split('.');
 if(p.length!==3)return null;
 const claims=JSON.parse(Buffer.from(p[1],'base64url').toString('utf8'));
 if(!verify('RSA-SHA256',Buffer.from(p[0]+'.'+p[1]),{key:idKey.publicKey,padding:constants.RSA_PKCS1_PADDING},Buffer.from(p[2],'base64url'))||claims.email!==principal||claims.aud!=='urn:test:gateway')return null;
 return {verified:true,principal,audience,expiresAtMs:1100000};
}
const signIntent=createMarketplaceRequestProofSigner({enabled:true,kid:'request-1',now,random:()=>cryptoNonce(),signMessage:message=>sign('RSA-SHA256',message,{key:key.privateKey,padding:constants.RSA_PKCS1_PADDING})});
let seq=0;function cryptoNonce(){return new Uint8Array(16).fill(++seq);}
const consumed=new Set(),verifiedIntent=createMarketplaceRequestProofVerifier({enabled:true,now,resolvePublicKey:()=>key.publicKey,consumeNonce:async({nonceHash})=>{if(consumed.has(nonceHash))return {allowed:false};consumed.add(nonceHash);return {allowed:true};}});
const reqHeaders=()=>({'content-type':'application/json','x-serverless-authorization':'Bearer cloud.signed.token','x-oldx-gateway-attestation':token,authorization:firebase});
const req=(headers,raw=body)=>new Request(root+path,{method:'POST',headers,body:raw});

test('gateway and private backend compose signed intent, verified identity and one-use nonce without exposing proof downstream',async()=>{
 consumed.clear();seq=0;let downstream=0,forwarded;
 const backend=createProofBoundBackendHop({enabled:true,audience:root,gatewayServiceAccount:principal,verifyAttestation:verifyIdentity,verifyRequestProof:verifiedIntent,now,backend:{async fetch(request){downstream++;assert.equal(request.headers.has(MARKETPLACE_REQUEST_PROOF_HEADER),false);return Response.json({ok:true});}}});
 const hop=createProofBoundGatewayHop({enabled:true,backendOrigin:root,signRequestProof:signIntent,fetchBackend:(url,options)=>{forwarded={url,headers:new Headers(options.headers),body:options.body};return backend.fetch(new Request(url,{method:'POST',headers:options.headers,body:options.body}));}});
 const response=await hop(root+path,{method:'POST',headers:reqHeaders(),body});
 assert.equal(response.status,200);assert.deepEqual(await response.json(),{ok:true});assert.equal(downstream,1);
 assert.equal(response.headers.has(MARKETPLACE_REQUEST_PROOF_HEADER),false);
 assert.equal((await backend.fetch(req(forwarded.headers,forwarded.body))).status,403);assert.equal(downstream,1);
 const again=await hop(root+path,{method:'POST',headers:reqHeaders(),body});assert.equal(again.status,200);assert.equal(downstream,2);
});
test('tampered body/auth/attestation, spoofed request proof and missing identity deny before backend dispatch',async()=>{
 consumed.clear();seq=0;let downstream=0;
 const backend=createProofBoundBackendHop({enabled:true,audience:root,gatewayServiceAccount:principal,verifyAttestation:verifyIdentity,verifyRequestProof:verifiedIntent,now,backend:{fetch(){downstream++;return Response.json({ok:true});}}});
 const proof=await signIntent({method:'POST',path,body,authorization:firebase,attestationToken:token});
 const headers={...reqHeaders(),[MARKETPLACE_REQUEST_PROOF_HEADER]:proof};
 assert.equal((await backend.fetch(req(headers,new TextEncoder().encode('{"bad":true}')))).status,403);
 assert.equal((await backend.fetch(req({...headers,authorization:'Bearer other.firebase.token'}))).status,403);
 assert.equal((await backend.fetch(req({...headers,'x-oldx-gateway-attestation':token.slice(0,-5)+'abcde'}))).status,403);
 assert.equal((await backend.fetch(req({...reqHeaders(),[MARKETPLACE_REQUEST_PROOF_HEADER]:'fake.signature'}))).status,403);
 assert.equal((await backend.fetch(req(reqHeaders()))).status,403);
 assert.equal(downstream,0);
 const gateway=createProofBoundGatewayHop({enabled:true,backendOrigin:root,signRequestProof:signIntent,fetchBackend:()=>Response.json({ok:true})});
 await assert.rejects(()=>gateway(root+path,{method:'POST',body,headers:{...reqHeaders(),[MARKETPLACE_REQUEST_PROOF_HEADER]:proof}}));
});
test('inactive/missing providers, untrusted URLs and proof echo deny without network side effects',async()=>{
 let sends=0;
 const off=createProofBoundGatewayHop({enabled:false,backendOrigin:root,signRequestProof:signIntent,fetchBackend:()=>{sends++;return Response.json({ok:true});}});
 await assert.rejects(()=>off(root+path,{method:'POST',headers:reqHeaders(),body}));
 const failed=createProofBoundGatewayHop({enabled:true,backendOrigin:root,signRequestProof:signIntent,fetchBackend:(_url,init)=>{sends++;return Response.json({leak:init.headers.get(MARKETPLACE_REQUEST_PROOF_HEADER)});}});
 await assert.rejects(()=>failed(root+path,{method:'POST',headers:reqHeaders(),body}));assert.equal(sends,1);
 await assert.rejects(()=>failed('https://forged.invalid'+path,{method:'POST',headers:reqHeaders(),body}));assert.equal(sends,1);
 const b=createProofBoundBackendHop();assert.equal((await b.fetch(req(reqHeaders()))).status,503);
 const wrong=createProofBoundBackendHop({enabled:true,audience:root,gatewayServiceAccount:principal,verifyAttestation:verifyIdentity,verifyRequestProof:null,backend:{fetch:()=>Response.json({ok:true})}});
 assert.equal((await wrong.fetch(req(reqHeaders()))).status,503);
});
