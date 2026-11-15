# OLDX Step 3 — Hosted Owner/Buyer Acceptance V2: independent review gates

Date: 2026-11-15  
Status: **SOURCE-ONLY REVIEW PACKET — NOT AN EXECUTABLE APPROVAL**  
Repository/branch: `yasminparmar087-ops/oldx-website` / `security-hardening-review`  
Operator for any later expressly authorized action: Yasmin Parmar (`yasminparmar087@gmail.com`)  
Project: `oldx-staging` / `asia-south1` / Cloud Run service `oldx-owner-read`  
Production (`oldx-1c983`): **HOLD / NO-GO**

## 0. Current, evidence-based position (do not redo)

- On 2026-11-15 the owner authorized **one** prior supervised staged `ownerbuyertrial` data-plane attempt. It finished **STOP**, not accepted. Four exact synthetic resources were later observed `ABSENT_AT_CHECK_TIME` with deletion acknowledgements; do not reset or reuse its private journal.
- The owner then executed two-step rollback and observed `ROLLBACK_VERIFIED_PASS`: remove only `ownerbuyertrial` tag, restore original private disabled service template, preserve original traffic `oldx-owner-read-00001-8kr` 100%, `healthcheck` `oldx-owner-read-00002-tid` 0%, `step3rc14` `oldx-owner-read-00003-nus` 0%, service IAM unchanged. This is historical **owner screenshot evidence**; not a claim that Cloud API was independently checked again now.
- The consumed environment-variable approval path is **hard disabled** in both `scripts/phase-b-fixture-session-v1.mjs` and `scripts/phase-b-owner-read-acceptance.mjs`. Fixture-only execution is also off. Previous `ownerbuyertrial`/revision `oldx-owner-read-00004-jus` and its image MUST NOT be treated as a freshly approved V2 target.
- Source-only classification now emits fixed, nonsecret failure stages **only after** the runner has confirmed four resources absent and fsynced its journal completion. That cannot recover the hidden reason for the already-stopped V1 session.
- `inspectCorrelatedHostedEdgeDenial` and `reviewScopedHostedDenialLogShape` are **offline evidence-structure verifiers**, not an authenticated Cloud Logging reader. They may return `MATCH` or `SHAPE_MATCH_ONLY` from mocked data. **Neither result establishes a real Cloud Run denial or authorizes any live request.**
- GitHub Safety CI for source commit `976d5778132db1835caf94479b18c26a8266dd66` finished **SUCCESS** (run `43701066486`); this is offline/emulator/browser evidence, not staging hosted acceptance. Later docs-only CI may still be running.

This packet supersedes older **unexecuted** V1 proposals where they conflict with the consumed authorization, test outcome, or verified rollback. It does **not** overwrite the V1 historical audit.

## 1. Decide readiness in this exact order, with no live operation yet

| Gate | Requirement before any new V2 execution | Currently supported result |
|---|---|---|
| G1 — Source | New independently reviewed runner revision and exact Git SHA; its specific execution gate remains default **OFF** until a new, scoped consent, with privacy-safe stage diagnostics | **PENDING**; V1 gate permanently OFF |
| G2 — Runtime image | New source-to-container provenance, immutable OCI index digest and verified canonical amd64 child, with reviewed Docker runtime | **PENDING**; old frozen image is V1 evidence only |
| G3 — Target | New unique tag, new revision as assigned by Cloud Run (never invent its name), audience and tag URL independently checked; no production/main-traffic change | **PENDING** |
| G4 — IAM | Dedicated named invoker, runtime service identity, no public principal, no broadened roles; configured conditional Firestore rights distinguished from **effective** DB isolation and DELETE denial | **PENDING EFFECTIVE PROOF** |
| G5 — Logging | Independently authenticated, project-scoped Cloud Logging reader; exact one-trace/one-entry request evidence (revision, service, URL, method, status, time, platform denial); no proof from headers or caller-supplied JSON alone | **PENDING** |
| G6 — Fixture lifecycle | New session identity and **new private create-once journal location**; owner-reviewed precise synthetic user/document identifiers, provenance and conditional deletion; no V1 journal deletion or reuse | **PENDING NEW CONSENT** |
| G7 — Supervised recovery | Fresh private sanitized service/IAM backup; validated restored disabled YAML; one named operator actively present for immediate cleanup and two-stage rollback, exact no-drift checks | **PENDING FRESH CHECK** |
| G8 — Budget and duration | Explicit finite request/time budget, max instances/min zero, spend monitoring, limits on Auth/Firestore/Cloud Logging calls, stop on ambiguous cost; alerts not a hard spend cap | **PENDING OWNER LIMITS** |
| G9 — Acceptance | Actual owner 200 private DTO, foreign buyer 403, missing/invalid Firebase 401, disabled route 503, anonymous invoker edge denial, no-store/rate behavior; separate negative permission/database-isolation evidence | **UNVERIFIED** |
| G10 — Closure | End-to-end exact-ID cleanup all absent; tag removed; original disabled template restored; traffic 100/0/0 and IAM unchanged; result independently reviewed | **PENDING FOR ANY FUTURE TRIAL** |

