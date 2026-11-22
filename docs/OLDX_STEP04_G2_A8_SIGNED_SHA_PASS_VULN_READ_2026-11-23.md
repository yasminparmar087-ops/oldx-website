# OLDX Step04 G2 A8 — signed source SHA PASS; read existing vulnerability metadata next

## Actual owner screenshot 23 November 2026 ~00:19 IST
```text
A8_SIGNED_V01_SOURCE_MATERIAL_COUNT=1
A8_SIGNED_SOURCE_COMMIT_SHA_MATCH=True
A8_SIGNED_SUBJECT_DIGEST_MATCH=True
A8_SIGNED_BUILDER_ID_RECOGNIZED=True
A8_SIGNED_COMMIT_MATERIALS=CONSISTENT_WITH_APPROVED_BUILD
A8_SIGNED_PAYLOAD_RAW=NOT_EXPORTED
A8_CLOUD_ACTIONS=NONE
A8_BUILD_OR_VERIFIER_RERUN=NONE
```

Together with earlier checksum-verified SLSA verifier v2.7.1 EXIT 0 and true private-log success message `PASSED: SLSA verification passed`, **exact approved Git commit source material, signed output digest, and GoogleHostedWorker builder identity PASS with bounded confidence**, in immutable single A8 image. Actual Build source commit `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`; image digest `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`. No reruns of build, verifier, previous local Grype or older scans. No new Cloud actions.

## Next: ONE exact digest read of existing Artifact Analysis vulnerability metadata — PREPARED NOT EXECUTED

Google Cloud officially supports `gcloud artifacts docker images describe IMAGE@sha256:... --show-package-vulnerability --format=json`; this is an **existing metadata read**, not `gcloud artifacts docker images scan`, which starts a new on-demand scan and might cost US$0.26 per image. Automatic scan availability and container scanning API state are NOT established; earlier `containeranalysis.googleapis.com` enable check alone is insufficient to claim auto-scanning. Only if discovery includes `FINISHED_SUCCESS` and package vulnerability summary exists do we display occurrence counts. No discovery metadata ≠ zero CVEs. This action has no new scan, Cloud Build, IAM, Artifact Registry write, Cloud Run, Firebase or billing mutation.

Exactly one owner PowerShell block below requests existing metadata by approved *immutable* image digest, validates returned image identity, saves full result as a new private local JSON under USERPROFILE, prints only sanitized discovery statuses, severity occurrence counts, provider total and distinct CRITICAL/HIGH CVE IDs where scan completed. It never prints credential or full JSON. Existing local file prevents repeat. All counts are provider-specific and NOT automatically equivalent to independent Grype findings; severity categories and package match counts differ by scanner. Only user screenshot of sanitized markers is required. If metadata missing or permission denied, STOP any claim that image is clear; decide later on a **single new-image-specific** Grype or explicitly approved on-demand paid scan.

