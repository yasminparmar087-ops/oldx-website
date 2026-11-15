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

### 4A. 15-Nov Step 02: numerical hosted V2 budget candidate (PROPOSAL, not authorization)

The following is one **conservative planning scenario** for G8 of the EXISTING V2 review packet, not an executable runner, billing cap, live consent or a new release plan. All new operations remain forbidden until exact source/image/recovery evidence, owner-specified consent and enforcement are complete.

| Dimension | Proposed limit for one supervised staging session | Must be proven before activation |
|---|---|---|
| Project/identity | ONLY oldx-staging, asia-south1, Firestore (default), named invoker and runtime service account under Yasmin | Fresh staging billing-link/credit/usage status and IAM; never touch production or create a secondary database |
| Time | At most 60 minutes, with an additional named supervised cleanup/rollback window | Monotonic execution guard, owner present, backup/preimage and verified rollback permissions before first mutation |
| Cloud Run | Request-based example: 1 vCPU, 512 MiB, minimum 0, maximum 1, concurrency 1; one new reviewed digest/tag at 0% MAIN traffic | Actual billing mode, request timeout, source-to-image provenance, protected invoker and original 100/0/0 traffic verified |
| Operations | At most 200 attempted HTTP invocations (including failed requests and retries) and 1,000 billed instance-seconds | Explicit versioned counters and fail-closed STOP; billing metrics can lag, so these are NOT platform-enforced spending limits |
| Firestore | Illustration: 2,000 document reads, 1,000 writes and 20 deletes including counters/cleanup | Runner counters must include transaction retries and index reads; only approved exact synthetic IDs, no other customer data |
| Auth/logging | Two approved synthetic Auth UIDs; propose 10 log queries, 2 returned entries per query | Need separately reviewed quotas/counters and real per-SKU billing; log result limits do not limit ingest, storage or query scanning |
| Cost | Propose a ₹100 incremental gross-spend escalation/STOP threshold for this one session, NOT YET OWNER-APPROVED | Reliable account-level gross usage observations and automated/manual STOP; monthly ₹2,000 alerts alone DO NOT cap spend |

**Transparent public-list-price arithmetic (NOT an invoice or all-in maximum):** Current published Cloud Run Tier 1 request-based rates are USD 0.000024/vCPU-second, USD 0.0000025/GiB-second and USD 0.40/million requests. For a hypothetical 1,000 active seconds at 1 vCPU + 0.5 GiB and 200 requests: CPU **USD 0.024000**, RAM **USD 0.001250**, requests **USD 0.000080**; Cloud Run subtotal **USD 0.025330**. Firestore *Standard* list pricing is USD 0.03/100k reads, USD 0.09/100k writes, USD 0.01/100k deletes: an illustrative 2,000 reads + 1,000 writes + 20 deletes costs **USD 0.001502**. Combined modelled Cloud Run+Firestore subset: **USD 0.026832**. Assuming only for illustration an exchange rate of INR 90 per USD and 18% tax, this subset is **approximately ₹2.85**. This INR assumption is NOT a verified exchange rate, account quotation, cost ceiling or guaranteed tax treatment.

**Excluded and potentially material costs:** Cloud Build and Artifact Registry image pushes/scans/storage, IAM Credentials and Firebase Auth use, Cloud Logging ingestion/scanning/retention, network egress, Firestore storage/index-entry reads and transaction amplification, cold starts/idle minutes outside model, preexisting services and other linked-account usage, local cloud SKUs and taxes. Free tiers/credits may reduce costs but are NOT verified for this project. Actual monthly billing and billing account project linkage have not been freshly read. A proposed ₹100 human STOP is NOT an enforceable ₹100 hard cap.

**Owner must clear these hard stops before any live staged V2 trial:**
1. Fresh **read-only** owner check of the project-linked billing account (redact account number), current gross usage and billing plan, active credits, service CPU/memory/billing mode, Logging/Artifact/Auth charges and whether a **service-specific spend cap budget** is supported and already configured. No billing changes or service enablement authorized.
2. Versioned V2 runner/source/image must independently prove **real** request/runtime/Firestore/Auth/Logging counters and fail-closed abort plus a **separate** supervised same-session four-ID cleanup. Existing runner is hard-OFF; no blind toggle or V1 one-shot reuse.
3. Fresh private disabled service+IAM preimage, zero-main-traffic new tag, exact immutable image provenance, correct runtime/invoker, and **both** approved rollback mutations (remove only new tag and restore original disabled template); independently confirm traffic 100/0/0 and each exact fixture absent. Stop on partial writes, collision, uncertain Auth UID cleanup, missing logs, no trustworthy cost reading or drift.
4. Preserve newer owner evidence without repetition: observed one-path runtime DELETE 403, authentic published deny-all Rules match and protected staging 18/18 preflight. Five Firestore database IAM Policy Troubleshooter HTTP400 results are **UNKNOWN**, not denial/grant; cross-database isolation and real CREATE/UPDATE remain UNVERIFIED. No extra database, repeat Policy Troubleshooter, credential/DELETE attempt, or IAM widening to force a PASS.
5. Require separate action-specific Yasmin approval later for fresh billing read, new image/tagged deploy with 2-part rollback, named invocations/token mint and synthetic data-plane operations. This packet and generic “continue” do NOT authorize any of them.

