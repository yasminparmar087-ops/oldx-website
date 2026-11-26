#!/usr/bin/env python3
"""OLDX Step05 H2Q: strictly 3 new read-only IAM policy retrievals, once.

Requires exact separate H2Q Owner approval, verified H2P2 final marker and
local evidence matching 3 distinct SA UIDs. Performs only one Resource Manager
POST :getIamPolicy (a READ operation) and two KMS GET :getIamPolicy requests.
No setIamPolicy, sign, create, grants, keys, deployment, or H2/production GO.
Preserves private full policies locally; prints only sanitized derived metadata.
One-shot marker is committed BEFORE the first IAM API request; DO NOT REPEAT.
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
from urllib import error, request

ROOT = Path("/root")
PROJECT = "oldx-staging"
OWNER = "yasminparmar087@gmail.com"
RING = "projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing"
KEY = RING + "/cryptoKeys/oldx-c2-attestation-rs256"
GW = "oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
IDENTITIES = {
    "mediator": ("oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com",
                 "100779414920484819274"),
    "gateway": (GW, "107238619872767759560"),
    "backend": ("oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com",
                "106984791114720194680"),
}
PROJECT_POLICY = "https://cloudresourcemanager.googleapis.com/v3/projects/oldx-staging:getIamPolicy"
RING_POLICY = "https://cloudkms.googleapis.com/v1/" + RING + ":getIamPolicy?options.requestedPolicyVersion=3"
KEY_POLICY = "https://cloudkms.googleapis.com/v1/" + KEY + ":getIamPolicy?options.requestedPolicyVersion=3"
ALLOWED = frozenset({
    ("POST", PROJECT_POLICY),
    ("GET", RING_POLICY),
    ("GET", KEY_POLICY),
})
READ_ONLY_POST_BODY = {"options": {"requestedPolicyVersion": 3}}
H2P2 = ROOT / ".oldx-step05-h2p2-partial-three-sa-reconcile-backend-only-once-20261127"
MARKER = ROOT / ".oldx-step05-h2q-three-iam-policy-reads-once-20261127"
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"


class Stop(Exception):
    pass


def need(ok, code):
    if not ok:
        raise Stop(code)


def sdk_call(env, args):
    try:
        p = subprocess.run([str(CLI), *args], env=env,
                           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=25, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_CLOUDSDK_TIMEOUT") from None
    need(p.returncode == 0, "ISOLATED_CLOUDSDK_FAILED")
    return p.stdout.decode("utf-8", "replace").strip()


def prior_h2p2():
    need(H2P2.is_file() and not H2P2.is_symlink()
         and H2P2.stat().st_uid == 0 and H2P2.stat().st_size <= 4096,
         "H2P2_MARKER_UNTRUSTED")
    lines = H2P2.read_text(encoding="utf-8").splitlines()
    need("ATTEMPT_CONSUMED=TRUE" in lines and "PROJECT=" + PROJECT in lines
         and "RESULT=PASS_GATEWAY_RECONCILED_AND_ONE_BACKEND_CREATED_VERIFIED"
         in lines, "H2P2_SUCCESS_MARKER_MISMATCH")
    pointers = [s[len("EVIDENCE="):] for s in lines if s.startswith("EVIDENCE=")]
    need(len(pointers) == 1, "H2P2_EVIDENCE_MISSING")
    p = Path(pointers[0])
    need(p.parent == ROOT and bool(re.fullmatch(
         r"oldx-h2p2-gateway-reconcile-backend-\d{8}T\d{6}Z", p.name))
         and p.is_dir() and not p.is_symlink() and p.stat().st_uid == 0,
         "H2P2_EVIDENCE_DIR_UNTRUSTED")
    f = p / "sanitized-h2p2-reconciliation.json"
    need(f.is_file() and not f.is_symlink() and f.stat().st_uid == 0
         and f.stat().st_size <= 16384, "H2P2_EVIDENCE_UNTRUSTED")
    data = json.loads(f.read_text(encoding="utf-8"))
    need(data.get("project") == PROJECT
         and data.get("result")
         == "PASS_GATEWAY_RECONCILED_AND_ONE_BACKEND_CREATED_VERIFIED"
         and data.get("mediator_verified") is True
         and data.get("gateway_verified") is True
         and data.get("backend_create_attempted") is True
         and data.get("backend_readback_verified") is True
         and data.get("mediator_uid") == IDENTITIES["mediator"][1]
         and data.get("gateway_uid") == IDENTITIES["gateway"][1]
         and data.get("backend_uid") == IDENTITIES["backend"][1]
         and data.get("iam_grants") is False
         and data.get("kms_signing") is False
         and data.get("sa_keys") is False
         and data.get("cloud_run") is False,
         "H2P2_EVIDENCE_TRUST_MISMATCH")


def owner_token():
    need(sys.argv[1:] == ["--owner-approved-exact-h2q-three-readonly-iam-policies-once"],
         "H2Q_OWNER_APPROVAL_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(), "ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(),
         "H2Q_ONE_SHOT_ALREADY_CONSUMED")
    need(len({u for _, u in IDENTITIES.values()}) == 3
         and len({e for e, _ in IDENTITIES.values()}) == 3,
         "NON_DISTINCT_SERVICE_IDENTITIES")
    prior_h2p2()
    need(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid == 0,
         "NATIVE_SDK_UNTRUSTED")
    need(CLI.is_file() and not CLI.is_symlink()
         and CLI.stat().st_uid == 0 and os.access(CLI, os.X_OK),
         "NATIVE_CLOUDSDK_UNTRUSTED")
    py = PY.resolve(strict=True)
    need(py.is_relative_to(SDK.resolve(strict=True)) and py.is_file()
         and py.stat().st_uid == 0 and os.access(py, os.X_OK),
         "BUNDLED_PYTHON_UNTRUSTED")
    need(CONFIG.is_dir() and not CONFIG.is_symlink()
         and CONFIG.stat().st_uid == 0,
         "ISOLATED_CONFIG_UNTRUSTED")
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
    need(sdk_call(env, ["auth", "list", "--filter=status:ACTIVE",
                        "--format=value(account)"]) == OWNER,
         "WRONG_OWNER")
    need(sdk_call(env, ["config", "get-value", "project"]) == PROJECT,
         "WRONG_STAGING_PROJECT")
    token = sdk_call(env, ["--quiet", "--account=" + OWNER,
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


def read_policy(method, url, token):
    need((method, url) in ALLOWED, "H2Q_METHOD_OR_URL_OUT_OF_SCOPE")
    body = (json.dumps(READ_ONLY_POST_BODY, separators=(",", ":")).encode("utf-8")
            if method == "POST" else None)
    try:
        with OPENER.open(request.Request(
            url, method=method, data=body, headers={
                "Authorization": "Bearer " + token,
                "Accept": "application/json",
                "User-Agent": "OLDX-H2Q-read-policies-only/1",
                **({"Content-Type": "application/json"} if body else {}),
            }), timeout=35) as r:
            raw = r.read(262145)
            need(r.status == 200 and len(raw) <= 262144,
                 "IAM_POLICY_HTTP_OR_SIZE_UNEXPECTED")
            value = json.loads(raw)
            need(isinstance(value, dict), "IAM_POLICY_RESPONSE_BAD_SCHEMA")
            return value
    except error.HTTPError as exc:
        status = exc.code
        exc.close()
        raise Stop("IAM_POLICY_HTTP_" + str(status)) from None
    except (error.URLError, ssl.SSLError, TimeoutError):
        raise Stop("IAM_POLICY_NETWORK_OR_TIMEOUT") from None


def summarize(policy, level):
    need(isinstance(policy, dict), "POLICY_OBJECT_MALFORMED")
    version = policy.get("version", 1)
    need(type(version) is int and version in (0, 1, 3),
         "IAM_POLICY_VERSION_UNEXPECTED")
    bindings = policy.get("bindings", [])
    need(isinstance(bindings, list) and len(bindings) <= 1000,
         "IAM_POLICY_BINDINGS_UNEXPECTED")
    etag = policy.get("etag")
    need(etag is None or isinstance(etag, str) and 0 < len(etag) <= 512,
         "IAM_POLICY_ETAG_BAD")
    counts = {
        "binding_count": len(bindings), "conditional_binding_count": 0,
        "member_count": 0, "gateway_direct_signer_count": 0,
        "other_direct_signer_member_count": 0,
        "broad_principal_binding_count": 0,
    }
    for bind in bindings:
        need(isinstance(bind, dict) and isinstance(bind.get("role"), str)
             and 1 <= len(bind["role"]) <= 256
             and isinstance(bind.get("members"), list)
             and len(bind["members"]) <= 10000,
             "IAM_BINDING_SCHEMA_BAD")
        mem = bind["members"]
        need(all(isinstance(v, str) and 1 <= len(v) <= 512 for v in mem),
             "IAM_MEMBERS_SCHEMA_BAD")
        counts["member_count"] += len(mem)
        cond = bind.get("condition")
        if cond is not None:
            need(isinstance(cond, dict)
                 and isinstance(cond.get("expression"), str)
                 and 0 < len(cond["expression"]) <= 8192,
                 "IAM_CONDITION_SCHEMA_BAD")
            counts["conditional_binding_count"] += 1
        if "allUsers" in mem or "allAuthenticatedUsers" in mem:
            counts["broad_principal_binding_count"] += 1
        if bind["role"] in ("roles/cloudkms.signer",
                            "roles/cloudkms.signerVerifier"):
            gw = "serviceAccount:" + GW
            counts["gateway_direct_signer_count"] += sum(m == gw for m in mem)
            counts["other_direct_signer_member_count"] += sum(m != gw for m in mem)
    if counts["conditional_binding_count"]:
        need(version == 3, "IAM_CONDITIONAL_POLICY_VERSION_NOT_3")
    if version == 0:
        need(not bindings, "IAM_VERSION_ZERO_WITH_BINDINGS")
    need(counts["member_count"] <= 200000, "IAM_MEMBER_COUNT_TOO_LARGE")
    return {
        "scope": {
            "project": "PROJECT_POLICY_ONLY",
            "ring": "KEYRING_DIRECT_POLICY_ONLY",
            "key": "CRYPTOKEY_DIRECT_POLICY_ONLY",
        }[level],
        "version": version,
        "etag_sha256": hashlib.sha256(etag.encode("utf-8")).hexdigest()
                       if etag else "NOT_PROVIDED",
        "etag_present": etag is not None,
        **counts,
        "effective_iam": "NOT_VERIFIED",
        "can_grant": False,
    }


def append(s):
    with MARKER.open("a", encoding="utf-8") as out:
        out.write(s + "\n")


def main():
    os.umask(0o077)
    try:
        token = owner_token()
    except (Stop, OSError, ValueError, TypeError, UnicodeError) as exc:
        print("OLDX_H2Q_RESULT=STOP_BEFORE_REQUEST")
        print("OLDX_H2Q_REASON=" +
              (str(exc) if isinstance(exc, Stop) else type(exc).__name__))
        print("OLDX_H2Q_CLOUD_WRITES=NONE")
        return 2

    evidence = ROOT / ("oldx-h2q-iam-policy-preflight-" +
                       datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd = os.open(MARKER, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                     | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write("ATTEMPT_CONSUMED=TRUE\nPROJECT=" + PROJECT
                      + "\nEVIDENCE=" + str(evidence) + "\n")
    except OSError:
        print("OLDX_H2Q_RESULT=STOP_MARKER")
        print("OLDX_H2Q_CLOUD_WRITES=NONE")
        return 2

    completed = {}
    result = "STOP_AFTER_MARKER"
    reason = "UNKNOWN"
    try:
        calls = [
            ("project", "POST", PROJECT_POLICY),
            ("ring", "GET", RING_POLICY),
            ("key", "GET", KEY_POLICY),
        ]
        for level, method, url in calls:
            append(level.upper() + "_READ_ABOUT_TO_BE_SENT=TRUE")
            item = read_policy(method, url, token)
            summary = summarize(item, level)
            (evidence / ("private-" + level + "-policy.json")).write_text(
                json.dumps(item, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            completed[level] = summary
            append(level.upper() + "_READ_VERIFIED=TRUE")
        need(len(completed) == 3, "THREE_POLICY_SCOPE_INCOMPLETE")
        result = "READ_ONLY_THREE_POLICY_LEVELS_WITH_LIMITS"
        reason = "PROJECT_RING_KEY_DIRECT_POLICIES_NOT_FULL_EFFECTIVE_IAM"
    except (Stop, OSError, ValueError, TypeError, UnicodeError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
    finally:
        try:
            (evidence / "sanitized-h2q-summary.json").write_text(
                json.dumps({
                    "project": PROJECT, "ring": RING, "key": KEY,
                    "principals": {k: {"uid": uid} for k, (_, uid) in IDENTITIES.items()},
                    "completed": completed, "result": result, "reason": reason,
                    "cloud_writes": False, "policy_grants": False,
                    "kms_sign": False, "sa_keys": False,
                    "h2": "NO_GO", "production": "NO_GO",
                    "org_folder_group_deny": "NOT_CHECKED",
                }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            append("RESULT=" + result)
            append("REASON=" + reason)
        except OSError:
            result = "STOP_EVIDENCE_WRITE"
        print("OLDX_H2Q_RESULT=" + result)
        print("OLDX_H2Q_REASON=" + reason)
        print("OLDX_H2Q_PROJECT=" + PROJECT)
        for level in ("project", "ring", "key"):
            summary = completed.get(level)
            print("OLDX_H2Q_" + level.upper() + "_READ=" +
                  ("VERIFIED" if summary else "NOT_VERIFIED"))
            if summary:
                print("OLDX_H2Q_" + level.upper() + "_BINDINGS=" +
                      str(summary["binding_count"]))
                print("OLDX_H2Q_" + level.upper() + "_CONDITIONAL=" +
                      str(summary["conditional_binding_count"]))
                print("OLDX_H2Q_" + level.upper() + "_GATEWAY_SIGNER_BINDINGS=" +
                      str(summary["gateway_direct_signer_count"]))
                print("OLDX_H2Q_" + level.upper() + "_ETAG_SHA256=" +
                      summary["etag_sha256"])
        print("OLDX_H2Q_ORG_FOLDER_GROUP_DENY_EFFECTIVE_IAM=NOT_CHECKED")
        print("OLDX_H2Q_IAM_GRANTS_KMS_SIGN_SA_KEYS_RUN=NONE")
        print("OLDX_H2Q_CLOUD_WRITES=NONE")
        print("OLDX_H2Q_H2_PRODUCTION=NO_GO")
        print("OLDX_H2Q_DO_NOT_REPEAT=TRUE")
    return 0 if result == "READ_ONLY_THREE_POLICY_LEVELS_WITH_LIMITS" else 2


if __name__ == "__main__":
    sys.exit(main())
