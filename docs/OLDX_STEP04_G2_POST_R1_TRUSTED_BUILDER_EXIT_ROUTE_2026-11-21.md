# OLDX Step04 — G2 post-R1 trusted-builder exit route (source-only, 21 Nov 2026)

## 21 Nov 2026 ~19:14 IST — G2 A1 read-only STOP: Cloud Build API DISABLED; no repeat (NEW LATEST)

Actual owner Windows PowerShell screenshot from the **one** preapproved A1 guarded read: `G2_CLOUD_BUILD_API=NOT_ENABLED`, `G2_BUILD_PREFLIGHT=STOP_NO_API_ACTIVATION`, `G2_CLOUD_WRITES=NONE`, return to `PS C:\Users\Yasmin Parmar>` without unexpected errors. Since API was disabled, **`gcloud builds connections list` was intentionally NOT CALLED**: no claim that the GitHub connection is missing or broken. Build SA and any new Cloud Build submission likewise NOT CHECKED/NOT STARTED. The API status query is **consumed**. [Canonical A1 observation and two-route decision packet](docs/OLDX_STEP04_G2_A1_BUILD_API_DISABLED_OWNER_DECISION_2026-11-21.md). Route A recommended for continuity with the existing private Artifact Registry/Cloud Run, but **requires a distinct owner YES** to enable *only* `cloudbuild.googleapis.com` on `oldx-staging`; this is a new project configuration mutation. It would NOT authorize build, IAM/SA changes, GitHub connection, billing, source pushes, image/registry writes, Cloud Run or Firebase. Route B is valid only as design fallback: GitHub repo current metadata **public**, so GitHub artifact attestations are supported for public repos, and standard public runners are free; however Linux runner ~14 GB total is insufficient to assume OLDX's prior 14 GiB conservative peak scratch, and GHCR/new provenance workflow needs additional permissions/storage/release decisions. **Do not enable API or launch a build without that new scoped approval**; never re-run old Grype, C1–C5, B1/R1 or G4 tests/queries. Existing G2 six severe findings 1 CRITICAL+5 HIGH and original-builder provenance UNKNOWN; `G4_OTHER_DB_DENY=UNVERIFIED`, `STEP04=HOLD`, `PRODUCTION=NO_GO`. **Next conversation action: owner yes/no on enabling this single API only**, then guarded one-time command if approved, with no other side effects. Older A1 'prepared-not-run' entries below are history.

## G2 PRE-BUILD A1 — ONE READ-ONLY API/CONNECTION INVENTORY (NEW LATEST, NOT YET EXECUTED)

**Reason to do this before drafting an executable build:** Current approved source-only route identifies a *future* attested Cloud Build from a **specific GitHub commit**. The repository does **not** prove that `oldx-staging` has the Cloud Build API enabled or a **2nd-generation GitHub connection** configured. Enabling Cloud Build/API, connecting a private GitHub repository, making a build service account, granting Registry writer, or running a build are **NEW actions**, not covered by previous private OFF-only B1/R1 approvals.

**New technical detail from current official docs (21 Nov):** Cloud Build supports `connectedRepository.revision` pinned to a Git commit SHA; a local `gcloud builds submit .` can upload a local working directory governed by `.gcloudignore`, and is NOT by itself evidence of a GitHub-connected, exact fetched commit. `gcloud builds get-default-service-account` is an available read-only query, but DO NOT run yet: default builder account can be broad, and our chosen future direction is an explicitly reviewed **least-privilege dedicated builder account**. With a user-managed builder, logs must have an approved Cloud Logging or user-owned Cloud Storage configuration; this may entail previously unapproved rights/storage and costs. Docker `images` top-level + `requestedVerifyOption: VERIFIED` are necessary design checks, not a guarantee that a future *completed* provenance record is trustworthy. A fresh Build source commit pin, immutable target, service identity, project-region support, disk/billing and exact write approval remain separately pending.

**Only A1 operator action proposed:** One `gcloud services list --enabled` read, and **only if the API is already enabled**, one regional `gcloud builds connections list --region=asia-south1` read. The latter is **region-only discovery**; 0 results here does not prove there is no connection in another region. No additional repo/identity lists, no IAM policy reads, no Cloud Build submissions, no API enable. Explicit Windows PowerShell `gcloud.cmd`, non-interactive `--quiet`, sanitized labels only. Never reuse the past B1/R1 commands or run this A1 repeatedly for status.

### Prepared single guarded Windows PowerShell block — READS ONLY, NOT EXECUTED

