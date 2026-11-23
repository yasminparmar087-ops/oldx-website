# OLDX A8 B1 - one private, 0%-main, default-OFF, owner-supervised deploy only.
# This creates ONE new Cloud Run revision. Never rerun on an ambiguous result.
& {
  try {
    $project = 'oldx-staging'
    $region = 'asia-south1'
    $service = 'oldx-owner-read'
    $account = 'yasminparmar087@gmail.com'
    $sa = 'oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com'
    $tag = 'a8off23nov'
    $oldImage = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-npmfree-20261121-a1@sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79'
    $a8Image = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'
    $marker = Join-Path $env:USERPROFILE 'oldx-step04-a8-b1-attempt-20261124.marker'
    if (Test-Path -LiteralPath $marker) { throw 'ONE_SHOT_ATTEMPT_ALREADY_RECORDED' }

    # New narrow pre-WRITE drift guard; prior full A8 prewrite already PASSED and is consumed.
    $read = @("--project=$project","--region=$region","--account=$account",'--format=json','--quiet')
    $raw = & gcloud.cmd run services describe $service @read 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) { throw 'SERVICE_FRESH_READ_FAILED' }
    $s = $raw | Out-String | ConvertFrom-Json -ErrorAction Stop
    if ([string]$s.metadata.name -cne $service -or
        [string]$s.status.latestReadyRevisionName -cne 'oldx-owner-read-00010-zud' -or
        [string]$s.spec.template.spec.serviceAccountName -cne $sa) {
      throw 'SERVICE_IDENTITY_OR_LATEST_DRIFT'
    }
    if ([string]$s.metadata.annotations.'run.googleapis.com/ingress' -cne 'all' -or
        [string]$s.metadata.annotations.'run.googleapis.com/invoker-iam-disabled' -notin @('','false')) {
      throw 'SERVICE_AUTH_OR_INGRESS_DRIFT'
    }
    $containers = @($s.spec.template.spec.containers | Where-Object { $null -ne $_ })
    if ($containers.Count -ne 1 -or [string]$containers[0].image -cne $oldImage) {
      throw 'EXISTING_IMAGE_OR_CONTAINER_DRIFT'
    }
    $c = $containers[0]
    $envs = @($c.env | Where-Object { $null -ne $_ })
    if ($envs.Count -ne 2) { throw 'EXISTING_ENV_COUNT_DRIFT' }
    foreach ($key in @('OLDX_PRODUCT_READ_ACTIVATE_STAGING','OLDX_PRODUCT_READ_STAGING_ADC')) {
      if (@($envs | Where-Object {
        [string]$_.name -ceq $key -and [string]$_.value -ceq 'false' -and $null -eq $_.valueFrom
      }).Count -ne 1) { throw 'EXISTING_ACTIVATION_FLAG_DRIFT' }
    }
    if (@($s.spec.template.spec.volumes | Where-Object { $null -ne $_ }).Count -ne 0 -or
        @($c.volumeMounts | Where-Object { $null -ne $_ }).Count -ne 0 -or
        [string]$s.spec.template.metadata.annotations.'run.googleapis.com/secrets' -ne '') {
      throw 'EXISTING_SECRET_OR_VOLUME_DRIFT'
    }
    $traffic = @($s.status.traffic | Where-Object { $null -ne $_ })
    $main = @($traffic | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00001-8kr' })
    $health = @($traffic | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00002-tid' })
    $step3 = @($traffic | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00003-nus' })
    if ($traffic.Count -ne 3 -or $main.Count -ne 1 -or
        $health.Count -ne 1 -or $step3.Count -ne 1 -or
        [string]$main[0].percent -cne '100' -or [string]$main[0].tag -ne '' -or
        [string]$health[0].tag -cne 'healthcheck' -or
        [string]$step3[0].tag -cne 'step3rc14' -or
        [string]$health[0].percent -notin @('','0') -or
        [string]$step3[0].percent -notin @('','0') -or
        @($traffic | Where-Object { $_.tag -cin @('ownerreadv2','a8off23nov') }).Count -ne 0) {
      throw 'MAIN_TRAFFIC_OR_TAG_DRIFT'
    }
    $policyRaw = & gcloud.cmd run services get-iam-policy $service @read 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $policyRaw) { throw 'DIRECT_IAM_READ_FAILED' }
    $policy = $policyRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $public = @($policy.bindings | ForEach-Object { $_.members } |
      Where-Object { $_ -cin @('allUsers','allAuthenticatedUsers') }).Count
    $directInvoker = @($policy.bindings | Where-Object {
      [string]$_.role -ceq 'roles/run.invoker'
    } | ForEach-Object { $_.members } | Where-Object { $_ }).Count
    if ($public -ne 0 -or $directInvoker -ne 1) {
      throw 'DIRECT_IAM_ACCESS_DRIFT'
    }
    'A8_B1_IMMEDIATE_PREWRITE=PASS_WITH_LIMITS'
    'A8_B1_INHERITED_IAM=OWNER_ACCEPTED_LIMIT_NOT_PROVEN'
    'A8_B1_A8_IMAGE=EXACT_PINNED_NEW_DIGEST'
    'A8_B1_OLD_MAIN_AND_TAGS=PREWRITE_PRESERVED'
    'A8_B1_ONE_SHOT_DEPLOY=BEGINNING'

    # CreateNew is exclusive: if an attempt marker already exists, never launch another deploy.
    $file = [System.IO.File]::Open($marker,[System.IO.FileMode]::CreateNew,
      [System.IO.FileAccess]::Write,[System.IO.FileShare]::None)
    $file.Dispose()

    $args = @('run','deploy',$service,
      "--project=$project","--region=$region","--account=$account",
      "--image=$a8Image","--service-account=$sa",
      '--no-traffic',"--tag=$tag",
      '--no-deploy-health-check','--cpu-throttling',
      '--cpu=1','--memory=512Mi','--concurrency=1',
      '--timeout=30','--min-instances=0','--max-instances=1',
      '--set-env-vars=OLDX_PRODUCT_READ_ACTIVATE_STAGING=false,OLDX_PRODUCT_READ_STAGING_ADC=false')
    & gcloud.cmd @args
    if ($LASTEXITCODE -ne 0) { throw 'DEPLOY_CLI_FAILED_OUTCOME_UNKNOWN' }
    'A8_B1_DEPLOY_CLI=EXIT_ZERO_POSTCHECK_REQUIRED'
    'A8_B1_NEW_TAG=a8off23nov_NOT_YET_VERIFIED'
    'A8_B1_POSTWRITE_TRAFFIC_AND_IMAGE=NOT_YET_VERIFIED'
    'A8_B1_HOSTED_HTTP=NOT_INVOKED'
    'A8_B1_R1_TAG_CLEANUP=NOT_EXECUTED'
    'A8_B1_R2=NO_OP_UNLESS_DRIFT'
    'A8_B1_NO_AUTOMATIC_RETRY=TRUE'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^[A-Z_]+$') { $reason = 'UNEXPECTED_ERROR' }
    'STOP_A8_B1_NO_AUTOMATIC_RETRY'
    "REASON=$reason"
    'A8_B1_VERIFY_ACTUAL_SERVICE_STATE_BEFORE_ANY_WRITE=TRUE'
  }
}
