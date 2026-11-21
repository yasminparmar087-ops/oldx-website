# OLDX Step04 — Post-R1 G4 distinct IAM allow-analysis gate (source-only)

## 21 Nov 2026 ~19:03 IST — corrected allow-policy query PASS WITH LIMITS (NEW LATEST)

**Owner-observed actual Windows PowerShell screenshot** from exactly one execution of the corrected nested-`mainAnalysis` parser in the immediately preceding section: terminal prompt returned, no STOP; visible output:

```text
G4_CORRECTED_SCHEMA=mainAnalysis.analysisResults
G4_ALLOW_ACTUAL_RESULT_COUNT=1
G4_ALLOW_UNCONDITIONAL=0
G4_ALLOW_EXACT_DEFAULT_DB_CONDITION=1
G4_ALLOW_OTHER_CONDITION=0
G4_ALLOW_RESULT=ALLOW_ONLY_ANALYSIS_WITH_LIMITS
G4_OTHER_DB_EFFECTIVE_DENY=UNVERIFIED
G4_DENY_AND_PAB_EFFECTIVE=UNVERIFIED
G4_CLOUD_WRITES=NONE
```

The corrected script would reach the last five lines only after checking `$r.mainAnalysis`, exact echo of the **project scope** and **runtime service account identity**, the four Firestore entity permissions GET/CREATE/UPDATE/DELETE, outer and nested `fullyExplored=true`, no nested noncritical errors, and each result's binding shape. These guards are **inferred from the successful control flow**, not separately printed fields. Therefore this is one valid scoped **Cloud Asset IAM allow-policy** snapshot for `serviceAccount:oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com` at project `oldx-staging`: exactly **one matching allow binding** and its **exact condition** `resource.name == "projects/oldx-staging/databases/(default)"`; zero unconditioned or other-conditioned *matches for this query*. This improves static allow-policy inventory substantially. The first 18:59 script's printed zero counts were an invalid parser artifact; **superseded, not to be reused as evidence**.

**What it does NOT establish:** All possible IAM permissions beyond these four, group/impersonation expansion (not requested), deny or Principal Access Boundary evaluation, IAM direct/exclusive Cloud Run invocation, the effective denial of a hypothetical second Firestore database, or any actual hosted Product API safety. The one-doc positive operations/DELETE403 observed previously on `(default)` remain separate consumed data-plane evidence. Do not infer cross-DB denial from the presence of a conditional allow binding alone. No second Firestore DB creation, extra policy analyzer request, Policy Troubleshooter retries, IAM edits, token minting or enabled Product request is needed/authorized merely for this checkpoint.

**Disposition:** `G4_ALLOW_POLICY_SELECTED_PRINCIPAL_FOUR_ENTITY_PERMISSIONS=COMPLETE_WITH_LIMITS`; `G4_ALLOW_MATCHES=1_EXACT_DEFAULT_DB_CONDITION`; `G4_UNCONDITIONAL_MATCHES=0_IN_QUERY_SCOPE`; `G4_EFFECTIVE_OTHER_DATABASE_DENIAL=UNVERIFIED`; `G4_EXCLUSIVE_CLOUD_RUN_INVOKER=NOT_PROVEN`; `G4_ENABLED_PRODUCT_API=NO_GO`; `G4_ANALYZER_REQUERY=DO_NOT_REPEAT`. Previous one-shot B1 private OFF-only deploy / 3 metadata GETs / R1 tag-only rollback are DONE, not repeatable by default. Original 100%-main stays `oldx-owner-read-00001-8kr`, historical old tags preserved; R2 no-op. Owner's security/cost residual-risk acceptance was only for the **finished** OFF-only B1 trial and must not silently apply to a future enabled rollout.

**Next Step04 decision:** Stop G4 allow-only evidence accumulation here. Reuse this result when designing a distinct *enabled* G4-B release gate; if there is no approved second database/resource on which to run a genuine negative test, retain `OTHER_DB_DENY=UNVERIFIED` rather than manufacture one. Move to outstanding independent G2 original-builder provenance and the six frozen severe CVE findings (1 CRITICAL, 5 HIGH) via already saved C4 evidence/monitoring; do NOT repeat builds, registry uploads, signing, Grype scans or C1–C5. Step04 **HOLD**, production **NO-GO**.

Provider references (for the precise limited interpretation): https://docs.cloud.google.com/asset-inventory/docs/reference/rest/v1/TopLevel/analyzeIamPolicy ; https://docs.cloud.google.com/policy-intelligence/docs/policy-analyzer-overview ; https://docs.cloud.google.com/iam/docs/policy-types .

