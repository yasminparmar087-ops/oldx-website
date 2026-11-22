# OLDX Step 04 G2 A8 — actual Cloud Build SUCCESS, immutable digest; next provenance read

Owner screenshot (22 Nov 2026 conversation; Windows taskbar date says 21 Nov) from one separate authenticated gcloud builds list/describe read:
```text
A8_BUILD_ID=2506826f-ab8d-41a6-a60c-3f2ea3e74bd5
A8_BUILD_STATUS=SUCCESS
A8_DECLARED_GIT_SOURCE=EXACT_SHA_MATCH
A8_RESOLVED_GIT_SHA=MATCH
A8_RESULT_IMAGE_DIGEST=sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc
A8_SIGNED_PROVENANCE=NOT_YET_INDEPENDENTLY_VERIFIED
A8_NEW_IMAGE_VULNERABILITY_SCAN=NOT_YET_VERIFIED
A8_READ_ONLY_CHECK_WRITES=NONE
A8_BUILD_RETRY=PROHIBITED
```

Exact immutable source commit: `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`; dedicated builder previously verified. Exact new private Registry image:
`asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`.

**Boundary**: SUCCESS + source SHA match + output digest are supported by observed Build API result, but not yet independently signed provenance, new-image security scan, runtime, G4 or G8. The one approved A8 build is CONSUMED, NO RETRIES, no marker deletion or new uploads. Earlier local npm-free scan is not a scan of this new artifact. STEP04=HOLD, PRODUCTION=NO_GO.

## One next owner-run, read-only exact digest provenance inspection — PREPARED, NOT EXECUTED

Google Cloud officially supports `gcloud artifacts docker images describe IMAGE@sha256:... --show-provenance --format=json`. The following block checks the returned image identity and stores a private JSON receipt to later run an independent SLSA verifier. It prints only sanitized counts, not signatures/tokens. No image scan, build, IAM, Registry write or Cloud Run deployment. A nonzero signature count is only metadata presence, NOT cryptographic verification. File in USERPROFILE should remain private; do not upload raw JSON to public GitHub.

```powershell
& {
  $stage = 'START'
  try {
    $digest = 'sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'
    $image = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@' + $digest
    $receipt = Join-Path $env:USERPROFILE 'oldx-a8-provenance-2506826f.json'
    $stage = 'LOCAL_FILE'
    if (Test-Path -LiteralPath $receipt) { throw 'A8_RECEIPT_ALREADY_EXISTS' }

    $stage = 'EXACT_IMAGE_PROVENANCE_READ'
    $argsList = @('artifacts','docker','images','describe',$image,
      '--project=oldx-staging','--account=yasminparmar087@gmail.com',
      '--show-provenance','--format=json','--quiet')
    $raw = & gcloud.cmd @argsList 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) {
      throw 'A8_PROVENANCE_READ_FAILED'
    }

    $stage = 'IMAGE_IDENTITY'
    $rawText = $raw | Out-String
    $data = $rawText | ConvertFrom-Json -ErrorAction Stop
    $reportedDigest = [string]$data.image_summary.digest
    $reportedFull = [string]$data.image_summary.fully_qualified_digest
    if (($reportedDigest -and $reportedDigest -cne $digest) -or
        ($reportedFull -and $reportedFull -cne $image) -or
        (-not $reportedDigest -and -not $reportedFull)) {
      throw 'A8_IMAGE_IDENTITY_MISMATCH'
    }
    'A8_REGISTRY_EXACT_DIGEST=VERIFIED_AT_READ'

    $stage = 'LOCAL_RECEIPT'
    $file = [System.IO.File]::Open($receipt,
      [System.IO.FileMode]::CreateNew,
      [System.IO.FileAccess]::Write,
      [System.IO.FileShare]::None)
    try {
      $bytes = [System.Text.Encoding]::UTF8.GetBytes($rawText)
      $file.Write($bytes,0,$bytes.Length)
    } finally { $file.Dispose() }
    'A8_PROVENANCE_LOCAL_RECEIPT=SAVED_PRIVATE'

    $items = @($data.provenance_summary.provenance |
      Where-Object { $null -ne $_ })
    "A8_PROVENANCE_ENTRY_COUNT=$($items.Count)"
    $signatureCount = 0
    foreach ($item in $items) {
      $signatureCount += @($item.build.inTotoSlsaProvenanceV1.envelope.signatures |
        Where-Object { $null -ne $_ }).Count
    }
    "A8_SIGNATURE_FIELDS_COUNT=$signatureCount"
    'A8_SIGNATURE_CRYPTOGRAPHIC_VERIFICATION=NOT_YET_DONE'
    'A8_IMAGE_SPECIFIC_SECURITY_SCAN=NOT_YET_DONE'
    'A8_CLOUD_WRITES=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^A8_[A-Z_]+$') {
      $reason = 'A8_UNEXPECTED_ERROR'
    }
    'STOP_A8_PROVENANCE_METADATA_CHECK'
    "STAGE=$stage"
    "REASON=$reason"
    'A8_CLOUD_WRITES=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  }
}
```

On `A8_REGISTRY_EXACT_DIGEST=VERIFIED_AT_READ`, provenance receipt saved and counts printed, proceed next to independent SLSA verifier with approved image SHA, GitHub source URI and GoogleHostedWorker builder. On any STOP, no automatic retry/build; diagnose exact stage. A new-image-specific vulnerability and runtime assessment remains outstanding under already approved A8 verification scope.

Official: https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance ; https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/docker/images/describe