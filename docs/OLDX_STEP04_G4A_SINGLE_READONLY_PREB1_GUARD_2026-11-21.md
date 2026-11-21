# OLDX Step 04 — G4-A finite Cloud Run pre-B1 read-only guard (SOURCE-ONLY)

## 21 Nov 2026 ~17:48 IST — G4-A fresh 3-GET read-only preflight PASS WITH LIMITS (NEW LATEST)

**Actual owner PowerShell screenshot** captured returned prompt and complete sanitized output: `G4A_SERVICE_GET=PASS`, `G4A_SERVICE_IAM_GET=PASS`, `G4A_PROJECT_IAM_GET=PASS`, `G4A_PRIVATE_DIRECT_POLICY_GUARD=MATCH`, `G4A_TRAFFIC_PREIMAGE=MATCH`, main `oldx-owner-read-00001-8kr:100`, old tags **exact** `healthcheck,step3rc14`, latest service-template flags `EXACT_FALSE`, service named Invoker 1, project Owner 2 / Editor 1 / project direct Run Invoker 0. Ends **`G4A_READ_ONLY_PREB1=COMPLETE_WITH_LIMITS`** and **`G4A_DEPLOYMENT=NOT_STARTED`**, without STOP. Full sanitized receipt [G4-A owner-observed PASS](docs/OLDX_STEP04_G4A_PREFLIGHT_OBSERVED_PASS_2026-11-21.md). **The 3-read script is CONSUMED; DO NOT REPEAT.** This is only as-of-time direct service/project IAM preimage and existing template/traffic identity; `PARENT_INHERITED_IAM=NOT_VERIFIED`, `OTHER_DATABASE_EFFECTIVE_DENIAL=NOT_VERIFIED`, `EXCLUSIVE_OWNER_INVOCATION=NOT_PROVEN`; older 100%-traffic revision flags were MISSING. No hosted invocation, build, Registry operation or deployment.

Owner's **conditional B1 approval** and **C4/G8 OFF-only risk acceptances** remain in force only within their stated narrow limits. **B1 has NOT been deployed**. Next is to source-only finalize an exact one-shot B1/R1/R2 execution+rollback packet and obtain specific owner R1/R2 consent. Current screenshot will be historical if deployment occurs later; fresh immediate pre-write service-state guard still required, not another full old scan/C5/three-GET replay. G2 independent original-builder provenance still UNKNOWN. `STEP04=HOLD`, `PRODUCTION=NO_GO`.


## 21 Nov 2026 — conditional B1 approval arrived, execute only this read-only gate NEXT

Owner has now expressly approved **one future B1 only conditional on G4-A PASS and remaining security review**. This is not permission to deploy before the guard is completed or to perform R1/R2. See [exact owner decision](OLDX_STEP04_B1_CONDITIONAL_OWNER_APPROVAL_2026-11-21.md). The single PowerShell block below remains **read-only**; run it once on owner Windows PowerShell when ready, share only sanitized output markers. `G4A_READ_ONLY=NOT_EXECUTED` until actual output; `B1_EXECUTION=BLOCKED_PENDING_RESULTS`. Even a `COMPLETE_WITH_LIMITS` output does not establish inherited-parent IAM or effective other-DB denial. Avoid repeating existing scans/billing/IAM snapshot or C5 separate revision reads.


Date: 21 Nov 2026. Repo: yasminparmar087-ops/oldx-website; authorized branch: security-hardening-review.

**This file is source-only preparation and has NOT been executed.** It authorizes no B1/R1/R2, IAM, billing, Firebase, image, signature or traffic write. Run only from the owner's Windows PowerShell with the existing authenticated `gcloud.cmd` on the desired supervised read-only gate. No Cloud Shell, no key material, no service invocation.

## Why this is genuinely new, not repeated C5
The prior G4 (~17:03) and C5 (~17:24) observations are frozen. This new one-shot combines a **fresh same-window service + direct-service-IAM + project-IAM** read, validates all three **together** against the owner-agreed exact traffic/tags/flags/identity, and emits only sanitized booleans/counts. This detects relevant subsequent drift; it is NOT a proof of folder/org inherited IAM, indirect custom roles, other-database effective denial, or a provider-wide hard cost stop. Repeat only when a specific newly authorized deployment is imminent and the prior snapshot has gone stale; do not keep running it for reassurance.

