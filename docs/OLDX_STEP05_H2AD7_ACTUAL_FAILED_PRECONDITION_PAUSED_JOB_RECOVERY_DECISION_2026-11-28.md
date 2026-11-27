# BAJUTO / OLDX Step05 — H2AD7 actual post-RunJob HTTP400 reconciliation; bounded recovery decision

## Actual user root Ubuntu WSL screenshot — 28 Nov 2026 ~00:53 IST

The owner ran immutable `scripts/step05_h2ad7_after_run400_job_and_audit_readonly_once_20261128.py` (creation commit `99c7cc5d8bed6528e8c381b23e9d9964a68d721e`, pinned blob `990e088b025940366448188e39383094dc8c06b5`) once after SHA/AST validation. Exact relevant stdout:
```text
H2AD7_MARKER=CONSUMED_NO_REPEAT
H2AD7_JOB_PAUSED_READONLY_OFF_HEALTH=VERIFIED
H2AD7_LAST_ATTEMPT_PRESENT=FALSE
H2AD7_JOB_STATUS_CODE=-1
H2AD7_AUDIT_LOGS_RETURNED=2
H2AD7_EXACT_RUN_AUDIT_1_CODE=9
H2AD7_EXACT_RUN_AUDIT_1_CATEGORY=UNKNOWN_NO_RAW_MESSAGE
H2AD7_EXACT_RUN_AUDIT_2_CODE=9
H2AD7_EXACT_RUN_AUDIT_2_CATEGORY=UNKNOWN_NO_RAW_MESSAGE
H2AD7_AUDIT_EXACT_JOB_MATCHES=2
H2AD7_EXECUTION_LOGS_RETURNED=0
H2AD7_EXECUTION_EXACT_JOB_MATCHES=0
H2AD7_RAW_ERRORS_IDENTITIES_AND_TOKENS=NOT_PRINTED
H2AD7_JOBS_RUN_RETRY_RESUME_IAM_CLEANUP=NONE
H2AD7_HTTP_DELIVERY=NOT_CONFIRMED_BY_THIS_READ
H2AD7_H2_PRODUCTION=NO_GO
H2AD7_DO_NOT_REPEAT=TRUE
H2AD7_RESULT=RUN400_JOB_AND_LOGS_READONLY_PASS_WITH_LIMITS
```

This is a **successful NEW read-only diagnostic**, NOT a successful hosted Gateway health check. The exact paused Scheduler job remains in `PAUSED` state, lastAttemptTime is absent, status.code=-1, two exact RunJob **Admin Activity** entries had `google.rpc.Code=9` (FAILED_PRECONDITION), and bounded execution logs returned zero matches. Both RunJob audit entries correspond to the earlier single H2AD6C API attempt or other matching calls; **do not infer they represent two target HTTP deliveries**. One prior H2AD6C attempt returned HTTP400, its body was discarded, so an exact rejection message is not known. No Scheduler HTTP delivery was proven, and there was NO H2AD7 Cloud write. These log results narrow the most plausible concern to a job state/precondition: PAUSED before `:run`. They **do not prove** PAUSED alone caused the rejection; empty JSON body used by H2AD6C also differed from the documented empty request body. Do not assert root cause definitively.

