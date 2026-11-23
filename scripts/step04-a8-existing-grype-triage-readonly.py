#!/usr/bin/env python3
"""OLDX Step04 A8: read an already-completed PRIVATE Grype report; no scan/network/writes."""
from collections import Counter
from pathlib import Path
import gzip
import hashlib
import json
import re
import sys

report = Path.home() / "oldx-a8-grype-new-digest-2506826f.json.gz"
expected_hash = "d5dab942824a3bf48c2680e879699e51af7a30142e4e23a52e13493de5e60783"
expected_image = ("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
                  "oldx-step04-g2-cloudbuild-20261122-a1@"
                  "sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc")


def stop(reason):
    print("STOP_A8_PRIVATE_GRYPE_TRIAGE")
    print("REASON=" + reason)
    print("A8_GRYPE_RERUN=NONE")
    print("A8_CLOUD_ACTIONS=NONE")
    sys.exit(1)


def safe(value, n=70):
    return re.sub(r"[^A-Za-z0-9_.+:/@-]", "_", str(value or "UNREPORTED"))[:n]


if not report.is_file():
    stop("A8_PRIVATE_COMPRESSED_REPORT_MISSING")
try:
    with gzip.open(report, "rb") as handle:
        raw = handle.read()
    actual_hash = hashlib.sha256(raw).hexdigest()
    if actual_hash != expected_hash:
        stop("A8_GRYPE_REPORT_SHA256_MISMATCH")
    data = json.loads(raw)
    target = ((data.get("source") or {}).get("target") or {})
    if expected_image not in str(target.get("userInput", "")):
        stop("A8_GRYPE_IMAGE_REFERENCE_MISMATCH")
    matches = data.get("matches")
    if not isinstance(matches, list):
        stop("A8_GRYPE_REPORT_MATCHES_MISSING")
    counts = Counter(str((m.get("vulnerability") or {}).get("severity", "UNKNOWN")).upper()
                     for m in matches)
    expected_counts = {"CRITICAL": 1, "HIGH": 23, "MEDIUM": 19, "LOW": 3}
    if len(matches) != 46 or any(counts[k] != v for k, v in expected_counts.items()):
        stop("A8_GRYPE_COUNTS_DIFFER_FROM_SCREENSHOT")
except (OSError, EOFError, ValueError, TypeError, KeyError, AttributeError):
    stop("A8_PRIVATE_REPORT_CANNOT_BE_PARSED")

severe = [m for m in matches if str((m.get("vulnerability") or {})
          .get("severity", "")).upper() in ("CRITICAL", "HIGH")]
cves = sorted({str((m.get("vulnerability") or {}).get("id", ""))
               for m in severe})
if len(severe) != 24 or len(cves) != 15:
    stop("A8_SEVERE_COUNT_NOT_AS_EXPECTED")

print("A8_LOCAL_COMPRESSED_REPORT=READ_ONLY")
print("A8_REPORT_RAW_SHA256=PASS")
print("A8_TARGET_IMMUTABLE_DIGEST=PASS")
print("A8_GRYPE_TOTAL_MATCHES=46")
print("A8_GRYPE_CRITICAL=1")
print("A8_GRYPE_HIGH=23")
print("A8_GRYPE_MEDIUM=19")
print("A8_GRYPE_LOW=3")
print("A8_SEVERE_UNIQUE_CVE_COUNT=15")
distro = data.get("distro") or {}
print("A8_GRYPE_DETECTED_DISTRO=" + safe(distro.get("name")))
print("A8_GRYPE_DETECTED_DISTRO_VERSION=" + safe(distro.get("version")))
fix_counts = Counter()
for match in sorted(severe,
                    key=lambda m: (0 if (m.get("vulnerability") or {})
                                     .get("severity", "").upper() == "CRITICAL" else 1,
                                   str((m.get("vulnerability") or {}).get("id", "")),
                                   str((m.get("artifact") or {}).get("name", "")))):
    vuln = match.get("vulnerability") or {}
    artifact = match.get("artifact") or {}
    fix = vuln.get("fix") or {}
    fix_state = safe(fix.get("state"), 30).upper()
    fix_versions = fix.get("versions") or []
    if not isinstance(fix_versions, list):
        fix_versions = []
    fix_counts[fix_state] += 1
    print("A8_SEVERE_MATCH=" + "|".join([
        safe(vuln.get("severity"), 15).upper(),
        safe(vuln.get("id"), 40),
        safe(artifact.get("name"), 55),
        safe(artifact.get("version"), 35),
        fix_state,
        safe(",".join(str(v) for v in fix_versions[:2]) if fix_versions else "UNREPORTED", 65)
    ]))
for status, amount in sorted(fix_counts.items()):
    print("A8_SEVERE_FIX_STATE_" + safe(status, 30) + "=" + str(amount))
print("A8_VENDOR_CVE_COVERAGE=REQUIRES_SEPARATE_CONFIRMATION")
print("A8_PRIVATE_FULL_JSON=NOT_EXPORTED")
print("A8_NO_SCAN_OR_CLOUD_ACTIONS=TRUE")
print("A8_STEP04=HOLD")
