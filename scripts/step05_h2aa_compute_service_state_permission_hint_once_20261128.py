#!/usr/bin/env python3
"""BAJUTO Step05 H2AA: two NEW metadata-only diagnostics after H2Z VPC HTTP403.
Never replay H2Z IAM/network requests, enable Compute API, or grant permissions.
Service Usage GET is an enabled/disabled check; project testIamPermissions is a
hint, not proof of network resource-specific or ancestor/effective permissions.
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
PROJECT = "oldx-staging"
NUMBER = "38472235077"
OWNER = "yasminparmar087@gmail.com"
OLD = ROOT / ".oldx-step05-h2z-project-iam-vpc-readonly-once-20261128"
MARK = ROOT / ".oldx-step05-h2aa-compute-state-permission-hint-once-20261128"
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
API_NAME = "projects/" + NUMBER + "/services/compute.googleapis.com"
STATE_URL = ("https://serviceusage.googleapis.com/v1/" + API_NAME
             + "?fields=name%2Cstate")
PERMISSION_URL = ("https://cloudresourcemanager.googleapis.com/v1/projects/"
                  + PROJECT + ":testIamPermissions")
PERMS = ("compute.networks.list", "compute.subnetworks.list")

class Stop(Exception):
    pass

def need(condition, reason):
    if not condition:
        raise Stop(reason)

def owner_token():
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(), "ROOT_WSL_REQUIRED")
    need(OLD.is_file() and not OLD.is_symlink() and OLD.stat().st_uid == 0,
         "H2Z_ONE_SHOT_MARKER_MISSING")
    r = OLD.read_text(encoding="utf-8").splitlines()
    for required in ("ATTEMPT=H2Z_THREE_DISTINCT_READONLY_METADATA_METHODS",
                     "PROJECT=oldx-staging",
                     "H2W_SERVICE_UID=2d87153f-155e-409f-a418-463c785d8467"):
        need(required in r, "H2Z_MARKER_IDENTITY_MISMATCH")
    need(not MARK.exists() and not MARK.is_symlink(), "H2AA_ALREADY_CONSUMED")
    need(SDK.is_dir() and not SDK.is_symlink()
         and CLI.is_file() and not CLI.is_symlink() and os.access(CLI, os.X_OK),
         "ISOLATED_NATIVE_CLI_MISSING")
    need(PY.resolve(strict=True).is_file() and CONFIG.is_dir()
         and not CONFIG.is_symlink(), "ISOLATED_SDK_AUTH_MISSING")
    env = dict(os.environ)
    env.update({"HOME": str(ROOT), "PATH": str(CLI.parent) + ":/usr/bin:/bin",
                "CLOUDSDK_CONFIG": str(CONFIG), "CLOUDSDK_PYTHON": str(PY),
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE", None)
    try:
        result = subprocess.run(
            [str(CLI), "--quiet", "--account=" + OWNER, "--project=" + PROJECT,
             "auth", "print-access-token"], env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=35, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("NATIVE_GCLOUD_AUTH_TIMEOUT")
    need(result.returncode == 0 and result.stdout.strip(), "OWNER_TOKEN_UNAVAILABLE")
    token = result.stdout.decode("utf-8", "strict").strip()
    need(40 < len(token) < 8192 and "\n" not in token, "INVALID_OWNER_TOKEN")
    return token

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

OPENER = request.build_opener(
    request.ProxyHandler({}), request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect(),
)

def call(token, url, method, data=None):
    need(url in (STATE_URL, PERMISSION_URL), "URL_OUT_OF_ALLOWLIST")
    need((url == STATE_URL and method == "GET" and data is None) or
         (url == PERMISSION_URL and method == "POST" and data is not None),
         "METHOD_NOT_READONLY_ALLOWLISTED")
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json",
               "User-Agent": "OLDX-H2AA-two-new-readonly-diagnostics/1"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = request.Request(
        url, method=method, headers=headers,
        data=json.dumps(data, separators=(",", ":")).encode("utf-8")
             if data is not None else None)
    try:
        with OPENER.open(req, timeout=35) as response:
            need(response.status == 200, "UNEXPECTED_HTTP_STATUS")
            raw = response.read(8193)
            need(len(raw) <= 8192, "PARTIAL_RESPONSE_TOO_LARGE")
    except error.HTTPError as exc:
        code = exc.code
        exc.close()
        raise Stop("HTTP_" + str(code))
    except (error.URLError, TimeoutError, ssl.SSLError):
        raise Stop("API_NETWORK_OR_TLS_FAILURE")
    obj = json.loads(raw)
    need(isinstance(obj, dict), "JSON_RESPONSE_NOT_OBJECT")
    return obj

def main():
    need(sys.argv[1:] == ["--h2aa-compute-state-and-two-permission-hints-readonly-once"],
         "EXACT_USER_FLAG_REQUIRED")
    token = owner_token()
    # Consume unique marker before the first new remote API call.
    fd = os.open(str(MARK), os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        out.write("ATTEMPT=H2AA_COMPUTE_API_STATE_AND_PERMISSION_HINTS\n")
        out.write("PROJECT=oldx-staging\nPREVIOUS=H2Z_PARTIAL_NETWORK_HTTP403\n")
    print("H2AA_MARKER=CONSUMED_NO_REPEAT")
    service = call(token, STATE_URL, "GET")
    need(service.get("name") == API_NAME, "COMPUTE_SERVICE_IDENTITY_DRIFT")
    state = service.get("state")
    need(state in ("ENABLED", "DISABLED"), "COMPUTE_SERVICE_STATE_UNKNOWN")
    print("H2AA_COMPUTE_API=" + state)
    if state == "DISABLED":
        print("H2AA_PERMISSION_HINTS=NOT_QUERIED_API_DISABLED")
        print("H2AA_VPC_403=CONSISTENT_WITH_DISABLED_API_NOT_CONCLUSIVE")
    else:
        rights = call(token, PERMISSION_URL, "POST", {"permissions": list(PERMS)})
        p = rights.get("permissions", [])
        need(isinstance(p, list) and all(isinstance(x, str) for x in p)
             and set(p).issubset(set(PERMS)), "UNEXPECTED_PERMISSION_HINTS")
        for perm in PERMS:
            print("H2AA_" + perm.upper().replace(".", "_") + "_PROJECT_HINT=" +
                  ("RETURNED" if perm in p else "NOT_RETURNED"))
        print("H2AA_VPC_403=CAUSE_UNRESOLVED_PROJECT_HINTS_ONLY")
    print("H2AA_VPC_INVENTORY=NOT_REPEATED")
    print("H2AA_NO_NEW_PERMISSION_GRANTS_API_ENABLE_OR_CLOUD_WRITES=TRUE")
    print("H2AA_EFFECTIVE_IAM_PRIVATE_ROUTING_HOSTED_HTTP=NOT_VERIFIED")
    print("H2AA_H2_PRODUCTION=NO_GO")
    print("H2AA_DO_NOT_REPEAT=TRUE")
    print("H2AA_RESULT=SERVICE_STATE_AND_OPTIONAL_PROJECT_PERMISSION_HINTS_PASS_WITH_LIMITS")

if __name__ == "__main__":
    try:
        main()
    except (Stop, OSError, ValueError, TypeError, UnicodeError, KeyError) as exc:
        print("H2AA_RESULT=STOP_BEFORE_OR_DURING_NEW_READONLY_DIAGNOSTICS")
        print("H2AA_REASON=" + (str(exc) if isinstance(exc, Stop) else type(exc).__name__))
        print("H2AA_NO_COMPUTE_ENABLE_OR_IAM_WRITES=TRUE")
        print("H2AA_DO_NOT_REPEAT_IF_MARKER_EXISTS=TRUE")
        print("H2AA_H2_PRODUCTION=NO_GO")
        sys.exit(2)
