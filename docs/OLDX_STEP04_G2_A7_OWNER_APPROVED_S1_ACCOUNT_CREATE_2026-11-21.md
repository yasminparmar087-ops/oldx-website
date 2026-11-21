# OLDX Step04 G2 A7 — owner approval recorded, S1 dedicated builder identity create prepared

Date: 21 November 2026, `yasminparmar087-ops/oldx-website` branch `security-hardening-review`; staging project `oldx-staging`.

## Owner consent, EXACT scope

The owner replied `ha manjuri chhe` to the A7 question immediately after the approved [A7 proposal](OLDX_STEP04_G2_A7_BUILDER_IDENTITY_LEAST_PRIVILEGE_APPROVAL_2026-11-21.md). Consent covers **only** (1) create `oldx-step04-build@oldx-staging.iam.gserviceaccount.com` (no user-managed keys), (2) `roles/artifactregistry.writer` ONLY on existing `oldx-staging-images` Artifact Registry repository, (3) `roles/logging.logWriter` in `oldx-staging` for `CLOUD_LOGGING_ONLY`, and (4) Yasmin's `roles/iam.serviceAccountUser` ONLY on the newly created builder SA if missing. No permissions for prior owner, no new IAM roles, Cloud Run/Firebase, billing changes, build, deploy, images, Docker or Grype.

**As of this file creation A7 is APPROVED but none of S1–S4 is observed executed. Do not claim execution without screenshot.**

## Controlled execution plan

Stage A7 into four owner-supervised mutation gates under this **one approval**, with GitHub checkpoints after each real screenshot: **S1** create exact account only; **S2** repo-scoped Artifact Registry Writer; **S3** project Logs Writer; **S4** owner Service Account User only on the new SA. This avoids a single unreviewable bulk IAM mutation and explicitly forbids automatic retries/rollbacks after an uncertain partial write. Approved scope does not grant permission for any new image build.

A6 read-only inventory at ~19:55 IST found target absent; it is CONSUMED. A **single fresh read directly before this first write** is necessary as a race guard, not a repeat diagnostic. If target exists, S1 must STOP without using or modifying it; if create succeeds but post-read fails, do not repeat create—reconcile current identity first. No key file/API enabled/broad IAM grant is part of S1.

## A7 S1 exact owner Windows PowerShell one-shot — PREPARED, NOT EXECUTED

```powershell
& {
  try {
    $email = 'oldx-step04-build@oldx-staging.iam.gserviceaccount.com'
    $common = @('--project=oldx-staging',
                '--account=yasminparmar087@gmail.com', '--quiet')

    $raw = & gcloud.cmd iam service-accounts list @common '--format=json' 2>$null
    if ($LASTEXITCODE -ne 0 -or $null -eq $raw) {
      throw 'A7_S1_PRE_READ_FAILED'
    }
    $list = @((($raw | Out-String) | ConvertFrom-Json -ErrorAction Stop) |
      Where-Object { $null -ne $_ })
    if (@($list | Where-Object { [string]$_.email -ceq $email }).Count -ne 0) {
      throw 'A7_S1_TARGET_ALREADY_EXISTS'
    }
    'G2_A7_S1_PREIMAGE=TARGET_ABSENT'

    $create = @('iam', 'service-accounts', 'create', 'oldx-step04-build',
      '--display-name=OLDX Step04 isolated staging builder',
      '--description=Keyless manual staging build identity') + $common + @('--format=json')
    & gcloud.cmd @create 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
      throw 'A7_S1_CREATE_UNCERTAIN'
    }
    'G2_A7_S1_CREATE_CLI=EXIT_ZERO'

    $postRaw = & gcloud.cmd iam service-accounts describe $email @common '--format=json' 2>$null
    if ($LASTEXITCODE -ne 0 -or $null -eq $postRaw) {
      throw 'A7_S1_POST_READ_FAILED'
    }
    $post = $postRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    if ([string]$post.email -cne $email -or
        [string]::IsNullOrWhiteSpace([string]$post.uniqueId) -or
        $post.disabled -eq $true) {
      throw 'A7_S1_POST_IDENTITY_MISMATCH'
    }
    'G2_A7_S1_ACCOUNT=CREATED_VERIFIED'
    'G2_A7_S1_IAM_ROLE_GRANTS=NOT_STARTED'
    'G2_A7_S1_KEY_COMMANDS=NONE'
    'G2_A7_S1_BUILD_DEPLOY=NOT_STARTED'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^A7_S1_[A-Z_]+$') {
      $reason = 'A7_S1_UNEXPECTED_ERROR'
    }
    'STOP_G2_A7_S1_NO_AUTOMATIC_RETRY'
    "REASON=$reason"
    'G2_A7_S1_CHECK_LIVE_ACCOUNT_BEFORE_ANY_NEW_WRITE'
  }
}
```

Expected only after owner's actual run: `G2_A7_S1_PREIMAGE=TARGET_ABSENT`; `G2_A7_S1_CREATE_CLI=EXIT_ZERO`; `G2_A7_S1_ACCOUNT=CREATED_VERIFIED`; `G2_A7_S1_IAM_ROLE_GRANTS=NOT_STARTED`; `G2_A7_S1_KEY_COMMANDS=NONE`; `G2_A7_S1_BUILD_DEPLOY=NOT_STARTED`.

Any `STOP_G2_A7_S1_NO_AUTOMATIC_RETRY` means **do not rerun** S1. If success, prepare ONE S2 repo policy binding read/write/postcheck, preserving unrelated bindings and refusing drift. S3 and S4 follow only after preceding verified state. No broad `roles/editor`, `roles/owner`, project-wide Registry Writer, additional Cloud Build agent Token Creator, old runtime service-account reuse, GitHub integration or production enable.

**A7 new image build remains NOT APPROVED; G2 one CRITICAL and five HIGH findings and unknown trusted original builder remain open. G4 cross-database/Cloud Run invoker effective controls unresolved. STEP04=HOLD, PRODUCTION=NO_GO.**

Official Google references: https://docs.cloud.google.com/sdk/gcloud/reference/iam/service-accounts/create ; https://docs.cloud.google.com/sdk/gcloud/reference/iam/service-accounts/describe ; https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts ; https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/repositories/add-iam-policy-binding ; https://docs.cloud.google.com/sdk/gcloud/reference/iam/service-accounts/add-iam-policy-binding .
