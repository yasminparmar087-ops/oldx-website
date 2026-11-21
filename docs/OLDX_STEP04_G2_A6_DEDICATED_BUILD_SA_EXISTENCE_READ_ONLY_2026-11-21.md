# OLDX Step04 — G2 A6 exact dedicated build identity existence preflight (SOURCE-ONLY)

21 Nov 2026, after owner A5 screenshot, repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`, GCP project `oldx-staging`.

## The consumed new result

Owner's actual Windows PowerShell output at ~19:51 IST after ONE `gcloud.cmd builds get-default-service-account --region=asia-south1`:

```text
G2_A5_DEFAULT_BUILD_SA=COMPUTE_DEFAULT
G2_A5_BUILD_SA_IAM_PRIVILEGES=NOT_CHECKED
G2_A5_DEDICATED_BUILDER=NOT_CREATED
G2_A5_CLOUD_BUILD_JOB=NOT_STARTED
G2_A5_CLOUD_WRITES=NONE
G2_A5_DEFAULT_IDENTITY_READ=COMPLETE_WITH_LIMITS
```

A5 is DONE, **never rerun**. Cloud Build's default identity would be Compute Engine default (project-number-specific account). Its *role grants and effective capabilities have never been verified by A5*; do NOT pronounce that identity universally overprivileged nor automatically use it in a new image build. Google's documented secure default is a **separately controlled user-managed build SA**.

OLDX's existing `oldx-product-read-staging` service account handles runtime Firestore/Auth requirements; **do not reuse a runtime identity for building** or grant it Artifact Registry write. The A4 GitSource alternative uses exact public Git URL and full SHA without a new GitHub v2 Connection.

## Proposed exact separate builder identity

Suggested **new** principal (not yet created or approved for creation): `oldx-step04-build@oldx-staging.iam.gserviceaccount.com`.

Before proposing *one combined explicit approval* to create/configure it, it is worth **one** read-only existence check to avoid a duplicate or name collision, using the supported Google `gcloud iam service-accounts list` for the exact project. Do not inspect IAM roles for every account or repeat the consumed old G4/B1 project IAM audits. The script reads SA metadata once and prints only whether **that one proposed email** is already present. It never prints the list, account emails or metadata. A `NOT_PRESENT` is scoped to returned list only, not proof of all impersonation paths, service-account quota, or grant eligibility.

### A6 — ONE Windows PowerShell READ ONLY, prepared NOT EXECUTED

```powershell
& {
  try {
    $argsList = @(
      'iam','service-accounts','list',
      '--project=oldx-staging',
      '--account=yasminparmar087@gmail.com',
      '--format=json',
      '--quiet'
    )
    $raw = & gcloud.cmd @argsList 2>$null
    if ($LASTEXITCODE -ne 0 -or $null -eq $raw) {
      throw 'G2_A6_ACCOUNT_LIST_FAILED'
    }
    $json = ($raw | Out-String).Trim()
    if ([string]::IsNullOrWhiteSpace($json)) {
      throw 'G2_A6_EMPTY_RESPONSE'
    }
    $parsed = ConvertFrom-Json -InputObject $json -ErrorAction Stop
    $accounts = @($parsed | Where-Object { $null -ne $_ })
    $target = @($accounts | Where-Object {
      [string]$_.email -ceq 'oldx-step04-build@oldx-staging.iam.gserviceaccount.com'
    })
    if ($target.Count -gt 1) {
      throw 'G2_A6_DUPLICATE_ACCOUNT_RESPONSE'
    }
    if ($target.Count -eq 0) {
      'G2_A6_DEDICATED_BUILDER_ID=NOT_PRESENT'
    } else {
      'G2_A6_DEDICATED_BUILDER_ID=EXISTS'
      if ($target[0].disabled -eq $true) {
        'G2_A6_DEDICATED_BUILDER_STATUS=DISABLED'
      } else {
        'G2_A6_DEDICATED_BUILDER_STATUS=NOT_MARKED_DISABLED'
      }
    }
    'G2_A6_OTHER_ACCOUNT_IAM=NOT_EVALUATED'
    'G2_A6_COMPUTE_DEFAULT_PERMISSIONS=NOT_CHECKED'
    'G2_A6_CLOUD_BUILD_JOB=NOT_STARTED'
    'G2_A6_CLOUD_WRITES=NONE'
    'G2_A6_EXISTENCE_READ=COMPLETE_WITH_LIMITS'
  } catch {
    'STOP_G2_A6_NO_AUTOMATIC_RETRY'
    'G2_A6_DEDICATED_BUILDER_ID=UNVERIFIED'
    'G2_A6_CLOUD_WRITES=NONE'
  }
}
```

Interpretation:

- `G2_A6_DEDICATED_BUILDER_ID=NOT_PRESENT` with `G2_A6_EXISTENCE_READ=COMPLETE_WITH_LIMITS`: planned dedicated identity is not currently listed. **Do NOT create it without separate owner approval**. Next prepare one bounded proposal with exact SA creation, Repository-scoped Artifact Registry Writer, Cloud Logging Writer scoped as required, and owner/Cloud Build agent service-account delegation strictly as official requirements permit. No broad Editor role. Exact costs, source SHA and unique new image must be approved separately.
- `EXISTS`: do not overwrite or modify it; inspect *only this target* with separate scope to establish effective specific rights before any use.
- `STOP_G2_A6_NO_AUTOMATIC_RETRY`: stop; no retry, no IAM role changes to force result.
- All results are **read-only**. No service-account keys, credentials, builds, Docker, scan, Registry write, Cloud Run or Firebase changes.

A6 does **not** justify touching the Compute default service account. If needed later, Google official Cloud Build user-managed SA docs require correctly scoped `iam.serviceAccounts.actAs`, log writes (Cloud Logging or owned bucket), and a build identity whose only Registry write scope is the approved existing `asia-south1/oldx-staging-images` repo (as known from previous OLDX C0/C1 evidence). Verify IAM roles/pricing once for the *new* identity, not by doing a broad status sweep.

**Current gate state:** A2 API enabled; A3 0 regional connections, consumed; A4 public direct GitSource documented but untested; A5 Compute default confirmed with privileges unknown; **A6 PREPARED_NOT_EXECUTED**, original G2 1 CRITICAL/5 HIGH unresolved, new trusted-builder provenance not yet generated, G4 actual cross-DB and exclusive invoker unverified. `STEP04=HOLD`, `PRODUCTION=NO_GO`.

Official docs:
- https://docs.cloud.google.com/sdk/gcloud/reference/iam/service-accounts/list
- https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts
- https://docs.cloud.google.com/build/docs/cloud-build-service-account-updates

**No GCP action executed to prepare this document.**
