# OLDX Step 04 G2 A8 — one owner-approved guarded build command

**22 November 2026 — PREPARED, NOT EXECUTED.** Exact user approval for one private Git SHA-pinned Cloud Build and new-image security/provenance verification is recorded in [A8 decision packet](OLDX_STEP04_G2_A8_SINGLE_TRUSTED_CLOUD_BUILD_APPROVAL_2026-11-22.md). No API enables, IAM, Cloud Run, Firebase, billing, production or automatic retries. Soft incremental ₹100 planning envelope is not an enforced cap; Cloud Build may implicitly create or use service-managed source staging storage.

**Run from Windows PowerShell prompt `PS ...>` not bare CMD.** Script downloads exactly pinned config from GitHub commit `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`, checks SHA256 `d7632e6fbd5ecb09f0b910be1a48641a912deb5f54f2e2c6d7f8311f19c6f49e`, reads 3 API states, confirms exactly named Registry package ABSENT only via authenticated HTTP 404, atomically creates a local no-repeat marker, then attempts **one** `gcloud builds submit` for the pinned public repository SHA. YAML has `E2_STANDARD_2`, 100GB disk, 1200s timeout, 600s queue TTL, dedicated SA, CLOUD_LOGGING_ONLY, requestedVerifyOption VERIFIED, top-level images output and no deploy. It neither emits a token nor prints the raw IAM policy. There is no automatic image scan in this single command; later checks are separate.

