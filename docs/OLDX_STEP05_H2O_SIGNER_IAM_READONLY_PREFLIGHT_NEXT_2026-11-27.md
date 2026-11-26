# OLDX Step05 H2O — next exact identity + KMS CryptoKey IAM metadata gate (SOURCE ONLY)

**27 Nov 2026 IST; BAJUTO public brand, OLDX technical identities.** Canonical H2N result: [actual H2N public SPKI SHA256 PASS](OLDX_STEP05_H2M_PASS_H2N_PUBLIC_PIN_SOURCE_NEXT_2026-11-27.md). H2N fingerprint is `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`, exact KMS CryptoKeyVersion `/1`, CRC32C verified. **H2N/H2M/H2L/H2K and all earlier cloud one-shots CONSUMED: NEVER RERUN or clear markers.**

## Trusted runtime binding proposal, NOT an actual Google principal inventory

Source call path `createC2PrivateGatewayHost` in `functions/staging-marketplace/c2-website-mediation.mjs` is the *only* proposed KMS signing caller. Source `scripts/c2-kms-request-signing.mjs` pins RSA_SIGN_PKCS1_2048_SHA256, exact version, public SPKI hash and fails closed without trusted signing provider. Distinct `mediator`, `gateway`, `backend` service identities are required by `scripts/c2-enabled-release-control.mjs`. Existing old disabled H1B trial `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` UID `115445220422157278526` is NEVER reused or automatically enabled.

Three **proposed only** user-managed SAs (their existence and UIDs are NOT verified):
- Website mediator: `oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com`
- Private gateway and **sole candidate KMS signer**: `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`
- Product backend: `oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com`

The narrowest practical **predefined** KMS role proposal is `roles/cloudkms.signer` for `serviceAccount:oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`, on the **one** CryptoKey `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256` ONLY (not project/ring). **Corrected per current Google Cloud KMS role reference (27 Nov 2026): `roles/cloudkms.signer` grants signing, NOT `viewPublicKey` / verification.** It is a predefined role with other basic location/project metadata permissions, not a single-permission custom role. Do NOT substitute `roles/cloudkms.signerVerifier` without separate documented necessity and consent. It must NEVER be granted to mediator/backend, `allUsers`, or old disabled trial SA. There is NO version-level IAM binding; use runtime version `/1` + pinned public key and verify version state. Independent approval and IAM preimage/etag review required before later write. References: https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles ; https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys/getIamPolicy .

## H2O read-only preflight source prepared; NOT OWNER APPROVED or executed

Script: `scripts/step05_h2o_signer_identity_key_iam_metadata_once_20261127.py`

- **Source commit:** `c01660085584177e6fcea648584897f0eea2a4ef`
- **Verified Git blob:** `1f325738a5478490a14496ef6702ac1e10f5fa2d`
- Limited to existing Owner's isolated root WSL Google config; validates H2N local PASS receipt, exact key, fingerprint, Google account and project.
- **Exactly 2 NEW HTTPS GETs**, no retries, no redirect: (1) IAM ServiceAccounts LIST at `https://iam.googleapis.com/v1/projects/oldx-staging/serviceAccounts?pageSize=100&fields=accounts%28email%2CuniqueId%2Cdisabled%29%2CnextPageToken` selecting only 3 candidate emails from complete page; (2) KMS `https://cloudkms.googleapis.com/v1/projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256:getIamPolicy` to examine direct key bindings only. **This is a new identity-specific narrow-field query**, not a re-run of consumed old broad H2R inventory, whose archived summary had counts but no trusted exact new identities/UIDs.
- Key policy may contain other members: no raw IAM memberships/credentials are printed or put in GitHub; local sanitized report includes only identity presence/UID, direct signer membership and other-signer counts; no IAM policy mutation and NO signing.
- Absent in **complete** user-visible list `NOT_IN_COMPLETE_PROJECT_LIST`; 403, pagination, stale/partial/invalid response = STOP/UNKNOWN, NOT proof of missing SA. Direct key policy is NOT effective inherited project/ring IAM. No automatic role assignment follows.
- A new exclusive one-shot marker `/root/.oldx-step05-h2o-signing-identity-and-key-policy-readonly-once-20261127` is consumed before first GET; never re-run/reset after STOP/timeout.
- This source was statically read back and scope-checked, but **not Python AST/runtime tested against live Google APIs** and is NOT proof of any actual accounts/IAM.

**Owner explicit H2O approval RECEIVED on 27 Nov 2026:** the Owner replied `ha manjuri chhe` to exactly TWO new read-only GET requests: the bounded `oldx-staging` IAM Service Accounts metadata list and the direct IAM policy read for the single named KMS CryptoKey, plus sanitized local analysis. This is distinct from previously consumed H2N. **Approval received is NOT live execution:** Google API requests are NOT yet attempted. No service-account create/enable/disable, IAM grant, signing, deploy or production operations are within this approval. No service account creation/disable/enable/delete, IAM grants/role changes, Service Usage, signing, Run, Firebase/Auth, Storage, billing or production is authorized.

