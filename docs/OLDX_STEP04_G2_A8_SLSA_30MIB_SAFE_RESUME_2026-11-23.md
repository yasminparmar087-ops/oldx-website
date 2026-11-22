# OLDX Step 04 G2 A8 — 30 MiB partial Windows SLSA verifier, safe HTTP range recovery

Actual owner screenshot (23 Nov 2026 00:03 IST) one local read-only integrity diagnosis:
```text
A8_LOCAL_FILE_SIZE_BYTES=31457280
A8_OFFICIAL_FILE_SIZE_BYTES=33884672
A8_SIZE_MATCH=False
A8_LOCAL_SHA256=411c4086a4a2defb187c2fb7550a616eff8a75961a0aeaa2c48681c90fc1e79f
A8_OFFICIAL_SHA256_MATCH=False
A8_FILE_MZ_HEADER=True
A8_VERIFIER_EXECUTION=NOT_STARTED
A8_LOCAL_FILE_CHANGE=NONE
A8_CLOUD_MUTATIONS=NONE
A8_BUILD_RETRY=PROHIBITED
```

**Interpretation:** the owner file is **exactly 30 MiB**, 2,427,392 bytes short of the official 33,884,672-byte release asset (92.8% received). Local MZ header indicates PE format prefix but does NOT authenticate the partial file. The hash mismatch is explained by incomplete size; partial bytes are NOT yet independently validated. Crucially, the verifier binary did NOT run, so no SLSA cryptographic judgment exists. Do not change expected hash, execute partial file, or repeat existing Cloud Build/Registry operations.

Official connected GitHub release API for `slsa-framework/slsa-verifier` tag `v2.7.1`, rechecked: Windows AMD64 asset size 33,884,672 and SHA256 `1d8f61ad747ecc3d375d2a563cebf2991748b7da1a9bda9a500804c3c499e3c0`. `curl --continue-at -` officially supports resuming an existing local file by asking the server for missing bytes. If the server ignores the HTTP Range request, curl may stop with nonzero; this is a transport limitation, not proof the OLDX image is compromised. See https://curl.se/docs/manpage.html and https://everything.curl.dev/usingcurl/downloads/resume.html.

## Next owner action: one scoped copy-and-resume then only verified binary may run — NOT EXECUTED

Windows PowerShell prompt required. One-shot command verifies ORIGINAL 30MiB prefix SHA256 and file size against exact owner screenshot, checks private previously obtained provenance receipt, then copies original partial verifier to a **different** local `%TEMP%` path and attempts curl resume from the official GitHub release asset, only **one** network attempt with no automatic retry. `--continue-at -` uses the local output length, and curl rejects a server which cannot satisfy resumption. It checks final size and **full SHA256** against independent GitHub release metadata BEFORE any execution. On PASS only, it creates a local no-repeat verification marker and invokes slsa-verifier once against the previously approved immutable OLDX image, local provenance, GitHub source repository and GoogleHostedWorker builder ID, writes private verifier output to user profile. No Cloud Build/Cloud Run/IAM/Firebase/billing mutations. It has read-only HTTP network access (GitHub and verifier possible public key lookups). If range unsupported or hash mismatch, STOP and DO NOT run binary; preserve both original and copied file. On any failure no automatic re-run or deleting marker/backup. A nonzero verifier exit can mean policy or source URI mismatch and is NOT proof image invalid. Keep local verifier output PRIVATE; share only terminal sanitized markers.

