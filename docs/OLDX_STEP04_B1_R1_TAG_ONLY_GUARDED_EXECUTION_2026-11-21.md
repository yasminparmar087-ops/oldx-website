# OLDX Step04 — owner-approved R1 only-new-tag cleanup, guarded
21 Nov 2026 ~18:20 IST. SOURCE ONLY: script prepared, NOT EXECUTED. Running this is a Cloud Run traffic-tag **WRITE**, unlike previous read-only checks.

## Inputs — previously verified and consumed
- New Cloud Run revision `oldx-owner-read-00010-zud` tagged `ownerreadv2` is 0%-main, exact frozen AMD64 child digest matches, env 2 false and direct service IAM no public member: [B1 post evidence](OLDX_STEP04_B1_POST_DEPLOY_PASS_CHILD_MATCH_2026-11-21.md).
- Existing root `oldx-owner-read-00001-8kr` 100%; old `healthcheck` and `step3rc14` intact. Previous post-B1 3 GETs consumed. No repeat build/upload/sign/Grype/old G4A/C5.
- User already gave explicit conditional **R1 approval**, remove only new `ownerreadv2` tag when ending this short private staging trial, and conditional **R2 approval** only if root main drifted. No production or Product API enablement.

## One guarded R1 Windows PowerShell operator block — not yet run
First one **fresh** read-only `services describe` checks that exactly four expected traffic entries remain, original root 100%, old two tags unchanged and new tag belongs only to `00010-zud` at 0%. Only then performs **one** `update-traffic --remove-tags=ownerreadv2` and **one** post-write `services describe` to confirm original root/tags and new tag absent. No IAM or billing write. The service may retain newest revision/template after the tag is removed. Cloud Run API CLI does not provide atomic compare-and-swap, so concurrent updates remain a residual risk; supervisor must stop other operators.

```powershell
& {
  try {
    $common = @('--project=oldx-staging','--region=asia-south1','--account=yasminparmar087@gmail.com','--format=json')
    $raw = & gcloud.cmd run services describe oldx-owner-read @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) { throw 'R1_PRE_READ_FAILED' }
    $s = $raw | Out-String | ConvertFrom-Json -ErrorAction Stop
    if ([string]$s.metadata.name -cne 'oldx-owner-read' -or
        [string]$s.status.latestReadyRevisionName -cne 'oldx-owner-read-00010-zud') {
      throw 'R1_SERVICE_IDENTITY_DRIFT'
    }
    $t = @($s.status.traffic | Where-Object { $null -ne $_ })
    $main = @($t | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00001-8kr' })
    $health = @($t | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00002-tid' })
    $step3 = @($t | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00003-nus' })
    $trial = @($t | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00010-zud' })
    if ($t.Count -ne 4 -or $main.Count -ne 1 -or $health.Count -ne 1 -or
        $step3.Count -ne 1 -or $trial.Count -ne 1 -or
        [string]$main[0].percent -cne '100' -or $main[0].tag -or
        [string]$health[0].tag -cne 'healthcheck' -or
        [string]$step3[0].tag -cne 'step3rc14' -or
        [string]$trial[0].tag -cne 'ownerreadv2' -or
        [string]$health[0].percent -notin @('','0') -or
        [string]$step3[0].percent -notin @('','0') -or
        [string]$trial[0].percent -notin @('','0')) {
      throw 'R1_TRAFFIC_PREIMAGE_DRIFT'
    }
    'R1_FRESH_PREIMAGE=MATCH'
    'R1_REMOVE_ONLY_TAG=ownerreadv2'
    & gcloud.cmd run services update-traffic oldx-owner-read --project=oldx-staging --region=asia-south1 --account=yasminparmar087@gmail.com --remove-tags=ownerreadv2
    if ($LASTEXITCODE -ne 0) { throw 'R1_WRITE_OUTCOME_UNCERTAIN' }
    'R1_WRITE_CLI=EXIT_ZERO'
    $afterRaw = & gcloud.cmd run services describe oldx-owner-read @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $afterRaw) { throw 'R1_POST_READ_FAILED' }
    $after = $afterRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $at = @($after.status.traffic | Where-Object { $null -ne $_ })
    $am = @($at | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00001-8kr' })
    $ah = @($at | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00002-tid' })
    $as = @($at | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00003-nus' })
    if ($am.Count -ne 1 -or $ah.Count -ne 1 -or $as.Count -ne 1 -or
        [string]$am[0].percent -cne '100' -or $am[0].tag -or
        [string]$ah[0].tag -cne 'healthcheck' -or
        [string]$as[0].tag -cne 'step3rc14' -or
        @($at | Where-Object { $_.tag -ceq 'ownerreadv2' }).Count -ne 0 -or
        @($at | Where-Object {
          $_.revisionName -cne 'oldx-owner-read-00001-8kr' -and
          [string]$_.percent -notin @('','0')
        }).Count -ne 0) { throw 'R1_POST_TRAFFIC_DRIFT' }
    'R1_NEW_TAG=ABSENT'
    'R1_OLD_MAIN_AND_TAGS=PRESERVED'
    'R2_TRAFFIC_RESTORE=NOT_REQUIRED_NO_OP'
    'R1_TAG_ONLY_REMOVAL=COMPLETE_WITH_LIMITS'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^R1_[A-Z_]+$') { $reason = 'R1_UNEXPECTED_ERROR' }
    'STOP_R1_NO_AUTOMATIC_RETRY'
    "REASON=$reason"
    'R1_CONFIRM_LIVE_STATE_BEFORE_ANY_NEW_WRITE'
  }
}
```

**STOP/no auto-retry:** any guard mismatch, command error or ambiguous post-state -> halt and inspect current state; don't redeploy B1 or blindly replay R1/R2. A successful R1 is *tag-only removal*, not deletion of new revision, rollback of service template, zero charges or proof of effective other-DB IAM denial.

Expected statuses until run: `B1_POST_METADATA=PASS_WITH_LIMITS`; `B1_CHILD_DIGEST=MATCH_FROZEN_C2`; `R1_GUARD_EXECUTION=NOT_STARTED`; `R2=NO_OP_WHILE_MAIN_100`; `STEP04=HOLD`; `PRODUCTION=NO_GO`.

Google official `update-traffic --remove-tags`: https://docs.cloud.google.com/sdk/gcloud/reference/run/services/update-traffic