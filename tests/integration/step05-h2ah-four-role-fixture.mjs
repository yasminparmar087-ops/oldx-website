// TEST ONLY: ephemeral local keys, SDK-shaped DB/Auth/KMS; never hosted evidence.
import {generateKeyPairSync,sign} from 'node:crypto';
import {AsyncLocalStorage} from 'node:async_hooks';
import {createServer} from 'node:http';
import {once} from 'node:events';
import {fork} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {createFourRoleAuthority,ROLES,canonical,sha} from '../../functions/staging-marketplace/four-role/contract.mjs';
import {createFourRoleProtocol,readBytes} from '../../functions/staging-marketplace/four-role/protocol.mjs';
import {createFourRoleServer} from '../../functions/staging-marketplace/four-role/server.mjs';
import {createFourRoleRuntime} from '../../functions/staging-marketplace/four-role/bindings.mjs';
import {createBackendLedgerRpc} from '../../functions/staging-marketplace/four-role/ledger-rpc.mjs';
import {createC2H2LifecycleStageLedger,createC2H2RemoteLifecycleStageLedger} from '../../scripts/c2-h2-lifecycle-stage-ledger.mjs';
import {createC2H2MultiSignLifecyclePolicy,C2_H2_LIFECYCLE_REVIEW_SCOPE as scope} from '../../scripts/c2-h2-lifecycle-signing-status-contract.mjs';
import {createC2H2LifecycleApprovalVerifier} from '../../scripts/c2-h2-lifecycle-approval.mjs';
import {createStagingMarketplaceBinding} from '../../scripts/staging-marketplace-context.mjs';
import {createStagingMarketplaceGuestRate} from '../../scripts/staging-marketplace-guest-rate.mjs';
import {parseMarketplaceCanonicalProofPayload} from '../../scripts/marketplace-gateway-request-proof.mjs';
import {H2S_VERSION,H2S_VERSION_URL,H2S_PUBLIC_URL} from '../../scripts/c2-h2-independent-kms-version-status.mjs';
import {c2Crc32c} from '../../scripts/c2-kms-request-signing.mjs';
import {lifecycleHttpFixture,baseTime,profile,seller,buyer} from './step05-lifecycle-http-fixture.mjs';
export {baseTime,profile,seller,buyer};
export const h=x=>sha(JSON.stringify(x));
export function makeProposal(){
 return {v:1,purpose:scope.purpose,projectId:scope.projectId,databaseId:scope.databaseId,runId:'batch',
 gatewayEmail:scope.gatewayEmail,gatewayUid:scope.gatewayUid,keyVersion:scope.keyVersion,keyPublicSpkiSha256:scope.keyPublicSpkiSha256,
 mode:'one-server-held-kms-grant',signAttempts:1,startsAtMs:baseTime-100,expiresAtMs:baseTime+600000,
 actors:{seller,buyer},approvalSha256:h('approval'),runNonceSha256:h('run'),
 phaseNonceSha256:Object.fromEntries(scope.phases.map(p=>[p,h(p)])),phases:[...scope.phases],
 limits:{maxRequests:20,maxActors:2,maxProducts:1,maxPhotos:1},grantServerOnly:true,
 legacyOneSignTombstoneImmutable:true,durableStageLedgerRequired:true};
}
export function makeCrypto(){
 const controller=generateKeyPairSync('rsa',{modulusLength:2048}),google=generateKeyPairSync('rsa',{modulusLength:2048});
 const proposal=makeProposal(),policy=createC2H2MultiSignLifecyclePolicy({enabled:true,proposal,mode:'bounded-per-request-multisign-v1',maxSignAttempts:6});
 const pub=controller.publicKey.export({type:'spki',format:'pem'}),pin=sha(controller.publicKey.export({type:'spki',format:'der'}));
 const approveBytes=Buffer.from(JSON.stringify({v:1,purpose:'oldx.c2.independent.multisign.approval.v1',
 policyDigest:h(policy),mode:policy.mode,maxSignAttempts:6,startsAtMs:policy.startsAtMs,expiresAtMs:policy.expiresAtMs}));
 const lifecycleApproval={publicKeyPem:pub,publicKeySha256:pin,envelope:{payload:approveBytes.toString('base64url'),
 signature:sign('RSA-SHA256',approveBytes,controller.privateKey).toString('base64url')}};
 const facts=Object.fromEntries(Object.entries(ROLES).map(([role,p],i)=>[role,{...p,
 image:'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/'+p.imageName+'@sha256:'+String(i+3).repeat(64),
 origin:'https://'+role+'.region.run.app',revision:role+'-h2ah-00001',attachmentEvidenceSha256:h(role)}]));
 const configuration={v:1,purpose:'oldx.h2ah.four-private-hosts.v1',projectId:'oldx-staging',databaseId:'(default)',
 sourceRevision:'a'.repeat(40),policyDigest:h(policy),releaseDigest:h('release'),lifecycleApprovalKeySha256:pin,
 startsAtMs:policy.startsAtMs,expiresAtMs:policy.expiresAtMs,roles:facts,
 network:{ingress:'internal',vpcEgress:'all-traffic',privateGoogleAccess:true,
 vpc:'projects/oldx-staging/global/networks/test-vpc',subnet:'projects/oldx-staging/regions/asia-south1/subnetworks/test-subnet'}};
 const authorityOptions=(patch={})=>{const c={...configuration,...patch},bytes=Buffer.from(canonical(c));
 return {configuration:c,controllerPublicKeyPem:pub,controllerSpkiSha256:pin,
 envelope:{payload:bytes.toString('base64url'),signature:sign('RSA-SHA256',bytes,controller.privateKey).toString('base64url')}};};
 const authority=createFourRoleAuthority({enabled:true,...authorityOptions(),now:()=>baseTime});
 const mint=(email,sub,aud)=>{const enc=x=>Buffer.from(JSON.stringify(x)).toString('base64url'),
 data=enc({alg:'RS256',kid:'four-role-google'})+'.'+enc({iss:'https://accounts.google.com',email,sub,aud,
 email_verified:true,iat:baseTime/1000,exp:baseTime/1000+3600});
 return data+'.'+sign('RSA-SHA256',Buffer.from(data),google.privateKey).toString('base64url');};
 const googleJwk={...google.publicKey.export({format:'jwk'}),alg:'RS256',kid:'four-role-google',use:'sig'};
 const keys=async()=>Response.json({keys:[googleJwk]},{headers:{'cache-control':'max-age=300'}});
 const metadata=(role,uid=ROLES[role].uid)=>async url=>new Response(
 mint(ROLES[role].principal,uid,new URL(url).searchParams.get('audience')),
 {headers:{'Metadata-Flavor':'Google'}});
 const protocol=(role,fetchPrivate,uid)=>createFourRoleProtocol({enabled:true,authority,role,
 fetchMetadata:metadata(role,uid),fetchGoogleKeys:keys,fetchPrivate,now:()=>baseTime});
 return {controller,google,proposal,policy,lifecycleApproval,facts,configuration,authorityOptions,authority,mint,keys,googleJwk,metadata,protocol};
}
export function message(child,type){
 return new Promise((resolve,reject)=>{
 const timeout=setTimeout(()=>{cleanup();reject(Error('CHILD_TIMEOUT_'+type));},6000);
 const receive=m=>{if(m.type===type){cleanup();resolve(m);}else if(m.type==='failed'){cleanup();reject(Error('CHILD_FAILED'));}};
 const exit=()=>{cleanup();reject(Error('CHILD_EXIT'));};
 function cleanup(){clearTimeout(timeout);child.off('message',receive);child.off('exit',exit);}
 child.on('message',receive);child.once('exit',exit);
 });
}
export async function createFourRoleFixture({readerUid}={}){
 const ownedServers=[];let ownedChild;
 try{
 const c=makeCrypto(),scopeContext=new AsyncLocalStorage(),servers=ownedServers,addresses={},protocols={};let signs=0;
 const durable=lifecycleHttpFixture({wire:()=>{throw Error('UNIT_ONLY');}});
 const binding=createStagingMarketplaceBinding(durable.options.runtimeOptions);
 const verifyLifecycleApproval=createC2H2LifecycleApprovalVerifier({enabled:true,policy:c.policy,...c.lifecycleApproval,now:()=>baseTime});
 const ledger=createC2H2LifecycleStageLedger({enabled:true,binding,policy:c.policy,verifyLifecycleApproval,now:()=>baseTime});
 const relay=async(url,init)=>{
 const role=Object.keys(c.facts).find(r=>c.facts[r].origin===new URL(url).origin);
 if(!addresses[role])throw Error('NO_TEST_ROUTE');
 const headers=new Headers(init.headers),iam=headers.get('x-serverless-authorization');
 if(iam)headers.set('x-serverless-authorization',iam.split('.').slice(0,2).join('.')+'.');
 const response=await fetch(addresses[role]+new URL(url).pathname,{...init,headers});
 return new Response(await response.arrayBuffer(),{status:response.status,headers:response.headers});
 };
 for(const role of ['mediator','gateway','backend'])protocols[role]=c.protocol(role,relay);
 const remoteGateway=createC2H2RemoteLifecycleStageLedger({enabled:true,policy:c.policy,protocol:protocols.gateway});
 const pins={website:{...c.facts.mediator,audience:'urn:oldx:h2ah:mediator'},
 gateway:{...c.facts.gateway,audience:'urn:oldx:h2ah:gateway'},backend:c.facts.backend};
 const statusReads=async()=>{
 const ctx=scopeContext.getStore(),role=ctx.role,usage=role==='gateway'?'sign':'verify';
 for(const [kind,url]of [['version',H2S_VERSION_URL],['public',H2S_PUBLIC_URL]]){
 const response=await protocols[role].send('reader','/internal/key-status',Buffer.from(JSON.stringify({name:H2S_VERSION,url})),
 {operation:usage+'-'+kind,reservation:ctx.reservation,phase:ctx.phase});
 if(response.status!==200)throw Error('READER_TEST_DENIED');
 const value=await response.json();if(value.name!==H2S_VERSION)throw Error('WRONG_TEST_KEY');
 }
 // Fixture intent signer independently checks its generated local RSA key.
 // This is NOT a successful match against the real historical SPKI pin.
 };
 const app=lifecycleHttpFixture({pins,googleProvider:{mint:c.mint,keys:c.keys},lifecycle:{policy:c.policy,ledger},
 wire:async(_origin,_target,request)=>{
 const ctx=scopeContext.getStore();return protocols.gateway.send('backend',new URL(request.url).pathname,
 new Uint8Array(await request.arrayBuffer()),{...ctx,operation:'product',headers:request.headers});
 },
 onSign:async bytes=>{
 const p=parseMarketplaceCanonicalProofPayload(bytes),ctx=scopeContext.getStore();
 const result=await remoteGateway.claimSign({reservation:ctx.reservation,proofSha256:sha(bytes),bodyHash:p.bodyHash,authHash:p.authHash,path:p.path});
 if(!result.allowed)throw Error('SIGN_REPLAY');signs++;
 },onStatus:statusReads});
 const guest=createStagingMarketplaceGuestRate({enabled:true,binding,policy:{windowMs:600000,guestLimit:20,globalLimit:20},now:()=>baseTime});
 const ledgerRpc=createBackendLedgerRpc({policy:c.policy,ledger,protocol:protocols.backend,guestAdmission:guest,now:()=>baseTime});
 const start=async(role,fetchHandler)=>{
 const server=createFourRoleServer({role,runtime:{ready:true,origin:c.facts[role].origin,fetch:fetchHandler}});
 server.listen(0,'127.0.0.1');await once(server,'listening');servers.push(server);
 addresses[role]='http://127.0.0.1:'+server.address().port;
 };
 await start('backend',async request=>{
 if(new URL(request.url).pathname==='/internal/ledger')return ledgerRpc(request);
 const ctx=await protocols.backend.receive(request,{fromRoles:['gateway'],path:new URL(request.url).pathname});
 return scopeContext.run({...ctx,role:'backend'},()=>app.backend.fetch(new Request(request.url,
 {method:'POST',headers:request.headers,body:ctx.body,signal:request.signal})));
 });
 await start('gateway',async request=>{
 const ctx=await protocols.gateway.receive(request,{fromRoles:['mediator'],path:new URL(request.url).pathname});
 return scopeContext.run({...ctx,role:'gateway'},()=>app.gatewayHost.fetch(new Request(request.url,
 {method:'POST',headers:request.headers,body:ctx.body,signal:request.signal})));
 });
 const child=ownedChild=fork(fileURLToPath(new URL('./step05-h2ah-reader-child-fixture.mjs',import.meta.url)),
 {stdio:['ignore','ignore','pipe','ipc']});
 const ready=message(child,'ready');
 const publicKey=generateKeyPairSync('rsa',{modulusLength:2048}).publicKey.export({type:'spki',format:'pem'});
 child.send({type:'start',configuration:{clock:baseTime,readerUid,proposal:c.proposal,
 authority:c.authorityOptions(),googlePrivateKeyPem:c.google.privateKey.export({type:'pkcs8',format:'pem'}),
 googleJwk:c.googleJwk,backendAddress:addresses.backend,
 versionValue:{name:H2S_VERSION,state:'ENABLED',algorithm:'RSA_SIGN_PKCS1_2048_SHA256',protectionLevel:'SOFTWARE'},
 publicValue:{name:H2S_VERSION,pem:publicKey,pemCrc32c:c2Crc32c(Buffer.from(publicKey)),algorithm:'RSA_SIGN_PKCS1_2048_SHA256',protectionLevel:'SOFTWARE'}}});
 const info=await ready;addresses.reader='http://127.0.0.1:'+info.port;
 const nativeSdk={initializeApp:options=>({options}),getAuth:()=>app.adminAuth,deleteApp:async()=>{}};
 const mediator=await createFourRoleRuntime({enabled:true,role:'mediator',authority:c.authority,
 configuration:{proposal:c.proposal},fetchMetadata:c.metadata('mediator'),fetchGoogleKeys:c.keys,
 fetchPrivate:relay,fetchKms:()=>{throw Error('MEDIATOR_CANNOT_KMS');},sdkLoader:async()=>nativeSdk,now:()=>baseTime});
 await start('mediator',request=>mediator.fetch(request));
 const counts=async()=>{const wait=message(child,'counts');child.send({type:'counts'});return wait;};
 const mode=async value=>{const wait=message(child,'mode');child.send({type:'mode',mode:value});await wait;};
 const reserve=async()=>{
 const result=await ledger.reserve({phase:'seller-save',actor:seller,nonceSha256:c.policy.phases[0].nonceSha256,
 requestSha256:h('body'),sessionSha256:h('session'),authSha256:h('auth')});
 await ledger.claimSign({reservation:result.reservation,proofSha256:h('proof'),bodyHash:h('body'),authHash:h('auth'),path:'/api/staging/marketplace/save'});
 return result.reservation;
 };
 return {c,ledger,durable,app,protocols,addresses,readerPid:info.pid,reserve,counts,mode,
 get signs(){return signs;},
 async close(){
 const done=once(child,'exit');child.send({type:'stop'});await done;
 for(const s of servers){s.closeAllConnections();await new Promise(r=>s.close(r));}
 await mediator.close();app.integration.destroy();durable.integration.destroy();
 }};
 }catch(error){
 ownedChild?.kill('SIGTERM');
 for(const server of ownedServers){server.closeAllConnections();await new Promise(r=>server.close(r));}
 throw error;
 }
}
