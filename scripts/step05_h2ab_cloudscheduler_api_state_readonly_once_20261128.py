#!/usr/bin/env python3
"""BAJUTO/OLDX H2AB: one NEW Cloud Scheduler API-state read after H2AA.
Zero Compute/VPC repeat, zero API enable/IAM/job/HTTP target writes.
"""
import json
import os
import platform
import ssl
import subprocess
import sys
from pathlib import Path
from urllib import request, error

ROOT = Path("/root")
OWNER = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
NUMBER = "38472235077"
CLI = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
PRIOR = ROOT / ".oldx-step05-h2aa-compute-state-permission-hint-once-20261128"
MARKER = ROOT / ".oldx-step05-h2ab-cloudscheduler-api-state-once-20261128"
SERVICE = "projects/" + NUMBER + "/services/cloudscheduler.googleapis.com"
URL = "https://serviceusage.googleapis.com/v1/" + SERVICE + "?fields=name%2Cstate"

class Stop(Exception):
    pass

def need(ok, why):
    if not ok:
        raise Stop(why)

def main():
    need(sys.argv[1:] == ["--h2ab-scheduler-api-state-readonly-once"],
         "EXACT_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(), "ROOT_WSL_REQUIRED")
    need(PRIOR.is_file() and not PRIOR.is_symlink() and PRIOR.stat().st_uid == 0,
         "H2AA_CONSUMED_MARKER_MISSING")
    old = PRIOR.read_text(encoding="utf-8").splitlines()
    need("ATTEMPT=H2AA_COMPUTE_API_STATE_AND_PERMISSION_HINTS" in old
         and "PROJECT=oldx-staging" in old, "H2AA_MARKER_WRONG_IDENTITY")
    need(not MARKER.exists() and not MARKER.is_symlink(),
         "H2AB_MARKER_CONSUMED_NO_RETRY")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI, os.X_OK)
         and PY.resolve(strict=True).is_file() and CONFIG.is_dir()
         and not CONFIG.is_symlink(), "ISOLATED_NATIVE_SDK_NOT_READY")
    env = dict(os.environ)
    env.update({"HOME": str(ROOT), "CLOUDSDK_CONFIG": str(CONFIG),
                "CLOUDSDK_PYTHON": str(PY), "PATH": str(CLI.parent) + ":/usr/bin:/bin",
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE", None)
    try:
        p = subprocess.run([str(CLI), "--quiet", "--account=" + OWNER,
                            "--project=" + PROJECT, "auth", "print-access-token"],
                           env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False, timeout=35)
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_OWNER_OAUTH_TIMEOUT")
    need(p.returncode == 0 and p.stdout.strip(), "OWNER_OAUTH_UNAVAILABLE")
    token = p.stdout.decode("utf-8", "strict").strip()
    need(40 < len(token) < 8192 and "\n" not in token, "TOKEN_FORMAT_INVALID")
    fd = os.open(str(MARKER), os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("ATTEMPT=H2AB_CLOUDSCHEDULER_API_STATE_READONLY\n")
        f.write("PROJECT=oldx-staging\nPREVIOUS=H2AA_COMPUTE_API_DISABLED\n")
    print("H2AB_MARKER=CONSUMED_NO_REPEAT")
    req = request.Request(URL, method="GET", headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "User-Agent": "OLDX-H2AB-only-one-new-Scheduler-ServiceUsage-GET/1"})
    class NoRedirect(request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None
    opener = request.build_opener(request.ProxyHandler({}),
        request.HTTPSHandler(context=ssl.create_default_context()), NoRedirect())
    try:
        with opener.open(req, timeout=35) as r:
            need(r.status == 200, "SERVICE_USAGE_STATUS_NOT_200")
            raw = r.read(8193)
            need(len(raw) <= 8192, "SERVICE_USAGE_RESPONSE_TOO_LARGE")
    except error.HTTPError as exc:
        code = exc.code
        exc.close()
        raise Stop("SERVICE_USAGE_HTTP_" + str(code))
    except (error.URLError, TimeoutError, ssl.SSLError):
        raise Stop("SERVICE_USAGE_NETWORK_OR_TLS_STOP")
    doc = json.loads(raw)
    need(isinstance(doc, dict) and doc.get("name") == SERVICE,
         "SERVICE_USAGE_PROJECT_OR_SERVICE_MISMATCH")
    state = doc.get("state")
    need(state in ("ENABLED", "DISABLED"), "SERVICE_USAGE_STATE_UNEXPECTED")
    print("H2AB_CLOUD_SCHEDULER_API=" + state)
    print("H2AB_SCHEDULER_JOB_IDENTITY_PERMISSIONS=NOT_QUERIED")
    print("H2AB_COMPUTE_API_AND_VPC=NOT_TOUCHED")
    print("H2AB_SCHEDULER_JOBS=NOT_CREATED_OR_RUN")
    print("H2AB_API_ENABLE_IAM_CLOUD_WRITES=NONE")
    print("H2AB_HOSTED_HTTP=NOT_TESTED")
    print("H2AB_H2_PRODUCTION=NO_GO")
    print("H2AB_DO_NOT_REPEAT=TRUE")
    print("H2AB_RESULT=ONE_NEW_SCHEDULER_API_STATE_READ_PASS_WITH_LIMITS")

if __name__ == "__main__":
    try:
        main()
    except (Stop, OSError, ValueError, TypeError, UnicodeError) as exc:
        print("H2AB_RESULT=STOP_BEFORE_OR_DURING_NEW_READ_ONLY_GET")
        print("H2AB_REASON=" + (str(exc) if isinstance(exc, Stop) else type(exc).__name__))
        print("H2AB_CLOUD_WRITES=NONE")
        print("H2AB_DO_NOT_REPEAT_IF_MARKER_EXISTS=TRUE")
        print("H2AB_H2_PRODUCTION=NO_GO")
        sys.exit(2)
