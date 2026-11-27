# OLDX Step05 H2S — New default-OFF Gateway KMS composition source (27 Nov 2026)

**Current actual baseline:** Owner H2R KMS CryptoKey IAM grant **PASS**, verified one binding and etag readback. [H2R actual evidence and prior H2S initial source](OLDX_STEP05_H2R_ACTUAL_PASS_H2S_GATEWAY_SIGNING_SOURCE_NEXT_2026-11-27.md). Step05 still ACTIVE, H2/production NO-GO; no KMS asymmetricSign or private Gateway runtime has ever been accepted. No older H2R/H2Q/H2P2/H2P1/H2O/H2N/H2M one-shot should be rerun, markers removed, images rebuilt, or Cloud scans repeated.

## New source-only implementation in this batch

Four files are current and GitHub readback verified on `security-hardening-review`:

| File | Git blob | What changed |
| --- | --- | --- |
| `scripts/c2-h2-gateway-kms-synthetic-transport.mjs` | `b00d0af565775f4b26084e85b148eb99c5d2f89c` | Hardened initial one-shot signing transport; mandatory cross-instance durable atomic sign budget, strict fixed KMS endpoint, metadata-bound injected credential, CRC32C, bounded JSON body/redirect rejection |
| `scripts/c2-h2-private-gateway-signing-composition.mjs` | `a166160adf4062769231d8f2c17468911a51c7a2` | Composes the existing `createC2KmsRequestSigning` (which does real RSA-SHA256 verification) with H2S transport; exact KMS Version /1, public SPKI fingerprint and verified Gateway UID; requires independently trusted key-version status provider |
| `functions/staging-marketplace/c2-h2-gateway-host-source.mjs` | `08d2e270818fe50bfe2bc62691bb15563f4de754` | Uses **existing** `createC2PrivateGatewayHost`; pins Mediator numeric UID, Gateway UID, source image format, IAM audiences, private origins and trusted ports; corrected audience regex to reject whitespace/control characters; remains default-OFF and creates no listener |
| `scripts/c2-h2-gateway-signing-source.test.mjs` | `5b87730f26335daf0efd845fc85d38b3dc1d197f` | Three focused OFF/fail-closed, synthetic injected mock sign with CRC and one-shot, and tampering/atomic-budget denial tests; no real credentials or Cloud calls |

**Source gate:** Each file fetched from GitHub and static security checks passed. This is **source-only / not Node runtime tested**. Repo engine requires Node >=24.12.0; the model's separate tool runtime is Node22 and is not a verified substitute. The new focused test command on a suitable existing Node24+ checkout is:

~~~bash
node --test scripts/c2-h2-gateway-signing-source.test.mjs
~~~

This is a **new narrowly scoped test**, not a repeat of the previous 11 G2–G6 PASS groups, Cloud scans, builds or older one-shots.

## Exact trust boundary and remaining source gaps

- The code and tests **never call Google Cloud or change the environment on import**. `enabled=false` by default. No public website route, H2 enabled Product publishing, new SA key or KMS IAM write. No Cloud Run service created or redeployed. Mark **H2S SOURCE PREPARED; not Cloud verified**.
- The intended signer is **only** `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`, UID `107238619872767759560`, for `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1`. KMS public DER SHA-256 from the owner H2N screenshot: `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`. The original PEM remains in private owner WSL evidence, not committed. The existing RSA verifier blocks any unrelated PEM even if injected by a host.
- **Required host ports not yet bound:** independently verified runtime identity and image digest, Cloud Run metadata access token for attached Gateway SA (no Owner OAuth/SA JSON keys/impersonation shortcut), HTTPS KMS transport, **durable transactionally consumed one-sign budget shared across instances**, independent trusted Key Version ENABLED status / fingerprint provider, private Invoker and audiences. Returning a matching `principal/uid` label from a callback is not cryptographic attestation. Runtime IAM and image must be verified separately against actual deployed revision.
- A CryptoKey-level `roles/cloudkms.signer` grant **does not** authorize status/public-key get. The independent status provider is mandatory; do not fake it or grant broader `signerVerifier` to bypass it.
- `consumeDurableSignBudget` is mandatory even though the synthetic transport tracks one attempt per *process*: many Cloud Run instances otherwise permit repeated signs. A local Map test stub can only support offline tests and never a real hosted trial.
- Signature response integrity is limited to KMS response checks at the transport layer, then the existing `createC2KmsRequestSigning` verifies the signature cryptographically with the pinned public key. A static source ready flag does not mean the private host is actually authenticated.
- Before any real H2S probe: verify Node24+ focused tests, binder and trusted metadata/status providers, immutable image provenance, Cloud Run configured runtime SA and authorized Invoker, independent synthetic run authorization and expiry, cleanup/rollback, **then** request a separately scoped owner approval for a private staging-only runtime and exactly one KMS `:asymmetricSign`. No LIVE H2S consent exists in this checkpoint.

