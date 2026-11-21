# OLDX Step04 G2 A7 S2 — repository-only Artifact Registry Writer (owner approved, PREPARED NOT EXECUTED)

## 21 Nov 2026 ~20:16 IST — S2 TARGET UNCONDITIONAL DIRECT BINDING VERIFIED, NO-OP (NEW LATEST)

**Actual owner PowerShell screenshot:** The screenshot's upper portion shows pasted source text of the **earlier guarded S2 script**, not the expected new read-only-only reconciliation script. Crucially, the **executed terminal output at the bottom** is:

```text
G2_A7_S2_WRITER=ALREADY_DIRECT_UNCONDITIONAL_NO_WRITE
G2_A7_S2_OTHER_IAM_WRITES=NONE
PS C:\Users\Yasmin Parmar>
```

This result is emitted **only by the existing unconditional target-binding no-op path** after the guarded S2 script fetched the exact repository IAM policy from `oldx-staging/asia-south1/oldx-staging-images`. Thus at ~20:16 IST the **direct unconditional** `roles/artifactregistry.writer` grant to `serviceAccount:oldx-step04-build@oldx-staging.iam.gserviceaccount.com` **was present**, and this latest run **did not issue another write**. The previous ~20:12 S2 STOP may have been caused after a successful prior mutation, but there is **no independent receipt of exactly when/which actor changed it** and **no stored complete old/new IAM policy delta from that attempt**. Do NOT claim unrelated bindings were independently proven preserved. The screenshot is **NOT** `G2_A7_S2_REPO_WRITER=ADDED_VERIFIED` and the S2 no-op path must not be confused with the separate read-only reconciliation source.

**State:** `A7_S2_TARGET_REPO_WRITER=DIRECT_UNCONDITIONAL_PRESENT_VERIFIED`; `A7_S2_LATEST_RUN=NO_WRITE`; `A7_S2_OTHER_BINDINGS_UNCHANGED=NOT_INDEPENDENTLY_VERIFIED`; `A7_S2=COMPLETE_WITH_LIMITS_CONSUMED`. **NEVER REPEAT S2 grant or its diagnostic**. The exact S1 builder identity was previously validated after a different STOP. A7 S3 project logging writer and S4 Yasmin actAs remain approved but **NOT EXECUTED**. Next: one owner-supervised, guarded S3 project-level `roles/logging.logWriter` to only builder SA, preserving unrelated bindings; [canonical S3 preparation](OLDX_STEP04_G2_A7_S3_LOGGING_WRITER_GUARDED_2026-11-21.md). Do not run S4 until S3 checkpoint.

No build, docker, registry upload, firebase, Cloud Run, or production action was proven; `STEP04=HOLD`, `PRODUCTION=NO_GO`.

---

## 21 Nov 2026 ~20:12 IST — S2 attempted, STOP_UNEXPECTED_ERROR; LIVE REPO POLICY UNKNOWN (LATEST)

The owner shared an actual Windows PowerShell screenshot from **ONE already approved A7 S2** attempt (not merely pasted script). Visible execution output ends:

```text
G2_A7_S2_PREIMAGE=TARGET_REPO_WRITER_ABSENT
STOP_G2_A7_S2_NO_AUTOMATIC_RETRY
REASON=S2_UNEXPECTED_ERROR
G2_A7_S2_CONFIRM_LIVE_REPO_POLICY_BEFORE_ANY_NEW_WRITE
PS C:\Users\Yasmin Parmar>
```

**Correct inference:** Fresh repository IAM read succeeded and showed no matching **direct** repository Writer binding at the preimage. There was **no** `G2_A7_S2_WRITE_CLI=EXIT_ZERO` and no `G2_A7_S2_REPO_WRITER=ADDED_VERIFIED`. The original catch mapped an unexpected PowerShell exception to a generic reason, losing its exact cause; the screenshot **does not determine** whether a write was attempted/partially committed. **Do not claim policy unchanged or role added.** It is equally unsafe to blindly rerun the S2 grant. All follow-on IAM writes **S3/S4 are BLOCKED until S2 state is reconciled**. Owner's original precisely scoped A7 authorization remains recorded but is not permission to auto-retry a partially unknown mutation.

**Official Google check:** `gcloud artifacts repositories get-iam-policy REPOSITORY --location=REGION` is a scoped **read**; `add-iam-policy-binding --condition=None` is a supported form but this fact does not identify the earlier unexpected PowerShell exception. See https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/repositories/get-iam-policy and https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/repositories/add-iam-policy-binding .

