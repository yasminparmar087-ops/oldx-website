# OLDX Step04 — G2 A3 one new Cloud Build connection inventory (region-only, read-only)

## 21 Nov 2026 ~19:27 IST — A3 ACTUALLY EXECUTED: 0 REGIONAL CONNECTIONS, DONE (NEW LATEST)

Owner's actual Windows PowerShell terminal screenshot (not a proposed script) shows successful completion of the exact one previously prepared read-only A3 command, and normal prompt return without STOP:

```text
G2_A3_CONNECTION_COUNT_ASIA_SOUTH1=0
G2_A3_GITHUB_CONNECTION_COUNT_ASIA_SOUTH1=0
G2_A3_GITHUB_REPOSITORY_OLDX_LINKED=UNVERIFIED
G2_A3_OTHER_REGIONS=NOT_CHECKED
G2_A3_BUILD_SERVICE_ACCOUNT=NOT_CHECKED
G2_A3_BUILD_REGISTRY_DEPLOY_WRITES=NONE
G2_A3_REGION_ONLY_READ=COMPLETE_WITH_LIMITS
PS C:\Users\Yasmin Parmar>
```

**Interpretation:** `gcloud.cmd builds connections list --region=asia-south1 --project=oldx-staging --account=yasminparmar087@gmail.com --format=json --quiet` returned successfully; the A3 code accepted the empty JSON-array response as a valid empty result. There are **zero currently returned Cloud Build v2 connections in the single queried region**, including GitHub connections. Does NOT prove the absence of connections in other regions, OLDX GitHub connectivity globally, build identity, builder permissions, or whether direct Git URL source could be used. No new Cloud Build job, Registry push, Cloud Run or IAM commands in A3. Cloud Build API A2 enabled/verified earlier at ~19:22 and is not to be re-enabled.

**`G2_A3=COMPLETE_WITH_LIMITS_CONSUMED` — do not run A3 again.** Next avoid automatic GitHub connection creation/secret/IAM setup. Current official `gcloud builds submit` documentation supports *direct public Git URL source* with `--git-source-revision=<commit SHA>` and the Build REST `GitSource` source type, independently of connectedRepository. Since OLDX repository metadata was observed `public`, evaluate that **less-privileged source-pinning lane** before considering a paid/persistent connection. This is documentation evidence only; no direct-URL build was tested and SLSA provenance scope for this source must still be independently verified on a separately approved future new image. [New exact A4 source-only evaluation](OLDX_STEP04_G2_A4_DIRECT_PUBLIC_GIT_SOURCE_EXIT_2026-11-21.md). Existing G2 six severe IDs and builder-origin `UNKNOWN`; G4 effective cross-DB/Cloud Run inherited invoker unverified, `STEP04=HOLD`, `PRODUCTION=NO_GO`.

---

Date: 21 Nov 2026. Repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Project `oldx-staging`, explicit owner account `yasminparmar087@gmail.com`.

## Current truth before A3

- **A1 consumed**: API `cloudbuild.googleapis.com` was NOT_ENABLED, safe STOP; no connection read was attempted.
- **A2 owner-run succeeded** at ~19:22 IST: owner screenshot printed `G2_A2_FRESH_PREIMAGE=API_NOT_ENABLED`, `G2_A2_ENABLE_CLI=EXIT_ZERO`, `G2_A2_CLOUD_BUILD_API=ENABLED_VERIFIED`, `G2_A2_ONE_TIME_ENABLE=COMPLETE`, normal PowerShell prompt, no STOP. See [A2 canonical observed receipt](OLDX_STEP04_G2_A2_CLOUDBUILD_API_ENABLE_OWNER_APPROVED_2026-11-21.md). **Never enable the API again.**
- Cloud Build **v2 connections in `asia-south1` remain unobserved**, because A1 properly stopped. API enable does not itself prove a GitHub connection exists.
- Before ANY new trusted builder submission, source pin, builder SA permissions/log storage, cost and Registry scope remain separately unverified and unapproved. Project Cloud Build API being enabled is not permission to build.
- B1/R1 OFF-only staging completed and consumed; old main 100% and original tags unchanged at last user-observed traffic check. G4 allow-policy one exact condition `(default)` with limits; effective cross-DB/Invoker unknown. G2 historic 1 CRITICAL/5 HIGH scanner matches and independent original-builder trust unknown. `STEP04=HOLD`, `PRODUCTION=NO_GO`.