- Calls (exactly 3 Cloud metadata/policy GETs): `gcloud run services describe oldx-owner-read`, `gcloud run services get-iam-policy oldx-owner-read`, `gcloud projects get-iam-policy oldx-staging`, with explicit region/project/Yasmin account/quiet/JSON; **no writes**.
- Expected unchanged baseline: main root `oldx-owner-read-00001-8kr` = 100%; `healthcheck` → `oldx-owner-read-00002-tid`, `step3rc14` (no hyphen) → `oldx-owner-read-00003-nus`; latestReady `00003-nus`; no fourth entry; project Owners 2, Editors 1, direct project Run Invokers 0, service named Invoker 1, neither direct service nor project bindings have public principals.
- Expected old current *service template* image is `oldx-owner-read-step3-rc@sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc` (NOT proposed npm-free `0844...`), explicit both feature flags `false`, known service runtime identity; Cloud Run IAM check not explicitly disabled. This is not a check of the old root revision's source, and NOT proof of any future new revision.
- If a legitimate owner-approved IAM change, reduction of project Owner count, new revision, new image, or ingress modification has occurred, script **STOPs** rather than quietly accepting an unknown preimage. Reconcile before creating a new execution scope. It is intentionally fail-closed even for safe drift.
- Policy outputs are processed only in PowerShell memory; no policy membership emails, tokens, URLs, other environment values or secret material printed or uploaded. stdout is sanitized. Commands suppress stderr to avoid leaking principal details.
- **Scope limit:** Service/project direct IAM policies do not include all inherited folder/org policy data, group expansion or custom roles. Project Owner/Editor may invoke. This probe is a drift guard, not an effective exclusive-invocation certification. See [G4 boundary](OLDX_STEP04_G4_OFF_ONLY_BOUNDARY_AND_EFFECTIVE_IAM_GATE_2026-11-21.md).

