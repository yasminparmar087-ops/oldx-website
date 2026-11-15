/**
 * OLDX V2 Cloud Logging: source-only, non-executing subprocess plan.
 *
 * This module contains no subprocess/network imports and no execution path.
 * A plan is NOT authenticated Cloud Logging evidence, permission, or a PASS.
 * The old one-shot hosted consent was spent; both hosted runners remain OFF.
 */
const GCP_PROJECT = 'oldx-staging';
const OPERATOR = 'yasminparmar087@gmail.com';
const MAX_PROCESS_MS = 1_500;
const MAX_STDOUT_BYTES = 65_536;

// Exactly the filter constructed by reviewScopedHostedDenialLogShape.
// Do not prefilter status, revision or URL: mismatched entries must remain.
const FILTER = /^trace="projects\/oldx-staging\/traces\/([a-f0-9]{32})" AND timestamp>="(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z)" AND timestamp<="(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z)"$/;

export function planOfflineV2LoggingProcess(...args) {
  const blocked = Object.freeze({decision: 'BLOCKED', executable: false, provenance: 'UNVERIFIED'});
  // Only the intended 8 string arguments plus the AbortSignal options object.
  if (args.length !== 9 || args.slice(0, 8).some(x => typeof x !== 'string') ||
      !args[8] || typeof args[8] !== 'object' ||
      Object.keys(args[8]).length !== 1 ||
      !(args[8].signal instanceof AbortSignal) || args[8].signal.aborted) {
    return blocked;
  }
  const [area, operation, filter, scope, account, limit, format, quiet, options] = args;
  if (area !== 'logging' || operation !== 'read' ||
      scope !== '--project=' + GCP_PROJECT ||
      account !== '--account=' + OPERATOR ||
      limit !== '--limit=2' || format !== '--format=json' || quiet !== '--quiet') return blocked;
  const match = FILTER.exec(filter);
  if (!match) return blocked;
  const [, trace, fromIso, untilIso] = match;
  const from = Date.parse(fromIso), until = Date.parse(untilIso);
  if (!Number.isSafeInteger(from) || !Number.isSafeInteger(until) ||
      new Date(from).toISOString() !== fromIso ||
      new Date(until).toISOString() !== untilIso ||
      until - from < 10_000 || until - from > 30_000) return blocked;

  const argv = Object.freeze(args.slice(0, 8));
  const processOptions = Object.freeze({
    shell: false, encoding: 'utf8', windowsHide: true,
    timeout: MAX_PROCESS_MS, maxBuffer: MAX_STDOUT_BYTES, killSignal: 'SIGKILL',
    signal: options.signal,
  });
  // Matching parameters are necessary, not sufficient: CLI identity,
  // provider credential authenticity, process exit, log provenance and IAM
  // cannot be proven by this local validation or by a mocked log reader.
  void trace;
  return Object.freeze({
    decision: 'OFFLINE_PLAN_ONLY',
    executable: false,
    provenance: 'UNVERIFIED',
    file: 'gcloud',
    argv,
    processOptions,
  });
}
