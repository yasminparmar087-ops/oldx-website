/** Phase B acceptance contract. Import-only; hosted execution is disabled. */
import {isDeepStrictEqual} from 'node:util';
import {privateProduct} from './phase-b-firestore-typed-fixture-preview.mjs';
import {authUids, project} from './phase-b-http-contract-review.mjs';

const route = '/api/staging/marketplace/owner';
export const ownerReadAudience = 'https://oldx-owner-read-lqpaz3pd5a-el.a.run.app';
const audience = ownerReadAudience;
const invoker = 'oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com';
// The uniquely approved 2026-11-15 hosted session is complete/STOP and
// its tagged Cloud Run revision was rolled back. Retire the spent authorization.
// No future hosted request may reuse the historical process environment flag.
const LIVE_HOSTED_ACCEPTANCE_ENABLED = false;
export function requireHostedAcceptanceEnabled() {
  if (!LIVE_HOSTED_ACCEPTANCE_ENABLED) throw new Error('HOSTED_ACCEPTANCE_DISABLED');
}

// Diagnostic categories are fixed source-authored names. Never echo a caught
// error, response body, OAuth/Firebase token, endpoint or provider message.
// These categories describe a future failed attempt, not a successful probe.
const hostedErrorCategories = Object.freeze({
  INVOCATION_TOKEN_GENERATION_FAILED: 'TOKEN_MINT',
  INVOCATION_AUDIENCE_UNVERIFIED: 'TOKEN_AUDIENCE',
  INVOCATION_IDENTITY_UNVERIFIED: 'TOKEN_IDENTITY',
  INVALID_HOSTED_ACCEPTANCE_INPUT: 'INPUT_GUARD',
  INVALID_ACCEPTANCE_INPUT: 'INPUT_GUARD',
  FIXTURE_IDENTITY_UNVERIFIED: 'FIXTURE_IDENTITY_GUARD',
  UNAPPROVED_ACCEPTANCE_TARGET: 'TARGET_GUARD',
});
const hostedProbeCategories = Object.freeze({
  'disabled-health': 'PROBE_DISABLED_HEALTH',
  'disabled-owner': 'PROBE_DISABLED_OWNER',
  'invoker-denied': 'PROBE_INVOKER_DENIAL',
  owner: 'PROBE_OWNER',
  'foreign-buyer': 'PROBE_BUYER_DENIAL',
  'missing-firebase': 'PROBE_MISSING_FIREBASE',
  'invalid-firebase': 'PROBE_INVALID_FIREBASE',
  'wrong-project': 'PROBE_WRONG_PROJECT',
  'quota-limit': 'PROBE_QUOTA_LIMIT',
  'quota-failure': 'PROBE_QUOTA_FAILURE',
});
const allowedHostedCategories = new Set([
  ...Object.values(hostedErrorCategories), ...Object.values(hostedProbeCategories), 'UNCLASSIFIED',
]);
export function classifyHostedAcceptanceError(error) {
  const message = error instanceof Error ? error.message : '';
  if (Object.hasOwn(hostedErrorCategories, message)) return hostedErrorCategories[message];
  const prefix = 'ACCEPTANCE_STOPPED_';
  const probe = message.startsWith(prefix) ? message.slice(prefix.length) : '';
  return Object.hasOwn(hostedProbeCategories, probe) ? hostedProbeCategories[probe] : 'UNCLASSIFIED';
}
// Called only after all four remote resources are checked absent and the
// private journal's completion marker was written. It cannot certify cleanup
// from a naked exception or from a user-controlled string.
export function completedHostedFailureCategory(error) {
  return error instanceof Error &&
    error.message === 'HOSTED_ACCEPTANCE_FAILED_FIXTURES_ABSENT' &&
    allowedHostedCategories.has(error.hostedFailureCategory)
    ? error.hostedFailureCategory : null;
}
const jwt = /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/;
const fixtureRequest = JSON.stringify({kind: 'product', id: privateProduct.id, requestId: null});
const ownerResponse = {
  ok: true, id: privateProduct.id, revision: privateProduct.revision,
  profile: privateProduct.profile, published: false, publicationRevision: 0, receipt: null,
};

