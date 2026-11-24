# OLDX Step 05 C2 — source-only enabled Product seller/buyer gap closure and finite pilot decision packet

## Latest verified C2-S1 source-only implementation checkpoint

Starting remote HEAD: `fbf7a5ea36eb99607b3999b26273e66e1bc1ff51`. Verified source commit: `e9a36ecede4c05e8bcd2cf2deabf99bdebb2d887` on `security-hardening-review`; documentation follows in its child commit (final branch SHA in Git history / Issue #17). This checkpoint supersedes older “C2-S1 not yet implemented” / “C1A not deployed” status below; historical evidence is preserved.

**C2-S1 = COMPLETE_SOURCE_CONTRACT_OFFLINE_VERIFIED. C2 hosted = BLOCKED; Step05 NOT DONE; production NO-GO.** No existing live route, deployment configuration, feature flag or resource was enabled.

New source:
- `functions/staging-marketplace/c2-website-mediation.mjs`: inactive, explicit default-OFF website/private-Gateway factories reuse existing Marketplace Gateway, Step05 Gateway/backend contracts and real RS256 Google identity verification. Separate browser Firebase Authorization, private-Gateway IAM credential, signed website identity, Gateway-to-backend identity and signed request intent. Stripped IAM headers are presence-only, never independent identity proof. Mandatory trusted guest admission; strict origins/routes/header filtering; identity expiry rechecked immediately before final dispatch; bounded deadlines and conservative same-request recovery.
- `scripts/c2-synthetic-cleanup-manifest.mjs`: default-OFF, descriptor-safe bounded DRAFT_ONLY manifest; synthetic run/actor/path/version guards. It executes no reads/deletes and excludes shared generation, nonce/rate, owner registry and infrastructure paths. A submitted manifest does not prove live ownership/version.
- `tests/integration/step05-c2-mediation.test.mjs`: seven distinct NEW offline groups, real ephemeral RSA signatures and existing backend pipeline with in-memory test doubles. No live credentials or hosted requests.

Actual verification (Node v26.13.0, isolated temporary source snapshot):
1. `node --test --test-isolation=none tests/integration/step05-c2-mediation.test.mjs` — initial six NEW groups: 6 PASS, 0 FAIL, 0 skipped.
2. After final expiry guards and a seventh group: `node --test --test-isolation=none --test-name-pattern="new website/private|website identity expiring" tests/integration/step05-c2-mediation.test.mjs` — 2 PASS, 0 FAIL.
3. After descriptor-safe cleanup validation: `node --test --test-isolation=none --test-name-pattern="synthetic cleanup plan" tests/integration/step05-c2-mediation.test.mjs` — 1 PASS, 0 FAIL.
These receipts cover **7 distinct new groups**, with targeted reruns of changed cases, NOT nine distinct tests or a claimed final seven-group single invocation. Historical suites were not rerun. Source blob SHAs: mediation `258707d4590de54c27f40a9a350e5aadc891a032`; cleanup `0801050987f224bff2a6c82702fef961658f74a7`; test `da5d05b9eb47e5665fa98bf64b51c3bfb0fca817`.

| Gate | Source result | Remaining genuine hosted requirement |
| --- | --- | --- |
| G1 | Website mediation and guest admission contracts implemented/offline verified | Actual website endpoint/mediator principal, private ingress IAM and trusted bounded guest provider not provisioned/bound; anonymous direct Gateway remains unavailable |
| G2 | Real RS256 identity and separate IAM/Firebase/assertion/intent boundaries reused and integrated | Actual credential/signing/key-version providers and audiences/principals require reviewed host binding; website identity is a short-lived bearer, not a one-use nonce. Final Gateway-to-backend nonce proof does not eliminate first-hop bearer replay |
| G3 | Existing project/default-database, Firebase revocation and ownership contracts reused unchanged | Actual least-privilege runtime SA/default-database data-plane acceptance unavailable |
| G4 | Existing publication/media gates preserved OFF | Publication/media policy and enabled acceptance remain BLOCKED |
| G5 | Synthetic cleanup draft validation implemented; shared paths excluded | Numeric nonce expiry is not Firestore TTL. Exact run-owned nonce cleanup/Timestamp TTL policy and fresh ownership/version/dependency readback are unresolved; no deletion authorized |
| G6 | Existing evidence and rollback separation preserved | Gateway 12 HIGH are OFF-only disposition; A8 15 severe are a separate set, not 27 distinct. Enabled security disposition, effective inherited IAM and hosted rollback acceptance remain BLOCKED |

C1A and C1B are **CONSUMED / PASS_WITH_LIMITS**, not permission to repeat: Gateway revision `oldx-step05-gateway-00001-thd`, service UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`, SA UID `102194769236111252832`, derived digest `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`. C1B used four hosted calls: anonymous /healthz404 (reserved-z caveat), anonymous /health403, Owner /health200, Owner Product POST503; limited 4/6 evidence only. This source task made NONE of those calls. Original backend root revision/100% and A8 revision/0% plus old tags remain protected; no Cloud reread/change made.

**One next owner action:** decide the existing C1A supervised <=24h trial disposition (recorded window approximately 24 Nov 23:19–25 Nov 23:19 IST): separately authorize exact NEW-only guarded cleanup, or explicitly bounded limited retention. No automatic deletion, extension or background monitoring is implied. No C2 live activation permission follows.

Cost: no new cloud/paid/API/build/scan/CI action in this batch; repository/source tooling only, with no claim about the existing trial's ongoing charges. No new INR hard cap or recurring billing form is imposed. Future paid or live actions still need separate specific authorization. No Cloud/IAM/Firebase/Billing/credential changes, image operations, old tests, C1A/B replay, Step04 work or deployment occurred. Local dirty Handoff and untracked .firebaserc were preserved; this remote update uses latest branch parent without force.


**Date:** 24 November 2026 IST. **Repository:** `yasminparmar087-ops/oldx-website`; **branch:** `security-hardening-review`. **Authority:** owner said “ok aagal vadho” after actual C1A and C1B new private default-OFF Gateway were confirmed `PASS_WITH_LIMITS`. This authorizes **continuing source-only C2 planning/review and reversible code preparation within earlier Step05 branch/source scope**, NOT Cloud Run deployment, enabled Product, Firebase/Firestore/KMS/signing-key/IAM/Rules/Billing changes, data creation, hosted HTTP or production.

## 0. Current verified exit — freeze, NEVER repeat

- **C1A infrastructure PASS_WITH_LIMITS:** one new no-role SA `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com`, uniqueId `102194769236111252832`; one already-built WSL Gateway image upload to existing `asia-south1` Artifact Registry, independent remote digest `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`; one PRIVATE default-OFF Cloud Run `oldx-step05-gateway` UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`, revision `oldx-step05-gateway-00001-thd`; effective current revision max 1, min 0, 1CPU/512MiB/concurrency1/5s, direct service IAM no public binding, inherited two Owner/one Editor historical potential access, IAM check enabled. Current image **12 HIGH distinct CVE IDs**, owner-accepted limited OFF-only; derived image `slsa_build_level: unknown`; original Distroless parent signature only.
- **C1B hosted OFF-only PASS_WITH_LIMITS:** 4 total calls under original 6/20min owner approval, #1 anonymous `GET /healthz` 404 (Google Cloud Run reserved suffix path possible), #2 anonymous `GET /health` 403, #3 Owner-authenticated `GET /health` 200, #4 Owner-authenticated `POST /api/staging/marketplace/owner` 503. `NO_CLOUD_WRITE=TRUE`. Existing C1B one-shot markers and receipts are consumed. `/healthz` HTTP404 by itself is NOT a security bypass or adequate identity test.
- **Step04 administrative exit Option B DONE**, original technical exit NOT MET: A8 private 0%-main hosted OFF503/effective Invoker/default-DB IAM/enabled-scope severe CVEs and full rollback remain separate carried gates. Historic **A8 15 severe CVE IDs**, separate from new Gateway's **12 HIGH IDs**; **do not add as 27 distinct without de-duplication**.
- **NO REPEATS**: prior 84+ focused Node receipts and later 77 offline integrated groups, old A8 B1/R1, C1A B1/B2/B3, C1B tokenized requests, WSL image build/Syft/Grype, Cosign, historic IAM/G4/(default) DB/billing inventory, automatic CI. Do not alter `oldx-owner-read` root 100%/tags, existing IAM, Firestore Rules or production. This document records decisions, **not additional tests**.

Canonical consumed proof: [C1A/B three-write and hosted test ledger](OLDX_STEP05_C1A_STAGE_B_THREE_WRITE_EXECUTION_LEDGER_2026-11-24.md); [Step05 original source integration and actual offline receipts](OLDX_STEP05_SOURCE_ONLY_KICKOFF_AND_MINIMUM_OWNER_BUYER_SLICE_2026-11-24.md); [master 15-step plan](OLDX_SINGLE_EXECUTION_PLAN_2026-11-13.md).

## 1. C2 objective — not a second OFF-only health check

The original master Step05 exit is a **genuine hosted Product owner/buyer thin vertical slice**: authenticated owner draft save/read/edit, permitted publish and withdrawal/archive, buyer guest list/detail (with safe public projection), owner/unauthorized denial, rate quota, idempotent retry after lost response, and **exact synthetic cleanup plus independently inspected rollback**. New C1B authenticated 200+API503 only proves PRIVATE OFF behaviour; it **does NOT** show any one Product data write, publication, buyer list or controlled deletion.

### Actual current code gates (GitHub on this branch)

| Existing source and blob | What is already in source | What it does NOT yet prove |
|---|---|---|
| `functions/staging-marketplace/cloud-run-gateway-off-server.mjs` / `25d2679bd4ea970c8b8a32a778fb26eb347bcdd6` | Deployed isolated OFF Node HTTP entrypoint; `/health` 200 and `/api/*` unconditional 503; no Firebase/imported app | Cannot enable owner/buyer traffic by setting a flag. C2 needs a separately reviewed composition, new build/risk approval and one authorized deploy |
| `functions/staging-marketplace/product-read-server.mjs` / `135e43d064c479a59a6f4b91a001c2bae9fb83f4` | Existing A8 limited `/owner` POST + health and fail-closed `createStagingAdminInitializer`; ADC project/service-account/default DB guards | No hosted save/archive/list/detail/publish/withdraw on this deployed path; no write/publish buyer end-to-end |
| `functions/staging-marketplace/cloud-run-http.mjs` / `cdd26ddc2dae0142baad5aa26c59d7fbd4393c13` | Inactive injection-only Node listener for `save/owner/archive/list/detail` exact paths, 503 default, bounded responses | Not a built/live Cloud Run entrypoint; no Admin/identity/signing/provider wiring |
| `functions/staging-marketplace/secure-product-pipeline.mjs` / `fa5a317803bdb67a6f6ffc4cf27dd7ee5bd7aecd` | Default-OFF trusted cryptographic Gateway and backend factories with Google identity vs distinct request-signing key, nonce/guest quota/cursor, existing Product runtimes | No real host listener, approved signer/provider, live Google identity proof, real shared Firestore concurrency, owner/buyer hosted flow. **Source explicitly passes `publicationEnabled:false`** in `createStep05Backend` |
| `functions/staging-marketplace/trusted-host.mjs` / `91489991d593169e939071ebf07b0169bf3d6ef9` and `scripts/marketplace-proof-bound-hop.mjs` / `464a4348095e15885909dbf555135afdc503dda2` | Distinct browser, Cloud Run IAM attestation, request intent signatures and backend verification; bounded, fail-closed | Real provider/KMS key and exact allowed browser origin/backend origin/audience must be chosen; browser cannot mint Google service-account Invoker identity by default |
| `features/marketplace/http-transport.mjs` / `4d928d604ee0be97682fa6bc06c6cac6ab85be8d` | Default-OFF HTTPS injected `POST` transport, Firebase bearer for private commands, bounded guest body/response, no automatic retry | Does not mint/store Cloud Run Invoker tokens and therefore **cannot reach current private IAM-required C1A Gateway directly from normal anonymous buyer browser** |
| `functions/staging-marketplace/public-runtime.mjs` / `493a6cd835f06da7f2878632e5fe79da7b3cec77` | Default-OFF separate public list/detail runtime with host-injected trusted guest quota and cursor/key; no commands | Does not establish public endpoint exposure, trust policy, production anti-abuse or native real-Firestore behaviour |
| `functions/staging-marketplace/runtime.mjs` / `749f4259068c4d9dd2f46706222c7a43ba47fb59`; `bootstrap.mjs` / `87feb6ff40e5e67c4c06638ba7906dfc71bd8a9f` | Existing authenticated command pipeline/quota/transactions with disabled defaults; bootstrap requires staged environment and refuses publication-enabled for real deployment | Publication remains OFF; direct client Firebase Rules are not a replacement for Admin IAM/data restrictions |
| `scripts/staging-marketplace-replay-nonce.mjs` / `2ddfa92659ddec5e9e18a7cfdfab3e76435f9756` | Native-shaped atomic Firestore replay consumer, nonce document with numeric `expiresAtMs` and explicit retention bound | No real TTL policy/automatic cleanup: Firestore TTL requires configured timestamp/date-time field and policy; numeric field alone does not expire/delete docs |

**Source verification classification:** all rows are GitHub source facts, NOT fresh Node24 run, cloud IAM/Firestore read or newly executed test. Existing focused offline integration tests reported in the source kickoff are retained, no repetition.

## 2. Six C2 blockers — close in order without duplicate work

| Gate | Exact missing evidence/decision | Smallest safe next action | Status |
|---|---|---|---|
| C2-G1 buyer-facing entry and dual auth | Current Cloud Run Gateway is IAM-private and 403s anonymous; guest buyer/browser cannot directly invoke it. Choose narrowly trusted website/server-to-server mediation **or** a separately reviewed public read-only surface with quotas/CORS/abuse controls, not implicit `allUsers` on this Gateway | Document exact origin/service-to-service principal and buyer transport boundary; source-only interface; **keep current private Gateway unchanged** | BLOCKED DESIGN |
| C2-G2 real cryptographic/key provider | Distinct Google-signed workload ID vs owner-controlled request proof keys: existing `getInvokerCredential`, `getGatewayAttestation`, `requestSigning.signMessage`, `requestVerification.resolvePublicKey` DI ports have no approved live provider/key version | One provider binding design with issuer/audience/principal, managed signer/key custody/rotation/revocation; no key creation/token mint/IAM changes now | BLOCKED PROVIDER |
| C2-G3 real runtime/SA/default DB | New C1A SA has **no roles**; A8 `/owner` runtime is not full enabled Product. Need exact separate least-privilege backend SA, `iam.serviceAccounts.actAs`, Google IAM invoker, `oldx-staging/(default)` only, Auth revocation and Firestore positive/negative owner/buyer tests | Review current code-native SA/project/DB checks and draft exact positive/negative one-default-DB policy; no IAM grant or extra DB now | BLOCKED IAM/DATA |
| C2-G4 publication/media acceptance | `createStep05Backend` hard-sets `publicationEnabled:false`; bootstrap rejects real publication enabled. Media must be managed-photo approved and existing owner/revision/withdraw checks intact | First source-only explicit publication provider decision and fail-closed capability gate; no bypass by changing a single env var | BLOCKED |
| C2-G5 nonce/TTL/cleanup and cost | `expiresAtMs` numeric is not Firestore Timestamp TTL; all admitted calls can cost nonce/Auth/rate/Firestore operations, even denied ones. No automatic cleanup | Exact synthetic ID manifest, nonce TTL Timestamp migration or exact-version guarded delete, retention policy and measured per-actor quota; no TTL policy write/data CRUD | BLOCKED |
| C2-G6 enabled-scope risk and rollback | Historic A8 15 severe findings and new Gateway 12 HIGH remain OFF-only risk dispositions; inherited IAM risk, old A8 hosted OFF503, backend owner/buyer denial and rollback not live-proved | One finite owner risk/rollback decision packet after G1–G5 source is ready; no repeat historic scans, no production GO | BLOCKED |

**External validation, not an OLDX source claim:** Google states Cloud Run end users generally do not have project/service IAM invocation privileges; browser Firebase end-user tokens do not automatically satisfy the service IAM Invoker check ([Cloud Run end users](https://docs.cloud.google.com/run/docs/authenticating/end-users), [Cloud Run private service-to-service](https://docs.cloud.google.com/run/docs/tutorials/secure-services)). Firebase Admin/server Firestore clients bypass Firebase Security Rules and rely on IAM, so least-privilege server enforcement is essential ([Firebase Rules queries](https://firebase.google.com/docs/firestore/security/rules-query)). Google Firestore TTL fields must be actual timestamp/date-time configured by TTL policy, not a numeric `expiresAtMs` application field ([Firestore TTL](https://docs.cloud.google.com/firestore/native/docs/ttl)).

## 3. Fastest permitted next implementation — SOURCE ONLY, one bounded code batch

### C2-S1: one reviewed **source-only host/dual-auth contract slice**

**Goal:** produce a reversible, default-OFF adapter/contract that composes existing five-route listener and `createStep05Gateway`/`createStep05Backend` ONLY when all trusted provider ports are supplied. Do not create new Firebase user, Product, URL, image or service. Preserve new and old deployed entrypoints.

**Scope for one focused Codex-assisted code batch if needed (not yet executed):**
1. Read current `AGENTS.md`, this packet and existing `secure-product-pipeline.mjs`, `trusted-host.mjs`, `cloud-run-http.mjs`, `http-transport.mjs`; use their actual APIs. Choose DI-only host adapter with `enabled=false` and no automatic `process.env` activation, credential/token/key mint, ADC/admin SDK creation or fetch side effects; reject wrong source/audience/origin/publisher and missing key/nonce/quota providers with 503.
2. Express **distinct browser Firebase identity vs backend service-to-service Google IAM ID token**; never forward browser-supplied privileged IAM/attestation/proof headers. For Guest, define the separate trustworthy internet path; **do NOT grant anonymous Invoker to current new private Gateway or pretend a browser token is a Cloud Run service token**.
3. Keep existing `publicationEnabled:false` on all operational runtime compositions until a separately signed C2 enabled-scope risk/provider decision. A source-only test may inject synthetic publication=true inside isolated disposable fixtures as ALREADY proven, but do not change deployed env/bootstrap for the sake of test.
4. Add only **new** narrow offline tests for missing-boundary 503, forged browser privileged headers/guest attempt, correct trusted identity/signing wiring, invalid/missing verified provider, and no network/ADC without explicit injected callbacks. Avoid rerunning 84/77 prior groups, prior image scan or broad CI.
5. Emit exact changed paths, test names, number **actually run**, results, source blobs, and edge cases to this same GitHub branch, updating this packet + Issue #17 with no-repeat receipt. Stop on any ambiguity; no deployment.

**Done definition for this batch:** trusted host contracts implemented default OFF, new narrow tests PASS, no Cloud or Firebase mutation. This is SOURCE readiness only. A future C2-H1 enabled hosted pilot remains separately owner-gated; code and tests alone do not close C2.

### One finite future C2-H1 synthetic pilot — DRAFT, **NOT AUTHORIZED**

- Preconditions: G1–G6 addressed; *specific* active owner/runner IAM, project number `38472235077`, target region `asia-south1`, immutable separately built/reviewed enabled image/service, exact runtime SA/default DB, key provider/rotation and real Firebase Auth, publication/photo provider; no inherited wildcard grant, no old service traffic change. Any inability to show safe guest path/permissions -> STOP. No current source automatically binds these.
- **Bound synthetic data:** max two separately created Auth actors (seller + buyer) ONLY if owners approve, max one Product and one managed photo ONLY if necessary and approved. Public guest list/detail does not require creating a third Auth user. Unique manifest exact document paths/UIDs/creation timestamps/versions/receipt IDs/nonce hashed paths/media generations and cloud resource UIDs captured at first write.
- **Bound acceptance cases (one pass):** seller sign-in→save draft→owner read/edit→publish only with approved media→buyer guest list/detail public DTO→buyer cannot mutate/see owner fields→other-owner denied→withdraw→buyer no longer sees item→archive→identical-requestId retry after lost response creates no duplicate→rate429, revocation/logout and fail-closed provider error. Actual statuses only from fresh single-run receipts, not generic claims.
- **Finite window**: one owner-approved schedule (e.g. 20m; calls/actions counted explicitly, not yet set) and small resource caps. Owner removed hard ₹ cap and pre-Billing screenshot formalities for speed; still no unbounded Cloud/KMS/data operations, per-request cost awareness, bounded recovery.
- **Cleanup**: after each new-object identity/ownership/generation/version/no-unexpected-dependency preimage, remove ONLY the newly created synthetic artifacts and separately authorized new resources; never broad sweep, second DB, old `oldx-owner-read` root/tags, old images/Registry, other Firebase users or real data. Real nonce TTL may be eventually consistent; do NOT assume instant cleanup. Independently prove no residual synthetic artifacts and old service rollback.
- **Explicit next approval**, to be requested ONLY after source readiness and fixed exact resource/actions: approve or reject C2-H1 new enabled host, scoped IAM, limited synthetic data/cleanup and disabled-to-enabled flag transition. **No approval currently granted.**

## 4. Existing C1A private Gateway disposition while C2 is prepared

The original NEW private C1A trial was approved as supervised <=24h, from **24 Nov 2026 about 23:19 IST through 25 Nov about 23:19 IST**. **No automation performs cleanup.** Before that deadline, owner must choose (a) guarded cleanup of exact newly created C1A service UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`, SA uniqueId `102194769236111252832` and image digest `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`, only if unreferenced; or (b) separately explicit extension of private OFF-only retention with limited risk accepted. **Neither is automatic in this C2 source packet.** Do not delete the existing Artifact Registry repository or old Cloud Run backend. Existing owner approval covered exact NEW-only safe cleanup, not unrelated resource deletion.

## 5. Snapshot / no-repeat state

```text
STEP04_ADMIN=04_OF_15_DONE_DECISION_ONLY
STEP04_ORIGINAL_TECH_EXIT=UNMET_HOLD_CARRIED
STEP05_C0=SOURCE_IMPLEMENTED_OFFLINE_VERIFIED
STEP05_C1A_PRIVATE_OFF=PASS_WITH_LIMITS_CONSUMED
STEP05_C1B_PRIVATE_OFF_HOSTED=PASS_WITH_LIMITS_CONSUMED_4_OF_6
STEP05_C2_SOURCE_GAP_MATRIX=COMPLETE_THIS_DOCUMENT
STEP05_C2_S1_DEFAULT_OFF_HOST_CONTRACT=NOT_YET_IMPLEMENTED
STEP05_C2_REAL_PROVIDER_AND_DATA_PLANE=NOT_ENABLED
STEP05_C2_ENABLED_HOSTED_PILOT=NOT_AUTHORIZED
STEP05_OVERALL=NOT_DONE
PRODUCTION=NO_GO
NO_NEW_CLOUD_IAM_FIREBASE_KMS_BILLING_DEPLOY_HTTP=TRUE_FOR_THIS_SOURCE_REVIEW
```


## 6. ONE copy/paste Codex task for C2-S1 (source-only heavy task; NOT YET RUN)

The owner prefers Codex for substantial code changes and minimal repeated checks. This is a **ready instruction**, not evidence that Codex executed it. Use an existing local Codex session against this review branch; do not start Cloud Shell/SDK or enable anything.

```text
OLDX Step05 C2-S1 SOURCE-ONLY, ONE PASS, NO REPEAT. Repo yasminparmar087-ops/oldx-website, branch security-hardening-review ONLY, never main.

FIRST READ AGENTS.md latest first, docs/OLDX_STEP05_C2_SOURCE_ONLY_ENABLED_SLICE_GAP_AND_ONE_PASS_IMPLEMENTATION_PACKET_2026-11-24.md, docs/OLDX_STEP05_SOURCE_ONLY_KICKOFF_AND_MINIMUM_OWNER_BUYER_SLICE_2026-11-24.md and the actual source of secure-product-pipeline.mjs, trusted-host.mjs, cloud-run-http.mjs, public-runtime.mjs, features/marketplace/http-transport.mjs. Check git status: preserve existing dirty/untracked owner files; do not reset/clean/overwrite. If already done by a newer commit, STOP and report no-op.

GOAL: Close ONLY source C2-G1/G2's trusted-host + buyer-transport contract seams with smallest reversible default-OFF dependency-injected source code; not C2 data activation. Keep actual deployed C1A private OFF-only Gateway, A8 old backend, source Bootstrap, IAM/Rules/Cloud Run configs, Dockerfiles, packages and production wholly unchanged. Do not create a public endpoint or change IAM Invoker to allUsers. Do not pretend a browser Firebase Auth ID token is a Cloud Run service-to-service IAM ID token. Separate bearer Firebase identity, backend IAM identity, and distinct request intent signer. For guest buyer, design a trusted browser->website/server-mediated path, OR explicitly leave a fail-closed unresolved provider port; never let current private Gateway be anonymous. Never use browser-supplied IAM, attestation, nonce, proof or client IP headers as trusted.

IMPLEMENTATION: If code needed, add one small inactive host contract/adapter that refuses with 503 unless injected allowed HTTPS origin, known principal/audience, validated distinct signed-request provider, trusted anonymous guest quota and signed cursor, safe backend binding are all present. Do not initialize Firebase Admin, ADC, KMS, new signing keys, Cloud Run token mint, HTTP listener, global fetch or environment on import. Keep publicationEnabled:false in operational composition. Reuse existing source modules and DTOs; avoid redesign or duplicate runtime. Add only new minimal tests for missing-provider 503, browser privileged header spoof denial, independent Firebase and Google IAM token channels, guest safe rejection if no trusted mediator, and no network/work when OFF. If a source change would need new cloud credentials/roles or real data, STOP and document unresolved dependency instead of stubbing success.

RUN ONLY newly relevant targeted Node tests for actual changed modules, one focused invocation each; no historic 84/77/other suites, no full CI, Docker build/Syft/Grype/Cosign, Cloud Shell, Billing, Firebase, Cloud Run, IAM or hosted HTTP. Record exact command and PASS/FAIL/SKIP; no invented results. No unbounded test loops or offline copied stale source. Commit only your new source/tests/docs on security-hardening-review, with [skip ci] if appropriate to avoid automatic duplicate workflows; do not alter AGENTS contrary to latest owner policy. Append exact source-only receipt and remaining C2-G3..G6 blockers to the canonical C2 doc and Issue #17. C2 enabled pilot, publication, backend privileges and production remain NO-GO; C1A/C1B one-shot results consumed. If a required dependency missing, stop with a precise source-only handoff rather than live action.
```
