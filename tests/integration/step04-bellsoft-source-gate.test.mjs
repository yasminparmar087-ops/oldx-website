import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import test from 'node:test';
import {BELLSOFT_IMAGE_EXECUTION_ENABLED,OLD_SIGNED_BELLSOFT_INDEX,
  reviewBellSoftSource,reviewBellSoftEvidenceShape,requireBellSoftImageExecution}
  from '../../scripts/step04-bellsoft-source-gate.mjs';
const read=p=>readFileSync(new URL('../../'+p,import.meta.url),'utf8');
const recipe=()=>({dockerfile:read('Dockerfile.product-read.bellsoft'),
  dockerignore:read('Dockerfile.product-read.bellsoft.dockerignore'),
  legacyDockerfile:read('Dockerfile.product-read.distroless')});
const hash=c=>'sha256:'+c.repeat(64);
test('source-only candidate has exact old COPY allowlist and execution is hard disabled',()=>{
 const r=reviewBellSoftSource(recipe());assert.equal(r.decision,'SOURCE_SHAPE_ONLY');
 assert.ok(r.allowlistedFileCount>=27);assert.equal(BELLSOFT_IMAGE_EXECUTION_ENABLED,false);
 assert.throws(requireBellSoftImageExecution,/BELLSOFT_IMAGE_EXECUTION_DISABLED/);
});
test('detect old image drift, extra context files, mutable base and COPY changes',()=>{
 const r=recipe();
 assert.equal(reviewBellSoftSource({...r,dockerfile:r.dockerfile+'RUN echo unapproved\n'}).reason,'RECIPE_GUARD');
 assert.equal(reviewBellSoftSource({...r,dockerfile:r.dockerfile.replace('CMD [','ENV OLDX_PRODUCT_READ_ACTIVATE_STAGING=true\nCMD [')}).reason,'RECIPE_GUARD');
 assert.equal(reviewBellSoftSource({...r,legacyDockerfile:r.legacyDockerfile+'changed'}).reason,'ORIGINAL_DOCKERFILE_DRIFT');
 assert.equal(reviewBellSoftSource({...r,dockerignore:r.dockerignore+'!secrets.env\n'}).reason,'CONTEXT_ALLOWLIST');
 assert.equal(reviewBellSoftSource({...r,dockerfile:r.dockerfile+'COPY secrets.env ./\n'}).reason,'SOURCE_COPY_DRIFT');
 assert.equal(reviewBellSoftSource({...r,dockerfile:r.dockerfile.replace('ARG OLDX_BELLSOFT_BASE_IMAGE\n','ARG OLDX_BELLSOFT_BASE_IMAGE=latest\n')}).reason,'RECIPE_GUARD');
});
const e=()=>({imageReference:'docker.io/bellsoft/hardened-nodejs@'+hash('a'),amd64ChildDigest:hash('b'),
 signedImageSubjectDigest:hash('a'),signedBomSubjectDigest:hash('a'),
 imageSignatureVerified:true,bomSignatureVerified:true,platform:'linux/amd64',
 glibcVersion:'2.43.0-r14',nodeVersion:'24.12.0',effectiveUid:10001,
 gccEvidenceSubjectDigest:hash('b'),gccEvidenceDigest:hash('c'),gccEvidenceKind:'VERIFIED_EXACT_COMPILED_POSIX_MEMALIGN',
 npmBundledUndiciEvidenceKind:'EXACT_BASE_AMD64_PACKAGE_JSON',
 npmBundledUndiciEvidenceSubjectDigest:hash('b'),npmBundledUndiciVersion:'6.29.1'});
test('old r11 base, unpatched glibc, unsigned subject and unsupported GCC stay blocked',()=>{
 const x=e();
 assert.equal(reviewBellSoftEvidenceShape({...x,gccEvidenceSubjectDigest:hash('d')}).reason,'GCC_BINARY_UNVERIFIED');
 assert.equal(reviewBellSoftEvidenceShape({...x,imageReference:'docker.io/bellsoft/hardened-nodejs@'+OLD_SIGNED_BELLSOFT_INDEX}).reason,'UNPATCHED_OR_UNPINNED_BASE');
 assert.equal(reviewBellSoftEvidenceShape({...x,glibcVersion:'2.43.0-r11'}).reason,'GLIBC_PATCH_UNPROVEN');
 assert.equal(reviewBellSoftEvidenceShape({...x,signedBomSubjectDigest:hash('d')}).reason,'PUBLISHER_SUBJECT_UNPROVEN');
 assert.equal(reviewBellSoftEvidenceShape({...x,gccEvidenceKind:'UNKNOWN'}).reason,'GCC_BINARY_UNVERIFIED');
 assert.equal(reviewBellSoftEvidenceShape({...x,effectiveUid:0}).reason,'NONROOT_UNVERIFIED');
 assert.equal(reviewBellSoftEvidenceShape({...x,nodeVersion:'26.0.0'}).reason,'NODE24_UNVERIFIED');
});
test('even perfect-shaped metadata never claims G2 PASS',()=>{
 const r=reviewBellSoftEvidenceShape(e());
 assert.equal(r.decision,'EVIDENCE_SHAPE_ONLY');
 assert.equal(r.liveExecution,'DISABLED');assert.equal(r.requiresIndependentPublisherAndDerivedAttestation,true);
});

test('reject the observed bundled undici 6.29.0 and unverified base paths',()=>{
 const x=e();
 assert.equal(reviewBellSoftEvidenceShape({...x,npmBundledUndiciVersion:'6.29.0'}).reason,
   'BUNDLED_NPM_UNDICI_UNPATCHED');
 assert.equal(reviewBellSoftEvidenceShape({...x,npmBundledUndiciVersion:'6.28.99'}).reason,
   'BUNDLED_NPM_UNDICI_UNPATCHED');
 assert.equal(reviewBellSoftEvidenceShape({...x,npmBundledUndiciVersion:'7.0.0'}).reason,
   'BUNDLED_NPM_UNDICI_UNPATCHED');
 assert.equal(reviewBellSoftEvidenceShape({...x,npmBundledUndiciVersion:'8.0.0'}).reason,
   'BUNDLED_NPM_UNDICI_UNPATCHED');
 assert.equal(reviewBellSoftEvidenceShape({...x,npmBundledUndiciVersion:undefined}).reason,
   'BUNDLED_NPM_UNDICI_UNPATCHED');
 assert.equal(reviewBellSoftEvidenceShape({...x,npmBundledUndiciEvidenceSubjectDigest:hash('d')}).reason,
   'NPM_BUNDLE_LOCATION_UNVERIFIED');
 assert.equal(reviewBellSoftEvidenceShape({...x,npmBundledUndiciEvidenceKind:'SIGNED_BASE_SBOM_ONLY'}).reason,
   'NPM_BUNDLE_LOCATION_UNVERIFIED');
 assert.equal(reviewBellSoftEvidenceShape({...x,npmBundledUndiciVersion:'6.29.1'}).decision,
   'EVIDENCE_SHAPE_ONLY');
});