---

## 21 Nov 2026 ~18:59 IST — FIRST ANALYZER QUERY RAN, BUT OUTPUT PARSER IS WRONG (NEW LATEST)

Owner's actual Windows PowerShell screenshot (not merely pasted code) shows `G4_ALLOW_ANALYZER_RESULT_COUNT=0`, `G4_ALLOW_ANALYZER_UNCONDITIONAL_MATCHES=0`, `G4_ALLOW_ANALYZER_CONDITIONAL_MATCHES=0`, `G4_ALLOW_ANALYZER=ALLOW_ONLY_QUERY_COMPLETE`, `G4_CROSS_DATABASE_NEGATIVE_DENIAL=UNVERIFIED`, `G4_IAM_DENY_AND_PAB_EFFECTIVE=UNVERIFIED`, `G4_PROVIDER_WRITES=NONE`, normal prompt, no STOP. The Cloud Asset request evidently returned with CLI exit zero and outer `fullyExplored` true. **However the results counts are INVALID** due to our PowerShell parser bug: it read `$r.analysisResults` and `$r.nonCriticalErrors` at the **wrong top-level fields**. Google's official `AnalyzeIamPolicyResponse` schema uses **`$r.mainAnalysis.analysisResults`**, **`$r.mainAnalysis.nonCriticalErrors`** and **`$r.mainAnalysis.fullyExplored`**. See https://docs.cloud.google.com/asset-inventory/docs/reference/rest/v1/TopLevel/analyzeIamPolicy#response-body. Thus 0 was an artifact of PowerShell's null-as-empty behavior, not verified absence of IAM grants. Previous actual one-doc positive access makes a security claim from these zeros particularly unsafe. Outer `fullyExplored` alone does NOT validate the nested analysis.

**Corrected state:** `G4_ANALYZER_FIRST_REQUEST=SUCCESSFUL_RETURN_SCHEMA_MISPARSED`; `G4_ACTUAL_RESULT_COUNT=UNKNOWN`; `G4_ALLOW_MATCHES=UNKNOWN`; `G4_ALLOW_ANALYZER_PASS=NOT_ESTABLISHED`; no Cloud/Firestore/IAM writes. The original PowerShell block ran in a child scope (`& { ... }`) and did not save raw JSON, so there is no retained raw response in the supplied screenshot to reparse locally. **One correctly parsed duplicate of THIS OTHERWISE INCOMPLETE READ-ONLY QUERY is justified solely to repair the parser defect**. It is *not* a rerun of any completed C1–C5/G4A/B1/R1/Firestore tests or scans. Do not execute the old buggy block again, do not expand IAM privileges or enable services, no extra query retries if corrected one fails.

### One corrected owner-run READ-ONLY query — prepared, NOT EXECUTED

The corrected command below reads `mainAnalysis`, verifies project+principal+four permissions echoed by `analysisQuery`, requires both nested and outer `fullyExplored`, and checks nested errors. Only prints counts of unconditional, exact-default-db and other conditional bindings; no member, role, condition text, token or request URL is printed. **Counts are allow-policy observations, NOT effective Firestore isolation, IAM deny or PAB proof.** Even a true zero match needs reconciliation with previous positive runtime proof.

