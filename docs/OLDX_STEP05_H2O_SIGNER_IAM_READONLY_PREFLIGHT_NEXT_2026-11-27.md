# OLDX Step05 H2O — next exact identity + KMS CryptoKey IAM metadata gate (SOURCE ONLY)

**27 Nov 2026 IST; BAJUTO public brand, OLDX technical identities.** Canonical H2N result: [actual H2N public SPKI SHA256 PASS](OLDX_STEP05_H2M_PASS_H2N_PUBLIC_PIN_SOURCE_NEXT_2026-11-27.md). H2N fingerprint is \`69a50e43b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba\`, exact KMS CryptoKeyVersion \`/1\`, CRC32C verified. **H2N/H2M/H2L/H2K and all earlier cloud one-shots CONSUMED: NEVER RERUN or clear markers.**

## Trusted runtime binding proposal, NOT an actual Google principal inventory

Source call path \`createC2PrivateGatewayHost\` in \`functions/staging-marketplace/c2-website-mediation.mjs\` is the *only* proposed KMS signing caller. Source \`scripts/c2-kms-request-signing.mjs\` pins RSA_SIGN_PKCS1_2048_SHA256, exact version, public SPKI hash and fails closed without trusted signing provider. Distinct \`mediator\`, \`gateway\`, \`backend\` service identities are required by \`scripts/c2-enabled-release-control.mjs\`. Existing old disabled H1B trial \`oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com\` UID \`115445220422157278526\` is NEVER reused or automatically enabled.

Three **proposed only** user-managed SAs (their existence and UIDs are NOT verified):
- Website mediator: \`oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com\`
- Private gateway and **sole candidate KMS signer**: \`oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com\`
- Product backend: \`oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com\`

The narrowest practical **predefined** KMS role proposal is \`roles/cloudkms.signer\` for \`serviceAccount:oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com\`, on the **one** CryptoKey \`projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256\` ONLY (not project/ring). This role also includes verification/public-key access; it is not a single-permission custom role. It must NEVER be granted to mediator/backend, \`allUsers\`, or old disabled trial SA. There is NO version-level IAM binding; use runtime version \`/1\` + pinned public key and verify version state. Independent approval and IAM preimage/etag review required before later write. References: https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles ; https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys/getIamPolicy .

## H2O read-only preflight source prepared; NOT OWNER APPROVED or executed

Script: \`scripts/step05_h2o_signer_identity_key_iam_metadata_once_20261127.py\`

- **Source commit:** \`d12ab24e0351edfcc75bcbf0b38f207947a9d03f\`
- **Verified Git blob:** \`413f69949f3d8a7611e405b453df6b491136f3c2\`
- Limited to existing Owner's isolated root WSL Google config; validates H2N local PASS receipt, exact key, fingerprint, Google account and project.
- **Exactly 2 NEW HTTPS GETs**, no retries, no redirect: (1) IAM ServiceAccounts LIST at \`https://iam.googleapis.com/v1/projects/oldx-staging/serviceAccounts?pageSize=100&fields=accounts%28email%2CuniqueId%2Cdisabled%29%2CnextPageToken\` selecting only 3 candidate emails from complete page; (2) KMS \`https://cloudkms.googleapis.com/v1/projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256:getIamPolicy\` to examine direct key bindings only. **This is a new identity-specific narrow-field query**, not a re-run of consumed old broad H2R inventory, whose archived summary had counts but no trusted exact new identities/UIDs.
- Key policy may contain other members: no raw IAM memberships/credentials are printed or put in GitHub; local sanitized report includes only identity presence/UID, direct signer membership and other-signer counts; no IAM policy mutation and NO signing.
- Absent in **complete** user-visible list \`NOT_IN_COMPLETE_PROJECT_LIST\`; 403, pagination, stale/partial/invalid response = STOP/UNKNOWN, NOT proof of missing SA. Direct key policy is NOT effective inherited project/ring IAM. No automatic role assignment follows.
- A new exclusive one-shot marker \`/root/.oldx-step05-h2o-signing-identity-and-key-policy-readonly-once-20261127\` is consumed before first GET; never re-run/reset after STOP/timeout.
- This source was statically read back and scope-checked, but **not Python AST/runtime tested against live Google APIs** and is NOT proof of any actual accounts/IAM.

**Owner approval for this new exact read scope is STILL REQUIRED.** Previous H2N permission was only for two KMS version/publicKey GETs; generic \`ok aagal vadho\` authorizes source-only work, not H2O Google calls. No service account creation/disable/enable/delete, IAM grants/role changes, Service Usage, signing, Run, Firebase/Auth, Storage, billing or production is authorized.

### ONE owner WSL paste ONLY AFTER explicit scoped H2O read-only consent

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2o-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2o.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/d12ab24e0351edfcc75bcbf0b38f207947a9d03f/scripts/step05_h2o_signer_identity_key_iam_metadata_once_20261127.py' &&
test "$(git hash-object "$d/h2o.py")" = '413f69949f3d8a7611e405b453df6b491136f3c2' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2o.py" &&
python3 -B "$d/h2o.py" --owner-approved-two-new-h2o-iam-metadata-gets-once
~~~

**Interpretation:** \`OLDX_H2O_RESULT=READ_ONLY_EXACT_SIGNER_IDENTITY_AND_KEY_POLICY_WITH_LIMITS\` is only metadata, NOT effective IAM verification. \`OLDX_H2O_CLOUD_WRITES=NONE\`. Screenshot ONLY sanitized \`OLDX_H2O_*\` lines; no auth tokens or private JSON. Any STOP = do not repeat, preserve marker/receipt. Next decide exact new-only SA creation (if needed), private service identity, key-level least predefined binding after **separate finite owner approval**; actual KMS sign/hosted Product gate stays NO-GO.

\`STEP05=ACTIVE; H2O=SOURCE_READY_UNAPPROVED_UNRUN; H2/PRODUCTION=NO_GO\`.
