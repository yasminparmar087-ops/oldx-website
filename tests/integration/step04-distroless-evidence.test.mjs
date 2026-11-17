import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import test from 'node:test';
import {G2_IMAGE_EXECUTION_ENABLED, requireG2ImageExecution,
  reviewG2ImageEvidence, reviewG2ScratchCapacity} from '../../scripts/step04-distroless-evidence.mjs';

const bytes = value => Buffer.from(JSON.stringify(value));
const sha = value => 'sha256:' + createHash('sha256').update(value).digest('hex');
const media = 'application/vnd.oci.image.';
const recipe = readFileSync(new URL('../../Dockerfile.product-read.distroless', import.meta.url));
const startedAt = Date.parse('2026-11-17T00:00:00Z');
function evidence({architecture = 'amd64', dbAge = 60_000, ignored = [], dbValid = true} = {}) {
  const scope = {
    destination: 'PRIVATE_LOCAL_OCI', maxGrossPaise: 0, startedAt, expiresAt: startedAt + 900_000,
    retainUntil: startedAt + 86_400_000, maxBytes: 100_000, maxDbAgeMs: 86_400_000,
    sourceSha: 'a'.repeat(40), recipeDigest: sha(recipe), scratchAvailableBytes: 14 * 1024 ** 3,
    builderDigest: 'sha256:dc26ae92c9fb15cf6b1d63e20f0944b2efe0f115b20e00be48fb23fceb061c54',
    builderAmd64Digest: sha('builder-amd64'),
    scannerArchiveDigest: 'sha256:e9da18cc1429e786722e32161288103600efffd8e483c90761f90485bd1bec85',
    contextDigest: sha('tracked-context'), approvalDigest: sha('separate-scope'),
    scannerVersion: '0.121.3', scannerDigest: sha('scanner'), databaseDigest: sha('database'),
    scanPolicyDigest: sha('unfiltered'),
  };
  const config = bytes({os: 'linux', architecture, config: {User: '65532:65532'}});
  const manifest = bytes({schemaVersion: 2, mediaType: media + 'manifest.v1+json',
    config: {digest: sha(config), size: config.length},
    layers: [{digest: sha('layer'), size: 5}]});
  const index = bytes({schemaVersion: 2, mediaType: media + 'index.v1+json',
    manifests: [{digest: sha(manifest), size: manifest.length, mediaType: media + 'manifest.v1+json',
      platform: {os: 'linux', architecture}}]});
  const match = (id, severity) => ({vulnerability: {id, severity}, artifact: {name: 'fixture', version: '1'}});
  const report = bytes({
    source: {type: 'image', target: {manifestDigest: sha(manifest), imageID: sha(config), os: 'linux', architecture}},
    descriptor: {name: 'grype', version: scope.scannerVersion, timestamp: new Date(startedAt + 1_000),
      db: {status: {schemaVersion: '6.1.3', valid: dbValid, built: new Date(startedAt + 1_000 - dbAge)}}},
    matches: [match('CVE-2026-84243', 'High'), match('CVE-2026-0001', 'Critical')], ignoredMatches: ignored,
  });
  const pinned = recipe.toString('utf8').replace(/\r\n/g, '\n')
    .replace('node:24-bookworm-slim ', 'node:24-bookworm-slim@' + scope.builderDigest + ' ');
  const provenance = bytes({_type: 'https://in-toto.io/Statement/v1',
    predicateType: 'https://slsa.dev/provenance/v1', subject: [{digest: {sha256: sha(manifest).slice(7)}}]});
  const sbom = bytes({bomFormat: 'CycloneDX'}), runtimeLog = Buffer.from('offline fixture');
  const receipt = {...scope,
    buildkitDigest: 'sha256:97719ccb2ac86fb44fd36f330a6d302f63dddd5326f3ada24f9c05ccac0d9098',
    windowsArchiveDigest: sha('archive'), windowsReportDigest: sha(report),
    evidenceManifestDigest: sha('checksums'), windowsManifestDigest: sha('checksums'),
    dockerfile: 'Dockerfile.product-read.distroless', attempt: 1,
    base: recipe.toString('utf8').match(/^FROM (gcr\.io\/\S+)$/m)[1],
    originalRecipeDigest: sha(recipe), pinnedRecipeDigest: sha(pinned), provenanceDigest: sha(provenance),
    sbomDigest: sha(sbom), runtimeLogDigest: sha(runtimeLog), archiveDigest: sha('archive'), archiveBytes: 200,
    retainedBytes: 10_000, completedAt: startedAt + 2_000,
    indexDigest: sha(index), childDigest: sha(manifest), configDigest: sha(config),
    reportDigest: sha(report), scanScope: 'squashed',
    runtime: {node: '24.12.0', childDigest: sha(manifest), sharpTransform: true, uid: 65532, port: 8080,
      health: 200, defaultOff: 503, sigtermExit: 0, sigtermMs: 100},
  };
  return {scope, recipe, index, manifest, config, provenance, sbom, runtimeLog, report, receipt};
}

