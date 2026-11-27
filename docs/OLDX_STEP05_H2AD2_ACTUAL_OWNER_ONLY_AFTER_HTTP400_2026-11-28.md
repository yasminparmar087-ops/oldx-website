# BAJUTO / OLDX Step05 — H2AD2 actual PASS, new probe SA exists, direct Invoker remains Owner-only

## 28 Nov 2026 ~00:29 IST, Owner root Ubuntu WSL screenshot

Actual one-time execution of `scripts/step05_h2ad2_after_400_sa_iam_reconciliation_readonly_once_20261128.py`, creation commit `3d91910dbb909eb99513f83bcd92a1047d18dd0f`, verified Git blob `920f73f5cd022f1d30a4897452fdd7623a8a0a96`. Screenshot showed pinned source downloaded, Git hash checked and Python AST parsed, followed by:

```text
H2AD2_MARKER=CONSUMED_NO_REPEAT
H2AD2_PRIVATE_GATEWAY_SAME_UID_INGRESS_OFF=VERIFIED
H2AD2_PROBE_SA=EXISTS_ENABLED_EXACT_UID_VERIFIED
H2AD2_PROBE_SA_UID=110217058111344002447
H2AD2_DIRECT_GATEWAY_IAM=OWNER_ONLY_PROBE_NOT_GRANTED
H2AD2_H2AD1_PRIOR_IAM_WRITE=HTTP_400_CAUSE_NOT_YET_PROVEN
H2AD2_SCHEDULER_JOB=NOT_CREATED_BY_THIS_SCRIPT
H2AD2_CLOUD_WRITES=NONE
H2AD2_NO_AUTOMATIC_PERMISSION_RETRY_OR_CLEANUP=TRUE
H2AD2_H2_PRODUCTION=NO_GO
H2AD2_DO_NOT_REPEAT=TRUE
H2AD2_RESULT=POST_HTTP400_READONLY_RECONCILIATION_PASS_WITH_LIMITS
```

**Correct interpretation:** The H2AD1 newly-created dedicated probe Service Account exists, enabled, verified with numeric immutable UID `110217058111344002447`. Existing Cloud Run Gateway service UID `2d87153f-155e-409f-a418-463c785d8467` still has internal-only ingress/default OFF and immutable H2U image. The **direct** policy currently retains only `user:yasminparmar087@gmail.com` `roles/run.invoker`; the intended `serviceAccount:oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com` is **NOT granted**. No broader effective/ancestor IAM conclusions. Original H2AD1 `:setIamPolicy` HTTP400 had no response body retained, so the error's exact cause is **UNKNOWN**. H2AD2 performed only three distinct post-failure metadata GETs and **NO Cloud writes**. No Scheduler job or authenticated hosted HTTP request yet.

**DO NOT repeat** consumed H2AD2, H2AD1 or previous H2AD0/H2AC/H2AB/H2AA/H2Z/H2W/H2X/H2Y/H2U/H2V tests/Cloud writes and do not reset/delete owner-local one-time markers. Do NOT recreate the probe Service Account, add project-wide roles, relax ingress, retry IAM blindly, delete it or auto-cleanup. Existing owner H2AD approval is for one scoped temporary identity/Invoker/job/health workflow; a **new corrective IAM write** after the failed single attempt should be separately authorized and grounded in a new diagnosis/readback.

## Narrow next action: new H2AD3 audit-log reason lookup, read-only only

Google Cloud official docs say Cloud Audit Logs can record `SetIamPolicy` calls and status, but a rejected API request might not produce a discoverable entry. See https://docs.cloud.google.com/iam/docs/review-iam-policy-history and https://docs.cloud.google.com/logging/docs/audit-logging. A new, bounded **Cloud Logging `entries:list` read-only POST** for 27 November 2026 18:45–19:25 UTC and `SetIamPolicy` method names, restricted to `oldx-staging`, can provide a sanitized reason category without redoing any IAM reads/writes. If no entries or access denied, label `UNKNOWN`; never assert propagation or malformed etag without evidence. This is a new diagnostic; not a repeat of the prior direct IAM policy GET.

## Step05 status

`H2AD0=ACTUAL_PASS_CONSUMED`; `H2AD1=SA_CREATED_ACTUAL_IAM_HTTP400_STOP_CONSUMED`; `H2AD2=ACTUAL_PASS_OWNER_ONLY_SA_EXISTS_CONSUMED`; `H2AD3=SOURCE_PLAN_NEXT`; `H2_HOSTED_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `PRODUCTION=NO_GO`.