Official command references: [Cloud Run describe](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/describe), [Cloud Run get IAM](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/get-iam-policy), [project IAM](https://docs.cloud.google.com/sdk/gcloud/reference/projects/get-iam-policy), [resource hierarchy inheritance](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control).

## Exact native PowerShell command, owner may run once read-only

Paste **as one block** in a Windows **PowerShell** `PS ...>` prompt, not CMD or WSL. Its internal `& { ... }` block avoids overwriting older `$svc` and `$servicePolicy` snapshots. Do not copy command output showing secrets: only the sanitized marker lines it emits.

```powershell
& {
  function Get-G4Json {
    param([string[]]$CliArgs, [string]$FailureCode)
    $raw = & gcloud.cmd @CliArgs 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) { throw $FailureCode }
    return ($raw | Out-String | ConvertFrom-Json -ErrorAction Stop)
  }
  function Count-G4Role {
    param($Policy, [string]$Role)
    return @($Policy.bindings | Where-Object { $_.role -ceq $Role } |
      ForEach-Object { $_.members } | Where-Object { $_ }).Count
  }
  function Count-G4Public {
    param($Policy)
    return @($Policy.bindings | ForEach-Object { $_.members } |
      Where-Object { $_ -cin @('allUsers','allAuthenticatedUsers') }).Count
  }
  try {
    $project = 'oldx-staging'
    $region = 'asia-south1'
    $service = 'oldx-owner-read'
    $common = @('--project=oldx-staging','--account=yasminparmar087@gmail.com','--format=json','--quiet')
    $g4svc = Get-G4Json -CliArgs (@('run','services','describe',$service,'--region=asia-south1') + $common) -FailureCode 'G4A_SERVICE_READ_FAILED'
    'G4A_SERVICE_GET=PASS'
    $g4iam = Get-G4Json -CliArgs (@('run','services','get-iam-policy',$service,'--region=asia-south1') + $common) -FailureCode 'G4A_SERVICE_IAM_READ_FAILED'
    'G4A_SERVICE_IAM_GET=PASS'
    $g4proj = Get-G4Json -CliArgs (@('projects','get-iam-policy',$project) + $common) -FailureCode 'G4A_PROJECT_IAM_READ_FAILED'
    'G4A_PROJECT_IAM_GET=PASS'

    if ($g4svc.metadata.name -cne $service -or
        $g4svc.status.latestReadyRevisionName -cne 'oldx-owner-read-00003-nus' -or
        $g4svc.spec.template.spec.serviceAccountName -cne 'oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com') {
      throw 'G4A_SERVICE_IDENTITY_DRIFT'
    }
    $a = $g4svc.metadata.annotations
    $ingress = [string]$a.'run.googleapis.com/ingress'
    $iamDisabled = [string]$a.'run.googleapis.com/invoker-iam-disabled'
    if ($ingress -cne 'all' -or $iamDisabled -notin @('','false')) {
      throw 'G4A_INGRESS_OR_IAM_CHECK_DRIFT'
    }
    $container = @($g4svc.spec.template.spec.containers | Where-Object { $null -ne $_ })
    if ($container.Count -ne 1 -or
        [string]$container[0].image -cne 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-owner-read-step3-rc@sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc') {
      throw 'G4A_SERVICE_TEMPLATE_IMAGE_DRIFT'
    }
    foreach ($name in @('OLDX_PRODUCT_READ_ACTIVATE_STAGING','OLDX_PRODUCT_READ_STAGING_ADC')) {
      $flag = @($container[0].env | Where-Object { $null -ne $_ -and $_.name -ceq $name })
      if ($flag.Count -ne 1 -or [string]$flag[0].value -cne 'false' -or $null -ne $flag[0].valueFrom) {
        throw 'G4A_TEMPLATE_FLAG_NOT_EXACT_FALSE'
      }
    }
    $traffic = @($g4svc.status.traffic | Where-Object { $null -ne $_ })
    if ($traffic.Count -ne 3) { throw 'G4A_TRAFFIC_ENTRY_COUNT_DRIFT' }
    $revs = @('oldx-owner-read-00001-8kr','oldx-owner-read-00002-tid','oldx-owner-read-00003-nus')
    foreach ($rev in $revs) {
      if (@($traffic | Where-Object { $_.revisionName -ceq $rev }).Count -ne 1) {
        throw 'G4A_TRAFFIC_REVISION_DRIFT'
      }
    }
    $root = @($traffic | Where-Object { $_.revisionName -ceq $revs[0] })[0]
    $health = @($traffic | Where-Object { $_.revisionName -ceq $revs[1] })[0]
    $step3 = @($traffic | Where-Object { $_.revisionName -ceq $revs[2] })[0]
    if ([string]$root.percent -cne '100' -or $root.tag -or
        $health.tag -cne 'healthcheck' -or $step3.tag -cne 'step3rc14' -or
        [string]$health.percent -notin @('','0') -or [string]$step3.percent -notin @('','0')) {
      throw 'G4A_TRAFFIC_TAG_OR_ROOT_DRIFT'
    }
    $svcPublic = Count-G4Public $g4iam
    $projPublic = Count-G4Public $g4proj
    $serviceInvokers = Count-G4Role $g4iam 'roles/run.invoker'
    $owners = Count-G4Role $g4proj 'roles/owner'
    $editors = Count-G4Role $g4proj 'roles/editor'
    $projectInvokers = Count-G4Role $g4proj 'roles/run.invoker'
    if ($svcPublic -ne 0 -or $projPublic -ne 0) { throw 'G4A_PUBLIC_POLICY_BINDING_FOUND' }
    if ($serviceInvokers -ne 1 -or $owners -ne 2 -or $editors -ne 1 -or $projectInvokers -ne 0) {
      throw 'G4A_IAM_MEMBER_COUNT_DRIFT'
    }
    'G4A_PRIVATE_DIRECT_POLICY_GUARD=MATCH'
    'G4A_TRAFFIC_PREIMAGE=MATCH'
    'G4A_MAIN=oldx-owner-read-00001-8kr:100'
    'G4A_EXISTING_TAGS=healthcheck,step3rc14'
    'G4A_LATEST_TEMPLATE_TWO_ACTIVATION_FLAGS=EXACT_FALSE'
    "G4A_SERVICE_INVOKER_MEMBERS=$serviceInvokers"
    "G4A_PROJECT_OWNER_MEMBERS=$owners EDITOR_MEMBERS=$editors PROJECT_INVOKER_MEMBERS=$projectInvokers"
    'G4A_PARENT_INHERITED_IAM=NOT_VERIFIED'
    'G4A_OTHER_DATABASE_EFFECTIVE_DENIAL=NOT_VERIFIED'
    'G4A_EXCLUSIVE_OWNER_INVOCATION=NOT_PROVEN'
    'G4A_DEPLOYMENT=NOT_STARTED'
    'G4A_READ_ONLY_PREB1=COMPLETE_WITH_LIMITS'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^G4A_[A-Z0-9_]+$') { $reason = 'G4A_UNEXPECTED_FAILURE' }
    'STOP_G4A_READ_ONLY_PREFLIGHT'
    "REASON=$reason"
    'G4A_DEPLOYMENT=NOT_STARTED'
  }
}
```

## Outcomes / STOP

- The success marker `G4A_READ_ONLY_PREB1=COMPLETE_WITH_LIMITS` means **only direct service/project policy drift and exact currently visible service/traffic preimage match**. It does not authorize B1 or establish G4-B cross-database security.
- Any `STOP_G4A_READ_ONLY_PREFLIGHT` is a fail-closed stop, **not a request to rerun**. Record which preceding `G4A_*_GET=PASS` lines were shown; diagnose only that new issue, and do not automatically retry.
- Once this succeeds, preserve that single screenshot as evidence in GitHub handoff *without raw IAM members*. Do not rerun C1/C2/C3/C4/old C5 or old G4/G8 snapshots.
- A **fresh immediate pre-mutation preimage** and separate owner-specific B1/R1/R2 execution approvals remain required; this read may be stale when B1 eventually happens.
- C4 six-CVE OFF-only risk accepted with limits; G8 OFF-only side-provider cost accepted with limits; G2 trust/builder provenance and G4 effective inherited/other-DB boundaries remain open. Step04 HOLD, production NO-GO.
