/**
 * OLDX Phase B V2 — inert, source-only release boundary.
 *
 * This module cannot mint credentials, call any cloud API, deploy, or authorize
 * a live execution. V1 one-shot approvals and journals are deliberately separate.
 * Review of a candidate and a local journal are NOT owner operational consent.
 */
import {constants, closeSync, fstatSync, fsyncSync, mkdirSync, openSync, writeSync} from 'node:fs';
import {homedir} from 'node:os';
import {join} from 'node:path';
import {runtimeSessionBudget} from './phase-b-fixture-session-v1.mjs';
import {conditionalFixtureDelete, validFirestoreReceipt} from './phase-b-offline-cleanup-guard.mjs';

export const V2_LIVE_EXECUTION_ENABLED = false;
const PROJECT = 'oldx-staging';
const REGION = 'asia-south1';
const SERVICE = 'oldx-owner-read';
const IMAGE = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-owner-read-step3-rc@sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc';
const RUNTIME = 'oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com';
const INVOKER = 'oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com';
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
  const keys = ['project', 'region', 'service', 'tag', 'image', 'runtime', 'invoker'];
  const valid = exactKeys(candidate, keys) &&
    candidate.project === PROJECT && candidate.region === REGION &&
    candidate.service === SERVICE && candidate.image === IMAGE &&
    candidate.runtime === RUNTIME && candidate.invoker === INVOKER &&
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
