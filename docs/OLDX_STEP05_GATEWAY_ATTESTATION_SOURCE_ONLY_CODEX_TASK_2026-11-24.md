# OLDX Step05 — one-shot Codex implementation of real cryptographic gateway proof (SOURCE ONLY)

**Owner continuation instruction:** implement actual minimal new source and focused regression tests; do not stop at planning. Maintain current branch `security-hardening-review` and existing 15-step plan. Current verified starting HEAD is the latest `security-hardening-review` branch, after `389ee568` forwarded-IAM compatibility and the independent [gateway proposal](OLDX_STEP05_GATEWAY_IDENTITY_AND_HOSTED_PREFLIGHT_DESIGN_2026-11-24.md).

## Newly verified account evidence; do NOT guess a gateway host

- Existing historical `VERCEL_ENVIRONMENT_VARIABLES.md` refers to old Vercel project **`oldx-webs`** connected to **legacy `paniruddhsinh088-beep/oldx-website`**. This is not a verified present deployment or a verified owner-controlled Vercel account.
- Currently connected Vercel team `OldX Store` (`old-x-store`, Hobby) has **0** listed projects, linked projects, deployments and aliases; current personal account also returned **0** deployments and aliases. Read-only `get_project('oldx-webs')` returned 404 in both current personal and team scopes. Do not conclude the historical project is deleted; it may be in a different Vercel account.
- `vercel.json` explicitly disables automatic deploy for `security-hardening-review`. `functions/staging-marketplace/product-read-server.mjs` still has owner POST+health ONLY; no buyer routes deployed. Source-only adapters in `trusted-host.mjs` are inactive.

## THE SINGLE TASK TO EXECUTE

Implement the **smallest genuinely cryptographic, fail-closed SOURCE-ONLY independent gateway-attestation verifier** for `functions/staging-marketplace/trusted-host.mjs`, with *no assumptions about the ultimately selected browser gateway host*. Treat the conditional preferred Google-managed keyless SA identity route as a candidate rather than established; do not mint tokens, call cloud, select SA, create IAM/WIF or deploy.

Read current `AGENTS.md`, latest `docs/OLDX_CURRENT_HANDOFF.md`, 15-step plan, Step05 receipt, gateway proposal, and current exact source/tests first. Preserve local dirty Handoff/.firebaserc and existing commits. Use current remote HEAD safely if local checkout is stale.

### A. Cryptographic independent principal proof — actual verified signature, not synthetic trust flag

- Build a small server-only, **default-disabled** verifier/adapter for an independently signed short-lived gateway assertion, with explicit, *server-trusted* issuer, distinct application-attestation audience, expected principal and public-key provider. Prefer a reviewed existing JOSE verifier/security library already pinned in this repository; otherwise use Node's native `crypto.verify` with a strict allowlist (e.g. RS256 only) and trusted-key injection.
- Parse bounded token/header and strictly verify signature **before trusting any claim**. Reject `alg:none`, algorithm/key confusion, unknown `kid`, unapproved key/issuer, token header-supplied `jku`/`x5u` URLs, oversized inputs, wrong issuer/audience, wrong principal and missing/unverified email claim when required by selected token type. Match `exp`, `nbf`, `iat`, max age and reasonable skew using validated numeric seconds; reject far-future or stale assertions. Use a **separate audience**, not the Cloud Run IAM audience. Never treat Cloud Run's signature-stripped `X-Serverless-Authorization` as a signed assertion.
- A Google-signed service-account ID token may have a numeric `sub` and a separately verified `email`; DO NOT assume `sub=email`. Support strictly validated configured identity types only; don't widen to arbitrary OIDC by default. Do not fabricate a new Google audience, service-account email, issuer or public-key URL.
- Keys/JWKS must come ONLY from an explicit trusted provider with safe, bounded retrieval/rotation and fail-closed behavior; no untrusted header-selected network URL, no secret checked into Git, no long-lived SA JSON keys, no hardcoded test key in production source. If exact provider/issuer wiring is impossible without owner-verified host config, implement the pure deterministic verifier with a required trusted resolver and leave actual host binding **BLOCKED**.
- Integrate the verified result into existing `verifyInvoker` contract ONLY after genuine signature validation; require matching exact audience, principal, expiry. Browser cannot submit or override the privileged assertion header; gateway must strip incoming forged assertion and attach only its own independently obtained assertion. Backend must remove privileged headers before Firebase runtime. Keep Firebase user `Authorization` and Google Cloud Run `X-Serverless-Authorization` separate; Cloud Run IAM remains independently enforced.
- Token replay: a signed bearer assertion is *not* one-time use. Document the residual replay window and guardrails (very short max-age, TLS/private IAM, fixed audience, mutation requestId+revision and limits), and whether a new signed request digest/nonce is necessary BEFORE any hosted approval. Do not claim replay impossible. Avoid automatically retrying mutated requests.
- Fail closed if a real trusted platform/signed-assertion provider is not configured. Never implement `verified:true` from caller-supplied claims, `origin`, `host`, `x-forwarded-*`, stripped IAM bytes or plain Firebase token.
- Do NOT turn publication on or alter currently deployed `product-read-server.mjs` owner-only routes. Keep all source factories OFF by default.

