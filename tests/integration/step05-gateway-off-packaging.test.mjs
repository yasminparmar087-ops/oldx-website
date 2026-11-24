import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawn} from 'node:child_process';
import {createServer} from 'node:net';
import {once} from 'node:events';
import {fileURLToPath} from 'node:url';
const read=p=>readFileSync(new URL('../../'+p,import.meta.url),'utf8');
const recipe=read('functions/staging-marketplace/Dockerfile.gateway-off');
test('new OFF image recipe pins exact verified AMD64 base without runtime override or builder',()=>{
 const lines=recipe.split(/\r?\n/).map(v=>v.trim()).filter(v=>v&&!v.startsWith('#'));
 assert.equal(lines[0],'FROM --platform=linux/amd64 gcr.io/distroless/nodejs24-debian13:nonroot@sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec');
 assert.equal(lines.filter(v=>v.startsWith('FROM ')).length,1);
 assert.equal(lines.some(v=>/^(ARG|RUN|ADD|ONBUILD|VOLUME|HEALTHCHECK)\b/.test(v)),false);
 assert.ok(lines.includes('USER 65532:65532'));assert.ok(lines.includes('STOPSIGNAL SIGTERM'));
 assert.ok(lines.includes('ENTRYPOINT ["/nodejs/bin/node"]'));assert.ok(lines.includes('CMD ["server.mjs"]'));
});
test('Dockerfile-specific context and COPY allow exactly one source, no credentials/dependencies',()=>{
 assert.deepEqual(recipe.split(/\r?\n/).filter(v=>v.startsWith('COPY ')),['COPY --chown=65532:65532 --chmod=0444 functions/staging-marketplace/cloud-run-gateway-off-server.mjs /app/server.mjs']);
 assert.deepEqual(read('functions/staging-marketplace/Dockerfile.gateway-off.dockerignore').trim().split(/\r?\n/),['**','!functions/','!functions/staging-marketplace/','!functions/staging-marketplace/cloud-run-gateway-off-server.mjs']);
 const source=read('functions/staging-marketplace/cloud-run-gateway-off-server.mjs');
 assert.deepEqual([...source.matchAll(/from '([^']+)'/g)].map(v=>v[1]).sort(),['node:events','node:http','node:path','node:url']);
 assert.doesNotMatch(source,/\b(?:fetch|readFile|applicationDefault|initializeApp)\s*\(/);
});
test('packaged exec entrypoint starts with hostile activation env, keeps API OFF and exits on SIGTERM',async()=>{
 const reserve=createServer();reserve.listen(0,'127.0.0.1');await once(reserve,'listening');const port=reserve.address().port;await new Promise(r=>reserve.close(r));
 const source=fileURLToPath(new URL('../../functions/staging-marketplace/cloud-run-gateway-off-server.mjs',import.meta.url));
 const child=spawn(process.execPath,[source],{windowsHide:true,env:{...process.env,PORT:String(port),NODE_OPTIONS:'',OLDX_PRODUCT_READ_ACTIVATE_STAGING:'true',OLDX_PRODUCT_READ_STAGING_ADC:'true',OLDX_STAGING_COMMANDS_ENABLED:'true',OLDX_STAGING_PUBLICATION_ENABLED:'true',GOOGLE_APPLICATION_CREDENTIALS:'/never-read/gateway-fixture.json'},stdio:['ignore','pipe','pipe']});
 let output='';child.stdout.on('data',v=>output+=v);child.stderr.on('data',v=>output+=v);
 const exited=once(child,'exit');let ready=false;
 try{
  const stopAt=Date.now()+5000;
  while(Date.now()<stopAt){try{const r=await fetch('http://127.0.0.1:'+port+'/healthz',{signal:AbortSignal.timeout(250)});if(r.status===200){ready=true;break;}}catch{}await new Promise(r=>setTimeout(r,20));}
  assert.equal(ready,true);
  const r=await fetch('http://127.0.0.1:'+port+'/api/staging/marketplace/save',{method:'POST',headers:{authorization:'Bearer private.fixture.token','x-serverless-authorization':'Bearer private.iam.token','x-oldx-gateway-attestation':'private.assertion.signature','x-oldx-gateway-request-proof':'private.proof'},body:'{"activate":true}'});
  assert.equal(r.status,503);assert.deepEqual(await r.json(),{ok:false,error:{code:'ENFORCEMENT_UNAVAILABLE'}});
  child.kill('SIGTERM');
  const deadline=new Promise((_,reject)=>{const t=setTimeout(()=>reject(Error('SIGTERM timeout')),3000);t.unref();});
  const [code,signal]=await Promise.race([exited,deadline]);
  // Windows process.kill can terminate directly rather than deliver POSIX signal.
  if(process.platform!=='win32')assert.equal(code,0);else assert.ok(code===0||signal==='SIGTERM');
  assert.equal(output,'');
 }finally{if(child.exitCode===null&&child.signalCode===null)child.kill('SIGKILL');}
});
