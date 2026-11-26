#!/usr/bin/env python3
"""OLDX Step05 H2K: one OWNER-APPROVED KMS API enable, UID-bound project guard.

EXPLICIT scope: enable ONLY cloudkms.googleapis.com in oldx-staging.
No KMS key/keyring/version, IAM policy, Run, Firestore/Auth, Storage or H2 enable.
Uses the isolated owner WSL gcloud solely to obtain short-lived OAuth in memory.
Read-only fresh preflight -> ONE Service Usage services.enable POST -> bounded
operation polling -> exact filtered state readback. Never retry the POST.
Do not rerun this one-shot after marker consumption even on timeout or failure.
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
from urllib import error, request

ROOT = Path("/root")
PROJECT = "oldx-staging"
PROJECT_NUMBER = "38472235077"
OWNER = "yasminparmar087@gmail.com"
SERVICE = "cloudkms.googleapis.com"
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2F = ROOT / ".oldx-step05-h2-exact-two-states-fields-only-once-20261126"
MARKER = ROOT / ".oldx-step05-h2-kms-api-enable-owner-once-20261127"
BASE = f"https://serviceusage.googleapis.com/v1/projects/{PROJECT_NUMBER}/services/{SERVICE}"
GET_STATE = BASE + "?fields=name%2Cstate"
ENABLE = BASE + ":enable"
OP_BASE = "https://serviceusage.googleapis.com/v1/operations/"
ALLOWED_METHODS = {("GET", GET_STATE), ("POST", ENABLE)}

class Stop(Exception):
    pass

def require(ok, why):
    if not ok:
        raise Stop(why)

def gcloud(env, args):
    try:
        p = subprocess.run([str(CLI)] + args, env=env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=25, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_GCLOUD_TIMEOUT") from None
    require(p.returncode == 0, "ISOLATED_GCLOUD_FAILED")
    return p.stdout.decode("utf-8", "replace").strip()

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

OPENER = request.build_opener(
    request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect(),
)

def rest(method, url, token):
    operation = (method == "GET" and url.startswith(OP_BASE)
       and bool(re.fullmatch(re.escape(OP_BASE)
                            + r"[A-Za-z0-9._-]{6,200}", url)))
    require((method, url) in ALLOWED_METHODS or operation,
            "URL_OR_METHOD_OUTSIDE_APPROVED_SCOPE")
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "User-Agent": "OLDX-H2K-approved-KMS-API-only/1",
    }
    data = None
    if method == "POST":
        # services.enable expects an empty request body, no KMS key parameters.
        data = b""
        headers["Content-Type"] = "application/json"
    try:
        with OPENER.open(request.Request(
                url, headers=headers, method=method, data=data),
                timeout=35) as response:
            raw = response.read(8193)
            require(response.status == 200 and len(raw) <= 8192,
                    "UNEXPECTED_SERVICE_USAGE_RESPONSE")
            obj = json.loads(raw)
            require(isinstance(obj, dict), "SERVICE_USAGE_SCHEMA")
            return 200, obj
    except error.HTTPError as exc:
        status = exc.code
        exc.close()
        return status, {}
    except (error.URLError, TimeoutError, ssl.SSLError):
        raise Stop("SERVICE_USAGE_NETWORK_OR_TIMEOUT") from None

def state(token):
    status, obj = rest("GET", GET_STATE, token)
    require(status == 200, "API_STATE_GET_HTTP_" + str(status))
    require(obj.get("name") ==
            f"projects/{PROJECT_NUMBER}/services/{SERVICE}",
            "API_STATE_PROJECT_OR_SERVICE_MISMATCH")
    value = obj.get("state")
    require(value in ("ENABLED", "DISABLED"), "API_STATE_UNRECOGNIZED")
    return value

def preflight():
    require(sys.argv[1:] == ["--approved-single-kms-api-enable-once"],
            "EXACT_FLAG_REQUIRED")
    require(platform.system() == "Linux" and os.geteuid() == 0
            and "microsoft" in platform.release().lower(),
            "OWNER_ROOT_WSL_REQUIRED")
    require(not MARKER.exists() and not MARKER.is_symlink(),
            "H2K_ONESHOT_ALREADY_CONSUMED")
    require(H2F.is_file() and not H2F.is_symlink()
            and H2F.stat().st_uid == 0,
            "H2F_RECEIPT_NOT_TRUSTED")
    lines = H2F.read_text(encoding="utf-8").splitlines()
    require("ATTEMPT_CONSUMED=TRUE" in lines
            and "RESULT=EXACT_TWO_API_STATES_FIELDS_ONLY_WITH_LIMITS" in lines,
            "H2F_ACTUAL_PASS_NOT_CONFIRMED")
    entries = [s[9:] for s in lines if s.startswith("EVIDENCE=")]
    require(len(entries) == 1, "H2F_EVIDENCE_PATH_UNKNOWN")
    evid = Path(entries[0])
    require(evid.parent == ROOT
            and bool(re.fullmatch(r"oldx-h2-two-fields-only-\d{8}T\d{6}Z", evid.name))
            and evid.is_dir() and not evid.is_symlink()
            and evid.stat().st_uid == 0, "H2F_EVIDENCE_DIR_INVALID")
    evidence = evid / "sanitized-h2-fields-only.json"
    require(evidence.is_file() and not evidence.is_symlink()
            and evidence.stat().st_uid == 0 and evidence.stat().st_size <= 8192,
            "H2F_EVIDENCE_FILE_INVALID")
    doc = json.loads(evidence.read_text(encoding="utf-8"))
    require(isinstance(doc, dict) and doc.get("project") == PROJECT
            and doc.get("api_states", {}).get(SERVICE) == "API_DISABLED"
            and doc.get("api_states", {}).get("identitytoolkit.googleapis.com") == "API_ENABLED",
            "H2F_FROZEN_API_STATUS_MISMATCH")
    require(SDK.is_dir() and not SDK.is_symlink()
            and SDK.stat().st_uid == 0, "NATIVE_SDK_UNVERIFIED")
    require(CLI.is_file() and not CLI.is_symlink()
            and CLI.stat().st_uid == 0 and os.access(CLI, os.X_OK),
            "NATIVE_CLI_UNVERIFIED")
    python = PY.resolve(strict=True)
    require(python.is_relative_to(SDK.resolve(strict=True))
            and python.is_file() and python.stat().st_uid == 0
            and os.access(python, os.X_OK), "NATIVE_PYTHON_UNVERIFIED")
    require(CONFIG.is_dir() and not CONFIG.is_symlink()
            and CONFIG.stat().st_uid == 0, "ISOLATED_CONFIG_UNVERIFIED")
    env = dict(os.environ)
    env.update({
        "HOME": str(ROOT),
        "PATH": str(SDK / "bin") + ":/usr/bin:/bin",
        "CLOUDSDK_CONFIG": str(CONFIG),
        "CLOUDSDK_PYTHON": str(PY),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false",
    })
    env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE", None)
    require(gcloud(env, ["auth", "list", "--filter=status:ACTIVE",
                         "--format=value(account)"]) == OWNER,
            "WRONG_ACTIVE_OWNER")
    require(gcloud(env, ["config", "get-value", "project"]) == PROJECT,
            "WRONG_ISOLATED_PROJECT")
    token = gcloud(env, ["--quiet", "--account=" + OWNER,
                          "auth", "print-access-token"])
    require(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", token)),
            "ISOLATED_OWNER_TOKEN_UNAVAILABLE")
    return token

def write_marker_line(s):
    with MARKER.open("a", encoding="utf-8") as out:
        out.write(s + "\n")

def main():
    os.umask(0o077)
    try:
        token = preflight()
        initial = state(token)  # Fresh KMS-only guard before the authorized write.
    except (Stop, OSError, ValueError, UnicodeError, TypeError, KeyError) as exc:
        print("OLDX_H2K_RESULT=STOP_BEFORE_ENABLE")
        print("OLDX_H2K_REASON=" + (str(exc) if isinstance(exc, Stop)
              else type(exc).__name__))
        print("OLDX_H2K_ENABLE_ATTEMPTED=FALSE")
        return 2

    if initial == "ENABLED":
        print("OLDX_H2K_RESULT=ALREADY_ENABLED_NO_WRITE")
        print("OLDX_H2K_REASON=FRESH_KMS_STATE_ENABLED")
        print("OLDX_H2K_ENABLE_ATTEMPTED=FALSE")
        print("OLDX_H2K_H2_ENABLED=NOT_ATTEMPTED")
        return 0
    require(initial == "DISABLED", "FRESH_KMS_STATE_NOT_DISABLED")

    evidence = ROOT / ("oldx-h2k-kms-api-owner-enable-"
                       + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd = os.open(MARKER, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                     | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE=" + str(evidence)
                      + "\nPROJECT=" + PROJECT + "\nSERVICE=" + SERVICE + "\n")
    except OSError:
        print("OLDX_H2K_RESULT=STOP_MARKER")
        return 2

    final = "STOP_AFTER_MARKER"
    reason = "UNKNOWN"
    state_after = "NOT_VERIFIED"
    operation = "NOT_OBTAINED"
    attempted = False
    try:
        print("OLDX_H2K_STAGE=ONE_OWNER_APPROVED_KMS_API_ENABLE_ATTEMPT", flush=True)
        write_marker_line("ENABLE_REQUEST_ABOUT_TO_BE_SENT=TRUE")
        attempted = True
        status, body = rest("POST", ENABLE, token)
        require(status == 200, "KMS_API_ENABLE_HTTP_" + str(status))
        name = body.get("name")
        require(isinstance(name, str)
                and bool(re.fullmatch(r"operations/[A-Za-z0-9._-]{6,200}", name)),
                "KMS_ENABLE_OPERATION_ID_INVALID")
        operation = name
        write_marker_line("OPERATION_NAME=" + name)

        # One enable operation only. Polling is GET, never another enable.
        done = False
        for _ in range(12):
            code, item = rest("GET",
                             "https://serviceusage.googleapis.com/v1/" + name,
                             token)
            require(code == 200, "KMS_OPERATION_GET_HTTP_" + str(code))
            if item.get("done") is True:
                require(not item.get("error"), "KMS_ENABLE_OPERATION_ERROR")
                done = True
                break
            time.sleep(3)
        require(done, "KMS_OPERATION_NOT_COMPLETE_IN_BOUNDED_WINDOW")
        state_after = state(token)
        require(state_after == "ENABLED", "KMS_ENABLE_READBACK_NOT_ENABLED")
        final = "PASS_KMS_API_ENABLED_EXACT_PROJECT_VERIFIED"
        reason = "ONE_ENABLE_OPERATION_DONE_AND_KMS_ONLY_READBACK_ENABLED"
    except (Stop, OSError, ValueError, UnicodeError, TypeError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
        # A partially completed POST can still succeed in Google Cloud.
        # Do not retry; report this attempt as ambiguous if not verified.
    finally:
        try:
            data = {
                "project": PROJECT, "project_number": PROJECT_NUMBER,
                "service": SERVICE, "initial_state": initial,
                "enable_attempted": attempted, "operation_name": operation,
                "verified_final_state": state_after,
                "result": final, "reason": reason,
                "key_ring_or_key_created": False,
                "iam_or_other_cloud_resource_changed_by_this_script": False,
                "h2": "NO_GO", "production": "NO_GO",
            }
            (evidence / "sanitized-kms-api-enablement.json").write_text(
                json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            write_marker_line("RESULT=" + final)
            write_marker_line("REASON=" + reason)
        except OSError:
            final = "STOP_EVIDENCE_WRITE"
        print("OLDX_H2K_PROJECT=" + PROJECT)
        print("OLDX_H2K_SERVICE=" + SERVICE)
        print("OLDX_H2K_ENABLE_ATTEMPTED=" + str(attempted).upper())
        print("OLDX_H2K_RESULT=" + final)
        print("OLDX_H2K_REASON=" + reason)
        print("OLDX_H2K_FINAL_KMS_API_STATE=" + state_after)
        print("OLDX_H2K_OTHER_RESOURCES_IAM_KEYS=NOT_CHANGED_BY_SCRIPT")
        print("OLDX_H2K_H2_ENABLED=NOT_ATTEMPTED")
        print("OLDX_H2K_DO_NOT_REPEAT=TRUE")
    return 0 if final == "PASS_KMS_API_ENABLED_EXACT_PROJECT_VERIFIED" else 2

if __name__ == "__main__":
    sys.exit(main())
