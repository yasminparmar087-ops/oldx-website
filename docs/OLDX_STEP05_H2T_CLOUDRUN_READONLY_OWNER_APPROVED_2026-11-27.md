# OLDX Step05 H2T — Owner-approved bounded Cloud Run read-only inventory (27 Nov 2026)

## Why H2T; existing completed work MUST NOT be repeated

On 27 Nov ~21:14 IST, Owner screenshot confirmed **three new H2S KMS KeyVersion status OFFLINE focused tests actual 3/3 PASS**, 0 FAIL on Node24.22.3, one-shot marker consumed. [H2S receipt](OLDX_STEP05_H2S_KMS_INDEPENDENT_VERSION_STATUS_SOURCE_2026-11-27.md). Prior one-sign Firestore ledger 3/3, metadata OAuth 3/3, synthetic signing mock 3/3, H2N two KeyVersion/public-key GETs and H2R one exact CryptoKey Gateway signer IAM grant also completed. **Do not run them again, clear markers, repeat scans/builds or recreate SA.**

Verified service-account identity (H2P2 prior): Gateway `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`, UID `107238619872767759560`. **An account existing is NOT proof that a Cloud Run service/revision uses it.** Old H1B `oldx-c2-website-mediator` test service was **deleted and readback 404** on 26 Nov; **never recreate, re-probe or delete again**.

## Exact Owner approval and source

Owner explicitly answered **"ha manjuri chhe"** to **one bounded read-only inspection** of H2S Cloud Run service/revision, attached identity, image, ingress and direct service-level Invoker IAM in `oldx-staging` / `asia-south1`. This approval is **not** an authorization for new KMS GET/signing, project IAM changes, Firestore/Firebase operations, service deployment, service-account creation, billing changes or production.

Prepared **only** `scripts/step05_h2t_one_region_private_cloudrun_iam_inventory_readonly_once_20261127.py`.
- Immutable source commit **`4e3c52b9b176644c8ff5dd936aaec7390acb87cf`**
- Git blob SHA1 **`d529c3137d7ef3989ac6773c0b2ac8ecb816185c`**
- Static GitHub readback/scope checks PASS; Python AST, Owner WSL execution and Cloud API outcomes **NOT yet performed**.
- Requires Ubuntu root WSL, exact isolated native Cloud SDK and Yasmin Owner `oldx-staging` active project/account and new exact CLI consent flag. Uses Owner OAuth **only to read Cloud Run Admin API metadata**, never KMS signing or SA impersonation, and does not publish bearer token.
- Creates new one-shot marker **before Cloud Run GET**, `/root/.oldx-step05-h2t-run-inventory-readonly-once-20261127`; do not remove or rerun on partial/STOP.
- Calls only `GET https://run.googleapis.com/v2/projects/oldx-staging/locations/asia-south1/services?pageSize=100` with up to **3 regional pages**; if paginated beyond third, unreachable/malformed or unauthorized then STOP, **no false claims of complete absence**.
- On one **complete** region list, matches at most **four** H2-candidate services by name `oldx-c2-*` or exact previous H2 Mediator/Gateway/Backend runtime SA email. Only for those listed matches, calls **one** service `:getIamPolicy` GET and, where there is a ready revision name, **one** exact ready-revision GET. Max **3 list + 4 IAM + 4 revision GETs**, no extra service GET or arbitrary project wildcard. No distinct request to the old deleted H1B service.
- Prints only sanitized service labels, attached service-account email, ingress, `invokerIamDisabled`, direct broad Invoker count and whether ready image is pinned to `@sha256:` in its configured reference. Private JSON evidence saved under `/root/oldx-h2t-cloudrun-inventory-YYYYMMDDTHHMMSSZ`; **do not commit raw IAM policies or tokens**.
- **NOT** a proof of inherited IAM, organization/folder/group/deny conditions, public reachability, attested immutable image provenance, Gateway's effective KMS permission, KMS KeyVersion current status or Firestore write authorization. `invokerIamDisabled` and direct `roles/run.invoker` help flag potential public exposure; absence of broad direct members is not equivalent to private effective IAM.
- The script makes **zero Cloud writes and zero HTTP invocation to the application**, never fetches KMS metadata, never signs, creates, deploys, deletes or sets IAM.
- Google REST API documentation: [services.list](https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/list), [service getIamPolicy](https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/getIamPolicy), [ready revision get](https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services.revisions/get).

### One exact Ubuntu root WSL command — NEW read-only authorization already received

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2t-ro-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2t.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/4e3c52b9b176644c8ff5dd936aaec7390acb87cf/scripts/step05_h2t_one_region_private_cloudrun_iam_inventory_readonly_once_20261127.py' &&
test "$(git hash-object "$d/h2t.py")" = 'd529c3137d7ef3989ac6773c0b2ac8ecb816185c' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2t.py" &&
python3 -B "$d/h2t.py" --owner-approved-exact-h2t-cloudrun-service-iam-inventory-readonly-once
~~~

**On success only:** `OLDX_H2T_RESULT=READ_ONLY_CLOUDRUN_REGION_LIST_AND_MATCHED_IAM_VERIFIED_WITH_LIMITS`, `OLDX_H2T_LIST_COMPLETE=TRUE`, `CLOUD_WRITES_KMS_SIGN=NONE`, `H2_PRODUCTION=NO_GO`, `DO_NOT_REPEAT=TRUE`. If zero H2 candidates with complete list, that only establishes no candidates under tested name/attached-SA rules in this ONE region as of the read—not global absence. On `STOP`, partial/denied/timeout, keep marker and local evidence. **Do not retry** this one-shot without distinct recovery review.

**Current:** H2T OWNER_APPROVED_SOURCE_READY_NOT_EXECUTED. Step05 ACTIVE; H2/PRODUCTION NO-GO. Wait for actual Owner WSL receipt to mark H2T PASS/STOP; no success is assumed before receipt.
