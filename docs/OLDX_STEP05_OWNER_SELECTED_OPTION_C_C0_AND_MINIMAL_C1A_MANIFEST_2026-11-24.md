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
