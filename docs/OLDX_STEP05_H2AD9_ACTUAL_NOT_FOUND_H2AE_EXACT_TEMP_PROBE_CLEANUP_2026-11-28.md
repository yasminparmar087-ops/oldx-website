# BAJUTO / OLDX Step05 — H2AD9 actual NOT_FOUND; H2AE scoped temporary Scheduler probe cleanup, 28 Nov 2026

## Owner actual root Ubuntu WSL screenshot ~01:03 IST

Owner executed immutable `scripts/step05_h2ad9_actual_delivery_cloudrun_logs_readonly_once_20261128.py`, frozen source commit `b0d8a7d417c5ca726b6ae7cf3ae5df5d41a948a7`, Git blob `4e0fba4a193be86a4759a99c2932f4ada9e671c8`, after expected hash and AST checks. Screenshot shows:

```text
H2AD9_MARKER=CONSUMED_NO_REPEAT
H2AD9_JOB_FINAL_PAUSED=VERIFIED
H2AD9_LAST_ATTEMPT_PRESENT=TRUE
H2AD9_JOB_LAST_STATUS_CODE=-1
H2AD9_SCHEDULER_EXECUTION_LOG_ENTRIES=2
H2AD9_SCHEDULER_ATTEMPT_STARTED_COUNT=1
H2AD9_SCHEDULER_ATTEMPT_FINISHED_COUNT=1
H2AD9_ATTEMPT_FINISHED_1_STATUS=NOT_FOUND
H2AD9_CLOUD_RUN_REQUEST_LOG_ENTRIES=0
H2AD9_EXACT_CLOUD_RUN_HEALTH_REQUEST_LOGS=0
H2AD9_INDEPENDENT_DELIVERY_VERDICT=HTTP_DELIVERY_NOT_VERIFIED
H2AD9_OFF_JSON_BODY=NOT_CAPTURED_BY_REQUEST_LOGS
H2AD9_LOG_RAW_PAYLOADS_URLS_TOKENS=NOT_PRINTED
H2AD9_JOBS_RUN_PAUSE_RESUME_IAM_CLOUD_WRITES=NONE
H2AD9_JOB_AND_PROBE_CLEANUP=NOT_ATTEMPTED
H2AD9_H2_PRODUCTION=NO_GO
H2AD9_DO_NOT_REPEAT=TRUE
H2AD9_RESULT=ONE_INDEPENDENT_DELIVERY_LOG_READ_PASS_WITH_LIMITS
```

**Interpretation:** The **read-only H2AD9 evidence collection PASS**, but the **private Gateway hosted /healthz HTTP check is NOT PASSED**. Cloud Scheduler started and finished one attempt, finishing with `NOT_FOUND`; Cloud Run exact GET /healthz request logs were 0. No Cloud Run HTTP 200 was verified and no actual `mode:"OFF"` response body was independently observed. Job remains PAUSED. The separate H2AD8 `jobs.run` API HTTP200 had merely accepted one manual request. Do NOT represent this as a successful private HTTP test, an authentication test pass, or a Product seller/buyer test.

