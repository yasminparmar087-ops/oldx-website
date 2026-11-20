#!/usr/bin/env python3
"""OLDX Step04: read-only severe finding package-location reconciliation.

Uses the ONE existing complete new BellSoft-derived image Grype scan.
No Grype, network, image mutation, build, registry, or file write.
"""
import hashlib
import json
from pathlib import Path
from collections import Counter

ROOT=Path("/mnt/d/OLDX/G2/oldx-bellsoft-derived-20261120-a1")
R=ROOT/"grype-new-image-once-a1"/"grype-full.json"
S=ROOT/"grype-new-image-once-a1"/"summary.json"
L=ROOT/"src"/"package-lock.json"
EXPECTED_ID="sha256:161fedc0e3479070e8897cc349f196b0c72c5cd11a2494a558610f42116b17bb"
EXPECTED_SOURCE="3a4d5f0657c0d55cbedac3b6461353e4d2a69de1"

def guard(ok,label):
    if not ok: raise SystemExit("STOP_LOCATIONS_"+label)

def short(v,length=210):
    return str(v or "").replace("\n"," ").replace("\r"," ")[:length]

guard(all(p.is_file() and not p.is_symlink() for p in [R,S,L]),"FILES")
s=json.loads(S.read_text(encoding="utf-8"))
guard(s.get("status")=="COMPLETE_REVIEW_REQUIRED" and s.get("image_id")==EXPECTED_ID
      and s.get("source_commit")==EXPECTED_SOURCE and s.get("matches")==28,"IDENTITY")
guard(hashlib.sha256(R.read_bytes()).hexdigest()==s.get("report_sha256"),"REPORT_HASH")
d=json.loads(R.read_text(encoding="utf-8"))
ls=json.loads(L.read_text(encoding="utf-8"))
und=(ls.get("packages") or {}).get("node_modules/undici",{}).get("version")
guard(und=="6.29.1","SOURCE_LOCK_UNDICI")
matches=d.get("matches")
guard(isinstance(matches,list) and len(matches)==28,"MATCHES")
severity=Counter(str(m.get("vulnerability",{}).get("severity","")).upper() for m in matches)
guard(dict(severity)=={"CRITICAL":1,"HIGH":8,"MEDIUM":17,"LOW":2},"SEVERITIES")
severe=[m for m in matches if m.get("vulnerability",{}).get("severity","").upper() in ("CRITICAL","HIGH")]
guard(len(severe)==9 and len(set(m["vulnerability"]["id"] for m in severe))==9,"SEVERE")

print("SEALED_REPORT_AND_SOURCE_LOCK=PASS")
print("PINNED_SOURCE_UNDICI=6.29.1")
for i,m in enumerate(sorted(severe,key=lambda x:(x["vulnerability"]["id"])),1):
    a=m["artifact"]
    v=m["vulnerability"]
    locs=a.get("locations") or []
    paths=[]
    for item in locs:
        path=item.get("path") if isinstance(item,dict) else item
        if path:
            paths.append(short(path,230))
    print(f"FINDING_{i}_ID="+short(v.get("id"),90))
    print(f"FINDING_{i}_PACKAGE="+short(a.get("name"))+
          " INSTALLED="+short(a.get("version"),55)+" PURL="+short(a.get("purl"),260))
    print(f"FINDING_{i}_LOCATIONS="+json.dumps(paths[:8],ensure_ascii=True))
    print(f"FINDING_{i}_LOCATION_COUNT="+str(len(paths)))
print("LOCATIONS_READ_ONLY=COMPLETE")
