import assert from 'node:assert/strict';
import test from 'node:test';
import {runOwnerReadAcceptance, runHostedOwnerReadAcceptance, simulateKeylessOwnerReadAcceptance, inspectAnonymousDenial,
  classifyHostedAcceptanceError, completedHostedFailureCategory,
  inspectCorrelatedHostedEdgeDenial, reviewScopedHostedDenialLogShape} from '../../scripts/phase-b-owner-read-acceptance.mjs';
import {privateProduct} from '../../scripts/phase-b-firestore-typed-fixture-preview.mjs';
import {planOfflineV2LoggingProcess} from '../../scripts/phase-b-v2-logging-process-plan.mjs';

const googleToken = ('fake.' + Buffer.from(JSON.stringify({aud: 'https://oldx-owner-read-lqpaz3pd5a-el.a.run.app', iss: 'https://accounts.google.com', exp: 4102444800, email: 'oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com', email_verified: true})).toString('base64url') + '.token');
const root = '---oldx-owner-read-lqpaz3pd5a-el.a.run.app';
const firebaseToken = (sub) => 'fake.' + Buffer.from(JSON.stringify({sub, aud: 'oldx-staging', iss: 'https://securetoken.google.com/oldx-staging', exp: 4102444800, firebase: {sign_in_provider: 'password'}})).toString('base64url') + '.token';
const inputs = {
  disabledOrigin: 'https://healthcheck' + root,
  enabledOrigin: 'https://phase-b-acceptance' + root,
  enabledTag: 'phase-b-acceptance',
  googleToken: googleToken,
  ownerToken: firebaseToken('synthetic-seller-a'),
  buyerToken: firebaseToken('synthetic-buyer-b'),
};
const error = (code) => ({ok: false, error: {code}});
const responses = {
  'disabled-health': [200, {ok: true}],
  'disabled-owner': [503, error('ENFORCEMENT_UNAVAILABLE')],
  'invoker-denied': [403, undefined],
  owner: [200, {ok: true, id: privateProduct.id, revision: 1, profile: privateProduct.profile,
    published: false, publicationRevision: 0, receipt: null}],
  'foreign-buyer': [403, error('DENIED')],
  'missing-firebase': [401, error('AUTH_REQUIRED')],
  'invalid-firebase': [401, error('AUTH_REQUIRED')],
  'wrong-project': [401, error('AUTH_REQUIRED')],
  'quota-limit': [429, error('RATE_LIMITED')],
  'quota-failure': [503, error('UNAVAILABLE')],
};
function reply(caseId) {
  const [status, body] = responses[caseId];
  return {status, body, cacheControl: 'private, no-store'};
}

test('bounded matrix separates caller and Firebase identities and checks the exact fixture DTO', async () => {
  const seen = [];
  const firebase = {owner: inputs.ownerToken, 'foreign-buyer': inputs.buyerToken,
    'disabled-owner': inputs.ownerToken, 'invalid-firebase': 'invalid.test.signature',
    'wrong-project': 'fake.other.project', 'quota-limit': inputs.ownerToken, 'quota-failure': inputs.ownerToken};
  const result = await runOwnerReadAcceptance({...inputs, wrongProjectToken: 'fake.other.project',
    quotaMode: 'controlled', send(request) {
      const {caseId, headers, body} = request;
      seen.push(caseId);
      assert.equal(headers['X-Serverless-Authorization'],
        caseId === 'invoker-denied' ? undefined : 'Bearer ' + inputs.googleToken);
      assert.equal(headers.Authorization, firebase[caseId] ? 'Bearer ' + firebase[caseId] : undefined);
      assert.equal(request.redirect, 'error');
      assert.ok(request.signal instanceof AbortSignal);
      if (body) assert.deepEqual(JSON.parse(body), {kind: 'product', id: privateProduct.id, requestId: null});
      return reply(caseId);
    }});
  assert.deepEqual(seen, Object.keys(responses));
  assert.deepEqual(result, {passed: seen, deferred: []});
});

