#!/usr/bin/env python3
"""BAJUTO Step05 H2AD5: one Owner-approved Scheduler job CREATE and immediate PAUSE.

Identity is the EXISTING H2AD1 temporary SA with H2AD4 verified direct Cloud Run
Invoker binding. No new SA or IAM write, no jobs.run, no hosted HTTP probe yet.
Cron date Feb 29 (next 2028) is a guard, NOT a replacement for pause/cleanup.
Never retry CREATE or PAUSE; ambiguous responses require separate reconciliation.
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
from urllib import request, error, parse

ROOT=Path("/root")
PROJECT="oldx-staging"
OWNER="yasminparmar087@gmail.com"
REGION="asia-south1"
SERVICE=f"projects/{PROJECT}/locations/{REGION}/services/oldx-c2-h2-private-gateway"
SERVICE_UID="2d87153f-155e-409f-a418-463c785d8467"
SA="oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
SA_UID="110217058111344002447"
IMAGE=("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
       "oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2")
GATEWAY_SA="oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
JOB=f"projects/{PROJECT}/locations/{REGION}/jobs/oldx-h2ad-off-healthz-20261128"
SURL="https://run.googleapis.com/v2/"+SERVICE
POLICY=SURL+":getIamPolicy"
SA_URL="https://iam.googleapis.com/v1/projects/"+PROJECT+"/serviceAccounts/"+SA
SA_TEST=SA_URL+":testIamPermissions"
JURL="https://cloudscheduler.googleapis.com/v1/"+JOB
CREATE="https://cloudscheduler.googleapis.com/v1/projects/"+PROJECT+"/locations/"+REGION+"/jobs"
PAUSE=JURL+":pause"
GET_ALLOW={SURL,POLICY,SA_URL,JURL}
POST_ALLOW={SA_TEST,CREATE,PAUSE}
H2AD4=ROOT/".oldx-step05-h2ad4-one-corrective-exact-invoker-once-20261128"
H2AD0=ROOT/".oldx-step05-h2ad0-scheduler-target-preflight-once-20261128"
MARK=ROOT/".oldx-step05-h2ad5-new-single-job-create-pause-once-20261128"
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"

class Stop(Exception): pass
def need(ok,why):
    if not ok: raise Stop(why)
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
OPENER=request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())

def api(method,url,token,payload=None):
    need((method=="GET" and url in GET_ALLOW) or
         (method=="POST" and url in POST_ALLOW and isinstance(payload,dict)),
         "GOOGLE_API_OUTSIDE_EXACT_ALLOWLIST")
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",
             "User-Agent":"BAJUTO-H2AD5-one-paused-future-GET-healthz-job/1"}
    data=None
    if method=="POST":
        headers["Content-Type"]="application/json"
        data=json.dumps(payload,sort_keys=True,separators=(",",":")).encode("utf-8")
    req=request.Request(url,headers=headers,data=data,method=method)
    try:
        with OPENER.open(req,timeout=35) as r:
            raw=r.read(131073)
            need(len(raw)<=131072,"API_RESPONSE_OVER_128K")
            doc=json.loads(raw) if raw else {}
            need(isinstance(doc,dict),"API_RESPONSE_NOT_JSON_OBJECT")
            return r.status,doc,"NONE"
    except error.HTTPError as exc:
        status=exc.code
        exc.close()
        return status,{},"HTTP_"+str(status)
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("NETWORK_OR_TIMEOUT_AMBIGUOUS_DO_NOT_RETRY")

def lines(path):
    need(path.is_file() and not path.is_symlink() and path.stat().st_uid==0,
         "PRIOR_RECEIPT_MISSING_OR_UNTRUSTED")
    return path.read_text(encoding="utf-8").splitlines()

def owner_token_and_base():
    need(sys.argv[1:]==["--h2ad5-owner-approved-one-scheduler-job-create-pause-once"],
         "EXACT_OWNER_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"ROOT_UBUNTU_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(),"H2AD5_ALREADY_CONSUMED")
    h4=lines(H2AD4)
    need("ATTEMPT_CONSUMED=TRUE" in h4 and
         "GATEWAY_SERVICE_UID="+SERVICE_UID in h4 and
         "PROBE_SA_UID="+SA_UID in h4 and
         "CORRECTIVE_IAM_SET_ABOUT_TO_BE_SENT=TRUE" in h4,
         "H2AD4_CORRECTION_ATTEMPT_MARKER_MISMATCH")
    h0=lines(H2AD0)
    need("RESULT=READONLY_TARGET_URI_AND_RESOURCE_ABSENCE_PASS_WITH_LIMITS" in h0,
         "H2AD0_TARGET_URI_RECEIPT_MISSING")
    dirs=[Path(x[9:]) for x in h0 if x.startswith("EVIDENCE=")]
    need(len(dirs)==1 and dirs[0].parent==ROOT and
         re.fullmatch(r"oldx-h2ad0-scheduler-readonly-\d{8}T\d{6}Z",dirs[0].name)
         and dirs[0].is_dir() and not dirs[0].is_symlink() and
         dirs[0].stat().st_uid==0,"H2AD0_EVIDENCE_DIR_UNTRUSTED")
    fp=dirs[0]/"sanitized-preflight.json"
    need(fp.is_file() and not fp.is_symlink() and fp.stat().st_uid==0
         and fp.stat().st_size<=8192,"H2AD0_EVIDENCE_NOT_FOUND")
    doc=json.loads(fp.read_text(encoding="utf-8"))
    base=doc.get("default_run_app_base_uri")
    need(isinstance(base,str) and re.fullmatch(r"https://[A-Za-z0-9.-]+\.run\.app",base)!=None
         and doc.get("service_uid")==SERVICE_UID
         and doc.get("scheduler_probe_sa")==SA
         and doc.get("scheduler_probe_job")==JOB
         and doc.get("new_sa_http")==404 and doc.get("new_job_http")==404,
         "H2AD0_FROZEN_BASE_IDENTITY_MISMATCH")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK)
         and PY.resolve(strict=True).is_file()
         and CONFIG.is_dir() and not CONFIG.is_symlink(),"OWNER_ISOLATED_SDK_MISSING")
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
            env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,timeout=35,check=False)
    except subprocess.TimeoutExpired: raise Stop("OWNER_OAUTH_TIMEOUT")
    need(p.returncode==0 and p.stdout.strip(),"OWNER_OAUTH_NOT_AVAILABLE")
    token=p.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)!=None,
         "OWNER_OAUTH_TOKEN_INVALID")
    return token,base

def inspect_service(doc,base):
    need(doc.get("name")==SERVICE and doc.get("uid")==SERVICE_UID,
         "PRIVATE_GATEWAY_UID_DRIFT")
    need(doc.get("ingress")=="INGRESS_TRAFFIC_INTERNAL_ONLY"
         and doc.get("invokerIamDisabled",False) is False
         and doc.get("defaultUriDisabled",False) is False
         and doc.get("uri")==base,
         "PRIVATE_GATEWAY_INTERNAL_IAM_URI_DRIFT")
    template=doc.get("template") or {}
    containers=template.get("containers") or []
    need(template.get("serviceAccount")==GATEWAY_SA and
         len(containers)==1 and isinstance(containers[0],dict) and
         containers[0].get("image")==IMAGE and
         ("OLDX_H2U_MODE","OFF") in {
          (v.get("name"),v.get("value")) for v in containers[0].get("env",[])
          if isinstance(v,dict)},"PRIVATE_GATEWAY_IMAGE_OR_OFF_DRIFT")

def inspect_iam(policy):
    bs=policy.get("bindings",[])
    need(isinstance(bs,list) and len(bs)==1 and isinstance(bs[0],dict)
         and bs[0].get("role")=="roles/run.invoker"
         and "condition" not in bs[0]
         and isinstance(bs[0].get("members"),list)
         and len(bs[0]["members"])==2
         and set(bs[0]["members"])=={"user:"+OWNER,"serviceAccount:"+SA},
         "DIRECT_IAM_NOT_OWNER_PLUS_EXACT_PROBE_ONLY")

def job_payload(base):
    return {"name":JOB,
      "description":"BAJUTO H2AD temporary single manual OFF-only /healthz probe; delete after bounded evidence",
      "schedule":"0 0 29 2 *", "timeZone":"Etc/UTC",
      "httpTarget":{
          "uri":base+"/healthz","httpMethod":"GET",
          "headers":{"Accept":"application/json"},
          "oidcToken":{"serviceAccountEmail":SA,"audience":base}},
      "attemptDeadline":"30s",
      "retryConfig":{"retryCount":0,"maxRetryDuration":"0s"}}

def inspect_job(job,base):
    need(isinstance(job,dict) and job.get("name")==JOB,
         "SCHEDULER_JOB_NAME_UNEXPECTED")
    need(job.get("schedule")=="0 0 29 2 *" and
         job.get("timeZone") in ("Etc/UTC","UTC") and
         job.get("attemptDeadline")=="30s",
         "SCHEDULER_UNEXPECTED_SCHEDULE_DEADLINE")
    target=job.get("httpTarget") or {}
    oidc=target.get("oidcToken") or {}
    need(target.get("uri")==base+"/healthz" and
         target.get("httpMethod")=="GET" and
         oidc.get("serviceAccountEmail")==SA and
         oidc.get("audience")==base,"SCHEDULER_URI_METHOD_OIDC_DRIFT")
    retry=job.get("retryConfig") or {}
    need(retry.get("retryCount",0)==0 and
         retry.get("maxRetryDuration","0s") in ("0s",None),
         "SCHEDULER_UNEXPECTED_RETRY_POLICY")
    need(not job.get("lastAttemptTime"),"SCHEDULER_ALREADY_ATTEMPTED")

def main():
    os.umask(0o077)
    token,base=owner_token_and_base()
    # Fresh narrowly scoped gate before the new JOB create.
    st,service,_=api("GET",SURL,token)
    need(st==200,"EXACT_GATEWAY_GET_HTTP_"+str(st))
    inspect_service(service,base)
    st,policy,_=api("GET",POLICY,token)
    need(st==200,"EXACT_DIRECT_IAM_GET_HTTP_"+str(st))
    inspect_iam(policy)
    st,sa,_=api("GET",SA_URL,token)
    need(st==200 and sa.get("email")==SA and
         str(sa.get("uniqueId"))==SA_UID and
         sa.get("disabled") is not True,"EXACT_SA_UID_OR_ENABLED_DRIFT")
    st,perms,_=api("POST",SA_TEST,token,{"permissions":["iam.serviceAccounts.actAs"]})
    need(st==200 and "iam.serviceAccounts.actAs" in perms.get("permissions",[]),
         "OWNER_SA_ACTAS_NOT_CONFIRMED")
    st,_,_=api("GET",JURL,token)
    need(st==404,"EXACT_NEW_JOB_NAME_NOT_EMPTY_HTTP_"+str(st))
    fd=os.open(str(MARK),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT="+PROJECT+
                "\nSERVICE_UID="+SERVICE_UID+"\nPROBE_SA_UID="+SA_UID+
                "\nJOB="+JOB+"\nTARGET_BASE="+base+"\n")
    print("H2AD5_MARKER=CONSUMED_NO_REPEAT",flush=True)
    print("H2AD5_STAGE=ONE_NEW_FAR_FUTURE_SCHEDULED_JOB_CREATE",flush=True)
    with MARK.open("a",encoding="utf-8") as f:f.write("JOB_CREATE_ABOUT_TO_BE_SENT=TRUE\n")
    create_status=0
    create_error="UNATTEMPTED"
    try:
        create_status,created,create_error=api("POST",CREATE,token,job_payload(base))
    except Stop:
        # The POST might have been committed: reconcile exact job GET before
        # considering an attempted PAUSE, do not automatically POST CREATE again.
        create_error="NETWORK_OR_TIMEOUT_AFTER_CREATE_MAYBE_APPLIED"
    print("H2AD5_JOB_CREATE_HTTP="+str(create_status))
    print("H2AD5_CREATE_ERROR_CATEGORY="+create_error)
    # Reconcile only exact newly named job, even when create returned ambiguous.
    st,job,_=api("GET",JURL,token)
    need(st==200,"POST_CREATE_EXACT_JOB_NOT_VERIFIED_HTTP_"+str(st))
    inspect_job(job,base)
    state=job.get("state")
    if state=="ENABLED":
        print("H2AD5_STAGE=ONE_IMMEDIATE_JOB_PAUSE",flush=True)
        with MARK.open("a",encoding="utf-8") as f:
            f.write("JOB_PAUSE_ABOUT_TO_BE_SENT=TRUE\n")
        st,paused,_=api("POST",PAUSE,token,{})
        need(st==200,"PAUSE_HTTP_"+str(st)+"_NO_RETRY")
        need(paused.get("state")=="PAUSED",
             "PAUSE_RESPONSE_NOT_PAUSED_NO_RETRY")
    else:
        need(state=="PAUSED","UNEXPECTED_JOB_STATE_NO_AUTOMATIC_DISPATCH")
    st,verified,_=api("GET",JURL,token)
    need(st==200,"PAUSED_JOB_READBACK_HTTP_"+str(st))
    inspect_job(verified,base)
    need(verified.get("state")=="PAUSED","JOB_NOT_PAUSED_AFTER_READBACK")
    need(create_status==200,"CREATE_AMBIGUOUS_BUT_JOB_NOW_PAUSED_NEEDS_REVIEW")
    print("H2AD5_NEW_JOB=EXACT_ONE_CREATED_AND_PAUSED")
    print("H2AD5_TARGET=READONLY_GET_HEALTHZ_WITH_EXACT_OIDC")
    print("H2AD5_NEXT_SCHEDULE=FEB29_NOT_DISPATCHED")
    print("H2AD5_JOB_PAUSED=VERIFIED")
    print("H2AD5_HTTP_DISPATCH=NOT_ATTEMPTED")
    print("H2AD5_PROBE_SA_UID="+SA_UID)
    print("H2AD5_CLOUD_WRITE_SCOPE=ONE_JOB_CREATE_ONE_PAUSE_ONLY")
    print("H2AD5_PRODUCTION_H2=NO_GO")
    print("H2AD5_DO_NOT_REPEAT=TRUE")
    print("H2AD5_RESULT=PASS_ONE_NEW_PAUSED_OIDC_HEALTHZ_JOB_WITH_LIMITS")

if __name__=="__main__":
    try:main()
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyError) as e:
        print("H2AD5_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_PARTIAL_JOB_WRITE")
        print("H2AD5_REASON="+(str(e) if isinstance(e,Stop) else type(e).__name__))
        print("H2AD5_ACTION=DO_NOT_RERUN_OR_MANUALLY_DISPATCH_AMBIGUOUS_JOB")
        print("H2AD5_PRODUCTION_H2=NO_GO")
        sys.exit(2)
