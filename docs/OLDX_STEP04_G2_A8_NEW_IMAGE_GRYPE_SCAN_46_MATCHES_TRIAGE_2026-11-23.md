# OLDX Step04 G2 A8 — exact new-image Grype scan COMPLETE; severe package/fix triage next

## Actual owner Cloud Shell screenshot — 23 November 2026 ~20:20 IST

The prior **ONE** checksum-pinned source script from immutable commit `4143923068933523bb62a16cb16eff997431d736` was successfully fetched and executed in Google Cloud Shell `oldx-staging`. The scanner was **Grype v0.122.1** whose official release archive SHA256 was verified. It scanned exactly the *new private immutable A8 image* `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`, **not** the earlier different BellSoft local image.

Observed bottom markers (source: actual screenshot):

```text
/tmp/oldx-a8-grype-source-2506826f.sh: OK
A8_GRYPE_NEW_RELEASE=v0.122.1
A8_DOWNLOAD_TO_TMP_ONLY=YES
A8_OFFICIAL_GRYPE_ARCHIVE_SHA256=PASS
A8_NEW_DIGEST_GRYPE_ATTEMPT=STARTED_ONCE
A8_IMAGE_SOURCE=PRIVATE_REGISTRY_IMMUTABLE_DIGEST
A8_GRYPE_SCAN_COMMAND_EXIT_CODE=0
A8_GRYPE_REPORT_SCHEMA=PASS
A8_GRYPE_SOURCE_IMAGE_REFERENCE_MATCH=True
A8_GRYPE_MATCH_TOTAL=46
A8_GRYPE_CRITICAL=1
A8_GRYPE_HIGH=23
A8_GRYPE_MEDIUM=19
A8_GRYPE_LOW=3
A8_GRYPE_NEGLIGIBLE=0
A8_GRYPE_UNKNOWN=0
A8_GRYPE_SEVERE_UNIQUE_IDS=15
A8_GRYPE_DB_BUILT=UNREPORTED
A8_GRYPE_REPORT_SHA256=d5dab942824a3bf48c2680e879699e51af7a30142e4e23a52e13493de5e60783
A8_VULNERABILITY_TRIAGE=REQUIRED_NOT_AUTOMATIC_PASS
A8_PRIVATE_FULL_REPORT=HOME_COMPRESSED_SAVED
A8_NEW_IMAGE_SCAN=ONE_COMPLETED_REPORT
A8_CLOUD_WRITES=NONE
A8_BUILD_AND_SLSA_RERUN=NONE
A8_STEP04=HOLD_PENDING_FINDINGS_AND_RUNTIME
```

**Important:** 46 are Grype *package-vulnerability matches*, **not 46 distinct CVEs**. Among 24 CRITICAL/HIGH matches, 15 unique severe IDs. The Grype DB build date **was NOT reported by the initial summarizer**; scanner advisory coverage for BellSoft Hardened Containers and vendor fixability remain to be independently evaluated. A completed scan is NOT security clearance. Never conflate with old image's historical 1 CRITICAL / 5 HIGH results, nor interpret higher counts as newly introduced CVEs without comparable DB/config/image. Prior SLSA/build/source SHA/digest all PASS and consumed, never repeat. Google on-demand scanner unsupported BellSoft OS, first attempted operation failed with durable marker, do not retry.

**Full private exact report** was saved on Cloud Shell HOME as `$HOME/oldx-a8-grype-new-digest-2506826f.json.gz`. The uncompressed report was SHA256 `d5dab942824a3bf48c2680e879699e51af7a30142e4e23a52e13493de5e60783` on initial scan. DO NOT upload full report to public GitHub or reveal auth/config. HOME capacity had 39MiB free before the scan; compressed backup reported SAVED. TMP still holds raw report until ephemeral reset; do not delete markers or rerun scan even if TMP gone.

## Next: ONE local-only triage of ALREADY SAVED gzip — PREPARED NOT EXECUTED

- Script: [`scripts/step04-a8-existing-grype-triage-readonly.py`](../scripts/step04-a8-existing-grype-triage-readonly.py), first-containing immutable commit `cc48e23a0bfd74fc8c0e845faab7246e92672221`.
- Exact Git blob `7f91cfcc5583f631879879b59ee22aca29ef9d67` and script SHA256 `7a8df6c7c56a21897914e647482081524d5cd80aa143e504e8886de5b367b845` (**locally compiled with Python, exact blob identity compared with GitHub source**).
- It reads ONLY the gzip report from owner Cloud Shell HOME. Confirms SHA256 of **decompressed original report** equals actual scan receipt; checks the exact approved image reference and expected 46-match/24-severe/15-unique counts; then prints up to 24 CRITICAL/HIGH records as sanitized severity|CVE|package|installed-version|fix-state|up-to-2-fix-versions, severity summary and distro. No token, private JSON, cloud access, image scan, DB update, build, SLSA verifier, IAM/API/Registry/Firebase/Cloud Run or billing changes.
- Fix-state strings are scanner database hints only. In particular `FIXED` means upstream/vendor declares a fix version available, **not that new image already contains fix**. `NOT-FIXED` or missing status are not proof never fixable. DB freshness/coverage still needs later evaluation.

**Exactly one short owner command to execute in SAME Linux Google Cloud Shell:**

```bash
(
  set -e
  p='/tmp/oldx-a8-grype-triage-source-2506826f.py'
  if [ -e "$p" ]; then echo 'STOP_A8_TRIAGE_SCRIPT_PATH_ALREADY_USED'; exit 1; fi
  curl --fail --location --silent --show-error --retry 0 --connect-timeout 15 --max-time 60 \
    'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/cc48e23a0bfd74fc8c0e845faab7246e92672221/scripts/step04-a8-existing-grype-triage-readonly.py' -o "$p"
  echo '7a8df6c7c56a21897914e647482081524d5cd80aa143e504e8886de5b367b845  /tmp/oldx-a8-grype-triage-source-2506826f.py' | sha256sum -c -
  python3 "$p"
)
```

This is a local report read and will not start another scan. If `STOP`, diagnose the exact symptom rather than replay or deleting files. Share **only sanitized terminal screenshot** of its outputs. After reading the affected package & fix versions, group the 15 severe CVE IDs by actual fixability and runtime reachability, compare official vendor advisories where applicable; propose least-rebuild mitigation and owner risk acceptance plan. New image runtime/nonroot/default DB guard, G4 cross database/effective invoker, G8 gross cost and final owner release decision still OPEN.

**Status:** `A8_ONE_NEW_DIGEST_GRYPE_SCAN=COMPLETE_WITH_46_MATCHES`, `A8_SIGNED_PROVENANCE=PASS`, `A8_SEVERE_FINDINGS=TRIAGE_REQUIRED`, `STEP04=HOLD`, `PRODUCTION=NO_GO`.