function checkedOrigin(origin, tag) {
  // Require the tag on the owner-verified staging service host. The operator must also
  // independently verify tag-to-revision and traffic mappings before any live run.
  const expected = ownerReadAudience.replace('https://', 'https://' + tag + '---');
  if (origin !== expected || !/^[a-z][a-z0-9-]{0,30}$/.test(tag)) throw new Error('UNAPPROVED_ACCEPTANCE_TARGET');
  return origin;
}

// The token is supplied in memory by a separately authorized keyless caller.
// Cloud Run, not this local claims check, authenticates the signature and IAM.
function checkGoogleInvocationAudience(token) {
  try {
    const parts = token.split('.');
    const claims = JSON.parse(Buffer.from(parts[1], 'base64url').toString('utf8'));
    if (parts.length === 3 && parts.every((part) => /^[A-Za-z0-9_-]+$/.test(part)) &&
        claims.aud === audience &&
        ['https://accounts.google.com', 'accounts.google.com'].includes(claims.iss) &&
        Number.isSafeInteger(claims.exp) && claims.exp > Date.now() / 1000) {
      if (claims.email === invoker &&
          claims.email_verified === true) return;
      throw new Error('INVOCATION_IDENTITY_UNVERIFIED');
    }
  } catch (error) {
    if (error.message === 'INVOCATION_IDENTITY_UNVERIFIED') throw error;
    // Never include token data in errors.
  }
  throw new Error('INVOCATION_AUDIENCE_UNVERIFIED');
}

