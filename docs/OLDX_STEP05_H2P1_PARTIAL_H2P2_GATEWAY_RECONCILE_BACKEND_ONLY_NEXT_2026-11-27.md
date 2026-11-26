# OLDX Step05 H2P2 — conditional one-Backend recovery after H2P1 partial STOP

**27 Nov 2026 ~00:55 IST — H2P1 ACTUAL STOP_AFTER_MARKER**. [Owner screenshot result and receipt](OLDX_STEP05_H2O_ACTUAL_PASS_H2P1_THREE_SAS_CREATION_NEXT_2026-11-27.md). Exact `oldx-staging`, fresh attempt count TWO, one actual verified enabled Mediator UID `100779414920484819274`, Gateway create attempted but immediate email GET readback HTTP 404; Gateway existence / UID **UNVERIFIED**, and Backend **NOT ATTEMPTED**. IAM grants/SA keys/KMS sign/Run/production NONE. H2P1 marker CONSUMED: **DO NOT rerun H2P1 or recreate Gateway**.

Google Cloud [Create Service Accounts](https://docs.cloud.google.com/iam/docs/service-accounts-create) documents that a new account may take time to become readable and recommends retrying read requests with exponential backoff; [Manage Service Accounts](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts) recommends numeric `uniqueId` immediately after creation. These are plausible explanations, **not evidence** that the Gateway was created. No new live Google calls have been made in this planning phase.

## H2P2 proposed NEW, finite recovery — SOURCE PREPARED ONLY, not approved or executed

**Exact source:** `scripts/step05_h2p2_gateway_reconcile_one_backend_create_conditional_owner_once_20261127.py`

- Source commit: `53bd2864eb9b7fb374ad0fe901ff4c2e2eeee20b`.
- Verified Git blob: `2cd4731290abfd14d31b8c9602549f73a97334ef`.
- Uses existing isolated Yasmin root WSL SDK/project without new login, config change, Cloud Shell, builds, scans or tests. Reads H2P1 local one-shot marker and exact root-owned sanitized receipt; requires **specific** `STOP_AFTER_MARKER / GATEWAY_READBACK_HTTP_404`, attempted `MEDIATOR,GATEWAY`, one verified Mediator UID `100779414920484819274`, and no Backend attempt.
- New H2P2 marker `/root/.oldx-step05-h2p2-partial-three-sa-reconcile-backend-only-once-20261127` is created **before any H2P2 Cloud requests**, so one finite batch. **Do not reset/repeat after a STOP.**
- Exact read-only preflight: ONE `oldx-staging` first-page IAM serviceAccounts.list with narrow `email,uniqueId,disabled,name,projectId` fields, no nextPageToken; requires Mediator exact email/UID and Gateway distinct enabled account with numeric UID; requires Backend not in the complete page. Then GET exact Mediator by pinned numeric UID and Gateway by listed numeric UID, checking response email/UID/status/project. Then GET exact Backend email requiring 404, not 403 or other status. If Gateway is missing/unknown or any guard fails, **STOP without new resource writes**; **NEVER send a Gateway-create POST**.
- **ONLY IF the above all pass:** ONE backend-only `projects.serviceAccounts.create` POST for `oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com`, display name `OLDX H2 Product Backend`. Validate returned immutable UID, distinct from Mediator/Gateway. GET-by-numeric-UID readback, bounded **5 GETs total** with only GET backoff at 0/1/2/4/8 seconds if HTTP 404 is transient. There is only **one** Backend create POST ever in this script; no automatic duplicate creates or partial cleanup.
- Report locally `OLDX_H2P2_*` and private sanitized evidence; never OAuth token or whole IAM inventory in GitHub.
- Strict NON-SCOPE: **no create/recreate/enable/disable/delete of Gateway, Mediator or old H1B trial SA**; no IAM grants, SA keys, CryptoKey IAM policy/sign, Cloud Run, Firebase/Auth, Firestore, Storage, image push, deployment, DNS, billing settings, enabled Product or production. Backend creation itself does not bind it to Cloud Run.
- If Gateway remains absent in new complete list or has mismatched data: **STOP with no Backend creation**. If Backend creation returns ambiguous outcome or bounded readback fails: **STOP, no retry of create**. Later reconciliation would need new evidence and consent.
- New script was **GitHub readback verified and statically guard-inspected**; **Python AST/runtime and Google API execution have NOT occurred**. Thus no H2P2 account state or Google permission is yet established.

### 27 Nov 2026 — Exact H2P2 owner consent RECEIVED; execution NOT YET ATTEMPTED

Owner explicitly replied **“ha manjuri chhe”** to the narrowly described **H2P2** recovery: a fresh project-only SA listing, numeric-UID readbacks of already-attempted Mediator/Gateway, exact Backend absence GET, and, **only if all pass**, exactly ONE new Backend Service Account creation with bounded GET-only verification. Consent does **not** cover Gateway recreation, retrying H2P1, Service Account keys, KMS signing, IAM grants, Cloud Run deployment, Firebase or production. The script still has **NOT been run**; do not claim success before operator results.

This is **not** covered by prior H2P1 one-shot (consumed) or H2O metadata consent. It authorizes a finite new set of narrowly scoped **IAM read-only reconciliations** plus **at most one new BACKEND account creation**, conditional on Gateway + Mediator UID confirmation; includes up to five read-only post-create GETs and bounded backoff. It does **not** authorize any Gateway recreate, project/crypto IAM grant, signing or deployment. A new service account resource may have administrative implications; no user-managed key or recurring VM/Cloud Run cost is caused by this script alone.

### ONE root Ubuntu WSL paste — under the now-confirmed, exact H2P2 consent

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2p2-recovery.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2p2.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/53bd2864eb9b7fb374ad0fe901ff4c2e2eeee20b/scripts/step05_h2p2_gateway_reconcile_one_backend_create_conditional_owner_once_20261127.py' &&
test "$(git hash-object "$d/h2p2.py")" = '2cd4731290abfd14d31b8c9602549f73a97334ef' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2p2.py" &&
python3 -B "$d/h2p2.py" --owner-explicitly-approved-h2p2-reconcile-and-one-backend-create-if-safe
~~~

**Success only if all three numerically verified:** `OLDX_H2P2_RESULT=PASS_GATEWAY_RECONCILED_AND_ONE_BACKEND_CREATED_VERIFIED` and `OLDX_H2P2_BACKEND_READBACK_VERIFIED=TRUE`. No result or STOP can be treated as H2/production acceptance. DO NOT rerun any one-shot or clear markers.

**Current status:** `H2P1=PARTIAL_STOP_ACTUAL`, `H2P2=OWNER_APPROVED_SOURCE_READY_NOT_EXECUTED`, `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`. After H2P2 actual success the remaining technical gap is properly scoped CryptoKey-level signing permission, effective IAM and trusted hosted Product integration, not more SA creations.

## 27 Nov 2026 ~01:01 IST — OWNER H2P2 ACTUAL PASS, THREE DEDICATED SAs VERIFIED

Owner submitted WSL terminal screenshot after executing the pinned script at source commit `53bd2864eb9b7fb374ad0fe901ff4c2e2eeee20b` and verifying blob `2cd4731290abfd14d31b8c9602549f73a97334ef`. Actual sanitized results:

~~~text
OLDX_H2P2_RESULT=PASS_GATEWAY_RECONCILED_AND_ONE_BACKEND_CREATED_VERIFIED
OLDX_H2P2_REASON=PREVIOUS_GATEWAY_UID_AND_BACKEND_NEW_UID_VERIFIED
OLDX_H2P2_MEDIATOR_VERIFIED=TRUE
OLDX_H2P2_MEDIATOR_UID=100779414920484819274
OLDX_H2P2_GATEWAY_VERIFIED=TRUE
OLDX_H2P2_GATEWAY_UID=107238619872767759560
OLDX_H2P2_BACKEND_CREATE_ATTEMPTED=TRUE
OLDX_H2P2_BACKEND_READBACK_VERIFIED=TRUE
OLDX_H2P2_BACKEND_UID=106984791114720194680
OLDX_H2P2_GATEWAY_CREATE_REPEATED=FALSE
OLDX_H2P2_IAM_GRANTS_KMS_SIGN_RUN_SA_KEYS=NONE
OLDX_H2P2_H2_PRODUCTION=NO_GO
OLDX_H2P2_DO_NOT_REPEAT=TRUE
~~~

**Identity mapping now verified in oldx-staging:**

| Role | Exact service account email | Google immutable uniqueId | H2 status |
|---|---|---|---|
| Mediator | `oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com` | `100779414920484819274` | VERIFIED enabled |
| Gateway | `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` | `107238619872767759560` | VERIFIED enabled |
| Backend | `oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com` | `106984791114720194680` | VERIFIED enabled |

H2P1's transient Gateway 404 has now been resolved by exact project list and numeric-ID readback; Gateway was **not** recreated. The sole new resource added by H2P2 was Backend, also readback-verified by numeric UID. All three identities are distinct; no user-managed SA keys or IAM grant issued by either creation script. H2P2 one-shot marker `/root/.oldx-step05-h2p2-partial-three-sa-reconcile-backend-only-once-20261127` now consumed: **NEVER repeat H2P1/H2P2, remove their markers, or recreate any of the three SAs.** Old H1B trial SA `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` UID `115445220422157278526` remains DISABLED and untouched.

**NEXT critical dependency:** exact CryptoKey-level `roles/cloudkms.signer` on `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256` for **only** the verified `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` (immutable UID `107238619872767759560`). **No IAM grant yet.** Fresh key policy/etag, inherited IAM scope and resource-level role review are needed before a separate scoped owner authorization for any IAM write. The Google [KMS official role table](https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles) states `roles/cloudkms.signer` grants **sign**, but **not** public-key verification. Previous assistant prose that it included verification was incorrect; do not use `signerVerifier` unless truly required. KMS signing adapter may require separate status metadata permission/provider binding rather than expanding signer permissions. `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`.
