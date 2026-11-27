#!/usr/bin/env python3
"""BAJUTO Step05 H2AD4: SOURCE ONLY until separate owner approval.
One corrective IAM binding attempt for ALREADY CREATED and verified probe SA.
No SA creation, no project-level IAM, no Scheduler job, no HTTP, KMS or Firebase.
Prior H2AD1 failed with HTTP400; H2AD3 audit hinted principal rejection.
One new bounded attempt can still fail; never replay after marking intent.
"""
from __future__ import annotations
import json
import os
import platform
import re
import ssl
import subprocess
import sys
from pathlib import Path
from urllib import request, error

ROOT=Path("/root")
PROJECT="oldx-staging"
OWNER="yasminparmar087@gmail.com"
SERVICE="projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway"
SERVICE_UID="2d87153f-155e-409f-a418-463c785d8467"
SA="oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
SA_UID="110217058111344002447"
GATEWAY_SA="oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
IMAGE=("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
       "oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2")
SRV_URL="https://run.googleapis.com/v2/"+SERVICE
POLICY=SRV_URL+":getIamPolicy"
SETPOLICY=SRV_URL+":setIamPolicy"
SA_URL="https://iam.googleapis.com/v1/projects/"+PROJECT+"/serviceAccounts/"+SA
GET_ALLOW={SRV_URL,POLICY,SA_URL}
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
OLD1=ROOT/".oldx-step05-h2ad1-probe-sa-and-exact-invoker-once-20261128"
OLD2=ROOT/".oldx-step05-h2ad2-after-400-reconcile-readonly-once-20261128"
OLD3=ROOT/".oldx-step05-h2ad3-iam400-admin-activity-logs-once-20261128"
MARK=ROOT/".oldx-step05-h2ad4-one-corrective-exact-invoker-once-20261128"
OWNER_MEMBER="user:"+OWNER
PROBE_MEMBER="serviceAccount:"+SA

class Stop(Exception):pass
def need(ok,reason):
    if not ok:raise Stop(reason)

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(
    request.ProxyHandler({}),request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect())

def error_category(obj):
    if not isinstance(obj,dict):return "UNAVAILABLE"
    err=obj.get("error") or {}
    msg=str(err.get("message") or "").lower() if isinstance(err,dict) else ""
    if ("service account" in msg or SA.lower() in msg or "principal" in msg) and any(
            x in msg for x in ("not exist","not found","invalid","unknown","not yet","reject")):
        return "PROBE_PRINCIPAL_REJECTED"
    if "etag" in msg:return "ETAG_REJECTED"
    if "condition" in msg:return "POLICY_CONDITION_ERROR"
    if "permission" in msg:return "PERMISSION_ERROR"
    if "constraint" in msg or "organization policy" in msg:return "ORG_POLICY_ERROR"
    if "invalid" in msg or "bad request" in msg:return "INVALID_ARGUMENT_OTHER"
    return "UNCLASSIFIED_NO_RAW_MESSAGE"

def call(method,url,token,body=None):
    need((method=="GET" and url in GET_ALLOW) or
         (method=="POST" and url==SETPOLICY and isinstance(body,dict)),
         "METHOD_OR_RESOURCE_OUTSIDE_EXACT_SCOPE")
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",
             "User-Agent":"BAJUTO-H2AD4-existing-probe-one-correction/1"}
    raw_body=None
    if body is not None:
        headers["Content-Type"]="application/json"
        raw_body=json.dumps(body,separators=(",",":"),sort_keys=True).encode("utf-8")
    req=request.Request(url,method=method,headers=headers,data=raw_body)
    try:
        with OPENER.open(req,timeout=35) as response:
            data=response.read(131073)
            need(len(data)<=131072,"RESPONSE_EXCEEDS_128_KIB")
            parsed=json.loads(data) if data else {}
            need(isinstance(parsed,dict),"RESPONSE_INVALID_JSON")
            return response.status,parsed,"NONE"
    except error.HTTPError as exc:
        status=exc.code
        data=exc.read(8193)
        exc.close()
        category="UNAVAILABLE"
        if len(data)<=8192:
            try:category=error_category(json.loads(data))
            except (ValueError,UnicodeError,TypeError):pass
        return status,{},category
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("UNKNOWN_NETWORK_OR_TIMEOUT_NO_AUTOMATIC_REPLAY")

