# OLDX Step 04 — B1 SDK 593 secondary local flags PASS and cached-env inspection gate

## 21 Nov 2026 ~18:04 IST — cached B1 env inspection PASSED: exactly 2 false flags, 0 secrets (NEW LATEST)

Actual owner's Windows PowerShell screenshot shows **`B1_ENV_FROM_CACHED_SERVICE=YES_HISTORICAL`**, **`B1_ENV_NAME_COUNT=2`**, `B1_ENV_OTHER_NAMES=` (empty), **`B1_ENV_SECRET_REFERENCE_COUNT=0`**, **`B1_ENV_FLAGS=EXACT_FALSE`**, `B1_ENV_VALUES_OR_SECRETS_PRINTED=NO`, `B1_ENV_LOCAL_INSPECTION=COMPLETE`. All values from pre-existing `$svc` **cached historical latest service template**, **no new Cloud GET**, no deployment; **do NOT rerun**. Exact two keys are `OLDX_PRODUCT_READ_ACTIVATE_STAGING` and `OLDX_PRODUCT_READ_STAGING_ADC`. [Owner-observed env proof, nonexecuting digest-pinned B1 command draft, remaining STOPs](docs/OLDX_STEP04_B1_HISTORICAL_ENV_EXACT_TWO_FALSE_2026-11-21.md). Old 100%-main revision's flags MISSING, not proven false. The proposed `--set-env-vars` with precisely these two literal false values will only be safe if **fresh immediate prewrite** current service env/secret/volume/traffic guard matches; image pinned `sha256:0844b637...`, **`--no-traffic --tag=ownerreadv2`**, `--no-deploy-health-check`, `--cpu-throttling`, min0/max1, old main/tags preserved, no public IAM change; R1 tag-only/R2 conditional traffic approvals previously recorded. No direct deploy has been issued. **Next distinct read-only issue:** G4 parent organization/folder ancestry verification (`gcloud projects describe`, new metadata, not a repeated old G4 IAM policy GET); then prepare exact final pre-mutation drift guard. G4 parent inherited/other-DB still UNVERIFIED, independent builder provenance UNKNOWN, G2 HOLD, Step04 HOLD and production NO-GO.


Date: 21 November 2026 ~18:00 IST. Branch `security-hardening-review`. **SOURCE ONLY; no Cloud Run deployment or billing mutation**.

## New owner screenshot: actual second local help PASS

The owner ran once `gcloud.cmd run deploy --help | Select-String -Pattern '--no-deploy-health-check','--cpu-throttling','--invoker-iam-check'` on installed Google Cloud SDK 593.0.0. Windows PowerShell returned the normal prompt and displayed:

```text
requests. Use --cpu-throttling to enable and --no-cpu-throttling to ...
--no-deploy-health-check to disable.
Use --invoker-iam-check to enable and --no-invoker-iam-check to ...
```

These prove all three relevant flag spellings are exposed in the installed local CLI help. **No hosted execution or Cloud API call**. Do not rerun either local flag-help check, SDK version, previous C5 or 17:48 G4-A GETs. Do not update SDK merely for the available-update notice.

