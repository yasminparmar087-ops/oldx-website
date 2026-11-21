# OLDX Step04 G2 A7 S3 — one guarded project Cloud Logging Writer grant (PREPARED, NOT EXECUTED)

21 November 2026 after owner's 20:16 IST verified S2 direct unconditional Artifact Registry Writer; branch `security-hardening-review`; project `oldx-staging`; owner `yasminparmar087@gmail.com`.

## Owner-approved boundary and verified preconditions

- **A7 approval ALREADY OBTAINED** (no new consent request): exactly one dedicated keyless builder `oldx-step04-build@oldx-staging.iam.gserviceaccount.com`, repository-scoped Artifact Registry Writer, project Cloud Logging Writer, and Yasmin-only resource-scoped Service Account User if needed. No manual role changes to other users, no `roles/editor`, no build, no registry upload, no deployment.
- S1 target SA existence was verified by an exact `gcloud iam service-accounts describe` after unexpected STOP; creator/time of original attempt unknown, no create retry.
- S2 first add-binding attempt stopped with unexpected PowerShell error. Subsequent owner's **actual ~20:16 IST screenshot** from re-entered original S2 code emitted `G2_A7_S2_WRITER=ALREADY_DIRECT_UNCONDITIONAL_NO_WRITE` and `G2_A7_S2_OTHER_IAM_WRITES=NONE`. That **proves the exact direct unconditional target binding was present at the later read**; no new IAM write on that latest no-op. Does not prove timing/actor of the earlier write nor independent preservation of all unrelated repository bindings. **S2 complete with limits; never rerun it.** [Canonical S2 reconciliation](OLDX_STEP04_G2_A7_S2_REPOSITORY_WRITER_GUARDED_2026-11-21.md).
- **S3 is a separate project-level permission** `roles/logging.logWriter` and may permit writing project logs broadly. It is approved only for future `CLOUD_LOGGING_ONLY` manual Cloud Build and does not grant reading logs, IAM admin or Artifact Registry administration.
- This A7 step does **not authorize** Cloud Build runs, a mutable GitHub trigger, credentials, project billing, storage bucket creation, Firebase, Cloud Run, public ingress, or production.

## One owner-run PowerShell S3 — PREPARED_NOT_EXECUTED

One fresh read of the exact project IAM policy is needed before this **new project IAM write**, not a repeat of old G4 read for reassurance. If the direct unconditional target role+member already exists, exit no-op. If conditional/duplicate, STOP. Otherwise attempt exactly **one** `gcloud projects add-iam-policy-binding oldx-staging --member=serviceAccount:oldx-step04-build@oldx-staging.iam.gserviceaccount.com --role=roles/logging.logWriter --condition=None`, then exactly one project policy post-read. Compare **role+condition+member tuples** to require all existing member tuples unchanged and only the new intended one added, without printing any policy/member list. Project policy changes outside these tuple values (e.g., etag) are not asserted unchanged. The write is not guaranteed against a concurrent external policy editor; post-delta mismatch is STOP, no automatic repair.

