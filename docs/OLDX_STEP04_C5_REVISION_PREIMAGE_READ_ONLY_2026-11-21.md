# OLDX Step 04 — C5 revision preimage / rollback-safe READ-ONLY gate (21 Nov 2026)

## 21 Nov 2026 ~17:12 IST — C5 revision preimage guard STOP before any revision GET; mismatch is local-check result, NOT proven live drift (LATEST)

**Actual owner's native PowerShell screenshot:** After pasting the planned C5 first-read script in the same `PS C:\Users\Yasmin Parmar>` shell, the only **result** lines were:
```text
STOP_C5_REVISION_PREIMAGE
REASON=C5_TRAFFIC_PREIMAGE_CHANGED
```
The script first checked `$svc.metadata.name`, expected three `$svc.status.traffic` entries, latest Ready `00003-nus`, and one entry per `00001-8kr`, `00002-tid`, `00003-nus`. It then evaluates **four local comparisons** `[string]$main.percent -ne '100'`, truthy `$main.tag`, `$health.tag -ne 'healthcheck'`, `$step3.tag -ne 'step3-rc14'` and threw before printing `C5_PREVIOUS_TRAFFIC_PREIMAGE=MATCH`. Crucially the `gcloud run revisions describe` loop is *after* this throw: **NONE of the planned three new revision GETs were issued**, nor any Cloud Run/IAM/Billing write. Do **NOT** infer actual live traffic drift from the guard label; the comparison was made against already fetched in-memory ~17:03 snapshot. The four individual comparison outcomes have **not** been observed. Previous old service/IAM/Billing read-only snapshot remains valid for its observation time; C1/C2/C3/C4 results remain frozen.

**Recovery recommended NEXT — owner read-only local PowerShell only; NOT YET RUN:** Inspect the already-loaded `$svc.status.traffic` in memory without any `gcloud` call, log/output **only booleans** for the 4 guard predicates and presence/count of exactly expected 3 revisions (no URLs, principal names, auth tokens or environment values). Do not print raw labels/secret fields. If variable missing, STOP and explicitly decide whether a separate live refresh needs consent; no blind replay of the previous three-revision script. After exact mismatch isolated, adjust the **comparison/check logic** in source-only docs if needed, never silently bypass drift safeguards. Before any C5 rollout, still require **fresh current preimage**, exact authorized B1, rollback R1/R2 preserving 100% `00001-8kr` and tags, C4 owner risk disposition, G4 effective limitations and G8 side-provider cost acceptance.

**State:** `C5_PREIMAGE_ATTEMPT=LOCAL_GUARD_STOP`, `C5_REVISION_GETS=ZERO`, `C5_PREIMAGE_READ_ONLY_COMPLETE=NO`, `C5_DEPLOYMENT=NOT_STARTED`; C3 local Sigstore signature PASS; C4 1C/5H acceptance OPEN; G2 HOLD, G4 cross-DB OPEN, G8 all-provider STOP OPEN; Step04 HOLD, production NO-GO. **Do not simply re-run the failing command.**

**Prepared source-only, NOT executed. Owner's current follow-up "ok aagal vadho" applies to continuing without redoing completed checks, not approval to deploy or mutate project resources.** All work on `security-hardening-review`. Do not run the old consumed C1 upload, Grype, C3 signing or C4 one-shot again.

## Reason for one targeted revision read

Latest actual owner screenshot ~17:03/17:07 IST established project `oldx-staging`, Cloud Run service `oldx-owner-read`, region `asia-south1`, 3 traffic records, **main 100% on `oldx-owner-read-00001-8kr`**; `oldx-owner-read-00002-tid` tagged `healthcheck`; `oldx-owner-read-00003-nus` tagged `step3-rc14` and latest Ready. The latest **service template** image is old Step3 RC digest `sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc` — NOT the prospective private npm-free `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`. Latest Ready revision is **not** the 100% traffic revision. No cloud mutation occurred, but exact old revision image/env, resources and rollback preimage are still unverified. In-memory `$svc` and `$servicePolicy` resulted from the approved read-only snapshot. Use `$svc` only for the frozen expected preimage, not a claim of current state at some later time.

