# OLDX Step05 C1A — Actual v2 reconciling field ABSENT confirmed; new guarded service-only deletion source

**26 Nov 2026 IST — owner evidence received, new source prepared; NO DELETE executed in this new step.** Repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`.

## Actual screenshot — completed distinct read-only diagnostic

The owner launched the pinned `9ceec4c76e4b20cfbd7c785c2f47ba7fa2e046f7` read-only Cloud Run v2 diagnostic once. Terminal output:
```
C1A_DIAG_RESULT=READ_ONLY_DIAG_COMPLETE
C1A_DIAG_REASON=EXACT_SERVICE_UID_MATCH
C1A_V2_RECONCILING=ABSENT
C1A_V2_GENERATION=MATCH
C1A_V2_TERMINAL_CONDITION=CONDITION_SUCCEEDED
C1A_V2_REVISION_PAIR=MATCH
C1A_V2_SERVICE_ACCOUNT=MATCH
C1A_V2_IMAGE=MATCH
C1A_V2_ETAG=PRESENT
C1A_V2_TRAFFIC=PRESENT
C1A_V2_TRAFFIC_STATUSES=PRESENT
C1A_V2_RECONCILING_ROOT_CAUSE=MISSING_FIELD_CAUSED_STRICT_FALSE_GUARD
C1A_DIAG_CLOUD_WRITES=NONE
C1A_RESOURCE_DELETED=NO
```
This **CONFIRMS** the source-level reason for the preceding C1A service delete `STOP / C1A_RECONCILING_OR_UNKNOWN / WRITE_ATTEMPTED=FALSE`: the original strict Python `service.get('reconciling') is False` condition rejects the *absent* field (common proto3 default-false JSON omission), even though independent v2 observedGeneration equals generation and the terminalCondition is `CONDITION_SUCCEEDED`. **No previous or current delete request was sent**. The original deletion marker and read-only diagnostic marker were **each CONSUMED**. Do not rerun/delete/reuse either, nor repeat the earlier C1A preflight/old tests, H1A or S3/S3B.

The diagnostic proves only the listed fields and exact service UID at the moment of read, **not** the fresh service IAM, Eventarc dependency status, desired/observed traffic content, effective permissions or deletion success.

## NEW distinct guarded C1A SERVICE-ONLY one-shot

Within owner's prior **explicit guarded C1A-only cleanup** approval, a corrected *separate* immutable Python source file is prepared:
- Path `scripts/step05_c1a_conditional_service_cleanup_v2_once_20261126.py`
- Git pinned first-containing commit `f4e6cf371629192f99eb34f246e2b1b3fe67d708`
- Verified Git blob `c06ba137af39569f7dccfb28700b494207494a33`
- Independent SHA256 from exact GitHub readback `b14ec3337da93fe31c8bd3f5dce9279e3aa776be743c8e5839ab5ba89b6db5a5`
- Derived from previously frozen code; changes are only **new marker**, **new exact CLI flag**, **mandatory original failed-delete marker plus successful diagnostic marker AND sanitized private receipt**, and **fail-closed reconciling validator fix**. Does not broaden original deletion targets.

New validator only accepts **absent** or **explicit false** `reconciling`, AND requires `terminalCondition.state == CONDITION_SUCCEEDED`, unchanged generation, ready+created revision, template runtime SA, digest, IAM check, image, desired/observed traffic, UID, ETag and all old gates. Null, true, failed/missing terminal condition, changed target/UID/revision or any unverified state STOP. Its embedded self-check includes **absent field positive**, **explicit false positive**, **true/UID/IAM bypass rejection**, **terminal-condition failure rejection** and Eventarc exact/full-path dependency rejection. The embedded checks have **NOT been run** in the Owner Cloud Shell yet; source static readback verified only.

**New marker** `~/.oldx-step05-c1a-conditional-service-delete-v2-once-20261126` is distinct from all consumed markers. The script reads prior private receipts, then performs fresh exact C1A service v2 GET, direct IAM policy read and region Eventarc trigger list. Any mismatch, missing permission/dependency or API error STOP before real deletion; it uses same fresh ETag first for `DELETE?validateOnly=true` and only if valid submits at most ONE REAL `DELETE?etag=...` of **ONLY `projects/oldx-staging/locations/asia-south1/services/oldx-step05-gateway`**. Real DELETE is destructive and Cloud Run removes the service and its revisions. It does NOT delete the separately retained runtime SA or image/repository, change IAM, H1B, Firebase or other old assets. A successful delete response is an async operation, not proof of service absence; after any write/timeout do NOT retry. For real status use a new separate **read-only** operation/service receipt.

Official Google reference confirms v2 `DELETE` accepts `etag` and `validateOnly`: https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/delete . Cloud Run v2 service `reconciling` and terminal conditions: https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services and https://docs.cloud.google.com/run/docs/reference/rest/v2/Condition .

## Exact Owner Google Cloud Shell command — one new C1A-only attempt

Requires owner's **already-authenticated Google Cloud Shell**, NOT Windows CMD/WSL. Use entire one-paste block without outer parentheses:

```bash
bash -euo pipefail <<'OLDX_C1A_DELETE_V2'
umask 077
d=$(mktemp -d "$HOME/oldx-c1a-delete-v2-source.XXXXXXXX")
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/delete_v2.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/f4e6cf371629192f99eb34f246e2b1b3fe67d708/scripts/step05_c1a_conditional_service_cleanup_v2_once_20261126.py'
printf '%s  %s\n' 'b14ec3337da93fe31c8bd3f5dce9279e3aa776be743c8e5839ab5ba89b6db5a5' "$d/delete_v2.py" | sha256sum --check --status
python3 -B "$d/delete_v2.py" --delete-only-c1a-service-v2-once
OLDX_C1A_DELETE_V2
```

Only downloads immutable source from pinned GitHub commit and checks SHA256 before local execution. **If `C1A_SERVICE_DELETE_RESULT=STOP` and `C1A_WRITE_ATTEMPTED=FALSE`, no deletion was sent and new marker is consumed.** If result is `WRITE_OUTCOME_UNKNOWN_STOP`, a real deletion request may have been sent; never resend. If result `DELETE_ACCEPTED_PENDING_COMPLETION` or `DELETE_OPERATION_DONE_NEEDS_READBACK`, a new read-only operation/service-status verification remains mandatory. Never delete old marker or retry a one-shot on failure. Share only `C1A_` screenshot; do not upload logs, API token or entire private evidence.

## Gates still intact

`C1A_LOCAL_READONLY_PREFLIGHT=ACTUAL_PASS_WITH_LIMITS_CONSUMED`, `C1A_FIRST_DELETE=STOP_NO_WRITE_CONSUMED`, `C1A_V2_DIAGNOSTIC=ACTUAL_READ_ONLY_DIAG_COMPLETE_CONSUMED`, `C1A_SECOND_SERVICE_DELETE=PREPARED_NOT_RUN`. Existing C1A private OFF retention approval expires **28 Nov 2026 23:19 IST** with no automatic extension or cleanup. No C1A service, runtime SA or registry image deleted yet. No H1B W1–W6 deployment, H2 or production permission.
