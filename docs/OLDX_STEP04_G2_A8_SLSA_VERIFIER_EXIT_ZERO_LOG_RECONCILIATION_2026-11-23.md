# OLDX Step 04 G2 A8 — resumed verifier checksum PASS, v2.7.1 EXIT ZERO; local success-text reconcile

## Actual owner screenshot: 23 November 2026 ~00:10 IST
```text
A8_ORIGINAL_PARTIAL_FILE=PRESERVED
A8_CURL_RESUME_EXIT_CODE=0
A8_RESUMED_FILE_SIZE_BYTES=33884672
A8_OFFICIAL_VERIFIER_BINARY_SHA256=PASS
A8_SLSA_VERIFIER_EXIT_CODE=0
A8_SIGNED_IMAGE_SOURCE_BUILDER=EXIT_ZERO_OUTPUT_REVIEW
A8_VERIFIER_LOG=SAVED_PRIVATE
A8_NEW_IMAGE_SECURITY_SCAN=NOT_YET_DONE
A8_CLOUD_MUTATIONS=NONE
A8_BUILD_RETRY=PROHIBITED
```

One owner-approved verifier attempt was actually executed only after official SHA256 matched, checking exact new A8 image `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`, GitHub source `github.com/yasminparmar087-ops/oldx-website` and trusted Cloud Build builder ID `https://cloudbuild.googleapis.com/GoogleHostedWorker`. Source Git commit from Build API remains `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`. **No new build or binary download required; do not run the verifier again.**

## Why exit-zero was labeled `OUTPUT_REVIEW`

Previous script only searched private verifier output for `PASSED: Verified SLSA provenance`. The older SLSA Framework documentation gives that wording; other supported successful output is `PASSED: SLSA verification passed`. This is a **text-classifier issue candidate**, not a verifier cryptographic failure: v2.7.1 successfully exited with code 0. Actual private output text has NOT yet been read by this assistant; do not assert which variant was printed until local check. Official sources: https://github.com/slsa-framework/slsa-verifier (Cloud Build documentation section shows first form); https://docs.stackable.tech/home/stable/guides/verifying-image-provenance/ (second form).

## Next: ONE LOCAL-ONLY PRIVATE LOG SHAPE INSPECTION — prepared, not run

PowerShell 5.1 reads *existing* private `%USERPROFILE%\oldx-a8-slsa-verifier-2506826f.log`, confirms the one-shot marker and official SHA256 of previously resumed verifier, and prints sanitized true/false flags for **both** supported success-message forms, no raw log, no source payload/secrets. No network calls, no cloud/billing/IAM/Registry/Firestore writes, no new verification attempt. Exit-zero was observed in prior screenshot, not re-derived from log; when one supported PASS pattern is found in same prior saved log it corroborates cryptographic verification of builder + source repository + digest under the pinned tool policy. It does not independently certify the exact 40-character Git commit against signed build materials or clear vulnerabilities/G4/G8.

```powershell
& {
  try {
    $log = Join-Path $env:USERPROFILE 'oldx-a8-slsa-verifier-2506826f.log'
    $exe = Join-Path $env:TEMP 'oldx-slsa-verifier-v2.7.1-resumed-once.exe'
    $marker = Join-Path $env:USERPROFILE '.oldx-a8-slsa-2506826f-attempted'
    $expectedHash = '1d8f61ad747ecc3d375d2a563cebf2991748b7da1a9bda9a500804c3c499e3c0'

    if (-not (Test-Path -LiteralPath $log -PathType Leaf)) {
      throw 'A8_VERIFIER_LOG_MISSING'
    }
    if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) {
      throw 'A8_VERIFIER_ATTEMPT_MARKER_MISSING'
    }
    if (-not (Test-Path -LiteralPath $exe -PathType Leaf)) {
      throw 'A8_VERIFIER_BINARY_MISSING'
    }

    $hash = (Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -cne $expectedHash) {
      throw 'A8_VERIFIER_BINARY_IDENTITY_CHANGED'
    }
    'A8_VERIFIER_BINARY_SHA256=PASS'

    $text = Get-Content -LiteralPath $log -Raw -Encoding UTF8 -ErrorAction Stop
    if ([string]::IsNullOrWhiteSpace($text)) {
      throw 'A8_VERIFIER_LOG_EMPTY'
    }
    $oldPattern = $text -match '(?im)^\s*PASSED:\s*Verified SLSA provenance\s*$'
    $newPattern = $text -match '(?im)^\s*PASSED:\s*SLSA verification passed\s*$'
    "A8_LOG_OLD_SUCCESS_PATTERN=$oldPattern"
    "A8_LOG_ALTERNATE_SUCCESS_PATTERN=$newPattern"
    if ($oldPattern -or $newPattern) {
      'A8_VERIFIER_SUCCESS_TEXT=PRESENT'
      'A8_WITH_PRIOR_EXIT_ZERO=CRYPTO_PASS_SUPPORTED'
    } else {
      'A8_VERIFIER_SUCCESS_TEXT=NOT_FOUND'
      'A8_CRYPTO_VERDICT=REQUIRES_FURTHER_REVIEW'
    }

    'A8_SIGNED_EXACT_GIT_COMMIT_SHA=NOT_INDEPENDENTLY_CHECKED'
    'A8_NEW_IMAGE_SECURITY_SCAN=NOT_DONE'
    'A8_CLOUD_NETWORK_ACTIONS=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^A8_[A-Z_]+$') {
      $reason = 'A8_LOCAL_LOG_READ_ERROR'
    }
    'STOP_A8_VERIFIER_LOCAL_LOG_CLASSIFICATION'
    "REASON=$reason"
    'A8_CLOUD_NETWORK_ACTIONS=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  }
}
```

**If neither PASS pattern occurs**, do not mark G2 provenance fully passed; inspect only minimal redacted lines of private log through a distinct sensitive-safe diagnostic rather than uploading raw log. Do not execute the old one-shot again. After supported PASS text, next narrowly compare signed statement source commit materials to previously Build API-verified full SHA, then **one new image digest-specific Grype/Artifact Analysis** and bounded runtime/default DB guard evidence. Overall Step04 HOLD and production NO_GO until independent G4/G8 and risk decisions.