## ONE A3 operator command — PREPARED_NOT_EXECUTED

Exactly **one** `gcloud.cmd builds connections list --region=asia-south1` call, **read-only**. Uses explicit project and Yasmin owner identity. Suppresses raw JSON (Cloud Build Connection can contain Secret Manager version references and GitHub account metadata) and prints **counts only**. `githubConfig` is the documented Cloud Build v2 GitHub.com connection type. Checks every returned name belongs to the exact expected project / region and refuses unexpected response shape/scope. Empty JSON array `[]` is a valid 0 result, not an API failure. On any 403/permission error/parse error, STOP with no retries; never auto-enable another API, IAM or service agent.

```powershell
& {
  try {
    $gargs = @(
      'builds','connections','list',
      '--project=oldx-staging',
      '--region=asia-south1',
      '--account=yasminparmar087@gmail.com',
      '--format=json',
      '--quiet'
    )
    $raw = & gcloud.cmd @gargs 2>$null

    if ($LASTEXITCODE -ne 0) {
      throw 'G2_A3_CONNECTION_READ_FAILED'
    }

    $json = ($raw | Out-String).Trim()
    if ([string]::IsNullOrWhiteSpace($json)) {
      throw 'G2_A3_EMPTY_RESPONSE'
    }

    if ($json -ceq '[]') {
      $items = @()
    } else {
      $parsed = ConvertFrom-Json -InputObject $json -ErrorAction Stop
      $items = @($parsed | Where-Object { $null -ne $_ })
    }

    foreach ($item in $items) {
      if ([string]$item.name -cnotmatch '^projects/(oldx-staging|38472235077)/locations/asia-south1/connections/[^/]+$') {
        throw 'G2_A3_UNEXPECTED_RESOURCE_SCOPE'
      }
    }

    $github = @($items | Where-Object { $null -ne $_.githubConfig })

    "G2_A3_CONNECTION_COUNT_ASIA_SOUTH1=$($items.Count)"
    "G2_A3_GITHUB_CONNECTION_COUNT_ASIA_SOUTH1=$($github.Count)"
    'G2_A3_GITHUB_REPOSITORY_OLDX_LINKED=UNVERIFIED'
    'G2_A3_OTHER_REGIONS=NOT_CHECKED'
    'G2_A3_BUILD_SERVICE_ACCOUNT=NOT_CHECKED'
    'G2_A3_BUILD_REGISTRY_DEPLOY_WRITES=NONE'
    'G2_A3_REGION_ONLY_READ=COMPLETE_WITH_LIMITS'
  } catch {
    'STOP_G2_A3_NO_AUTOMATIC_RETRY'
    'G2_A3_CONNECTION_INVENTORY=UNVERIFIED'
    'G2_A3_BUILD_REGISTRY_DEPLOY_WRITES=NONE'
  }
}
```

**Output interpretation:**
- `G2_A3_REGION_ONLY_READ=COMPLETE_WITH_LIMITS` with GitHub count **zero**: no Github.com connections returned **in this region only**. It is not evidence that Cloud Build is broken or connections are absent in all regions; do NOT create one automatically.
- Count positive: merely the number of GitHub.com Cloud Build Connection resources returned in `asia-south1`. This does NOT confirm any specific OLDX repository is linked, that connection state is `COMPLETE`, nor that the Build SA is adequate. Only a distinct targeted, approved repository/link check follows if warranted.
- `STOP_G2_A3_NO_AUTOMATIC_RETRY`: do not run the same query again; record uncertainty. Do not make a policy grant or API enablement to force the check to work.
- This A3 does not make a Cloud Build job, create any GitHub connection, write to Artifact Registry, run Docker/Grype, deploy/enable Cloud Run/Firebase, or grant IAM.
- No need to repeat earlier API enabled-service inventory; A2 already verified it. No need to replay C1–C5, B1/R1, G4, billing or CI.

Official references verified: https://docs.cloud.google.com/sdk/gcloud/reference/builds/connections/list and https://docs.cloud.google.com/build/docs/api/reference/rest/v2/projects.locations.connections .

**Status at save time**: `A2=ENABLED_VERIFIED_COMPLETE`; `A3=PREPARED_NOT_EXECUTED`; `G2_TRUSTED_BUILDER=UNKNOWN`; `STEP04=HOLD`; `PRODUCTION=NO_GO`. No GCP call was executed by ChatGPT to create this GitHub text.
