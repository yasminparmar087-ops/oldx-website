# OLDX Step04 G2 A8 — scanner capability PASS; one exact image scan from Linux Cloud Shell

## Actual owner screenshot 23 November 2026 ~00:27 IST (Windows PowerShell)
```text
A8_ON_DEMAND_SCANNING_API_ENABLED=True
A8_AUTO_SCANNING_API_ENABLED=False
A8_WINDOWS_GRYPE_INSTALLED=False
A8_NEW_SCAN_STARTED=NO
A8_APIS_CHANGED=NONE
A8_BUILD_AND_VERIFIER_RERUN=NONE
```

Conclusions: On-Demand Scanning API is ALREADY enabled in `oldx-staging`; automatic scanning is disabled, and there is no Windows Grype executable in PATH. Earlier read-only Artifact Analysis metadata found 0 scan discovery entries, i.e., NO EXISTING COVERAGE, not zero vulnerabilities. Prior owner granted one *new-image-specific* verification scan within A8 soft ₹100 spend planning envelope; do not request another redundant approval for this exact bounded single on-demand scan. Published scan list price US$0.26/image before possible taxes/other project charges; the budget is not a billing-enforced cap. Do not enable automatic scanning or any API, change IAM, rebuild or upload, touch Cloud Run/Firebase/billing.

### Platform guard: Google explicitly does NOT support on-demand scans on Windows

Official Google scan OS packages guide states On-Demand Scanning is supported on Linux and macOS, **NOT Windows** even for remote Artifact Registry targets. Therefore the next command MUST run in **Google Cloud Shell (Linux), NOT Windows PowerShell / CMD**. Cloud Shell is preferred to installing Grype or another scanner. Use owner Google account `yasminparmar087@gmail.com`; if Cloud Shell's active identity differs, STOP and reconcile sign-in separately, do not grant more roles. Cloud Shell HOME is persistent across normal resets, and small marker/private text log can be retained there.

### Exact owner-run ONE scan operation — PREPARED, NOT EXECUTED

Image is the already approved unique private Artifact Registry immutable digest:
`asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`.

`gcloud artifacts docker images scan IMAGE --remote --location=asia --async` officially supports exact digest and starts ONE on-demand paid scan; `asia` is the scan multi-region (not `asia-south1`, which is the Registry region). `--async` returns scan operation ID, **NOT scan vulnerability results**. It may initiate remote extraction/analysis and bill for scan. Command creates a durable exclusive marker BEFORE submission and prints a sanitized operation identifier (if present), stores original response PRIVATELY, DOES NOT automatically retry, query results, build, deploy, enable APIs or modify IAM/Firebase/Cloud Run. Any nonzero/unknown scan must be reconciled with the original log and operation before ANY new paid scan. `--quiet` suppresses interactive prompts; marker is **never deleted**.

```bash
(
  set -uo pipefail
  umask 077
  account='yasminparmar087@gmail.com'
  image='asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'
  marker="$HOME/.oldx-a8-on-demand-scan-2506826f-attempted"
  log="$HOME/oldx-a8-on-demand-scan-2506826f.log"

  if [ "$(uname -s)" != 'Linux' ]; then
    echo 'STOP_A8_SCAN_REQUIRES_CLOUD_SHELL_LINUX'; exit 1
  fi
  active="$(gcloud auth list --filter='status:ACTIVE' --format='value(account)' --quiet 2>/dev/null | head -n 1)"
  if [ "$active" != "$account" ]; then
    echo 'STOP_A8_SCAN_WRONG_ACTIVE_ACCOUNT'; exit 1
  fi
  if [ -e "$marker" ] || [ -e "$log" ]; then
    echo 'STOP_A8_SCAN_ALREADY_ATTEMPTED_NO_RETRY'; exit 1
  fi
  if ! mkdir -m 700 "$marker" 2>/dev/null; then
    echo 'STOP_A8_SCAN_MARKER_CREATE_FAILED'; exit 1
  fi
  echo 'A8_SCAN_ONE_ATTEMPT_MARKER=CREATED'
  echo 'A8_SCAN_TARGET=APPROVED_IMMUTABLE_DIGEST'
  if gcloud artifacts docker images scan "$image" \
      --remote --location=asia --async \
      --project=oldx-staging --account="$account" \
      --format=json --quiet >"$log" 2>&1; then
    echo 'A8_SCAN_COMMAND_EXIT_CODE=0'
    operation="$(grep -Eo 'projects/oldx-staging/locations/asia/operations/[A-Za-z0-9-]+' "$log" | head -n 1 || true)"
    if [ -n "$operation" ]; then
      echo "A8_SCAN_OPERATION=$operation"
    else
      echo 'A8_SCAN_OPERATION=NOT_EXTRACTED_REVIEW_PRIVATE_LOG'
    fi
    echo 'A8_SCAN_RESULT=AWAIT_OPERATION_READ'
  else
    echo 'STOP_A8_SCAN_SUBMIT_FAILED_OR_AMBIGUOUS'
    echo 'A8_SCAN_STATE=RECONCILE_BEFORE_ANY_NEW_WRITE'
  fi
  echo 'A8_PRIVATE_SCAN_LOG=SAVED_IN_CLOUD_SHELL_HOME'
  echo 'A8_BUILD_OR_VERIFIER_RERUN=NONE'
  echo 'A8_SCAN_RETRY=PROHIBITED'
)
```

**After command:** If it prints `A8_SCAN_OPERATION=projects/oldx-staging/locations/asia/operations/...`, use an independent READ-ONLY `gcloud artifacts docker images get-operation` for that exact operation. When done, the returned `response.scan` identifies one exact scan. Then use one `gcloud artifacts docker images list-vulnerabilities SCAN_NAME --location=asia` and privately save result/triage severe findings. Google's on-demand results available 48 hours; save findings in a private receipt promptly. Do not interpret async success as scan completion or clean image. No repeat build or SLSA verifier.

Documentation checked 23 Nov 2026: https://docs.cloud.google.com/artifact-analysis/docs/scan-os-on-demand (explicit Windows unsupported, Linux/macOS supported), https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/docker/images/scan (`--remote`, `--async`, `--location=asia`), https://cloud.google.com/artifact-analysis/pricing (US$0.26 per scan).

Step04 HOLD, production NO_GO; pending scan and detailed CVE disposition, focused runtime/default DB guard, G4 cross-database/effective invoker and G8 gross spend / rollback gate.