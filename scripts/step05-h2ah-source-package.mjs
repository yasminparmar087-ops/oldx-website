import {readFile,lstat,mkdir,writeFile,realpath} from 'node:fs/promises';
import {resolve,relative,dirname} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const run=promisify(execFile),hash=x=>createHash('sha256').update(x).digest('hex');
const roles=['mediator','gateway','backend','reader'];
export async function collectFourRoleClosure(root,role){
 if(!roles.includes(role))throw Error('ROLE');
 const files=new Set(),queue=['functions/staging-marketplace/four-role/'+role+'.mjs'];
 while(queue.length){
 const path=queue.pop();if(files.has(path))continue;
 const full=resolve(root,path),rel=relative(root,full);
 if(rel.startsWith('..')||rel.startsWith('/')||(await lstat(full)).isSymbolicLink())throw Error('UNSAFE_SOURCE_PATH');
 const source=await readFile(full,'utf8');files.add(path);
 for(const m of source.matchAll(/(?:from\s*|import\s*\(?\s*)['"](\.[^'"]+)['"]/g)){
 const dep=relative(root,resolve(dirname(full),m[1])).replaceAll('\\','/');queue.push(dep);
 }
 }
 return [...files].sort();
}
// PREPARES FILES ONLY. No image/registry/cloud/SDK invocation or implicit npm.
// Requires clean isolated review-branch checkout; never resets owner's work.
export async function prepareFourRoleSourceBundle({root,role,target}={}){
 const cwd=await realpath(root);
 const branch=(await run('git',['branch','--show-current'],{cwd})).stdout.trim();
 const dirty=(await run('git',['status','--porcelain'],{cwd})).stdout;
 const revision=(await run('git',['rev-parse','HEAD'],{cwd})).stdout.trim();
 if(branch!=='security-hardening-review'||dirty||!/^[a-f0-9]{40}$/.test(revision))throw Error('ISOLATED_CLEAN_REVIEW_SOURCE_REQUIRED');
 const destination=resolve(target);
 if(!relative(cwd,destination).startsWith('..'))throw Error('DESTINATION_MUST_BE_OUTSIDE_CHECKOUT');
 await mkdir(destination); // Exclusive: never overwrite a previous bundle/marker.
 const closure=await collectFourRoleClosure(cwd,role);
 const base='deployment/four-role/',metadata=[base+role+'/package.json',base+role+'/package-lock.json',
 base+'Dockerfile.'+role,base+'Dockerfile.'+role+'.dockerignore',base+role+'/copy-closure.json',base+'manifest.json',base+'runtime-config.example.json'];
 const files={},inputs={};
 for(const path of [...closure,...metadata]){
 const full=resolve(cwd,path);if((await lstat(full)).isSymbolicLink())throw Error('SYMLINK');
 const bytes=await readFile(full),out=resolve(destination,path);
 await mkdir(dirname(out),{recursive:true});await writeFile(out,bytes,{flag:'wx'});
 inputs[path]=hash(bytes);if(closure.includes(path))files[path]=hash(bytes);
 }
 for(const name of ['package.json','package-lock.json'])files[name]=inputs[base+role+'/'+name];
 const provenance={v:1,role,sourceRevision:revision,files,inputs};
 await writeFile(resolve(destination,base+'source-provenance.json'),JSON.stringify(provenance,null,2)+'\n',{flag:'wx'});
 return Object.freeze({role,sourceRevision:revision,context:destination,files:closure.length,
 provenanceSha256:hash(JSON.stringify(provenance,null,2)+'\n')});
}
if(process.argv[1]&&pathToFileURL(process.argv[1]).href===import.meta.url){
 const [flag,role,target]=process.argv.slice(2);
 if(flag!=='--prepare-source-only'||!target)throw Error('SOURCE_ONLY_FLAG_ROLE_TARGET_REQUIRED');
 console.log(JSON.stringify(await prepareFourRoleSourceBundle({root:process.cwd(),role,target})));
}
