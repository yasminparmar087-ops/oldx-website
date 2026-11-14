# OLDX Step 3 — One-pass Staging Acceptance Decision Packet
Date: 2026-11-14
Branch: `security-hardening-review`
Status: **PREPARATION ONLY; STAGING NO-GO; PRODUCTION HOLD / NO-GO**

## Goal and invariant

Complete the Final Strategic Plan's Cloud Run-compatible Backend and Security Step 3 in the smallest evidence-supported number of sessions, without repeating already passed tests, expanding IAM to work around inconclusive diagnostics, changing production, or running unsafe fixtures. `LIVE_EXECUTION_ENABLED=false` remains invariant on review source. No live action is authorized by this document. Owner Yasmin must separately approve each currently unapproved cloud mutation, hosted activation and data-plane test after reviewing its *exact* version, operation, risk and cleanup.

## 1. Do NOT redo — reusable evidence

| Subgate | Evidence as of 2026-11-14 | What it does NOT prove |
|---|---|---|
| Local application packaging | Cloud Shell owner screenshot: Docker mirror `node:24-bookworm-slim` download succeeded; Docker BuildKit 13/13 FINISHED, `oldx-product-read-step3:local` local image; no source Dockerfile edit | Hosted revision deployment/activation |
| Local API fail-closed | Docker `--network none` run and in-container HTTP smoke: `/health` 200; `POST /api/staging/marketplace/owner` 503 `ENFORCEMENT_UNAVAILABLE`; `/unknown` 404; all PASS. Container cleaned via shell trap | Enabled owner read/Firestore IAM |
| Focused Node backend tests and production dependency audit | Owner Cloud Shell screenshot: 26/26 Node tests PASS, npm audit --omit=dev: 0 advisories. Separate 6/6 Auth fake integration PASS and earlier already documented offline runs | Any live permission or CRUD |
| Google Cloud configuration | Owner previously observed `--check-configuration` 10/10 MATCH; later `--cloud-preflight` progressed after correcting *local* gcloud active project to `oldx-staging`. One direct service invoker binding, 0 public bindings, pinned audience `https://oldx-owner-read-lqpaz3pd5a-el.a.run.app`, rollback baseline CONFIGURATION_MATCH | Effective invoker, inherited IAM or rollback execution |
| Anonymous edge denial | One pinned `healthcheck` tag anonymous GET returned Google frontend HTTP 403, HTML nonempty, no redirect | The verifier's correlated request log was `MISSING`, so `anonymousDenial.result=BLOCKED`; not logged-denial PASS |
| Runtime SA config | Enabled, 0 user-managed keys; `oldxProductReadFirestore` contains `datastore.databases.get`, `datastore.entities.get/create/update` and **no** entity delete. Binding limited by *configured* condition `resource.name == "projects/oldx-staging/databases/(default)"` | Actual effective Firestore condition, negative other-database boundary or entity delete denial |
| Operator token grant | Yasmin directly bound to narrow custom `iam.serviceAccounts.getAccessToken` role on exact runtime SA. Policy Troubleshooter direct Allow GRANTED; **overall UNKNOWN** due to PAB visibility | Actual access-token exchange, datastore operations or final effective access |
| Historical staging synthetic Auth | One separately authorized disabled/passwordless Auth probe was created, read, deleted and UID absence verified. Four target IDs previously observed absent in a dated, read-only preflight. | Current absence immediately before writes, four-resource CRUD/cleanup, enabled user sign-in/hosted acceptance |

## 2. Strict order; avoid rework

### Gate A — Source and evidence packet (no cloud resources)

- Verify exact reviewed branch SHA, repository cleanliness and current default-off `Dockerfile.product-read` / server.
- Treat Docker and unchanged focused suites as completed evidence; no image rebuild, repeat tests or repeated custom-role screenshots unless source or provider configuration materially changes.
- Compare documented missing items to code. **Do not interpret a cloud IAM Role containing create/update as read-only**; supported quota-counter transactions require narrow write authority.
- Identify exact requirements for the positive and negative hosted tests (owner, foreign buyer, unauthenticated, wrong-project/expired token; quota/audit, safe DTO), short-lived named invoker identity, and exact cleanup evidence.
- The latest GUI evidence supersedes older **missing getAccessToken grant** proposals in older sections of `docs/PHASE_B_PERMISSION_AND_APPROVAL_MATRIX.md`. Do not create another grant.

### Gate B — Non-mutating operator-ready preflight (no repeated exploratory probes)

