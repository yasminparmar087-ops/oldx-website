# OLDX Step04 — G2 post-R1 trusted-builder exit route (source-only, 21 Nov 2026)

**Decision type:** new *execution architecture decision*, **not** a source-code fix, scanner pass, permission grant or build/deployment authorization.

Owner-locked repository `yasminparmar087-ops/oldx-website`, work branch `security-hardening-review`. Read [current handoff](OLDX_CURRENT_HANDOFF.md), [single execution plan](OLDX_SINGLE_EXECUTION_PLAN_2026-11-13.md), [C4 six-severe risk packet](OLDX_STEP04_C4_RESIDUAL_RISK_DECISION_PACKET_2026-11-21.md), [C2/C3 custody evidence](OLDX_STEP04_NPMFREE_NO_REBUILD_CUSTODY_ROUTE_2026-11-21.md) first. This record supplements (does not silently amend) original Step04 release conditions.

## 1. Actual consumed G2 evidence — do not repeat

- **Source:** prior frozen npm-free build source commit `fcc96574b6388dc441a0b5d3eade48e79c7ebb24`, Dockerfile `Dockerfile.product-read.bellsoft-npm-free`, reviewed Dockerfile-specific allowlist; `node:24-bookworm-slim` dependency stage and immutable BellSoft nonroot runtime stage, source-level npm deletion at build time.
- **Artifact:** OCI index `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`, AMD64 child `sha256:3150d898c8e013c833bac8b7f8adb8411023449093658d5c5c478a55d7ec28d1`; C2 local/remote index & child identity previously matched with limits.
- **C3 cryptographic custody:** local Sigstore keyless bundle cryptographically VERIFIED OK with explicit approved signer Google OIDC identity and index subject digest; original `--upload=false` (no Registry signature/referrer), **not** independent source/builder SLSA.
- **One local derived image build, isolated Node/Sharp/Firebase/startup/default-OFF/503/SIGTERM checks and one **UNFILTERED** Grype report have already been consumed**. Scanner remains **1 CRITICAL, 5 HIGH, 12 MEDIUM, 2 LOW**; no release-safe scanner clearance or signed image-specific VEX.
- **B1 and R1:** one private 0%-main OFF-only B1 revision `oldx-owner-read-00010-zud` was deployed, verified to use the exact frozen C2 child and both activation flags false, then `ownerreadv2` tag was removed by previously authorized R1. Original `oldx-owner-read-00001-8kr` remained 100% main with `healthcheck` and `step3rc14` tags. R2 NO-OP. This **concludes the owner-approved narrow OFF-only staging trial**; it does not approve future enabled deployment or purge the new revision/latest template.
- **G4 progress:** one corrected Cloud Asset Policy Analyzer query for the exact runtime service account and four Firestore entity permissions found one binding with exact `oldx-staging/(default)` IAM condition, zero unconditional query-scoped bindings; **other-DB actual negative denial and effective Cloud Run invoker exclusivity remain UNVERIFIED**. G8 all-provider hard spending cap still not proved.

**Strict no-repeat list:** do not replay build, Grype, C1 registry upload, C2 index/child checks, C3 sign/verify, CLI presence probes, CI, B1/R1, G4 one-doc proof or analyzer, IAM/billing diagnostics. The periodic OLDX G2 Security Watch already exists; **do not create a second monitor**.

## 2. The six frozen severe findings — current scoped disposition, NOT patches

Based on the *existing OLDX six-row source/evidence packet*, **not a new Grype scan**:

| Scanner finding | Existing evidence | Remaining condition |
|---|---|---|
| `CVE-2019-1010022` — glibc, CRITICAL | Upstream/Red Hat dispute the security classification; OLDX scanner preserves CRITICAL | Exact BellSoft image VEX or qualified reviewer/owner decision for a *future enabled* scope; cannot silently dismiss |
| `CVE-2019-1010023` — glibc, HIGH | Trigger is inspection of crafted/untrusted ELF via `ldd`; first-party review didn't show route | Transitive/native executable chain not exhaustively ruled out |
| `CVE-2026-0861` — glibc, HIGH | BellSoft advisory affected upstream range reported as 2.30–2.42, frozen `2.43.0-r14` outside | Image-specific signed VEX/lineage not independently certified; do not compare different version streams solely by `-r` |
| `CVE-2026-19499` — glibc, HIGH | BellSoft same-stream fixed `2.43.0-r6`; frozen `2.43.0-r14` | Positive vendor-version candidate, not a freshly re-scanned fix or signed VEX |
| `CVE-2026-84243` — glibc, HIGH | BellSoft Stream fixed `2.43.0-r14`, same as frozen installed | Exact version match candidate; release review of package lineage and trust-boundary exposure |
| `CVE-2026-119586` — sqlite-libs, HIGH | SQLite upstream describes unsafe sqlite3 **CLI** `.recover` → second unsafely invoked CLI, not ordinary C library vulnerability | CLI execution chain not proven reachable nor fully excluded; keep finding visible |

Do not convert **vendor-fixed-version candidate**, **upstream disputed**, **not shown reachable**, or **owner narrow risk acceptance** into `FIXED`, `NO_VULNERABILITIES`, or global production acceptance. Previous owner's specific C4 and G8 limited consents were **only for the completed private default-OFF B1 trial**.

## 3. Trusted-original-builder provenance is genuinely different from the completed C3 signing

C3 cryptographically proves that an approved identity signed the *already-existing OCI digest*, not which independent trusted builder made the filesystem or which source and exact build invocation it used. An attestation authored later cannot turn the old, privately built OCI image into an independently witnessed original build.

