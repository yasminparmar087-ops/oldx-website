#!/usr/bin/env python3
"""BAJUTO/OLDX H2AD6B — first actual Scheduler /healthz run after H2AD6
pre-dispatch STOP caused by status field presence alone.

Never replay H2AD6. Fail closed unless PAUSED, exact read-only OIDC target,
no lastAttemptTime, no prior H2AD6 marker, and optional status is only
the empty / google.rpc.OK default status (without message/details).
Only ONE jobs.run call; no job resume, job create, IAM, or automatic cleanup.
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
from pathlib import Path
from urllib import request, error

ROOT = Path("/root")
PROJECT = "oldx-staging"
OWNER = "yasminparmar087@gmail.com"
JOB = "projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128"
SERVICE_UID = "2d87153f-155e-409f-a418-463c785d8467"
PROBE_SA = "oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
PROBE_SA_UID = "110217058111344002447"
JURL = "https://cloudscheduler.googleapis.com/v1/" + JOB
RUN_URL = JURL + ":run"
H2AD5 = ROOT / ".oldx-step05-h2ad5-new-single-job-create-pause-once-20261128"
OLD_H2AD6 = ROOT / ".oldx-step05-h2ad6-one-manual-paused-job-dispatch-once-20261128"
MARK = ROOT / ".oldx-step05-h2ad6b-status-aware-manual-health-run-once-20261128"
CLI = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"

class Stop(Exception):
    pass

def need(ok, reason):
    if not ok:
        raise Stop(reason)

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

OPENER = request.build_opener(
    request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()), NoRedirect())

def api(method, url, token):
    need((method == "GET" and url == JURL) or
         (method == "POST" and url == RUN_URL),
         "ONLY_EXACT_JOB_GET_OR_ONE_RUN_ALLOWED")
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "User-Agent": "BAJUTO-H2AD6B-status-aware-one-OFF-health-run/1",
    }
    # RunJobRequest has no fields, use an empty body, not an application payload.
    req = request.Request(url, method=method, headers=headers,
                          data=b"" if method == "POST" else None)
    try:
        with OPENER.open(req, timeout=35) as resp:
            need(resp.status == 200, "JOB_API_UNEXPECTED_SUCCESS_STATUS")
            raw = resp.read(65537)
            need(len(raw) <= 65536, "JOB_RESPONSE_SIZE_CAP")
    except error.HTTPError as exc:
        code = exc.code
        exc.close()
        raise Stop("JOB_API_HTTP_" + str(code) + "_NO_RETRY")
    except (error.URLError, ssl.SSLError, TimeoutError):
        raise Stop("JOB_API_NETWORK_OR_TIMEOUT_NO_RETRY")
    obj = json.loads(raw)
    need(isinstance(obj, dict), "JOB_RESPONSE_NOT_JSON_OBJECT")
    return obj

def prior():
    need(sys.argv[1:] == ["--h2ad6b-owner-approved-status-aware-one-health-run-once"],
         "EXACT_OWNER_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0 and
         "microsoft" in platform.release().lower(), "ROOT_UBUNTU_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(), "H2AD6B_ALREADY_CONSUMED")
    # Original H2AD6 STOP was before its one-dispatch marker. If the marker
    # exists, any dispatch outcome is unknown: never dispatch through recovery.
    need(not OLD_H2AD6.exists() and not OLD_H2AD6.is_symlink(),
         "ORIGINAL_H2AD6_MARKER_EXISTS_UNKNOWN_DISPATCH_NO_NEW_RUN")
    need(H2AD5.is_file() and not H2AD5.is_symlink() and
         H2AD5.stat().st_uid == 0, "H2AD5_JOB_PAUSE_MARKER_NOT_TRUSTED")
    lines = H2AD5.read_text(encoding="utf-8").splitlines()
    for item in (
        "ATTEMPT_CONSUMED=TRUE",
        "PROJECT=" + PROJECT,
        "SERVICE_UID=" + SERVICE_UID,
        "PROBE_SA_UID=" + PROBE_SA_UID,
        "JOB=" + JOB,
        "JOB_CREATE_ABOUT_TO_BE_SENT=TRUE",
        "JOB_PAUSE_ABOUT_TO_BE_SENT=TRUE",
    ):
        need(item in lines, "H2AD5_PRIOR_OWNER_IDENTITY_OR_PHASE_MISMATCH")
    bases = [x[len("TARGET_BASE="):] for x in lines
             if x.startswith("TARGET_BASE=")]
    need(len(bases) == 1 and re.fullmatch(
        r"https://[A-Za-z0-9.-]+\.run\.app", bases[0]) is not None,
        "H2AD5_TARGET_BASE_NOT_EXACT_HTTPS_RUN_APP")
    need(CLI.is_file() and not CLI.is_symlink() and
         os.access(CLI, os.X_OK) and PY.resolve(strict=True).is_file()
         and CONFIG.is_dir() and not CONFIG.is_symlink(),
         "ISOLATED_OWNER_NATIVE_SDK_NOT_READY")
    env = dict(os.environ)
    env.update({
        "HOME": str(ROOT), "PATH": str(CLI.parent) + ":/usr/bin:/bin",
        "CLOUDSDK_CONFIG": str(CONFIG), "CLOUDSDK_PYTHON": str(PY),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false",
    })
    env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE", None)
    try:
        p = subprocess.run(
            [str(CLI), "--quiet", "--account=" + OWNER,
             "--project=" + PROJECT, "auth", "print-access-token"],
            env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=35, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_OWNER_OAUTH_TIMEOUT")
    need(p.returncode == 0 and bool(p.stdout.strip()),
         "ISOLATED_OWNER_OAUTH_UNAVAILABLE")
    token = p.stdout.decode("utf-8", "strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", token) is not None,
         "OWNER_TOKEN_INVALID_FORMAT")
    return token, bases[0]

def inspect(job, base):
    need(job.get("name") == JOB and job.get("state") == "PAUSED",
         "JOB_NOT_EXACT_PAUSED")
    need(job.get("schedule") == "0 0 29 2 *" and
         job.get("timeZone") in ("Etc/UTC", "UTC") and
         job.get("attemptDeadline") == "30s", "JOB_SCHEDULE_DRIFT")
    target = job.get("httpTarget") or {}
    oidc = target.get("oidcToken") or {}
    need(target.get("uri") == base + "/healthz" and
         target.get("httpMethod") == "GET" and
         oidc.get("serviceAccountEmail") == PROBE_SA and
         oidc.get("audience") == base,
         "JOB_READONLY_ENDPOINT_OR_OIDC_IDENTITY_DRIFT")
    retry = job.get("retryConfig") or {}
    need(retry.get("retryCount", 0) == 0 and
         retry.get("maxRetryDuration", "0s") in ("0s", None),
         "JOB_RETRY_POLICY_DRIFT")

def benign_unattempted_status(job):
    # A nonempty status field is NOT by itself evidence of a prior attempt.
    # But an actual failure, message, details or recorded lastAttemptTime
    # cannot be dismissed merely because the job has the expected target.
    need(not job.get("lastAttemptTime"), "LAST_ATTEMPT_PRESENT_NO_DISPATCH")
    status = job.get("status", {})
    need(isinstance(status, dict), "SCHEDULER_STATUS_NOT_OBJECT")
    category = "OMITTED_OR_EMPTY" if not status else "DEFAULT_OK_NO_MESSAGE"
    need(set(status.keys()).issubset({"code", "message", "details"}),
         "STATUS_HAS_UNEXPECTED_FIELDS_ABORT")
    code = status.get("code", 0)
    need(isinstance(code, int) and not isinstance(code, bool) and code == 0,
         "NONZERO_OR_UNEXPECTED_PREVIOUS_STATUS_CODE_ABORT")
    need(status.get("message", "") in ("", None),
         "PREEXISTING_NONEMPTY_STATUS_MESSAGE_ABORT")
    need(status.get("details", []) in ([], None),
         "PREEXISTING_STATUS_DETAILS_ABORT")
    return category

def main():
    os.umask(0o077)
    token, base = prior()
    job = api("GET", JURL, token)
    inspect(job, base)
    category = benign_unattempted_status(job)
    print("H2AD6B_PREEXISTING_STATUS_CATEGORY=" + category)
    print("H2AD6B_LAST_ATTEMPT=ABSENT")
    # Mark BEFORE sole allowed write; if any error after this line do not retry.
    fd = os.open(str(MARK), os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT=" + PROJECT +
                "\nJOB=" + JOB + "\nSERVICE_UID=" + SERVICE_UID +
                "\nPROBE_SA_UID=" + PROBE_SA_UID + "\n")
        f.write("TARGET_BASE=" + base + "\nONE_RUN_ABOUT_TO_BE_SENT=TRUE\n")
    print("H2AD6B_MARKER=CONSUMED_NO_REPEAT", flush=True)
    print("H2AD6B_STAGE=ONE_PAUSED_HEALTHZ_MANUAL_RUN", flush=True)
    accepted = api("POST", RUN_URL, token)
    need(accepted.get("name") == JOB,
         "MANUAL_RUN_ACCEPTED_RESPONSE_NOT_EXACT_JOB_NO_RETRY")
    print("H2AD6B_ONE_MANUAL_RUN_API=HTTP_200_ACCEPTED", flush=True)
    # Read-only observation may lag. It is NOT the target HTTP result.
    latest = {}
    for _ in range(5):
        time.sleep(2)
        latest = api("GET", JURL, token)
        inspect(latest, base)
        if latest.get("lastAttemptTime"):
            break
    status = latest.get("status") or {}
    code = status.get("code", "UNKNOWN_OR_PENDING") if isinstance(status, dict) else "UNKNOWN"
    if isinstance(code, bool) or not isinstance(code, (str, int)):
        code = "UNEXPECTED"
    print("H2AD6B_JOB_REMAINS_PAUSED=VERIFIED")
    print("H2AD6B_LAST_ATTEMPT_PRESENT=" +
          str(bool(latest.get("lastAttemptTime"))).upper())
    print("H2AD6B_STATUS_CODE=" + str(code))
    print("H2AD6B_TARGET_HTTP_200_AND_BODY=NOT_INDEPENDENTLY_VERIFIED")
    print("H2AD6B_NEXT=READ_SCHEDULER_DELIVERY_AND_CLOUD_RUN_SERVER_LOGS")
    print("H2AD6B_IAM_SA_JOB_CLEANUP=NOT_ATTEMPTED")
    print("H2AD6B_CLOUD_WRITES=ONE_JOBS_RUN_ONLY")
    print("H2AD6B_H2_PRODUCTION=NO_GO")
    print("H2AD6B_DO_NOT_REPEAT=TRUE")
    print("H2AD6B_RESULT=ONE_PAUSED_MANUAL_RUN_ACCEPTED_WITH_LIMITS")

if __name__ == "__main__":
    try:
        main()
    except (Stop, OSError, ValueError, TypeError, UnicodeError, KeyError) as exc:
        print("H2AD6B_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_ONE_RUN")
        print("H2AD6B_REASON=" +
              (str(exc) if isinstance(exc, Stop) else type(exc).__name__))
        print("H2AD6B_ACTION=DO_NOT_REPEAT_OR_RESUME_OR_AUTOCLEANUP")
        print("H2AD6B_H2_PRODUCTION=NO_GO")
        sys.exit(2)
