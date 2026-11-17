import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {mkdtempSync, rmSync, readFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import test from 'node:test';
import {reviewV2Candidate, reviewV2Manifest, requireV2LiveExecution,
  reviewV2OfflineConditionalCleanup, reviewV2OfflineProbe, rehearseV2AmbiguousCreateOffline,
  V2_LIVE_EXECUTION_ENABLED} from '../../scripts/phase-b-v2-session-source.mjs';

const moduleUrl = new URL('../../scripts/phase-b-v2-session-source.mjs', import.meta.url);
const source = readFileSync(moduleUrl, 'utf8');
const historicalImage = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-owner-read-step3-rc@sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc';
// Synthetic only: never claim the review-only new digest exists in Artifact Registry.
const image = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-v2-source-only@sha256:' + 'a'.repeat(64);
const candidate = {
  project: 'oldx-staging', region: 'asia-south1', service: 'oldx-owner-read',
  tag: 'ownerreadv2', image,
  runtime: 'oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com',
  invoker: 'oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com',
};
const seller = 'synthetic-seller-v2-abcdef123456';
const manifest = {authUids: [seller, 'synthetic-buyer-v2-abcdef123456'],
  firestoreDocs: ['marketplaceActors_v1/' + seller,
    'marketplacePrivate_v1/product_synthetic-v2-abcdef123456']};

test('V2 candidate is inert; retired targets, wrong project and invented approval cannot grant execution', () => {
  assert.equal(V2_LIVE_EXECUTION_ENABLED, false);
  assert.equal(reviewV2Candidate(candidate).decision, 'SOURCE_REVIEW_ONLY');
  assert.equal(reviewV2Candidate(candidate).ownerConsent, 'UNVERIFIED');
  assert.equal(reviewV2Candidate(candidate).liveExecution, 'DISABLED');
  for (const bad of [
    {...candidate, tag: 'ownerbuyertrial'}, {...candidate, tag: 'step3rc14'},
    {...candidate, tag: 'healthcheck'}, {...candidate, project: 'oldx-1c983'},
    {...candidate, image: historicalImage},
    {...candidate, image: image.replace('asia-south1-docker', 'us-central1-docker')},
    {...candidate, image: image.replace('a'.repeat(64), 'malformed-digest')},
    {...candidate, ownerApproved: true},
  ]) assert.equal(reviewV2Candidate(bad).decision, 'BLOCKED');
  assert.throws(() => requireV2LiveExecution(), /V2_LIVE_EXECUTION_DISABLED/);
  assert.doesNotMatch(source, /(?:from|require\()\s*['"](?:node:)?(?:http|https|child_process)/);
  assert.doesNotMatch(source, /\bfetch\s*\(/);
});

test('new V2 manifest uses distinct reviewed-format synthetic IDs and exact four-resource allowlist', () => {
  assert.equal(reviewV2Manifest(manifest), 'SOURCE_REVIEW_ONLY');
  for (const bad of [
    {...manifest, authUids: ['synthetic-seller-a', manifest.authUids[1]]},
    {...manifest, firestoreDocs: ['marketplaceActors_v1/synthetic-seller-a', manifest.firestoreDocs[1]]},
    {...manifest, firestoreDocs: [manifest.firestoreDocs[0], 'marketplacePrivate_v1/product_synthetic-phase-b-read-01']},
    {...manifest, extra: 'approved'},
    {authUids: manifest.authUids, firestoreDocs: manifest.firestoreDocs.slice(0, 1)},
  ]) assert.equal(reviewV2Manifest(bad), 'BLOCKED');
});

test('create-once private V2 journal never touches V1; unknown mutations remain STOP requiring owner', () => {
  const home = mkdtempSync(join(tmpdir(), 'oldx-v2-source-'));
  const code = [
    "import assert from 'node:assert/strict';",
    "import {existsSync,readFileSync,statSync} from 'node:fs';",
    "import {join} from 'node:path';",
    "import {homedir} from 'node:os';",
    'import {openV2LocalJournal} from ' + JSON.stringify(moduleUrl.href) + ';',
    'const manifest = ' + JSON.stringify(manifest) + ';',
    "const id = '00000000-0000-4000-8000-000000000003';",
    'const journal = openV2LocalJournal(id, manifest);',
    'assert.equal(typeof journal.complete, "undefined");',
    'assert.equal(typeof journal.cleanup, "undefined");',
    'journal.recordUnknown(manifest.authUids[0], "CREATE_UNKNOWN");',
    'assert.throws(() => journal.recordUnknown(manifest.authUids[0], "CREATE_UNKNOWN"), /V2_JOURNAL_STOP/);',
    'assert.throws(() => journal.recordUnknown(manifest.firestoreDocs[1], "DELETE_UNKNOWN"), /V2_JOURNAL_STOP/);',
    'assert.throws(() => journal.recordUnknown("synthetic-seller-a", "DELETE_UNKNOWN"), /V2_JOURNAL_STOP/);',
    'journal.close();',
    'assert.throws(() => openV2LocalJournal(id, manifest), /EEXIST/);',
    'const root = join(homedir(), ".oldx-phase-b-hosted-v2");',
    'const content = readFileSync(join(root,"journal.jsonl"), "utf8");',
    'assert.match(content, /CREATE_UNKNOWN/);',
    'assert.doesNotMatch(content, /ALL_ABSENT_VERIFIED/);',
    'assert.equal(statSync(root).mode & 0o077, 0);',
    'assert.equal(statSync(join(root,"journal.jsonl")).mode & 0o077, 0);',
    'assert.equal(existsSync(join(homedir(), ".oldx-phase-b-hosted-v1")), false);',
    'assert.equal(existsSync(join(homedir(), ".oldx-phase-b-fixtures-v1")), false);',
  ].join('\n');
  try {
    const run = spawnSync(process.execPath, ['--input-type=module', '-e', code],
      {encoding:'utf8', timeout:5000, env:{...process.env, HOME:home}});
    assert.equal(run.status, 0, run.stderr);
  } finally {
    rmSync(home, {recursive:true, force:true});
  }
});


test('offline reuse of V1 conditional receipt guard stops mismatched or unauthenticated provenance', () => {
  const id = '00000000-0000-4000-8000-000000000003';
  const root = 'projects/oldx-staging/databases/(default)/documents/';
  const receipt = {marker:id, name:root + manifest.firestoreDocs[1],
    createTime:'2026-11-15T00:00:00Z', updateTime:'2026-11-15T00:00:01Z'};
  const input = {candidate, manifest, sessionId:id,
    resource:manifest.firestoreDocs[1], original:receipt, observed:{...receipt}};
  assert.deepEqual(reviewV2OfflineConditionalCleanup(input), {
    decision:'SOURCE_RECEIPT_SHAPE_ONLY', provenance:'UNVERIFIED',
    liveExecution:'DISABLED', cloudAccess:'NONE',
  });
  for (const change of [
    {resource:'marketplacePrivate_v1/unapproved', original:receipt},
    {resource:manifest.firestoreDocs[0]},
    {original:{...receipt, name:undefined}},
    {observed:{...receipt, name:root + manifest.firestoreDocs[0]}},
    {observed:{...receipt, name:receipt.name.replace('(default)', 'other')}},
    {observed:{...receipt, name:receipt.name.replace('oldx-staging', 'other-project')}},
    {observed:{...receipt, updateTime:'2026-11-15T00:00:02Z'}},
    {original:{...receipt, exists:false}},
    {observed:{...receipt, exists:false}},
    {original:{...receipt, hasUnexpectedChanges:true}},
    {observed:{...receipt, hasUnexpectedChanges:true}},
    {original:{...receipt, marker:'some-other-session'}},
    {observed:undefined}, {candidate:{...candidate, tag:'ownerbuyertrial'}},
  ]) {
    assert.equal(reviewV2OfflineConditionalCleanup({...input,...change}).decision,
      'STOP_MANUAL_RECOVERY');
  }
});

test('V2 offline adapter reuses V1 attempted-request budget, records only UNKNOWN in new journal', () => {
  const home = mkdtempSync(join(tmpdir(), 'oldx-v2-rehearsal-'));
  const child = [
    "import assert from 'node:assert/strict';",
    "import {existsSync,readFileSync} from 'node:fs';",
    "import {homedir} from 'node:os';",
    "import {join} from 'node:path';",
    'import {rehearseV2AmbiguousCreateOffline} from ' + JSON.stringify(moduleUrl.href) + ';',
    'const candidate = ' + JSON.stringify(candidate) + ';',
    'const manifest = ' + JSON.stringify(manifest) + ';',
    "const id = '00000000-0000-4000-8000-000000000003';",
    'const input = {candidate,manifest,sessionId:id,resource:manifest.authUids[0]};',
    'assert.equal(rehearseV2AmbiguousCreateOffline({...input,resource:"synthetic-seller-a"}).decision,"BLOCKED");',
    'assert.equal(existsSync(join(homedir(), ".oldx-phase-b-hosted-v2")),false);',
    'assert.equal(rehearseV2AmbiguousCreateOffline(input).decision,"STOP_MANUAL_RECOVERY");',
    'const journal = readFileSync(join(homedir(), ".oldx-phase-b-hosted-v2","journal.jsonl"),"utf8");',
    'assert.match(journal,/CREATE_UNKNOWN/);',
    'assert.doesNotMatch(journal,/ALL_ABSENT_VERIFIED|DELETE_ACKNOWLEDGED/);',
    'assert.equal(existsSync(join(homedir(), ".oldx-phase-b-hosted-v1")),false);',
    'assert.equal(existsSync(join(homedir(), ".oldx-phase-b-fixtures-v1")),false);',
    'assert.throws(() => rehearseV2AmbiguousCreateOffline(input), /EEXIST/);',
  ].join('\n');
  try {
    const run = spawnSync(process.execPath, ['--input-type=module', '-e', child],
      {encoding:'utf8', timeout:5000, env:{...process.env, HOME:home}});
    assert.equal(run.status, 0, run.stderr);
  } finally {
    rmSync(home, {recursive:true, force:true});
  }
});

function probeDraft(targetChanges = {}, reviewChanges = {}) {
  const target = {...candidate, tag: 'v2-source-probe', revision: 'oldx-owner-read-v2probe',
    image: image.replace(/sha256:.+/, 'sha256:' + 'a'.repeat(64)),
    amd64Digest: 'sha256:' + 'b'.repeat(64), sourceSha: 'c'.repeat(40), ...targetChanges};
  const sessionId = '00000000-0000-4000-8000-000000000004';
  const issuedAt = Date.now() - 1_000;
  const evidence = Object.fromEntries(['tagAvailability', 'sourceImageProvenance', 'identity',
    'effectiveIam', 'financeStop', 'nineCveDisposition', 'b1', 'r1', 'r2', 'cleanup']
    .map((key, i) => [key, String(i + 1).padStart(64, '0')]));
  const review = {issuedAt, expiresAt: issuedAt + 180_000, maxGrossPaise: 100,
    evidence, ...reviewChanges};
  const {project, region, service, tag, revision, image: uri, amd64Digest, sourceSha, runtime, invoker} = target;
  review.scopeSha256 = createHash('sha256').update(JSON.stringify(['OLDX_V2_OFFLINE_PROBE',
    [project, region, service, tag, revision, uri, amd64Digest, sourceSha, runtime, invoker],
    sessionId, manifest.authUids, manifest.firestoreDocs, review.issuedAt, review.expiresAt,
    review.maxGrossPaise, Object.values(review.evidence)])).digest('hex');
  return {target, manifest, sessionId, review, journalState: 'UNUSED',
    probe: {scopeSha256: review.scopeSha256, status: 403, redirected: false, body: ''}};
}

test('V2 offline probe binds exact scope and accepts only a denial shape with execution OFF', () => {
  const draft = probeDraft();
  assert.deepEqual(reviewV2OfflineProbe(draft), {decision: 'SOURCE_PROBE_SHAPE_ONLY',
    ownerConsent: 'UNVERIFIED', liveExecution: 'DISABLED', cloudAccess: 'NONE'});
  assert.throws(() => requireV2LiveExecution(draft), /V2_LIVE_EXECUTION_DISABLED/);
  for (const change of [
    {ownerApproved: true},
    {target: {...draft.target, tag: 'v2-unbound'}},
    {probe: {...draft.probe, scopeSha256: 'd'.repeat(64)}},
    {probe: {...draft.probe, redirected: true}},
    {probe: {...draft.probe, body: 'unverified denial'}},
    {probe: {...draft.probe, body: ' '.repeat(32_769)}},
  ]) assert.equal(reviewV2OfflineProbe({...draft, ...change}).decision, 'BLOCKED');
});

test('V2 offline probe rejects retired targets, fixture replay and unsupported review evidence', () => {
  // Regression: even a freshly recomputed fingerprint must reject the old five-CVE field.
  const legacyEvidence = Object.fromEntries(Object.entries(probeDraft().review.evidence)
    .map(([key, value]) => [key === 'nineCveDisposition' ? 'fiveCveDisposition' : key, value]));
  for (const draft of [
    probeDraft({tag: 'ownerbuyertrial'}),
    probeDraft({revision: 'oldx-owner-read-00003-nus'}),
    probeDraft({revision: 'oldx-owner-read-00004-jus'}),
    probeDraft({image: historicalImage}),
    probeDraft({sourceSha: '2eebfa7a0c1a66d6c8563162aa5e612570f7a1e1'}),
    probeDraft({invoker: 'unapproved'}),
    probeDraft({}, {evidence: legacyEvidence}),
    probeDraft({}, {evidence: {...probeDraft().review.evidence, nineCveDisposition: true}}),
    probeDraft({}, {evidence: {...probeDraft().review.evidence, r1: probeDraft().review.evidence.r2}}),
    {...probeDraft(), manifest: {...manifest, authUids: ['synthetic-seller-a', manifest.authUids[1]]}},
  ]) assert.equal(reviewV2OfflineProbe(draft).decision, 'BLOCKED');
});

test('V2 offline probe stops on invalid expiry, insufficient cleanup time or unknown journal', () => {
  const now = Date.now();
  for (const review of [
    {issuedAt: now - 1_000, expiresAt: now - 1},
    {issuedAt: now + 60_000, expiresAt: now + 180_000},
    {issuedAt: now - 1_000, expiresAt: now + 20 * 60_000},
    {issuedAt: now - 1_000, expiresAt: now + 80_000},
    {maxGrossPaise: 0},
  ]) assert.equal(reviewV2OfflineProbe(probeDraft({}, review)).decision, 'BLOCKED');
  for (const journalState of ['CREATE_UNKNOWN', 'UPDATE_UNKNOWN', 'DELETE_UNKNOWN']) {
    assert.equal(reviewV2OfflineProbe({...probeDraft(), journalState}).decision,
      'STOP_MANUAL_RECOVERY');
  }
  assert.equal(reviewV2OfflineProbe({...probeDraft(), journalState: undefined}).decision, 'BLOCKED');
});