**Sources checked 15 Nov 2026:** https://cloud.google.com/run/pricing (Cloud Run Tier 1 request-based list prices), https://cloud.google.com/firestore/pricing (Standard document operations), https://docs.cloud.google.com/billing/docs/how-to/budgets (alerts-only budgets DO NOT cap spend). Google also describes service-specific spend-cap budgets at https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps; **availability and applicability to OLDX are unverified**, and none is newly enabled here.

**Decision after this calculation:** G8 remains BLOCKED until owner/account-specific pricing and genuinely enforced counters/recovery are checked. No cloud operation, new CI run or code activation was performed by this document. Step 02/15 ACTIVE; staging hosted NO-GO; production HOLD/NO-GO.


When ready, ask Yasmin for **separate, concise approvals** covering (a) read-only config/log/identity inspection, (b) new container publish and 0%-traffic tagged deployment plus both rollback mutations, (c) named invocation/token mint and (d) exact synthetic create/update/delete/quota tests with supervised cleanup. A generic “continue” or yesterday's spent approval authorizes none of these.

### 4B. Owner-observed billing/Cloud Run read-only snapshot (15 Nov ~20:24 IST)

**G8 PARTIALLY EVIDENCED — NOT READY OR AUTHORIZED.** The owner supplied actual Google Cloud Shell/Console screenshots showing staging project billing linked and enabled, linked account open, and account Overview trial status. The billing account lists **two linked projects**, so its **Cost ₹0.04 / Savings ₹0.04 / Total ₹0.00** and displayed **No-cost Free Trial credit ₹28,569 / 87 days remaining** are ACCOUNT-level observations, **not oldx-staging-only totals**, nor confirmed current service/SKU costs or a spending cap. Do not copy the visible billing account ID. A separate "Active credits: 0" indicator cannot be substituted for the explicitly shown no-cost Free Trial credit. Gross project-only costs and credit application remain UNKNOWN until an OLDX-filtered Reports view.

Actual Cloud Run sanitized service template for oldx-owner-read, asia-south1: 1 CPU / 512Mi, concurrency=1, timeout=30s, request-based mode **inferred from default/missing cpu-throttling annotation**, correct runtime-SA identity, latest-ready oldx-owner-read-00003-nus, and unchanged protected traffic 00001-8kr=100% / 00002-tid healthcheck=0% / 00003-nus step3rc14=0%. **Important variance against proposed max1:** current maximumInstancesService=20, maximumInstancesRevision=1; both minimum-instance annotations NOT_SET. Do not pretend max20 is max1 or assume a new revision inherits max1 automatically. Never change the existing service-wide max20 to max1 based on this packet: that would be a live infrastructure mutation needing separate impact review, rollback and explicit owner consent.

**Remaining narrow informational task:** owner opens Billing > Reports, filters exact Project oldx-staging, date 1–15 Nov 2026, groups by Service, and sends a screenshot showing charges/credits if available. Check existing Budgets and caps read-only: alerts-only vs a truly enabled and applicable enforced spend cap. The proposed ₹100 STOP / monthly ₹2,000 preference remains *unapproved and not a hard limit*. If authentic project charges, ceiling, fresh disabled revision/rollback and hard run counters cannot all be reviewed, preserve G8 BLOCKED and V2 hosted NO-GO. Neither Cloud Shell tool output nor the account Overview gives real per-project SKU spend on its own.

**Status:** Source-only evidence update; no IAM, Cloud Run config, billing or Firebase changes; no extra CI. Step 02/15 ACTIVE, staging hosted NO-GO, production HOLD/NO-GO.


### 4C. Project-specific current-month cost is verified; spend-cap and V2 limits still not proven

**New actual owner Billing Reports evidence, 15 Nov ~20:50 IST:** With **Group by Project**, current-month charge period and savings (All), the explicit `oldx-staging` project row shows **usage cost ₹0.04, other savings −₹0.04, subtotal ₹0.00**. Bottom total ₹0.00, Free Trial credit ₹28,569 visible. This is project-specific billing evidence at report time, NOT just the account-wide URL context or an assumed cost allocation. Earlier Service grouping showed Cloud Run ₹0.04 before savings but did not show project filtering concurrently; treat exactly which billed SKU drove staging's ₹0.04 as **NOT separately verified**. Reporting can lag actual consumption.

**G8 remains BLOCKED** notwithstanding the small historical bill: current Cloud Run service maximum **20** while existing revision maximum **1**; source G8 proposed 200 attempts, 1,000 instance-seconds and ₹100 human STOP are not independently enforced; new V2 revision min/max/image provenance and complete rollback journal still unverified; exact project gross spend **so far** is not a reliable prospective cap. The user may read **Billing → Budgets and caps** to distinguish ordinary alerts from actually configured enforceable service-specific spend cap, but must not edit/create/enable one on this evidence. No assumption that Trial credit can safely cover unbounded staging tests.

**Next:** owner screenshot of **Budgets and caps** (read-only, redact billing account details); then resolve real cost enforcement and test counters in existing G8 plan. No new checker, Cloud IAM/Rules/Billing/Run mutation or old probe rerun.

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