### One distinct *read-only* post-STOP reconciliation — PREPARED NOT EXECUTED

The code makes exactly ONE repository IAM policy read for `oldx-staging-images` in `oldx-staging/asia-south1`, with Yasmin as explicit account. It outputs only direct target principal `roles/artifactregistry.writer` binding counts, separated by conditional/unconditional, and no raw IAM policy, identities, ETags or tokens. A `0` means **no direct repo binding at the time of this read**, NOT proof that the S2 CLI never submitted a write or that inherited permissions are absent. A successful direct unconditional match confirms its **current presence only**; absent a stored full preimage, it cannot assert all other bindings were preserved. An unexpected/multiple/conditional result means manual review before next write.

```powershell
& {
  try {
    $member = 'serviceAccount:oldx-step04-build@oldx-staging.iam.gserviceaccount.com'
    $role = 'roles/artifactregistry.writer'
    $argsList = @(
      'artifacts','repositories','get-iam-policy','oldx-staging-images',
      '--project=oldx-staging',
      '--location=asia-south1',
      '--account=yasminparmar087@gmail.com',
      '--format=json','--quiet'
    )
    $raw = & gcloud.cmd @argsList 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) {
      throw 'REPOSITORY_POLICY_READ_FAILED'
    }
    $policy = $raw | Out-String | ConvertFrom-Json -ErrorAction Stop
    if ($null -eq $policy -or $policy -isnot [psobject]) {
      throw 'REPOSITORY_POLICY_SHAPE_UNKNOWN'
    }
    $unconditional = 0
    $conditional = 0
    foreach ($binding in @($policy.bindings)) {
      if ($null -eq $binding) { continue }
      if ([string]$binding.role -cne $role) { continue }
      foreach ($principal in @($binding.members)) {
        if ([string]$principal -cne $member) { continue }
        if ($null -eq $binding.condition) {
          $unconditional++
        } else {
          $conditional++
        }
      }
    }
    "G2_A7_S2_DIRECT_UNCONDITIONAL_COUNT=$unconditional"
    "G2_A7_S2_DIRECT_CONDITIONAL_COUNT=$conditional"
    if ($unconditional -eq 1 -and $conditional -eq 0) {
      'G2_A7_S2_REPO_WRITER=PRESENT_VERIFIED_AFTER_STOP'
    } elseif ($unconditional -eq 0 -and $conditional -eq 0) {
      'G2_A7_S2_REPO_WRITER=NO_DIRECT_BINDING_AT_READ'
    } else {
      'G2_A7_S2_REPO_WRITER=AMBIGUOUS_BINDINGS_REVIEW'
    }
    'G2_A7_S2_CREATE_OR_GRANT_RETRY=PROHIBITED'
    'G2_A7_S2_OTHER_BINDINGS_PRESERVED=NOT_INDEPENDENTLY_VERIFIED'
    'G2_A7_S3_S4=NOT_STARTED'
    'G2_A7_S2_CLOUD_WRITES=NONE_IN_RECONCILIATION'
  } catch {
    'STOP_G2_A7_S2_READ_ONLY_RECONCILIATION'
    'G2_A7_S2_REPO_WRITER=UNVERIFIED'
    'G2_A7_S3_S4=BLOCKED'
  }
}
```

- If `G2_A7_S2_REPO_WRITER=PRESENT_VERIFIED_AFTER_STOP`, log **S2 target binding present with limits**; DO NOT repeat the S2 add-binding command; only then consider already owner-approved S3 with its own exact prewrite IAM guards. `OTHER_BINDINGS_PRESERVED=NOT_INDEPENDENTLY_VERIFIED` remains truthful.
- If `NO_DIRECT_BINDING_AT_READ`, do **not** immediately replay S2; instead inspect the *actual earlier CLI error* in a **new separate, read-only/local diagnostic** before designing a corrected write. A 0 can reflect no direct role but inherited grants were not checked.
- On `AMBIGUOUS_BINDINGS_REVIEW` or any STOP: no IAM modifications or automatic retries; retain `STEP04=HOLD`.
- This reconciliation does NOT run Cloud Build, change service-account keys, Registry image storage, any IAM role, Firebase, Cloud Run, GitHub workflow, spend or production settings.
- Previous S1 identity is `EXISTS_VERIFIED_AFTER_STOP`, A1–A6/C1–C5/B1-R1/G4 consumed (never redo). G2 six severe scan findings and builder-origin provenance still unresolved. `PRODUCTION=NO_GO`.

---

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
