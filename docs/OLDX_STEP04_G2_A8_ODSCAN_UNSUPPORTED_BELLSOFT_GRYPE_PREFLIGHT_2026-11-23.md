# OLDX Step04 G2 A8 — unsupported BellSoft On-Demand scan, alternate Grype preflight

Actual owner's Cloud Shell local-log diagnostic screenshot 23 Nov 2026 ~00:35 IST:
```text
A8_MARKER_PRESENT=True
A8_PRIVATE_LOG_READ=PASS
A8_OPERATION_COUNT=0
A8_ERROR_CATEGORIES=UNCLASSIFIED
A8_DIAGNOSTIC=Locally extracting packages and versions from remote container image...
A8_DIAGNOSTIC=Failed.
A8_DIAGNOSTIC=ERROR: (gcloud.artifacts.docker.images.scan) Extraction failed: operating system BellSoft Hardened Containers is not supported for On-Demand Scanning
A8_NEW_SCAN_STARTED_BY_CHECK=NO
A8_CLOUD_CHANGES=NONE
A8_SCAN_RETRY=PROHIBITED
```

Root cause is Google's unsupported BellSoft Hardened Containers OS/image analysis path. Not an image vulnerability finding, not 0 CVEs, and not remedied by re-enabling APIs. No operation ID in the private log, though nonappearance alone cannot prove remote absence or zero bill. Preserve the one-attempt marker and private log and do not replay gcloud on-demand scan. The original unique Cloud Build image and signed provenance have passed (including commit materials), but this new digest STILL LACKS A VULNERABILITY SCAN. No cloud resource changed by this local log-only diagnostic.

Approved alternative for the one-new-image scan is Anchore Grype: historical older LOCAL BellSoft-derived image under WSL successfully had a single frozen Grype scan (1 CRITICAL, 5 HIGH, 12 MEDIUM, 2 LOW), which is NOT a scan of the new image. Anchore supports scanning a remote registry image without Docker daemon, using Docker-config registry credential helpers. Confirm current binary and registry auth readiness before any download or execution; not all hardened OS distro vulnerability feeds are equivalent, and results need coverage and DB-date qualification. Do not rebuild/reupload the image, make IAM/billing/Cloud Run changes, or re-run consumed Grype on old image.

Exact new immutable A8 image: asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc.

NEXT ONE Cloud Shell Linux local-only preflight, prepared and NOT EXECUTED: checks installed Grype/Syft/credential helpers, existence of Docker config (not its content), and HOME filesystem free MiB. No cloud API, new scan, download, token, file mutation. Use same Cloud Shell, no repeat of old auth or scan. Output is safe to screenshot.

```bash
(
  if [ "$(uname -s)" != Linux ]; then
    echo A8_STOP_NOT_LINUX; exit 1
  fi
  for tool in grype syft docker-credential-gcloud docker-credential-gcr curl tar; do
    if command -v "$tool" >/dev/null 2>&1; then
      printf 'A8_TOOL_%s=AVAILABLE\n' "$tool"
    else
      printf 'A8_TOOL_%s=ABSENT\n' "$tool"
    fi
  done
  if [ -f "$HOME/.docker/config.json" ]; then
    echo A8_DOCKER_AUTH_CONFIG=EXISTS
  else
    echo A8_DOCKER_AUTH_CONFIG=ABSENT
  fi
  free_kb="$(df -Pk "$HOME" | awk 'NR==2 {print $4}')"
  echo "A8_HOME_FS_FREE_MIB=$((free_kb/1024))"
  echo A8_GOOGLE_ON_DEMAND_SCANNER=UNSUPPORTED_BELLSOFT_OS
  echo A8_NEW_GRYPE_SCAN=NOT_STARTED
  echo A8_CLOUD_MUTATIONS=NONE
  echo A8_GOOGLE_SCAN_RETRY=PROHIBITED
)
```

If Grype is installed, plan one exact digest-bound Grype registry image scan with read-only credentials and private JSON receipt. If absent, prefer official checksum-pinned Grype install in Cloud Shell or reuse the user's historical WSL Grype; first check disk and helper availability. Do not assume the old WSL scanner binary or DB exists in Cloud Shell. Don't claim zero vulnerabilities from unsupported scanner.

Official references: https://oss.anchore.com/docs/reference/grype/cli/ ; https://oss.anchore.com/docs/guides/private-registries/ ; https://docs.cloud.google.com/artifact-registry/docs/docker/authentication .

Pending: new-image vulnerability CVE findings and fixability, focused runtime/default-DB guard, G4 cross-DB/invoker, G8 total costs and owner launch decision. STEP04 HOLD / PRODUCTION NO_GO.