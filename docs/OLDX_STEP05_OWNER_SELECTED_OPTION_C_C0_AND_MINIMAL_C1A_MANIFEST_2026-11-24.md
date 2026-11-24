# OLDX Step 05 — OPTION C OWNER-SELECTED *PLANNING ONLY*; C0/C1A minimal no-repeat manifest

**Date:** 24 Nov 2026 IST. **Repository:** `yasminparmar087-ops/oldx-website` at `security-hardening-review`. **Starting remote HEAD reviewed:** `074e18f12b7562b28f85280d9608af9242f39e8b`.

## 1. Specific owner selection and its strict limits

Immediately after the assistant proposed: "શું આપણે Option C — અલગ Cloud Run Gatewayને આગળના આયોજન માટે પસંદ કરીએ? આ મંજૂરી માત્ર Architecture Planning માટે હશે; કોઈ નવી Service બનાવવા કે ખર્ચ કરવાની નહીં", the owner responded **"ha aa pramane aagal vadho"** (yes, proceed accordingly).

Therefore:
- `STEP05_GATEWAY_ARCHITECTURE=OPTION_C_CLOUD_RUN_GATEWAY_OWNER_SELECTED_FOR_PLANNING`.
- `STEP05_GATEWAY_C0_PLANNING=AUTHORIZED`.
- `STEP05_GATEWAY_C1A_RESOURCE_CREATION=NOT_APPROVED`.
- `STEP05_GATEWAY_C1B_OFF_HOSTED_PROBES=NOT_APPROVED`.
- `STEP05_GATEWAY_C2_KEYLESS_SIGNING_KMS_IAM_ENABLED_USER_TRAFFIC=NOT_APPROVED`.
- `STEP04_ADMIN=04/15_DONE_DECISION_ONLY`; `STEP04_ORIGINAL_TECHNICAL=UNMET`; `STEP05_SOURCE=INTEGRATED_OFFLINE_TEST_VERIFIED` (77 historical distinct PASS case receipts, NOT a single run); `STEP05_HOSTED=BLOCKED`; `PRODUCTION=NO_GO`.

**This owner selection is NOT permission to create a Cloud Run service, attach a service account, build/push an image, enable an API, create a KMS key or role, change IAM, fire any hosted request, modify Rules/Auth/Firestore, or spend money.** Any further consent must be narrowly scoped to the precise action below and independently recorded. No previous Step04 B1/R1/scan/A8 probe authorization is reusable.

## 2. Existing known facts reused — NOT rerun

