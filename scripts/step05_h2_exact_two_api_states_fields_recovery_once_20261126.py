#!/usr/bin/env python3
"""OLDX H2F: one NEW bounded partial-response API state recovery.

PREVIOUS H2E was consumed and STOPPED on UNEXPECTED_SERVICE_USAGE_RESPONSE,
probably due to the strict 64 KiB raw response cap. Never run H2E again.
This performs only two NEW Google Service Usage GETs with fields=name,state.
No service enablement, IAM changes, key material, Auth/user data, or deploy.
"""
from __future__ import annotations

import json
import os
import platform
import re
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error

PROJECT = "oldx-staging"
NUMBER = "38472235077"
OWNER = "yasminparmar087@gmail.com"
ROOT = Path("/root")
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
PRIOR = ROOT / ".oldx-step05-h2-exact-api-enablement-get-once-20261126"
MARKER = ROOT / ".oldx-step05-h2-exact-two-states-fields-only-once-20261126"
BASE = f"https://serviceusage.googleapis.com/v1/projects/{NUMBER}/services/"
APIS = ("cloudkms.googleapis.com", "identitytoolkit.googleapis.com")
# Standard Google API partial-response selector: request only two small fields.
URLS = {name: BASE + name + "?fields=name%2Cstate" for name in APIS}

class Stop(Exception):
    pass

def require(ok, message):
    if not ok:
        raise Stop(message)

