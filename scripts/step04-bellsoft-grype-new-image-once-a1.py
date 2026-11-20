#!/usr/bin/env python3
"""OLDX Step 04 — exact one local, unfiltered NEW BellSoft image Grype scan.

Runs once, no rebuild, no image pull, no DB download/update, no registry/cloud writes.
STOP is final: retain its receipt, never retry without forensic review.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from collections import Counter

ROOT = Path("/mnt/d/OLDX/G2/oldx-bellsoft-derived-20261120-a1")
SOURCE = ROOT / "src"
EVIDENCE = ROOT / "runtime-once-a1" / "summary.json"
DEST = ROOT / "grype-new-image-once-a1"
TAG = "oldx-bellsoft-local:20261120-a1"
IMAGE_ID = "sha256:161fedc0e3479070e8897cc349f196b0c72c5cd11a2494a558610f42116b17bb"
SOURCE_SHA = "3a4d5f0657c0d55cbedac3b6461353e4d2a69de1"
GRYPE = Path("/root/.oldx-g2-tools/grype")
DB_CACHE = Path("/root/.oldx-g2-tools/db-cache-raw")
DB = DB_CACHE / "6/vulnerability.db"
DB_SHA = "303ba44739343769e0e15bd0d50af62e142491b256bb533a8cfaf13ab00ca1b7"

def stop(reason):
    print("STOP_NEW_GRYPE="+reason,flush=True)
    sys.exit(2)

def run(args, timeout=30):
    return subprocess.run(args,check=True,capture_output=True,text=True,timeout=timeout).stdout.strip()

def sha256_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(4*1024*1024),b""):
            h.update(block)
    return h.hexdigest()

try:
    if not (SOURCE/".git").is_dir() or not (ROOT/"build.log").is_file() or not (ROOT/"build-metadata.json").is_file():
        stop("BUILD_RECEIPT_MISSING")
    if run(["git","-C",str(SOURCE),"rev-parse","HEAD"])!=SOURCE_SHA:
        stop("SOURCE_COMMIT_DRIFT")
    if not EVIDENCE.is_file() or EVIDENCE.is_symlink():
        stop("RUNTIME_RECEIPT_MISSING")
    e=json.loads(EVIDENCE.read_text(encoding="utf-8"))
    tests=e.get("runtime",{})
    if e.get("outcome")!="PASS" or e.get("image_id")!=IMAGE_ID or e.get("source_commit")!=SOURCE_SHA:
        stop("RUNTIME_NOT_PASS")
    if e.get("sigterm_exit_code")!=0 or any(tests.get(k)!="PASS" for k in ("sharp","firebase_admin_imports","health_200","default_off_503")):
        stop("RUNTIME_CHECKS_INCOMPLETE")
    if not (isinstance(tests.get("uid"),int) and tests.get("uid")>0):
        stop("NONROOT_UNVERIFIED")
    if DEST.exists() or DEST.is_symlink():
        stop("SCAN_ALREADY_ATTEMPTED")
    if run(["git","-C",str(SOURCE),"status","--porcelain"])!="":
        stop("SOURCE_DIRTY")
    image=json.loads(run(["docker","image","inspect",TAG]))[0]
    cfg=image.get("Config") or {}
    if image.get("Id")!=IMAGE_ID or image.get("Os")!="linux" or image.get("Architecture")!="amd64":
        stop("IMAGE_ID_DRIFT")
    if cfg.get("User")!="appuser" or cfg.get("Entrypoint")!=["/usr/bin/node"] or cfg.get("Cmd")!=["functions/staging-marketplace/product-read-server.mjs"]:
        stop("IMAGE_RUNTIME_CONFIG_DRIFT")
    if TAG not in (image.get("RepoTags") or []):
        stop("IMAGE_TAG_MISSING")
    if not GRYPE.is_file() or not os.access(GRYPE,os.X_OK) or not DB.is_file():
        stop("GRYPE_OR_DB_NOT_FOUND")
    if sha256_file(DB)!=DB_SHA:
        stop("IMPORTED_DB_SHA_DRIFT")
    if "0.121.3" not in run([str(GRYPE),"version"],timeout=20):
        stop("GRYPE_VERSION_DRIFT")
    d_free=int(run(["df","-Pk","/mnt/d"]).splitlines()[-1].split()[3])
    if d_free<12*1024*1024:
        stop("D_FREE_BELOW_12G")
    print("NEW_IMAGE_GRYPE_PREFLIGHT=PASS",flush=True)
except SystemExit:
    raise
except Exception as exc:
    print("STOP_NEW_GRYPE_PREFLIGHT_ERROR="+type(exc).__name__,flush=True)
    sys.exit(2)

DEST.mkdir(mode=0o700)
report=DEST/"grype-full.json"
log=DEST/"grype.log"
config=DEST/"empty-config.yaml"
summary_path=DEST/"summary.json"
config.write_text("{}\n",encoding="utf-8")
env=dict(os.environ)
for key in list(env):
    if key.startswith("GRYPE_") or key.startswith("SYFT_"):
        del env[key]
env.update({
  "GRYPE_DB_CACHE_DIR":str(DB_CACHE),
  "GRYPE_DB_AUTO_UPDATE":"false",
  "GRYPE_CHECK_FOR_APP_UPDATE":"false",
})
args=[str(GRYPE),"--config",str(config),"docker:"+TAG,
      "--scope","squashed","--output","json"]
result={"source_commit":SOURCE_SHA,"image_id":IMAGE_ID,
        "scan_target":"docker:"+TAG,"db_sha256":DB_SHA,"scope":"squashed",
        "scanner":"grype 0.121.3","suppression":"none",
        "status":"SCAN_START"}
summary_path.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print("ONE_NEW_IMAGE_UNFILTERED_GRYPE_STARTING",flush=True)

try:
    with report.open("xb") as out, log.open("xb") as err:
        proc=subprocess.Popen(args,stdout=out,stderr=err,env=env)
        try:
            rc=proc.wait(timeout=480)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try: proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill(); proc.wait()
            result["status"]="STOP_TIMEOUT_DO_NOT_RETRY"
            stop("SCAN_TIMEOUT_DO_NOT_RETRY")
    result["scan_return_code"]=rc
    if rc!=0:
        result["status"]="STOP_SCANNER_RETURN_DO_NOT_RETRY"
        stop("SCANNER_RETURN_"+str(rc)+"_DO_NOT_RETRY")
    data=json.loads(report.read_text(encoding="utf-8"))
    matches=data.get("matches")
    if not isinstance(matches,list) or not isinstance(data.get("source"),dict):
        result["status"]="STOP_REPORT_SCHEMA"
        stop("REPORT_SCHEMA")
    # Do not filter the report: summarize all matches and all severities including unknown.
    severity=Counter(str(m.get("vulnerability",{}).get("severity","Unknown")).upper() for m in matches)
    high_ids=sorted({str(m.get("vulnerability",{}).get("id","")) for m in matches
                     if str(m.get("vulnerability",{}).get("severity","")).upper() in ("HIGH","CRITICAL")})
    result.update({"status":"COMPLETE_REVIEW_REQUIRED","matches":len(matches),
                   "severity_counts":dict(severity),"high_critical_unique":high_ids,
                   "report_sha256":sha256_file(report)})
    print("GRYPE_SCAN_EXIT=0",flush=True)
    print("TOTAL_MATCHES="+str(len(matches)),flush=True)
    print("SEVERITIES="+json.dumps(dict(severity),sort_keys=True),flush=True)
    print("HIGH_CRITICAL_UNIQUE="+str(len(high_ids)),flush=True)
    print("HIGH_CRITICAL_IDS="+",".join(high_ids),flush=True)
    print("NEW_GRYPE_REPORT_SHA256="+result["report_sha256"],flush=True)
    print("NEW_IMAGE_ONE_FULL_GRYPE_SCAN=COMPLETE_REVIEW_REQUIRED",flush=True)
except SystemExit:
    raise
except Exception as exc:
    result["status"]="STOP_"+type(exc).__name__+"_DO_NOT_RETRY"
    print("STOP_NEW_GRYPE_POSTSTART="+type(exc).__name__,flush=True)
    sys.exit(2)
finally:
    summary_path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PRIVATE_REPORT="+str(report),flush=True)
    print("SUMMARY="+str(summary_path),flush=True)
