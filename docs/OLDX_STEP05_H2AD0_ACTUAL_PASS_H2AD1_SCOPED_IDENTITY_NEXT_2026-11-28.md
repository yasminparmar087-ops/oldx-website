# BAJUTO / OLDX Step05 — H2AD0 Owner Actual PASS; H2AD1 owner-approved probe SA and target-only Invoker next

## Screenshot received: 28 November 2026 ~00:23 IST, root Ubuntu WSL

Exact source `scripts/step05_h2ad0_private_gateway_scheduler_probe_readonly_preflight_once_20261128.py` from immutable commit `63c63934080da8ba7140b86df7b85c748f703d8d`, Git blob `1addb78a91a2524461fcc6961894a060a2e2de44`. Owner screenshot shows hash verified and AST parsed before execution.

```text
H2AD0_MARKER=CONSUMED_NO_REPEAT
H2AD0_HEALTH_PATH=/healthz
H2AD0_NEW_PROBE_SA=ABSENT_404
H2AD0_NEW_SCHEDULER_JOB=ABSENT_404
H2AD0_GATEWAY_UID_INGRESS_OFF_IMAGE=VERIFIED_AT_READ
H2AD0_EVIDENCE=/root/oldx-h2ad0-scheduler-readonly-20261127T185331Z
H2AD0_HOSTED_HTTP=NOT_TESTED
H2AD0_CLOUD_WRITES=NONE
H2AD0_PRODUCTION_H2=NO_GO
H2AD0_DO_NOT_REPEAT=TRUE
H2AD0_RESULT=READONLY_TARGET_URI_AND_RESOURCE_ABSENCE_PASS_WITH_LIMITS
```

Target base URI is now **known in Owner-private root-local `sanitized-preflight.json` receipt**, rather than inventing/custom-deriving URL; the original terminal output additionally printed `H2AD0_TARGET_RUN_APP_BASE` with a default https `run.app` hostname. New unique names are confirmed absent 404 at the same read:
- `oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`
- `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128`.

Cloud Run service UID exactly `2d87153f-155e-409f-a418-463c785d8467`, internal ingress, Owner-only direct IAM previously verified, `OLDX_H2U_MODE=OFF`, exact immutable H2U image `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`. The readback is **NOT hosted HTTP success**; no job/SA was created and no IAM changed in H2AD0.

H2AD0 one-shot marker `/root/.oldx-step05-h2ad0-scheduler-target-preflight-once-20261128` is CONSUMED. DO NOT RERUN, reset or delete. Previous H2W/H2Y/H2Z/H2AA/H2AB/H2AC/H2U/H2V tests/builds/GET markers likewise not repeated.

## Owner approved scoped H2AD test

Owner expressly answered `ha manjuri chhe` to the planned full temporary private probe identity, **exact** new Gateway-only Invoker role, one Scheduler manual healthz attempt, and UID/etag guarded cleanup. H2AD1 below is the first **two cloud-write operations** of that approved flow. Approval covers only the specific new probe identity/resource and target; not broad project IAM, allUsers, existing Gateway SA privilege, a real KMS sign, Firebase, Product launch or production. Cloud Scheduler usage/Cloud Run requests may incur charges. Keep resource duration short.

## H2AD1 source-only prepared (NOT Owner-run yet)

- New source: `scripts/step05_h2ad1_create_scoped_probe_sa_invoker_once_20261128.py`
- Immutable creation commit `d51a3641cbaad0ae17085fb526d59f2b31f4bf57`
- GitHub readback verified blob SHA1 `ca99db3d52e4a44e2e3097a94094f94a98771906`. Static one-write-per-target, guard, no-job checks PASS. **No Cloud execution or Python runtime test claimed.**
- Prior H2AD0 actual PASS marker and exact private receipt is verified; previous exact new SA/job 404, fresh Cloud Run UID/internal/auth/OFF/image/URI and existing direct service-level **exact Owner-only** Invoker policy with ETag checked again solely because a new **IAM write** is about to occur. This is NOT a repeat of H2Y readiness analysis.
- Before writing, ensures probe SA/job still absent; creates a distinct one-time root marker `/root/.oldx-step05-h2ad1-probe-sa-and-exact-invoker-once-20261128`.
- Exactly **ONE** `POST https://iam.googleapis.com/v1/projects/oldx-staging/serviceAccounts` to create **only** the temporary `oldx-h2ad-probe-20261128` SA, validates returned immutable numeric UID, and one new-SA GET readback.
- Only after verified new SA does **ONE** direct `POST https://run.googleapis.com/v2/projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway:setIamPolicy` preserving existing Owner Invoker plus **only** `serviceAccount:oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`. Fails closed if anything else is in direct binding/policy; guards using prior current policy ETag and reads back exact Owner+probe binding.
- No `allUsers`/`allAuthenticatedUsers`, no project-level IAM grants, no Scheduler job creation or run yet; no H2U Gateway deploy/ingress/visibility change, no KMS/Firestore/media/Product modifications.
- Unknown/partial response from a write = **STOP_WITHOUT_RETRY**; no automatic rollback without new exact UID/etag evidence. Keep marker with partial resource details for unique follow-up. Local Owner identity SDK never logged; no OAuth stored.

### One new root Ubuntu WSL paste — do not run twice

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad1-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad1.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/d51a3641cbaad0ae17085fb526d59f2b31f4bf57/scripts/step05_h2ad1_create_scoped_probe_sa_invoker_once_20261128.py' &&
test "$(git hash-object "$d/h2ad1.py")" = 'ca99db3d52e4a44e2e3097a94094f94a98771906' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad1.py" &&
python3 -B "$d/h2ad1.py" --h2ad1-owner-approved-one-probe-sa-exact-invoker-once
```

**Result not assumed:** `H2AD1_RESULT=PASS_ONE_PROBE_SA_UID_AND_EXACT_GATEWAY_INVOKER` would confirm the first identity/IAM gate only. `H2AD1_SCHEDULER_JOB=NOT_CREATED` and `H2AD1_HOSTED_HTTP=NOT_TESTED` remain. If STOP, do NOT rerun or create a second SA/role; preserve marker and inspect possible partial cloud writes.

## Next after actual H2AD1 PASS

Build one exact, immediately paused far-future `GET /healthz` Cloud Scheduler OIDC job using the **newly verified SA uniqueId**, the saved default `run.app` target and matching base OIDC audience. Single manual `:run` only after exact paused/target/SA checks, no arbitrary future recurring execution. **Scheduler is at-least-once delivery:** `retryCount=0` does not absolutely prevent duplicate dispatch; the route is read-only and must not mutate Product, Firestore or KMS. Observe actual delivery log result; `:run` request acceptance is not HTTP 200 proof. On ambiguous results, preserve paused job and wait for bounded read-only reconciliation without blind retry. Cleanup only those newly created job/SA/Invoker resources by matching immutable UID/ETag once no request is running.

Official references: [Cloud Run internal origin](https://docs.cloud.google.com/run/docs/securing/ingress), [Cloud Scheduler job API](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs), [Scheduler at-least-once delivery](https://docs.cloud.google.com/scheduler/docs/configuring/deduplicate-job-requests), [RunJob](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/run), [PauseJob](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/pause).

## Step 05 exit: do not confuse with this health gate

After HTTP OFF health, still open: real independent KMS status/sign and runtime identities; Firebase Auth + Firestore transactions/nonce budgets; managed photo moderation/publication; full authenticated hosted synthetic seller→publish→buyer→edit→withdraw; approved enabled image provenance/security, rollback and final decision. `STEP05=ACTIVE`; `H2=NO_GO`; `PRODUCTION=NO_GO`.
