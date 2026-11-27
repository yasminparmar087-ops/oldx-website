#!/usr/bin/env python3
"""BAJUTO/OLDX Step05 H2AD2: ONE NEW read-only reconciliation after H2AD1 IAM 400.

H2AD1 created and read back its dedicated probe SA, then attempted exactly one
Cloud Run setIamPolicy which returned HTTP400. Do not repeat H2AD1 or the IAM
write. This NEW one-shot reads only the exact service UID, exact created
service account UID, and direct service IAM to classify actual state.
No network/Compute, no Scheduler job, no IAM write, no automatic cleanup.
"""
from __future__ import annotations

import json
import os
import platform
import re
import ssl
import subprocess
import sys
from pathlib import Path
from urllib import error, request

ROOT = Path("/root")
PROJECT = "oldx-staging"
OWNER = "yasminparmar087@gmail.com"
SERVICE = "projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway"
SERVICE_UID = "2d87153f-155e-409f-a418-463c785d8467"
PROBE_SA = "oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
IMAGE = ("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
         "oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2")
CLI = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
PRIOR = ROOT / ".oldx-step05-h2ad1-probe-sa-and-exact-invoker-once-20261128"
MARKER = ROOT / ".oldx-step05-h2ad2-after-400-reconcile-readonly-once-20261128"
SERVICE_URL = "https://run.googleapis.com/v2/" + SERVICE
SA_URL = "https://iam.googleapis.com/v1/projects/" + PROJECT + "/serviceAccounts/" + PROBE_SA
POLICY_URL = SERVICE_URL + ":getIamPolicy"
ALLOWED = {SERVICE_URL, SA_URL, POLICY_URL}

class Stop(Exception):
    pass

def need(condition, reason):
    if not condition:
        raise Stop(reason)

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

OPENER = request.build_opener(
    request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect(),
)

def read_only(token, url):
    need(url in ALLOWED, "NEW_GET_OUTSIDE_EXACT_ALLOWLIST")
    req = request.Request(url, method="GET", headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "User-Agent": "BAJUTO-H2AD2-read-after-exact-IAM400-no-write/1",
    })
    try:
        with OPENER.open(req, timeout=35) as response:
            need(response.status == 200, "GET_UNEXPECTED_STATUS")
            raw = response.read(131073)
            need(len(raw) <= 131072, "GET_RESPONSE_TOO_LARGE")
    except error.HTTPError as exc:
        status = exc.code
        exc.close()
        raise Stop("EXACT_GET_HTTP_" + str(status))
    except (error.URLError, TimeoutError, ssl.SSLError):
        raise Stop("EXACT_GET_NETWORK_OR_TLS_STOP")
    doc = json.loads(raw)
    need(isinstance(doc, dict), "EXACT_GET_JSON_NOT_OBJECT")
    return doc

def get_token_and_expected_sa_uid():
    need(sys.argv[1:] == ["--h2ad2-after-h2ad1-http400-readonly-reconcile-once"],
         "EXACT_DIAGNOSTIC_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0 and
         "microsoft" in platform.release().lower(), "OWNER_ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(), "H2AD2_ALREADY_CONSUMED")
    need(PRIOR.is_file() and not PRIOR.is_symlink() and PRIOR.stat().st_uid == 0,
         "H2AD1_PRIOR_MARKER_NOT_PRESENT")
    lines = PRIOR.read_text(encoding="utf-8").splitlines()
    for line in (
        "ATTEMPT_CONSUMED=TRUE",
        "PROJECT=" + PROJECT,
        "SERVICE_UID=" + SERVICE_UID,
        "PROBE_SA=" + PROBE_SA,
        "GATEWAY_INVOKER_SET_ABOUT_TO_BE_SENT=TRUE",
    ):
        need(line in lines, "H2AD1_MARKER_EXPECTED_STATE_MISSING")
    need("RESULT=PASS_ONE_PROBE_SA_UID_AND_EXACT_GATEWAY_INVOKER" not in lines,
         "PRIOR_H2AD1_ALREADY_PASSED_UNEXPECTED")
    uid_lines = [s.split("=", 1)[1] for s in lines if s.startswith("SA_UID=")]
    need(len(uid_lines) == 1 and
         re.fullmatch(r"[0-9]{12,30}", uid_lines[0]) is not None,
         "H2AD1_CREATED_SA_UID_NOT_RECORDED")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI, os.X_OK) and
         PY.resolve(strict=True).is_file() and CONFIG.is_dir() and
         not CONFIG.is_symlink(), "ISOLATED_NATIVE_OWNER_SDK_MISSING")
    env = dict(os.environ)
    env.update({
        "HOME": str(ROOT), "CLOUDSDK_CONFIG": str(CONFIG),
        "CLOUDSDK_PYTHON": str(PY),
        "PATH": str(CLI.parent) + ":/usr/bin:/bin",
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
            stderr=subprocess.PIPE, timeout=35, check=False,
        )
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_OWNER_OAUTH_TIMEOUT")
    need(p.returncode == 0 and bool(p.stdout.strip()),
         "ISOLATED_OWNER_OAUTH_NOT_AVAILABLE")
    token = p.stdout.decode("utf-8", "strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", token) is not None,
         "OWNER_TOKEN_FORMAT_UNEXPECTED")
    return token, uid_lines[0]

