# OLDX Step05 H2K — ACTUAL single approved Cloud KMS API enable PASS (owner screenshot)

**27 Nov 2026 ~00:14 IST** owner `OLDX-Ubuntu-24.04` WSL screenshot. Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Source pinned commit `85b9cfd8991c15d719959f6cfcf223c84bec778d`, exact Git blob `3104edcca5fa81943186da72d58be95b8c81e426`, script `scripts/step05_h2_kms_api_enable_one_approved_once_20261127.py`. Owner explicitly approved enabling **only `cloudkms.googleapis.com` on `oldx-staging`**. Screenshot, not assistant direct GCP access, is evidence.

## Actual output (verbatim)

```text
OLDX_H2K_STAGE=ONE_OWNER_APPROVED_KMS_API_ENABLE_ATTEMPT
OLDX_H2K_PROJECT=oldx-staging
OLDX_H2K_SERVICE=cloudkms.googleapis.com
OLDX_H2K_ENABLE_ATTEMPTED=TRUE
OLDX_H2K_RESULT=PASS_KMS_API_ENABLED_EXACT_PROJECT_VERIFIED
OLDX_H2K_REASON=ONE_ENABLE_OPERATION_DONE_AND_KMS_ONLY_READBACK_ENABLED
OLDX_H2K_FINAL_KMS_API_STATE=ENABLED
OLDX_H2K_OTHER_RESOURCES_IAM_KEYS=NOT_CHANGED_BY_SCRIPT
OLDX_H2K_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2K_DO_NOT_REPEAT=TRUE
```

**ACTUAL:** Exactly one Service Usage enable request completed, its operation was polled, and exact project/KMS service state read back as `ENABLED` in `oldx-staging`, project number `38472235077`. New H2K marker `/root/.oldx-step05-h2-kms-api-enable-owner-once-20261127` **CONSUMED**, do not delete/reset/re-execute. `identitytoolkit.googleapis.com` was already ENABLED in the separate H2F actual prior read, but the unresolved Firebase Auth config GET HTTP403 was NOT retested here. This step does not create any key ring, CryptoKey, version, IAM role/policy, Cloud Run service or Firebase resources. It does not approve H2 or production.

**All previous H2R/H2P/H2E/H2F/H2K and H1B one-shots consumed**. Never replay builds, scans, Registry push, disabled SA cleanup or existing host probes for this. Separate H1B trial SA UID `115445220422157278526` remains disabled, not deleted; earliest ≥24h dependency review is **27 Nov 2026 22:14:17 IST**, not automatic deletion.

## Fastest genuinely new next action: narrow KMS metadata inventory AFTER service activation

Now KMS API is ENABLED, one **new** project-and-region-scoped **read-only KMS keyRings.list** at `projects/oldx-staging/locations/asia-south1` is warranted because previous listing was attempted while API DISABLED and returned 403. If any key rings exist, check at most three exact ring `cryptoKeys.list` metadata collections to learn whether any `ASYMMETRIC_SIGN` key exists. GET-only; never use `asymmetricSign` or create key/version; no KMS private bytes or IAM grants. Paginated/403 responses must be UNKNOWN/PARTIAL, NOT absence. If zero rings visible from a verified complete list, a new dedicated key ring/key would need separate owner approval and provenance controls. If KMS metadata still 403, inspect a narrowly sanitized Google error reason before granting roles. Authentication API config 403 remains a separate issue; do not repeat that GET casually.

Official docs: https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings/list ; https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys/list . The eventual signer must use purpose `ASYMMETRIC_SIGN` with appropriate algorithm, version and independently pinned public key, not a random existing key.

**State:** `H2K=ACTUAL_PASS_CLOUD_KMS_API_ENABLED`, `H2_ENABLED=NOT_ATTEMPTED`, `KMS_KEYRINGS_AND_SIGNING_KEYS=NOT_INVENTORIED_POST_ENABLE`, `AUTH_CONFIG_403=UNRESOLVED`, `STEP05=ACTIVE`, `PRODUCTION=NO_GO`.