test('unexpected data, caching or a transport failure stops immediately and stays redacted', async () => {
  for (const issue of ['extra-data', 'cache', 'transport']) {
    const seen = [];
    await assert.rejects(runOwnerReadAcceptance({...inputs, send({caseId}) {
      seen.push(caseId);
      const response = reply(caseId);
      if (caseId !== 'owner') return response;
      if (issue === 'transport') throw new Error('raw upstream detail');
      if (issue === 'cache') return {...response, cacheControl: 'public'};
      return {...response, body: {...response.body, phaseBFixtureSessionId: 'unexpected'}};
    }}), {message: 'ACCEPTANCE_STOPPED_owner'});
    assert.deepEqual(seen, ['disabled-health', 'disabled-owner', 'invoker-denied', 'owner']);
  }
});

test('wrong origin or shared identity cannot send requests and optional probes report deferred', async () => {
  const wrongCaller = 'fake.' + Buffer.from(JSON.stringify({
    aud: 'https://oldx-owner-read-lqpaz3pd5a-el.a.run.app', iss: 'https://accounts.google.com',
    exp: 4102444800, email: 'other@example.invalid', email_verified: true,
  })).toString('base64url') + '.token';
  for (const [patch, expected] of [
    [{googleToken: wrongCaller}, /INVOCATION_IDENTITY_UNVERIFIED/],
    [{ownerToken: firebaseToken('unrelated-owner')}, /FIXTURE_IDENTITY_UNVERIFIED/],
  ]) {
    await assert.rejects(runOwnerReadAcceptance({...inputs, ...patch,
      send() { assert.fail('Unexpected request'); }}), expected);
  }
  await assert.rejects(runOwnerReadAcceptance({...inputs, googleToken: 'fake.other.audience',
    send() { assert.fail('Unexpected request'); }}), /INVOCATION_AUDIENCE_UNVERIFIED/);
  const send = ({caseId}) => reply(caseId);
  for (const patch of [{enabledOrigin: inputs.enabledOrigin + '/extra'}, {buyerToken: inputs.googleToken}]) {
    await assert.rejects(runOwnerReadAcceptance({...inputs, ...patch,
      send() { assert.fail('Unexpected request'); }}), /INVALID_ACCEPTANCE_INPUT|UNAPPROVED_ACCEPTANCE_TARGET/);
  }
  const result = await runOwnerReadAcceptance({...inputs, send});
  assert.deepEqual(result.deferred, ['wrong-project', 'quota-limit', 'quota-failure']);
});

const hosted = {...inputs, projectId: 'oldx-staging', getOperatorAccessToken: async () => 'synthetic-access-token'};

test('keyless transport mints once and keeps operator OAuth separate from hosted headers', async () => {
  const cases = Object.keys(responses).slice(0, 7);
  let requests = 0;
  const result = await simulateKeylessOwnerReadAcceptance(hosted, async (url, options) => {
    assert.equal(options.redirect, 'error');
    assert.ok(options.signal instanceof AbortSignal);
    if (requests++ === 0) {
      assert.equal(url, 'https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com:generateIdToken');
      assert.equal(options.method, 'POST');
      assert.equal(options.headers.Authorization, 'Bearer synthetic-access-token');
      assert.equal(options.headers['X-Goog-User-Project'], 'oldx-staging');
      assert.deepEqual(JSON.parse(options.body), {
        audience: 'https://oldx-owner-read-lqpaz3pd5a-el.a.run.app', includeEmail: true,
      });
      return Response.json({token: googleToken});
    }
    const name = cases[requests - 2];
    const origin = name.startsWith('disabled') ? inputs.disabledOrigin : inputs.enabledOrigin;
    const health = ['disabled-health', 'invoker-denied'].includes(name);
    assert.equal(url, origin + (health ? '/health' : '/api/staging/marketplace/owner'));
    assert.equal(options.method, health ? 'GET' : 'POST');
    assert.equal(options.headers['X-Serverless-Authorization'], name === 'invoker-denied' ? undefined : 'Bearer ' + googleToken);
    const firebase = {'disabled-owner': inputs.ownerToken, owner: inputs.ownerToken,
      'foreign-buyer': inputs.buyerToken, 'invalid-firebase': 'invalid.test.signature'}[name];
    assert.equal(options.headers.Authorization, firebase ? 'Bearer ' + firebase : undefined);
    const [status, body] = responses[name];
    return body === undefined ? new Response(null, {status}) :
      Response.json(body, {status, headers: {'cache-control': 'private, no-store'}});
  });
  assert.equal(requests, 8);
  assert.deepEqual(result.passed, cases);
});