export async function readBounded(response) {
  if (!response.body) return '';
  const chunks = [];
  let bytes = 0;
  for await (const chunk of response.body) {
    bytes += chunk.length;
    if (bytes > 32_768) throw new Error('RESPONSE_TOO_LARGE');
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString('utf8');
}

// Header hints are diagnostic only. An intermediary or application can emit
// a 403 and the same headers, so these hints cannot qualify a nonblank body.
export function inspectAnonymousDenial(response, body) {
  const blank = body.trim() === '';
  return {
    result: !response.redirected && response.status === 403 && blank ? 'MATCH' : 'BLOCKED',
    httpStatus: response.status,
    mediaType: ['text/html', 'text/plain', 'application/json'].find((type) =>
      response.headers.get('content-type')?.split(';')[0].trim().toLowerCase() === type) ?? 'OTHER_OR_ABSENT',
    body: body.length === 0 ? 'EMPTY' : blank ? 'WHITESPACE_ONLY' : 'NONEMPTY',
    serverHint: response.headers.get('server')?.trim().toLowerCase() === 'google frontend'
      ? 'GOOGLE_FRONTEND' : 'OTHER_OR_ABSENT',
    redirected: response.redirected,
  };
}

// Offline-only proof checker for a FUTURE separately approved test. Input
// `entries` must come from an authenticated, read-only Cloud Logging query
// matching the unique request trace; caller-supplied JSON is NOT proof.
// This does not invoke Cloud Run, query logs, or authorize a live session.
export function inspectCorrelatedHostedEdgeDenial({
  response, body, entries, traceId, startedAt, finishedAt, revision, tag,
} = {}) {
  try {
    if (typeof traceId !== 'string' || !/^[a-f0-9]{32}$/.test(traceId) ||
        typeof revision !== 'string' || !/^oldx-owner-read-[a-z0-9-]{1,47}$/.test(revision) ||
        typeof tag !== 'string' || !/^[a-z][a-z0-9-]{0,30}$/.test(tag) ||
        !Number.isSafeInteger(startedAt) || !Number.isSafeInteger(finishedAt) ||
        finishedAt < startedAt || finishedAt - startedAt > 20_000 ||
        typeof body !== 'string' || body.length < 1 || body.length > 32_768 ||
        !Array.isArray(entries) || entries.length !== 1 ||
        response?.status !== 403 || response.redirected !== false ||
        typeof response.headers?.get !== 'function' ||
        response.headers.get('content-type')?.split(';')[0].trim().toLowerCase() !== 'text/html') {
      return 'BLOCKED';
    }
    const echo = response.headers.get('x-cloud-trace-context');
    if (echo !== null &&
        !new RegExp('^' + traceId + '(?:/[0-9]+)?(?:;o=[01])?
  projectId, getOperatorAccessToken, ownerToken, buyerToken,
  disabledOrigin, enabledOrigin, enabledTag, timeout = (limit) => limit,
}, fetchRequest) {
  if (projectId !== project || typeof getOperatorAccessToken !== 'function' ||
      ![ownerToken, buyerToken].every((token) => typeof token === 'string' && jwt.test(token)) ||
      checkedOrigin(disabledOrigin, 'healthcheck') === checkedOrigin(enabledOrigin, enabledTag)) {
    throw new Error('INVALID_HOSTED_ACCEPTANCE_INPUT');
  }
  checkFirebaseIdentity(ownerToken, authUids[0]);
  checkFirebaseIdentity(buyerToken, authUids[1]);

  let googleToken;
  try {
    const signal = AbortSignal.timeout(timeout(15_000));
    const accessToken = await getOperatorAccessToken({signal});
    if (signal.aborted || typeof accessToken !== 'string' ||
        !/^[A-Za-z0-9._~+/-]{1,8192}={0,2}$/.test(accessToken)) throw new Error();
    const response = await fetchRequest(
      'https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/' + invoker + ':generateIdToken',
      {method: 'POST', redirect: 'error', signal, headers: {
        Authorization: 'Bearer ' + accessToken, 'Content-Type': 'application/json', 'X-Goog-User-Project': project,
      }, body: JSON.stringify({audience, includeEmail: true})});
    if (response.status !== 200) {
      await response.body?.cancel();
      throw new Error();
    }
    googleToken = JSON.parse(await readBounded(response)).token;
    if (signal.aborted || typeof googleToken !== 'string' || !jwt.test(googleToken)) throw new Error();
  } catch {
    throw new Error('INVOCATION_TOKEN_GENERATION_FAILED');
  }
  return runOwnerReadAcceptance({
    disabledOrigin, enabledOrigin, enabledTag, googleToken, ownerToken, buyerToken,
    async send({caseId, url, method, headers, body, signal}) {
      signal = AbortSignal.any([signal, AbortSignal.timeout(timeout(15_000))]);
      const response = await fetchRequest(url, {method, headers, body, signal, redirect: 'error'});
      const raw = await readBounded(response);
      if (signal.aborted) throw new Error('HOSTED_PROBE_TIMEOUT');
      if (caseId === 'invoker-denied') {
        // Only the status is consumed by the harness. Never discard unexpected
        // application data and count it as an invocation denial.
        if (inspectAnonymousDenial(response, raw).result !== 'MATCH') throw new Error('EDGE_DENIAL_UNVERIFIED');
        return {status: response.status};
      }
      return {status: response.status, cacheControl: response.headers.get('cache-control'), body: JSON.parse(raw)};
    },
  });
}

export async function runHostedOwnerReadAcceptance(options) {
  requireHostedAcceptanceEnabled();
  return runKeylessAcceptance(options, fetch);
}

export function simulateKeylessOwnerReadAcceptance(options, fakeFetch) {
  return runKeylessAcceptance(options, fakeFetch);
}

function checkFirebaseIdentity(token, uid) {
  try {
    const claims = JSON.parse(Buffer.from(token.split('.')[1], 'base64url').toString('utf8'));
    if (claims.sub === uid && claims.aud === project &&
        claims.iss === 'https://securetoken.google.com/' + project &&
        claims.firebase?.sign_in_provider === 'password' &&
        Number.isSafeInteger(claims.exp) && claims.exp > Date.now() / 1000) return;
  } catch {
    // Do not expose claims or parsing errors.
  }
  throw new Error('FIXTURE_IDENTITY_UNVERIFIED');
}

export async function runOwnerReadAcceptance({
  send, disabledOrigin, enabledOrigin, enabledTag, googleToken, ownerToken, buyerToken,
  wrongProjectToken, quotaMode = 'deferred',
}) {
  const disabled = checkedOrigin(disabledOrigin, 'healthcheck');
  const enabled = checkedOrigin(enabledOrigin, enabledTag);
  if (enabled === disabled || typeof send !== 'function' ||
      ![googleToken, ownerToken, buyerToken].every((token) =>
        typeof token === 'string' && jwt.test(token)) ||
      new Set([googleToken, ownerToken, buyerToken]).size !== 3 ||
      !['deferred', 'controlled'].includes(quotaMode) ||
      (wrongProjectToken !== undefined &&
        (typeof wrongProjectToken !== 'string' ||
          !jwt.test(wrongProjectToken) ||
          [googleToken, ownerToken, buyerToken].includes(wrongProjectToken)))) {
    throw new Error('INVALID_ACCEPTANCE_INPUT');
  }
  checkGoogleInvocationAudience(googleToken);
  checkFirebaseIdentity(ownerToken, authUids[0]);
  checkFirebaseIdentity(buyerToken, authUids[1]);

  const passed = [];
  const deadline = performance.now() + 60 * 60 * 1000;
  const failure = (code) => ({ok: false, error: {code}});
  async function probe(name, origin, status, expected, {firebase, invoke = true, health = false} = {}) {
    const headers = {};
    if (!health) headers['Content-Type'] = 'application/json';
    if (invoke) headers['X-Serverless-Authorization'] = 'Bearer ' + googleToken;
    if (firebase) headers.Authorization = 'Bearer ' + firebase;
    try {
      const remaining = deadline - performance.now();
      if (remaining < 1 || passed.length >= 200) throw new Error();
      const signal = AbortSignal.timeout(Math.floor(Math.min(remaining, 15_000)));
      const response = await send({
        caseId: name, url: origin + (health ? '/health' : route),
        method: health ? 'GET' : 'POST', headers, body: health ? undefined : fixtureRequest,
        redirect: 'error', signal,
      });
      if (signal.aborted || response.status !== status ||
          (expected !== undefined && (response.cacheControl !== 'private, no-store' ||
            !isDeepStrictEqual(response.body, expected))) ||
          (expected === undefined && response.body !== undefined)) throw new Error();
      passed.push(name);
    } catch {
      // Suppress response bodies, headers and transport errors.
      throw new Error('ACCEPTANCE_STOPPED_' + name);
    }
  }
  await probe('disabled-health', disabled, 200, {ok: true}, {health: true});
  await probe('disabled-owner', disabled, 503, failure('ENFORCEMENT_UNAVAILABLE'), {firebase: ownerToken});
  await probe('invoker-denied', enabled, 403, undefined, {invoke: false, health: true});
  await probe('owner', enabled, 200, ownerResponse, {firebase: ownerToken});
  await probe('foreign-buyer', enabled, 403, failure('DENIED'), {firebase: buyerToken});
  await probe('missing-firebase', enabled, 401, failure('AUTH_REQUIRED'));
  await probe('invalid-firebase', enabled, 401, failure('AUTH_REQUIRED'), {firebase: 'invalid.test.signature'});
  if (wrongProjectToken !== undefined) {
    await probe('wrong-project', enabled, 401, failure('AUTH_REQUIRED'), {firebase: wrongProjectToken});
  }
  if (quotaMode === 'controlled') {
    // Offline or an explicitly reviewed setup that controls quota state and
    // dependency failure independently. The harness does not induce cloud faults.
    await probe('quota-limit', enabled, 429, failure('RATE_LIMITED'), {firebase: ownerToken});
    await probe('quota-failure', enabled, 503, failure('UNAVAILABLE'), {firebase: ownerToken});
  }
  return {passed, deferred: [
    ...(wrongProjectToken === undefined ? ['wrong-project'] : []),
    ...(quotaMode === 'deferred' ? ['quota-limit', 'quota-failure'] : []),
  ]};
}
).test(echo)) return 'BLOCKED';
    const entry = entries[0];
    const time = Date.parse(entry?.timestamp);
    const expectedUrl = ownerReadAudience.replace('https://', 'https://' + tag + '---') + '/health';
    if (entry?.logName !== 'projects/oldx-staging/logs/run.googleapis.com%2Frequests' ||
        entry.trace !== 'projects/oldx-staging/traces/' + traceId ||
        entry.resource?.type !== 'cloud_run_revision' ||
        entry.resource?.labels?.project_id !== project ||
        entry.resource?.labels?.service_name !== 'oldx-owner-read' ||
        entry.resource?.labels?.revision_name !== revision ||
        entry.httpRequest?.requestMethod !== 'GET' ||
        entry.httpRequest?.requestUrl !== expectedUrl ||
        entry.httpRequest?.status !== 403 ||
        !Number.isFinite(time) || time < startedAt - 5000 || time > finishedAt + 5000 ||
        typeof entry.textPayload !== 'string' ||
        !/^The request was not authenticated\.(?:\s|$)/.test(entry.textPayload)) return 'BLOCKED';
    return 'MATCH';
  } catch {
    // No output contains body, trace, revision, logs or raw network errors.
    return 'BLOCKED';
  }
}

