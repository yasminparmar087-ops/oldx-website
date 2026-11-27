# BAJUTO / OLDX Step05 — H2AB actual Scheduler API disabled, H2AC scoped enable requires owner approval

## ACTUAL OWNER screenshot 28 Nov 2026 ~00:13 IST

Owner WSL executed pinned `scripts/step05_h2ab_cloudscheduler_api_state_readonly_once_20261128.py` (source commit `ab2c24a872525052d493987c9b850ef1b768e101`, verified blob `4ee2c66c9586b6fbc5ee4fbd0a2881491b7ee270`). Screenshot shows one hash/AST check and **actual**:

```text
H2AB_MARKER=CONSUMED_NO_REPEAT
H2AB_CLOUD_SCHEDULER_API=DISABLED
H2AB_SCHEDULER_JOB_IDENTITY_PERMISSIONS=NOT_QUERIED
H2AB_COMPUTE_API_AND_VPC=NOT_TOUCHED
H2AB_SCHEDULER_JOBS=NOT_CREATED_OR_RUN
H2AB_API_ENABLE_IAM_CLOUD_WRITES=NONE
H2AB_HOSTED_HTTP=NOT_TESTED
H2AB_H2_PRODUCTION=NO_GO
H2AB_DO_NOT_REPEAT=TRUE
H2AB_RESULT=ONE_NEW_SCHEDULER_API_STATE_READ_PASS_WITH_LIMITS
```

Exactly one new Service Usage partial state GET succeeded for `projects/38472235077/services/cloudscheduler.googleapis.com`: **DISABLED**. H2AB is **ACTUAL PASS_WITH_LIMITS**, not Scheduler job execution or hosted Gateway proof. Earlier H2AA Compute Engine API DISABLED actual and H2Z project IAM partial PASS / first VPC HTTP403 remain unchanged. Zero Cloud writes, IAM, Compute, VPC, scheduler jobs or hosted HTTP from H2AB.

**One-shot marker consumed:** `/root/.oldx-step05-h2ab-cloudscheduler-api-state-once-20261128`. NEVER rerun or reset H2AB, H2AA, H2Z, H2W, H2X/H2Y, H2V push, H2U image build or previous source test/Cloud checks.

## Why Cloud Scheduler, what remains unproven

Official [Cloud Run ingress](https://docs.cloud.google.com/run/docs/securing/ingress) and [Cloud Scheduler internal target guide](https://docs.cloud.google.com/scheduler/docs/creating) recognize a **Cloud Scheduler job in the same project targeting the default `run.app` service URL** as eligible for `INGRESS_TRAFFIC_INTERNAL_ONLY`. For authenticated services the job uses a separately authorized service account and OIDC ID token with correct audience; it must have target-service-only `roles/run.invoker` ([Cloud Run + Scheduler](https://docs.cloud.google.com/run/docs/triggering/using-scheduler)). This is a potential no-VPC route, NOT current proof of identity, endpoint readiness or a successful invocation.

Google's [Cloud Scheduler pricing](https://cloud.google.com/scheduler/pricing) describes a per-job charge/free allowance; eligibility depends on the billing account's job count, plus possible Cloud Run use charges. Do not assume zero cost or grant a recurring job indefinitely. Creating any job or IAM binding would be a **separate new cloud write** requiring exact identity, no broad grants, one controlled dispatch, evidence and cleanup.

## Source-only NEW H2AC prepared; no Cloud execution, NOT owner approved yet

- Source: `scripts/step05_h2ac_approved_single_scheduler_api_enable_once_20261128.py`
- Creation commit: `6f1397678ae78c9984bfcccc5e5aff538de22791`
- Verified readback blob: `0152009468f7cd02967852f8b0ef722be5bf2149`
- GitHub static scope/readback checks PASS; local AST and owner-run Cloud outcomes **NOT CLAIMED**.
- Separate approval required for a single **new real cloud write**: enable **only** `cloudscheduler.googleapis.com` in `oldx-staging`, project number `38472235077`. Prior H2AB check is not consent; old general approval for other APIs is not consent for this API.
- If approved, H2AC checks exact root Ubuntu WSL Owner isolated config/previous H2AB consumed marker and **fresh one-ServiceUsage GET**. If already enabled it does no write. Otherwise creates a distinct one-shot marker **before the first authorized POST**, makes exactly **ONE** `POST https://serviceusage.googleapis.com/v1/projects/38472235077/services/cloudscheduler.googleapis.com:enable`, GET-only bounded operation poll and exact readback; no repeated enable on ambiguous timeout.
- Marker (only upon approved execution): `/root/.oldx-step05-h2ac-scheduler-api-enable-approved-once-20261128`.
- No Compute Engine enable, VPC or subnet calls, IAM grant, Scheduler job creation, Run invocation, Gateway change, KMS sign, Firestore write, registry or production activation.
- GitHub source preparation is not a Cloud action. **Do not issue the execution command until Owner's explicit H2AC approval.**

## Next exact owner decision

**Request:** "Approve exactly ONE `cloudscheduler.googleapis.com` API enable in `oldx-staging` only, with existing isolated Owner access and H2AC one-time guarded script; no Scheduler jobs, IAM, production or other resources yet?" If Owner says yes, give the pinned SHA-validated one-paste H2AC script execution. If no, remain in source-only planning. After H2AC real PASS, decide a separate narrow OIDC identity, `run.app` URL/health route, target-only Cloud Run Invoker grant, single manually dispatched paused job and guarded deletion; no automatic invocations or recurring schedule.

**Checkpoint:** `H2AB=ACTUAL_PASS_SCHEDULER_API_DISABLED_CONSUMED`; `H2AC=SOURCE_ONLY_PREPARED_AWAITING_EXPLICIT_OWNER_APPROVAL`; `H2_HOSTED_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `H2=NO_GO`; `PRODUCTION=NO_GO`.
