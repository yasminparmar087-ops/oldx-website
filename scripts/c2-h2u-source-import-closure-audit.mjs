#!/usr/bin/env node
// Step05 H2U source-only import closure inventory; NO build/deploy/runtime import.
// Run from an immutable GitHub source checkout with Node >=24.12.
// Reads local JS sources only; no network, Google credentials, Docker or writes.
import {readFileSync,lstatSync,realpathSync} from 'node:fs';
import {resolve,dirname,relative,extname,sep} from 'node:path';
import {createHash} from 'node:crypto';
import {builtinModules} from 'node:module';

const root=realpathSync(process.cwd());
const start='scripts/c2-h2u-cloud-run-private-off-main.mjs';
const queued=[start], visited=new Map(), externals=new Map();
const builtins=new Set(builtinModules.map(x=>x.replace(/^node:/,'')));
const maxFiles=256, maxTotal=5*1024*1024;
let byteSum=0;
const stop=(why,path)=>{throw Error('H2U_CLOSURE_STOP_'+why+(path?':'+path:''));};
function within(file){
  const path=resolve(root,file);
  const rel=relative(root,path);
  if(rel.startsWith('..'+sep)||rel==='..'||rel.startsWith(sep))stop('OUTSIDE_ROOT',file);
  const stat=lstatSync(path);
  if(!stat.isFile()||stat.isSymbolicLink())stop('SOURCE_NOT_REGULAR',file);
  if(realpathSync(path)!==path)stop('SOURCE_SYMLINK_PARENT',file);
  if(stat.size>1024*1024)stop('SOURCE_FILE_TOO_LARGE',file);
  return {path,rel,stat};
}
function imports(source,rel){
  const out=[];
  // A conservative static import/export-from scanner. Unrecognized syntax,
  // dynamic import, require or new module loading APIs are NOT allowed here.
  // Positive output still needs build-time Node ESM linker verification.
  if(/\bimport\s*\(|\brequire\s*\(|\bcreateRequire\s*\(|\bmodule\.register/.test(source))
    stop('DYNAMIC_MODULE_LOADING',rel);
  const stmt=/(?:^|\n)\s*(?:import|export)\s+(?:[\s\S]{0,400}?)\bfrom\s*(['"])([^'"\r\n]+)\1/g;
  for(const match of source.matchAll(stmt))out.push(match[2]);
  const side=/(?:^|\n)\s*import\s*(['"])([^'"\r\n]+)\1\s*;?/g;
  for(const match of source.matchAll(side))out.push(match[2]);
  // For diagnostic readiness only, not final trusted packaging without ESM
  // linker smoke. Empty "out" is valid for import-free modules.
  return [...new Set(out)];
}
while(queued.length){
  if(visited.size>=maxFiles)stop('EXCESSIVE_FILE_COUNT');
  const entry=queued.shift();
  if(visited.has(entry))continue;
  const {path,rel,stat}=within(entry);
  const ext=extname(path);
  if(!['.mjs','.js','.json'].includes(ext))stop('UNSUPPORTED_EXTENSION',entry);
  byteSum+=stat.size;
  if(byteSum>maxTotal)stop('EXCESSIVE_TOTAL_BYTES');
  const content=readFileSync(path);
  visited.set(rel,{
    size:content.length,
    sha256:createHash('sha256').update(content).digest('hex'),
  });
  if(ext==='.json')continue;
  const text=content.toString('utf8');
  for(const spec of imports(text,rel)){
    if(spec.startsWith('node:')){
      if(!builtins.has(spec.slice(5)))stop('UNKNOWN_NODE_BUILTIN',spec);
    }else if(spec.startsWith('.')){
      const target=relative(root,resolve(dirname(path),spec));
      if(!visited.has(target)&&!queued.includes(target))queued.push(target);
    }else{
      if(!externals.has(spec))externals.set(spec,[]);
      externals.get(spec).push(rel);
    }
  }
}
const result={
  checkpoint:'H2U_OFF_SOURCE_ONLY_IMPORT_CLOSURE',
  entry:start,
  fileCount:visited.size,
  totalSourceBytes:byteSum,
  files:[...visited].sort(([a],[b])=>a.localeCompare(b))
    .map(([path,data])=>({path,...data})),
  barePackageImports:[...externals].sort(([a],[b])=>a.localeCompare(b))
    .map(([specifier,requiredBy])=>({specifier,requiredBy:requiredBy.sort()})),
  conclusion:'STATIC_IMPORT_SCAN_ONLY_NOT_LINKER_OR_RUNTIME_VERIFIED',
  noCloudActions:true,noDockerBuild:true,
};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
