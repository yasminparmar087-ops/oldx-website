#!/usr/bin/env python3
"""BAJUTO/OLDX H2AD7: post H2AD6C HTTP400, read-only reconciliation ONLY.
One exact Scheduler job GET + at most two distinct Cloud Logging entries.list
read-method POSTs (Scheduler RunJob Admin Activity, Scheduler execution logs).
NO jobs.run replay, resume, pause, IAM, SA, Cloud Run, KMS or Firestore writes.
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
JOBID="oldx-h2ad-off-healthz-20261128"
JOB="projects/oldx-staging/locations/asia-south1/jobs/"+JOBID
SA="oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
SA_UID="110217058111344002447"
GATEWAY_UID="2d87153f-155e-409f-a418-463c785d8467"
JURL="https://cloudscheduler.googleapis.com/v1/"+JOB
LURL="https://logging.googleapis.com/v2/entries:list"
H2AD5=ROOT/".oldx-step05-h2ad5-new-single-job-create-pause-once-20261128"
H2AD6C=ROOT/".oldx-step05-h2ad6c-minus1-log-guard-one-manual-run-once-20261128"
MARK=ROOT/".oldx-step05-h2ad7-post-run400-logging-reconcile-once-20261128"
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
AUDIT_FILTER=(
 'logName="projects/oldx-staging/logs/cloudaudit.googleapis.com%2Factivity" '
 'AND protoPayload.serviceName="cloudscheduler.googleapis.com" '
 'AND protoPayload.methodName:"RunJob" '
 'AND timestamp>="2026-11-27T18:45:00Z"')
EXEC_FILTER=(
 'logName="projects/oldx-staging/logs/cloudscheduler.googleapis.com%2Fexecutions" '
 'AND resource.type="cloud_scheduler_job" '
 'AND resource.labels.project_id="oldx-staging" '
 'AND resource.labels.location="asia-south1" '
 'AND resource.labels.job_id="'+JOBID+'" '
 'AND timestamp>="2026-11-27T18:45:00Z"')

class Stop(Exception):pass
def need(ok,reason):
    if not ok:raise Stop(reason)
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())

def read_method(method,url,token,body=None):
    need((method=="GET" and url==JURL and body is None) or
         (method=="POST" and url==LURL and
          isinstance(body,dict) and body.get("filter") in (AUDIT_FILTER,EXEC_FILTER)),
         "METHOD_OR_ENDPOINT_OUT_OF_READ_ONLY_ALLOWLIST")
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",
             "User-Agent":"BAJUTO-H2AD7-post-run400-two-logs-one-job-readonly/1"}
    data=None
    if method=="POST":
        headers["Content-Type"]="application/json"
        data=json.dumps(body,separators=(",",":")).encode("utf-8")
    req=request.Request(url,headers=headers,method=method,data=data)
    try:
        with OPENER.open(req,timeout=35) as response:
            need(response.status==200,"READ_HTTP_UNEXPECTED_SUCCESS")
            raw=response.read(131073)
            need(len(raw)<=131072,"READ_RESPONSE_SIZE_CAP")
    except error.HTTPError as ex:
        status=ex.code
        ex.close()
        raise Stop("READ_HTTP_"+str(status))
    except (error.URLError,ssl.SSLError,TimeoutError):
        raise Stop("READ_NETWORK_OR_TLS_TIMEOUT")
    obj=json.loads(raw)
    need(isinstance(obj,dict),"READ_JSON_NOT_OBJECT")
    return obj

def trusted_lines(path,required):
    need(path.is_file() and not path.is_symlink() and path.stat().st_uid==0,
         "PRIOR_ONE_SHOT_MARKER_MISSING")
    lines=path.read_text(encoding="utf-8").splitlines()
    for item in required:
        need(item in lines,"PRIOR_RECEIPT_IDENTITY_DRIFT")
    return lines

def token_and_base():
    need(sys.argv[1:]==["--h2ad7-after-run400-logs-and-job-readonly-once"],
         "EXACT_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"ROOT_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(),"H2AD7_ALREADY_CONSUMED")
    h5=trusted_lines(H2AD5,("ATTEMPT_CONSUMED=TRUE","PROJECT="+PROJECT,
        "SERVICE_UID="+GATEWAY_UID,"PROBE_SA_UID="+SA_UID,"JOB="+JOB,
        "JOB_CREATE_ABOUT_TO_BE_SENT=TRUE","JOB_PAUSE_ABOUT_TO_BE_SENT=TRUE"))
    trusted_lines(H2AD6C,("ATTEMPT_CONSUMED=TRUE","PROJECT="+PROJECT,
        "GATEWAY_UID="+GATEWAY_UID,"PROBE_SA_UID="+SA_UID,
        "JOB="+JOB,"ONE_JOBS_RUN_ABOUT_TO_BE_SENT=TRUE"))
    bases=[s[12:] for s in h5 if s.startswith("TARGET_BASE=")]
    need(len(bases)==1 and
         re.fullmatch(r"https://[A-Za-z0-9.-]+\.run\.app",bases[0]),
         "FROZEN_RUN_APP_BASE_MISSING")
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
        p=subprocess.run([str(CLI),"--quiet","--account="+OWNER,
          "--project="+PROJECT,"auth","print-access-token"],env=env,
          stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
          timeout=35,check=False)
    except subprocess.TimeoutExpired:raise Stop("ISOLATED_OWNER_AUTH_TIMEOUT")
    need(p.returncode==0 and p.stdout.strip(),"ISOLATED_OWNER_AUTH_FAILED")
    token=p.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token),
         "OWNER_TOKEN_INVALID_FORMAT")
    return token,bases[0]

def category(message):
    if not isinstance(message,str):return "NO_MESSAGE"
    s=message.lower()
    if "paus" in s or "not enabled" in s or "not active" in s:
        return "PAUSED_OR_NOT_ENABLED_JOB"
    if "body" in s or "payload" in s or "empty" in s or "json" in s:
        return "REQUEST_BODY_OR_SCHEMA_REJECTION"
    if "permission" in s or "denied" in s or "unauthorized" in s:
        return "AUTH_OR_IAM_REJECTION"
    if "not found" in s or "does not exist" in s:
        return "JOB_NOT_FOUND"
    if "invalid" in s or "argument" in s or "malformed" in s:
        return "INVALID_ARGUMENT_UNCLASSIFIED"
    return "UNKNOWN_NO_RAW_MESSAGE"

def exact_logs(token,kind,filter_value):
    payload={"resourceNames":["projects/"+PROJECT],"filter":filter_value,
             "pageSize":100,"orderBy":"timestamp desc"}
    doc=read_method("POST",LURL,token,payload)
    rows=doc.get("entries",[])
    need(isinstance(rows,list) and len(rows)<=100,
         "LOG_ROWS_INVALID")
    need(not doc.get("nextPageToken"),
         "PAGINATED_LOGS_NOT_EXHAUSTIVE")
    print("H2AD7_"+kind+"_LOGS_RETURNED="+str(len(rows)))
    exact=0
    for row in rows:
        if not isinstance(row,dict):continue
        pp=row.get("protoPayload") or {}
        if kind=="AUDIT":
            if not isinstance(pp,dict):continue
            resource=str(pp.get("resourceName") or "")
            req=pp.get("request") or {}
            reqname=str(req.get("name") or "") if isinstance(req,dict) else ""
            # Avoid attributing other jobs' audit errors to our target.
            if JOB not in resource and JOB not in reqname:continue
            exact+=1
            status=pp.get("status") or {}
            if not isinstance(status,dict):status={}
            code=status.get("code","UNKNOWN")
            if isinstance(code,bool) or not isinstance(code,(str,int)):
                code="UNKNOWN"
            if exact<=5:
                print("H2AD7_EXACT_RUN_AUDIT_"+str(exact)+"_CODE="+str(code))
                print("H2AD7_EXACT_RUN_AUDIT_"+str(exact)+"_CATEGORY="+category(status.get("message","")))
        else:
            exact+=1
    print("H2AD7_"+kind+"_EXACT_JOB_MATCHES="+str(exact))
    return exact

def main():
    os.umask(0o077)
    token,base=token_and_base()
    fd=os.open(str(MARK),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT=H2AD7_POST_RUN400_READONLY_RECONCILIATION\n")
        f.write("PROJECT="+PROJECT+"\nJOB="+JOB+"\n")
        f.write("GATEWAY_UID="+GATEWAY_UID+"\nPROBE_SA_UID="+SA_UID+"\n")
    print("H2AD7_MARKER=CONSUMED_NO_REPEAT")
    job=read_method("GET",JURL,token)
    need(job.get("name")==JOB and job.get("state")=="PAUSED",
         "JOB_NAME_OR_PAUSED_STATE_DRIFT")
    t=job.get("httpTarget") or {}
    oidc=t.get("oidcToken") or {}
    need(t.get("uri")==base+"/healthz" and t.get("httpMethod")=="GET"
         and oidc.get("serviceAccountEmail")==SA and oidc.get("audience")==base,
         "JOB_ENDPOINT_OR_OIDC_DRIFT")
    print("H2AD7_JOB_PAUSED_READONLY_OFF_HEALTH=VERIFIED")
    print("H2AD7_LAST_ATTEMPT_PRESENT="+str(bool(job.get("lastAttemptTime"))).upper())
    status=job.get("status") or {}
    code=status.get("code","OMITTED_OR_PENDING") if isinstance(status,dict) else "UNKNOWN"
    if isinstance(code,bool) or not isinstance(code,(str,int)):
        code="UNKNOWN"
    print("H2AD7_JOB_STATUS_CODE="+str(code))
    exact_logs(token,"AUDIT",AUDIT_FILTER)
    exact_logs(token,"EXECUTION",EXEC_FILTER)
    print("H2AD7_RAW_ERRORS_IDENTITIES_AND_TOKENS=NOT_PRINTED")
    print("H2AD7_JOBS_RUN_RETRY_RESUME_IAM_CLEANUP=NONE")
    print("H2AD7_HTTP_DELIVERY=NOT_CONFIRMED_BY_THIS_READ")
    print("H2AD7_H2_PRODUCTION=NO_GO")
    print("H2AD7_DO_NOT_REPEAT=TRUE")
    print("H2AD7_RESULT=RUN400_JOB_AND_LOGS_READONLY_PASS_WITH_LIMITS")

if __name__=="__main__":
    try:main()
    except (Stop,OSError,ValueError,TypeError,KeyError,UnicodeError) as e:
        print("H2AD7_RESULT=STOP_BEFORE_OR_DURING_READONLY_RECONCILIATION")
        print("H2AD7_REASON="+(str(e) if isinstance(e,Stop) else type(e).__name__))
        print("H2AD7_NO_RUN_RETRY_OR_CLOUD_WRITES=TRUE")
        print("H2AD7_H2_PRODUCTION=NO_GO")
        sys.exit(2)
