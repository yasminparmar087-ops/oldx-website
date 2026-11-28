# BAJUTO / OLDX Step05 — bounded lifecycle source integration receipt
Date: 28 November 2026 (IST). Branch: `security-hardening-review` only.

## Verified source and architectural decision

Starting remote HEAD `8e2a3c4099f0a674daba8ffb5ec007dd5a1fb907`. Tested implementation commit: `d13e16296343284a3c5049011497e8055ff149a2` (`[skip ci]`). The documentation commit following it records this evidence. Local owner checkout was behind the remote and retained its dirty Handoff and untracked `.firebaserc`; no pull/reset, owner-file overwrite, force push or main change. Work used an isolated, current-remote source snapshot.

**ONE KMS signature cannot satisfy this protocol's six fresh request signatures.** `createMarketplaceRequestProofSigner` signs canonical bytes containing method/path, exact body hash, Firebase Authorization hash, independently signed Gateway attestation hash, fresh random nonce and ≤30-second expiry. Changing any stage/body/session/attestation/nonce changes signed bytes. Backend independently verifies actual RSA signature, request bindings and durable nonce. A signed server-held grant could authorize a different protocol, but cannot produce these RSA signatures; no delegation/local production private key/bearer replacement is introduced. The earlier one-grant review contract remains historical SOURCE REVIEW, never activation authority.

Alternative implemented: a DIFFERENT default-OFF future authority for exactly six per-request sign attempts and six ordered stages, up to20 backend requests/20minutes, two synthetic actors, one Product/one managed photo. Existing KeyVersion /1 and immutable SPKI remain fixed. No key/version creation, no implicit approval, and no change to the historical permanent global ONE-sign tombstone or consumed status reader. No provider recreation/run-ID/grant rotation can renew the new global ledger either.

## Implemented behavior

- Existing lifecycle contract extended with a separately branded/WeakSet multi-sign SOURCE policy (`activationAllowed:false`); old one-grant validator untouched. New independent, server-held RSA approval verifier checks exact policy bytes/digest, public SPKI pin, mode, six-attempt cap and validity window. Only a successfully constructed branded verifier for the same policy can bind the ledger; callback-shaped “authorized:true” substitutes are rejected. Actual operator approval key/pin/custody remain unavailable/unverified; generated local keys are tests only.
- Native staging Firestore stage ledger uses the existing verified binding/allowed rate collection and maxAttempts3 transaction wrapper. One permanent global document per Gateway UID/KeyVersion/purpose (not runId). Reserve → atomic single sign claim → independently verified backend claim → confirmed stage advancement. Body/Auth/canonical-proof/session hashes and stage nonces are bound; no raw tokens or body are persisted. Two instances/concurrent attempts serialize; ordered stages, wrong policy/run rotation and replay fail closed. Pending/UNKNOWN and ambiguous outcomes never automatically retry. No TTL/delete/reset API.
- Separate durable status-read slots permit at most sign-version/sign-public/verify-version/verify-public per stage,24 exact GET attempts total. Recreating a reader cannot renew these slots. New independent reader transport enforces exact KMS endpoints, GET/no redirects/no cookies, bounded600ms/16KiB JSON, separate principal+UID, independently verified reader authority, metadata-derived credential port and durable budget before GET. Signer/mediator/backend identities are rejected as independent readers. Actual status is validated using the existing metadata/CRC/RSA/SPKI predicates; no fake ENABLED or stale cache.
- Existing KMS signing composition extended with a separately branded lifecycle signer. It requires actual pinned PEM and native branded policy/ledger, canonical proof, atomic attempt claim and fresh trusted key status before the existing CRC/RSA-verified signer. It never invokes/recreates the legacy one-sign transport. Missing PEM/status/context/authority blocks the new path.
- A separate backend public-key resolver has **no KMS sign credential/port**. It enforces the real immutable pin, kid, expiry and independently read verify-status. Future hosts require this branded resolver; a Gateway signer is not reused as the backend verifier.
- New server-held stage controller verifies Firebase actor/revocation through the existing Auth adapter on every stage (including Buyer orchestration while public backend reads remain guest-only), checks session stability, stage/path/visibility/Product scope, reserves before dispatch and bounds request/response bytes/deadline. It dispatches through existing HTTP mediation. Public Firebase tokens are not forwarded as IAM, and lifecycle reservation is server context, not an authorization header. Lost response/session drift/expiry cannot authorize retry.
- Existing secure backend integrates the optional native lifecycle admission **after** independently verified Google identity, canonical RSA proof and Firebase auth, **before** nonce/Product side effects. The same policy/ledger must bind the same Product and actors. Atomic backend claim prevents a signed-but-unreserved action or a second instance from dispatching twice.
- Release control exposes immutable principal/image bindings for all three roles. Existing assembly now requires all three to match approved host facts and rejects nested accessor facts. New separate mediator/Gateway/backend source factories stay OFF by default and require lifecycle/backend/key gates before exposing an enabled candidate. No listener, environment activation or image packaging/deployment is added; existing H2U OFF server/image is untouched.

