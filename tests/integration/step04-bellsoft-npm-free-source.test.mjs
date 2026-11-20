import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
import test from 'node:test';

const read = name => readFileSync(new URL('../../' + name, import.meta.url), 'utf8');
const frozen = read('Dockerfile.product-read.bellsoft');
const alternate = read('Dockerfile.product-read.bellsoft-npm-free');
const frozenIgnore = read('Dockerfile.product-read.bellsoft.dockerignore');
const candidateIgnore = read('Dockerfile.product-read.bellsoft-npm-free.dockerignore');
const marker = 'FROM ${OLDX_BELLSOFT_BASE_IMAGE} AS runtime\nWORKDIR /app\nENV NODE_ENV=production\n';
const pinnedMarker = 'FROM docker.io/bellsoft/hardened-nodejs@sha256:ef00ba8e634402e8dd3b374643fdbc178e876c7a312c9d55e4734efaa1e93d94 AS runtime\nWORKDIR /app\nENV NODE_ENV=production\n';
const oldHeader = "# OLDX BellSoft source-only candidate: no image build or deploy is authorized.\n# Must be given a NEW signed/patched Node24 linux/amd64 base digest explicitly;\n# previously signed fd67... has glibc r11 and is NOT acceptable for G2.\nARG OLDX_BELLSOFT_BASE_IMAGE\n";
const pinnedHeader = "# OLDX Step04 EXPERIMENTAL npm-free runtime, SOURCE-ONLY; no build or deploy authorized.\n# Pin the owner-verified signed BellSoft Node24 glibc-r14 OCI index immutable digest.\n# AMD64 child sha256:3862d478c2737d8386911b777d713e56a26e182f7c107e702be23a7b1cfe4799 was separately verified.\n# Only linux/amd64 is within the reviewed evidence; do not use a mutable tag or base override.\n";
const runLines = alternate.split(/\r?\n/).filter(s => s.startsWith('RUN '));
const scrubArgs = JSON.parse(runLines.at(-1).slice(4));
const scrub = scrubArgs[2];

test('source-only experimental recipe exactly extends frozen one, never changes app copies', () => {
  const extra = alternate.slice(alternate.indexOf(pinnedMarker) + pinnedMarker.length,
    alternate.indexOf('COPY --from=dependencies /app/node_modules'));
  assert.equal(alternate, frozen.replace(oldHeader, pinnedHeader).replace(marker, pinnedMarker + extra));
  assert.ok(!alternate.includes('ARG OLDX_BELLSOFT_BASE_IMAGE'));
  assert.equal(alternate.match(/^FROM .* AS runtime$/gm)?.length, 1);
  assert.equal(candidateIgnore, frozenIgnore, 'candidate must reuse the identical strict Docker context allowlist');
  assert.ok(candidateIgnore.startsWith('**\n')||candidateIgnore.includes('\n**\n'));

  assert.deepEqual(alternate.split('\n').filter(s=>s.startsWith('COPY ')),
    frozen.split('\n').filter(s=>s.startsWith('COPY ')));
  assert.equal(runLines.length, 2); // Original npm ci in builder, one runtime scrub
  assert.deepEqual(scrubArgs.slice(0,2), ['/usr/bin/node','-e']);
  assert.match(extra, /USER 0\nRUN \[/);
  assert.match(extra, /USER appuser\n/);
  assert.match(scrub, /undici\.version!=='6\.29\.0'/);
  assert.ok(!alternate.includes('OLDX_PRODUCT_READ_ACTIVATE_STAGING=true'));
  assert.ok(!alternate.includes('OLDX_PRODUCT_READ_STAGING_ADC=true'));
});
function simulate({npmName='npm', undiciName='undici', undiciVersion='6.29.0', uid=0, directory=true}={}) {
  const root='/usr/lib/node_modules/npm';
  const removed=[];
  const fakeFs={
    readFileSync(p){
      assert.ok([root+'/package.json',root+'/node_modules/undici/package.json'].includes(p));
      return JSON.stringify(p.endsWith('/undici/package.json')
        ? {name:undiciName,version:undiciVersion} : {name:npmName});
    },
    lstatSync(p){assert.equal(p,root);return {isDirectory:()=>directory};},
    rmSync(p,opts){
      assert.equal(p,root);assert.equal(opts.recursive,true); assert.equal(Object.keys(opts).length,1);
      removed.push(p);
    },
    existsSync(p){assert.equal(p,root);return removed.length===0;}
  };
  try {
    runInNewContext(scrub,{
      require:(n)=>{assert.equal(n,'node:fs');return fakeFs;},
      process:{getuid:()=>uid}
    },{timeout:1000});
    return {ok:true,removed};
  } catch(e) {return {ok:false,removed,error:e.message};}
}
test('bounded Node-only removal accepts exact vulnerable bundled npm and deletes only that tree',()=>{
  assert.deepEqual(simulate(),{ok:true,removed:['/usr/lib/node_modules/npm']});
});
test('fails closed on wrong npm identity, patched bundle, non-root or symlinked root',()=>{
  for(const change of [
    {npmName:'fake'}, {undiciName:'fake'}, {undiciVersion:'6.29.1'},
    {undiciVersion:'6.28.0'}, {uid:10001}, {directory:false}
  ]) {
    const x=simulate(change);
    assert.equal(x.ok,false);
    assert.deepEqual(x.removed,[]);
  }
});
