# OLDX Step04 G2 A7 S2 — repository-only Artifact Registry Writer (owner approved, PREPARED NOT EXECUTED)

Date 21 Nov 2026, after exact S1 identity confirmation at ~20:07 IST. Source branch: `security-hardening-review`, project `oldx-staging`.

## Live evidence consumed and boundary

- S1 first creation block stopped with `A7_S1_UNEXPECTED_ERROR` and the create outcome was ambiguous. The owner's **subsequent separate one-time read-only describe** positively established `G2_A7_S1_ACCOUNT=EXISTS_VERIFIED_AFTER_STOP`, `G2_A7_S1_CREATE_RETRY=PROHIBITED`, `G2_A7_S2_IAM_WRITES=NOT_STARTED`, no STOP. [S1 receipt](OLDX_STEP04_G2_A7_OWNER_APPROVED_S1_ACCOUNT_CREATE_2026-11-21.md). Identity checked exact email, uniqueId nonempty, not disabled; who/when created unknown. **Never recreate or replay S1**.
- Owner's earlier A7 explicit approval remains in scope: one `oldx-step04-build@oldx-staging.iam.gserviceaccount.com` SA without keys, `roles/artifactregistry.writer` **only on** existing repository `oldx-staging/asia-south1/oldx-staging-images`, `roles/logging.logWriter` staging project, `roles/iam.serviceAccountUser` owner Yasmin on new builder SA only. Nothing else. **No build or deploy**.
- S2 is one isolated authorized write gate for **only** `roles/artifactregistry.writer` as `serviceAccount:oldx-step04-build@oldx-staging.iam.gserviceaccount.com` on Artifact Registry **repository**, not project/organization.
- This is an IAM policy mutation granting future upload capability; account existence does not itself grant uploading. This script cannot guarantee no concurrent external policy change between its read and write, but the supported Google `add-iam-policy-binding` command uses IAM policy read/modify/write and this packet verifies exact policy delta after. If concurrency or unexpected conditions cause a different delta, STOP and reconcile; never automatically revoke/retry.
- Do not expose full pre/post policy, members, tokens, keys or etag in output. Previous historical repo-level `bindings` was null; **do not assume it's still null**—fresh preimage read is essential before granting the role.
- S3 and S4 are already approved but **not executed**; do not run them until S2 is positively verified.

## Exact one-shot Windows PowerShell block — PREPARED NOT RUN

