import test from 'node:test';
import assert from 'node:assert/strict';
import {generateKeyPairSync,sign,constants} from 'node:crypto';
import {createC2WebsiteMediator,createC2PrivateGatewayHost,MEDIATED_ORIGIN_HEADER} from '../../functions/staging-marketplace/c2-website-mediation.mjs';
import {createStep05Backend} from '../../functions/staging-marketplace/secure-product-pipeline.mjs';
import {createMarketplaceHttpTransport} from '../../features/marketplace/http-transport.mjs';
import {createAuthenticatedMarketplaceCommands} from '../../features/marketplace/authenticated-command-client.mjs';
import {createMarketplacePublicClient} from '../../features/marketplace/public-read-client.mjs';
import {prepareC2SyntheticCleanupManifest} from '../../scripts/c2-synthetic-cleanup-manifest.mjs';
import {STAGING_MARKETPLACE_COLLECTIONS as c,STAGING_RATE_COLLECTION} from '../../scripts/staging-marketplace-context.mjs';
import {fakeFirestoreSdk} from './fake-firestore-sdk.mjs';
const key=generateKeyPairSync('rsa',{modulusLength:2048}),intent=generateKeyPairSync('rsa',{modulusLength:2048});
const site='https://website.invalid',gateway='https://gateway.invalid',backendOrigin='https://backend.invalid';
const websiteSa='website-mediator@oldx-staging.iam.gserviceaccount.com',gatewaySa='gateway-only@oldx-staging.iam.gserviceaccount.com';
const issuer='https://accounts.google.com',webAudience='urn:test:website-mediation',appAudience='urn:test:gateway-attestation';
const clock=1800000000000,now=()=>clock;
const profile={title:'ગુજરાતી हिन्दी',description:'Synthetic',category:'cars',locationLabel:'Sample',basePrice:1,isSold:false,storeId:null,photos:[]};
function jwt(email,sub,aud,overrides={}){
 const enc=v=>Buffer.from(JSON.stringify(v)).toString('base64url'),input=enc({alg:'RS256',kid:'google-fixture'})+'.'+enc({iss:issuer,aud,email,sub,email_verified:true,iat:clock/1000,exp:clock/1000+3600,...overrides});
 return input+'.'+sign('RSA-SHA256',Buffer.from(input),{key:key.privateKey,padding:constants.RSA_PKCS1_PADDING}).toString('base64url');
}
function fixture(){
 const f=fakeFirestoreSdk();let identityPatch={},lose=false,guestAllowed=true,credentialCalls=0,admissions=0,authCalls=0;
 const wires=[];
 function collection(name){
  const constraints=[];let fields;
  const q={doc:id=>({...f.sdk.doc(f.db,name,id),get:async()=>{const r=await f.sdk.getDocFromServer(f.sdk.doc(f.db,name,id));return {exists:r.exists(),data:r.data};}}),select(...v){fields=v;return q;},where(...v){constraints.push(f.sdk.where(...v));return q;},orderBy(...v){constraints.push(f.sdk.orderBy(...v));return q;},startAfter(v){constraints.push(f.sdk.startAfter(v));return q;},limit(v){constraints.push(f.sdk.limit(v));return q;},async get(){const r=await f.sdk.getDocsFromServer(f.sdk.query(f.sdk.collection(f.db,name),...constraints));return {docs:r.docs.map(d=>({id:d.id,data:()=>Object.fromEntries(Object.entries(d.data()).filter(([k])=>!fields||fields.includes(k)))}))};}};return q;
 }
 const db={projectId:'oldx-staging',databaseId:'(default)',collection,runTransaction:(work,opts)=>f.sdk.runTransaction(f.db,tx=>work({get:async ref=>{const s=await tx.get(ref);return {exists:s.exists(),data:s.data};},set:(...v)=>tx.set(...v),delete:(...v)=>tx.delete(...v)}),opts)};
 const auth={app:{options:{projectId:'oldx-staging'}},verifyIdToken:async(token,revoked)=>{authCalls++;assert.equal(revoked,true);const uid=token.split('.')[0];if(!['seller','buyer'].includes(uid))throw Error('Invalid user');return {uid,sub:uid,aud:'oldx-staging',iss:'https://securetoken.google.com/oldx-staging',iat:clock/1000,exp:clock/1000+3600};}};
 for(const uid of ['seller','buyer'])f.seed(c.actors,uid,{uid,canWrite:true,canPublish:true,suspended:false});f.seed(c.generations,'current',{value:0});
 const fetchKeys=async(url,init)=>{assert.equal(url,'https://www.googleapis.com/oauth2/v3/certs');assert.equal(init.redirect,'error');return Response.json({keys:[{...key.publicKey.export({format:'jwk'}),alg:'RS256',kid:'google-fixture',use:'sig'}]},{headers:{'cache-control':'max-age=300'}});};
 const backend=createStep05Backend({enabled:true,audience:backendOrigin,gatewayServiceAccount:gatewaySa,googleIdentity:{identityType:'google-service-account',issuer,attestationAudience:appAudience,expectedSubject:'222',fetchRequest:fetchKeys},requestVerification:{resolvePublicKey:({kid})=>kid==='intent-key'?intent.publicKey:null},runtimeOptions:{projectId:'oldx-staging',deploymentEnvironment:'preview',adminFirestore:db,adminAuth:auth,FieldValue:{serverTimestamp:f.sdk.serverTimestamp},ratePolicy:{windowMs:60000,actorLimit:50,globalLimit:100}},guestPolicy:{windowMs:60000,guestLimit:10,globalLimit:20},cursorKey:new Uint8Array(32).fill(33),now});
 const gatewayOptions={backendOrigin,gatewayServiceAccount:gatewaySa,attestationAudience:appAudience,
  getInvokerCredential:()=>({type:'cloud-run-iam-id-token',token:'backend.iam.signature',principal:gatewaySa,audience:backendOrigin,expiresAtMs:clock+60000}),
  getGatewayAttestation:()=>({token:jwt(gatewaySa,'222',appAudience),principal:gatewaySa,audience:appAudience,expiresAtMs:clock+60000}),
  requestSigning:{kid:'intent-key',signMessage:bytes=>sign('RSA-SHA256',bytes,{key:intent.privateKey,padding:constants.RSA_PKCS1_PADDING})},
  fetchBackend:async(url,init)=>{const headers=new Headers(init.headers);wires.push({headers:new Headers(headers),body:new Uint8Array(init.body)});assert.equal(headers.get('x-serverless-authorization'),'Bearer backend.iam.signature');headers.set('x-serverless-authorization','Bearer backend.payload.');return backend.fetch(new Request(url,{...init,headers}));}};
 const hostOptions={enabled:true,privateGatewayOrigin:gateway,mediatorPrincipal:websiteSa,websiteIdentity:{identityType:'google-service-account',issuer,attestationAudience:webAudience,expectedSubject:'111',fetchRequest:fetchKeys},allowedOrigins:[site],gatewayOptions,now};
 const host=createC2PrivateGatewayHost(hostOptions);
 const mediatorOptions={enabled:true,websiteOrigin:site,allowedOrigins:[site],privateGatewayOrigin:gateway,mediatorPrincipal:websiteSa,mediationAudience:webAudience,now,
  consumeGuestAdmission:(_input,ctx)=>{admissions++;assert.equal(ctx.deadlineAt,clock+5000);return {allowed:guestAllowed};},
  getGatewayInvokerCredential:()=>{credentialCalls++;return {type:'cloud-run-iam-id-token',token:'website.iam.signature',principal:websiteSa,audience:gateway,expiresAtMs:clock+60000};},
  getWebsiteAttestation:()=>({token:jwt(websiteSa,'111',webAudience,identityPatch),principal:websiteSa,audience:webAudience,expiresAtMs:clock+60000}),
  fetchPrivateGateway:async(url,init)=>{const h=new Headers(init.headers);assert.equal(h.get('x-serverless-authorization'),'Bearer website.iam.signature');h.set('x-serverless-authorization','Bearer website.payload.');const response=await host.fetch(new Request(url,{...init,headers:h}));if(lose){lose=false;throw Error('Lost response');}return response;}};
 const mediator=createC2WebsiteMediator(mediatorOptions);
 const browser=(op,body,token=null,extra={})=>new Request(site+'/api/staging/marketplace/'+op,{method:'POST',headers:{origin:site,'content-type':'application/json',...(token?{authorization:'Bearer '+token}:{}),...extra},body:JSON.stringify(body)});
 const transport=createMarketplaceHttpTransport({enabled:true,origin:site,fetchRequest:(url,init)=>mediator.fetch(new Request(url,{...init,headers:{...init.headers,origin:site}}))});
 const command=createAuthenticatedMarketplaceCommands({enabled:true,getToken:scope=>({...scope,token:scope.uid+'.test.token'}),sendCommand:transport.sendCommand}),reads=createMarketplacePublicClient({enabled:true,sendRead:transport.sendRead});
 const seedPublic=()=>{const {photos,...fields}=profile,row={id:'public-p',kind:'product',revision:1,...fields};f.seed(c.publicViews,'product_public-p',row);f.seed(c.privateRecords,'product_public-p',{id:'public-p',kind:'product',revision:1,ownerUid:'seller',published:true,publicationRevision:1,publicProfile:row,profile,privateContact:'private'});};
 return {f,wires,host,mediator,hostOptions,mediatorOptions,browser,command,reads,seedPublic,
  badIdentity:patch=>identityPatch=patch,lose:()=>lose=true,blockGuests:()=>guestAllowed=false,
  get admissions(){return admissions;},get credentialCalls(){return credentialCalls;},get authCalls(){return authCalls;}};
}
const input={id:null,expectedRevision:0,publication:'draft',profile,requestId:'same-request'},seller={session:{uid:'seller',sessionId:'seller-session'}};
test('new website/private-Gateway boundary composes actual signatures, seller ownership and guest public projection',async()=>{
 const x=fixture(),saved=await x.command.save(input,seller);assert.equal(saved.ok,true);
 const id=saved.id;assert.equal((await x.command.owner({kind:'product',id,requestId:null},seller)).ok,true);
 assert.equal((await x.command.owner({kind:'product',id,requestId:null},{session:{uid:'buyer',sessionId:'buyer-session'}})).code,'DENIED');
 x.seedPublic();const page=await x.reads.list({kind:'product',limit:12,category:'',storeId:null,cursor:null});assert.equal(page.ok,true);assert.equal(page.items[0].id,'public-p');assert.doesNotMatch(JSON.stringify(page),/ownerUid|privateContact|photos/);
 assert.equal((await x.reads.detail({kind:'product',id:'public-p'})).ok,true);
 assert.equal(x.admissions,2);assert.equal(x.wires.at(-1).headers.get('authorization'),null);
 assert.ok(x.wires.every(w=>w.headers.get(MEDIATED_ORIGIN_HEADER)===null));
});
test('default OFF and every mandatory mediator/host provider gap return503 without credentials/store work',async()=>{
 const x=fixture(),req=x.browser('list',{kind:'product',limit:12,category:'',storeId:null,cursor:null});
 assert.equal((await createC2WebsiteMediator().fetch(req)).status,503);assert.equal((await createC2PrivateGatewayHost().fetch(req)).status,503);
 for(const patch of [{consumeGuestAdmission:null},{getGatewayInvokerCredential:null},{getWebsiteAttestation:null},{fetchPrivateGateway:null},{allowedOrigins:[]},{privateGatewayOrigin:null}]){
  assert.equal((await createC2WebsiteMediator({...x.mediatorOptions,...patch}).fetch(req)).status,503);
 }
 for(const patch of [{websiteIdentity:null},{gatewayOptions:null},{allowedOrigins:[]},{mediatorPrincipal:null},{gatewayOptions:{...x.hostOptions.gatewayOptions,requestSigning:{}}}]){
  assert.equal((await createC2PrivateGatewayHost({...x.hostOptions,...patch}).fetch(req)).status,503);
 }
 assert.equal(x.credentialCalls,0);assert.equal(x.f.commits,0);
});
test('unmediated anonymous/Firebase-only caller cannot invoke private host; browser privileged headers fail before providers',async()=>{
 const x=fixture();
 for(const headers of [{},{authorization:'Bearer seller.test.token'},{'x-serverless-authorization':'Bearer website.payload.',[MEDIATED_ORIGIN_HEADER]:site},{'x-serverless-authorization':'Bearer website.payload.',[MEDIATED_ORIGIN_HEADER]:site,'x-oldx-gateway-attestation':'fake.claims.signature'}]){
  const r=await x.host.fetch(new Request(gateway+'/api/staging/marketplace/list',{method:'POST',headers,body:'{}'}));assert.equal(r.status,403);
 }
 for(const h of ['x-serverless-authorization','x-oldx-gateway-attestation','x-oldx-gateway-request-proof','x-oldx-gateway-nonce',MEDIATED_ORIGIN_HEADER]){
  assert.equal((await x.mediator.fetch(x.browser('save',input,'seller.test.token',{[h]:'forged'}))).status,403);
 }
 assert.equal(x.credentialCalls,0);assert.equal(x.authCalls,0);assert.equal(x.f.commits,0);
});
test('wrong website origin, signed audience/principal/subject and guest quota fail closed',async()=>{
 const x=fixture();assert.equal((await x.mediator.fetch(x.browser('list',{},null,{origin:'https://foreign.invalid'}))).status,403);assert.equal(x.credentialCalls,0);
 for(const patch of [{aud:appAudience},{email:gatewaySa},{sub:'222'},{iss:'https://foreign.invalid'}]){
  const y=fixture();y.badIdentity(patch);assert.equal((await y.mediator.fetch(y.browser('save',input,'seller.test.token'))).status,403);assert.equal(y.f.commits,0);assert.equal(y.authCalls,0);
 }
 x.blockGuests();assert.equal((await x.reads.list({kind:'product',limit:12,category:'',storeId:null,cursor:null})).code,'RATE_LIMITED');assert.equal(x.credentialCalls,0);
});
test('mediation lost-result retry keeps requestId with fresh final proof/nonce; cancellation never acquires credentials',async()=>{
 const x=fixture();x.lose();assert.equal((await x.command.save(input,seller)).code,'OUTCOME_UNKNOWN');
 const retry=await x.command.save(input,seller);assert.equal(retry.ok,true);assert.deepEqual(x.wires[0].body,x.wires[1].body);assert.notEqual(x.wires[0].headers.get('x-oldx-gateway-request-proof'),x.wires[1].headers.get('x-oldx-gateway-request-proof'));
 assert.equal([...x.f.snapshot()].filter(([p])=>p.startsWith(c.privateRecords+'/')).length,1);
 const y=fixture(),aborted=new Request(y.browser('list',{}),{signal:AbortSignal.abort()});assert.equal((await y.mediator.fetch(aborted)).status,503);assert.equal(y.credentialCalls,0);assert.equal(y.f.commits,0);
});
test('synthetic cleanup plan is bounded draft only; shared nonce/generation/foreign records never approved',()=>{
 const runId='run1',uid='synthetic-c2-run1-seller';
 const config={enabled:true,projectId:'oldx-staging',databaseId:'(default)',runId,actors:[uid],records:[{path:c.privateRecords+'/product_synthetic',ownerUid:uid,runId,updateTime:'2026-11-24T00:00:00.123456789Z'}]};
 const plan=prepareC2SyntheticCleanupManifest(config);assert.equal(plan.decision,'DRAFT_ONLY');assert.equal(plan.authorized,false);config.records[0].path='changed';assert.notEqual(plan.records[0].path,'changed');
 assert.equal(prepareC2SyntheticCleanupManifest().decision,'STOP');
 for(const path of [STAGING_RATE_COLLECTION+'/'+'a'.repeat(64),c.generations+'/current','products/real',c.actors+'/real',c.privateRecords+'/store_real']){
  assert.equal(prepareC2SyntheticCleanupManifest({...config,records:[{...plan.records[0],path}]}).decision,'STOP');
 }
 assert.equal(prepareC2SyntheticCleanupManifest({...config,projectId:'oldx-1c983'}).decision,'STOP');
});

