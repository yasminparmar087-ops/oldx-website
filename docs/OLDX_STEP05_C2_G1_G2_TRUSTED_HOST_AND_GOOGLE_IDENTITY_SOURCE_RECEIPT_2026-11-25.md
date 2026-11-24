# OLDX Step 05 C2 G1/G2 — trusted website host and Google service identity source receipt

**25 November 2026 IST.** Branch `security-hardening-review`, repository `yasminparmar087-ops/oldx-website`. Following the owner's **"ok aagal vadho"**, this work continues **source-only** Step05 G1/G2: a real host selection inventory and one fresh default-OFF Cloud Run metadata identity provider. **C2 live, enabled Product API and production remain NO-GO**. No IAM/Cloud/Firebase/Firestore/KMS/Registry/Vercel write or hosted HTTP call was performed.

## 1. Actual G1 host evidence — no guessed Vercel account

- Read-only connected Vercel tool `list_projects` for the **connected user** returned `projects: []`, count 0. `list_teams` returned **OldX Store**, team ID `team_IN7a5URL55GBOrLtYz7jyay7`, slug `old-x-store`. Read-only `list_projects` scoped to this exact team also returned `projects: []`, count 0.
- This proves **no accessible projects in this currently connected user/team scope**, NOT absence of any OLDX deployment in other accounts/teams. Do not assert Vercel is globally disconnected/unavailable or that `oldx-webs` has been deleted.
- Current GitHub `vercel.json` has `git.deploymentEnabled.security-hardening-review: false`, build command `node scripts/generate-firebase-env.js && node scripts/build-static-assets.mjs`, output `public`. The actual branch has static `index.html` and `admin.html`, `package.json` and **no root `api/` directory**. No current trusted website API/mediator host has been proven or deployed.
- Historical Vercel docs name an older linked account/repository; they are **not** current account/deployment evidence. No attempt to modify or reconnect an external Vercel project under this task.

**G1 architecture recommendation, SOURCE-ONLY, NOT approved for deployment:** prefer a dedicated, isolated, owner-reviewed **staging Cloud Run website-mediator** with a NEW runtime SA (distinct from existing C1A Gateway SA) if an existing authenticated website-side Vercel function/project cannot be verified under the intended owner. A browser would call the separately approved staging mediator, which enforces strict paths/headers, backend Firebase user identity for seller, durable guest pool quota for public list/detail, and independently authenticates to the EXISTING IAM-private Gateway. The mediator's browser-facing surface is **NOT** the existing C1A Gateway and must undergo separate explicit public-ingress, abuse/rate, scope/cost and identity reviews. Do not make C1A `allUsers` or attach server credentials to browser code. If the existing Vercel project is subsequently proven accessible, re-evaluate a server-side Vercel mediator without inventing Google identity token minting or exposing keys.