```powershell
& {
  $stage = 'START'
  try {
    $project = 'oldx-staging'
    $member = 'serviceAccount:oldx-step04-build@oldx-staging.iam.gserviceaccount.com'
    $role = 'roles/logging.logWriter'
    $common = @(
      '--account=yasminparmar087@gmail.com',
      '--format=json', '--quiet'
    )

    function Member-Keys($policy) {
      foreach ($b in @($policy.bindings)) {
        if ($null -eq $b) { continue }
        if (-not $b.role) { throw 'S3_BINDING_ROLE_MISSING' }
        $condition = if ($null -eq $b.condition) {
          ''
        } else {
          ConvertTo-Json -InputObject $b.condition -Compress -Depth 10
        }
        foreach ($m in @($b.members)) {
          if ($null -ne $m) {
            "$([string]$b.role)|$condition|$([string]$m)"
          }
        }
      }
    }

    $readArgs = @('projects','get-iam-policy',$project) + $common
    $stage = 'PRE_READ'
    $preRaw = & gcloud.cmd @readArgs 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $preRaw) {
      throw 'S3_PRE_READ_FAILED'
    }
    $pre = $preRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $hits = @(@($pre.bindings | Where-Object { $null -ne $_ }) |
      Where-Object { $_.role -ceq $role -and
                     @($_.members) -ccontains $member })
    if (@($hits | Where-Object { $null -ne $_.condition }).Count -ne 0) {
      throw 'S3_TARGET_HAS_CONDITIONAL_BINDING'
    }
    if ($hits.Count -gt 1) {
      throw 'S3_TARGET_DUPLICATE_BINDINGS'
    }
    if ($hits.Count -eq 1) {
      'G2_A7_S3_LOGGING_WRITER=ALREADY_DIRECT_UNCONDITIONAL_NO_WRITE'
      'G2_A7_S3_BUILD_DEPLOY_IAM_OTHER_WRITES=NONE'
      return
    }

    $stage = 'PREIMAGE_CHECK'
    $before = @(Member-Keys $pre | Sort-Object)
    'G2_A7_S3_PREIMAGE=TARGET_LOGGING_WRITER_ABSENT'

    $writeArgs = @(
      'projects','add-iam-policy-binding',$project,
      "--member=$member", "--role=$role", '--condition=None'
    ) + $common
    $stage = 'WRITE'
    & gcloud.cmd @writeArgs 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
      throw 'S3_WRITE_OUTCOME_UNCERTAIN'
    }
    'G2_A7_S3_WRITE_CLI=EXIT_ZERO'

    $stage = 'POST_READ'
    $postRaw = & gcloud.cmd @readArgs 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $postRaw) {
      throw 'S3_POST_READ_FAILED'
    }
    $post = $postRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $expected = @($before) + @("$role||$member")
    $actual = @(Member-Keys $post | Sort-Object)
    $stage = 'DELTA_CHECK'
    $difference = @(Compare-Object -ReferenceObject $expected -DifferenceObject $actual)
    if ($difference.Count -ne 0) {
      throw 'S3_POLICY_DELTA_UNEXPECTED'
    }
    'G2_A7_S3_PROJECT_LOGGING_WRITER=ADDED_VERIFIED'
    'G2_A7_S3_OTHER_PROJECT_IAM_MEMBER_TUPLES=PRESERVED'
    'G2_A7_S3_S4=NOT_STARTED'
    'G2_A7_S3_BUILD_DEPLOY=NONE'
  }
  catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^S3_[A-Z_]+$') {
      $reason = 'S3_UNEXPECTED_ERROR'
    }
    'STOP_G2_A7_S3_NO_AUTOMATIC_RETRY'
    "STAGE=$stage"
    "REASON=$reason"
    'G2_A7_S3_CONFIRM_LIVE_PROJECT_IAM_BEFORE_ANY_NEW_WRITE'
  }
}
```

## Result handling

- `G2_A7_S3_PROJECT_LOGGING_WRITER=ADDED_VERIFIED`: one conditional-free direct binding added and post-read tuple change exactly intended, **if** none concurrently changed the policy. Proceed only after screenshot/receipt to S4 guarded Yasmin-only actAs on the builder SA resource.
- `G2_A7_S3_LOGGING_WRITER=ALREADY_DIRECT_UNCONDITIONAL_NO_WRITE`: existing direct grant observed, no S3 write; S3 can be considered complete with limits.
- `STOP_G2_A7_S3_NO_AUTOMATIC_RETRY`: **do not rerun the S3 script**, even if `S3_WRITE_OUTCOME_UNCERTAIN`. Use one distinct targeted read-only project IAM reconciliation before any further IAM changes. STOP does not prove binding absent or no write. The output includes a sanitized `STAGE=` marker to locate pre-read/write/post-read/delta-check problems without printing sensitive policy details.
- Never print raw project IAM policy, users, etags, credentials or tokens, and never remove unrelated grants or add roles to the former owner.
- **No build/deploy/Registry image writes** within S3; original G2 unfiltered scan has 1 CRITICAL + 5 HIGH and trusted independent builder provenance remains UNKNOWN; G4 effective other DB denial and Cloud Run invoker exclusivity remain UNVERIFIED. `STEP04=HOLD`, `PRODUCTION=NO_GO`.

Official: https://docs.cloud.google.com/sdk/gcloud/reference/projects/get-iam-policy ; https://docs.cloud.google.com/sdk/gcloud/reference/projects/add-iam-policy-binding ; https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts

**GitHub-only preparation; no Cloud command executed by author.**
