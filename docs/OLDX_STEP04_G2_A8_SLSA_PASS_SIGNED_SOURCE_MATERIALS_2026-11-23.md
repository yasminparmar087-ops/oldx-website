# OLDX Step04 G2 A8 — SLSA verifier success text confirmed, local signed source commit check

**Actual owner screenshot 23 Nov 2026 00:16 IST:** Existing private SLSA verifier log (no new network actions) returned:
```text
A8_LOG_VERIFIED_SLSA_PATTERN=False
A8_LOG_SLSA_PASSED_PATTERN=True
A8_PRIOR_EXIT_ZERO_AND_PASS_TEXT=SUPPORTED
A8_VERIFIER_RERUN=NONE
A8_CLOUD_ACTIONS=NONE
```

Pair this with the previously actually observed official SHA256-matched slsa-verifier Windows v2.7.1 binary, exit code `0`, exact immutable new image `@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`, expected source `github.com/yasminparmar087-ops/oldx-website`, and trusted builder `https://cloudbuild.googleapis.com/GoogleHostedWorker`: **independent SLSA verifier PASS supported for digest/source-repo/builder under verifier's policy**. The previous `EXIT_ZERO_OUTPUT_REVIEW` was just a too-narrow success-text matcher, not a cryptographic failure. Preserve private verifier logfile, existing provenance JSON, and local one-shot marker. Never rerun verifier, resume, Cloud Build, or historical scans.

**Still not concluded:** the exact **40-hex Git commit** `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71` matched source in the Cloud Build API's declared and resolved Git source, but has not been independently compared to the **decoded signed envelope's** material digest. New image vulnerability scan and focused runtime/default DB checks, plus separate G4/G8 are open. Step04 HOLD / production NO_GO.

## Next: purely local signed SLSA v0.1 payload material comparison — PREPARED_NOT_RUN

The current official Google Cloud Build provenance documentation shows DSSE payload stored as URL-safe base64 in `provenance_summary.provenance[].envelope.payload`. The SLSA v0.1 specification defines `statement.predicate.materials[].uri` with `digest.sha1` for source commit, and `statement.subject[].digest.sha256` for the output. Only decode the ONE SLSA v0.1 entry from existing private local JSON; compare exact repo identity, 40-hex commit, output digest and GoogleHostedWorker builder ID. Print only booleans/counts, no raw payload, keys, signatures, or source. **Parsing is read-only, not a substitute for the earlier genuine slsa-verifier crypto check**. If material omitted or unexpected, report NOT FULLY PROVEN; no guesses or repeat build.

```powershell
& {
  try {
    $path = Join-Path $env:USERPROFILE 'oldx-a8-provenance-2506826f.json'
    $sha = '31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71'
    $digest = '6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
      throw 'A8_PRIVATE_PROVENANCE_MISSING'
    }
    $data = Get-Content -LiteralPath $path -Raw -Encoding UTF8 |
      ConvertFrom-Json -ErrorAction Stop
    if ([string]$data.image_summary.digest -cne "sha256:$digest") {
      throw 'A8_IMAGE_DIGEST_NOT_MATCHED'
    }
    $items = @($data.provenance_summary.provenance |
      Where-Object {
        $_ -and $_.build.intotoStatement.predicateType -ceq 'https://slsa.dev/provenance/v0.1'
      })
    if ($items.Count -ne 1) { throw 'A8_V01_ENTRY_NOT_UNIQUE' }

    $p = [string]$items[0].envelope.payload
    if ([string]::IsNullOrWhiteSpace($p)) { throw 'A8_SIGNED_PAYLOAD_MISSING' }
    $p = $p.Replace('-','+').Replace('_','/')
    $p = $p.PadRight(([int][Math]::Ceiling($p.Length / 4.0) * 4),'=')
    $statement = [System.Text.Encoding]::UTF8.GetString(
      [System.Convert]::FromBase64String($p)
    ) | ConvertFrom-Json -ErrorAction Stop
    if ([string]$statement.predicateType -cne 'https://slsa.dev/provenance/v0.1') {
      throw 'A8_PAYLOAD_TYPE_MISMATCH'
    }

    $materials = @($statement.predicate.materials |
      Where-Object { $null -ne $_ })
    $repoMaterials = @($materials | Where-Object {
      [string]$_.uri -match '^git\+https://github\.com/yasminparmar087-ops/oldx-website(\.git)?($|[@#])' -or
      [string]$_.uri -match '^https://github\.com/yasminparmar087-ops/oldx-website(\.git)?($|[@#])'
    })
    $exactSource = @($repoMaterials | Where-Object {
      [string]$_.digest.sha1 -ceq $sha
    }).Count -gt 0

    $subjects = @($statement.subject | Where-Object { $null -ne $_ })
    $exactImage = @($subjects | Where-Object {
      [string]$_.digest.sha256 -ceq $digest
    }).Count -gt 0
    $builder = [string]$statement.predicate.builder.id
    $builderRecognized = $builder -match '^https://cloudbuild\.googleapis\.com/GoogleHostedWorker($|@)'

    "A8_SIGNED_V01_SOURCE_MATERIAL_COUNT=$($repoMaterials.Count)"
    "A8_SIGNED_SOURCE_COMMIT_SHA_MATCH=$exactSource"
    "A8_SIGNED_SUBJECT_DIGEST_MATCH=$exactImage"
    "A8_SIGNED_BUILDER_ID_RECOGNIZED=$builderRecognized"
    if ($exactSource -and $exactImage -and $builderRecognized) {
      'A8_SIGNED_COMMIT_MATERIALS=CONSISTENT_WITH_APPROVED_BUILD'
    } else {
      'A8_SIGNED_COMMIT_MATERIALS=NOT_FULLY_PROVEN'
    }
    'A8_SIGNED_PAYLOAD_RAW=NOT_EXPORTED'
    'A8_CLOUD_ACTIONS=NONE'
    'A8_BUILD_OR_VERIFIER_RERUN=NONE'
  } catch {
    'STOP_A8_LOCAL_SIGNED_SOURCE_CHECK'
    'A8_SIGNED_COMMIT_MATERIALS=UNVERIFIED'
    'A8_CLOUD_ACTIONS=NONE'
    'A8_BUILD_OR_VERIFIER_RERUN=NONE'
  }
}
```

After owner runs, if all three matches are TRUE and the earlier independent SLSA verifier PASS is preserved, the signed source material consistency gate is supported with bounds. If any missing, inspect fields or use targeted shape report, never silently treat Build API SHA as signed provenance SHA. Remaining G2 new-image-specific CVE scan/runtime risk acceptance and G4/G8 STOP remain open. No Cloud Run deploy / Firebase / IAM / billing writes.

References: https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance ; https://slsa.dev/spec/v0.1/provenance ; https://docs.cloud.google.com/build/gcb-buildtypes/google-builder/v1