#!/usr/bin/env python3
"""OLDX Step04: one local offline runtime smoke for one already-built BellSoft image (v2: image-ID transcription corrected).

Requires owner-scoped prior build receipt. No new image build/scan/pull/push/cloud calls.
Runs a named, network-none, no-host-ports, nonroot container once and removes it.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

RUN = Path("/mnt/d/OLDX/G2/oldx-bellsoft-derived-20261120-a1")
EVIDENCE = RUN / "runtime-once-a1"
IMAGE = "oldx-bellsoft-local:20261120-a1"
IMAGE_ID = "sha256:161fedc0e3479070e8897cc349f196b0c72c5cd11a2494a558610f42116b17bb"
SOURCE_SHA = "3a4d5f0657c0d55cbedac3b6461353e4d2a69de1"
NAME = "oldx-bellsoft-runtime-20261120-a1"

def cmd(argv, timeout=45, check=True):
    result = subprocess.run(argv, text=True, capture_output=True, timeout=timeout)
    if check and result.returncode != 0:
        raise RuntimeError("COMMAND_FAILED_" + str(argv[1] if len(argv)>1 else argv[0]))
    return result

def guard(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def local_image():
    return json.loads(cmd(["docker","image","inspect", IMAGE]).stdout)[0]

try:
    guard((RUN/"src"/".git").is_dir() and (RUN/"build.log").is_file() and
          (RUN/"build-metadata.json").is_file(), "BUILD_RECEIPT_MISSING")
    guard(cmd(["git","-C",str(RUN/"src"),"rev-parse","HEAD"]).stdout.strip()==SOURCE_SHA,
          "SOURCE_COMMIT_DRIFT")
    guard(not EVIDENCE.exists() and not EVIDENCE.is_symlink(), "RUNTIME_ALREADY_ATTEMPTED")
    info=local_image()
    config=info.get("Config") or {}
    guard(info.get("Id")==IMAGE_ID and info.get("Os")=="linux" and
          info.get("Architecture")=="amd64", "IMAGE_ID_MISMATCH")
    guard(config.get("User")=="appuser", "IMAGE_USER_NOT_APPUSER")
    guard(config.get("Entrypoint")==["/usr/bin/node"], "NODE_ENTRYPOINT_DRIFT")
    guard(config.get("Cmd")==["functions/staging-marketplace/product-read-server.mjs"],
          "SERVER_CMD_DRIFT")
    guard(not cmd(["docker","container","inspect",NAME], check=False).returncode==0,
          "CONTAINER_NAME_EXISTS")
    print("RUNTIME_PREFLIGHT=PASS",flush=True)
except Exception as exc:
    print("STOP_RUNTIME_PREFLIGHT="+str(exc),flush=True)
    sys.exit(2)

EVIDENCE.mkdir(mode=0o700)
created=False
summary={"image_id":IMAGE_ID,"source_commit":SOURCE_SHA,
         "test":"NEW_BELLSOFT_LOCAL_OFFLINE_RUNTIME","outcome":"INCOMPLETE"}
js = """
import sharp from 'sharp';
await import('firebase-admin/app');
await import('firebase-admin/auth');
await import('firebase-admin/firestore');
const ver = process.versions.node.split('.').map(Number);
if (ver[0] !== 24 || ver[1] < 12) throw Error('NODE_VERSION');
if (process.getuid?.() === 0 || process.getuid?.() == null) throw Error('ROOT_OR_UNKNOWN_UID');
const out = await sharp({create:{width:2,height:2,channels:4,background:'#c44'}}).png().toBuffer();
const result = await sharp(out).metadata();
if (result.width !== 2 || result.height !== 2 || result.format !== 'png') throw Error('SHARP_TRANSFORM');
const health = await fetch('http://127.0.0.1:8080/healthz',{signal:AbortSignal.timeout(5000)});
const hbody = await health.json();
if (health.status !== 200 || hbody.ok !== true) throw Error('HEALTH_200');
const off = await fetch('http://127.0.0.1:8080/api/staging/marketplace/owner',
 {method:'POST',headers:{'content-type':'application/json'},body:'{}',
 signal:AbortSignal.timeout(5000)});
const obody = await off.json();
if (off.status !== 503 || obody?.error?.code !== 'ENFORCEMENT_UNAVAILABLE') throw Error('DEFAULT_OFF_503');
console.log(JSON.stringify({node:process.versions.node,uid:process.getuid(),
 sharp:'PASS',firebase_admin_imports:'PASS',health_200:'PASS',default_off_503:'PASS'}));
"""
try:
    print("ONE_OFFLINE_CONTAINER_STARTING",flush=True)
    cmd(["docker","run","--detach","--name",NAME,"--network","none",
         "--read-only","--tmpfs","/tmp:rw,nosuid,size=64m",
         "--cap-drop","ALL","--security-opt","no-new-privileges",
         "--pids-limit","128","--memory","768m","--cpus","1",
         IMAGE],timeout=90)
    created=True
    time.sleep(2)
    tested=cmd(["docker","exec",NAME,"/usr/bin/node","--input-type=module",
                "--eval",js],timeout=70)
    results=json.loads(tested.stdout.strip().splitlines()[-1])
    summary["runtime"]=results
    print("NODE24_NONROOT_SHARP_FIREBASE_HEALTH_OFF=PASS",flush=True)
    stopped=cmd(["docker","stop","--time","12",NAME],timeout=35)
    code=cmd(["docker","inspect","--format","{{.State.ExitCode}}",NAME]).stdout.strip()
    guard(code=="0","SIGTERM_EXIT_"+code)
    summary["sigterm_exit_code"]=0
    summary["outcome"]="PASS"
    print("SIGTERM_CLEAN_EXIT=PASS",flush=True)
    print("ONE_OFFLINE_RUNTIME=PASS",flush=True)
except Exception as exc:
    summary["outcome"]="STOP"
    summary["error_type"]=type(exc).__name__
    print("STOP_RUNTIME_REVIEW="+type(exc).__name__,flush=True)
finally:
    if created:
        logs=cmd(["docker","logs","--tail","80",NAME],timeout=12,check=False)
        (EVIDENCE/"container.log").write_text((logs.stdout+"\n"+logs.stderr)[-12000:],encoding="utf-8")
        try:
            cmd(["docker","rm","--force",NAME],timeout=30)
        except Exception:
            print("STOP_CONTAINER_CLEANUP_CHECK",flush=True)
            summary["cleanup"]="UNVERIFIED"
    (EVIDENCE/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("RUNTIME_EVIDENCE="+str(EVIDENCE/"summary.json"),flush=True)
if summary["outcome"]!="PASS":
    sys.exit(2)
