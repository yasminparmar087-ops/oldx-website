#!/usr/bin/env python3
"""BAJUTO Step05 H2AD1: owner-approved ONE temporary Scheduler-probe service account
and ONE direct invoker IAM addition on the exact private OFF-only Gateway.
No Scheduler job creation, execution, KMS, Product, Firestore, Compute or production.

A failed/ambiguous write is NEVER retried or automatically rolled back.
Preserve the one-shot marker and exact resource UID for conditional cleanup.
"""
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
OWNER="yasminparmar087@gmail.com"
PROJECT="oldx-staging"
REGION="asia-south1"
SNAME=f"projects/{PROJECT}/locations/{REGION}/services/oldx-c2-h2-private-gateway"
UID="2d87153f-155e-409f-a418-463c785d8467"
GATEWAY_SA="oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
IMAGE=("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
       "oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2")
PROBE_ID="oldx-h2ad-probe-20261128"
PROBE_SA=PROBE_ID+"@oldx-staging.iam.gserviceaccount.com"
JOB=f"projects/{PROJECT}/locations/{REGION}/jobs/oldx-h2ad-off-healthz-20261128"
BASE_SA="https://iam.googleapis.com/v1/projects/"+PROJECT+"/serviceAccounts"
URL_SA=BASE_SA+"/"+PROBE_SA
URL_SA_CREATE=BASE_SA
URL_JOB="https://cloudscheduler.googleapis.com/v1/"+JOB
SURL="https://run.googleapis.com/v2/"+SNAME
POLICY=SURL+":getIamPolicy"
SETPOLICY=SURL+":setIamPolicy"
ALLOWED_GET={URL_SA,URL_JOB,SURL,POLICY}
ALLOWED_POST={URL_SA_CREATE,SETPOLICY}
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
PRIOR=ROOT/".oldx-step05-h2ad0-scheduler-target-preflight-once-20261128"
MARK=ROOT/".oldx-step05-h2ad1-probe-sa-and-exact-invoker-once-20261128"

class Stop(Exception):pass
def need(ok,reason):
    if not ok:raise Stop(reason)
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())

def call(method,url,token,body=None):
    need((method=="GET" and url in ALLOWED_GET) or
         (method=="POST" and url in ALLOWED_POST),"OUT_OF_SCOPE_API_METHOD")
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",
             "User-Agent":"OLDX-H2AD1-one-probe-sa-and-one-private-invoker/1"}
    data=None
    if body is not None:
        data=json.dumps(body,sort_keys=True,separators=(",",":")).encode("utf-8")
        headers["Content-Type"]="application/json"
    req=request.Request(url,headers=headers,data=data,method=method)
    try:
        with OPENER.open(req,timeout=35) as r:
            raw=r.read(262145)
            need(len(raw)<=262144,"API_RESPONSE_TOO_LARGE")
            obj=json.loads(raw) if raw else {}
            need(isinstance(obj,dict),"API_INVALID_JSON")
            return r.status,obj
    except error.HTTPError as e:
        code=e.code
        e.close()
        return code,{}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("API_NETWORK_TIMEOUT_OR_AMBIGUOUS_WRITE")

def append(line):
    with MARK.open("a",encoding="utf-8") as f:f.write(line+"\n")

def policy_owner_only(p):
    bindings=p.get("bindings",[])
    return (isinstance(bindings,list) and len(bindings)==1 and
      isinstance(bindings[0],dict) and
      bindings[0].get("role")=="roles/run.invoker" and
      bindings[0].get("members")==["user:"+OWNER] and
      "condition" not in bindings[0])

def policy_owner_plus_probe(p):
    bindings=p.get("bindings",[])
    return (isinstance(bindings,list) and len(bindings)==1 and
      isinstance(bindings[0],dict) and
      bindings[0].get("role")=="roles/run.invoker" and
      "condition" not in bindings[0] and
      isinstance(bindings[0].get("members"),list) and
      len(bindings[0]["members"])==2 and
      set(bindings[0]["members"])==
      {"user:"+OWNER,"serviceAccount:"+PROBE_SA})

