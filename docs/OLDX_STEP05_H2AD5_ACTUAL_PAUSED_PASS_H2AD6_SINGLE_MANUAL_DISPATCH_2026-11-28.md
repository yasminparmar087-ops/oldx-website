# BAJUTO / OLDX Step05 — H2AD5 actual job CREATED+PAUSED PASS, next H2AD6 single manual health dispatch

## Owner screenshot, 28 November 2026 ~00:40 IST

Owner root WSL executed previously approved immutable `scripts/step05_h2ad5_approved_single_scheduler_job_create_pause_once_20261128.py`, creation commit `cea6bdd5e93f0151e86297657aa408db83ab77bf`, verified Git blob `4025ade55b39e5164a7643d08c0584054508130f`. Screenshot shows hash/AST check and these actual outputs:

```text
H2AD5_MARKER=CONSUMED_NO_REPEAT
H2AD5_STAGE=ONE_NEW_FAR_FUTURE_SCHEDULED_JOB_CREATE
H2AD5_JOB_CREATE_HTTP=200
H2AD5_CREATE_ERROR_CATEGORY=NONE
H2AD5_STAGE=ONE_IMMEDIATE_JOB_PAUSE
H2AD5_NEW_JOB=EXACT_ONE_CREATED_AND_PAUSED
H2AD5_TARGET=READONLY_GET_HEALTHZ_WITH_EXACT_OIDC
H2AD5_NEXT_SCHEDULE=FEB29_NOT_DISPATCHED
H2AD5_JOB_PAUSED=VERIFIED
H2AD5_HTTP_DISPATCH=NOT_ATTEMPTED
H2AD5_PROBE_SA_UID=110217058111344002447
H2AD5_CLOUD_WRITE_SCOPE=ONE_JOB_CREATE_ONE_PAUSE_ONLY
H2AD5_PRODUCTION_H2=NO_GO
H2AD5_DO_NOT_REPEAT=TRUE
H2AD5_RESULT=PASS_ONE_NEW_PAUSED_OIDC_HEALTHZ_JOB_WITH_LIMITS
```

**Meaning:** ONE new exact Cloud Scheduler job was created and paused, confirmed readback. No HTTP dispatch at that point. Job location `asia-south1`, name `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128`, target the previously verified private `run.app` URI plus `GET /healthz`. OIDC identity is existing dedicated `oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`, immutable numeric UID `110217058111344002447`. No new SA, no new Invoker grants, no KMS or Firebase usage. The direct-only Owner+probe Gateway `roles/run.invoker` policy was previously ACTUAL PASS in H2AD4, service UID `2d87153f-155e-409f-a418-463c785d8467`, `INTERNAL_ONLY`, Gateway OFF.

**Do not repeat H2AD5** or clear consumed marker `/root/.oldx-step05-h2ad5-new-single-job-create-pause-once-20261128`; do not rerun any H2AD4/H2AD3/H2AD2/H2AD1/H2AD0/H2AC/H2W/H2Y/H2U/H2V or old Cloud tests/build/Registry scripts.

## H2AD6 — new script SOURCE ONLY, OWNER APPROVED dispatch within existing scoped H2AD consent

The Owner's earlier authorization explicitly covered ONE controlled manual read-only health dispatch of the exact paused Scheduler job, and exact cleanup after proof. H2AD6 performs only this one dispatch, not cleanup. It does NOT change the Gateway ingress, job schedule, IAM, SA, KMS, Firestore, Firebase, Product, image or production. Google Cloud's official `jobs.run` v1 API describes a **forced dispatch now** (POST, empty body), but does not guarantee a successful HTTP target invocation or synchronous response body. Paused job semantics are not assumed by our script; if the API rejects dispatch in PAUSED state, H2AD6 will STOP with no retry/resume:
- https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/run
- https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs
- https://docs.cloud.google.com/scheduler/docs/troubleshooting
- https://docs.cloud.google.com/scheduler/docs/viewing-logs

