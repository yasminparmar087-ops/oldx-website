# OLDX Step 05 — owner-authorized SOURCE-ONLY kickoff, inspected product ports and minimum hosted vertical slice

**24 Nov 2026**, on `security-hardening-review` only. Owner explicitly authorized Step04 `DONE — DECISION-ONLY HOLD HANDOFF`; Step05 **source-only code review and planning** now authorized, but **LIVE hosted authenticated execution blocked**. This is a source-only checkpoint, **NOT** a new implementation, test pass, auth/Cloud change, integration proof or production release.

## 1. Step05 master requirement, unchanged

Master plan Step05 is **"ONE genuine hosted Product owner/buyer thin vertical slice incl. authenticated read/write/publish/withdraw, denials, quota and retry"**. Live exit: hosted positive and negative cases, independently authenticated evidence, bounded cost, exact synthetic cleanup and independently verified rollback ALL PASS. Transferred original Step04 technical gates (private A8 hosted OFF 503, effective IAM, Firestore SA `(default)` scope, 15 severe CVEs for enabled scope, manual cost preflight/STOP, traffic/recovery) remain hard prerequisites before live enabled Step05.

See [owner Option B approval and technical-gate handoff](OLDX_STEP04_OWNER_APPROVED_DECISION_ONLY_CLOSEOUT_AND_STEP05_HANDOFF_2026-11-24.md). **Do not** interpret Step05 source kickoff as permission to activate Firebase ADC/Product or deploy.

## 2. Actual reviewed source in GitHub current branch (not generic assumptions)

| Path / frozen blob SHA | What code currently exposes | Step05 implication |
|---|---|---|
| `functions/staging-marketplace/product-read-server.mjs`, `135e43d064c479a59a6f4b91a001c2bae9fb83f4` | Current Cloud Run Node HTTP server has health GET/HEAD, route **only** `/api/staging/marketplace/owner`, disabled `503` by default, bounded JSON/headers and POST; source explicitly says **no write or guest routes registered**. Its staging Admin initializer checks project, default DB, runtime SA/ADC, flags and dangerous environment. | Proven A8 OFF-only owner *read* adapter **is not** a hosted Product save/archive/publish/withdraw/buyer complete vertical slice. Do not claim it is |
| `functions/staging-marketplace/cloud-run-http.mjs`, `4fd07e1da7cc4b370d5d9ec19993f348110cc499` | Source-only generic Node listener supports exactly `save`, `owner`, `archive` paths; default `enabled=false` returns 503; injects handlers and bounds response to 65,536 bytes. Comment says **inactive**, no auto-open-port or Firebase init. | Potential reusable three-route transport, but **not proven actually composed/hosted**; avoid turning it on without release gates |
| `functions/staging-marketplace/runtime.mjs`, `749f4259068c4d9dd2f46706222c7a43ba47fb59` | Maps `save/owner/archive` to command runtime, token verification, atomic quota and Firestore repo dependencies only under `enabled=true`; exported env parser fails closed unless `OLDX_STAGING_COMMANDS_ENABLED=true`, `VERCEL_ENV=preview`, Firebase stage/project exact, valid rate vars, and publication separately gated. | Backend composition/route and security seams exist in source; actual hosted owner/buyer integration and data plane are **not independently proven** |
| `functions/staging-marketplace/bootstrap.mjs`, `87feb6ff40e5e67c4c06638ba7906dfc71bd8a9f` | Inactive deployment bootstrap; initializes Firebase Admin only after parsed staging gates; explicitly refuses when publicationEnabled true and emulator hosts set. | Source-only dependency-injection seam exists; **no permitted active runtime** in current task |
| `features/marketplace/product-integration.mjs`, `953509239ba7afec11f7101d3e7a307ea0f56475` | Pure UI orchestration with trusted injected `ports`, enabled=false by default, per-session cancellation, replay-safe requestId / unknown-outcome retry, owner draft `save(profile, draft/publish/withdraw)`, `archive`, owner/list/detail/inbox/chat read methods; no Firebase/fetch/storage globals. | UI contract is reusable but **trusted real hosted adapters and authenticated round-trip not verified** |
| `features/marketplace/product-integration-dom.mjs`, `9e5e8a583bbd404c093ee7c21e25f4d73c400128` | Existing Sell form and Product detail/inbox/chat UI are connected through the injected model; checks form save guards, photo readiness, session on/offline restoration. `enabled=false` default. | Prior browser/UI source and fixture tests are NOT equal to live authenticated Step05 integration |
| `tests/browser/product-integration.test.mjs`, `4ad1aa9c48b43fdd02c7f230e7546fea9121bc34` | Existing browser tests cover actual controls for draft duplicate-guard, Chat guest gating, logout/account switch, offline retry, navigation and owner recovery, multilingual/mobile. | Reuse these tests; don't rerun wide CI just to show source presence; if later modifying an adapter, target only relevant tests |

These are **specific source declarations read for this kickoff**, not new test execution or a claim of current deployed architecture. For backend methods not covered here (buyer/public access, external publication mapping), inspect their exact code paths before proposing edits.

## 3. Minimum source-only next steps — one pass, no architecture redesign

1. **Make one contract table of ports vs actual source routes**: UI `save/owner/archive/list/detail` plus buyer-facing/reads, runtime `save/owner/archive`, real A8 Cloud Run `owner` only, inactive generic listener three routes; distinguish served, implemented inactive, and absent/unknown. Review source for exact request/response DTOs, authorization, rate limit, receipt idempotency, conflict, public projection; never fabricate an endpoint.
2. **Trace the genuine Step05 happy and denial journeys offline:** seller sign-in → draft save → publish → seller reload → buyer guest/public listing/detail → buyer/seller authorization boundaries → seller withdraw/archive → retry after lost response → cancellation/logout → deterministic synthetic cleanup. Note publication is source-gated separately and the inactive bootstrap rejects publicationEnable true; not ready for a hosted pass.
3. **Decide smallest source changes only if required**: Prefer existing trusted ports and runtime; do not add unaudited direct Firebase client writes, mutable global state, unbounded retries or bypass IAM. Any source change must be branch-only and covered by minimal new local tests. No platform activation/Cloud operations.
4. **Keep release gate packet adjacent to any eventual enabled-test proposal**: real current effective invoker/Firestore SA, false flag preservation until specifically approved, new-scope 15-CVE disposition, ₹1,000 manual stop/₹2,000 unguaranteed goal, finite budget/authenticated resource cleanup/tag-only rollback and independently verified 503.
5. **Stop at exact source-only owner handoff** before any new paid or live staging operation; request distinct explicit owner approval for any actual enabled host, data-plane or Cloud write.

## 4. Current status

```text
STEP04_ADMIN_EXIT=DONE_DECISION_ONLY_HOLD_HANDOFF
STEP04_TECHNICAL_EXIT=UNMET_CARRIED_TO_STEP05_13
STEP05_NEXT=SOURCE_ONLY_CODE_REVIEW_AUTHORIZED
STEP05_SOURCE_KICKOFF=REPO_CODE_PATHS_INSPECTED_NO_TEST_EXECUTION
STEP05_LIVE_AUTH_OWNER_BUYER=BLOCKED
A8_R1_UNTAGGED=YES_AND_CONSUMED
CLOUD_BUILDS_SCANS_DEPLOYS_OR_BILLING_ACTIONS=NONE
PRODUCTION=NO_GO
```
