/**
 * OLDX V2 local process-control rehearsal ONLY.
 *
 * This module NEVER invokes gcloud or reads live Cloud Logging. It runs one
 * fixed source-controlled, no-cloud fixture using the current Node executable.
 * It deliberately does not accept executable paths, argv arrays or credentials.
 * This confirms local process behavior, NOT authenticated GCP provenance.
 */
import {execFile} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const FIXTURE = fileURLToPath(new URL('../tests/integration/fixtures/phase-b-v2-local-child.mjs', import.meta.url));
const MODES = new Set(['ok', 'hang', 'overflow', 'error']);
const TIMEOUT_MS = 1200;
const OUTPUT_BYTES = 4096;

export async function rehearseOfflineV2Subprocess(mode) {
  const verdict = outcome => Object.freeze({
    outcome, cloudAccess: 'NONE', evidence: 'LOCAL_FIXTURE_ONLY',
  });
  if (typeof mode !== 'string' || !MODES.has(mode)) return verdict('BLOCKED');
  return new Promise(resolve => {
    // No shell and no inherited env secrets. The child is a fixed, local Node
    // file; there is no configurable binary/argument path to run gcloud.
    execFile(process.execPath, [FIXTURE, mode], {
      shell: false,
      encoding: 'utf8',
      windowsHide: true,
      timeout: TIMEOUT_MS,
      killSignal: 'SIGKILL',
      maxBuffer: OUTPUT_BYTES,
      env: {},
    }, (error, stdout, stderr) => {
      // Do not return the exception, stdout or stderr, ever.
      if (error) {
        if (error.code === 'ERR_CHILD_PROCESS_STDIO_MAXBUFFER') {
          return resolve(verdict('OUTPUT_LIMIT'));
        }
        if (error.killed && error.signal === 'SIGKILL') {
          return resolve(verdict('PROCESS_TERMINATED'));
        }
        return resolve(verdict('PROCESS_FAILED'));
      }
      if (mode === 'ok' &&
          stderr === '' &&
          stdout === 'OLDX_LOCAL_SUBPROCESS_FIXTURE_OK\n') {
        return resolve(verdict('LOCAL_PROCESS_ONLY_PASS'));
      }
      return resolve(verdict('BLOCKED'));
    });
  });
}