```powershell
& {
  try {
    $repo = 'oldx-staging-images'
    $member = 'serviceAccount:oldx-step04-build@oldx-staging.iam.gserviceaccount.com'
    $role = 'roles/artifactregistry.writer'
    $argsCommon = @(
      '--project=oldx-staging',
      '--account=yasminparmar087@gmail.com',
      '--location=asia-south1',
      '--format=json',
      '--quiet'
    )

    function Get-Tuples($policy) {
      foreach ($b in @($policy.bindings | Where-Object { $null -ne $_ })) {
        if (-not $b.role) { throw 'S2_POLICY_ROLE_MISSING' }
        $cond = if ($null -ne $b.condition) {
          ConvertTo-Json -InputObject $b.condition -Compress -Depth 8
        } else { '' }
        foreach ($m in @($b.members | Where-Object { $null -ne $_ })) {
          "$([string]$b.role)|$cond|$([string]$m)"
        }
      }
    }

    $readArgs = @('artifacts','repositories','get-iam-policy',$repo) + $argsCommon
    $preRaw = & gcloud.cmd @readArgs 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $preRaw) {
      throw 'S2_REPO_PRE_READ_FAILED'
    }
    $pre = $preRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $match = @(@($pre.bindings | Where-Object { $null -ne $_ }) |
      Where-Object {
        $_.role -ceq $role -and @($_.members) -ccontains $member
      })
    if (@($match | Where-Object { $null -ne $_.condition }).Count -gt 0) {
      throw 'S2_TARGET_CONDITIONAL_BINDING_REVIEW'
    }
    if ($match.Count -gt 1) {
      throw 'S2_DUPLICATE_TARGET_BINDING'
    }
    if ($match.Count -eq 1) {
      'G2_A7_S2_WRITER=ALREADY_DIRECT_UNCONDITIONAL_NO_WRITE'
      'G2_A7_S2_OTHER_IAM_WRITES=NONE'
      return
    }

    $before = @(Get-Tuples $pre | Sort-Object)
    'G2_A7_S2_PREIMAGE=TARGET_REPO_WRITER_ABSENT'
    $writeArgs = @('artifacts','repositories','add-iam-policy-binding',$repo,
      "--member=$member","--role=$role",'--condition=None') + $argsCommon
    $writeRaw = & gcloud.cmd @writeArgs 2>$null
    if ($LASTEXITCODE -ne 0) {
      throw 'S2_WRITE_OUTCOME_UNCERTAIN'
    }
    'G2_A7_S2_WRITE_CLI=EXIT_ZERO'

    $postRaw = & gcloud.cmd @readArgs 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $postRaw) {
      throw 'S2_POST_READ_FAILED'
    }
    $post = $postRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $actual = @(Get-Tuples $post | Sort-Object)
    $expected = @(@($before + @("$role||$member")) | Sort-Object)
    if (@(Compare-Object -ReferenceObject $expected -DifferenceObject $actual).Count -ne 0) {
      throw 'S2_POLICY_DELTA_UNEXPECTED'
    }
    'G2_A7_S2_REPO_WRITER=ADDED_VERIFIED'
    'G2_A7_S2_OTHER_BINDINGS=PRESERVED_IN_REPO_POLICY'
    'G2_A7_S2_S3_S4=NOT_STARTED'
    'G2_A7_S2_BUILD_DEPLOY=NONE'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^S2_[A-Z_]+$') {
      $reason = 'S2_UNEXPECTED_ERROR'
    }
    'STOP_G2_A7_S2_NO_AUTOMATIC_RETRY'
    "REASON=$reason"
    'G2_A7_S2_CONFIRM_LIVE_REPO_POLICY_BEFORE_ANY_NEW_WRITE'
  }
}
```

### How to interpret

**Successful new binding:** `G2_A7_S2_PREIMAGE=TARGET_REPO_WRITER_ABSENT`, `G2_A7_S2_WRITE_CLI=EXIT_ZERO`, `G2_A7_S2_REPO_WRITER=ADDED_VERIFIED`, `G2_A7_S2_OTHER_BINDINGS=PRESERVED_IN_REPO_POLICY`. The expected tuple calculation includes pre-existing policy bindings unchanged plus exactly one new unconditional repository role+member. After successful screenshot, checkpoint S2 complete and only then prepare S3.

**Already present no-op:** `G2_A7_S2_WRITER=ALREADY_DIRECT_UNCONDITIONAL_NO_WRITE`; S2 is complete by preimage only for direct unconditional repo binding, not proof of actual upload attempts or inherited rights.

**STOP:** `STOP_G2_A7_S2_NO_AUTOMATIC_RETRY` on failed read/write, existing conditional target, policy delta drift, etc. STOP does not prove the write failed or that repo policy unchanged. No retry, manual reconciliation required before S3/S4 or any build.

Do not recheck old A1–A6/C1–C5/Grype/C3 signing/B1-R1/G4/CI/billing, and no new build/registry artifact/Docker/Cloud Run/Firebase/production. New builder permissions alone do not resolve G2 original scan 1 CRITICAL + 5 HIGH or independent original-builder provenance. `STEP04=HOLD`, `PRODUCTION=NO_GO`.

Official references: https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/repositories/get-iam-policy ; https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/repositories/add-iam-policy-binding ; https://docs.cloud.google.com/artifact-registry/docs/access-control .

**No cloud operation was executed by this GitHub documentation change.**
