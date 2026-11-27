// NEW H2U source-only real local HTTP smoke. Not an existing test replay.
// Run ONLY in nonroot read-only Docker with --network none, no port publish,
// exact 65-file Owner source snapshot mounted read-only.
// No Cloud Run, Firebase, Firestore, KMS, IAM, tokens, image build or deployment.
import {spawn} from 'node:child_process';
import {readFileSync,lstatSync,realpathSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,relative,isAbsolute,sep} from 'node:path';

const fail=reason=>{throw Error('H2U_OFF_HTTP_SMOKE_'+reason);};
const root='/source';
const manifest='/evidence/source-closure.json';
const sha='12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc';
const sha256=x=>createHash('sha256').update(x).digest('hex');
const bytes=readFileSync(manifest);
if(sha256(bytes)!==sha)fail('MANIFEST_CHANGED');
const m=JSON.parse(bytes.toString('utf8'));
if(m.fileCount!==65||m.totalSourceBytes!==349667||
   m.entry!=='scripts/c2-h2u-cloud-run-private-off-main.mjs'||
   !Array.isArray(m.files)||m.files.length!==65||
   !Array.isArray(m.barePackageImports)||m.barePackageImports.length!==0)
   fail('MANIFEST_SCOPE');
const base=realpathSync(root);
let bytesSeen=0;
for(const f of m.files){
  if(!f||typeof f.path!=='string'||
     !/^(?:[a-zA-Z0-9._-]+\/)*[a-zA-Z0-9._-]+\.(?:mjs|js)$/.test(f.path)||
     f.path.split('/').includes('..')||f.path==='.'||
     !/^[a-f0-9]{64}$/.test(f.sha256)||!Number.isSafeInteger(f.size))
    fail('UNSAFE_ENTRY');
  const target=resolve(base,f.path);
  const rel=relative(base,target);
  if(!rel||rel.startsWith('..'+sep)||rel==='..'||isAbsolute(rel)||
     realpathSync(target)!==target)fail('INVALID_SOURCE_PATH');
  const st=lstatSync(target);
  if(!st.isFile()||st.isSymbolicLink()||st.size!==f.size)fail('MISSING_SOURCE');
  const data=readFileSync(target);
  if(sha256(data)!==f.sha256)fail('MODIFIED_SOURCE');
  bytesSeen+=data.length;
}
if(bytesSeen!==349667)fail('SOURCE_SIZE_DRIFT');

const port='18347';
const url='http://127.0.0.1:'+port;
let child;
let terminated=false;
let stdout='',stderr='';
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function request(method,path,headers={}){
 const res=await fetch(url+path,{
   method,headers,redirect:'manual',cache:'no-store',signal:AbortSignal.timeout(1500),
 });
 const payload=await res.text();
 return {status:res.status,body:JSON.parse(payload),
   cache:res.headers.get('cache-control')};
}
try{
  child=spawn(process.execPath,[resolve(base,m.entry)],{
    cwd:base,env:{PORT:port,OLDX_H2U_MODE:'OFF'},
    stdio:['ignore','pipe','pipe'],windowsHide:true,
  });
  child.stdout.setEncoding('utf8');
  child.stderr.setEncoding('utf8');
  child.stdout.on('data',part=>{stdout+=part.slice(0,1000);});
  child.stderr.on('data',part=>{stderr+=part.slice(0,1000);});
  let live=false;
  for(let i=0;i<80;i++){
    if(child.exitCode!==null)fail('CHILD_EARLY_EXIT');
    try{
      const health=await request('GET','/healthz');
      if(health.status===200&&health.body.mode==='OFF'&&
         health.body.service==='oldx-c2-private-gateway'&&
         health.cache==='private, no-store'){live=true;break;}
      fail('UNSAFE_HEALTH_RESPONSE');
    }catch(e){
      if(String(e.message||e).startsWith('H2U_OFF_HTTP_SMOKE_'))throw e;
      await sleep(40);
    }
  }
  if(!live)fail('SERVER_NEVER_HEALTHY');
  const off=await request('POST','/api/staging/marketplace/save',
    {'authorization':'Bearer synthetic-owner','x-oldx-enable':'true'});
  if(off.status!==503||off.body?.error?.code!=='H2_GATEWAY_DISABLED')
    fail('PRODUCT_REQUEST_NOT_OFF');
  const unknown=await request('GET','/unlisted');
  if(unknown.status!==404||unknown.body?.error?.code!=='NOT_FOUND')
    fail('UNKNOWN_ROUTE_OPEN');
  if(!stdout.includes('H2U_OFF_ONLY_LISTENING=TRUE'))fail('NOT_LISTENING_LOG');
  if(stderr.includes('token')||stderr.includes('password'))fail('UNEXPECTED_SECRET_DIAGNOSTIC');
  console.log('OLDX_H2U_OFF_RUNTIME_SMOKE=PASS_LOCAL_LISTENER_WITH_LIMITS');
  console.log('OLDX_H2U_OFF_RUNTIME_SOURCE_FILES=65');
  console.log('OLDX_H2U_OFF_RUNTIME_HEALTH_STATUS=200_OFF');
  console.log('OLDX_H2U_OFF_RUNTIME_SAVE_STATUS=503_DISABLED');
  console.log('OLDX_H2U_OFF_RUNTIME_UNKNOWN_STATUS=404');
  console.log('OLDX_H2U_OFF_RUNTIME_NETWORK=DOCKER_LOOPBACK_ONLY');
  console.log('OLDX_H2U_OFF_RUNTIME_CLOUD_WRITES=NONE');
  console.log('OLDX_H2U_OFF_RUNTIME_IMAGE_BUILD=NONE');
  console.log('OLDX_H2U_H2_PRODUCTION=NO_GO');
}finally{
  if(child){
    if(child.exitCode===null)child.kill('SIGTERM');
    await Promise.race([
      new Promise(resolve=>child.once('exit',resolve)),
      sleep(1000),
    ]);
    if(child.exitCode===null)child.kill('SIGKILL');
  }
}