**Future G2 provenance choices (only if separately approved):**

**A. Retain existing signed index/custody, no rebuild.** Sufficient evidence for the *completed restricted OFF-only staging decision only*. This is today's default: **NO NEW WRITE**, G2 independent builder `UNKNOWN`, enabled/production `HOLD`. Owner's stated eventual willingness to launch despite patches not arriving is not an authorization to declare the current image secure or automatically enable Product API.

**B. ONE new, independently attested release artifact, preferred for a future enabled build.** Prefer an isolated Google **Cloud Build** source-pinned run, with the actual `security-hardening-review` **approved SHA** captured **at approval time**; use the exact reviewed npm-free Dockerfile and allowlisted context, pinned AMD64 base digests, fresh unique *private staging* output package/tag, and `options.requestedVerifyOption: VERIFIED` plus top-level `images` output. Google explicitly documents that an ad-hoc `docker push` step does **not** yield Cloud Build provenance, so fail closed on that workflow shape. This creates a **different immutable OCI digest**; must verify the resulting attested subject digest, source/commit/materials/builder identity, signed predicate and artifact ancestry without treating the old C3 bundle as the new artifact's signature. An attestation must be evaluated for actual trust/coverage; `VERIFIED` in configuration alone is not evidence of a completed provenance record. One focused new image vulnerability assessment and required runtime compatibility/privileged path checks apply **only to that new artifact**; don't rerun old image's entire review. No automatic Cloud Run deployment, Firebase access or traffic changes.

**Alternative GitHub Actions:** official GitHub/Docker build attestation may also be considered for a separately designed **manual** workflow. Existing `.github/workflows/oldx-step04-npm-free-source.yml` is **source-only**, no build; existing `oldx-step04-distroless-one-shot.yml` is hard-disabled. The normal GitHub runner is listed with **14 GB** storage (total VM disk, **not 14 GiB guaranteed available scratch**). Earlier OLDX conservative peak scratch budget was **14 GiB**, so a default hosted runner is NOT assumed safe for combined build/scan; don't reactivate old consumed one-shot workflow. Avoid adding CI credentials/secrets or enabled triggers without owner approval.

## 4. Concrete approval/preflight gates for a future ONE new builder run — not approved now

Do **not** write or execute a live `cloudbuild.yaml` / API request now: absent final owner-approved exact source SHA, unique Registry target, first-party Cloud Build service identity/IAM capability, region, original base pins, active billing/quota, spend/resource ceiling, no-public-storage/privacy/log-retention and rollback policies.

Before *any* future new Cloud Build action, obtain separate approval stating:
1. Exact target **staging project**, approved human operator and runtime/build service identities; no broad IAM elevation, no long-lived key, never use production.
2. Pinned **Git SHA** and exact **two Docker base digests** plus a source-only Dockerfile/allowlist integrity check against the approved commit, no unreviewed build args, network sources or secrets embedded in OCI provenance/logs.
3. Exactly one uniquely named **private Artifact Registry staging image**, no overwrite/mutable tag collision; no Cloud Run deployment/traffic/IAM/Rules/Firestore/Products enablement. Treat new image storage/scanning/egress and Cloud Build time as billable possible.
4. Bounded machine/disk/time budget; Cloud Build pricing currently documents **2,500 free monthly e2-standard-2 minutes per billing account**, but OLDX actual remaining free balance, eligibility and service-specific charges are **not verified**, so no assumed ₹0 hard guarantee.
5. Verified provenance predicate/subject and non-critical errors/coverage, fresh **new-image only** scan and source/runtime change-impact acceptance; STOP on digest mismatch, missing provenance, unapproved rights or unexpected cost/storage/CI shape. No auto retry, automatic release, token or hosted requests.
6. Reconcile six existing severe findings for the new subject without changing the frozen old report; require an appropriately scoped **enabled/production** owner risk disposition if any remain, and independently satisfy G4 effective data-plane IAM plus G8 cost gates.

**One later new build is NOT a repetition of the already completed local image build:** it creates a different artifact expressly to obtain new independent builder evidence. However it is a new external write/action and must **not** be triggered by a generic `ok aagal vadho` or prior B1 consent.

## 5. Exact next checkpoint

- **Now:** G2 signed custody=PASS with limits, C4 six findings=OPEN, independent original-builder=UNKNOWN, source-only trusted-builder release route=PREPARED. `G2_FULL_RELEASE=HOLD`. No cloud writes, Docker/Grype/CI, identity or billing changes.
- **Until separately approved:** daily existing G2 Watch monitors for **material new official** CVE/vendor evidence; do not duplicate the monitor. The next *genuinely new* G2 task is a separately scoped **new release-builder preflight/approval**, not reopening C1–C5.
- **G4 effective other-DB/Invoker** and **G8 whole-project spend risk** are independent blockers for future enabled Product launch. Production `NO_GO`.
- Keep website product/features and owner-locked 15-step order intact, no Codex for source-only checkpoint.

Official documentation consulted 21 Nov 2026:
- Cloud Build provenance: https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance
- Cloud Build config: https://docs.cloud.google.com/build/docs/build-config-file-schema
- Cloud Build price/free tier: https://cloud.google.com/build/pricing
- GitHub runner resources: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- Docker build provenance: https://docs.docker.com/build/metadata/attestations/
- BellSoft fixed package advisories: https://docs.bell-sw.com/security/cves/CVE-2026-19499/ ; https://docs.bell-sw.com/security/cves/CVE-2026-84243 ; https://docs.bell-sw.com/security/cves/CVE-2026-0861
