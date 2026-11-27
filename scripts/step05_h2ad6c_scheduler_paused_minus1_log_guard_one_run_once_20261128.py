#!/usr/bin/env python3
"""BAJUTO/OLDX H2AD6C: ONE first manual OFF health attempt with -1 status/log gate.

H2AD6 and H2AD6B stopped before any POST jobs.run. Unlike earlier scripts,
this narrowly accepts the observed possible PAUSED/-1 state only if exact
Scheduler job, no lastAttemptTime, and a bounded, complete Cloud Scheduler
execution-log query shows NO attempts for this exact new job. A log absence
alone does not prove absence of requests; require ALL independent safeguards.
No automatic retry, resume, cleanup, IAM, service or Product changes.
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
JOB_ID="oldx-h2ad-off-healthz-20261128"
JOB="projects/oldx-staging/locations/asia-south1/jobs/"+JOB_ID
GATEWAY_UID="2d87153f-155e-409f-a418-463c785d8467"
PROBE_SA="oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
PROBE_UID="110217058111344002447"
JURL="https://cloudscheduler.googleapis.com/v1/"+JOB
RUN_URL=JURL+":run"
LOGS_URL="https://logging.googleapis.com/v2/entries:list"
H2AD5=ROOT/".oldx-step05-h2ad5-new-single-job-create-pause-once-20261128"
H2AD6=ROOT/".oldx-step05-h2ad6-one-manual-paused-job-dispatch-once-20261128"
H2AD6B=ROOT/".oldx-step05-h2ad6b-status-aware-manual-health-run-once-20261128"
MARK=ROOT/".oldx-step05-h2ad6c-minus1-log-guard-one-manual-run-once-20261128"
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
LOG_FILTER=(
    'logName="projects/oldx-staging/logs/cloudscheduler.googleapis.com%2Fexecutions" '
    'AND resource.type="cloud_scheduler_job" '
    'AND resource.labels.project_id="oldx-staging" '
    'AND resource.labels.location="asia-south1" '
    'AND resource.labels.job_id="'+JOB_ID+'" '
    'AND timestamp>="2026-11-27T18:45:00Z"')
LOG_PAYLOAD={"resourceNames":["projects/oldx-staging"],
             "filter":LOG_FILTER,"orderBy":"timestamp desc","pageSize":100}

class Stop(Exception): pass
def need(ok,why):
    if not ok: raise Stop(why)

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
OPENER=request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())

def call(method,url,token,data=None):
    need((method=="GET" and url==JURL and data is None) or
         (method=="POST" and url==LOGS_URL and data is LOG_PAYLOAD) or
         (method=="POST" and url==RUN_URL and data is None),
         "METHOD_URL_BODY_OUT_OF_EXACT_ALLOWLIST")
    headers={"Authorization":"Bearer "+token,
             "Accept":"application/json",
             "User-Agent":"BAJUTO-H2AD6C-status-minus1-log-gate-one-run/1"}
    body=None
    if method=="POST":
        headers["Content-Type"]="application/json"
        body=json.dumps(data if data is not None else {},
                        separators=(",",":")).encode("utf-8")
    req=request.Request(url,method=method,headers=headers,data=body)
    try:
        with OPENER.open(req,timeout=35) as response:
            need(response.status==200,"API_UNEXPECTED_HTTP_SUCCESS_STATUS")
            raw=response.read(131073)
            need(len(raw)<=131072,"API_RESPONSE_TOO_LARGE")
    except error.HTTPError as exc:
        status=exc.code
        exc.close()
        raise Stop("API_HTTP_"+str(status)+"_NO_RETRY")
    except (error.URLError,ssl.SSLError,TimeoutError):
        raise Stop("API_NETWORK_OR_TIMEOUT_AMBIGUOUS_NO_RETRY")
    doc=json.loads(raw)
    need(isinstance(doc,dict),"API_JSON_RESPONSE_NOT_OBJECT")
    return doc

def token_and_base():
    need(sys.argv[1:]==["--h2ad6c-first-manual-off-health-run-minus1-log-guard-once"],
         "EXACT_OWNER_SCOPED_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),
         "ROOT_OWNER_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(),
         "H2AD6C_ALREADY_CONSUMED")
    # Both predecessor scripts had stopped before their first jobs.run POST.
    # A marker for either means this assumption is invalid, fail closed.
    for marker in (H2AD6,H2AD6B):
        need(not marker.exists() and not marker.is_symlink(),
             "PRIOR_DISPATCH_MARKER_PRESENT_NO_NEW_RUN")
    need(H2AD5.is_file() and not H2AD5.is_symlink() and
         H2AD5.stat().st_uid==0,"H2AD5_SUCCESS_RECEIPT_UNTRUSTED")
    lines=H2AD5.read_text(encoding="utf-8").splitlines()
    for expected in ("ATTEMPT_CONSUMED=TRUE","PROJECT="+PROJECT,
                     "SERVICE_UID="+GATEWAY_UID,"PROBE_SA_UID="+PROBE_UID,
                     "JOB="+JOB,"JOB_CREATE_ABOUT_TO_BE_SENT=TRUE",
                     "JOB_PAUSE_ABOUT_TO_BE_SENT=TRUE"):
        need(expected in lines,"H2AD5_EXPECTED_FROZEN_IDENTITY_MISMATCH")
    bases=[v[len("TARGET_BASE="):] for v in lines
           if v.startswith("TARGET_BASE=")]
    need(len(bases)==1 and re.fullmatch(
         r"https://[A-Za-z0-9.-]+\.run\.app",bases[0]) is not None,
         "H2AD5_EXACT_BASE_URI_INVALID")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK)
         and PY.resolve(strict=True).is_file() and CONFIG.is_dir() and
         not CONFIG.is_symlink(),"ISOLATED_NATIVE_OWNER_SDK_MISSING")
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
    need(p.returncode==0 and bool(p.stdout.strip()),
         "OWNER_OAUTH_UNAVAILABLE")
    token=p.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token) is not None,
         "TOKEN_FORMAT_UNEXPECTED")
    return token,bases[0]

def inspect_exact_job(doc,base):
    need(doc.get("name")==JOB and doc.get("state")=="PAUSED",
         "JOB_NAME_OR_PAUSED_STATE_DRIFT")
    need(doc.get("schedule")=="0 0 29 2 *" and
         doc.get("timeZone") in ("Etc/UTC","UTC") and
         doc.get("attemptDeadline")=="30s",
         "JOB_SCHEDULE_DEADLINE_DRIFT")
    target=doc.get("httpTarget") or {}
    oidc=target.get("oidcToken") or {}
    need(target.get("uri")==base+"/healthz" and
         target.get("httpMethod")=="GET" and
         oidc.get("serviceAccountEmail")==PROBE_SA and
         oidc.get("audience")==base,
         "JOB_READONLY_HEALTH_OR_OIDC_DRIFT")
    retry=doc.get("retryConfig") or {}
    need(retry.get("retryCount",0)==0 and
         retry.get("maxRetryDuration","0s") in ("0s",None),
         "JOB_RETRY_DRIFT")

def validate_pre_run_status(doc):
    need(not doc.get("lastAttemptTime"),
         "PRIOR_LAST_ATTEMPT_TIME_PRESENT_ABORT")
    status=doc.get("status",{})
    need(isinstance(status,dict) and
         set(status.keys()).issubset({"code","message","details"}),
         "NON_STANDARD_STATUS_SHAPE_ABORT")
    code=status.get("code")
    need(isinstance(code,int) and not isinstance(code,bool) and code==-1,
         "NON_MINUS_ONE_OR_MISSING_STATUS_CODE_ABORT")
    need(status.get("message","") in ("",None) and
         status.get("details",[]) in ([],None),
         "NONEMPTY_PREVIOUS_STATUS_MESSAGE_OR_DETAILS_ABORT")
    return code

def ensure_no_logged_attempts(token):
    data=call("POST",LOGS_URL,token,LOG_PAYLOAD)
    rows=data.get("entries",[])
    need(isinstance(rows,list) and len(rows)<=100,
         "SCHEDULER_EXECUTION_LOG_RESPONSE_UNEXPECTED")
    need(not data.get("nextPageToken"),
         "SCHEDULER_EXECUTION_LOG_PAGINATED_UNKNOWN_ABORT")
    print("H2AD6C_EXACT_JOB_LOG_ENTRIES="+str(len(rows)))
    # Fail on ANY exact preexisting Scheduler execution log in this time range.
    # No read from unrelated projects, users, request payloads or private logs.
    need(len(rows)==0,"PRIOR_SCHEDULER_EXECUTION_LOGS_PRESENT_NO_NEW_DISPATCH")

def main():
    os.umask(0o077)
    token,base=token_and_base()
    first=call("GET",JURL,token)
    inspect_exact_job(first,base)
    code=validate_pre_run_status(first)
    print("H2AD6C_JOB=EXACT_PAUSED_READONLY_HEALTH_OIDC")
    print("H2AD6C_PREVIOUS_STATUS_CODE="+str(code))
    print("H2AD6C_LAST_ATTEMPT_TIME=ABSENT")
    ensure_no_logged_attempts(token)
    # Check exact job again immediately after log review, before any write.
    second=call("GET",JURL,token)
    inspect_exact_job(second,base)
    validate_pre_run_status(second)
    fd=os.open(str(MARK),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT="+PROJECT+
                "\nJOB="+JOB+"\nGATEWAY_UID="+GATEWAY_UID+
                "\nPROBE_SA_UID="+PROBE_UID+"\nTARGET_BASE="+base+"\n")
        f.write("ONE_JOBS_RUN_ABOUT_TO_BE_SENT=TRUE\n")
    print("H2AD6C_MARKER=CONSUMED_NO_REPEAT",flush=True)
    print("H2AD6C_STAGE=FIRST_ONE_MANUAL_PAUSED_JOB_RUN",flush=True)
    accepted=call("POST",RUN_URL,token)
    need(accepted.get("name")==JOB,
         "JOBS_RUN_API_RESPONSE_NOT_EXACT_JOB_NO_RETRY")
    print("H2AD6C_JOBS_RUN_API=HTTP_200_ACCEPTED")
    # Bounded read-only observation, not a second dispatch.
    latest={}
    for _ in range(5):
        time.sleep(2)
        latest=call("GET",JURL,token)
        inspect_exact_job(latest,base)
        if latest.get("lastAttemptTime"):break
    status=latest.get("status") or {}
    s_code=status.get("code","UNKNOWN_OR_PENDING") if isinstance(status,dict) else "UNKNOWN"
    if isinstance(s_code,bool) or not isinstance(s_code,(int,str)):
        s_code="UNKNOWN"
    print("H2AD6C_JOB_REMAINS_PAUSED=VERIFIED")
    print("H2AD6C_LAST_ATTEMPT_PRESENT="+str(bool(latest.get("lastAttemptTime"))).upper())
    print("H2AD6C_LAST_SCHEDULER_STATUS_CODE="+str(s_code))
    print("H2AD6C_TARGET_HTTP_200_OR_OFF_BODY=NOT_YET_PROVEN")
    print("H2AD6C_FOLLOWUP=ONE_NEW_READONLY_DELIVERY_AND_CLOUD_RUN_LOG_CHECK")
    print("H2AD6C_JOB_IAM_SA_CLEANUP=NOT_ATTEMPTED")
    print("H2AD6C_OTHER_CLOUD_WRITES=NONE")
    print("H2AD6C_H2_PRODUCTION=NO_GO")
    print("H2AD6C_DO_NOT_REPEAT=TRUE")
    print("H2AD6C_RESULT=ONE_MANUAL_RUN_ACCEPTED_REQUIRES_HTTP_PROOF")

if __name__=="__main__":
    try:main()
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyError) as exc:
        print("H2AD6C_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_ONE_DISPATCH")
        print("H2AD6C_REASON="+(str(exc) if isinstance(exc,Stop) else type(exc).__name__))
        print("H2AD6C_NO_RETRY_NO_RESUME_NO_AUTOMATIC_CLEANUP=TRUE")
        print("H2AD6C_H2_PRODUCTION=NO_GO")
        sys.exit(2)
