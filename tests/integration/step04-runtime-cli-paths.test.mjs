import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import test from 'node:test';

const read = path => readFileSync(new URL('../../' + path, import.meta.url), 'utf8');
const dockerfile = read('Dockerfile.product-read.bellsoft-npm-free');

function firstPartyRuntimeInputs(recipe) {
  const source = recipe.split(/\r?\n/)
    .filter(line => /^COPY /.test(line) && !line.startsWith('COPY --from'))
    .flatMap(line => line.trim().split(/\s+/).slice(1, -1))
    .filter(path => /^(features|scripts|functions)\/.*\.(?:mjs|js|cjs)$/.test(path));
  return [...new Set(source)];
}

// Narrow source-only attack-path guard: not a binary/rootfs/third-party audit.
// Check source imports AND literal dangerous CLI or Node process-launch paths.
// A passing test NEVER proves an executable or transitive package is absent.
function riskyDirectCliPath(source) {
  const patterns = [
    /\b(?:node:)?child_process\b/i,
    /\b(?:sqlite3|ldd)\b/i,
    /\.recover\b/i,
    /(?<![\w.])(?:spawn|spawnSync|exec|execSync|execFile|execFileSync)\s*\(/,
  ];
  return patterns.some(pattern => pattern.test(source));
}

test('exactly the 27 copied first-party runtime JS inputs are reviewed', () => {
  const paths = firstPartyRuntimeInputs(dockerfile);
  assert.equal(paths.length, 27, 'do not silently skip newly copied JS files');
  assert.equal(new Set(paths).size, paths.length);
  for (const path of paths) {
    assert.match(path, /^(?:features|scripts|functions)\//);
    assert.ok(!path.includes('..'));
    assert.equal(riskyDirectCliPath(read(path)), false,
      'CLI/process-launch path needs separate review: ' + path);
  }
});

test('guard rejects direct CLI and subprocess use; ignores RegExp.exec()', () => {
  for (const s of [
    "import {spawn} from 'node:child_process';",
    "const mod = await import('node:child_process');",
    "require('child_process')",
    "spawn('bash', ['-c','true'])",
    "execFile('ldd', ['/tmp/input'])",
    "const tool = 'sqlite3'",
    "const script = '.recover'",
  ]) assert.equal(riskyDirectCliPath(s), true, s);
  assert.equal(riskyDirectCliPath("const x = /a/.exec('aaa');"), false);
});

// The limited static guard does not analyze transitive native or npm packages,
// dynamically assembled strings, scripts outside the final Docker image,
// or the BellSoft base filesystem. Retain G2 HOLD until those are evaluated.
