# OLDX Step 05 C1A — Eventarc all-locations error classified from saved evidence

**26 November 2026 IST, actual user screenshots, only offline saved evidence inspected.** Repository `yasminparmar087-ops/oldx-website` branch `security-hardening-review`. Previous handoff: [saved CLI error diagnostics](OLDX_STEP05_C1A_EVENTARC_TEMP_GRANT_REVOKED_LIST_FAILED_OFFLINE_DIAG_2026-11-26.md).

## Grounded screenshot result

After correcting the `EVENTARC-ALL-LOCATIONS_NONZERO` literal hyphen/underscore mismatch, the Owner Cloud Shell **offline** read of the previously saved private `eventarc-all-locations.stderr` and `.exit` successfully yielded:

```text
C1A_EVENTARC_EXIT=1
C1A_EVENTARC_ERROR_CLASS=PERMISSION_DENIED
C1A_ERROR_DETAIL=ERROR: (gcloud.eventarc.triggers.list) PERMISSION_DENIED: Eventarc API has not been used in project oldx-staging before or it is disabled. Enable it by visiting [URI] then retry. If you enabled this API recently, wait a ...
IAM_REVOKE=PREVIOUSLY_VERIFIED
OFFLINE_ONLY=TRUE
```

**Correct interpretation:** the actual underlying Eventarc all-location CLI error is **SERVICE/API AVAILABILITY**, not simply proof that the Viewer IAM role was too weak. Google says the Eventarc API **has not been used OR is disabled**; that is an ambiguous error and **not standalone proof of exact Service Usage enabled state**. It also does **not** prove Eventarc triggers absent, or that any trigger exists. Earlier one-shot project-only temporary `roles/eventarc.viewer` was actually added and then explicitly **REMOVED_AND_VERIFIED** after the failed list; it is not active as a result of that one-shot. The read-only marker parse had initially failed on `REASON=EVENTARC-ALL-LOCATIONS_NONZERO` (hyphens from script's `name.upper()`); that local mismatch is now resolved without changing marker.

No new Cloud API call or IAM mutation was performed in this latest offline diagnostic. The prior grant/list/revoke marker, both C1A deletion no-write STOP markers, source/field diagnostics, S3/S3B and other completed work remain CONSUMED. Do not repeat/reset any of those actions. The user has approved guarded C1A-only cleanup, and a *past* single temporary Eventarc Viewer grant/list/revoke, **not** API enablement or an additional IAM grant. C1A service, runtime SA and immutable Registry image remain NOT DELETED.

## New necessary, limited one-time read-only gate

Check only whether `eventarc.googleapis.com` is currently enabled for **`oldx-staging`** through Service Usage, **without enabling/disabling the API**, switching account, granting IAM, or rerunning Eventarc triggers. Google's official `gcloud services list --enabled` lists enabled APIs: https://docs.cloud.google.com/sdk/gcloud/reference/services/list and https://docs.cloud.google.com/service-usage/docs/list-services .

Suggested one command for Owner Google Cloud Shell (the only new Google API read in next action):

```bash
gcloud --quiet --account=yasminparmar087@gmail.com --project=oldx-staging services list --enabled --format='value(config.name)' | grep -Fx 'eventarc.googleapis.com' || true
```

**Caution**: an empty pipeline by itself is ambiguous (permission or CLI failure vs disabled). Instead run the guarded variant below and only classify `ENABLED` after a successful `gcloud services list` exit, otherwise report STOP:

```bash
bash -euo pipefail <<'OLDX_EVENTARC_SERVICE_STATE'
o="$(mktemp)"
if gcloud --quiet --account=yasminparmar087@gmail.com --project=oldx-staging services list --enabled --format='value(config.name)' > "$o"; then
  if grep -Fxq 'eventarc.googleapis.com' "$o"; then
    echo EVENTARC_API_STATE=ENABLED
  else
    echo EVENTARC_API_STATE=NOT_IN_ENABLED_LIST
  fi
else
  echo EVENTARC_API_STATE=STOP_UNVERIFIED
fi
rm -f "$o"
OLDX_EVENTARC_SERVICE_STATE
```

This **does not** enable Eventarc, create Eventarc triggers, grant/revoke IAM, or delete Cloud Run. Note `NOT_IN_ENABLED_LIST` is evidence only of not appearing in the successful enabled-services list at that time; this alone does not assert whether the API was never used or previously disabled, nor rule out every past dependency.

## Decision after state read

If `NOT_IN_ENABLED_LIST`: the recent Eventarc list error is consistent with disabled/not-yet-enabled API. **DO NOT** automatically turn it on or infer there are zero triggers. Decide separately whether a one-time supervised API enablement + fresh authorized all-locations list + disable/rollback is warranted, considering potential effects of disabling and the risk that enabling may activate existing integrations. That is a *new* project configuration change needing express owner consent, plus renewed temporary Viewer consent and verified revocation. Alternatives include an owner-approved change in cleanup risk acceptance with documented dependency limitations; no silent guard bypass.

If `ENABLED`: the error may be propagation/other issue; first inspect exact API status/permissions from a new scoped read, not the consumed trigger-list command. If `STOP_UNVERIFIED`, do not proceed to deletion or mutate API/IAM. Original C1A retention approval expires **28 Nov 2026 23:19 IST**, no automatic shutdown or extension. H1B W1–W6, H2, production remain NO-GO.
