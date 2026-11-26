#!/usr/bin/env python3
"""OLDX H2P2 conditional post-H2P1 partial recovery; NO cloud action until
separate exact owner approval. Reconcile Mediator and the ambiguous Gateway.
NEVER retry/create Gateway. Only if Gateway uniquely verified, Backend absent
on full project list AND exact GET=404, create Backend ONCE and GET-by-UID.
New one-shot marker before first GET; fail closed on any ambiguity. No IAM
roles/keys/Run/KMS/production changes. Do not reset H2P1 or H2P2 markers.
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
OWNER = "yasminparmar087@gmail.com"
MEDIATOR = "oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com"
GATEWAY = "oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
BACKEND = "oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com"
BACKEND_ID = "oldx-c2-product-backend"
BACKEND_LABEL = "OLDX H2 Product Backend"
MEDIATOR_UID = "100779414920484819274"
OLD_DISABLED = "oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com"
ROOT_URL = "https://iam.googleapis.com/v1/projects/oldx-staging/serviceAccounts"
LIST_URL = (ROOT_URL + "?pageSize=100&fields=accounts%28email%2C"
            "uniqueId%2Cdisabled%2Cname%2CprojectId%29%2CnextPageToken")
BACKEND_URL = ROOT_URL + "/" + BACKEND
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2P1 = ROOT / ".oldx-step05-h2p1-three-h2-runtime-service-accounts-owner-once-20261127"
MARKER = ROOT / ".oldx-step05-h2p2-partial-three-sa-reconcile-backend-only-once-20261127"
STATUS_PASS = "PASS_GATEWAY_RECONCILED_AND_ONE_BACKEND_CREATED_VERIFIED"


class Stop(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Stop(why)


def cli(env, args):
    try:
        out = subprocess.run([str(CLI), *args], env=env,
                             stdin=subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=25, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_GCLOUD_TIMEOUT") from None
    need(out.returncode == 0, "ISOLATED_GCLOUD_FAILED")
    return out.stdout.decode("utf-8", "replace").strip()


def prior_h2p1_receipt():
    need(H2P1.is_file() and not H2P1.is_symlink()
         and H2P1.stat().st_uid == 0 and H2P1.stat().st_size <= 4096,
         "H2P1_MARKER_UNTRUSTED")
    lines = H2P1.read_text(encoding="utf-8").splitlines()
    need("ATTEMPT_CONSUMED=TRUE" in lines
         and "PROJECT=" + PROJECT in lines
         and "RESULT=STOP_AFTER_MARKER" in lines
         and "REASON=GATEWAY_READBACK_HTTP_404" in lines,
         "H2P1_PARTIAL_STOP_MISMATCH")
    ev = [x[len("EVIDENCE="):] for x in lines if x.startswith("EVIDENCE=")]
    need(len(ev) == 1, "H2P1_EVIDENCE_UNAVAILABLE")
    directory = Path(ev[0])
    need(directory.parent == ROOT and bool(re.fullmatch(
         r"oldx-h2p1-three-runtime-sas-\d{8}T\d{6}Z", directory.name))
         and directory.is_dir() and not directory.is_symlink()
         and directory.stat().st_uid == 0, "H2P1_EVIDENCE_DIR_UNTRUSTED")
    f = directory / "sanitized-h2p1-created-sas.json"
    need(f.is_file() and not f.is_symlink() and f.stat().st_uid == 0
         and f.stat().st_size <= 16384, "H2P1_RECEIPT_UNTRUSTED")
    doc = json.loads(f.read_text(encoding="utf-8"))
    verified = doc.get("verified_created")
    need(doc.get("project") == PROJECT
         and doc.get("result") == "STOP_AFTER_MARKER"
         and doc.get("reason") == "GATEWAY_READBACK_HTTP_404"
         and doc.get("attempted") == ["MEDIATOR", "GATEWAY"]
         and isinstance(verified, list) and len(verified) == 1
         and verified[0] == {
             "kind": "MEDIATOR",
             "email": MEDIATOR,
             "uid": MEDIATOR_UID,
             "state": "ENABLED_NO_ROLES_ASSIGNED_BY_THIS_SCRIPT"}
         and doc.get("kms_iam_grants") is False
         and doc.get("service_account_keys") is False
         and doc.get("cloud_run") is False,
         "H2P1_RECEIPT_CONTENT_MISMATCH")


def owner_token():
    need(sys.argv[1:] == [
        "--owner-explicitly-approved-h2p2-reconcile-and-one-backend-create-if-safe"
    ], "H2P2_SCOPE_APPROVAL_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(), "ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(),
         "H2P2_ONESHOT_ALREADY_CONSUMED")
    need(len({MEDIATOR, GATEWAY, BACKEND, OLD_DISABLED}) == 4
         and len(MEDIATOR_UID) >= 10, "IDENTITY_SCOPE_DRIFT")
    prior_h2p1_receipt()
    need(SDK.is_dir() and not SDK.is_symlink()
         and SDK.stat().st_uid == 0, "NATIVE_SDK_UNTRUSTED")
    need(CLI.is_file() and not CLI.is_symlink()
         and CLI.stat().st_uid == 0 and os.access(CLI, os.X_OK),
         "NATIVE_CLI_UNTRUSTED")
    py = PY.resolve(strict=True)
    need(py.is_relative_to(SDK.resolve(strict=True))
         and py.is_file() and py.stat().st_uid == 0
         and os.access(py, os.X_OK), "NATIVE_PYTHON_UNTRUSTED")
    need(CONFIG.is_dir() and not CONFIG.is_symlink()
         and CONFIG.stat().st_uid == 0, "ISOLATED_CONFIG_UNTRUSTED")
    env = dict(os.environ)
    env.update({"HOME": str(ROOT),
                "PATH": str(SDK / "bin") + ":/usr/bin:/bin",
                "CLOUDSDK_CONFIG": str(CONFIG), "CLOUDSDK_PYTHON": str(PY),
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE", None)
    need(cli(env, ["auth", "list", "--filter=status:ACTIVE",
                   "--format=value(account)"]) == OWNER, "WRONG_OWNER")
    need(cli(env, ["config", "get-value", "project"]) == PROJECT,
         "WRONG_PROJECT")
    token = cli(env, ["--quiet", "--account=" + OWNER,
                      "auth", "print-access-token"])
    need(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", token)),
         "OWNER_TOKEN_UNAVAILABLE")
    return token


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = request.build_opener(request.ProxyHandler({}),
                               request.HTTPSHandler(context=ssl.create_default_context()),
                               NoRedirect())


def numeric_url(uid):
    need(isinstance(uid, str) and bool(re.fullmatch(r"\d{10,32}", uid)),
         "INVALID_NUMERIC_SA_UID")
    return ROOT_URL + "/" + uid


def rest(method, url, token, body=None, numeric_ids=frozenset()):
    allowed_get = {LIST_URL, BACKEND_URL, numeric_url(MEDIATOR_UID)}
    allowed_get.update(numeric_url(u) for u in numeric_ids)
    need((method == "GET" and url in allowed_get and body is None)
         or (method == "POST" and url == ROOT_URL and body == {
             "accountId": BACKEND_ID,
             "serviceAccount": {"displayName": BACKEND_LABEL}}),
         "H2P2_REQUEST_OUT_OF_SCOPE")
    raw_body = (json.dumps(body, separators=(",", ":")).encode("utf-8")
                if body is not None else None)
    req = request.Request(url, method=method, data=raw_body, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "User-Agent": "OLDX-H2P2-partial-SA-reconcile-and-one-backend/1",
        **({"Content-Type": "application/json"} if raw_body is not None else {})})
    try:
        with OPENER.open(req, timeout=35) as response:
            raw = response.read(32769)
            need(response.status == 200 and len(raw) <= 32768,
                 "IAM_UNEXPECTED_HTTP_OR_RESPONSE_SIZE")
            result = json.loads(raw)
            need(isinstance(result, dict), "IAM_RESPONSE_SCHEMA_INVALID")
            return 200, result
    except error.HTTPError as exc:
        code = exc.code
        exc.close()
        return code, {}
    except (error.URLError, ssl.SSLError, TimeoutError):
        raise Stop("IAM_NETWORK_OR_TIMEOUT") from None


def identity(item, email, uid=None):
    need(isinstance(item, dict) and item.get("email") == email
         and isinstance(item.get("uniqueId"), str)
         and bool(re.fullmatch(r"\d{10,32}", item["uniqueId"]))
         and item.get("disabled", False) is False,
         "SERVICE_ACCOUNT_IDENTITY_OR_STATUS_DRIFT")
    if uid is not None:
        need(item["uniqueId"] == uid, "SERVICE_ACCOUNT_UID_DRIFT")
    if "projectId" in item:
        need(item["projectId"] == PROJECT, "SA_PROJECT_ID_DRIFT")
    if "name" in item:
        need(item["name"] == "projects/" + PROJECT + "/serviceAccounts/" + email
             or item["name"] == ("projects/" + PROJECT +
                                 "/serviceAccounts/" + item["uniqueId"]),
             "SA_CANONICAL_NAME_DRIFT")
    return item["uniqueId"]


def list_summary(obj):
    need(not obj.get("nextPageToken"), "SA_LIST_NOT_COMPLETE")
    arr = obj.get("accounts", [])
    need(isinstance(arr, list) and 1 <= len(arr) <= 100,
         "SA_LIST_SCHEMA_OR_COUNT")
    accounts = {}
    for entry in arr:
        need(isinstance(entry, dict) and
             isinstance(entry.get("email"), str)
             and len(entry["email"]) <= 320
             and bool(re.fullmatch(r"[A-Za-z0-9._+-]{1,100}@[A-Za-z0-9.-]{1,180}",
                                   entry["email"]))
             and entry["email"] not in accounts, "SA_LIST_DUPLICATE_OR_BAD_EMAIL")
        accounts[entry["email"]] = entry
    need(MEDIATOR in accounts, "MEDIATOR_MISSING_IN_COMPLETE_LIST")
    identity(accounts[MEDIATOR], MEDIATOR, MEDIATOR_UID)
    need(GATEWAY in accounts, "GATEWAY_NOT_VISIBLE_STOP_NO_RECREATE")
    gateway_uid = identity(accounts[GATEWAY], GATEWAY)
    need(gateway_uid != MEDIATOR_UID, "GATEWAY_UID_NOT_DISTINCT")
    need(BACKEND not in accounts, "BACKEND_UNEXPECTEDLY_PRESENT_STOP")
    return gateway_uid


def append(line):
    with MARKER.open("a", encoding="utf-8") as out:
        out.write(line + "\n")


def main():
    os.umask(0o077)
    try:
        token = owner_token()
    except (Stop, OSError, ValueError, TypeError, UnicodeError) as exc:
        print("OLDX_H2P2_RESULT=STOP_BEFORE_REQUEST")
        print("OLDX_H2P2_REASON=" +
              (str(exc) if isinstance(exc, Stop) else type(exc).__name__))
        print("OLDX_H2P2_CLOUD_WRITES=NONE")
        return 2

    evidence = ROOT / ("oldx-h2p2-gateway-reconcile-backend-" +
                       datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd = os.open(MARKER, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write("ATTEMPT_CONSUMED=TRUE\nPROJECT=" + PROJECT +
                      "\nEVIDENCE=" + str(evidence) + "\n")
    except OSError:
        print("OLDX_H2P2_RESULT=STOP_MARKER")
        print("OLDX_H2P2_CLOUD_WRITES=NONE")
        return 2

    gateway_uid = "NOT_VERIFIED"
    backend_uid = "NOT_VERIFIED"
    mediator_verified = False
    gateway_verified = False
    backend_write_attempted = False
    backend_readback_verified = False
    result = "STOP_AFTER_MARKER"
    reason = "UNKNOWN"
    try:
        # New exact-scope reconciliation: one project listing, and two
        # numeric-UID readbacks; never retry the ambiguous Gateway CREATE.
        code, listing = rest("GET", LIST_URL, token)
        need(code == 200, "ACCOUNT_LIST_HTTP_" + str(code))
        gateway_uid = list_summary(listing)
        code, mediator = rest("GET", numeric_url(MEDIATOR_UID), token)
        need(code == 200, "MEDIATOR_UID_READBACK_HTTP_" + str(code))
        identity(mediator, MEDIATOR, MEDIATOR_UID)
        mediator_verified = True
        code, gateway = rest("GET", numeric_url(gateway_uid), token,
                             numeric_ids=frozenset({gateway_uid}))
        need(code == 200, "GATEWAY_UID_READBACK_HTTP_" + str(code))
        identity(gateway, GATEWAY, gateway_uid)
        gateway_verified = True
        # Backend must remain fresh missing in exact project before one write.
        code, _ = rest("GET", BACKEND_URL, token)
        need(code == 404, "BACKEND_FRESH_ABSENCE_HTTP_" + str(code))

        append("BACKEND_CREATE_ABOUT_TO_BE_SENT=TRUE")
        backend_write_attempted = True
        code, created = rest("POST", ROOT_URL, token, {
            "accountId": BACKEND_ID,
            "serviceAccount": {"displayName": BACKEND_LABEL}})
        need(code == 200, "BACKEND_CREATE_HTTP_" + str(code))
        backend_uid = identity(created, BACKEND)
        need(backend_uid not in {MEDIATOR_UID, gateway_uid},
             "BACKEND_DUPLICATE_UID")
        # Google documents possible post-create eventual consistency.
        # Bounded GET-only backoff; NEVER re-POST or create another account.
        for delay in (0, 1, 2, 4, 8):
            if delay:
                time.sleep(delay)
            code, readback = rest("GET", numeric_url(backend_uid), token,
                                  numeric_ids=frozenset({backend_uid}))
            if code == 404:
                continue
            need(code == 200, "BACKEND_READBACK_HTTP_" + str(code))
            identity(readback, BACKEND, backend_uid)
            backend_readback_verified = True
            break
        need(backend_readback_verified, "BACKEND_UID_READBACK_NOT_VISIBLE")
        result = STATUS_PASS
        reason = "PREVIOUS_GATEWAY_UID_AND_BACKEND_NEW_UID_VERIFIED"
    except (Stop, OSError, ValueError, TypeError, UnicodeError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
    finally:
        try:
            (evidence / "sanitized-h2p2-reconciliation.json").write_text(
                json.dumps({
                    "project": PROJECT,
                    "mediator_verified": mediator_verified,
                    "mediator_uid": MEDIATOR_UID if mediator_verified else None,
                    "gateway_verified": gateway_verified,
                    "gateway_uid": gateway_uid,
                    "backend_create_attempted": backend_write_attempted,
                    "backend_uid": backend_uid,
                    "backend_readback_verified": backend_readback_verified,
                    "result": result, "reason": reason,
                    "kms_signing": False, "iam_grants": False,
                    "sa_keys": False, "cloud_run": False,
                    "h2": "NO_GO", "production": "NO_GO",
                }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            append("RESULT=" + result)
            append("REASON=" + reason)
        except OSError:
            result = "STOP_EVIDENCE_WRITE"
        print("OLDX_H2P2_RESULT=" + result)
        print("OLDX_H2P2_REASON=" + reason)
        print("OLDX_H2P2_MEDIATOR_VERIFIED=" + str(mediator_verified).upper())
        print("OLDX_H2P2_MEDIATOR_UID=" + (MEDIATOR_UID if mediator_verified
                                        else "NOT_VERIFIED"))
        print("OLDX_H2P2_GATEWAY_VERIFIED=" + str(gateway_verified).upper())
        print("OLDX_H2P2_GATEWAY_UID=" + gateway_uid)
        print("OLDX_H2P2_BACKEND_CREATE_ATTEMPTED=" +
              str(backend_write_attempted).upper())
        print("OLDX_H2P2_BACKEND_READBACK_VERIFIED=" +
              str(backend_readback_verified).upper())
        print("OLDX_H2P2_BACKEND_UID=" + backend_uid)
        print("OLDX_H2P2_GATEWAY_CREATE_REPEATED=FALSE")
        print("OLDX_H2P2_IAM_GRANTS_KMS_SIGN_RUN_SA_KEYS=NONE")
        print("OLDX_H2P2_H2_PRODUCTION=NO_GO")
        print("OLDX_H2P2_DO_NOT_REPEAT=TRUE")
    return 0 if result == STATUS_PASS else 2


if __name__ == "__main__":
    sys.exit(main())
