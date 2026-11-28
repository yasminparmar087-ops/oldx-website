import test from 'node:test';
import assert from 'node:assert/strict';
import {fork} from 'node:child_process';
import {once} from 'node:events';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire,registerHooks,syncBuiltinESMExports} from 'node:module';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {createFourRoleAuthority,ROLES,sha} from '../../functions/staging-marketplace/four-role/contract.mjs';
import {createFourRoleServer} from '../../functions/staging-marketplace/four-role/server.mjs';
import {createFourRoleProtocol,CONTEXT,ASSERTION} from '../../functions/staging-marketplace/four-role/protocol.mjs';
import {createFourRoleRuntime} from '../../functions/staging-marketplace/four-role/bindings.mjs';
import {bootstrapFourRole} from '../../functions/staging-marketplace/four-role/bootstrap.mjs';
import {createFirebaseNativeBindings} from '../../functions/staging-marketplace/four-role/firebase-native.mjs';
import {createRemoteReaderStatus} from '../../functions/staging-marketplace/four-role/remote-status.mjs';
import {collectFourRoleClosure} from '../../scripts/step05-h2ah-source-package.mjs';
import {H2S_VERSION,H2S_VERSION_URL} from '../../scripts/c2-h2-independent-kms-version-status.mjs';
import {makeCrypto,createFourRoleFixture,message,baseTime,profile,seller,buyer,h} from './step05-h2ah-four-role-fixture.mjs';
const root=fileURLToPath(new URL('../../',import.meta.url));