Source `scripts/step05_h2ad6_one_paused_job_manual_off_health_dispatch_once_20261128.py`:
- Creation commit `0bf8d4be4e4ded465757b40fef12c0e9b6532ee8`
- Verified Git blob SHA1 `4afd1cc3d3f29a3e664e0e107d21f76d59f4ee28`.
- GitHub readback/static one-POST-only guard PASS. Owner Python AST / Cloud dispatch **NOT YET EXECUTED**. No hosted HTTP claim.
- Prereq root-owned H2AD5 one-shot marker with exact project, service UID, SA UID, job name, persisted default `run.app` base, create and pause attempt markers. Exact isolated native Owner SDK and token.
- NEW one-time root marker `/root/.oldx-step05-h2ad6-one-manual-paused-job-dispatch-once-20261128` is written **before the ONE `:run` POST**, so even HTTP400/403/timeout is consumed; never blindly rerun or resume. No automation or scheduler repeat manually.
- Fresh exact job GET confirms state `PAUSED`, `GET /healthz`, OIDC `audience=base run.app` and exact SA identity, schedule `0 0 29 2 *` UTC, deadline30sec, retryCount0, and no previous attempt/status. This is **new dispatch-time validation**, not redoing the old creation, IAM scan or readiness probes.
- Makes exactly one `POST https://cloudscheduler.googleapis.com/v1/projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128:run` with empty JSON object. If successful, must return HTTP200, exact job name. This means **DISPATCH ACCEPTED**, NOT target HTTP success.
- After accepted response, at most 7 GET polls of the **same exact job**, spaced 3 sec, verify it remains PAUSED with the same target+identity and check new `lastAttemptTime` and sanitized `status.code`. A missing status/code is UNKNOWN; HTTP200/JSON `mode:OFF` **cannot** be claimed from `jobs.run` or status alone. Future separate H2AD7 new bounded read-only Scheduler `AttemptFinished` and Cloud Run server-side log proof required.
- If a STOP occurs, no re-dispatch or manual resume, no automatic cleanup of identity/job until any in-flight delivery reconciled; preserve marker/receipt and screenshot. Google Scheduler can have at-least-once behavior even with retry0, but endpoint is read-only OFF /healthz.

### ONE exact WSL root Ubuntu command, H2AD6 only

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad6-once.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad6.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/0bf8d4be4e4ded465757b40fef12c0e9b6532ee8/scripts/step05_h2ad6_one_paused_job_manual_off_health_dispatch_once_20261128.py' &&
test "$(git hash-object "$d/h2ad6.py")" = '4afd1cc3d3f29a3e664e0e107d21f76d59f4ee28' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad6.py" &&
python3 -B "$d/h2ad6.py" --h2ad6-owner-approved-one-paused-scheduler-health-run-once
```

An optimistic example result string only **after actual API acceptance** would be `H2AD6_RESULT=ONE_MANUAL_RUN_ACCEPTED_DELIVERY_NEEDS_INDEPENDENT_PROOF`. If PAUSED run is denied, `STOP_BEFORE_OR_AFTER_POSSIBLE_ONE_DISPATCH`; never repeat with resume on own initiative. If asynchronous job logging lags, proceed to fresh **read-only** log verification, not a second jobs.run.

**Outstanding after H2AD6:** H2AD7 delivery+Cloud Run server-side status proof; exact newly created job and test SA / Invoker **cleanup with precondition checks**. Also H2 core enabled real KMS identity/signing, Firebase Auth/Firestore durable nonce/quotas, media moderation/publication, real hosted synthetic seller→buyer vertical flow, release and rollback decision still OPEN. H2/production NO-GO.

**Checkpoint**: `H2AD5=OWNER_ACTUAL_PASS_JOB_PAUSED_CONSUMED`; `H2AD6=SOURCE_ONLY_READY_OWNER_NOT_RUN`; `H2_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `PRODUCTION=NO_GO`.
