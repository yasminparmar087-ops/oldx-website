import test from 'node:test';
import assert from 'node:assert/strict';
import {generateKeyPairSync,sign,constants,createSecretKey} from 'node:crypto';
import {createGatewayAttestationVerifier,GATEWAY_ATTESTATION_HEADER as header} from '../../scripts/gateway-attestation.mjs';
import {createTrustedMarketplaceBackend,createAttestedStagingMarketplaceHost,createAttestedMarketplaceGateway} from '../../functions/staging-marketplace/trusted-host.mjs';
import {createMarketplaceCommandHttp} from '../../scripts/marketplace-command-http.mjs';
// Ephemeral fixture keys only; never saved/exported or claimed to be Google keys.
const rsa=generateKeyPairSync('rsa',{modulusLength:2048}),wrong=generateKeyPairSync('rsa',{modulusLength:2048});
const clock=1800000000000,now=()=>clock,seconds=clock/1000;
const audience='https://private-staging.invalid',attestationAudience='urn:oldx:test:gateway-attestation';
const principal='gateway-only@oldx-staging.iam.gserviceaccount.com',subject='123456789012345678901',issuer='https://accounts.google.com';
const config={enabled:true,identityType:'google-service-account',issuer,attestationAudience,iamAudience:audience,expectedPrincipal:principal,expectedSubject:subject,now,resolvePublicKey:({issuer:i,kid})=>i===issuer&&kid==='test-key'?rsa.publicKey:null};
const claims={iss:issuer,aud:attestationAudience,sub:subject,email:principal,email_verified:true,iat:seconds,exp:seconds+3600};
function token(c=claims,h={alg:'RS256',kid:'test-key',typ:'JWT'},key=rsa.privateKey){
 const enc=v=>Buffer.from(typeof v==='string'?v:JSON.stringify(v)).toString('base64url');
 const body=enc(h)+'.'+enc(c);
 return body+'.'+sign('RSA-SHA256',Buffer.from(body),{key,padding:constants.RSA_PKCS1_PADDING}).toString('base64url');
}
const req=value=>new Request(audience+'/api/staging/marketplace/list',{method:'POST',headers:{...(value===null?{}:{[header]:value})},body:'{}'});
const verify=(v,t,ctx={})=>v(req(t),{audience,...ctx});
test('real RSA signature establishes pinned numeric subject and verified email for separate audience',async()=>{
 const v=createGatewayAttestationVerifier(config),proof=await verify(v,token());
 assert.equal(proof.verified,true);assert.equal(proof.principal,principal);assert.equal(proof.subject,subject);assert.notEqual(proof.subject,proof.principal);
 assert.equal(proof.audience,audience);assert.equal(proof.assertionAudience,attestationAudience);assert.equal(proof.expiresAtMs,clock+60000);
 assert.equal(createGatewayAttestationVerifier(),null);
 assert.equal(createGatewayAttestationVerifier({...config,attestationAudience:audience}),null);
 assert.equal(createGatewayAttestationVerifier({...config,identityType:'arbitrary-oidc'}),null);
 assert.equal(await verify(v,token(),{audience:'https://foreign.invalid'}),null);
 assert.equal(await verify(v,null),null);
});
test('signature tampering, wrong keys/kid, key confusion and header URLs fail cryptographically closed',async()=>{
 const v=createGatewayAttestationVerifier(config),good=token(),parts=good.split('.');
 const badPayload=Buffer.from(JSON.stringify({...claims,email:'foreign@oldx-staging.iam.gserviceaccount.com'})).toString('base64url');
 assert.equal(await verify(v,[parts[0],badPayload,parts[2]].join('.')),null);
 const sig=Buffer.from(parts[2],'base64url');sig[0]^=1;
 assert.equal(await verify(v,[parts[0],parts[1],sig.toString('base64url')].join('.')),null);
 assert.equal(await verify(v,token(claims,undefined,wrong.privateKey)),null);
 assert.equal(await verify(v,token(claims,{alg:'RS256',kid:'unknown'})),null);
 for(const key of [wrong.publicKey,rsa.privateKey,createSecretKey(Buffer.alloc(32)),generateKeyPairSync('ec',{namedCurve:'P-256'}).publicKey]){
  assert.equal(await verify(createGatewayAttestationVerifier({...config,resolvePublicKey:()=>key}),good),null);
 }
 let resolves=0;const guarded=createGatewayAttestationVerifier({...config,resolvePublicKey:()=>{resolves++;return rsa.publicKey;}});
 for(const h of [{alg:'none',kid:'test-key'},{alg:'HS256',kid:'test-key'},{alg:'RS256',kid:'test-key',jku:'https://untrusted.invalid'},{alg:'RS256',kid:'test-key',x5u:'https://untrusted.invalid'},{alg:'RS256',kid:'test-key',jwk:{}},{alg:'RS256',kid:'test-key',crit:['alg']},'{"alg":"RS256","alg":"none","kid":"test-key"}']){
  assert.equal(await verify(guarded,token(claims,h)),null);
 }
 assert.equal(resolves,0);
});
test('issuer/audience/principal/time checks run after signature and reject stale/future/malformed claims',async()=>{
 const v=createGatewayAttestationVerifier(config);
 for(const patch of [{iss:'https://foreign.invalid'},{aud:audience},{aud:[attestationAudience]},{sub:principal},{sub:'987654321'},{email:'foreign@oldx-staging.iam.gserviceaccount.com'},{email:undefined},{email_verified:false},{email_verified:'true'},{email_verified:undefined},{iat:seconds-61},{iat:seconds+6},{iat:seconds+.1},{exp:seconds},{exp:seconds+3601},{exp:'1800000100'},{nbf:seconds+6},{nbf:-1},{nbf:seconds+4000}]){
  assert.equal(await verify(v,token({...claims,...patch})),null,JSON.stringify(patch));
 }
 assert.equal(await verify(v,token('{"iss":"https://accounts.google.com","iss":"evil"}')),null);
 for(const malformed of ['', 'a.b', 'a.b.', 'a.b.c.d', 'x'.repeat(8193), token()+'='])assert.equal(await verify(v,malformed),null);
 assert.equal(await verify(createGatewayAttestationVerifier({...config,now:()=>NaN}),token()),null);
 const futureOk=await verify(v,token({...claims,iat:seconds+4,nbf:seconds+4}));assert.equal(futureOk.verified,true);
});
test('trusted resolver rotation/failure/cancellation/deadline never trusts token-selected network configuration',async()=>{
 const seen=[];let current=rsa.publicKey;
 const v=createGatewayAttestationVerifier({...config,resolvePublicKey:input=>{seen.push(input);return current;}});
 assert.ok(await verify(v,token()));current=wrong.publicKey;assert.equal(await verify(v,token()),null);
 assert.deepEqual(Object.keys(seen[0]).sort(),['issuer','kid','signal']);assert.equal(seen[0].issuer,issuer);assert.equal(seen[0].kid,'test-key');
 assert.equal(await verify(v,token(),{signal:AbortSignal.abort()}),null);
 let stopped=false;
 const slow=createGatewayAttestationVerifier({...config,keyTimeoutMs:10,resolvePublicKey:({signal})=>{signal.addEventListener('abort',()=>stopped=true);return new Promise(()=>{});}});
 assert.equal(await verify(slow,token()),null);assert.equal(stopped,true);
 assert.equal(await verify(createGatewayAttestationVerifier({...config,resolvePublicKey:()=>{throw Error('private provider failure');}}),token()),null);
});
test('actual signed gateway assertion integrates with stripped IAM and separate Firebase ownership boundary',async()=>{
 const site='https://ui-staging.invalid',firebase='seller.firebase.signature',iam='cloud.iam.signature';
 let user='seller',authCalls=0,attestCalls=0,dispatches=0;
 const http=createMarketplaceCommandHttp({enabled:true,now,verifyFirebaseToken:async(t,ctx)=>{
  authCalls++;assert.equal(ctx.checkRevoked,true);if(t!==firebase)throw Error('Invalid user');return {uid:user};
 },consumeRateLimit:()=>({allowed:true}),createRepository:()=>({owner:async()=>user==='seller'?{ok:true,id:'p',revision:1,profile:{title:'ગુજરાતી हिन्दी',description:'Synthetic',category:'cars',locationLabel:'Sample',basePrice:1,isSold:false,storeId:null,photos:[]},published:false,publicationRevision:0,receipt:null}:{ok:false,code:'DENIED'}})});
 const runtime={handle(path,r,ctx){assert.equal(r.headers[header],undefined);assert.equal(r.headers['x-serverless-authorization'],undefined);return http.handle(path.split('/').at(-1),r,ctx);}};
 const backend=createTrustedMarketplaceBackend({enabled:true,audience,gatewayServiceAccount:principal,verifyInvoker:createGatewayAttestationVerifier(config),commandRuntime:runtime,publicRuntime:{handle:()=>({status:200,body:{ok:true}})},now});
 const options={enabled:true,backendOrigin:audience,gatewayServiceAccount:principal,allowedOrigins:[site],attestationAudience,now,
  getInvokerCredential:()=>({type:'cloud-run-iam-id-token',token:iam,principal,audience,expiresAtMs:clock+60000}),
  getGatewayAttestation:({audience:a})=>{attestCalls++;assert.equal(a,attestationAudience);return {token:token(),principal,audience:a,expiresAtMs:clock+60000};},
  fetchBackend:(url,init)=>{dispatches++;const h=new Headers(init.headers);assert.equal(h.get('x-serverless-authorization'),'Bearer '+iam);assert.notEqual(h.get(header),iam);
   // Simulate platform forwarding only. This test does NOT verify real IAM.
   h.set('x-serverless-authorization','Bearer cloud.payload.');return backend.fetch(new Request(url,{...init,headers:h}));}};
 const gateway=createAttestedMarketplaceGateway(options);
 const browser=(auth=firebase,extra={})=>new Request(site+'/api/staging/marketplace/owner',{method:'POST',headers:{origin:site,'content-type':'application/json',...(auth?{authorization:'Bearer '+auth}:{}),...extra},body:JSON.stringify({kind:'product',id:'p',requestId:null})});
 const r=await gateway.fetch(browser());assert.equal(r.status,200);assert.equal(authCalls,1);assert.equal(r.headers.has(header),false);assert.equal(r.headers.has('x-serverless-authorization'),false);
 user='other';assert.equal((await gateway.fetch(browser())).status,403);
 assert.equal((await gateway.fetch(browser('invalid.user.signature'))).status,401);
 assert.equal((await gateway.fetch(browser(null))).status,401);
 const before=[authCalls,attestCalls,dispatches];assert.equal((await gateway.fetch(browser(firebase,{[header]:token()}))).status,403);assert.deepEqual([authCalls,attestCalls,dispatches],before);
 const direct=new Request(audience+'/api/staging/marketplace/owner',{method:'POST',headers:{'content-type':'application/json',authorization:'Bearer '+firebase,'x-serverless-authorization':'Bearer cloud.payload.'},body:'{}'});
 assert.equal((await backend.fetch(direct)).status,403);
 const bad=createAttestedMarketplaceGateway({...options,getGatewayAttestation:()=>({token:token(claims,undefined,wrong.privateKey),principal,audience:attestationAudience,expiresAtMs:clock+60000})});
 const n=authCalls;assert.equal((await bad.fetch(browser())).status,403);assert.equal(authCalls,n);
});
test('attested source factories stay OFF or fail closed without real trusted provider configuration',async()=>{
 const request=new Request(audience+'/api/staging/marketplace/list',{method:'POST',body:'{}'});
 assert.equal((await createAttestedMarketplaceGateway().fetch(request)).status,503);
 assert.equal((await createAttestedStagingMarketplaceHost().fetch(request)).status,503);
 let bypass=0;const host=createAttestedStagingMarketplaceHost({enabled:true,audience,gatewayServiceAccount:principal,verifyInvoker:()=>{bypass++;return {verified:true};},attestation:{...config,resolvePublicKey:null}});
 assert.equal((await host.fetch(request)).status,503);assert.equal(bypass,0);
 assert.equal((await createAttestedMarketplaceGateway({enabled:true,attestationAudience}).fetch(request)).status,503);
});