test('NEW H2AH four executable processes expose OFF health, block Product and terminate',async()=>{
 const children=[];
 try{
 for(const role of Object.keys(ROLES)){
 const child=fork(resolve(root,'functions/staging-marketplace/four-role/'+role+'.mjs'),
 {env:{...process.env,PORT:'0',OLDX_H2AH_ENABLED:'false'},stdio:['ignore','ignore','pipe','ipc']});children.push(child);
 const started=await message(child,'h2ah-listening'),address='http://127.0.0.1:'+started.port;
 assert.equal(started.role,role);assert.notEqual(started.pid,process.pid);
 const health=await fetch(address+'/healthz');assert.equal(health.status,200);
 assert.deepEqual(await health.json(),{ok:true,role,state:'OFF',productReady:false});
 assert.equal((await fetch(address+'/api/staging/marketplace/save',{method:'POST',body:'{}'})).status,503);
 assert.equal((await fetch(address+'/internal/key-status',{method:'POST',body:'{}'})).status,503);
 const exited=once(child,'exit');child.kill('SIGTERM');await exited;
 }
 }finally{for(const child of children)if(child.exitCode===null&&!child.killed)child.kill('SIGTERM');}
 // Windows child termination is not claimed as Linux container graceful SIGTERM.
});
test('NEW H2AH signed host authority rejects boolean trust, forged envelope, UID/image drift and expiry',()=>{
 const c=makeCrypto();
 assert.equal(createFourRoleAuthority({enabled:true,configuration:{authorized:true}}),null);
 assert.equal(createFourRoleAuthority({enabled:true,...c.authorityOptions(),envelope:{signature:'fake',payload:'fake'},now:()=>baseTime}),null);
 for(const role of Object.keys(ROLES)){
 const roles=JSON.parse(JSON.stringify(c.facts));roles[role].uid='123';
 assert.equal(createFourRoleAuthority({enabled:true,...c.authorityOptions({roles}),now:()=>baseTime}),null);
 }
 assert.equal(createFourRoleAuthority({enabled:true,...c.authorityOptions(),now:()=>c.policy.expiresAtMs}),null);
 for(const digest of [c.facts.gateway.image.slice(-64),'49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec']){
 const roles=JSON.parse(JSON.stringify(c.facts));roles.backend.image=roles.backend.image.slice(0,-64)+digest;
 assert.equal(createFourRoleAuthority({enabled:true,...c.authorityOptions({roles}),now:()=>baseTime}),null);
 }
 assert.equal(c.authority.fresh(),true);
});
test('NEW H2AH full Google-signed context denies stripped-header-only, wrong UID, body or audience',async()=>{
 const c=makeCrypto();let captured;
 const gateway=c.protocol('gateway',async(url,init)=>{captured=new Request(url,{...init,signal:undefined});return Response.json({ok:true});});
 const reader=c.protocol('reader',()=>{throw Error('not used');});
 const input=Buffer.from(JSON.stringify({name:H2S_VERSION,url:H2S_VERSION_URL}));
 await gateway.send('reader','/internal/key-status',input,{operation:'sign-version',reservation:h('stage')});
 const original=captured.clone(),valid=await reader.receive(captured,{fromRoles:['gateway'],path:'/internal/key-status'});
 assert.equal(valid.uid,ROLES.gateway.uid);
 const request=async headers=>new Request(original.url,{method:'POST',headers,body:await original.clone().arrayBuffer()});
 const bare=new Headers({'x-serverless-authorization':'Bearer stripped.payload.'});
 await assert.rejects(reader.receive(await request(bare),{fromRoles:['gateway'],path:'/internal/key-status'}));
 const missingIam=new Headers(original.headers);missingIam.delete('x-serverless-authorization');
 await assert.rejects(reader.receive(await request(missingIam),{fromRoles:['gateway'],path:'/internal/key-status'}));
 const expectedAudience='urn:oldx:h2ah:context:'+sha(Buffer.from(original.headers.get(CONTEXT),'base64url'));
 for(const [sub,aud]of [[ROLES.gateway.uid,'urn:foreign'],['123',expectedAudience]]){
 const wrong=new Headers(original.headers);wrong.set(ASSERTION,c.mint(ROLES.gateway.principal,sub,aud));
 await assert.rejects(reader.receive(await request(wrong),{fromRoles:['gateway'],path:'/internal/key-status'}));
 }
 const changed=new Request(original.url,{method:'POST',headers:original.headers,body:'{}'});
 await assert.rejects(reader.receive(changed,{fromRoles:['gateway'],path:'/internal/key-status'}));
 for(const role of ['gateway','backend']){
 const wrongUid=c.protocol(role,async(url,init)=>{captured=new Request(url,{...init,signal:undefined});return Response.json({ok:true});},'123');
 await assert.rejects(wrongUid.send('reader','/internal/key-status',input,
 {operation:role==='gateway'?'sign-version':'verify-version',reservation:h('stage')}));
 }
});
test('NEW H2AH Reader process consumes one durable slot before ambiguous GET, with no retry',async()=>{
 const f=await createFourRoleFixture();
 try{
 assert.notEqual(f.readerPid,process.pid);
 const reservation=await f.reserve();await f.mode('ambiguous');
 const send=()=>f.protocols.gateway.send('reader','/internal/key-status',
 Buffer.from(JSON.stringify({name:H2S_VERSION,url:H2S_VERSION_URL})),{operation:'sign-version',reservation});
 assert.equal((await send()).status,503);assert.equal((await send()).status,503);
 assert.equal((await f.counts()).calls,1);
 assert.equal(f.durable.f.get('marketplaceRateLimits_v1',f.ledger.recordId).statusReads,1);
 }finally{await f.close();}
});
test('NEW H2AH Reader rejects malformed public metadata and never leaks OAuth/provider extras',async()=>{
 const f=await createFourRoleFixture();
 try{
 const reservation=await f.reserve();await f.mode('malformed');
 const response=await f.protocols.gateway.send('reader','/internal/key-status',
 Buffer.from(JSON.stringify({name:H2S_VERSION,url:H2S_VERSION_URL})),{operation:'sign-version',reservation});
 assert.equal(response.status,503);assert.doesNotMatch(await response.text(),/MUST_NEVER_LEAK|access_token|privateKey/);
 assert.equal((await f.counts()).calls,1);
 }finally{await f.close();}
});
test('NEW H2AH wrong Reader attached UID fails before KMS and budget mutation',async()=>{
 const f=await createFourRoleFixture({readerUid:'123'});
 try{
 const reservation=await f.reserve();
 const response=await f.protocols.gateway.send('reader','/internal/key-status',
 Buffer.from(JSON.stringify({name:H2S_VERSION,url:H2S_VERSION_URL})),{operation:'sign-version',reservation});
 assert.equal(response.status,503);assert.equal((await f.counts()).calls,0);
 assert.equal(f.durable.f.get('marketplaceRateLimits_v1',f.ledger.recordId).statusReads,0);
 }finally{await f.close();}
});
test('NEW H2AH missing Reader OAuth consumes slot safely and cannot be refreshed to retry it',async()=>{
 const f=await createFourRoleFixture();
 try{
 const reservation=await f.reserve();await f.mode('missing-token');
 const send=()=>f.protocols.gateway.send('reader','/internal/key-status',
 Buffer.from(JSON.stringify({name:H2S_VERSION,url:H2S_VERSION_URL})),{operation:'sign-version',reservation});
 assert.equal((await send()).status,503);await f.mode('normal');assert.equal((await send()).status,503);
 assert.equal((await f.counts()).calls,0);
 }finally{await f.close();}
});
test('NEW H2AH exact real SPKI pin remains blocked despite well-formed synthetic Reader key',async()=>{
 const f=await createFourRoleFixture();
 try{
 const reservation=await f.reserve();
 const status=createRemoteReaderStatus({protocol:f.protocols.gateway,getStageContext:()=>({reservation,phase:'seller-save'})});
 await assert.rejects(status({name:H2S_VERSION}),/PIN_UNVERIFIED/);
 assert.equal((await f.counts()).calls,2);
 // New client cannot refresh the same durable slots.
 await assert.rejects(status({name:H2S_VERSION}));assert.equal((await f.counts()).calls,2);
 }finally{await f.close();}
});
test('NEW H2AH six Seller-Buyer stages cross four HTTP roles with Reader in a separate process and 24 GET slots',async()=>{
 const f=await createFourRoleFixture();
 try{
 const id='c2_batch_product';let photo;
 for(let i=0;i<6;i++){
 if(i===1)photo=f.app.attach(id);
 const publicRead=i===2||i===3,uid=publicRead?buyer:seller;
 const operation=i===2?'list':i===3?'detail':'save';
 const body=i===2?{kind:'product',limit:1,category:'',storeId:null,cursor:null}:i===3?{kind:'product',id}:
 {kind:'product',id:i===0?null:id,requestId:'h2ah_'+i,expectedRevision:i===0?0:i===1?1:i===4?2:3,
 publication:i===1?'publish':i===5?'withdraw':'draft',profile:photo??profile};
 const response=await fetch(f.addresses.mediator+'/api/staging/marketplace/'+operation,{
 method:'POST',headers:{authorization:'Bearer '+uid+'.synthetic.token','x-serverless-authorization':'Bearer operator.payload.','content-type':'application/json'},body:JSON.stringify(body)});
 const value=await response.json();
 assert.equal(response.status,200,JSON.stringify({i,value,trace:f.app.trace}));
 assert.equal(value.ok,true,JSON.stringify(value));
 if(publicRead)assert.doesNotMatch(JSON.stringify(value),/ownerUid|privateContact|processedDigest/);
 }
 assert.equal(f.signs,6);assert.equal((await f.counts()).calls,24);
 const row=f.durable.f.get('marketplaceRateLimits_v1',f.ledger.recordId);
 assert.equal(row.state,'COMPLETE');assert.equal(row.statusReads,24);
 assert.equal(row.signAttempts,6);assert.equal(f.app.f.get('marketplacePublic_v1','product_'+id),null);
 assert.notEqual(f.readerPid,process.pid);
 }finally{await f.close();}
});
test('NEW H2AH bootstrap and four factories stay OFF without real authority/provenance, with zero IO',async()=>{
 let calls=0;const io=()=>{calls++;throw Error('must not run');};
 for(const role of Object.keys(ROLES)){
 const host=await createFourRoleRuntime({role,fetchMetadata:io,fetchPrivate:io});
 assert.equal(host.ready,false);
 assert.equal((await bootstrapFourRole(role,{env:{},read:io,transport:io})).ready,false);
 }
 assert.equal(calls,0);
 const paths=[];
 const bad=await bootstrapFourRole('reader',{env:{OLDX_H2AH_ENABLED:'true'},
 read:async path=>{paths.push(String(path));throw Error('missing independently mounted evidence');},transport:io});
 assert.equal(bad.ready,false);assert.equal(calls,0);
 assert.ok(paths.includes('/run/oldx/config/runtime.json'));assert.ok(paths.includes('/run/oldx/trust/controller-spki.sha256'));
});
test('NEW H2AH Firebase SDK bindings use explicit Compute metadata auth and keep Reader/Gateway SDK-free',async()=>{
 const c=makeCrypto(),captures={};const protocol=c.protocol('backend',()=>{throw Error('NO_NETWORK');});
 class Compute{constructor(options){captures.compute=options;}}
 class GoogleAuth{constructor(options){captures.auth=options;}}
 class Firestore{constructor(options){captures.db=options;this.projectId=options.projectId;this.databaseId=options.databaseId;}
 async terminate(){captures.closed=true;}}
 class Storage{constructor(options){captures.storage=options;}}
 const sdk={initializeApp:options=>({options}),getAuth:app=>({app,verifyIdToken:()=>{throw Error('not executed');}}),
 deleteApp:async()=>{},Firestore,Storage,Compute,GoogleAuth,FieldValue:{}};
 const native=await createFirebaseNativeBindings({protocol,fetchMetadata:c.metadata('backend'),sdkLoader:async()=>sdk,now:()=>baseTime});
 assert.equal(captures.compute.serviceAccountEmail,'default');
 assert.equal(captures.db.projectId,'oldx-staging');assert.equal(captures.db.databaseId,'(default)');
 assert.ok(captures.auth.authClient instanceof Compute);assert.ok(captures.db.auth instanceof GoogleAuth);
 assert.equal(captures.storage.retryOptions.autoRetry,false);await native.close();
 let imports=0;
 await assert.rejects(createFirebaseNativeBindings({protocol:c.protocol('reader',()=>{}),
 sdkLoader:()=>{imports++;throw Error('forbidden');}}),/FIREBASE_ROLE/);
 assert.equal(imports,0);
});
test('NEW H2AH role COPY closures and dependency locks are complete, immutable and contain no cloud automation',async()=>{
 const plan=JSON.parse(await readFile(resolve(root,'deployment/four-role/manifest.json'),'utf8'));
 assert.equal(plan.executionAllowed,false);assert.equal(plan.network.ingress,'internal');
 assert.equal(plan.network.vpcEgress,'all-traffic');assert.equal(plan.invokerEdges.length,6);
 const example=JSON.parse(await readFile(resolve(root,'deployment/four-role/runtime-config.example.json'),'utf8'));
 assert.equal(createFourRoleAuthority({enabled:true,configuration:example.configuration}),null);
 for(const role of Object.keys(ROLES)){
 const base='deployment/four-role/',docker=await readFile(resolve(root,base+'Dockerfile.'+role),'utf8');
 const files=await collectFourRoleClosure(root,role),declared=JSON.parse(await readFile(resolve(root,base+role+'/copy-closure.json'),'utf8'));
 assert.deepEqual(files,declared.files);assert.ok(files.every(p=>docker.includes(JSON.stringify(p))));
 for(const line of docker.split('\n').filter(l=>l.startsWith('FROM ')))assert.match(line,/@sha256:[a-f0-9]{64}/);
 assert.match(docker,/USER 65532:65532/);assert.match(docker,/STOPSIGNAL SIGTERM/);
 assert.match(docker,/ENTRYPOINT \["\/nodejs\/bin\/node"\]/);
 assert.doesNotMatch(docker,/^(?:ADD|ARG|HEALTHCHECK) /m);
 const manifest=JSON.parse(await readFile(resolve(root,base+role+'/package.json'),'utf8'));
 const lock=JSON.parse(await readFile(resolve(root,base+role+'/package-lock.json'),'utf8'));
 assert.deepEqual(manifest.dependencies,lock.packages[''].dependencies);
 for(const [name,version]of Object.entries(manifest.dependencies)){
 assert.equal(lock.packages['node_modules/'+name].version,version);
 assert.match(lock.packages['node_modules/'+name].integrity,/^sha512-/);
 }
 if(role==='gateway'||role==='reader')assert.equal(Object.keys(manifest.dependencies).length,0);
 assert.equal(plan.services[role].uri,'UNKNOWN_REAL_RUN_APP_URI');
 assert.match(plan.services[role].image,/UNKNOWN_NEW_CHILD_IMAGE$/);
 assert.equal(plan.services[role].cloudRunServiceTemplate.spec.template.spec.containers[0].env[0].value,'false');
 assert.equal(plan.services[role].cloudRunServiceTemplate.metadata.annotations['run.googleapis.com/ingress'],'internal');
 const spec=plan.services[role].cloudRunServiceTemplate.spec.template.spec;
 assert.ok(spec.containers[0].volumeMounts.some(v=>v.mountPath==='/run/oldx/config'));
 assert.ok(spec.containers[0].volumeMounts.some(v=>v.mountPath==='/run/oldx/trust'));
 for(const volume of spec.volumes)assert.match(volume.secret.items[0].key,/^UNKNOWN_APPROVED_.*VERSION_NUMBER$/);
 // Validate transitive lock closure without registry access or npm installation.
 const resolveDep=(from,name)=>{let at=from;for(;;){
 const candidate=(at?at+'/':'')+'node_modules/'+name;
 if(lock.packages[candidate])return candidate;
 const index=at.lastIndexOf('/node_modules/');if(index>=0)at=at.slice(0,index);else if(at)at='';else return null;
 }};
 for(const [path,entry]of Object.entries(lock.packages)){
 if(!path)continue;
 for(const name of Object.keys({...entry.dependencies,...entry.optionalDependencies,...entry.peerDependencies}))
 assert.ok(resolveDep(path,name)||entry.optionalDependencies?.[name]||entry.peerDependenciesMeta?.[name]?.optional,
 path+' unresolved '+name);
 }
 }
});

