#!/usr/bin/env python3
"""OLDX Step05 H1B W1: one NEW no-key SA creation, receipt and resource-rights check.

W0 actual PASS and G2B actual PASS are inputs, never re-run.
Before the single POST create: exact new SA and Cloud Run service GET 404; latest
project-level create/delete/run cleanup rights read-only testIamPermissions.
No Cloud Run deployment, IAM grants, key issuance, registry push or old deletion.
On partial/unknown create response STOP; never retry this write/marker.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import re
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from urllib import request, error

OWNER="yasminparmar087@gmail.com"
PROJECT="oldx-staging"
REGION="asia-south1"
SERVICE="oldx-c2-website-mediator"
ID="oldx-c2-mediator"
EMAIL=f"{ID}@{PROJECT}.iam.gserviceaccount.com"
SA_NAME=f"projects/{PROJECT}/serviceAccounts/{EMAIL}"
SA_URL=f"https://iam.googleapis.com/v1/{SA_NAME}"
SA_CREATE=f"https://iam.googleapis.com/v1/projects/{PROJECT}/serviceAccounts"
RUN_URL=f"https://run.googleapis.com/v2/projects/{PROJECT}/locations/{REGION}/services/{SERVICE}"
PROJECT_PERMS=f"https://cloudresourcemanager.googleapis.com/v1/projects/{PROJECT}:testIamPermissions"
ROOT=Path("/root")
SDK=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI=SDK/"bin/gcloud"
PY=SDK/"platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
W0=ROOT/".oldx-h1b-w0-new-target-readonly-once-20261126"
G2B=ROOT/".oldx-h1b-g2b-retained-single-push-once-20261126"
MARKER=ROOT/".oldx-h1b-w1-new-no-key-sa-create-once-20261126"
NEEDED={"iam.serviceAccounts.create","iam.serviceAccounts.delete",
        "run.services.create","run.services.delete","run.services.get"}
class Stop(Exception):
    pass

def must(ok,why):
    if not ok:
        raise Stop(why)

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        return None

opener=request.build_opener(request.ProxyHandler({}),
           request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())

def call(method,url,token,body=None):
    must(url in (SA_URL,SA_CREATE,RUN_URL,PROJECT_PERMS,
                 SA_URL+":testIamPermissions"),"UNEXPECTED_API_URL")
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",
             "User-Agent":"OLDX-H1B-W1-single-new-SA/1"}
    data=None
    if body is not None:
        data=json.dumps(body,separators=(",",":"),sort_keys=True).encode()
        headers["Content-Type"]="application/json"
    req=request.Request(url,data=data,headers=headers,method=method)
    try:
        with opener.open(req,timeout=35) as res:
            raw=res.read(262145)
            must(len(raw)<=262144,"API_PAYLOAD_TOO_LARGE")
            parsed=json.loads(raw) if raw else {}
            must(isinstance(parsed,dict),"API_RESPONSE_SCHEMA_INVALID")
            return res.status,parsed
    except error.HTTPError as exc:
        code=exc.code
        exc.close()
        return code,{}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("GOOGLE_API_NETWORK_OR_TIMEOUT_STOP") from None

def gcloud_env():
    must(sys.argv[1:]==["--w1-single-new-no-key-sa-once"],"EXACT_FLAG_REQUIRED")
    must(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"ROOT_IN_OWNER_WSL_REQUIRED")
    must(not MARKER.exists() and not MARKER.is_symlink(),"W1_ONESHOT_ALREADY_CONSUMED")
    must(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,
         "NATIVE_SDK_NOT_VERIFIED")
    must(CLI.is_file() and not CLI.is_symlink() and CLI.stat().st_uid==0 and
         os.access(CLI,os.X_OK),"NATIVE_CLI_MISMATCH")
    py=PY.resolve(strict=True)
    must(py.is_relative_to(SDK.resolve(strict=True)) and py.is_file() and
         py.stat().st_uid==0 and os.access(py,os.X_OK),"BUNDLED_PYTHON_MISMATCH")
    must(CONFIG.is_dir() and not CONFIG.is_symlink() and CONFIG.stat().st_uid==0,
         "ISOLATED_OWNER_CONFIG_NOT_VERIFIED")
    for marker,text in ((W0,"RESULT=READ_ONLY_NEW_TARGETS_ABSENT_WITH_LIMITS"),
                        (G2B,"RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED")):
        must(marker.is_file() and not marker.is_symlink() and marker.stat().st_uid==0
             and text in marker.read_text(encoding="utf-8").splitlines(),
             "PRIOR_W0_OR_G2B_RECEIPT_MISSING")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":f"{SDK}/bin:/usr/bin:/bin",
        "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    def output(cmd):
        try:
            res=subprocess.run(cmd,env=env,stdin=subprocess.DEVNULL,
              stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25,check=False)
        except subprocess.TimeoutExpired:
            raise Stop("GCLOUD_LOCAL_TIMEOUT") from None
        must(res.returncode==0,"GCLOUD_LOCAL_COMMAND_FAILED")
        return res.stdout.decode("utf-8","replace").strip()
    must(output([str(CLI),"auth","list","--filter=status:ACTIVE",
                 "--format=value(account)"])==OWNER,"WRONG_OWNER")
    must(output([str(CLI),"config","get-value","project"])==PROJECT,
         "WRONG_PROJECT")
    token=output([str(CLI),"--quiet","--account="+OWNER,"auth","print-access-token"])
    must(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)),"OWNER_TOKEN_UNAVAILABLE")
    return token

def main():
    os.umask(0o077)
    try:
        token=gcloud_env()
        # These are NEW, immediately-pre-write guard GETs, NOT repeats of W0.
        status,_=call("GET",RUN_URL,token)
        must(status==404,"NEW_SERVICE_COLLISION_OR_UNKNOWN_HTTP_"+str(status))
        status,_=call("GET",SA_URL,token)
        must(status==404,"NEW_SA_COLLISION_OR_UNKNOWN_HTTP_"+str(status))
        status,perms=call("POST",PROJECT_PERMS,token,
                          {"permissions":sorted(NEEDED)})
        must(status==200,"PROJECT_DELETE_AND_CREATE_CHECK_HTTP_"+str(status))
        got=perms.get("permissions",[])
        must(isinstance(got,list) and all(isinstance(x,str) for x in got) and
             NEEDED.issubset(set(got)),"CREATE_OR_CLEANUP_PERMISSION_UNVERIFIED")
    except (Stop,OSError,ValueError,UnicodeError,TypeError) as exc:
        print("H1B_W1_RESULT=STOP_BEFORE_SA_CREATE")
        print("H1B_W1_REASON="+(str(exc) if isinstance(exc,Stop) else type(exc).__name__))
        print("H1B_W1_SA_CREATE_ATTEMPTED=FALSE")
        return 2
    evidence=ROOT/("oldx-h1b-w1-sa-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd=os.open(MARKER,os.O_CREAT|os.O_EXCL|os.O_WRONLY|
                   getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"w") as f:
            f.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE="+str(evidence)+"\n")
    except OSError:
        print("H1B_W1_RESULT=STOP_MARKER")
        return 2
    state="STOP_AFTER_MARKER"
    reason="UNKNOWN"
    uid=None
    write_attempted=False
    try:
        write_attempted=True
        print("H1B_W1_STAGE=ONE_APPROVED_NEW_SA_CREATE_ATTEMPT",flush=True)
        status,created=call("POST",SA_CREATE,token,{
            "accountId":ID,
            "serviceAccount":{
                "displayName":"OLDX H1B OFF-only private staging mediator",
                "description":"One-time no-user-data isolated staging trial; no user-managed keys"
            }})
        must(status==200,"SA_CREATE_HTTP_"+str(status)+"_POSSIBLE_PARTIAL_WRITE")
        uid=str(created.get("uniqueId",""))
        must(created.get("email")==EMAIL and
             bool(re.fullmatch(r"[0-9]{12,30}",uid)) and
             created.get("projectId")==PROJECT,
             "CREATE_RESPONSE_IDENTITY_UNKNOWN")
        status,now=call("GET",SA_URL,token)
        must(status==200 and now.get("email")==EMAIL and
             str(now.get("uniqueId"))==uid and
             now.get("disabled") is not True,
             "CREATED_SA_READBACK_MISMATCH")
        status,granted=call("POST",SA_URL+":testIamPermissions",token,
                    {"permissions":["iam.serviceAccounts.actAs",
                                    "iam.serviceAccounts.delete"]})
        must(status==200 and
             {"iam.serviceAccounts.actAs","iam.serviceAccounts.delete"}.issubset(
               set(granted.get("permissions",[]))),
             "NEW_SA_ACTAS_OR_DELETE_PERMISSION_UNVERIFIED")
        (evidence/"created-sa-sanitized.json").write_text(json.dumps({
            "email":EMAIL,"uniqueId":uid,"project":PROJECT,
            "new_user_managed_keys_requested":False,
            "new_iam_bindings_requested":False,
            "resource_actAs_and_delete_permissions":"RETURNED",
            "next":"W3 private_OFF service only after separate guard",
            "cloud_resource_writes":"ONE_NEW_SERVICE_ACCOUNT_CREATE"},indent=2)+"\n")
        state="NEW_NO_KEY_SA_CREATED_RIGHTS_PASS_WITH_LIMITS"
        reason="SA_UID_READBACK_AND_ACTAS_DELETE_PASS"
    except (Stop,OSError,TypeError,ValueError,UnicodeError) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        with MARKER.open("a") as f:
            if uid:
                f.write("SA_UID="+uid+"\n")
            f.write("RESULT="+state+"\nREASON="+reason+"\n")
        print("H1B_W1_SA_UID="+(uid if uid else "UNKNOWN"))
        print("H1B_W1_SA_CREATE_ATTEMPTED="+str(write_attempted).upper())
        print("H1B_W1_RESULT="+state)
        print("H1B_W1_REASON="+reason)
        print("H1B_W1_CLOUD_RUN_DEPLOY=NOT_ATTEMPTED")
        print("H1B_W1_IAM_BINDINGS_AND_KEYS=NONE_CREATED_BY_THIS_SCRIPT")
        print("H1B_W1_DO_NOT_REPEAT=TRUE")
    return 0 if state=="NEW_NO_KEY_SA_CREATED_RIGHTS_PASS_WITH_LIMITS" else 2

if __name__=="__main__":
    sys.exit(main())
