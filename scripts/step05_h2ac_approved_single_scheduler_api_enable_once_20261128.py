#!/usr/bin/env python3
"""BAJUTO Step05 H2AC — ONE separately owner-approved Scheduler API enable.
SOURCE-ONLY until owner explicitly approves. No Scheduler job, IAM, Compute,
VPC, KMS, Firestore, Cloud Run deployment or hosted HTTP request.
"""
from __future__ import annotations
import json
import os
import platform
import re
import ssl
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error

ROOT = Path("/root")
PROJECT = "oldx-staging"
PROJECT_NUMBER = "38472235077"
OWNER = "yasminparmar087@gmail.com"
SERVICE = "cloudscheduler.googleapis.com"
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
PRIOR = ROOT / ".oldx-step05-h2ab-cloudscheduler-api-state-once-20261128"
MARKER = ROOT / ".oldx-step05-h2ac-scheduler-api-enable-approved-once-20261128"
BASE = "https://serviceusage.googleapis.com/v1/projects/" + PROJECT_NUMBER + "/services/" + SERVICE
STATE = BASE + "?fields=name%2Cstate"
ENABLE = BASE + ":enable"
OPERATIONS = "https://serviceusage.googleapis.com/v1/operations/"

class Stop(Exception):
    pass

def need(ok, msg):
    if not ok:
        raise Stop(msg)

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

OPENER = request.build_opener(
    request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()), NoRedirect())

def call(method, url, token):
    allowed_operation = (method == "GET" and
        re.fullmatch(re.escape(OPERATIONS) + r"[A-Za-z0-9._-]{6,200}", url) is not None)
    need((method, url) in (("GET", STATE), ("POST", ENABLE)) or
         allowed_operation, "METHOD_OR_URL_OUT_OF_SCOPE")
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "User-Agent": "OLDX-H2AC-approved-one-Scheduler-API-only/1"}
    if method == "POST":
        headers["Content-Type"] = "application/json"
    req = request.Request(
        url, method=method, headers=headers,
        data=b"{}" if method == "POST" else None)
    try:
        with OPENER.open(req, timeout=35) as res:
            need(res.status == 200, "HTTP_NOT_200")
            data = res.read(8193)
            need(len(data) <= 8192, "RESPONSE_TOO_LARGE")
    except error.HTTPError as exc:
        status = exc.code
        exc.close()
        raise Stop("HTTP_" + str(status))
    except (error.URLError, ssl.SSLError, TimeoutError):
        raise Stop("NETWORK_OR_TLS_UNCERTAIN")
    obj = json.loads(data)
    need(isinstance(obj, dict), "RESPONSE_NOT_OBJECT")
    return obj

def get_state(token):
    obj = call("GET", STATE, token)
    need(obj.get("name") == "projects/" + PROJECT_NUMBER + "/services/" + SERVICE,
         "SERVICE_PROJECT_IDENTITY_DRIFT")
    state = obj.get("state")
    need(state in ("ENABLED", "DISABLED"), "API_STATE_NOT_EXACT")
    return state

