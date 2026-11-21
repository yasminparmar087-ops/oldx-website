# OLDX Step04 — B1 new revision deployed, post-deploy metadata check READY

## 21 Nov 2026 ~18:20 IST — B1 post-deploy 3-GET PASS WITH LIMITS; frozen OCI AMD64 CHILD DIGEST EXACT MATCH (NEW LATEST)

Owner's screenshot of the **single bounded post-B1 read-only** service + new `oldx-owner-read-00010-zud` revision + service IAM GETs shows `B1_POST_METADATA=PASS_WITH_LIMITS`, old root `00001-8kr=100%` and old `healthcheck`/`step3rc14` tags `MATCH`, new `ownerreadv2` tag on `00010-zud` **0%-main** MATCH, exact service OCI index `0844b637...` MATCH, new both feature flags EXACT_FALSE, resource/scaling PASS, **zero direct public principals and one direct service Invoker**. Cloud Run emitted resolved revision child `sha256:3150d898c8e013c833bac8b7f8adb8411023449093658d5c5c478a55d7ec28d1`: **byte-for-byte EQUAL** to already-frozen registry Linux/AMD64 C2 manifest under signed index `sha256:0844b637...` as documented in [npm-free custody C2 resolved discrepancy](docs/OLDX_STEP04_NPMFREE_NO_REBUILD_CUSTODY_ROUTE_2026-11-21.md). **No digest mismatch**; NO new registry/scan/build/sign/get needed. Canonical [B1 PASS+child-match receipt](docs/OLDX_STEP04_B1_POST_DEPLOY_PASS_CHILD_MATCH_2026-11-21.md). This metadata verifies only private DEFAULT-OFF/503 intended configuration with limits; no hosted 503 API response was requested, IAM exclusivity/other-database deny still unknown, 1 CRITICAL/5 HIGH scanner findings retained under owner OFF-only acceptance. Owner already conditionally approved B1 and R1/R2. **Next** end single supervised tagged trial via owner-approved **R1 remove only `ownerreadv2`** after fresh exact-state traffic/tag guard, post-confirm old root/tags; **R2 NO-OP** while original 100% root intact. R1 removes tag but not latest template/new revision. `B1_DEPLOYED=YES_ONCE`, `B1_POST_METADATA=PASS_WITH_LIMITS`, `B1_CHILD_DIGEST=MATCH_FROZEN_C2`, `R1_EXECUTED=NO`, `STEP04=HOLD`, production NO-GO. All old GETs C5/G4 and scans consumed; do not repeat for reassurance.


Date: 21 Nov 2026 ~18:16 IST. Owner observed actual Google Cloud SDK 593 PowerShell console deployment. This packet is written only to `security-hardening-review` and does NOT trigger a second deployment or requests to the new URL.

## Actual deployment receipt from owner screenshot — CONSUMED

Exactly **one** owner-run approved `gcloud.cmd run deploy oldx-owner-read` with immutable existing image index `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`, `--no-traffic --tag=ownerreadv2`, two explicit literal false env flags, `--no-deploy-health-check --cpu-throttling`, 1 CPU, 512Mi, concurrency1, timeout30, min0/max1, same runtime service account, expected project/region.

```text
Deploying container to Cloud Run service [oldx-owner-read] in project [oldx-staging] region [asia-south1]
OK Deploying... Done.
  OK Creating Revision...
Done.
Service [oldx-owner-read] revision [oldx-owner-read-00010-zud] has been deployed and is serving 0 percent of traffic.
```

Screenshot contains a generated `ownerreadv2` dedicated tag URL (omitted here as no invocations are authorized). It also shows returned PowerShell prompt. **B1_NEW_REVISION_CREATED=YES**, `B1_NEW_REVISION=oldx-owner-read-00010-zud`, **`B1_MAIN_TRAFFIC_NEW_REVISION=0_PERCENT_AS_REPORTED_BY_CLI`**. **DO NOT repeat deploy.** This is a CLI successful *create* receipt, NOT confirmation of old root/old tags, deployed index vs resolved child digest, current IAM, all runtime flags or resources; independent post-deploy read-only metadata is still required. There are no hosted API calls, billing/IAM/Firebase writes, new scans/builds/uploads or run rollback commands reported.

## One bounded after-deploy read-only verification, NOT YET EXECUTED

Windows PowerShell, **once**, with explicit project/account/region; only **3 GETs**: `run services describe`, `run revisions describe oldx-owner-read-00010-zud`, `run services get-iam-policy`. No GETs for old revisions, project IAM or G8 billing, no HTTP calls to tagged URL. Parses in memory and prints only sanitized statuses and any resolved digest. Checks original root 100% revision `00001-8kr`, old `healthcheck`/exact `step3rc14` bindings, new `ownerreadv2` on exactly `00010-zud` at 0% main, template OCI-index digest, new revision env flags and no volumes, CPU/memory/concurrency/timeout/min/max, direct public IAM count zero and one Run Invoker. **Must not conflate revision resolved child digest with OCI index digest; output resolved digest for comparison with already frozen C2 child, do not call it tampered without evidence.** `G4_PARENT_ORG_FOLDER_PARENT=NO_PARENT_REPORTED` in earlier read, but project custom roles / effective IAM exclusive invocation and other-DB denial still not proven.