Current latest service template has `OLDX_PRODUCT_READ_ACTIVATE_STAGING=false` and `OLDX_PRODUCT_READ_STAGING_ADC=false` exactly, no explicit IAM-check disable flag, minScale annotations NOT_SET, maxScale 1. These settings were **not** verified on 100%-traffic and both older tagged revisions. Zero public service IAM members but one named Invoker, two project Owners and one project Editor -> nonexclusive potential invokers; `INGRESS=all`. No all-provider G8 hard spend stop; Cloud Run-only ₹100 spend-cap separate historic evidence. No hosted C5 approval.

Official Google docs: [View revision details](https://docs.cloud.google.com/run/docs/managing/revisions), [gcloud run revisions describe](https://docs.cloud.google.com/sdk/gcloud/reference/run/revisions/describe), [tagged revisions and rollbacks](https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration). **Do not use `update-traffic` in this step.**

## One targeted read-only command, NEXT owner action, NOT YET EXECUTED

Paste only in **same existing** `PS ...>` PowerShell shell that holds `$svc` (not CMD). It uses exactly 3 new **`gcloud run revisions describe` READ** calls, no service/IAM/Billing rereads and no disk evidence uploads. All returned JSON is parsed **in memory**; only limited metadata and *booleans* for exact expected env names are printed. No secret env values, principal names, tokens, URLs or raw policy are echoed. If the old `$svc` variable is missing, STOP without network request. Do not run again after a STOP without diagnosing the reason.

```powershell
try {
    if ($null -eq $svc -or $svc.metadata.name -ne 'oldx-owner-read') {
        throw 'C5_PRIOR_SERVICE_SNAPSHOT_MISSING'
    }
    $expected = @(
        'oldx-owner-read-00001-8kr',
        'oldx-owner-read-00002-tid',
        'oldx-owner-read-00003-nus'
    )
    $t = @($svc.status.traffic | Where-Object { $null -ne $_ })
    if ($t.Count -ne 3 -or $svc.status.latestReadyRevisionName -ne $expected[2]) {
        throw 'C5_PREIMAGE_UNEXPECTED'
    }
    foreach ($n in $expected) {
        if (@($t | Where-Object { $_.revisionName -eq $n }).Count -ne 1) {
            throw 'C5_TRAFFIC_REVISION_MISMATCH'
        }
    }
    $main = @($t | Where-Object { $_.revisionName -eq $expected[0] })[0]
    $health = @($t | Where-Object { $_.revisionName -eq $expected[1] })[0]
    $step3 = @($t | Where-Object { $_.revisionName -eq $expected[2] })[0]
    if ([string]$main.percent -ne '100' -or $main.tag -or
        $health.tag -ne 'healthcheck' -or $step3.tag -ne 'step3-rc14') {
        throw 'C5_TRAFFIC_PREIMAGE_CHANGED'
    }
    'C5_PREVIOUS_TRAFFIC_PREIMAGE=MATCH'
    'C5_MAIN_TRAFFIC_REVISION=oldx-owner-read-00001-8kr'
    'C5_MAIN_TRAFFIC_PERCENT=100'
    'C5_EXISTING_TAGS=healthcheck,step3-rc14'

    foreach ($n in $expected) {
        $raw = & gcloud.cmd run revisions describe $n '--project=oldx-staging' '--region=asia-south1' '--account=yasminparmar087@gmail.com' '--format=json' '--quiet' 2>$null
        if ($LASTEXITCODE -ne 0 -or -not $raw) { throw 'C5_REVISION_READ_FAILED' }
        $rev = $raw | Out-String | ConvertFrom-Json -ErrorAction Stop
        if ($rev.metadata.name -ne $n -or @($rev.spec.containers).Count -ne 1) {
            throw 'C5_REVISION_ID_OR_CONTAINER_SHAPE_STOP'
        }
        $container = @($rev.spec.containers)[0]
        $img = [string]$container.image
        if ($img -match '@(sha256:[0-9a-f]{64})$') {
            $imageDigest = $Matches[1]
        } else {
            $imageDigest = 'NOT_PINNED_REVIEW'
        }
        $a = $rev.metadata.annotations
        $min = [string]$a.'autoscaling.knative.dev/minScale'
        $max = [string]$a.'autoscaling.knative.dev/maxScale'
        if (-not $min) { $min = 'NOT_SET' }
        if (-not $max) { $max = 'NOT_SET' }
        $cpu = [string]$container.resources.limits.cpu
        $mem = [string]$container.resources.limits.memory
        if (-not $cpu) { $cpu = 'NOT_SET' }
        if (-not $mem) { $mem = 'NOT_SET' }
        $con = [string]$rev.spec.containerConcurrency
        $timeout = [string]$rev.spec.timeoutSeconds
        if (-not $con) { $con = 'NOT_SET' }
        if (-not $timeout) { $timeout = 'NOT_SET' }
        "C5_REVISION=$n"
        "C5_IMAGE_DIGEST=$imageDigest"
        "C5_CPU=$cpu MEMORY=$mem CONCURRENCY=$con TIMEOUT_SECONDS=$timeout"
        "C5_REVISION_MIN=$min MAX=$max"
        foreach ($flag in @('OLDX_PRODUCT_READ_ACTIVATE_STAGING','OLDX_PRODUCT_READ_STAGING_ADC')) {
            $v = @($container.env | Where-Object { $null -ne $_ -and $_.name -eq $flag })
            if ($v.Count -eq 0) { $state = 'MISSING' }
            elseif ($v.Count -eq 1 -and $null -eq $v[0].valueFrom -and
                    [string]$v[0].value -ceq 'false') { $state = 'EXACT_FALSE' }
            else { $state = 'NOT_FALSE_OR_SECRET_REF_REVIEW' }
            "C5_ENV_$flag=$state"
        }
    }
    'C5_REVISION_PREIMAGE_READ_ONLY=COMPLETE'
    'C5_ROLLBACK=PLAN_ONLY'
    'C5_DEPLOYMENT=NOT_STARTED'
} catch {
    'STOP_C5_REVISION_PREIMAGE'
    "REASON=$($_.Exception.Message)"
}
```

## Read-only evidence interpretation and STOP gates

- This output is **three specific revision snapshots at read time**, not an automatic lock against future drift. If any STOP, do not rerun the whole command, do not enable API/change IAM, do not deploy; reconcile reported issue first.
- It shows exact ready revision's resource info and which existing digest is on each revision. Only flags `false` or `MISSING` can be considered *not activated by that named key*; **missing is not a global proof of default OFF** and no unprinted env or code path is inspected. Even a 0%-main tagged revision can receive requests at its tag URL.
- Do not log/save full response JSON, env vars/values, service account principal roster or billing account data to public GitHub.
- After output, prepare **R1 remove only proposed new `ownerreadv2` tag** and **R2 preserve/restore original `00001-8kr=100%` plus both existing tags** (under separate explicit owner cloud-write approval), not `--to-latest`. Do not execute rollback now or assume `--to-revisions` by itself preserves tags.
- Require new C5 B1 live deploy decision detailing no real customer data, explicit owner acceptance of remaining C4 1 CRITICAL/5 HIGH, effective IAM nonexclusivity and G8 uncapped side-service expense, min0/max1/duration/rollback guard. **No live B1 until those gates**; G2 HOLD, G4 effective other-DB OPEN, G8 all-provider hard spend stop OPEN, Step04 HOLD, production NO-GO.

## Checkpoint states

```text
C1_C2=FROZEN_WITH_SCOPED_PASS
C3_LOCAL_KEYLESS_DSSE=CRYPTOGRAPHICALLY_VERIFIED
C4_SIX_SEVERE_CVE_REVIEW=CONDITIONAL_PENDING_OWNER_ACCEPTANCE
G4_SERVICE_CURRENT_SNAPSHOT_AND_IN_MEMORY_REVIEW=COMPLETE
G4_EFFECTIVE_OTHER_DB_DENIAL=OPEN
G8_PROVIDER_WIDE_FINANCIAL_HARD_STOP=OPEN
C5_REVISION_PREIMAGE_READ_ONLY=PREPARED_NOT_RUN
C5_DEPLOYMENT=NOT_STARTED
STEP04=HOLD
PRODUCTION=NO_GO
```
