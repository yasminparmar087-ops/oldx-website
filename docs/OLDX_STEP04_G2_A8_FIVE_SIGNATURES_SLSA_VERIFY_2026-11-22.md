# OLDX Step04 G2 A8 — FIVE provenance signatures / independent SLSA verification next

Actual owner PowerShell screenshot: A8_LOCAL_EXACT_DIGEST=PASS; A8_ENTRY_COUNT=2; Entry 1 SLSA_V0_1 with 3 envelope signature fields, payload present, resource match True; Entry 2 type UNKNOWN with 2 envelope signature fields, payload present, resource match True; A8_TOTAL_ENVELOPE_SIGNATURE_FIELDS=5; cryptographic verification NOT DONE; new-image security scan NOT DONE; cloud reads/writes NONE; build retry PROHIBITED. UNKNOWN means only unrecognized source-only classifier, not a cryptographic failure.

Subject: new private Registry image digest sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc. Build 2506826f-ab8d-41a6-a60c-3f2ea3e74bd5, source 31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71. Do NOT rebuild, rescan historic image, delete marker or overwrite new image.

## One owner-side Windows PowerShell SLSA verifier — PREPARED_NOT_EXECUTED

Google Cloud Build's official provenance guide endorses slsa-verifier verify-image with --provenance-path, --source-uri and --builder-id. Official SLSA Framework GitHub release API tag v2.7.1 (27 Jun 2025) reports Windows AMD64 slsa-verifier-windows-amd64.exe SHA256 1d8f61ad747ecc3d375d2a563cebf2991748b7da1a9bda9a500804c3c499e3c0, 33,884,672 bytes. This PowerShell block downloads that exact binary from official release only if absent, checks the SHA256 BEFORE executing it, then runs only one verifier attempt on existing local private provenance receipt, exact image digest, expected GitHub source URI, trusted GoogleHostedWorker builder ID, and saves raw verifier output to a private local logfile. No cloud mutations, build/registry/Cloud Run/Firestore changes. The verifier might make read-only network lookups.

```powershell
& {
  $ErrorActionPreference = 'Stop'
  $stage = 'START'
  try {
    $receipt = Join-Path $env:USERPROFILE 'oldx-a8-provenance-2506826f.json'
    $exe = Join-Path $env:TEMP 'oldx-slsa-verifier-v2.7.1-windows-amd64.exe'
    $log = Join-Path $env:USERPROFILE 'oldx-a8-slsa-verifier-2506826f.log'
    $expectedHash = '1d8f61ad747ecc3d375d2a563cebf2991748b7da1a9bda9a500804c3c499e3c0'
    $image = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'
    $stage = 'LOCAL_GUARDS'
    if (-not (Test-Path -LiteralPath $receipt -PathType Leaf)) { throw 'A8_PROVENANCE_RECEIPT_MISSING' }
    if (Test-Path -LiteralPath $log) { throw 'A8_VERIFIER_PREVIOUS_ATTEMPT_LOG_EXISTS' }
    $stage = 'GET_PINNED_VERIFIER'
    if (-not (Test-Path -LiteralPath $exe -PathType Leaf)) {
      Invoke-WebRequest -UseBasicParsing -Uri 'https://github.com/slsa-framework/slsa-verifier/releases/download/v2.7.1/slsa-verifier-windows-amd64.exe' -OutFile $exe -ErrorAction Stop
    }
    $stage = 'VERIFY_VERIFIER_SHA256'
    $actualHash = (Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -cne $expectedHash) { throw 'A8_VERIFIER_BINARY_HASH_MISMATCH' }
    'A8_OFFICIAL_VERIFIER_BINARY_SHA256=PASS'
    $stage = 'ONE_CRYPTOGRAPHIC_CHECK'
    $argsList = @('verify-image',$image,"--provenance-path=$receipt",
      '--source-uri=github.com/yasminparmar087-ops/oldx-website',
      '--builder-id=https://cloudbuild.googleapis.com/GoogleHostedWorker')
    $prev = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
      & $exe @argsList *> $log
      $code = [int]$LASTEXITCODE
    } finally { $ErrorActionPreference = $prev }
    "A8_SLSA_VERIFIER_EXIT_CODE=$code"
    if ($code -eq 0) {
      $output = Get-Content -LiteralPath $log -Raw -ErrorAction Stop
      if ($output -match 'PASSED:\s*Verified SLSA provenance') {
        'A8_SIGNED_IMAGE_SOURCE_BUILDER=CRYPTO_VERIFIED'
      } else {
        'A8_SIGNED_IMAGE_SOURCE_BUILDER=EXIT_ZERO_OUTPUT_REVIEW'
      }
    } else {
      'A8_SIGNED_IMAGE_SOURCE_BUILDER=NOT_VERIFIED_REVIEW_PRIVATE_LOG'
    }
    'A8_VERIFIER_LOG=SAVED_PRIVATE'
    'A8_NEW_IMAGE_SECURITY_SCAN=NOT_YET_DONE'
    'A8_CLOUD_MUTATIONS=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^A8_[A-Z_]+$') { $reason = 'A8_VERIFICATION_UNEXPECTED_ERROR' }
    'STOP_A8_SLSA_VERIFICATION'
    "STAGE=$stage"
    "REASON=$reason"
    'A8_CLOUD_MUTATIONS=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  }
}
```

Interpretation: code zero plus expected PASSED text is a cryptographic verification of the expected builder/source repository/digest *within verifier's policy*, not necessarily proof the signed statement itself has the exact 40-hex source SHA; follow-on review must check signed materials. Nonzero or unexpected output STOP without retrying build or relaxing source rules; a direct public GitSource not using GitHub triggers may result in source URI mismatch, which requires bounded review. Do not share private log contents or raw provenance; share only sanitised terminal lines. After verification, image-specific vulnerability scan + nonroot/startup/default-DB runtime review still needed; Step04 HOLD, production NO_GO.

Sources: https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance ; https://github.com/slsa-framework/slsa-verifier/releases/tag/v2.7.1 ; https://docs.cloud.google.com/build/gcb-buildtypes/google-worker/v1