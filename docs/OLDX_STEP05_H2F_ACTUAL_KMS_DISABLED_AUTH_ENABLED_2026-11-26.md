# OLDX Step05 H2F — actual API state results: Cloud KMS disabled, Identity Toolkit enabled

**26 November 2026 ~23:24 IST, owner Ubuntu WSL screenshot**. Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Source was the pinned `scripts/step05_h2_exact_two_api_states_fields_recovery_once_20261126.py` commit `f228b02cfbbbe4dab8d67cd5398615ca2e56408d`, Git blob `362ffb697ab316e7ed3152cb613c3db5e35e8b6c`. This result is owner's actual terminal output (not independent live GCP calls by assistant).

## ACTUAL owner stdout

```text
OLDX_H2F_RESULT=EXACT_TWO_API_STATES_FIELDS_ONLY_WITH_LIMITS
OLDX_H2F_REASON=PARTIAL_RESPONSE_METADATA_ONLY
OLDX_H2F_KMS_API=API_DISABLED
OLDX_H2F_AUTH_API=API_ENABLED
OLDX_H2F_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2F_CLOUD_RESOURCE_WRITES=NONE
OLDX_H2F_NO_IAM_KMS_AUTH_CHANGES=TRUE
OLDX_H2F_DO_NOT_REPEAT=TRUE
```

The new **two-field-filtered Google Service Usage GETs succeeded**. For `oldx-staging` project number `38472235077`, `cloudkms.googleapis.com` reported exactly **DISABLED** and `identitytoolkit.googleapis.com` reported exactly **ENABLED** on this snapshot. H2F script verified exact returned project number/service resource identity. No API enablement or any Google Cloud write. H2F one-shot marker `/root/.oldx-step05-h2-exact-two-states-fields-only-once-20261126` CONSUMED; NEVER rerun or clear. Prior H2E consumed-stop, H2P, H2R and every earlier G1/G2B/W0/W1/W3V/W3–W6/W6SA/H1A/old C1A source/resource checks remain consumed: **DO NOT REPEAT**. This is neither confirmation of any KMS key existence nor evidence of a cryptographic signing version or H2 readiness.

**Implication for H2 G2 signing:** enabling Cloud KMS API is a genuine Google Cloud project write prerequisite if this project will use Cloud KMS managed signing. It does not automatically create a key ring, key, version, IAM binding, service account, or hosted service. The existing 403 to KMS metadata while API was disabled is consistent with disabled service (not proof that disabling was the only factor). Before an API enable write, obtain a separate precise owner authorization limited to `cloudkms.googleapis.com` on **`oldx-staging` only**. Google documentation: https://docs.cloud.google.com/service-usage/docs/enable-disable and https://docs.cloud.google.com/kms/docs/create-key . Permission `serviceusage.services.enable` is required. When owner approves, use an isolated single-API enable command with `--project=oldx-staging` and narrowly verify only the resulting service state; no IAM/KMS key creation, no service/deploy/registry writes. **Do not enable without that explicit approval.**

**Auth interpretation:** `identitytoolkit.googleapis.com` is already ENABLED; do NOT enable it again or grant extra IAM roles simply because prior `GET /admin/v2/projects/oldx-staging/config` produced HTTP403. Previous H2P project-level `firebaseauth.configs.get` permission returned as present, so investigate exact Auth 403 service/policy/error reason via a separate future **sanitized read-only diagnostic only if necessary**, not full token/raw response logging. No claims Auth provider works end-to-end until actual synthetic sign-in is separately approved/tested.

**Existing metadata snapshot** (previous saved H2P, no new listing): `asia-south1` Cloud Run count 1, no C2 service candidates, project service accounts 7 (one C2-named), Storage buckets 0, `(default)` Firestore DB metadata visible. Counts not all-regions inventory, do not treat absence of project Storage buckets as inability to choose a managed media provider without a later decision. No three distinct H2 runtime SA identities, approved managed photo provider, independent signed owner approval verifier, atomic durable nonce/budget, enabled immutable image security/provenance/rollback is yet established. Full Step05 active, enabled hosted seller/buyer Product thin slice not verified; H2/production **NO-GO**.

**H1B old separate lifecycle:** exact test SA `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, immutable UID `115445220422157278526`, **DISABLED NOT DELETED** since 2026-11-26 22:14:17 IST. Earliest after >=24h separate dependency review 2026-11-27 22:14:17 IST; no automatic deletion, not part of this H2F gate.

**CURRENT STATUS:** `H2F=OWNER_ACTUAL_PASS_KMS_DISABLED_AUTH_ENABLED_CONSUMED`; `H2_KMS_ENABLE=NOT_APPROVED_OR_ATTEMPTED_IN_THIS_STEP`; `AUTH_CONFIG_403=UNRESOLVED`; `H2_ENABLED=NO_GO`; `PRODUCTION=NO_GO`.