```powershell
& {
  $ErrorActionPreference = 'Stop'
  $stage = 'START'
  $markerCreated = $false
  $project = 'oldx-staging'
  $owner = 'yasminparmar087@gmail.com'
  $sourceSha = '31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71'
  $gitUrl = 'https://github.com/yasminparmar087-ops/oldx-website'
  $image = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1:one-shot'
  $config = Join-Path $env:TEMP 'oldx-a8-config-31888e7a-20261122.yaml'
  $marker = Join-Path $env:USERPROFILE '.oldx-a8-20261122-attempted'
  $log = Join-Path $env:USERPROFILE 'oldx-a8-20261122-build.log'
  try {
    $stage = 'LOCAL_GUARD'
    if ((Test-Path -LiteralPath $marker) -or
        (Test-Path -LiteralPath $config) -or
        (Test-Path -LiteralPath $log)) {
      throw 'A8_LOCAL_PATH_ALREADY_USED_STOP'
    }

    $stage = 'PINNED_CONFIG_FETCH'
    $configUrl = "https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/$sourceSha/cloudbuild.step04-g2-npmfree-one-shot.yaml"
    Invoke-WebRequest -UseBasicParsing -Uri $configUrl -OutFile $config -ErrorAction Stop
    $gotHash = (Get-FileHash -LiteralPath $config -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($gotHash -cne 'd7632e6fbd5ecb09f0b910be1a48641a912deb5f54f2e2c6d7f8311f19c6f49e') {
      throw 'A8_PINNED_CONFIG_HASH_MISMATCH'
    }
    'A8_PINNED_CONFIG_SHA256=PASS'

    $stage = 'REQUIRED_API_READ'
    $enabled = @(& gcloud.cmd services list --enabled "--project=$project" "--account=$owner" '--format=value(config.name)' --quiet 2>$null)
    if ($LASTEXITCODE -ne 0 -or -not $enabled) {
      throw 'A8_API_READ_UNVERIFIED'
    }
    if ($enabled -notcontains 'cloudbuild.googleapis.com' -or
        $enabled -notcontains 'containeranalysis.googleapis.com' -or
        $enabled -notcontains 'artifactregistry.googleapis.com') {
      throw 'A8_REQUIRED_API_NOT_ENABLED_STOP'
    }
    'A8_REQUIRED_APIS=ENABLED_READ_ONLY'

    $stage = 'EXACT_TARGET_ABSENCE_READ'
    $tokenLines = @(& gcloud.cmd auth print-access-token "--account=$owner" 2>$null)
    if ($LASTEXITCODE -ne 0 -or -not $tokenLines) {
      throw 'A8_OWNER_TOKEN_UNAVAILABLE'
    }
    $token = [string]$tokenLines[-1]
    $packageUrl = 'https://artifactregistry.googleapis.com/v1/projects/oldx-staging/locations/asia-south1/repositories/oldx-staging-images/packages/oldx-step04-g2-cloudbuild-20261122-a1'
    $httpStatus = 0
    try {
      $res = Invoke-WebRequest -UseBasicParsing -Method Get -Uri $packageUrl -Headers @{Authorization="Bearer $token"} -ErrorAction Stop
      $httpStatus = [int]$res.StatusCode
    } catch {
      if ($null -eq $_.Exception.Response) {
        throw 'A8_PACKAGE_READ_UNKNOWN'
      }
      $httpStatus = [int]$_.Exception.Response.StatusCode
    }
    $token = $null
    if ($httpStatus -ne 404) {
      throw 'A8_TARGET_NOT_CONFIRMED_ABSENT_STOP'
    }
    'A8_EXACT_NEW_REGISTRY_PACKAGE=ABSENT_HTTP404'

    $stage = 'CREATE_ONE_ATTEMPT_MARKER'
    $fs = [System.IO.File]::Open(
      $marker,
      [System.IO.FileMode]::CreateNew,
      [System.IO.FileAccess]::Write,
      [System.IO.FileShare]::None
    )
    try {
      $bytes = [System.Text.Encoding]::UTF8.GetBytes('ONE_SUBMIT_ATTEMPT_ONLY|' + $sourceSha)
      $fs.Write($bytes,0,$bytes.Length)
    } finally {
      $fs.Dispose()
    }
    $markerCreated = $true
    'A8_ATTEMPT_MARKER=CREATED_NO_AUTOMATIC_RETRY'

    $stage = 'SUBMIT_ONCE'
    $submitArgs = @(
      'builds','submit',$gitUrl,
      "--git-source-revision=$sourceSha",
      "--config=$config",
      "--substitutions=_IMAGE=$image",
      '--region=asia-south1',
      "--project=$project",
      "--account=$owner",
      '--suppress-logs',
      '--quiet'
    )
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
      & gcloud.cmd @submitArgs *> $log
      $code = [int]$LASTEXITCODE
    } finally {
      $ErrorActionPreference = $previousPreference
    }

    "A8_GCLOUD_EXIT_CODE=$code"
    "A8_PRIVATE_LOCAL_LOG=$log"
    if ($code -ne 0) {
      throw 'A8_SUBMIT_OR_BUILD_NOT_VERIFIED_NO_RETRY'
    }
    'A8_BUILD_CLI=EXIT_ZERO'
    'A8_PROVENANCE_AND_SECURITY=NOT_YET_VERIFIED'
    'A8_CLOUD_RUN_DEPLOY=NONE'
    'A8_DO_NOT_REPEAT_BUILD'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^A8_[A-Z_]+$') {
      $reason = 'A8_UNEXPECTED_ERROR'
    }
    'STOP_OLDX_A8_NO_AUTOMATIC_RETRY'
    "STAGE=$stage"
    "REASON=$reason"
    "A8_ATTEMPT_MARKER_CREATED=$markerCreated"
    'A8_CLOUD_RUN_DEPLOY=NONE_BY_THIS_COMMAND'
    'A8_CHECK_ACTUAL_BUILD_AND_REGISTRY_STATE_BEFORE_ANY_NEW_WRITE'
  }
}
```

**Interpret output:** `A8_PINNED_CONFIG_SHA256=PASS`, `A8_REQUIRED_APIS=ENABLED_READ_ONLY`, `A8_EXACT_NEW_REGISTRY_PACKAGE=ABSENT_HTTP404` must all appear before the attempt marker. `A8_BUILD_CLI=EXIT_ZERO` is one CLI-reported build success, **not a G2 security PASS**. On `STOP_OLDX_A8_NO_AUTOMATIC_RETRY` do not re-run and do not remove marker: read `STAGE=`, `REASON=` and `A8_ATTEMPT_MARKER_CREATED=`. Once marker created, even a nonzero or invisible CLI result can mean a provider job was submitted; reconcile **read-only** before any new write. The local CLI output log is `%USERPROFILE%\oldx-a8-20261122-build.log`, keep private. No Cloud Run deploy, no production changes by script. Source upload bucket or related managed side effects not independently verified; no explicit bucket create in script.

**Following actual ONE build,** independently verify Cloud Build ID, full source SHA, output digest, signed provenance and builder identity, exact new-artifact scan/runtime, keep Step04 HOLD and production NO_GO. Google reference: https://docs.cloud.google.com/sdk/gcloud/reference/builds/submit ; https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance ; https://docs.cloud.google.com/artifact-registry/docs/reference/rest/v1/projects.locations.repositories.packages/get .