**A pass on G1–G8 makes only a candidate ready for a specific owner decision. It is NOT permission to deploy, mint tokens, invoke an endpoint, create fixtures or run the harness. G9 and G10 alone can establish a hosted decision.**

## 2. V2 Cloud Run denial — provenance, not just matching strings

The existing V1 hosted `invoker-denied` path requires a blank-body 403, while the V1 preflight accepts nonempty Google Frontend HTML **only if** a separately correlated request log proves platform denial. A simple `status=403`, `server=Google Frontend`, trace header, or simulated JSON log is **insufficient**. Do not loosen these controls simply to turn a STOP into a green test.

A future V2 harness must do all of the following before claiming platform-authentication denial:

1. Issue one reviewed unauthenticated **GET /health** to a newly verified, unique 0%-general-traffic tag URL, with a fresh 128-bit request trace, no Firebase/Google credentials in this denial request.
2. Collect the response within an approved short deadline; retain raw bodies and tokens only in private ephemeral process memory, never CI artifacts, public logs, commits, screenshots or chat. Ensure no redirect and an actual nonempty HTML 403 if using the HTML route.
3. Use a **separate** authenticated Cloud Logging query under Yasmin's approved identity, scoped to `oldx-staging`, trace and a narrow timestamp interval; capture all potentially conflicting records (request limit at least two), not just entries pre-filtered to matching revision/403.
4. Reject missing/duplicate/stale/nonmatching entries. Require the expected log name, `cloud_run_revision` resource, project, service, **actual new revision**, requested tag URL/method/403, trace and platform denial text. The log-reader's authenticated invocation and authorization must be independently established; a source callback may otherwise fabricate the same objects.
5. If Cloud Run IAM rejects a call before it is logged, or Cloud Logging cannot provide this evidence, classify **UNVERIFIED**. Investigate a separately reviewed alternative without granting more IAM or silently accepting a 403.

Current source functions are intentionally `SHAPE_MATCH_ONLY`. Before a real V2 harness, review any direct gcloud/Cloud Logging reader invocation, account configuration drift, transport timeout, log volume/cost, and exact provenance capture. **No standalone source unit test can demonstrate actual cloud log provenance.**

## 3. Supervised fixture and rollback contract

- **No old replay:** V1's private `~/.oldx-phase-b-hosted-v1` journal, prior session ID and `ownerbuyertrial` tag/revision are historical records. Do not rename, remove, wipe or mutate them to bypass create-once protection. A V2 journal requires a *new* nonoverlapping private directory, exact reviewed schema and code, and its own explicit consent. Avoid reusing the old four resource identifiers absent a new owner decision; even if the owner chooses the same exact IDs, establish a new separate journal and provenance check.
- Exact owner-approved synthetic Auth UIDs and Firestore document paths only. Create and verify under a bounded separate session; use new session marker and independent original create/updateTime evidence, password-protected synthetic users and short-lived tokens. Do not write or inspect actual user data.
- Negative DELETE-denial, different-database IAM condition proof, runtime transaction/rate counters and quota failure simulation must be separately scoped. **A custom IAM role lacking `datastore.entities.delete` is configuration evidence, not a demonstrated delete denial or per-document limitation.**
- Journal each possibly ambiguous mutation **before** the call. On collision, changed provenance, unexpected status, timeout after possible write, token expiry, unknown rollback state, unapproved extra resource or cost threshold: **STOP**, preserve immutable evidence; no blind replay/cleanup. Pre-review exact-ID manual recovery by Yasmin.
- If the session can complete, verify each fixture is absent by independent GET/lookup, then stop tagged requests, remove **only the new tag**, compare traffic, restore the previously captured **original disabled** Cloud Run service template after a fresh no-drift check, compare IAM and original 100/0/0 protected traffic. These are two distinct mutations and a replacement may add a disabled revision; do not assume atomic rollback.
- The old backup at `~/.oldx-hosted-rollout-before` is V1 historical evidence. Create a **fresh private V2 preimage** under a new location only after specific owner approval and no unrelated drift. Never commit or paste IAM members, env secret values, tokens or private journals.

## 4. Limit and approval packet — proposed, NOT approved

Before requesting a V2 live-test decision, fill these fields from **fresh, independently verified evidence**. Unknown values are hard stops, not placeholder permissions:

