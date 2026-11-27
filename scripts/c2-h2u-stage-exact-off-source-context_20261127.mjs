// BAJUTO/OLDX H2U: stage ONLY EXACT existing 65-file OFF Gateway source
// from already-produced Owner-local manifest into a minimal OCI build context.
// SOURCE ONLY: no source evaluation, Docker build, network, cloud IAM or deploy.
// No base image or usable Containerfile is selected without independent approval.
import {
  readFileSync,writeFileSync,copyFileSync,statSync,lstatSync,realpathSync,
  mkdirSync,openSync,closeSync,readdirSync,
} from 'node:fs';
import {dirname,resolve,relative,isAbsolute,sep} from 'node:path';
import {createHash} from 'node:crypto';

const manifestPath='/evidence/source-closure.json';
const sourceDir='/evidence/source';
const out='/out/h2u-off-source-context';
const EXPECTED='12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc';
const SHA=/^[0-9a-f]{64}$/;
const fail=code=>{throw Error('H2U_CONTEXT_STOP_'+code);};
const hash=data=>createHash('sha256').update(data).digest('hex');
if(process.argv.length!==2)fail('UNEXPECTED_ARGS');

const raw=readFileSync(manifestPath);
if(hash(raw)!==EXPECTED)fail('MANIFEST_HASH');
let manifest;
try{manifest=JSON.parse(raw.toString('utf8'));}
catch{fail('MANIFEST_JSON');}
if(manifest?.checkpoint!=='H2U_OFF_SOURCE_ONLY_IMPORT_CLOSURE'||
   manifest.entry!=='scripts/c2-h2u-cloud-run-private-off-main.mjs'||
   manifest.fileCount!==65||manifest.totalSourceBytes!==349667||
   manifest.conclusion!=='STATIC_IMPORT_SCAN_ONLY_NOT_LINKER_OR_RUNTIME_VERIFIED'||
   !Array.isArray(manifest.files)||manifest.files.length!==65||
   !Array.isArray(manifest.barePackageImports)||manifest.barePackageImports.length!==0)
   fail('MANIFEST_CONTRACT');

const sourceRoot=realpathSync(sourceDir);
const outputRoot=realpathSync('/out');
const list=new Map();
let size=0;
const safePath=/^(?:[A-Za-z0-9._-]+\/)*[A-Za-z0-9._-]+\.(?:mjs|js)$/;
for(const file of manifest.files){
  if(!file||typeof file.path!=='string'||!safePath.test(file.path)||
     file.path.split('/').includes('..')||list.has(file.path)||
     !Number.isSafeInteger(file.size)||file.size<0||file.size>1048576||
     typeof file.sha256!=='string'||!SHA.test(file.sha256))
    fail('SOURCE_ENTRY_INVALID');
  const full=resolve(sourceRoot,file.path);
  const rel=relative(sourceRoot,full);
  if(!rel||isAbsolute(rel)||rel==='..'||rel.startsWith('..'+sep)||
     realpathSync(full)!==full)fail('SOURCE_ESCAPE_OR_SYMLINK');
  const stat=lstatSync(full);
  if(!stat.isFile()||stat.isSymbolicLink()||stat.size!==file.size)
    fail('SOURCE_CHANGED');
  const data=readFileSync(full);
  if(hash(data)!==file.sha256)fail('SOURCE_HASH_CHANGED');
  size+=data.length;
  list.set(file.path,{size:file.size,sha256:file.sha256,source:full});
}
if(list.size!==65||size!==349667||!list.has(manifest.entry))
  fail('FILE_COUNT_OR_BYTES');

mkdirSync(out,{mode:0o700});
const contextRoot=realpathSync(out);
const appDir=resolve(contextRoot,'app');
mkdirSync(appDir,{mode:0o755});
const filePaths=[...list.keys()].sort();
for(const path of filePaths){
  const p=list.get(path);
  const dest=resolve(appDir,path);
  const rel=relative(appDir,dest);
  if(!rel||isAbsolute(rel)||rel==='..'||rel.startsWith('..'+sep))
    fail('DEST_ESCAPE');
  mkdirSync(dirname(dest),{recursive:true,mode:0o755});
  const fd=openSync(dest,'wx',0o644);
  closeSync(fd);
  copyFileSync(p.source,dest);
  const bytes=readFileSync(dest);
  if(hash(bytes)!==p.sha256||bytes.length!==p.size)
    fail('STAGED_HASH_MISMATCH');
}
const pkg={
  name:'oldx-h2u-private-off-gateway',
  version:'0.0.0-staging',
  private:true,
  type:'module',
  description:'Default-OFF H2U private Gateway only. No npm dependencies.',
};
writeFileSync(resolve(contextRoot,'package.json'),
 JSON.stringify(pkg,null,2)+'\n',{mode:0o644,flag:'wx'});
