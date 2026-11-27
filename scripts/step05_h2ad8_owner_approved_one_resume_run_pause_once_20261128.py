#!/usr/bin/env python3
"""BAJUTO Step05 H2AD8 — SOURCE ONLY until NEW specific Owner approval.

This is a *different* bounded Cloud Scheduler operation after H2AD6C jobs.run
HTTP400/FAILED_PRECONDITION: one PAUSED->ENABLED resume, exactly one :run
with an EMPTY (zero byte) body, then one safe PAUSE containment attempt.
No repeat of consumed old run requests, job creation, new SA/IAM or Product.
If anything becomes ambiguous, no further run. Preserve local marker.
A successful jobs.run API response is NOT proof of Gateway HTTP 200.
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
OWNER="yasminparmar087@gmail.com"
PROJECT="oldx-staging"
JOB="projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128"
SA="oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
SA_UID="110217058111344002447"
GATEWAY_UID="2d87153f-155e-409f-a418-463c785d8467"
JURL="https://cloudscheduler.googleapis.com/v1/"+JOB
RESUME=JURL+":resume"
RUN=JURL+":run"
PAUSE=JURL+":pause"
ALLOWED_GET={JURL}
ALLOWED_POST={RESUME,RUN,PAUSE}
H2AD5=ROOT/".oldx-step05-h2ad5-new-single-job-create-pause-once-20261128"
H2AD6C=ROOT/".oldx-step05-h2ad6c-minus1-log-guard-one-manual-run-once-20261128"
H2AD7=ROOT/".oldx-step05-h2ad7-post-run400-logging-reconcile-once-20261128"
MARK=ROOT/".oldx-step05-h2ad8-one-resume-run-pause-once-20261128"
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"

class Stop(Exception):pass
def need(ok,why):
    if not ok:raise Stop(why)
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(
    request.ProxyHandler({}),request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect())

def api(method,url,token):
    need((method=="GET" and url in ALLOWED_GET) or
         (method=="POST" and url in ALLOWED_POST),
         "METHOD_OR_URL_OUTSIDE_EXACT_JOB_SCOPE")
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",
             "User-Agent":"BAJUTO-H2AD8-once-resume-run-pause/1"}
    data=None
    if method=="POST":
        # Cloud Scheduler explicitly requires EMPTY request body (not '{}').
        headers["Content-Type"]="application/json"
        data=b""
    req=request.Request(url,method=method,headers=headers,data=data)
    try:
        with OPENER.open(req,timeout=35) as response:
            raw=response.read(65537)
            need(len(raw)<=65536,"API_RESPONSE_TOO_LARGE")
            doc=json.loads(raw) if raw else {}
            need(isinstance(doc,dict),"API_RESPONSE_NOT_OBJECT")
            return response.status,doc
    except error.HTTPError as ex:
        status=ex.code
        ex.close()
        return status,{}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("NETWORK_OR_TIMEOUT_AMBIGUOUS_DO_NOT_RETRY")

def marker_lines(path,required):
    need(path.is_file() and not path.is_symlink() and path.stat().st_uid==0,
         "OWNER_PRIOR_MARKER_MISSING")
    ls=path.read_text(encoding="utf-8").splitlines()
    for x in required:need(x in ls,"OWNER_PRIOR_RECEIPT_IDENTITY_MISMATCH")
    return ls

def preflight():
    need(sys.argv[1:]==["--h2ad8-new-owner-approved-one-resume-run-pause-once"],
         "EXPLICIT_NEW_OWNER_APPROVAL_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"ROOT_UBUNTU_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(),"H2AD8_ALREADY_CONSUMED")
    old=marker_lines(H2AD5,("ATTEMPT_CONSUMED=TRUE","PROJECT="+PROJECT,
        "SERVICE_UID="+GATEWAY_UID,"PROBE_SA_UID="+SA_UID,"JOB="+JOB,
        "JOB_CREATE_ABOUT_TO_BE_SENT=TRUE","JOB_PAUSE_ABOUT_TO_BE_SENT=TRUE"))
    marker_lines(H2AD6C,("ATTEMPT_CONSUMED=TRUE","PROJECT="+PROJECT,
        "GATEWAY_UID="+GATEWAY_UID,"PROBE_SA_UID="+SA_UID,
        "JOB="+JOB,"ONE_JOBS_RUN_ABOUT_TO_BE_SENT=TRUE"))
    marker_lines(H2AD7,("ATTEMPT=H2AD7_POST_RUN400_READONLY_RECONCILIATION",
        "PROJECT="+PROJECT,"GATEWAY_UID="+GATEWAY_UID,
        "PROBE_SA_UID="+SA_UID,"JOB="+JOB))
    base=[l[len("TARGET_BASE="):] for l in old if l.startswith("TARGET_BASE=")]
    need(len(base)==1 and re.fullmatch(r"https://[A-Za-z0-9.-]+\.run\.app",base[0]),
         "FROZEN_DEFAULT_RUN_APP_URI_NOT_VERIFIED")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK)
         and PY.resolve(strict=True).is_file() and CONFIG.is_dir()
         and not CONFIG.is_symlink(),"ISOLATED_OWNER_SDK_NOT_READY")
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
    except subprocess.TimeoutExpired:raise Stop("OWNER_OAUTH_TIMEOUT")
    need(p.returncode==0 and p.stdout.strip(),"OWNER_OAUTH_NOT_AVAILABLE")
    token=p.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token),
         "OWNER_TOKEN_FORMAT_INVALID")
    return token,base[0]

def require_job(job,base,expected_state):
    need(job.get("name")==JOB and job.get("state")==expected_state,
         "JOB_NAME_OR_STATE_DRIFT")
    need(job.get("schedule")=="0 0 29 2 *" and
         job.get("timeZone") in ("Etc/UTC","UTC") and
         job.get("attemptDeadline")=="30s",
         "JOB_SCHEDULE_OR_DEADLINE_CHANGED")
    target=job.get("httpTarget") or {}
    oidc=target.get("oidcToken") or {}
    need(target.get("uri")==base+"/healthz" and
         target.get("httpMethod")=="GET" and
         oidc.get("serviceAccountEmail")==SA and
         oidc.get("audience")==base,
         "JOB_OFF_HEALTH_OR_OIDC_DRIFT")
    retry=job.get("retryConfig") or {}
    need(retry.get("retryCount",0)==0 and
         retry.get("maxRetryDuration","0s") in ("0s",None),
         "JOB_RETRY_POLICY_DRIFT")

def append(line):
    with MARK.open("a",encoding="utf-8") as f:f.write(line+"\n")

def main():
    os.umask(0o077)
    token,base=preflight()
    st,job=api("GET",JURL,token)
    need(st==200,"INITIAL_JOB_GET_HTTP_"+str(st))
    require_job(job,base,"PAUSED")
    need(not job.get("lastAttemptTime"),"POSSIBLE_PREVIOUS_HTTP_DELIVERY_ABORT")
    # Last seen precondition code9 / no execution is prior frozen evidence.
    # Do not infer a successful target request from this job's status field.
    fd=os.open(str(MARK),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT="+PROJECT+"\nJOB="+JOB+
                "\nSERVICE_UID="+GATEWAY_UID+"\nPROBE_SA_UID="+SA_UID+
                "\nTARGET_BASE="+base+"\n")
        f.write("ONE_RESUME_ABOUT_TO_BE_SENT=TRUE\n")
    print("H2AD8_MARKER=CONSUMED_NO_REPEAT",flush=True)
    resumed_attempted=False
    run_attempted=False
    run_api_accepted=False
    pause_attempted=False
    pause_verified=False
    problem="NONE"
    try:
        resumed_attempted=True
        print("H2AD8_STAGE=ONE_JOB_RESUME",flush=True)
        st,res=api("POST",RESUME,token)
        need(st==200 and res.get("name")==JOB,
             "RESUME_REJECTED_OR_AMBIGUOUS_HTTP_"+str(st))
        require_job(res,base,"ENABLED")
        st,enabled=api("GET",JURL,token)
        need(st==200,"POST_RESUME_GET_FAILED_"+str(st))
        require_job(enabled,base,"ENABLED")
        need(not enabled.get("lastAttemptTime"),
             "JOB_ATTEMPT_APPEARED_BEFORE_MANUAL_RUN")
        append("ONE_RUN_ABOUT_TO_BE_SENT=TRUE")
        run_attempted=True
        print("H2AD8_STAGE=ONE_EMPTY_BODY_MANUAL_RUN",flush=True)
        st,run_result=api("POST",RUN,token)
        need(st==200 and run_result.get("name")==JOB,
             "RUN_FAILED_OR_AMBIGUOUS_HTTP_"+str(st))
        run_api_accepted=True
        print("H2AD8_JOBS_RUN_API=HTTP_200_ACCEPTED_NOT_TARGET_PROOF",flush=True)
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as ex:
        problem=str(ex) if isinstance(ex,Stop) else type(ex).__name__
        print("H2AD8_OPERATION_STOP="+problem,flush=True)
    finally:
        # Safety containment: even if resume/run outcome was ambiguous, try to
        # bring the EXACT job back to PAUSED (at most ONE pause POST).
        if resumed_attempted:
            check_status=0
            check={}
            try:check_status,check=api("GET",JURL,token)
            except (Stop,OSError,ValueError,TypeError,UnicodeError):pass
            if check_status==200 and check.get("state")=="PAUSED":
                pause_verified=True
            else:
                pause_attempted=True
                try:
                    append("ONE_PAUSE_ABOUT_TO_BE_SENT=TRUE")
                    print("H2AD8_STAGE=ONE_CONTAINMENT_PAUSE",flush=True)
                    pst,pjob=api("POST",PAUSE,token)
                    if pst==200 and pjob.get("name")==JOB and pjob.get("state")=="PAUSED":
                        pause_verified=True
                except (Stop,OSError,ValueError,TypeError,UnicodeError):
                    pass
            # One final GET to classify the resulting state. Never replay
            # a failed pause within this run, even if still ENABLED.
            try:
                state_status,after=api("GET",JURL,token)
                if state_status==200:
                    pause_verified=(after.get("name")==JOB and
                                    after.get("state")=="PAUSED")
            except (Stop,OSError,ValueError,TypeError,UnicodeError):
                pause_verified=False
    print("H2AD8_RESUME_ATTEMPTED="+str(resumed_attempted).upper())
    print("H2AD8_RUN_ATTEMPTED="+str(run_attempted).upper())
    print("H2AD8_RUN_API_ACCEPTED="+str(run_api_accepted).upper())
    print("H2AD8_PAUSE_ATTEMPTED="+str(pause_attempted).upper())
    print("H2AD8_FINAL_JOB_PAUSED_VERIFIED="+str(pause_verified).upper())
    print("H2AD8_JOB_HTTP_TARGET_STATUS=NOT_INDEPENDENTLY_VERIFIED")
    print("H2AD8_SA_IAM_JOB_CREATE_DELETE_WRITES=NONE")
    print("H2AD8_H2_PRODUCTION=NO_GO")
    print("H2AD8_DO_NOT_REPEAT=TRUE")
    if not pause_verified:
        print("H2AD8_RESULT=STOP_JOB_MAY_REMAIN_ENABLED_NEEDS_EXACT_RECOVERY")
        sys.exit(2)
    if problem!="NONE" or not run_api_accepted:
        print("H2AD8_RESULT=STOP_SAFE_PAUSED_MANUAL_RUN_NOT_PROVEN")
        sys.exit(2)
    print("H2AD8_RESULT=ONE_MANUAL_RUN_ACCEPTED_AND_JOB_REPAUSED_WITH_LIMITS")
    print("H2AD8_NEXT=INDEPENDENT_SCHEDULER_AND_CLOUD_RUN_DELIVERY_READ")

if __name__=="__main__":
    try:main()
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyError) as ex:
        print("H2AD8_RESULT=STOP_BEFORE_OR_DURING_ONE_SHOT")
        print("H2AD8_REASON="+(str(ex) if isinstance(ex,Stop) else type(ex).__name__))
        print("H2AD8_ACTION=DO_NOT_REPEAT_MANUALLY_INSPECT_JOB_STATE")
        print("H2AD8_H2_PRODUCTION=NO_GO")
        sys.exit(2)
