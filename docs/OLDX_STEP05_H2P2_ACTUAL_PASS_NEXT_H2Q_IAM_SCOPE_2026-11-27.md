# OLDX Step05 — H2P2 actual PASS; next H2Q IAM policy boundary

**27 Nov 2026 ~01:01 IST.** Owner's WSL screenshot is the actual result. The three H2 runtime service account emails and distinct immutable UIDs were verified, with H2P1 partial resolved during H2P2:

| Runtime | Exact email | Actual uniqueId |
| --- | --- | --- |
| Mediator | `oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com` | `100779414920484819274` |
| Gateway | `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` | `107238619872767759560` |
| Backend | `oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com` | `106984791114720194680` |

Exact owner output: `PASS_GATEWAY_RECONCILED_AND_ONE_BACKEND_CREATED_VERIFIED`, `GATEWAY_CREATE_REPEATED=FALSE`, `BACKEND_READBACK_VERIFIED=TRUE`, `IAM_GRANTS_KMS_SIGN_RUN_SA_KEYS=NONE`, `H2_PRODUCTION=NO_GO`, `DO_NOT_REPEAT=TRUE`. [Full actual receipt](OLDX_STEP05_H2P1_PARTIAL_H2P2_GATEWAY_RECONCILE_BACKEND_ONLY_NEXT_2026-11-27.md). **All H2P1/H2P2 (and H2O/H2N/H2M) markers are consumed; NEVER rerun these one-shot scripts.**

## Next narrow H2Q preflight — SOURCE/DECISION ONLY, no Cloud execution

Target KMS CryptoKey: `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256`, exact version `/cryptoKeyVersions/1`, pinned DER SPKI SHA256 `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`.

Proposed subsequent **new owner-approved, finite read-only Cloud policy collection**, not covered by prior H2P2 consent:

1. **Resource Manager v3 project getIamPolicy**: `POST https://cloudresourcemanager.googleapis.com/v3/projects/oldx-staging:getIamPolicy` with only `{"options":{"requestedPolicyVersion":3}}`. This POST **reads** a policy; it is NOT `setIamPolicy`.
2. **KMS Key Ring getIamPolicy**: `GET https://cloudkms.googleapis.com/v1/projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing:getIamPolicy?options.requestedPolicyVersion=3`.
3. **KMS CryptoKey getIamPolicy**: `GET https://cloudkms.googleapis.com/v1/projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256:getIamPolicy?options.requestedPolicyVersion=3`.

Require existing isolated Yasmin owner WSL project/session; H2P2 successful local receipt + three exact immutable UIDs; one new exclusive H2Q marker before Cloud calls; no retries on ambiguous response; no redirects; fail-closed on 403, partial/invalid policies or conditional-binding ambiguity. Store original policy/etag privately on WSL and only sanitized direct-role/conditions counts and policy etag hash on GitHub. **Any IAM inherited from org/folder, group membership or deny policies remains UNKNOWN unless separately verified**; direct project/ring/key policy summaries alone are not a full effective-permission test. Do not assume permission absent because a direct binding is absent.

**After the H2Q review (not approved here)** propose only `roles/cloudkms.signer` on that one CryptoKey to `serviceAccount:oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` (UID `107238619872767759560`), using a fresh policy/etag preimage, single scoped change, checked readback and rollback boundary. **No permission for mediator/backend. No wider project/ring grants.** Importantly, per [official Google Cloud KMS roles](https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles), `roles/cloudkms.signer` grants signing only, **not** `viewPublicKey`/Verify; any status/metadata provider required by `scripts/c2-kms-request-signing.mjs` is a separate trust decision. Never swap to broader `signerVerifier` merely to avoid a source dependency.

References: [Project getIamPolicy](https://docs.cloud.google.com/resource-manager/reference/rest/v3/projects/getIamPolicy), [Key Ring getIamPolicy](https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings/getIamPolicy), [CryptoKey getIamPolicy](https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys/getIamPolicy).

**Current authorization:** Source-only planning and GitHub docs permitted. **H2Q Cloud IAM reads are NOT owner-approved or run; H2Q execution script has NOT yet been pushed**. No IAM grant, KMS signing, runtime deployment, product activation or production GO. Step05 ACTIVE, H2/production NO-GO.