def inspect_service(s,base):
    need(s.get("name")==SNAME and s.get("uid")==UID,"SERVICE_UID_OR_NAME_DRIFT")
    need(s.get("ingress")=="INGRESS_TRAFFIC_INTERNAL_ONLY" and
         s.get("invokerIamDisabled",False) is False and
         s.get("defaultUriDisabled",False) is False,
         "INGRESS_OR_AUTH_GUARD_DRIFT")
    need(s.get("uri")==base,"RUN_APP_URL_DRIFT")
    t=s.get("template") or {}
    cs=t.get("containers") or []
    need(t.get("serviceAccount")==GATEWAY_SA and len(cs)==1 and
         cs[0].get("image")==IMAGE,"RUNTIME_IDENTITY_OR_IMAGE_DRIFT")
    need(("OLDX_H2U_MODE","OFF") in
         {(x.get("name"),x.get("value")) for x in cs[0].get("env",[])
          if isinstance(x,dict)},"H2U_NO_LONGER_OFF")

def token_and_receipt():
    need(sys.argv[1:]==["--h2ad1-owner-approved-one-probe-sa-exact-invoker-once"],
         "EXACT_OWNER_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"ROOT_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(),"H2AD1_ALREADY_CONSUMED")
    need(PRIOR.is_file() and not PRIOR.is_symlink() and PRIOR.stat().st_uid==0,
         "H2AD0_MARKER_MISSING")
    lines=PRIOR.read_text(encoding="utf-8").splitlines()
    need("RESULT=READONLY_TARGET_URI_AND_RESOURCE_ABSENCE_PASS_WITH_LIMITS" in lines
         and "PROJECT=oldx-staging" in lines and "H2W_SERVICE_UID="+UID in lines,
         "H2AD0_ACTUAL_PASS_NOT_MATCHED")
    paths=[v[len("EVIDENCE="):] for v in lines if v.startswith("EVIDENCE=")]
    need(len(paths)==1,"H2AD0_EVIDENCE_NOT_UNIQUE")
    path=Path(paths[0])
    need(path.parent==ROOT and
         bool(re.fullmatch(r"oldx-h2ad0-scheduler-readonly-\d{8}T\d{6}Z",path.name))
         and path.is_dir() and not path.is_symlink() and path.stat().st_uid==0,
         "H2AD0_EVIDENCE_PATH_INVALID")
    fp=path/"sanitized-preflight.json"
    need(fp.is_file() and not fp.is_symlink() and fp.stat().st_uid==0
         and fp.stat().st_size<=8192,"H2AD0_EVIDENCE_MISSING")
    receipt=json.loads(fp.read_text(encoding="utf-8"))
    base=receipt.get("default_run_app_base_uri")
    need(isinstance(base,str) and
         re.fullmatch(r"https://[A-Za-z0-9.-]+\.run\.app",base)!=None and
         receipt.get("service_uid")==UID and
         receipt.get("scheduler_probe_sa")==PROBE_SA and
         receipt.get("scheduler_probe_job")==JOB and
         receipt.get("new_sa_http")==404 and receipt.get("new_job_http")==404,
         "H2AD0_TARGET_OR_RESOURCE_RECEIPT_DRIFT")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK)
         and PY.resolve(strict=True).is_file() and CONFIG.is_dir()
         and not CONFIG.is_symlink(),"ISOLATED_SDK_OR_AUTH_MISSING")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":str(CLI.parent)+":/usr/bin:/bin",
        "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    try:
        p=subprocess.run([str(CLI),"--quiet","--account="+OWNER,
             "--project="+PROJECT,"auth","print-access-token"],
             env=env,stdin=subprocess.DEVNULL,
             stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=35,check=False)
    except subprocess.TimeoutExpired:raise Stop("ISOLATED_OAUTH_TIMEOUT")
    need(p.returncode==0 and p.stdout.strip(),"ISOLATED_OWNER_OAUTH_MISSING")
    token=p.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)!=None,
         "TOKEN_FORMAT_UNKNOWN")
    return token,base

