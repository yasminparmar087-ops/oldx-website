# BAJUTO / OLDX Step05 H2AD3 — actual IAM400 audit principal-rejection hint; H2AD4 new corrective write pending owner consent

## Grounded Owner screenshot 28 Nov 2026 ~00:32 IST

Owner Ubuntu WSL executed exact new `scripts/step05_h2ad3_failed_iam400_audit_log_readonly_once_20261128.py`, commit `cd8598692d35070babbd0bd30d859ef04d6136a4`, SHA-1 blob `feaa022f91054120baa9d71ef8bc7b71fb05241f`. Screenshot shows SHA check and Python AST check prior to execution. Actual output:

```text
H2AD3_MARKER=CONSUMED_NO_REPEAT
H2AD3_AUDIT_LOG_QUERY=ONE_BOUNDED_ADMIN_ACTIVITY_READ
H2AD3_ENTRIES_RETURNED=2
H2AD3_MORE_LOG_PAGES=FALSE
H2AD3_EXACT_GATEWAY_ENTRIES=1
H2AD3_MATCH_1_CODE=3
H2AD3_MATCH_1_CATEGORY=PROBE_SERVICE_ACCOUNT_PRINCIPAL_REJECTED
H2AD3_RAW_MESSAGES_AND_PRINCIPALS=NOT_PRINTED
H2AD3_IAM_RETRY_AND_CLOUD_WRITES=NONE
H2AD3_HOSTED_HTTP=NOT_TESTED
H2AD3_H2_PRODUCTION=NO_GO
H2AD3_DO_NOT_REPEAT=TRUE
H2AD3_RESULT=ADMIN_ACTIVITY_READ_WITH_LIMITS_NOT_ROOT_CAUSE_PROOF
```

**Nuance:** Google RPC status `code=3` maps to `INVALID_ARGUMENT`. The script classified ONE exact Gateway audit-log status message as `PROBE_SERVICE_ACCOUNT_PRINCIPAL_REJECTED`, using a limited keyword classifier on an unprinted message, so this is a **strong diagnostic hint but NOT the precise raw cause**. It does not prove IAM propagation as the unique explanation, nor authorize an unlimited retry. Google IAM [create service account docs](https://docs.cloud.google.com/iam/docs/service-accounts-create) explicitly explain that newly created service accounts can take time to appear through eventual consistency. Cloud Run [setIamPolicy method](https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/setIamPolicy) and [IAM Policy etag](https://docs.cloud.google.com/run/docs/reference/rest/Shared.Types/Policy) establish correct membership/etag write semantics. The prior H2AD1 SA readback could succeed while a distinct IAM principal validator still rejected the new principal immediately after create.

## Frozen post-failure state

- H2AD1 one-shot: new dedicated probe SA successfully created/verified, one exact Cloud Run :setIamPolicy HTTP400, STOP and marker consumed.
- H2AD2 actual postwrite read-only: SA `oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`, immutable numeric UID **`110217058111344002447`**, exists and enabled; Cloud Run target `projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway`, immutable UID **`2d87153f-155e-409f-a418-463c785d8467`**, internal/OFF; direct Invoker policy is **Owner only**, probe NOT granted.
- H2AD3: one read-only audit-log list returned the above category; **no IAM/Cloud writes**. One-shot marker `/root/.oldx-step05-h2ad3-iam400-admin-activity-logs-once-20261128` consumed.
- H2AD0 target run.app URL and job name collision check previously actual PASS; NO Scheduler job has been created. No hosted Gateway HTTP test yet.
- DO NOT repeat H2AD1/H2AD2/H2AD3 or any consumed H2AD0/H2AC/H2AB/H2AA/H2Z/H2W/H2X/H2Y/H2U/H2V/cloud resource creation, builds, tests, scans, registry push or delete their markers.

## Next H2AD4: source-only bounded corrective IAM attempt — NOT authorized/run yet

`scripts/step05_h2ad4_owner_approved_existing_probe_exact_iam_correction_once_20261128.py`
- New source creation commit `e25c84e22c718b3cdb5e4e2a1dc113e955889605`.
- GitHub verified source blob `1406253ede3e24ea1034985b3e625354f32115ea`, scoped static allowlist checks PASS; no Owner Python execution or live cloud result claimed.
- Source precondition exact root WSL one-shot H2AD1/H2AD2/H2AD3 markers (including immutable existing SA UID and service UID), isolated owner SDK/config.
- Fresh **read-only before-write validation**: exact old SA GET confirms UID & enabled; exact service GET confirms immutable UID, internal ingress, enforced Invoker, OFF image and runtime identity; direct service IAM policy GET ensures **Owner only** and a current ETag (or if already Owner+same probe, exit without write). Unexpected policy means STOP, no write.
- Only if still Owner-only, one **new one-shot marker** `/root/.oldx-step05-h2ad4-one-corrective-exact-invoker-once-20261128` before exactly ONE new corrective `POST .../services/oldx-c2-h2-private-gateway:setIamPolicy` with just `roles/run.invoker` members `user:yasminparmar087@gmail.com` and `serviceAccount:oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`, preserving the current IAM ETag; exact response/readback must show just those two members.
- No new SA, job, Compute/VPC, KMS, Firestore, Firebase, Product, other role or project-wide IAM; ingress remains `INTERNAL_ONLY`, Product `OFF`. A 400/network timeout/mismatch is ambiguous and consumes the local marker: **DO NOT RETRY or auto-clean up**; sanitized error category printed without raw log or principals.
- Corrective IAM write might still fail if principal visibility or other validations continue. No success/hosted HTTP claims before actual Owner output.
- **New scoped Owner consent is required**, because the prior H2AD1 attempt was consumed and H2AD3 only authorizes analysis. Do not supply/execute the script's live command until the Owner expressly approves exactly one *additional* restricted IAM set attempt after this diagnosis. This is not blanket security risk acceptance.
- After H2AD4 successful actual readback, proceed with already approved SINGLE paused Scheduler job and one manually triggered read-only `GET /healthz`, separately verify delivery and UID/ETag-guarded cleanup. A one-shot health probe doesn't finish Step05; real seller/buyer hosted G2–G6 paths remain open.

**Owner decision to request:** "હાલની Test Service Account (UID `110217058111344002447`) માટે માત્ર `oldx-c2-h2-private-gateway` પર `roles/run.invoker` ઉમેરવાનો એક નવો guarded પ્રયાસ મંજૂર છે? Ownerની permission યથાવત્ અને Product OFF રહેશે."

## Accurate gates

`H2AD3=OWNER_ACTUAL_AUDIT_READ_PASS_WITH_LIMITS_CONSUMED`;
`H2AD1=SA_CREATED_IAM400_STOP_CONSUMED`;
`H2AD2=OWNER_ONLY_PROBE_NOT_GRANTED_CONSUMED`;
`H2AD4=SOURCE_READY_AWAITING_EXPLICIT_NEW_IAM_WRITE_APPROVAL`;
`H2AD_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
