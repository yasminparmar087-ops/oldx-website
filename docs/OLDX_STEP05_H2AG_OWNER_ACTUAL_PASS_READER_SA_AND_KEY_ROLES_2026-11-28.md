# BAJUTO / OLDX Step05 — H2AG OWNER ACTUAL PASS (28 November 2026 IST)

## Real operator evidence (WSL root screenshot)

The Owner executed the previously consented **ONE-SHOT H2AG** runner from immutable Git commit `4cce529f8319eb415f9b3e4eeb378a70423b6774`, path `scripts/step05_h2ag_exact_reader_sa_two_key_roles_once_20261128.py`, verified Git blob `9ea97a0d0638962813a5d03b2942eac752a8cbf4` using `git hash-object` and Python AST before running. Local command was run from WSL root (Windows CMD `wsl -u root`).

**Exact observed sanitized output from user screenshot**:

```text
H2AG_MARKER=CONSUMED_NO_REPEAT
H2AG_READER_CREATED_UID=107336955065718475994
H2AG_READER_SA_UID_ENABLED=VERIFIED
H2AG_READER_READ_ONLY_KEY_ROLES_POST=VERIFIED
H2AG_READER_SA=107336955065718475994
H2AG_SA_CREATE_ATTEMPTED=TRUE
H2AG_ONE_KEY_IAM_WRITE_ATTEMPTED=TRUE
H2AG_KEY_READER_ROLES_READBACK=VERIFIED
H2AG_EXISTING_GATEWAY_SIGNER=PRESERVED_VERIFIED
H2AG_OLD_H2R_H2AF_MARKERS=UNTOUCHED
H2AG_OTHER_IAM_KMS_SIGN_FIRESTORE_RUN_WRITES=NONE
H2AG_H2_PRODUCTION=NO_GO
H2AG_DO_NOT_REPEAT=TRUE
H2AG_RESULT=ONE_READER_SA_TWO_KEY_READ_ONLY_ROLES_PASS
H2AG_REASON=UID_AND_EXACT_ETAG_POLICY_READBACK_VERIFIED
```

**Conclusion**: Actual H2AG Cloud execution PASS with UID-verified newly created reader service account `oldx-c2-kms-reader@oldx-staging.iam.gserviceaccount.com` numeric UID **`107336955065718475994`** in project `oldx-staging`. On the **single existing** `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256`, the new Reader got `roles/cloudkms.viewer` and `roles/cloudkms.publicKeyViewer`; original Gateway-only `roles/cloudkms.signer` preserved, exact role policy readback and new ETag verified by the one-shot runner. No Reader JSON keys, no KMS signature, no other IAM/project/ring changes, no Product data writes or deployment by the script.

**DO NOT REPEAT** H2AG, do not reset `/root/.oldx-step05-h2ag-one-reader-sa-two-key-only-roles-once-20261128` or delete/create the reader account, and do not rerun prior H2R, H2AF, H2AD tests. H2AG's actual Cloud write is already done, so the previous prospective decision document is historical and must no longer be treated as pending.

## What this PASS is NOT

- Does **not** independently prove reader workload identity is attached to a **running Cloud Run revision**, or that it can access KMS through its own metadata token; no hosted reader service was deployed and no real version GET/publicKey GET was performed by this execution.
- Does **not** prove current KeyVersion `ENABLED`, pinned live PEM/SPKI, signed independent operator multi-sign approval, native Firebase/Firestore/Storage runtime, three new immutable enabled host image digests or real service-to-service private networking. Historical H2AD9 `NOT_FOUND` hosted health remains unproven.
- Does **not** authorize H2 enablement, new image build/push, live KMS signing or staging Product writes. Step05 ACTIVE, production OFF/NO-GO.

## Highest-impact next action — no more reader IAM probes

Move directly to **ONE consolidated Codex image/runtime preparation** for three distinct default-OFF, future-enabled mediator/Gateway/backend private-staging host images, with exact reader account pinned to `oldx-c2-kms-reader@oldx-staging.iam.gserviceaccount.com` / UID `107336955065718475994`. Reuse existing factories, new lifecycle six-phase source and 18 tested cases; **do not rerun previous tests**. Prepare deployment-ready but not deployed entrypoints, frozen Dockerfiles/COPY manifests/Cloud Run host-to-host identity/audience and private-network specifications, real read-only reader-host metadata provenance path, native Firebase/media/Firestore adapter injection, deterministic source→OCI digest evidence plan, rollback/cleanup and one bounded 6-sign/24-read/20-request test. Do not invent new image digests; build/push/deploy require a separate exact scope owner decision.

For source guidance see:
- `docs/OLDX_STEP05_BOUNDED_LIFECYCLE_SOURCE_INTEGRATION_RECEIPT_2026-11-28.md`
- `docs/OLDX_STEP05_PRIVATE_STAGING_SINGLE_ACCEPTANCE_PACKET_2026-11-28.md`
- `docs/OLDX_STEP05_H2AG_OWNER_APPROVED_EXACT_READER_SA_KEY_ROLES_RUNNER_2026-11-28.md` (historical approval/one-shot)
- `functions/staging-marketplace/c2-future-role-hosts.mjs`
- `scripts/c2-h2-independent-kms-reader-ports.mjs`.

**Actual checkpoint**: `H2AG=OWNER_ACTUAL_CLOUD_PASS`; `READER_UID=107336955065718475994`; `H2AG_MARKER=CONSUMED_DO_NOT_REPEAT`; `SOURCE_LOCAL_18_NEW_TESTS=PASS_AS_PRIOR_RECEIPT`; `HOSTED_SELLER_BUYER=NOT_VERIFIED`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
