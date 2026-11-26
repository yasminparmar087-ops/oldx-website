# OLDX Step05 — H2Q actual PASS; H2R single-key Gateway signing role proposal

**27 Nov 2026 ~01:08 IST; latest H2Q Owner screenshot.** BAJUTO public brand / OLDX technical names, project **oldx-staging**, branch **security-hardening-review**. H2Q one-shot was actually executed using immutable source `4d9f871f86c7bb3d523a8f877639d4b8594eff5a`. It returned:

- `OLDX_H2Q_RESULT=READ_ONLY_THREE_POLICY_LEVELS_WITH_LIMITS`, `PROJECT_READ=VERIFIED`, **17** direct project IAM bindings of which **1 conditional**, Gateway signer count **0**.
- `RING_READ=VERIFIED`, **0** ring policy bindings; `KEY_READ=VERIFIED`, **0** CryptoKey policy bindings; Gateway signer count **0** at both.
- `ORG_FOLDER_GROUP_DENY_EFFECTIVE_IAM=NOT_CHECKED`; IAM grants/KMS signs/SA key creation/Cloud Run NONE; Cloud writes NONE. **H2Q PASS is policy-read completion, not proof of effective permission**. Project's 1 conditional binding must remain unchanged.
- [H2Q source, owner consent, receipt and prior identities](OLDX_STEP05_H2P2_ACTUAL_PASS_NEXT_H2Q_IAM_SCOPE_2026-11-27.md). H2Q marker `/root/.oldx-step05-h2q-three-iam-policy-reads-once-20261127` **CONSUMED**, never rerun or reset H2Q or H2P2, H2P1, H2O, H2N, H2M. Private raw policies/etags are retained only in Owner's root WSL folder.

## Next H2R exact target (only a proposal; NOT approved or executed)

Add **ONE** `roles/cloudkms.signer` IAM policy binding for **only**:

- Member: `serviceAccount:oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` (verified immutable UID `107238619872767759560`).
- CryptoKey: `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256` ONLY.
- The real signing adapter must separately pin **version /1** and SPKI SHA256 `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`. No per-version IAM policy.
- No access grant to `oldx-c2-web-mediator`, `oldx-c2-product-backend`, older disabled H1B trial SA, other principals, ring or project. `roles/cloudkms.signer` grants signing **not** public-key viewing; don't broaden to `signerVerifier`.

