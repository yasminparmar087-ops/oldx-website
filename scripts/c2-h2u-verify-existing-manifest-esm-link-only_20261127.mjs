// OLDX Step05 H2U: NEW source-only Node ESM LINK verification, no evaluate().
 // Consumes the PREVIOUS already-produced Owner-local immutable 65-file
// manifest and source tree. Strictly NO HTTP listener, Google API, KMS,
// Cloud Run, Docker build or old test rerun.
import {readFileSync,lstatSync,realpathSync} from 'node:fs';
import {resolve,dirname,relative,isAbsolute,sep,extname} from 'node:path';
import {createHash} from 'node:crypto';
import {builtinModules} from 'node:module';
import vm from 'node:vm';

const expectHash='12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc';
const rootPath='/evidence/source';
const manifestPath='/evidence/source-closure.json';
const fail=code=>{throw Error('H2U_LINK_STOP_'+code);};
if(process.argv.length!==2)fail('NO_ARGS_ALLOWED');
if(typeof vm.SourceTextModule!=='function'||
   typeof vm.SyntheticModule!=='function')fail('VM_MODULES_UNAVAILABLE');
const root=realpathSync(rootPath);
const manifestBytes=readFileSync(manifestPath);
if(createHash('sha256').update(manifestBytes).digest('hex')!==expectHash)
  fail('OLD_MANIFEST_HASH_MISMATCH');
let m;
try{m=JSON.parse(manifestBytes.toString('utf8'));}
catch{fail('MANIFEST_JSON_INVALID');}
if(m?.checkpoint!=='H2U_OFF_SOURCE_ONLY_IMPORT_CLOSURE'||
   m.entry!=='scripts/c2-h2u-cloud-run-private-off-main.mjs'||
   m.fileCount!==65||m.totalSourceBytes!==349667||
   !Array.isArray(m.files)||m.files.length!==65||
   !Array.isArray(m.barePackageImports)||m.barePackageImports.length!==0||
   m.conclusion!=='STATIC_IMPORT_SCAN_ONLY_NOT_LINKER_OR_RUNTIME_VERIFIED'||
   m.noCloudActions!==true||m.noDockerBuild!==true)
   fail('PREVIOUS_MANIFEST_CONTRACT');
const files=new Map();let total=0;
for(const item of m.files){
  if(!item||typeof item.path!=='string'||
     !/^(?:[a-zA-Z0-9._-]+\/)*[a-zA-Z0-9._-]+\.(?:mjs|js)$/.test(item.path)||
     item.path.split('/').includes('..')||
     !Number.isSafeInteger(item.size)||item.size<0||item.size>1048576||
     typeof item.sha256!=='string'||!/^[0-9a-f]{64}$/.test(item.sha256)||
     files.has(item.path))fail('UNSAFE_FILE_ENTRY');
  const full=resolve(root,item.path);
  const rel=relative(root,full);
  if(!rel||rel.startsWith('..'+sep)||rel==='..'||isAbsolute(rel)||
     realpathSync(full)!==full)fail('FILE_OUTSIDE_OR_SYMLINK');
  const stat=lstatSync(full);
  if(!stat.isFile()||stat.isSymbolicLink()||stat.size!==item.size)
     fail('MISSING_OR_CHANGED_SOURCE');
  const data=readFileSync(full);
  if(createHash('sha256').update(data).digest('hex')!==item.sha256)
     fail('SOURCE_SHA256_CHANGED');
  total+=data.length;files.set(item.path,data.toString('utf8'));
}
if(total!==349667||!files.has(m.entry))fail('MANIFEST_FILE_COUNT_OR_BYTES');
const context=vm.createContext(Object.create(null));
const modules=new Map(), builtins=new Map();
for(const [path,src] of files){
  try{modules.set(path,new vm.SourceTextModule(src,{context,identifier:path}));}
  catch{fail('ESM_SYNTAX_'+path);}
}
const builtinNames=new Set(builtinModules.map(s=>s.replace(/^node:/,'')));
let edges=0;
async function linker(spec,parent){
  edges++;
  if(edges>1024)fail('EXCESSIVE_IMPORTS');
  if(typeof spec!=='string'||typeof parent?.identifier!=='string')
    fail('UNTRUSTED_IMPORT');
  if(spec.startsWith('node:')){
    const name=spec.slice(5);
    if(!builtinNames.has(name))fail('UNKNOWN_NODE_BUILTIN');
    if(!builtins.has(spec)){
      const namespace=await import(spec); // built-in Node module ONLY.
      builtins.set(spec,new vm.SyntheticModule(Object.keys(namespace),
        ()=>{}, {context,identifier:spec}));
    }
    return builtins.get(spec);
  }
  if(!spec.startsWith('.')||spec.includes('?')||spec.includes('#')||
     spec.includes('\u0000'))fail('EXTERNAL_OR_UNSAFE_IMPORT');
  const target=relative('.',resolve(dirname(parent.identifier),spec))
    .replaceAll('\\','/');
  if(!files.has(target)||!modules.has(target))fail('IMPORT_OUTSIDE_PINNED_65');
  return modules.get(target);
}
// Node vm.SourceTextModule.link() parses and binds all static ESM imports,
// including named imports/exports. It does NOT execute/evaluate the entrypoint.
const entry=modules.get(m.entry);
await entry.link(linker);
if(entry.status!=='linked')fail('ROOT_NOT_LINKED');
const unlinked=[...modules].filter(([,obj])=>obj.status!=='linked');
if(unlinked.length)fail('UNREACHABLE_OR_UNLINKED_MANIFEST_FILES');
process.stdout.write('OLDX_H2U_ESM_LINK_RESULT=PASS_SOURCE_LINK_ONLY\n');
process.stdout.write('OLDX_H2U_ESM_LINK_MANIFEST_SHA256='+expectHash+'\n');
process.stdout.write('OLDX_H2U_ESM_LINK_SOURCE_FILES='+modules.size+'\n');
process.stdout.write('OLDX_H2U_ESM_LINK_STATIC_EDGES='+edges+'\n');
process.stdout.write('OLDX_H2U_ESM_LINK_BUILTIN_MODULES='+builtins.size+'\n');
process.stdout.write('OLDX_H2U_ESM_LINK_EXTERNAL_IMPORTS=0\n');
process.stdout.write('OLDX_H2U_ESM_SOURCE_EVALUATED=FALSE\n');
process.stdout.write('OLDX_H2U_ESM_LINK_CLOUD_WRITES=NONE\n');
process.stdout.write('OLDX_H2U_ESM_LINK_BUILDS_PULLS_SCANS=NONE\n');
process.stdout.write('OLDX_H2U_H2_PRODUCTION=NO_GO\n');