### ONE owner WSL paste — H2O read-only scope now explicitly approved

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2o-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2o.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/c01660085584177e6fcea648584897f0eea2a4ef/scripts/step05_h2o_signer_identity_key_iam_metadata_once_20261127.py' &&
test "$(git hash-object "$d/h2o.py")" = '1f325738a5478490a14496ef6702ac1e10f5fa2d' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2o.py" &&
python3 -B "$d/h2o.py" --owner-approved-two-new-h2o-iam-metadata-gets-once
~~~

**Interpretation:** `OLDX_H2O_RESULT=READ_ONLY_EXACT_SIGNER_IDENTITY_AND_KEY_POLICY_WITH_LIMITS` is only metadata, NOT effective IAM verification. `OLDX_H2O_CLOUD_WRITES=NONE`. Screenshot ONLY sanitized `OLDX_H2O_*` lines; no auth tokens or private JSON. Any STOP = do not repeat, preserve marker/receipt. Next decide exact new-only SA creation (if needed), private service identity, key-level least predefined binding after **separate finite owner approval**; actual KMS sign/hosted Product gate stays NO-GO.

`STEP05=ACTIVE; H2O=OWNER_APPROVED_SOURCE_READY_NOT_EXECUTED; H2/PRODUCTION=NO_GO`.

## 27 Nov 2026 ~00:44 IST — H2O pre-request STOP and exact-source correction

Owner WSL screenshot after the originally pinned source `d12ab24e0...` returned `OLDX_H2O_RESULT=STOP_BEFORE_REQUEST`, `REASON=H2N_PIN_MISMATCH`, `CLOUD_WRITES=NONE`. The preflight rejected the incorrectly transcribed H2N fingerprint before obtaining OAuth, before the H2O one-shot marker, and before any H2O Cloud GET. **No H2O API reads or IAM writes happened in that attempt.** H2N/H2M PASS and markers remain intact.

Directly reexamined original H2N screenshot: correct first 8 digits `69a50043`, not the earlier assistant's `69a50e43` transcription. Remaining digits unchanged. Correct full SPKI hash `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`. H2N's locally generated fingerprint/receipt was correct; the error was in the assistant's GitHub H2N note and subsequently hard-coded H2O check. The original H2O source never made a Cloud request and its H2O marker was not created on this STOP path.

**Recovery (source-only):** corrected only H2O constant to exact screenshot hash; no trust/IAM/URL/logic relaxation. New source immutable commit `c01660085584177e6fcea648584897f0eea2a4ef`, blob `1f325738a5478490a14496ef6702ac1e10f5fa2d`. Pinned command above now points to corrected script. Owner's prior two-GET approval has NOT been consumed (no GET attempted) and applies to this unchanged exact read-only scope; use single corrected script once after hash verification. If next STOP is after marker/GET, never retry or delete marker.

## 27 Nov 2026 ~00:49 IST — OWNER ACTUAL H2O READ-ONLY SUCCESS (LATEST)

Owner supplied WSL terminal screenshot after exact corrected H2O commit `c01660085584177e6fcea648584897f0eea2a4ef` SHA-matched and Python AST check; the previously documented STOP-before-request was separately preserved, not repeated. Actual sanitized H2O output:

~~~text
OLDX_H2O_RESULT=READ_ONLY_EXACT_SIGNER_IDENTITY_AND_KEY_POLICY_WITH_LIMITS
OLDX_H2O_REASON=DIRECT_ACCOUNT_LIST_AND_KEY_POLICY_NOT_EFFECTIVE_IAM
OLDX_H2O_ACCOUNT_LIST_SCOPE=COMPLETE_VISIBLE_PAGE
OLDX_H2O_MEDIATOR=NOT_IN_COMPLETE_PROJECT_LIST
OLDX_H2O_GATEWAY=NOT_IN_COMPLETE_PROJECT_LIST
OLDX_H2O_BACKEND=NOT_IN_COMPLETE_PROJECT_LIST
OLDX_H2O_KEY_POLICY_SCOPE=EXACT_CRYPTOKEY_DIRECT_POLICY_ONLY
OLDX_H2O_GATEWAY_DIRECT_SIGNER=FALSE
OLDX_H2O_INHERITED_IAM=NOT_CHECKED
OLDX_H2O_IAM_GRANT=NOT_ATTEMPTED
OLDX_H2O_CLOUD_WRITES=NONE
OLDX_H2O_H2_PRODUCTION=NO_GO
OLDX_H2O_DO_NOT_REPEAT=TRUE
~~~

**Actual evidence conclusion:** all three newly proposed service-account emails are absent in the complete visible first page of the exact **oldx-staging** project account list. This is not absence globally or in other projects. The KMS CryptoKey direct policy has no direct binding for the proposed Gateway signer; inherited project/folder/organization IAM is **not checked**, so effective signer permission remains unknown. No role changes, SA creation, KMS signing, host activation or production writes were attempted. The H2O one-shot marker is now consumed: /root/.oldx-step05-h2o-signing-identity-and-key-policy-readonly-once-20261127. Never rerun/reset H2O, or previous H2N/H2M/H2L/H2K etc.

**Next:** prepare a separately authorized, exact three-account creation-only H2P1, requiring prior H2O actual local saved evidence and fresh exact-name absence checks. Do **not** bind KMS signing or create keys during this new stage; that is a distinct future scoped decision. No IAM write approval has been granted yet. Step05 IN_PROGRESS, H2/PRODUCTION NO-GO.
