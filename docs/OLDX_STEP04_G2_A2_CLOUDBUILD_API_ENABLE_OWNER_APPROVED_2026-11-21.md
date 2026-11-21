# OLDX Step04 G2 A2 — one exact Cloud Build API enable approved, owner-run guarded command

## 21 Nov 2026 ~19:22 IST — A2 OWNER EXECUTED: CLOUD BUILD API ENABLED_VERIFIED (NEW LATEST)

**Actual owner Windows PowerShell screenshot** after exactly the previously approved single guarded A2 command, returned to normal PowerShell prompt **without STOP**:

```text
G2_A2_FRESH_PREIMAGE=API_NOT_ENABLED
G2_A2_SINGLE_API_ENABLE_ATTEMPT=BEGIN
Operation "operations/acf.p2-38472235077-..." finished successfully.
G2_A2_ENABLE_CLI=EXIT_ZERO
G2_A2_CLOUD_BUILD_API=ENABLED_VERIFIED
G2_A2_BUILD_DEPLOY_IAM_COMMANDS=NONE
G2_A2_ONE_TIME_ENABLE=COMPLETE
PS C:\Users\Yasmin Parmar>
```

The owner-supervised single `gcloud.cmd services enable cloudbuild.googleapis.com --project=oldx-staging --account=yasminparmar087@gmail.com --quiet` command returned successfully and **one** post-enable enabled-service read found the expected API. The fresh prewrite read saw disabled before this one attempt. **`G2_A2=COMPLETE_VERIFIED`**, **`CLOUD_BUILD_API=ENABLED_AS_OF_OWNER_SCREENSHOT`**. A2 is now **CONSUMED: DO NOT RUN AGAIN**. `G2_A2_BUILD_DEPLOY_IAM_COMMANDS=NONE` establishes no such CLI subcommands in the prepared script, **not** a global audit of provider-managed service agent IAM changes. The screenshot does **not** assert a GitHub connection was queried, a Cloud Build job ran, or that any image, deployment, IAM grants or billing configuration were otherwise modified by the operator. The Cloud Build service may provision its own managed service agent as documented; do not infer the entire IAM policy is unchanged.

**NEXT distinct evidence:** One **read-only** `gcloud.cmd builds connections list --region=asia-south1` using the same owner and project. This check was intentionally never run in A1 because API was disabled. A regional list cannot prove the state in other regions; a connection count does not prove OLDX's repository is linked. Do not create a connection, service account or source trigger without separate exact approval. Continue Step04 G2 with independent builder provenance and 1 CRITICAL/5 HIGH frozen Grype risk unresolved, G4 effective other-DB/Invoker unverified. `STEP04=HOLD`, `PRODUCTION=NO_GO`. No redo of C1–C5/B1/R1/G4/A1/A2.

---

Date: 21 Nov 2026. Repo: `yasminparmar087-ops/oldx-website`, `security-hardening-review`.

## Actual owner permission — NEW

In the chat immediately after [G2 A1 Cloud Build API-disabled STOP](OLDX_STEP04_G2_A1_BUILD_API_DISABLED_OWNER_DECISION_2026-11-21.md), the owner explicitly replied `ha manjuri chhe` (yes, approved) to the exact question:

> "શું તમે માત્ર `oldx-staging` projectમાં `cloudbuild.googleapis.com` API ચાલુ કરવાની મંજૂરી આપો છો? આ મંજૂરીમાં build, IAM ફેરફાર, Registry upload, billing configuration બદલવી કે deployment કરવું સામેલ નથી."

**Authorization recorded:** `G2_A2_OWNER_APPROVAL=YES_ONE_API_ONLY` for **one** attempt at enabling `cloudbuild.googleapis.com` in **project `oldx-staging`**, using named owner identity `yasminparmar087@gmail.com`; one bounded fresh pre-enable enabled-services read, one enable write **only if still disabled**, and one post-enable enabled-services verification read. All other new provider actions require separate authorization.

**Not yet executed:** As of this document commit, owner has **NOT** shared any A2 command output. `G2_A2_API_ENABLE=APPROVED_PREPARED_NOT_RUN`; `G2_A2_CURRENT_CLOUD_API_STATE=LAST_OBSERVED_DISABLED_A1`, not a live current-state claim. The permission does not extend to Cloud Build submissions, GitHub source connection, triggers, IAM/SA or logging edits, registry pushes, source uploads, credentials, billing settings, Firebase/Firestore, Cloud Run traffic, production or feature activation.

**Provider-managed side effects:** Google Cloud docs state enabling Cloud Build commonly creates a Google-managed Cloud Build service agent and may grant its automatic service-agent role. This is an **inherent provider-side effect of the specifically approved API enable**, not a separately authorized manual IAM change; its presence/privileges must be reviewed at the later builder-account gate rather than claiming no IAM consequences whatsoever. No Cloud Build jobs are scheduled or run merely by this operator command; a pre-existing trigger or external automation is not inspected in this A2 scope.

## The exact one-shot owner Windows PowerShell A2 guard — PREPARED, NOT EXECUTED