### B. Minimal targeted offline regression

Create only focused new/changed tests, using **actual locally generated throwaway RSA signing keys** and Node crypto verification, not a callback returning `verified:true`. Include a valid cryptographically signed assertion, wrong key/kid, tampered signature/payload, issuer/audience/principal mismatch, stale/expired/future, malformed/oversize, forbidden header key URLs and untrusted browser assertion denial; check independent proof remains required even with a platform-shaped signature-stripped IAM header. Assert Firebase ownership/auth remains separate.

Use 1–3 test commands. Don't rerun the historic 48 Step05 cases or Step04 build/SLSA/Grype/CI/Cloud probes unless a changed test requires it. Report Node version and distinction from real Node24/hosted.

### C. Preserve and report actual gate facts

Prepare exact **source-only** gateway attestation wiring contract and an unfilled operational configuration checklist for one owner-reviewed host:
- actual old Vercel `oldx-webs` ownership/project lookup 404 in current connection: no host selected;
- if a verified Vercel preview Function is found later, assess OIDC WIF, SA impersonation, IAM ID-token mint, independent signed attestation, cost/quotas and host routing;
- if that host cannot be verified, present alternate Cloud Run gateway as conditional fallback **without provisioning**;
- never claim IAM exclusive because historic 2 Owners+1 Editor may inherit;
- preserve old 0%-main A8 and original root 100%/tags;
- G2 15 severe CVEs enabled-scope review, G4 effective IAM/SA, G8 gross costs (₹1,000 manual STOP/₹2,000 non-hard goal), media/publication, bounded synthetic exact-ID cleanup and rollback remain OPEN.

### D. Required finalization

1. Verify minimal source/test edits; commit and push to `security-hardening-review` if safe.
2. Update existing Step05 receipt, current Handoff, and only the Step05 status note in the 15-step master plan, without altering master scope or prematurely marking 05 DONE.
3. Return **starting and final SHA**, precise files/changes, *new* PASS/FAIL tests, verified vs unverified aspects, and **ONE next action**. Mark `STEP05_SOURCE_ATTESTATION=PARTIAL_OR_TEST_VERIFIED` with accurate caveats; `STEP05_HOSTED=BLOCKED`, `PRODUCTION=NO_GO`.

**STRICTLY FORBIDDEN:** Vercel/Cloud Run deploy, publish, create project, assign IAM, alter Rules/Auth/Firestore/Billing, mint real provider tokens, create secrets, production traffic or paid action. The existing user authorization is ONLY source-only work. Do not repeat completed 48 Step05 tests or Step04 consumed workflows.
