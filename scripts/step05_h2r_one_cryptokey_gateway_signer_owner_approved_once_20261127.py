#!/usr/bin/env python3
"""OLDX H2R: source-only until owner consents to EXACT one KMS key IAM grant.

Scope: ONLY the staging cryptoKey and ONLY one serviceAccount gateway binding
roles/cloudkms.signer. Never grant to mediator/backend or project/keyRing.
Exact H2Q local owner receipt + 3 pinned UIDs + project/ring/key policy snapshot.
Fresh key getIamPolicy must be bytewise-equivalent at JSON object level to the
privately retained H2Q preimage and etag. One setIamPolicy POST, no retries,
one GET-only readback. Never roll back automatically on partial/ambiguous result.
No signing, Cloud Run, IAM at other scopes, Firebase, H2 GO or production.
"""
from __future__ import annotations

import hashlib
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

ROOT = Path("/root")
PROJECT = "oldx-staging"
OWNER = "yasminparmar087@gmail.com"
GW = "oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
MEMBER = "serviceAccount:" + GW
ROLE = "roles/cloudkms.signer"
U = {"mediator": "100779414920484819274",
     "gateway": "107238619872767759560",
     "backend": "106984791114720194680"}
KEY = ("projects/oldx-staging/locations/asia-south1/keyRings/"
       "oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256")
BASE = "https://cloudkms.googleapis.com/v1/" + KEY
GET = BASE + ":getIamPolicy?options.requestedPolicyVersion=3"
SET = BASE + ":setIamPolicy"
ALLOWED = frozenset({("GET", GET), ("POST", SET)})
H2Q = ROOT / ".oldx-step05-h2q-three-iam-policy-reads-once-20261127"
MARKER = ROOT / ".oldx-step05-h2r-gateway-single-key-signer-grant-once-20261127"
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
GCLOUD = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"


class Stop(Exception):
    pass


def need(condition, reason):
    if not condition:
        raise Stop(reason)


def parse_small_owned(path, max_size=65536):
    need(path.is_file() and not path.is_symlink()
         and path.stat().st_uid == 0 and path.stat().st_size <= max_size,
         "LOCAL_EVIDENCE_FILE_UNTRUSTED")
    return json.loads(path.read_text(encoding="utf-8"))


def h2q_preimage():
    need(H2Q.is_file() and not H2Q.is_symlink()
         and H2Q.stat().st_uid == 0 and H2Q.stat().st_size <= 4096,
         "H2Q_MARKER_UNTRUSTED")
    lines = H2Q.read_text(encoding="utf-8").splitlines()
    need("ATTEMPT_CONSUMED=TRUE" in lines
         and "PROJECT=" + PROJECT in lines
         and "RESULT=READ_ONLY_THREE_POLICY_LEVELS_WITH_LIMITS" in lines,
         "H2Q_PASS_MISSING")
    paths = [x[9:] for x in lines if x.startswith("EVIDENCE=")]
    need(len(paths) == 1, "H2Q_EVIDENCE_MISSING")
    folder = Path(paths[0])
    need(folder.parent == ROOT and
         bool(re.fullmatch(r"oldx-h2q-iam-policy-preflight-\d{8}T\d{6}Z", folder.name))
         and folder.is_dir() and not folder.is_symlink()
         and folder.stat().st_uid == 0, "H2Q_EVIDENCE_DIRECTORY_UNTRUSTED")

    saved = parse_small_owned(folder / "sanitized-h2q-summary.json")
    need(saved.get("project") == PROJECT
         and saved.get("key") == KEY
         and saved.get("result") == "READ_ONLY_THREE_POLICY_LEVELS_WITH_LIMITS"
         and saved.get("cloud_writes") is False
         and saved.get("policy_grants") is False
         and saved.get("kms_sign") is False
         and saved.get("org_folder_group_deny") == "NOT_CHECKED"
         and all(saved.get("principals", {}).get(k, {}).get("uid") == uid
                 for k, uid in U.items()), "H2Q_SAVED_SUMMARY_DRIFT")

    completed = saved.get("completed", {})
    project = completed.get("project", {})
    ring = completed.get("ring", {})
    key = completed.get("key", {})
    need(project.get("scope") == "PROJECT_POLICY_ONLY"
         and project.get("binding_count") == 17
         and project.get("conditional_binding_count") == 1
         and project.get("gateway_direct_signer_count") == 0,
         "H2Q_PROJECT_SNAPSHOT_MISMATCH")
    need(ring.get("scope") == "KEYRING_DIRECT_POLICY_ONLY"
         and ring.get("binding_count") == 0
         and ring.get("conditional_binding_count") == 0,
         "H2Q_RING_SNAPSHOT_MISMATCH")
    need(key.get("scope") == "CRYPTOKEY_DIRECT_POLICY_ONLY"
         and key.get("binding_count") == 0
         and key.get("conditional_binding_count") == 0
         and key.get("gateway_direct_signer_count") == 0
         and key.get("etag_present") is True
         and isinstance(key.get("etag_sha256"), str)
         and bool(re.fullmatch(r"[0-9a-f]{64}", key["etag_sha256"])),
         "H2Q_KEY_SNAPSHOT_MISMATCH")

    original = parse_small_owned(folder / "private-key-policy.json")
    need(type(original) is dict
         and set(original).issubset({"version", "etag", "bindings"})
         and original.get("bindings", []) == []
         and type(original.get("version", 1)) is int
         and original.get("version", 1) in (0, 1, 3),
         "H2Q_KEY_POLICY_UNEXPECTED")
    etag = original.get("etag")
    need(isinstance(etag, str) and 0 < len(etag) <= 512
         and hashlib.sha256(etag.encode("utf-8")).hexdigest()
         == key["etag_sha256"], "H2Q_KEY_ETAG_MISMATCH")
    # Exclude all project/ring writes even if they contain other IAM bindings.
    return original, etag


