#!/usr/bin/env python3
"""OLDX Step05 H2M: source-only until separate exact owner consent.

On approved supervised owner WSL execution, create exactly ONE new KMS key ring
and ONE new SOFTWARE RSA2048 PKCS1 SHA256 ASYMMETRIC_SIGN CryptoKey with its
single initial key version, in oldx-staging/asia-south1. No other cloud writes.
The irreversibly consumed one-shot marker is installed BEFORE the first POST.
On ambiguous HTTP or partial success, STOP: never retry/reconcile by creation.
NO IAM grant, asymmetricSign, public-key fetch, H2 activation or production.
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
OWNER = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
LOCATION = "asia-south1"
RING_ID = "oldx-c2-h2-signing"
KEY_ID = "oldx-c2-attestation-rs256"
ALGORITHM = "RSA_SIGN_PKCS1_2048_SHA256"
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
GCLOUD = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2K = ROOT / ".oldx-step05-h2-kms-api-enable-owner-once-20261127"
H2L = ROOT / ".oldx-step05-h2-postenable-kms-rings-keys-readonly-once-20261127"
MARKER = ROOT / ".oldx-step05-h2m-new-ring-key-one-create-once-20261127"
HOST = "https://cloudkms.googleapis.com/v1/"
PARENT = f"projects/{PROJECT}/locations/{LOCATION}"
RING = f"{PARENT}/keyRings/{RING_ID}"
KEY = f"{RING}/cryptoKeys/{KEY_ID}"
CREATE_RING = HOST + PARENT + "/keyRings?keyRingId=" + RING_ID
GET_RING = HOST + RING
CREATE_KEY = HOST + RING + "/cryptoKeys?cryptoKeyId=" + KEY_ID + "&skipInitialVersionCreation=false"
GET_KEY = HOST + KEY
GET_VERSIONS = HOST + KEY + "/cryptoKeyVersions?pageSize=10"
GET_VERSION = HOST + KEY + "/cryptoKeyVersions/1"
ALLOWED = {
    ("GET", GET_RING), ("POST", CREATE_RING), ("POST", CREATE_KEY),
    ("GET", GET_KEY), ("GET", GET_VERSIONS), ("GET", GET_VERSION),
}


class Stop(Exception):
    pass


def need(ok, reason):
    if not ok:
        raise Stop(reason)


def cli(env, args):
    try:
        p = subprocess.run([str(GCLOUD)] + args, env=env,
                           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=25, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_GCLOUD_TIMEOUT") from None
    need(p.returncode == 0, "ISOLATED_GCLOUD_FAILED")
    return p.stdout.decode("utf-8", "replace").strip()


def receipt(path, required):
    need(path.is_file() and not path.is_symlink() and path.stat().st_uid == 0
         and path.stat().st_size <= 4096, "PRIOR_RECEIPT_UNTRUSTED")
    lines = path.read_text(encoding="utf-8").splitlines()
    need(all(x in lines for x in required), "PRIOR_RECEIPT_RESULT_MISMATCH")
    return lines


def owner_token():
    need(sys.argv[1:] == ["--owner-explicitly-approved-one-new-h2m-ring-and-key"],
         "EXACT_OWNER_APPROVAL_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(), "ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(),
         "H2M_ONE_SHOT_ALREADY_CONSUMED")
    receipt(H2K, ["ATTEMPT_CONSUMED=TRUE", "PROJECT=" + PROJECT,
                  "SERVICE=cloudkms.googleapis.com",
                  "RESULT=PASS_KMS_API_ENABLED_EXACT_PROJECT_VERIFIED"])
    lines = receipt(H2L, ["ATTEMPT_CONSUMED=TRUE",
                          "RESULT=KMS_POST_ENABLE_METADATA_READ_WITH_LIMITS"])
    pointers = [s[9:] for s in lines if s.startswith("EVIDENCE=")]
    need(len(pointers) == 1, "H2L_EVIDENCE_MISSING")
    evid = Path(pointers[0])
    need(evid.parent == ROOT and evid.name.startswith("oldx-h2-kms-metadata-")
         and evid.is_dir() and not evid.is_symlink()
         and evid.stat().st_uid == 0, "H2L_EVIDENCE_DIR_UNTRUSTED")
    previous = evid / "sanitized-kms-ring-key-metadata.json"
    need(previous.is_file() and not previous.is_symlink()
         and previous.stat().st_uid == 0 and previous.stat().st_size <= 16384,
         "H2L_EVIDENCE_FILE_UNTRUSTED")
    saved = json.loads(previous.read_text(encoding="utf-8"))
    need(saved.get("project") == PROJECT and saved.get("location") == LOCATION
         and saved.get("resource_writes") is False
         and saved.get("summary", {}).get("rings", {}).get("state")
         == "COMPLETE_VISIBLE_PAGE"
         and saved.get("summary", {}).get("rings", {}).get("count") == 0
         and saved.get("summary", {}).get("ring_names") == [],
         "H2L_ZERO_RING_PROOF_MISMATCH")
    need(SDK.is_dir() and not SDK.is_symlink()
         and SDK.stat().st_uid == 0, "NATIVE_SDK_UNTRUSTED")
    need(GCLOUD.is_file() and not GCLOUD.is_symlink()
         and GCLOUD.stat().st_uid == 0 and os.access(GCLOUD, os.X_OK),
         "NATIVE_GCLOUD_UNTRUSTED")
    python = PY.resolve(strict=True)
    need(python.is_relative_to(SDK.resolve(strict=True))
         and python.is_file() and python.stat().st_uid == 0
         and os.access(python, os.X_OK), "NATIVE_PYTHON_UNTRUSTED")
    need(CONFIG.is_dir() and not CONFIG.is_symlink()
         and CONFIG.stat().st_uid == 0, "ISOLATED_CONFIG_UNTRUSTED")
    env = dict(os.environ)
    env.update({
        "HOME": str(ROOT), "PATH": str(SDK / "bin") + ":/usr/bin:/bin",
        "CLOUDSDK_CONFIG": str(CONFIG), "CLOUDSDK_PYTHON": str(PY),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false",
    })
    env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE", None)
    need(cli(env, ["auth", "list", "--filter=status:ACTIVE",
                   "--format=value(account)"]) == OWNER,
         "WRONG_OWNER_ACCOUNT")
    need(cli(env, ["config", "get-value", "project"]) == PROJECT,
         "WRONG_STAGING_PROJECT")
    token = cli(env, ["--quiet", "--account=" + OWNER,
                      "auth", "print-access-token"])
    need(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", token)),
         "OWNER_TOKEN_NOT_AVAILABLE")
    return token


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = request.build_opener(request.ProxyHandler({}),
                               request.HTTPSHandler(context=ssl.create_default_context()),
                               NoRedirect())


def rest(method, url, token, body=None):
    need((method, url) in ALLOWED, "OUT_OF_SCOPE_KMS_REQUEST")
    if method == "POST":
        need(body is not None, "POST_BODY_REQUIRED")
        data = json.dumps(body, separators=(",", ":")).encode("utf-8")
    else:
        need(body is None, "UNEXPECTED_GET_BODY")
        data = None
    headers = {"Authorization": "Bearer " + token,
               "Accept": "application/json",
               "User-Agent": "OLDX-H2M-owner-one-ring-one-key/1"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    try:
        with OPENER.open(request.Request(url, method=method,
                                         data=data, headers=headers),
                         timeout=35) as response:
            raw = response.read(32769)
            need(response.status == 200 and len(raw) <= 32768,
                 "UNEXPECTED_KMS_RESPONSE")
            obj = json.loads(raw)
            need(isinstance(obj, dict), "INVALID_KMS_RESPONSE_SCHEMA")
            return 200, obj
    except error.HTTPError as exc:
        status = exc.code
        exc.close()
        return status, {}
    except (error.URLError, TimeoutError, ssl.SSLError):
        raise Stop("KMS_NETWORK_OR_TIMEOUT") from None


def exact_key(obj):
    return (
        obj.get("name") == KEY
        and obj.get("purpose") == "ASYMMETRIC_SIGN"
        and isinstance(obj.get("versionTemplate"), dict)
        and obj["versionTemplate"].get("algorithm") == ALGORITHM
        and obj["versionTemplate"].get("protectionLevel") == "SOFTWARE"
        and "nextRotationTime" not in obj
        and "rotationPeriod" not in obj
        and obj.get("importOnly") is not True
    )


def append(s):
    with MARKER.open("a", encoding="utf-8") as out:
        out.write(s + "\n")


def main():
    os.umask(0o077)
    try:
        token = owner_token()
        # One NEW exact-target freshness check. 403 is NOT equivalent to 404.
        status, _ = rest("GET", GET_RING, token)
        need(status == 404, "NEW_RING_NOT_FRESH_404_HTTP_" + str(status))
    except (Stop, OSError, ValueError, TypeError, UnicodeError) as exc:
        print("OLDX_H2M_RESULT=STOP_BEFORE_WRITE")
        print("OLDX_H2M_REASON=" + (str(exc) if isinstance(exc, Stop)
                                     else type(exc).__name__))
        print("OLDX_H2M_WRITE_ATTEMPTED=FALSE")
        return 2

    evidence = ROOT / ("oldx-h2m-new-signing-key-"
                       + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd = os.open(MARKER, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                     | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write("ATTEMPT_CONSUMED=TRUE\nPROJECT=" + PROJECT
                      + "\nLOCATION=" + LOCATION
                      + "\nRING=" + RING_ID + "\nKEY=" + KEY_ID
                      + "\nEVIDENCE=" + str(evidence) + "\n")
    except OSError:
        print("OLDX_H2M_RESULT=STOP_MARKER")
        print("OLDX_H2M_WRITE_ATTEMPTED=FALSE")
        return 2

    ring_attempt = False
    key_attempt = False
    verified_ring = False
    verified_key = False
    version = "NOT_VERIFIED"
    result = "STOP_AFTER_MARKER"
    reason = "UNKNOWN"
    try:
        # Exactly ONE keyRing create POST and exact GET readback.
        append("RING_CREATE_ABOUT_TO_BE_SENT=TRUE")
        ring_attempt = True
        code, item = rest("POST", CREATE_RING, token, {})
        need(code == 200 and item.get("name") == RING,
             "RING_CREATE_RESPONSE_UNVERIFIED_HTTP_" + str(code))
        code, item = rest("GET", GET_RING, token)
        need(code == 200 and item.get("name") == RING,
             "RING_READBACK_UNVERIFIED_HTTP_" + str(code))
        verified_ring = True

        # Exactly ONE CryptoKey create POST; initial version implicitly
        # created by Google KMS. No additional version create request.
        append("KEY_CREATE_ABOUT_TO_BE_SENT=TRUE")
        key_attempt = True
        body = {"purpose": "ASYMMETRIC_SIGN",
                "versionTemplate": {
                    "algorithm": ALGORITHM, "protectionLevel": "SOFTWARE"}}
        code, item = rest("POST", CREATE_KEY, token, body)
        need(code == 200 and exact_key(item),
             "KEY_CREATE_RESPONSE_UNVERIFIED_HTTP_" + str(code))
        code, item = rest("GET", GET_KEY, token)
        need(code == 200 and exact_key(item),
             "KEY_READBACK_UNVERIFIED_HTTP_" + str(code))
        verified_key = True

        code, items = rest("GET", GET_VERSIONS, token)
        need(code == 200 and not items.get("nextPageToken"),
             "KEY_VERSION_LIST_UNVERIFIED_HTTP_" + str(code))
        versions = items.get("cryptoKeyVersions", [])
        need(isinstance(versions, list) and len(versions) == 1,
             "KEY_VERSION_COUNT_NOT_EXACTLY_ONE")
        v = versions[0]
        need(isinstance(v, dict)
             and v.get("name") == KEY + "/cryptoKeyVersions/1"
             and v.get("algorithm") == ALGORITHM
             and v.get("protectionLevel") == "SOFTWARE",
             "INITIAL_VERSION_ALGORITHM_UNVERIFIED")
        version = v["name"]
        # Google documents initial ASYMMETRIC version PENDING_GENERATION.
        # Poll GET-only, at most 12 times; never create another version.
        for i in range(12):
            if v.get("state") == "ENABLED":
                break
            need(v.get("state") == "PENDING_GENERATION",
                 "INITIAL_VERSION_UNEXPECTED_STATE")
            time.sleep(3)
            code, v = rest("GET", GET_VERSION, token)
            need(code == 200, "INITIAL_VERSION_GET_HTTP_" + str(code))
            need(v.get("name") == version and v.get("algorithm") == ALGORITHM
                 and v.get("protectionLevel") == "SOFTWARE",
                 "INITIAL_VERSION_METADATA_DRIFT")
        need(v.get("state") == "ENABLED",
             "INITIAL_VERSION_STILL_PENDING_AFTER_BOUNDED_GETS")
        result = "PASS_ONE_NEW_RING_KEY_SOFTWARE_VERSION_VERIFIED"
        reason = "EXACT_POST_CREATE_READBACKS_CONFIRMED"
    except (Stop, OSError, ValueError, TypeError, UnicodeError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
        # No cleanup and no retry after any write; report partial state.
    finally:
        try:
            saved = {"project": PROJECT, "location": LOCATION,
                     "ring": RING, "key": KEY, "algorithm": ALGORITHM,
                     "protection": "SOFTWARE",
                     "ring_create_attempted": ring_attempt,
                     "key_create_attempted": key_attempt,
                     "ring_readback_verified": verified_ring,
                     "key_readback_verified": verified_key,
                     "version_verified": version, "result": result,
                     "reason": reason, "iam_write": False,
                     "signing_operation": False,
                     "h2": "NO_GO", "production": "NO_GO"}
            (evidence / "sanitized-h2m-one-ring-key.json").write_text(
                json.dumps(saved, indent=2, sort_keys=True) + "\n",
                encoding="utf-8")
            append("RESULT=" + result)
            append("REASON=" + reason)
        except OSError:
            result = "STOP_EVIDENCE_WRITE"
        print("OLDX_H2M_RESULT=" + result)
        print("OLDX_H2M_REASON=" + reason)
        print("OLDX_H2M_PROJECT=" + PROJECT)
        print("OLDX_H2M_REGION=" + LOCATION)
        print("OLDX_H2M_RING_CREATE_ATTEMPTED=" + str(ring_attempt).upper())
        print("OLDX_H2M_KEY_CREATE_ATTEMPTED=" + str(key_attempt).upper())
        print("OLDX_H2M_RING_READBACK_VERIFIED=" + str(verified_ring).upper())
        print("OLDX_H2M_KEY_READBACK_VERIFIED=" + str(verified_key).upper())
        print("OLDX_H2M_VERSION=" + version)
        print("OLDX_H2M_IAM_SIGN_H2_PRODUCTION_WRITES=NONE")
        print("OLDX_H2M_DO_NOT_REPEAT=TRUE")
    return 0 if result == "PASS_ONE_NEW_RING_KEY_SOFTWARE_VERSION_VERIFIED" else 2


if __name__ == "__main__":
    sys.exit(main())
