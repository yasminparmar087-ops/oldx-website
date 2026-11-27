#!/usr/bin/env python3
"""BAJUTO/OLDX Step05 H2AD6: exactly ONE approved manual Cloud Scheduler run.

The already-created OIDC job must still be PAUSED and target ONLY GET
/healthz of the unchanged internal-only OFF Gateway. This script sends ONE
jobs.run request, never repeats it and never resumes the schedule. A jobs.run
API success is NOT proof that the Cloud Run HTTP target returned 200.
Run separately scoped H2AD7 execution-log read after H2AD6 to confirm delivery.
"""
from __future__ import annotations
import json
import os
import platform
import re
import ssl
import subprocess
import sys
import time
from pathlib import Path
from urllib import request, error

ROOT=Path("/root")
PROJECT="oldx-staging"
OWNER="yasminparmar087@gmail.com"
JOB="projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128"
SERVICE_UID="2d87153f-155e-409f-a418-463c785d8467"
PROBE_SA="oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
PROBE_SA_UID="110217058111344002447"
JURL="https://cloudscheduler.googleapis.com/v1/"+JOB
RUN_URL=JURL+":run"
OLD=ROOT/".oldx-step05-h2ad5-new-single-job-create-pause-once-20261128"
MARK=ROOT/".oldx-step05-h2ad6-one-manual-paused-job-dispatch-once-20261128"
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"

class Stop(Exception):pass
def need(ok, why):
    if not ok:raise Stop(why)
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(
    request.ProxyHandler({}),request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect())

def api(method, url, token):
    need((method=="GET" and url==JURL) or
         (method=="POST" and url==RUN_URL),
         "ONLY_EXACT_JOB_GET_OR_SINGLE_RUN_PERMITTED")
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",
             "User-Agent":"BAJUTO-H2AD6-once-paused-job-get-healthz/1"}
    data=None
    if method=="POST":
        headers["Content-Type"]="application/json"
        data=b"{}"
    req=request.Request(url,method=method,headers=headers,data=data)
    try:
        with OPENER.open(req,timeout=35) as response:
            raw=response.read(65537)
            need(len(raw)<=65536,"JOB_RESPONSE_OVER_64K")
            doc=json.loads(raw) if raw else {}
            need(isinstance(doc,dict),"JOB_JSON_NOT_OBJECT")
            return response.status,doc
    except error.HTTPError as exc:
        status=exc.code
        exc.close()
        return status,{}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("JOB_API_NETWORK_OR_TIMEOUT_NO_RETRY")

def token_and_target():
    need(sys.argv[1:]==["--h2ad6-owner-approved-one-paused-scheduler-health-run-once"],
         "EXACT_OWNER_APPROVED_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),
         "ROOT_UBUNTU_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(),
         "H2AD6_MARKER_ALREADY_CONSUMED")
    need(OLD.is_file() and not OLD.is_symlink() and OLD.stat().st_uid==0,
         "H2AD5_SUCCESSFUL_CREATE_PAUSE_MARKER_MISSING")
    lines=OLD.read_text(encoding="utf-8").splitlines()
    for x in ("ATTEMPT_CONSUMED=TRUE",
              "PROJECT="+PROJECT,
              "SERVICE_UID="+SERVICE_UID,
              "PROBE_SA_UID="+PROBE_SA_UID,
              "JOB="+JOB,
              "JOB_CREATE_ABOUT_TO_BE_SENT=TRUE",
              "JOB_PAUSE_ABOUT_TO_BE_SENT=TRUE"):
        need(x in lines,"H2AD5_MARKER_IDENTITY_OR_PHASE_NOT_MATCHED")
    bases=[v[len("TARGET_BASE="):] for v in lines if v.startswith("TARGET_BASE=")]
    need(len(bases)==1 and
         re.fullmatch(r"https://[A-Za-z0-9.-]+\.run\.app",bases[0]) is not None,
         "H2AD5_TARGET_BASE_UNEXPECTED")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK)
         and PY.resolve(strict=True).is_file() and CONFIG.is_dir()
         and not CONFIG.is_symlink(),"ISOLATED_OWNER_NATIVE_SDK_MISSING")
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
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_OWNER_OAUTH_TIMEOUT")
    need(p.returncode==0 and bool(p.stdout.strip()),"OWNER_OAUTH_NOT_AVAILABLE")
    token=p.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token) is not None,
         "OWNER_TOKEN_FORMAT_INVALID")
    return token,bases[0]

