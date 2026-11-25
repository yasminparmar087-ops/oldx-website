# OLDX FAST TRACK — Current resume checkpoint

**Updated 26 Nov 2026 IST — workflow-only change; no new application/cloud execution.**
Repo: yasminparmar087-ops/oldx-website | Branch: security-hardening-review.
Read [permanent operating policy](OLDX_FAST_TRACK_POLICY.md) first; this is the short mutable index. Latest dated evidence takes priority if a concurrent session has moved ahead. Preserve original [master 15-step plan](OLDX_SINGLE_EXECUTION_PLAN_2026-11-13.md) and [historical handoff](OLDX_CURRENT_HANDOFF.md).

## Actual status and current critical path
- Steps 01–04 administrative/decision exits recorded; Step 04 technical requirements carried into 05/13. Step 05 active, **not done**. Steps 06–12 contain source-only progress, actual hosted integrations and acceptance still needed. Step 13/14 pending, Android Step 15 separate.
- H1A local image/build/SBOM/Grype/runtime complete PASS_WITH_LIMITS; 12 distinct HIGH, no Critical reported. Retained local H1A image, no rebuild or rescan. [H1A receipt](OLDX_STEP05_MAXIMUM_SAFE_SOURCE_EXECUTION_RECEIPT_2026-11-25.md).
- Native WSL SDK working. H1B G1 actual READ_ONLY_WITH_LIMITS: 7 project + 4 registry requested permissions returned; new SA actAs unknown, WSL auth not configured; G1 consumed. [G1 actual](OLDX_STEP05_H1B_G1_OWNER_SCREENSHOT_PASS_AND_G2_FASTPATH_2026-11-26.md).
- C1A old Cloud Run service confirmed removed; old SA and registry image retained, references unknown. Not a blocker for H1B; no repeat deletion/readback, no shared deletion. [C1A confirmed](OLDX_STEP05_C1A_OPTION_B_SERVICE_DELETION_CONFIRMED_2026-11-26.md), [residual assets](OLDX_STEP05_C1A_SA_IMAGE_METADATA_PRESENT_DEPENDENCY_PENDING_2026-11-26.md).
- Last reviewed pre-policy branch HEAD 9bc857cf5ed56fe0a0cff9b219d3593b46d3a9fd (docs checkpoint; not a new source CI assertion).
- Owner approved G2 native WSL OAuth + isolated Docker helper for asia-south1-docker.pkg.dev + one retained H1A push with remote digest verification. G2A source prepared, actual operator execution NOT evidenced in latest reviewed docs. [Exact G2A command and G2B boundary](OLDX_STEP05_H1B_G2_OWNER_APPROVED_WSL_LOGIN_ONE_SHOT_SOURCE_2026-11-26.md).

## One next action
Check if a newer G2A result has been saved/supplied. If none, use existing pinned G2A owner-approved WSL login script (no repeat consent, no new script). After actual G2A PASS, prepare reviewed G2B retained-image push as already approved; exact immutable digest proof. W1–W6 SA/Cloud Run/IAM/hosted probes, H2 and production not authorized by G2. Later bounded batch needs precise independent consent.

## NO-REPEAT / independent work
- Do not replay H1A build/SBOM/scan/runtime, S1/S1R/S2/S3B setup/preflights, G1 or C1A consumed attempts. Never reset markers. Do not move image to full Cloud Shell HOME.
- Reuse existing Product UI Step 06 source-only work, and prepare independently unblocked P0 integration within recorded authorizations; later Steps 07–12 source-only execution must respect any latest narrower sequencing decision. No new unapproved live access. [Store gap Issue #22](https://github.com/yasminparmar087-ops/oldx-website/issues/22).
- Production **HOLD/NO-GO**. No new code CI claim, deployment, Firebase/IAM/Billing or real data changes in workflow update.

## Update this block after meaningful progress
Timestamp | current branch/code SHA and actual CI | active step | verified outcome + receipt link | approval scope/consumed actions | one next action | independent P0 | production status. Replace rather than append; preserve old details in Git history/linked receipts. Verify save. Do not store secrets. Newer dated actual evidence overrides stale entries, reconcile before any write.