```powershell
& {
  try {
    $common = @('--project=oldx-staging','--account=yasminparmar087@gmail.com','--format=json','--quiet')
    $rawS = & gcloud.cmd run services describe oldx-owner-read --region=asia-south1 @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $rawS) { throw 'SERVICE_READ_FAILED' }
    $s = $rawS | Out-String | ConvertFrom-Json -ErrorAction Stop
    'B1_POST_SERVICE_READ=PASS'

    $rawR = & gcloud.cmd run revisions describe oldx-owner-read-00010-zud --region=asia-south1 @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $rawR) { throw 'REVISION_READ_FAILED' }
    $r = $rawR | Out-String | ConvertFrom-Json -ErrorAction Stop
    'B1_POST_REVISION_READ=PASS'

    $rawI = & gcloud.cmd run services get-iam-policy oldx-owner-read --region=asia-south1 @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $rawI) { throw 'SERVICE_IAM_READ_FAILED' }
    $policy = $rawI | Out-String | ConvertFrom-Json -ErrorAction Stop
    'B1_POST_SERVICE_IAM_READ=PASS'

    $newRev = 'oldx-owner-read-00010-zud'
    $wantedImage = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-npmfree-20261121-a1@sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79'
    $wantedSA = 'oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com'
    if ([string]$s.metadata.name -cne 'oldx-owner-read' -or
        [string]$s.status.latestReadyRevisionName -cne $newRev -or
        [string]$r.metadata.name -cne $newRev) { throw 'SERVICE_OR_REVISION_IDENTITY_DRIFT' }

    $traffic = @($s.status.traffic | Where-Object { $null -ne $_ })
    if ($traffic.Count -ne 4) { throw 'TRAFFIC_ENTRY_COUNT_DRIFT' }
    $a = @($traffic | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00001-8kr' })
    $h = @($traffic | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00002-tid' })
    $t = @($traffic | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00003-nus' })
    $n = @($traffic | Where-Object { $_.revisionName -ceq $newRev })
    if ($a.Count -ne 1 -or $h.Count -ne 1 -or $t.Count -ne 1 -or $n.Count -ne 1 -or
        [string]$a[0].percent -cne '100' -or [string]$a[0].tag -ne '' -or
        [string]$h[0].tag -cne 'healthcheck' -or [string]$t[0].tag -cne 'step3rc14' -or
        [string]$n[0].tag -cne 'ownerreadv2' -or
        [string]$h[0].percent -notin @('','0') -or
        [string]$t[0].percent -notin @('','0') -or
        [string]$n[0].percent -notin @('','0')) { throw 'TRAFFIC_OR_TAG_DRIFT' }
    'B1_POST_OLD_MAIN_AND_TAGS=MATCH'
    'B1_POST_NEW_TAG_ZERO_MAIN=MATCH'

    if ([string]$s.spec.template.spec.serviceAccountName -cne $wantedSA -or
        [string]$r.spec.serviceAccountName -cne $wantedSA) { throw 'RUNTIME_IDENTITY_DRIFT' }
    $sCont = @($s.spec.template.spec.containers | Where-Object { $null -ne $_ })
    $rCont = @($r.spec.containers | Where-Object { $null -ne $_ })
    if ($sCont.Count -ne 1 -or $rCont.Count -ne 1) { throw 'CONTAINER_COUNT_DRIFT' }
    if ([string]$sCont[0].image -cne $wantedImage) { throw 'SERVICE_IMAGE_INDEX_MISMATCH' }
    'B1_POST_SERVICE_TEMPLATE_IMAGE_INDEX=MATCH'
    $revisionImage = [string]$rCont[0].image
    if ($revisionImage -ceq $wantedImage) {
      'B1_POST_REVISION_IMAGE=EXACT_INDEX'
    } elseif ($revisionImage -match '@sha256:([a-f0-9]{64})$') {
      "B1_POST_REVISION_RESOLVED_DIGEST=sha256:$($Matches[1])"
      'B1_POST_REVISION_IMAGE=RESOLVED_DIGEST_REQUIRES_FROZEN_CHILD_MATCH'
    } else { throw 'REVISION_IMAGE_UNEXPECTED' }

    $envs = @($rCont[0].env | Where-Object { $null -ne $_ })
    if ($envs.Count -ne 2) { throw 'REVISION_ENV_COUNT_DRIFT' }
    foreach ($key in @('OLDX_PRODUCT_READ_ACTIVATE_STAGING','OLDX_PRODUCT_READ_STAGING_ADC')) {
      if (@($envs | Where-Object { $_.name -ceq $key -and [string]$_.value -ceq 'false' -and $null -eq $_.valueFrom }).Count -ne 1) {
        throw 'REVISION_ENV_NOT_EXACT_FALSE'
      }
    }
    'B1_POST_REVISION_ENV=EXACT_TWO_FALSE'
    if (@($r.spec.volumes | Where-Object { $null -ne $_ }).Count -ne 0 -or
        @($rCont[0].volumeMounts | Where-Object { $null -ne $_ }).Count -ne 0) {
      throw 'REVISION_VOLUME_DRIFT'
    }
    if ([string]$r.spec.containerConcurrency -cne '1' -or
        [string]$r.spec.timeoutSeconds -notin @('30','30s') -or
        [string]$rCont[0].resources.limits.cpu -cne '1' -or
        [string]$rCont[0].resources.limits.memory -cne '512Mi') {
      throw 'REVISION_RESOURCE_DRIFT'
    }
    'B1_POST_REVISION_RESOURCES=CPU1_MEM512Mi_CONCURRENCY1_TIMEOUT30'
    $maxScale = [string]$r.metadata.annotations.'autoscaling.knative.dev/maxScale'
    $minScale = [string]$r.metadata.annotations.'autoscaling.knative.dev/minScale'
    if ($maxScale -cne '1' -or $minScale -notin @('','0')) { throw 'REVISION_SCALING_DRIFT' }
    'B1_POST_REVISION_SCALING=MIN_ZERO_OR_UNSET_MAX_ONE'

    $public = @($policy.bindings | ForEach-Object { $_.members } |
      Where-Object { $_ -cin @('allUsers','allAuthenticatedUsers') }).Count
    $invokers = @($policy.bindings | Where-Object { $_.role -ceq 'roles/run.invoker' } |
      ForEach-Object { $_.members } | Where-Object { $_ }).Count
    $ingress = [string]$s.metadata.annotations.'run.googleapis.com/ingress'
    $iamDisabled = [string]$s.metadata.annotations.'run.googleapis.com/invoker-iam-disabled'
    if ($public -ne 0 -or $invokers -ne 1 -or
        $ingress -cne 'all' -or $iamDisabled -notin @('','false')) {
      throw 'DIRECT_IAM_OR_INGRESS_DRIFT'
    }
    'B1_POST_SERVICE_DIRECT_IAM=NO_PUBLIC_MEMBER_ONE_INVOKER'
    'B1_POST_PARENT_EFFECTIVE_IAM=NOT_FULLY_PROVEN'
    'B1_POST_OTHER_DATABASE_DENY=UNVERIFIED'
    'B1_POST_HOSTED_PRODUCT_REQUESTS=NOT_PERFORMED'
    'B1_POST_METADATA=PASS_WITH_LIMITS'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^[A-Z_]+$') { $reason = 'UNEXPECTED_ERROR' }
    'STOP_B1_POST_DEPLOY_VERIFICATION'
    "REASON=$reason"
    'B1_POST_METADATA=NOT_VERIFIED'
  }
}
```

