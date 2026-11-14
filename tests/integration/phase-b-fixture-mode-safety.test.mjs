import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import test from 'node:test';

const script = fileURLToPath(new URL('../../scripts/phase-b-fixture-session-v1.mjs', import.meta.url));
const source = readFileSync(script, 'utf8');

test('fixture-only and hosted modes remain independently hard-off with no credential access', () => {
  for (const args of [
    ['--execute-fixtures'],
    ['--execute'],
    ['--execute', '--hosted-tag=step3rc14',
      '--hosted-revision=oldx-owner-read-00003-nus',
      '--hosted-digest=sha256:' + 'a'.repeat(64)],
  ]) {
    const run = spawnSync(process.execPath, [script, ...args], {
      encoding: 'utf8', timeout: 5_000,
      env: {...process.env, PATH: ''},
    });
    assert.equal(run.status, 2, args.join(' '));
    assert.match(run.stderr, /STOP: request blocked or session incomplete/);
    assert.doesNotMatch(run.stdout + run.stderr, /token|password|Bearer/i);
  }
});

test('source binds runtime mint and runtime transport only to hosted mode', () => {
  assert.match(source, /const LIVE_EXECUTION_ENABLED = false;/);
  assert.match(source, /const fixtureOnly = args\.length === 1 && args\[0\] === '--execute-fixtures';/);
  assert.match(source, /requireSafe\(\(fixtureOnly \|\| hosted\) && LIVE_EXECUTION_ENABLED, 'LIVE_EXECUTION_DISABLED'\)/);
  assert.match(source, /const credential = hosted \? await mintRuntimeCredential\(/);
  assert.match(source, /hosted \? runtimeFixtureTransport\(boundedPhaseBRequest, credential, budget\) : null/);
  assert.match(source, /const afterSignIn = hosted && hostedFixtureCallback\(/);
  assert.match(source, /const budget = runtimeSessionBudget\(hosted \? credential\.expiry : Date\.now\(\) \+ 240_000\)/);
});