Google official [run deploy reference](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy) explains that the default deployment health check schedules one revision instance, while `--no-deploy-health-check` opts out of that *deploy-time* check. This **does not** prevent an instance from starting in the future if a caller invokes a tagged URL or scaling conditions change. Google official [service env config](https://docs.cloud.google.com/run/docs/configuring/services/environment-variables) warns `--set-env-vars` replaces omitted previous keys; `--update-env-vars` retains previously specified keys. Both must be reviewed against complete new-revision env-key and secret-reference expectations.

`B1_DEPLOY_HEALTH_FLAG_LOCAL_HELP=PASS`
`B1_CPU_THROTTLING_FLAG_LOCAL_HELP=PASS`
`B1_INVOKER_IAM_CHECK_FLAG_LOCAL_HELP=PASS`
`B1_SDK_VERSION=593.0.0`
`B1_HELP_CHECKS=COMPLETE_DO_NOT_REPEAT`
`B1_DEPLOYMENT=NOT_STARTED`
`STEP04=HOLD`

## Next minimally sufficient local-only diagnostic — NOT YET EXECUTED

Objective: identify **env key names only**, and **number** of secret references in the *previously loaded in-memory* `$svc` from the owner's ~17:03 snapshot. No values, tokens, account policy members or secret reference identities are printed. This is **source-only design evidence**, not a fresh authorization to deploy; old `$svc` remains historical.

Paste the following as **one block in the same PowerShell window** that still contains `$svc`:

```powershell
& {
  try {
    if ($null -eq $svc -or [string]$svc.metadata.name -cne 'oldx-owner-read') {
      throw 'B1_ENV_CACHED_SERVICE_NOT_AVAILABLE'
    }
    $containers = @($svc.spec.template.spec.containers | Where-Object { $null -ne $_ })
    if ($containers.Count -ne 1) { throw 'B1_ENV_CONTAINER_COUNT_UNEXPECTED' }
    $envs = @($containers[0].env | Where-Object { $null -ne $_ })
    $names = @($envs | ForEach-Object { [string]$_.name } | Sort-Object -Unique)
    if ($names.Count -ne $envs.Count) { throw 'B1_ENV_DUPLICATE_KEY_OR_UNNAMED_ENTRY' }
    foreach ($name in @('OLDX_PRODUCT_READ_ACTIVATE_STAGING','OLDX_PRODUCT_READ_STAGING_ADC')) {
      $match = @($envs | Where-Object { $_.name -ceq $name -and [string]$_.value -ceq 'false' -and $null -eq $_.valueFrom })
      if ($match.Count -ne 1) { throw 'B1_ENV_FLAG_NOT_EXACT_FALSE' }
    }
    $secretRefs = @($envs | Where-Object { $null -ne $_.valueFrom }).Count
    $otherNames = @($names | Where-Object { $_ -cnotin @('OLDX_PRODUCT_READ_ACTIVATE_STAGING','OLDX_PRODUCT_READ_STAGING_ADC') })
    'B1_ENV_FROM_CACHED_SERVICE=YES_HISTORICAL'
    "B1_ENV_NAME_COUNT=$($names.Count)"
    "B1_ENV_OTHER_NAMES=$($otherNames -join ',')"
    "B1_ENV_SECRET_REFERENCE_COUNT=$secretRefs"
    'B1_ENV_FLAGS=EXACT_FALSE'
    'B1_ENV_VALUES_OR_SECRETS_PRINTED=NO'
    'B1_ENV_LOCAL_INSPECTION=COMPLETE'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^B1_ENV_[A-Z0-9_]+$') { $reason = 'B1_ENV_UNEXPECTED_ERROR' }
    'STOP_B1_ENV_LOCAL_INSPECTION'
    "REASON=$reason"
  }
}
```

If `STOP_B1_ENV_LOCAL_INSPECTION`, do **NOT** rerun C5/G4-A or fetch fresh Cloud state just to recover a lost cache. Diagnose the single STOP. If `B1_ENV_LOCAL_INSPECTION=COMPLETE`, use the *names/counts only* to choose an exact safe new-revision env policy before writing any `gcloud run deploy` command. No changes to old revisions result from this read.

## B1 execution prerequisites still open

- Confirm exact new revision environment and **all inherited env/secret/volume relationships** using a fresh immediate pre-write service-state guard when the real B1 operation is being considered. This local historical cache does not prove current live state.
- New OCI index pinned: `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`. C3 local receipt previously verified, independent original trusted builder provenance remains UNKNOWN.
- Preserve old root main `oldx-owner-read-00001-8kr=100%`, old tags `healthcheck`, exact `step3rc14`. B1 only one future private `ownerreadv2` 0%-main, product activation flags `false`, no public caller, no real user data, no Firestore/Auth requests.
- Owner B1 conditional approval and R1/R2 conditional rollback approvals all recorded, but live execution is NOT yet permitted until all gates checked. R1 removing the new tag is NOT a restore of the service template; R2 is NO-OP while root main and old tags are intact, and any incident requires exact-state review.
- G4 inherited IAM/other-DB deny remains UNKNOWN; G8 all-provider hard cap unproven, residual OFF-only owner cost risk accepted; C4 1 CRITICAL/5 HIGH residual risk accepted strictly for OFF-only, not enabled traffic.
- No existing tests, Grype image scan, builds, signatures, uploads, old read-only probes or local CLI help are to be repeated for another PASS.

`B1_HISTORICAL_ENV_INVENTORY=PREPARED_NOT_EXECUTED`
`B1_EXACT_DEPLOY_COMMAND=SOURCE_REVIEW_PENDING`
`B1_CLOUD_WRITE=NONE`
`PRODUCTION=NO_GO`
