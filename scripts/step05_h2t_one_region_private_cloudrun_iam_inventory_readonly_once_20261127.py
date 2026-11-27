#!/usr/bin/env python3
"""OLDX Step05 H2T: owner-approved ONE region Cloud Run read-only inventory.

Only GET Cloud Run v2 services.list (max 3 pages) + at most four matching
services' getIamPolicy and latest ready Revision GET. No POST, PUT, PATCH, DELETE,
KMS, Firestore, Firebase, public HTTP invocation or Cloud Run state mutation.
This is service-direct IAM only, NOT effective inherited permissions. The list
must be complete or report STOP, never claim absence from partial pages.
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
from urllib import error, parse, request

ROOT = Path("/root")
OWNER = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
REGION = "asia-south1"
PARENT = f"projects/{PROJECT}/locations/{REGION}"
BASE = "https://run.googleapis.com/v2/" + PARENT + "/services"
GW = "oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
GATEWAY_UID = "107238619872767759560"  # earlier H2P2, NOT a Cloud Run proof
H2_SAS = {
    GW,
    "oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com",
    "oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com",
}
OLD_DELETED = "oldx-c2-website-mediator"  # prior H1B deleted, no standalone GET
MARK = ROOT / ".oldx-step05-h2t-run-inventory-readonly-once-20261127"
SDK = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI = SDK / "bin/gcloud"
PY = SDK / "platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
SCOPED = re.compile(r"[a-z][a-z0-9-]{0,62}")
REV = re.compile(r"[a-z][a-z0-9-]{0,62}")
SHA_IMAGE = re.compile(r"^.+@sha256:[0-9a-f]{64}$")
TIMEOUT = 28

class Stop(Exception):
    pass

def need(ok, why):
    if not ok:
        raise Stop(why)

def gcloud(env, args):
    try:
        p = subprocess.run([str(CLI), *args], env=env,
                           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=28, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("NATIVE_GCLOUD_TIMEOUT") from None
    need(p.returncode == 0, "ISOLATED_GCLOUD_FAILURE")
    return p.stdout.decode("utf-8", "replace").strip()

def owner_auth():
    need(sys.argv[1:] ==
         ["--owner-approved-exact-h2t-cloudrun-service-iam-inventory-readonly-once"],
         "EXACT_READONLY_APPROVAL_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0 and
         "microsoft" in platform.release().lower(), "ROOT_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(), "H2T_ATTEMPT_CONSUMED")
    need(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid == 0 and
         CLI.is_file() and not CLI.is_symlink() and
         CLI.stat().st_uid == 0 and os.access(CLI, os.X_OK),
         "NATIVE_SDK_MISSING_OR_UNTRUSTED")
    py = PY.resolve(strict=True)
    need(py.is_relative_to(SDK.resolve(strict=True)) and
         py.is_file() and py.stat().st_uid == 0 and os.access(py, os.X_OK),
         "BUNDLED_PYTHON_UNTRUSTED")
    need(CONFIG.is_dir() and not CONFIG.is_symlink() and
         CONFIG.stat().st_uid == 0, "ISOLATED_CONFIG_UNTRUSTED")
    env = dict(os.environ)
    env.update({"HOME": str(ROOT),
                "PATH": str(SDK / "bin") + ":/usr/bin:/bin",
                "CLOUDSDK_CONFIG": str(CONFIG),
                "CLOUDSDK_PYTHON": str(PY),
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE", None)
    need(gcloud(env, ["auth", "list", "--filter=status:ACTIVE",
                      "--format=value(account)"]) == OWNER, "WRONG_ACTIVE_OWNER")
    need(gcloud(env, ["config", "get-value", "project"]) == PROJECT,
         "WRONG_STAGING_PROJECT")
    token = gcloud(env, ["--quiet", "--account=" + OWNER,
                         "auth", "print-access-token"])
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}", token) is not None,
         "OWNER_ACCESS_TOKEN_UNAVAILABLE")
    return token

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

OPENER = request.build_opener(
    request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect())

def read_json(url, token):
    # The only service is run.googleapis.com. Every request is a GET to the
    # frozen project/region service prefix; no server-provided arbitrary URL.
    need(url.startswith(BASE) and
         (url == BASE + "?pageSize=100" or
          url.startswith(BASE + "?pageSize=100&pageToken=") or
          re.fullmatch(r"/[a-z][a-z0-9-]{0,62}(?::getIamPolicy|/revisions/[a-z][a-z0-9-]{0,62})",
                       url[len(BASE):]) is not None),
         "NON_ALLOWLISTED_READ_URL")
    req = request.Request(url, method="GET", headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "User-Agent": "OLDX-H2T-readonly-cloudrun-inventory/1",
    })
    try:
        with OPENER.open(req, timeout=TIMEOUT) as response:
            data = response.read(350001)
            need(response.status == 200 and len(data) <= 350000,
                 "CLOUDRUN_RESPONSE_STATUS_OR_SIZE")
            value = json.loads(data.decode("utf-8"))
            need(isinstance(value, dict), "CLOUDRUN_RESPONSE_NOT_OBJECT")
            return value
    except error.HTTPError as exc:
        code = exc.code
        exc.close()
        raise Stop("CLOUDRUN_READ_HTTP_" + str(code)) from None
    except (error.URLError, ssl.SSLError, TimeoutError):
        raise Stop("CLOUDRUN_READ_NETWORK_OR_TIMEOUT") from None

def revision_name(service, value):
    if not isinstance(value, str) or not value:
        return None
    root = service + "/revisions/"
    suffix = value.removeprefix(root) if value.startswith(root) else value
    need(REV.fullmatch(suffix) is not None, "READY_REVISION_NAME_OUT_OF_SCOPE")
    return root + suffix

def extract_image(items):
    if not isinstance(items, list) or len(items) > 4:
        return {"status": "UNKNOWN", "image": None}
    values = [c.get("image") for c in items if isinstance(c, dict)]
    if len(values) != len(items) or not values:
        return {"status": "UNKNOWN", "image": None}
    if not all(isinstance(s, str) and len(s) <= 1024 for s in values):
        return {"status": "UNKNOWN", "image": None}
    # A revision image reference with an @sha256 digest is pinned as configured;
    # this is NOT a binary provenance or registry signature verification.
    return {"status": "ALL_REFERENCES_DIGEST_PINNED" if all(
            SHA_IMAGE.fullmatch(v) for v in values) else
            "TAGGED_OR_UNVERIFIED", "image_sha256": [
                hashlib.sha256(v.encode()).hexdigest() for v in values]}

def summarize_policy(p):
    bindings = p.get("bindings", [])
    need(isinstance(bindings, list) and len(bindings) <= 2000,
         "IAM_POLICY_BINDINGS_MALFORMED")
    broad = 0
    invokers = 0
    conditional = 0
    for binding in bindings:
        need(isinstance(binding, dict) and isinstance(binding.get("role"), str)
             and isinstance(binding.get("members"), list),
             "IAM_BINDING_MALFORMED")
        members = binding["members"]
        need(len(members) <= 10000 and all(isinstance(m, str) for m in members),
             "IAM_MEMBERS_MALFORMED")
        if binding.get("condition") is not None:
            conditional += 1
        if binding["role"] == "roles/run.invoker":
            invokers += len(members)
            broad += sum(m in ("allUsers", "allAuthenticatedUsers")
                         for m in members)
    return {"direct_binding_count": len(bindings),
            "direct_invoker_member_count": invokers,
            "direct_broad_invoker_members": broad,
            "conditional_bindings_count": conditional,
            "inherited_or_group_or_deny_effective_iam": "NOT_CHECKED"}

def main():
    os.umask(0o077)
    try:
        token = owner_auth()
    except (Stop, OSError, ValueError, TypeError) as exc:
        print("OLDX_H2T_RESULT=STOP_BEFORE_CLOUDRUN_GET")
        print("OLDX_H2T_REASON=" + (str(exc) if isinstance(exc, Stop)
                                   else type(exc).__name__))
        print("OLDX_H2T_CLOUD_WRITES=NONE")
        return 2
    evidence = ROOT / ("oldx-h2t-cloudrun-inventory-" +
                       datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd = os.open(MARK, os.O_CREAT | os.O_EXCL | os.O_WRONLY |
                     getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            file.write("ATTEMPT_CONSUMED=TRUE\nPROJECT=" + PROJECT +
                       "\nREGION=" + REGION +
                       "\nEVIDENCE=" + str(evidence) + "\n")
    except OSError:
        print("OLDX_H2T_RESULT=STOP_MARKER_CREATION")
        print("OLDX_H2T_CLOUD_WRITES=NONE")
        return 2
    result = "STOP_AFTER_MARKER"
    reason = "UNKNOWN"
    item = {"project": PROJECT, "region": REGION,
            "scope": "CLOUDRUN_V2_SERVICES_AND_MATCHING_SERVICE_DIRECT_IAM",
            "requested_methods": ["GET_ONLY"],
            "pages_read": 0,
            "complete_list": False,
            "matched": [], "region_service_count": None,
            "gateway_attached_service_count": None,
            "unrelated_services_not_probed": True,
            "firebase_firestore_iam": "NOT_CHECKED",
            "kms_iam_or_signing": "NOT_CHECKED",
            "org_folder_group_deny_effective_iam": "NOT_CHECKED"}
    try:
        services = []
        page_token = None
        for i in range(3):
            url = BASE + "?pageSize=100"
            if page_token:
                url += "&pageToken=" + parse.quote(page_token, safe="")
            data = read_json(url, token)
            item["pages_read"] += 1
            batch = data.get("services", [])
            need(isinstance(batch, list) and len(batch) <= 100,
                 "SERVICE_LIST_MALFORMED")
            for s in batch:
                need(isinstance(s, dict) and
                     isinstance(s.get("name"), str) and
                     s["name"].startswith(BASE.removeprefix(
                         "https://run.googleapis.com/v2/") + "/"),
                     "SERVICE_LIST_NAME_MALFORMED")
                suffix = s["name"].split("/")[-1]
                need(SCOPED.fullmatch(suffix) is not None,
                     "SERVICE_NAME_UNSAFE")
            services.extend(batch)
            need(not data.get("unreachable"), "REGIONAL_LIST_UNREACHABLE")
            page_token = data.get("nextPageToken") or None
            need(page_token is None or
                 (isinstance(page_token, str) and 0 < len(page_token) <= 2048),
                 "LIST_TOKEN_MALFORMED")
            if not page_token:
                break
        need(not page_token, "REGIONAL_SERVICE_LIST_MORE_THAN_THREE_PAGES")
        item["complete_list"] = True
        names = [s["name"] for s in services]
        need(len(names) == len(set(names)), "SERVICE_LIST_DUPLICATE_NAME")
        item["region_service_count"] = len(services)
        item["gateway_attached_service_count"] = sum(
            (s.get("template") or {}).get("serviceAccount") == GW
            for s in services if isinstance(s.get("template") or {}, dict))
        matched = []
        for s in services:
            name = s["name"]
            short = name.split("/")[-1]
            template = s.get("template") or {}
            if not isinstance(template, dict):
                template = {}
            if (short.startswith("oldx-c2-") or
                template.get("serviceAccount") in H2_SAS):
                matched.append(s)
        need(len(matched) <= 4, "MATCHING_H2_SERVICES_OVER_BOUNDED_LIMIT")
        for service in matched:
            name = service["name"]
            short = name.split("/")[-1]
            template = service.get("template") or {}
            if not isinstance(template, dict):
                template = {}
            iam = read_json("https://run.googleapis.com/v2/" + name +
                            ":getIamPolicy", token)
            revision = revision_name(name, service.get("latestReadyRevision"))
            rev = (read_json("https://run.googleapis.com/v2/" + revision,
                             token) if revision else {})
            ready_sa = rev.get("serviceAccount") if rev else None
            rec = {
                "name": short,
                "service_uid": service.get("uid"),
                "template_sa": template.get("serviceAccount") or "UNKNOWN",
                "template_sa_matches_verified_gateway_email":
                    template.get("serviceAccount") == GW,
                "ready_revision": revision or "UNKNOWN",
                "ready_sa": ready_sa or "UNKNOWN",
                "ready_sa_matches_verified_gateway_email": ready_sa == GW,
                "ready_revision_uid": rev.get("uid") if rev else None,
                "ingress": service.get("ingress", "UNKNOWN"),
                "invoker_iam_disabled": service.get("invokerIamDisabled",
                                                    "UNKNOWN"),
                "iap_enabled": service.get("iapEnabled", "UNKNOWN"),
                "reconciling": service.get("reconciling", "UNKNOWN"),
                "template_image": extract_image(template.get("containers")),
                "ready_image": extract_image(rev.get("containers"))
                               if rev else {"status": "UNKNOWN"},
                "direct_service_iam": summarize_policy(iam),
                "effective_public_access": "NOT_PROVEN_BY_DIRECT_POLICY",
            }
            item["matched"].append(rec)
        result = "READ_ONLY_CLOUDRUN_REGION_LIST_AND_MATCHED_IAM_VERIFIED_WITH_LIMITS"
        reason = "SERVICE_DIRECT_POLICY_NOT_EFFECTIVE_INHERITED_IAM"
    except (Stop, OSError, ValueError, TypeError, UnicodeError, KeyError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
    finally:
        item["result"] = result
        item["reason"] = reason
        try:
            (evidence / "sanitized-h2t-cloudrun-inventory.json").write_text(
                json.dumps(item, sort_keys=True, indent=2) + "\n",
                encoding="utf-8")
            with MARK.open("a", encoding="utf-8") as file:
                file.write("RESULT=" + result + "\nREASON=" + reason + "\n")
        except OSError:
            result, reason = "STOP_LOCAL_EVIDENCE_WRITE", "EVIDENCE_UNAVAILABLE"
        print("OLDX_H2T_RESULT=" + result)
        print("OLDX_H2T_REASON=" + reason)
        print("OLDX_H2T_PROJECT=" + PROJECT)
        print("OLDX_H2T_REGION=" + REGION)
        print("OLDX_H2T_LIST_COMPLETE=" + str(item["complete_list"]).upper())
        print("OLDX_H2T_SERVICES_COUNT=" + str(item["region_service_count"]))
        print("OLDX_H2T_H2_MATCHED_SERVICES=" + str(len(item["matched"])))
        print("OLDX_H2T_GATEWAY_SA_TEMPLATE_SERVICE_COUNT=" +
              str(item["gateway_attached_service_count"]))
        for k, rec in enumerate(item["matched"]):
            print("OLDX_H2T_MATCH_" + str(k + 1) + "=" +
                  rec["name"] + "|SA=" + str(rec["ready_sa"]) +
                  "|INGRESS=" + str(rec["ingress"]) +
                  "|INVOKER_IAM_DISABLED=" + str(rec["invoker_iam_disabled"]) +
                  "|DIRECT_BROAD_INVOKERS=" +
                  str(rec["direct_service_iam"]["direct_broad_invoker_members"]) +
                  "|READY_IMAGE=" + rec["ready_image"]["status"])
        print("OLDX_H2T_EFFECTIVE_IAM=NOT_VERIFIED")
        print("OLDX_H2T_FIRESTORE_KMS=NOT_CHECKED")
        print("OLDX_H2T_EVIDENCE=" + str(evidence))
        print("OLDX_H2T_CLOUD_WRITES_KMS_SIGN=NONE")
        print("OLDX_H2T_H2_PRODUCTION=NO_GO")
        print("OLDX_H2T_DO_NOT_REPEAT=TRUE")
    return 0 if result.startswith("READ_ONLY_") else 2

if __name__ == "__main__":
    raise SystemExit(main())