```powershell
& {
  try {
    $identity = 'serviceAccount:oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com'
    $perms = @('datastore.entities.get','datastore.entities.create',
               'datastore.entities.update','datastore.entities.delete')
    $argsList = @(
      'asset','analyze-iam-policy','--project=oldx-staging',
      "--identity=$identity",
      ('--permissions=' + ($perms -join ',')),
      '--expand-roles','--show-response','--format=json',
      '--account=yasminparmar087@gmail.com','--quiet'
    )
    $raw = & gcloud.cmd @argsList 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) { throw 'QUERY_FAILED' }
    $r = $raw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $main = $r.mainAnalysis
    if ($null -eq $main -or $null -eq $main.analysisQuery) {
      throw 'MISSING_MAIN_ANALYSIS'
    }
    if ($r.fullyExplored -ne $true -or $main.fullyExplored -ne $true) {
      throw 'INCOMPLETE_ANALYSIS'
    }
    $q = $main.analysisQuery
    if ([string]$q.scope -cnotin @('projects/oldx-staging',
                                   'projects/38472235077') -or
        [string]$q.identitySelector.identity -cne $identity) {
      throw 'QUERY_SCOPE_MISMATCH'
    }
    $expected = ($perms | Sort-Object -CaseSensitive) -join '|'
    $actual = (@($q.accessSelector.permissions |
      Where-Object { $_ } | Sort-Object -CaseSensitive) -join '|')
    if ($actual -cne $expected) { throw 'QUERY_PERMISSIONS_MISMATCH' }
    $items = @($main.analysisResults | Where-Object { $null -ne $_ })
    $partial = @($items | Where-Object { $_.fullyExplored -ne $true }).Count
    $errors = @($main.nonCriticalErrors | Where-Object { $null -ne $_ }).Count
    if ($partial -ne 0 -or $errors -ne 0) { throw 'PARTIAL_RESULT' }
    $unconditional = 0
    $exact = 0
    $otherConditional = 0
    foreach ($item in $items) {
      if ($null -eq $item.iamBinding) { throw 'BINDING_SHAPE_UNKNOWN' }
      $expr = [string]$item.iamBinding.condition.expression
      if ([string]::IsNullOrWhiteSpace($expr)) {
        $unconditional++
      } elseif ($expr -ceq 'resource.name == "projects/oldx-staging/databases/(default)"') {
        $exact++
      } else {
        $otherConditional++
      }
    }
    'G4_CORRECTED_SCHEMA=mainAnalysis.analysisResults'
    "G4_ALLOW_ACTUAL_RESULT_COUNT=$($items.Count)"
    "G4_ALLOW_UNCONDITIONAL=$unconditional"
    "G4_ALLOW_EXACT_DEFAULT_DB_CONDITION=$exact"
    "G4_ALLOW_OTHER_CONDITION=$otherConditional"
    if ($items.Count -eq 0) {
      'G4_ALLOW_RESULT=ZERO_MATCHES_NEEDS_RECONCILIATION'
    } else {
      'G4_ALLOW_RESULT=ALLOW_ONLY_ANALYSIS_WITH_LIMITS'
    }
    'G4_OTHER_DB_EFFECTIVE_DENY=UNVERIFIED'
    'G4_DENY_AND_PAB_EFFECTIVE=UNVERIFIED'
    'G4_CLOUD_WRITES=NONE'
  } catch {
    'STOP_G4_CORRECTED_QUERY_NO_AUTOMATIC_RETRY'
    'G4_ALLOW_RESULT=UNVERIFIED'
    'G4_CLOUD_WRITES=NONE'
  }
}
```

**STOP means no automatic rerun.** If `G4_ALLOW_RESULT=ALLOW_ONLY_ANALYSIS_WITH_LIMITS`, discuss exact conditional/unconditional categories before any new action; a returned `0` is `ZERO_MATCHES_NEEDS_RECONCILIATION`, not denial. After capturing one sanitized result, stop the analyzer phase and move to the remaining independent G4 effective isolation or G2 security/provenance issues without repeating successful old work.

---

Date: 21 Nov 2026, after owner screenshot verified R1 tag-only removal. Repository `yasminparmar087-ops/oldx-website`; branch `security-hardening-review`.

## Continuity / consumed work

- [R1 canonical receipt](OLDX_STEP04_R1_TAG_ONLY_COMPLETE_2026-11-21.md): `R1_TAG_ONLY_REMOVAL=COMPLETE_WITH_LIMITS`, original `oldx-owner-read-00001-8kr` 100% main and original `healthcheck`/`step3rc14` tags preserved. No new tagged URL request or enabled Product API.
- Earlier B1 created private default-OFF/503 candidate `00010-zud`, 0% main, source pinned. Target `ownerreadv2` tag has now been removed. **Do not redeploy, re-tag or repeat B1/R1.**
- G4 positive one-doc runtime service identity CREATE/GET/UPDATE plus negative DELETE 403 and operator cleanup on **`oldx-staging/(default)`** already completed. Previous project/service IAM preimage and no-parent metadata were already read. Do not redo them.
- Five past database Policy Troubleshooter attempts were HTTP400 / unknown, and earlier evidence says `policytroubleshooter.googleapis.com` was not enabled. Do **not** retry failed tuples or enable it. The Cloud Asset API `cloudasset.googleapis.com` availability in this project is **UNKNOWN**, not inferred from Troubleshooter's separate status.
- One observed direct service-level `roles/run.invoker` grant plus project 2 Owners and 1 Editor show that **effective invoker exclusivity is not proven**. Do not silently remove another owner's roles, grant permissions, make IAM edits, or claim exclusive access.
- Original existing condition `resource.name == "projects/oldx-staging/databases/(default)"` is syntactically aligned with Google's per-database conditional binding guidance, but not a proof all applicable bindings have this condition or that effective access to a different database is denied. Firestore client Rules do not replace Admin SDK IAM.

