# OLDX Step04 G2 A5 — one default build service identity read-only preflight

## 21 Nov 2026 ~19:51 IST — A5 OWNER ACTUALLY EXECUTED, COMPUTE_DEFAULT (NEW LATEST)

Actual owner Windows PowerShell terminal screenshot of the prepared **one** `gcloud.cmd builds get-default-service-account` read (no STOP, prompt returned) shows:

```text
G2_A5_DEFAULT_BUILD_SA=COMPUTE_DEFAULT
G2_A5_BUILD_SA_IAM_PRIVILEGES=NOT_CHECKED
G2_A5_DEDICATED_BUILDER=NOT_CREATED
G2_A5_CLOUD_BUILD_JOB=NOT_STARTED
G2_A5_CLOUD_WRITES=NONE
G2_A5_DEFAULT_IDENTITY_READ=COMPLETE_WITH_LIMITS
PS C:\Users\Yasmin Parmar>
```

**A5 is COMPLETE_WITH_LIMITS and CONSUMED; DO NOT RERUN.** The guarded parsing in the owner-run block confirms that Cloud Build's *default* would be the **Compute Engine default service account** (`38472235077-compute@developer.gserviceaccount.com`) for `oldx-staging/asia-south1`. The screenshot printed only the category; principal specificity is inferred from the exact checked regex in the executed command. It does **not** demonstrate that this principal has effective builder/registry/logging rights or that it is safe or unsafe to grant it more roles; **permissions were NOT CHECKED**. Per current official Google Cloud guidance, using a separately configured user-managed build service account is the more controlled option; don't silently submit using Compute default or expand its project-wide privileges. `oldx-product-read-staging` (existing restricted runtime principal) is **NOT** a replacement builder; preserve separation.

**Next distinct minimal action:** [A6 single read-only inventory for the exact proposed user-managed builder SA](OLDX_STEP04_G2_A6_DEDICATED_BUILD_SA_EXISTENCE_READ_ONLY_2026-11-21.md), to avoid creating a duplicate. No IAM role grant, service-account creation, build, Registry write, source upload, Cloud Run or Firebase change authorized by A5. After this, consolidate the **one future build identity, repo-level Registry writer, logging, actAs, time/cost/disk budget** into a separately explicit owner-approved bounded setup; do not multiply repetitive generic IAM scans. Existing direct public GitSource lane was prepared in A4 without requiring Cloud Build v2 connection. All prior A1-A5, C1-C5, B1/R1, G4 proofs remain consumed.

**Current release:** old scan has **1 CRITICAL and 5 HIGH findings**; independent original builder provenance `UNKNOWN`, G4 effective other-DB denial and Cloud Run exclusive invoker `UNVERIFIED`, `STEP04=HOLD`, `PRODUCTION=NO_GO`.

---

21 November 2026, branch `security-hardening-review`, project `oldx-staging`.

## Why only this now

- Actual A3 owner screenshot found zero v2 Cloud Build connections in `asia-south1`; **A3 DONE, do not repeat**. API was enabled and verified in consumed A2. No GitHub connection, job, registry, IAM or deployment changes made.
- [A4 source-only route](OLDX_STEP04_G2_A4_NO_GITHUB_CONNECTION_PUBLIC_GITSOURCE_ROUTE_2026-11-21.md) established an alternate official, **direct public Git URL plus immutable full commit SHA** Cloud Build `GitSource` submission path. This can avoid new persistent connection/Secret Manager GitHub OAuth. **Do not submit a build yet**.
- Before proposing a new nondeployed image, identify what service account Cloud Build would **default to**, without assuming we will use it. Google's official `gcloud builds get-default-service-account` is read-only and returns a `serviceAccountEmail` field per API; depending on configuration it may be Compute Engine default, legacy Cloud Build, or empty. None of these results grants authorization to use the account or proves sufficient/least-privileged IAM. A dedicated builder is preferred *after* scoping its permissions/cost, and no new grants are authorized.

## One operator-supervised, read-only Windows PowerShell A5 — PREPARED_NOT_EXECUTED

