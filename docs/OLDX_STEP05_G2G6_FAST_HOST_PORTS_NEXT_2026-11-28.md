# BAJUTO / OLDX Step05 — fast G2–G6 host binding checkpoint, 28 November 2026

## ACTUAL source progress, no hosted changes

Owner priority is time, genuine Seller→Buyer feature progress, and NO repetition of completed scans, builds, tests or Cloud/Scheduler probes.

Starting GitHub branch security-hardening-review HEAD 97ac6aac3c2f19d95699d246984370bab798643d. H2AF previous Owner ACTUAL PASS cleanup preserved: temporary Scheduler job deleted, probe Invoker revoked retaining Owner, probe SA disabled/deleted, original OFF Cloud Run service unchanged. Previous H2AD9 single hosted health Scheduler run ended NOT_FOUND with zero Cloud Run GET /healthz logs. Do not pretend hosted health succeeded.

**New changes actually pushed:**

1. functions/staging-marketplace/c2-g2g6-enabled-host-source-assembly.mjs
   - Source gate edit commit e798a4d9f3953ce52e09fb49343b0ece84f779fe
   - Git blob a390d58d30fd1fad70ec2d1809518a6f31e0338b.
   - NEW strict mandatory trusted callback checks *before* constructing website mediator, private Gateway or enabled backend. Website now needs invoker credentials, attestation, guest admission and an actual Gateway HTTP transport. Gateway needs independent trusted KMS status, KMS REST and permanent Firestore one-sign callbacks, source public-key provider and private backend transport. Backend needs actual Firebase Auth verification, Firestore transaction, media bindings, Google verification key resolver and signed proof resolver. Reject image, origin, principal UID, project drift, accessors on top-level host records and wrong backend audience. No fabricated KMS success or in-process bypass of private Cloud Run IAM. ALL OFF by default; new source does not deploy or touch original immutable H2U OFF image.
2. tests/integration/step05-c2-g2g6-new-host-assembly.test.mjs
   - New extension commit 56f041d44c7b56a4a17e9661447796e0ca4ea61c
   - Git blob 003a4dd5ded3dd01dcc9209db47e3fd9d514b642.
   - SIX focused NEW test cases: four earlier cases default-OFF/forged release control/missing KMS/old digest and UID drift, and two new tests for structurally supplied host port callbacks without correct PEM (must not call providers) and mismatched Gateway/backend origin (must not call providers).

Readback SHA verified. Isolated V8 syntax/default-OFF/missing-host guard smoke checked and PASS; **six Node tests NOT executed**. Assistant runtime cannot clone remote repo due to DNS and has no local project checkout. Do NOT claim six tests passed. No Cloud/KMS, Firebase, IAM, Registry, deploy, live product or production action occurred.

## One next fast source action (use Codex for heavy integration only)

In yasminparmar087-ops/oldx-website, branch security-hardening-review, have Codex:

1. Read AGENTS.md latest checkpoint, this exact document, the two new G2–G6 files, existing Step05 H2S KMS/version-status/one-sign Firestore budget adapters and the release control.
2. Run ONLY: node --test tests/integration/step05-c2-g2g6-new-host-assembly.test.mjs, using existing Node>=24 and installed dependencies. Fix and rerun only any failing new case, NOT historic tests/CI/builds/scans.
3. Extend current new assembly only with missing real host providers or validated bindings that directly bring the approved 1-Product/1-photo/2-synthetic-actor Seller→Buyer staging flow closer; reuse existing factories. Do not assert trustworthy version/key status from a signer-only SA, create a mock durable one-sign budget, forward browser auth as Cloud Run IAM or make OFF-only H2U image enabled. If live runtime IAM, KMS/Firestore roles, image digest, approval evidence or Auth grants are missing, leave enabled flow DEFAULT OFF and name the exact blocker for a *single later scoped owner decision*.
4. Add only NEW focused cases for newly implemented host-provider code. Commit/push only security-hardening-review. Return exact remote SHA, new test counts and remaining real hosted permissions/approval/rollback gates. No Google Cloud API/write, KMS sign, Firebase/Firestore writes, product publication, image deploy, new SA/job, production or real data.
5. Do NOT repeat consumed H2AD0–H2AF one-shot scripts, earlier Step05 H2S/H1B/CI test groups or Cloud Scheduler probes. GitHub is canonical for next chat.

## Honest status

H2AF resource cleanup ACTUAL PASS; new G2–G6 host gate code PUSHED and STATIC guard PASS; SIX NEW NODE TESTS AUTHORED BUT NOT RUN; hosted synthetic Seller→Buyer acceptance NOT VERIFIED; Step05 ACTIVE; production NO-GO. Do not misrepresent source-only as working hosted marketplace.