- New reviewed source commit: **TBD**
- New immutable OCI image index + canonical child: **TBD / TBD**
- Current verified disabled service template and IAM fingerprint: **TBD**
- New unique tag and assigned revision/verified URL/JWT audience: **TBD / TBD / TBD**
- Dedicated operator/invoker/runtime SA scope and effective IAM isolation/delete proof status: **TBD**
- Exact Auth UIDs and two document IDs for a new session: **TBD, requires new owner decision**
- Fresh private journal path and cleanup operator: **TBD**
- Maximum authorized clock time, request count, bounded Cloud Logging reads, write budget, instance ceiling and explicit spend/stop amount: **TBD**
- Fresh private service template backup/rollback file and independent no-drift check: **TBD**

A dated prior plan proposed a *planning envelope* of up to **200 attempted requests per hour and 1,000 billed instance-seconds**; these are **not automatic execution limits or spending authorization**. Confirm the current actual cloud prices and current billing/usage before any cost-bearing approval. The configured monthly ₹2,000 alert is not a hard cap.

When ready, ask Yasmin for **separate, concise approvals** covering (a) read-only config/log/identity inspection, (b) new container publish and 0%-traffic tagged deployment plus both rollback mutations, (c) named invocation/token mint and (d) exact synthetic create/update/delete/quota tests with supervised cleanup. A generic “continue” or yesterday's spent approval authorizes none of these.

## 5. Evidence matrix and decision

| Evidence source | Allowed conclusion |
|---|---|
| Existing green GitHub CI, emulator tests, masked mock logs | **SOURCE-VERIFIED ONLY** |
| V1 rollback screenshot and four-absent journal | **V1 CLEANUP/RESTORE VERIFIED AT THAT TIME ONLY** |
| Fresh Cloud Run/IAM config snapshots | **CONFIGURED STATE VERIFIED**, not per-document runtime rights |
| Authenticated, trace-correlated Cloud Run log with reviewed provenance | **ONE VERIFIED EDGE-DENIAL PROBE**, not entire product |
| End-to-end named owner/buyer/denial/quota/isolation proofs, reviewed cleanup/rollback | **ELIGIBLE FOR OWNER STAGING ACCEPTANCE DECISION** |

**Present decision:** V2 not runnable or authorized; `STAGING HOSTED ACCEPTANCE = NO-GO`, `STAGING RELEASE = NO-GO`, `PRODUCTION = HOLD/NO-GO`. This document is informational source-only material and does not activate any test or service.


## 6. 2026-11-15 — reviewed offline CLI process plan (not a runnable reader)

Review-branch source `scripts/phase-b-v2-logging-process-plan.mjs` contains an **inert** `planOfflineV2LoggingProcess` helper. It has no `child_process` import, no shell command invocation, no network call, no credentials, and `executable: false` on both accepted and blocked plans. Only the exact eight arguments already produced by `reviewScopedHostedDenialLogShape` plus one active `AbortSignal` option are allowed. It rejects different project/account, arbitrary flags, unsafe trace/filter syntax, inverted/noncanonical dates, windows greater than 30 seconds, cancelled signals and extra parameters.

A valid *offline* plan fixes `gcloud logging read`, `--project=oldx-staging`, the intended owner account, `--limit=2`, JSON output, and no shell; it outlines an OS-level `execFile` timeout of **1,500 ms**, stdout/stderr buffer budget of **65,536 bytes**, and `SIGKILL` timeout signal. These values are conservative **proposed source guards**, not measured viable real gcloud startup latency nor guaranteed total-cost or subprocess-tree limits. A future separately approved executable implementation must enforce actual OS termination, isolate credentials, demonstrate the real authenticated principal and effective project permissions, bound retries/log-volume and refuse secret/trace disclosure. `--account` in arguments is a desired configuration flag, **not an attestation of identity**; a callback returning matching synthetic JSON remains `SHAPE_MATCH_ONLY`.

The focused offline regression file `tests/integration/phase-b-owner-read-acceptance.test.mjs` verifies the plan is produced **inside** the mocked reader callback while the signal is active, and rejects extra flags, production/account drift, injection, oversized time windows and stale/aborted signals. An intermediate test wrongly checked the signal *after* the adapter had correctly aborted it in its `finally` cleanup; the final source test moved that observation inside the reader callback, without weakening the guard. Source changes: `e0e4007665be847b602926e4fe9ef98bcf30c4d0`, `c31a47601ae164c83b3382558bd22fa5ebeebbe8`, `d36b29d9b14427024536db9fc86aedbb820d8c31`.

Before a future live reader is considered, an independent security review must pin the exact executable path/binary version, distinguish desired `--account` from authenticated principal provenance, validate process termination and output censoring in a no-cloud harness, and obtain a **new exact owner approval** for even a live read. No previous one-shot `ownerbuyertrial` authorization can be reused. `STAGING HOSTED ACCEPTANCE NO-GO / STAGING RELEASE NO-GO / PRODUCTION HOLD/NO-GO`.