Authoritative references checked 28 Nov 2026:
- [Google RPC code9 FAILED_PRECONDITION](https://developers.google.com/actions-center/reference/grpc-api-v2/status_codes): state prerequisite was not satisfied
- [Cloud Scheduler Job resume REST](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/resume): transitions PAUSED to ENABLED; empty request body
- [Cloud Scheduler Job run REST](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/run): forces now, empty request body; API 200 is NOT target HTTP success
- [Cloud Scheduler Job pause REST](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/pause): transitions ENABLED to PAUSED; empty request body
- [Cloud Scheduler Job resource](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs): lastAttemptTime, status and cron/retry fields

## Preserved exact resources and no-repeat rules

- Cloud Scheduler API already ENABLED in project `oldx-staging`; Compute Engine API DISABLED. No VPC needed for same-project Scheduler calling default run.app private Cloud Run.
- Exactly one already created paused Scheduler job: `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128`, target `GET /healthz`, OIDC `oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`, audience frozen default run.app base; schedule `0 0 29 2 *` UTC (next matching Feb 29, 2028), retryCount0, 30-second deadline.
- Existing enabled probe SA UID `110217058111344002447`; direct target-only `roles/run.invoker` Owner+probe actual H2AD4 PASS. Cloud Run Gateway service UID `2d87153f-155e-409f-a418-463c785d8467`, internal ingress enforced, image frozen OFF. No Product publication, KMS sign, Firestore/Media writes, or production changes.
- H2AD7 root marker `/root/.oldx-step05-h2ad7-post-run400-logging-reconcile-once-20261128` consumed. H2AD6C marker consumed after failed `:run` POST; H2AD6B/H2AD6 aborted pre-dispatch. NEVER reset/retry H2AD7/H2AD6C/H2AD6B/H2AD6/H2AD5/H2AD4/H2AD3/H2AD2/H2AD1/H2AD0 or earlier H2/H1 one-shots. Do not recreate a job, probe SA or grant new roles.

## Narrow next decision — NEW H2AD8, source planning only; NOT Owner approved

A *different, explicitly authorized recovery* might satisfy the precondition: exact existing job PAUSED + no known delivery, then `jobs.resume` **ONCE**, verify `ENABLED` and the far-future schedule + immutable read-only target/OIDC, `jobs.run` **ONCE** with **empty (zero-byte)** request body, immediately `jobs.pause` **ONCE** and read back `PAUSED`; independent H2AD9 execution and Cloud Run logs will be needed for delivery/HTTP status. This is **more than the old consumed one-run authorization**: it includes a temporary enable window and another real `:run` POST. Requires **new Owner explicit approval** for exactly the one three-action sequence, no broad IAM/new job/SA.

Risks/gates:
- Temporary ENABLED state permits scheduled execution if cron were imminent; frozen cron is February 29 UTC, no schedule expected in this session but not a security guarantee. Fail closed if schedule, target, OIDC, retry config, state, owner/perms or unique IDs drift. No permanent resume.
- Pause must be attempted as safe containment even if run fails; pause itself may return an ambiguous result and require read-only reconciliation. NEVER automatically repeat `:run`. If resume fails/uncertain, do not run; reconcile job state; stop for manual containment if not PAUSED. Do not report safe if state may be ENABLED.
- `jobs.run` returns a Job resource on acceptance, not HTTP target response; require separately verified Scheduler AttemptFinished log and preferably Cloud Run request HTTP status. Target `/healthz` is read-only and Product remains OFF. Scheduler has at-least-once semantics; ONE API call is not a promise of exactly one delivered request.
- After proven delivery or no in-flight execution, cleanup the one existing job, remove ONLY new probe from Gateway direct IAM preserving Owner, and disable/delete exact probe SA UID. No blind cleanup while delivery uncertain. The previously approved H2AD cleanup can proceed only after its own preconditions.
- If Owner declines an additional dispatch, prioritize **exact resource cleanup** instead of more speculative job tests and leave H2 OFF HTTP unverified. Step05 still has real G2–G6 crypto/Firebase/media/seller-buyer hosted gates.

**Checkpoint:** `H2AD7=ACTUAL_PASS_WITH_LIMITS_READONLY_CONSUMED`; `JOB=PAUSED`; `FAILED_PRECONDITION_CODE9=OBSERVED_CAUSE_UNCONFIRMED`; `H2AD8=NEW_RESUME_RUN_PAUSE_AWAITING_OWNER_APPROVAL`; `H2_HOSTED_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `PRODUCTION=NO_GO`.
