# OLDX Step05 — Cloud Run Gateway Option C: source-only architecture, cost envelope and FINITE owner consent design

Date: 24 Nov 2026 (IST). Repository: `yasminparmar087-ops/oldx-website`; branch `security-hardening-review`. Starting verified HEAD: `159d28a272e1932a01e5860a613e21b57717805d`.

**STATUS: PROPOSED CONDITIONAL FALLBACK / DESIGN ONLY / NOT OWNER-APPROVED / NO RESOURCES CREATED.**
`STEP04_ADMIN=04/15_DONE_DECISION_ONLY`; `STEP04_ORIGINAL_TECHNICAL=UNMET`; `STEP05_SOURCE=INTEGRATED_OFFLINE_TEST_VERIFIED` (77 distinct reported PASS cases, not a single full run); `STEP05_HOSTED=BLOCKED`; `PRODUCTION=NO_GO`.

## 1. Why choose a conditional next direction without repeating old searches

- The old repository guide referred to a legacy `oldx-webs` Vercel project under the former repository account; prior **consumed** Vercel read-only discovery saw zero matching projects/deployments on the current linked team and a 404 for that project in the linked account. **Do not search it again** or assert the legacy site was deleted. There is still no owner-verified deployable Vercel Function or HTTPS gateway origin for Step05.
- The latest verified `secure-product-pipeline.mjs` has both existing `createStep05Gateway` and `createStep05Backend` **default OFF**. It already composes separate Firebase user authentication, Cloud Run platform IAM hop ID token, independent Google-signed gateway service identity, separate signed request-intent, atomic cross-instance nonce, guest quota/cursor and Product runtime. It does **not** instantiate a deployed listener, token source, KMS signer or host.
- **Conditional recommendation Option C:** if the owner cannot supply an EXISTING accessible, verified Vercel staging gateway (no repeated legacy discovery), plan a **separate new Cloud Run Gateway** using a dedicated attached managed service account; preserve existing Cloud Run **Product backend PRIVATE**, original A8 0%-main and `00001-8kr` root. A new Gateway is *not* an approved/deployed service, and introduces image, IAM, potential spend and guest-abuse gates.
- Official Google secure two-service pattern: public-facing frontend Cloud Run service calls private backend using an attached service identity with `roles/run.invoker` on the backend only. See https://docs.cloud.google.com/run/docs/tutorials/secure-services and https://docs.cloud.google.com/run/docs/authenticating/service-to-service.

## 2. Minimal target architecture, separate credentials and stages

```text
Future user browser / Capacitor client
   | Firebase ID token for SELLER commands; none for guest public-list/detail
   v
NEW Cloud Run Gateway  [START PRIVATE + default-OFF; not public on first deploy]
   Dedicated gateway SA, no Firebase Admin/Firestore direct data permissions
   (1) fetch Google-signed IAM ID token for EXACT private Backend service URL
       -> X-Serverless-Authorization (Cloud Run platform checks signature)
   (2) independently signed Google service-account ID token for DISTINCT
       application attestation audience (backend validates issuer/sub/email/iat/exp)
   (3) independently RSA-signed method/path/body/auth/attestation proof
       using a separately approved fixed Key Version signer
   v
Existing/private Cloud Run Product service (A8 0%-main remains OFF; NO reroute)
   Cloud Run IAM-required ingress + app-side independent attestation verifier
   + signed intent + transactional once-only replay nonce
   + revoked Firebase user/ownership or guest quota/cursor/media guards
   v
oldx-staging/(default) [ONLY after separately approved real Firestore scope]
```

**First deployment MUST NOT be publicly reachable or enable any Product API.** Proposed initial Gateway: Cloud Run service auth REQUIRED, ingress reviewed, `enabled=false`, no traffic to existing Product enabled revision, no Firebase/Firestore permissions for Gateway, minimum instances `0`, conservative service-level maximum instances `1`, request-based billing and bounded ingress body/headers/deadlines. Maximum instances is NOT a guaranteed whole-provider money cap and cannot safely be treated as an abuse limit. A later public gateway decision requires a distinct owner approval (only public gateway may become accessible; Product backend never `allUsers`). On a public gateway, CORS/Origin is NOT caller authentication; add effective abuse controls before guest access and size quotas for unauthenticated requests. No Cloud Armor/API Gateway/CDN or extra paid service assumed.

