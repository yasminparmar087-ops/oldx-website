/**
 * Offline evidence boundary for ONE future, separately authorized local run.
 * Continue only with a pinned source/context, private create-once destination,
 * verified inputs and zero incremental provider spend. The owner supplies the
 * window, byte and retention limits. Stop on first failure; no retry or upload.
 * Retain the OCI layout and raw evidence privately. Clean only the exact run's
 * temporary staging files; remove retained evidence under its own approval.
 * This module neither executes the run nor verifies signatures or disk custody.
 */
import {createHash} from 'node:crypto';

export const G2_IMAGE_EXECUTION_ENABLED = false;
export function requireG2ImageExecution() {
  throw new Error('G2_IMAGE_EXECUTION_DISABLED');
}

const DOCKERFILE = 'Dockerfile.product-read.distroless';
const BUILDER = 'node:24-bookworm-slim';
const BASE = 'gcr.io/distroless/nodejs24-debian13@sha256:6abfcb367ebc291572c774c1592a986be2ab26a2486f73093401327495a5962a';
const HISTORICAL = new Set([
  BASE.split('@')[1],
  'sha256:d4b8c34560df58c821ebda89a2897d7d183220c0debaf474a2b67a6c7cc22064',
  'sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc',
  'sha256:eabe4207e307d1e487a30e4afd3abe8cda3792883a752864a5d6f80c45cd082c',
  'sha256:903c3ae187e783fbfc3a1599d951c5150a43acd4bbdb50686218d4ab15c46990',
]);
const HIGH_IDS = ['CVE-2026-102010', 'CVE-2026-19499', 'CVE-2026-5435',
  'CVE-2026-84243', 'CVE-2026-95619'];
const MEDIA = 'application/vnd.oci.image.';
const sha = value => typeof value === 'string' && /^sha256:[a-f0-9]{64}$/.test(value);
const digest = bytes => 'sha256:' + createHash('sha256').update(bytes).digest('hex');
const validBytes = (value, limit) => Buffer.isBuffer(value) && value.length > 0 && value.length <= limit;
const stop = reason => Object.freeze({decision: 'STOP', reason, liveExecution: 'DISABLED'});
const isNewDigest = value => sha(value) && !HISTORICAL.has(value);

function pinnedRecipe(recipe, builderDigest) {
  const lines = recipe.toString('utf8').split(/\r?\n/);
  const from = lines.filter(line => /^\s*FROM /i.test(line));
  if (from.length !== 2 || from[0] !== `FROM ${BUILDER} AS dependencies` ||
      from[1] !== `FROM ${BASE}`) return null;
  return Buffer.from(lines.map(line => line === from[0]
    ? `FROM ${BUILDER}@${builderDigest} AS dependencies` : line).join('\n'));
}

