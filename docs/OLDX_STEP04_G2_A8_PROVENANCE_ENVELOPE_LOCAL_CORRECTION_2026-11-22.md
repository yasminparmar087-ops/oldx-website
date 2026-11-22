# OLDX Step04 G2 A8 — provenance metadata 2 entries; signature field path correction

Owner screenshot shows the exact immutable A8 image digest VERIFIED_AT_READ, private JSON saved at `C:\Users\Yasmin Parmar\oldx-a8-provenance-2506826f.json`, `A8_PROVENANCE_ENTRY_COUNT=2`, `A8_SIGNATURE_FIELDS_COUNT=0`, `A8_SIGNATURE_CRYPTOGRAPHIC_VERIFICATION=NOT_YET_DONE`, `A8_IMAGE_SPECIFIC_SECURITY_SCAN=NOT_YET_DONE`, no cloud writes and build retry prohibited. This is **not** a failed cryptographic verification, and cannot establish an unsigned image.

**Important code-path defect in the previous source-only diagnostic:** It counted `$item.build.inTotoSlsaProvenanceV1.envelope.signatures`, which does not match the officially documented response shape. Google's current Cloud Build provenance guide locates signed material at `.provenance_summary.provenance[].envelope.signatures`, whereas the predicate lives under `.build.intotoStatement.predicateType`.

Authoritative: https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance (view provenance example and validate provenance section; current guide uses `.envelope.signatures`). Exact image is `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`. Build ID `2506826f-ab8d-41a6-a60c-3f2ea3e74bd5`, pinned Git SHA `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`. No new build or scan justified by the mistaken count.

## Next: one purely local read-only shape reconciliation — PREPARED NOT EXECUTED

PowerShell 5.1, `PS ...>` prompt. Reads existing private receipt only; does NOT print or upload raw JSON, signature/payload/key material or private provenance metadata. It checks exact previously observed image identity and two entries, then reports per-entry SLSA predicate category, corrected envelope-signature field count, payload-presence boolean and resource-URI match. These are *shape observations only*, **never** cryptographic verification. On any STOP do not rerun build or delete receipt.

```powershell
& {
  try {
    $path = Join-Path $env:USERPROFILE 'oldx-a8-provenance-2506826f.json'
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
      throw 'A8_PRIVATE_RECEIPT_NOT_FOUND'
    }
    $data = Get-Content -LiteralPath $path -Raw -Encoding UTF8 |
      ConvertFrom-Json -ErrorAction Stop

    $digest = 'sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'
    $image = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@' + $digest
    $seenDigest = [string]$data.image_summary.digest
    $seenFull = [string]$data.image_summary.fully_qualified_digest
    if (($seenDigest -and $seenDigest -cne $digest) -or
        ($seenFull -and $seenFull -cne $image) -or
        (-not $seenDigest -and -not $seenFull)) {
      throw 'A8_LOCAL_DIGEST_MISMATCH'
    }

    $entries = @($data.provenance_summary.provenance |
      Where-Object { $null -ne $_ })
    if ($entries.Count -ne 2) {
      throw 'A8_ENTRY_COUNT_CHANGED'
    }
    'A8_LOCAL_EXACT_DIGEST=PASS'
    "A8_ENTRY_COUNT=$($entries.Count)"

    $total = 0
    for ($i = 0; $i -lt $entries.Count; $i++) {
      $e = $entries[$i]
      $sigs = @($e.envelope.signatures |
        Where-Object { $_ -and -not [string]::IsNullOrWhiteSpace([string]$_.sig) })
      $total += $sigs.Count
      $type = [string]$e.build.intotoStatement.predicateType
      $version = if ($type -ceq 'https://slsa.dev/provenance/v1') {
        'SLSA_V1'
      } elseif ($type -ceq 'https://slsa.dev/provenance/v0.1') {
        'SLSA_V0_1'
      } else {
        'UNKNOWN'
      }
      $payloadPresent = -not [string]::IsNullOrWhiteSpace(
        [string]$e.envelope.payload)
      $resourceMatches = ([string]$e.resourceUri -ceq "https://$image" -or
                          [string]$e.resourceUri -ceq $image)

      "A8_ENTRY_$($i + 1)_TYPE=$version"
      "A8_ENTRY_$($i + 1)_ENVELOPE_SIGNATURE_FIELDS=$($sigs.Count)"
      "A8_ENTRY_$($i + 1)_PAYLOAD_PRESENT=$payloadPresent"
      "A8_ENTRY_$($i + 1)_RESOURCE_URI_MATCH=$resourceMatches"
    }
    "A8_TOTAL_ENVELOPE_SIGNATURE_FIELDS=$total"
    'A8_CRYPTOGRAPHIC_SIGNATURE_VERIFICATION=NOT_DONE'
    'A8_NEW_IMAGE_SECURITY_SCAN=NOT_DONE'
    'A8_CLOUD_READS_OR_WRITES=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^A8_[A-Z_]+$') {
      $reason = 'A8_LOCAL_JSON_CHECK_FAILED'
    }
    'STOP_A8_LOCAL_PROVENANCE_SHAPE_CHECK'
    "REASON=$reason"
    'A8_CLOUD_READS_OR_WRITES=NONE'
    'A8_BUILD_RETRY=PROHIBITED'
  }
}
```

After the owner screenshot, proceed to **actual** `slsa-verifier verify-image` with an independently pinned verifier/version and expected exact image digest, GitHub URI and GoogleHostedWorker builder. Google guide explicitly requires independent SLSA verification, not just signature field presence. Later do one new-image-specific vulnerability scan and focused runtime (new DB guard), within existing A8 verification consent. Until then: G2 HOLD; Step04 HOLD; Production NO_GO.