import assert from 'node:assert/strict';
import test from 'node:test';
import {rehearseOfflineV2Subprocess} from '../../scripts/phase-b-v2-local-process-rehearsal.mjs';

test('no-cloud subprocess rehearsal handles only a fixed synthetic Node fixture', async () => {
  const result = await rehearseOfflineV2Subprocess('ok');
  assert.deepEqual(result, {
    outcome: 'LOCAL_PROCESS_ONLY_PASS',
    cloudAccess: 'NONE',
    evidence: 'LOCAL_FIXTURE_ONLY',
  });
  assert.ok(Object.isFrozen(result));
});

test('offline subprocess has bounded timeout and redacts output overflow and stderr', async () => {
  const began = performance.now();
  const timeout = await rehearseOfflineV2Subprocess('hang');
  const elapsed = performance.now() - began;
  assert.equal(timeout.outcome, 'PROCESS_TERMINATED');
  assert.ok(elapsed < 5_000, 'process termination must be bounded');
  assert.equal(timeout.cloudAccess, 'NONE');
  assert.equal(timeout.evidence, 'LOCAL_FIXTURE_ONLY');

  const overflow = await rehearseOfflineV2Subprocess('overflow');
  assert.equal(overflow.outcome, 'OUTPUT_LIMIT');
  assert.equal(JSON.stringify(overflow).includes('XXXX'), false);

  const failure = await rehearseOfflineV2Subprocess('error');
  assert.equal(failure.outcome, 'PROCESS_FAILED');
  assert.equal(JSON.stringify(failure).includes('PRIVATE_TOKEN_NEVER_ECHO_FROM_CHILD'), false);
  assert.equal(Object.values(failure).some(v => /token|stderr|stdout/i.test(v)), false);
});

test('invalid, injected and provider-like modes never start the local fixture', async () => {
  for (const mode of [
    undefined, null, '', '../gcloud', '--impersonate-service-account=owner',
    'logging read', 'gcloud', 'prod', 'ok\nshell', {}, ['ok'], 12,
  ]) {
    assert.deepEqual(await rehearseOfflineV2Subprocess(mode), {
      outcome: 'BLOCKED', cloudAccess: 'NONE', evidence: 'LOCAL_FIXTURE_ONLY',
    });
  }
});
