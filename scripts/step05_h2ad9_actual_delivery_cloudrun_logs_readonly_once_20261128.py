#!/usr/bin/env python3
"""BAJUTO/OLDX Step05 H2AD9 — first independent evidence after H2AD8.

One exact paused Scheduler job GET and two bounded read-only Cloud Logging
entries:list calls: this job's Scheduler executions and private Gateway's
Cloud Run request logs. NEVER dispatch/replay/resume/pause/create/delete,
write IAM or reveal identity tokens or raw log payloads.
A verified Cloud Run HTTP 200 does not independently verify response BODY.
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
JOBID="oldx-h2ad-off-healthz-20261128"
JOB=f"projects/{PROJECT}/locations/{REGION}/jobs/{JOBID}"
GATEWAY="oldx-c2-h2-private-gateway"
GATEWAY_UID="2d87153f-155e-409f-a418-463c785d8467"
PROBE_SA="oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
PROBE_UID="110217058111344002447"
JURL="https://cloudscheduler.googleapis.com/v1/"+JOB
LOGS="https://logging.googleapis.com/v2/entries:list"
H2AD5=ROOT/".oldx-step05-h2ad5-new-single-job-create-pause-once-20261128"
H2AD8=ROOT/".oldx-step05-h2ad8-one-resume-run-pause-once-20261128"
MARK=ROOT/".oldx-step05-h2ad9-post-accepted-run-readonly-delivery-once-20261128"
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
SINCE="2026-11-27T18:45:00Z"
SCH_FILTER=(
 'logName="projects/oldx-staging/logs/cloudscheduler.googleapis.com%2Fexecutions" '
 'AND resource.type="cloud_scheduler_job" '
 'AND resource.labels.project_id="oldx-staging" '
 'AND resource.labels.location="asia-south1" '
 'AND resource.labels.job_id="'+JOBID+'" '
 'AND timestamp>="'+SINCE+'"')
RUN_FILTER=(
 'logName="projects/oldx-staging/logs/run.googleapis.com%2Frequests" '
 'AND resource.type="cloud_run_revision" '
 'AND resource.labels.project_id="oldx-staging" '
 'AND resource.labels.location="asia-south1" '
 'AND resource.labels.service_name="'+GATEWAY+'" '
 'AND httpRequest.requestMethod="GET" '
 'AND timestamp>="'+SINCE+'"')

class Stop(Exception):pass
def need(ok,reason):
    if not ok:raise Stop(reason)

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

OPENER=request.build_opener(
    request.ProxyHandler({}),request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect())

def google_read(method,url,token,body=None):
    need((method=="GET" and url==JURL and body is None) or
         (method=="POST" and url==LOGS and isinstance(body,dict)
          and body.get("filter") in (SCH_FILTER,RUN_FILTER)
          and body.get("resourceNames")==["projects/"+PROJECT]
          and body.get("pageSize")==100),
         "READ_ONLY_API_ALLOWLIST_REJECTED")
    headers={"Authorization":"Bearer "+token,
             "Accept":"application/json",
             "User-Agent":"BAJUTO-H2AD9-exact-OFF-health-delivery-readonly/1"}
    data=None
    if method=="POST":
        headers["Content-Type"]="application/json"
        data=json.dumps(body,separators=(",",":")).encode("utf-8")
    req=request.Request(url,method=method,data=data,headers=headers)
    try:
        with OPENER.open(req,timeout=35) as response:
            need(response.status==200,"READ_API_SUCCESS_STATUS_NOT_200")
            raw=response.read(262145)
            need(len(raw)<=262144,"READ_RESPONSE_TOO_LARGE")
    except error.HTTPError as ex:
        code=ex.code
        ex.close()
        raise Stop("READ_HTTP_"+str(code))
    except (error.URLError,ssl.SSLError,TimeoutError):
        raise Stop("READ_API_NETWORK_OR_TLS_UNKNOWN")
    obj=json.loads(raw)
    need(isinstance(obj,dict),"READ_RESPONSE_NOT_JSON_OBJECT")
    return obj

def trusted_lines(path,required):
    need(path.is_file() and not path.is_symlink() and path.stat().st_uid==0,
         "PRIOR_ROOT_RECEIPT_MISSING")
    lines=path.read_text(encoding="utf-8").splitlines()
    for v in required:
        need(v in lines,"PRIOR_FROZEN_IDENTITY_MISMATCH")
    return lines

def owner_token_and_base():
    need(sys.argv[1:]==["--h2ad9-independent-off-http-delivery-readonly-once"],
         "EXACT_H2AD9_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0
         and "microsoft" in platform.release().lower(),"ROOT_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(),"H2AD9_ALREADY_CONSUMED")
    h5=trusted_lines(H2AD5,("ATTEMPT_CONSUMED=TRUE","PROJECT="+PROJECT,
        "SERVICE_UID="+GATEWAY_UID,"PROBE_SA_UID="+PROBE_UID,
        "JOB="+JOB,"JOB_CREATE_ABOUT_TO_BE_SENT=TRUE",
        "JOB_PAUSE_ABOUT_TO_BE_SENT=TRUE"))
    h8=trusted_lines(H2AD8,("ATTEMPT_CONSUMED=TRUE","PROJECT="+PROJECT,
        "SERVICE_UID="+GATEWAY_UID,"PROBE_SA_UID="+PROBE_UID,
        "JOB="+JOB,"ONE_RESUME_ABOUT_TO_BE_SENT=TRUE",
        "ONE_RUN_ABOUT_TO_BE_SENT=TRUE"))
    bases=[line[len("TARGET_BASE="):] for line in h5
           if line.startswith("TARGET_BASE=")]
    need(len(bases)==1 and
         re.fullmatch(r"https://[A-Za-z0-9.-]+\.run\.app",bases[0]) is not None
         and "TARGET_BASE="+bases[0] in h8,
         "FROZEN_TARGET_URI_NOT_MATCHED")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK)
         and PY.resolve(strict=True).is_file()
         and CONFIG.is_dir() and not CONFIG.is_symlink(),
         "ISOLATED_OWNER_SDK_NOT_READY")
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
             "--project="+PROJECT,"auth","print-access-token"],env=env,
             stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,timeout=35,check=False)
    except subprocess.TimeoutExpired:raise Stop("ISOLATED_OWNER_OAUTH_TIMEOUT")
    need(p.returncode==0 and p.stdout.strip(),"OWNER_OAUTH_UNAVAILABLE")
    token=p.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token) is not None,
         "OWNER_TOKEN_FORMAT_UNEXPECTED")
    return token,bases[0]

def get_logs(token,query,kind):
    payload={"resourceNames":["projects/"+PROJECT],"filter":query,
             "orderBy":"timestamp desc","pageSize":100}
    obj=google_read("POST",LOGS,token,payload)
    rows=obj.get("entries",[])
    need(isinstance(rows,list) and len(rows)<=100,"LOG_ENTRIES_INVALID")
    need(not obj.get("nextPageToken"),"LOG_ENTRIES_PAGINATED_NOT_COMPLETE")
    print("H2AD9_"+kind+"_LOG_ENTRIES="+str(len(rows)))
    return rows

def job_guard(obj,base):
    need(obj.get("name")==JOB and obj.get("state")=="PAUSED",
         "POST_RUN_JOB_NOT_SAME_PAUSED")
    need(obj.get("schedule")=="0 0 29 2 *" and
         obj.get("timeZone") in ("Etc/UTC","UTC") and
         obj.get("attemptDeadline")=="30s",
         "JOB_SCHEDULE_OR_DEADLINE_DRIFT")
    target=obj.get("httpTarget") or {}
    oidc=target.get("oidcToken") or {}
    need(target.get("httpMethod")=="GET" and
         target.get("uri")==base+"/healthz" and
         oidc.get("serviceAccountEmail")==PROBE_SA and
         oidc.get("audience")==base,
         "JOB_OIDC_OR_HEALTHZ_TARGET_DRIFT")
    retry=obj.get("retryConfig") or {}
    need(retry.get("retryCount",0)==0 and
         retry.get("maxRetryDuration","0s") in ("0s",None),
         "JOB_RETRY_CONFIG_DRIFT")

def sched_status(rows):
    finished=[]
    started=0
    for row in rows:
        if not isinstance(row,dict):continue
        labels=(row.get("resource") or {}).get("labels") or {}
        if (not isinstance(labels,dict) or labels.get("job_id")!=JOBID
            or labels.get("location")!=REGION):continue
        data=row.get("jsonPayload") or {}
        if not isinstance(data,dict):continue
        typename=str(data.get("@type") or "")
        if typename.endswith(".AttemptStarted"):started+=1
        if typename.endswith(".AttemptFinished"):
            status=data.get("status")
            status_s=status if isinstance(status,str) else "UNKNOWN"
            # Status is an enum-like label, not raw diagnostics or request data.
            if re.fullmatch(r"[A-Za-z0-9_-]{1,48}",status_s) is None:
                status_s="UNKNOWN"
            finished.append(status_s)
    print("H2AD9_SCHEDULER_ATTEMPT_STARTED_COUNT="+str(started))
    print("H2AD9_SCHEDULER_ATTEMPT_FINISHED_COUNT="+str(len(finished)))
    for i,s in enumerate(finished[:5],1):
        print("H2AD9_ATTEMPT_FINISHED_"+str(i)+"_STATUS="+s)
    return finished

def server_status(rows,base):
    exact=[]
    for row in rows:
        if not isinstance(row,dict):continue
        resource=row.get("resource") or {}
        labels=resource.get("labels") or {}
        if (not isinstance(labels,dict)
            or labels.get("service_name")!=GATEWAY
            or labels.get("location")!=REGION):continue
        req=row.get("httpRequest") or {}
        if not isinstance(req,dict):continue
        if req.get("requestMethod")!="GET":continue
        url=req.get("requestUrl")
        if not isinstance(url,str):continue
        p=parse.urlsplit(url)
        # Avoid raw URL printing; exact base/healthz only.
        if p.scheme!="https" or p.netloc!=parse.urlsplit(base).netloc or p.path!="/healthz":
            continue
        if p.query or p.fragment or p.username or p.password:continue
        code=req.get("status")
        if isinstance(code,bool) or not isinstance(code,int):continue
        exact.append(code)
    print("H2AD9_EXACT_CLOUD_RUN_HEALTH_REQUEST_LOGS="+str(len(exact)))
    for i,v in enumerate(exact[:5],1):
        print("H2AD9_CLOUD_RUN_HEALTH_"+str(i)+"_HTTP_STATUS="+str(v))
    return exact

def main():
    os.umask(0o077)
    token,base=owner_token_and_base()
    fd=os.open(str(MARK),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT=H2AD9_ONE_NEW_LOG_DELIVERY_READONLY\n")
        f.write("PROJECT="+PROJECT+"\nJOB="+JOB+
                "\nGATEWAY_UID="+GATEWAY_UID+"\nPROBE_SA_UID="+PROBE_UID+"\n")
    print("H2AD9_MARKER=CONSUMED_NO_REPEAT",flush=True)
    job=google_read("GET",JURL,token)
    job_guard(job,base)
    print("H2AD9_JOB_FINAL_PAUSED=VERIFIED")
    print("H2AD9_LAST_ATTEMPT_PRESENT="+
          str(bool(job.get("lastAttemptTime"))).upper())
    status=job.get("status") or {}
    code=status.get("code","OMITTED") if isinstance(status,dict) else "UNKNOWN"
    if isinstance(code,bool) or not isinstance(code,(str,int)):code="UNKNOWN"
    print("H2AD9_JOB_LAST_STATUS_CODE="+str(code))
    sched=get_logs(token,SCH_FILTER,"SCHEDULER_EXECUTION")
    finished=sched_status(sched)
    cloud=get_logs(token,RUN_FILTER,"CLOUD_RUN_REQUEST")
    http=server_status(cloud,base)
    if 200 in http:
        verdict="CLOUD_RUN_HTTP_200_LOG_VERIFIED_BODY_NOT_CAPTURED"
    elif http:
        verdict="CLOUD_RUN_HTTP_NON200_OR_UNKNOWN"
    elif "SUCCESS" in finished:
        verdict="SCHEDULER_SUCCESS_LOGGED_RUN_REQUEST_LOG_NOT_MATCHED"
    else:
        verdict="HTTP_DELIVERY_NOT_VERIFIED"
    print("H2AD9_INDEPENDENT_DELIVERY_VERDICT="+verdict)
    print("H2AD9_OFF_JSON_BODY=NOT_CAPTURED_BY_REQUEST_LOGS")
    print("H2AD9_LOG_RAW_PAYLOADS_URLS_TOKENS=NOT_PRINTED")
    print("H2AD9_JOBS_RUN_PAUSE_RESUME_IAM_CLOUD_WRITES=NONE")
    print("H2AD9_JOB_AND_PROBE_CLEANUP=NOT_ATTEMPTED")
    print("H2AD9_H2_PRODUCTION=NO_GO")
    print("H2AD9_DO_NOT_REPEAT=TRUE")
    print("H2AD9_RESULT=ONE_INDEPENDENT_DELIVERY_LOG_READ_PASS_WITH_LIMITS")

if __name__=="__main__":
    try:main()
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyError) as e:
        print("H2AD9_RESULT=STOP_BEFORE_OR_DURING_READONLY_DELIVERY_CHECK")
        print("H2AD9_REASON="+(str(e) if isinstance(e,Stop) else type(e).__name__))
        print("H2AD9_CLOUD_WRITES=NONE")
        print("H2AD9_NO_RETRY_NO_JOB_RESUME_OR_DELETE=TRUE")
        print("H2AD9_H2_PRODUCTION=NO_GO")
        sys.exit(2)
