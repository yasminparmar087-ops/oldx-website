# BAJUTO / OLDX Step05 — H2AD4 Owner ACTUAL PASS; next H2AD5 creates ONE paused Scheduler OIDC health job

## 28 Nov 2026 ~00:36 IST Owner root Ubuntu WSL screenshot — H2AD4 ACTUAL PASS

Owner ran frozen script `scripts/step05_h2ad4_owner_approved_existing_probe_exact_iam_correction_once_20261128.py` from commit `e25c84e22c718b3cdb5e4e2a1dc113e955889605` with Git SHA1 blob `1406253ede3e24ea1034985b3e625354f32115ea` checked in shell, Python AST checked, then executed once. Actual output:

```text
H2AD4_MARKER=CONSUMED_NO_REPEAT
H2AD4_STAGE=ONE_CORRECTIVE_GATEWAY_ONLY_IAM_SET
H2AD4_IAM_SET_HTTP=200
H2AD4_IAM_ERROR_CATEGORY=NONE
H2AD4_GATEWAY_IAM=OWNER_PLUS_EXACT_PROBE_ONLY
H2AD4_PROBE_SA_UID=110217058111344002447
H2AD4_SCHEDULER_JOB=NOT_CREATED_OR_RUN
H2AD4_HOSTED_HTTP=NOT_TESTED
H2AD4_OTHER_IAM_KMS_FIRESTORE_PRODUCT_WRITES=NONE
H2AD4_H2_PRODUCTION=NO_GO
H2AD4_DO_NOT_REPEAT=TRUE
H2AD4_RESULT=PASS_ONE_CORRECTIVE_EXACT_INVOKER_WITH_LIMITS
```

**Facts:** The single corrective exact Cloud Run IAM write succeeded HTTP200 and post-write direct service-level IAM readback showed ONLY Owner `user:yasminparmar087@gmail.com` and the existing probe `serviceAccount:oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com` as `roles/run.invoker`, on exact Cloud Run service UID `2d87153f-155e-409f-a418-463c785d8467`. The temporary probe SA immutable UID remains `110217058111344002447`. This proves **direct binding** but not ancestor/effective IAM or that a hosted HTTP request succeeded. Gateway remains internal ingress with `OLDX_H2U_MODE=OFF`. H2AD4 one-shot `/root/.oldx-step05-h2ad4-one-corrective-exact-invoker-once-20261128` CONSUMED: do not retry or reset. Historical H2AD3/H2AD2/H2AD1/H2AD0/H2AC/H2AB/H2AA/H2Z/H2W/H2Y/H2U/H2V and old Cloud/KMS tests already consumed; no repeats.

## H2AD5: new distinct frozen source, no owner execution yet

Earlier Owner expressly approved the bounded one private-health workflow: existing temporary SA, exact target-only Invoker, one controlled Scheduler job, single manual GET /healthz, and exact guarded cleanup. This H2AD5 phase creates and **pauses exactly ONE** future-scheduled OIDC job. It does **not** run it. Cloud Scheduler `jobs.create` and `jobs.pause` are two NEW real Cloud writes within that previously approved test scope.

