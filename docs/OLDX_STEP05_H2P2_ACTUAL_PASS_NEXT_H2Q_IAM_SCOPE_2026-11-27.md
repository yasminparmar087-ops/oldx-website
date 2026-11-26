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

## 27 Nov 2026 — H2Q exact three policy reads OWNER APPROVED, SOURCE READY, UNEXECUTED

Owner explicitly answered **"ha manjuri chhe"** to the three **read-only** IAM policy requests above, including the project `POST :getIamPolicy` (a read, **not** a write), Key Ring `GET :getIamPolicy`, and CryptoKey `GET :getIamPolicy`. No approval for `setIamPolicy`, service account changes, signing, deployment, Firebase, H2 enablement or production. H2P2 success already established; its one-shot is consumed.

- **Exact new source:** `scripts/step05_h2q_three_level_iam_policies_readonly_once_20261127.py`
- **Immutable source commit:** `4d9f871f86c7bb3d523a8f877639d4b8594eff5a`
- **Verified Git blob:** `b003bbc6b8838674136b799f9bde6015dd7acb82`
- Static scope audit PASS: validates H2P2 owner WSL marker/private receipt and all 3 immutable UIDs, exact Yasmin owner, isolated WSL SDK and `oldx-staging`; one exclusive H2Q marker before all Cloud reads, exact 3-method+URL allowlist, no redirect/retries, strict policy parsing and version-3 request. Handles empty version-0 policy only with empty bindings.
- Private original 3 policy bodies/etags are retained **locally in root-owned evidence folder**, not uploaded to GitHub; CLI output and repo can contain only sanitized binding/condition counts and etag hash. IAM grants/execution still `NONE`. Do not share OAuth token/raw policies.
- Source GitHub blob and source constraints readback confirmed; **Python AST/runtime and Google Cloud API calls NOT executed yet**. Operator command includes AST parse before entering script. Any network/error/status `STOP` after H2Q marker => **do not repeat** or clear markers.
- Reading project/ring/key policies **does not establish effective access** from folder/org/group/deny policies or verify dynamic conditions. A role grant needs separate identity & IAM policy review and consent.

### Exactly one Ubuntu WSL root paste — under this specific consent

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2q-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2q.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/4d9f871f86c7bb3d523a8f877639d4b8594eff5a/scripts/step05_h2q_three_level_iam_policies_readonly_once_20261127.py' &&
test "$(git hash-object "$d/h2q.py")" = 'b003bbc6b8838674136b799f9bde6015dd7acb82' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2q.py" &&
python3 -B "$d/h2q.py" --owner-approved-exact-h2q-three-readonly-iam-policies-once
~~~

**Expected qualified read-only success:** `OLDX_H2Q_RESULT=READ_ONLY_THREE_POLICY_LEVELS_WITH_LIMITS` and 3 `_READ=VERIFIED` lines. `OLDX_H2Q_IAM_GRANTS_KMS_SIGN_SA_KEYS_RUN=NONE`, `OLDX_H2Q_CLOUD_WRITES=NONE`, `OLDX_H2Q_DO_NOT_REPEAT=TRUE`. A PASS is a policy **metadata** outcome, not KMS signing authorization or hosted H2 readiness. On STOP after any attempt, preserve the one-shot receipts and request distinct read-only reconciliation approval.

**Current:** `H2Q=OWNER_APPROVED_SOURCE_READY_NOT_EXECUTED`; `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`.

