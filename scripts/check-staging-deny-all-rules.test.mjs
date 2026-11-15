import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { checkStagingDenyAllRules } from './check-staging-deny-all-rules.mjs';

const baseline = readFileSync(new URL('../tests/firestore-emulator/deny-all.rules', import.meta.url), 'utf8');
const release = {name:'projects/oldx-staging/releases/cloud.firestore',rulesetName:'projects/oldx-staging/rulesets/fixture'};
const ruleset = {name:release.rulesetName,source:{files:[{content:baseline.replaceAll('\r\n','\n').replaceAll('\n','\r\n')}]}};

test('accepts the linked default staging release and fingerprints its source', () => {
  assert.match(checkStagingDenyAllRules(release, ruleset, baseline).sha256, /^[a-f0-9]{64}$/);
});

test('rejects an unrelated release, unrelated ruleset and additional source', () => {
  assert.throws(() => checkStagingDenyAllRules({...release,name:release.name+'/other'},ruleset,baseline), /default Firestore/);
  assert.throws(() => checkStagingDenyAllRules(release,{...ruleset,name:release.rulesetName+'-other'},baseline), /does not match/);
  assert.throws(() => checkStagingDenyAllRules(release,{...ruleset,source:{files:[...ruleset.source.files,{content:baseline}]}},baseline), /exactly one/);
});

test('rejects a ruleset containing any difference from the reviewed source', () => {
  assert.throws(() => checkStagingDenyAllRules(release,{...ruleset,source:{files:[{content:baseline.replace('if false','if true')}]}},baseline), /differs/);
});


test('accepts published deny-all Rules without local explanatory comments or same-line formatting', () => {
  const published = baseline
    .split('\n').filter(line => !line.trim().startsWith('//')).join('\n')
    .replace("rules_version = '2';", "rules_version='2';")
    .replace('allow read, write: if false;', 'allow read,write:if false;');
  const result = checkStagingDenyAllRules(release, {
    ...ruleset, source: {files: [{content: published}]},
  }, baseline);
  assert.match(result.sha256, /^[a-f0-9]{64}$/);
  assert.equal(result.ruleset, release.rulesetName);
});

test('rejects added grants, changed deny predicate, narrowed match, malformed extra tokens and empty source', () => {
  const published = baseline.split('\n').filter(line => !line.trim().startsWith('//')).join('\n');
  for (const changed of [
    published.replace('if false', 'if true'),
    published.replace('allow read, write: if false;', 'allow read: if false;'),
    published.replace('match /{document=**}', 'match /items/{document}'),
    published.replace('allow read, write: if false;', 'allow read, write: if false; allow read: if true;'),
    published + '\nallow read: if true;\n',
    published + '\n/* unterminated',
    '',
  ]) {
    assert.throws(() => checkStagingDenyAllRules(release, {
      ...ruleset, source: {files: [{content: changed}]},
    }, baseline), /Rules tokens differ/);
  }
});
