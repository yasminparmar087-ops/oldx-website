#!/usr/bin/env python3
"""OLDX C1A: locate the read-only CLI failure before a consumed delete attempt.

Only one C1A service IAM GET, then one asia-south1 Eventarc triggers LIST
if the IAM read succeeded with no direct bindings. No Cloud write/delete.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

OWNER = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
REGION = "asia-south1"
SERVICE = "oldx-step05-gateway"
PRIOR = ".oldx-step05-c1a-conditional-service-delete-v2-once-20261126"
MARKER = ".oldx-step05-c1a-cli-read-failure-diagnostic-once-20261126"
MAX_LEN = 256 * 1024
TIMEOUT = 20

class Halt(Exception):
    pass

def ensure(condition, reason):
    if not condition:
        raise Halt(reason)

def safe_private_file(p: Path):
    ensure(not p.is_symlink() and p.is_file() and
           p.stat().st_uid == os.geteuid() and
           p.stat().st_size <= MAX_LEN, "PRIOR_MARKER_UNSAFE")

def classify_error(returncode: int, err: str, out: str) -> str:
    if returncode == 0 and len(out.encode("utf-8")) <= MAX_LEN and len(err.encode("utf-8")) <= MAX_LEN:
        return "EXIT_ZERO"
    combined=(err + "\n" + out[:800]).lower()
    if any(v in combined for v in ("permission_denied", "permission denied", "403", "not authorized")):
        return "PERMISSION_DENIED"
    if any(v in combined for v in ("unauthenticated", "invalid credentials", "401", "login required")):
        return "AUTH_UNAVAILABLE"
    if any(v in combined for v in ("api has not been used", "api is disabled", "api not enabled", "service_disabled")):
        return "API_DISABLED"
    if any(v in combined for v in ("invalid choice", "unrecognized arguments", "no such command")):
        return "CLI_COMMAND_OR_FLAG_ERROR"
    if any(v in combined for v in ("not found", "cannot find", "404")):
        return "TARGET_NOT_FOUND_REPORTED"
    if returncode == 0:
        return "OUTPUT_OVERSIZED"
    return "NONZERO_OTHER"

def stage_run(gcloud: str, label: str, args: list[str], evidence: Path, env: dict):
    cmd = [gcloud, "--quiet", "--account=" + OWNER, "--project=" + PROJECT,
           *args, "--format=json"]
    try:
        r = subprocess.run(cmd, cwd=str(evidence.parent), env=env,
                           stdin=subprocess.DEVNULL, capture_output=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT", None
    ensure(len(r.stdout) <= MAX_LEN and len(r.stderr) <= MAX_LEN, label + "_OUTPUT_OVERSIZED")
    out = r.stdout.decode("utf-8", errors="replace")
    err = r.stderr.decode("utf-8", errors="replace")
    (evidence / (label + ".stdout")).write_text(out, encoding="utf-8")
    (evidence / (label + ".stderr")).write_text(err, encoding="utf-8")
    (evidence / (label + ".exit")).write_text(str(r.returncode) + "\n", encoding="utf-8")
    code = classify_error(r.returncode, err, out)
    if code != "EXIT_ZERO":
        return r.returncode, code, None
    try:
        data = json.loads(out)
    except ValueError:
        return r.returncode, "INVALID_JSON", None
    return r.returncode, "READ_OK", data

def check_policy(data):
    ensure(isinstance(data, dict), "SERVICE_IAM_SCHEMA_UNKNOWN")
    bindings=data.get("bindings", [])
    ensure(isinstance(bindings, list), "SERVICE_IAM_BINDINGS_SCHEMA_UNKNOWN")
    return "NO_DIRECT_BINDINGS" if not bindings else "DIRECT_BINDINGS_PRESENT_STOP"

def check_eventarc(data):
    ensure(isinstance(data, list), "EVENTARC_LIST_SCHEMA_UNKNOWN")
    for item in data:
        ensure(isinstance(item, dict), "EVENTARC_ITEM_SCHEMA_UNKNOWN")
        destination=item.get("destination")
        ensure(isinstance(destination, dict), "EVENTARC_DESTINATION_SCHEMA_UNKNOWN")
        cloud_run=destination.get("cloudRun", destination.get("cloud_run"))
        if cloud_run is not None:
            ensure(isinstance(cloud_run, dict), "EVENTARC_CLOUDRUN_SCHEMA_UNKNOWN")
            name=cloud_run.get("service")
            ensure(isinstance(name, str) and bool(name), "EVENTARC_SERVICE_TARGET_MISSING")
            if name.rsplit("/",1)[-1] == SERVICE:
                return "C1A_DEPENDENCY_PRESENT_STOP"
    return "NO_C1A_CLOUDRUN_TARGET_IN_SUCCESSFUL_REGIONAL_LIST_WITH_LIMITS"

def main():
    os.umask(0o077)
    if sys.argv[1:] != ["--diagnose-c1a-cli-reads-once"]:
        print("C1A_READ_DIAG_RESULT=STOP_FLAG_REQUIRED")
        return 2
    home=Path.home()
    try:
        ensure(platform.system() == "Linux" and
               "microsoft" not in platform.release().lower() and
               os.geteuid() != 0 and home.is_dir(), "OWNER_CLOUD_SHELL_NONROOT_REQUIRED")
        prior=home/PRIOR
        safe_private_file(prior)
        rows=prior.read_text(encoding="utf-8").splitlines()
        ensure({"ATTEMPT_CONSUMED", "RESULT=STOP",
                "REASON=C1A_LIVE_CLI_READ_FAILED",
                "WRITE_ATTEMPTED=False"}.issubset(set(rows)),
               "PREVIOUS_DELETE_STOP_NOT_EXACTLY_VERIFIED")
        marker=home/MARKER
        ensure(not marker.exists() and not marker.is_symlink(), "READ_DIAG_MARKER_ALREADY_CONSUMED")
        gcloud=shutil.which("gcloud")
        ensure(gcloud and Path(gcloud).is_file() and not gcloud.startswith("/mnt/"),
               "GCLOUD_NOT_FOUND")
        evidence=home/("oldx-c1a-cli-read-diagnostic-" +
                       datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
        ensure(not evidence.exists() and not evidence.is_symlink(), "EVIDENCE_COLLISION")
    except (Halt, OSError, UnicodeError) as exc:
        print("C1A_READ_DIAG_RESULT=STOP_PREFLIGHT")
        print("C1A_READ_DIAG_REASON=" + (str(exc) if isinstance(exc,Halt) else type(exc).__name__))
        return 2
    evidence.mkdir(mode=0o700)
    fd=os.open(marker, os.O_EXCL | os.O_CREAT | os.O_WRONLY |
               getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "w") as handle:
        handle.write("ATTEMPT_CONSUMED\nEVIDENCE=" + str(evidence) + "\n")
    env=dict(os.environ)
    env.update({"CLOUDSDK_CORE_DISABLE_PROMPTS":"1",
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1"})
    iam_state="NOT_QUERIED"
    eventarc_state="NOT_QUERIED"
    result="STOP"
    reason="UNDETERMINED"
    try:
        _, iam_state, data=stage_run(
            gcloud, "service_iam",
            ["run","services","get-iam-policy",SERVICE,"--region="+REGION],
            evidence,env)
        if iam_state=="READ_OK":
            iam_state=check_policy(data)
        if iam_state=="NO_DIRECT_BINDINGS":
            _,eventarc_state,data=stage_run(
                gcloud,"eventarc",
                ["eventarc","triggers","list","--location="+REGION],evidence,env)
            if eventarc_state=="READ_OK":
                eventarc_state=check_eventarc(data)
        if iam_state=="NO_DIRECT_BINDINGS" and eventarc_state=="NO_C1A_CLOUDRUN_TARGET_IN_SUCCESSFUL_REGIONAL_LIST_WITH_LIMITS":
            result="READ_ONLY_DIAG_WITH_LIMITS"
            reason="BOTH_NARROW_READS_SUCCEEDED"
        else:
            reason="IAM_OR_EVENTARC_DIAG_NEEDS_REVIEW"
    except (Halt,OSError,UnicodeError,ValueError,TypeError,subprocess.SubprocessError) as exc:
        reason=str(exc) if isinstance(exc,Halt) else type(exc).__name__
    finally:
        (evidence/"summary.json").write_text(json.dumps({
            "result":result,"reason":reason,
            "iam":iam_state,"eventarc":eventarc_state,
            "writes_attempted":False,
            "deleted":False,
        },sort_keys=True) + "\n",encoding="utf-8")
        with marker.open("a") as handle:
            handle.write("RESULT="+result+"\nREASON="+reason+"\n")
    print("C1A_READ_DIAG_IAM="+iam_state)
    print("C1A_READ_DIAG_EVENTARC="+eventarc_state)
    print("C1A_READ_DIAG_RESULT="+result)
    print("C1A_READ_DIAG_REASON="+reason)
    print("C1A_CLOUD_WRITES=NONE")
    print("C1A_RESOURCE_DELETED=NO")
    return 0 if result=="READ_ONLY_DIAG_WITH_LIMITS" else 2

if __name__=="__main__":
    sys.exit(main())
