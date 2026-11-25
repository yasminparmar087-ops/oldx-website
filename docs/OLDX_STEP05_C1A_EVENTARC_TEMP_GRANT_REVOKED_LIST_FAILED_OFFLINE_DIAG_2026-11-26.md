# OLDX Step 05 — Actual temporary Eventarc Viewer grant/revoke succeeded, all-location listing FAILED

## Second owner offline screenshot — exact `REASON` punctuation mismatch identified from pinned source

Owner's **offline-only** marker inspection now prints:
```text
ATTEMPT_CONSUMED_MATCH=True
RESULT_MATCH=True
REASON_MATCH=False
REVOKE_MATCH=True
RESULT_SAVED=STOP_WITH_REVOKE_VERIFIED
REASON_SAVED=UNKNOWN_OR_NONSTANDARD
REVOKE_SAVED=REMOVED_AND_VERIFIED
EVIDENCE_POINTER_COUNT=1
LITERAL_NEWLINE_ESCAPES=False
OFFLINE_ONLY=TRUE
```
Pinned original source `scripts/step05_c1a_eventarc_temporary_viewer_read_revoke_once_20261126.py` at immutable `360dd60b6541e2f4cdbbc5583a3f4d75a94b2426` Git blob `bcad5d9a99a515db62086b05e7a89e960ea811a6` was **reopened/verified directly in GitHub**. Its `CLI.json` line 130 constructs `name.upper() + '_' + code`, where name is **`eventarc-all-locations`** line 204. Therefore for a CLI NONZERO error the script saves the literal value **`REASON=EVENTARC-ALL-LOCATIONS_NONZERO`** (hyphens), not the incorrectly anticipated `REASON=EVENTARC_ALL_LOCATIONS_NONZERO` (underscores). Likewise the previous offline diagnostic's allowlist `[A-Z0-9_]` rejected hyphens, yielding `REASON_SAVED=UNKNOWN_OR_NONSTANDARD`. This is a **confirmed code-to-diagnostic format mismatch**, not new Cloud error or revocation failure. It explains the visible marker mismatch; the preserved Eventarc stderr still must be read to determine *why* CLI exited nonzero. No marker changed.

**Next zero-Cloud step:** local Python must validate exact hyphenated REASON; verify RESULT, REVOKE, evidence path and summary; only then read the **previously saved** `eventarc-all-locations.exit` and `eventarc-all-locations.stderr`, output a sanitized error classification/line. No `gcloud`, IAM grant/revoke, fresh list or deletion. Exact revocation remained `REMOVED_AND_VERIFIED`; C1A service/SA/image not deleted. All markers remain consumed. No further Cloud IAM grant authorized.

## New owner screenshot — offline marker guard STOP, NOT an Eventarc retry

The user ran the **local Python-only** snippet from the prior handoff to inspect saved Eventarc error data. Its observable terminal output ended **`STOP: MARKER_MISMATCH`**; the snippet exited during its **marker subset assertion**, before reading the existing `summary.json`, `eventarc-all-locations.exit`, or `eventarc-all-locations.stderr`. Therefore **the saved Eventarc CLI error is still unclassified**. This is a new **offline inspection failure** only; it is **NOT a Cloud IAM/revoke failure**, not a fresh Eventarc API call, not a new deletion attempt and does not supersede the previous actual `C1A_EVENTARC_REVOKE=REMOVED_AND_VERIFIED` Cloud Shell readback. Do not assert what exact marker field differed; screenshot does not show its contents.

**Next zero-Cloud diagnostic**: inspect ONLY the consumed marker’s bounded length, owner/symlink state, presence of `ATTEMPT_CONSUMED`, `EVIDENCE=` pointer count, and whitelisted `RESULT`, `REASON`, `REVOKE` values, without printing the evidence path or private IAM payload. Compare exact expected `RESULT=STOP_WITH_REVOKE_VERIFIED`, `REASON=EVENTARC_ALL_LOCATIONS_NONZERO`, `REVOKE=REMOVED_AND_VERIFIED` separately. If mismatch, preserve all original bytes for reconciliation, never change the marker or loosen guard blindly. **No `gcloud`, no IAM add/remove, no service DELETE, no reruns.**

**26 Nov 2026 IST.** Owner screenshot in authenticated `yasminparmar087@cloudshell` (project `oldx-staging`) after the immutable script at `360dd60b6541e2f4cdbbc5583a3f4d75a94b2426`. This record supersedes prior `NOT_EXECUTED` wording in [original temp-viewer plan](OLDX_STEP05_C1A_TEMP_EVENTARC_VIEWER_OWNER_APPROVAL_AND_ONE_SHOT_2026-11-26.md). This assistant has not itself made Google Cloud calls.