**Checkpoint:** `H2R=ACTUAL_PASS_CONSUMED`; `H2S=SOURCE_ONLY_STATIC_READBACK_PASS_TESTS_NOT_RUN`; `STEP05=ACTIVE`; `H2=NO_GO`; `PRODUCTION=NO_GO`. The website brand is BAJUTO; unchanged internal technical names OLDX.

## 27 Nov 2026 — exact local Node24 focused test runner SOURCE READY, NOT RUN

New script: `scripts/step05_h2s_focused_local_docker_tests_once_20261127.sh`, immutable source commit `7d52daab24af8742866d00b7534fd19284319ce9`, Git blob `3356c65226ca1307be607715f087a329931e0d51`.

**Source snapshot:** Verified exact H2S `security-hardening-review` branch commit `bb3ea2fe1a581f00683c08f01a2a3c52d9637764`. All five H2S/core files were individually Git-blob verified at this commit. The global repo's "latest" commit `66114ebf...` was from `main`, *not* this branch, and must NOT be used to test H2S.

In the owner's existing Ubuntu root WSL, the runner uses ONLY a previously cached local Node24 image `oldx-h1a-c2-mediator-off:local-20261124t195244z` (no pull/build/scan). It downloads the immutable source archive from GitHub to a private `/root` directory, validates five exact Git blob hashes, checks runtime Node >=24.12, runs ONLY `node --test scripts/c2-h2-gateway-signing-source.test.mjs` in Docker with `--network none`, read-only source, read-only filesystem, nonroot UID and resource limits. It verifies TAP summary **3 tests / 3 pass / 0 fail / 0 skipped / 0 todo** and saves local test log + SHA256. No SDK install, Git push, Google credentials, Cloud/production calls or older test suites.

**NOT executed yet.** The current result is GitHub source readback and static audit, not Node24 test PASS. If the local cached image is missing, archive download fails, hashes mismatch, or a test fails, STOP and preserve output; do not pull/build a new image or repeat old one-shots.

### Exact one-command owner WSL execution (local-only tests)

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2s-test-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/test.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/7d52daab24af8742866d00b7534fd19284319ce9/scripts/step05_h2s_focused_local_docker_tests_once_20261127.sh' &&
test "$(git hash-object "$d/test.sh")" = '3356c65226ca1307be607715f087a329931e0d51' &&
bash -n "$d/test.sh" &&
bash "$d/test.sh"
~~~

Success only if the runner actually reports `OLDX_H2S_NEW_FOCUSED_TESTS=PASS_3_GROUPS`, `OLDX_H2S_CLOUD_WRITES=NONE`, `OLDX_H2S_H2_PRODUCTION=NO_GO`. This is OFFLINE mocking, not actual trusted Gateway KMS signing or hosted Product acceptance.

**Runner pre-execution correction:** initial local runner had a malformed TAP check in a preliminary GitHub source revision. It was **NEVER executed**. Corrected literal checks for `# tests 3`, `# pass 3`, `# fail 0`, `# skipped 0`, `# todo 0` on source commit `7d52daab24af8742866d00b7534fd19284319ce9`, blob `3356c65226ca1307be607715f087a329931e0d51`. Only use the updated hash-pinned WSL paste above; no older runner revision.

## 27 Nov 2026 ~20:40 IST — actual H2S STOP before tests; safe local recovery

Owner WSL screenshot: old runner reported `OLDX_H2S_NEW_FOCUSED_TESTS=STOP`, `OLDX_H2S_TEST_STARTED=FALSE`, `OLDX_H2S_CLOUD_WRITES=NONE`, `OLDX_H2S_BUILDS_PULLS_SCANS=NONE`. Docker error: `exec: "node": executable file not found in $PATH`. The runner's `STOP_NODE_VERSION_BELOW_REPO_ENGINE` is a misleading label: Node was **never invoked**, so its version is unknown. Zero new test groups were run. WSL root worked; the missing /var/run/motd.new at login is nonblocking cosmetic output.

