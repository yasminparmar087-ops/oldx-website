#!/usr/bin/env python3
"""BAJUTO/OLDX H2Z: one bounded project IAM + VPC metadata audit, READ-ONLY.
Do not confuse a project allow policy with effective/inherited IAM, or a VPC
inventory with an authenticated internal Cloud Run HTTP test.
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
OWNER = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
REGION = "asia-south1"
H2W = ROOT / ".oldx-step05-h2w-new-internal-off-cloudrun-service-once-20261127"
MARK = ROOT / ".oldx-step05-h2z-project-iam-vpc-readonly-once-20261128"
SERVICE_UID = "2d87153f-155e-409f-a418-463c785d8467"
IMAGE = ("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
         "oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2")
CLI = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY = ROOT / "oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG = ROOT / "oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
IAM_URL = "https://cloudresourcemanager.googleapis.com/v1/projects/oldx-staging:getIamPolicy"
NETWORK_URL = "https://compute.googleapis.com/compute/v1/projects/oldx-staging/global/networks?maxResults=100"
SUBNET_URL = ("https://compute.googleapis.com/compute/v1/projects/oldx-staging/"
              "regions/asia-south1/subnetworks?maxResults=100")

class Stop(Exception):
    pass

def need(ok, why):
    if not ok:
        raise Stop(why)

def get_token():
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(), "ROOT_UBUNTU_WSL_REQUIRED")
    need(H2W.is_file() and not H2W.is_symlink() and H2W.stat().st_uid == 0,
         "H2W_PASS_MARKER_MISSING")
    receipt = H2W.read_text(encoding="utf-8").splitlines()
    for line in ("RESULT=PASS_NEW_INTERNAL_OFF_SERVICE_AND_OWNER_DIRECT_INVOKER_WITH_LIMITS",
                 "SERVICE_UID=" + SERVICE_UID, "IMAGE=" + IMAGE):
        need(line in receipt, "H2W_MARKER_RECEIPT_MISMATCH")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI, os.X_OK),
         "ISOLATED_NATIVE_GCLOUD_MISSING")
    need(PY.resolve(strict=True).is_file() and CONFIG.is_dir()
         and not CONFIG.is_symlink(), "ISOLATED_CREDENTIALS_MISSING")
    need(not MARK.exists() and not MARK.is_symlink(), "H2Z_ALREADY_CONSUMED_DO_NOT_REPEAT")
    env = dict(os.environ)
    env.update({"HOME": str(ROOT), "CLOUDSDK_CONFIG": str(CONFIG),
                "CLOUDSDK_PYTHON": str(PY),
                "PATH": str(CLI.parent) + ":/usr/bin:/bin",
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING": "1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK": "1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA": "false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE", None)
    try:
        run = subprocess.run([str(CLI), "--quiet", "--account=" + OWNER,
                              "--project=" + PROJECT, "auth", "print-access-token"],
                             env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, timeout=35, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_OWNER_OAUTH_TIMEOUT")
    need(run.returncode == 0 and run.stdout.strip(), "OWNER_OAUTH_UNAVAILABLE")
    token = run.stdout.decode("utf-8").strip()
    need(40 < len(token) < 8192 and "\n" not in token, "OAUTH_TOKEN_INVALID")
    return token

def read_json(token, url, method="GET", payload=None):
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json",
               "User-Agent": "OLDX-H2Z-three-new-metadata-reads/1"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = request.Request(url, headers=headers, method=method,
                          data=json.dumps(payload).encode("utf-8") if payload is not None else None)
    opener = request.build_opener(request.ProxyHandler({}),
                                  request.HTTPSHandler(context=ssl.create_default_context()))
    try:
        with opener.open(req, timeout=35) as response:
            need(response.status == 200, "HTTP_RESPONSE_NOT_200")
            raw = response.read(262145)
            need(len(raw) <= 262144, "RESPONSE_TOO_LARGE")
    except error.HTTPError as exc:
        code = exc.code
        exc.close()
        raise Stop("HTTP_" + str(code))
    except (error.URLError, ssl.SSLError, TimeoutError):
        raise Stop("NETWORK_OR_TLS_STOP")
    doc = json.loads(raw)
    need(isinstance(doc, dict), "INVALID_RESPONSE_OBJECT")
    return doc

def complete_items(doc, label):
    need(not doc.get("nextPageToken"), label + "_PAGINATED_UNKNOWN")
    items = doc.get("items", [])
    need(isinstance(items, list) and len(items) <= 100, label + "_ITEMS_UNEXPECTED")
    return items

def main():
    need(sys.argv[1:] == ["--h2z-owner-project-iam-vpc-readonly-once"],
         "EXACT_CONSENT_FLAG_REQUIRED")
    token = get_token()
    # Local one-shot marker precedes the FIRST remote Cloud request.
    fd = os.open(str(MARK), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("ATTEMPT=H2Z_THREE_DISTINCT_READONLY_METADATA_METHODS\n")
        f.write("PROJECT=oldx-staging\nH2W_SERVICE_UID=" + SERVICE_UID + "\n")
    print("H2Z_MARKER=CONSUMED_NO_RETRY")
    print("H2Z_REQUEST_PLAN=ONE_PROJECT_GET_IAM_POLICY_READ_POST_AND_TWO_COMPUTE_GETS")
    policy = read_json(token, IAM_URL, method="POST",
                       payload={"options": {"requestedPolicyVersion": 3}})
    binds = policy.get("bindings", [])
    need(isinstance(binds, list), "IAM_BINDINGS_UNEXPECTED")
    invoker = 0
    owner_editor = 0
    public = 0
    conditional = 0
    for b in binds:
        need(isinstance(b, dict) and isinstance(b.get("role"), str)
             and isinstance(b.get("members", []), list), "IAM_BINDING_MALFORMED")
        role = b["role"]
        members = b.get("members", [])
        if role == "roles/run.invoker":
            invoker += 1
            public += sum(m in ("allUsers", "allAuthenticatedUsers") for m in members)
        if role in ("roles/owner", "roles/editor"):
            owner_editor += 1
        if "condition" in b:
            conditional += 1
    print("H2Z_PROJECT_IAM_POLICY=READ_COMPLETE_VERSION_" + str(policy.get("version", "UNKNOWN")))
    print("H2Z_PROJECT_DIRECT_RUN_INVOKER_BINDINGS=" + str(invoker))
    print("H2Z_PROJECT_DIRECT_OWNER_EDITOR_BINDINGS=" + str(owner_editor))
    print("H2Z_PROJECT_DIRECT_PUBLIC_INVOKER_MEMBERS=" + str(public))
    print("H2Z_PROJECT_CONDITIONAL_BINDINGS=" + str(conditional))
    print("H2Z_PROJECT_IAM_PRINCIPAL_IDENTITIES=NOT_PRINTED")
    networks = complete_items(read_json(token, NETWORK_URL), "NETWORKS")
    subnets = complete_items(read_json(token, SUBNET_URL), "SUBNETS")
    need(all(isinstance(v, dict) for v in networks + subnets), "VPC_ITEMS_MALFORMED")
    pga = sum(s.get("privateIpGoogleAccess") is True for s in subnets)
    print("H2Z_VPC_NETWORKS_VISIBLE=" + str(len(networks)))
    print("H2Z_REGIONAL_SUBNETS_VISIBLE=" + str(len(subnets)))
    print("H2Z_REGIONAL_PRIVATE_GOOGLE_ACCESS_TRUE=" + str(pga))
    print("H2Z_EFFECTIVE_OR_ANCESTOR_IAM=NOT_VERIFIED")
    print("H2Z_CUSTOM_ROLE_AND_CONDITION_EFFECTS=NOT_EVALUATED")
    print("H2Z_INTERNAL_ORIGIN_VPC_ROUTING=NOT_VERIFIED")
    print("H2Z_HOSTED_HTTP_AND_SIGNING=NOT_TESTED")
    print("H2Z_CLOUD_WRITES=NONE_POST_GET_IAM_POLICY_IS_A_READ_METHOD")
    print("H2Z_H2_PRODUCTION=NO_GO")
    print("H2Z_DO_NOT_REPEAT=TRUE")
    print("H2Z_RESULT=PROJECT_IAM_AND_VPC_READONLY_PASS_WITH_LIMITS")

if __name__ == "__main__":
    try:
        main()
    except (Stop, OSError, ValueError, TypeError, KeyError) as exc:
        print("H2Z_RESULT=STOP_PARTIAL_OR_BEFORE_READ_ONLY_AUDIT")
        print("H2Z_REASON=" + (str(exc) if isinstance(exc, Stop) else type(exc).__name__))
        print("H2Z_EFFECTIVE_IAM_AND_INTERNAL_ROUTING=NOT_VERIFIED")
        print("H2Z_CLOUD_WRITES=NONE")
        print("H2Z_H2_PRODUCTION=NO_GO")
        print("H2Z_DO_NOT_REPEAT_IF_MARKER_EXISTS=TRUE")
        sys.exit(2)
