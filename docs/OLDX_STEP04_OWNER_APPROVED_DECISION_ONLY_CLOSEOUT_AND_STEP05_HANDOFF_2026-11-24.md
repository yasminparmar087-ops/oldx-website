# OLDX Step 04/15 — ACTUAL OWNER-APPROVED DECISION-ONLY HOLD HANDOFF → Step 05 source-only

**Date 24 November 2026. This is a change to the OWNER-LOCKED Step 04 *administrative workflow exit only*, authorized by the owner. No declaration of original technical exit PASS, no launch enablement and no Cloud write.**
Canonical repo `yasminparmar087-ops/oldx-website` — branch `security-hardening-review` only.

## 1. Exact explicit owner approval and scope

Immediately after reading the exact A/B choice and the following question:

> "શું તમે વિકલ્પ Bને સ્પષ્ટ મંજૂરી આપો છો—Step 04 માત્ર વહીવટી રીતે પૂર્ણ કરવો અને અધૂરી ટેક્નિકલ સુરક્ષા-શરતો Step 05/13 માટે ફરજિયાત રાખવી?"

the owner answered **"ha manjuri aapu chhu"** ("Yes, I give approval"). This approves **OPTION B**, explicitly not Option A's continued strict technical exit blocking all later source-only work. Prior "ok aagal vadho" was not this specific owner exit change and should not be used in its place.

**New ledger:**
- `STEP04_WORKFLOW_EXIT=04/15 DONE — DECISION-ONLY HOLD HANDOFF`.
- `STEP04_ORIGINAL_TECHNICAL_EXIT=UNMET / TECHNICAL_HOLD`.
- `STEP05=NEXT / SOURCE-ONLY PLANNING_AND_CODE_REVIEW AUTHORIZED; LIVE_HOSTED_AND_ENABLED=BLOCKED_OWNER`.
- `STEP13_RELEASE_GATES=CARRIED_FORWARD_UNCHANGED`.
- `PRODUCTION=NO_GO`, `ANDROID_PLAY_SUBMISSION=NOT_AUTHORIZED`.
- **15-step tracker administrative done count = 04/15**; this number denotes source/workflow decisions accepted, **not four fully technically released stages**.

This owner approval does **not** authorize additional billable hosted HTTP requests, new tags, new or repeated B1/R1, Cloud Run deploy/route/revision deletion, IAM role grants/removals/identity migration, Firebase Auth/Firestore data-plane or Rules, a second DB, Billing/quotas/service enablement, production go-live or production-like risk acceptance. No live Cloud requests were performed in writing this record.

## 2. Frozen verified Step 04 accomplishments — DO NOT REPEAT

- Immutable **NEW A8** digest `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`; signed Cloud Build/SLSA builder/source/subject verification. Grype one scan **46 package-vulnerability matches / 15 distinct severe CVE IDs**; classification **7 version-fix candidates, 2 disputed historic, 1 SQLite CLI-only, 5 BellSoft OpenSSL vendor affected lines**. Exact 27 JS module source reachability assessed with native/transitive limits, local network-none/read-only/nonroot protected route 503 and health200 tested.
- Owner-observed **one actual NEW Cloud Run A8** `oldx-owner-read-00012-vib` deployed on private staging 0%-main; post-deploy exact image service and revision digest, runtime service account, FALSE/FALSE product activation and ADC flags, no secret volume, resources and direct service IAM no-public/one named invoker verified `PASS_WITH_LIMITS`.
- Owner-approved **R1** removed ONLY `a8off23nov` tag; postwrite shows root `oldx-owner-read-00001-8kr` at **100%** with old `healthcheck` and `step3rc14` tags intact, R2 NO-OP. A8 `00012-vib` revision and latest service template **REMAIN** (no template rollback/deletion). A8 hosted default-OFF HTTP 503 **NOT tested**.
- One corrected G4 Cloud Asset **allow-policy analysis**: selected runtime SA and four Firestore entity operations yielded one exact `oldx-staging/(default)` conditional allow and zero unconditional IN QUERY SCOPE. One actual Firestore database inventory contains ONLY `(default)`, 0 non-default. Existing historic one-doc positive/negative receipt completed. Direct IAM no-public isn't exclusive effective invoker (historical project 2 Owners and 1 Editor).
- Three separate user-owned **G2/G4/G8 risk dispositions** for this already completed private/default-OFF A8 scope **ACCEPTED_WITH_LIMITS**. G8 manual ₹1,000 pre-new-paid-work review/STOP trigger and ₹2,000 goal are **not** hard all-provider spend caps. All earlier execution approvals have been **consumed**.
- [Actual A8 B1/postcheck/R1](OLDX_STEP04_A8_B1_R1_R2_OWNER_ACTION_CONSENT_ONE_SHOT_2026-11-24.md), [consolidated G2/G4/G8](OLDX_STEP04_G2_G4_G8_POST_A8_TRIAL_RISK_DISPOSITION_2026-11-24.md), [exact A/B owner choice](OLDX_STEP04_POST_A8_EXIT_CHOICE_AND_HOSTED_PROOF_BOUNDARY_2026-11-24.md).

## 3. Mandatory UNMET technical release gates now carried forward unchanged