def gcloud(env, args):
    try:
        result = subprocess.run(
            [str(CLI)] + args, env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=25, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("NATIVE_GCLOUD_TIMEOUT") from None
    require(result.returncode == 0, "NATIVE_GCLOUD_FAILED")
    return result.stdout.decode("utf-8", "replace").strip()

def owner_token():
    require(sys.argv[1:] == ["--h2-two-api-states-fields-only-once"],
            "EXACT_FLAG_REQUIRED")
    require(platform.system() == "Linux" and os.geteuid() == 0
            and "microsoft" in platform.release().lower(),
            "ROOT_OWNER_WSL_REQUIRED")
    require(not MARKER.exists() and not MARKER.is_symlink(),
            "H2F_MARKER_ALREADY_CONSUMED")
    require(PRIOR.is_file() and not PRIOR.is_symlink()
            and PRIOR.stat().st_uid == 0, "PRIOR_H2E_RECEIPT_NOT_TRUSTED")
    prior = PRIOR.read_text(encoding="utf-8").splitlines()
    require("ATTEMPT_CONSUMED=TRUE" in prior
            and "RESULT=STOP_AFTER_MARKER" in prior
            and "REASON=UNEXPECTED_SERVICE_USAGE_RESPONSE" in prior,
            "PRIOR_H2E_EXACT_STOP_NOT_VERIFIED")
    require(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid == 0,
            "NATIVE_SDK_UNVERIFIED")
    require(CLI.is_file() and not CLI.is_symlink()
            and CLI.stat().st_uid == 0 and os.access(CLI, os.X_OK),
            "NATIVE_GCLOUD_UNVERIFIED")
    python = PY.resolve(strict=True)
    require(python.is_relative_to(SDK.resolve(strict=True)) and python.is_file()
            and python.stat().st_uid == 0 and os.access(python, os.X_OK),
            "NATIVE_PYTHON_UNVERIFIED")
    require(CONFIG.is_dir() and not CONFIG.is_symlink()
            and CONFIG.stat().st_uid == 0, "ISOLATED_CONFIG_UNVERIFIED")

    env = dict(os.environ)
    env.update({
        "HOME": str(ROOT),
        "PATH": f"{SDK}/bin:/usr/bin:/bin",
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
            "WRONG_OWNER_PRINCIPAL")
    require(gcloud(env, ["config", "get-value", "project"]) == PROJECT,
            "WRONG_ISOLATED_PROJECT")
    token = gcloud(env, ["--quiet", "--account=" + OWNER,
                         "auth", "print-access-token"])
    require(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", token)),
            "OWNER_OAUTH_TOKEN_UNAVAILABLE")
    return token

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

OPENER = request.build_opener(
    request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect(),
)

def read_partial_state(url, name, token):
    require(name in APIS and url == URLS[name],
            "UNEXPECTED_API_OR_FIELDS")
    req = request.Request(url, method="GET", headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "User-Agent": "OLDX-H2F-ServiceUsage-two-fields-once/1",
    })
    try:
        with OPENER.open(req, timeout=30) as resp:
            raw = resp.read(8193)
            require(resp.status == 200 and len(raw) <= 8192,
                    "PARTIAL_RESPONSE_UNEXPECTED_SIZE_OR_STATUS")
            doc = json.loads(raw)
            require(isinstance(doc, dict), "PARTIAL_JSON_INVALID")
            require(doc.get("name") == f"projects/{NUMBER}/services/{name}",
                    "PARTIAL_SERVICE_IDENTITY_MISMATCH")
            state = doc.get("state")
            require(state in ("ENABLED", "DISABLED"),
                    "PARTIAL_STATE_NOT_EXACT")
            return "API_" + state
    except error.HTTPError as exc:
        code = exc.code
        exc.close()
        return "UNKNOWN_HTTP_" + str(code)
    except (error.URLError, TimeoutError, ssl.SSLError):
        return "UNKNOWN_NETWORK_OR_TIMEOUT"

def main():
    os.umask(0o077)
    try:
        token = owner_token()
    except (Stop, OSError, ValueError, UnicodeError, TypeError) as exc:
        print("OLDX_H2F_RESULT=STOP_BEFORE_REQUEST")
        print("OLDX_H2F_REASON=" +
              (str(exc) if isinstance(exc, Stop) else type(exc).__name__))
        print("OLDX_H2F_CLOUD_RESOURCE_WRITES=NONE")
        return 2

    evidence = ROOT / ("oldx-h2-two-fields-only-" +
                       datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd = os.open(MARKER, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE=" + str(evidence) + "\n")
    except OSError:
        print("OLDX_H2F_RESULT=STOP_MARKER_OR_EVIDENCE")
        return 2

    states = {}
    final = "STOP_AFTER_MARKER"
    reason = "UNKNOWN"
    try:
        for name in APIS:
            states[name] = read_partial_state(URLS[name], name, token)
        final = "EXACT_TWO_API_STATES_FIELDS_ONLY_WITH_LIMITS"
        reason = "PARTIAL_RESPONSE_METADATA_ONLY"
    except (Stop, OSError, UnicodeError, ValueError, TypeError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
    finally:
        try:
            (evidence / "sanitized-h2-fields-only.json").write_text(
                json.dumps({
                    "project": PROJECT,
                    "partial_response_fields": ["name", "state"],
                    "api_states": states,
                    "prior_h2e": "CONSUMED_STOP_AFTER_MARKER",
                    "h2": "NO_GO",
                    "production": "NO_GO",
                    "cloud_resource_writes": False,
                }, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            with MARKER.open("a", encoding="utf-8") as out:
                out.write("RESULT=" + final + "\nREASON=" + reason + "\n")
        except OSError:
            final = "STOP_EVIDENCE_WRITE"
        print("OLDX_H2F_RESULT=" + final)
        print("OLDX_H2F_REASON=" + reason)
        print("OLDX_H2F_KMS_API=" +
              states.get(APIS[0], "UNKNOWN_NOT_CONFIRMED"))
        print("OLDX_H2F_AUTH_API=" +
              states.get(APIS[1], "UNKNOWN_NOT_CONFIRMED"))
        print("OLDX_H2F_H2_ENABLED=NOT_ATTEMPTED")
        print("OLDX_H2F_CLOUD_RESOURCE_WRITES=NONE")
        print("OLDX_H2F_NO_IAM_KMS_AUTH_CHANGES=TRUE")
        print("OLDX_H2F_DO_NOT_REPEAT=TRUE")
    return 0 if final == "EXACT_TWO_API_STATES_FIELDS_ONLY_WITH_LIMITS" else 2

if __name__ == "__main__":
    sys.exit(main())
