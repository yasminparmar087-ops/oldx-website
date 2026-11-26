# OLDX Step05 H2S — H2R actual PASS, next trusted Gateway synthetic KMS signing

**27 Nov 2026 ~01:16 IST, Owner actual screenshot.** [H2R immutable policy change receipt](OLDX_STEP05_H2Q_ACTUAL_PASS_H2R_ONE_KEY_SIGNER_APPROVAL_2026-11-27.md). Owner executed hash-verified source commit `0b7c1f4dd397046544c47feee01c729d83ca5248`, blob `044d1f1622241efb9865e56cb9bdaa1064ac4848`.

Actual result: `OLDX_H2R_RESULT=PASS_EXACT_ONE_CRYPTOKEY_GATEWAY_SIGNER_BINDING_VERIFIED`, fresh preimage = TRUE, one setIamPolicy POST attempted = TRUE, response/readback verified = TRUE, no other cloud writes/signing/SA keys/Run, H2/production NO-GO, DO_NOT_REPEAT=TRUE.

The one authorized KMS key IAM binding is **exactly** `roles/cloudkms.signer` for `serviceAccount:oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` (UID `107238619872767759560`) on `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256`. No access was granted to website mediator or product backend. H2R marker is consumed. No older H2Q/H2P2/H2P1/H2O/H2N/H2M one-shots should be rerun, markers cleared or keys recreated.

## H2S new SOURCE-ONLY bridge, no live execution

New file: `scripts/c2-h2-gateway-kms-synthetic-transport.mjs`.
- Immutable source commit `2473f62fe1c7e2dbd09fe71eea6ea4a3d19f8dd1`; verified Git blob `ce3deed6ef714d45de7f1d29b63ad830736e960e`.
- **Default OFF, one synthetic call maximum**, with exact KeyVersion `/1`, Gateway account and UID pinned. No ambient Google auth, no JSON SA keys, no Owner WSL OAuth, no impersonation, no automatic retry or redirect. Requires **injected trusted private Gateway runtime credential source** and injected `fetchKms` transport; nothing will execute merely by importing the module.
- Validates the incoming SHA-256 digest/CRC32C, enforces exact request method/endpoint/body, requires metadata-derived trusted Gateway credential source and expiry, checks Google response `verifiedDigestCrc32c`, response name, `SOFTWARE`, signature length/CRC32C. It outputs the normalized REST response to the existing `scripts/c2-kms-request-signing.mjs` which independently verifies RSA-SHA256 with the H2N pinned public SPKI SHA256 `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`.
- Source static scope guard readback PASS. **No Node runtime tests, Google KMS call, host wiring, Cloud Run deploy, signer identity proof, IAM change or Product H2 activation.** No claim of live successful signing.
- `roles/cloudkms.signer` provides `cloudkms.cryptoKeyVersions.useToSign` but **does not grant viewPublicKey**. Existing `createC2KmsRequestSigning` independently requires `getKeyVersionStatus` returning `ENABLED`, algorithm and SPKI SHA256. H2S source does not forge that provider or silently broaden the IAM role. A separately trusted status provider is still a hard gate.

## Critical next live gate — NOT APPROVED YET

The existing Owner WSL OAuth account must **not** sign and claim that the Gateway SA works. Do not create or download a JSON SA private key or assign `roles/iam.serviceAccountTokenCreator` just for a probe. To prove H2R permission genuinely works, a verified, nonpublic, bounded **Cloud Run Gateway runtime actually attached to the Gateway UID** must obtain its access token through Cloud Run metadata, issue **one** synthetic KMS `:asymmetricSign` request with digest CRC32C, verify returned CRC32C and an RSA-SHA256 signature against the pinned public key, store a sanitized receipt, then remain private/default OFF. Before that Cloud gate, separately verify deployed image provenance, region, Cloud Run service identity/Invoker restriction and audience, a short-lived synthetic request/TTL, independently trusted key status, explicit rollback and cleanup; protect all OAuth credentials and raw policies from GitHub. No public route, product publish or production.

Google official refs: [KMS asymmetricSign REST](https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/asymmetricSign), [KMS signer role](https://docs.cloud.google.com/iam/docs/roles-permissions/cloudkms), [integrity guidelines](https://docs.cloud.google.com/kms/docs/data-integrity-guidelines).

**Next work:** source-only integration/review of gateway host, trusted workload credential port, status provider and narrow deployment manifest; then obtain a new finite owner authorization for exact private staging-only Cloud Run runtime/one synthetic sign. **H2S live not approved or executed**, Step05 ACTIVE, H2 and production NO-GO. Older passing local modules and security scans should not be rerun.
