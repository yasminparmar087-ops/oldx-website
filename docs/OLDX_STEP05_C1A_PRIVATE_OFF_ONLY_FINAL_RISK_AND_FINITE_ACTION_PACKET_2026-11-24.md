# OLDX Step05 C1A — PRIVATE / OFF-ONLY Gateway risk and finite change packet (SOURCE REVIEW ONLY)

**Date:** 2026-11-24 IST. **Repository:** `yasminparmar087-ops/oldx-website`; branch `security-hardening-review`. **Baseline verified HEAD at preparation:** `2111816131534ca3f7deeedd9b10ffc96928717f`.

**Status:** `OPTION_C_C0_PLANNING_SELECTED` / `STEP05_IMAGE_SOURCE_AND_LOCAL_TESTS_PASS_WITH_LIMITS` / `STEP05_NEW_GATEWAY_12_HIGH_CVE_RISK_DISPOSITION_PREPARED_NOT_ACCEPTED` / `C1A_AUTHORIZATION=NO` / `C1B_AUTHORIZATION=NO` / `C2_AUTHORIZATION=NO` / `STEP05_HOSTED_BLOCKED` / `PRODUCTION_NO_GO`.

This note is a **finite non-executable planning and risk review packet**. The owner said "ok aagal vadho" to continue source-only work, **NOT** to deploy, create a resource/key/service account or spend money. There were **zero** Google Cloud API actions, IAM changes, deployment, Docker builds, security rescans, old-test reruns, GitHub CI triggers, KMS or Firebase/Firestore operations for this document. Do not interpret any historical Step04 A8 OFF-only acceptance as C1A consent.

## 1. Exactly what was established; do not repeat it

| Subject | Consumed, previously saved proof | Scope / limitation |
|---|---|---|
| OFF-only source | `functions/staging-marketplace/cloud-run-gateway-off-server.mjs`, `Dockerfile.gateway-off` and corresponding deny-all context | GET/HEAD `/health[z]` process health; default API503; no Firebase, Cloud Run token mint, KMS, Product activation or outbound provider clients |
| Source immutable base | `gcr.io/distroless/nodejs24-debian13:nonroot@sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec` | Pinned *base child manifest*, **not** derived Gateway image or verified publisher signature |
| Local derived OFF Gateway | WSL Docker image **ID** `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`; tag `oldx-step05-gateway-off:wsl-once-20261124-801` | NONROOT65532, linux/amd64, read-only, 503, health200, SIGTERM PASS; a **LOCAL Docker image ID is not a remotely pushed Artifact Registry manifest digest** |
| New-image SBOM and Grype | Syft JSON and CycloneDX PASS; Grype VALID. Report at owner's local `/root/oldx-step05-scan-recovery-20261124T123515Z/` | **55 package matches** = HIGH18 / MEDIUM20 / LOW6 / NEGLIGIBLE11; **12 distinct HIGH CVE IDs**. No fresh Grype scan authorized or needed |
| 12 HIGH family grouping | gcc-14: 2 distinct IDs / 8 package matches; openssl: 9 IDs / 9; glibc: 1 ID / 1 | All screenshot Grype fix metadata `NONE_LISTED`; does **not** mean no official fix forever |
| Native linkage snapshot | Node `process.report.getReport().sharedObjects` from that exact new image | `libstdc++.so.6`, `libgcc_s.so.1`, `libc.so.6` loaded; no `libssl` or `libcrypto` in this **single `node -e` process snapshot**; not proof of native-code nonreachability or absence from image |
| Historical prior Step04 A8 | Existing private `oldx-owner-read` A8 `00012-vib` 0%-main; original `00001-8kr` 100% main with protected `healthcheck`/`step3rc14` tags. Old A8 Grype **15 distinct severe CVEs** | **DIFFERENT IMAGE**, old A8 owner-accepted limited default-OFF G2/G4/G8 risk only. No A8 private hosted503, effective inherited Invoker, or enabled user tests proved. Never sum 12 and 15 as distinct combined CVEs |
| Testing ledger | 84 historical distinct focused offline PASS case receipts, plus separately documented new container checks | Not one end-to-end hosted suite; do not rerun old 84 or scan A8/Gateway |

