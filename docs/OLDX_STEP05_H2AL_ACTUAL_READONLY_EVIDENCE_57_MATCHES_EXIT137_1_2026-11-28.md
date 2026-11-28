# BAJUTO / OLDX — Step05 H2AL actual read-only evidence; H2AK consumed, partial Mediator, no rescan

Date: 2026-11-28 ~22:56 IST, user supplied actual WSL root terminal screenshot.

## Read-only H2AL result (no newly invoked scan, build, Docker mutation, Cloud call)

```text
H2AL_MODE=READ_ONLY_NO_SCAN_NO_DOCKER_WRITES
H2AL_H2AK_MARKER=CONSUMED
H2AL_H2AJ_MARKER=EXISTS_UNTOUCHED
H2AL_MARKER_ROLES=ROLE=mediator ABOUT_TO_CHECK
H2AL_MARKER_RESULT=RESULT=STOP_PARTIAL_LOCAL_READ_ONLY_ACCEPTANCE
H2AL_RECORDED_OUTCOME=STOP_PARTIAL_LOCAL_READ_ONLY_ACCEPTANCE
H2AL_RECORDED_REASON=LOCAL_CONTAINER_CLEANUP_UNKNOWN
H2AL_SUMMARY_ROLES=mediator
H2AL_MEDIATOR_GRYPE_JSON=EXISTS_COMPLETE_JSON
H2AL_MEDIATOR_GRYPE_MATCHES=57
H2AL_MEDIATOR_SEVERITIES=High:18,Low:6,Medium:20,Negligible:11,Unknown:2
H2AL_MEDIATOR_GRYPE_DB_CHECKSUM_OR_AGE=NOT_INFERRED
H2AL_GATEWAY_GRYPE_JSON=ABSENT
H2AL_BACKEND_GRYPE_JSON=ABSENT
H2AL_READER_GRYPE_JSON=ABSENT
H2AL_DOCKER_PS_BEGIN
H2AL_DOCKER_PS_END
H2AL_EVENT=create|oldx-h2ak-mediator-28e1f0|<no value>
H2AL_EVENT=start|oldx-h2ak-mediator-28e1f0|<no value>
H2AL_EVENT=exec_create| /nodejs/bin/node -e ... [two attempts; redacted]
H2AL_EVENT=exec_start| /nodejs/bin/node -e ...
H2AL_EVENT=exec_die|oldx-h2ak-mediator-28e1f0|137
H2AL_EVENT=die|oldx-h2ak-mediator-28e1f0|1
H2AL_EVENT=destroy|oldx-h2ak-mediator-28e1f0|<no value>
H2AL_IMAGE=User=65532:65532|Entrypoint=["/nodejs/bin/node"]|Cmd=["functions/staging-marketplace/four-role/mediator.mjs"]|WorkingDir=/app|OS=linux|Arch=amd64
H2AL_DO_NOT_RERUN_H2AK=TRUE
H2AL_DOCKER_BUILD_PUSH_EXEC_STOP_RM_SCAN=NONE
H2AL_CLOUD_IAM_KMS_FIREBASE_WRITES=NONE
```

The displayed Docker events were long/truncated on the terminal and not copied verbatim to this durable receipt. Above records only relevant tokens actually seen: created/started, exec 137, main container exit 1, destroyed.

**Established evidence:**
- **Mediator Grype original scan COMPLETE**: `/root/oldx-h2ak-images-20261128T160610Z-42e006/mediator-grype.json`, 57 total findings, **18 HIGH, 0 Critical shown**, 20 Medium, 6 Low, 11 Negligible, 2 Unknown. Raw file and exact package/CVE findings remain in the Owner's private root evidence. No repeat of Mediator Grype scan is justified. Severity counts are findings, not unique CVE IDs and not a security clearance.
- Gateway/Backend/Reader **have NOT been scanned** and their runtime checks have NOT been attempted. H2AK is consumed; do not rerun or clear marker.
- First Mediator Docker image inspect confirms Linux/AMD64, `65532:65532`, Distroless Node entrypoint /app. **Nonroot image configuration is confirmed, but a healthy running OFF HTTP service is NOT proven.**
- Docker events show `exec_die 137` (an exec process was SIGKILL-terminated; cause UNKNOWN: could be memory/resource pressure, container teardown, another event) and main container `die 1` (process failure; cause UNKNOWN), then `destroy`. There is **no surviving container in docker ps -a**; no logs. Distinguish SIGKILL evidence from proof of OOM; do NOT claim Docker OOM confirmed.
- The original `smoke` cleanup `docker stop` failed after the container had auto-removed (`--rm`), masking the primary startup/health error. We cannot recover original stdout/stderr from H2AK, because it was never persistently recorded.

## Confirmed source defects needing ONE consolidated correction BEFORE any more scans

Existing `scripts/step05_h2ak_four_pinned_new_images_scan_offhealth_once_20261128.py` (source blob `f9b6f2f15cd1c5a59405d33f09e158434b7c2773`) had:
1. `smoke()` finally cleanup raises `LOCAL_CONTAINER_CLEANUP_UNKNOWN`, masking the first runtime failure and/or an otherwise correct smoke result.
2. `docker run --rm` auto-removes crashed containers, concealing logs and making subsequent `docker stop` nonzero.
3. `run()` discards STDERR for failed Docker/node processes, losing decisive failure detail.
4. Grype raw JSON is saved before runtime, but severity summary is persisted only *after* successful `smoke()`. H2AL recovered valid raw Mediator scan and counts; do not rescan it.
5. `--memory 512m --cpus 0.5` + an extra Node exec process can contribute to contention; not proof of cause. Avoid arbitrary OOM attribution. Future diagnostic must capture `docker inspect State.OOMKilled`, exit code, error, and logs while retained, with **no `--rm`**.
6. The Node24 distroless process static-imports multiple ESM modules even in OFF mode. A missing import/dependency/runtime exception would exit nonzero before the HTTP server binds; its presence is not established by old localhost simulation. Verify *actual image runtime imports and startup* before approving any Cloud Run deployment.
7. Per-image scan state and per-image nonroot runtime state MUST be separate durable receipts. Unknown runtime should neither erase complete scan evidence nor trigger a repeated vulnerability scan, and must not claim other three roles are scanned.

## Next action

Owner instructed: **find and fix errors properly BEFORE scanning again**. Do SOURCE-ONLY implementation and NEW focused offline tests for error/exit-code logging, idempotent/observable cleanup, no `--rm`, staged per-role completed-scan receipts, selective only three remaining Grype scans, and one bounded mediator OFF health rerun **under new explicit approval**. No Docker run/stop/pull/build/scan or Cloud operations now. Preserve H2AK, H2AJ, H2AI, H2AG one-shot markers.

H2AL is READ-ONLY COMPLETED. Next H2AM should use an entirely NEW unique marker and a separately approved, carefully bounded local runtime diagnostic/remaining scans; never reuse the old H2AK script. Even after future local runtime PASS, private Cloud Run and hosted Seller–Buyer remain not verified, production OFF.

**Canonical checkpoint:** `H2AJ=FOUR_PRIVATE_REGISTRY_PASS`; `H2AK=CONSUMED_PARTIAL_DO_NOT_REPEAT`; `H2AL=READ_ONLY_COMPLETE`; `MEDIATOR_GRYPE=57_MATCHES_18_HIGH_0_CRITICAL`; `MEDIATOR_OFF_HTTP=NOT_VERIFIED`; `OTHERS_GRYPE=NOT_RUN`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
