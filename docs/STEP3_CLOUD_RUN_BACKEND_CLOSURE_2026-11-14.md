# OLDX Final Strategic Plan — Step 3 closure plan (2026-11-14)

**Scope:** Step 3 of `docs/OLDX_FINAL_ARCHITECTURE_AND_COST_DECISION_2026-11-07.md`: make existing disabled/emulator-locked trusted SDK/HTTP adapters Cloud Run-compatible, without production activation; review IAM, identity, permissions, audits, transport.

**Decision:** finish the source-only portion efficiently; preserve final security acceptance gates. This document does not authorize any live cloud read/write, permission modification, token minting, deployment, fixture execution, or billing. Only `security-hardening-review`; Production **HOLD / NO-GO**.

## Verified/reusable material — do not redo

1. Existing Product/Store/Service/Chat/Inbox/Provider SDK and HTTP composition and focused isolated tests already described in the launch decision register and handoff. Reuse the present contracts; no wholesale rewrites.
2. Private Cloud Run `oldx-owner-read` disabled revisions, IAM-enforced invocation and health/disabled endpoint responses are *historical staging evidence*, not enabled application acceptance. See `docs/OLDX_CURRENT_HANDOFF.md`.
3. Reviewed Phase B exact-identifier fixture runner, default-disabled `LIVE_EXECUTION_ENABLED=false`, fixed allowlist, journal/conditional Firestore cleanup and supervised Auth cleanup option 2. Read-only and offline review tools already exist.
4. 2026-11-14 owner GUI screenshots confirmed enabled narrow `getAccessToken` custom role on the exact runtime service account, no listed user-managed keys, custom Firestore role containing `datastore.databases.get`, `datastore.entities.create/get/update` and no entity-delete, and configured condition expression `resource.name == "projects/oldx-staging/databases/(default)"`. No additional token grant or repeated IAM listing is indicated.
5. Policy Troubleshooter **Allow** granted, but overall decision **UNKNOWN** due to inaccessible Principal Access Boundary evaluation. Do not report effective access PASS or broaden IAM to solve a diagnostic UNKNOWN.

## Minimal sequence (only next unmet gate)

**3A — Source contract closure, no cloud access.** Review current auth/token validation and revocation, owner/participant identity, private DTO boundaries, trust limits, rate/quota/audit logs, HTTP response and retry semantics, client session invalidation and existing Cloud Run ADC configuration. Run only impacted offline tests for a real change; avoid repeating broad suites solely to restate an already recorded pass. Record exact code gaps versus already implemented controls. Fix the smallest source gap if safely testable. Confirm every executable live entry remains default-off.

**3B — Offline security evidence packet.** Consolidate the existing IAM screenshots, role scope, token-binding evidence, scripts, exact resources, cleanup ownership, current immutable SHA and stop conditions into one packet. Label **configured** versus **effective** rights separately. Avoid asking the owner to repeat console screenshots or paste long commands. A condition expression is configuration evidence, not demonstrated database isolation. Database IAM may be broader than per-document scope even when a fixture runner has exact-ID allowlists.

**3C — Separately approved bounded read-only acceptance.** Only if necessary to finish Step 3 and after exact owner approval, evaluate access from the intended operator and service identity. Prefer single minimal preflight over repeated exploratory attempts; show exact project, principal, reads, expected output, cost/risk, and what constitutes BLOCKED. Do not access live records without approval. If Google permission diagnostics remain UNKNOWN, stop and report precisely; don't repeat an unsupported tuple or silently change IAM.

**3D — Separately approved staging mutation / negative-permission acceptance, only when strictly necessary.** Requires a new, specific approval of exact SHA, synthetic IDs and two Firestore paths, creation/update/cleanup commands, active owner/operator, retention and same-day recovery window. `--execute` cannot be used while hard-disabled; no unilateral change to the gate. Verify intended runtime GET/CREATE/UPDATE, DELETE-denial and actual database isolation, request/audit/transport behavior, and operator cleanup, and record absence of all fixtures after supervised cleanup. No owner-read activation without its own gate and approval. Auth cleanup lacks an atomic UID-generation precondition; stop on ambiguity, journal before delete, no retries.

**3E — Source closure / acceptance decision.** Mark Step 3 **SOURCE-READY** only after targeted source tests and code review support it; mark Step 3 **STAGING-ACCEPTED** only when 3C/3D evidence and their separate approvals are complete. If blocked on owner permission, leave `STAGING-ACCEPTED = NO` while continuing permitted source work for later strategic steps. Do not call a healthy disabled Cloud Run service live-ready.

## Current result / immediate action

- **Configuration evidence:** recorded; avoid replay.
- **Live runtime token generation:** unverified.
- **Runtime Firestore GET/CREATE/UPDATE and DELETE denial:** unverified.
- **Effective named database isolation / PAB:** unverified.
- **Operator exact-ID cleanup permissions and fixture absence:** unverified.
- **Approved fixture execution:** not granted; hard-disabled.
- **Production:** HOLD / NO-GO.

**Next coding action:** use repo-only source review to identify the first concrete unresolved Step 3 issue and run targeted offline tests before proposing any cloud operation. If existing source already satisfies an item, record evidence rather than edit it. Keep cost and developer credits minimal. No duplicated manual IAM investigation.