Authoritative upstream receipts:
[12-CVE triage and native linkage](OLDX_STEP05_NEW_GATEWAY_12_HIGH_CVE_TRIAGE_2026-11-24.md),
[local WSL build, SBOM, Grype and snapshot evidence](OLDX_STEP05_ONE_FREE_LOCAL_IMAGE_BUILD_NEXT_HANDOFF_2026-11-24.md),
[existing C1A resource naming/cost design](OLDX_STEP05_OWNER_SELECTED_OPTION_C_C0_AND_MINIMAL_C1A_MANIFEST_2026-11-24.md).

## 2. Finite private OFF-only residual security risk DISPOSITION PROPOSAL — NOT ACCEPTED

**Proposed boundary:** C1A could *only* create/prepare **one NEW private, IAM-authenticated, default-OFF Gateway**, with NO Product route enablement, NO Firebase/Firestore/KMS/owner-read backend invoker privileges, NO public anonymous access, and NO C1B HTTP probes. The image is not free of known vulnerabilities. Owner has **NOT accepted** these 12 new image findings even for C1A. No production/ENABLED exception is proposed.

| Residual family | Evidenced facts | C1A OFF-only risk statement and exact limitation |
|---|---|---|
| GCC runtime 2 CVE IDs (8 binary-package matches) | `libstdc++` and `libgcc_s` **loaded** in snapshot; no untrusted HTTP path to `erase_if`/aligned allocation established | **UNKNOWN REMOTE REACHABILITY; RISK OPEN.** C1A can be considered only with immutable disabled routes, IAM, minimal invocation, nonroot/readonly, no credentials/data-role and explicit LIMITED owner decision. No patch assertion |
| OpenSSL 9 CVE IDs (9 matches) | vulnerable `libssl3t64` package present in SBOM; **not dynamically loaded** in one simple Node `-e` snapshot; OFF source has no explicit QUIC/CMS/DANE/AES-GCM-SIV route | **NO EXPLICIT CODEPATH EVIDENCED; RISK OPEN.** Node/native embedded/lazy-linked crypto paths not excluded. Absence in one list cannot classify issues as eliminated or declare C2 safe |
| glibc 1 CVE ID (1 match) | `libc.so.6` **loaded**; source does not load untrusted gettext catalogs or accept `LANGUAGE` from caller | **LINKED; EXPLOIT PATH UNPROVEN; RISK OPEN.** No general hardened libc exemption or remotely-unreachable guarantee |
| Other 37 non-HIGH package matches | 20 Medium / 6 Low / 11 Negligible | Still part of retained report; this C1A packet does not silently convert their severity to NONE or certify patch state |
| Publisher/source provenance | Public base index/child/config raw SHA256 previously verified, but publisher Cosign policy/attestation remains UNVERIFIED and derived image remains local only | **HARD BLOCK for cloud publishing decision** until exact official publisher/signature requirement, source-to-derived-image trace and immutable registry digest have accepted evidence |
| Existing IAM / project inheritance | Historical project 2 Owners/1 Editor and effective permissions not newly verified | A direct named `run.invoker` grant is **NOT exclusivity proof**. Keep old account privilege unchanged, obtain effective principal review under distinct authorized read-only preflight |

**Explicit owner consent (future) must identify whether they accept these residual risks for C1A ONLY.** Passing a Grype scan while 12 HIGH IDs remain is NOT acceptance. If a new patched official base becomes available, selecting it is a **different source/image/build/scan project requiring fresh approval**; do not silently redo this trial or use mutable/unofficial distributions. A blanket waiver for C2 or live traffic is prohibited.

## 3. Exact proposed C1A resource & change surface — ALL UNCREATED/UNAPPROVED