def main():
    os.umask(0o077)
    token,base=token_and_receipt()
    # New write-time preflight, not a repeat of H2Y readiness.
    st,s=call("GET",SURL,token)
    need(st==200,"FRESH_GATEWAY_GET_HTTP_"+str(st))
    inspect_service(s,base)
    st,p=call("GET",POLICY,token)
    need(st==200 and policy_owner_only(p) and
         isinstance(p.get("etag"),str) and bool(p["etag"]),
         "DIRECT_POLICY_NO_LONGER_OWNER_ONLY")
    st,_=call("GET",URL_SA,token)
    need(st==404,"PROBE_SA_COLLISION_HTTP_"+str(st))
    st,_=call("GET",URL_JOB,token)
    need(st==404,"PROBE_JOB_COLLISION_HTTP_"+str(st))
    fd=os.open(str(MARK),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT="+PROJECT+
                "\nSERVICE_UID="+UID+"\nPROBE_SA="+PROBE_SA+
                "\nPROBE_JOB="+JOB+"\nTARGET_BASE="+base+"\n")
    print("H2AD1_MARKER=CONSUMED_NO_REPEAT",flush=True)
    print("H2AD1_STAGE=ONE_NEW_TEMP_PROBE_SA_CREATE",flush=True)
    append("SA_CREATE_ABOUT_TO_BE_SENT=TRUE")
    st,created=call("POST",URL_SA_CREATE,token,{
        "accountId":PROBE_ID,
        "serviceAccount":{
            "displayName":"OLDX H2AD one-time private OFF health probe",
            "description":"Temporary dedicated OIDC probe; no KMS/Firestore/Product privileges"}})
    need(st==200,"PROBE_SA_CREATE_HTTP_"+str(st)+"_MAYBE_PARTIAL")
    sa_uid=str(created.get("uniqueId",""))
    need(created.get("email")==PROBE_SA and
         re.fullmatch(r"[0-9]{12,30}",sa_uid)!=None and
         created.get("disabled") is not True,"NEW_PROBE_SA_CREATION_UID_UNKNOWN")
    append("SA_UID="+sa_uid)
    st,actual=call("GET",URL_SA,token)
    need(st==200 and actual.get("email")==PROBE_SA and
         str(actual.get("uniqueId"))==sa_uid and
         actual.get("disabled") is not True,
         "NEW_PROBE_SA_READBACK_NOT_VERIFIED")
    # Re-check direct IAM before a privilege grant; keep Owner binding exactly.
    st,pol=call("GET",POLICY,token)
    need(st==200 and policy_owner_only(pol) and bool(pol.get("etag")),
         "DIRECT_IAM_CHANGED_AFTER_SA_CREATE")
    proposed={"etag":pol["etag"],"version":1,
        "bindings":[{"role":"roles/run.invoker",
                     "members":["user:"+OWNER,"serviceAccount:"+PROBE_SA]}]}
    print("H2AD1_STAGE=ONE_SERVICE_ONLY_PROBE_INVOKER_ADDITION",flush=True)
    append("GATEWAY_INVOKER_SET_ABOUT_TO_BE_SENT=TRUE")
    st,new=call("POST",SETPOLICY,token,{"policy":proposed})
    need(st==200 and policy_owner_plus_probe(new),
         "INVOKER_SET_HTTP_OR_RESPONSE_MISMATCH_"+str(st))
    st,verified=call("GET",POLICY,token)
    need(st==200 and policy_owner_plus_probe(verified) and
         isinstance(verified.get("etag"),str) and bool(verified["etag"]),
         "INVOKER_POST_WRITE_READBACK_MISMATCH")
    append("SERVICE_POLICY_ETAG_AFTER="+verified["etag"])
    append("RESULT=PASS_ONE_PROBE_SA_UID_AND_EXACT_GATEWAY_INVOKER")
    print("H2AD1_PROBE_SA_UID="+sa_uid)
    print("H2AD1_TARGET_SERVICE_UID="+UID)
    print("H2AD1_DIRECT_OWNER_BINDING=PRESERVED")
    print("H2AD1_DIRECT_PROBE_INVOKER=VERIFIED_TARGET_ONLY")
    print("H2AD1_SCHEDULER_JOB=NOT_CREATED")
    print("H2AD1_HOSTED_HTTP=NOT_TESTED")
    print("H2AD1_COMPUTE_VPC_KMS_FIRESTORE_PRODUCT_WRITES=NONE")
    print("H2AD1_H2_PRODUCTION=NO_GO")
    print("H2AD1_DO_NOT_REPEAT=TRUE")
    print("H2AD1_RESULT=PASS_ONE_PROBE_SA_UID_AND_EXACT_GATEWAY_INVOKER")

if __name__=="__main__":
    try:
        main()
    except (Stop,OSError,ValueError,TypeError,KeyError,UnicodeError) as ex:
        print("H2AD1_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_PARTIAL_WRITE")
        print("H2AD1_REASON="+(str(ex) if isinstance(ex,Stop) else type(ex).__name__))
        print("H2AD1_ACTION=DO_NOT_RERUN_OR_AUTOCLEANUP_ON_AMBIGUOUS_WRITE")
        print("H2AD1_H2_PRODUCTION=NO_GO")
        sys.exit(2)
