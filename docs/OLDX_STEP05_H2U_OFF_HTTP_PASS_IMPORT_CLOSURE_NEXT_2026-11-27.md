# BAJUTO / OLDX Step05 H2U — OFF HTTP actual tests PASS; next source import closure audit

**27 Nov 2026, after ~21:30 IST owner WSL result. Source only; NO new Cloud approval.**

## Accepted actual result (do NOT repeat)

[H2U OFF HTTP test receipt](OLDX_STEP05_H2U_PRIVATE_OFF_HTTP_SOURCE_NEW_TESTS_2026-11-27.md): Node `24.22.3`, new 3/3 PASS and 0 fail; wrapper `OLDX_H2U_OFF_HTTP_NEW_TESTS=PASS_3_GROUPS`. Screenshot log SHA256 `0d8e788ee26281cb176671b7e5041439468f35c6c55e3c1c437e2a88ccf1f6c3`; owner-local evidence `/root/oldx-h2u-off-http-new.1pr8M7N3`; Cloud writes/builds/pulls/scans NONE. One-shot marker `/root/.oldx-step05-h2u-off-http-three-focused-once-20261127` consumed. Do not run or delete marker, repeat earlier H2S/H2T/H2R/H2N checks, image scans/builds or H1B trial.

The 3 cases were simulated-request mock tests, NOT real HTTP listener/OCI build/Cloud Run IAM. The OFF gateway entrypoint imports `createC2H2GatewayHostSource()` in default-OFF mode; that factory imports `c2-website-mediation.mjs`, `secure-product-pipeline.mjs`, `trusted-host.mjs`, `runtime.mjs`, `public-runtime.mjs` and their transitive scripts. **The full dependency closure has not yet been enumerated.** Copying just the HTTP handler and entrypoint to a Docker image is insufficient, and blindly copying the entire repository would inflate exposure of unused files. A dedicated H2 Gateway runtime image must not re-label the H1B mediator image.

## New source-only static import closure inventory, NOT executed

- New `scripts/c2-h2u-source-import-closure-audit.mjs` (Git blob `654d66ebf5088d2f9169ea5811098c4d89f77114`, commit `176a8e39e5fa8a1b3e2016f5938b3a569152f34d`). Starting at the exact H2U Cloud Run OFF main, recursively reads local `import`/`export from` paths, fails on path escaping/symlinks/missing modules/dynamic require, reports each file's SHA256 and bare external package imports. **Does not execute any imported source**, build images, contact Google Cloud, consume prior tests, or inspect Owner credentials.
- New one-shot offline root WSL runner `scripts/step05_h2u_source_closure_one_offline_audit_20261127.sh`, source commit `60b377583d9a1076a9be41e8ed8846958a3da1d9`, Git blob `85d5071c77f4beb806209a26e9cc1634d979f2a7`. Downloads only an immutable GitHub source snapshot (commit `176a8e39e5fa8a1b3e2016f5938b3a569152f34d`), checks the scanner plus H2U main/host/HTTP Git blobs, reuses cached local `oldx-h1a-c2-mediator-off:local-20261124t195244z` Node24 image with `--network none`, nonroot UID and read-only mount. It writes a private import-manifest JSON, outputs file count, external package import names and SHA256. No test suite or Docker build/pull/push/scan.
- **Static regex scanner only**: a PASS is NOT an ESM runtime link verification, package dependency authorization, full OCI manifest or image provenance. A STOP may mean unsupported import syntax or missing source; do not loosen security guards automatically. No imports are executed by the scanner.
- New audit marker `/root/.oldx-step05-h2u-import-closure-audit-once-20261127` is set only just before the source scan. On STOP, preserve log/output and do not repeat or remove marker without focused diagnosis.

### One new Ubuntu root WSL paste: static import closure only

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2u-closure-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/closure.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/60b377583d9a1076a9be41e8ed8846958a3da1d9/scripts/step05_h2u_source_closure_one_offline_audit_20261127.sh' &&
test "$(git hash-object "$d/closure.sh")" = '85d5071c77f4beb806209a26e9cc1634d979f2a7' &&
bash -n "$d/closure.sh" &&
bash "$d/closure.sh"
~~~

Successful run output will include `OLDX_H2U_IMPORT_CLOSURE=STATIC_AUDIT_PASS_WITH_LIMITS`, source file count, package names and private evidence path. Do not assume that result before Owner runs it. A failure is `OLDX_H2U_IMPORT_CLOSURE=STOP`, and should be diagnosed with retained evidence, not re-executed blindly.

## Remaining H2 gates

Only after complete dependency inventory and one strictly scoped build plan: separate Owner approval for a new immutable Gateway image build/push, private Cloud Run service with correct verified Gateway UID `107238619872767759560`, ingress and IAM Invoker; and distinct independent real KeyVersion status reader, permanent one-sign Firestore transaction permissions/no TTL, authenticated mediator/backend and separate one-time KMS signing authorization. The H2U OFF app has not bound those real providers, and image provenance/hosted behavior are unknown.

**Checkpoint:** H2U OFF source tests ACTUAL PASS 3/3 CONSUMED; H2U static import closure SOURCE-READY, NOT EXECUTED; Step05 ACTIVE; H2/Production NO-GO.
