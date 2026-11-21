# OLDX Step 04 — G8 service-cap scope and narrowly gated OFF-only cost decision

## 21 Nov 2026 — OWNER G8 RESIDUAL COST RISK ACCEPTED FOR NARROW OFF-ONLY TRIAL (LATEST)

**Direct owner reply in the continuing OLDX conversation:** `ha svikaru chhu` ("Yes, I accept") to this exact question: **accept limited residual exposure to possible additional Google Cloud costs beyond the Cloud Run-only cap, solely for a future private, DEFAULT-OFF/503 staging attempt, while understanding that ₹2,000 is not a guaranteed whole-project maximum and deployment requires separate approval.** This is a **recorded risk-disposition decision only**, not B1, R1, R2, cloud spend creation, Cloud Run deploy, request/invocation, image publish, IAM/billing/Roles edit, or broader enabled release authorization.

- `G8_OFF_ONLY_RISK_ACCEPTED_WITH_LIMITS=YES` (owner; 21 Nov 2026; prospective single bounded supervised staging trial only)
- `G8_PROVIDER_WIDE_HARD_RUPEE_STOP=NOT_PROVEN`, `G8_CLOUD_RUN_CAP_CURRENT_STATUS=NOT_RECHECKED`; alerts are not guaranteed hard limits
- Future scope to specify separately: one new `ownerreadv2` 0%-main private tag, immutable exact image, default OFF/503, 20-min supervised **proposed**, min0/max1, concurrency1, 1CPU/512Mi, timeout30s, no app/test traffic or Firestore/Auth data-plane operations, original root traffic and old tags intact; evaluate possible unexpected charges, stop/recovery control, and operator monitoring
- **B1_RELEASE_CONSENT=NOT_GRANTED**, **R1_CONSENT=NOT_GRANTED**, **R2_CONSENT=NOT_GRANTED**. C4 six-severe CVE owner disposition and G4 inherited/cross-DB controls still OPEN; G2 trusted original builder provenance UNKNOWN; Step04 HOLD, production NO-GO

**Next:** Advance C4 six-CVE conditional-risk decision separately, and G4 effective boundaries/compensating no-data-plane isolation; no redundant G8 read-only snapshot, scan, image build/push or C5 revision reads. Preserve prior dates as history; latest heading supersedes older `NOT_GRANTED_IN_THIS_STEP` status.

Date: 21 Nov 2026. Source-only, not a live budget, billing, IAM, or Cloud Run action.

## Why this decision is needed
This checkpoint follows C5 `C5_REVISION_PREIMAGE_READ_ONLY=COMPLETE` from the owner's 17:24 IST screenshot. C5 R1/R2 rollback design is already saved separately in [C5 rollback guard plan](OLDX_STEP04_C5_R1_R2_ROLLBACK_GUARD_PLAN_2026-11-21.md). DO NOT repeat existing C1–C5 build/upload/sign/scan/revision reads or the G4/G8 ~17:03 read-only snapshot.