- Owner-approved named operator/project only: `yasminparmar087@gmail.com` / `oldx-staging`.
- Confirm the specific current revision's service URL, tag, main traffic and IAM binding by reusing the latest valid record. Re-read *only if changed*.
- The last `--cloud-preflight` was `BLOCKED` **solely for anonymous log-correlation evidence** despite HTTP 403. Do not endlessly repeat the request. Determine whether a trustworthy log entry for this particular edge rejection is necessarily available. This is an evidence-design issue, not proof that the service is open or a reason to grant permissions. If the verifier's strict log check cannot be satisfied, keep that gate BLOCKED and propose an independently reviewable alternative; do not silently weaken a security test.
- For Firestore IAM, the configured (default) resource condition and PAB-incomplete allow result are **not proof** of true database isolation; avoid the previously rejected Policy Troubleshooter Firestore tuple. Define only a narrowly scoped, separately authorized runtime proof capable of establishing the needed positive permission, and preserve UNVERIFIED for negative scope when untestable.

### Gate C — Exact owner approval packet, *before* any staging changes

One compact decision bundle, with *separate lines/consents* for:
1. **Identity/token/invocation evidence:** exact operator, existing dedicated `oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com`, service, audience, token acquisition and *whether* one bounded hosted invocation is approved; no unreviewed token display.
2. **Runtime/Firestore evidence:** which exact `(default)` database operations, with any disposable ID needed and its own delete-denial risk; positive and negative expectations, and how condition isolation will or cannot be demonstrated.
3. **Cloud Run activation:** immutable code/image digest, tagged revision and env/identity, **0% main traffic**, allowed temporary IAM/revision operations, cost envelope, monitoring and complete manual rollback; approval not inferred from earlier conditional invoker setup.
4. **Fixture lifecycle and user auth:** exact two enabled Auth UIDs and two Firestore paths, two sign-ins, key handling, exclusive persisted journal, reviewed runner, fresh create-only preflight, cleanup operator and controlled same-session deletion. Prior *planning* consent and earlier one-user probe are not approval to bypass the source hard-off gate.
5. **Quotas/budget/traffic:** bounded 200-request / 60-minute / 1,000 billed-instance-second operational stop limits only if still compatible with the reviewed packet, **not** a guarantee of cloud billing cap, plus rate-limit counter ownership/cleanup and failure recovery.

Only relevant subsets should be requested once the exact executable evidence and risks are ready. A generic "continue" is not authorization for these mutations. No `--execute`, toggles, tagging, token mint, API enablement, service-account/IAM/Rules/Billing change or live Firebase read/write until the specific approvals.

### Gate D — One supervised acceptance session (not yet authorized)

Only after all Gate C exact scopes and rollback are approved:
- Fresh exact-ID collision read before create (previous absence is stale); stop on any EXISTS/UNKNOWN.
- Snapshot original 0%-traffic/tag/disabled baseline, private journal and runtime budgets; no unexpected service traffic.
- Fixed exact create-only Auth/Firestore, owner/buyer sign-in and two-identity invocation through specifically approved keyless invoker; record only redacted response decisions. The runner must preserve tokens only transiently and fail closed.
- Verify authorized owner's bounded projected DTO, foreign-buyer denial, unauthenticated and wrong identity denial, revocation/token behavior and rate/quota/audit expectations. A disabled GET test is not enabled owner-read acceptance.
- Cleanup under reviewed exact provenance and Firestore `updateTime` preconditions; Auth UID deletion lacks CAS/generation guard so an unexpected UID change or unknown receipt requires STOP and supervised human resolution. No retries after ambiguous remote writes. Re-verify all four exact paths absent and counter state.
- Explicit authorized tagged rollback, verify original disabled revision/100% main traffic and previously agreed denial health; record cost/limits, no secret data.

### Gate E — Closure judgment

Record **SOURCE-READY** only for proven source/local packaging/checks. Record **STAGING-ACCEPTED** only for full gated live evidence and cleanup/rollback. Keep status NO-GO for any missing IAM boundary, invoker, logging, fixture or rollback evidence; distinguish BLOCKED and UNVERIFIED rather than hiding them. Production remains HOLD / NO-GO pending independent release authorization.

## 3. Shortest next action

**No additional Cloud Shell command is needed immediately.** Existing container build and smoke evidence are successful. First prepare a narrow approval-ready *diff* of Gate C exact changes (if genuinely required) and flag any unready recovery/code paths, **source-only**, on `security-hardening-review`. Present Yasmin with one decision (as few individually scoped approvals as genuinely necessary), not a repeated command per diagnostic. If the documentation-only decision cannot be made safe, park that subgate and continue only independent repository-only work, without calling Step 3 staging complete.

This plan deliberately makes no changes to Dockerfile, code gate, IAM, Firebase data, Rules, Cloud Run, Billing or Production.

## 4. 2026-11-15 — minimum unblocking diff after owner-approved source-only continuation

This is a **source-only release decision**, no live action authorized by generic continuation. The owner specifically requested **only necessary checks** and consented to preparation of one safe, supervised Step 3 staging acceptance session. Previous Docker build/audit, Artifact Registry OCI index `c5fc856b...` (linux/amd64 manifest `eabe4207...`), 0%-main-traffic default-OFF tagged revision `oldx-owner-read-00003-nus` (`step3rc14`), anonymous 403+403, authorized Google health 200 and disabled owner 503, runtime SA token+one GET 404, operator two GET 404 and Auth GET/DELETE policy `CAN_ACCESS` are already documented. Do not rerun unchanged checks.

