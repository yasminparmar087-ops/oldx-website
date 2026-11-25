# OLDX Step 05 — C1A Option B exact deletion ACCEPTED; final operation/service readback PENDING

**2026-11-26 ~01:32 IST** Owner's actual Google Cloud Shell screenshot, `oldx-staging`; work on GitHub `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`.

## 1. What actually happened

User executed hash-checked immutable [C1A Option B service-only one-shot](https://github.com/yasminparmar087-ops/oldx-website/blob/388a485b72ebdb7885176dba3ceb839b0202fba8/scripts/step05_c1a_option_b_service_only_conditional_delete_once_20261126.py) under the owner-approved limited unknown Eventarc dependency risk exception. **Actual** terminal output:

```text
C1A_LOCAL_GUARDS=PASS_SYNTHETIC_NO_CLOUD
C1A_OPTION_B_EVENTARC_RISK=OWNER_ACCEPTED_UNVERIFIED
C1A_EVENTARC_CHECK=NOT_RUN_BY_EXPLICIT_EXCEPTION
C1A_SERVICE_DELETE_RESULT=DELETE_ACCEPTED_PENDING_COMPLETION
C1A_REASON=AWAIT_INDEPENDENT_OPERATION_AND_SERVICE_CHECK
C1A_WRITE_ATTEMPTED=TRUE
C1A_SERVICE_ACCOUNT_DELETED=NO
C1A_REGISTRY_IMAGE_DELETED=NO
C1A_UNRELATED_RESOURCES_CHANGED=NONE_REQUESTED
```

**Crucial distinction:** the Cloud Run API returned an operation receipt accepting one real conditional DELETE after the script's fresh UID/revision/image/SA/health/generation/traffic/direct IAM checks and `validateOnly=true` passed. This is **NOT YET** proof the operation completed or the exact service disappeared. Do not claim C1A cleanup fully complete. `WRITE_ATTEMPTED=TRUE` means **NEVER repeat any DELETE**, earlier scripts, reset markers, grant/list/revoke Eventarc, or run a new DELETE of the same mutable service name. The new one-shot local marker `~/.oldx-step05-c1a-option-b-conditional-service-delete-once-20261126` is CONSUMED. The script saved the accepted operation name in private `operation.json` and summary in the `EVIDENCE=` folder named by the marker. No need for user to provide or reveal the full private operation resource name.

No IAM/API enablement/regrant happened in this Option B one-shot; the prior temporary Eventarc Viewer was independently REMOVED_AND_VERIFIED. Eventarc dependency inventory **still UNKNOWN and owner accepted only for this C1A service**. Separate runtime service account and pinned image were **not** deleted. Never touch `oldx-owner-read`, H1B, shared Registry or other resources.

## 2. Only next action: NEW independent one-shot READ-ONLY verification

A dedicated source-only [new readback script](https://github.com/yasminparmar087-ops/oldx-website/blob/6036b39261f7092fb7c64cb756868f9573b875f1/scripts/step05_c1a_option_b_readonly_delete_operation_verify_once_20261126.py) created:
- first-containing immutable commit **`6036b39261f7092fb7c64cb756868f9573b875f1`**;
- Git blob SHA-1 **`da226ab9f3efbc27933ba0a9e85393ec864b6d6b`**, obtained by reading back the exact GitHub source at pinned commit;
- one-time marker `~/.oldx-step05-c1a-option-b-service-delete-readback-once-20261126`, distinct from all consumed markers.

Source safety properties statically verified from GitHub readback:
- Reads original consumed Option B delete marker and private matching `summary.json` / `operation.json`. Requires exact `RESULT=DELETE_ACCEPTED_PENDING_COMPLETION`, `WRITE_ATTEMPTED=True`, exact C1A target name and operation namespace, no previous SA/image deletion.
- Authenticates as expected Owner without printing token, makes only **two bounded HTTPS GET** requests against Cloud Run Admin v2: saved operation's latest state and the exact service `projects/oldx-staging/locations/asia-south1/services/oldx-step05-gateway`; no Cloud writes, no DELETE, no IAM/API/registry action. Google Cloud Run official method: https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.operations/get .
- A result of **`C1A_READBACK_RESULT=CONFIRMED_REMOVED`** requires BOTH `C1A_OPERATION_STATE=DONE_NO_ERROR` and `C1A_SERVICE_STATE=404_NOT_FOUND`. Any operation error, pending state, mismatched original UID, unexpected API status or visible/deleting service is `NOT_YET_CONFIRMED` or `STOP`, never a made-up success. The original service might still be visible for some time while delete completes.
- Persists only sanitized summary in a new private evidence folder `~/oldx-c1a-option-b-delete-readback-<UTC>/summary.json`; sensitive token or raw API payload not printed. Marker consumed even on fail/unknown to avoid uncontrolled replay.
- **No execution in owner's Cloud Shell as of document creation**; not yet actual deletion confirmation. GitHub source syntax can be independently checked with Python `ast.parse` in the command before running, and file bytes checked by `git hash-object` against pinned Git blob. Static source review is NOT actual live verification.

## 3. Exact one-paste Owner Cloud Shell READ-ONLY command

Paste in already-authenticated `yasminparmar087@cloudshell` for `oldx-staging`. **Only retrieval of the new immutable source and two GETs; no Cloud mutation.**

```bash
bash -euo pipefail <<'OLDX_C1A_READBACK'
umask 077
d=$(mktemp -d "$HOME/oldx-c1a-readback-source.XXXXXXXX")
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/readback.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/6036b39261f7092fb7c64cb756868f9573b875f1/scripts/step05_c1a_option_b_readonly_delete_operation_verify_once_20261126.py'
test "$(git hash-object "$d/readback.py")" = 'da226ab9f3efbc27933ba0a9e85393ec864b6d6b' || { echo 'STOP: SOURCE_HASH_MISMATCH'; exit 2; }
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/readback.py"
python3 -B "$d/readback.py" --verify-c1a-option-b-delete-readonly-once
OLDX_C1A_READBACK
```

If source/hash/syntax fails, Python verification has not been invoked; no Cloud reads/writes. If Python runs but returns STOP/PENDING, its distinct marker is consumed; DO NOT repeat the same script or issue deletion. Share only the `C1A_` result lines/screenshot. No proof of full removal unless both operation success and service 404 are observed.

## 4. Ongoing scope and deadline

Prior C1A private OFF retention authorization expires **28 Nov 2026 23:19 IST**. No background/scheduled cleanup or extension, no additional service deletion. If deletion has not finished by then, only read-only tracking/escalation with owner consent; don't override safeguards. C1A SA and Registry image later require independent no-reference checks and separate scoped cleanup decision. H1B W1–W6/H2/production remain NO-GO.

**Checkpoint:** `C1A_CONDITIONAL_DELETE=ACTUAL_ACCEPTED_ASYNC`, `C1A_WRITE_ATTEMPTED=TRUE`, `C1A_SERVICE_REMOVAL=NOT_YET_CONFIRMED`, `C1A_READBACK=PREPARED_NOT_RUN`, `SA_IMAGE_DELETED=NO`, `EVENTARC=UNKNOWN_OWNER_ACCEPTED`.