### Fresh authoritative provider documentation (21 Nov 2026, research only)
- Google Cloud: [Manage spend cap budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps) — **one eligible Google Cloud service + one project + one month**. Listed eligible APIs are Gemini API, Gemini Enterprise Agent Platform, **Cloud Run**, Cloud Run functions; **not** Firestore, Artifact Registry, or Cloud Logging in this documented list. A spend cap is not a multi-service/project universal hard cost lock.
- Google Cloud: [Spend caps behavior and limitations](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps#limitations) — reporting/enforcement latency permits billed **overages**; in-flight requests may finish; persistent storage/fixed usage may continue costing after API usage pauses. New month's spend caps reset; manual lift can make the remainder of the current month uncapped until a qualifying configuration change.
- Firebase: [Spend caps for Firebase services](https://firebase.google.com/docs/projects/billing/spend-caps) — eligible Firebase-side set currently AI Logic, App Hosting (underlying Cloud Run), Cloud Functions, Extensions; **not general Firestore/Storage/Auth**. Preview, latency applies.
- Google Cloud: [Alerts-only budget documentation](https://docs.cloud.google.com/billing/docs/how-to/budgets) — alerts alone do not automatically stop usage.

## Existing OLDX facts, carefully scoped
1. Existing owner-observed **historical ₹100/month Cloud Run service-category spend cap** (NOT freshly read as part of 17:03 G8) and ₹2,000/month broader alerts-only planning cap; do not call either an enforcement guarantee for all provider services.
2. 21 Nov ~17:03 approved read-only `billingEnabled=True` on `oldx-staging`; **no current cap configuration or spend amount verified** in that GET. No change made.
3. The bounded C5 proposed private 0%-main `ownerreadv2` is NOT deployed. A tagged 0%-main revision is still callable by a permitted principal; no tested total elimination of requests. Existing main 100%-traffic old revision remains.
4. A planned <20 minute supervised operator window, max one revision/attempt, min0/max1/concurrency1, 1vCPU/512Mi, 30s, two feature flags EXACT_FALSE and no test data/API requests are **proposed controls** and must be confirmed by exact future authorized B1 scope, not proof of zero cost or 100% total-price cap.
5. Side-provider exposure includes Artifact Registry storage/signature bytes, Cloud Logging, Firestore/Auth, storage/network/egress, and reporting lag. Even when data-plane endpoints are OFF, pre-existing usage and infrastructure charges may occur. Do not claim fixed rupee bounds from an illustrative plan.

## G8 decision paths
**A. Strict guaranteed all-provider cap prerequisite:** Remain `G8=BLOCKED`, `B1=NO_GO`; supported Google service-cap controls cannot prove a hard rupee ceiling over every OLDX provider today. Do not rerun the same billing snapshot or silently equate alert with hard stop.

**B. Explicit OWNER-ACCEPTED bounded financial residual exposure — only one future OFF-only B1** (not yet approved):
- Owner understands service-specific enforcement + overage/side-provider limitations, and **separately expressly accepts limited but not mathematically guaranteed maximum charges** for a supervised *private* staging-only default-OFF/503 trial. No assertion of a project-wide hard cap.
- Prepare one exact immutable digest, short-lived/keyless credentials, owner at console supervising; fresh read-only **immediately pre-write** service/IAM/traffic/tag/preimage; no concurrent drift. Keep previous root `oldx-owner-read-00001-8kr` at 100%, `healthcheck` tag on `00002-tid`, `step3rc14` on `00003-nus`, new tag `ownerreadv2` 0%-main.
- Proposed 1 attempted B1; 20-minute human-reviewed window; min0/max1/concurrency1, 1CPU/512Mi, 30s, request-based, 503-only flags explicitly false; no hosted test request, Auth/Firestore read/write, new database, billing/IAM/Rules changes, or public access.
- Supervised R1 remove only future new tag; conditional R2 no-op if original 100%/tags remain (else separately approved incident restoration); never `--to-latest` or `--clear-tags`. Note: removing a tag does not guarantee deletion/zero cost.
- A future B1 requires a separately approved exact B1 **and** separately approved R1/R2 and all upstream security/identity/custody decisions. Accepting G8 **risk** is NOT the same as G8 hard-stop PASS or cloud action approval.

## Strict status / remaining gates
- `G8_DOC_SCOPE_RESEARCH=COMPLETE`
- `G8_CLOUD_RUN_SPEND_CAP=HISTORIC_OWNER_OBSERVATION_NOT_REFRESHED`
- `G8_PROVIDER_WIDE_HARD_RUPEE_STOP=NOT_PROVEN`
- `G8_OWNER_RESIDUAL_FINANCIAL_EXPOSURE_ACCEPTANCE=NOT_GRANTED_IN_THIS_STEP`
- `C4_SECURITY=1_CRITICAL_5_HIGH_OWNER_DISPOSITION_PENDING`
- `G2_LOCAL_SIGNATURE=VERIFIED`; `G2_INDEPENDENT_BUILDER_PROVENANCE=UNKNOWN`; `G2_RELEASE=HOLD`
- `G4_NONEXCLUSIVE_STAGING_TRIAL_LIMITED_ACCEPTANCE=HISTORICAL`; `G4_EFFECTIVE_OTHER_DB_DENIAL=OPEN`
- `C5_THREE_REVISION_READ=COMPLETE`, `R1_R2=SOURCE_ONLY_PLANNED`
- `B1_R1_R2_EXECUTED=NO`; `STEP04=HOLD`; `PRODUCTION=NO_GO`

**Next meaningful decision:** Request **one precise written owner risk disposition** about G8 residual cross-provider cost for future *DEFAULT-OFF* trial under these bounds, not a deploy instruction. If accepted, log `G8_OFF_ONLY_RISK_ACCEPTED_WITH_LIMITS` but keep `G8_PROVIDER_WIDE_HARD_STOP=NOT_PROVEN`. Independently request the six-CVE owner decision and verify parent/other-database effective IAM or an adequate no-data-plane isolation proposal before exact B1 authorization. Source-only review/acceptance may proceed without additional cloud reads now.
