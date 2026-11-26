# OLDX Step05 — H2 provider metadata-only readiness: ACTUAL owner WSL result, 26 November 2026 ~23:07 IST

Source: owner screenshot from `OLDX-Ubuntu-24.04` WSL root, following pinned `scripts/step05_h2_provider_readonly_inventory_once_20261126.py` commit `a97d83e57824f168bc2e2c978cc545aeb885d68b`, verified blob `490095ca85821b22b5f2f4b4270b41986a08eb81`. Assistant did NOT execute Cloud API calls. Branch: `security-hardening-review`.

## Exact actual screenshot (verbatim)

```text
OLDX_H2R_RESULT=READ_ONLY_METADATA_WITH_LIMITS
OLDX_H2R_REASON=STATIC_INVENTORY_NOT_H2_AUTHORITY
OLDX_H2R_PROJECT=ACTIVE_IDENTITY_MATCH
OLDX_H2R_CLOUD_RUN=FIRST_PAGE_COMPLETE
OLDX_H2R_SERVICE_ACCOUNTS=FIRST_PAGE_COMPLETE
OLDX_H2R_KMS_KEY_RINGS=UNKNOWN_HTTP_403
OLDX_H2R_KMS_SIGNING_KEYS=NOT_ESTABLISHED
OLDX_H2R_FIRESTORE_DEFAULT_DB=METADATA_VISIBLE_EXACT
OLDX_H2R_AUTH_CONFIG=UNKNOWN_HTTP_403
OLDX_H2R_STORAGE_BUCKETS=FIRST_PAGE_COMPLETE
OLDX_H2R_H2_BINDINGS=NOT_SELECTED_OR_INDEPENDENTLY_VERIFIED
OLDX_H2R_APPROVAL_VERIFIER=NOT_BOUND_OR_INDEPENDENTLY_VERIFIED
OLDX_H2R_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2R_SA_KMS_DB_STORAGE_WRITES=NONE
OLDX_H2R_NO_SIGNING_OR_PRIVATE_KEY_BYTES_REQUESTED=TRUE
OLDX_H2R_DO_NOT_REPEAT=TRUE
```

**Verified limited meaning**: project identity `oldx-staging` ACTIVE, regional `asia-south1` Cloud Run services and project IAM Service Accounts first pages complete without pagination; exact `(default)` Firestore DB metadata accessible, project Storage bucket first page complete. The printed console view does **not display counts, candidate service names, SA c2 count or bucket count**; only the script's *already written, private sanitized* local JSON evidence has those details. Avoid new Cloud list calls just to rediscover them.

**403 is UNKNOWN, not absence:** KMS `keyRings.list` and Identity Toolkit `projects.getConfig` returned HTTP403. This does not establish no KMS ring/key, no signing version, disabled Firebase Email/Password, or failed existing website login. A denial may involve IAM, org policies, API service enablement, or provider restrictions; only an exact new scoped permission diagnosis can narrow this. The prior UI screenshot showing Auth Email/Password enabled is historical evidence, NOT this principal's API-access proof. No KMS crypto key/version/public key/creator role/approval verifier/verified new enabled image is selected.

**Do not repeat:** one-shot marker `/root/.oldx-step05-h2-provider-readonly-inventory-once-20261126` consumed; never rerun, clear or replay the read-only inventory. Also do not redo H1A build/security scan, G1/G2A/G2B/W0/W1/W3V/W3–W6/W6SA, Origin1/0, earlier Codex 11 focused tests, or C1A residual operations.

## Precise next fast path — NO cloud writes and no repeat listings

1. Read only the **existing local sanitized evidence JSON** using the `EVIDENCE=` field in the exact one-shot marker and print only the bounded service candidate names/counts, SA c2 count, and bucket count. Never upload OAuth tokens or unredacted IAM listings.
2. For KMS 403, official Google Cloud KMS list permissions include `cloudkms.keyRings.list` (Viewer `roles/cloudkms.viewer`). For Firebase Auth `getConfig`, official permission is `firebaseauth.configs.get` (Viewer `roles/firebaseauth.viewer` or other appropriately scoped roles). Do NOT blindly grant roles; first confirm effective owner/project context, identify exact required read-only access and request separate scoped IAM approval for a write.
3. An optional **one NEW narrowly targeted** IAM testIamPermissions on the project for those two permissions can supplement diagnosis but is NOT a repeat of G1 (old G1 checked other project/Registry permissions). A project-level answer is only a hint, not a proof of key-level or service-level access; do not infer nonexistent keys from missing permission or 403. Do not check keys by signing and do not create any keys/SA or modify Firebase.
4. Select exact three distinct runtime principals, enabled images and KMS ASYMMETRIC_SIGN version only after verified provider existence and independent approval; no H2 enablement now.

**Current status**: `H2_READONLY_METADATA=ACTUAL_PASS_WITH_LIMITS_CONSUMED`; `KMS_RING=UNKNOWN_403`; `FIREBASE_AUTH_CONFIG=UNKNOWN_403`; `CLOUD_RUN/SA/DB/BUCKET=METADATA_READABLE`; `H2_BINDINGS=NOT_SELECTED`; `APPROVAL_VERIFIER=NOT_BOUND`; `H2/PRODUCTION=NO_GO`. Previous H1B test SA UID `115445220422157278526` remains **disabled, not deleted**, earliest dependency review Nov 27 22:14:17 IST. Existing H1B OFF image not enabled and cannot be used as H2 enabled image.

Sources: https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles ; https://docs.cloud.google.com/identity-platform/docs/reference/rest/v2/projects/getConfig ; https://docs.cloud.google.com/iam/docs/roles-permissions/firebaseauth .