test('hosted gate and invalid project or fixture identity stop before credentials', async () => {
  const options = {...hosted, getOperatorAccessToken() { assert.fail('Credential callback reached'); }};
  const noFetch = () => assert.fail('Fetch reached');
  await assert.rejects(runHostedOwnerReadAcceptance(options), {message: 'HOSTED_ACCEPTANCE_DISABLED'});
  await assert.rejects(simulateKeylessOwnerReadAcceptance({...options, projectId: 'another-project'}, noFetch),
    {message: 'INVALID_HOSTED_ACCEPTANCE_INPUT'});
  await assert.rejects(simulateKeylessOwnerReadAcceptance({...options, buyerToken: inputs.ownerToken}, noFetch),
    {message: 'FIXTURE_IDENTITY_UNVERIFIED'});
});

test('mint denial, timeout, wrong claims and malformed responses stop without retry', async () => {
  const cases = [
    [() => new Response('private detail', {status: 403}), 'INVOCATION_TOKEN_GENERATION_FAILED'],
    [() => { throw new DOMException('private timeout detail', 'TimeoutError'); }, 'INVOCATION_TOKEN_GENERATION_FAILED'],
    [() => new Response('{'), 'INVOCATION_TOKEN_GENERATION_FAILED'],
    [() => Response.json({token: 'fake.invalid.token'}), 'INVOCATION_AUDIENCE_UNVERIFIED'],
    [() => {
      const claims = JSON.parse(Buffer.from(googleToken.split('.')[1], 'base64url'));
      claims.email = 'wrong@example.invalid';
      return Response.json({token: 'fake.' + Buffer.from(JSON.stringify(claims)).toString('base64url') + '.token'});
    }, 'INVOCATION_IDENTITY_UNVERIFIED'],
  ];
  for (const [respond, message] of cases) {
    let count = 0;
    await assert.rejects(simulateKeylessOwnerReadAcceptance(hosted, () => {
      count++;
      return respond();
    }), {message});
    assert.equal(count, 1);
  }
});

test('HTML 403 cannot be called verified anonymous denial without independent edge evidence', () => {
  const html = new Response('<html>Not authenticated</html>', {
    status: 403, headers: {'content-type': 'text/html', server: 'Google Frontend'},
  });
  const observed = inspectAnonymousDenial(html, '<html>Not authenticated</html>');
  assert.equal(observed.httpStatus, 403);
  assert.equal(observed.mediaType, 'text/html');
  assert.equal(observed.body, 'NONEMPTY');
  assert.equal(observed.result, 'BLOCKED');
  const empty = inspectAnonymousDenial(new Response(null, {status: 403}), '');
  assert.equal(empty.result, 'MATCH');
  const fakeApp = inspectAnonymousDenial(
    Response.json({ok: false, error: {code: 'DENIED'}}, {status: 403}),
    JSON.stringify({ok: false, error: {code: 'DENIED'}}));
  assert.equal(fakeApp.result, 'BLOCKED');
  // A status/header-shaped response is not Google Cloud Run IAM proof.
  // The historical preflight used an independent request-log correlation.
});