**Minimal concrete blockers found by source reading:**

1. **Source Gate A — actual runner hard OFF:** `scripts/phase-b-fixture-session-v1.mjs` declares `LIVE_EXECUTION_ENABLED=false` and `scripts/phase-b-owner-read-acceptance.mjs` declares `LIVE_HOSTED_ACCEPTANCE_ENABLED=false`. This is intentional and should remain default-off. A future *distinct, immutable, owner-reviewed activation mechanism* may allow only one exact staging session. Approval to prepare or previous 0% default-off deploy does **not** authorize flipping either switch.
2. **Source Gate B — OCI digest acceptance bug:** `inspectPhaseBConfiguration(...,{hostedTarget})` checks `value.status?.imageDigest?.endsWith('@' + hostedTarget.digest)` (near lines 589–595 of fixture script). Real `oldx-owner-read-00003-nus` Cloud Run revision reports child **linux/amd64 platform manifest** `sha256:eabe4207e307d1e487a30e4afd3abe8cda3792883a752864a5d6f80c45cd082c`, while verified pinned Artifact Registry image URL is parent **OCI index** `sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc`. A direct equality requirement against the wrong digest type would incorrectly report a mismatch. Before any live runner approval, patch the verifier narrowly to require a verified provenance relation between the immutable registry index and Cloud Run's exact chosen platform manifest (or an explicitly pinned and separately verified platform digest), without accepting arbitrary suffixes. Add **focused** positive index→manifest and negative unrelated-manifest offline regressions; do not rerun the whole suite.
3. **Source Gate C — cleanup after early failures is supervised, not automatic:** `runSession` has normal-flow conditional Firestore exact-ID deletion and Auth UID deletion, but `finally` only drops volatile credentials and closes the journal. A failure after some creates can leave partial fixtures; journal states `CREATE_UNKNOWN`, `UPDATE_UNKNOWN`, `DELETE_UNKNOWN` must trigger STOP and private operator-reviewed recovery, **not retry, broad delete or automatic cleanup claim**. Confirm exclusive private journal availability and a real named recovery path before creating any data. Firestore conditional delete only if session marker, createTime, updateTime match. Auth deletion must freshly verify UID/email/creationTime; no atomic generation guard.
4. **Configuration Gate D — default-OFF tagged revision is NOT enabled Owner Read acceptance:** the only approved new tag `step3rc14` currently has `OLDX_PRODUCT_READ_ACTIVATE_STAGING=false` and `OLDX_PRODUCT_READ_STAGING_ADC=false`. Authorized test 503 is expected. Enabled owner/buyer testing requires a **new** separately approved immutable staging-tagged revision with explicit activation env and 0% main traffic and an independent rollback, not mutation/redeployment of `step3rc14` or promotion of main traffic. Scope minimum 0/1 instances, concurrency 1, CPU 1/512Mi, bounded request rates and time/cost, existing private Cloud Run invoker and runtime SA, no IAM/Rules/Billing changes without a distinct approval.
5. **Runtime/cleanup Gate E:** operator GET on two exact docs and Auth policy GET/DELETE `CAN_ACCESS` exist, but operator effective Firestore DELETE, runtime CREATE/UPDATE, runtime DELETE denial and cross-database isolation remain unverified. The failed Firestore Policy Troubleshooter tuple HTTP 400 is **inconclusive**. No speculative DELETE on absent resources. Prove cleanup capability through narrowly reviewed policy evidence and only under a distinctly approved exact fixture lifecycle; if effective delete remains uncertain, **do not create fixtures**.

**One consolidated proposed decision AFTER source bug fix + focused offline tests:** owner separately reviews immutable runner SHA and enabled-revision image digest, explicit new unique 0%-main-traffic tag and nonsecret env, fixed two Auth UIDs `synthetic-seller-a`/`synthetic-buyer-b`, exactly two fixed Firestore documents `marketplaceActors_v1/synthetic-seller-a`/`marketplacePrivate_v1/product_synthetic-phase-b-read-01`, two transient sign-ins, fixed private owner read and buyer denial probes, and same-session operator conditional cleanup of precisely these four fixtures. Exact limits and abort/recovery ownership must be frozen. Require four-ID preflight **only immediately before approved create**, no repeated earlier checks; explicitly separate consent to staging revision deployment/activation from Firebase creates/updates/deletes and final tag removal/rollback. If cleanup is not safely recoverable, do not proceed even if generic approval was given.

**Currently permitted next work:** repository-only narrow verifier bug fix and minimal focused tests on `security-hardening-review`; record outcomes and ask for exact live-scoped approval later. No cloud request or mutation was performed by this document update. **STAGING NO-GO / PRODUCTION HOLD / NO-GO**.