## Exact changed source/test files

- `scripts/c2-h2-lifecycle-signing-status-contract.mjs` — blob `75a7f987de2687b378218f3f320b710eac1928e1`
- `scripts/c2-h2-lifecycle-stage-ledger.mjs` — blob `47140b97f3f80979088ec488e5ebd660be762999`
- `scripts/c2-h2-lifecycle-boundary.mjs` — blob `be9b8bd7fe5d8dacd17f7077cb286e66a1f6a310`
- `scripts/marketplace-gateway-request-proof.mjs` — blob `7abc5d1624ccaa832bb9c94c40de31018a1c653a`
- `scripts/c2-h2-independent-kms-reader-ports.mjs` — blob `818df254328078ecbcceb6cc2eaabaa8198415b8`
- `functions/staging-marketplace/c2-lifecycle-stage-controller.mjs` — blob `491b9deba9419f594f7780a117900370d7425f54`
- `scripts/c2-h2-private-gateway-signing-composition.mjs` — blob `90e480cc6faefb85f47baf49f55f19c9dac8ff4f`
- `functions/staging-marketplace/c2-h2-gateway-host-source.mjs` — blob `5502fe686679c66aa8b0925c29f6754bc487e086`
- `functions/staging-marketplace/c2-g2g6-enabled-host-source-assembly.mjs` — blob `aa72d583287e5ea7fe49325bcfb3a508f55a250d`
- `functions/staging-marketplace/c2-future-role-hosts.mjs` — blob `22b5b195d0810605cbf5b7f3ccddf2ac6d228342`
- `scripts/c2-h2-lifecycle-approval.mjs` — blob `dbcc7ab39b1d2973d692343f455f6f2260aaeb6d`
- `tests/integration/step05-lifecycle-http-fixture.mjs` — blob `4f18b63fd42ef3c90d77e11df9293f14aa8a0da5`
- `tests/integration/step05-c2-bounded-lifecycle-new.test.mjs` — blob `8a84dad8be289b83c962dada6c3a7f61a2f8fc8a`
- `scripts/c2-h2-independent-kms-version-status.mjs` — blob `f8183c9417eb017c2b646366ccf90dc5522aff09`
- `scripts/c2-h2-lifecycle-kms-status.mjs` — blob `5497f363929e1a4ec16c23910c0880dbaf733d66`
- `scripts/c2-enabled-release-control.mjs` — blob `2e10afb342d416f30ad3dceb97bfae91a050e7f0`
- `functions/staging-marketplace/secure-product-pipeline.mjs` — blob `501b2a50b11682c263517305749d3a8487ab89fb`

Existing media, moderation, photo ownership/revision, public projection, signed cursor, Firebase enforcement, guest/run budget, cleanup/version reconciliation, repository receipts/idempotency and UI session modules were reused. No broad rewrite or dependency installation.

## Actual NEW verification — not hosted acceptance

Local Windows Node `v26.13.0`, isolated current-remote snapshot, SDK-shaped transaction/Auth/KMS/metadata/JWKS doubles and ephemeral locally generated RSA keys. Three actual localhost HTTP servers model mediator→private Gateway→backend; simulated IAM signature stripping is explicitly NOT real Cloud Run enforcement. SDK-shaped serialized transactions model atomicity, NOT Firestore Emulator/live conflict evidence.

All **18 distinct NEW cases** now have passing evidence. There was intentionally no final blanket rerun: affected cases were selected after each change; four unchanged cases retained their earlier pass. Previous12 G2–G6 +7 lifecycle results were not rerun or relabeled.

All commands use `node --test --test-isolation=none` and `tests/integration/step05-c2-bounded-lifecycle-new.test.mjs`:
1. Initial load failed before tests due to a literal newline escape in the new helper; fixed.
2. First substantive full NEW file run:11 cases,10PASS/1FAIL, exit1,1982.7188ms. Failure exposed a real response-body cancellation bug after a successful HTTP response.
3. `--test-name-pattern="NEW six-stage"`:1PASS, exit0,791.7221ms, after buffering the bounded response inside deadline. No blind full rerun.
4. `--test-name-pattern="NEW (future|server-held|durable|ambiguous|ledger|six-stage|stage controller|lifecycle status|changed release|unknown HTTP|independent lifecycle|assembly rejects)"`:12PASS, exit0,720.3713ms, after adding branded approvals/ledger, durable read slots and host bindings.
5. `--test-name-pattern="NEW (durable|canonical|six-stage)"`:3PASS, exit0,660.9976ms, after real backend stage admission was wired.
6. `--test-name-pattern="NEW (independent reader|independent lifecycle|reader deadline)"`:3PASS, exit0,1009.331ms, after independent reader identity/deadline hardening.
7. `--test-name-pattern="NEW release photo-owner"`:1PASS, exit0,641.2401ms, checked against the changed backend dependency.
8. `--test-name-pattern="NEW (future multi-sign|backend key resolver|stage controller)"`:3PASS, exit0,622.1269ms, after separating least-privilege verification keys.