def classify_policy(policy):
    bindings = policy.get("bindings", [])
    need(isinstance(bindings, list), "DIRECT_BINDINGS_NOT_LIST")
    etag = policy.get("etag")
    need(isinstance(etag, str) and bool(etag), "DIRECT_IAM_ETAG_MISSING")
    if len(bindings) != 1 or not isinstance(bindings[0], dict):
        return "OTHER_POLICY_NO_NEW_WRITE"
    binding = bindings[0]
    if binding.get("role") != "roles/run.invoker" or "condition" in binding:
        return "OTHER_POLICY_NO_NEW_WRITE"
    members = binding.get("members")
    if not isinstance(members, list) or len(set(members)) != len(members):
        return "OTHER_POLICY_NO_NEW_WRITE"
    if members == ["user:" + OWNER]:
        return "OWNER_ONLY_PROBE_NOT_GRANTED"
    if len(members) == 2 and set(members) == {
        "user:" + OWNER, "serviceAccount:" + PROBE_SA,
    }:
        return "OWNER_AND_EXACT_PROBE_GRANTED"
    return "OTHER_POLICY_NO_NEW_WRITE"

def main():
    os.umask(0o077)
    token, expected_sa_uid = get_token_and_expected_sa_uid()
    # Unique marker BEFORE the first new Google read. Never reset on STOP.
    fd = os.open(str(MARKER),
                 os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("ATTEMPT=H2AD2_DISTINCT_POST_HTTP400_READONLY_RECONCILIATION\n")
        f.write("PROJECT=" + PROJECT + "\n")
        f.write("SERVICE_UID=" + SERVICE_UID + "\n")
        f.write("EXPECTED_SA_UID=" + expected_sa_uid + "\n")
    print("H2AD2_MARKER=CONSUMED_NO_REPEAT", flush=True)

    service = read_only(token, SERVICE_URL)
    need(service.get("name") == SERVICE and service.get("uid") == SERVICE_UID,
         "TARGET_SERVICE_UID_DRIFT")
    need(service.get("ingress") == "INGRESS_TRAFFIC_INTERNAL_ONLY" and
         service.get("invokerIamDisabled", False) is False,
         "TARGET_INTERNAL_OR_INVOKER_ENFORCEMENT_DRIFT")
    template = service.get("template") or {}
    containers = template.get("containers") or []
    need(template.get("serviceAccount") ==
         "oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com" and
         len(containers) == 1 and
         isinstance(containers[0], dict) and
         containers[0].get("image") == IMAGE and
         ("OLDX_H2U_MODE", "OFF") in {
             (e.get("name"), e.get("value"))
             for e in containers[0].get("env", []) if isinstance(e, dict)
         }, "TARGET_IMAGE_OR_OFF_MODE_DRIFT")
    print("H2AD2_PRIVATE_GATEWAY_SAME_UID_INGRESS_OFF=VERIFIED")

    sa = read_only(token, SA_URL)
    need(sa.get("email") == PROBE_SA and
         str(sa.get("uniqueId")) == expected_sa_uid and
         sa.get("disabled") is not True,
         "EXACT_NEW_SA_IDENTITY_OR_STATE_UNEXPECTED")
    print("H2AD2_PROBE_SA=EXISTS_ENABLED_EXACT_UID_VERIFIED")
    print("H2AD2_PROBE_SA_UID=" + expected_sa_uid)

    policy = read_only(token, POLICY_URL)
    result = classify_policy(policy)
    print("H2AD2_DIRECT_GATEWAY_IAM=" + result)
    print("H2AD2_H2AD1_PRIOR_IAM_WRITE=HTTP_400_CAUSE_NOT_YET_PROVEN")
    print("H2AD2_SCHEDULER_JOB=NOT_CREATED_BY_THIS_SCRIPT")
    print("H2AD2_CLOUD_WRITES=NONE")
    print("H2AD2_NO_AUTOMATIC_PERMISSION_RETRY_OR_CLEANUP=TRUE")
    print("H2AD2_H2_PRODUCTION=NO_GO")
    print("H2AD2_DO_NOT_REPEAT=TRUE")
    print("H2AD2_RESULT=POST_HTTP400_READONLY_RECONCILIATION_PASS_WITH_LIMITS")

if __name__ == "__main__":
    try:
        main()
    except (Stop, OSError, ValueError, UnicodeError, TypeError, KeyError) as exc:
        print("H2AD2_RESULT=STOP_BEFORE_OR_DURING_POST_HTTP400_READONLY_GET")
        print("H2AD2_REASON=" +
              (str(exc) if isinstance(exc, Stop) else type(exc).__name__))
        print("H2AD2_CLOUD_WRITES=NONE")
        print("H2AD2_NO_IAM_RETRY_OR_CLEANUP=TRUE")
        print("H2AD2_H2_PRODUCTION=NO_GO")
        sys.exit(2)