**Reason UNKNOWN:** Official [Google Cloud Scheduler troubleshooting](https://docs.cloud.google.com/scheduler/docs/troubleshooting) maps `URL_ERROR-ERROR_NOT_FOUND` to an HTTP 404 response, often due to target URL/resource issues. However our H2AD9 sanitization only printed the enum-like `status:NOT_FOUND` without raw `debugInfo`, so **we have NOT proven the exact returned HTTP status or origin of the response**. Official [Cloud Run ingress docs](https://docs.cloud.google.com/run/docs/securing/ingress) recognize same-project Scheduler to default run.app as internal origin. Potential issues include edge/ingress/URL mapping, identity routing or another pre-container rejection; **none is proven**. Do not relax `INGRESS_TRAFFIC_INTERNAL_ONLY`, grant public access or repeat this already used one-shot job without a separately scoped reason and owner approval. Keep this failure as residual Step05 gate; defer root-cause evidence to real G2–G6 work rather than an infinite loop.

## Existing H2AD resources and earlier Owner-approved exact cleanup scope

The Owner previously approved a bounded single temporary H2AD probe identity, exact Cloud Run service-only Invoker grant, one Scheduler job/manual read-only health request, and **exact guarded cleanup** of the temporary resources. H2AD8 additional run approval already exercised. The remaining cleanup is within that old explicit scope, not a new production release or a new service action:
- Project `oldx-staging`; exact Scheduler job `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128`, **PAUSED** after H2AD8 and at H2AD9 last readback; far-future `0 0 29 2 *` UTC schedule, GET /healthz, matching dedicated OIDC identity, retryCount0.
- Exact internal OFF Gateway `projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway`, immutable service UID `2d87153f-155e-409f-a418-463c785d8467`, `INGRESS_TRAFFIC_INTERNAL_ONLY`, H2U image frozen `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`. **Gateway remains in place**, no redeploy, no route change. Direct Invoker policy after H2AD4 is `Owner + probe SA`; only probe may be removed, Owner MUST remain.
- One temporary probe `oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`, immutable numeric SA UID `110217058111344002447`; **not** the Gateway runtime signer/service identity. No keys were created.
- Previous H2AD0 through H2AD9, H2K/H2M, H2U/V/W and older H1B source/test/cloud one-shots are all consumed and **MUST NOT be repeated**. Keep root-owned local receipt files; do not clear markers after partial result.

## New H2AE exact cleanup — SOURCE prepared, NOT Owner-run

Frozen script `scripts/step05_h2ae_exact_temporary_scheduler_probe_cleanup_once_20261128.py`
- New creation commit `ac502f38998834dab7e538ac23d71a5e820d6b24`.
- GitHub fetched/verified source blob SHA1 `70ada14844cd999a5c0a0f729bfaa8d5a6aa7e8a`; static operation and allowlist audit PASS (one job DELETE, one owner-preserving service ETag policy update, one numeric UID-specific probe SA disable, one UID-specific probe SA delete; **NO jobs.run**).
- Preflight exact old H2AD5/H2AD8/H2AD9 **root-owned markers**, project/service UID/probe numeric UID/target URI. Fresh GET reads: exact job must be PAUSED, matching GET healthz/OIDC/far-future schedule/retry, `lastAttemptTime` present; exact Gateway UID/internal/OFF runtime SA and frozen image; exact service-level direct Invoker policy Owner+probe with current ETag; probe SA exists and UID exact, enabled.
- **New pre-cleanup Scheduler executions log read-only** (distinct purpose: prove no in-flight delivery): must have exactly **one AttemptStarted + one AttemptFinished**, finished status exactly `NOT_FOUND`, complete nonpaginated exact job filter. This is not a new health dispatch or a repeat of H2AD9 for certification; it is a destructive cleanup **safety precondition**. If logs unavailable/mismatch, STOP **before any mutation**. A matching completed attempt is evidence it is no longer in flight, not a successful HTTP request.
- Only if all preconditions PASS, create unique `/root/.oldx-step05-h2ae-exact-temp-probe-cleanup-once-20261128` marker **before any writes**. Stages are each one attempt with root-only staged receipts. All writes and exact post-write readbacks:
  1. **ONE** `DELETE` exact PAUSED Scheduler job, then GET 404 (job name and complete frozen target are prechecked).
  2. **ONE** direct `POST .../services/oldx-c2-h2-private-gateway:setIamPolicy` with fresh ETag, just `roles/run.invoker: user:yasminparmar087@gmail.com`, preserving Owner, removing only temporary probe, verified by fresh readback. No project-wide IAM.
  3. **ONE** `POST .../serviceAccounts/<numeric probe UID>:disable`, GET exact email and numeric UID disabled state.
  4. **ONE** `DELETE .../serviceAccounts/<same numeric probe UID>`, GET exact email 404.
- No Scheduler manual rerun, ingress ALL, SA create, new permissions, API enable, project IAM, Firebase, Cloud KMS, Firestore, Product or production write. This is **deletion of temporary test resources only**; no longer-needed probe SA is intentionally removed by numeric immutable UID, NOT the existing Cloud Run runtime SA.
- If any stage returns HTTP error, timeout, unexpected state, or partial cleanup, **DO NOT REPEAT**. Marker and appended stage names identify where to perform a distinct exact reconciliation later. Never assume a cloud write rolled back automatically. Gateway service stays OFF and production NO-GO.

### ONE exact new root Ubuntu WSL cleanup command

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ae-cleanup-once.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ae.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/ac502f38998834dab7e538ac23d71a5e820d6b24/scripts/step05_h2ae_exact_temporary_scheduler_probe_cleanup_once_20261128.py' &&
test "$(git hash-object "$d/h2ae.py")" = '70ada14844cd999a5c0a0f729bfaa8d5a6aa7e8a' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ae.py" &&
python3 -B "$d/h2ae.py" --h2ae-owner-approved-exact-temporary-probe-cleanup-once
```

If **and only if Owner actually executes and receives** `H2AE_RESULT=EXACT_TEMP_JOB_PROBE_INVOKER_SA_CLEANUP_PASS`: all four exact cleanup stages completed and readbacks verified. On `H2AE_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_PARTIAL_CLEANUP`, don't re-run; recover from exact staged marker with a *different* UID/etag-guarded reconciliation instead of starting fresh. The preflight may intentionally STOP, no write, if logs indicate incomplete in-flight work. It has **NOT been executed in Cloud** as of this GitHub record.

## After cleanup: main Step05 track, not more repeated H2AD

Step05 remains ACTIVE, H2/production NO-GO. The status of private hosted HTTP health is **UNVERIFIED/FAILED ATTEMPT**, recorded as residual, not closure. Re-focus on independent hosted/KMS signing identity, Firebase Auth/Firestore nonce+budget and durable transactions, media review/publish/withdraw, final G2-G6 seller→publish→buyer→edit→withdraw with synthetic resources and approval/rollback plan. Do not mark source-only passes as hosted integration. Any future hosted Gateway HTTP attempt needs a new strategy and independent approval, not repeated Scheduler job recreation.