def marker_lines(path):
    need(path.is_file() and not path.is_symlink() and path.stat().st_uid==0,
         "PRIOR_MARKER_NOT_TRUSTED")
    return path.read_text(encoding="utf-8").splitlines()

def active_token():
    need(sys.argv[1:]==["--h2ad4-owner-approved-one-existing-probe-invoker-correction-once"],
         "EXACT_NEW_OWNER_APPROVAL_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0
         and "microsoft" in platform.release().lower(),"ROOT_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(),"H2AD4_ALREADY_CONSUMED")
    first=marker_lines(OLD1)
    second=marker_lines(OLD2)
    third=marker_lines(OLD3)
    for x in ("ATTEMPT_CONSUMED=TRUE","SERVICE_UID="+SERVICE_UID,
              "SA_UID="+SA_UID,"GATEWAY_INVOKER_SET_ABOUT_TO_BE_SENT=TRUE"):
        need(x in first,"H2AD1_PARTIAL_SA_CREATE_NOT_MATCHED")
    for x in ("ATTEMPT=H2AD2_DISTINCT_POST_HTTP400_READONLY_RECONCILIATION",
              "SERVICE_UID="+SERVICE_UID,"EXPECTED_SA_UID="+SA_UID):
        need(x in second,"H2AD2_RECONCILIATION_MARKER_NOT_MATCHED")
    for x in ("ATTEMPT=ONE_NEW_CLOUD_LOGGING_IAM400_READONLY_LIST",
              "SERVICE_UID="+SERVICE_UID,"PROBE_SA_UID="+SA_UID):
        need(x in third,"H2AD3_AUDIT_MARKER_NOT_MATCHED")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK)
         and PY.resolve(strict=True).is_file() and CONFIG.is_dir()
         and not CONFIG.is_symlink(),"ISOLATED_OWNER_SDK_MISSING")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":str(CLI.parent)+":/usr/bin:/bin",
                "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    try:
        result=subprocess.run([str(CLI),"--quiet","--account="+OWNER,
          "--project="+PROJECT,"auth","print-access-token"],
          env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,timeout=35,check=False)
    except subprocess.TimeoutExpired:raise Stop("OWNER_OAUTH_TIMEOUT")
    need(result.returncode==0 and result.stdout.strip(),"OWNER_OAUTH_UNAVAILABLE")
    token=result.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)!=None,
         "OWNER_OAUTH_TOKEN_INVALID")
    return token

def policy_state(p):
    bs=p.get("bindings",[])
    need(isinstance(bs,list) and isinstance(p.get("etag"),str)
         and bool(p["etag"]),"POLICY_ETAG_OR_BINDINGS_INVALID")
    if len(bs)!=1 or not isinstance(bs[0],dict):return "OTHER"
    b=bs[0]
    if b.get("role")!="roles/run.invoker" or "condition" in b:return "OTHER"
    members=b.get("members")
    if not isinstance(members,list) or len(members)!=len(set(members)):
        return "OTHER"
    if members==[OWNER_MEMBER]:return "OWNER_ONLY"
    if len(members)==2 and set(members)=={OWNER_MEMBER,PROBE_MEMBER}:
        return "OWNER_PLUS_PROBE"
    return "OTHER"