test('G2 offline evidence links a new retained amd64 image and keeps findings on HOLD', () => {
  const input = evidence();
  const result = reviewG2ImageEvidence(input);
  assert.equal(result.decision, 'HOLD_FINDINGS');
  assert.equal(result.indexDigest, sha(input.index));
  assert.equal(result.childDigest, sha(input.manifest));
  assert.equal(result.highMatches, 1);
  assert.equal(result.criticalMatches, 1);
  assert.equal(Object.keys(result.tracked).length, 5);
  assert.equal(result.tracked['CVE-2026-84243'], 1);
  assert.equal(result.signaturesAndCustody, 'REQUIRES_INDEPENDENT_VERIFICATION');
  assert.equal(G2_IMAGE_EXECUTION_ENABLED, false);
  assert.throws(() => requireG2ImageExecution(input), /G2_IMAGE_EXECUTION_DISABLED/);
});

test('G2 offline evidence stops on wrong image, expired cost scope or unretained capture', () => {
  const input = evidence();
  const check = (changes, reason) => assert.equal(reviewG2ImageEvidence({...input, ...changes}).reason, reason);
  const bytesFromSnapshot = Math.floor(9.6 * 1024 ** 3);
  assert.equal(reviewG2ScratchCapacity(bytesFromSnapshot).decision, 'STOP');
  assert.equal(reviewG2ScratchCapacity(bytesFromSnapshot).requiredBytes, 14 * 1024 ** 3);
  assert.equal(reviewG2ScratchCapacity(14 * 1024 ** 3).decision, 'CAPACITY_SHAPE_ONLY');
  check({scope: {...input.scope, scratchAvailableBytes: bytesFromSnapshot}}, 'DISK_BUDGET');
  check({scope: {...input.scope, builderDigest: sha('another-builder')}}, 'SCOPE');
  check({scope: {...input.scope, maxGrossPaise: 1}}, 'SCOPE');
  check({receipt: {...input.receipt, windowsManifestDigest: sha('wrong')}}, 'PROVENANCE_OR_RETENTION');
  check({scope: {...input.scope, expiresAt: input.scope.startedAt + 1_200_001}}, 'SCOPE');
  check({receipt: {...input.receipt, attempt: 2}}, 'PROVENANCE_OR_RETENTION');
  check({receipt: {...input.receipt, retainedBytes: 100_001}}, 'PROVENANCE_OR_RETENTION');
  check({receipt: {...input.receipt, pinnedRecipeDigest: sha('mutable')}}, 'PROVENANCE_OR_RETENTION');
  check({receipt: {...input.receipt, childDigest: sha('different')}}, 'DIGEST');
  assert.equal(reviewG2ImageEvidence(evidence({architecture:'arm64'})).reason, 'OCI_PLATFORM_OR_CONTENT');
});

test('G2 offline evidence rejects stale or suppressed scan and failed runtime checks', () => {
  assert.equal(reviewG2ImageEvidence(evidence({dbValid: false})).reason, 'SCAN');
  assert.equal(reviewG2ImageEvidence(evidence({dbAge: 86_400_001})).reason, 'SCAN');
  assert.equal(reviewG2ImageEvidence(evidence({ignored: [{}]})).reason, 'SCAN');
  const input = evidence();
  assert.equal(reviewG2ImageEvidence({...input, receipt: {...input.receipt,
    runtime: {...input.receipt.runtime, defaultOff: 200}}}).reason, 'RUNTIME');
});
