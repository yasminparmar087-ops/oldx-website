import test from 'node:test';
import assert from 'node:assert/strict';
import {generateKeyPairSync,sign,constants} from 'node:crypto';
import {createMarketplaceRequestProofSigner,createMarketplaceRequestProofVerifier} from '../../scripts/marketplace-gateway-request-proof.mjs';
const rsa=generateKeyPairSync('rsa',{modulusLength:2048}),other=generateKeyPairSync('rsa',{modulusLength:2048});
const route='/api/staging/marketplace/save',attestation='signed.identity.attestationexample',firebase='Bearer seller.firebase.token';
let clock=1000000,n=0;
const now=()=>clock;
const buffer=v=>Buffer.from(v);
const signer=(overrides={})=>createMarketplaceRequestProofSigner({enabled:true,kid:'bound-key-1',now,random:()=>Buffer.alloc(16,++n),signMessage:async bytes=>sign('RSA-SHA256',bytes,{key:rsa.privateKey,padding:constants.RSA_PKCS1_PADDING}),...overrides});
const verifier=(consumeNonce,options={})=>createMarketplaceRequestProofVerifier({enabled:true,now,resolvePublicKey:async()=>rsa.publicKey,consumeNonce,...options});
const input=(patch={})=>({method:'POST',path:route,body:buffer('{"requestId":"same-retry"}'),authorization:firebase,attestationToken:attestation,...patch});
function sharedStore(){const consumed=new Set();return async ({nonceHash})=>{if(consumed.has(nonceHash))return {allowed:false};consumed.add(nonceHash);return {allowed:true};};}

test('new signature binds exact command request; atomic nonce rejects replay, fresh nonce permits same-requestId recovery',async()=>{
 n=0;clock=1000000;const s=signer(),v=verifier(sharedStore());const command=input();
 const p=await s(command);assert.ok(p&&p.length<=2048);
 assert.equal(await v({...command,proof:p}),true);
 assert.equal(await v({...command,proof:p}),false);
 const next=await s(command);assert.notEqual(next,p);
 assert.equal(await v({...command,proof:next}),true);
});
test('mutated method/path/body/Firebase token/attestation and forged signatures are denied without consuming a nonce',async()=>{
 n=0;clock=2000000;let consumes=0;const v=verifier(async()=>{consumes++;return {allowed:true};});const command=input();const proof=await signer()(command);
 assert.equal(await v({...command,proof,path:'/api/staging/marketplace/owner'}),false);
 assert.equal(await v({...command,proof,method:'GET'}),false);
 assert.equal(await v({...command,proof,body:buffer('{"requestId":"changed"}')}),false);
 assert.equal(await v({...command,proof,authorization:'Bearer another.firebase.token'}),false);
 assert.equal(await v({...command,proof,attestationToken:'different.identity.tokenexample'}),false);
 assert.equal(await v({...command,proof:proof.slice(0,-1)+(proof.endsWith('A')?'B':'A')}),false);
 assert.equal(await verifier(async()=>({allowed:true}),{resolvePublicKey:async()=>other.publicKey})({...command,proof}),false);
 assert.equal(consumes,0);
 assert.equal(await v({...command,proof}),true);assert.equal(consumes,1);
});
test('expired, future, malformed, no durable nonce, timeout and disabled routes fail closed',async()=>{
 n=0;clock=3000000;const command=input(),s=signer(),proof=await s(command);
 assert.equal(createMarketplaceRequestProofVerifier(),null);
 assert.equal(createMarketplaceRequestProofSigner(),null);
 const noStore=verifier(async()=>({allowed:false}));assert.equal(await noStore({...command,proof}),false);
 assert.equal(await verifier(async()=>({allowed:true}),{now:()=>clock+30000})({...command,proof}),false);
 assert.equal(await verifier(async()=>({allowed:true}),{now:()=>clock-5000})({...command,proof}),false);
 assert.equal(await verifier(async()=>({allowed:true}),{resolvePublicKey:async()=>null})({...command,proof}),false);
 assert.equal(await verifier(async()=>({allowed:true}),{resolvePublicKey:async()=>new Promise(()=>{}),timeoutMs:10})({...command,proof}),false);
 assert.equal(await verifier(async()=>({allowed:true}))({...command,proof:'abc.bad'}),false);
 assert.equal(await s(input({path:'/admin/delete'})),null);
 assert.equal(await s(input({body:buffer('x'.repeat(33000))})),null);
 const canceled=new AbortController();canceled.abort();
 assert.equal(await verifier(async()=>({allowed:true}))({...command,proof,signal:canceled.signal}),false);
});
test('anonymous reads bind to no Firebase token and accept valid cryptographic proof with independent nonce store',async()=>{
 n=0;clock=4000000;const command=input({path:'/api/staging/marketplace/detail',body:buffer('{"id":"p1"}'),authorization:null});
 const p=await signer()(command),v=verifier(sharedStore());
 assert.equal(await v({...command,proof:p}),true);
 assert.equal(await v({...command,proof:p,authorization:firebase}),false);
});