def isolated_token():
    need(sys.argv[1:] ==
         ["--owner-approved-exact-h2r-one-key-gateway-signer-iam-grant-once"],
         "H2R_OWNER_SCOPED_CONSENT_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(), "ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(),
         "H2R_ONE_SHOT_ALREADY_CONSUMED")
    need(len(set(U.values())) == 3
         and GW == "oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com",
         "IDENTITY_SCOPE_DRIFT")
    original, etag = h2q_preimage()
    need(SDK.is_dir() and not SDK.is_symlink()
         and SDK.stat().st_uid == 0, "NATIVE_SDK_UNTRUSTED")
    need(GCLOUD.is_file() and not GCLOUD.is_symlink()
         and GCLOUD.stat().st_uid == 0 and os.access(GCLOUD, os.X_OK),
         "NATIVE_GCLOUD_UNTRUSTED")
    py = PY.resolve(strict=True)
    need(py.is_relative_to(SDK.resolve(strict=True))
         and py.is_file() and py.stat().st_uid == 0
         and os.access(py, os.X_OK), "NATIVE_PYTHON_UNTRUSTED")
    need(CONFIG.is_dir() and not CONFIG.is_symlink()
         and CONFIG.stat().st_uid == 0, "ISOLATED_CONFIG_UNTRUSTED")
    env = dict(os.environ)
    env.update({"HOME": str(ROOT), "PATH": str(SDK / "bin") + ":/usr/bin:/bin",
                "CLOUDSDK_CONFIG": str(CONFIG), "CLOUDSDK_PYTHON": str(PY),
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE", None)

    def cli(args):
        try:
            proc = subprocess.run([str(GCLOUD), *args],
                env=env, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=25, check=False)
        except subprocess.TimeoutExpired:
            raise Stop("ISOLATED_GCLOUD_TIMEOUT") from None
        need(proc.returncode == 0, "ISOLATED_GCLOUD_FAILED")
        return proc.stdout.decode("utf-8", "replace").strip()

    need(cli(["auth", "list", "--filter=status:ACTIVE",
              "--format=value(account)"]) == OWNER,
         "WRONG_OWNER")
    need(cli(["config", "get-value", "project"]) == PROJECT,
         "WRONG_PROJECT")
    token = cli(["--quiet", "--account=" + OWNER,
                 "auth", "print-access-token"])
    need(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", token)),
         "OWNER_TOKEN_UNAVAILABLE")
    return token, original, etag


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = request.build_opener(request.ProxyHandler({}),
                               request.HTTPSHandler(context=ssl.create_default_context()),
                               NoRedirect())


def api(method, url, token, body=None):
    need((method, url) in ALLOWED, "IAM_OPERATION_NOT_ALLOWLISTED")
    if method == "POST":
        need(body == {"policy": {
            "version": 3, "etag": body.get("policy", {}).get("etag"),
            "bindings": [{"role": ROLE, "members": [MEMBER]}]},
            "updateMask": "bindings,etag"},
            "IAM_POST_BODY_OUTSIDE_EXACT_ROLE_SCOPE")
    else:
        need(body is None, "UNEXPECTED_GET_BODY")
    data = (json.dumps(body, separators=(",", ":")).encode("utf-8")
            if body is not None else None)
    try:
        with OPENER.open(request.Request(url, method=method, data=data, headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "User-Agent": "OLDX-H2R-single-key-signer-binding/1",
            **({"Content-Type": "application/json"} if data is not None else {}),
        }), timeout=35) as resp:
            raw = resp.read(32769)
            need(resp.status == 200 and len(raw) <= 32768,
                 "KMS_IAM_HTTP_OR_RESPONSE_SIZE_UNEXPECTED")
            obj = json.loads(raw)
            need(isinstance(obj, dict), "KMS_IAM_RESPONSE_BAD_SCHEMA")
            return obj
    except error.HTTPError as exc:
        code = exc.code
        exc.close()
        raise Stop("KMS_IAM_HTTP_" + str(code)) from None
    except (error.URLError, ssl.SSLError, TimeoutError):
        raise Stop("KMS_IAM_NETWORK_OR_TIMEOUT") from None


def expected_after(policy):
    need(type(policy) is dict
         and policy.get("bindings") == [{"role": ROLE, "members": [MEMBER]}]
         and type(policy.get("version", 1)) is int
         and policy.get("version", 1) in (1, 3)
         and isinstance(policy.get("etag"), str)
         and 0 < len(policy["etag"]) <= 512
         and set(policy).issubset({"version", "etag", "bindings"}),
         "IAM_POLICY_RESPONSE_NOT_EXACT_SINGLE_BINDING")
    return policy["etag"]


def append(line):
    with MARKER.open("a", encoding="utf-8") as out:
        out.write(line + "\n")


def main():
    os.umask(0o077)
    try:
        token, old_policy, old_etag = isolated_token()
    except (Stop, OSError, TypeError, ValueError, UnicodeError) as e:
        print("OLDX_H2R_RESULT=STOP_BEFORE_REQUEST")
        print("OLDX_H2R_REASON=" +
              (str(e) if isinstance(e, Stop) else type(e).__name__))
        print("OLDX_H2R_KMS_POLICY_WRITES=NONE")
        return 2

    evidence = ROOT / ("oldx-h2r-one-key-gateway-signer-" +
                       datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd = os.open(MARKER, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                     | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write("ATTEMPT_CONSUMED=TRUE\nPROJECT=" + PROJECT +
                      "\nKEY=" + KEY + "\nEVIDENCE=" + str(evidence) + "\n")
    except OSError:
        print("OLDX_H2R_RESULT=STOP_MARKER")
        print("OLDX_H2R_KMS_POLICY_WRITES=NONE")
        return 2

    result = "STOP_AFTER_MARKER"
    reason = "UNKNOWN"
    sent = False
    set_verified = False
    readback_verified = False
    preimage_verified = False
    try:
        append("FRESH_KEY_POLICY_GET_ABOUT_TO_BE_SENT=TRUE")
        current = api("GET", GET, token)
        need(current == old_policy, "FRESH_POLICY_DIFFERS_FROM_H2Q_SNAPSHOT")
        preimage_verified = True

        body = {"policy": {"version": 3,
                           "etag": old_etag,
                           "bindings": [{"role": ROLE, "members": [MEMBER]}]},
                "updateMask": "bindings,etag"}
        append("KEY_POLICY_SINGLE_GRANT_POST_ABOUT_TO_BE_SENT=TRUE")
        sent = True
        changed = api("POST", SET, token, body)
        new_etag = expected_after(changed)
        need(new_etag != old_etag, "KMS_POLICY_ETAG_NOT_ADVANCED")
        set_verified = True

        append("KEY_POLICY_READBACK_GET_ABOUT_TO_BE_SENT=TRUE")
        got = api("GET", GET, token)
        need(expected_after(got) == new_etag, "KMS_GRANT_READBACK_ETAG_DRIFT")
        readback_verified = True
        (evidence / "private-after-key-policy.json").write_text(
            json.dumps(got, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        result = "PASS_EXACT_ONE_CRYPTOKEY_GATEWAY_SIGNER_BINDING_VERIFIED"
        reason = "ONE_SETIAM_POLICY_ETAG_GUARDED_READBACK"
    except (Stop, OSError, TypeError, ValueError, UnicodeError) as e:
        reason = str(e) if isinstance(e, Stop) else type(e).__name__
        # Never auto-retry write or rollback after ambiguous failure.
    finally:
        try:
            (evidence / "sanitized-h2r-grant.json").write_text(
                json.dumps({
                    "project": PROJECT, "key": KEY, "gateway_uid": U["gateway"],
                    "role": ROLE,
                    "preimage_verified": preimage_verified,
                    "set_policy_post_attempted": sent,
                    "set_policy_response_verified": set_verified,
                    "readback_verified": readback_verified,
                    "result": result, "reason": reason,
                    "other_resource_writes": False,
                    "kms_signing": False, "sa_keys": False,
                    "h2": "NO_GO", "production": "NO_GO",
                    "effective_inherited_iam": "NOT_CHECKED",
                }, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            append("RESULT=" + result)
            append("REASON=" + reason)
        except OSError:
            result = "STOP_EVIDENCE_WRITE"
        print("OLDX_H2R_RESULT=" + result)
        print("OLDX_H2R_REASON=" + reason)
        print("OLDX_H2R_PROJECT=" + PROJECT)
        print("OLDX_H2R_GATEWAY_UID=" + U["gateway"])
        print("OLDX_H2R_FRESH_PREIMAGE_VERIFIED=" + str(preimage_verified).upper())
        print("OLDX_H2R_ONE_KEY_POLICY_POST_ATTEMPTED=" + str(sent).upper())
        print("OLDX_H2R_SET_RESPONSE_VERIFIED=" + str(set_verified).upper())
        print("OLDX_H2R_READBACK_VERIFIED=" + str(readback_verified).upper())
        print("OLDX_H2R_OTHER_CLOUD_WRITES_KMS_SIGN_SA_KEYS_RUN=NONE")
        print("OLDX_H2R_H2_PRODUCTION=NO_GO")
        print("OLDX_H2R_DO_NOT_REPEAT=TRUE")
    return 0 if result == "PASS_EXACT_ONE_CRYPTOKEY_GATEWAY_SIGNER_BINDING_VERIFIED" else 2


if __name__ == "__main__":
    sys.exit(main())