def main():
    os.umask(0o077)
    token=active_token()
    st,sa,_=call("GET",SA_URL,token)
    need(st==200 and sa.get("email")==SA
         and str(sa.get("uniqueId"))==SA_UID
         and sa.get("disabled") is not True,
         "EXACT_EXISTING_PROBE_SA_MISSING_OR_UID_DRIFT")
    st,service,_=call("GET",SRV_URL,token)
    need(st==200 and service.get("name")==SERVICE
         and service.get("uid")==SERVICE_UID
         and service.get("ingress")=="INGRESS_TRAFFIC_INTERNAL_ONLY"
         and service.get("invokerIamDisabled",False) is False
         and service.get("defaultUriDisabled",False) is False,
         "TARGET_SERVICE_UID_OR_INGRESS_DRIFT")
    t=service.get("template") or {}
    cs=t.get("containers") or []
    need(t.get("serviceAccount")==GATEWAY_SA and len(cs)==1
         and isinstance(cs[0],dict) and cs[0].get("image")==IMAGE
         and ("OLDX_H2U_MODE","OFF") in {
              (v.get("name"),v.get("value")) for v in cs[0].get("env",[])
              if isinstance(v,dict)},"GATEWAY_SIGNER_OR_OFF_IMAGE_DRIFT")
    st,policy,_=call("GET",POLICY,token)
    need(st==200,"IAM_DIRECT_POLICY_GET_FAILED_"+str(st))
    state=policy_state(policy)
    if state=="OWNER_PLUS_PROBE":
        print("H2AD4_RESULT=ALREADY_GRANTED_NO_CLOUD_WRITE")
        print("H2AD4_DIRECT_OWNER_AND_PROBE=VERIFIED")
        print("H2AD4_HOSTED_HTTP=NOT_TESTED")
        print("H2AD4_H2_PRODUCTION=NO_GO")
        return
    need(state=="OWNER_ONLY","POLICY_DRIFT_ABORT_NO_IAM_WRITE")
    need(policy.get("version",1) in (1,None),
         "UNEXPECTED_IAM_POLICY_VERSION")
    # Mark intent before the only allowed corrective Cloud write.
    fd=os.open(str(MARK),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT="+PROJECT+"\n")
        f.write("GATEWAY_SERVICE_UID="+SERVICE_UID+"\nPROBE_SA_UID="+SA_UID+"\n")
        f.write("CORRECTIVE_IAM_SET_ABOUT_TO_BE_SENT=TRUE\n")
    print("H2AD4_MARKER=CONSUMED_NO_REPEAT",flush=True)
    print("H2AD4_STAGE=ONE_CORRECTIVE_GATEWAY_ONLY_IAM_SET",flush=True)
    proposed={"policy":{
        "etag":policy["etag"],
        "version":1,
        "bindings":[{"role":"roles/run.invoker",
                     "members":[OWNER_MEMBER,PROBE_MEMBER]}]}}
    status,changed,err=call("POST",SETPOLICY,token,proposed)
    print("H2AD4_IAM_SET_HTTP="+str(status))
    print("H2AD4_IAM_ERROR_CATEGORY="+err)
    need(status==200 and policy_state(changed)=="OWNER_PLUS_PROBE",
         "CORRECTIVE_IAM_SET_REJECTED_OR_UNVERIFIED_NO_RETRY")
    st,verified,_=call("GET",POLICY,token)
    need(st==200 and policy_state(verified)=="OWNER_PLUS_PROBE",
         "CORRECTIVE_IAM_POST_WRITE_READBACK_FAILED_NO_RETRY")
    print("H2AD4_GATEWAY_IAM=OWNER_PLUS_EXACT_PROBE_ONLY")
    print("H2AD4_PROBE_SA_UID="+SA_UID)
    print("H2AD4_SCHEDULER_JOB=NOT_CREATED_OR_RUN")
    print("H2AD4_HOSTED_HTTP=NOT_TESTED")
    print("H2AD4_OTHER_IAM_KMS_FIRESTORE_PRODUCT_WRITES=NONE")
    print("H2AD4_H2_PRODUCTION=NO_GO")
    print("H2AD4_DO_NOT_REPEAT=TRUE")
    print("H2AD4_RESULT=PASS_ONE_CORRECTIVE_EXACT_INVOKER_WITH_LIMITS")

if __name__=="__main__":
    try:main()
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyError) as e:
        print("H2AD4_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_IAM_WRITE")
        print("H2AD4_REASON="+(str(e) if isinstance(e,Stop) else type(e).__name__))
        print("H2AD4_NO_RETRY_NO_AUTOMATIC_CLEANUP=TRUE")
        print("H2AD4_H2_PRODUCTION=NO_GO")
        sys.exit(2)