```powershell
& {
  $stage = 'LOCAL_PRECHECK'
  try {
    $old = Join-Path $env:TEMP 'oldx-slsa-verifier-v2.7.1-windows-amd64.exe'
    $new = Join-Path $env:TEMP 'oldx-slsa-verifier-v2.7.1-resumed-once.exe'
    $log = Join-Path $env:USERPROFILE 'oldx-a8-slsa-verifier-2506826f.log'
    $marker = Join-Path $env:USERPROFILE '.oldx-a8-slsa-2506826f-attempted'
    $receipt = Join-Path $env:USERPROFILE 'oldx-a8-provenance-2506826f.json'
    $partialHash = '411c4086a4a2defb187c2fb7550a616eff8a75961a0aeaa2c48681c90fc1e79f'
    $fullHash = '1d8f61ad747ecc3d375d2a563cebf2991748b7da1a9bda9a500804c3c499e3c0'
    $url = 'https://github.com/slsa-framework/slsa-verifier/releases/download/v2.7.1/slsa-verifier-windows-amd64.exe'
    $image = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'

    if ((Test-Path -LiteralPath $new) -or (Test-Path -LiteralPath $log) -or
        (Test-Path -LiteralPath $marker)) {
      throw 'A8_RESUME_OR_VERIFY_ALREADY_ATTEMPTED'
    }
    if (-not (Test-Path -LiteralPath $receipt -PathType Leaf)) {
      throw 'A8_PRIVATE_PROVENANCE_RECEIPT_MISSING'
    }
    if ((Get-Item -LiteralPath $old -ErrorAction Stop).Length -ne 31457280) {
      throw 'A8_PARTIAL_SIZE_CHANGED'
    }
    if ((Get-FileHash -LiteralPath $old -Algorithm SHA256).Hash.ToLowerInvariant() -cne $partialHash) {
      throw 'A8_PARTIAL_HASH_CHANGED'
    }
    $null = Get-Command curl.exe -ErrorAction Stop
    Copy-Item -LiteralPath $old -Destination $new -ErrorAction Stop
    'A8_ORIGINAL_PARTIAL_FILE=PRESERVED'

    $stage = 'RESUME_REMAINING_BYTES_ON_COPY'
    $curlArgs = @('--fail','--location','--continue-at','-',
      '--retry','0','--connect-timeout','20','--max-time','600',
      '--silent','--show-error','--output',$new,$url)
    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
      & curl.exe @curlArgs 2>$null
      $curlCode = [int]$LASTEXITCODE
    } finally { $ErrorActionPreference = $previous }
    "A8_CURL_RESUME_EXIT_CODE=$curlCode"
    if ($curlCode -ne 0) { throw 'A8_HTTP_RANGE_RESUME_NOT_COMPLETED' }

    $stage = 'VERIFY_COMPLETED_DOWNLOAD_SHA256'
    $newSize = (Get-Item -LiteralPath $new).Length
    "A8_RESUMED_FILE_SIZE_BYTES=$newSize"
    if ($newSize -ne 33884672) { throw 'A8_COMPLETE_SIZE_MISMATCH' }
    $actualHash = (Get-FileHash -LiteralPath $new -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -cne $fullHash) { throw 'A8_COMPLETED_BINARY_HASH_MISMATCH' }
    'A8_OFFICIAL_VERIFIER_BINARY_SHA256=PASS'

    $stage = 'ONE_SLSA_CRYPTO_CHECK'
    $m = [System.IO.File]::Open($marker,[System.IO.FileMode]::CreateNew,
      [System.IO.FileAccess]::Write,[System.IO.FileShare]::None)
    $m.Dispose()
    $argsList = @('verify-image',$image,
      "--provenance-path=$receipt",
      '--source-uri=github.com/yasminparmar087-ops/oldx-website',
      '--builder-id=https://cloudbuild.googleapis.com/GoogleHostedWorker')
    $previous = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
      & $new @argsList *> $log
      $code = [int]$LASTEXITCODE
    } finally { $ErrorActionPreference = $previous }
    "A8_SLSA_VERIFIER_EXIT_CODE=$code"
    if ($code -eq 0) {
      $out = Get-Content -LiteralPath $log -Raw -ErrorAction Stop
      if ($out -match 'PASSED:\s*Verified SLSA provenance') {
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
    if ($reason -cnotmatch '^A8_[A-Z_]+$') { $reason = 'A8_UNEXPECTED_ERROR' }
    'STOP_A8_SAFE_RESUME_OR_VERIFICATION'
    "STAGE=$stage"
    "REASON=$reason"
    'A8_CLOUD_MUTATIONS=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  }
}
```

Existing source/build/digest evidence consumed: A8 Build ID `2506826f-ab8d-41a6-a60c-3f2ea3e74bd5`, pinned source `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`, immutable new Registry image `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`. Original 5 provenance signature fields were PRESENT, but cryptographic verification remains PENDING until this run succeeds. G2 CVE scan of this *new* image, focused default-DB runtime assessment, G4 other-DB/invoker, G8 spend/STOP all outstanding. Step04 HOLD; production NO_GO.