Use `gcloud.cmd` (Windows Cloud SDK) with **pinned explicit** `--project=oldx-staging` and `--account=yasminparmar087@gmail.com`. The new fresh pre-image read is justified **only to guard a live write** and is not a replay of completed A1 diagnostic. If the API is already enabled, exit without a write; otherwise make exactly one enable attempt. Return STOP on any unexpected CLI/read status or uncertain post-check. This script never auto-retries and never attempts rollback; only operator may reconcile current API state after an uncertain result.

```powershell
& {
  try {
    $project = 'oldx-staging'
    $account = 'yasminparmar087@gmail.com'
    $api = 'cloudbuild.googleapis.com'
    $flags = @(
      "--project=$project",
      "--account=$account",
      '--quiet'
    )

    $before = @(& gcloud.cmd services list --enabled @flags '--format=value(config.name)' 2>$null)
    if ($LASTEXITCODE -ne 0 -or $before.Count -eq 0) {
      throw 'G2_A2_PRE_READ_FAILED'
    }
    $beforeMatches = @($before | Where-Object { $_.Trim() -ceq $api })
    if ($beforeMatches.Count -eq 1) {
      'G2_A2_API=ALREADY_ENABLED_NO_WRITE_NEEDED'
      'G2_A2_BUILD_DEPLOY_IAM_COMMANDS=NONE'
      return
    }
    if ($beforeMatches.Count -ne 0) { throw 'G2_A2_PRE_STATE_AMBIGUOUS' }

    'G2_A2_FRESH_PREIMAGE=API_NOT_ENABLED'
    'G2_A2_SINGLE_API_ENABLE_ATTEMPT=BEGIN'
    & gcloud.cmd services enable cloudbuild.googleapis.com @flags
    if ($LASTEXITCODE -ne 0) {
      throw 'G2_A2_WRITE_OUTCOME_UNCERTAIN'
    }
    'G2_A2_ENABLE_CLI=EXIT_ZERO'

    $after = @(& gcloud.cmd services list --enabled @flags '--format=value(config.name)' 2>$null)
    if ($LASTEXITCODE -ne 0 -or
        @($after | Where-Object { $_.Trim() -ceq $api }).Count -ne 1) {
      throw 'G2_A2_POST_READ_NOT_VERIFIED'
    }

    'G2_A2_CLOUD_BUILD_API=ENABLED_VERIFIED'
    'G2_A2_BUILD_DEPLOY_IAM_COMMANDS=NONE'
    'G2_A2_ONE_TIME_ENABLE=COMPLETE'
  }
  catch {
    'STOP_G2_A2_NO_AUTOMATIC_RETRY'
    'G2_A2_ENABLE_OR_VERIFICATION=UNCERTAIN'
    'G2_A2_CHECK_ACTUAL_API_STATE_BEFORE_ANY_NEW_WRITE'
  }
}
```

### Expected sanitized terminal evidence

- On truly newly enabled: `G2_A2_FRESH_PREIMAGE=API_NOT_ENABLED`, `G2_A2_ENABLE_CLI=EXIT_ZERO`, `G2_A2_CLOUD_BUILD_API=ENABLED_VERIFIED`, `G2_A2_ONE_TIME_ENABLE=COMPLETE`.
- On drift/no-op: `G2_A2_API=ALREADY_ENABLED_NO_WRITE_NEEDED`. This is not proof of who enabled it or when.
- On uncertainty: `STOP_G2_A2_NO_AUTOMATIC_RETRY`. **DO NOT re-run the same enable block**, and do not blindly disable or rollback the API. Request one new scoped read-only reconciliation if needed and record outcome before any new write.
- Normal console/Cloud SDK messages may also appear. Do not paste credentials/tokens; screenshots of sanitized status are sufficient.

## Exact continuation after the owner sends real output

1. Record actual observed A2 outcome verbatim and scope-limited in this file, the top of `AGENTS.md`, `docs/OLDX_CURRENT_HANDOFF.md`, and Issue #17. **No success claim before screenshot.**
2. **If enabled and verified**: stop A2. Next a **separately scoped read-only** `gcloud builds connections list --region=asia-south1` (previous A1 deliberately never ran), then a dedicated least-privilege builder identity/source pin/one-shot cost gate. This does not authorize a build or connection creation.
3. If not enabled/uncertain: hold Cloud Build provisioning, no retries, no new permissions or automatic API enable.
4. Never re-run old npm-free image build, local or remote Grype, existing registry push/C2/C3 signature, B1/R1/R2, G4 one-doc/analyzer or CI/billing checks for reassurance. Existing G2 Security Watch already handles material official advisories.
5. Existing image G2 severe findings **1 CRITICAL + 5 HIGH** and independent original-builder SLSA remain unresolved. G4 effective cross-DB denial and exclusive Cloud Run Invoker also unresolved. **`STEP04=HOLD`, `PRODUCTION=NO_GO`**.

Official sources:
- https://docs.cloud.google.com/sdk/gcloud/reference/services/enable
- https://docs.cloud.google.com/service-usage/docs/enable-disable
- https://docs.cloud.google.com/build/docs/set-up
- https://docs.cloud.google.com/build/docs/securing-builds/configure-access-for-cloud-build-service-account

*Writing this source-only GitHub note does not invoke Google Cloud or enable the API.*