test('NEW H2AH Reader cannot expose a private PEM disguised as a public response',async()=>{
 const f=await createFourRoleFixture();
 try{
 const reservation=await f.reserve();await f.mode('private-pem');
 const send=(kind,url)=>f.protocols.gateway.send('reader','/internal/key-status',
 Buffer.from(JSON.stringify({name:H2S_VERSION,url})),{operation:'sign-'+kind,reservation});
 assert.equal((await send('version',H2S_VERSION_URL)).status,200);
 const response=await send('public',H2S_VERSION_URL+'/publicKey');
 assert.equal(response.status,503);assert.doesNotMatch(await response.text(),/BEGIN.*PRIVATE KEY|MUST_NEVER_LEAK/);
 assert.equal((await f.counts()).calls,2);
 }finally{await f.close();}
});
test('NEW H2AH concurrent signed Reader requests have only one globally committed GET slot',async()=>{
 const f=await createFourRoleFixture();
 try{
 const reservation=await f.reserve();
 const send=()=>f.protocols.gateway.send('reader','/internal/key-status',
 Buffer.from(JSON.stringify({name:H2S_VERSION,url:H2S_VERSION_URL})),{operation:'sign-version',reservation});
 const responses=await Promise.all([send(),send()]);
 assert.deepEqual(responses.map(r=>r.status).sort(),[200,503]);assert.equal((await f.counts()).calls,1);
 }finally{await f.close();}
});
test('NEW H2AH expired runtime authority returns OFF health and cannot dispatch',async()=>{
 let bound=true,calls=0;
 const server=createFourRoleServer({role:'mediator',runtime:{ready:true,isBound:()=>bound,origin:'https://mediator.region.run.app',
 fetch:async()=>{calls++;return new Response(null,{status:200});}}});
 server.listen(0,'127.0.0.1');await once(server,'listening');
 try{
 const url='http://127.0.0.1:'+server.address().port;
 assert.equal((await(await fetch(url+'/healthz')).json()).state,'BOUND');
 bound=false;assert.equal((await(await fetch(url+'/healthz')).json()).state,'OFF');
 assert.equal((await fetch(url+'/api/staging/marketplace/save',{method:'POST',body:'{}'})).status,503);
 assert.equal(calls,0);
 }finally{server.closeAllConnections();await new Promise(r=>server.close(r));}
});