test('website identity expiring during token/signing work cannot reach backend; malformed guests do not consume quota',async()=>{
 const x=fixture();let time=clock,forwards=0;
 const host=createC2PrivateGatewayHost({...x.hostOptions,now:()=>time,gatewayOptions:{...x.hostOptions.gatewayOptions,
  getInvokerCredential:()=>{time+=61000;return {type:'cloud-run-iam-id-token',token:'backend.iam.signature',principal:gatewaySa,audience:backendOrigin,expiresAtMs:time+60000};},
  getGatewayAttestation:()=>({token:jwt(gatewaySa,'222',appAudience),principal:gatewaySa,audience:appAudience,expiresAtMs:time+60000}),
  fetchBackend:()=>{forwards++;throw Error('must not forward expired identity');}
 }});
 const request=new Request(gateway+'/api/staging/marketplace/save',{method:'POST',headers:{'content-type':'application/json',authorization:'Bearer seller.test.token','x-serverless-authorization':'Bearer website.payload.','x-oldx-gateway-attestation':jwt(websiteSa,'111',webAudience),[MEDIATED_ORIGIN_HEADER]:site},body:JSON.stringify(input)});
 assert.equal((await host.fetch(request)).status,202);assert.equal(forwards,0);assert.equal(x.f.commits,0);
 assert.equal((await x.mediator.fetch(x.browser('list',{},null,{'content-type':'text/plain'}))).status,415);
 assert.equal((await x.mediator.fetch(x.browser('list',{},null,{'cookie':'untrusted'}))).status,403);assert.equal(x.admissions,0);
 let getters=0;
 const row={path:c.privateRecords+'/product_synthetic',ownerUid:'synthetic-c2-run1-seller',updateTime:'2026-11-24T00:00:00Z',get runId(){getters++;return 'run1';}};
 assert.equal(prepareC2SyntheticCleanupManifest({enabled:true,projectId:'oldx-staging',databaseId:'(default)',runId:'run1',actors:['synthetic-c2-run1-seller'],records:[row]}).decision,'STOP');assert.equal(getters,0);
});