```powershell
& {
  try {
    $common = @(
      '--project=oldx-staging',
      '--account=yasminparmar087@gmail.com',
      '--quiet'
    )

    $names = @(& gcloud.cmd services list --enabled @common '--format=value(config.name)' 2>$null)
    if ($LASTEXITCODE -ne 0 -or $names.Count -eq 0) {
      throw 'G2_SERVICE_INVENTORY_FAILED'
    }

    if (@($names | Where-Object { $_ -ceq 'cloudbuild.googleapis.com' }).Count -ne 1) {
      'G2_CLOUD_BUILD_API=NOT_ENABLED'
      'G2_BUILD_PREFLIGHT=STOP_NO_API_ACTIVATION'
      'G2_CLOUD_WRITES=NONE'
      return
    }

    'G2_CLOUD_BUILD_API=ALREADY_ENABLED'

    $raw = & gcloud.cmd builds connections list '--region=asia-south1' @common '--format=json' 2>$null
    if ($LASTEXITCODE -ne 0 -or $null -eq $raw) {
      throw 'G2_CONNECTION_READ_UNAVAILABLE'
    }
    $data = ($raw | Out-String | ConvertFrom-Json -ErrorAction Stop)
    $all = @($data | Where-Object { $null -ne $_ })
    $github = @($all | Where-Object { $null -ne $_.githubConfig })
    "G2_CONNECTIONS_ASIA_SOUTH1_COUNT=$($all.Count)"
    "G2_GITHUB_CONNECTIONS_ASIA_SOUTH1_COUNT=$($github.Count)"
    'G2_GITHUB_REPO_PIN_AND_BUILDER_ACCOUNT=NOT_VERIFIED'
    'G2_CONNECTED_SOURCE_OTHER_REGIONS=NOT_CHECKED'
    'G2_BUILD_OR_DEPLOY=NOT_STARTED'
    'G2_CLOUD_WRITES=NONE'
  } catch {
    'STOP_G2_READ_ONLY_PREFLIGHT_NO_AUTOMATIC_RETRY'
    'G2_BUILD_READINESS=UNVERIFIED'
    'G2_CLOUD_WRITES=NONE'
  }
}
```

**Interpretation:**
- API `NOT_ENABLED`: STOP without enabling it. This is a new prerequisite, not a security finding; ask the owner for **separately scoped explicit enablement/cost/least-privilege approval** only if a trusted build is still chosen.
- API `ALREADY_ENABLED` + GitHub connection count `0`: no **GitHub-type connection in the specific checked region**; source connected to another region or unconnected is still UNKNOWN. Next choice is one minimal *other region* discovery if justified or a separately approved setup, **not** a guessed repo ID.
- Count greater than 0: confirms **connection resource existence only**, not OLDX's repository connected, installation usable or authorized code access; next can be one targeted repository listing for the named connection after scoping.
- Any STOP: do not rerun automatically, change IAM or enable APIs. Record the exact sanitized output in GitHub and choose the next distinct action.
- No result authorizes build submission; `G2_TRUSTED_ORIGINAL_BUILDER=UNKNOWN`; old image/C3/Grype/CVE count unchanged; `STEP04=HOLD`, production NO-GO.

**Future new-build gate (not A1):** one approved Git SHA fetched by trusted Build source, exact already-reviewed Dockerfile/digest-pinned builder/base, separate limited build SA with source/Registry/logging privileges, approved single private output + monthly/one-shot expense guard, build machine/disk and timeout (earlier Cloud Shell 14 GiB scratch is NOT evidence that default Cloud Build disk is sufficient), provenance **actually** verified for builder/source/materials/new output and one new-image-only security/runtime assessment. No unreviewed automatic triggers. Preserve existing Cloud Run main traffic and all OLDX features.

**Official references:** https://docs.cloud.google.com/sdk/gcloud/reference/services/list ; https://docs.cloud.google.com/sdk/gcloud/reference/builds/connections/list ; https://docs.cloud.google.com/build/docs/running-builds/submit-build-via-cli-api ; https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts ; https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance ; https://cloud.google.com/build/pricing .

**Checkpoint now:** `G2_PRE_BUILD_A1=PREPARED_NOT_EXECUTED`, `G2_BUILD_API=UNVERIFIED`, `G2_GITHUB_CONNECTION=UNVERIFIED`, `G2_BUILD_EXECUTION=NOT_AUTHORIZED`, `G2_BUILDER_PROVENANCE=UNKNOWN`, `G2_SIX_CVE_SCANNER_CLEARANCE=NO`, `STEP04=HOLD`, `PRODUCTION=NO_GO`.

---

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