test('hosted failures expose only exact allowlisted stages after verified cleanup', () => {
  const names = {
    INVOCATION_TOKEN_GENERATION_FAILED: 'TOKEN_MINT',
    INVOCATION_AUDIENCE_UNVERIFIED: 'TOKEN_AUDIENCE',
    INVOCATION_IDENTITY_UNVERIFIED: 'TOKEN_IDENTITY',
    INVALID_HOSTED_ACCEPTANCE_INPUT: 'INPUT_GUARD',
    FIXTURE_IDENTITY_UNVERIFIED: 'FIXTURE_IDENTITY_GUARD',
    'ACCEPTANCE_STOPPED_invoker-denied': 'PROBE_INVOKER_DENIAL',
    ACCEPTANCE_STOPPED_owner: 'PROBE_OWNER',
    'ACCEPTANCE_STOPPED_foreign-buyer': 'PROBE_BUYER_DENIAL',
    'ACCEPTANCE_STOPPED_quota-limit': 'PROBE_QUOTA_LIMIT',
  };
  for (const [message, expected] of Object.entries(names)) {
    assert.equal(classifyHostedAcceptanceError(new Error(message)), expected);
    const verified = new Error('HOSTED_ACCEPTANCE_FAILED_FIXTURES_ABSENT');
    Object.defineProperty(verified, 'hostedFailureCategory', {value: expected});
    assert.equal(completedHostedFailureCategory(verified), expected);
    assert.equal(completedHostedFailureCategory(new Error(message)), null);
  }
  for (const hostile of [
    new Error('ACCEPTANCE_STOPPED_owner private-token'), new Error('ACCEPTANCE_STOPPED_unknown'),
    new Error('HTTP 403 username@example.com'), new Error('INVOCATION_TOKEN_GENERATION_FAILED\nsecret'),
    new Error('HOSTED_ACCEPTANCE_FAILED_FIXTURES_ABSENT'),
    {message: 'ACCEPTANCE_STOPPED_owner'}, null,
  ]) {
    assert.equal(classifyHostedAcceptanceError(hostile), 'UNCLASSIFIED');
    assert.equal(completedHostedFailureCategory(hostile), null);
  }
  const forged = new Error('HOSTED_ACCEPTANCE_FAILED_FIXTURES_ABSENT');
  forged.hostedFailureCategory = 'PROBE_OWNER private data';
  assert.equal(completedHostedFailureCategory(forged), null);
  assert.equal(completedHostedFailureCategory(
    new Error('HOSTED_ACCEPTANCE_FAILED_FIXTURES_ABSENT')), null);
});

