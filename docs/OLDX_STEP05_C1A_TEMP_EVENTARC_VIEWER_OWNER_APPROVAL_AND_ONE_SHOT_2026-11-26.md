# OLDX Step 05 C1A — Owner-approved temporary Eventarc Viewer (grant → all-locations read → revoke)

**26 November 2026 IST.** Repository: `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`.

## 1. Actual Owner decision and current state

After actual Owner Cloud Shell receipt `C1A_READ_DIAG_IAM=NO_DIRECT_BINDINGS`, `C1A_READ_DIAG_EVENTARC=PERMISSION_DENIED`, `C1A_READ_DIAG_RESULT=STOP`, `C1A_CLOUD_WRITES=NONE`, `C1A_RESOURCE_DELETED=NO`, Owner replied **"ha manjuri chhe"** specifically to **grant `roles/eventarc.viewer` temporarily to Yasmin's own account for only project `oldx-staging`, inspect Eventarc triggers, then revoke that new permission**. Consent is for this minimal IAM grant/list/revoke lifecycle, NOT for additional permissions, a different principal, public access, Cloud Run/SA/image deletion or H1B deployment.

As of this document, **NO Cloud IAM grant/revoke or new Eventarc list has been executed in Owner Cloud Shell** by the assistant. Cloud Shell command below is for the user to run under the already-authorized account. Existing C1A gateway service, dedicated runtime SA and image remain; historical C1A cleanup retention approval ends **28 Nov 2026 23:19 IST**, no automated deletion.

All earlier C1A read-only, v2-field diagnostic, first/second guarded deletion attempts (both `WRITE_ATTEMPTED=FALSE`), and the latest denied Eventarc read diagnostic have their own **CONSUMED one-shot markers**. Do not delete or rerun.

## 2. Exact IAM grant, read, revoke boundaries

New standalone code `scripts/step05_c1a_eventarc_temporary_viewer_read_revoke_once_20261126.py`, immutable first-containing GitHub commit **`360dd60b6541e2f4cdbbc5583a3f4d75a94b2426`**, exact Git blob **`bcad5d9a99a515db62086b05e7a89e960ea811a6`**, independent SHA256 of exact tested/GitHub-read-back source **`3aa301705aea84a6dbec127984becf405bdf973aaaf9a5eac85e05b8c66f86f5`**. Local source and GitHub blob match exactly.

One new one-shot marker: `~/.oldx-step05-c1a-eventarc-temp-viewer-grant-list-revoke-once-20261126` (consumed before Cloud command). Private evidence in `~/oldx-c1a-eventarc-temp-viewer-<UTC>` owned by Owner, mode 0700. Preserve older evidence and markers. Script:
- Locally requires the *exact* consumed previous C1A diagnostic marker + private saved summary of `IAM=NO_DIRECT_BINDINGS`, `Eventarc=PERMISSION_DENIED`, `writes_attempted=false`.
- Checks the current active Cloud Shell account is **only `yasminparmar087@gmail.com`**, existing project IAM policy under explicit `oldx-staging`, and refuses to mutate an already-preexisting Eventarc Viewer binding for that owner. No Cloud project/identity default changes.
- On that same **project only**, adds **one** conditional IAM role `roles/eventarc.viewer` for `user:yasminparmar087@gmail.com` with a **unique condition title and automatic effective expiry 25 minutes after creation**, expression `request.time < timestamp("<UTC-expiration>")`. This is additional **read-only Eventarc metadata access** and can see other Eventarc resource metadata in the project; not an Eventarc Administrator/Editor grant. Verifies the exact new conditional binding.
- Runs **one** owner-authenticated `gcloud eventarc triggers list --location=- --project=oldx-staging --format=json`, which Google documents as all locations (including global), with a 75-second bound and no retry. Requires complete successful JSON list and known destinations; if any trigger destination points at exact `oldx-step05-gateway` (including fully-qualified service path), STOP. Errors/partial/unrecognized replies never count as absence. Count/details saved privately; console prints nonsensitive classification.
- **Always** enters `finally` to revoke **only the newly created exact conditional Owner member/role/title/expression** and read the project policy to confirm it is gone. No other binding/role, account or project should be changed. If grant failed/ambiguous, it checks whether the exact conditional binding exists and removes it if safe. If revocation cannot be confirmed, result is `STOP_IAM_REVOCATION_NOT_VERIFIED` and the terminal displays **`C1A_URGENT_MANUAL_IAM_REVOKE=REQUIRED`**.
- Even if immediate revoke fails or process is interrupted, **time condition is designed to expire effective privilege** after 25 minutes; expired IAM policy binding might remain and need manual removal. This is **not** a substitute for checking revocation. If Cloud Shell/browser exits abruptly before the finally block, use the private grant-scope receipt to manually remove **that exact conditional binding**, and verify through project IAM; do not issue a blanket role removal.
- **NO Cloud Run DELETE**, no image/SA/Registry delete, no Firebase/Firestore/KMS/deployment/billing changes, no API enable and no account impersonation. No C1A cleanup can be called complete from this Eventarc listing alone.