Every passing selection:0FAIL/0SKIP/0CANCEL. Counts above are execution counts, **not** additive unique coverage. Final unique18: OFF roles; actual approval RSA/pin/expiry; two-instance reserve/sign/backend replay/concurrency; ambiguous transaction/sign-result quarantine; wrong actor/nonce/forged verifier; canonical proof forgery/body/session tamper; wrong signed audience; exact independent GET authority/budget/403; six-stage HTTP journey; session switch/expiry; photo-owner/quota/cleanup revision; durable ordered read slots; immutable release roles; unknown HTTP quarantine; wrong PEM/no budget renewal; getter/forged signer rejection; uncooperative600ms reader; backend wrong-pin OFF.

The six-stage local journey actually completed save draft → approved managed photo publish → Buyer list/detail with private contact/owner fields filtered → Seller edit → withdraw. Exactly6 proof signatures and6 requests on EACH of three localhost hops; durable stage record COMPLETE/signAttempts6; Product public view absent after withdraw; fresh ledger cannot replay. Native Firebase/Google/KMS status/auth responses were simulated. No successful test with the real pinned KMS PEM or actual lifecycle signer is claimed; wrong generated PEM correctly stays blocked. Existing normal Product backend auth/privacy/media logic was exercised; Node24/real Cloud/Firestore conflict/hosted acceptance were not run.

## Remaining exact gates / ONE consolidated future authorization packet

Source progress is substantial; **live provider bindings and hosted acceptance remain OPEN**, not Step05 DONE:
- Actual independently named reader SA/UID, runtime identity proof, least-privilege exact-version/public-key read authority and authenticated reader service transport. No supplied credential label is independent proof. Do not broaden Gateway signer to signerVerifier or use Owner OAuth/SA JSON keys.
- Real pinned public PEM/status; independently held approval public-key pin and signed exact multi-sign policy; separately approved release digest with immutable new enabled images and verified source provenance/rollback/security evidence. Historical OFF images/approvals cannot activate this candidate.
- Actual per-process metadata/JWKS/HTTP transports and trusted request-local signing/verification stage context, same native permanent ledger, Firebase SDK staging/default DB and synthetic actor grants, durable guest/run budgets, media/moderation/photo state, exact revision/dependency cleanup evidence. No in-memory production substitutes.
- Exact private service/revision/SA UID/Invoker/audience/internal-only ingress and fresh hosted health evidence. H2AD9 NOT_FOUND/zero health logs is unresolved; no definite source cause was established, no source “fix” or new probe is claimed. H2AF cleanup remains PASS.
- Only after these concrete identities/digests/custody inputs exist, present **ONE** bounded private-staging acceptance packet: exact existing KeyVersion /1, at most6 separately approved sign attempts, at most24 exact status/public-key GET attempts, at most20 Product requests within20minutes,2 synthetic actors/1 Product/1 photo; exact native document scopes; source/revision/image pins; STOP on any error/unknown/mismatch; permanent evidence retention and no automatic retry/reset; separate exact cleanup consent. Missing reader identity/permissions/new image pins mean this packet is **not yet executable approval**. No new key/version, public IAM/ingress, production or broad resource permission is implied.

Highest-impact next action: finish that one concrete host/provider/authority packet (including request-local context and existing-or-new independent reader identity) before requesting any live acceptance execution. No repeat of completed diagnostics, scans, builds, IAM audit or Scheduler probes is needed for this source checkpoint.

## Preservation and cost

No Cloud request, KMS sign, staging/live Firebase/Firestore/Storage data, IAM/SA/key/version, Rules/Billing, Registry, image build/pull/scan, CI dispatch, Scheduler probe, deploy or production activation occurred. No new paid resource/usage was incurred by this source batch; ordinary coding/GitHub usage only. Future KMS/reader/Cloud Run/Firestore usage would be separately approved and priced; no zero-cost hosted claim. Push messages use `[skip ci]`; workflows were not modified.

All historical commits, consumed markers, prior results, original ONE-sign/status controls, H2AF cleanup, H2AD9 unresolved health, security HOLDs and15-step sequence are preserved. Step05 ACTIVE; H2 hosted acceptance NOT VERIFIED; production OFF / NO-GO.