```powershell
& {
  $stage = 'PRECHECK'
  try {
    $digest = 'sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'
    $image = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@' + $digest
    $report = Join-Path $env:USERPROFILE 'oldx-a8-artifact-vulns-2506826f.json'
    if (Test-Path -LiteralPath $report) { throw 'A8_VULN_REPORT_ALREADY_EXISTS' }

    $stage = 'READ_EXISTING_SCAN_METADATA'
    $argsList = @('artifacts','docker','images','describe',$image,
      '--show-package-vulnerability','--format=json',
      '--project=oldx-staging','--account=yasminparmar087@gmail.com','--quiet')
    $raw = & gcloud.cmd @argsList 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) { throw 'A8_VULN_METADATA_READ_FAILED' }

    $stage = 'VERIFY_IMAGE_IDENTITY'
    $rawText = $raw | Out-String
    $data = $rawText | ConvertFrom-Json -ErrorAction Stop
    $gotDigest = [string]$data.image_summary.digest
    $gotFull = [string]$data.image_summary.fully_qualified_digest
    if (($gotDigest -and $gotDigest -cne $digest) -or
        ($gotFull -and $gotFull -cne $image) -or
        (-not $gotDigest -and -not $gotFull)) {
      throw 'A8_VULN_METADATA_DIGEST_MISMATCH'
    }
    'A8_VULN_TARGET_IMAGE_DIGEST=PASS'

    $stage = 'SAVE_PRIVATE_RECEIPT'
    $fs = [System.IO.File]::Open($report,[System.IO.FileMode]::CreateNew,
      [System.IO.FileAccess]::Write,[System.IO.FileShare]::None)
    try {
      $bytes = [System.Text.Encoding]::UTF8.GetBytes($rawText)
      $fs.Write($bytes,0,$bytes.Length)
    } finally { $fs.Dispose() }
    'A8_VULN_METADATA_RECEIPT=PRIVATE_LOCAL_SAVED'

    $scanRows = @($data.discovery_summary.discovery | Where-Object { $_ })
    $states = @($scanRows | ForEach-Object { [string]$_.discovery.analysisStatus } |
      Where-Object { $_ } | Sort-Object -Unique)
    "A8_SCAN_DISCOVERY_ENTRIES=$($scanRows.Count)"
    "A8_SCAN_STATES=$($states -join ',')"
    $scanPassed = @($states | Where-Object { $_ -ceq 'FINISHED_SUCCESS' }).Count -gt 0
    $summary = $data.package_vulnerability_summary
    if (-not $scanPassed -or $null -eq $summary) {
      'A8_NEW_IMAGE_VULNERABILITIES=UNVERIFIED_OR_SCAN_NOT_READY'
    } else {
      'A8_SCAN_DISCOVERY=FINISHED_SUCCESS'
      $v = $summary.vulnerabilities
      foreach ($level in @('CRITICAL','HIGH','MEDIUM','LOW','NEGLIGIBLE','UNKNOWN')) {
        $prop = if ($null -ne $v) { $v.PSObject.Properties[$level] } else { $null }
        $count = if ($null -eq $prop) { 0 } else {
          @($prop.Value | Where-Object { $_ }).Count
        }
        "A8_VULNERABILITY_$($level)_OCCURRENCES=$count"
      }
      "A8_PROVIDER_REPORTED_TOTAL=$($summary.total_vulnerability_found)"
      $severe = @($v.CRITICAL) + @($v.HIGH)
      $ids = @($severe | Where-Object { $_ } | ForEach-Object {
        [string]$_.vulnerability.shortDescription
      } | Where-Object { $_ -match '^CVE-[0-9]{4}-[0-9]{4,}$' } |
        Sort-Object -Unique)
      "A8_SEVERE_UNIQUE_CVE_IDS=$($ids -join ',')"
      'A8_FINDINGS_REQUIRE_TRIAGE=YES'
    }
    'A8_NEW_SCAN_STARTED_BY_COMMAND=NO'
    'A8_CLOUD_MUTATIONS=NONE'
    'A8_BUILD_OR_VERIFIER_RERUN=NONE'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^A8_[A-Z_]+$') { $reason = 'A8_UNEXPECTED_ERROR' }
    'STOP_A8_EXISTING_VULN_METADATA_READ'
    "STAGE=$stage"
    "REASON=$reason"
    'A8_CLOUD_MUTATIONS=NONE'
    'A8_BUILD_OR_VERIFIER_RERUN=NONE'
  }
}
```

Follow-on after evidence: triage severe CVEs and vendor fixability; one focused new-digest runtime/default Firestore `(default)` guard and nonroot startup test, G4 effective other-DB/invoker and G8 all-provider cost gate. Step04 HOLD, production NO_GO. Do not redeploy image as a scanning workaround.

Official sources: https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/docker/images/describe ; https://docs.cloud.google.com/artifact-analysis/docs/package-scan-automatic ; https://cloud.google.com/artifact-analysis/pricing