# OLDX Step 04 G2 — explicit owner limited residual security-risk acceptance (24 November 2026)

**Decision: G2 OWNER RISK DECISION COMPLETE — RISK ACCEPTED WITH LIMITS.**
**Not: G2 vulnerability FIXED, zero severe CVEs, independent exploitability exclusion, original technical exit PASS, approval for enabled API, or production GO.**

## 1. Exact owner authorization and scope

After the assistant offered the *narrow* G2 acceptance in this chat, the owner's actual reply was **"ha manjuri aapu chhu"** ("Yes, I give approval"). The immediately preceding question explicitly asked whether the owner approves G2 remaining risk **with all listed conditions**, limited solely to the current **Step 04 PRIVATE, DEFAULT-OFF staging** scope. The same approved text stated:
- A8 holds all **15** documented severe scanner CVE IDs with security uncertainty; five OpenSSL vendor affected-line findings are still unresolved; risks may entail availability failures, crashes, resource exhaustion, or other security effects not conclusively ruled out.
- A8 is immutable image `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`, source Git SHA `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`; no new image is being approved or built.
- Both activation flags `OLDX_PRODUCT_READ_ACTIVATE_STAGING=false` and `OLDX_PRODUCT_READ_STAGING_ADC=false` stay exactly FALSE; **no Product API or Firebase ADC/data-plane activation**, IAM/Billing/Rules changes or production launch.
- Private access, currently accepted narrow authorized-invoker controls **with known inherited IAM caveats**, nonroot, low resources, request bounds and existing rollback controls remain. **No new hosted URL invocation**, new tag, revised traffic or resource write follows from this acceptance.
- Future security/fix evidence should be tracked, but no claim of existing vendor fix or forced rescanning of already scanned A8.
- **G4 effective inherited invoker and other-DB denial, G8 whole-provider gross cost/hard stop, original Step04 hosted/security exit requirements remain OPEN**. Any ENABLED, broader staging, or production risk/GO decision is separate and must be explicitly authorized at that time.

This decision **accepts residual uncertainty for the already bounded DEFAULT-OFF Step04 private configuration only**. It does **not** extend expired one-shot A8 B1/R1 consents, authorize another Cloud Run trial, authorize publicly available traffic, or waive a future security assessment for an enabled website.

## 2. Exact G2 source-backed risk inventory retained (no scanner rerun)

Original owner's immutable A8 single Grype scan: **46 package-vulnerability matches**, comprised 1 CRITICAL + 23 HIGH + 19 MEDIUM + 3 LOW, with **15 distinct CRITICAL/HIGH CVE IDs** among 24 severe package matches. Retain every original finding; do not reduce reported counts based on this acceptance.

| Category | CVE IDs and observed vendor/source interpretation |
|---|---|
| **7 BellSoft fixed-version candidates — NOT independently certified as fixed in A8** | `CVE-2026-0861`, `CVE-2026-19499`, `CVE-2026-84243`, `CVE-2026-107496`, `CVE-2026-88823`, `CVE-2026-95691`, `CVE-2026-95692` |
| **2 disputed historic glibc items** | `CVE-2019-1010022`, `CVE-2019-1010023` — upstream/distribution severity disputed or narrow risky `ldd` path |
| **1 SQLite CLI path** | `CVE-2026-119586` — untrusted SQLite `.recover` CLI pipeline; not proven reachable or absent from all native paths |
| **5 BellSoft OpenSSL Stream affected line / no established A8 backport** | `CVE-2026-107493`, `CVE-2026-107494`, `CVE-2026-121482`, `CVE-2026-124709`, `CVE-2026-84786` — potentially vulnerable QUIC, DANE, CMS/CRL, PEM APIs depending on application/native usage; unresolved |

Vendor-source and old exact-source analysis are recorded in [post-A8 G2/G4/G8 decision packet](OLDX_STEP04_G2_G4_G8_POST_A8_TRIAL_RISK_DISPOSITION_2026-11-24.md), [frozen A8 15-CVE triage](OLDX_STEP04_G2_A8_15_SEVERE_CVE_VENDOR_DISPOSITION_2026-11-23.md) and [27-module exact source audit](OLDX_STEP04_G2_A8_EXACT_COMMIT_SOURCE_REACHABILITY_AND_APK_ORIGIN_2026-11-23.md). No direct unsafe QUIC/CMS/DANE/PEM API entry found in inspected JS; Node/Firebase/transitive/native exploit reachability **not conclusively excluded**. Scanner PURL BellSoft namespace is metadata, not vendor-signed APK supply-chain proof.

## 3. Existing Step04 containment verified; new work not implied

One A8 nonroot/no-network/readonly local test actually produced `healthz=200`, protected owner POST `503` in OFF configuration. One later Cloud Run `oldx-owner-read-00012-vib` actual B1 at **0% main** was postchecked with exact signed A8 index and revision digest, both activation flags FALSE, no secret volumes, low-resource bounds, direct IAM without public principal / one direct Invoker, all **PASS_WITH_LIMITS**. Owner-approved R1 then removed only `a8off23nov` and confirmed existing `oldx-owner-read-00001-8kr=100%` main and historical `healthcheck`/`step3rc14` tags retained. R2 NO-OP. **A8 revision and latest template remain**, not restored; hosted HTTP not invoked; inherited IAM exclusivity not proven. [Actual receipt](OLDX_STEP04_A8_B1_R1_R2_OWNER_ACTION_CONSENT_ONE_SHOT_2026-11-24.md).

**No-repeat covenant:** Prior Build, SLSA, Grype, local Docker, snapshot audits, exact A8 B1, postcheck and R1 are consumed. No repeat to obtain ceremonial evidence; future genuinely distinct mitigations/patches may require separate authorization.

## 4. Decision ledger and remaining hard boundaries

| Gate | After new owner approval |
|---|---|
| G2 owner residual-risk disposition for **CURRENT PRIVATE DEFAULT-OFF A8 ONLY** | **ACCEPTED_WITH_LIMITS — owner decision completed** |
| G2 scanner and vendor vulnerabilities physically patched | **NOT PROVEN**; 15 severe distinct IDs remain recorded, 5 OpenSSL vendor affected-line findings unresolved |
| G2 exploitability through all third-party/native paths | **NOT FULLY VERIFIED** |
| G2 *future* ENABLED staging / production risk authorization | **NOT AUTHORIZED**; requires fresh narrower review/owner approval |
| G4 effective Invoker exclusivity and hypothetical other Firestore database negative access | **UNVERIFIED**; do not create artificial second DB |
| G8 all-provider guaranteed gross ₹2,000 hard STOP | **NOT PROVEN / unsupported as a single cap**; existing service-specific caps and alerts aren't equivalent |
| Cloud Run A8 B1/postwrite and R1 cleanup | **COMPLETE_WITH_LIMITS, CONSUMED**; no new write |
| Step04 ORIGINAL TECHNICAL EXIT | **ACTIVE/HOLD, NOT A TECHNICAL PASS** |
| Step05 and production | **STEP05 NOT AUTHORIZED; PRODUCTION NO-GO** |

**The owner's approval is valid within the quoted narrow risk scope, not a broad security waiver.** The next purposeful work is G4 effective access-control strategy and G8 realistic finite-budget stop/recovery decision, **not another A8 rebuild/scan/deploy**, and not changing the owner-locked Step04 completion definition. Save future acceptance decisions with distinct scope, actual evidence and no false PASS.
