# BAJUTO / OLDX Step05 — H2AD6C one jobs.run POST HTTP400, H2AD7 read-only reconciliation

## Owner actual screenshot, 28 Nov 2026 ~00:50 IST

Owner executed prior immutable source `scripts/step05_h2ad6c_scheduler_paused_minus1_log_guard_one_run_once_20261128.py`, creation commit `61797095d7d857f1f5373d79bacf574f4808f5d9`, Git blob `5994f1c3f7370c913c50d558ca07e1596587e1ab`; source hash and Python AST were checked in screenshot. Actual stdout:
```text
H2AD6C_JOB=EXACT_PAUSED_READONLY_HEALTH_OIDC
H2AD6C_PREVIOUS_STATUS_CODE=-1
H2AD6C_LAST_ATTEMPT_TIME=ABSENT
H2AD6C_EXACT_JOB_LOG_ENTRIES=0
H2AD6C_MARKER=CONSUMED_NO_REPEAT
H2AD6C_STAGE=FIRST_ONE_MANUAL_PAUSED_JOB_RUN
H2AD6C_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_ONE_DISPATCH
H2AD6C_REASON=API_HTTP_400_NO_RETRY
H2AD6C_NO_RETRY_NO_RESUME_NO_AUTOMATIC_CLEANUP=TRUE
H2AD6C_H2_PRODUCTION=NO_GO
```

**Strict interpretation:**
- H2AD6 original and H2AD6B both halted BEFORE any `jobs.run`. This H2AD6C, however, PASSED exact job/SA/health/OIDC/PAUSED, code -1, no lastAttemptTime, and zero scoped Scheduler execution logs, then created the one-shot marker and made **ONE actual `POST ...jobs/oldx-h2ad-off-healthz-20261128:run`**. Cloud Scheduler API returned **HTTP 400**. The script deliberately discarded the error body; the concrete error reason is **UNKNOWN**. No success, HTTP target status or actual Cloud Run /healthz response was established.
- Possible causes to distinguish rather than assume: Scheduler API enforcement against a PAUSED job; request body rejected. The failed H2AD6C source sent JSON `{}` whereas [Google Cloud Scheduler v1 RunJob](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/run) says **request body must be empty**. Empty JSON might be treated as an empty message or might fail; **it is not proven to be the root cause**. The Google docs describe a run-now operation but do not unequivocally guarantee acceptance for a PAUSED job; no claim to that effect. The pre-existing status code -1 likewise does not prove previous dispatch.
- No additional job, identity, Cloud Run, IAM, KMS, Firestore or Product writes from H2AD6C other than the **attempted jobs.run**. Original Cloud Scheduler Job last confirmed PAUSED; state after POST 400 must be read back. Cloud Run ingress `INTERNAL_ONLY`, Product `OFF`. H2/production NO-GO.
- **DO NOT REPEAT** H2AD6C, clear its `/root/.oldx-step05-h2ad6c-minus1-log-guard-one-manual-run-once-20261128` marker, or repeat original H2AD6/H2AD6B, H2AD5 job creation/pause, H2AD4 IAM, H2AD1 probe SA or earlier H2 resources. Do not manually resume job or retry dispatch until new evidence and explicit new scope/approval. Temporary Scheduler Job, direct Invoker grant and SA still exist and should be eventually cleaned with UID/ETag guards after uncertain dispatch is reconciled.

## New H2AD7: one isolated, new, no-write diagnosis SOURCE READY, NOT Owner-run

- Source: `scripts/step05_h2ad7_after_run400_job_and_audit_readonly_once_20261128.py`
- Creation commit `99c7cc5d8bed6528e8c381b23e9d9964a68d721e`
- Verified Git blob SHA1 `990e088b025940366448188e39383094dc8c06b5`.
- Root Ubuntu WSL isolated native Owner gcloud, exact consumed H2AD5/H2AD6C markers and UID. New marker `/root/.oldx-step05-h2ad7-post-run400-logging-reconcile-once-20261128` written before new cloud reads. No reruns after STOP.
- Only **three distinct read-method calls**:
  1. GET exact `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128` for **post-400 current PAUSED/lastAttemptTime/status and exact OFF healthz OIDC target**, a new postfailure purpose.
  2. POST `https://logging.googleapis.com/v2/entries:list` (read-only) for bounded **Scheduler RunJob Admin Activity audit** entries since 27 Nov 2026 18:45 UTC, and only print codes/sanitized categories for the exact job.
  3. Another read-only `entries:list` on exact Scheduler execution log for that job/time window, capped at 100. No pagination follow-up, no prints of raw status messages, emails, bearer credentials, log bodies or etags.
- Admin Activity logs are not guaranteed to contain rejected requests; **no match never proves why 400 occurred**. Rejected HTTP400 might have happened before any log emission. Log categories can be ambiguous; use them as hints, not definitive statements.
- Cloud Scheduler log and RunJob authoritative references:
  - https://docs.cloud.google.com/scheduler/docs/viewing-logs
  - https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/run
  - https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs

### One exact Ubuntu root WSL paste (new H2AD7 only)

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad7-log-readonly.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad7.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/99c7cc5d8bed6528e8c381b23e9d9964a68d721e/scripts/step05_h2ad7_after_run400_job_and_audit_readonly_once_20261128.py' &&
test "$(git hash-object "$d/h2ad7.py")" = '990e088b025940366448188e39383094dc8c06b5' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad7.py" &&
python3 -B "$d/h2ad7.py" --h2ad7-after-run400-logs-and-job-readonly-once
```

A successful **read-only** result would be `H2AD7_RESULT=RUN400_JOB_AND_LOGS_READONLY_PASS_WITH_LIMITS`; this is **NOT hosted health success**. A STOP is not reason to retry previous jobs.run. If logs show PAUSED job rejection vs body validation, require new scoped permission before a distinct guarded new dispatch strategy. The previous one-dispatch approval was already attempted and consumed by H2AD6C; do not treat it as unlimited repeated run permission.

## Step 05 remaining work after H2AD7

1. Distinct H2 hosted health delivery proof (not just status 200 from Scheduler API).
2. Guarded deletion of one test Scheduler job, removal of only new SA Invoker from private Gateway preserving Owner, and exact SA UID-based disable/remove after no in-flight requests.
3. Independent actual KMS/identity/Firebase Auth/Firestore nonce and quotas/media, enabled release source, real synthetic seller → publish → buyer read → edit → withdraw, security/rollback/owner decision (G2–G6) still OPEN.

**Checkpoint:** `H2AD6C=ACTUAL_JOBS_RUN_HTTP400_ONE_POST_CONSUMED`; `H2AD7=SOURCE_READY_NOT_RUN`; `H2_HTTP=NOT_VERIFIED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
