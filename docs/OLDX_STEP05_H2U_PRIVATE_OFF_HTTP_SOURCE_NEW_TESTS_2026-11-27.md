# BAJUTO / OLDX Step05 H2U — OFF-only Cloud Run HTTP entrypoint source and 3 new tests (27 Nov 2026)

## Exact confirmed baseline and immutable scope

Latest owner H2T Cloud Run v2 `oldx-staging/asia-south1` read-only regional list **ACTUAL PASS_WITH_LIMITS**: `SERVICES_COUNT=1`, `H2_MATCHED_SERVICES=0`, `GATEWAY_SA_TEMPLATE_SERVICE_COUNT=0`, completed list; no mutation; H2T marker consumed. [Actual H2T receipt](OLDX_STEP05_H2T_CLOUDRUN_READONLY_OWNER_APPROVED_2026-11-27.md). The one unrelated service was **not** individually inspected; its IAM and revision are not established. No other region is covered.

H2S synthetic KMS signature transport, metadata OAuth port, durable Firestore one-sign budget and independent KeyVersion status each have their **different previously accepted offline Node24 focused tests** PASS, 3/3 each. H2N two real read-only KMS GETs and H2R exact signer IAM grant were completed. **Do not rerun any older groups, one-shot cloud checks, scripts, builds/scans or clear markers.** Actual private H2 Gateway deployment, runtime issuer/IAM, Firestore and KMS sign are NOT verified.

## New H2U minimal entrypoint, source-only / OFF-only

| File | Verified Git blob | Scope |
| --- | --- | --- |
| `functions/staging-marketplace/c2-h2u-private-off-http.mjs` | `704ba162a1fa60c5379d4fee6126ddeb86ae02c8` | Built-in `node:http` private OFF-mode handler/server factory. Import creates **no listener**. Strict Cloud Run `PORT` parse, timeouts, connection-close headers. Only GET `/healthz` returns 200, explicit OFF; five exact marketplace operations return 503, others 404. No enabled switch, no tokens, SDK or outgoing calls |
| `scripts/c2-h2u-cloud-run-private-off-main.mjs` | `3df3405459a6d9ac504ae10fc7e56caee657f8ca` | Actual Node process entrypoint. Imports **existing** `createC2H2GatewayHostSource()` with no providers and checks `ready===false`. Refuses any `OLDX_H2U_MODE` other than undefined or `OFF`; requires valid Cloud Run `PORT`, then listens on `0.0.0.0`. Handles SIGTERM shutdown. NEVER sets H2-enabled mode |
| `scripts/c2-h2u-private-off-http.test.mjs` | `b568f99c481460410995773f30dbd20f1d35f1f3` | Exactly **3 NEW** focused test groups: OFF-only health/marketplace routes, fake enabling headers/query rejection, strict PORT + server not autostarted + entrypoint static OFF contract. Authored **NOT RUNTIME EXECUTED YET** |
| `scripts/step05_h2u_off_http_new_three_focused_offline_once_20261127.sh` | `ca7fe55e85c89d19a0891ecffb6889d58386135e` | Hash-pinned Ubuntu root WSL single new Node24 Docker test runner with cached image, no network, nonroot, read-only filesystem and no build/pull/scan/Cloud operations. Requires TAP exactly 3/3, 0 fails/skip/cancel/todo; one permanent attempt marker |

**All three authored H2U source files were individually read back at immutable source commit `b0b3d04fb6726bad138e02bb8a38c217c0ad3124` and each Git blob matches the pinned hash.** New script source commit `37e850c81f57ccb298cf8f7457a49389ddec1b6e` (Git blob above). Neither actual Docker Node24 tests nor container build/deploy have run for H2U yet. Source readback/static inspection is NOT runtime acceptance.

### Critical trust boundary

The OFF HTTP handler is intentionally **not** an authorization engine: Cloud Run's **actual private IAM Invoker and ingress** must deny unauthorized callers before forwarding any `/healthz` or API request. A 200 health response does NOT prove authentication. The Node handler ignores Authorization and all caller-supplied "enable" fields instead of treating them as trusted provider configuration. It never calls signing, KMS, Firebase, Firestore, backend, mediator or metadata endpoints. OFF-only is NOT an implemented H2 Product vertical slice and should never be reported as ready for publish.

**Missing before real Gateway:** pinned nonroot OCI image build definition/binary provenance for this entrypoint and full runtime imports; verified Gateway SA `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` UID `107238619872767759560` attached to **new** private Cloud Run revision; exact authorized Mediator Invoker/audience/ingress; separately authorized fresh KMS KeyVersion /1 metadata/public-key reader; real trusted host metadata OAuth transport; exact permanent Firestore `(default)` one-sign ledger transaction access and no TTL; validated PEM SHA and Backend links; short-lived owner sign approval and rollback. Existing H1B OFF mediator image **must NOT** be relabeled or deployed as H2.

No H2U approval was granted for image build, registry push, Cloud Run create/update, IAM binding, Firestore Rules/TTL change or `:asymmetricSign`. None occurred during source commits. OFF server is **source-prepared only**, not deployed or tested as a Cloud Run revision. Retain `H2=NO_GO`, `PRODUCTION=NO_GO`.

## One NEW targeted offline Node24 test — available, NOT executed

Owner's existing root Ubuntu WSL and previously cached `oldx-h1a-c2-mediator-off:local-20261124t195244z` Docker image are reused. Runner downloads only the immutable H2U GitHub source archive, checks three exact H2U Git blobs, uses cached image absolute Node entrypoint (previously `/nodejs/bin/node`), `--network none`, `--pull never`, `--read-only`, nonroot UID, explicit TAP reporter, and executes **only** `scripts/c2-h2u-private-off-http.test.mjs` (not older tests). One marker created immediately before the test start:
`/root/.oldx-step05-h2u-off-http-three-focused-once-20261127`.

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2u-off-test-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2u.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/37e850c81f57ccb298cf8f7457a49389ddec1b6e/scripts/step05_h2u_off_http_new_three_focused_offline_once_20261127.sh' &&
test "$(git hash-object "$d/h2u.sh")" = 'ca7fe55e85c89d19a0891ecffb6889d58386135e' &&
bash -n "$d/h2u.sh" &&
bash "$d/h2u.sh"
~~~

Success requires actual `OLDX_H2U_OFF_HTTP_NEW_TESTS=PASS_3_GROUPS`, Node >=24.12 and TAP exactly 3 tests / pass 3 / fail 0. If STOP, do not rerun, delete the attempt marker or repeat prior suites; preserve local log/evidence and fix only the new H2U cause in source.

**Checkpoint:** `H2T=ACTUAL_PASS_WITH_LIMITS_CONSUMED`; `H2U=SOURCE_OFF_ENTRYPOINT_PREPARED_NEW_3_TESTS_UNRUN`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
