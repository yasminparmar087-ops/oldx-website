/**
 * OLDX Phase B V2 — inert, source-only release boundary.
 *
 * This module cannot mint credentials, call any cloud API, deploy, or authorize
 * a live execution. V1 one-shot approvals and journals are deliberately separate.
 * Review of a candidate and a local journal are NOT owner operational consent.
 */
import {createHash} from 'node:crypto';
import {constants, closeSync, fstatSync, fsyncSync, mkdirSync, openSync, writeSync} from 'node:fs';
import {homedir} from 'node:os';
import {join} from 'node:path';
import {inspectAnonymousDenial} from './phase-b-owner-read-acceptance.mjs';
import {runtimeSessionBudget} from './phase-b-fixture-session-v1.mjs';
import {conditionalFixtureDelete, validFirestoreReceipt} from './phase-b-offline-cleanup-guard.mjs';

export const V2_LIVE_EXECUTION_ENABLED = false;
const PROJECT = 'oldx-staging';
const DOCUMENT_ROOT = `projects/${PROJECT}/databases/(default)/documents/`;
const REGION = 'asia-south1';
const SERVICE = 'oldx-owner-read';
// Exact source/index values plus a separately owner-verified private Registry URI.
// These constants are review-only: a URI match is NOT trusted SLSA provenance or deploy permission.
const V2_LOCAL_INDEX = 'sha256:93b70b8b09255194974bc46c7e5942c81531261b81224bd80fa575330f7572e4';
const V2_LOCAL_AMD64 = 'sha256:fde6b74beb8a62678fdc9df4598e5ef1affc2c8be0d89d3502938d4daac4fd68';
const V2_LOCAL_SOURCE = 'd13818acc66e1ffcca5e72209658e24129a1061d';
// Owner's one approved Registry copy: exact package+immutable index, not an arbitrary package with same digest.
const V2_PRIVATE_IMAGE = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-d13818-a1@' + V2_LOCAL_INDEX;
const IMAGE = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-owner-read-step3-rc@sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc';
const RUNTIME = 'oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com';
const INVOKER = 'oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com';
// B1 review is intentionally disabled-only; a future enabled trial needs NEW source and owner approval.
// This caller-supplied scope value does not verify actual deployed environment flags.
const B1_MODE = 'DEFAULT_OFF_503_ONLY';
// One intended private 0%-MAIN tag only; source review cannot verify provider tag availability.
const B1_TAG = 'ownerreadv2';
const RETIRED_TAGS = new Set(['ownerbuyertrial', 'healthcheck', 'step3rc14']);
const UUID = /^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i;
const SELLER = /^synthetic-seller-v2-[a-z0-9]{12,24}$/;
const BUYER = /^synthetic-buyer-v2-[a-z0-9]{12,24}$/;
const PRODUCT = /^marketplacePrivate_v1\/product_synthetic-v2-[a-z0-9]{12,24}$/;

function exactKeys(value, keys) {
  return value && typeof value === 'object' && !Array.isArray(value) &&
    Object.keys(value).length === keys.length && keys.every(key => Object.hasOwn(value, key));
}

export function reviewV2Candidate(candidate) {
  // Candidate review cannot prove that the tag is unused or that Cloud IAM,
  // revision resource limits, original traffic, or spend have not drifted.
  const keys = ['project', 'region', 'service', 'tag', 'image', 'runtime', 'invoker', 'b1Mode'];
  // Old registry image is historical, NOT the locally rescanned V2 source.
  // A new image digest is only a source shape until remote custody is proven.
  const imageDigest = typeof candidate?.image === 'string' && V2_IMAGE.exec(candidate.image)?.[1];
  const valid = exactKeys(candidate, keys) &&
    candidate.project === PROJECT && candidate.region === REGION &&
    candidate.service === SERVICE && candidate.image === V2_PRIVATE_IMAGE &&
    imageDigest === V2_LOCAL_INDEX &&
    !HISTORICAL_DIGESTS.has(imageDigest) &&
    candidate.runtime === RUNTIME && candidate.invoker === INVOKER &&
    candidate.b1Mode === B1_MODE && candidate.tag === B1_TAG &&
    typeof candidate.tag === 'string' && /^[a-z][a-z0-9-]{0,30}$/.test(candidate.tag) &&
    !RETIRED_TAGS.has(candidate.tag);
  return Object.freeze({
    decision: valid ? 'SOURCE_REVIEW_ONLY' : 'BLOCKED',
    ownerConsent: 'UNVERIFIED', liveExecution: 'DISABLED',
    tagAvailability: 'UNVERIFIED', immutableRegistryStatus: 'UNVERIFIED',
  });
}

export function requireV2LiveExecution() {
  // Never toggle by env var, CLI flag, or caller-supplied boolean.
  throw new Error('V2_LIVE_EXECUTION_DISABLED');
}

