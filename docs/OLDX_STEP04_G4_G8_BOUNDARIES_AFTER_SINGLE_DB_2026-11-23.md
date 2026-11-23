# OLDX Step 04 — concise as-observed exit decision packet after G4 no-other-database inventory

Date 23 Nov 2026 ~22:21 IST. Owner's request: continue Step 04 rapidly **without repeating** successful Cloud Build/SLSA/Grype/runtime, CI, B1/R1 deployment/rollback, direct policy/analyzer, billing and database reads. This is a *source-only decision packet* and contains no new Cloud action or new owner's authorization.

## What is conclusively observed

| Gate | Latest evidence | Exact status |
|---|---|---|
| G2 image integrity | Cloud Build exact new SHA, signed builder/source/subject SLSA checks, private Registry immutable image | Signed new image identity PASS |
| G2 vulnerability | Grype v0.122.1 one new-image scan (46 matches: 1 CRITICAL, 23 HIGH, 19 MEDIUM, 3 LOW; 15 unique severe IDs); vendor package PURLs BellSoft HC and seven vendor-fixed-version candidates | Scan COMPLETE; some CVEs/coverage still require threat/owner disposition, not zero-severe PASS |
| G2 actual image OFF-only runtime | Actual local Cloud Shell Docker `--network none --read-only`, `USER appuser`, UID non-root, `/healthz=200`, protected POST `503`, no Firebase network | **PASS_WITH_LIMITS**, local only, not Cloud Run-hosted enabled data plane |
| G4 direct IAM | One corrected Cloud Asset selected-principal 4-permission analysis: one `(default)` conditional allow binding; zero unconditional match in its query; historic one-doc positive and DELETE403 | **ALLOW_ONLY_WITH_LIMITS**; effective cross-db denial & exhaustive invoker not proven |
| G4 actual DB inventory (NEW) | Owner Cloud Shell `gcloud firestore databases list` read-only `oldx-staging`: exactly 1 database `(default)`, 0 other DBs | **COMPLETE**; actual negative other-DB access test not currently possible using an existing target; do not create test DB |
| G4 existing B1/R1 | One historical private no-main-traffic default-OFF Cloud Run revision deployed, tagged revision later untagged by R1, root 100% and old tags preserved; R2 not needed | **EXECUTED/CONSUMED**; no B1 or R1 repeat |
| G8 gross-cost bounds | Cloud Run service-specific cap / old ₹2,000 alerts plus limited off-only owner risk acceptance | **ALL-PROVIDER HARD STOP NOT PROVEN** and cannot be inferred from alerts-only/project billing |

## Strict project contract and risk-accepted future alternative

Original 15-step master plan Step04 exit requires independently authorized and evidenced private tagged staging revision, immutable source/image, real IAM/Rules/invoker/default-OFF 503, gross-cost STOP and independent verified recovery; notes default-OFF B1 does not establish enabled Firestore CREATE/UPDATE or cross-database denial. Do not change that exit definition or mark Step04 DONE without an explicit owner-approved **scoped exit revision** or truly sufficient proof.

A private **default-OFF** local image runtime is genuinely PASS_WITH_LIMITS, and prior restricted B1/R1 happened once; the previously accepted cost and severe CVE residual risk was narrow and **already consumed** by that prior OFF-only trial, not permission to turn on Firebase ADC or public traffic.

For **future enabled Product API** to advance safely:
- Keep pinned `oldx-staging/(default)` as the **only allowed database**; use exact runtime service account and minimum scoped permissions, fail closed for DB/project/credential drift; require distinct approved testing (real Firestore operation and denials) under authenticated staging before enabled rollout. With only one DB, keep *hypothetical other-DB effective negative denial* recorded as unverified, not manufactured PASS.
- Reconcile Cloud Run invoker exclusivity: existing project Owners/Editor may have effective access even when no public member appears; current direct invoker single member not exclusive. Before an enabled hosted request, obtain point-in-time real authorization model and independent permission/denial checks.
- Treat remaining 15 severe CVE IDs honestly. Seven fixed-version BellSoft candidates are not vendor-signed package proof, two old glibc disputes, one SQLite CLI-only condition, five potentially affected OpenSSL paths; map real reachability and keep owner-accepted residual risk with mitigation where no upstream vendor fix exists. Don't delete existing Grype report or regenerate image just to improve a count.
- Billing: Cloud Run spend caps are single-service; budget alerts don't stop Firestore/Auth/Storage/Artifact Registry/Cloud Logging/network usage. Define max test calls/duration/revisions, cost-monitoring, response/rollback operator and service cost thresholds; **cannot advertise guaranteed provider-wide ₹2,000 cap**. A new enabled/production action needs fresh explicit scoped owner approval, not inherited OFF-only consent.
- Protect existing root 100%-traffic revision, private IAM, default-OFF until new test/rollback consent. Do not change production now.