Local existing source evidence: `/root/oldx-h2s-focused-offline.0Mh9HZuX` (archive downloaded, source blobs verified), do not redownload or repeat old runner.

**New source-only recovery**: `scripts/step05_h2s_recover_cached_node_absolute_entrypoint_20261127.sh`, commit `cbe3a995067688b466a7c09947a517388caa42c5`, Git blob `6f7c79b54a5f8242ed1598ddf371027be717cb94`. It reuses the exact local source and existing cached Docker image; inspects the image's configured absolute Node entrypoint instead of assuming the unqualified `node` is in PATH. If the configured entrypoint is not a confirmed absolute Node binary, it stops with diagnostic metadata rather than guessing. No pull, build, scan, source archive download, Google API, IAM, signing or production action. It requires precisely three new PASS tests, and creates a new local one-shot test marker only immediately before executing them. **New script not yet run; no PASS claimed.**

One Ubuntu WSL root paste:

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2s-entrypoint-fix.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/fix.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/cbe3a995067688b466a7c09947a517388caa42c5/scripts/step05_h2s_recover_cached_node_absolute_entrypoint_20261127.sh' &&
test "$(git hash-object "$d/fix.sh")" = '6f7c79b54a5f8242ed1598ddf371027be717cb94' &&
bash -n "$d/fix.sh" &&
bash "$d/fix.sh"
~~~

If STOP appears preserve output/evidence, no blind rerun. H2/production NO-GO.

## 27 Nov 2026 ~20:44 IST — owner actual Node24 H2S 3 focused tests PASS; wrapper-only STOP

Owner's subsequent WSL screenshot of exact cached-source recovery script `cbe3a995067688b466a7c09947a517388caa42c5` / Git blob `6f7c79b54a5f8242ed1598ddf371027be717cb94` confirms **Node test execution completed successfully**:

~~~text
OLDX_H2S_NODE_ENTRYPOINT=/nodejs/bin/node
OLDX_H2S_NODE_VERSION=24.22.3
OLDX_H2S_ONLY_TEST=scripts/c2-h2-gateway-signing-source.test.mjs
ℹ tests 3
ℹ suites 0
ℹ pass 3
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
STOP_TAP_SUMMARY_MISMATCH # tests 3
OLDX_H2S_NEW_FOCUSED_TESTS=STOP
OLDX_H2S_TEST_STARTED=TRUE
OLDX_H2S_SOURCE_COMMIT=bb3ea2fe1a581f00683c08f01a2a3c52d9637764
OLDX_H2S_LOCAL_EVIDENCE=/root/oldx-h2s-focused-offline.0Mh9HZuX
OLDX_H2S_CLOUD_WRITES=NONE
OLDX_H2S_BUILDS_PULLS_SCANS=NONE
OLDX_H2S_H2_PRODUCTION=NO_GO
~~~

The three actual test cases shown as successful in screenshot:
1. `H2S: default OFF and composition rejects missing real trust providers`
2. `H2S: valid synthetic digest and CRC reaches one mocked KMS transport only`
3. `H2S: reject bad checksum, denied durable budget and mutated KMS signature`

**Precise interpretation:** Real Node v24.22.3 execution (engine >=24.12) **PASS 3 / FAIL 0**, source snapshot `bb3ea2...` verified, no Cloud calls. The wrapper's final `STOP` is caused by **strict shell checking `# tests 3`** while Node 24 selected the *spec* reporter that prints `ℹ tests 3`. Because shell `pipefail` passed through the test command to the summary check, the Node runner finished with zero failures; the shell wrapper's own final status is **STOP / summary-format mismatch**. **Do not mislabel the tests as failed, but do not label the wrapper as PASS.** No SHA256 evidence hash was produced by wrapper because it exited at the format check; local log `/root/oldx-h2s-focused-offline.0Mh9HZuX/new-h2s-focused-recovered-node24.log` is retained (not uploaded or independently read here).

**NO REPEAT:** `h2s-node24-new-focused-test-attempt.marker` is consumed. Do NOT re-run H2S tests, re-run Docker, remove markers, redownload source, repeat historical G1/H2/H1B checks, or use Owner OAuth to sign KMS. The new 3-group offline source gate has actual Node PASS evidence; private Gateway Cloud Run identity, independent key version status provider, durable atomic budget, strict Invoker, deployment and actual KMS `:asymmetricSign` remain **NOT VERIFIED/NOT AUTHORIZED**. `H2S_OFFLINE_TESTS=ACTUAL_PASS_3_0_WITH_WRAPPER_REPORTER_STOP`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