export function reviewV2Manifest(manifest) {
  const keys = ['authUids', 'firestoreDocs'];
  if (!exactKeys(manifest, keys) || !Array.isArray(manifest.authUids) ||
      !Array.isArray(manifest.firestoreDocs) || manifest.authUids.length !== 2 ||
      manifest.firestoreDocs.length !== 2) return 'BLOCKED';
  const [seller, buyer] = manifest.authUids;
  const [actor, product] = manifest.firestoreDocs;
  return typeof seller === 'string' && SELLER.test(seller) &&
    typeof buyer === 'string' && BUYER.test(buyer) && seller !== buyer &&
    actor === 'marketplaceActors_v1/' + seller &&
    typeof product === 'string' && PRODUCT.test(product) &&
    new Set([...manifest.authUids, ...manifest.firestoreDocs]).size === 4
    ? 'SOURCE_REVIEW_ONLY' : 'BLOCKED';
}

export function openV2LocalJournal(sessionId, manifest) {
  // Local-only create-once evidence; never a remote write, cleanup permit, or
  // independent ownership proof. This root cannot overlap either V1 journal.
  if (typeof sessionId !== 'string' || !UUID.test(sessionId) ||
      reviewV2Manifest(manifest) !== 'SOURCE_REVIEW_ONLY') {
    throw new Error('INVALID_V2_JOURNAL_INPUT');
  }
  const root = join(homedir(), '.oldx-phase-b-hosted-v2');
  mkdirSync(root, {mode: 0o700}); // EEXIST is a deliberate fail-stop; never reset.
  let dir;
  let fd;
  try {
    dir = openSync(root, constants.O_RDONLY | constants.O_DIRECTORY | constants.O_NOFOLLOW);
    const d = fstatSync(dir);
    if (!d.isDirectory() || d.uid !== process.getuid() || (d.mode & 0o077) !== 0) {
      throw new Error('UNSAFE_V2_JOURNAL_DIRECTORY');
    }
    fd = openSync(join(root, 'journal.jsonl'),
      constants.O_WRONLY | constants.O_CREAT | constants.O_EXCL | constants.O_NOFOLLOW, 0o600);
    const allowed = new Set([...manifest.authUids, ...manifest.firestoreDocs]);
    const append = value => {
      writeSync(fd, JSON.stringify({...value, at: new Date().toISOString()}) + '\n');
      fsyncSync(fd);
    };
    append({version: 3, project: PROJECT, database: '(default)', sessionId,
      authUids: [...manifest.authUids], firestoreDocs: [...manifest.firestoreDocs]});
    fsyncSync(dir);
    // Durably record the new directory entry as V1 did, without opening V1 evidence.
    const parent = openSync(homedir(), constants.O_RDONLY | constants.O_DIRECTORY | constants.O_NOFOLLOW);
    try { fsyncSync(parent); } finally { closeSync(parent); }
    let closed = false;
    const recorded = new Set();
    return Object.freeze({
      recordUnknown(resource, operation) {
        // V2 currently has NO provider-verified transition receipt; it may
        // record one CREATE intent per exact resource and nothing afterward.
        // UPDATE/DELETE and retries require a future independently reviewed
        // receipt/conditional transition before they can be enabled.
        if (closed || !allowed.has(resource) || operation !== 'CREATE_UNKNOWN' ||
            recorded.has(resource) || recorded.size >= 4) {
          throw new Error('V2_JOURNAL_STOP_REQUIRES_OWNER');
        }
        recorded.add(resource);
        append({resource, state: operation});
      },
      close() {
        if (closed) return;
        closed = true;
        closeSync(fd);
      },
      // Deliberately NO complete(), cleanup(), retry(), or live execution method:
      // future independent remote exact-ID proof is required before acceptance.
    });
  } catch (error) {
    if (fd !== undefined) closeSync(fd);
    throw error; // Preserve create-once residue on any failure, never delete.
  } finally {
    if (dir !== undefined) closeSync(dir);
  }
}


// This is the ONLY V1 reusable logic wired into V2 at this stage:
// a pure attempted-HTTP budget and a deterministic conditional receipt guard.
// Importing these functions does NOT run V1's hard-disabled CLI. This V2 module
// has no network/subprocess/token facility and cannot make a hosted request.
const stopped = () => Object.freeze({
  decision: 'STOP_MANUAL_RECOVERY', provenance: 'UNVERIFIED',
  liveExecution: 'DISABLED', cloudAccess: 'NONE',
});