**Prepared H2R source, NOT EXECUTED:** `scripts/step05_h2r_one_cryptokey_gateway_signer_owner_approved_once_20261127.py`
- Immutable source commit: `0b7c1f4dd397046544c47feee01c729d83ca5248`
- Git blob readback: `044d1f1622241efb9865e56cb9bdaa1064ac4848`
- Source static guard inspection PASS; Python AST/runtime/Google API behavior have not been executed. One-time root WSL owner flag required; strict Yasmin account/project/isolated native SDK/verified H2Q marker and local saved evidence for **3 UID matches**; requires project direct policy **17 bindings, 1 conditional**, ring/key direct binding **0**, key etag present and exact private original policy.
- New H2R exclusive marker created **before any H2R Cloud call**. Exactly **one NEW CryptoKey GET :getIamPolicy** and exact comparison with private H2Q policy object/etag. Any unexpected change, no etag, mismatch or error STOP **without IAM write**.
- Only after fresh preimage match, exactly **one** `POST https://cloudkms.googleapis.com/v1/projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256:setIamPolicy` with one role/member binding, prior etag, `updateMask="bindings,etag"`. Validate response contains only that binding and **changed etag**, then **one** fresh CryptoKey policy GET confirming exact binding/etag.
- On ambiguous write, 403/404, readback mismatch or timeout **STOP, never re-POST, never auto-rollback or clear marker**. Private before/after policy and sanitized receipts stay on Owner WSL. On STOP preserving the previous private H2Q policy is needed for distinct safe recovery review, not a license to overwrite.
- No org/folder/group/deny effective-IAM conclusion, no claims of working signing, no asymmetricSign, SA JSON keys, Cloud Run deployment or identity binding, Firebase, Firestore, photos, DNS, Product H2 enabled run or production launch. Any separately required status/metadata reader is NOT implicitly granted.
- Google official reference: [setIamPolicy replaces policy and uses etag](https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys/setIamPolicy), [KMS least privilege](https://docs.cloud.google.com/kms/docs/iam), [IAM effective policy limitations](https://docs.cloud.google.com/iam/docs/troubleshoot-policies).

**27 Nov 2026 — exact H2R OWNER WRITE APPROVAL RECEIVED; NOT EXECUTED:** Owner replied **“ha manjuri chhe”** to the single proposed `roles/cloudkms.signer` policy binding for `serviceAccount:oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` (UID `107238619872767759560`) on only CryptoKey `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256`, including one fresh read-only preimage GET and one read-only verification GET. This is separate from earlier H2Q read consent. No access to project/keyring/mediator/backend; no signing operation, SA keys, deployment or production. **Consent recorded does not mean the IAM write was attempted or succeeded.**

### One Ubuntu root WSL paste — within the now-approved exact H2R grant

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2r-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2r.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/0b7c1f4dd397046544c47feee01c729d83ca5248/scripts/step05_h2r_one_cryptokey_gateway_signer_owner_approved_once_20261127.py' &&
test "$(git hash-object "$d/h2r.py")" = '044d1f1622241efb9865e56cb9bdaa1064ac4848' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2r.py" &&
python3 -B "$d/h2r.py" --owner-approved-exact-h2r-one-key-gateway-signer-iam-grant-once
~~~

Expected only on real success: `OLDX_H2R_RESULT=PASS_EXACT_ONE_CRYPTOKEY_GATEWAY_SIGNER_BINDING_VERIFIED`; `ONE_KEY_POLICY_POST_ATTEMPTED=TRUE`, `READBACK_VERIFIED=TRUE`, `OTHER_CLOUD_WRITES_KMS_SIGN_SA_KEYS_RUN=NONE`, `DO_NOT_REPEAT=TRUE`. No additional Cloud work without new scoped consent.

**CURRENT:** H2Q actual PASS, H2R OWNER_APPROVED_SOURCE_READY_NOT_EXECUTED, Step05 ACTIVE, H2/PRODUCTION NO-GO.

## 27 Nov 2026 ~01:16 IST — H2R ACTUAL OWNER CLOUD PASS (LATEST, supersedes pre-run statements)

Owner supplied a WSL screenshot after executing pinned source commit `0b7c1f4dd397046544c47feee01c729d83ca5248`, blob `044d1f1622241efb9865e56cb9bdaa1064ac4848`. The screenshot shows the hash check and Python AST command followed by the following actual output:

~~~text
OLDX_H2R_RESULT=PASS_EXACT_ONE_CRYPTOKEY_GATEWAY_SIGNER_BINDING_VERIFIED
OLDX_H2R_REASON=ONE_SETIAM_POLICY_ETAG_GUARDED_READBACK
OLDX_H2R_PROJECT=oldx-staging
OLDX_H2R_GATEWAY_UID=107238619872767759560
OLDX_H2R_FRESH_PREIMAGE_VERIFIED=TRUE
OLDX_H2R_ONE_KEY_POLICY_POST_ATTEMPTED=TRUE
OLDX_H2R_SET_RESPONSE_VERIFIED=TRUE
OLDX_H2R_READBACK_VERIFIED=TRUE
OLDX_H2R_OTHER_CLOUD_WRITES_KMS_SIGN_SA_KEYS_RUN=NONE
OLDX_H2R_H2_PRODUCTION=NO_GO
OLDX_H2R_DO_NOT_REPEAT=TRUE
~~~

**ACTUAL VERIFIED:** KMS CryptoKey `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256` has exactly one direct `roles/cloudkms.signer` member `serviceAccount:oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`, UID `107238619872767759560`. Fresh H2Q preimage/etag was checked, policy set response validated, and fresh GET readback confirmed the exact binding. No project or ring IAM modification, mediator/backend grant, SA key, KMS asymmetricSign, Run, H2 activation or production by this script. No evidence of **effective runtime signing** yet; folder/org/group/deny scope still not checked.

**Consumed:** H2R one-shot marker `/root/.oldx-step05-h2r-gateway-single-key-signer-grant-once-20261127`. NEVER run H2R/H2Q/H2P2/other consumed one-shots again, never remove markers, never repeat policy grant. H2R is the single IAM binding gate DONE, not Step05 overall DONE.

**Next gate H2S** must prove an *authenticated actual private Gateway runtime*, bearing the newly verified Gateway service-account identity (not the WSL Owner OAuth account and not an impersonated SA JSON key), can perform **one** bounded synthetic `CryptoKeyVersion /1:asymmetricSign` while checking `verifiedDigestCrc32c`, returned `signatureCrc32c`, public SPKI fingerprint `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`, and RSA-SHA256 verification. Google KMS `roles/cloudkms.signer` grants `useToSign` but **not** `viewPublicKey`; use previously pinned public key as independent verifier and separately review key-version status provider. No runtime/host or KMS sign has yet been approved or executed. Avoid Owner-credential sign which cannot validate the Gateway IAM binding; avoid creating SA JSON keys or granting Token Creator solely for a probe.