test('independent Cloud Run trace/log evidence can qualify a hosted HTML 403 only with exact matching metadata', () => {
  const traceId = 'abcdef1234567890abcdef1234567890';
  const at = Date.parse('2026-11-15T09:30:00.000Z');
  const url = 'https://ownerbuyertrial---oldx-owner-read-lqpaz3pd5a-el.a.run.app/health';
  const entry = {
    logName: 'projects/oldx-staging/logs/run.googleapis.com%2Frequests',
    trace: 'projects/oldx-staging/traces/' + traceId,
    resource: {type: 'cloud_run_revision', labels: {
      project_id: 'oldx-staging', service_name: 'oldx-owner-read',
      revision_name: 'oldx-owner-read-00004-jus',
    }},
    httpRequest: {requestMethod: 'GET', requestUrl: url, status: 403},
    timestamp: new Date(at + 500).toISOString(),
    textPayload: 'The request was not authenticated. Request denied.',
  };
  const html = '<html>Not authenticated</html>';
  const response = new Response(html, {status: 403, headers: {
    'content-type': 'text/html; charset=utf-8',
    'x-cloud-trace-context': traceId + '/1;o=1',
  }});
  const input = {
    response, body: html, entries: [entry], traceId,
    startedAt: at, finishedAt: at + 1000,
    revision: 'oldx-owner-read-00004-jus', tag: 'ownerbuyertrial',
  };
  assert.equal(inspectCorrelatedHostedEdgeDenial(input), 'MATCH');
  const fail = (change) => assert.equal(
    inspectCorrelatedHostedEdgeDenial({...input, ...change}), 'BLOCKED');
  fail({entries: []});
  fail({entries: [entry, entry]});
  fail({traceId: 'wrong'});
  fail({revision: 'oldx-owner-read-00003-nus'});
  fail({tag: 'healthcheck'});
  fail({body: ''});
  fail({finishedAt: at + 30000});
  fail({response: new Response('denied', {status: 403, headers: {
    'content-type': 'application/json',
  }})});
  fail({response: new Response(html, {status: 401, headers: {'content-type': 'text/html'}})});
  fail({response: new Response(html, {status: 403, headers: {
    'content-type': 'text/html', 'x-cloud-trace-context': '0'.repeat(32),
  }})});
  for (const mutate of [
    {trace: 'projects/oldx-staging/traces/' + '0'.repeat(32)},
    {logName: 'projects/oldx-staging/logs/run.googleapis.com%2Fstderr'},
    {resource: {...entry.resource, labels: {...entry.resource.labels, revision_name: 'wrong'}}},
    {resource: {...entry.resource, labels: {...entry.resource.labels, project_id: 'production'}}},
    {httpRequest: {...entry.httpRequest, requestUrl: url + '/other'}},
    {httpRequest: {...entry.httpRequest, status: 200}},
    {httpRequest: {...entry.httpRequest, requestMethod: 'POST'}},
    {timestamp: new Date(at - 6000).toISOString()},
    {textPayload: 'Application returned forbidden'},
  ]) fail({entries: [{...entry, ...mutate}]});
  // This pure comparison alone never attests where entries came from.
  // Only a future authenticated, scoped logging read can supply that provenance.
});

