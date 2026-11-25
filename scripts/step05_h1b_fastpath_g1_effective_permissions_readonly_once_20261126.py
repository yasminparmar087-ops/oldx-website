#!/usr/bin/env python3
"""OLDX Step05 H1B: project and existing Registry testIamPermissions only.

One-shot read-only IAM permission test, no role/project config/image/cloud changes.
Source intended ONLY for Yasmin's authenticated nonroot Google Cloud Shell.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import re
import shutil
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from urllib import request, error

OWNER="yasminparmar087@gmail.com"
PROJECT="oldx-staging"
REPO=f"projects/{PROJECT}/locations/asia-south1/repositories/oldx-staging-images"
MARKER=".oldx-step05-h1b-g1-effective-permissions-readonly-once-20261126"
PROJECT_PERMISSIONS={
    "SA_CREATE":"iam.serviceAccounts.create",
    "SA_DELETE_PROJECT":"iam.serviceAccounts.delete",
    "SA_ACTAS_PROJECT":"iam.serviceAccounts.actAs",
    "RUN_CREATE":"run.services.create",
    "RUN_DELETE_PROJECT":"run.services.delete",
    "RUN_SET_IAM_PROJECT":"run.services.setIamPolicy",
    "RUN_GET":"run.services.get"
}
REGISTRY_PERMISSIONS={
    "REPO_UPLOAD":"artifactregistry.repositories.uploadArtifacts",
    "REPO_DOWNLOAD":"artifactregistry.repositories.downloadArtifacts",
    "REPO_GET":"artifactregistry.repositories.get",
    "REPO_VERSION_DELETE":"artifactregistry.versions.delete"
}
class Stop(Exception): pass
def need(value, why):
    if not value: raise Stop(why)
def token_from_owner(gcloud):
    r=subprocess.run([gcloud,"--quiet","--account="+OWNER,"auth","print-access-token"],
                     stdin=subprocess.DEVNULL,capture_output=True,timeout=20,
                     env={**os.environ,"CLOUDSDK_CORE_DISABLE_PROMPTS":"1"})
    need(r.returncode==0,"OWNER_TOKEN_UNAVAILABLE")
    token=r.stdout.decode("ascii","strict").strip()
    need(bool(re.fullmatch(r"[A-Za-z0-9._~-]{40,4096}",token)),
         "OWNER_TOKEN_INVALID")
    return token
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
def test_permissions(token,url,permissions):
    body=json.dumps({"permissions":permissions},separators=(",",":")).encode("utf-8")
    req=request.Request(url,data=body,method="POST",
           headers={"Authorization":"Bearer "+token,
                    "Content-Type":"application/json","Accept":"application/json",
                    "User-Agent":"OLDX-H1B-effective-permissions-readonly/1"})
    opener=request.build_opener(request.ProxyHandler({}),
            request.HTTPSHandler(context=ssl.create_default_context()),
            NoRedirect())
    try:
        with opener.open(req,timeout=25) as res:
            need(res.status==200,"IAM_TEST_RESPONSE_NOT_200")
            data=res.read(65537)
            need(len(data)<=65536,"IAM_TEST_TOO_LARGE")
    except error.HTTPError as exc:
        raise Stop("IAM_TEST_HTTP_"+str(exc.code)) from None
    except (error.URLError,TimeoutError):
        raise Stop("IAM_TEST_NETWORK_STOP") from None
    try: obj=json.loads(data)
    except (ValueError,UnicodeError): raise Stop("IAM_TEST_INVALID_JSON")
    need(isinstance(obj,dict) and isinstance(obj.get("permissions",[]),list),
         "IAM_TEST_SCHEMA_INVALID")
    granted=obj.get("permissions",[])
    need(all(isinstance(p,str) and p in permissions for p in granted)
         and len(set(granted))==len(granted),"IAM_TEST_UNKNOWN_PERMISSION")
    return set(granted)
def main():
    os.umask(0o077)
    if sys.argv[1:]!=["--h1b-g1-effective-permissions-readonly-once"]:
        print("H1B_G1_RESULT=STOP_FLAG_REQUIRED"); return 2
    home=Path.home()
    try:
        need(platform.system()=="Linux"
             and "microsoft" not in platform.release().lower()
             and os.geteuid()!=0 and home.is_dir() and not home.is_symlink(),
             "OWNER_CLOUD_SHELL_NONROOT_REQUIRED")
        gcloud=shutil.which("gcloud")
        need(gcloud and Path(gcloud).is_file() and not gcloud.startswith("/mnt/"),
             "GCLOUD_NOT_FOUND")
        marker=home/MARKER
        need(not marker.exists() and not marker.is_symlink(),"ONESHOT_CONSUMED")
        evidence=home/("oldx-h1b-g1-permissions-"+
                 datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
        need(not evidence.exists() and not evidence.is_symlink(),
             "EVIDENCE_COLLISION")
    except (Stop,OSError) as exc:
        print("H1B_G1_RESULT=STOP_PREFLIGHT")
        print("H1B_G1_REASON="+(str(exc) if isinstance(exc,Stop) else "OS_ERROR"))
        return 2
    evidence.mkdir(mode=0o700)
    fd=os.open(marker,os.O_EXCL|os.O_CREAT|os.O_WRONLY|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w") as f:
        f.write("ATTEMPT_CONSUMED\nEVIDENCE="+str(evidence)+"\n")
    results={}
    outcome="STOP"
    reason="UNKNOWN"
    try:
        token=token_from_owner(gcloud)
        project=test_permissions(token,
            "https://cloudresourcemanager.googleapis.com/v1/projects/"
            +PROJECT+":testIamPermissions",list(PROJECT_PERMISSIONS.values()))
        for name,permission in PROJECT_PERMISSIONS.items():
            results["PROJECT_"+name] = "RETURNED" if permission in project else "NOT_RETURNED"
        repo=test_permissions(token,
            "https://artifactregistry.googleapis.com/v1/"+REPO+":testIamPermissions",
            list(REGISTRY_PERMISSIONS.values()))
        for name,permission in REGISTRY_PERMISSIONS.items():
            results[name] = "RETURNED" if permission in repo else "NOT_RETURNED"
        required=[
           "PROJECT_SA_CREATE","PROJECT_RUN_CREATE","PROJECT_RUN_DELETE_PROJECT",
           "REPO_UPLOAD","REPO_GET"
        ]
        outcome=("READ_ONLY_WITH_LIMITS" if all(results[x]=="RETURNED" for x in required)
                 else "READ_ONLY_MISSING_REQUIRED_PERMISSIONS")
        reason="PROJECT_AND_REPOSITORY_PERMISSIONS_TESTED"
    except (Stop,ValueError,UnicodeError,OSError,TypeError,subprocess.TimeoutExpired) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        (evidence/"sanitized-result.json").write_text(
            json.dumps({"result":outcome,"reason":reason,"permissions":results,
                        "cloud_resource_writes":False,
                        "future_service_account_actas":"NOT_YET_TESTABLE",
                        "wslauth":"NOT_CONFIGURED_BY_THIS_SCRIPT",
                        "h1b_image_remote_digest":"UNKNOWN"},sort_keys=True)+"\n")
        with marker.open("a") as f:
            f.write("RESULT="+outcome+"\nREASON="+reason+"\n")
    for key in PROJECT_PERMISSIONS:
        print("H1B_G1_PROJECT_"+key+"="+results.get("PROJECT_"+key,"NOT_TESTED"))
    for key in REGISTRY_PERMISSIONS:
        print("H1B_G1_"+key+"="+results.get(key,"NOT_TESTED"))
    print("H1B_G1_FUTURE_NEW_SA_ACTAS=NOT_YET_TESTABLE")
    print("H1B_G1_WSL_AUTH=NOT_CONFIGURED")
    print("H1B_G1_RESULT="+outcome)
    print("H1B_G1_REASON="+reason)
    print("H1B_G1_CLOUD_RESOURCE_WRITES=NONE")
    return 0 if outcome=="READ_ONLY_WITH_LIMITS" else 2
if __name__=="__main__": sys.exit(main())
