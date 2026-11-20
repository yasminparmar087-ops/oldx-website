#!/usr/bin/env python3
"""Read-only integrity check of OLDX's EXISTING npm-free WSL journal and scan.

NEVER creates an image, scans, connects to Docker/Cloud or modifies evidence.
A PASS verifies internal local evidence consistency, NOT trustworthy builder
provenance, original artifact authenticity, patched CVEs or deployment approval.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from collections import Counter

ROOT = Path("/mnt/d/OLDX/G2/oldx-bellsoft-npmfree-20261120-a1")
SOURCE = "fcc96574b6388dc441a0b5d3eade48e79c7ebb24"
BASE_INDEX = "sha256:ef00ba8e634402e8dd3b374643fdbc178e876c7a312c9d55e4734efaa1e93d94"
BASE_AMD64 = "sha256:3862d478c2737d8386911b777d713e56a26e182f7c107e702be23a7b1cfe4799"
SCANNER_DB = "303ba44739343769e0e15bd0d50af62e142491b256bb533a8cfaf13ab00ca1b7"
IMAGE = "oldx-bellsoft-npmfree:20261120-a1"
COUNTS = {"CRITICAL": 1, "HIGH": 5, "MEDIUM": 12, "LOW": 2}
SEVERE = {
    "CVE-2019-1010022": ("CRITICAL", "glibc", "2.43.0-r14"),
    "CVE-2019-1010023": ("HIGH", "glibc", "2.43.0-r14"),
    "CVE-2026-0861": ("HIGH", "glibc", "2.43.0-r14"),
    "CVE-2026-19499": ("HIGH", "glibc", "2.43.0-r14"),
    "CVE-2026-84243": ("HIGH", "glibc", "2.43.0-r14"),
    "CVE-2026-119586": ("HIGH", "sqlite-libs", "3.54.1-r0"),
}
UNDICI_IDS = {"GHSA-2m5v-pch6-74hx", "GHSA-qrxm-fqhp-jwvm", "GHSA-xjj6-f33q-929c"}

class Stop(Exception):
    pass

def need(condition, reason):
    if not condition:
        raise Stop(reason)

def read_fixed(root, name, max_bytes):
    need(root.is_dir() and not root.is_symlink(), "LOCAL_ROOT_UNSAFE")
    file = root / name
    need(file.is_file() and not file.is_symlink(), "LOCAL_FILE_UNSAFE")
    descriptor = os.open(file, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        info = os.fstat(descriptor)
        need(stat.S_ISREG(info.st_mode) and 1 <= info.st_size <= max_bytes, "LOCAL_SIZE_INVALID")
        with os.fdopen(descriptor, "rb") as f:
            descriptor = None
            data = f.read(max_bytes + 1)
        need(len(data) <= max_bytes, "LOCAL_TOO_LARGE")
        return data
    finally:
        if descriptor is not None:
            os.close(descriptor)

def verify(root=ROOT):
    raw_summary = read_fixed(root, "summary.json", 128 * 1024)
    raw_scan = read_fixed(root, "new-image-grype-full.json", 32 * 1024 * 1024)
    try:
        summary = json.loads(raw_summary)
        report = json.loads(raw_scan)
    except (ValueError, UnicodeDecodeError) as exc:
        raise Stop("LOCAL_JSON_INVALID") from exc
    need(isinstance(summary, dict) and isinstance(report, dict), "LOCAL_JSON_SHAPE")
    need(summary.get("source_sha") == SOURCE and
         summary.get("base_index") == BASE_INDEX and
         summary.get("base_amd64_child") == BASE_AMD64 and
         summary.get("scanner_db_sha256") == SCANNER_DB and
         summary.get("planned_image") == IMAGE, "PINNED_IDENTITY_DRIFT")
    need(summary.get("stage") == "COMPLETE_REVIEW_REQUIRED" and
         summary.get("outcome") == "DONE_NOT_SECURITY_CLEARANCE" and
         summary.get("execution") == "one_new_image_only", "JOURNAL_NOT_COMPLETE")
    image_id = summary.get("image_id")
    need(isinstance(image_id, str) and
         re.fullmatch(r"sha256:[a-f0-9]{64}", image_id) is not None,
         "LOCAL_IMAGE_ID_INVALID")
    runtime = summary.get("runtime")
    need(isinstance(runtime, dict) and
         type(runtime.get("uid")) is int and runtime["uid"] > 0 and
         isinstance(runtime.get("node"), str) and
         runtime["node"].startswith("24.") and
         runtime.get("npm_path_absent") is True and
         all(runtime.get(name) == "PASS" for name in (
             "sharp", "firebase_admin_imports", "health_200", "default_off_503")),
         "RUNTIME_RECEIPT_DRIFT")
    scan = summary.get("new_image_scan")
    need(isinstance(scan, dict) and
         scan.get("conclusion") == "REVIEW_REQUIRED_NOT_G2_PASS" and
         scan.get("db_sha256") == SCANNER_DB and
         scan.get("full_report_local_only") == str(root / "new-image-grype-full.json") and
         scan.get("bundled_undici_high_remaining") == [], "SCAN_RECEIPT_DRIFT")
    scan_hash = hashlib.sha256(raw_scan).hexdigest()
    need(scan.get("full_report_sha256") == scan_hash, "SCAN_SHA256_MISMATCH")
    matches = report.get("matches")
    need(isinstance(matches, list) and isinstance(report.get("source"), dict),
         "FULL_SCAN_SCHEMA_INVALID")
    counts = Counter()
    severe = {}
    for match in matches:
        need(isinstance(match, dict), "SCAN_MATCH_INVALID")
        v = match.get("vulnerability") or {}
        need(isinstance(v, dict), "SCAN_VULNERABILITY_INVALID")
        level = str(v.get("severity", "UNKNOWN")).upper()
        counts[level] += 1
        if level in ("HIGH", "CRITICAL"):
            pkg = match.get("artifact") or {}
            need(isinstance(pkg, dict), "SCAN_PACKAGE_INVALID")
            cve = v.get("id")
            need(isinstance(cve, str) and cve not in severe, "SEVERE_DUPLICATE_OR_MISSING_ID")
            severe[cve] = (level, pkg.get("name"), pkg.get("version"))
    need(dict(counts) == COUNTS and
         scan.get("severity_counts") == COUNTS and
         scan.get("match_count") == len(matches) == 20, "SCAN_COUNTS_DRIFT")
    need(severe == SEVERE and
         scan.get("severe_ids") == sorted(SEVERE) and
         not UNDICI_IDS.intersection(severe), "SCAN_SEVERE_SUBJECT_DRIFT")
    return {
        "source_sha": SOURCE,
        "image_id": image_id,
        "report_sha256": scan_hash,
        "summary_sha256": hashlib.sha256(raw_summary).hexdigest(),
    }

def main():
    try:
        checked = verify()
    except (Stop, OSError, TypeError) as exc:
        code = str(exc) if isinstance(exc, Stop) else "LOCAL_IO_ERROR"
        print("STOP_LOCAL_IMAGE_EVIDENCE=" + code)
        return 2
    print("OLDX_NPMFREE_LOCAL_EVIDENCE=INTEGRITY_PASS")
    for key, value in checked.items():
        print(key.upper() + "=" + value)
    print("IMAGE_BUILD_RUNTIME_SCAN=PREVIOUSLY_COMPLETE")
    print("INDEPENDENT_SIGNED_BUILDER_PROVENANCE=UNVERIFIED")
    print("DEPLOYABLE_REGISTRY_DIGEST=UNVERIFIED")
    print("G2_SECURITY_CLEARANCE=HOLD")
    print("CLOUD_AND_LOCAL_CHANGES=NONE")
    return 0

if __name__ == "__main__":
    sys.exit(main())
