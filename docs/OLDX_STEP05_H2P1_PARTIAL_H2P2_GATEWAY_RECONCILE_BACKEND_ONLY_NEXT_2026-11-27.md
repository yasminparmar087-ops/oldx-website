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

### New separate Owner consent REQUIRED before execution

This is **not** covered by prior H2P1 one-shot (consumed) or H2O metadata consent. It authorizes a finite new set of narrowly scoped **IAM read-only reconciliations** plus **at most one new BACKEND account creation**, conditional on Gateway + Mediator UID confirmation; includes up to five read-only post-create GETs and bounded backoff. It does **not** authorize any Gateway recreate, project/crypto IAM grant, signing or deployment. A new service account resource may have administrative implications; no user-managed key or recurring VM/Cloud Run cost is caused by this script alone.

### ONE root Ubuntu WSL paste — ONLY AFTER this exact new consent

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2p2-recovery.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2p2.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/53bd2864eb9b7fb374ad0fe901ff4c2e2eeee20b/scripts/step05_h2p2_gateway_reconcile_one_backend_create_conditional_owner_once_20261127.py' &&
test "$(git hash-object "$d/h2p2.py")" = '2cd4731290abfd14d31b8c9602549f73a97334ef' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2p2.py" &&
python3 -B "$d/h2p2.py" --owner-explicitly-approved-h2p2-reconcile-and-one-backend-create-if-safe
~~~

**Success only if all three numerically verified:** `OLDX_H2P2_RESULT=PASS_GATEWAY_RECONCILED_AND_ONE_BACKEND_CREATED_VERIFIED` and `OLDX_H2P2_BACKEND_READBACK_VERIFIED=TRUE`. No result or STOP can be treated as H2/production acceptance. DO NOT rerun any one-shot or clear markers.

**Current status:** `H2P1=PARTIAL_STOP_ACTUAL`, `H2P2=SOURCE_READY_UNAPPROVED_UNRUN`, `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`. After H2P2 actual success the remaining technical gap is properly scoped CryptoKey-level signing permission, effective IAM and trusted hosted Product integration, not more SA creations.