def inspect_job(doc,base,strict_prior_attempt=True):
    need(doc.get("name")==JOB and doc.get("state")=="PAUSED",
         "EXACT_JOB_NAME_OR_PAUSED_STATE_DRIFT")
    need(doc.get("schedule")=="0 0 29 2 *" and
         doc.get("timeZone") in ("Etc/UTC","UTC") and
         doc.get("attemptDeadline")=="30s",
         "JOB_SCHEDULE_DEADLINE_DRIFT")
    target=doc.get("httpTarget") or {}
    identity=target.get("oidcToken") or {}
    need(target.get("httpMethod")=="GET" and
         target.get("uri")==base+"/healthz" and
         identity.get("serviceAccountEmail")==PROBE_SA and
         identity.get("audience")==base,
         "JOB_HEALTHZ_OR_OIDC_IDENTITY_DRIFT")
    retry=doc.get("retryConfig") or {}
    need(retry.get("retryCount",0)==0 and
         retry.get("maxRetryDuration","0s") in ("0s",None),
         "JOB_RETRY_CONFIG_DRIFT")
    if strict_prior_attempt:
        need(not doc.get("lastAttemptTime"),
             "PREEXISTING_ATTEMPT_ABORT_NO_MORE_DISPATCH")
        need(not doc.get("status"),
             "PREEXISTING_STATUS_ABORT_NO_MORE_DISPATCH")

def main():
    os.umask(0o077)
    token,base=token_and_target()
    st,old=api("GET",JURL,token)
    need(st==200,"EXACT_PAUSED_JOB_GET_HTTP_"+str(st))
    inspect_job(old,base)
    # One-shot marker MUST precede the sole dispatch. Even a 4xx or timeout
    # consumes the operation because backend delivery may be ambiguous.
    fd=os.open(str(MARK),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT="+PROJECT+
                "\nJOB="+JOB+"\nPROBE_SA_UID="+PROBE_SA_UID+
                "\nSERVICE_UID="+SERVICE_UID+"\nTARGET_BASE="+base+"\n")
        f.write("ONE_JOB_RUN_ABOUT_TO_BE_SENT=TRUE\n")
    print("H2AD6_MARKER=CONSUMED_NO_REPEAT",flush=True)
    print("H2AD6_STAGE=EXACT_ONE_MANUAL_SCHEDULER_RUN",flush=True)
    status,accepted=api("POST",RUN_URL,token)
    print("H2AD6_JOB_RUN_HTTP="+str(status),flush=True)
    need(status==200 and accepted.get("name")==JOB,
         "JOB_RUN_NOT_ACCEPTED_OR_RESPONSE_UNKNOWN_NO_RETRY")
    print("H2AD6_MANUAL_DISPATCH=ACCEPTED_ONCE",flush=True)
    # Wait a bounded time for a newly appearing attempt. A GET is observation
    # not another dispatch. API status may lag: never infer HTTP 200 from run().
    latest={}
    for _ in range(7):
        time.sleep(3)
        st,new=api("GET",JURL,token)
        need(st==200,"POST_RUN_JOB_READ_HTTP_"+str(st))
        inspect_job(new,base,strict_prior_attempt=False)
        latest=new
        if new.get("lastAttemptTime"):
            break
    status_obj=latest.get("status") or {}
    code=status_obj.get("code","OMITTED_OR_PENDING") if isinstance(status_obj,dict) else "UNKNOWN"
    print("H2AD6_JOB_REMAINS_PAUSED=VERIFIED")
    print("H2AD6_LAST_ATTEMPT_PRESENT="+str(bool(latest.get("lastAttemptTime"))).upper())
    print("H2AD6_SCHEDULER_STATUS_CODE="+str(code))
    print("H2AD6_DIRECT_HOSTED_HTTP_STATUS_AND_BODY=NOT_YET_VERIFIED")
    print("H2AD6_NEXT=READ_EXECUTION_LOGS_AND_CLOUD_RUN_REQUEST_STATUS_ONCE")
    print("H2AD6_SCHEDULER_JOB_DELETE_AND_IAM_CLEANUP=NOT_ATTEMPTED")
    print("H2AD6_OTHER_CLOUD_WRITES=NONE")
    print("H2AD6_H2_PRODUCTION=NO_GO")
    print("H2AD6_DO_NOT_REPEAT=TRUE")
    print("H2AD6_RESULT=ONE_MANUAL_RUN_ACCEPTED_DELIVERY_NEEDS_INDEPENDENT_PROOF")

if __name__=="__main__":
    try:main()
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyError) as exc:
        print("H2AD6_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_ONE_DISPATCH")
        print("H2AD6_REASON="+(str(exc) if isinstance(exc,Stop) else type(exc).__name__))
        print("H2AD6_ACTION=NO_RERUN_NO_RESUME_NO_AUTOMATIC_CLEANUP")
        print("H2AD6_H2_PRODUCTION=NO_GO")
        sys.exit(2)
