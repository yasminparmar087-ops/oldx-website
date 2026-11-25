# OLDX Step 05 C1A — Service Usage enabled list excludes Eventarc API (actual owner screenshot)

**2026-11-26 ~01:23 IST, actual Owner Cloud Shell read-only result.** Branch `security-hardening-review`, repository `yasminparmar087-ops/oldx-website`.

## Exact new result

Owner ran the previously proposed **read-only** Cloud Service Usage list, with exact account `yasminparmar087@gmail.com`, project `oldx-staging` and `gcloud services list --enabled --format='value(config.name)'`, then an exact line match against `eventarc.googleapis.com`. The command's successful branch printed:

```text
EVENTARC_API_STATE=NOT_IN_ENABLED_LIST
```

This establishes **`eventarc.googleapis.com` is absent from the successfully retrieved enabled-services list at that instant**. It is consistent with the previously saved Eventarc trigger-list CLI error `PERMISSION_DENIED: Eventarc API has not been used in project oldx-staging before or it is disabled`. It does **NOT** prove that all historical Eventarc triggers are absent, that no other event transport exists, or that enabling the API now would be safe. No trigger-list response was obtained; Eventarc dependency inventory remains **UNKNOWN**.

The previous **temporary** `roles/eventarc.viewer` project binding granted only to Owner was **REMOVED_AND_VERIFIED** in owner Cloud Shell in the same prior one-shot; this Service Usage command did not modify any IAM/API state. The distinct prior grant/list/revoke marker and all prior C1A delete markers are **CONSUMED**, must not be rerun or removed. **No C1A service, runtime SA, pinned image, shared Artifact Registry or other resource has been deleted.**

## Source and official semantics

Google Service Usage `services.list` with `state:ENABLED` filters enabled APIs: https://docs.cloud.google.com/service-usage/docs/list-services . `gcloud services list --enabled` implements the same category: https://docs.cloud.google.com/sdk/gcloud/reference/services/list . Cloud Run v2 supports `etag` and `validateOnly` for a specific conditional service deletion, but does not automatically delete images or service accounts: https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/delete .

## Next owner decision: do not silently enable an unused API

**Recommended minimum-churn course**: do NOT enable `eventarc.googleapis.com` or regrant Eventarc Viewer solely to facilitate deletion of the historical IAM-private, OFF C1A service, unless the Owner chooses a new explicit, time-bounded API-enable + all-locations trigger-list + permission-revoke/rollback cycle after its operational impact is reviewed. The enabled-services absence is a strong negative operational signal but **not the earlier required complete dependency inventory**. Thus the existing *strict* no-unknown-dependency guard prevents blind deletion; this is a decision gate, not a mandate to run another giant set of old tests.

To close by the 28 Nov 2026 23:19 IST existing C1A retention expiration, available choices:
1. **A — strict verification**: owner explicitly approves one carefully scoped temporary Eventarc API enablement + any necessary **new** Viewer grant and all-locations read (each requires a new IAM/API write); discover and handle any dependencies, then revoke roles, and consider whether disabling API again is safe. Enabling an API can change project behavior and needs a scoped rollback decision. Do not claim safe zero-side-effects.
2. **B — limited evidence risk acceptance**: owner separately and explicitly accepts **unknown historical Eventarc dependency visibility** for exact C1A resource removal, knowing that it might leave a broken trigger or other integrations. The deletion must still be guarded by fresh exact C1A UID/ETag, revision, image, runtime SA, direct IAM, traffic and any other available dependency evidence; no broad cleanup, no owner-read/H1B, no SA/image deletion until independent no-reference verification. This is a deviation from earlier strict policy, **not authorized by previous general “ha manjuri chhe”**.
3. **C — finite retention extension**: if neither is acceptable before deadline, the Owner chooses a new exact end time and cleanup operator; no automatic deletion/extension exists.

No new Cloud API enablement, IAM grant/revoke or service deletion is approved by this screenshot alone. User's current reply provided evidence only, not an affirmative choice to bypass gates.

**Current:** `C1A_SERVICE_USAGE_EVENTARC=NOT_IN_ENABLED_LIST`, `C1A_TRIGGER_INVENTORY=UNKNOWN`, `C1A_TEMP_VIEWER=REMOVED_AND_VERIFIED`, `C1A_SERVICE_DELETED=NO`, `C1A_SA_IMAGE_DELETED=NO`, `H1B_W1-W6/H2/PRODUCTION=NO_GO`.