def token_preflight():
    need(sys.argv[1:] == ["--h2ac-owner-approved-one-scheduler-api-enable-once"],
         "EXACT_OWNER_APPROVAL_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(), "ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(),
         "H2AC_ALREADY_CONSUMED_DO_NOT_REPEAT")
    need(PRIOR.is_file() and not PRIOR.is_symlink() and PRIOR.stat().st_uid == 0,
         "H2AB_READONLY_RECEIPT_MISSING")
    receipt = PRIOR.read_text(encoding="utf-8").splitlines()
    for expected in (
        "ATTEMPT=H2AB_CLOUDSCHEDULER_API_STATE_READONLY",
        "PROJECT=oldx-staging", "PREVIOUS=H2AA_COMPUTE_API_DISABLED"):
        need(expected in receipt, "H2AB_RECEIPT_NOT_MATCHED")
    need(SDK.is_dir() and not SDK.is_symlink()
         and CLI.is_file() and not CLI.is_symlink()
         and os.access(CLI, os.X_OK)
         and PY.resolve(strict=True).is_file()
         and CONFIG.is_dir() and not CONFIG.is_symlink(),
         "ISOLATED_OWNER_SDK_OR_AUTH_MISSING")
    env = dict(os.environ)
    env.update({
        "HOME": str(ROOT), "PATH": str(CLI.parent) + ":/usr/bin:/bin",
        "CLOUDSDK_CONFIG": str(CONFIG), "CLOUDSDK_PYTHON": str(PY),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE", None)
    try:
        result = subprocess.run(
            [str(CLI), "--quiet", "--account=" + OWNER, "--project=" + PROJECT,
             "auth", "print-access-token"], env=env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=35, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("OWNER_OAUTH_TIMEOUT")
    need(result.returncode == 0 and result.stdout.strip(), "OWNER_OAUTH_UNAVAILABLE")
    token = result.stdout.decode("utf-8", "strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", token) is not None,
         "OAUTH_TOKEN_INVALID")
    return token

def record(line):
    with MARKER.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def main():
    os.umask(0o077)
    try:
        token = token_preflight()
        initial = get_state(token)
    except (Stop, OSError, TypeError, ValueError, UnicodeError) as exc:
        print("H2AC_RESULT=STOP_BEFORE_ENABLE")
        print("H2AC_REASON=" + (str(exc) if isinstance(exc, Stop) else type(exc).__name__))
        print("H2AC_ENABLE_ATTEMPTED=FALSE")
        return 2
    if initial == "ENABLED":
        print("H2AC_RESULT=ALREADY_ENABLED_NO_WRITE")
        print("H2AC_ENABLE_ATTEMPTED=FALSE")
        print("H2AC_H2_PRODUCTION=NO_GO")
        return 0
    need(initial == "DISABLED", "FRESH_SCHEDULER_STATE_NOT_DISABLED")
    evidence = ROOT / ("oldx-h2ac-scheduler-api-enable-" +
                       datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd = os.open(str(MARKER), os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT=" + PROJECT +
                    "\nSERVICE=" + SERVICE + "\nEVIDENCE=" + str(evidence) + "\n")
    except OSError:
        print("H2AC_RESULT=STOP_MARKER_BEFORE_WRITE")
        return 2
    attempted = False
    operation_name = "NOT_RETURNED"
    final_state = "NOT_VERIFIED"
    result = "STOP_AFTER_MARKER"
    reason = "UNKNOWN"
    try:
        record("ENABLE_REQUEST_ABOUT_TO_BE_SENT=TRUE")
        attempted = True
        print("H2AC_STAGE=ONE_SCHEDULER_API_ENABLE_ATTEMPT", flush=True)
        response = call("POST", ENABLE, token)
        op = response.get("name")
        need(isinstance(op, str) and
             re.fullmatch(r"operations/[A-Za-z0-9._-]{6,200}", op) is not None,
             "ENABLE_OPERATION_NAME_INVALID")
        operation_name = op
        record("OPERATION_NAME=" + operation_name)
        done = False
        for _ in range(12):
            item = call("GET", "https://serviceusage.googleapis.com/v1/" + op, token)
            if item.get("done") is True:
                need(not item.get("error"), "OPERATION_REPORTED_ERROR")
                done = True
                break
            time.sleep(3)
        need(done, "OPERATION_NOT_COMPLETED_IN_BOUNDED_WINDOW")
        final_state = get_state(token)
        need(final_state == "ENABLED", "SCHEDULER_API_NOT_VERIFIED_ENABLED")
        result = "PASS_EXACT_SCHEDULER_API_ENABLED"
        reason = "ONE_ENABLE_DONE_STATE_READBACK_ENABLED"
    except (Stop, OSError, TypeError, ValueError, UnicodeError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
    finally:
        try:
            (evidence / "sanitized-api-result.json").write_text(
                json.dumps({
                    "project": PROJECT, "project_number": PROJECT_NUMBER,
                    "service": SERVICE, "initial": initial,
                    "post_attempt": attempted, "operation": operation_name,
                    "final_state": final_state, "result": result, "reason": reason,
                    "job_created_or_run": False, "iam_or_other_resource_write": False,
                    "h2": "NO_GO", "production": "NO_GO"
                }, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            record("RESULT=" + result)
            record("REASON=" + reason)
        except OSError:
            result = "STOP_EVIDENCE_WRITE"
        print("H2AC_ENABLE_ATTEMPTED=" + str(attempted).upper())
        print("H2AC_SCHEDULER_API_STATE=" + final_state)
        print("H2AC_RESULT=" + result)
        print("H2AC_REASON=" + reason)
        print("H2AC_JOBS_IAM_COMPUTE_VPC_CLOUDRUN_WRITES=NONE")
        print("H2AC_H2_PRODUCTION=NO_GO")
        print("H2AC_DO_NOT_REPEAT=TRUE")
    return 0 if result == "PASS_EXACT_SCHEDULER_API_ENABLED" else 2

if __name__ == "__main__":
    sys.exit(main())
