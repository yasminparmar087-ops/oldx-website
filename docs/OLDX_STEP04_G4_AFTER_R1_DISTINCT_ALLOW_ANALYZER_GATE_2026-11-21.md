# OLDX Step04 — Post-R1 G4 distinct IAM allow-analysis gate (source-only)

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

```powershell
& {
  try {
    $argsList = @(
      'asset','analyze-iam-policy',
      '--project=oldx-staging',
      '--identity=serviceAccount:oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com',
      '--permissions=datastore.entities.get,datastore.entities.create,datastore.entities.update,datastore.entities.delete',
      '--expand-roles','--show-response','--format=json',
      '--account=yasminparmar087@gmail.com','--quiet'
    )
    $raw = & gcloud.cmd @argsList 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) {
      throw 'ALLOW_ANALYZER_UNAVAILABLE_OR_DENIED'
    }
    $r = $raw | Out-String | ConvertFrom-Json -ErrorAction Stop
    if ($null -eq $r.fullyExplored) { throw 'ALLOW_ANALYZER_OUTPUT_SHAPE_UNKNOWN' }
    $items = @($r.analysisResults | Where-Object { $null -ne $_ })
    $incomplete = @($items | Where-Object { $_.fullyExplored -ne $true }).Count
    $errors = @($r.nonCriticalErrors | Where-Object { $null -ne $_ }).Count
    "G4_ALLOW_ANALYZER_RESULT_COUNT=$($items.Count)"
    "G4_ALLOW_ANALYZER_UNCONDITIONAL_MATCHES=$(@($items | Where-Object { -not $_.iamBinding.condition }).Count)"
    "G4_ALLOW_ANALYZER_CONDITIONAL_MATCHES=$(@($items | Where-Object { $_.iamBinding.condition }).Count)"
    if ($r.fullyExplored -eq $true -and $incomplete -eq 0 -and $errors -eq 0) {
      'G4_ALLOW_ANALYZER=ALLOW_ONLY_QUERY_COMPLETE'
    } else {
      'G4_ALLOW_ANALYZER=INCOMPLETE_NOT_A_PASS'
    }
    'G4_CROSS_DATABASE_NEGATIVE_DENIAL=UNVERIFIED'
    'G4_IAM_DENY_AND_PAB_EFFECTIVE=UNVERIFIED'
    'G4_PROVIDER_WRITES=NONE'
  } catch {
    'STOP_G4_ALLOW_ANALYZER_NO_RETRY'
    'G4_ALLOW_ANALYZER=NOT_VERIFIED'
    'G4_PROVIDER_WRITES=NONE'
  }
}
```

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
