# OLDX Step04 — post-A8 trial residual risk disposition, vendor evidence and no-repeat owner decision

**Date:** 24 November 2026. **Evidence-only / SOURCE-ONLY, not permission to change live cloud resources.** GitHub `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Use the existing exact A8 digest `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`; do not build, rescan, invoke, deploy, delete a revision, re-run B1/R1 or audit old databases/billing.

## A. Latest confirmed execution baseline (completed once)

Owner-observed new A8 `oldx-owner-read-00012-vib` private Cloud Run B1 CLI exit 0 at **0% main**, new-image **exact digest/flags/resources/SA/direct IAM metadata PASS_WITH_LIMITS**, then owner-approved R1 removed ONLY new `a8off23nov` tag. Original `oldx-owner-read-00001-8kr` remains **100% main**, old `healthcheck` and `step3rc14` tags intact. `R2=NO_OP`. **New A8 revision and latest service template remain**, not a full template rollback. Hosted HTTP 503 path was NOT invoked; no staging ADC or Firestore read/write was performed. [Actual user screenshot/receipt](OLDX_STEP04_A8_B1_R1_R2_OWNER_ACTION_CONSENT_ONE_SHOT_2026-11-24.md). All such operations and old B1/R1 are CONSUMED, no repeat.

## B. G2 — newest vendor disposition, 15 severe scanner IDs kept intact

Actual one-shot Grype: **46 package-vulnerability matches** (1 CRITICAL, 23 HIGH, 19 MEDIUM, 3 LOW) containing **15 DISTINCT CRITICAL/HIGH CVE IDs**, not 46 different severe vulnerabilities. Four package lines in signed A8 have scanner-produced BellSoft PURLs: `glibc 2.43.0-r14`, `libcrypto3 3.5.9-r1`, `libssl3 3.5.9-r1`, `sqlite-libs 3.54.1-r0`. PURL is scanner **metadata only**, NOT independent signed APK-package provenance.

| Group | 15-ID grouping | Evidence status as of 24 Nov; no automatic clearance |
|---|---|---|
| Seven version-line candidate fixes | CVE-2026-0861, CVE-2026-19499, CVE-2026-84243; CVE-2026-107496, CVE-2026-88823, CVE-2026-95691, CVE-2026-95692 | BellSoft Stream *fixed-version candidate* matches the observed scanner package versions. Still requires independently adequate package/vendor origin and backport verification before claiming actually patched in A8. Preserve Grype records; not seven certified fixes. |
| Two disputed historic glibc reports | CVE-2019-1010022 and CVE-2019-1010023 | Upstream/distribution dispute or `ldd` on untrusted files call-path limitations; risk contextual, NOT blanket deleted. |
| SQLite CLI-only entry | CVE-2026-119586 | Upstream SQLite says this is NOT a bug in SQLite core library; needs `sqlite3 .recover` command pipeline on untrusted DB. No direct app call found in frozen exact-commit JS audit, but immutable image CLI/native presence not independently ruled out. |
| **FIVE current BellSoft affected OpenSSL paths** | **CVE-2026-107493, CVE-2026-107494, CVE-2026-121482, CVE-2026-124709, CVE-2026-84786** | BellSoft security pages for the four latter label Hardened Containers Stream **Vulnerable**; important new fifth vendor-origin proof: **BellSoft's own BELL-CVE-2026-107493 OSV record** (published 20 Nov, modified 21 Nov) lists affected `pkg:apk/bellsoft-hardened-containers/openssl?arch=source&distro=stream`, introduced `3.1.1-r1`, **no fixed event recorded**. A8 `openssl 3.5.9-r1` lies in affected package line absent evidence of BellSoft backport. This closes the *vendor status discovery gap*, not the affected code path / exploitability / risk acceptance gap. |

BellSoft evidence:
- https://docs.bell-sw.com/security/cves/CVE-2026-107494
- https://docs.bell-sw.com/security/cves/CVE-2026-121482
- https://docs.bell-sw.com/security/cves/CVE-2026-124709/
- https://docs.bell-sw.com/security/cves/CVE-2026-84786
- **New fifth vendor-source OSV:** https://osv.dev/vulnerability/BELL-CVE-2026-107493 and original https://github.com/bell-sw/osv-database/blob/master/BELL-CVE/BELL-CVE-2026-107493.json
- https://www.openssl-library.org/news/secadv/20261117.txt (upstream 17 Nov OpenSSL bulletin: public repository fixes for reported issues, releases carrying fixes **scheduled** 1 Dec 2026; specifically `CVE-2026-107493` and `CVE-2026-124709` recommend OpenSSL **3.5.10**; schedule NOT proof it has been released, nor of any BellSoft rebuild or deployed A8 patch). OpenSSL upstream rates those two **Low**, but old Grype severe package matches and BellSoft vendor scores stay recorded unchanged.
- https://www.sqlite.org/cves.html (CLI-only SQLite).
- Previously recorded all seven BellSoft fixes, upstream dispute sources and exact-package triage: [A8 prior full disposition](OLDX_STEP04_G2_A8_15_SEVERE_CVE_VENDOR_DISPOSITION_2026-11-23.md).

**Previously CONSUMED exact-build Git source audit (do NOT repeat):** All 27 JS modules copied into A8 runtime were source-reviewed at signed commit `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`. App entry uses `node:http.createServer` with **no direct** QUIC listener; inspected JS does not directly call DANE, CMS/PKCS#7/CRL, non-NULL-stack `PEM_X509_INFO_read_bio_ex`, `ldd` on untrusted executables, SQLite `.recover` or subprocess APIs. [Exact frozen source audit](OLDX_STEP04_G2_A8_EXACT_COMMIT_SOURCE_REACHABILITY_AND_APK_ORIGIN_2026-11-23.md). Indirect Node/OpenSSL, Firebase SDK, native/transitive or future enabled code paths are **not fully proven absent**. A8 actual no-network nonroot read-only local runtime 200/503 and hosted A8 exact flags FALSE/FALSE are meaningful controls for OFF-only trial, **not proof of no severe vulnerability**.

**G2 owner disposition needed for NEXT enabled/testing scope:** Have owner acknowledge all 15 scanner IDs, prioritize five affected vendor package-line OpenSSL findings, accept only a specifically bounded residual risk if actual reachable paths are sufficiently constrained, and keep mitigations: private/authorized invokers, no enabled Product API/ADC by default, no QUIC/CMS/DANE direct endpoints, nonroot, short request timeouts, finite test calls, stop/recovery controls. Do **not** use the already consumed OFF-only A8 consent as authorization for a new enabled trial or production. Vendor may release fixes later: require new image provenance and targeted scan ONLY upon a genuinely approved new image/update, not just to improve status now.

## C. G4 — least privilege: what is actually established and what isn't

- After A8 B1, **direct service IAM zero public members, one named invoker; invoker IAM check enabled**, 0%-main A8 and old 100% main preserved. That is direct policy **PASS_WITH_LIMITS**, NOT exclusive effective invoker. Official Cloud Run IAM docs: Project Owners/Editors may invoke, and existing project IAM observation (2 Owners, 1 Editor) is distinct from the single named service Invoker. https://docs.cloud.google.com/run/docs/securing/managing-access
- Existing one corrected Cloud Asset allow-policy analysis found one exact runtime SA conditional Firestore allow for `oldx-staging/(default)` and the four GET/CREATE/UPDATE/DELETE entity permissions, zero unconditional within that query, not exhaustive effective-denial proof. One owner Firestore databases inventory actually showed **one only `(default)` DB, zero others**. No existing second DB to test negative access; **do not fabricate one**. No new IAM grant/change or identity migration now.
- **Safe intermediate conclusion:** private default-OFF A8 source/runtime/postwrite evidence supports limited containment; cannot close **enabled Cloud Run exclusive invoker** or **effective runtime service account negative other-DB access**. Before enabled authenticated data plane, require separate exact resource-bound effective IAM review and authenticated positive/negative staging tests, with owner authorization. If any new DB is later created, fresh negative proof is mandatory; not retroactive PASS.

## D. G8 — spending STOP: record achievable controls instead of an impossible total hard cap

Current Google Cloud spend cap support (official docs last updated 10 Nov 2026): one eligible service/project; supported includes Cloud Run and functions, Google AI API/Agent Platform. No single cap over Firestore, Auth, Storage, Registry, Logging, networking; **budget alerts do not enforce a provider-wide ₹2,000 maximum**. Even eligible service caps have reporting/enforcement latency, in-flight costs and persistent storage costs. https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps ; https://docs.cloud.google.com/billing/docs/how-to/budgets

For next separately authorized enabled staging:
1. Use exact project/account/resource IDs and a *finite* operator-supervised execution window; bound requests, new revisions, image pushes, service instance min0/max1 and any synthetic documents with deterministic guarded cleanup. Quantify expected cost including registry/logs, and set owner stop trigger **below** ₹2,000 (planning threshold, not mathematical maximum).
2. Maintain current separate Cloud Run service spend cap and broader alerting; confirm live settings only **as part of a new specifically approved release preflight**, not periodic audit reruns.
3. Name operator who can stop testing, remove new tag / disable service as appropriate, and independently confirm rollback; no automatic production or billing mutation. Side-provider costs and lag remain explicitly risk-accepted for each actual trial.
4. If owner insists on *guaranteed* single ₹2,000 project-wide hard stop, **G8 BLOCKED by provider support**. No amount of repeat billing reports fixes it.

## E. Strict decision boundary / no-repeat next action

| Gate | Today | Next real advancement (no automatic cloud execution) |
|---|---|---|
| G2 | Signed A8 and OFF-only source/local/hosted-metadata evidence good; **all 15 scanner severe IDs preserved, 5 current BellSoft OpenSSL affected-line statuses known** | Specific owner residual-risk decision for the **next** proposed enabled or production scope, independent of previous OFF-only trial; no unsupported declaration of patched/no path |
| G4 | Direct service no-public and 1 named Invoker, exact default-only DB inventory; **effective inherited invoker and other-DB negative denial NOT PROVEN** | One concrete security design decision: how to restrict effective invokers and test other-DB boundary without creating a fake DB; enabled trial only after narrowly authorized independent evidence |
| G8 | One service cap + broad alerts + successful finite OFF-only B1/R1; **provider-wide hard max NOT PROVEN** | Owner-approved bounded financial risk and precise stop/rollback for any NEXT enabled operation, NOT a guaranteed rupee cap |
| Step04 original exit | **HOLD**. Actual A8 B1+postcheck+R1 consumed; NO hosted HTTP/Firestore test. | Preserve original exit unless owner explicitly revises it. If true technical completion is demanded, further real IAM/hosted/financial assurance is required. An owner-approved **decision-only conditional handoff** is a separate workflow option, not a false PASS or security waiver. |
| Production | **NO-GO** | No rollout/website live enablement under any OFF-only acceptance |

**This packet itself adds NO new Cloud action, test, image, scan, IAM/billing/firebase change or production approval.** Save/checkpoint now, use it to avoid repeat work in any later chat.


## 24 Nov 2026 — NEW OWNER G2 DECISION: LIMITED RISK ACCEPTANCE GRANTED FOR CURRENT PRIVATE DEFAULT-OFF A8

In the next user turn **after** being presented the exact 15-severe-ID categories and the narrow consent text, the owner explicitly replied **"ha manjuri aapu chhu"**. This is the direct approval of **only** Step04 A8 **private, default-OFF** residual G2 risk with mandatory controls; it **does not** mean 15 CVEs fixed, no OpenSSL vendor exposure, complete no-reachability proof, unconditional staging enabled API or production release approval. **Canonical detailed signed-image/15-ID scope ledger**: [OLDX_STEP04_G2_OWNER_LIMITED_RISK_ACCEPTANCE_2026-11-24.md](OLDX_STEP04_G2_OWNER_LIMITED_RISK_ACCEPTANCE_2026-11-24.md). This new dated owner decision **supersedes any earlier sentence in this document that says owner G2 decision is still pending for the current OFF-only scope**; those earlier paragraphs are preserved as historical investigation and potential *future enabled-scope* requirements.

`G2_OWNER_CURRENT_A8_OFF_ONLY_RISK_DECISION=ACCEPTED_WITH_LIMITS`, `G2_SCANNER_15_DISTINCT_SEVERE=UNCHANGED`, `G2_FIVE_OPENSSL_VENDOR_AFFECTED=OPEN`, `G2_COMPLETE_NATIVE_REACHABILITY=UNPROVEN`, `G2_ENABLED_OR_PRODUCTION_SCOPE_ACCEPTANCE=NOT_GRANTED`, `G4_EFFECTIVE_INVOCATION_AND_OTHER_DB_DENY=UNVERIFIED`, `G8_HARD_PROJECT_WIDE_2000_INR_STOP=NOT_PROVEN`, `STEP04_ORIGINAL_TECHNICAL_EXIT=HOLD`, `PRODUCTION=NO_GO`.

No cloud action, code change, build, new security scan, SLSA, deployment, hosted request, IAM/billing/Rules write or production change occurred as a consequence of recording this decision. Do not replay prior A8 B1/R1 or broad past tests. **Next remaining Step04 work:** G4 effective inherited invoker scope and practical non-default database policy response; G8 realistic bounded-cost STOP and recovery. Both need their own scoped outcome/approval.


## 24 Nov 2026 — G4 owner decision separately DRAFTED, not yet accepted

The source-only G4 default-OFF owner risk decision is now prepared at [OLDX_STEP04_G4_DEFAULT_OFF_IAM_OWNER_DECISION_PROPOSAL_2026-11-24.md](OLDX_STEP04_G4_DEFAULT_OFF_IAM_OWNER_DECISION_PROPOSAL_2026-11-24.md). This strictly **reuses**, not repeats, the 21-Nov corrected one-result conditional default-DB allow analysis, A8 one actual 0%-main private postwrite/direct-IAM no-public/one named invoker, historical 2 Project Owners/1 Editor, and one existing Firestore `(default)` DB/zero others. Cloud Run project Owners/Editors may invoke even without direct named service-level grants; Cloud Asset allow-only analysis cannot prove effective denial/PAB; Firestore Admin server SDK bypasses Firestore Security Rules. There is no actual second DB to test and no purpose to fabricate one. Current A8 Product flags still FALSE, old root 100% and tags retained, A8 R1 already consumed.

**New G4 owner acceptance is NOT assumed from the prior G2 consent or earlier spent A8 one-shot risk acknowledgement.** Ask one explicit G4 decision for **current PRIVATE DEFAULT-OFF A8-only inherited IAM/other-DB-negative uncertainty**, with all required enabled/production effective Invoker and Firestore tests left binding. Only after actual owner acceptance may `G4_OWNER_CURRENT_OFF_ONLY_RISK=ACCEPTED_WITH_LIMITS` be written. At this point `G4_OWNER_DECISION=PROPOSED_NOT_APPROVED`, `G4_EXCLUSIVE_INVOKER=UNVERIFIED`, `G4_OTHER_DB_EFFECTIVE_NEGATIVE=UNVERIFIED`, `G4_ENABLED=NO_GO`, `G8_PROVIDER_WIDE_CAP=NOT_PROVEN`, `STEP04_TECHNICAL_EXIT=HOLD`, `PRODUCTION=NO_GO`. No new Cloud/IAM/Firestore tests, deployments, or role changes were performed.


## 24 November 2026 — ACTUAL OWNER G4 LIMITED ACCEPTANCE FOR CURRENT A8 PRIVATE DEFAULT-OFF

**Owner actually replied “ha svikaru chhu” to the exact G4 prompt**, acknowledging inherited Project Owner/Editor potential invocation plus no real second database for effective negative-denial verification, **only** for already completed private DEFAULT-OFF A8 configuration. [Detailed exact scoped G4 owner approval with verbatim evidence](OLDX_STEP04_G4_DEFAULT_OFF_IAM_OWNER_DECISION_PROPOSAL_2026-11-24.md). `G4_OWNER_A8_PRIVATE_DEFAULT_OFF_RISK=ACCEPTED_WITH_LIMITS`, `G4_OWNER_DECISION_FOR_THIS_SCOPE=COMPLETE`; `G4_EXCLUSIVE_INVOKER_EFFECTIVE=UNVERIFIED`, `G4_OTHER_DB_EFFECTIVE_NEGATIVE=UNVERIFIED`, `G4_ENABLED_HOSTED_ACCESS=NO_GO`, `G4_CURRENT_PRIVATE_DIRECT_POLICY=PASS_WITH_LIMITS`, `G4_DEFAULT_DB_ONLY_INVENTORY=COMPLETE`. No new IAM grant/role change, creation of second database, provider call, Firebase/ADC activation, hosted HTTP or production authorization. G2 current OFF-only consent is already accepted separately; do not ask again. **G8 whole-provider guaranteed hard cost stop remains NOT PROVEN**, although narrow earlier OFF-only trial financial risk was accepted and used. Original Step04 technical exit remains **ACTIVE/HOLD**. Any future ENABLED staging or production must have its own exact effective IAM and budget/rollback gates, not inherit this residual risk acceptance.

**G8 next truthful action:** present an explicitly *non-guaranteed* bounded gross-spend/operator stop and cost-exposure choice for the existing OFF-only staging/Step04 workflow, **not** re-run old billing snapshots and **not** represent a service-specific cap as a project-wide ₹2,000 ceiling. The new G8 choice is NOT approved yet.
