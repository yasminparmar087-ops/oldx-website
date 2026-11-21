# OLDX Step 04 — G4 parent metadata receipt and one-scope B1 pre-write service guard
Date: 21 Nov 2026 ~18:08 IST. Branch `security-hardening-review`. **B1 NOT DEPLOYED.**

## Owner screenshot: ONE Cloud Resource Manager project GET complete

Observed Windows PowerShell terminal output, after the earlier cached env check, without printing parent IDs:
```text
G4_PROJECT_PARENT=NO_PARENT_REPORTED
G4_PROJECT_PARENT_READ=COMPLETE_WITH_LIMITS
G4_PARENT_READ_CLOUD_CHANGES=NONE
```

**Interpretation:** `gcloud projects describe oldx-staging` succeeded for the expected project and its metadata did not include a `parent` field. This supports `G4_PROJECT_ORG_FOLDER_PARENT=NOT_REPORTED`, consistent with a stand-alone/no-organization project, and removes a concrete reason to conduct org/folder-parent inherited-policy traversal *if this metadata is authoritative and unchanged*. **Do not label all effective IAM approved or fully exclusive**. Service/project Owner/Editor roles, custom roles, member-group access, runtime SA permissions and other Firestore database denial remain separately in scope. Google [resource hierarchy documentation](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects) allows a top-level No organization project; [project describe documentation](https://docs.cloud.google.com/resource-manager/docs/view-update-projects) includes project parent metadata. This snapshot is as-of-observed, not a permanent lock.

`G4_PARENT_METADATA_GET=COMPLETE_DO_NOT_REPEAT`
`G4_PARENT_INHERITED_FOLDER_OR_ORG=NOT_REPORTED`
`G4_FULL_EFFECTIVE_IAM_EXCLUSIVITY=UNVERIFIED`
`G4_OTHER_DATABASE_DENIAL=UNVERIFIED`

## One **new** immediately pre-write Cloud Run service state check (PREPARED, NOT EXECUTED)

This is a **single new service describe GET**, intentionally not rerunning the old G4-A three-policy GET block or C5 revision-specific reads. It ensures exact original service latest-template image, runtime service account, original root traffic and old tags, explicit 2 false environment keys, zero env-key secret refs, zero volumes and secret annotation, IAM-invoker check not explicitly disabled, and no new `ownerreadv2` tag before **one** conditional B1 attempt.

**Run only immediately before a real B1 operator decision, while owner supervising; if B1 is postponed this check becomes historical and should not trigger repeat reads merely for reassurance.** This command does no writes, secrets are never output. A STOP means freeze, diagnose that single new deviation, no automatic retry. It cannot establish *current* effective IAM: prior 17:48 G4-A direct IAM check is a point-in-time receipt, and security changes after it are separately possible. The B1 rollout must remain strictly private DEFAULT-OFF/503 with all caveats understood.

```powershell
& {
  try {
    $raw = & gcloud.cmd run services describe oldx-owner-read --project=oldx-staging --region=asia-south1 --account=yasminparmar087@gmail.com --format=json 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) { throw 'SERVICE_READ_FAILED' }
    $s = $raw | Out-String | ConvertFrom-Json -ErrorAction Stop

    if ([string]$s.metadata.name -cne 'oldx-owner-read' -or
        [string]$s.status.latestReadyRevisionName -cne 'oldx-owner-read-00003-nus' -or
        [string]$s.spec.template.spec.serviceAccountName -cne 'oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com') {
      throw 'IDENTITY_OR_LATEST_DRIFT'
    }
    $ann = $s.metadata.annotations
    if ([string]$ann.'run.googleapis.com/ingress' -cne 'all' -or
        [string]$ann.'run.googleapis.com/invoker-iam-disabled' -notin @('','false')) {
      throw 'ACCESS_CONFIGURATION_DRIFT'
    }

    $containers = @($s.spec.template.spec.containers | Where-Object { $null -ne $_ })
    if ($containers.Count -ne 1) { throw 'CONTAINER_COUNT_DRIFT' }
    $c = $containers[0]
    if ([string]$c.image -cne 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-owner-read-step3-rc@sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc') {
      throw 'TEMPLATE_IMAGE_DRIFT'
    }
    $envs = @($c.env | Where-Object { $null -ne $_ })
    $required = @('OLDX_PRODUCT_READ_ACTIVATE_STAGING','OLDX_PRODUCT_READ_STAGING_ADC')
    if ($envs.Count -ne 2) { throw 'ENV_COUNT_DRIFT' }
    foreach ($name in $required) {
      if (@($envs | Where-Object { $_.name -ceq $name -and [string]$_.value -ceq 'false' -and $null -eq $_.valueFrom }).Count -ne 1) {
        throw 'ENV_FLAG_OR_SECRET_DRIFT'
      }
    }
    if (@($s.spec.template.spec.volumes | Where-Object { $null -ne $_ }).Count -ne 0 -or
        @($c.volumeMounts | Where-Object { $null -ne $_ }).Count -ne 0 -or
        [string]$s.spec.template.metadata.annotations.'run.googleapis.com/secrets' -ne '') {
      throw 'VOLUME_OR_SECRET_DRIFT'
    }

    $t = @($s.status.traffic | Where-Object { $null -ne $_ })
    if ($t.Count -ne 3) { throw 'TRAFFIC_COUNT_DRIFT' }
    $r1 = @($t | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00001-8kr' })
    $r2 = @($t | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00002-tid' })
    $r3 = @($t | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00003-nus' })
    if ($r1.Count -ne 1 -or $r2.Count -ne 1 -or $r3.Count -ne 1 -or
        [string]$r1[0].percent -cne '100' -or [string]$r1[0].tag -ne '' -or
        [string]$r2[0].tag -cne 'healthcheck' -or [string]$r3[0].tag -cne 'step3rc14' -or
        [string]$r2[0].percent -notin @('','0') -or [string]$r3[0].percent -notin @('','0')) {
      throw 'TRAFFIC_OR_TAG_DRIFT'
    }
    'B1_FINAL_SERVICE_READ=PASS'
    'B1_FINAL_SERVICE_IDENTITY=MATCH'
    'B1_FINAL_LATEST_TEMPLATE=MATCH_OLD'
    'B1_FINAL_ENV=EXACT_TWO_FALSE'
    'B1_FINAL_SECRET_AND_VOLUME_REFS=ZERO'
    'B1_FINAL_ROOT_AND_OLD_TAGS=MATCH'
    'B1_FINAL_OWNERREADV2_TAG=ABSENT'
    'B1_FINAL_POLICY_PROOF=HISTORICAL_G4A_WITH_LIMITS'
    'B1_FINAL_DEPLOYMENT=NOT_STARTED'
    'B1_FINAL_SERVICE_PREWRITE=PASS_WITH_LIMITS'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^[A-Z_]+$') { $reason = 'UNEXPECTED_ERROR' }
    'STOP_B1_FINAL_SERVICE_PREWRITE'
    "REASON=$reason"
    'B1_FINAL_DEPLOYMENT=NOT_STARTED'
  }
}
```

## Exact approved B1 scope for later human release
- Owner conditional B1 one-trial scope consent, R1 tag-only removal approval, R2 original root restoration conditional approval, C4 six-CVE and G8 cost residual-risk acceptances with OFF-only limits already recorded.
- Immutable existing npm-free OCI index `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`; no new build, scan, signing/upload, IAM/Billing/Firebase/Rules changes.
- Separate **nonexecuting** draft at [two-false-env B1 command](OLDX_STEP04_B1_HISTORICAL_ENV_EXACT_TWO_FALSE_2026-11-21.md) uses `--no-traffic --tag=ownerreadv2`, `--no-deploy-health-check --cpu-throttling`, `--set-env-vars` exact two false flags, min0/max1, 1CPU/512Mi, concurrency1/timeout30; current SDK 593 flag-help verified. Do not paste a deploy from this document until fresh pre-write shows PASS and operator scope confirmed.
- Root `00001-8kr=100%`, tags `healthcheck` on `00002-tid`, `step3rc14` on `00003-nus` must persist. No host app request. A 0%-main tagged URL remains callable by authorized principals and may incur costs. `--no-deploy-health-check` disables deploy-time health probing, NOT all future startup.
- R1 removes **only** new tag after verifying revision; R2 is traffic **NO-OP** if original main/tags intact. Neither automatically restores changed service template or deletes new revision; no full rollback without separate incident review.
- Existing G2 independent original-builder provenance remains UNKNOWN; full G4 effective IAM and multi-DB negative test OPEN; Product API and production remain NO-GO.

**Decision ledger:** `G4_PARENT_METADATA=NO_PARENT_REPORTED`, `B1_FINAL_PREWRITE=SOURCE_ONLY_PREPARED`, `B1_CLOUD_WRITE=NONE`, `STEP04=HOLD`, `PRODUCTION=NO_GO`.