## Exact actual screenshot

```text
C1A_EVENTARC_GRANTED=TRUE
C1A_EVENTARC_LIST=NOT_QUERIED
C1A_EVENTARC_REVOKE=REMOVED_AND_VERIFIED
C1A_EVENTARC_TEMP_EXPIRES_UTC=2026-11-25T20:06:26Z
C1A_EVENTARC_RESULT=STOP_WITH_REVOKE_VERIFIED
C1A_EVENTARC_REASON=EVENTARC_ALL_LOCATIONS_NONZERO
C1A_CLOUD_RUN_DELETED=NO
C1A_SERVICE_ACCOUNT_DELETED=NO
C1A_REGISTRY_IMAGE_DELETED=NO
```

**Important parser semantics**: `LIST=NOT_QUERIED` is the default local `list_result` retained when the attempted CLI `gcloud eventarc triggers list --location=-` exits nonzero. The code **did attempt one all-location list command**, but had **no successful returned listing**, so it cannot establish either presence or absence of C1A triggers. Do NOT infer that no list command was issued, or that there are zero triggers.

The exact conditional IAM grant was verified active, then the script's `finally` ran the precise remove operation and a separate project IAM policy readback; `REMOVED_AND_VERIFIED` confirms the **newly introduced conditional Viewer binding is absent** in that readback. Do NOT claim every other IAM binding is absent, or deletion succeeded. The 25-minute conditional expiry was `2026-11-25T20:06:26Z`; expiry is a secondary safeguard, **not** proof of revocation by itself. No C1A Cloud Run service, C1A SA or Registry image was deleted, no service-delete request was sent by this Eventarc workflow. There were IAM **grant + remove writes**, so do not claim `CLOUD_WRITES=NONE` globally.

The distinct one-shot marker `~/.oldx-step05-c1a-eventarc-temp-viewer-grant-list-revoke-once-20261126` is now **CONSUMED**. DO NOT rerun grant/list/revoke, delete markers, repeat prior C1A guarded delete attempts, rescan H1A or redo S3/S3B. The earlier Eventarc regional read was permission denied; the new all-locations read nonzero's underlying cause **UNKNOWN** until the existing saved private stderr is examined. Could be IAM propagation/permissions/flag/API errors, but none is yet verified.

## Next step: OFFLINE saved error inspection only — no new IAM or Cloud calls

The pinned source writes the attempted list's private evidence to `~/oldx-c1a-eventarc-temp-viewer-<UTC>/eventarc-all-locations.exit` and `eventarc-all-locations.stderr`, with folder stored as `EVIDENCE=<path>` in the consumed marker. It also writes `summary.json`. One small Python read of those **already saved** files, after validating exact marker/summary state, can classify the actual failure. Do **not** upload unredacted stderr/IAM policies or credentials to GitHub. Do not use `gcloud` in the offline inspection. Since the source captured errors locally, there is no reason to grant Viewer again before reading the saved error.

Minimal expected offline output is sanitized `C1A_SAVED_LIST_EXIT`, `C1A_SAVED_LIST_ERROR_CLASS`, `C1A_SAVED_LIST_ERROR_DETAIL` if safely redacted, and `OFFLINE_ONLY=TRUE`. Do not claim root cause until actual output arrives. Exact helpful possible classes: permission propagation/403, CLI flag, Eventarc API disabled, unsupported aggregation or other. If there is an ambiguous error, preserve stopped state rather than guessing.

After the saved error is classified, decide **separately** whether a different read-only method is technically needed; any new grant is a new IAM mutation requiring an explicit owner approval. Google's documented `gcloud eventarc triggers list --location=-` is the official all-location form: https://docs.cloud.google.com/sdk/gcloud/reference/eventarc/triggers/list. A failed aggregate response must NEVER be converted to a successful empty list. Existing C1A guarded cleanup remains blocked on dependency visibility.

## Current safety, deadline and handoff

`C1A_TEMP_GRANT=ACTUAL_TRUE`; `C1A_TEMP_REVOKE=ACTUAL_REMOVED_AND_VERIFIED`; `C1A_EVENTARC_AGGREGATE_LIST=NONZERO_UNKNOWN_CAUSE`; `C1A_SERVICE_DELETED=NO`; `C1A_RUNTIME_SA_DELETED=NO`; `C1A_REGISTRY_IMAGE_DELETED=NO`; `C1A_ALL_OLD_ONE_SHOTS=CONSUMED`; `H1B_W1-W6/H2/PRODUCTION=NO_GO`. Original C1A private OFF retention owner authorization ends **28 Nov 2026 23:19 IST**, no scheduled deletion/extension. Do not let the deadline trigger an unauthorized bypass.