**Cloud Run IAM ID token:** fetch from the attached service identity's metadata server using fixed backend service URL as `audience`. Tag URL is NOT an IAM audience; platform strips the forwarded X-Serverless-Authorization signature, so app must never treat its forwarded bytes as principal proof. Backend must independently verify the second signed attestation. Google official docs: https://docs.cloud.google.com/run/docs/authenticating/service-to-service .

**Application attestation:** separate exact purpose-bound audience, pin real dedicated SA email AND numeric `sub`, `email_verified`, issuer, signature and expiry with existing Google JWKS verifier; do not reuse platform forwarded token as attestation. Existing gateway metadata says attestation expires within 120 seconds and backend source defaults to `iat` max 60 seconds. Google identity tokens normally have up-to ~1h `exp`; **P0 compatibility question** is whether provider reliably returns a freshly issued JWT with `iat` within 60 seconds for every hop or after cache refresh. If not, SOURCE change + new narrowly scoped test to separately bound *request replay* with already implemented 15s proof and retain verified identity expiration must be formally reviewed; do not silently loosen verifier or cache year-old identity tokens.

**Request-intent signer:** preferred source-compatible candidate is a **fixed Cloud KMS SOFTWARE RSA 2048 `RSA_SIGN_PKCS1_2048_SHA256` CryptoKeyVersion**, NOT the Google OAuth ID-token JWKS key and NOT a downloaded SA JSON private key. Gateway's `signMessage(bytes)` must compute SHA-256 of the exact canonical proof bytes then call Cloud KMS `asymmetricSign` with that digest, returning strictly bounded RSA signature. Backend's `requestVerification.resolvePublicKey(kid)` trusts ONLY the independently pinned exact KMS key version public key; `kid` is a fixed allowed opaque mapping to that version, NOT a request-selected KMS URL. Separate permissions: `cloudkms.cryptoKeyVersions.useToSign` for Gateway only on the reviewed key, `cloudkms.cryptoKeyVersions.viewPublicKey` for the reviewed Backend verifier or safe pinned public key distribution. Version rotation requires explicit dual-version/cutover/retire plan and short signed-proof overlap, not fallback to any key or broad KMS roles. This is a **candidate**: new key/keyring, IAM, API, region, latency and cost still require approval. Google KMS: https://docs.cloud.google.com/kms/docs/create-validate-signatures .

**Alternative `iamcredentials.signBlob` needs a separate design:** it returns `keyId` AFTER signing, whereas current canonical request-intent payload embeds `kid` BEFORE signing. A naive adapter breaks at Google managed-key rotation; `roles/iam.serviceAccountTokenCreator` may be broader than minimal KMS signing. Do not simply wire `signBlob` or grant Token Creator as a shortcut. Google docs: https://docs.cloud.google.com/iam/docs/reference/credentials/rest/v1/projects.serviceAccounts/signBlob .

## 3. Cost envelope — guidance, NOT spending authorization

Official pricing snapshots reviewed 24 Nov 2026:
- Cloud Run **request-based** allocation has a free tier (measured at us-central1 rates) for **2 million requests**, 180,000 vCPU-seconds and 360,000 GiB-seconds monthly, **across eligible billing-account services**, not guaranteed free to OLDX. Exact region, memory/CPU, cold starts, min instances, ingress calls, logs, network and build/registry affect gross spend. Request-based instances with min 0 can scale down and avoid idle compute charges, but a new service is NOT assured ₹0. https://cloud.google.com/run/pricing
- Cloud KMS SOFTWARE RSA-2048 active key version list rate **USD $0.000082192/hour** (~**$0.06 for 730h**), plus **$0.03 per 10,000 cryptographic operations** (e.g. $0.003 for 1,000 if charged at list rate). This is **ONLY KMS** and excludes actual tax, billable additional public-key retrieval calls, Cloud Run, logging, build/Artifact Registry, Firestore, Firebase Auth, egress and any FX/tax. Do **NOT** assume Autokey-only free quota applies to a manually created key. https://cloud.google.com/kms/pricing
- Every admitted signed attempt may perform KMS signing and downstream metadata token lookup; backend may charge Firestore nonce transaction even on later Product policy denial. Guest quota is NOT an anti-abuse hard cost control. Public Gateway processing itself may be billed on rejected requests. Limit ingress, request count and time, use no automatic retry, and produce measured gross provider estimate before approval.
- ₹1,000 is the prior owner's **MANUAL STOP/review before new paid action** trigger; ₹2,000/month is a NON-GUARANTEED risk-budget target, not a service-global hard stop. Project Billing alerts / Cloud Run maximum instances / free trials DO NOT provide all-provider guarantees.
- For any future finite hosted trial, obtain verified service region and resource shape, actual current gross provider usage, free-trial offsets/expiry, projected worst-case 20min/6 request burst, KMS key active-hour/operations, nonce read+write+TTL cleanup/delete and Pub/Sub/log/storage costs, Cloud Run image scan/build and existing private backend idle/calls. Record currency, effective taxes, reporting lag and exact operator STOP/rollback.

