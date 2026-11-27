# BAJUTO / OLDX Step05 — H2AA actual PASS: Compute Engine API DISABLED; VPC-free Scheduler path chosen for feasibility

## Actual Owner root WSL screenshot — 28 Nov 2026 ~00:10 IST

Owner ran the **single previously prepared** H2AA script `scripts/step05_h2aa_compute_service_state_permission_hint_once_20261128.py` from immutable commit `a680630c453b77add54e80496d1c0688b658900d`, verified Git blob `a04ec5a2b4572f2cf0c634b41ab168f0a8444c25`. Screenshot shows the hash/AST-checked download and these result fields:

```text
H2AA_MARKER=CONSUMED_NO_REPEAT
H2AA_COMPUTE_API=DISABLED
H2AA_PERMISSION_HINTS=NOT_QUERIED_API_DISABLED
H2AA_VPC_403=CONSISTENT_WITH_DISABLED_API_NOT_CONCLUSIVE
H2AA_VPC_INVENTORY=NOT_REPEATED
H2AA_NO_NEW_PERMISSION_GRANTS_API_ENABLE_OR_CLOUD_WRITES=TRUE
H2AA_EFFECTIVE_IAM_PRIVATE_ROUTING_HOSTED_HTTP=NOT_VERIFIED
H2AA_H2_PRODUCTION=NO_GO
H2AA_DO_NOT_REPEAT=TRUE
H2AA_RESULT=SERVICE_STATE_AND_OPTIONAL_PROJECT_PERMISSION_HINTS_PASS_WITH_LIMITS
```

**Read-only H2AA actual PASS with limits.** The exact Google Service Usage `compute.googleapis.com` state was **DISABLED** in `oldx-staging` / project number `38472235077`. H2Z first `compute.networks.list` HTTP403 is consistent with disabled Compute API but its root cause remains **not conclusively verified**, because error details were intentionally not retained. No new permission hints were requested after disabled state. Do not infer no VPC networks, that Owner lacks compute permissions, or that the original HTTP403 was necessarily IAM denial.

Previously frozen evidence:
- H2Z: project IAM policy v3 actual read PASS, project **direct** `roles/run.invoker` bindings 0, Owner/Editor bindings 2, public Invoker members 0, conditional IAM bindings 1; first Compute networks read 403 and regional subnets read **NOT ATTEMPTED**. Effective/ancestor IAM not audited.
- H2W: new `oldx-c2-h2-private-gateway` service UID `2d87153f-155e-409f-a418-463c785d8467`, exact off-only immutable Gateway image, internal ingress, Owner-only direct Invoker binding verified at that time.
- H2Y: raw actual script STOP false negative on omitted default-false proto3 `reconciling`; existing service response independently supports **CONTROL_PLANE_READY_PASS_WITH_LIMITS** at snapshot date, not hosted HTTP invocation.

## Do not repeat

`/root/.oldx-step05-h2aa-compute-state-permission-hint-once-20261128` is **consumed**. Never delete/reset it or rerun H2AA. Earlier H2Z, H2W, H2X/H2Y, H2U build, H2V Registry push, H2T, H2S, H1B and old focused tests are likewise consumed. No Cloud writes made by H2AA.

## Fastest safe path to **one actual OFF-only hosted HTTP probe** without Compute/VPC

Official Google Cloud Run ingress documentation: https://docs.cloud.google.com/run/docs/securing/ingress states that **Cloud Scheduler** in the same project (or compatible VPC-SC perimeter) sending to the **default `run.app` host** is an accepted `internal` source. For a Google Cloud Run-to-Cloud Run caller, VPC routing is required; this does not apply to native Cloud Scheduler source.

Official references:
- https://docs.cloud.google.com/scheduler/docs/creating — Cloud Scheduler can invoke internal-ingress Cloud Run within same project using default `run.app` URL.
- https://docs.cloud.google.com/run/docs/triggering/using-scheduler — authenticated Cloud Run requires OIDC service-account identity, correct audience and IAM Invoker.
- https://docs.cloud.google.com/scheduler/docs/http-target-auth — token identity/least privilege.
- https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs — jobs are recurring assets; pause/cleanup required.

This is an **option**, not evidence that the API is currently enabled, IAM OIDC invoker bound, endpoint reachable or HTTP 200 observed. Cloud Scheduler API state is not yet known; it may require a new **billable API enablement**. A new Scheduler job is also a cloud write and potentially a monthly recurring charge; do not blindly create recurring jobs or assume free quota. A suitable OIDC-calling service account needs an exact target-only `roles/run.invoker` binding, and the job creator needs `iam.serviceAccounts.actAs` on that specific account. Owner-only direct Cloud Run invoker is **not** sufficient for a Scheduler job automatically.

### Next smallest **distinct** gate: H2AB (source-only, owner has not executed)

Inspect only `cloudscheduler.googleapis.com` Service Usage state (one new metadata GET, **not a Compute or VPC repeat**). If API disabled, separately request owner approval for one narrowly scoped Scheduler-based OFF-only HTTP test; if enabled, prepare exact bounded identity/permissions/jobs plan before any write. Do not grant Gateway signer KMS privileges to the Scheduler token identity. Prefer a dedicated single-purpose probe service account, reusing an existing appropriately isolated identity only if security review demonstrates no cross-role privilege issue. Schedule paused/far future until deliberate single run; verify its retry policy, exact URL/path, max executions, responses, cleanup, and handle any ambiguities without replaying. Avoid default public ingress or temporary `allUsers`.

Never claim a successful H2 HTTP probe until receiving actual Cloud Scheduler dispatch/response and Cloud Run server-side evidence; control-plane readiness is not an HTTP result. Independent KMS /1 status-reader, durable Firestore one-sign transaction, actual approved synthetic sign, derived image security/provenance and hosted seller/buyer exit remain pending.

**Checkpoint 28 Nov:** `H2AA=ACTUAL_PASS_COMPUTE_API_DISABLED_NO_REPEAT`; `H2AB_SCHEDULER_API_STATE=NOT_CHECKED`; `H2_HOSTED_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `H2=NO_GO`; `PRODUCTION=NO_GO`.
