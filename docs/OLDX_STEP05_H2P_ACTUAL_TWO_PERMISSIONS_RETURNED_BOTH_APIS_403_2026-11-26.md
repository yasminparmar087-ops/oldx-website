# OLDX Step05 H2P — actual owner permission hints returned for both denied APIs

**Owner WSL screenshot at 26 November 2026 ~23:14 IST**, current repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Actual operator executed pinned `scripts/step05_h2_two_permission_and_saved_receipt_once_20261126.py` commit `6aba3e75c4493611fea5a51c00fd8c6b5093a7d9`, Git blob `bf11763e14ceb778990616d17e9e0475ea3679c2`. Source file and prior receipt were already verified; no Cloud writes. Assistant has not directly accessed the owner's Google Cloud credentials or Cloud API.

## Exact owner result (verbatim)

```text
OLDX_H2P_RESULT=LOCAL_EVIDENCE_AND_TWO_PERMISSION_HINTS_WITH_LIMITS
OLDX_H2P_REASON=NO_RESOURCE_OR_IAM_CHANGE
OLDX_H2P_AUTH_CONFIG=UNKNOWN_HTTP_403_FROM_PRIOR_RUN
OLDX_H2P_C2_SERVICE_ACCOUNT_COUNT=1
OLDX_H2P_C2_SERVICE_CANDIDATES=NONE
OLDX_H2P_CLOUD_RUN_COUNT=1
OLDX_H2P_CLOUD_RUN_LIST=FIRST_PAGE_COMPLETE
OLDX_H2P_FIRESTORE_DB=METADATA_VISIBLE_EXACT_FROM_PRIOR_RUN
OLDX_H2P_KMS_RING_LIST=UNKNOWN_HTTP_403_FROM_PRIOR_RUN
OLDX_H2P_SERVICE_ACCOUNTS_COUNT=7
OLDX_H2P_SERVICE_ACCOUNTS_LIST=FIRST_PAGE_COMPLETE
OLDX_H2P_STORAGE_BUCKETS_COUNT=0
OLDX_H2P_STORAGE_BUCKETS_LIST=FIRST_PAGE_COMPLETE
OLDX_H2P_PROJECT_PERMISSION_TEST=PROJECT_TEST_200_WITH_LIMITS
OLDX_H2P_KMS_LIST_PERMISSION=RETURNED_AT_PROJECT
OLDX_H2P_AUTH_CONFIG_PERMISSION=RETURNED_AT_PROJECT
OLDX_H2P_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2P_CLOUD_RESOURCE_WRITES=NONE
OLDX_H2P_DO_NOT_REPEAT=TRUE
```

**Meaning and strict limits:** Previously saved H2R metadata had **one regional Cloud Run service**, **zero candidate names matching `oldx-c2`**, **seven project Service Accounts**, **one SA with 'c2' in email**, and **zero Storage buckets** (first-page complete; no pagination in returned scope). These are snapshot counts only, **not** proof no H2 service exists in any other region/project, no media provider exists, or effective runtime IAM. The `(default)` Firestore DB metadata previously returned exact.

One narrowly scoped Cloud Resource Manager **project-level** `testIamPermissions` returned **both** `cloudkms.keyRings.list` and `firebaseauth.configs.get` for the active Owner principal. **DO NOT claim the old 403 resolved**: prior H2R GET to `cloudkms.googleapis.com/v1/projects/oldx-staging/locations/asia-south1/keyRings` and `identitytoolkit.googleapis.com/admin/v2/projects/oldx-staging/config` both returned **HTTP403**. Project-level permission hints do **not** ensure API enablement, effective resource/conditional policy, per-API authorization, or absence of organization restrictions. The original H2R code discarded structured Google error details; reason still **UNDETERMINED**, not simply "permissions missing". No new IAM grant, KMS key, Firebase Auth change, H2 activation, Registry, Cloud Run or production action.

**Never rerun H2P or H2R**, reset markers or replay prior G1/G2B/W0/W1/W3V/W3-W6/W6SA, old build/scan, prior Codex local test groups and older C1A work. H2P marker `/root/.oldx-step05-h2-two-permission-readonly-once-20261126` consumed; previous H2R retained local JSON stays private. H1B trial SA exact UID `115445220422157278526` remains disabled not deleted; earliest separate post-disable review **27 Nov 2026 at 22:14:17 IST**, no automatic deletion.

## One new high-value next diagnostic — no random role grants

The next justified **new** read-only test is two exact **Service Usage `services.get`** calls (NOT repeats of H2R 7-GET inventory or project permission test) to check current project API service state:
- `projects/38472235077/services/cloudkms.googleapis.com`
- `projects/38472235077/services/identitytoolkit.googleapis.com`

These are not KMS key/user/Auth config reads or writes. If `state=DISABLED` (confirmed), proposing an enable operation would require separate explicit owner approval; do not enable automatically. If `state=ENABLED` but previous target GET was 403, next narrow choice is a controlled 403 error-reason capture (sanitized status/reason only, no raw token/project IAM policy/keys/users) to distinguish IAM_PERMISSION_DENIED, SERVICE_DISABLED, API_KEY_SERVICE_BLOCKED, policy/condition or quota/config. A 403/404 in Service Usage must remain UNKNOWN, not interpreted as absence. Do not grant more privileges merely because old request failed. `testIamPermissions` is designed as an introspection hint, not an authoritative call replay. H2/production NO-GO.

**Current:** `H2R=ACTUAL_PASS_WITH_LIMITS_CONSUMED`, `H2P=ACTUAL_PASS_WITH_LIMITS_CONSUMED`, `KMS_403=UNRESOLVED`, `IDENTITY_TOOLKIT_403=UNRESOLVED`, `BOTH_PROJECT_PERMISSIONS=RETURNED_WITH_LIMITS`, `H2_BINDINGS=UNSELECTED`, `APPROVAL_VERIFIER=UNBOUND`, `STEP05=IN_PROGRESS`, `H2/PRODUCTION=NO_GO`.

Official references: https://docs.cloud.google.com/service-usage/docs/reference/rest/v1/services/get ; https://docs.cloud.google.com/iam/docs/testing-permissions ; https://docs.cloud.google.com/identity-platform/docs/reference/rest/v2/projects/getConfig .
