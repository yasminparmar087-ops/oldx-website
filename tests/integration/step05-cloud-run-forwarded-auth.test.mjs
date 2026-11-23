import test from 'node:test';
import assert from 'node:assert/strict';
import {createTrustedMarketplaceBackend} from '../../functions/staging-marketplace/trusted-host.mjs';
import {createMarketplaceCommandHttp} from '../../scripts/marketplace-command-http.mjs';
const audience='https://private-staging.invalid',principal='gateway-only@oldx-staging.iam.gserviceaccount.com',now=()=>100000;
const path=op=>'/api/staging/marketplace/'+op;
const firebase='seller.firebase.signature';
function fixture({trusted=true,verify=true,claims={},uid='seller'}={}){
 const seen=[];let verifiedUser=0;
 // Independently supplied TEST proof; never derives principal/verified from
 // X-Serverless-Authorization, JWT payload, marker, Origin or forwarded headers.
 const proof={verified:true,principal,audience,expiresAtMs:200000,...claims};
 const http=createMarketplaceCommandHttp({enabled:true,now,verifyFirebaseToken:async token=>{
  verifiedUser++;if(token!==firebase)throw Error('Invalid Firebase user');
  return {uid};
 },consumeRateLimit:()=>({allowed:true}),createRepository:()=>({owner:async()=>{
  if(uid!=='seller')return {ok:false,code:'DENIED'};
  return {ok:true,id:'product',revision:1,profile:{title:'ગુજરાતી हिन्दी',description:'Synthetic',category:'cars',locationLabel:'Sample',basePrice:1,isSold:false,storeId:null,photos:[]},published:false,publicationRevision:0,receipt:null};
 }})});
 const commandRuntime={handle(route,request,context){seen.push(request.headers);return http.handle(route.split('/').at(-1),request,context);}};
 const publicRuntime={handle(_path,request){seen.push(request.headers);return Promise.resolve({status:200,body:{ok:true,items:[],nextCursor:null,publicationEpoch:0}});}};
 const backend=createTrustedMarketplaceBackend({enabled:true,audience,gatewayServiceAccount:principal,now,
  ...(verify?{verifyInvoker:async()=>trusted?proof:null}:{}),commandRuntime,publicRuntime});
 const request=(iam,auth=firebase,op='owner',extra={})=>new Request(audience+path(op),{method:'POST',headers:{'content-type':'application/json',...(iam===null?{}:{'x-serverless-authorization':iam}),...(auth===null?{}:{authorization:'Bearer '+auth}),...extra},body:JSON.stringify(op==='owner'?{kind:'product',id:'product',requestId:null}:{kind:'product',limit:12,category:'',storeId:null,cursor:null})});
 return {backend,request,seen,get verifiedUser(){return verifiedUser;}};
}
test('signature-stripped forwarding is transport-only; independent proof and valid Firebase identity still required',async()=>{
 // Google documents signature removal, NOT an exact replacement syntax.
 // Exercise empty/missing signature and marker representations without relying
 // on any representation as a platform-authentication attestation.
 for(const stripped of ['Bearer header.payload.','Bearer header.payload','Bearer header.payload.SIGNATURE_REMOVED_BY_GOOGLE']){
  const x=fixture(),r=await x.backend.fetch(x.request(stripped));assert.equal(r.status,200);
  assert.equal(x.verifiedUser,1);assert.equal(x.seen[0].authorization,'Bearer '+firebase);
  assert.equal(x.seen[0]['x-serverless-authorization'],undefined);
 }
 const guest=fixture();assert.equal((await guest.backend.fetch(guest.request('Bearer header.payload.',null))).status,401);assert.equal(guest.verifiedUser,0);
 const invalid=fixture();assert.equal((await invalid.backend.fetch(invalid.request('Bearer header.payload.','invalid.firebase.signature'))).status,401);
 const other=fixture({uid:'other'});assert.equal((await other.backend.fetch(other.request('Bearer header.payload.'))).status,403);
 const publicRead=fixture();assert.equal((await publicRead.backend.fetch(publicRead.request('Bearer header.payload.',null,'list'))).status,200);assert.equal(publicRead.verifiedUser,0);
 assert.equal((await publicRead.backend.fetch(publicRead.request('Bearer header.payload.',firebase,'list'))).status,403);
});
test('stripped/full/spoofed headers cannot replace missing independent gateway proof',async()=>{
 const missing=fixture({verify:false});assert.equal((await missing.backend.fetch(missing.request('Bearer header.payload.'))).status,503);assert.equal(missing.verifiedUser,0);
 for(const header of ['Bearer header.payload.','Bearer header.payload','Bearer header.payload.SIGNATURE_REMOVED_BY_GOOGLE','Bearer forged.claims.signature']){
  const x=fixture({trusted:false});
  const r=await x.backend.fetch(x.request(header,firebase,'owner',{'x-forwarded-user':principal,'x-gateway-verified':'true'}));
  assert.equal(r.status,403);assert.equal(x.seen.length,0);assert.equal(x.verifiedUser,0);
 }
 for(const claims of [{verified:false},{principal:'foreign@oldx-staging.iam.gserviceaccount.com'},{audience:'https://foreign.invalid'},{expiresAtMs:99999}]){
  const x=fixture({claims});assert.equal((await x.backend.fetch(x.request('Bearer header.payload.'))).status,403);assert.equal(x.seen.length,0);
 }
 const x=fixture();
 for(const iam of [null,'not-bearer', 'Bearer '+ 'a'.repeat(8193)]){
  assert.equal((await x.backend.fetch(x.request(iam))).status,403);
 }
 assert.equal((await x.backend.fetch(x.request('Bearer '+firebase))).status,401);assert.equal(x.seen.length,0);
 assert.equal((await createTrustedMarketplaceBackend().fetch(x.request('Bearer header.payload.'))).status,503);
});