## Fastest truthful next action

**No further Cloud Shell verification is justified just to recheck this G4 inventory.** Consolidate one owner-reviewed scope decision: keep Step04 **HOLD with limitations** while planning the next bounded authenticated enabled test in Step05, **or** explicitly revise the Step04 exit to a *decision-only/conditional handoff* (as Steps02/03 were separately revised earlier), **without** calling technical G4/G8 PASS. Such an exit revision needs unmistakable owner consent and must carry unmet security gates forward; it cannot silently authorize Step05 live Firebase/Cloud Run or production.

Recommended current status: `STEP04=HOLD`, `G2_A8_LOCAL_RUNTIME=PASS_WITH_LIMITS`, `G4_DB_INVENTORY=PASS_ONE_DEFAULT_ONLY`, `G4_EFFECTIVE_OTHER_DB_DENY=UNVERIFIED`, `G4_EXCLUSIVE_INVOKER=NOT_PROVEN`, `G8_PROJECT_WIDE_HARD_RUPEE_STOP=NOT_PROVEN`, `PRODUCTION=NO_GO`.

Canonical screenshot record: [G4 single-DB inventory](OLDX_STEP04_G4_SINGLE_DEFAULT_DB_INVENTORY_PASS_2026-11-23.md). Prior runtime evidence: [A8 isolated runtime PASS](OLDX_STEP04_G2_A8_ISOLATED_RUNTIME_PASS_G4_G8_NEXT_2026-11-23.md). Plan: [15 steps, Section 0](OLDX_SINGLE_EXECUTION_PLAN_2026-11-13.md). Official vendor limitations: https://firebase.google.com/docs/firestore/manage-databases ; https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps ; https://docs.cloud.google.com/billing/docs/how-to/budgets .


## Task 23 — Proposed exact owner choice for Step04 administrative closeout (23 Nov 2026; NOT APPROVED)

The owner's desire to finish Step04 quickly is a **goal**, **not** consent to revise its original technical exit, spend money, activate Firebase, deploy or waive serious vulnerabilities. Review of current `AGENTS.md`, master plan Section 0 and latest handoff found no sound no-repeat command to transform the *existing* G4 single-default-DB inventory into effective other-DB denial, nor a Cloud Run-only cap into an all-provider gross-cost guarantee. Do not invent those claims or create a throwaway DB. The real one-shot Build/SLSA/Grype/local runtime/B1/R1/inventory work is all consumed.

**Proposed option A — preserve original exit:** `STEP04=ACTIVE/HOLD` until independently sufficient hosted IAM/invoker, vulnerability decision, all-provider cost/rollback acceptance and owner approvals exist. `03/15 DONE`, `05 NOT_AUTHORIZED`, production `NO_GO`.

**Proposed option B — explicit owner-approved workflow/decision exit only:** On a *new, explicit, recorded owner approval*, amend Step04's **administrative** exit to “`04/15 DONE — DECISION-ONLY HOLD HANDOFF`”; Step05 becomes the **NEXT / BLOCKED-owner** gate. Carry the original technical release requirements forward, never treat them as passed: 15 distinct severe scanner CVEs and residual-risk decision, full effective runtime/invoker/auth/default-DB security (hypothetical cross-DB denial unverified), bounded all-provider spending/STOP with no invented ₹2,000 provider-wide hard cap, and independent hosted data-plane/rollback/cleanup tests. Before any actual enabled staging trial or production, these must receive their own adequate evidence, owner acceptance, risk limits and distinct consent. Existing OFF-only B1/R1 permission is exhausted. Option B is not authorization for any IAM, billing, Firebase Rules/data, Cloud Run/Registry, further scan, live token, deploy or production change. `PRODUCTION=NO_GO` remains.

**At this checkpoint: OPTION B IS NOT YET APPROVED.** Therefore retain `STEP04=HOLD_ORIGINAL_EXIT_UNMET` and do not edit the 15-step tracker to a completed count. In the next chat, ask only for the exact scoped owner decision when proceeding; do not repeat earlier Cloud Shell commands. [Task 23 no-repeat review saved on Issue #17](https://github.com/yasminparmar087-ops/oldx-website/issues/17#issuecomment-7108401337).
