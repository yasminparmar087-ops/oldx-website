#!/usr/bin/env python3
"""OLDX Step05 H2O: NEW, exact H2 signer identity + key-policy inventory, READ ONLY.

SOURCE ONLY until separate explicit Owner approval for this new read scope.
One project ServiceAccount list with narrow field mask and ONE exact CryptoKey
getIamPolicy GET. No IAM mutation, resource creation, sign, deploy or H2 GO.
Results are direct-resource observations, NOT effective inherited IAM grants.
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
OWNER = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
GATEWAY = "oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
CANDIDATES = {
    "mediator": "oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com",
    "gateway": GATEWAY,
    "backend": "oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com",
}
OLD_DISABLED = "oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com"
KEY = ("projects/oldx-staging/locations/asia-south1/keyRings/"
       "oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256")
VERSION = KEY + "/cryptoKeyVersions/1"
SPKI_PIN = "69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba"
ROLE = "roles/cloudkms.signer"
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2N = ROOT / ".oldx-step05-h2n-public-spki-pin-readonly-once-20261127"
MARKER = ROOT / ".oldx-step05-h2o-signing-identity-and-key-policy-readonly-once-20261127"
SA_URL = ("https://iam.googleapis.com/v1/projects/oldx-staging/serviceAccounts"
          "?pageSize=100&fields=accounts%28email%2CuniqueId%2Cdisabled%29%2CnextPageToken")
POLICY_URL = "https://cloudkms.googleapis.com/v1/" + KEY + ":getIamPolicy"
ALLOWED = frozenset((SA_URL, POLICY_URL))
SA_PATTERN = re.compile(r"[a-z][a-z0-9-]{4,28}[a-z0-9]@oldx-staging[.]iam[.]gserviceaccount[.]com")


class Stop(Exception):
    pass


def need(condition, code):
    if not condition:
        raise Stop(code)


def cli(env, args):
    try:
        process = subprocess.run([str(CLI), *args], env=env,
                                 stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 timeout=25, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("OWNER_GCLOUD_TIMEOUT") from None
    need(process.returncode == 0, "OWNER_GCLOUD_FAILED")
    return process.stdout.decode("utf-8", "replace").strip()


def owner_token():
    need(sys.argv[1:] == ["--owner-approved-two-new-h2o-iam-metadata-gets-once"],
         "EXACT_NEW_H2O_CONSENT_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(), "ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(),
         "H2O_ONE_SHOT_ALREADY_CONSUMED")
    need(H2N.is_file() and not H2N.is_symlink() and H2N.stat().st_uid == 0
         and H2N.stat().st_size <= 4096, "H2N_MARKER_UNTRUSTED")
    receipt = H2N.read_text(encoding="utf-8").splitlines()
    need("ATTEMPT_CONSUMED=TRUE" in receipt
         and "RESULT=PASS_PUBLIC_SPKI_PIN_VERIFIED_READONLY" in receipt,
         "H2N_SUCCESS_NOT_VERIFIED")
    pointers = [line[9:] for line in receipt if line.startswith("EVIDENCE=")]
    need(len(pointers) == 1, "H2N_EVIDENCE_UNKNOWN")
    parent = Path(pointers[0])
    need(parent.parent == ROOT and bool(re.fullmatch(
         r"oldx-h2n-public-key-pin-\d{8}T\d{6}Z", parent.name))
         and parent.is_dir() and not parent.is_symlink()
         and parent.stat().st_uid == 0, "H2N_EVIDENCE_DIR_UNTRUSTED")
    path = parent / "sanitized-h2n-public-pin.json"
    need(path.is_file() and not path.is_symlink()
         and path.stat().st_uid == 0 and path.stat().st_size <= 8192,
         "H2N_EVIDENCE_UNTRUSTED")
    saved = json.loads(path.read_text(encoding="utf-8"))
    need(saved.get("version") == VERSION
         and saved.get("result") == "PASS_PUBLIC_SPKI_PIN_VERIFIED_READONLY"
         and saved.get("algorithm") == "RSA_SIGN_PKCS1_2048_SHA256"
         and saved.get("spki_sha256") == SPKI_PIN
         and saved.get("pem_crc32c") == "VERIFIED"
         and saved.get("resource_writes") is False, "H2N_PIN_MISMATCH")
    need(len(set(CANDIDATES.values())) == 3
         and all(SA_PATTERN.fullmatch(v) for v in CANDIDATES.values())
         and OLD_DISABLED not in CANDIDATES.values(),
         "UNSAFE_PRINCIPAL_PROPOSAL")
    need(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid == 0,
         "NATIVE_SDK_UNTRUSTED")
    need(CLI.is_file() and not CLI.is_symlink() and CLI.stat().st_uid == 0
         and os.access(CLI, os.X_OK), "NATIVE_CLI_UNTRUSTED")
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


def get(url, token):
    need(url in ALLOWED, "OUT_OF_SCOPE_URL")
    try:
        with OPENER.open(request.Request(url, method="GET", headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "User-Agent": "OLDX-H2O-bounded-IAM-metadata-only/1",
        }), timeout=35) as response:
            raw = response.read(32769)
            need(response.status == 200 and len(raw) <= 32768,
                 "UNEXPECTED_IAM_METADATA_RESPONSE")
            item = json.loads(raw)
            need(isinstance(item, dict), "INVALID_IAM_METADATA_SCHEMA")
            return item
    except error.HTTPError as exc:
        code = exc.code
        exc.close()
        raise Stop("HTTP_" + str(code)) from None
    except (error.URLError, ssl.SSLError, TimeoutError):
        raise Stop("NETWORK_OR_TIMEOUT") from None


def accounts_summary(data):
    need(not data.get("nextPageToken"), "IAM_ACCOUNTS_PARTIAL_PAGE")
    items = data.get("accounts", [])
    need(isinstance(items, list) and 1 <= len(items) <= 100,
         "IAM_ACCOUNTS_UNEXPECTED_COUNT")
    by_email = {}
    for item in items:
        need(isinstance(item, dict), "IAM_ACCOUNT_ITEM_SCHEMA")
        email = item.get("email")
        # Existing project inventory may include Google-managed/default SAs
        # outside the proposed user-managed oldx-staging suffix. Validate
        # their structure without granting or selecting any of them.
        need(isinstance(email, str) and len(email) <= 320
             and bool(re.fullmatch(r"[A-Za-z0-9._+-]{1,100}@[A-Za-z0-9.-]{1,180}", email))
             and email not in by_email, "IAM_ACCOUNT_EMAIL_UNEXPECTED")
        uid = item.get("uniqueId")
        need(isinstance(uid, str) and bool(re.fullmatch(r"\d{10,32}", uid)),
             "IAM_ACCOUNT_UID_UNEXPECTED")
        need(isinstance(item.get("disabled", False), bool),
             "IAM_ACCOUNT_DISABLED_SCHEMA")
        by_email[email] = (uid, item.get("disabled", False))
    report = {}
    for kind, email in CANDIDATES.items():
        if email not in by_email:
            report[kind] = {"state": "NOT_IN_COMPLETE_PROJECT_LIST"}
        else:
            uid, disabled = by_email[email]
            report[kind] = {"state": "PRESENT_DISABLED" if disabled
                            else "PRESENT_ENABLED", "uid": uid}
    # This is fresh narrow-field identity-selection evidence, NOT a recheck
    # of the historical H1B SA-disable one-shot, which remains consumed.
    return {"scope": "COMPLETE_VISIBLE_PAGE",
            "count": len(items), "candidates": report,
            "old_trial_account_in_list": OLD_DISABLED in by_email}


def policy_summary(data):
    bindings = data.get("bindings", [])
    need(isinstance(bindings, list) and len(bindings) <= 100,
         "KEY_IAM_POLICY_BINDINGS_SCHEMA")
    chosen = "serviceAccount:" + GATEWAY
    direct_signer = False
    non_candidate_signer_count = 0
    policy_has_conditions = False
    for item in bindings:
        need(isinstance(item, dict) and isinstance(item.get("role"), str)
             and isinstance(item.get("members"), list)
             and len(item["members"]) <= 150, "KEY_IAM_BINDING_SCHEMA")
        role = item["role"]
        members = item["members"]
        need(all(isinstance(v, str) and len(v) <= 256 for v in members),
             "KEY_IAM_MEMBERS_SCHEMA")
        if "condition" in item:
            policy_has_conditions = True
        if role in ("roles/cloudkms.signer", "roles/cloudkms.signerVerifier"):
            if chosen in members:
                direct_signer = True
            non_candidate_signer_count += sum(v != chosen for v in members)
    etag = data.get("etag")
    need(etag is None or isinstance(etag, str) and len(etag) <= 256,
         "KEY_IAM_ETAG_SCHEMA")
    return {"scope": "EXACT_CRYPTOKEY_DIRECT_POLICY_ONLY",
            "direct_gateway_signer_present": direct_signer,
            "other_direct_signer_members_count": non_candidate_signer_count,
            "has_conditional_bindings": policy_has_conditions,
            "etag_sha256": hashlib.sha256(etag.encode()).hexdigest() if etag else None,
            "inherited_project_or_ring_policy": "NOT_CHECKED",
            "safe_to_grant": False}


def main():
    os.umask(0o077)
    try:
        token = owner_token()
    except (Stop, OSError, ValueError, TypeError, UnicodeError) as exc:
        print("OLDX_H2O_RESULT=STOP_BEFORE_REQUEST")
        print("OLDX_H2O_REASON=" + (str(exc) if isinstance(exc, Stop)
                                    else type(exc).__name__))
        print("OLDX_H2O_CLOUD_WRITES=NONE")
        return 2

    evidence = ROOT / ("oldx-h2o-signer-iam-metadata-" +
                       datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd = os.open(MARKER, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                     | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE=" + str(evidence) + "\n")
    except OSError:
        print("OLDX_H2O_RESULT=STOP_MARKER")
        return 2

    summary = {}
    result = "STOP_AFTER_MARKER"
    reason = "UNKNOWN"
    try:
        # NEW exact two metadata GETs. Never retry either request.
        summary["identity"] = accounts_summary(get(SA_URL, token))
        summary["key_policy"] = policy_summary(get(POLICY_URL, token))
        result = "READ_ONLY_EXACT_SIGNER_IDENTITY_AND_KEY_POLICY_WITH_LIMITS"
        reason = "DIRECT_ACCOUNT_LIST_AND_KEY_POLICY_NOT_EFFECTIVE_IAM"
    except (Stop, OSError, ValueError, TypeError, UnicodeError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
    finally:
        try:
            (evidence / "sanitized-h2o-iam-metadata.json").write_text(
                json.dumps({"project": PROJECT, "key": KEY, "role_proposal": ROLE,
                            "summary": summary, "result": result, "reason": reason,
                            "cloud_writes": False, "sign_attempt": False,
                            "h2": "NO_GO", "production": "NO_GO"},
                           indent=2, sort_keys=True) + "\n", encoding="utf-8")
            with MARKER.open("a", encoding="utf-8") as out:
                out.write("RESULT=" + result + "\nREASON=" + reason + "\n")
        except OSError:
            result = "STOP_EVIDENCE_WRITE"
        print("OLDX_H2O_RESULT=" + result)
        print("OLDX_H2O_REASON=" + reason)
        identity = summary.get("identity", {})
        print("OLDX_H2O_ACCOUNT_LIST_SCOPE=" + identity.get("scope", "NOT_VERIFIED"))
        for kind, item in identity.get("candidates", {}).items():
            print("OLDX_H2O_" + kind.upper() + "=" + item["state"])
            if "uid" in item:
                print("OLDX_H2O_" + kind.upper() + "_UID=" + item["uid"])
        policy = summary.get("key_policy", {})
        print("OLDX_H2O_KEY_POLICY_SCOPE=" + policy.get("scope", "NOT_VERIFIED"))
        print("OLDX_H2O_GATEWAY_DIRECT_SIGNER=" +
              str(policy.get("direct_gateway_signer_present", "UNKNOWN")).upper())
        print("OLDX_H2O_INHERITED_IAM=NOT_CHECKED")
        print("OLDX_H2O_IAM_GRANT=NOT_ATTEMPTED")
        print("OLDX_H2O_CLOUD_WRITES=NONE")
        print("OLDX_H2O_H2_PRODUCTION=NO_GO")
        print("OLDX_H2O_DO_NOT_REPEAT=TRUE")
    return 0 if result == "READ_ONLY_EXACT_SIGNER_IDENTITY_AND_KEY_POLICY_WITH_LIMITS" else 2


if __name__ == "__main__":
    sys.exit(main())
