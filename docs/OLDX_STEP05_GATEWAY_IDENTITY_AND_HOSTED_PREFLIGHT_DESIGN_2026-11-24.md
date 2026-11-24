# OLDX Step05 — independent gateway identity and bounded hosted acceptance design (SOURCE-ONLY)

Date: 2026-11-24 IST. Repo: `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`.

**Status: DESIGN / OWNER DECISION PENDING; NO CLOUD AUTHORIZATION.** This review starts from the verified `389ee56811506f21434de97859ef2826426bb90b` Step05 forwarded-IAM source correction. No existing Step04 B1/R1/test/scan is to be repeated. `STEP04_ADMIN=04/15_DONE_DECISION_ONLY`, `STEP04_TECH=UNMET`, `STEP05_HOSTED=BLOCKED`, `PRODUCTION=NO_GO`.

## 1. Verified source and platform facts

- Actual current hosted `functions/staging-marketplace/product-read-server.mjs` exposes only private owner POST plus health. It is **not** a buyer/public host. `functions/staging-marketplace/trusted-host.mjs` is an inactive dependency-injected gateway/backend contract; `createStagingMarketplaceTrustedHost` explicitly forces `publicationEnabled:false`. No live signed principal verifier is installed.
- Google Cloud Run checks an incoming Google-signed ID token in `X-Serverless-Authorization: Bearer ...` while retaining `Authorization` for Firebase application identity; Cloud Run **strips the former token signature before forwarding to the container**. `389ee568` correctly changed the backend to validate only bounded forwarding syntax, **not principal authenticity**. Source synthetic tests are not IAM proofs. See [Google Cloud Run service-to-service](https://docs.cloud.google.com/run/docs/authenticating/service-to-service).
- `verifyInvoker(request)` presently requires a **separately authenticated** proof with exact `audience`, `principal`, `verified`, `expiresAtMs`. Header presence, JWT payload without a verified signature, Origin, Host, `X-Forwarded-*`, Firebase token, raw Vercel claim or a hardcoded `verified:true` are **NOT** proofs.
- Vercel documents OIDC federation to Google Cloud **on all plans** and exact environment/owner/project scoped Workload Identity Federation subjects. Its WIF approach exchanges short-lived Vercel OIDC for Google IAM credentials; the Vercel OIDC token is **not itself a Cloud Run invoker ID token**. [Vercel GCP OIDC](https://vercel.com/docs/oidc/gcp); [Google WIF](https://docs.cloud.google.com/iam/docs/workload-identity-federation).
- A read-only search of Vercel projects named `oldx` through the currently accessible Vercel connection returned no projects. This **does not disprove** historical Vercel staging or identify the correct account/team/host. Do not guess a URL, team slug, environment, project ID or SA. Obtain exact owner-verified deployment metadata before configuring origin or WIF.
- Existing Step05 two source batches have separately documented **31 + 15 = 46** focused synthetic cases, and forwarded-header correction adds **2 new PASS cases = 48 distinct reported cases**. This is NOT a combined test suite or live verification.

## 2. Preferred low-rework candidate (CONDITIONAL, not authorized)

**Option V: reuse a verified existing Vercel staging/preview Function as the browser-facing gateway, and keep the actual Google Cloud Run Product backend PRIVATE.** The existing Vercel account/project must first be demonstrated to support this exact function and OIDC federation; if not, STOP and reconsider Option C.

```text
Approved preview Website / Android client
  -- HTTPS + Firebase ID token for seller commands, no end-user IAM token -->
Vercel SERVER-ONLY Function (public gateway, fail-closed)
  -- Vercel workload OIDC -> GCP WIF -> short-lived Google ID token -->
Private Cloud Run Product backend (Cloud Run IAM enforced)
  -- verified Firebase revocation/owner/quotas + verified gateway attestation -->
oldx-staging Firestore (default), only with approved runtime SA
```

**Distinct security credentials / headers:**
1. `Authorization: Bearer <Firebase user ID token>` only on seller commands. It is never substituted for Cloud Run IAM identity; guest list/detail omit it.
2. `X-Serverless-Authorization: Bearer <Google-signed Cloud Run ID token>` only from the trusted server-side gateway, audience EXACT existing private service URL (not a traffic-tag URL, browser host or unverified custom domain). Cloud Run authenticates this. The signature-stripped forwarded value is only syntax, never a principal proof.
3. **Independent principal proof still mandatory:** a separate signed, independently verifiable, backend-purpose-bound short-lived attestation from the approved gateway workload identity; its issuer/signature/algorithm/audience/expiration and *exact owner/project/preview environment or service-account principal* MUST be checked by a maintained verifier. Candidate implementation: a separate Google-signed ID token issued for a **distinct attestation audience**, conveyed in a tightly restricted custom server-only header and cryptographically verified in backend via Google public keys. Do not reuse the Cloud Run IAM audience for the attestation token, expose it to the browser, blindly trust an assertion returned by `fetchBackend`, or silently relax `verifyInvoker`. A dedicated Vercel OIDC assertion with distinct approved backend audience and independently verified Vercel issuer/JWKS is an alternative requiring separate review. **Neither source adapter nor specific authority is presently selected/implemented.**
4. A signed attestation is still a bearer credential; mitigate replay by separation of audience, short acceptable `iat` age/`exp`, HTTPS, no request/log leakage, bounded request/replay policy, dedicated least-privileged identity, and deny on missing or stale keys/JWKS. Consider binding sensitive mutations to a request digest/nonce if the approved verifier design supports it. A source-only verified SDK/library adapter is required before enabling.
5. The backend must verify Firebase user token cryptographically and check revocation, original resource owner, rate, publication and media prerequisites. Existing requestId/revision/idempotency remains unchanged.
6. The backend's Cloud Run IAM effective policy must be independently audited for inherited Owners/Editors; direct named invoker alone is not evidence of exclusive access. The second signed attestation is defense-in-depth, not a substitute for real IAM-required ingress.

**Why conditional Option V first:** reuse already intended Vercel web presence and avoid inventing a second deployed Cloud Run gateway. Real billing, Vercel project/account support, WIF setup/API requirements, IAM role breadth, gateway Function quotas, custom header attestation, integration tests and practical maintenance cost remain unknown. NO ₹0 claim or guarantee.

**Fallback Option C:** a separate Google Cloud Run gateway with its own attached managed service account obtaining keyless short-lived Google-signed ID tokens from the metadata server. This is a Google-documented public-to-private Cloud Run pattern but introduces a new service, potential recurring consumption and further IAM/deploy approval. A public gateway is **not** the same as a public Product backend; guest abuse and authentic user security still need protection. See [Google secured Cloud Run service-to-service](https://docs.cloud.google.com/run/docs/authenticating/service-to-service) and [metadata token](https://docs.cloud.google.com/docs/authentication/get-id-token). Do not provision Option C as a workaround without owner consent.

**NEVER use:** downloaded long-lived service account JSON keys; Firebase ID token as `X-Serverless-Authorization`; direct Firestore browser writes; `allUsers` on the private Product backend; local fake `verified:true`; query/body/headers-controlled IAM audience or principal; a wildcard CORS policy; blanket role grants or unrelated new Cloud services.

## 3. Exact configuration inventory — owner verification REQUIRED

| Field | Required validation | Present status |
| --- | --- | --- |
| Public Gateway host + HTTPS origin(s) | Exact approved Vercel project/team/preview deployment URL and expected browser origin(s); mobile client policy separately | UNKNOWN; no URL assumed |
| WIF issuer/subject/audience | Exact issuer mode, owner, project, preview environment, identity-pool/provider and subject match | UNVERIFIED, no pool created |
| Gateway service account | Distinct `oldx-staging` SA whose only necessary backend invoke and narrowly scoped credential acquisition rights are reviewed | NOT SELECTED; no grant |
| Private Cloud Run service/root audience | Exact project/region/service URL and 0%-main tag semantics, existing revision/image/flags/rollback preimage | Historical Step04 evidence only; fresh pre-call review |
| Backend principal proof | Actual independent signed attestation issuer, audience, principal binding, trusted verifier, JWKS/key refresh, expiry and failure behavior | NO VERIFIER IMPLEMENTED |
| Firebase seller ID + Firestore | Real Auth project, verify revocation; exact `oldx-staging/(default)` SA conditions and allowlisted synthetic records | Hosted effective proof PENDING |
| Cursor signing key | Dedicated key source/version/rotation, only server-side, key never in GitHub/browser/logs; no key generated here | MISSING OPERATIONAL CONFIG |
| Anonymous quota | Current shared pool only (not per-person). Exact guestLimit/globalLimit/window, expiry metadata vs confirmed deletion policy, cost and availability risk | SOURCE READY; policy not approved |
| Photos/publication | Native managed image validation, upload/quarantine/moderation & atomic publish/withdraw, config gates | NOT HOSTED APPROVED |
| Cost & recovery | All-provider gross cost forecast, bound calls/time, ₹1,000 manual STOP, ₹2,000 non-hard target, exact-ID guarded cleanup, root/tag rollback | PENDING FINITE CONSENT |

## 4. Required source-only verification BEFORE asking for any enablement

1. Choose one evidence-backed gateway implementation **only after** validating actual hosting project. Use existing `functions/staging-marketplace/trusted-host.mjs` and injected ports, no architecture rewrite.
2. Implement or bind real **independently signed** principal assertion verifier, not `verified:true` from request headers. Decode only AFTER signature verification; validate algorithm/key source, issuer, audience distinct from Cloud Run IAM root, exact principal/subject, env, `iat`, `exp`; reject missing, invalid, expired, rotated and replay-risk conditions. Keep it source-only default OFF. Do not mint real tokens or create keys until separately approved.
3. Ensure client cannot set `X-Serverless-Authorization` or independent assertion; gateway overwrites/strips these. Test real platform-stripped IAM syntax with synthetic stubs; verify distinct Firebase credentials; guest/no-Origin/CORS/preflight policy, mutation errors and unknown-commit retry remain safe.
4. Match the existing host server/Node24 support and approved project guards. Do not change existing Product owner-only Cloud Run service/flags or deploy tags. Current synthetic Node v26 is NOT Node24 hosted proof.
5. Add only changed-code-focused offline tests and save exact results. Reuse Step05 48-case historical receipts; do not repeat full build/scan/CI without need.

## 5. Sequential, finite hosted proposal (NOT OWNER-APPROVED)

**Gate H0 (strict preflight):** independently verify exact Vercel project/URL and enabled OIDC capability; effective Cloud Run IAM invoker policy including inherited Owners/Editor, runtime Firestore SA/default-DB conditions and no extra DB; original A8 revision/0%-main/false flags/old root; original 15 severe CVEs and new ENABLED-scope disposition; real gross-cost estimate and reporting lag; source verifier tests; photo/retention/cleanup proof. If any critical blocker, `STOP/NO_GO`.

**Gate H1 (separately scoped OFF-only request):** only with a NEW action-specific owner consent: specify current service/image/revision, optional **one new temporary tag** strictly on existing A8 0%-main revision (the default URL points to OLD revision, not A8), exact count of authenticated health/503/unauthorized probes, max duration/cost, before/after tag/traffic snapshot, independent exact-tag cleanup. No re-deploy or reused historical approval. Record what was actually called; fail closed.

**Gate H2 (separate enabled synthetic proposal, LATER):** after H0/H1 and a further approval for an exact bounded release candidate, prepare allowlisted **max two reserved synthetic Auth users and their actor records; max one synthetic product and one approved managed image**, capture generated IDs from receipts, explicit every document/media/quota/receipt/audit/generation key and preimage/etag/version-safe cleanup; include seller create/edit/publish/owner/withdraw/archive; guest read list/detail; deny cross-owner, absent/revoked user; quota, signed cursor, retry after unknown commit. Preservation/reversion of old traffic/tags, no broad deletes. Do not start while production/Security P0 unresolved or original bootstrap refuses publication.

**Gate H3 (after evidence, not automatically):** owner evaluates Step05 real hosted PASS, separate Step13 original risk/rollout security acceptance and eventual Step14 production GO. No administrative Step05 closeout based on source tests.

There is **NO** unconditional one-click script or approval contained in this packet. Required actual numeric call/time/cost ceilings and known resource identifiers will be prepared only from verified host/account data and then submitted for fresh owner permission.

## 6. Risk and cost decisions unchanged

- Existing `₹1,000` is a **manual review/STOP before future paid action** threshold; `₹2,000/month` is an aspiration, NOT an enforceable all-provider hard cap. Do not extrapolate a fixed per-day cost from inactive source. Review Cloud Run, Vercel Functions, WIF/IAMCredentials/STS, Firestore/Auth, storage/photos, Secret Manager, egress/logging, taxes and free-trial offsets/expiry.
- Step04 G2: 15 distinct severe CVEs/46 package matches, OFF-only historical owner risk acceptance, NOT an enabled-scope fix. Require fresh threat/mitigation/owner choice for an ENABLED Product trial.
- Step04 G4: historic two Owners and one Editor may inherit Cloud Run invocation; direct service policy not sufficient. Only current `(default)` Firestore DB exists; **do not create a second database** to make a negative proof.
- Step04 G8: existing Cloud Run-only cap and budget alerts are not hard whole-provider spend controls; rollback/cleanup/access evidence must precede any paid experiment.
- Never change production traffic/root `00001-8kr=100%`, historical tags `healthcheck`/`step3rc14`, real records, IAM, Firebase Rules or billing under this SOURCE-only review.

## 7. Decision and next one action

**Recommendation subject to evidence:** explore reuse of verified Vercel preview gateway + short-lived OIDC WIF; accept only independently authenticated signed gateway attestation distinct from Cloud Run IAM and Firebase tokens; fallback to separate Cloud Run gateway solely after measured risk/cost and explicit approval.

**Immediate next action:** identify and verify the actual owner-controlled Vercel staging project/account/HTTPS preview origin and OIDC capabilities **read-only**, then fill configuration inventory and prepare ONE targeted source-only Codex task for the attestation verifier. Since the currently connected Vercel account returned 0 matching projects, do not invent or select its hostname here. No Cloud IAM/API writes or live authentication call.

**Evidence consulted:** current GitHub `AGENTS.md`, `docs/OLDX_CURRENT_HANDOFF.md`, 15-step plan, existing Step05 receipt, `trusted-host.mjs`, `product-read-server.mjs`; Google Cloud Run/WIF docs and Vercel official OIDC/GCP docs linked above. No tests or provider execution in this document-only decision packet.

**Owner approval state:** `GATEWAY_OPTION_V=RECOMMENDED_CONDITIONALLY_NOT_SELECTED`; `GATEWAY_PROOF=NOT_IMPLEMENTED`; `H0-H3=NOT_AUTHORIZED`; `STEP05_HOSTED=BLOCKED`; `PRODUCTION=NO_GO`.
