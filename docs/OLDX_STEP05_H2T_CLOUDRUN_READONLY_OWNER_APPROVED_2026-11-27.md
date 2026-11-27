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

## 27 Nov 2026 ~21:21 IST — OWNER ACTUAL H2T READ-ONLY PASS WITH LIMITS (CONSUMED)

Owner's Ubuntu root WSL screenshot after running the exact previously authorized, Git-blob-verified immutable script at commit `4e3c52b9b176644c8ff5dd936aaec7390acb87cf`:

~~~text
OLDX_H2T_RESULT=READ_ONLY_CLOUDRUN_REGION_LIST_AND_MATCHED_IAM_VERIFIED_WITH_LIMITS
OLDX_H2T_REASON=SERVICE_DIRECT_POLICY_NOT_EFFECTIVE_INHERITED_IAM
OLDX_H2T_PROJECT=oldx-staging
OLDX_H2T_REGION=asia-south1
OLDX_H2T_LIST_COMPLETE=TRUE
OLDX_H2T_SERVICES_COUNT=1
OLDX_H2T_H2_MATCHED_SERVICES=0
OLDX_H2T_GATEWAY_SA_TEMPLATE_SERVICE_COUNT=0
OLDX_H2T_EFFECTIVE_IAM=NOT_VERIFIED
OLDX_H2T_FIRESTORE_KMS=NOT_CHECKED
OLDX_H2T_EVIDENCE=/root/oldx-h2t-cloudrun-inventory-20261127T155120Z
OLDX_H2T_CLOUD_WRITES_KMS_SIGN=NONE
OLDX_H2T_H2_PRODUCTION=NO_GO
OLDX_H2T_DO_NOT_REPEAT=TRUE
~~~

**Exact interpretation and bounded claim:** v2 Cloud Run regional services list is **complete** for `oldx-staging/asia-south1` at that read. Exactly **one Cloud Run service** was listed; **zero** services matched the H2 `oldx-c2-*` name / verified Mediator, Gateway or Backend service-account attachment criteria, and **zero** services' template attached the H2 Gateway SA. The existing one unrelated service was **not inspected individually for IAM or revisions**, since H2T intentionally limited matching to H2 candidates. Thus the return string `...MATCHED_IAM_VERIFIED_WITH_LIMITS` means the conditional algorithm completed—not that any H2 service IAM was actually read. **No H2 Cloud Run Gateway deployment/ready revision is established in this region**, and it is not evidence about other projects/regions, unrelated IAM or an effective inherited permissions analysis. One previous H1B service had already been deleted/verified 404; never rebuild/replay it merely for this inventory.

**One-shot permanently consumed:** `/root/.oldx-step05-h2t-run-inventory-readonly-once-20261127` and the above root-local evidence must be preserved. DO NOT rerun H2T, reset marker, repeat prior H2N/H2R/IAM/SA probes or older Node tests. No cloud mutations/signing happened.

**Next rational critical path: H2U source-only private Gateway deployment packet and runtime blocker resolution.** Since H2T shows zero current H2 runtime candidates, a future fresh *new* private Cloud Run Gateway service/revision (NOT the one unrelated service) is required for actual runtime signing. Its image must actually compile/include the H2 Gateway host and trusted provider bindings, not simply re-label the old H1B OFF-only image. Do not deploy unconnected stub as if H2 is ready. Before approval to deploy: verified reproducible new immutable image, exact runtime Gateway SA `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` UID `107238619872767759560`, private ingress and narrowly scoped Invoker policy, nonpublic default-OFF behavior, independent authorized KeyVersion `/1` status/PEM reader (no broadened signer role), real allowed `(default)` Firestore document transaction/retention for permanent one-sign budget, tight synthetic approval window, test/readback, rollback/cleanup. None of those newly hosted permissions or deploys were authorized by this read-only approval.

**Status:** `H2T=ACTUAL_PASS_WITH_LIMITS_CONSUMED`; `H2_RUNTIME_SERVICE_IN_REGION=NO_H2_MATCH`; `H2_HOSTED_KMS_SIGNING=NOT_ATTEMPTED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