async function runKeylessAcceptance({
  projectId, getOperatorAccessToken, ownerToken, buyerToken,
  disabledOrigin, enabledOrigin, enabledTag, timeout = (limit) => limit,
}, fetchRequest) {
  if (projectId !== project || typeof getOperatorAccessToken !== 'function' ||
      ![ownerToken, buyerToken].every((token) => typeof token === 'string' && jwt.test(token)) ||
      checkedOrigin(disabledOrigin, 'healthcheck') === checkedOrigin(enabledOrigin, enabledTag)) {
    throw new Error('INVALID_HOSTED_ACCEPTANCE_INPUT');
  }
  checkFirebaseIdentity(ownerToken, authUids[0]);
  checkFirebaseIdentity(buyerToken, authUids[1]);

  let googleToken;
  try {
    const signal = AbortSignal.timeout(timeout(15_000));
    const accessToken = await getOperatorAccessToken({signal});
    if (signal.aborted || typeof accessToken !== 'string' ||
        !/^[A-Za-z0-9._~+/-]{1,8192}={0,2}$/.test(accessToken)) throw new Error();
    const response = await fetchRequest(
      'https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/' + invoker + ':generateIdToken',
      {method: 'POST', redirect: 'error', signal, headers: {
        Authorization: 'Bearer ' + accessToken, 'Content-Type': 'application/json', 'X-Goog-User-Project': project,
      }, body: JSON.stringify({audience, includeEmail: true})});
    if (response.status !== 200) {
      await response.body?.cancel();
      throw new Error();
    }
    googleToken = JSON.parse(await readBounded(response)).token;
    if (signal.aborted || typeof googleToken !== 'string' || !jwt.test(googleToken)) throw new Error();
  } catch {
    throw new Error('INVOCATION_TOKEN_GENERATION_FAILED');
  }
  return runOwnerReadAcceptance({
    disabledOrigin, enabledOrigin, enabledTag, googleToken, ownerToken, buyerToken,
    async send({caseId, url, method, headers, body, signal}) {
      signal = AbortSignal.any([signal, AbortSignal.timeout(timeout(15_000))]);
      const response = await fetchRequest(url, {method, headers, body, signal, redirect: 'error'});
      const raw = await readBounded(response);
      if (signal.aborted) throw new Error('HOSTED_PROBE_TIMEOUT');
      if (caseId === 'invoker-denied') {
        // Only the status is consumed by the harness. Never discard unexpected
        // application data and count it as an invocation denial.
        if (inspectAnonymousDenial(response, raw).result !== 'MATCH') throw new Error('EDGE_DENIAL_UNVERIFIED');
        return {status: response.status};
      }
      return {status: response.status, cacheControl: response.headers.get('cache-control'), body: JSON.parse(raw)};
    },
  });
}

