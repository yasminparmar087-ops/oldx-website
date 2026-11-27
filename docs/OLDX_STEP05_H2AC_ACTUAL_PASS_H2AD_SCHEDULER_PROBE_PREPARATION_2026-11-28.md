# BAJUTO / OLDX Step05 H2AC actual PASS — prepare one internal Cloud Scheduler HTTP probe (H2AD)

## 28 November 2026 ~00:17 IST, owner screenshot — ACTUAL H2AC PASS

Owner executed the *approved* frozen source `scripts/step05_h2ac_approved_single_scheduler_api_enable_once_20261128.py`, commit `6f1397678ae78c9984bfcccc5e5aff538de22791`, previously verified Git blob `0152009468f7cd02967852f8b0ef722be5bf2149`; screenshot shows full sha-checked download/AST and:

```text
H2AC_STAGE=ONE_SCHEDULER_API_ENABLE_ATTEMPT
H2AC_ENABLE_ATTEMPTED=TRUE
H2AC_SCHEDULER_API_STATE=ENABLED
H2AC_RESULT=PASS_EXACT_SCHEDULER_API_ENABLED
H2AC_REASON=ONE_ENABLE_DONE_STATE_READBACK_ENABLED
H2AC_JOBS_IAM_COMPUTE_VPC_CLOUDRUN_WRITES=NONE
H2AC_H2_PRODUCTION=NO_GO
H2AC_DO_NOT_REPEAT=TRUE
```

Only `cloudscheduler.googleapis.com` Service Usage API was enabled and its final enabled state read back for `oldx-staging` project `38472235077`. No Scheduler job was created or run. No IAM, Compute Engine API, VPC, Cloud Run, KMS, Firestore or production change. H2AC is **ACTUAL PASS**, not a hosted application HTTP test.

**Do not repeat.** H2AC root WSL marker `/root/.oldx-step05-h2ac-scheduler-api-enable-approved-once-20261128` consumed. H2AB/H2AA/H2Z/H2X/H2Y, H2W private service creation + Owner direct Invoker, H2U one local image build, H2V registry push, prior KMS/Node/H1B tests are consumed. Do not delete marker or rerun cloud reads/builds for cosmetics.

## Grounded target already hosted, default OFF, intended endpoints

Source `scripts/c2-h2u-cloud-run-private-off-main.mjs` imports `functions/staging-marketplace/c2-h2u-private-off-http.mjs`. Exact accepted request handler:
- `GET /healthz` expects HTTP **200** JSON with `ok:true`, `service:"oldx-c2-private-gateway"`, `mode:"OFF"`.
- `GET /api/staging/marketplace/detail` expects HTTP **503** with `H2_GATEWAY_DISABLED`, while remaining OFF. A single **GET /healthz** is sufficient for H2AD initial hosted liveness; avoid triggering product routes or KMS.
- H2W private Cloud Run service name `projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway`, immutable **service UID** `2d87153f-155e-409f-a418-463c785d8467`, runtime SA `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` (distinct SA UID `107238619872767759560`), image digest `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`. Internal-only ingress and `OLDX_H2U_MODE=OFF`.
- H2Y raw one-shot returned `STOP_NEW_REVISION_READY_NOT_VERIFIED`, but existing same readback has proto3 omitted default-false reconciliation with generation=observed=1, ready==created revision, terminal succeeded, traffic 100%, supporting **CONTROL_PLANE_READY_PASS_WITH_LIMITS** on that snapshot. It is not HTTP proof. DO NOT rerun H2Y.

Google Cloud documentation says **same-project Cloud Scheduler** can reach an `internal` Cloud Run service using its *default* `run.app` URL; a separate Scheduler OIDC service account requires exact target-only `roles/run.invoker`, and the user creating the job requires SA actAs. Do not confuse Scheduler native origin with cross-Cloud-Run VPC routing:
- https://docs.cloud.google.com/run/docs/securing/ingress
- https://docs.cloud.google.com/scheduler/docs/creating
- https://docs.cloud.google.com/run/docs/triggering/using-scheduler
- https://docs.cloud.google.com/scheduler/docs/http-target-auth
- https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs
- https://cloud.google.com/scheduler/pricing

## H2AD — source-only proposed narrow next gate; NOT owner approved

The H2AC approval was *only* to enable the API; it does **not** approve new job or IAM/service-account writes. Before a real H2AD HTTP probe, prepare exact fresh **read-only preflight and guarded write plan**:

1. **Cloud Run exact target (new information only):** obtain service's default `uri` (must be HTTPS `*.run.app`, not custom domain) and verify the UID/ingress/IAM-enforced/OFF/image identity immediately before any write. H2W/H2Y original snapshots did not print/preserve a verified default service URL. This new `uri` read serves a new distinct purpose, *not* to re-derive H2Y readiness.
2. **Dedicated least-privilege OIDC probe identity:** create only an explicitly approved short-lived, dedicated Scheduler probe service account if no already-isolated suitable principal exists; **never** use the privileged H2 Gateway signer SA, disabled H1B trial SA, Owner user email as the OIDC token identity, or service agent for token impersonation. Bind `roles/run.invoker` only on **this specific UID-pinned service**, preserve Owner direct binding, do not add project-level or public principals. Check exact `iam.serviceAccounts.actAs` before create.
3. **One Scheduler HTTP job only** in `oldx-staging/asia-south1`, target `GET {default_run.app_uri}/healthz`, OIDC service-account email and audience base URL (no path), controlled headers/method/deadline/retry policy. **A new job is recurring**, so use a safe far-future schedule, pause it immediately, never rely on `retryCount:0` alone to prohibit later cron invocations, then one manual `:run` only after explicit Owner approval. Delete job / remove exact single Invoker grant / disable probe SA with UID and ETag checks after conclusively receiving expected results, or preserve paused resources and report ambiguous failures (do not blindly replay dispatch).
4. **Evidence:** Scheduler `:run` accepted does **not** mean target HTTP succeeded. Require scoped Scheduler delivery status (and if available sanitized Cloud Run server-side request status) to establish actual 200/expected OFF JSON; if only dispatch metadata is available, mark hosted HTTP **NOT FULLY VERIFIED**. No private headers, tokens, IAM principal lists or raw logs in GitHub.
5. **Cost:** Scheduler pricing depends on billing-account job count (official pricing has a free-job allowance, may not apply), plus Cloud Run request costs; no guaranteed ₹0. Do not create recurring permanent resources without cleanup. No enabling Compute API/VPC or relaxing ingress to `ALL`.

**Next owner decision** after the source-only guarded operational packet is ready: approve a single dedicated H2AD probe identity + target-only Invoker binding + one far-future immediately-paused Scheduler job + one manual authenticated GET `/healthz` + UID/etag-guarded cleanup, with the no-repeat/no-public/no-prod limits above. Do not treat this H2AC enable approval as approval for H2AD cloud mutations.

**Checkpoint:** `H2AC=OWNER_ACTUAL_PASS_CLOUDSCHEDULER_API_ENABLED_CONSUMED`; `H2AD=SOURCE_ONLY_PLANNED_AWAITING_SEPARATE_WRITE_APPROVAL`; `H2_HOSTED_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
