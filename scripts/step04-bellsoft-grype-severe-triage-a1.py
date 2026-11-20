#!/usr/bin/env python3
"""Read-only, bounded triage of ONE completed OLDX Step04 BellSoft Grype JSON.

Verifies the saved report SHA-256 and scan identity. Prints limited package
identity, fix/disposition, and source metadata for all critical/high matches.
No image build/pull, no Grype, no database update, no network, no file writes.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

BASE = Path("/mnt/d/OLDX/G2/oldx-bellsoft-derived-20261120-a1/grype-new-image-once-a1")
REPORT = BASE / "grype-full.json"
SUMMARY = BASE / "summary.json"
EXPECTED_IMAGE = "sha256:161fedc0e3479070e8897cc349f196b0c72c5cd11a2494a558610f42116b17bb"
EXPECTED_DB = "303ba44739343769e0e15bd0d50af62e142491b256bb533a8cfaf13ab00ca1b7"
EXPECTED_SOURCE = "3a4d5f0657c0d55cbedac3b6461353e4d2a69de1"
EXPECTED_SEVERITIES = {"CRITICAL": 1, "HIGH": 8, "MEDIUM": 17, "LOW": 2}

def stop(name):
    raise SystemExit("STOP_READ_ONLY_TRIAGE_" + name)

def clip(value, n=135):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=True, sort_keys=True)
    return str(value or "").replace("\n", " ").replace("\r", " ")[:n]

try:
    if not SUMMARY.is_file() or not REPORT.is_file() or SUMMARY.is_symlink() or REPORT.is_symlink():
        stop("MISSING_REPORT")
    size=REPORT.stat().st_size
    if size<=0 or size>64*1024*1024:
        stop("REPORT_SIZE")
    s=json.loads(SUMMARY.read_text(encoding="utf-8"))
    if (s.get("status")!="COMPLETE_REVIEW_REQUIRED" or
        s.get("image_id")!=EXPECTED_IMAGE or
        s.get("db_sha256")!=EXPECTED_DB or
        s.get("source_commit")!=EXPECTED_SOURCE or
        s.get("scan_target")!="docker:oldx-bellsoft-local:20261120-a1" or
        s.get("matches")!=28):
        stop("SCAN_IDENTITY")
    digest=hashlib.sha256(REPORT.read_bytes()).hexdigest()
    if digest!=s.get("report_sha256"):
        stop("REPORT_SHA256_MISMATCH")
    data=json.loads(REPORT.read_text(encoding="utf-8"))
    matches=data.get("matches")
    if not isinstance(matches,list) or len(matches)!=28:
        stop("MATCHES_CHANGED")
    counts=Counter(str(m.get("vulnerability",{}).get("severity","Unknown")).upper() for m in matches)
    if dict(counts)!=EXPECTED_SEVERITIES:
        stop("SEVERITY_CHANGED")
    severe=[m for m in matches if str(m.get("vulnerability",{}).get("severity","")).upper() in ("CRITICAL","HIGH")]
    ids={str(m.get("vulnerability",{}).get("id","")) for m in severe}
    if len(severe)!=9 or len(ids)!=9 or set(s.get("high_critical_unique",[]))!=ids:
        stop("SEVERE_IDS_CHANGED")
    print("SEALED_REPORT_SHA256=PASS")
    print("LOCAL_IMAGE_SCAN_IDENTITY=PASS")
    print("SCANNER_DB_SNAPSHOT=2026-11-17")
    print("SEVERE_MATCHES=9")
    print("REPORT_SOURCE_TYPE="+clip((data.get("source") or {}).get("type")))
    distro=data.get("distro",{})
    print("REPORT_DISTRO="+clip(distro))
    for i,m in enumerate(sorted(severe,key=lambda x:(str(x.get("vulnerability",{}).get("severity"))!="Critical",
                        str(x.get("vulnerability",{}).get("id","")))),1):
        v=m.get("vulnerability",{})
        a=m.get("artifact",{})
        f=v.get("fix") or {}
        if not isinstance(f,dict):
            f={}
        detail=m.get("matchDetails") or []
        matcher=sorted({str(x.get("type","")) for x in detail if isinstance(x,dict)})
        print("FINDING_"+str(i)+"="+
              " | ".join([
                "SEVERITY:"+clip(v.get("severity"),20),
                "ID:"+clip(v.get("id"),85),
                "PACKAGE:"+clip(a.get("name")),
                "INSTALLED:"+clip(a.get("version")),
                "TYPE:"+clip(a.get("type"),35),
                "FIX_STATE:"+clip(f.get("state"),35),
                "FIX_VERSIONS:"+clip(f.get("versions"),220),
                "NAMESPACE:"+clip(v.get("namespace")),
                "MATCHER:"+clip(matcher,100)
              ]))
    print("NEW_GRYPE_SEVERE_TRIAGE_READ_ONLY=COMPLETE")
except SystemExit:
    raise
except Exception as exc:
    print("STOP_READ_ONLY_TRIAGE_ERROR="+type(exc).__name__)
    sys.exit(2)
