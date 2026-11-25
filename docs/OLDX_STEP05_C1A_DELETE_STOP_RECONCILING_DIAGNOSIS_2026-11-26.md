# OLDX Step05 C1A — real conditional delete STOP before write; reconciling-only diagnosis

**26 November 2026 IST.** Branch `security-hardening-review`. This is newer than [C1A service-only delete packet](OLDX_STEP05_C1A_GUARDED_CONDITIONAL_SERVICE_DELETE_OWNER_APPROVED_2026-11-26.md). **No C1A resource was deleted; no actual delete request was sent.**

## 1. ACTUAL owner Cloud Shell screenshot, exact result

Owner executed pinned `9d221bc5b037433e151308cc91f61b010d846e03` C1A service-only delete source once under prior limited C1A cleanup consent. New terminal screenshot prints:

```text
C1A_LOCAL_GUARDS=PASS_SYNTHETIC_NO_CLOUD
C1A_SERVICE_DELETE_RESULT=STOP
C1A_REASON=C1A_RECONCILING_OR_UNKNOWN
C1A_WRITE_ATTEMPTED=FALSE
C1A_SERVICE_ACCOUNT_DELETED=NO
C1A_REGISTRY_IMAGE_DELETED=NO
C1A_UNRELATED_RESOURCES_CHANGED=NONE_REQUESTED
```

The exact original Python code in `inspect_current` first verifies `name`, service UID and etag and then demands `service.get('reconciling') is False`. Thus current v2 GET and these initial checks succeeded, but **the script did not disclose whether the actual `reconciling` JSON field was absent, true, null or another value**. The current generation, revision, traffic, template, IAM, Eventarc, `validateOnly` and real DELETE guards in this second script were not reached. In particular, **never infer service deletion, an IAM mutation, successful downstream identity checks or actual reconciliation state from this STOP**.

Separate original **C1A read-only** preflight remains historically `READ_ONLY_PASS_WITH_LIMITS`, `service,service_iam,revisions,runtime_sa` PASS, but was consumed prior to this STOP.

The first conditional-delete one-shot marker `~/.oldx-step05-c1a-conditional-service-delete-once-20261126` is now **CONSUMED** with `RESULT=STOP`, `REASON=C1A_RECONCILING_OR_UNKNOWN`, `WRITE_ATTEMPTED=False`. **DO NOT rerun, reset/delete marker, reissue DELETE, modify resources or repeat old C1A/B probes.**

## 2. Source-level explanation and limits

Google Cloud Run v2's `reconciling` field is an output-only Boolean. A true value means active reconciliation; after reconciliation it is false. REST JSON may omit default false Boolean fields; the original code's strict requirement `service.get('reconciling') is False` also STOPs on an **absent** field. This is a **plausible source validation mismatch, NOT a proven runtime cause** without one more fresh, narrow read. Also check `terminalCondition.state` and observed/generation equivalence; those are separately important for readiness, but no automatic reinterpretation of missing `reconciling` as healthy is authorized by this note.

Official docs: https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services (reconciling/observed generation/terminal condition), https://docs.cloud.google.com/go/docs/reference/cloud.google.com/go/run/latest/apiv2/runpb (protobuf JSON omitted-default encoding).

## 3. NEW and independent diagnostic, NO cloud resource mutations

NEW `scripts/step05_c1a_v2_reconciling_readonly_diagnostic_once_20261126.py`, first immutable commit `9ceec4c76e4b20cfbd7c785c2f47ba7fa2e046f7`, exact Git blob `38b30ab62dec78954ad341193c9e4c79208cba6c`, SHA256 of GitHub read-back exact source bytes `9eea272ebc554a03257a2e28e07a7fc9aee4bf3ea3826ce626c3cf126d9d217f`. No external runnable binary/image, no previously consumed script modified. Source was read back and SHA256 independently verified; owner Cloud Shell execution still **NOT OBSERVED**.

This new script:
- Guards exact owner/nonroot Cloud Shell and checks *original consumed delete marker* must have `RESULT=STOP`, `REASON=C1A_RECONCILING_OR_UNKNOWN`, `WRITE_ATTEMPTED=False` before any token or Cloud request. Does not touch original marker contents.
- Creates a **separate** one-shot local marker `~/.oldx-step05-c1a-v2-reconciling-readonly-once-20261126` before any live read. Only retrieves the exact Owner's access token without displaying/storing it, then makes **one direct Cloud Run v2 HTTPS GET** of **only** `projects/oldx-staging/locations/asia-south1/services/oldx-step05-gateway`, TLS verified, 20s timeout, no redirects/proxy or retry.
- Requires the **full exact service name + frozen UID**, then prints **sanitized status only**: `reconciling` field is `ABSENT`, `EXPLICIT_FALSE`, `EXPLICIT_TRUE`, or invalid; generation/observed match, terminalCondition state, revision pair, runtime SA/image digest yes/no, etag and traffic statuses presence. Does NOT print access token, full service JSON or IAM metadata. Private sanitized receipt in `~/oldx-c1a-v2-reconciling-diagnostic-<UTC>/sanitized-diagnostic.json`.
- NO DELETE, `validateOnly`, IAM write, SA/image/Registry cleanup, login, account switch, Cloud Run revision/traffic modification, H1B operations, Firebase or billing change. A STOP consumes only the **new** diagnostic marker; do not rerun it or assume permissions.
- **Do not call diagnosis success C1A cleanup success.** Even if the field is absent/explicit false, a NEW separate owner-supervised deletion action with fresh etag and all safety/dependency checks remains to be designed and is NOT executed by this read.

## 4. One-paste Owner Google Cloud Shell — DIAGNOSIS ONLY

Paste below in **existing Owner Google Cloud Shell**, not Windows CMD/WSL, and do not add outer `(` or `)`:

```bash
bash -euo pipefail <<'OLDX_C1A_V2_DIAG'
umask 077
d=$(mktemp -d "$HOME/oldx-c1a-v2-diag-source.XXXXXXXX")
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/diag.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/9ceec4c76e4b20cfbd7c785c2f47ba7fa2e046f7/scripts/step05_c1a_v2_reconciling_readonly_diagnostic_once_20261126.py'
printf '%s  %s\n' '9eea272ebc554a03257a2e28e07a7fc9aee4bf3ea3826ce626c3cf126d9d217f' "$d/diag.py" | sha256sum --check --status
python3 -B "$d/diag.py" --inspect-existing-v2-once
OLDX_C1A_V2_DIAG
```

If source fetch/hash fails, the Python diagnostic is not invoked; report the error without changing URL or SHA. If it runs and STOPs, the new marker is consumed; never retry automatically. Share only `C1A_DIAG_RESULT`, `C1A_DIAG_REASON` and `C1A_V2_` lines/screenshot. Every run should print `C1A_DIAG_CLOUD_WRITES=NONE` and `C1A_RESOURCE_DELETED=NO` if script reaches its final section.

## 5. Gates unchanged

Original C1A retention permission ends **28 November 2026 23:19 Asia/Kolkata**; no scheduled automatic deletion or extension. The original owner’s C1A exact-guarded cleanup approval remains in force, but a consumed STOP marker cannot be bypassed. After fresh read-only diagnosis, decide whether to prepare a strictly safer **new** guarded service-only one-shot with complete prerequisites, or stop for live reconciliation/dependency changes. No H1B W1–W6 writes; H2 and production NO-GO. Historical H1A/S1/S1R/S2/S3/S3B and C1A/C1B completed checks/builds/scans stay consumed, never redo.
