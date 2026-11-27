# BAJUTO / OLDX Step05 H2U — ESM link ACTUAL PASS; NEW OFF-only loopback runtime smoke

## Actual Owner result at 27 Nov 2026 ~21:44 IST

Previously completed single source-only ESM link audit: `OLDX_H2U_ESM_LINK_AUDIT=PASS_SOURCE_LINK_ONLY_WITH_LIMITS`, immutable manifest SHA256 `12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc`, **65 distinct local JS source files / 174 static ESM import links / 3 Node built-in modules / zero external package imports**, `OLDX_H2U_ESM_SOURCE_EVALUATED=FALSE`; owner screenshot-reported new log SHA256 `45442053d1b27788ef2ffddbe58c7d92fb9deaa863f1aeb9dc7f304a163661e1`, evidence `/root/oldx-h2u-esm-link-only.Rd7En4st`, no Cloud writes/builds/scans. [Canonical actual receipt](OLDX_STEP05_H2U_IMPORT_CLOSURE_ACTUAL_PASS_ESM_LINK_NEXT_2026-11-27.md). Source bytes 349667 previously scanned on Node24.22.3.

**Previous 65-file scanner and ESM link-only attempts are both CONSUMED, DO NOT REPEAT**. No prior H2U HTTP 3/3, H2S tests, H2T, H2N, H2R, H1B tests, Cloud probes, builds, scans or marker resets. Owner's source manifest and 65 files remain in `/root/oldx-h2u-import-closure.2oCNZVHV`; their paths are Owner-private and not uploaded to this chat. The screenshot manifest SHA is an integrity PIN, not a list of file paths. No fabricated 65-file COPY list.

## One distinct new offline local real-listener smoke — source READY, NOT RUN

Previously, request simulation tests and ESM linking passed, but **no actual H2U Node HTTP server was started**. The next **smallest useful unverified source-only gate** is to start the exact default-OFF entrypoint in an **isolated no-network** local Node24 process, loopback only, no Docker port publication. That validates application module evaluation and real HTTP responses without a Cloud deployment or replacing the old cached test image.

| New artifact | Git blob | Purpose |
| --- | --- | --- |
| `scripts/c2-h2u-new-off-http-local-listener-smoke-once_20261127.mjs` | `6d03c523abbc1550f0260749ce878d5836d5cf79` | Reads existing immutable 65-file manifest/each source hash first; spawns exact OFF entrypoint with only `PORT=18347` and `OLDX_H2U_MODE=OFF`; does actual HTTP GET localhost `/healthz` expected 200 mode OFF, POST save with synthetic enable/authorization headers expected 503, GET unknown path expected 404; terminates child with SIGTERM; no real credentials |
| `scripts/step05_h2u_new_off_listener_real_loopback_once_20261127.sh` | `c178a74aad0a6f3fc01a4a18b8d49e13d45c0e22` | Owner root WSL one-shot runner, existing cached Node24 image, immutable previous source/manifest mounted read-only, Docker `--network none` and no `-p` port publication, UID65532, read-only rootfs, no pull/build/scan/cloud. Download ONLY new Git-hash-verified 4.7kB smoke source, not 65 files or old audit |

- The new smoke script was committed at `ff4648fff1d2ba7d0c814e2f27c5f67c3af65f70`; the runner at `d823754cf52e8b7d221efd136d88c0c50045ca44`. They were both GitHub-fetched and checked for exact blobs. **New smoke is not executed yet**; no actual runtime PASS may be claimed.
- Uses dedicated attempt marker `/root/.oldx-step05-h2u-off-listener-smoke-once-20261127`; never clear it or rerun the same one-shot if STOP.
- Network namespace is isolated; loopback is available only inside the container. Neither the Cloud Run endpoint nor outside web gets a route. There is no app credential, KMS/Firestore action or Cloud writes in this local smoke.
- Even **if** this PASSes, it proves only locally started default-OFF Node HTTP listener. It does **not** prove private Cloud Run IAM/Invoker, externally attached service account, new dedicated immutable OCI image, runtime signing, media/Firestore permission, KMS fresh KeyVersion read access or production readiness.
- Cloud Run service-identity/Invoker enforcement and ingress/private routing still require separate scoped Owner approval before build/deploy. Do not use historical H1A/H1B mediator image as the new H2 release image; here it is a **cached offline Node24 test runtime only**.

### One NEW root Ubuntu WSL command, not yet executed

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2u-listener-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/smoke.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/d823754cf52e8b7d221efd136d88c0c50045ca44/scripts/step05_h2u_new_off_listener_real_loopback_once_20261127.sh' &&
test "$(git hash-object "$d/smoke.sh")" = 'c178a74aad0a6f3fc01a4a18b8d49e13d45c0e22' &&
bash -n "$d/smoke.sh" &&
bash "$d/smoke.sh"
~~~

Successful actual output must include `OLDX_H2U_OFF_LISTENER_ONE_SHOT=PASS_WITH_LIMITS`, `OLDX_H2U_OFF_RUNTIME_HEALTH_STATUS=200_OFF`, `SAVE_STATUS=503_DISABLED`, `UNKNOWN_STATUS=404`, cloud writes NONE, image builds/pulls/scans NONE. On STOP preserve local evidence; do not retry/reset without separate focused diagnosis.

**NEXT after the new smoke actual PASS (not before):** minimal source-only image packaging plan from exact Owner manifest (with 65 file-specific hashes), independent base-image digest and Node24 runtime pin, then separately approved image build and private Cloud Run Gateway service with proven IAM and trusted providers. `STEP05=ACTIVE; H2/PRODUCTION=NO_GO`.
