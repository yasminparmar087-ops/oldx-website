import assert from 'node:assert/strict';
import {mkdtempSync, readFileSync, rmSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import test from 'node:test';

const script = fileURLToPath(new URL('../../scripts/phase-b-fixture-session-v1.mjs', import.meta.url));
const source = readFileSync(script, 'utf8');

test('fixture-only and hosted execution remain hard-off with no credential access', () => {
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
  assert.match(source, /const LIVE_FIXTURE_ONLY_ENABLED = false;/);
  assert.match(source, /fixtureOnly && LIVE_FIXTURE_ONLY_ENABLED/);
  assert.match(source, /hosted && LIVE_EXECUTION_ENABLED/);
  assert.match(source, /const credential = hosted \? await mintRuntimeCredential\(/);
  assert.match(source, /hosted \? runtimeFixtureTransport\(boundedPhaseBRequest, credential, budget\) : null/);
  assert.match(source, /const afterSignIn = hosted && hostedFixtureCallback\(/);
  assert.match(source, /const budget = runtimeSessionBudget\(hosted \? credential\.expiry : Date\.now\(\) \+ 240_000\)/);
});


test('fresh four-ID preflight stays read-only, fails closed on journal or unknown lookup', () => {
  const beginning = source.indexOf("if (args.length === 1 && args[0] === '--preflight-fixtures')");
  const end = source.indexOf("if (args.length === 1 && args[0] === '--check-configuration')", beginning);
  assert.ok(beginning > 0 && end > beginning, 'dedicated preflight must precede other checks');
  const block = source.slice(beginning, end);
  assert.match(block, /guardOperator\(\)/);
  assert.match(block, /lstatSync\(journalRoot\(\)\)/);
  assert.match(block, /error\?\.code !== 'ENOENT'/);
  assert.match(block, /STOP: EXISTING_FIXTURE_JOURNAL_REQUIRES_REVIEW/);
  assert.match(block, /inspectRecovery\(liveSend, null\)/);
  assert.match(block, /return allAbsent \? 0 : 3/);
  assert.doesNotMatch(block, /readFileSync\(3|openJournal|createUser|createDoc|deleteUser|deleteDoc|runtimeFixtureTransport|mintRuntimeCredential/);
  assert.match(source, /const LIVE_EXECUTION_ENABLED = false;/);
});


test('disabled fixture-only path retains Linux, operator and private FD3 safety prerequisites', () => {
  const gate = source.indexOf("const fixtureOnly = args.length === 1 && args[0] === '--execute-fixtures'");
  const keyRead = source.indexOf("const key = readFileSync(3, 'utf8').trim()", gate);
  const run = source.indexOf("await runSession(transport(", keyRead);
  assert.ok(gate > 0 && keyRead > gate && run > keyRead);
  const path = source.slice(gate, run);
  assert.match(path, /fixtureOnly && LIVE_FIXTURE_ONLY_ENABLED/);
  assert.match(path, /hosted && LIVE_EXECUTION_ENABLED/);
  assert.match(path, /if \(hosted\) requireHostedAcceptanceEnabled\(\)/);
  assert.match(path, /requireSafe\(process\.platform === 'linux', 'CLOUD_SHELL_REQUIRED'\)/);
  assert.match(path, /guardOperator\(\)/);
  assert.match(path, /readFileSync\(3, 'utf8'\)/);
  assert.match(path, /inspectPhaseBConfiguration\(gcloud, \{preflight: true, hostedTarget\}\)/);
  assert.match(source, /const LIVE_EXECUTION_ENABLED = false;/);
});


test('both fixture-only and hosted execution flags stay hard-off after fixture audit', () => {
  assert.match(source, /const LIVE_FIXTURE_ONLY_ENABLED = false;/);
  assert.match(source, /const LIVE_EXECUTION_ENABLED = false;/);
  assert.match(source, /const credential = hosted \? await mintRuntimeCredential\(/);
});

test('fixture-only configuration diagnostic is read-only and uses the same pinned gate as execution', () => {
  const start = source.indexOf("if (args.length === 1 && args[0] === '--check-fixture-configuration')");
  const end = source.indexOf("if (args.length === 1 && args[0] === '--preflight-fixtures')", start);
  assert.ok(start > 0 && end > start, 'dedicated read-only diagnostic must exist');
  const block = source.slice(start, end);
  assert.match(block, /guardOperator\(\)/);
  assert.match(block, /inspectFixtureOnlyStagingConfiguration\(gcloud\)/);
  assert.match(block, /blockingChecks/);
  assert.doesNotMatch(block, /readFileSync\(3|openJournal|runSession|createUser|createDoc|deleteUser|deleteDoc|mintRuntimeCredential/);
  assert.match(source, /tag: 'step3rc14'/);
  assert.match(source, /revision: 'oldx-owner-read-00003-nus'/);
  assert.match(source, /digest: 'sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc'/);
  assert.match(source, /: inspectFixtureOnlyStagingConfiguration\(gcloud\)/);
  assert.match(source, /const LIVE_EXECUTION_ENABLED = false;/);
});


test('hosted journal is isolated from accepted fixture journal in private temporary HOME', () => {
  // Completely offline: both journal files are created under a throwaway HOME,
  // never the operator's existing completed fixture evidence.
  const home = mkdtempSync(join(tmpdir(), 'oldx-journal-isolation-'));
  const moduleUrl = new URL('../../scripts/phase-b-fixture-session-v1.mjs', import.meta.url).href;
  const child = [
    "import assert from 'node:assert/strict';",
    "import {existsSync} from 'node:fs';",
    "import {homedir} from 'node:os';",
    "import {join} from 'node:path';",
    'import {openJournal,journalStatus} from ' + JSON.stringify(moduleUrl) + ';',
    "const fixtureId = '00000000-0000-4000-8000-000000000001';",
    "const hostedId = '00000000-0000-4000-8000-000000000002';",
    'openJournal(fixtureId).close();',
    'const fixture = join(homedir(), ".oldx-phase-b-fixtures-v1");',
    'const hosted = join(homedir(), ".oldx-phase-b-hosted-v1");',
    'assert.equal(existsSync(fixture), true);',
    'assert.equal(existsSync(hosted), false);',
    'openJournal(hostedId, "hosted").close();',
    'assert.equal(existsSync(hosted), true);',
    'assert.equal(journalStatus().sessionId, fixtureId);',
    'assert.equal(journalStatus("hosted").sessionId, hostedId);',
    'assert.throws(() => openJournal(hostedId, "hosted"), {code:"EEXIST"});',
    'assert.throws(() => journalStatus("unknown"), /INVALID_JOURNAL_SCOPE/);',
  ].join('\n');
  try {
    const run = spawnSync(process.execPath, ['--input-type=module', '-e', child], {
      encoding: 'utf8', timeout: 5_000, env: {...process.env, HOME: home},
    });
    assert.equal(run.status, 0, run.stderr);
  } finally {
    rmSync(home, {recursive: true, force: true});
  }
});

test('hosted journal recovery status remains read-only and all live modes hard-off', () => {
  assert.match(source, /const LIVE_FIXTURE_ONLY_ENABLED = false;/);
  assert.match(source, /const LIVE_EXECUTION_ENABLED = false;/);
  assert.ok(source.includes("const journalRoot = (scope = 'fixture')"));
  assert.ok(source.includes("'.oldx-phase-b-hosted-v1'"));
  assert.ok(source.includes("['--status', '--status-hosted'].includes(args[0])"));
  assert.ok(source.includes("journalStatus(args[0] === '--status-hosted' ? 'hosted' : 'fixture')"));
  assert.ok(source.includes("hosted ? (id) => openJournal(id, 'hosted') : openJournal"));
  assert.ok(source.includes("return allAbsent && journal?.completed && !journal.stale ? 0 : 3"));
});
