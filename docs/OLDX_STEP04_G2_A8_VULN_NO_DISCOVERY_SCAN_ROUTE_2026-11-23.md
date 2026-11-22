# OLDX Step04 G2 A8: no existing vulnerability metadata; scanner capability preflight

Actual 23 Nov 2026 ~00:23 IST owner screenshot of new immutable-image Artifact Registry metadata read:
```text
A8_VULN_TARGET_IMAGE_DIGEST=PASS
A8_VULN_METADATA_RECEIPT=PRIVATE_LOCAL_SAVED
A8_SCAN_DISCOVERY_ENTRIES=0
A8_SCAN_STATES=
A8_NEW_IMAGE_VULNERABILITIES=UNVERIFIED_OR_SCAN_NOT_READY
A8_NEW_SCAN_STARTED_BY_COMMAND=NO
A8_CLOUD_MUTATIONS=NONE
A8_BUILD_OR_VERIFIER_RERUN=NONE
```

Interpretation: no existing completed scan discovered for the new image. Zero discovery entries is NOT zero vulnerabilities. Full private metadata receipt retained on owner's Windows computer. All A8 build/provenance/digest/source and official checksum-pinned SLSA verifier PASS are consumed; never repeat.

Next ONE PowerShell strictly read-only: list enabled services in project oldx-staging to check ondemandscanning.googleapis.com and containerscanning.googleapis.com; detect already-installed Windows Grype. Prints booleans only. No scan/API enable/IAM/Registry/Firebase/Cloud Run/billing changes.

```powershell
& {
  try {
    $raw = @(& gcloud.cmd services list --enabled '--project=oldx-staging' '--account=yasminparmar087@gmail.com' '--format=value(config.name)' --quiet 2>$null)
    if ($LASTEXITCODE -ne 0 -or $raw.Count -eq 0) { throw 'A8_ENABLED_SERVICES_READ_FAILED' }
    $services = @($raw | ForEach-Object { ([string]$_).Trim() })
    $onDemand = $services -contains 'ondemandscanning.googleapis.com'
    $autoScan = $services -contains 'containerscanning.googleapis.com'
    $winGrype = $null -ne (Get-Command grype.exe -ErrorAction SilentlyContinue)
    "A8_ON_DEMAND_SCANNING_API_ENABLED=$onDemand"
    "A8_AUTO_SCANNING_API_ENABLED=$autoScan"
    "A8_WINDOWS_GRYPE_INSTALLED=$winGrype"
    'A8_NEW_SCAN_STARTED=NO'
    'A8_APIS_CHANGED=NONE'
    'A8_BUILD_AND_VERIFIER_RERUN=NONE'
  } catch {
    'STOP_A8_SCANNER_CAPABILITY_PREFLIGHT'
    'A8_SCAN_API_STATE=UNVERIFIED'
    'A8_CLOUD_CHANGES=NONE'
  }
}
```

If On-Demand Scanning API is already enabled, owner-approved single new-image-specific scan may be prepared under A8 verification scope without API enable, with no retry and expected published list price US$0.26 per image (soft ₹100 planning limit is not a hard cost ceiling). Scan results may expire in 48h. If API is disabled, do not auto-enable; assess an already-available local or WSL Grype route and ask for separate authority before any API switch. Automatic Container Scanning API enables future scans project-wide; never switch it on as an expedient workaround.

Exact approved image: asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc.

After new image scan, focused runtime/default DB, G4 other DB/invoker and G8 gross-cost STOP remain open. Step04 HOLD, production NO_GO.

Sources: https://docs.cloud.google.com/artifact-analysis/docs/scan-os-on-demand ; https://cloud.google.com/artifact-analysis/pricing ; https://oss.anchore.com/docs/guides/private-registries/