**HARD CURRENT BLOCK:** existing C1A service `oldx-step05-gateway`, service UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`, immutable digest `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`, is **compiled OFF-only**: its deployed `cloud-run-gateway-off-server.mjs` always returns 503 on `/api/*`. It **cannot become C2 enabled just by an environment flag**. A future separately reviewed enabled image/deploy, backend and data-plane contract is mandatory before a genuine seller/buyer hosted slice.

## 2. Actual G2 source progress — one new default-OFF identity provider, NOT real Google mint proof

New repository source: [`scripts/c2-cloud-run-metadata-identity.mjs`](../scripts/c2-cloud-run-metadata-identity.mjs), Git blob **`aa3422c84a83f2a3de6701e13c226fa16ba47df4`**. New focused tests [`tests/integration/step05-c2-cloud-run-identity.test.mjs`](../tests/integration/step05-c2-cloud-run-identity.test.mjs), Git blob **`3762ec16f787f3cd1fdc2db072671988572ce5a9`**. Actual GitHub blobs were read back and matched the EXACT independently tested local source bytes; no re-execution against Cloud.

`createC2CloudRunMetadataIdentity` accepts **explicit host-injected** `fetchMetadata`, `serviceAccount`, `invokerAudience` and a distinct `assertionAudience`. When `enabled=false` (default), or any required config missing, it refuses without contacting metadata. When an approved trusted Cloud Run host later injects a metadata transport, it requests audience-bound short-lived Google ID tokens exclusively from a fixed metadata-server URL (`/computeMetadata/v1/instance/service-accounts/default/identity?audience=...&format=full`) with `Metadata-Flavor: Google`, fail-closed redirect/no-cache settings, abort/deadline and 8 KiB response bound. It validates token syntax, issuer, `email`, `email_verified`, numeric `sub`, `iat`, `exp`, exact audience and age. It produces separated `getInvokerCredential` (`type: cloud-run-iam-id-token`) and `getWebsiteAttestation` functions to be used by the existing C2-S1 injected website/private-Gateway factories **only with fresh reviewed live account/host binding**.

**Critical trust boundary:** Locally parsing claims does **NOT** verify an RSA signature. This adapter trusts the future *actual Google Compute Metadata Server identity transport* and the associated Cloud Run service runtime identity; signed ID token verification must still occur independently at Cloud Run Invoker/IAM ingress and the existing Google-JWKS/RS256 verifier of `c2-website-mediation.mjs`. Test fixture JWTs are NOT Google-signed. A malicious/fake injected `fetchMetadata` is **not secure**. No default global `fetch`, credentials, service-account key, SDK import, network call or Google IAM role is introduced by this source file.

### NEW focused test receipt — 4 PASS, no old test replay

**Tested exact source bytes** in isolated local Node `v22.16.0`, command:
```sh
node --test tests/integration/step05-c2-cloud-run-identity.test.mjs
```
Results: **4 new tests PASS, 0 FAIL, 0 SKIP**. Tests cover (1) disabled no-network and no implicit credentials; (2) distinct exact server IAM and website assertion audiences, metadata request shape; (3) wrong audience/abort/missing provider denying before any fetch; (4) malformed metadata, mismatched email/audience/claims, old token, bad response/oversize denying without token disclosure. These are new offline fixture checks only, no real Google-signed JWT, no hosted proof, no broad CI, no historic Step04/C1A/C1B tests. Source and tests are exactly the GitHub file blob SHAs reported above.

Official references (external, not OLDX test results): [Google Cloud Run service-to-service authentication](https://docs.cloud.google.com/run/docs/authenticating/service-to-service), [Cloud Run service identity](https://docs.cloud.google.com/run/docs/securing/service-identity), and [Cloud Run end-user authentication](https://docs.cloud.google.com/run/docs/authenticating/end-users). They establish metadata-based service-account ID tokens for trusted Cloud Run workloads, and separate end-user Firebase credentials; they do NOT certify OLDX host configuration.

## 3. Exactly what G1/G2 still require before a real trial

| Gate | Prepared today | Required before enabling |
|---|---|---|
| G1 trusted website host | Connected Vercel read-only user/team both EMPTY; conditional Cloud Run staging mediator architecture | Determine actual operator account/staging origin, exactly named **NEW** mediator host + public browser access/abuse controls, authenticated mediator SA, safe public guest quota, CORS and API transport; separate owner approval for any new service/public surface |
| G2 service identity + signing | New default-OFF metadata ID token source port, existing C2-S1 verified RS256 Google JWKS backend and independent request proof crypto | Actual Cloud Run runtime SA unique ID/sub, **target Gateway URI/audience**, explicit separate assertion audience, IAM `roles/run.invoker` scope only on exact target (if authorized), real metadata provider and key custody; *independent* request-intent signer/public verification key provider, controlled revocation/rotation; no keyless-only assumption |
| G3–G6 | Existing source/decision docs intact; no duplicated work | Firestore least-privilege `(default)` permissions and revocation positive/negative; media/publication policy; nonce TTL/cleanups; enabled-image risk disposition and rollback; one approved hosted synthetic run |

**Minimal future two-phase execution:** (1) one separate scoped host/provider READ-ONLY resource/identity/gross preflight with verified actual owner/provider account and exact target names, no repeats of old IAM inventories; (2) **only with separate explicit owner approval** create/bind any NEW mediator image, SA, IAM and enabled backend/signer/Firestore synthetic test, execute a finite call budget with exact UID/generation cleanup and reversible rollback. No public invoker exception or old service traffic changes may be inferred from this source work.

## 4. Locked no-repeat and retention

C1A Private OFF-only staging and C1B hosted `403/200/503` are already `PASS_WITH_LIMITS` (C1B 4 of 6 HTTP calls consumed). C2-S1 contracts and **7 earlier offline test groups** already PASS; none repeated. Original A8 old Product, original signed Distroless parent, scans/84 old Node cases, old IAM/default DB inventory, C1A build/push/service and C1B HTTP were **NOT rerun**. New Gateway's **12 HIGH** findings and earlier A8's **15 severe** findings remain OFF-only risk acceptances, not C2-enabled clearance. No provider tokens or secrets printed/saved.

Owner approved keeping only NEW C1A private default-OFF resources through **28 Nov 2026 23:19 IST**. No automatic cleanup, monitoring, IAM or deployment change; later exact new UID/digest/no-dependency guarded cleanup or distinct retention approval must be decided by that date.

**Snapshot:** `C2_G1_CONNECTED_VERCEL_PROJECTS=0_IN_THIS_SCOPE`; `C2_G1_HOST_LIVE=NOT_SELECTED`; `C2_G2_METADATA_PROVIDER_SOURCE_ONLY=4_NEW_TESTS_PASS`; `C2_G2_REAL_PROVIDER/REQUEST_SIGNER=BLOCKED`; `C2_ENABLED_HOSTED=NO_GO`; `PRODUCTION=NO_GO`.
