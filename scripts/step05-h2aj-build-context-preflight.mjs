// BAJUTO Step05 H2AJ: SOURCE-ONLY rigorous Buildx context/Dockerfile validation.
// No Docker/build/registry/Cloud I/O. Never alters H2AI's consumed marker.
// Docker --file MUST be absolute and inside the unique prepared context, not
// relative to WSL's current directory. This closes the observed lstat failure.
import {readFile, lstat, realpath} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {resolve, relative, dirname, isAbsolute, sep} from 'node:path';
import {pathToFileURL} from 'node:url';
const roles=new Set(['mediator','gateway','backend','reader']);
const sha=x=>createHash('sha256').update(x).digest('hex');
const BASE='gcr.io/distroless/nodejs24-debian13:nonroot@sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec';
const BUILDER='node:24-bookworm-slim@sha256:dc26ae92c9fb15cf6b1d63e20f0944b2efe0f115b20e00be48fb23fceb061c54';
const fail=reason=>{throw Error('H2AJ_CONTEXT_'+reason);};
const legal=p=>typeof p==='string'&&/^(?:features|functions|scripts|deployment\/four-role)\/[a-zA-Z0-9_./-]+$/.test(p)&&
 !p.split('/').includes('..')&&!p.split('/').includes('.')&&!p.includes('//');