test('scoped Cloud Logging adapter accepts only matching mock shape, never live proof', async () => {
  const traceId = '0123456789abcdef0123456789abcdef';
  const startedAt = Date.parse('2026-11-15T09:30:00Z');
  const finishedAt = startedAt + 1000;
  const tag = 'futuretrial';
  const revision = 'oldx-owner-read-00006-abc';
  const url = 'https://' + tag + '---oldx-owner-read-lqpaz3pd5a-el.a.run.app/health';
  const entry = {
    logName: 'projects/oldx-staging/logs/run.googleapis.com%2Frequests',
    trace: 'projects/oldx-staging/traces/' + traceId,
    resource: {type: 'cloud_run_revision', labels: {
      project_id: 'oldx-staging', service_name: 'oldx-owner-read', revision_name: revision,
    }},
    httpRequest: {requestMethod: 'GET', requestUrl: url, status: 403},
    timestamp: new Date(startedAt + 500).toISOString(),
    textPayload: 'The request was not authenticated. Request denied.',
  };
  const body = '<html>unauthenticated</html>';
  const response = new Response(body, {status: 403, headers: {
    'content-type': 'text/html', 'x-cloud-trace-context': traceId + '/1;o=0',
  }});
  const calls = [];
  let processPlan;
  const read = async (...args) => {
    calls.push(args);
    processPlan = planOfflineV2LoggingProcess(...args);
    return JSON.stringify([entry]);
  };
  const input = {read, response, body, traceId, startedAt, finishedAt, tag, revision};
  assert.equal(await reviewScopedHostedDenialLogShape(input), 'SHAPE_MATCH_ONLY');
  assert.equal(calls.length, 1);
  assert.ok(calls[0].at(-1)?.signal instanceof AbortSignal);
  assert.equal(calls[0].at(-1).signal.aborted, true);
  assert.equal(processPlan.decision, 'OFFLINE_PLAN_ONLY');
  assert.equal(processPlan.executable, false);
  assert.equal(processPlan.provenance, 'UNVERIFIED');
  assert.equal(processPlan.file, 'gcloud');
  assert.equal(processPlan.processOptions.shell, false);
  assert.equal(processPlan.processOptions.timeout, 1500);
  assert.equal(processPlan.processOptions.maxBuffer, 65536);
  assert.equal(processPlan.processOptions.killSignal, 'SIGKILL');
  assert.deepEqual(calls[0].slice(0, -1), [
    'logging', 'read',
    'trace="projects/oldx-staging/traces/' + traceId + '" AND ' +
      'timestamp>="' + new Date(startedAt - 5000).toISOString() + '" AND ' +
      'timestamp<="' + new Date(finishedAt + 5000).toISOString() + '"',
    '--project=oldx-staging', '--account=yasminparmar087@gmail.com',
    '--limit=2', '--format=json', '--quiet',
  ]);

  // Invalid/mismatched requests must not make even a mocked Logging call.
  calls.length = 0;
  for (const patch of [
    {traceId: 'injected" OR true'}, {startedAt: '2026-11-15T09:30Z'},
    {finishedAt: finishedAt + 20000}, {revision: 'production'},
    {tag: 'no/valid/tag'}, {body: ''},
    {readTimeoutMs: 0}, {readTimeoutMs: -1}, {readTimeoutMs: 2001},
    {readTimeoutMs: Infinity}, {readTimeoutMs: '100'},
    {tag: 'ownerbuyertrial'}, {tag: 'healthcheck'}, {tag: 'step3rc14'},
    {revision: 'oldx-owner-read-00001-8kr'},
    {revision: 'oldx-owner-read-00002-tid'},
    {revision: 'oldx-owner-read-00003-nus'},
    {revision: 'oldx-owner-read-00004-jus'},
    {response: new Response('denied', {status: 401, headers: {'content-type': 'text/html'}})},
    {response: Response.json({error: 'denied'}, {status: 403})},
  ]) assert.equal(await reviewScopedHostedDenialLogShape({...input, ...patch}), 'BLOCKED');
  assert.equal(calls.length, 0);
  for (const reply of [
    JSON.stringify([]), JSON.stringify([entry, entry]),
    JSON.stringify([{...entry, httpRequest: {...entry.httpRequest, status: 200}}]),
  ]) assert.equal(await reviewScopedHostedDenialLogShape({
    ...input, read: () => reply,
  }), 'BLOCKED');
  for (const result of ['{bad', '{}', 'x'.repeat(65_537)]) assert.equal(
    await reviewScopedHostedDenialLogShape({...input, read: () => result}), 'UNVERIFIED');
  assert.equal(await reviewScopedHostedDenialLogShape({
    ...input, read: () => { throw new Error('sensitive provider details'); },
  }), 'UNVERIFIED');
  assert.equal(await reviewScopedHostedDenialLogShape({...input, read: undefined}), 'BLOCKED');

  // The caller receives a bounded decision even if an async log reader hangs.
  // Cancellation is advisory to the injected reader; never promise to kill
  // a subprocess that does not cooperate.
  let released;
  let signal;
  const pending = new Promise(resolve => { released = resolve; });
  const began = Date.now();
  const timeoutResult = await reviewScopedHostedDenialLogShape({
    ...input, readTimeoutMs: 25,
    read: (...args) => { signal = args.at(-1).signal; return pending; },
  });
  assert.equal(timeoutResult, 'UNVERIFIED');
  assert.ok(signal instanceof AbortSignal);
  assert.equal(signal.aborted, true);
  assert.ok(Date.now() - began < 1000);
  // A late forged "matching" log cannot change a completed STOP verdict.
  released(JSON.stringify([entry]));
  await Promise.resolve();
  assert.equal(timeoutResult, 'UNVERIFIED');

  const abortResult = await reviewScopedHostedDenialLogShape({
    ...input, readTimeoutMs: 25,
    read: (...args) => new Promise((_resolve, reject) => {
      const signaled = args.at(-1).signal;
      signaled.addEventListener('abort', () => reject(new Error('private provider error')),
        {once: true});
    }),
  });
  assert.equal(abortResult, 'UNVERIFIED');
});