## 4. Safety and administrative gates — NO CLOUD ACTION under this doc

### Gate C0 — source/owner decision, current phase
Owner can approve **Option C as the planning preference ONLY** (not provisioning). Verify final resource names, region, existing backend canonical service URI and no accidental production URL through an owner-supplied authenticated Cloud Console screenshot or canonical saved evidence; **do not replay** consumed old A8/IAM/DB/Vercel tests to fill already established historical fields. Distinguish already evidenced vs currently unverified. Confirm managed SA, key version/signing principal, exact private audience and review-branch source-to-image mapping, shared nonce retention and cleanup approach. A single precise H1 action consent can then be drafted. If host project or identity cannot be established, remain HOLD and continue other independent source tasks.

### Gate C1 — future PRIVATE DEFAULT-OFF Gateway staging (fresh owner consent REQUIRED)
Before any resource creation or API activation, specify: new gateway service + SA name, region/image hash/provenance/security scan and CVE disposition, KMS fixed key version and narrowly scoped permissions (if selected), Cloud Run invoker/ingress permissions, exact new resource count, max runtime/time/calls and gross cost ceiling, preimage, protected old backend/root/tags, rollback and version-safe cleanup. Initial new gateway private `enabled=false`, no public access, min instances=0, service-level max=1 and no active Product Firebase/media writes. No IAM role widening to former paniruddhsinh account, no `allUsers` on Product. Any tag on existing A8 `00012-vib` to reach its 0%-main revision needs **its own newly approved tag+exact cleanup**; untagged service URL is OLD 100% root, not A8. Never repeat consumed B1/R1.
Only after a signed image/SBOM/CVE review, independently verified effective Invoker and SA/default-DB conditions, separate approval could permit at most **6 bounded OFF-only requests within 20 minutes**; these numbers are a proposal, NOT executed limits. Leave original root `00001-8kr=100%` and `healthcheck`/`step3rc14` tags untouched.

### Gate C2 — future public/ENABLED synthetic seller/buyer (SECOND fresh approval REQUIRED)
First settle original **15 severe CVE** enabled-scope threat disposition (prior G2 owner acceptance covers OFF A8 only), effective inherited Owners/Editor IAM access, product-authorization and Firebase Auth project, media/provider publication requirements, actual Seller+Guest endpoint abuse, cross-instance nonce and configured Firestore TTL/guarded deletion. Metadata `expiresAtMs` alone DOES NOT configure TTL. Prepare exact max 2 synthetic Auth actors, max 1 Product and 1 approved managed image, exact receipt/nonce/quota/media/audit/generation IDs and preimages, rollback and finite time/calls/cost; no wildcard deletes, real-user inventory or second DB. Public Gateway requires separate authorization and must fail closed if any credential/provider/retention binding missing. Production NO-GO until Step13/14 approvals.

### C0 vs C1/C2 owner's boundaries
- **C0 is documentation / planning only**, safe under current source-only permission.
- **C1** would create at least a Cloud Run service, service account and possibly KMS key/roles (all NEW, potentially billable): absolutely NO current authorization.
- **C2** would permit actual user data/guest APIs: absolutely NO current authorization.

## 5. Exactly one next action

**Proposed owner question:** “Shall OLDX choose **Option C: separate Cloud Run Gateway** as the **planning preference only**, preserving private default-OFF Product backend, while deferring any new resource/IAM/API/key/billing/deploy/testing until a separate finite C1 permission packet?” If YES, freeze this as the chosen DESIGN and prepare the exact new-resource manifest/cost table from owner-verified existing resource IDs, without live API actions. If NO, remain source-only and wait for actual accessible Vercel origin/host identity without repeating old discovery.

**No cloud operations, deployments, Service Account creation, KMS actions, IAM roles, Auth/Firestore, billing, tests/build/scan/CI or paid actions are performed by this design note.** The existing 77 distinct offline case receipts remain historical, never rerun. Existing Step05 source code and default-OFF deployments remain unchanged.