Only a single `gcloud.cmd builds get-default-service-account` call in `oldx-staging` `asia-south1` using Yasmin account. Parses `serviceAccountEmail` in official API response and prints **category only**, never complete SA email or secrets. Uses known observed project number `38472235077` solely for guarding identity classification. If absent, prints `NONE_REPORTED`; this does NOT establish there is no usable separately specified user-managed SA. If unexpected shape or permission failure, STOP and no automatic retry.

```powershell
& {
  try {
    $gargs = @(
      'builds','get-default-service-account',
      '--project=oldx-staging',
      '--region=asia-south1',
      '--account=yasminparmar087@gmail.com',
      '--format=json',
      '--quiet'
    )
    $raw = & gcloud.cmd @gargs 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) {
      throw 'G2_A5_READ_FAILED'
    }
    $result = $raw | Out-String | ConvertFrom-Json -ErrorAction Stop
    if ($null -eq $result -or
        -not ($result.PSObject.Properties.Name -contains 'serviceAccountEmail')) {
      throw 'G2_A5_RESPONSE_SHAPE_UNKNOWN'
    }
    $accountResource = [string]$result.serviceAccountEmail
    if ([string]::IsNullOrWhiteSpace($accountResource)) {
      'G2_A5_DEFAULT_BUILD_SA=NONE_REPORTED'
    } elseif ($accountResource -cmatch '^projects/(oldx-staging|38472235077)/serviceAccounts/38472235077-compute@developer\.gserviceaccount\.com$') {
      'G2_A5_DEFAULT_BUILD_SA=COMPUTE_DEFAULT'
    } elseif ($accountResource -cmatch '^projects/(oldx-staging|38472235077)/serviceAccounts/38472235077@cloudbuild\.gserviceaccount\.com$') {
      'G2_A5_DEFAULT_BUILD_SA=LEGACY_CLOUD_BUILD'
    } elseif ($accountResource -cmatch '^projects/(oldx-staging|38472235077)/serviceAccounts/[^/]+$') {
      'G2_A5_DEFAULT_BUILD_SA=OTHER_UNCLASSIFIED'
    } else {
      throw 'G2_A5_ACCOUNT_RESOURCE_UNEXPECTED'
    }
    'G2_A5_BUILD_SA_IAM_PRIVILEGES=NOT_CHECKED'
    'G2_A5_DEDICATED_BUILDER=NOT_CREATED'
    'G2_A5_CLOUD_BUILD_JOB=NOT_STARTED'
    'G2_A5_CLOUD_WRITES=NONE'
    'G2_A5_DEFAULT_IDENTITY_READ=COMPLETE_WITH_LIMITS'
  } catch {
    'STOP_G2_A5_NO_AUTOMATIC_RETRY'
    'G2_A5_DEFAULT_BUILD_SA=UNVERIFIED'
    'G2_A5_CLOUD_WRITES=NONE'
  }
}
```

## Post-result decisions

- `G2_A5_DEFAULT_BUILD_SA=COMPUTE_DEFAULT`: do **not** silently use it; least privilege and explicit new build identity/account approval needed.
- `LEGACY_CLOUD_BUILD`: do not presume correct permissions/exclusive access; still require reviewed actual grants and build-specific identity decision.
- `NONE_REPORTED`: likely need a user-specified SA before build, but existence of candidate SAs not checked.
- `OTHER_UNCLASSIFIED`: stop and inspect only that exact result with owner permission, not a full IAM audit.
- STOP: never rerun this A5 automatically, no IAM changes.
- `A5` does **not** create a service account or grant roles, configure Cloud Logging, create buckets, upload sources, build, scan or deploy.
- Following identity result, prepare one explicit approval for **a single** pinned Git-source `images`+`requestedVerifyOption: VERIFIED` **new image** with cost/time/disk/log/provider rights bounded. Don't repeat old C1–C5, Grype/C3, B1/R1, G4/Policy Analyzer or API enablement.
- G2 1 CRITICAL/5 HIGH original scanner findings unchanged, independent builder origin unknown until new attestation verified; G4 effective cross-DB/Invoker unverified. `STEP04=HOLD`, `PRODUCTION=NO_GO`.

Official docs:
- https://docs.cloud.google.com/sdk/gcloud/reference/builds/get-default-service-account
- https://docs.cloud.google.com/build/docs/api/reference/rest/v1/projects.locations/getDefaultServiceAccount
- https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts

**Prepared source-only; no live cloud command run here.**
