# BAJUTO / OLDX Step05 — fast G2–G6 host binding checkpoint, 28 November 2026

## 28 Nov 2026 — G2–G6 requested six tests ACTUAL PASS; metadata host identity bindings SOURCE ONLY

Starting remote HEAD `0a3fd92747e1caae7ba5f9cbf86abf27f68d4dee`, branch `security-hardening-review`. The six formerly unrun assembly cases were executed FIRST, once, on local Windows Node `v26.13.0`: `node --test --test-isolation=none tests/integration/step05-c2-g2g6-new-host-assembly.test.mjs` — exit 0, 6 tests / 6 pass / 0 fail / 0 skipped / 0 cancelled, 1407.315 ms. No initial failures; no old suites repeated. These six results precede the additive metadata wrapper change below.

Source: reused `createC2CloudRunMetadataIdentity` with an optional numeric `expectedSubject` consistency pin, and added `createC2G2G6MetadataBoundHostSourceAssembly` to the existing assembly. The new default-OFF wrapper binds mediator→Gateway and Gateway→backend IAM and independent attestation ports, fixes their distinct service-account UID/audience relationships, rejects competing providers/accessors, and requires separately injected server-only metadata transports for the two actual workload processes. No ambient fetch, SDK initialization, credentials, listener or in-process IAM shortcut. Firebase user Authorization and existing real HTTP transports remain separate. Metadata parsing does NOT independently authenticate a workload; actual Cloud Run IAM plus downstream Google RS256 verification remain mandatory.

NEW focused verification ONLY: `node --test --test-isolation=none tests/integration/step05-c2-g2g6-metadata-host-bindings.test.mjs` — exit 0, 6 tests / 6 pass / 0 fail / 0 skipped / 0 cancelled, 316.0548 ms. Covers OFF/invalid UID, exact distinct metadata audiences/short attestation lease, wrong UID/role/stripped token, arbitrary audience with zero calls, accessor rejection, provider conflicts and downstream UID/audience drift. Unsigned offline JWT fixtures test transport/shape only; no successful cryptographic authentication or complete hosted assembly is claimed. Total this batch: 12 executed cases, 12 pass; no repeat of either suite. Node24-specific execution was not repeated.

Verified tested-byte Git blobs: metadata adapter `2e23127b3b2fec1875259be21c26a7a9fbfe9e6a`; assembly `c2a07643fb7396834ffe06a22e005502ab3fc21b`; new six-case suite `644221ba5346e5d160cde557a2e3b98a2b90c7ea`. Source was tested in an isolated current-remote snapshot; owner's old local checkout, dirty Handoff and untracked `.firebaserc` were untouched. Documentation derives from remote versions, preserving historical evidence.

**Minimum remaining hosted blockers (not fixed by adding callback names):**
1. Independently authenticated, least-privilege KMS KeyVersion/public-key status reader and fresh pinned PEM/status. Signer-only SA is not a reader; do not manufacture ENABLED or grant signerVerifier.
2. Actual native Firebase Auth/Firestore/media providers, verified staging app/database, durable guest/run budgets and permanent no-TTL Firestore sign tombstone authority; synthetic actor grants/config remain unverified. Existing safe factories are retained, no mock durable ledger substituted.
3. Real distinct host-process metadata/HTTP/JWKS transports, immutable enabled-image provenance, exact runtime UID/Invoker/audience and independently approved release evidence. Original H2U OFF image cannot become enabled through configuration.
4. Existing H2S signing transport and status reader each consume only ONE attempt per instance; the Firestore sign tombstone is permanent/global. This is insufficient for a multi-request save→owner→list/detail→archive lifecycle. Do not reset/delete the tombstone, recreate providers to bypass it or silently raise limits. A separately scoped bounded lifecycle signing/status design and authorization are required before hosted acceptance.

**Next single safe action:** prepare the narrow source-only lifecycle signing/status budget contract for owner review, with exact max operations, expiry, durable replay limits, identities and STOP/cleanup rules; reuse current one-sign evidence and leave it consumed. This does not authorize signing, IAM or deployment. Cloud authorization, if later requested, must name exact resources/roles/limits; broad consent is not used to perform unrequested Cloud actions.

H2AF historical cleanup PASS preserved; H2AD9 hosted health NOT_FOUND/zero logs remains NOT a hosted health success. No Cloud calls/writes, KMS sign, Firebase operations, Scheduler probes, CI dispatch, build/pull/scan, deploy or paid resource activity in this batch. Push uses `[skip ci]`. Step05 ACTIVE; all existing security HOLDs and 15-step sequence preserved; production OFF / NO-GO.

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