| Object | Scope / current state |
|---|---|
| Project/region | Historical `oldx-staging`, `asia-south1` (Mumbai). **Not refreshed; must verify exact billing/project and regional quotas just before approved action** |
| NEW Cloud Run service | Candidate `oldx-step05-gateway` — **NOT created**; request billing, `minInstances=0`, `maxInstances=1`, `concurrency=1`, `1vCPU / 512MiB`, `timeout=5s`, startup boost OFF, container port8080, Linux nonroot/read-only image, `NODE_ENV=production`, no secrets or credential/proxy/ADC env |
| NEW attached runtime SA | Candidate `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com` — **NOT created**; attach to Gateway ONLY with zero project-level Firebase/Auth/Firestore/KMS/Cloud Run-backend invoker grants; no downloadable keys |
| Existing Registry | Historical `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images` — reuse it if independently verified in approved future preflight, not a new Registry; at most ONE newly approved immutable reviewed Gateway image artifact |
| Exact image to be deployed | **[UNAVAILABLE]**: local Docker **image ID above is NOT a pushed manifest digest**; immutable Artifact Registry image reference `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/<approved-new-image-name>@sha256:<approved-remote-manifest-digest>` remains UNKNOWN |
| Public network exposure vs IAM | **C1A candidate** `ingress=all` only IF direct authorized tester is chosen: publicly network-reachable, but Cloud Run **Invoker IAM check REQUIRED**, no `--no-invoker-iam-check`, no `allUsers`/`allAuthenticatedUsers` role; owner must acknowledge network reachability. Alternative `ingress=internal` only if an ACTUAL compatible private origin/tester path is proven; Cloud Shell is NOT automatically an allowed private origin |
| Exact invocation principal | **[UNFILLED]**; grant `roles/run.invoker` on NEW service to one explicitly identified authorized tester only, after owner acceptance; historical inherited permissions mean it may not be sole effective invoker |
| Exact deploying principal | **[UNFILLED]**; use current authorized deployer, least privilege. Must have approved Cloud Run create/update/get and *on NEW resources* `run.services.getIamPolicy/setIamPolicy`, and `iam.serviceAccounts.actAs` on NEW SA. If extra grant needed STOP and consent separately, no broad Owner/Editor/TokenCreator |
| External APIs / extra resources | **ZERO** unapproved new KMS, WIF, Cloud Armor, VPC connector, Load Balancer, new billing service, Artifact Registry repo, Firestore database, Firebase/Firestore TTL, public DNS, media, synthetic user; any required API enablement or service-agent is a separate STOP |
| Preserved old backend | Existing `oldx-owner-read` 100%-root `00001-8kr`, A8 `00012-vib` 0%-main, old tags `healthcheck`/`step3rc14` and its IAM/env/routes ALL untouched; no backend calls from new Gateway in C1A |

Proposed change count **UP TO**: 1 NEW runtime SA creation, 1 new reviewed image upload into the existing repository, 1 new Cloud Run service create with single disabled revision, 1 IAM `roles/run.invoker` service-level binding to **exact named tester** if explicitly included. Readbacks limited to the newly created identifiers plus previously authorized protected-baseline comparisons. **NO actual hosted HTTP calls under C1A**; C1B separate.

