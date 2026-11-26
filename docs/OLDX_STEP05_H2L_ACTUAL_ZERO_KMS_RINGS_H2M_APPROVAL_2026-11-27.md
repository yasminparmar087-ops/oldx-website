# OLDX Step05 H2L — ACTUAL PASS: zero Cloud KMS key rings in asia-south1; H2M exact owner decision

**27 November 2026 ~00:20 IST** actual Owner WSL screenshot. GitHub repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Owner executed NEW source `scripts/step05_h2_kms_post_enable_ring_key_metadata_once_20261127.py` pinned commit `f9ea10cfd8c5fcde89c02ed7d6c704de5f990ce0`, verified blob `e95594640a4b71d8fd9390d6684d77f004d4ef97`. Assistant did not make a direct Cloud API request.

## Actual owner result — DONE / DO NOT REPEAT

```text
OLDX_H2L_RESULT=KMS_POST_ENABLE_METADATA_READ_WITH_LIMITS
OLDX_H2L_REASON=BOUNDED_GET_ONLY_NOT_H2_APPROVAL
OLDX_H2L_RING_LIST=COMPLETE_VISIBLE_PAGE
OLDX_H2L_RING_COUNT=0
OLDX_H2L_RING_NAMES=NONE
OLDX_H2L_KMS_KEY_OR_VERSION_CREATED=FALSE
OLDX_H2L_RESOURCE_WRITES=NONE
OLDX_H2L_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2L_DO_NOT_REPEAT=TRUE
```

**Grounded scope:** In `oldx-staging`, KMS location **`asia-south1` ONLY**, `keyRings.list` succeeded with a complete, unpaginated visible page containing **zero key rings** as the Owner principal. This is not a claim about other locations, projects, pre-existing signing keys elsewhere, permission to create resources, or a fully ready H2 provider. No CryptoKeys/versions created; no key version or public-key pin. Previous H2K API enablement succeeded and remains consumed; never repeat H2R/H2P/H2E/H2F/H2K/H2L; do not reset markers. H1B test SA UID `115445220422157278526` stays disabled/not deleted; earliest separate 24-hour review 27 Nov 22:14:17 IST.

## Confirmed existing source-level requirement

Latest actual repo `scripts/c2-kms-request-signing.mjs` accepts `RSA_SIGN_PKCS1_2048_SHA256` (also RSA 3072/4096 PKCS1 SHA256). Requires exact KMS version path under `projects/oldx-staging/locations/asia-south1/keyRings/.../cryptoKeys/.../cryptoKeyVersions/N`, ENABLED version state, separate trust-bound public DER SPKI SHA256 pin and independent `asymmetricSign` provider. Its verifier uses `RSA-SHA256` with `RSA_PKCS1_PADDING`. Thus **Google Cloud KMS SOFTWARE** RSA 2048 / PKCS1-v1.5 SHA256 is an exact contract-compatible default, rather than a new algorithm architecture. No real KMS signing authorized by this discovery.

## Proposed H2M creation — STILL NEEDS EXPLICIT OWNER APPROVAL

Exact bounded proposed resources:
- Project: `oldx-staging` (number `38472235077`).
- Region: `asia-south1`.
- One NEW key ring: `oldx-c2-h2-signing`.
- One NEW key: `oldx-c2-attestation-rs256`.
- Key purpose: `ASYMMETRIC_SIGN`.
- Version template algorithm: `RSA_SIGN_PKCS1_2048_SHA256`.
- Protection: `SOFTWARE`, not HSM; one initial version, no rotation or subsequent versions automatically configured by this proposal.
- Allow only exact project/region/IDs, one authorized creation attempt for each resource (create ring, read back, create key, read back version) with an irreversible one-shot marker guarding repeat in ambiguous cases.
- Do NOT grant IAM, sign a request, fetch or use private key material, provision Cloud Run/Firestore/Auth/media, enable H2/production or modify billing configuration. A separately approved next phase would verify version/public SPKI pin and signer-only runtime access, without using a browser secret.

**Caution:** Creating the first key version is a real billable resource; Google's Cloud KMS SOFTWARE rate is about `US$0.06/month` for one active key version plus separately billed cryptographic operations (published USD list rate; actual currency/taxes/credits may differ). Key ring and key names are location-bound and cannot simply be renamed or moved. Deletion/destruction can be irreversible; do not create anything without explicit approval. Source: https://cloud.google.com/kms/pricing ; https://docs.cloud.google.com/kms/docs/create-key ; https://docs.cloud.google.com/kms/docs/create-key-ring ; https://docs.cloud.google.com/kms/docs/delete-kms-resources .

**Decision requested:** explicitly authorize only these **two** new Cloud KMS resources and an initial SOFTWARE RSA-signing version in oldx-staging/asia-south1, with readbacks and one-shot no-repeat safeguards. This is NOT included in the previous separate consent to enable only the KMS API. Do not attempt this write until Owner approves.

## Broader project remains

H2 enabled hosted Product seller/buyer flow, distinct mediator/gateway/backend identities, independent approval verifier, durable budget/nonce/TTL, managed moderated media, Auth config 403 diagnosis, new enabled image provenance and rollout/cleanup still NOT COMPLETE. H2 and production remain NO-GO. Previous OFF-only H1B remote image cannot be reused as enabled H2 image.

**Checkpoint:** `H2K_KMS_API=ACTUAL_ENABLED`, `H2L_KEY_RING_LIST=ACTUAL_COMPLETE_ZERO_ASIA_SOUTH1`, `H2M_KEY_CREATION=PROPOSED_NOT_AUTHORIZED`, `STEP05=ACTIVE`, `PRODUCTION=NO_GO`.
