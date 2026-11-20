#!/usr/bin/env python3
"""OLDX Step04 one local filesystem-exposure probe of already-built image.

Never starts a container; only docker create, docker cp exact paths, docker rm.
No scan, build, registry network/pull, host ports, image modifications or secrets.
Outputs existence/copy status, which alone is NOT a vulnerability disposition.
"""
import json
import subprocess
import sys
from pathlib import Path
from io import BytesIO
import tarfile

ROOT=Path("/mnt/d/OLDX/G2/oldx-bellsoft-derived-20261120-a1")
EVIDENCE=ROOT/"fs-exposure-once-a1"
RUNTIME=ROOT/"runtime-once-a1"/"summary.json"
SCAN=ROOT/"grype-new-image-once-a1"/"summary.json"
IMAGE="oldx-bellsoft-local:20261120-a1"
ID="sha256:161fedc0e3479070e8897cc349f196b0c72c5cd11a2494a558610f42116b17bb"
NAME="oldx-bellsoft-fs-exposure-20261120-a1"
PATHS=[
    "/usr/bin/sqlite3",
    "/bin/sqlite3",
    "/usr/local/bin/sqlite3",
    "/usr/bin/ldd",
    "/bin/ldd",
    "/usr/local/bin/ldd",
    "/usr/lib/node_modules/npm/node_modules/undici/package.json",
    "/app/node_modules/undici/package.json"
]

def call(args,timeout=30):
    return subprocess.run(args,text=True,capture_output=True,timeout=timeout)
def guard(condition,code):
    if not condition:
        print("STOP_FS_PREFLIGHT="+code,flush=True)
        sys.exit(2)
try:
    guard(not EVIDENCE.exists() and not EVIDENCE.is_symlink(),"ALREADY_ATTEMPTED")
    guard(RUNTIME.is_file() and SCAN.is_file(),"RECEIPT_MISSING")
    r=json.loads(RUNTIME.read_text())
    s=json.loads(SCAN.read_text())
    guard(r.get("outcome")=="PASS" and r.get("image_id")==ID,"RUNTIME_RECEIPT")
    guard(s.get("status")=="COMPLETE_REVIEW_REQUIRED" and
          s.get("image_id")==ID and s.get("matches")==28,"SCAN_RECEIPT")
    info=call(["docker","image","inspect",IMAGE])
    guard(info.returncode==0,"IMAGE_MISSING")
    d=json.loads(info.stdout)[0]
    guard(d.get("Id")==ID and d.get("Os")=="linux" and
          d.get("Architecture")=="amd64","IMAGE_IDENTITY")
    guard(call(["docker","container","inspect",NAME]).returncode!=0,"CONTAINER_NAME_OCCUPIED")
    print("FS_PROBE_PREFLIGHT=PASS",flush=True)
except SystemExit:
    raise
except Exception as e:
    print("STOP_FS_PREFLIGHT_ERROR="+type(e).__name__,flush=True)
    sys.exit(2)

EVIDENCE.mkdir(mode=0o700)
result={"image_id":ID,"mode":"container_create_only_never_started",
        "status":"STARTED","results":{}}
created=False
try:
    p=call(["docker","create","--name",NAME,"--network","none",
            "--read-only","--cap-drop","ALL","--entrypoint","/usr/bin/node",IMAGE,"--help"],timeout=45)
    if p.returncode!=0:
        raise RuntimeError("DOCKER_CREATE_FAILED")
    created=True
    print("FS_INSPECT_ONLY_CONTAINER_CREATED_NOT_STARTED",flush=True)
    for target in PATHS:
        proc=subprocess.run(["docker","cp",NAME+":"+target,"-"],
                            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
        state="PRESENT" if proc.returncode==0 else "NOT_CONFIRMED"
        extra={}
        if proc.returncode==0 and target.endswith("undici/package.json"):
            try:
                with tarfile.open(fileobj=BytesIO(proc.stdout),mode="r:") as tf:
                    found=next((f for f in tf if f.isfile() and f.name.endswith("package.json")),None)
                    if found:
                        obj=json.load(tf.extractfile(found))
                        extra["version"]=obj.get("version")
                        extra["package_name"]=obj.get("name")
            except Exception:
                extra["parse"]="INDETERMINATE"
        result["results"][target]={"state":state,**extra}
        print("PATH="+target+" STATE="+state+
              (" VERSION="+str(extra.get("version")) if "version" in extra else ""),flush=True)
    result["status"]="INSPECTION_COMPLETE_REVIEW_REQUIRED"
    print("FS_INSPECTION_READ_ONLY=COMPLETE",flush=True)
except Exception as e:
    result["status"]="STOP_"+type(e).__name__
    print("STOP_FS_REVIEW="+type(e).__name__,flush=True)
finally:
    if created:
        rm=call(["docker","rm","--force",NAME],timeout=30)
        result["cleanup"]="PASS" if rm.returncode==0 else "STOP_CLEANUP_MANUAL"
        print("FS_ONLY_CONTAINER_CLEANUP="+result["cleanup"],flush=True)
    (EVIDENCE/"summary.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("FS_EVIDENCE="+str(EVIDENCE/"summary.json"),flush=True)
if result["status"]!="INSPECTION_COMPLETE_REVIEW_REQUIRED" or result.get("cleanup")!="PASS":
    sys.exit(2)
