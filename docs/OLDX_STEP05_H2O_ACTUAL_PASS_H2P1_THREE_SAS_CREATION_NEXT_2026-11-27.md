# OLDX Step05 H2P1 — Three new runtime SAs, exact creation-only proposal

**27 Nov 2026 ~00:49 IST.** BAJUTO public brand; OLDX internal technical resources unchanged. [Latest H2O actual screenshot receipt](OLDX_STEP05_H2O_SIGNER_IAM_READONLY_PREFLIGHT_NEXT_2026-11-27.md) confirms:
- `OLDX_H2O_RESULT=READ_ONLY_EXACT_SIGNER_IDENTITY_AND_KEY_POLICY_WITH_LIMITS`.
- `OLDX_H2O_ACCOUNT_LIST_SCOPE=COMPLETE_VISIBLE_PAGE`.
- Three exact newly proposed identities (Mediator/Gateway/Backend) each `NOT_IN_COMPLETE_PROJECT_LIST` **only in oldx-staging**; not globally absent.
- Exact new KMS CryptoKey direct policy does not grant the Gateway signing role (`FALSE`). **Inherited/effective IAM NOT checked**. Zero IAM writes and zero Cloud writes.
- H2O marker is consumed. **NEVER repeat H2O, H2N, H2M or earlier one-shot checks, erase receipts or remove old disabled trial SA.**

## Next allowed proposal (SOURCE READY; NEW OWNER WRITE APPROVAL REQUIRED)

Exactly **three fresh user-managed Service Accounts** in `oldx-staging`, initially with **NO roles or user-managed keys** created by this script:
1. `oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com` — private website mediator runtime
2. `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` — private Gateway; *future* exclusive candidate for KMS signing
3. `oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com` — private Product backend

The old `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` SA UID `115445220422157278526` remains **DISABLED/NOT DELETED**, never touched or selected. No other resources, service accounts, default SAs or project policy changed.

**Prepared script (NOT EXECUTED):** `scripts/step05_h2p1_one_create_three_runtime_sas_owner_approved_once_20261127.py`
- Source commit `06e970d20fb944f90d75fac71d6cb8617d4727d4`
- Git blob readback `3707bef2cc485d4eacd68bd4927b8150ce68a1d7`
- Uses retained root Owner WSL native isolated gcloud and exact project/account. Requires H2O one-shot success and root-owned sanitized evidence containing a complete project list with all 3 absent and direct-KMS-policy signer false, but **does not infer inherited IAM absence**.
- Before writing, makes exactly three target-name IAM GETs to require **three HTTP 404s**. Any 403/other/timeout STOP BEFORE FIRST POST; existing account is never overwritten or modified. HTTP 404 on exact project resource path is scoped absence, not permission for general IAM creation.
- After fresh absence preflight, creates exclusive `/root/.oldx-step05-h2p1-three-h2-runtime-service-accounts-owner-once-20261127` marker **before** cloud write. Exactly up to 3 IAM v1 `projects.serviceAccounts.create` POSTs with fixed `accountId` and `displayName`; follows each with one exact-email GET to verify matching immutable UID, canonical name, enabled state, project. No retries, no parallel creations, no delete, no key issuance. On partial/ambiguous POST/GET, stop and record which attempts / UIDs were confirmed. Never rerun after marker, do not auto-cleanup partial state.
- Outputs sanitized short `OLDX_H2P1_*` summary; local private receipt, no OAuth tokens in GitHub.
- Strict non-scope: **NO** CryptoKey `setIamPolicy`, IAM grant, SA key, signing request, Cloud Run service/deployment, Firebase/Auth/Firestore/Storage, billing settings, prod or H2 enable. A successful create is just identity scaffolding, **not** managed identities bound to trusted workloads.
- Source statically inspected and GitHub blob verified; Python AST/runtime/local Google calls **NOT yet tested**. Must be checked by operator command before any cloud action.

**27 Nov 2026 — OWNER EXPLICIT H2P1 APPROVAL RECEIVED:** Owner replied **“ha manjuri chhe”** to creation of exactly THREE new accounts listed above in `oldx-staging`, with the three fresh 404 reads and immediate UID readbacks, accepting the one-shot partial-STOP behavior. This is separate from H2O read authorization; it covers **at most three ServiceAccounts.create writes only**. Live execution still **NOT ATTEMPTED**, and no IAM role or Service Account key creation, KMS grant/sign, Run/Firebase/production changes are authorized. Default SA creation itself does not grant project roles; later service usage may be billable. Permission `iam.serviceAccounts.create` is required; authorization is NOT proven by H2O. Google docs: https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/create ; https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/get .

### Single Owner Ubuntu WSL root paste — under exact H2P1 approval now received

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2p1-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2p1.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/06e970d20fb944f90d75fac71d6cb8617d4727d4/scripts/step05_h2p1_one_create_three_runtime_sas_owner_approved_once_20261127.py' &&
test "$(git hash-object "$d/h2p1.py")" = '3707bef2cc485d4eacd68bd4927b8150ce68a1d7' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2p1.py" &&
python3 -B "$d/h2p1.py" --owner-explicitly-approved-only-three-new-h2-runtime-sa-creates
~~~

Expected fully verified `OLDX_H2P1_RESULT=PASS_THREE_NEW_H2_RUNTIME_SERVICE_ACCOUNTS_CREATED_VERIFIED`; 3 UID receipts; `OLDX_H2P1_IAM_GRANTS_KEYS_KMS_SIGN_RUN=NONE`. On STOP do not repeat or clear markers; preserve evidence for new *read-only* reconciliation before any new consent. No guaranteed complete batch. `STEP05=ACTIVE`, `H2P1=OWNER_APPROVED_SOURCE_READY_NOT_EXECUTED`, `H2/PRODUCTION=NO_GO`.

Next after H2P1 ACTUAL PASS: choose the exact **CryptoKey-level** KMS signer-only role and effective inherited IAM status, source-check preimage/etag/rollback; separate owner consent for any KMS policy write, then real host bindings and one finite private synthetic acceptance. Do not assume CryptoKeyVersion IAM binding supports a version-specific grant; runtime pin remains `/1` with public SPKI hash `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`.
