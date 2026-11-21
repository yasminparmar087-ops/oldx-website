# OLDX Step04 G2 A7 — owner approval recorded, S1 dedicated builder identity create prepared

## 21 Nov 2026 ~20:03 IST — OWNER S1 STOP_UNEXPECTED_ERROR: CREATE STATE UNKNOWN (LATEST)

Actual owner Windows PowerShell screenshot after one **approved A7 S1** attempted execution shows these lines at the bottom:

```text
G2_A7_S1_PREIMAGE=TARGET_ABSENT
STOP_G2_A7_S1_NO_AUTOMATIC_RETRY
REASON=A7_S1_UNEXPECTED_ERROR
G2_A7_S1_CHECK_LIVE_ACCOUNT_BEFORE_ANY_NEW_WRITE
PS C:\Users\Yasmin Parmar>
```

**Interpretation:** The fresh read-only prewrite target absence check succeeded; S1 entered the subsequent script section but **no `G2_A7_S1_CREATE_CLI=EXIT_ZERO` or `G2_A7_S1_ACCOUNT=CREATED_VERIFIED` was printed**. Whether the service-account create call ran or partially succeeded is **UNKNOWN**. The catcher normalized an unexpected PowerShell exception to `A7_S1_UNEXPECTED_ERROR`, losing its specific diagnostic. This output is NOT proof the account was created; it is also NOT proof it was absent after the attempted create. No IAM role grants, build, registry upload, deployment or credential-key commands were present in the S1 block. Treat `A7_S1=STOP_UNCERTAIN`, `A7_S2_S3_S4=BLOCKED_NOT_EXECUTED`. Do not rerun the original S1, do not create a second account, do not guess a cause for the exception, and do not proceed to S2 permissions until identity has been independently read.

**Distinct one-time reconciliation (READ-ONLY, PREPARED NOT EXECUTED):** A targeted `gcloud.cmd iam service-accounts describe` **only on this exact builder identity**, as supported by Google's official CLI. Returns sanitized existence, not full metadata, unique ID, credentials, or broad listings. The Google CLI documentation cautions a describe failure can be due to a non-existent account OR lack of permission; therefore **failure is NOT labeled NOT_PRESENT**, and must STOP without retrying create or granting any role. If the exact identity is found enabled, this resolves existence (but not who created it), so S2 can then be separately guarded under the *already granted* owner A7 scope. If no verified identity, stop and design a different scoped read-only diagnostic; no new write.

```powershell
& {
  try {
    $email = 'oldx-step04-build@oldx-staging.iam.gserviceaccount.com'
    $argsList = @(
      'iam','service-accounts','describe',$email,
      '--project=oldx-staging',
      '--account=yasminparmar087@gmail.com',
      '--format=json','--quiet'
    )
    $raw = & gcloud.cmd @argsList 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) {
      'G2_A7_S1_ACCOUNT=NOT_CONFIRMED_READ_FAILED'
      'G2_A7_S1_CREATE_RETRY=PROHIBITED'
      'G2_A7_S2_IAM_WRITES=BLOCKED'
      return
    }
    $sa = $raw | Out-String | ConvertFrom-Json -ErrorAction Stop
    if ([string]$sa.email -cne $email -or
        [string]::IsNullOrWhiteSpace([string]$sa.uniqueId) -or
        $sa.disabled -eq $true) {
      throw 'IDENTITY_MISMATCH'
    }
    'G2_A7_S1_ACCOUNT=EXISTS_VERIFIED_AFTER_STOP'
    'G2_A7_S1_CREATOR_AND_TIME=NOT_PROVEN'
    'G2_A7_S1_CREATE_RETRY=PROHIBITED'
    'G2_A7_S2_IAM_WRITES=NOT_STARTED'
  } catch {
    'STOP_G2_A7_S1_READ_ONLY_RECONCILIATION'
    'G2_A7_S1_ACCOUNT=UNVERIFIED'
    'G2_A7_S2_IAM_WRITES=BLOCKED'
  }
}
```

No Cloud command was executed by the assistant in recording this note. Do not claim `A7_S1_COMPLETE` until a screenshot of actual successful reconciliation. Preserve all already-completed A1–A6, C1–C5, B1/R1, G4, original Grype/CI/billing and current 15-step plan; G2 security/provenance and G4 other-DB gates remain open. `STEP04=HOLD`, `PRODUCTION=NO_GO`.

---

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
