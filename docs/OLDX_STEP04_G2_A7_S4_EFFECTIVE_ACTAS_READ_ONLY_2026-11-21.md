## 21 Nov 2026 ~22:05 IST — S4 ACTUAL OWNER SCREENSHOT: EFFECTIVE VERIFIED (NEW LATEST)

Owner executed the previously prepared S4 PowerShell within `PS C:\Users\Yasmin Parmar>`. Actual printed result:

```text
G2_A7_S4_OWNER_ACTAS=EFFECTIVE_VERIFIED
G2_A7_S4_NEW_IAM_GRANT=NOT_NEEDED
G2_A7_S4_CLOUD_IAM_WRITES=NONE
G2_A7_S4_BUILD_DEPLOY=NONE
```

The authenticated owner `yasminparmar087@gmail.com`'s request to Google IAM `projects.serviceAccounts.testIamPermissions` for exact resource `projects/oldx-staging/serviceAccounts/oldx-step04-build@oldx-staging.iam.gserviceaccount.com` returned `iam.serviceAccounts.actAs`. This is effective permission at check time, **not necessarily a direct resource binding**, not authority to conclude which inherited role provided the permission. **No new `roles/iam.serviceAccountUser` grant is required and it MUST NOT be added redundantly.** The read-only permission request was a POST and printed no token. No Cloud Build/Registry/Cloud Run/deploy was performed.

**A7 S1–S4 CHECKPOINT:** S1 exact account EXISTS_VERIFIED_AFTER_STOP (original creation actor/time unknown); S2 repository Writer direct unconditional PRESENT_WITH_LIMITS (original write delta/actor unknown); S3 project Logging Writer direct unconditional PRESENT_WITH_LIMITS (original write delta/actor unknown); S4 owner actAs EFFECTIVE_VERIFIED, NO IAM GRANT. Mark `A7=IAM_SETUP_COMPLETE_WITH_EVIDENCE_LIMITS`; ALL four substeps **CONSUMED, NEVER RERUN**, do not recreate keys, adjust IAM or recheck permissions just for reassurance.

**Remaining G2 Step04:** user-managed builder permissions alone do NOT create a new trusted image, establish actual Cloud Build provenance or clear prior frozen image scan findings (1 CRITICAL + 5 HIGH), G4 runtime/default-DB/Cloud Run invoker and G8 all-service costs/STOP remain unresolved. Next is source-only freeze of one exact Dockerfile/commit SHA, build parameters/cost envelope and provenance acceptance then separately scoped owner approval **before one new Cloud Build job / private Artifact Registry image**. Existing A4 direct accessible public GitSource route is supported only as proposal, NOT attempted. No mutable branch/ref, fallback identity, auto-retry, deploy, production.

---

# OLDX Step04 G2 A7 S4 — owner effective actAs read-only check (prepared 21 Nov 2026)

## Current exact consumed state
- S1 dedicated builder account existence verified after earlier uncertain create. No keys created; avoid recreating.
- S2 repository-scoped `roles/artifactregistry.writer` for `serviceAccount:oldx-step04-build@oldx-staging.iam.gserviceaccount.com` on `oldx-staging-images` in `asia-south1` present direct unconditional, with no independent unrelated-policy-delta proof. NO repeat.
- S3 owner screenshot ~20:27 IST: `S3_UNCONDITIONAL_COUNT=1`, `S3_CONDITIONAL_COUNT=0`, `S3=PRESENT_VERIFIED_AFTER_STOP`, `S3_NO_WRITE_PERFORMED`. Current project Logging Writer direct unconditional binding is present. Earlier write stage error was ambiguous; NO repeat.
- Owner previously approved S4 `roles/iam.serviceAccountUser` only for `user:yasminparmar087@gmail.com` on the **new builder SA resource** IF NEEDED. No approval for granting any other principals, project-wide SA User, Cloud Build execution, new image or Cloud Run deploy.
- Official documentation says `roles/owner` typically includes `iam.serviceAccounts.actAs`, so **avoid an unnecessary S4 IAM write** by first querying current owner's EFFECTIVE permission on the exact resource. The SA's own IAM policy alone would not prove inherited roles. Google IAM service-account `testIamPermissions` is a permission-check POST only, not a policy mutation.

## One owner-run Windows PowerShell, S4 read-only — NOT YET RUN
Uses the existing gcloud owner login solely to obtain an access token **in memory**, then sends one `testIamPermissions` POST for exactly `iam.serviceAccounts.actAs`. Do NOT paste its token into chat or logs. Only sanitized status printed. If token/API lookup fails, STOP; it does not imply missing role. This is not a build nor an IAM mutation.

```powershell
& {
  try {
    $owner = 'yasminparmar087@gmail.com'
    $sa = 'oldx-step04-build@oldx-staging.iam.gserviceaccount.com'
    $token = & gcloud.cmd auth print-access-token "--account=$owner" 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $token) {
      throw 'S4_TOKEN_UNAVAILABLE'
    }
    $token = [string](@($token)[-1])
    $uri = "https://iam.googleapis.com/v1/projects/oldx-staging/serviceAccounts/${sa}:testIamPermissions"
    $body = '{"permissions":["iam.serviceAccounts.actAs"]}'
    $result = Invoke-RestMethod -Method Post -Uri $uri -Headers @{Authorization="Bearer $token"} -ContentType 'application/json' -Body $body -ErrorAction Stop
    if (@($result.permissions) -contains 'iam.serviceAccounts.actAs') {
      'G2_A7_S4_OWNER_ACTAS=EFFECTIVE_VERIFIED'
      'G2_A7_S4_NEW_IAM_GRANT=NOT_NEEDED'
    } else {
      'G2_A7_S4_OWNER_ACTAS=NOT_GRANTED_AT_CHECK'
      'G2_A7_S4_NEW_IAM_GRANT=REQUIRES_GUARDED_SA_POLICY_REVIEW'
    }
    'G2_A7_S4_CLOUD_IAM_WRITES=NONE'
    'G2_A7_S4_BUILD_DEPLOY=NONE'
  } catch {
    'STOP_G2_A7_S4_EFFECTIVE_PERMISSION_CHECK'
    'G2_A7_S4_OWNER_ACTAS=UNVERIFIED'
    'G2_A7_S4_CLOUD_IAM_WRITES=NONE'
  }
}
```

## Decision
- `G2_A7_S4_OWNER_ACTAS=EFFECTIVE_VERIFIED`: the required actAs permission is present now. S4 is satisfied by effective authorization; **do not add a redundant direct role**. This does NOT prove complete Cloud Build permissions, service-agent configuration, source provenance or ability to publish images.
- `G2_A7_S4_OWNER_ACTAS=NOT_GRANTED_AT_CHECK`: no current actAs in this context. Do not automatically grant it. Next prepare a *different*, guarded, approved resource-scoped S4 service-account-policy read + single only-if-absent role addition for Yasmin, post-delta proof, stop on uncertainty.
- `STOP`: token/API/auth/network trouble, cannot interpret as permission absence. Diagnose locally or through specific distinct safe check, do not grant role as fallback.

Official Google docs: https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/testIamPermissions ; https://docs.cloud.google.com/iam/docs/attach-service-accounts ; https://docs.cloud.google.com/iam/docs/manage-access-service-accounts

**No execution in GitHub.** Historical A1–A6, C1–C5, prior B1/R1, G4 and CI/Grype remain consumed. G2 original 1 CRITICAL + 5 HIGH and trustworthy builder provenance unknown; Step04 HOLD and production NO_GO.
