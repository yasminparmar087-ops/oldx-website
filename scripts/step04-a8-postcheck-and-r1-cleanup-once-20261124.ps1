# OLDX A8 24-Nov owner-approved post-deploy metadata verification then R1 new-tag-only cleanup.
# ONE owner-supervised operation. Never rerun after any ambiguous traffic write.
& {
  try {
    $service = 'oldx-owner-read'
    $newRev = 'oldx-owner-read-00012-vib'
    $tag = 'a8off23nov'
    $sa = 'oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com'
    $a8 = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'
    $repo = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1'
    $common = @('--project=oldx-staging','--region=asia-south1','--account=yasminparmar087@gmail.com','--format=json','--quiet')
    $marker = Join-Path $env:USERPROFILE 'oldx-step04-a8-r1-attempt-20261124.marker'
    if (Test-Path -LiteralPath $marker) { throw 'R1_ALREADY_ATTEMPTED_DO_NOT_RETRY' }

    # These are the ONE distinct POSTWRITE service/new-revision/direct-IAM checks.
    $sRaw = & gcloud.cmd run services describe $service @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $sRaw) { throw 'POST_SERVICE_READ_FAILED' }
    $s = $sRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $rRaw = & gcloud.cmd run revisions describe $newRev @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $rRaw) { throw 'POST_REVISION_READ_FAILED' }
    $r = $rRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $iamRaw = & gcloud.cmd run services get-iam-policy $service @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $iamRaw) { throw 'POST_SERVICE_IAM_READ_FAILED' }
    $iam = $iamRaw | Out-String | ConvertFrom-Json -ErrorAction Stop

    if ([string]$s.metadata.name -cne $service -or
        [string]$s.status.latestReadyRevisionName -cne $newRev -or
        [string]$r.metadata.name -cne $newRev -or
        [string]$s.spec.template.spec.serviceAccountName -cne $sa -or
        [string]$r.spec.serviceAccountName -cne $sa) {
      throw 'SERVICE_REVISION_OR_SA_DRIFT'
    }
    if ([string]$s.metadata.annotations.'run.googleapis.com/ingress' -cne 'all' -or
        [string]$s.metadata.annotations.'run.googleapis.com/invoker-iam-disabled' -notin @('','false')) {
      throw 'INGRESS_OR_IAM_CHECK_DRIFT'
    }
    $sContainers = @($s.spec.template.spec.containers | Where-Object { $null -ne $_ })
    $rContainers = @($r.spec.containers | Where-Object { $null -ne $_ })
    if ($sContainers.Count -ne 1 -or $rContainers.Count -ne 1 -or
        [string]$sContainers[0].image -cne $a8) {
      throw 'EXACT_A8_IMAGE_TEMPLATE_MISMATCH'
    }
    $rImage = [string]$rContainers[0].image
    if ($rImage -cne $a8 -and
        -not $rImage.StartsWith($repo + '@sha256:',[System.StringComparison]::Ordinal)) {
      throw 'REVISION_REPOSITORY_OR_DIGEST_DRIFT'
    }
    if ($rImage -ne $a8 -and $rImage -notmatch '@sha256:[a-f0-9]{64}$') {
      throw 'REVISION_RESOLVED_DIGEST_FORMAT_DRIFT'
    }
    $envs = @($rContainers[0].env | Where-Object { $null -ne $_ })
    if ($envs.Count -ne 2) { throw 'REVISION_ENV_COUNT_DRIFT' }
    foreach ($key in @('OLDX_PRODUCT_READ_ACTIVATE_STAGING','OLDX_PRODUCT_READ_STAGING_ADC')) {
      if (@($envs | Where-Object {
        [string]$_.name -ceq $key -and [string]$_.value -ceq 'false' -and $null -eq $_.valueFrom
      }).Count -ne 1) { throw 'REVISION_ACTIVATION_OR_ADC_DRIFT' }
    }
    if (@($r.spec.volumes | Where-Object { $null -ne $_ }).Count -ne 0 -or
        @($rContainers[0].volumeMounts | Where-Object { $null -ne $_ }).Count -ne 0) {
      throw 'REVISION_VOLUME_OR_SECRET_DRIFT'
    }
    if ([string]$r.spec.containerConcurrency -cne '1' -or
        [string]$r.spec.timeoutSeconds -notin @('30','30s') -or
        [string]$rContainers[0].resources.limits.cpu -cne '1' -or
        [string]$rContainers[0].resources.limits.memory -cne '512Mi') {
      throw 'REVISION_RESOURCES_DRIFT'
    }
    $max = [string]$r.metadata.annotations.'autoscaling.knative.dev/maxScale'
    $min = [string]$r.metadata.annotations.'autoscaling.knative.dev/minScale'
    if ($max -cne '1' -or $min -notin @('','0')) { throw 'REVISION_SCALING_DRIFT' }

    $t = @($s.status.traffic | Where-Object { $null -ne $_ })
    $main = @($t | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00001-8kr' })
    $health = @($t | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00002-tid' })
    $step3 = @($t | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00003-nus' })
    $new = @($t | Where-Object { $_.revisionName -ceq $newRev })
    if ($t.Count -ne 4 -or $main.Count -ne 1 -or $health.Count -ne 1 -or
        $step3.Count -ne 1 -or $new.Count -ne 1 -or
        [string]$main[0].percent -cne '100' -or [string]$main[0].tag -ne '' -or
        [string]$health[0].tag -cne 'healthcheck' -or
        [string]$step3[0].tag -cne 'step3rc14' -or
        [string]$new[0].tag -cne $tag -or
        [string]$health[0].percent -notin @('','0') -or
        [string]$step3[0].percent -notin @('','0') -or
        [string]$new[0].percent -notin @('','0')) {
      throw 'TRAFFIC_TAG_OR_ROOT_DRIFT'
    }

    $public = @($iam.bindings | ForEach-Object { $_.members } |
      Where-Object { $_ -cin @('allUsers','allAuthenticatedUsers') }).Count
    $directInvoker = @($iam.bindings | Where-Object {
      [string]$_.role -ceq 'roles/run.invoker'
    } | ForEach-Object { $_.members } | Where-Object { $_ }).Count
    if ($public -ne 0 -or $directInvoker -ne 1) { throw 'DIRECT_IAM_DRIFT' }

    'A8_POST_SERVICE_REVISION_IAM=PASS_WITH_LIMITS'
    'A8_POST_NEW_REVISION=00012_VIB'
    'A8_POST_SERVICE_IMAGE=EXACT_SIGNED_A8_INDEX'
    if ($rImage -ceq $a8) {
      'A8_POST_REVISION_IMAGE=EXACT_A8_DIGEST'
    } else {
      'A8_POST_REVISION_IMAGE=RESOLVED_CHILD_DIGEST_REQUIRES_SEPARATE_CUSTODY_MATCH'
      "A8_POST_REVISION_RESOLVED_IMAGE=$rImage"
    }
    'A8_POST_NEW_TAG_0_PERCENT=VERIFIED'
    'A8_POST_OLD_ROOT_AND_TAGS=VERIFIED'
    'A8_POST_BOTH_FLAGS=EXACT_FALSE'
    'A8_POST_DIRECT_IAM=NO_PUBLIC_ONE_NAMED_INVOKER'
    'A8_POST_INHERITED_IAM=UNVERIFIED'
    'A8_POST_OTHER_DB_DENIAL=UNVERIFIED'
    'A8_POST_HOSTED_HTTP=NOT_INVOKED'
    'A8_R1_EXACT_PREIMAGE=PASS'
    'A8_R1_REMOVE_ONLY_TAG=a8off23nov'

    # Exclusive local marker to prevent repeating this already-approved R1 write.
    $file = [System.IO.File]::Open($marker,[System.IO.FileMode]::CreateNew,
      [System.IO.FileAccess]::Write,[System.IO.FileShare]::None)
    $file.Dispose()
    & gcloud.cmd run services update-traffic $service --project=oldx-staging --region=asia-south1 --account=yasminparmar087@gmail.com --remove-tags=a8off23nov
    if ($LASTEXITCODE -ne 0) { throw 'R1_CLI_RESULT_UNCERTAIN_NO_RETRY' }
    'A8_R1_WRITE_CLI=EXIT_ZERO'

    # Separate targeted read AFTER the ONLY traffic-tag write.
    $afterRaw = & gcloud.cmd run services describe $service @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $afterRaw) { throw 'R1_POST_SERVICE_READ_FAILED' }
    $after = $afterRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $at = @($after.status.traffic | Where-Object { $null -ne $_ })
    $am = @($at | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00001-8kr' })
    $ah = @($at | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00002-tid' })
    $as = @($at | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00003-nus' })
    if ([string]$after.metadata.name -cne $service -or
        $at.Count -ne 3 -or $am.Count -ne 1 -or $ah.Count -ne 1 -or
        $as.Count -ne 1 -or
        [string]$am[0].percent -cne '100' -or [string]$am[0].tag -ne '' -or
        [string]$ah[0].tag -cne 'healthcheck' -or
        [string]$as[0].tag -cne 'step3rc14' -or
        [string]$ah[0].percent -notin @('','0') -or
        [string]$as[0].percent -notin @('','0') -or
        @($at | Where-Object { $_.tag -ceq $tag }).Count -ne 0) {
      throw 'R1_POST_TRAFFIC_DRIFT'
    }
    'A8_R1_NEW_TAG=ABSENT'
    'A8_R1_OLD_100_PERCENT_MAIN_AND_TAGS=PRESERVED'
    'A8_R1_TAG_ONLY_CLEANUP=COMPLETE_WITH_LIMITS'
    'A8_R2_TRAFFIC_RESTORE=NO_OP_NOT_REQUIRED'
    'A8_NEW_REVISION_AND_LATEST_TEMPLATE=RETAINED_NOT_ROLLED_BACK'
    'A8_STEP04=HOLD_PENDING_G2_G4_G8'
    'A8_DEPLOY_R1_RETRY=PROHIBITED'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^[A-Z_]+$') { $reason = 'UNEXPECTED_ERROR' }
    'STOP_A8_POSTCHECK_OR_R1_NO_AUTOMATIC_RETRY'
    "REASON=$reason"
    'A8_MUST_RECONCILE_LIVE_STATE_BEFORE_ANY_NEW_WRITE'
  }
}
