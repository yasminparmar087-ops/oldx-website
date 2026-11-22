# OLDX Step 04 G2 A8 — SHA256 mismatch during verifier acquisition, local diagnosis next

Owner's **actual** Windows PowerShell screenshot (23 Nov 2026 ~00:01 IST, taskbar) from one approved SLSA verifier download-and-verify command:

```text
STOP_A8_SLSA_VERIFICATION
STAGE=VERIFY_VERIFIER_SHA256
REASON=A8_VERIFIER_BINARY_HASH_MISMATCH
A8_CLOUD_MUTATIONS=NONE
A8_BUILD_RETRY=PROHIBITED
```

**Decision:** Security guard correctly blocked execution of untrusted/mismatching binary. No verifier invocation or cryptographic result was obtained. No indication new OLDX image is invalid. The previous A8 remote Cloud Build SUCCESS/approved full SHA and immutable digest/5 envelope signature fields are **consumed and preserved**. Do not rerun Cloud Build, change image/Registry/IAM, delete provenance receipt, retry the verifier blindly, or lower expected hash.

**Independent official upstream evidence** reread from `https://api.github.com/repos/slsa-framework/slsa-verifier/releases/tags/v2.7.1` through connected GitHub on this turn (not an inferred download): exactly `slsa-verifier-windows-amd64.exe`, size `33884672` bytes, `sha256:1d8f61ad747ecc3d375d2a563cebf2991748b7da1a9bda9a500804c3c499e3c0`; original download URL `https://github.com/slsa-framework/slsa-verifier/releases/download/v2.7.1/slsa-verifier-windows-amd64.exe`. The expected hash in previous command was correct according to current GitHub release metadata. Mismatch is LOCAL FILE INTEGRITY/TRANSPORT problem until diagnosed, not a known compromise. Earlier progress screenshots showed `Invoke-WebRequest` transfer increments.

## Next one strictly local read-only diagnosis (prepared, NOT run)

Read the exact previously downloaded `%TEMP%\oldx-slsa-verifier-v2.7.1-windows-amd64.exe`: size, SHA256, and two-byte PE `MZ` header. Do **not** execute, delete, rename, resume or redownload automatically. Do not output binary contents or local secrets. Official size and hash are fixed as above.

```powershell
& {
  try {
    $path = Join-Path $env:TEMP 'oldx-slsa-verifier-v2.7.1-windows-amd64.exe'
    $expectedSize = 33884672
    $expectedHash = '1d8f61ad747ecc3d375d2a563cebf2991748b7da1a9bda9a500804c3c499e3c0'
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
      throw 'A8_VERIFIER_LOCAL_FILE_NOT_FOUND'
    }
    $f = Get-Item -LiteralPath $path -ErrorAction Stop
    $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant()
    $stream = [System.IO.File]::OpenRead($path)
    try {
      $a = $stream.ReadByte()
      $b = $stream.ReadByte()
    } finally {
      $stream.Dispose()
    }
    "A8_LOCAL_FILE_SIZE_BYTES=$($f.Length)"
    "A8_OFFICIAL_FILE_SIZE_BYTES=$expectedSize"
    "A8_SIZE_MATCH=$($f.Length -eq $expectedSize)"
    "A8_LOCAL_SHA256=$hash"
    "A8_OFFICIAL_SHA256_MATCH=$($hash -ceq $expectedHash)"
    "A8_FILE_MZ_HEADER=$($a -eq 77 -and $b -eq 90)"
    'A8_VERIFIER_EXECUTION=NOT_STARTED'
    'A8_LOCAL_FILE_CHANGE=NONE'
    'A8_CLOUD_MUTATIONS=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  } catch {
    'STOP_A8_LOCAL_VERIFIER_FILE_DIAGNOSTIC'
    'A8_VERIFIER_FILE_STATE=UNVERIFIED'
    'A8_LOCAL_FILE_CHANGE=NONE'
    'A8_CLOUD_MUTATIONS=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  }
}
```

Interpretation: size shorter than 33,884,672 bytes suggests partial download; HTML/redirect response likely non-MZ header. Same length but different SHA256 indicates content mismatch, and execution remains blocked regardless of extension/header. If size/hash both match a future read, only then re-evaluate the verification action—but **do not replay the old one-shot PowerShell script**, since its first-run behavior/output log may have changed. Any error STOP, no cloud action. Plan a new isolated temp destination and strict hash guard for an alternate transfer only after observing the result; do not substitute a random installer or skip SHA256.

Still pending A8: **independent** signed provenance verification and new-image-specific vulnerability/runtime assessment; G4 and G8 open. Step04 HOLD, production NO_GO.