// Caller-supplied receipt shapes are NOT authenticated provider evidence.
// Never return a deletion command or claim remote cleanup from this review.
export function reviewV2OfflineConditionalCleanup({candidate, manifest, sessionId, resource, original, observed} = {}) {
  if (reviewV2Candidate(candidate).decision !== 'SOURCE_REVIEW_ONLY' ||
      reviewV2Manifest(manifest) !== 'SOURCE_REVIEW_ONLY' ||
      typeof sessionId !== 'string' || !UUID.test(sessionId) ||
      typeof resource !== 'string' || !manifest.firestoreDocs.includes(resource)) return stopped();
  try {
    // Like V1 document evidence, bind both receipts to the exact database and path.
    const expectedName = DOCUMENT_ROOT + resource;
    if (original?.name !== expectedName || observed?.name !== expectedName) return stopped();
    // Existing V1 cleanup refuses an absent/changed resource. Preserve that
    // fail-stop behavior even for caller-supplied offline receipt shapes.
    if (original?.exists === false || observed?.exists === false ||
        original?.hasUnexpectedChanges === true || observed?.hasUnexpectedChanges === true) return stopped();
    if (!validFirestoreReceipt(original, sessionId)) return stopped();
    conditionalFixtureDelete(original, observed);
    return Object.freeze({
      decision: 'SOURCE_RECEIPT_SHAPE_ONLY', provenance: 'UNVERIFIED',
      liveExecution: 'DISABLED', cloudAccess: 'NONE',
    });
  } catch {
    return stopped();
  }
}

// The only side effect is a NEW private V2 file in a local HOME, never a cloud
// operation. Its create-once record deliberately ends at CREATE_UNKNOWN.
// The shared V1 budget guards ONE hypothetical request without performing it;
// it does NOT authorize or charge for actual HTTP or imply deletion occurred.
export function rehearseV2AmbiguousCreateOffline({candidate, manifest, sessionId, resource} = {}) {
  if (reviewV2Candidate(candidate).decision !== 'SOURCE_REVIEW_ONLY' ||
      reviewV2Manifest(manifest) !== 'SOURCE_REVIEW_ONLY' ||
      typeof sessionId !== 'string' || !UUID.test(sessionId) ||
      typeof resource !== 'string' ||
      ![...manifest.authUids, ...manifest.firestoreDocs].includes(resource)) {
    return Object.freeze({decision: 'BLOCKED', liveExecution: 'DISABLED', cloudAccess: 'NONE'});
  }
  const budget = runtimeSessionBudget(Date.now() + 240_000);
  budget.beforeMutation();
  budget.beforeHttpAttempt(); // hypothetical attempt only; no network call
  const journal = openV2LocalJournal(sessionId, manifest);
  try {
    journal.recordUnknown(resource, 'CREATE_UNKNOWN');
    return stopped(); // Ambiguous simulated create NEVER becomes verified.
  } finally {
    journal.close();
  }
}

const V2_TARGET_KEYS = ['project', 'region', 'service', 'tag', 'revision', 'image', 'amd64Digest',
  'sourceSha', 'runtime', 'invoker', 'b1Mode'];
const V2_REVIEW_KEYS = ['scopeSha256', 'issuedAt', 'expiresAt', 'maxGrossPaise', 'scanSubjectImage', 'evidence'];
const V2_EVIDENCE = ['tagAvailability', 'sourceImageProvenance', 'identity', 'effectiveIam',
  'financeStop', 'nineCveDisposition', 'b1', 'r1', 'r2', 'cleanup'];
const SHA256 = /^[a-f0-9]{64}$/;
const HISTORICAL_DIGESTS = new Set([
  IMAGE.split('@')[1],
  'sha256:eabe4207e307d1e487a30e4afd3abe8cda3792883a752864a5d6f80c45cd082c',
]);
const HISTORICAL_REVISIONS = new Set([
  'oldx-owner-read-00001-8kr', 'oldx-owner-read-00002-tid', 'oldx-owner-read-00003-nus',
  'oldx-owner-read-00004-jus', // Consumed V1 tagged trial; never reuse as V2.
]);
const V2_IMAGE = /^asia-south1-docker\.pkg\.dev\/oldx-staging\/oldx-staging-images\/[a-z0-9][a-z0-9._-]{0,127}@(sha256:[a-f0-9]{64})$/;