- Source `scripts/step05_h2ad5_approved_single_scheduler_job_create_pause_once_20261128.py`.
- Frozen create commit `cea6bdd5e93f0151e86297657aa408db83ab77bf`.
- GitHub-verified Git blob SHA1 `4025ade55b39e5164a7643d08c0584054508130f`; static scope check: only one job CREATE and one PAUSE, one read-only testIamPermissions call, **no jobs.run, no IAM write, no SA create, no Product or production change**.
- Exact target URI from trusted previous H2AD0 root-owned saved JSON, not hardcoded or guessed. Runtime-only request target `GET <saved default https run.app>/healthz`, OIDC `serviceAccountEmail=oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`, audience **base run.app URI without path**, never token contents in repo.
- Exact new job identity `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128`.
- New preflight verifies H2AD0 actual PASS saved root receipt; H2AD4 attempt marker, **fresh exact** existing SA immutable UID/enabled, Cloud Run UID/internal/Invoker/OFF/image/URI, direct IAM ONLY Owner+probe, Owner `iam.serviceAccounts.actAs` on **this SA**, exact job GET must be 404. These are write-time guards for a NEW job, not repeating consumed H2Y/H2AD0 for status farming.
- One-shot marker `/root/.oldx-step05-h2ad5-new-single-job-create-pause-once-20261128` **before any job create**. Creates job with OIDC GET `/healthz`, attempt deadline 30s, `retryCount:0`, explicit UTC schedule `0 0 29 2 *` (next matching February 29 is 2028). The far-future schedule provides an extra safety buffer while immediate `jobs.pause` is issued; it is NOT permanent safety or an alternative to clean deletion. If create outcome ambiguous, code attempts exactly one distinct GET to reconcile specific job before conditional pause; never retries create. Then reads same job and demands state `PAUSED` and exact target/SA/schedule. No automatic manual dispatch or recurring work happens as part of this script.
- No promise of ₹0 (Cloud Scheduler/free quota may depend on billing-account job count; Cloud Run costs may accrue on the later manual request). No VPC/Compute, no new API enable, no project IAM or public member, no Cloud Run redeploy.
- STOP or partial after marker: **never rerun H2AD5 or clear marker**. The job might exist in `ENABLED` state; the chosen February 29 cron is a containment buffer but promptly plan a distinct exact read-only reconciliation and pause if needed, without recreating it. Do not manually invoke any ambiguous job. Do not attempt cleanup without UID+resource state evidence.

Official Cloud Scheduler v1 sources checked 28 Nov:
- https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/create
- https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/pause
- https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs
- https://docs.cloud.google.com/scheduler/docs/access-control
- https://docs.cloud.google.com/run/docs/securing/ingress

### Single new owner Ubuntu root WSL command (H2AD5 only)

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad5-once.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad5.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/cea6bdd5e93f0151e86297657aa408db83ab77bf/scripts/step05_h2ad5_approved_single_scheduler_job_create_pause_once_20261128.py' &&
test "$(git hash-object "$d/h2ad5.py")" = '4025ade55b39e5164a7643d08c0584054508130f' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad5.py" &&
python3 -B "$d/h2ad5.py" --h2ad5-owner-approved-one-scheduler-job-create-pause-once
```

Do not assume result. If successful: `H2AD5_RESULT=PASS_ONE_NEW_PAUSED_OIDC_HEALTHZ_JOB_WITH_LIMITS`, `H2AD5_JOB_PAUSED=VERIFIED`, `H2AD5_HTTP_DISPATCH=NOT_ATTEMPTED`. `STOP` means possible partial cloud write; do not retry and preserve screenshot.

## AFTER actual H2AD5 only

Under same Owner's previous limited H2AD authorization, prepare one **new one-shot** exact `jobs.run` from PAUSED if supported by API and bounded per-target log read for actual HTTP 2xx; a mere `jobs.run` API response is NOT proof of delivery. If Google rejects run while PAUSED, do not repeatedly run; consider a guarded finite resume/run/pause alternative, with no cron occurrence near present time. Reconcile lastAttemptTime/status and exact Scheduler AttemptFinished log. Only after no in-flight job, delete **exact** new job, remove **only** probe SA direct invoker from specific Gateway preserving Owner role, disable/delete the **same UID** probe SA with dependency and retention checks. Uncertain delivery or cleanup => stop rather than delete/recreate to force a PASS.

## Remaining Step05 not solved by OFF health

G2–G6 real two-hop identity, KMS sign/status proof, Firebase Auth and Firestore transaction durability/nonce and quotas, approved media/photo moderation, source-to-hosted enabled H2 image/independent owner approval, synthetic seller save→publish→buyer read→edit→withdraw, audit, rollback and final release decision remain **OPEN**. `STEP05=ACTIVE`; `H2=NO_GO`; `PRODUCTION=NO_GO`.

**Checkpoint:** `H2AD4=OWNER_ACTUAL_PASS_EXACT_INVOCATION_IAM_NO_REPEAT`; `H2AD5=SOURCE_READY_UNEXECUTED`; `SCHEDULER_JOB=NOT_YET_CREATED`; `H2_HTTP=NOT_TESTED`; `PRODUCTION=NO_GO`.