## New distinct option: one bounded Cloud Asset IAM allow-policy analysis

A different query than the old project IAM snapshot or failed Policy Troubleshooter: **one** read-only `gcloud asset analyze-iam-policy` request for the **runtime service account** and the exact Firestore entity GET/CREATE/UPDATE/DELETE permissions at project scope. Google's Cloud Asset Inventory docs describe this as analyzing IAM allow policies; it can list conditional and unconditional binding matches and account for relevant inherited allow policy scope, subject to query completeness/permissions and data freshness. It **does not** evaluate IAM deny / Principal Access Boundary policies, does **not** prove effective access to a nonexistent other database, and cannot be substituted for a separately approved real negative isolation acceptance. The existing `NO_PARENT_REPORTED` observation narrows hierarchy questions but isn't an IAM PASS.

**Cost/permissions:** Google's Cloud Asset Inventory pricing states service usage is free (no Cloud Storage/BigQuery export in this query); Policy Analyzer requests consume query quota. IAM requires `cloudasset.assets.analyzeIamPolicy`, `cloudasset.assets.searchAllResources`, `cloudasset.assets.searchAllIamPolicies`, and for custom role analysis `iam.roles.get`; CLI may require `serviceusage.services.use`. Do not add a role or enable an API to force a result. If service disabled, access denied, incomplete or ambiguous: STOP and record **UNKNOWN**, not PASS.

### ONE optional owner-supervised Windows PowerShell query — PREPARED, NOT EXECUTED

This new query is read-only, no stored token and no printed identity/member/condition text. Exactly one `gcloud.cmd asset analyze-iam-policy` request if run. `--show-response` ensures a structured API result; output prints only counts and completeness, not policies. The query intentionally does not expand groups or impersonation and therefore cannot establish exhaustive effective authority.

**DEPRECATED — DO NOT RUN:** The former script used wrong top-level result fields; it is superseded by the corrected one above.

Run only once, and do not retry if it reports STOP, error or incomplete. A result with `UNCONDITIONAL_MATCHES > 0` is a **review trigger** and not automatically an exploitable broad grant. Zero matches is not proof of denial, especially without group/impersonation expansion and effective condition context. The presence of `DELETE` permission in a matched IAM role must be reconciled against previous 403 from the *actual* runtime principal and binding condition; no new DELETE operation.

## Next decision after that single distinct query

- If a query is successful, interpret ONLY what the sanitized allow matches support and identify whether broader/unconditional grants need a separate expert/owner review.
- If blocked by API/permission, **do not enable** any API or grant a wider role; label static allow inventory unresolved and keep G4 HOLD.
- If source evidence alone cannot show an additional IAM/security problem, proceed to other independent Step04 G2 trust and CVE tasks; don't manufacture a second database, repeat old checks, or make the user run redundant commands.
- Enabled Product API remains **NO-GO** until separately authorized and independently supported effective IAM/other-database access controls; no image/traffic/Rules/IAM/Firebase changes under this packet.

## Official references

- https://firebase.google.com/docs/firestore/manage-databases (conditional per-database IAM and console warning)
- https://docs.cloud.google.com/sdk/gcloud/reference/asset/analyze-iam-policy (exact CLI flags, read-only query)
- https://docs.cloud.google.com/policy-intelligence/docs/policy-analyzer-overview (allow-only, limitations, freshness)
- https://docs.cloud.google.com/policy-intelligence/docs/analyze-iam-policies (required permissions and results)
- https://cloud.google.com/asset-inventory/pricing (free service, other storage costs only)
- https://docs.cloud.google.com/asset-inventory/docs/quota (query quota)

Current ledger: `R1=DONE`; `G4_ALLOW_ANALYZER=PREPARED_NOT_RUN`; `G4_EFFECTIVE_OTHER_DB_DENY=UNVERIFIED`; `G4_EFFECTIVE_EXCLUSIVE_INVOKER=UNVERIFIED`; `G2_INDEPENDENT_BUILDER_PROVENANCE=UNKNOWN`; `STEP04=HOLD`; `PRODUCTION=NO_GO`.