**If STOP:** Do not run B1 again and do not automatically remove tag or restore traffic. Diagnose the specific mismatch using existing values, then choose the narrowly approved R1 or R2 only if its conditional scope actually applies. Cloud Run tag-only removal does NOT erase new revision/latest template. If the postcheck succeeds, do not declare live Product API enabled/production ready.

## Status (as-of actual screenshot)
`B1_OWNER_ONE_SHOT_DEPLOY_COMMAND=EXECUTED_ONCE`
`B1_REVISION_CREATE_CLI=SUCCESS`
`B1_NEW_REVISION=oldx-owner-read-00010-zud`
`B1_NEW_REVISION_MAIN_TRAFFIC_CLI=0_PERCENT`
`B1_POST_DEPLOY_METADATA_VERIFICATION=PENDING`
`R1_EXECUTED=NO`
`R2_EXECUTED=NO`
`C4_G8_OWNER_RISK_ACCEPTED=OFF_ONLY_WITH_LIMITS`
`G4_EFFECTIVE_EXCLUSIVE_IAM_AND_OTHER_DB_DENY=UNVERIFIED`
`G2_TRUSTED_BUILDER_PROVENANCE=UNKNOWN`
`STEP04=HOLD`
`PRODUCTION=NO_GO`

References: [Cloud Run revision management](https://docs.cloud.google.com/run/docs/managing/revisions), [tag and traffic semantics](https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration), [revision digest fields](https://docs.cloud.google.com/run/docs/reference/rest/v1/namespaces.revisions).