export async function runHostedOwnerReadAcceptance(options) {
  requireHostedAcceptanceEnabled();
  return runKeylessAcceptance(options, fetch);
}

export function simulateKeylessOwnerReadAcceptance(options, fakeFetch) {
  return runKeylessAcceptance(options, fakeFetch);
}

function checkFirebaseIdentity(token, uid) {
  try {
    const claims = JSON.parse(Buffer.from(token.split('.')[1], 'base64url').toString('utf8'));
    if (claims.sub === uid && claims.aud === project &&
        claims.iss === 'https://securetoken.google.com/' + project &&
        claims.firebase?.sign_in_provider === 'password' &&
        Number.isSafeInteger(claims.exp) && claims.exp > Date.now() / 1000) return;
  } catch {
    // Do not expose claims or parsing errors.
  }
  throw new Error('FIXTURE_IDENTITY_UNVERIFIED');
}

export async function runOwnerReadAcceptance({
  send, disabledOrigin, enabledOrigin, enabledTag, googleToken, ownerToken, buyerToken,
  wrongProjectToken, quotaMode = 'deferred',
}) {
  const disabled = checkedOrigin(disabledOrigin, 'healthcheck');
  const enabled = checkedOrigin(enabledOrigin, enabledTag);
  if (enabled === disabled || typeof send !== 'function' ||
      ![googleToken, ownerToken, buyerToken].every((token) =>
        typeof token === 'string' && jwt.test(token)) ||
      new Set([googleToken, ownerToken, buyerToken]).size !== 3 ||
      !['deferred', 'controlled'].includes(quotaMode) ||
      (wrongProjectToken !== undefined &&
        (typeof wrongProjectToken !== 'string' ||
          !jwt.test(wrongProjectToken) ||
          [googleToken, ownerToken, buyerToken].includes(wrongProjectToken)))) {
    throw new Error('INVALID_ACCEPTANCE_INPUT');
  }
  checkGoogleInvocationAudience(googleToken);
  checkFirebaseIdentity(ownerToken, authUids[0]);
  checkFirebaseIdentity(buyerToken, authUids[1]);

  const passed = [];
  const deadline = performance.now() + 60 * 60 * 1000;
  const failure = (code) => ({ok: false, error: {code}});
  async function probe(name, origin, status, expected, {firebase, invoke = true, health = false} = {}) {
    const headers = {};
    if (!health) headers['Content-Type'] = 'application/json';
    if (invoke) headers['X-Serverless-Authorization'] = 'Bearer ' + googleToken;
    if (firebase) headers.Authorization = 'Bearer ' + firebase;
    try {
      const remaining = deadline - performance.now();
      if (remaining < 1 || passed.length >= 200) throw new Error();
      const signal = AbortSignal.timeout(Math.floor(Math.min(remaining, 15_000)));
      const response = await send({
        caseId: name, url: origin + (health ? '/health' : route),
        method: health ? 'GET' : 'POST', headers, body: health ? undefined : fixtureRequest,
        redirect: 'error', signal,
      });
      if (signal.aborted || response.status !== status ||
          (expected !== undefined && (response.cacheControl !== 'private, no-store' ||
            !isDeepStrictEqual(response.body, expected))) ||
          (expected === undefined && response.body !== undefined)) throw new Error();
      passed.push(name);
    } catch {
      // Suppress response bodies, headers and transport errors.
      throw new Error('ACCEPTANCE_STOPPED_' + name);
    }
  }
  await probe('disabled-health', disabled, 200, {ok: true}, {health: true});
  await probe('disabled-owner', disabled, 503, failure('ENFORCEMENT_UNAVAILABLE'), {firebase: ownerToken});
  await probe('invoker-denied', enabled, 403, undefined, {invoke: false, health: true});
  await probe('owner', enabled, 200, ownerResponse, {firebase: ownerToken});
  await probe('foreign-buyer', enabled, 403, failure('DENIED'), {firebase: buyerToken});
  await probe('missing-firebase', enabled, 401, failure('AUTH_REQUIRED'));
  await probe('invalid-firebase', enabled, 401, failure('AUTH_REQUIRED'), {firebase: 'invalid.test.signature'});
  if (wrongProjectToken !== undefined) {
    await probe('wrong-project', enabled, 401, failure('AUTH_REQUIRED'), {firebase: wrongProjectToken});
  }
  if (quotaMode === 'controlled') {
    // Offline or an explicitly reviewed setup that controls quota state and
    // dependency failure independently. The harness does not induce cloud faults.
    await probe('quota-limit', enabled, 429, failure('RATE_LIMITED'), {firebase: ownerToken});
    await probe('quota-failure', enabled, 503, failure('UNAVAILABLE'), {firebase: ownerToken});
  }
  return {passed, deferred: [
    ...(wrongProjectToken === undefined ? ['wrong-project'] : []),
    ...(quotaMode === 'deferred' ? ['quota-limit', 'quota-failure'] : []),
  ]};
}