// These are offline evidence references, not authenticated consent. The scope
// fingerprint uses this documented field order, independent of JSON key order.
export function reviewV2OfflineProbe(input) {
  const {target, manifest, sessionId, review, journalState, probe} = input ?? {};
  const blocked = () => Object.freeze({
    decision: ['CREATE_UNKNOWN', 'UPDATE_UNKNOWN', 'DELETE_UNKNOWN'].includes(journalState)
      ? 'STOP_MANUAL_RECOVERY' : 'BLOCKED',
    ownerConsent: 'UNVERIFIED', liveExecution: 'DISABLED', cloudAccess: 'NONE',
  });
  if (!exactKeys(input, ['target', 'manifest', 'sessionId', 'review', 'journalState', 'probe']) ||
      journalState !== 'UNUSED' || !exactKeys(target, V2_TARGET_KEYS) ||
      reviewV2Manifest(manifest) !== 'SOURCE_REVIEW_ONLY' ||
      typeof sessionId !== 'string' || !UUID.test(sessionId) ||
      !exactKeys(review, V2_REVIEW_KEYS)) return blocked();

  const index = typeof target.image === 'string' && V2_IMAGE.exec(target.image)?.[1];
  if (target.project !== PROJECT || target.region !== REGION || target.service !== SERVICE ||
      target.runtime !== RUNTIME || target.invoker !== INVOKER ||
      target.b1Mode !== B1_MODE || target.tag !== B1_TAG ||
      typeof target.tag !== 'string' || !/^[a-z][a-z0-9-]{0,30}$/.test(target.tag) ||
      RETIRED_TAGS.has(target.tag) ||
      typeof target.revision !== 'string' || !/^oldx-owner-read-[a-z0-9-]{1,47}$/.test(target.revision) ||
      HISTORICAL_REVISIONS.has(target.revision) ||
      !index || index !== V2_LOCAL_INDEX || target.image !== V2_PRIVATE_IMAGE ||
      HISTORICAL_DIGESTS.has(index) ||
      typeof target.amd64Digest !== 'string' || target.amd64Digest !== V2_LOCAL_AMD64 ||
      !/^sha256:[a-f0-9]{64}$/.test(target.amd64Digest) || index === target.amd64Digest ||
      HISTORICAL_DIGESTS.has(target.amd64Digest) ||
      typeof target.sourceSha !== 'string' || target.sourceSha !== V2_LOCAL_SOURCE ||
      !/^[a-f0-9]{40}$/.test(target.sourceSha) ||
      target.sourceSha === '2eebfa7a0c1a66d6c8563162aa5e612570f7a1e1') return blocked();

  const {issuedAt, expiresAt, maxGrossPaise, scanSubjectImage, evidence, scopeSha256} = review;
  const now = Date.now();
  if (!Number.isSafeInteger(issuedAt) || !Number.isSafeInteger(expiresAt) ||
      issuedAt > now || expiresAt <= now || expiresAt - issuedAt > 20 * 60_000 ||
      // Planning envelope only: capped at the existing ₹100 Cloud Run-only
      // spend-cap amount. Not provider-enforced all-service cost containment.
      !Number.isSafeInteger(maxGrossPaise) || maxGrossPaise < 1 || maxGrossPaise > 10_000 ||
      // A scan claim for a NEW local-only npm-free image cannot support the OLD
      // private-registry index that this V2 review is expressly pinned to.
      // This is claimant-declared subject consistency, NOT authenticated
      // Grype provenance, artifact signature or a deployment authorization.
      scanSubjectImage !== target.image || scanSubjectImage !== V2_PRIVATE_IMAGE ||
      !exactKeys(evidence, V2_EVIDENCE) ||
      !V2_EVIDENCE.every(key => typeof evidence[key] === 'string' && SHA256.test(evidence[key])) ||
      new Set([evidence.b1, evidence.r1, evidence.r2, evidence.cleanup]).size !== 4) return blocked();

  // The OCI index is target.image; amd64Digest is its derived runnable child.
  // This digest binds the offline shape only; it authenticates no documents.
  const fingerprint = createHash('sha256').update(JSON.stringify([
    'OLDX_V2_OFFLINE_PROBE', V2_TARGET_KEYS.map(key => target[key]), sessionId,
    manifest.authUids, manifest.firestoreDocs, issuedAt, expiresAt, maxGrossPaise,
    scanSubjectImage, V2_EVIDENCE.map(key => evidence[key]),
  ])).digest('hex');
  if (scopeSha256 !== fingerprint || !exactKeys(probe, ['scopeSha256', 'status', 'redirected', 'body']) ||
      probe.scopeSha256 !== fingerprint || probe.status !== 403 || probe.redirected !== false ||
      typeof probe.body !== 'string' || Buffer.byteLength(probe.body) > 32_768) return blocked();

  try {
    // One synthetic attempted request; reuse V1's time and cleanup reserve.
    runtimeSessionBudget(expiresAt).beforeHttpAttempt();
    if (inspectAnonymousDenial({status: probe.status, redirected: probe.redirected,
      headers: new Headers()}, probe.body).result !== 'MATCH') return blocked();
    return Object.freeze({
      decision: 'SOURCE_PROBE_SHAPE_ONLY', ownerConsent: 'UNVERIFIED',
      liveExecution: 'DISABLED', cloudAccess: 'NONE',
    });
  } catch {
    return blocked();
  }
}