test('NEW H2AH actual installed pinned Firebase clients initialize and close offline without token/Cloud calls',async()=>{
 const localRequire=createRequire(resolve(process.env.OLDX_EXISTING_SDK_ROOT??root,'package.json'));
 const names=new Set(['firebase-admin/app','firebase-admin/auth','@google-cloud/firestore','@google-cloud/storage','google-auth-library']);
 const locations=new Map([...names].map(name=>[name,pathToFileURL(localRequire.resolve(name)).href]));
 const hooks=registerHooks({resolve(specifier,context,nextResolve){
 if(names.has(specifier))return {url:locations.get(specifier),shortCircuit:true};
 return nextResolve(specifier,context);
 }});
 let native,credentials=0,networkAttempts=0;
 const originals=[];
 for(const [name,methods]of [['node:http',['request','get']],['node:https',['request','get']],['node:net',['connect','createConnection']],['node:tls',['connect']]]){
 const module=localRequire(name);for(const method of methods){originals.push([module,method,module[method]]);
 module[method]=()=>{networkAttempts++;throw Error('OFFLINE_SDK_NETWORK_FORBIDDEN');};}}
 syncBuiltinESMExports();
 try{
 const c=makeCrypto(),protocol=c.protocol('backend',()=>{throw Error('NO_PRIVATE_NETWORK');});
 native=await createFirebaseNativeBindings({protocol,fetchMetadata:()=>{credentials++;throw Error('NO_TOKEN_ACQUISITION');},now:()=>baseTime});
 assert.equal(native.adminFirestore.constructor.name,'Firestore');
 assert.equal(native.adminFirestore.projectId,'oldx-staging');assert.equal(native.adminFirestore.databaseId,'(default)');
 assert.equal(native.adminAuth.app.options.projectId,'oldx-staging');
 assert.equal(typeof native.FieldValue.serverTimestamp,'function');
 assert.equal(credentials,0);assert.equal(networkAttempts,0);
 }finally{await native?.close();hooks.deregister();for(const [module,method,original]of originals)module[method]=original;syncBuiltinESMExports();}
});

test('NEW H2AH Mediator never treats forwarded IAM header as Firebase actor or stage authority',async()=>{
 const f=await createFourRoleFixture();
 try{
 const body=JSON.stringify({kind:'product',id:null,requestId:'denied',expectedRevision:0,publication:'draft',profile});
 for(const authorization of [null,'Bearer '+buyer+'.synthetic.token']){
 const headers={'content-type':'application/json','x-serverless-authorization':'Bearer stripped.payload.'};
 if(authorization)headers.authorization=authorization;
 const response=await fetch(f.addresses.mediator+'/api/staging/marketplace/save',{method:'POST',headers,body});
 assert.equal(response.status,403);
 }
 assert.equal(f.durable.f.get('marketplaceRateLimits_v1',f.ledger.recordId),null);
 assert.equal((await f.counts()).calls,0);assert.equal(f.signs,0);
 }finally{await f.close();}
});
