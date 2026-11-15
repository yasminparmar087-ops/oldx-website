/**
 * No-cloud child fixture for V2 local subprocess termination tests.
 * No imports, credentials, sockets, file mutations or Google Cloud calls.
 * Only the test-only local probe is allowed to invoke this file.
 */
const mode = process.argv[2];
switch (mode) {
  case 'ok':
    process.stdout.write('OLDX_LOCAL_SUBPROCESS_FIXTURE_OK\n');
    break;
  case 'hang':
    setInterval(() => {}, 1000);
    break;
  case 'overflow':
    process.stdout.write('X'.repeat(8_192));
    break;
  case 'error':
    // Test the parent must not forward provider-like sensitive stderr.
    process.stderr.write('PRIVATE_TOKEN_NEVER_ECHO_FROM_CHILD\n');
    process.exitCode = 5;
    break;
  default:
    process.exitCode = 9;
}
