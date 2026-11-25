# OLDX Step05 C1A — Actual owner preflight PASS; guarded service-only conditional delete prepared

**26 November 2026 IST — source-ready / owner Cloud Shell deletion NOT YET EXECUTED.** Branch `security-hardening-review`, repository `yasminparmar087-ops/oldx-website`. This is downstream of [the owner's scoped C1A cleanup authorization and preflight](OLDX_STEP05_C1A_OWNER_APPROVED_GUARDED_CLEANUP_PREFLIGHT_2026-11-26.md); it does NOT expand cleanup beyond C1A.

## 1. Actual completed owner Cloud Shell evidence

User's screenshot after the specifically approved, source-hash-pinned Cloud Shell preflight shows:

```text
C1A_VERIFIED_STAGES=service,service_iam,revisions,runtime_sa
C1A_CLEANUP_PREFLIGHT=READ_ONLY_PASS_WITH_LIMITS
C1A_REASON=EXACT_HISTORIC_C1A_IDENTIFIERS_MATCH
C1A_CLOUD_WRITES=NONE
C1A_RESOURCE_DELETED=NO
```

Therefore the ORIGINAL newly created C1A `oldx-step05-gateway` in project `oldx-staging`, region `asia-south1`, historically frozen service UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`, one revision `oldx-step05-gateway-00001-thd`, runtime SA `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com` uniqueId `102194769236111252832`, exact immutable image `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`, one 100% route/no traffic tag, no direct Invoker IAM binding, no env/volumes were checked by the approved read-only script. **Those reads may become stale and did not delete anything.** Original read-only one-shot marker `~/.oldx-step05-c1a-cleanup-readonly-once-20261126` is now CONSUMED and must not be deleted or rerun.

Owner's earlier explicit **"ha manjuri chhe"** authorizes only exact new C1A resource cleanup after matching UID/dependency guards; DOES NOT authorize service account/image automatic deletion or any H1B/other Cloud mutation. Before this new script runs, **no C1A deletion has happened**.

## 2. Distinct next guarded service-only one-shot

NEW script `scripts/step05_c1a_conditional_service_cleanup_once_20261126.py`, pinned final immutable commit **`9d221bc5b037433e151308cc91f61b010d846e03`**, Git blob **`b9444ffd37119f05b9bb7c1e0586e623ab7e5c41`**, independently computed exact GitHub file bytes SHA256 **`0950110ffb31310da5bb2d4ea83f8656dc16728dbf6d40088cb5deaa5e626d00`** (source fetched back at pinned commit). Previous intermediate sources `ac0dd1c...`, `b47c89b...` are NOT the operational source.

The script's one actual **conditional** write targets only Cloud Run Admin v2 `DELETE https://run.googleapis.com/v2/projects/oldx-staging/locations/asia-south1/services/oldx-step05-gateway?etag=<fresh-readback-etag>`. Google documents v2 `DeleteServiceRequest.etag` and `validate_only` as supported request fields: [official API RPC](https://docs.cloud.google.com/run/docs/reference/rpc/google.cloud.run.v2), [service management/deletion semantics](https://docs.cloud.google.com/run/docs/managing/services). A write is NOT attempted unless all prior source and live guards pass.

**Safety gates, in exact order:**
1. Exact owner nonroot Cloud Shell; original consumed C1A preflight marker and private files prove `PASS_WITH_LIMITS`, exact UID/one revision/direct IAM empty/SA UID, not a regenerated response. The new script has an embedded **synthetic local self-check** for correct UID/etag, rejection of changed UID/reconciling/disabled IAM, catching exact and full-path Eventarc dependencies, and public direct IAM binding rejection; it must PASS before any live request.
2. A DIFFERENT NEW one-shot marker `~/.oldx-step05-c1a-conditional-service-delete-once-20261126` is created **before any live Cloud command**. Do not delete or replay it on timeout, error or partial result. Private evidence in `~/oldx-c1a-service-delete-<UTC>`.
3. Obtain exact Owner's access token in child subprocess without printing/storing it; direct Cloud Run v2 **GET** with TLS. Must freshly match **full resource name, original immutable UID, exact ready/created revision, SA email, immutable image, no secrets/env/volume, one 100%-route/no tag, IAM Invoker check not disabled, no active reconciliation, generation matches observed, and nonempty etag**. Any mismatch stops before write.
4. Narrow re-read exact C1A service-level IAM (no direct bindings) and same-region Eventarc trigger list; if any dependency references exact C1A service name (short or full path), or the dependency inspection is unavailable/permission denied, STOP. This is a bounded safety read, not a replay of old C1A tests/builds or broad project audit.
5. Call v2 **DELETE validateOnly=true** with the exact fresh etag. This *does not delete the service*. It must return a recognizable named operation. If validation fails/unknown, STOP.
6. Call **ONE REAL etag-conditional DELETE** only after all guards; no retry. A successful Cloud Run v2 response is an asynchronous **operation receipt**, not instant proof that the service has disappeared. The script records `DELETE_ACCEPTED_PENDING_COMPLETION` or `DELETE_OPERATION_DONE_NEEDS_READBACK` (or a STOP), and does **not** declare full cleanup. If a network error occurs after write may have been attempted, `WRITE_OUTCOME_UNKNOWN_STOP` and manual readback only, NO retry/deletion of something else.

**Never included in this source:** `gcloud run services delete` by mutable name without etag; any SA delete, Artifact Registry image/tag/repository delete, other revisions or traffic edits, IAM changes, owner-read or H1B changes. This operation is irreversible if successful; Google states deletion removes all revisions but not Artifact Registry images. Future C1A SA and image cleanup each require distinct independent no-other-reference checks and no blanket delete.

**Testing claim limit:** Source is read-back and SHA256 verified. Its embedded synthetic guards are authored but have **not been executed against owner Cloud Shell**; they will run locally BEFORE marker/API at the next owner invocation. No new live Cloud request or delete has occurred as of writing this handoff. Do not claim deployment/cleanup PASS without actual owner result.

## 3. Exact one-paste Owner Cloud Shell command — SERVICE ONLY

Use only Owner Google Cloud Shell `yasminparmar087@cloudshell` under `oldx-staging`; NOT Windows CMD, WSL or an unauthenticated SDK. All lines from opening `bash` to ending delimiter inclusive. No enclosing `(` / `)` characters.

```bash
bash -euo pipefail <<'OLDX_C1A_DELETE'
umask 077
d=$(mktemp -d "$HOME/oldx-c1a-delete-source.XXXXXXXX")
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/delete.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/9d221bc5b037433e151308cc91f61b010d846e03/scripts/step05_c1a_conditional_service_cleanup_once_20261126.py'
printf '%s  %s\n' '0950110ffb31310da5bb2d4ea83f8656dc16728dbf6d40088cb5deaa5e626d00' "$d/delete.py" | sha256sum --check --status
python3 -B "$d/delete.py" --delete-only-c1a-service-once
OLDX_C1A_DELETE
```

The bootstrap downloads only this pinned Python SOURCE, not a binary/image. The hash check must PASS before the one-shot process runs. If source retrieval fails, no deletion marker is consumed. If script STOPs after marker creation, marker is consumed: DO NOT rerun or bypass the gate. Keep full stdout/stderr/access token private; share only `C1A_` result lines/screenshots.

Expected safe result classes, **not predicted outcomes**:
- `C1A_SERVICE_DELETE_RESULT=STOP_PREFLIGHT` or `STOP`: no delete requested if `C1A_WRITE_ATTEMPTED=FALSE`.
- `C1A_SERVICE_DELETE_RESULT=WRITE_OUTCOME_UNKNOWN_STOP`: real request might have been sent; **NEVER retry**; inspect exact current service/operation separately.
- `C1A_SERVICE_DELETE_RESULT=DELETE_ACCEPTED_PENDING_COMPLETION`: API accepted one delete; **NOT service deletion confirmed**; inspect named operation and exact service absence separately.
- `C1A_SERVICE_DELETE_RESULT=DELETE_OPERATION_DONE_NEEDS_READBACK`: same, service removal still requires independent verification.
- Every result prints `C1A_SERVICE_ACCOUNT_DELETED=NO` and `C1A_REGISTRY_IMAGE_DELETED=NO` because those are not part of this operation.

## 4. Continuing after actual result

1. If delete accepted/done: one **new** read-only check of exact Cloud Run long-running operation and service absent/deleting state, never issue same DELETE twice.
2. Only when Cloud Run deletion independently confirmed: check whether C1A SA (uniqueId frozen) is referenced by any other workload and whether C1A image digest/tag is referenced by any other service/revision before proposing their **separate guarded** deletion. On uncertain inventories/errors, retain and record PARTIAL cleanup without pretending C1A completely gone. Never delete shared `oldx-staging-images` repository.
3. C1A retention previously approved through **28 Nov 2026 23:19 Asia/Kolkata**, no automatic timer or cleanup. This owner-approved one-shot script is a supervised action, not scheduled. Step05 H1B W1–W6, H2 and production remain NO-GO.

**Actual state before owner next command**: `C1A_READONLY_PREFLIGHT=PASS_WITH_LIMITS_CONSUMED`, `C1A_SERVICE_DELETE=OWNER_AUTHORIZED_SOURCE_PREPARED_NOT_RUN`, `SA_AND_IMAGE_DELETE=NOT_PERFORMED`, `H1B_CLOUD_WRITES=NOT_AUTHORIZED`.