## 3. Tests and verified technical references

New offline tests `tests/integration/test_step05_c1a_eventarc_temp_viewer_20261126.py`; **11 synthetic local cases PASS**, including exact short/full-path C1A dependency detection, wrong project/Owner, unknown destinations, new policy matching and no-flag fail-closed. A separate **local fake-Cloud Shell lifecycle simulation** ran full grant/list/revoke with fake CLI, returned `READ_ONLY_PASS_WITH_LIMITS` and verified fake IAM bindings were removed. **These are simulations, NOT Google Cloud actual IAM checks or live role changes.**

Official references, checked 26 Nov:
- Grant and conditional TTL: https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding and https://docs.cloud.google.com/iam/docs/configuring-temporary-access
- Exact condition revoke: https://docs.cloud.google.com/sdk/gcloud/reference/projects/remove-iam-policy-binding
- Eventarc Viewer permissions: https://docs.cloud.google.com/eventarc/standard/docs/access-control
- Eventarc all-location list: https://docs.cloud.google.com/sdk/gcloud/reference/eventarc/triggers/list

## 4. One-paste Owner Google Cloud Shell command — actual NEW IAM writes

Use **Yasmin's already-authenticated Google Cloud Shell**, where the expected project context is `oldx-staging`. Do NOT run in Windows CMD, WSL, other user's account, Codex or CI. This deliberately **changes project IAM**, performs one read, and **reverses the new IAM change**, all subject to guards.

```bash
bash -euo pipefail <<'OLDX_C1A_EVTARC_TEMP'
umask 077
d=$(mktemp -d "$HOME/oldx-c1a-eventarc-temp-source.XXXXXXXX")
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/ev.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/360dd60b6541e2f4cdbbc5583a3f4d75a94b2426/scripts/step05_c1a_eventarc_temporary_viewer_read_revoke_once_20261126.py'
printf '%s  %s\n' '3aa301705aea84a6dbec127984becf405bdf973aaaf9a5eac85e05b8c66f86f5' "$d/ev.py" | sha256sum --check --status
python3 -B "$d/ev.py" --temporary-eventarc-viewer-once
OLDX_C1A_EVTARC_TEMP
```

If download or checksum fails, Python has not run; never bypass integrity checks. **Once the script begins it consumes its unique marker, even on STOP; do not re-run, delete marker or manually repeat an IAM grant.** If `C1A_URGENT_MANUAL_IAM_REVOKE=REQUIRED` or `C1A_EVENTARC_REVOKE` is anything other than `REMOVED_AND_VERIFIED` or `BINDING_NOT_PRESENT_VERIFIED` after an attempted grant, treat access as unresolved and prioritize supervised manual exact-condition revocation. Do not post raw private IAM policies/tokens to GitHub.

Possible positive outcome (NOT claimed ahead of Owner execution):
```text
C1A_EVENTARC_GRANTED=TRUE
C1A_EVENTARC_LIST=NO_C1A_TRIGGER_IN_SUCCESSFUL_ALL_LOCATION_LIST_WITH_LIMITS
C1A_EVENTARC_REVOKE=REMOVED_AND_VERIFIED
C1A_EVENTARC_RESULT=READ_ONLY_PASS_WITH_LIMITS
C1A_CLOUD_RUN_DELETED=NO
```

If no new role can be granted with current Owner effective IAM, the script STOPs. If listing fails after a grant, it still attempts exact revocation. Any successful negative list is a **point-in-time only** Eventarc dependency signal, not proof against every possible dependency. C1A guarded service deletion, async completion, and separate SA/image no-reference checks remain future steps with separately verified live receipts.

**Next owner evidence:** only `C1A_EVENTARC_GRANTED`, `C1A_EVENTARC_LIST`, `C1A_EVENTARC_REVOKE`, `C1A_EVENTARC_TEMP_EXPIRES_UTC`, `C1A_EVENTARC_RESULT`, `C1A_EVENTARC_REASON` screenshot; if revocation uncertain, deal with IAM recovery before anything else. H1B W1–W6, H2 and production are still NO-GO.