**Important IAM distinction:** Cloud Run service *deployer* and attached *runtime identity* are separate. A runtime SA needs no Google API roles simply to start an OFF-only server; the deployer needs `iam.serviceAccounts.actAs` to attach it. An unverified default project SA is NOT a substitute for the explicitly scoped new SA. [Cloud Run service identity](https://docs.cloud.google.com/run/docs/securing/service-identity); [IAM permissions](https://docs.cloud.google.com/run/docs/reference/iam/roles); [Invoker checks](https://docs.cloud.google.com/run/docs/securing/managing-access).

## 4. Actual cost calculation and finite owner stop-gates — NO PRETEND HARD ₹ CAP

A prior public-rate worksheet in [C1A owner manifest](OLDX_STEP05_OWNER_SELECTED_OPTION_C_C0_AND_MINIMAL_C1A_MANIFEST_2026-11-24.md) shows reference Cloud Run request-based CPU/memory/request, Registry, Logs and Build costs; **do not treat USD reference rates as exact Mumbai bill or a user-approved spend**. Request-based billing can include instance startup, shutdown and request processing; `minInstances=0`, `maxInstances=1`, an expiry reminder or Google Budget Alert is **NOT** a universal monetary hard stop. [Cloud Run billing](https://docs.cloud.google.com/run/docs/configuring/billing-settings), [Cloud Run pricing including Mumbai region](https://cloud.google.com/run/pricing), [Cloud Run max instances](https://docs.cloud.google.com/run/docs/configuring/max-instances).

The future execution packet must fill all of:

| REQUIRED PRE-C1A cost value | Current value |
|---|---|
| Account/project payer, operator and actual region SKU | `[UNVERIFIED]` |
| Current **gross** usage/spend across existing OLDX providers (not just net after credits) and billing lag | `[UNVERIFIED]` |
| Remaining free trial/allowance and expected expiry, if any | `[UNVERIFIED]` |
| NEW immutable image compressed artifact size, Registry storage/retention/network charges | `[NOT PUBLISHED]` |
| Build/push source: local WSL2 derived image versus cloud; credentials and egress constraints | `[UNDECIDED]`; Cloud Build NOT approved |
| Incremental exposure: 1 runtime SA, 1 image, 1 disabled Cloud Run service, logs, request billing, start/stop, source-to-registry upload, 24h service and <=7d image retention | `[INR TOTAL NOT CALCULATED]` |
| Owner's explicit, finite **maximum approved NEW gross spend**, abort/cleanup authorization and reporting delay | `[NO C1A PERMISSION]` |

Historical owner position: **₹1,000 monthly manual STOP/review-before-new-paid-action threshold**; **₹2,000/month target NOT an enforceable all-provider cap**. Never infer that a few-off HTTP calls are automatically free or that a budget alert immediately stops Cloud Run.

**Conditional future STOP before any Cloud write** if the exact operator/payer, current gross spend/available account limit, actual region price and authorized incremental INR ceiling cannot be determined in the separately scoped preflight. No unlimited monitoring/billing work proposed.

## 5. Finite C1A sequence / protections / new-resource-only rollback — DOCUMENT ONLY

**NO EXECUTE COMMANDS APPROVED**. This is a logical sequence, not permission to run Cloud Shell:

1. Owner explicitly selects **network mode** (IAM-required all-ingress with known externally reachable URL vs verified private internal route) and records acceptance of **12 new image HIGH CVE residuals for C1A ONLY**, still forbidding C2.
2. Obtain distinct **narrow read-only** preflight authorization to confirm current `oldx-staging` project/region, existing Registry/service collisions, exact deployer and tester effective principal access, protected old service/SA/image preimages, actual payer and gross spending status. Never replay old A8 original build/probe/IAM inventory just to fill historical fields.
3. Freeze exact image source commit and immutable pushed **registry** digest, publisher signature policy, latest NEW image SBOM/Grype report hash and 12 CVE disposition. **Publishing itself would be a new approved action; do not confuse a local Docker image ID with registry immutable digest**. If publisher proof cannot be met, HOLD.
4. **Separate** owner finite C1A authorization must name exact **4 new write types**, target resource IDs and one image tag/digest, approved operator/ tester, ingress/IAM, max spend/time, cleanup authority and protected baselines; no new unplanned SA/IAM key/role granted. Any ambiguity => STOP.
5. Once separately authorized, at most 1 new SA, 1 image push, 1 off-only service create, 1 named `run.invoker` policy binding. Inspect precise new resource metadata, correct unchanged old backend/routing and saved evidence. No C1B probes, no Product calls, no user data/nonce.
6. **Rollback only under separately explicit cleanup authority** against exact new resource IDs/etags/generation and preimages, in dependency-safe order: stop/delete NEW service, remove NEW service-only IAM binding if safe, delete only owner-approved NEW image after required evidence retention and no consumers, then delete only newly created dedicated SA. Never delete existing Registry repo, old backend/root/tags, any historical A8 revision or other user data. On ambiguous partial write, STOP/inspect; no blind retry.

**Finite target** (proposal): 1 Cloud Run service, 1 SA, 1 image in existing Repo; OFF-only 24-hour supervised retention, <=7day image retention; C1A maximum **zero hosted HTTP probes**. Not yet owner-accepted or physically enforced. This plan **does not** claim a "hard cap" on spend.

## 6. C1B and C2 remain separate

- **C1B** (future distinct consent) at most **6 IAM-authenticated and denied Hosted OFF-only HTTP requests within 20 min**, exact known tester and audience, health200/API503/unauthorized denials. No auto retry, no Product/Firebase/Firestore/KMS/nonce data operations or activation, no implicit service cleanup.
- **C2** (future different consent) enabled seller/buyer Product stack, Google identity/KMS/request binding/nonce Timestamp TTL, media and publications, effective Firestore IAM and at least 15 separate prior A8 severe CVEs, Google Cloud gross budget/rollback: **NOT authorized**. Success of the OFF-only Gateway does NOT certify C2.

## 7. The NEXT ONE decision to move fast

**Recommended next milestone is a single targeted READ-ONLY current-account preflight**, not an immediate paid resource/deployment. It can fill the C1A operator/tester/ingress/price constraints without repeating historical image/test work. Produce a **separate narrow owner-consent request** for exact Google Cloud read-only scope before calling APIs; no current command is issued here.

Until preflight, the user does NOT need another Docker/Syft/Grype build/test. Leave both WSL Docker image and raw scanner reports untouched. Future progress is administrative/authorization and new-resource scope, not rerunning old work.

**Immutable decisions:** `OPTION_C_C0=SELECTED`, `C1A_PRIVATE_OFF_RISK=REVIEW_PROPOSED_NOT_ACCEPTED`, `C1A_EXECUTION=NOT_APPROVED`, `C1B/C2=NOT_APPROVED`, `STEP05_HOSTED=BLOCKED`, `PRODUCTION=NO_GO`.


## 24 Nov 2026 — Owner AUTHORIZED exact-target READ-ONLY Cloud C1A preflight; NOT YET EXECUTED

Owner responded **"ha manjuri chhe"** to the immediately preceding explicit scope: *read-only* `oldx-staging` C1A current project/operator/tester access, proposed new gateway and SA name, existing exact registry, billing linkage and scoped IAM preflight. This consent covers metadata and IAM policy **reads only**; no new cloud service/image/upload, credentials, IAM binding, Billing change, token mint output, hosted HTTP calls, KMS/Firebase/Firestore, API enabling, CI or cost-incurring Cloud Build/deploy. Existing Step04 A8 full IAM/service/scan work must NOT be repeated.

**Approved execution script created SOURCE ONLY:** [`scripts/step05-c1a-read-only-cloud-preflight.sh`](../scripts/step05-c1a-read-only-cloud-preflight.sh). It makes bounded `gcloud ... describe` GETs for exact project `oldx-staging`, candidate `oldx-step05-gateway` service in `asia-south1`, candidate `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com`, already-proposed regional Artifact Registry `oldx-staging-images`, `billing projects describe`, and **one newly targeted** direct project IAM binding snapshot for **active operator role hints and count of owner/editor binding members only**. No project-wide detailed principals, API tokens, billing-account numbers or secret credentials are printed; private raw temporary metadata is discarded. All results are summarized in a small private `$HOME/oldx-step05-c1a-readonly-*.txt` file. Name-collision failure and permission denied are distinguished; unknown/hidden does NOT mean resource absent. The active operator is masked in exported output; the exact tester is still **UNSELECTED**. Direct project binding counts are NOT effective inherited IAM. `billingEnabled` is ONLY billing-link status, NOT gross provider usage, remaining trial credit, guaranteed cost ceiling or approved spending.

**Runtime access:** this assistant has NO authenticated Google Cloud account/Cloud Shell session connector. The user will execute the approved new script in THEIR existing Cloud Shell. No Cloud API commands have actually been run by the assistant. No test/cost/identity evidence is invented from preparing a script.

**One current-user Cloud Shell command** will be authored from the pinned GitHub SOURCE COMMIT once source has passed static verification, without git clone or installation (Cloud Shell home previously only 39MiB available). It must download only the immutable new script to a uniquely named file under `/tmp`, check Bash syntax, and execute once. Do not print raw auth account or private resource metadata into the chat; send only the intentionally redacted summary.

**Gates unchanged:** `C1A_READ_ONLY_PREFLIGHT=OWNER_APPROVED_PREPARED_NOT_EXECUTED`; `C1A_OWNER_12_HIGH_CVE_RISK=NOT_ACCEPTED`; `C1A_NEW_WRITES/DEPLOYMENT=NOT_APPROVED`; `CURRENT_GROSS_BILL=UNKNOWN`; `PUBLISHER/DERIVED_REGISTRY_DIGEST=UNKNOWN`; `C1B/C2=NOT_APPROVED`; `STEP05_HOSTED=BLOCKED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — Owner Cloud Shell C1A read-only preflight EXECUTED: five scoped metadata checks OK, service lookup inconclusive

Owner submitted screenshot of previously-approved exact-script `=== SAFE C1A READ-ONLY PREFLIGHT SUMMARY ===`. **These are actual owner-observed Cloud Shell results**, not direct assistant API results, and no further command/build/CI/scan was repeated.

| Exact saved field | Screenshot result | What this actually establishes |
|---|---|---|
| `PROJECT` / `REGION` | `oldx-staging` / `asia-south1` | Requested staging/region |
| `PROJECT_METADATA_QUERY` / `PROJECT_LIFECYCLE_STATE` | `OK` / `ACTIVE` | Staging project metadata accessible |
| `ACTIVE_OPERATOR_ACCOUNT_HINT` | `ya***@gmail.com` | Masked Google principal; exact principal NOT in report; do NOT expose private Gmail or assume all rights |
| `TESTER_ACCOUNT` | `UNSELECTED_BY_OWNER` | Invoker/tester identity unresolved |
| `NEW_GATEWAY_SERVICE_QUERY` | **`UNVERIFIED_OTHER_ERROR`** | **Hard STOP. Cannot decide service name available vs collision vs permission/API/config error** |
| `C1A_SERVICE_NAME_COLLISION` | `UNKNOWN_STOP` | No new service creation authorized |
| `NEW_RUNTIME_SA_QUERY` | `NOT_FOUND_REPORTED` | Exact new proposed SA not found *in this lookup*; not an unconditional absence proof |
| `PROPOSED_EXISTING_REGISTRY_QUERY` | `OK`, format `DOCKER`, location `asia-south1` | Historical exact `oldx-staging-images` registry confirmed existing; no image pushed |
| `PROJECT_BILLING_LINK_QUERY` | `OK`, `BILLING_ENABLED=True`, `BILLING_ACCOUNT_LINK_PRESENT=True` | Billing LINKED only, not current gross spend, balance, trial credit or a free/no-spend guarantee |
| `C1A_DIRECT_PROJECT_IAM_QUERY` | `OK`, 2 direct Owner binding members; 1 direct Editor member | Direct counts only; existing historical high privilege remains; exact effective inherited principal access remains **NOT PROVEN** |
| `ACTIVE_OPERATOR_DIRECT_PROJECT_ROLE_HINTS` | `roles/owner` | The active operator has a direct project owner role; **do not grant any new broad role or remove former owner** |
| Gross INR / SKU+tax | `UNVERIFIED` | Cost gate not cleared |
| Remote image digest | `NOT_PUBLISHED` | Current local Docker image ID is not a deployable registry manifest |
| 12 HIGH owner decision | `NOT_GRANTED` | Separate C1A-only risk decision remains open |
| Cloud writes / hosted calls | `NOT_AUTHORIZED` | No create/deploy/HTTP consent |
| `NO_CLOUD_MUTATIONS` | `TRUE` | Script source contains only read-only metadata/IAM calls; no changes reported |

Owner saved a small redacted summary at `/home/yasminparmar087/oldx-step05-c1a-readonly-20261124T140144Z.txt`. It did NOT preserve the gcloud stderr of the new service lookup because the script intentionally deletes private scratch logs, so **cause of `UNVERIFIED_OTHER_ERROR` UNKNOWN**. Neither a NOT_FOUND claim nor a permission failure may be invented. All other successful tests were already completed and MUST NOT be rerun. Source previous 84 offline cases, 12-CVE Grype, old A8 image and IAM audits all left untouched.

### NEXT ONE *TARGETED* read-only error clarification — not the whole preflight again

From existing `oldx-staging` **Google Cloud Shell**:

```bash
gcloud --quiet run services describe oldx-step05-gateway --project=oldx-staging --region=asia-south1 --format='value(metadata.name)' 2>&1
```

This retries ONLY the sole failed lookup, purposely requests **name only** to avoid printing potentially sensitive service details, and displays the exact Cloud SDK error to classify the earlier inconclusive result. It does not create, enable, deploy, grant IAM, or invoke HTTP. **Do not** attempt enabling APIs or changing roles if error suggests it. User should share the short command output; if any private account information appears in an error, redact before sharing. One repeat of the FAILED lookup for diagnostic clarity is distinct from repeating previously completed successful checks. No other GCP command needed now.

**Frozen current status:** `C1A_READONLY_PREFLIGHT=PARTIAL_PASS`; `C1A_NEW_SERVICE_COLLISION=UNKNOWN_STOP`; `C1A_SA=NOT_FOUND_REPORTED`; `ARTIFACT_REGISTRY=EXISTS_DOCKER_ASIA_SOUTH1`; `BILLING_LINK=TRUE_GROSS_INR_UNKNOWN`; `DIRECT_OPERATOR_ROLE=OWNER_EFFECTIVE_IAM_UNKNOWN`; `12_HIGH_CVE_RISK_ACCEPTANCE=NO`; `C1A_DEPLOYMENT=NOT_APPROVED`; `C1B/C2=NOT_APPROVED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — Exact service collision CLARIFIED: Cloud Run reports Cannot find service

Owner ran **ONLY** the formerly inconclusive exact target read-only lookup in their `oldx-staging` Cloud Shell (none of the other five successful preflight probes repeated):

```bash
gcloud --quiet run services describe oldx-step05-gateway --project=oldx-staging --region=asia-south1 --format='value(metadata.name)' 2>&1
```

**Exact actual CLI output:** `ERROR: (gcloud.run.services.describe) Cannot find service [oldx-step05-gateway]`. This resolves the earlier `NEW_GATEWAY_SERVICE_QUERY=UNVERIFIED_OTHER_ERROR` / `C1A_SERVICE_NAME_COLLISION=UNKNOWN_STOP` as a targeted **NOT_FOUND_REPORTED** for that exact service in this project and region *at that moment*. It does not imply the name cannot be taken later, that IAM eligibility is verified, or that creating the service is authorized. Before any future approved create, perform only a fresh **just-in-time** name collision precheck, not a repeat of entire preflight.

**Root cause of the original misclassification:** `scripts/step05-c1a-read-only-cloud-preflight.sh` matches `not found|NOT_FOUND|does not exist` in stderr, but Cloud SDK actually says **`Cannot find service`**. Updated only the read-only script's classifier regex to also recognize `cannot find service`, source-only commit `e3ea4fb517b2c4e7ecafee79c370c782943b8b73`. **No script re-run**, no additional gcloud calls, no service/image/SA created, no IAM/Billing/old backend touched, no cost/spend verification, and no old 84/Syft/Grype/A8 repeat.

### Current precise C1A gate ledger

- `PROJECT_ACTIVE=CONFIRMED_AT_PREFLIGHT`; `REGION=asia-south1`; `EXISTING_DOCKER_REGISTRY=CONFIRMED`; `BILLING_ACCOUNT_LINK=ENABLED`; `DIRECT_OPERATOR_ROLE_HINT=roles/owner`.
- `NEW_SERVICE_NAME=NOT_FOUND_REPORTED_TARGETED` (previous accidental `UNKNOWN_STOP` specifically resolved); `NEW_RUNTIME_SA_NAME=NOT_FOUND_REPORTED`; neither is a guaranteed future vacant name.
- `DIRECT_PROJECT_BINDINGS=2_OWNERS_1_EDITOR`; `EFFECTIVE_INVOCATION_AND_INHERITED_IAM=UNVERIFIED`; `EXACT_TESTER_IDENTITY=UNSELECTED`.
- `ACTUAL_GROSS_ACCOUNT_PROVIDER_SPEND_INR=UNVERIFIED`; `PRECISE_REGIONAL_TOTAL_COST_AND_TAX_INR=UNVERIFIED`; `APPROVED_NEW_GROSS_SPEND_LIMIT=NONE`.
- `LOCAL_IMAGE_BUILD/SYFT/GRYPE=COMPLETE_WITH_12_DISTINCT_HIGH_IDS`; `REMOTE_PUBLISHED_MANIFEST_DIGEST_AND_PUBLISHER_SIGNATURE=NOT_VERIFIED`; `C1A_OWNER_NEW_IMAGE_12_CVE_LIMITED_RISK=NOT_ACCEPTED`.
- `C1A_CLOUD_WRITES/DEPLOYMENT=NOT_AUTHORIZED`; `C1B/C2=NOT_AUTHORIZED`; `STEP05_HOSTED=BLOCKED`; `PRODUCTION=NO_GO`.

**Next non-repeat step:** finish source-only limited C1A owner risk/price/operator proposal using existing facts, then obtain explicit approval for any new cost/IAM validation or write actions. The service existence question itself is **CLOSED** for the 24 Nov 2026 read-only check; **DO NOT run it again now**.