| Gate | Unmet technical statement | Where enforced before any enabled/live step |
|---|---|---|
| Hosted A8 route | No actual authenticated private hosted A8 health200/default-OFF Product503 and unauthorized access-denial trial; **R1 has already removed tag**. A new explicitly approved unique tag + finite HTTP and independent cleanup would be necessary, with zero old-root traffic changes; NEVER test default service URL and claim it was A8 | **Step05 pre-enabled staging**, and Step13 release evidence |
| Cloud Run effective IAM | Project Owner/Editor inherited invoke access and possible other principal/deny/PAB mean one direct named Invoker + zero direct public is **not exclusive effective IAM proof**. Avoid unauthorized identity/role modification | **Step05 before hosted authenticated data-plane**, Step13 |
| Firestore resource scope | Server Firebase Admin bypasses Rules; verify exact SA/project/`(default)`, least privileges, positive and negative authenticated synthetic CRUD/denials and guarded cleanup. One existing default DB means no genuine other-DB target. **Do not create a fake second DB**; if one arises later, require negative evidence then | **Step05 before enabled/auth testing**, Step13 |
| G2 CVEs | 15 distinct severe scanner CVEs remain, 5 BellSoft OpenSSL vendor-affected-line entries; 7 vendor-fix candidates aren't certified patched in exact immutable A8. Owner's OFF-only limited acceptance **does not cover enabled or production risk** | **Step05/13 new-scope threat/mitigation & owner disposition** |
| G8 cost limits | Cloud Run eligible service cap and budgets/alerts are NOT a guaranteed project-wide ₹2,000 gross stop. Owner adopted manual ₹1,000 review/STOP before new paid action; ≥₹2,000 risk target is not enforced. Actual current bill not fresh | **Step05 and Step13 release preflight: fresh gross forecast, finite window, cleanup, owner consent and independent recovery** |
| Rollback/traffic preservation | One R1 tag-only cleanup is proven, but **not full template rollback**. Root `00001-8kr=100%` and `healthcheck`/`step3rc14` are immutable comparison targets for any new, separately authorized trial. Never `--to-latest`/broad tag clear | **Before each future Cloud traffic/write**, and Step13 |
| Product hosted owner/buyer thin slice | Authenticated Product owner/buyer create/read/update/publish/withdraw + enforcement, denial, quotas, session/retry, receipts, private chat and cleanup not independently proven with current transport | **Step05 source code may be reviewed now, but LIVE tests and enablement BLOCKED** |

**These are hard future GO/NO-GO requirements.** The current workflow closeout does NOT change their criteria or waive their safety implications, and production remains HOLD.

## 4. NEW authorized Step05 scope and first safe work

Step05 definition from master: **"ONE genuine hosted Product owner/buyer thin vertical slice incl. authenticated read/write/publish/withdraw, denials, quota and retry"**. Its real hosted technical exit remains blocked by owner release gate(s) above.

The owner's Option B authorizes **SOURCE-ONLY Step05 planning, code review, documentation and offline test design** without service configuration, Firebase data-plane, token minting, deployments, traffic writes, new scans/builds, broad CI replays, or production. Resume specifically from Step05's existing source paths (`functions/staging-marketplace/{product-read-server,cloud-run-http,runtime,bootstrap}.mjs`, UI `features/marketplace/{product-integration,product-integration-dom}.mjs`, existing tests), identify minimum one-pass missing owner/buyer integration and reuse proven Step03/04 adapters; no architecture rewrite or feature reduction. If a new source change is truly needed, do not touch `main` and do only minimal targeted source/offline unit tests, with a new source-only receipt. No fresh enabled/hosted request under this approval.

## 5. Explicit authorization/result bits

```text
STEP04_OPTION_B_OWNER_EXPLICIT_CONSENT=YES
STEP04_ADMINISTRATIVE_EXIT=DONE_DECISION_ONLY_HOLD_HANDOFF
STEP04_ADMINISTRATIVE_COUNT=04_OF_15
STEP04_TECHNICAL_RELEASE=NOT_PASSED_GATES_CARRIED
STEP05_SOURCE_ONLY_PLANNING_AND_CODE_REVIEW=AUTHORIZED
STEP05_LIVE_AUTHENTICATED_PRODUCT_SLICE=BLOCKED
A8_BUILD_SCAN_SLSA_LOCAL_B1_POSTCHECK_R1=CONSUMED_DO_NOT_REPEAT
G2_G4_G8_OWNER_CURRENT_A8_OFF_ONLY_RISK=ACCEPTED_WITH_LIMITS
G4_EFFECTIVE_INVOKER_AND_OTHER_DB_DENIAL=UNVERIFIED
G8_PROVIDER_WIDE_HARD_2000_RUPEE_CAP=NOT_PROVEN
A8_HOSTED_PRIVATE_HTTP_503=NOT_TESTED
A8_00012_REVISION_LATEST_TEMPLATE=RETAINED
OLD_ROOT_TRAFFIC_AND_TAGS=NO_CHANGE
CLOUD_IAM_BILLING_FIREBASE_RULES_DEPLOYMENT_WRITES=NONE
PRODUCTION=NO_GO
```

**If a future assistant faces a conflict, this explicit 24-Nov owner Option B permission supersedes the dated “NOT OWNER-APPROVED” prospect in the earlier source-only choice doc, solely as a *new workflow decision*, not a retrospective security PASS.**
