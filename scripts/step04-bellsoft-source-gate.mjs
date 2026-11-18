/** SOURCE-ONLY BellSoft Step04 guards. Never performs build, scan or deploy. */
import {createHash} from 'node:crypto';
export const BELLSOFT_IMAGE_EXECUTION_ENABLED=false;
export const OLD_SIGNED_BELLSOFT_INDEX='sha256:fd67bdfa683df22bca1b149ae1ee1933e662831b895ff4c29ba98217b29c0769';
const ORIGINAL_GIT_BLOB='bcf27cd186668c6ac50af15f65e64df494774b28';
const ORIGINAL_BASE='gcr.io/distroless/nodejs24-debian13@sha256:6abfcb367ebc291572c774c1592a986be2ab26a2486f73093401327495a5962a';
const BUILDER='sha256:dc26ae92c9fb15cf6b1d63e20f0944b2efe0f115b20e00be48fb23fceb061c54';
const stop=reason=>({decision:'STOP',reason,liveExecution:'DISABLED'});
const digest=s=>typeof s==='string'&&/^sha256:[a-f0-9]{64}$/.test(s);
const blobSha=s=>createHash('sha1').update('blob '+Buffer.byteLength(s,'utf8')+'\0'+s).digest('hex');
const srcLines=s=>s.split(/\r?\n/).filter(x=>/^COPY\s+(?!--from=)/.test(x));
function srcList(s){
 const inputs=srcLines(s).flatMap(line=>{const parts=line.replace(/^COPY\s+/,'').trim().split(/\s+/);return parts.slice(0,-1);});
 return [...new Set(inputs)];
}
function expectedIgnore(files) {
 const entries=new Set(['**']);
 for(const f of files){const p=f.split('/');
  for(let i=1;i<p.length;i++)entries.add('!'+p.slice(0,i).join('/')+'/');
  entries.add('!'+f);
 }
 return entries;
}
export function reviewBellSoftSource({dockerfile,dockerignore,legacyDockerfile}={}){
 if(![dockerfile,dockerignore,legacyDockerfile].every(s=>typeof s==='string'))return stop('MISSING_SOURCE');
 if(blobSha(legacyDockerfile)!==ORIGINAL_GIT_BLOB||!legacyDockerfile.includes('FROM '+ORIGINAL_BASE))
  return stop('ORIGINAL_DOCKERFILE_DRIFT');
 if(srcLines(dockerfile).join('\n')!==srcLines(legacyDockerfile).join('\n'))
  return stop('SOURCE_COPY_DRIFT');
 // Compare every instruction, including ENV and COPY --from. Substring
 // checks allowed extra build steps and activation flags to pass the review.
 const instructions=value=>value.split(/\r?\n/).map(line=>line.trim())
  .filter(line=>line&&!line.startsWith('#')).join('\n');
 const expectedRecipe='ARG OLDX_BELLSOFT_BASE_IMAGE\n'+legacyDockerfile
  .replace('FROM node:24-bookworm-slim AS dependencies',
   'FROM node:24-bookworm-slim@'+BUILDER+' AS dependencies')
  .replace('FROM '+ORIGINAL_BASE,'FROM ${OLDX_BELLSOFT_BASE_IMAGE} AS runtime')
  .replace(/^USER 65532:65532\r?\n/m,'');
 if(instructions(dockerfile)!==instructions(expectedRecipe))return stop('RECIPE_GUARD');
 const expected=expectedIgnore(srcList(legacyDockerfile));
 const present=dockerignore.split(/\r?\n/).map(s=>s.trim()).filter(s=>s&&!s.startsWith('#'));
 if(present[0]!=='**'||new Set(present).size!==expected.size||
   present.some(s=>!expected.has(s))||[...expected].some(s=>!present.includes(s)))
  return stop('CONTEXT_ALLOWLIST');
 return {decision:'SOURCE_SHAPE_ONLY',liveExecution:'DISABLED',allowlistedFileCount:srcList(legacyDockerfile).length};
}
// Caller-asserted flags are NOT cryptographic trust verification; never returns G2 PASS.
export function reviewBellSoftEvidenceShape(e={}){
 const m=/^docker\.io\/bellsoft\/hardened-nodejs@(sha256:[a-f0-9]{64})$/.exec(e.imageReference||'');
 if(!m||m[1]===OLD_SIGNED_BELLSOFT_INDEX)return stop('UNPATCHED_OR_UNPINNED_BASE');
 if(!digest(e.amd64ChildDigest)||e.amd64ChildDigest===m[1]||e.signedImageSubjectDigest!==m[1]||
   e.signedBomSubjectDigest!==m[1]||e.platform!=='linux/amd64'||
   e.imageSignatureVerified!==true||e.bomSignatureVerified!==true)
  return stop('PUBLISHER_SUBJECT_UNPROVEN');
 const g=/^(\d+)\.(\d+)\.(\d+)-r(\d+)$/.exec(e.glibcVersion||'');
 if(!g||Number(g[1])!==2||Number(g[2])<43||
   (Number(g[2])===43&&(Number(g[3])<0||(Number(g[3])===0&&Number(g[4])<14))))
  return stop('GLIBC_PATCH_UNPROVEN');
 const n=/^24\.(\d+)\.(\d+)$/.exec(e.nodeVersion||'');
 if(!n||Number(n[1])<12)return stop('NODE24_UNVERIFIED');
 if(!Number.isSafeInteger(e.effectiveUid)||e.effectiveUid<=0)return stop('NONROOT_UNVERIFIED');
 const gccSubject=e.gccEvidenceKind==='SIGNED_VENDOR_VEX'?m[1]:e.amd64ChildDigest;
 if(!digest(e.gccEvidenceDigest)||e.gccEvidenceSubjectDigest!==gccSubject||
   !['SIGNED_VENDOR_VEX','VERIFIED_EXACT_COMPILED_POSIX_MEMALIGN'].includes(e.gccEvidenceKind))
  return stop('GCC_BINARY_UNVERIFIED');
 return {decision:'EVIDENCE_SHAPE_ONLY',liveExecution:'DISABLED',
  requiresIndependentPublisherAndDerivedAttestation:true,baseIndexDigest:m[1]};
}
export function requireBellSoftImageExecution(){throw new Error('BELLSOFT_IMAGE_EXECUTION_DISABLED');}