| Field | Historical documented evidence (dated; NOT a fresh Cloud read) | Impact |
| --- | --- | --- |
| Staging GCP project | `oldx-staging`; previously observed project no. `38472235077` | Target candidate only; re-confirm project identity within newly approved change window |
| Prior DB geography | Firestore Native `(default)` documented in `asia-south1` | Select Mumbai as **proposed** gateway region to avoid unnecessary cross-region overhead |
| Existing Artifact Registry repository | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images` documented as existing | **Reuse**, do NOT create a duplicate repository |
| Existing private backend service | `oldx-owner-read` prior revision `00012-vib` remains private, default-OFF, 0%-main; original `00001-8kr` at 100%, `healthcheck`/`step3rc14` tags protected | C1A must not touch this service, tag, route or IAM |
| Existing legacy Vercel lead | `oldx-webs` related to former repo owner; linked current Vercel team has 0 projects/deployments, old named lookup404 | Already checked; NEVER repeat merely to choose Option C |
| Software | `functions/staging-marketplace/secure-product-pipeline.mjs` source-only default-OFF composition; no runnable approved new Gateway container/image | **New disabled host entrypoint + image review needed before C1A**; no source project packaged in this packet |

References: [existing owner-approved Step04 ledger](OLDX_STEP04_OWNER_APPROVED_DECISION_ONLY_CLOSEOUT_AND_STEP05_HANDOFF_2026-11-24.md), [historical Cloud Run staging gate](cloud-run-product-owner-read-staging-gate.md), [Step05 integrated receipt](OLDX_STEP05_SOURCE_ONLY_KICKOFF_AND_MINIMUM_OWNER_BUYER_SLICE_2026-11-24.md), and [Option C security/cost design](OLDX_STEP05_CLOUD_RUN_GATEWAY_OPTION_C_SOURCE_ONLY_CONSENT_DESIGN_2026-11-24.md). Historical evidence does not prove current deployed status, billing or IAM inheritance.

## 3. Two-phase minimal new-resource decision — optimize time, risk and cost

**C1A — first possible hosted trial is ONLY a PRIVATE default-OFF Gateway, no live backend calls.** Keep the first trial smaller than originally proposed:
- One new PRIVATE Cloud Run service, candidate name `oldx-step05-gateway` (**PROPOSED ONLY / does not exist**), project `oldx-staging`, region `asia-south1`.
- One **new dedicated attached managed service account**, candidate `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com` (**PROPOSED ONLY**), with no Firestore/Auth/Firebase data roles, no SA key, no KMS signer or `roles/run.invoker` grant on the existing Product service yet.
- Use existing `oldx-staging-images` Registry and upload at most **ONE newly reviewed source-pinned immutable image** only if newly authorized; do not rebuild or rescan old Step04 A8 image. The Gateway needs a minimal independent OFF-only Node 24 server/port entrypoint, rejecting all `/api/*` with 503; health is NOT proof of Firebase readiness or private backend access. Current integrated Step05 factories do not currently provide a deployed Gateway image; source packaging and exactly focused **new** smoke tests are required before any resource approval.
- Proposed Cloud Run shape: request-based billing; `min-instances=0`, `max-instances=1`, `concurrency=1`, ~1 vCPU, ~512 MiB; authenticated `run.invoker` on the new Gateway **only for an exact named authorized tester**; no `allUsers` or `allAuthenticatedUsers`. Prefer `ingress=internal` only if an *actual compatible private tester path* is demonstrated and costed; do NOT claim Cloud Shell is automatically internal. If using `ingress=all`+IAM as a fallback, acknowledge this is publicly network-reachable but NOT anonymously invokable, and seek explicit change-level review. NO public access at C1A.
- **No Cloud KMS key, key ring, IAMCredentials, WIF, Cloud Build resource, Cloud Armor, VPC connector, load balancer, new Registry repository, Firestore TTL, Image Media resource or extra DB at C1A.** Minimize surprise cost and avoid a dependency that is unnecessary while every Product endpoint is OFF.
- At most one initial creation/deploy after separate approval; config-only readback of just that new service and exactly defined cleanup. Optional **C1B hosted OFF-only checks** with a named private caller, `GET /healthz` and `POST /api/staging/marketplace/owner -> 503`, no Firebase/nonce data operations, at most 6 requests in 20 minutes with no automatic retry, require **a separate C1B approval**, a valid private request path and explicit rollback/cost.
- No changes whatsoever to old `oldx-owner-read` A8 revision, root traffic or legacy tags; no reuse of consumed B1/R1. No production origin/domain/DNS changes.

**C2 (later; separate owner approval):** only after C1A/C1B evidence and explicit request:
- Grant dedicated Gateway SA narrowly scoped **Cloud Run Invoker** on the verified private backend (effective inherited roles independently reviewed); obtain two distinct Google-signed audience-specific tokens (IAM/private backend and independent app attestation) from attached identity metadata. Cloud Run strips IAM token signature before forwarding; backend verifies independent full signed attestation. Pin exact service SA email and numeric subject.
- New Cloud KMS SOFTWARE asymmetric key ring/key/version only if source preflight selects KMS as managed request-proof signer: candidate **key ring `oldx-step05-signing`, key `request-proof-rs256`, algorithm `RSA_SIGN_PKCS1_2048_SHA256`** (**ALL PROPOSED ONLY**). Fixed approved version/kid mapping and immutable public-key pin; backend Google OAuth JWKS checks Google identity token ONLY, NOT request-intent KMS signature. Signer uses SHA-256 digest of canonical request-intent bytes. Grant Gateway narrow `cloudkms.cryptoKeyVersions.useToSign` (possibly `roles/cloudkms.signer`) scoped to one CryptoKey, never project Owner or Token Creator as shortcut. KMS IAM is commonly CryptoKey-level, so cryptographic version pinning must also be enforced in application and key lifecycle. No public-key viewer required at runtime if approved pinned public verification key is delivered through an immutable trusted config; else only exact public-key reading permission.
- The **platform ID-token fresh iat limitation** must be proven before enabling: existing source rejects Google ID tokens older than a default ~60s, while metadata tokens may be cached with longer lifetime. Do NOT fake timestamps, relax issuer/principal/audience signature checks or rely on a token exp value alone. Either ensure real short-lived fresh tokens within bound or source-review a strict per-request proof freshness split (separate 15s signed intent).
- The **Firestore replay nonce field is NOT TTL-compatible now:** `scripts/staging-marketplace-replay-nonce.mjs` writes **numeric** `expiresAtMs`; Firestore TTL policies need a **Timestamp field**. A fresh consent must choose a narrowly scoped `expiresAt` Timestamp strategy, ensure no collateral collection cleanup (existing `marketplaceRateLimits_v1` is shared), and review Firebase Admin write permissions, TTL/guarded exact-ID cleanup, cost, revocation and rollback. Do not authorize generic rate collection deletion.
- Original Step04 G2 15 severe CVE enabled-scope disposition, G4 effective IAM/default DB isolation, G8 all-provider gross spend, media/photo/product publication, exact synthetic fixtures and cleanup and rollback remain required before public guest/ENABLED sellers.

## 4. Proposed C1A resource / permission / cost consent manifest — NOT EXECUTABLE UNTIL FILLED

| Item | Proposed precise limit | Current evidence / gate |
| --- | --- | --- |
| Owner and operator | Yasmin Parmar approval; exact deployer identity required | `DEPLOYER_PRINCIPAL=[UNKNOWN]`; do not add any privilege to former Owner `paniruddhsinh` |
| Project | `oldx-staging`, historical no. `38472235077` | `PROJECT_CURRENT_IDENTITY=[NOT FRESHLY VERIFIED]` |
| Region | `asia-south1` (Mumbai) | `REGION_CURRENT_QUOTA_AND_PRICES=[UNVERIFIED]` |
| NEW service | `oldx-step05-gateway`, private, `enabled=false`, IAM required, min0/max1/concurrency1 | `NEW_SERVICE_EXISTS=[NOT CHECKED/NOT CREATED]`; ensure no collision under newly approved preflight |
| NEW dedicated SA | `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com` | `NEW_SA_EXISTS=[NOT CHECKED/NOT CREATED]`; no keys |
| Registry | Reuse `oldx-staging-images` | `GATEWAY_IMAGE_DIGEST=[NOT BUILT]`; image/source/SBOM/CVE review prerequisite |
| Gateway ingress | Prefer internal *if tester path actually feasible*; otherwise IAM-required all-ingress with explicit network-access review | `INGRESS_MODE/TEST_ORIGIN=[OWNER DECISION REQUIRED]` |
| Named invoker | only exact staging tester on NEW Gateway | `TESTER_PRINCIPAL=[UNKNOWN]`; avoid allUsers and inherited privileges claims |
| Outbound IAM/backend | **No Product backend grant/call in C1A** | Keeps A8 0%-main untouched |
| KMS/nonce/media | ZERO newly created/used in C1A | Deferred to separate C2 review |
| Finite trial | initial creation + 1 disabled deploy; C1B maximum 6 private checks/20m, only with separate C1B approval | `REQUEST_TRANSPORT/PREIMAGE/ROLLBACK=[UNVERIFIED]` |
| Money | Current monthly gross all-provider baseline, exact region prices, remaining free trial, OCI image storage, logs, request-based compute/egress, taxes, reporting lag and finite maximum incremental exposure | `GROSS_FORECAST_RUPEES=[UNVERIFIED]`, `MAX_APPROVED_NEW_SPEND_RUPEES=[NOT APPROVED]`. ₹1,000 is manual pre-paid STOP, ₹2,000 is NOT a hard cap |
| Protected baseline | existing `oldx-owner-read-00001-8kr=100%`, A8 `00012-vib=0%-main`, existing `healthcheck`/`step3rc14` tags | No routing/IAM/revision changes to old service |
| Cleanup | exact NEW gateway service and newly created standalone SA/image only with **owner-approved** exact identities/version preimages; no broad delete | `CLEANUP_APPROVED=[NO]`; leaving min0 stopped service still retains billable Registry storage and logging |

**Cost formula, not a quote:** incremental gross cost = new gateway request CPU+memory+count/egress + immutable image storage/build + logs + any API/monitoring overhead + regional tax/FX. C1A purposely has **zero KMS/nonce/Auth/Firestore expected calls**, provided there is no accidental backend request and the gateway remains OFF. Conservative caps/min0/max1 are **not** guaranteed currency stop controls. Require owner-reviewed live quote and rollback if the packet is later submitted for a spend authorization.

## 5. Source-only preflight acceptance before C1A can be offered as an executable approval

1. Add a new isolated, explicit default-OFF Cloud Run Gateway entrypoint and image/Node24 packaging source without editing existing A8 deployment. It must return `GET /healthz` 200 only for process health, `POST /api/*` 503 under OFF and never execute Product/auth/nonce/KMS/network code.
2. Use **NEW** focused tests only: wrong/missing config/PORT, disabled POST, unknown paths, fail-closed HTTP methods, body cap, prompt shutdown, no credential or server-source leaks. Do not rerun 77 historical offline tests, Docker/SLSA/Grype old A8, B1/R1, Vercel discovery or old IAM inventory. A *new image* later needs its own security scan and pinned digest; historical A8 scan cannot certify it.
3. Confirm proposed naming, same-region repository, gateway tester private invocation transport, exact operator, service-current-existence and current account budget **within a separately approved read-only/pre-deploy scope**; do not claim existing saved evidence equals fresh cloud proof.
4. Draft an actionable owner request with precisely those new resources, action count, maximum rupee exposure/time window, exact IAM bindings, immutable source/image IDs, finite C1B calls, and **new-resource-only guarded recovery**. Owner explicitly grants C1A first; C1B must be separate after C1A status.
5. Do **not** preselect/wire long-lived secret keys; do not enable KMS, Firebase Auth, Firestore/Rules or Product publication. Start with OFF-only code.

## 6. Official documentation consulted — current source design only

- [Cloud Run service-to-service IAM tokens](https://docs.cloud.google.com/run/docs/authenticating/service-to-service)
- [Cloud Run ingress semantics](https://docs.cloud.google.com/run/docs/securing/ingress) — internal traffic and IAM are distinct; Cloud Shell may not be internal
- [Cloud Run service identities](https://docs.cloud.google.com/run/docs/securing/service-identity)
- [Cloud KMS RSA asymmetric signatures](https://docs.cloud.google.com/kms/docs/create-validate-signatures)
- [Cloud KMS scoped roles/permissions](https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles)
- [Firestore TTL requires a Timestamp field](https://firebase.google.com/docs/firestore/ttl)
- [Cloud Run billing](https://cloud.google.com/run/pricing), [Cloud KMS pricing](https://cloud.google.com/kms/pricing)

## 7. Current next ONE action

**Continue SOURCE-ONLY:** implement the minimal isolated, disabled Cloud Run Gateway Node24 entrypoint/container and NEW focused OFF-only local tests, then save image build/security preflight checklist and exact results on the review branch. No live build/publish/deploy. This reduces the source gap before a separately proposed owner consent for C1A. All 77 prior focused cases and old provider audits remain consumed, never repeated.

**No new Google Cloud services, service accounts, keys, credentials, IAM roles, Cloud Run image/build, Firestore TTL, deployment, billing, paid calls, tests of historical cases or Vercel lookups were performed to prepare this packet.**


## 8. C0 source follow-through — OFF-only gateway server and new focused tests SAVED

After owner selection and resource manifest C0, prepared the following **NEW** source-only assets without touching the old A8 `product-read-server.mjs` or current deployed backend:

- `functions/staging-marketplace/cloud-run-gateway-off-server.mjs` — totally isolated Node core HTTP server; responds 200 to exact GET/HEAD `/health`/`/healthz` process-health only; responds `503 ENFORCEMENT_UNAVAILABLE` for `/api` and all `/api/*`, regardless of forged IAM/Firebase/attestation headers or request content; responds bounded 404/405 for other paths/methods; explicit no-store/no-credentials/no echo; constrained PORT/host; SIGTERM-safe draining. It does **NOT** import Firebase, auth, Cloud KMS, metadata server, Product gateway or any externally networked module. There is no activation flag to turn on Product.
- `tests/integration/step05-cloud-run-gateway-off.test.mjs` — **4 brand-new** loopback HTTP test groups: health-only, immutable API-503 despite forged headers, unknown path and leak-denial, invalid bind and graceful shutdown.
- `functions/staging-marketplace/Dockerfile.gateway-off` — NEW minimal Docker source recipe requiring an externally supplied **immutable Node24 distroless base digest** via `NODE24_BASE_BY_DIGEST` with no default; copies ONLY the OFF server source as `/app/server.mjs` and inherits node entrypoint. This is deliberately **unbuildable as supplied without a newly reviewed exact base digest**. A Dockerfile is not a deployed or scanned image.

**Actual local NEW verification:** Node `v22.16.0` (not target Node24); executed `node --test tests/integration/step05-cloud-run-gateway-off.test.mjs` from a temporary folder mirroring exact new repo paths: **4 NEW PASS / 0 FAIL / 0 SKIP**. An earlier first run of the same new file under a temporary import path also passed 4/4; the final repo-path run is the counted verification. The new uploaded server and test files match the locally tested file byte counts **2626/3065 bytes**; no GitHub Actions workflow, Docker, Cloud Build or remote Node24 acceptance ran. Previous **77 distinct recorded offline cases NOT rerun**; current **81 distinct focused offline PASS case receipts in aggregate**, not one 81-case suite. The temporary work folder is not a production deployment.

**Important C1A prerequisites still BLOCKED:** immutable base `linux/amd64` digest, fresh security/build/source provenance and image manifest digest, actual private tester route, current region/quotas/spend, resource name collision check, explicit C1A permissions and new-resource-only cleanup. **No OCI image was built or pushed**, no Dockerfile SOURCE receipt suffices for C1A consent. C1A OFF-only version intentionally needs **NO KMS, backend IAM invocation grant, Firebase or Firestore/nonce operations**. Separate C1B only permits at most 6 hosted OFF-only checks after approval; C2 remains distinct enabled-auth scenario.

**One next source-only action:** complete a precise container-image build/review **proposal** with immutable base digest selection and owner-scoped private C1A spend/operator approval packet; do not build/push/create Cloud resources until the new action is separately approved. `OPTION_C_PLANNING_SELECTED=true` but `C1A_APPROVAL=false`, `C1B_APPROVAL=false`, `C2_APPROVAL=false`, `STEP05_HOSTED=BLOCKED`, `PRODUCTION=NO_GO`.


## 24 Nov 2026 — C1A packaging finalized in SOURCE; resource consent still BLOCKED

**Start:** `2309d6a819ce164fb337ed9a997c8809e2c781fe`. **Verified packaging/source commit:** [`88fd08dca9e09de336c3f31b1ebbf26c563b0040`](https://github.com/yasminparmar087-ops/oldx-website/commit/88fd08dca9e09de336c3f31b1ebbf26c563b0040); following docs commit saves this update and final HEAD is in GitHub history/report. No C1A/C1B/C2 consent inferred.

### 9. Exact immutable base candidate and evidence classification
Official [Google Distroless image catalog](https://github.com/GoogleContainerTools/distroless/blob/main/README.md) lists Node24 Debian13/nonroot/amd64. Public registry read 24-Nov-2026, no layer pulls:
- Tag queried ONCE successfully: `gcr.io/distroless/nodejs24-debian13:nonroot`.
- Returned OCI index `sha256:39b0407357c9fadf1a9708d22088f02de21f0e1e8a688474eea2d8701e7d5693`.
- Unique linux/amd64 child `sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec`.
- Config `sha256:547351d91ab0a68f850b2ae32ca2ef0531d8a3a956ac0793d5cb2fbff4fde563`: linux/amd64, User65532, Entrypoint ["/nodejs/bin/node"], no CMD. Manifest lists22 layers totaling55,495,051 compressed bytes; NOT measured derived/uncompressed/build-peak size.
- Exact SHA256 recomputed over raw INDEX, CHILD MANIFEST and CONFIG bytes and matched their content-addressed references; platform/config verified via official HTTPS registry metadata. Initial sandbox connection refused; approved metadata-only retry succeeded. Tag not repeatedly polled; subsequent reads were pinned index/child/config only, FOUR successful small metadata GETs, ZERO filesystem layers/builds/pushes.
- Publisher Cosign/signature transparency proof NOT VERIFIED. Node24 exact patch-level/runtime execution NOT VERIFIED. No base/derived SBOM/CVE elimination claim. Official immutable metadata candidate is not a completed Gateway image.

### 10. Actual minimal packaging correction and tests
`functions/staging-marketplace/Dockerfile.gateway-off` now has ONE literal FROM with fixed linux/amd64 CHILD digest; no mutable tag fallback, ARG default/missing-input/override, builder, RUN, npm or shell. Explicit nonroot65532:65532, readonly0444 single-source COPY, exec Node ENTRYPOINT/CMD and SIGTERM. Removed no-default ARG draft: required digest is now literal source; missing/changed pin is rejected by packaging check rather than silently accepting an operator's arbitrary base argument.
NEW `Dockerfile.gateway-off.dockerignore` denies everything except required directories and ONE OFF-server file. Dockerfile/ignore metadata may be sent by Docker itself, but no application dependencies, Git, .env, credentials, Firebase/config or other source can be copied. Existing OFF server code unchanged: only Node core, no provider client or Product activation path. C1A must use repository-root context and this exact Dockerfile-specific ignore.

NEW `tests/integration/step05-gateway-off-packaging.test.mjs`, Node **v26.13.0**:
- `node --test --test-isolation=none tests/integration/step05-gateway-off-packaging.test.mjs`: **2 PASS/1 FAIL**, failure **spawn EPERM from sandbox**, not an app assertion.
- Approved local-only retry of ONLY failed case: `node --test --test-isolation=none --test-name-pattern="packaged exec entrypoint" tests/integration/step05-gateway-off-packaging.test.mjs`: **1 PASS/0 FAIL**.
- THREE NEW distinct cases verified in aggregate; initial full invocation was NOT green. Exact digest/COPY/context/user/entrypoint/SIGTERM source checks; real subprocess starts despite hostile Product/ADC/publication env+nonexistent credential-path fixture, health200, API503 despite forged headers, no stdout/stderr leakage, process termination observed. Windows process.kill may terminate directly; this is NOT POSIX handler/LinuxPID1/container SIGTERM proof. No test credential file created.
- Historical81 NOT replayed. 84 cumulative recorded offline groups, NOT one84-case run. Docker and Podman both NOT FOUND; no toolchain installed or disk/build experiment attempted. No new or old image built/pulled/scanned. Linux Node24 container smoke, full-image security evidence, publisher signature/provenance and distinct DERIVED Gateway digest remain REQUIRED before deployment.

### 11. Precise C1A specification — frozen proposal, NOT executable/approved
Target proposed names remain oldx-staging / asia-south1 / NEW oldx-step05-gateway / NEW oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com. Reuse historical existing repository oldx-staging-images; do not create a registry, duplicate SA/service or API/service-agent automatically. Check collisions in separately approved preflight; proposals are NOT existence evidence.

| Field | Required future C1A value / STOP gate |
|---|---|
| Owner/operator | Yasmin owner consent; deployer Google principal **[UNFILLED]**, current existing entitlements reviewed; no former-Owner privilege changes |
| Exact image | **[UNBUILT DERIVED GATEWAY DIGEST]**, source 88fd08dca9e09de336c3f31b1ebbf26c563b0040, exact recipe/context above. STOP if digest is BASE index/child/config or old A8, mutable tag, no independent new-image security/provenance review |
| Resources | Request-based billing/CPU throttling; 1vCPU,512MiB, min0/max1, concurrency1, request timeout5s, CPU startup boost OFF, no GPU/volumes/secrets/extra containers; bind PORT8080; default platform TCP startup check only, no new HTTP probes/schedules/monitors in C1A |
| Entrypoint/env | Inherit exact reviewed exec image command; no override. No Product activation variable, NODE_OPTIONS/NODE_PATH/LD_PRELOAD/LD_LIBRARY_PATH, file-backed credentials/proxy/SDK env. Only NODE_ENV production and platform PORT/K_* metadata; no dotenv injection |
| IAM-required ingress | Require platform authentication; invoker check MUST NOT be disabled. No allUsers/allAuthenticatedUsers. Attached SA has NO Auth/Firestore/KMS/backend-Invoker roles for OFF scope |
| Network/tester | **Proposal for direct external authorized tester: ingress=all + mandatory IAM**, network reachable but not anonymously invokable. Needs explicit owner acceptance. Internal-only alternative remains BLOCKED without proven existing VPC-compatible path; no new VPC/LB/Cloud Shell assumption |
| Caller | Tester Google principal **[UNFILLED]**, exact named roles/run.invoker on NEW Gateway only; no project-wide role shortcut. Historic2Owners+1Editor inheritance means direct tester binding alone does NOT prove exclusivity |
| Protected resources | NO oldx-owner-read IAM/env/revision/tag/traffic changes. old root00001-8kr=100%, A8 00012-vib=0%-main, healthcheck/step3rc14 preserved. No backend invocation or publication |
| Retention | Proposed new service <=24h pending separate guarded cleanup approval; min0 is not deletion/storage stop. One image retained <=7days unless owner specifies required rollback evidence; manifests/reports in existing owner-controlled private storage, no new bucket |
| Money | Gross baseline/INR currency/FX/tax/free-tier remainder and hard incremental rupee consent **[UNFILLED]**. Manual₹1,000 STOP/review and non-hard₹2,000 goal unchanged |
| Finite C1A writes | At most1SA create,1new reviewed image upload (only if separately included),1service creation/OFF deploy,1service IAM policy update for exact tester; bounded metadata readbacks of those NEW resources only, no hosted HTTP calls |
| STOP | Any existing-name collision, wrong account/project, missing API/service-agent or unexpected inherited permission, unknown image/security status, drift in protected backend, unspecified spend/cleanup, unexpected privilege/activation/extra resource, write/timeout ambiguous outcome =>STOP/no retry/no overwrite |

**Exact IAM actions, all future/unapproved:** operator needs only required current permissions for run.services.create/update/get/delete and set/getIamPolicy on the NEW service; iam.serviceAccounts.create/get/delete on NEW SA, iam.serviceAccounts.actAs for attaching it. If actAs is missing, proposed roles/iam.serviceAccountUser binding to exact operator on NEW SA only must be separately included/consented; do not auto-grant project roles. Reuse existing authorized AR upload access; if absent STOP for exact repository permission decision, no blind writer grant. Attached SA gets no application project roles. Grant only roles/run.invoker to exact tester on NEW Gateway; inspect effective inherited grants without changing existing Owners/Editor. Any required API enablement, service-agent creation or extra registry/permission action is outside this packet and STOP.

**Pre-deploy order:** receive exact signed action consent with all blanks filled -> verify account/project/name collision/current allowed budget and protected preimage -> validate source SHA + derived digest/scan/provenance and strictOFF recipe/config -> perform only approved finite C1A writes -> inspect exact new SA/service/image/settings/IAM, preserve evidence ->STOP. No C1B auto-probe and no to-latest/broad cleanup.

**Recovery/cleanup:** never overwrite/delete a pre-existing service/SA/image. Record newly created resource UIDs/etag/revision/image digest and operator manifest; only those exact new resources may be removed under explicit exact-ID cleanup consent. Verify no unexpected dependency before SA/image deletion; no repository deletion, broad prune or old-backend rollback command. On uncertain partial create, freeze/read back only approved scope; no automatic repeated write. No cleanup authorization given here.

### 12. Public-rate worksheet — reference prices, NOT current account quote
Public official pages consulted24-Nov-2026; no Billing/project read. Rates below are public USD examples, **Mumbai/account-currency SKU selection and INR/tax remain unverified**:
- [Cloud Run pricing](https://cloud.google.com/run/pricing): displayed request-billed active CPU0.000024USD/vCPU-s, memory0.0000025USD/GiB-s, requests0.40USD/million; startup/shutdown also billable. Free tier shared/account-dependent, not assumed. Illustrative1instance x1200active seconds x(1CPU+0.5GiB)+6requests = **0.0303024USD compute/request component only**, excluding startup/shutdown beyond window, transient extra instances and every noncompute charge. max1/min0/time window is NOT a guaranteed cost ceiling.
- [Artifact Registry pricing](https://cloud.google.com/artifact-registry/pricing): listed0.000136986USD/GiB-hour above shared0.5GiB-month allowance (roughly0.10USD/GiB-month). Compute actual S_GiB x H_hours x rate; illustrative0.1GiB x168h =0.0023013648USD before allowance. Derived retained size is unknown; compressed base bytes are NOT registry total/account usage. Same-location transfer listed free; cross-location/internet egress separate.
- [Cloud Build pricing](https://cloud.google.com/build/pricing): public e2-standard-2 reference0.006USD/minute; hypothetical10minutes0.06USD, NOT approved, provisioned or consumed. No Docker/Podman locally; build execution/provider choice remains BLOCKED. Do not assume promotional free minutes available or activate a paid default pool under C1A.
- [Cloud Logging pricing](https://cloud.google.com/products/observability/pricing):0.50USD/GiB ingestion/storage incl first30days, first50GiB/project/month allowance subject existing usage. Budget L_GiB x0.50USD plus extended retention/export/custom metrics if proposed; no sinks/monitors added.
- Network/egress = actual destinationGB x official route/SKU rate; no VPC/LB proposed, no guessed flat cost. Tax, INR SKU/FX, gross existing spend, Registry storage/scan, build and retention remain **[UNFILLED]**. C1A OFF code intentionally makes ZERO Auth/Firestore/KMS/backend calls; platform billing/logging/storage do not become zero.

### 13. Three separate consent decisions — never a blanket approval
**C1A remains BLOCKED** until new Gateway derived image/provenance/security/runtime evidence, exact deployer/tester/ingress choice and current gross forecast+incremental money/cleanup consent are filled. This packet is source-ready for REVIEW only; not executable deployment authority.

**C1B — separately approved AFTER C1A:** exact new service URL/audience/tester/private-token method from C1A evidence, max6 calls within20min, no automatic retry: authenticated GET/HEAD health200 and authenticated Product POST503, unauthenticated/unauthorized denial. Exact schedule must fit six, e.g. two health calls, two OFF API calls, two denied calls. No nonce/user/Product/Firestore writes. No token mint/HTTP under this task. Clean ONLY new resources within already separately approved recovery scope; keep reports private/no tokens.

**C2 NOT AUTHORIZED:** KMS signer, real Google identity freshness, effective IAM/default DB, original15 severe CVEs' enabled-scope risk, Firestore Timestamp TTL strategy, media/photo/publication, actual seller/buyer acceptance and gross costs/rollback remain BLOCKED. C1A/C1B OFF results cannot certify them.

**Next ONE owner action:** review and authorize a separately bounded NEW Gateway build/security-evidence task on a suitable existing builder, with explicit no-deployment/no-old-image scope and any provider/cost limit filled first. No large toolchain install, Cloud Build or image push is implicitly authorized by this source task.


## 24 Nov 2026 — Owner approved ONE **FREE LOCAL** NEW-Gateway image evidence attempt, NOT deployment

Following the latest source-only packaging result at final HEAD `e74082d7a216550a54cebfc61ead8ea931966459`, the assistant offered **one limited cost-free NEW OFF Gateway local build, SBOM/security scan and Linux Node24 OFF-only smoke without Cloud/Registry push/deploy/IAM/spend**. The owner expressly replied **"ha manjuri chhe"**. This is ONE approved local build/evidence attempt, not blanket rescan/retry, old A8 B1/R1, paid service or C1A/C1B deployment approval.

**Tool availability:** Current assistant-side Linux runtime has ~30 GB free scratch but NO Docker/Podman/Buildah daemon or other builder, and public `gcr.io` DNS/network is blocked. Therefore an actual image cannot be built/scanned *in the present assistant runtime*. GitHub repo is PUBLIC; the official standard GitHub-hosted Linux runner would be free, but committing a new automatic workflow would also trigger the old unconditional `oldx-review-safety.yml` workflow and repeat historical safety checks. Respect owner's strict no-repeat instruction. No workflow/CI run was triggered. No attempt to use paid Google Cloud Build, create an IAM identity or push an image.

**Actionable safe alternative (existing owner's free Cloud Shell Docker if already available):** [one-shot local script](../scripts/step05-gateway-off-local-one-shot.sh), guarded with exact Git blob hashes of the THREE new Gateway input files and review branch/source, local daemon availability, Linux AMD64, >=4 GiB scratch and a persistent one-attempt marker set immediately before first Docker build. Script builds **ONLY** the new Gateway image locally with immutable reviewed Node24 base, never pushes/deploys; inspects Linux/amd64 and nonroot65532, runs a standalone read-only/network-none process test, checks Node24/readonly source, launches only the NEW OFF Gateway with network none, uses bounded local in-container health200 / Product503 and SIGTERM0 checks. Separately downloads pinned SHA256-checked official **Syft v1.57.1** and **Grype v0.121.3**, creates one CycloneDX SBOM and one Grype JSON scan of the newly derived image, reports distinct HIGH/CRITICAL CVE IDs and SHA256 of evidence reports. All generated image containers are removed by exact ID/tag and temp scanner binary/data cleaned on exit; the small report directory is retained under owner's Cloud Shell HOME. No secrets, cloud token, Firebase, new API, Registry upload, KMS or billed operation.

**Full upstream asset checksums independently read from official GitHub release metadata:**
- Syft Linux AMD64 v1.57.1 archive: `bf52519eb57f675d47c07d43213cb6dff6449f3d6d1147ff6701ed91f44eef0c`.
- Grype Linux AMD64 v0.121.3 archive: `e9da18cc1429e786722e32161288103600efffd8e483c90761f90485bd1bec85`.
- Both are public release downloads. No curl-pipe-to-shell or executable fetched without checksum.
- Local script content created, reviewed, and a corresponding local draft's Bash syntax was checked; **this does NOT constitute image BUILD/SBOM/SCAN PASS**, nor Linux Node24 hosted test. Only the new script was authored, with bounded readiness correction before user execution. Do not add these as NEW test cases to cumulative 84.

**Owner execution:** from Cloud Shell using a **fresh temporary public repo clone**, never overwrite owner's current working tree. Use one combined command:

```bash
d=$(mktemp -d /tmp/oldx-step05-build.XXXXXX) && git clone --quiet --depth 1 --single-branch --branch security-hardening-review https://github.com/yasminparmar087-ops/oldx-website.git "$d" && cd "$d" && bash scripts/step05-gateway-off-local-one-shot.sh
```

Run ONLY after checking that free Cloud Shell has a working local Docker daemon and adequate disk; the script itself refuses otherwise and never falls back to paid infra. It creates a single persisted `$HOME/.oldx-step05-new-gateway-image-build-consumed` marker **once**, and should not be repeated automatically after any failure. Share only `summary.txt` and compact failure/error from `build.log` if necessary; never send credentials. Scan results with severe CVEs mean HOLD for enabled usage, NOT automatic GO. Image ID is local Docker IMAGE ID, not an immutable pushed registry digest or publisher signature.

**CURRENT STATUS:** `OPTION_C_C0=OWNER_SELECTED`; `NEW_IMAGE_BUILD_AUTH=ONE_FREE_LOCAL_ATTEMPT_APPROVED_NOT_YET_EXECUTED`; `NEW_DERIVED_IMAGE_BUILD/SBOM/GRYPE/LINUX_SMOKE=NOT_EXECUTED`; `OLD84_TESTS=UNCHANGED_NOT_RERUN`; `C1A/C1B/C2_DEPLOY=NOT_AUTHORIZED`; `PRODUCTION=NO_GO`. Once execution result is obtained, record exact measured derived image evidence and build/sbom/scan findings in this manifest, then separately prepare finite C1A operator/tester/cost/deployment consent. Keep original Step04 G2/G4/G8 gates.

**No current-user Cloud Shell was accessed, and no actual Docker build, registry download, SBOM or Grype scan was executed by the assistant in this runtime.** Any assistant-created build script alone is not sufficient to call C1A ready.