// Source tree deliberately contains exactly verified files and no other data.
const listText=filePaths.map(p=>list.get(p).sha256+'  app/'+p).join('\n')+'\n';
writeFileSync(resolve(contextRoot,'SOURCE_SHA256SUMS'),listText,
 {mode:0o644,flag:'wx'});
const proposal=[
 'OLDX H2U OFF SOURCE CONTEXT — NOT AN OCI IMAGE',
 'Project: oldx-staging; branch: security-hardening-review',
 'PREVIOUS_MANIFEST_SHA256='+EXPECTED,
 'SOURCE_FILES=65',
 'SOURCE_BYTES=349667',
 'ESM_STATIC_LINK_EDGES_PREVIOUSLY_VERIFIED=174',
 'NODE_BUILTINS_PREVIOUSLY_VERIFIED=3',
 'EXTERNAL_IMPORTS_PREVIOUSLY_VERIFIED=0',
 'ENTRYPOINT=scripts/c2-h2u-cloud-run-private-off-main.mjs',
 'APPLICATION_MODE=OFF_ONLY',
 'NO_CONTAINERFILE_GENERATED=TRUE',
 'BASE_IMAGE_DIGEST=UNVERIFIED_AND_UNSELECTED',
 'NEW_CONTAINER_BUILD=NOT_AUTHORIZED',
 'REGISTRY_PUSH=NOT_AUTHORIZED',
 'CLOUD_RUN_DEPLOYMENT=NOT_AUTHORIZED',
 'FUTURE_BUILD_GATE=Verify exact pinned Node24 base image digest, entrypoint,',
 'nonroot UID, artifact provenance, Cloud Run private IAM and new Owner consent.',
 'DO_NOT_COPY=Owner credentials, gcloud config, test receipts, old Docker image.',
].join('\n')+'\n';
writeFileSync(resolve(contextRoot,'RELEASE_PLAN_NOT_A_DOCKERFILE.txt'),
 proposal,{mode:0o644,flag:'wx'});
const names=readdirSync(contextRoot).sort();
if(JSON.stringify(names)!==JSON.stringify([
 'RELEASE_PLAN_NOT_A_DOCKERFILE.txt','SOURCE_SHA256SUMS','app','package.json',
 ]))fail('EXTRA_CONTEXT_FILES');
if(readdirSync(resolve(contextRoot,'app')).length<1)
 fail('EMPTY_APP');
const listSha=hash(readFileSync(resolve(contextRoot,'SOURCE_SHA256SUMS')));
console.log('OLDX_H2U_CONTEXT_RESULT=PASS_65_FILES_SOURCE_ONLY');
console.log('OLDX_H2U_CONTEXT_FILE_COUNT=65');
console.log('OLDX_H2U_CONTEXT_SOURCE_BYTES=349667');
console.log('OLDX_H2U_CONTEXT_MANIFEST_SHA256='+EXPECTED);
console.log('OLDX_H2U_CONTEXT_SHA256SUMS_SHA256='+listSha);
console.log('OLDX_H2U_CONTEXT_PACKAGE_JSON=PRIVATE_MODULE_NO_DEPS');
console.log('OLDX_H2U_CONTEXT_CONTAINERFILE=NOT_GENERATED');
console.log('OLDX_H2U_CONTEXT_BASE_DIGEST=NOT_SELECTED');
console.log('OLDX_H2U_CONTEXT_CLOUD_WRITES=NONE');
console.log('OLDX_H2U_CONTEXT_IMAGE_BUILDS_PULLS_SCANS=NONE');
console.log('OLDX_H2U_H2_PRODUCTION=NO_GO');