// Pure checks over bytes and a separately captured receipt. Return hashes and
// counts only. The private raw report, build provenance, archive and logs stay
// with the approved local reviewer. On success the result is still evidence only.
export function reviewG2ImageEvidence({scope, recipe, index, manifest, config, provenance, sbom, runtimeLog, report, receipt} = {}) {
  if (!scope || scope.destination !== 'PRIVATE_LOCAL_OCI' || scope.maxGrossPaise !== 0 ||
      ![scope.startedAt, scope.expiresAt, scope.retainUntil, scope.maxBytes, scope.maxDbAgeMs]
        .every(Number.isSafeInteger) ||
      scope.expiresAt <= scope.startedAt || scope.expiresAt - scope.startedAt > 20 * 60_000 ||
      scope.retainUntil <= scope.expiresAt || scope.maxBytes < 1 ||
      scope.maxDbAgeMs < 1 || scope.maxDbAgeMs > 5 * 24 * 60 * 60_000 ||
      typeof scope.sourceSha !== 'string' || !/^[a-f0-9]{40}$/.test(scope.sourceSha) ||
      !isNewDigest(scope.builderDigest) || typeof scope.scannerVersion !== 'string' ||
      !/^0\.\d+\.\d+$/.test(scope.scannerVersion) ||
      ![scope.contextDigest, scope.recipeDigest, scope.approvalDigest, scope.scannerDigest,
        scope.databaseDigest, scope.scanPolicyDigest].every(sha)) {
    return stop('SCOPE');
  }
  const metadata = [recipe, index, manifest, config, provenance];
  if (!metadata.every(value => validBytes(value, 256 * 1024)) ||
      ![report, sbom, runtimeLog].every(value => validBytes(value, 32 * 1024 * 1024))) return stop('EVIDENCE_BYTES');
  const pinned = pinnedRecipe(recipe, scope.builderDigest);
  if (!pinned || receipt?.dockerfile !== DOCKERFILE ||
      receipt.sourceSha !== scope.sourceSha || receipt.builderDigest !== scope.builderDigest ||
      receipt.contextDigest !== scope.contextDigest || receipt.approvalDigest !== scope.approvalDigest ||
      receipt.base !== BASE || receipt.originalRecipeDigest !== scope.recipeDigest ||
      scope.recipeDigest !== digest(recipe) ||
      receipt.pinnedRecipeDigest !== digest(pinned) ||
      receipt.provenanceDigest !== digest(provenance) || receipt.sbomDigest !== digest(sbom) ||
      receipt.runtimeLogDigest !== digest(runtimeLog) ||
      !sha(receipt.archiveDigest) || !Number.isSafeInteger(receipt.archiveBytes) ||
      receipt.archiveBytes < 1 || !Number.isSafeInteger(receipt.retainedBytes) ||
      receipt.retainedBytes < receipt.archiveBytes + report.length + provenance.length + sbom.length + runtimeLog.length ||
      receipt.retainedBytes > scope.maxBytes ||
      !Number.isSafeInteger(receipt.completedAt) || receipt.completedAt > scope.expiresAt ||
      receipt.destination !== scope.destination || receipt.retainUntil !== scope.retainUntil ||
      receipt.attempt !== 1) return stop('PROVENANCE_OR_RETENTION');

  const indexDigest = digest(index), childDigest = digest(manifest), configDigest = digest(config);
  const identities = [indexDigest, childDigest, configDigest];
  if (!identities.every(isNewDigest) || new Set([...identities, scope.builderDigest]).size !== 4 ||
      receipt.indexDigest !== indexDigest || receipt.childDigest !== childDigest ||
      receipt.configDigest !== configDigest || receipt.reportDigest !== digest(report)) return stop('DIGEST');
  try {
    const parse = bytes => JSON.parse(bytes.toString('utf8'));
    const idx = parse(index), img = parse(manifest), cfg = parse(config);
    const amd64 = idx.manifests?.filter(item =>
      item.platform?.os === 'linux' && item.platform?.architecture === 'amd64');
    if (idx.schemaVersion !== 2 || idx.mediaType !== MEDIA + 'index.v1+json' ||
        amd64?.length !== 1 || amd64[0].digest !== childDigest || amd64[0].size !== manifest.length ||
        amd64[0].mediaType !== MEDIA + 'manifest.v1+json' ||
        img.schemaVersion !== 2 || img.mediaType !== MEDIA + 'manifest.v1+json' ||
        img.config?.digest !== configDigest || img.config.size !== config.length ||
        !img.layers?.length || !img.layers.every(layer => sha(layer.digest) &&
          Number.isSafeInteger(layer.size) && layer.size > 0) ||
        cfg.os !== 'linux' || cfg.architecture !== 'amd64' || cfg.config?.User !== '65532:65532') {
      return stop('OCI_PLATFORM_OR_CONTENT');
    }

    const statement = parse(provenance);
    if (!['https://in-toto.io/Statement/v0.1', 'https://in-toto.io/Statement/v1'].includes(statement._type) ||
        !['https://slsa.dev/provenance/v0.2', 'https://slsa.dev/provenance/v1'].includes(statement.predicateType) ||
        !statement.subject?.some(subject => subject.digest?.sha256 === childDigest.slice(7))) {
      return stop('PROVENANCE_SUBJECT');
    }

    const scan = parse(report);
    const scannedAt = Date.parse(scan.descriptor?.timestamp);
    const built = Date.parse(scan.descriptor?.db?.status?.built);
    if (scan.source?.type !== 'image' || scan.source.target?.manifestDigest !== childDigest ||
        scan.source.target.imageID !== configDigest || scan.descriptor?.name !== 'grype' ||
        scan.descriptor.version !== scope.scannerVersion || receipt.scannerDigest !== scope.scannerDigest ||
        receipt.databaseDigest !== scope.databaseDigest || receipt.scanScope !== 'squashed' ||
        receipt.scanPolicyDigest !== scope.scanPolicyDigest ||
        !Number.isFinite(scannedAt) || scannedAt < scope.startedAt || scannedAt > receipt.completedAt ||
        !Number.isFinite(built) || built > scannedAt || scannedAt - built > scope.maxDbAgeMs ||
        !Array.isArray(scan.matches) ||
        (Object.hasOwn(scan, 'ignoredMatches') &&
          (!Array.isArray(scan.ignoredMatches) || scan.ignoredMatches.length !== 0))) return stop('SCAN');

    const critical = [], high = [], tracked = Object.fromEntries(HIGH_IDS.map(id => [id, 0]));
    for (const item of scan.matches) {
      const {id, severity} = item.vulnerability;
      if (typeof id !== 'string' ||
          !['Critical', 'High', 'Medium', 'Low', 'Negligible', 'Unknown'].includes(severity) ||
          typeof item.artifact?.name !== 'string' || typeof item.artifact.version !== 'string') return stop('SCAN');
      if (severity === 'Critical') critical.push(id);
      if (severity === 'High') high.push(id);
      if (Object.hasOwn(tracked, id)) tracked[id]++;
      for (const related of item.relatedVulnerabilities ?? []) {
        if (related.id !== id && Object.hasOwn(tracked, related.id)) tracked[related.id]++;
      }
    }
    const runtime = receipt.runtime;
    const node = /^24\.(\d+)\.\d+$/.exec(runtime?.node ?? '');
    if (!node || Number(node[1]) < 12 || runtime.childDigest !== childDigest ||
        runtime.sharpTransform !== true || runtime.uid !== 65532 || runtime.port !== 8080 ||
        runtime.health !== 200 || runtime.defaultOff !== 503 || runtime.sigtermExit !== 0 ||
        !Number.isSafeInteger(runtime.sigtermMs) || runtime.sigtermMs < 0 || runtime.sigtermMs > 10_000) {
      return stop('RUNTIME');
    }
    return Object.freeze({
      decision: critical.length || high.length || Object.values(tracked).some(Boolean)
        ? 'HOLD_FINDINGS' : 'EVIDENCE_SHAPE_ONLY',
      liveExecution: 'DISABLED', signaturesAndCustody: 'REQUIRES_INDEPENDENT_VERIFICATION',
      indexDigest, childDigest, configDigest, reportDigest: receipt.reportDigest,
      criticalMatches: critical.length, highMatches: high.length, tracked: Object.freeze(tracked),
    });
  } catch {
    return stop('MALFORMED_EVIDENCE');
  }
}