const inside=(root,full)=>full.startsWith(root+sep);
async function file(root,path){
 if(!legal(path))fail('COPY_SOURCE_OUTSIDE_ALLOWLIST');
 const full=resolve(root,path);
 if(!inside(root,full))fail('ESCAPING_CONTEXT');
 const info=await lstat(full).catch(()=>fail('MISSING_FILE_'+path));
 if(!info.isFile()||info.isSymbolicLink())fail('UNSAFE_FILE_'+path);
 const real=await realpath(full);
 if(!inside(root,real))fail('SYMLINK_IN_PATH_'+path);
 return readFile(real);
}
function expectedParents(srcs,role){
 const dirs=new Set();
 for(const p of srcs){
  let d=dirname(p).replaceAll('\\','/');
  while(d!=='.'&&d!=='/'&&!dirs.has(d)){
    dirs.add(d+'/');d=dirname(d).replaceAll('\\','/');
  }
 }
 // The ignore file may include only these required directories/files.
 return new Set(['**',...Array.from(dirs,x=>'!'+x),
     ...Array.from(srcs,x=>'!'+x),
     '!deployment/four-role/Dockerfile.'+role,
     '!deployment/four-role/Dockerfile.'+role+'.dockerignore']);
}
export async function validateH2AJFourRoleBundle({role,context,sourceRevision}={}){
 if(!roles.has(role)||typeof context!=='string'||!isAbsolute(context)||
    !/^[a-f0-9]{40}$/.test(sourceRevision||''))fail('EXACT_INPUT_REQUIRED');
 const root=await realpath(context).catch(()=>fail('CONTEXT_MISSING'));
 if(root!==resolve(context))fail('SYMLINK_CONTEXT');
 const dockerRel='deployment/four-role/Dockerfile.'+role;
 const dockerfile=resolve(root,dockerRel);
 const dockerText=(await file(root,dockerRel)).toString('utf8');
 const instructions=dockerText.split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
 const from=instructions.filter(x=>x.startsWith('FROM '));
 const expectedFrom=role==='mediator'||role==='backend'
   ?['FROM --platform=linux/amd64 '+BUILDER+' AS dependencies',
     'FROM --platform=linux/amd64 '+BASE]
   :['FROM --platform=linux/amd64 '+BASE];
 if(JSON.stringify(from)!==JSON.stringify(expectedFrom))fail('IMMUTABLE_BASE_DRIFT');
 if(!instructions.includes('USER 65532:65532')||
    !instructions.includes('WORKDIR /app')||
    instructions.some(x=>x.startsWith('ADD ')||x.includes('USER root')||x.startsWith('RUN curl ')))fail('UNEXPECTED_DOCKER_DIRECTIVE');
 const srcs=[];
 let otherCopies=0, builderCopy=0;
 for(const line of instructions.filter(x=>x.startsWith('COPY '))){
   if(line.startsWith('COPY deployment/four-role/')){
      const expected='COPY deployment/four-role/'+role+'/package.json deployment/four-role/'+role+'/package-lock.json ./';
      if((role!=='mediator'&&role!=='backend')||line!==expected)fail('BUILDER_PACKAGE_COPY_DRIFT');
      builderCopy++;continue;
   }
   if(line.startsWith('COPY --from=dependencies ')){
      otherCopies++;
      if(role==='gateway'||role==='reader'||!line.includes('/deps/node_modules /app/node_modules'))
        fail('UNEXPECTED_STAGE_COPY');
      continue;
   }
   const pos=line.indexOf('[');
   if(pos<0)fail('COPY_SYNTAX');
   let args;
   try{args=JSON.parse(line.slice(pos));}catch{fail('COPY_JSON_SYNTAX');}
   if(!Array.isArray(args)||args.length!==2||!legal(args[0])||
      !args[1].startsWith('/app/')||!line.includes('--chown=65532:65532')||
      !line.includes('--chmod=0444'))fail('COPY_POLICY');
   srcs.push(args[0]);
 }
 if(otherCopies!==((role==='mediator'||role==='backend')?1:0)||
    builderCopy!==((role==='mediator'||role==='backend')?1:0))fail('STAGE_COPY_COUNT');
 const expectedCount=87;
 if(srcs.length!==expectedCount||new Set(srcs).size!==srcs.length)fail('COPY_INPUT_COUNT');
 const roleDir='deployment/four-role/'+role+'/';
 const packageFiles=[roleDir+'package.json',roleDir+'package-lock.json'];
 const provenance='deployment/four-role/source-provenance.json';
 if(!packageFiles.every(x=>srcs.includes(x))||!srcs.includes(provenance))fail('METADATA_COPY_MISSING');
 const closure=JSON.parse((await file(root,roleDir+'copy-closure.json')).toString('utf8'));
 if(closure?.v!==1||closure.role!==role||
    closure.entrypoint!=='functions/staging-marketplace/four-role/'+role+'.mjs'||
    !Array.isArray(closure.files)||
    closure.files.length!==84||new Set(closure.files).size!==84)fail('CLOSURE_MANIFEST');
 const realSources=new Set(srcs.filter(x=>!packageFiles.includes(x)&&x!==provenance));
 if(realSources.size!==84||closure.files.some(x=>!realSources.has(x)))fail('COPY_CLOSURE_DRIFT');
 const manifest=JSON.parse((await file(root,'deployment/four-role/manifest.json')).toString('utf8'));
 if(manifest?.executionAllowed!==false||manifest.project!=='oldx-staging')fail('FUTURE_DEPLOYMENT_NOT_OFF');
 const evidence=JSON.parse((await file(root,provenance)).toString('utf8'));
 if(evidence.v!==1||evidence.role!==role||evidence.sourceRevision!==sourceRevision||
    typeof evidence.inputs!=='object'||typeof evidence.files!=='object')fail('SOURCE_PROVENANCE');
 for(const path of [...srcs.filter(x=>x!==provenance),
       dockerRel,dockerRel+'.dockerignore',roleDir+'copy-closure.json',
       'deployment/four-role/manifest.json','deployment/four-role/runtime-config.example.json']){
   const bytes=await file(root,path);
   if(evidence.inputs[path]!==sha(bytes))fail('SOURCE_HASH_DRIFT_'+path);
 }
 for(const p of packageFiles){
   const short=p.slice(roleDir.length);
   if(evidence.files[short]!==evidence.inputs[p])fail('PACKAGE_PROVENANCE_DRIFT');
 }
 for(const p of realSources){
   if(evidence.files[p]!==evidence.inputs[p])fail('CLOSURE_PROVENANCE_DRIFT');
 }
 // Dockerfile-specific ignore is discovered beside the --file path; its
 // allowlist must make ALL COPY sources visible in the context.
 const ignore=(await file(root,dockerRel+'.dockerignore')).toString('utf8')
      .split(/\r?\n/).map(x=>x.trim()).filter(x=>x&&!x.startsWith('#'));
 const permitted=expectedParents(srcs,role);
 if(ignore.length!==permitted.size||
    ignore.some(x=>!permitted.has(x))||
    [...permitted].some(x=>!ignore.includes(x)))fail('DOCKERIGNORE_ALLOWLIST_DRIFT');
 if(!inside(root,dockerfile))fail('DOCKERFILE_NOT_IN_CONTEXT');
 return Object.freeze({role,sourceRevision,context:root,dockerfileAbsolutePath:dockerfile,
   copies:srcs.length,sourceClosure:realSources.size,provenanceSha256:sha(await file(root,provenance)),
   privateDefaultOff:true});
}
if(process.argv[1]&&pathToFileURL(resolve(process.argv[1])).href===import.meta.url){
  if(process.argv.length!==5)fail('CLI_ROLE_CONTEXT_REVISION_REQUIRED');
  const [role,context,sourceRevision]=process.argv.slice(2);
  console.log(JSON.stringify(await validateH2AJFourRoleBundle({role,context,sourceRevision})));
}
