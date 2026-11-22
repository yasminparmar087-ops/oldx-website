# OLDX Step04 G2 A8 — owner one-shot Cloud Build exit-zero screenshot, next read-only result reconciliation

**Actual owner screenshot 22 November 2026 ~23:07 local screenshot context** (taskbar on image says 21 Nov 23:07; avoid assuming authoritative provider timestamp). **This is new execution evidence, not a proposed command.**

```text
A8_PINNED_CONFIG_SHA256=PASS
A8_REQUIRED_APIS=ENABLED_READ_ONLY
A8_EXACT_NEW_REGISTRY_PACKAGE=ABSENT_HTTP404
A8_ATTEMPT_MARKER=CREATED_NO_AUTOMATIC_RETRY
A8_GCLOUD_EXIT_CODE=0
A8_PRIVATE_LOCAL_LOG=C:\Users\Yasmin Parmar\oldx-a8-20261122-build.log
A8_BUILD_CLI=EXIT_ZERO
A8_PROVENANCE_AND_SECURITY=NOT_YET_VERIFIED
A8_CLOUD_RUN_DEPLOY=NONE
A8_DO_NOT_REPEAT_BUILD
```

**Interpretation:** one owner-approved `gcloud builds submit` was attempted after pinned-config and required-services checks, prior package absence, and persisted local one-shot attempt marker. The command reported exit code zero, without a STOP. Do not repeat, delete marker, or execute another source build to verify. This is **CLI success**, not independently confirmed remote Cloud Build ID/SUCCESS, exact Git source resolved SHA, Registry immutable output digest, independent signed builder provenance, CVE disposition, runtime test, or G2 clearance. No Cloud Run deploy is invoked by this script; the command does not independently inspect the service traffic. The local log is **private and should never be pasted in full** (could contain other incidental console content).

**Exact next step, ONE user-run read-only operator command**: `gcloud builds list` scoped to `asia-south1`, up to 50 rows to find exactly one build with BOTH dedicated builder service account and one unique newly approved image; then `gcloud builds describe` for exact ID and sanitized checks only. If no unique match, STOP, no writes, no guesses, and use the prior private CLI log locally for a separate ID-only reconciliation rather than re-running the build. No Cloud Run/Registry mutation, no scanning, no IAM/API/billing edits. Report declared Git source versus resolved SHA distinctly and the build-result image digest if populated. `requestedVerifyOption: VERIFIED` is not independent cryptographic attestation verification. One future exact digest-bound scan/runtime requires separate follow-on under previously approved A8 verification scope.

```powershell
& {
  try {
    $project = 'oldx-staging'
    $region = 'asia-south1'
    $owner = 'yasminparmar087@gmail.com'
    $sha = '31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71'
    $sa = 'projects/oldx-staging/serviceAccounts/oldx-step04-build@oldx-staging.iam.gserviceaccount.com'
    $image = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1:one-shot'

    $raw = & gcloud.cmd builds list "--region=$region" "--project=$project" "--account=$owner" '--limit=50' '--format=json' --quiet 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) { throw 'A8_BUILD_LIST_READ_FAILED' }
    $rows = @($raw | Out-String | ConvertFrom-Json -ErrorAction Stop)
    $found = @($rows | Where-Object {
      $_ -and @($_.images) -ccontains $image -and
      $_.serviceAccount -ceq $sa
    })
    if ($found.Count -ne 1 -or -not $found[0].id) {
      throw 'A8_EXACT_BUILD_NOT_UNIQUE_IN_LIST'
    }
    $id = [string]$found[0].id
    if ($id -notmatch '^[0-9a-fA-F-]{36}$') { throw 'A8_BUILD_ID_UNEXPECTED' }

    $rawDetail = & gcloud.cmd builds describe $id "--region=$region" "--project=$project" "--account=$owner" '--format=json' --quiet 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $rawDetail) { throw 'A8_BUILD_DESCRIBE_READ_FAILED' }
    $b = $rawDetail | Out-String | ConvertFrom-Json -ErrorAction Stop
    if ([string]$b.id -cne $id -or [string]$b.serviceAccount -cne $sa -or
        @($b.images) -cnotcontains $image) {
      throw 'A8_BUILD_IDENTITY_MISMATCH'
    }
    "A8_BUILD_ID=$id"
    "A8_BUILD_STATUS=$($b.status)"
    if ($b.status -cne 'SUCCESS') { throw 'A8_BUILD_STATUS_NOT_SUCCESS' }

    $sourceOk = ($b.source.gitSource.url -ceq 'https://github.com/yasminparmar087-ops/oldx-website' -and
                 $b.source.gitSource.revision -ceq $sha)
    if ($sourceOk) { 'A8_DECLARED_GIT_SOURCE=EXACT_SHA_MATCH' }
    else { 'A8_DECLARED_GIT_SOURCE=UNVERIFIED' }

    if ($b.sourceProvenance.resolvedGitSource.revision -ceq $sha) {
      'A8_RESOLVED_GIT_SHA=MATCH'
    } else {
      'A8_RESOLVED_GIT_SHA=NOT_PROVEN'
    }

    $imgs = @($b.results.images | Where-Object { $_ -and $_.name -ceq $image })
    if ($imgs.Count -eq 1 -and [string]$imgs[0].digest -match '^sha256:[0-9a-fA-F]{64}$') {
      "A8_RESULT_IMAGE_DIGEST=$($imgs[0].digest)"
    } else {
      'A8_RESULT_IMAGE_DIGEST=NOT_PROVEN'
    }
    'A8_SIGNED_PROVENANCE=NOT_YET_INDEPENDENTLY_VERIFIED'
    'A8_NEW_IMAGE_VULNERABILITY_SCAN=NOT_YET_VERIFIED'
    'A8_READ_ONLY_CHECK_WRITES=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  } catch {
    'STOP_A8_BUILD_RESULT_RECONCILIATION'
    "REASON=$([string]$_.Exception.Message -replace '[^A-Za-z0-9_]', '_')"
    'A8_BUILD_RETRY=PROHIBITED'
    'A8_READ_ONLY_CHECK_WRITES=NONE'
  }
}
```

**Potential limits:** the Cloud Build list output might omit some requested Build fields, in which case the uniquely matched build is not guaranteed: STOP instead of counting a partial result. `results.images` and `sourceProvenance` may be absent in a listing or even describe; treat as not proven, not as passing. Exact source matching is deliberately strict and does not normalize or silently accept a mutable branch. If the browser/API is inaccessible, no second build or automatically widened IAM.

**State:** `A8_ONE_BUILD_CLI_EXIT_ZERO_OWNER_SCREENSHOT`, `A8_ONE_BUILD_ATTEMPT=CONSUMED`, `A8_SIGNED_PROVENANCE=UNKNOWN`, `A8_IMAGE_SECURITY_SCAN=NOT_YET_VERIFIED`, `STEP04=HOLD`, `PRODUCTION=NO_GO`. Other earlier A1–A7/C1–C5/B1/R1/G4 checks remain consumed. Official reference: https://docs.cloud.google.com/sdk/gcloud/reference/builds/describe ; https://docs.cloud.google.com/build/docs/api/reference/rest/v1/projects.locations.builds .
