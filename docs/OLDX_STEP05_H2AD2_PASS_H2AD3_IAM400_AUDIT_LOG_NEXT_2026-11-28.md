# BAJUTO / OLDX Step05 — H2AD2 actual owner-only readback PASS; H2AD3 one new audit-log diagnosis

## 28 Nov 2026, screenshot of Owner actual Ubuntu WSL execution

Owner ran source `scripts/step05_h2ad2_after_400_sa_iam_reconciliation_readonly_once_20261128.py`, creation commit `3d91910dbb909eb99513f83bcd92a1047d18dd0f`, Git blob `920f73f5cd022f1d30a4897452fdd7623a8a0a96`, after exact hash/AST checks. Actual stdout (not a simulated run):

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

Reconcile outcome: **the exact newly created H2AD1 test Service Account exists/enabled UID `110217058111344002447`; the exact new private Cloud Run Gateway remains internal/OFF/immutable and direct service IAM still Owner-only**. H2AD1's single IAM write returned HTTP400, its response body was discarded, and H2AD2 proves the new probe `roles/run.invoker` binding did not appear. We do **not** know why HTTP400 was returned; no claim of an etag error, propagation failure, org constraint or bad request schema is justified without separate evidence. No new job, no hosted HTTP test, no new cloud write in H2AD2; production H2 NO-GO.

**Consumed no-repeat:** `/root/.oldx-step05-h2ad2-after-400-reconcile-readonly-once-20261128` and older H2AD1/H2AD0/H2AC/H2AB/H2AA/H2Z/H2Y/H2W/H2U/H2V one-shots. Preserve markers and cloud state. Do not recreate another probe SA, retry the rejected policy write, modify project IAM, switch ingress public, or prematurely cleanup.

## H2AD3 source-only — new read-only audit logs reason lookup (NOT executed)

The original H2AD1 did not retain the HTTP400 response body, so Google Cloud's Admin Activity logs **might** contain a status/message for that `SetIamPolicy` attempt. Official Google Cloud references:
- https://docs.cloud.google.com/iam/docs/review-iam-policy-history
- https://docs.cloud.google.com/logging/docs/audit-logging
- https://docs.cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list

New frozen source `scripts/step05_h2ad3_failed_iam400_audit_log_readonly_once_20261128.py`
- Commit `cd8598692d35070babbd0bd30d859ef04d6136a4`; Git blob `feaa022f91054120baa9d71ef8bc7b71fb05241f` (readback and static allowlist/marker checks verified).
- Uses same isolated native Owner WSL SDK and OAuth; prior H2AD2 root-only marker exact project, Gateway UID and probe SA UID `110217058111344002447` must match.
- Creates new `/root/.oldx-step05-h2ad3-iam400-admin-activity-logs-once-20261128` before remote request and rejects reruns. If partial/STOP, do not clear marker.
- Makes **ONE** `POST https://logging.googleapis.com/v2/entries:list`, which is **READ-ONLY** despite POST: at most 30 Admin Activity audit entries with `SetIamPolicy` in `oldx-staging`, bounded to 27 Nov 2026 UTC 18:35–19:25 (screenshot time ~28 Nov 00:27 IST). Never reads broad contemporary user/app logs or historic IAM, and does not contact Cloud Run service, IAM APIs, Scheduler jobs, KMS or Firestore.
- Inspects only entries matching the exact target Gateway name; prints numeric status code and sanitized error category only, NOT raw audit entries, principal identifiers, email, IAM etags, OAuth bearer or error bodies. If no entry or pagination/403, it **does not establish any error cause**. If a recognizable error category is printed, that is a **hint**, not permission to perform an unapproved IAM write.
- May require `logging.logEntries.list` and an already enabled Cloud Logging API. Does not enable it or grant a role. A 403/disabled API is STOP; no automatic retry.
- GitHub readback/static guard PASS, **no Owner Cloud execution yet**.

### Exactly one new root Ubuntu WSL command — H2AD3 only

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad3-audit.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad3.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/cd8598692d35070babbd0bd30d859ef04d6136a4/scripts/step05_h2ad3_failed_iam400_audit_log_readonly_once_20261128.py' &&
test "$(git hash-object "$d/h2ad3.py")" = 'feaa022f91054120baa9d71ef8bc7b71fb05241f' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad3.py" &&
python3 -B "$d/h2ad3.py" --h2ad3-iam400-exact-admin-activity-readonly-once
```

**If H2AD3 read succeeds**: examine `H2AD3_EXACT_GATEWAY_ENTRIES` and sanitized `H2AD3_MATCH_*_CATEGORY` to determine whether focused, separately authorized IAM correction is justified. No raw PASS promised. **If no log match or 403**: do NOT assert a root cause. Choose a separate narrowly scoped alternative, without creating SA again or modifying owner policy automatically.

**Step05:** `H2AD2=ACTUAL_PASS_SA_EXISTS_OWNER_ONLY_CONSUMED`; `H2AD3=READ_ONLY_SOURCE_READY_UNRUN`; `H2AD_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `H2=NO_GO`; `PRODUCTION=NO_GO`. Even successful OFF-only health does not close remaining real Gateway/KMS/Auth/Firestore/media/enabled seller/buyer acceptance gates.