test('V2 CLI process plan blocks identities, extra flags, unbounded filters and expired signals', () => {
  const abort = new AbortController();
  const trace = 'a'.repeat(32);
  const from = '2026-11-15T09:29:55.000Z';
  const until = '2026-11-15T09:30:06.000Z';
  const filter = 'trace="projects/oldx-staging/traces/' + trace + '" AND ' +
    'timestamp>="' + from + '" AND timestamp<="' + until + '"';
  const exact = [
    'logging', 'read', filter,
    '--project=oldx-staging', '--account=yasminparmar087@gmail.com',
    '--limit=2', '--format=json', '--quiet', {signal: abort.signal},
  ];
  const plan = planOfflineV2LoggingProcess(...exact);
  assert.equal(plan.decision, 'OFFLINE_PLAN_ONLY');
  assert.equal(plan.executable, false);
  assert.equal(plan.provenance, 'UNVERIFIED');
  assert.equal(plan.file, 'gcloud');
  assert.deepEqual([...plan.argv], exact.slice(0, 8));
  assert.ok(Object.isFrozen(plan.argv));
  assert.ok(Object.isFrozen(plan.processOptions));
  assert.equal(plan.processOptions.timeout, 1500);
  assert.equal(plan.processOptions.maxBuffer, 65536);
  assert.equal(plan.processOptions.shell, false);
  assert.equal(plan.processOptions.signal, abort.signal);

  const blocked = patch => assert.equal(
    planOfflineV2LoggingProcess(...exact.map((v, i) =>
      Object.hasOwn(patch, i) ? patch[i] : v)).decision,
    'BLOCKED');
  blocked({0: 'iam'});
  blocked({1: 'write'});
  blocked({3: '--project=oldx-1c983'});
  blocked({4: '--account=other@example.invalid'});
  blocked({5: '--limit=200'});
  blocked({6: '--format=value(token)'});
  blocked({7: '--log-http'});
  blocked({8: {}});
  blocked({8: {signal: abort.signal, extra: 'true'}});
  blocked({8: {signal: 'faked'}});
  blocked({2: filter.replace(trace, 'Z'.repeat(32))});
  blocked({2: filter + ' OR true'});
  blocked({2: filter.replace(from, '2026-11-15T09:29:54.000Z').replace(until, '2026-11-15T09:30:26.000Z')});
  blocked({2: filter.replace(from, '2026-11-15T09:30:07.000Z')});
  blocked({2: filter.replace(from, '2026-11-31T09:29:55.000Z')});
  assert.equal(planOfflineV2LoggingProcess(...exact, '--impersonate-service-account=other').decision, 'BLOCKED');
  assert.equal(planOfflineV2LoggingProcess().decision, 'BLOCKED');
  abort.abort();
  assert.equal(planOfflineV2LoggingProcess(...exact).decision, 'BLOCKED');
  // A previous immutable plan cannot itself execute or become authenticated
  // Cloud Logging evidence when the signal expires.
  assert.equal(plan.executable, false);
  assert.equal(plan.provenance, 'UNVERIFIED');
});

test('hosted transport fails closed on oversized or unexpected denial body', async () => {
  let count = 0;
  await assert.rejects(simulateKeylessOwnerReadAcceptance(hosted, () => {
    switch (++count) {
      case 1: return Response.json({token: googleToken});
      case 2: return Response.json({ok: true}, {headers: {'cache-control': 'private, no-store'}});
      case 3: return Response.json(error('ENFORCEMENT_UNAVAILABLE'),
        {status: 503, headers: {'cache-control': 'private, no-store'}});
      default: return Response.json({unexpected: true}, {status: 403});
    }
  }), {message: 'ACCEPTANCE_STOPPED_invoker-denied'});
  assert.equal(count, 4);
  await assert.rejects(simulateKeylessOwnerReadAcceptance(hosted, () => new Response('x'.repeat(32_769))),
    {message: 'INVOCATION_TOKEN_GENERATION_FAILED'});
});
