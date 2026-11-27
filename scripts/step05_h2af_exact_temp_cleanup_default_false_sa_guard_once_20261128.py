#!/usr/bin/env python3
"""BAJUTO/OLDX Step05 H2AF — bounded cleanup of H2AD's ONE temporary probe.

PREREQUISITE: owner already authorized exact guarded cleanup in H2AD scope;
H2AD9 actual screenshot showed PAUSED, ONE AttemptStarted/Finished, status
NOT_FOUND, and ZERO exact Cloud Run /healthz request logs. HTTP health gate
is NOT a PASS; cleanup does not magically certify hosted Cloud Run success.

One job DELETE -> exact 404, one service-only ETag-guarded probe Invoker
removal preserving Owner, one probe SA DISABLE -> UID readback, one numeric-UID
SA DELETE -> 404 readback. No other services, IAM, production, Firebase,
KMS, Product or Registry changes. No retries or automated rollback of any
failed write; local root receipt marks each attempted stage.
"""
from __future__ import annotations
import json, os, platform, re, ssl, subprocess, sys
from pathlib import Path
from urllib import error,request

ROOT=Path("/root")
PROJECT="oldx-staging"
OWNER="yasminparmar087@gmail.com"
REGION="asia-south1"
JOBID="oldx-h2ad-off-healthz-20261128"
JOB=f"projects/{PROJECT}/locations/{REGION}/jobs/{JOBID}"
SERVICE=f"projects/{PROJECT}/locations/{REGION}/services/oldx-c2-h2-private-gateway"
SERVICE_UID="2d87153f-155e-409f-a418-463c785d8467"
SA="oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
SA_UID="110217058111344002447"
GATEWAY_SA="oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
IMAGE=("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
       "oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2")
JURL="https://cloudscheduler.googleapis.com/v1/"+JOB
SURL="https://run.googleapis.com/v2/"+SERVICE
POLICY=SURL+":getIamPolicy"
SETPOLICY=SURL+":setIamPolicy"
SA_URL="https://iam.googleapis.com/v1/projects/"+PROJECT+"/serviceAccounts/"+SA
SA_UID_URL="https://iam.googleapis.com/v1/projects/"+PROJECT+"/serviceAccounts/"+SA_UID
DISABLE=SA_UID_URL+":disable"
LOGS="https://logging.googleapis.com/v2/entries:list"
LOG_FILTER=(
 'logName="projects/oldx-staging/logs/cloudscheduler.googleapis.com%2Fexecutions" '
 'AND resource.type="cloud_scheduler_job" '
 'AND resource.labels.project_id="oldx-staging" '
 'AND resource.labels.location="asia-south1" '
 'AND resource.labels.job_id="'+JOBID+'" '
 'AND timestamp>="2026-11-27T18:45:00Z"')
GET_ALLOWED={JURL,SURL,POLICY,SA_URL}
POST_ALLOWED={LOGS,SETPOLICY,DISABLE}
DELETE_ALLOWED={JURL,SA_UID_URL}
H2AD5=ROOT/".oldx-step05-h2ad5-new-single-job-create-pause-once-20261128"
H2AD8=ROOT/".oldx-step05-h2ad8-one-resume-run-pause-once-20261128"
H2AD9=ROOT/".oldx-step05-h2ad9-post-accepted-run-readonly-delivery-once-20261128"
OLD_H2AE=ROOT/".oldx-step05-h2ae-exact-temp-probe-cleanup-once-20261128"
MARK=ROOT/".oldx-step05-h2af-exact-temp-probe-cleanup-once-20261128"
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
OWNER_M="user:"+OWNER
SA_M="serviceAccount:"+SA

class Stop(Exception):pass
def need(ok,reason):
    if not ok:raise Stop(reason)
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(
 request.ProxyHandler({}),request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())

def call(method,url,token,body=None):
    need((method=="GET" and url in GET_ALLOWED and body is None) or
         (method=="POST" and url in POST_ALLOWED and isinstance(body,dict)) or
         (method=="DELETE" and url in DELETE_ALLOWED and body is None),
         "API_OUTSIDE_EXACT_TEMP_CLEANUP_SCOPE")
    if method=="POST" and url==LOGS:
        need(body.get("resourceNames")==["projects/"+PROJECT]
             and body.get("filter")==LOG_FILTER
             and body.get("pageSize")==100,"LOG_QUERY_DRIFT")
    if method=="POST" and url==SETPOLICY:
        p=body.get("policy") or {}
        bs=p.get("bindings") or []
        need(p.get("version")==1 and len(bs)==1 and
             bs[0]=={"role":"roles/run.invoker","members":[OWNER_M]}
             and isinstance(p.get("etag"),str) and bool(p["etag"]),
             "OWNER_ONLY_IAM_POLICY_PAYLOAD_REQUIRED")
    if method=="POST" and url==DISABLE:
        need(body=={},"DISABLE_BODY_NOT_EMPTY")
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",
             "User-Agent":"BAJUTO-H2AF-frozen-one-probe-cleanup/1"}
    data=None
    if method=="POST":
        headers["Content-Type"]="application/json"
        # IAM disable requires a zero-length HTTP request body.
        data=(b"" if url==DISABLE else
              json.dumps(body,sort_keys=True,separators=(",",":")).encode("utf-8"))
    req=request.Request(url,method=method,headers=headers,data=data)
    try:
        with OPENER.open(req,timeout=35) as response:
            raw=response.read(262145)
            need(len(raw)<=262144,"API_RESPONSE_TOO_LARGE")
            doc=json.loads(raw) if raw else {}
            need(isinstance(doc,dict),"API_RESPONSE_NOT_JSON_OBJECT")
            return response.status,doc
    except error.HTTPError as ex:
        status=ex.code
        ex.close()
        return status,{}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("API_NETWORK_OR_TIMEOUT_POSSIBLE_PARTIAL_WRITE_NO_RETRY")

def trusted(path,required):
    need(path.is_file() and not path.is_symlink() and path.stat().st_uid==0,
         "OWNER_PRIOR_RECEIPT_MISSING")
    ls=path.read_text(encoding="utf-8").splitlines()
    for x in required:need(x in ls,"OWNER_PRIOR_IDENTITY_MISMATCH")
    return ls

def token_base():
    need(sys.argv[1:]==["--h2af-owner-approved-exact-temporary-probe-cleanup-once"],
         "EXACT_CLEANUP_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"ROOT_WSL_REQUIRED")
    need(not MARK.exists() and not MARK.is_symlink(),"H2AF_ALREADY_CONSUMED")
    # The predecessor H2AF stopped before its first write/marker. If this
    # old marker exists, abort instead of assuming its outcome.
    need(not OLD_H2AE.exists() and not OLD_H2AE.is_symlink(),
         "OLD_H2AE_MARKER_EXISTS_POSSIBLE_PARTIAL_CLEANUP_ABORT")
    prior=trusted(H2AD5,("ATTEMPT_CONSUMED=TRUE","PROJECT="+PROJECT,
       "SERVICE_UID="+SERVICE_UID,"PROBE_SA_UID="+SA_UID,"JOB="+JOB,
       "JOB_CREATE_ABOUT_TO_BE_SENT=TRUE","JOB_PAUSE_ABOUT_TO_BE_SENT=TRUE"))
    trusted(H2AD8,("ATTEMPT_CONSUMED=TRUE","PROJECT="+PROJECT,
       "SERVICE_UID="+SERVICE_UID,"PROBE_SA_UID="+SA_UID,
       "JOB="+JOB,"ONE_RESUME_ABOUT_TO_BE_SENT=TRUE",
       "ONE_RUN_ABOUT_TO_BE_SENT=TRUE"))
    trusted(H2AD9,("ATTEMPT=H2AD9_ONE_NEW_LOG_DELIVERY_READONLY",
       "PROJECT="+PROJECT,"JOB="+JOB,
       "GATEWAY_UID="+SERVICE_UID,"PROBE_SA_UID="+SA_UID))
    bases=[s[len("TARGET_BASE="):] for s in prior if s.startswith("TARGET_BASE=")]
    need(len(bases)==1 and
         re.fullmatch(r"https://[A-Za-z0-9.-]+\.run\.app",bases[0]) is not None,
         "FROZEN_RUN_APP_BASE_MISSING")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK)
         and PY.resolve(strict=True).is_file() and CONFIG.is_dir()
         and not CONFIG.is_symlink(),"OWNER_NATIVE_SDK_MISSING")
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
    except subprocess.TimeoutExpired:raise Stop("OWNER_OAUTH_TIMEOUT")
    need(p.returncode==0 and p.stdout.strip(),"OWNER_OAUTH_MISSING")
    token=p.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token) is not None,
         "OWNER_OAUTH_TOKEN_FORMAT_UNKNOWN")
    return token,bases[0]

def check_job(job,base):
    need(job.get("name")==JOB and job.get("state")=="PAUSED",
         "JOB_NOT_SAME_PAUSED_RESOURCE")
    need(job.get("schedule")=="0 0 29 2 *" and
         job.get("timeZone") in ("Etc/UTC","UTC") and
         job.get("attemptDeadline")=="30s",
         "JOB_CRON_DEADLINE_DRIFT")
    target=job.get("httpTarget") or {}
    oidc=target.get("oidcToken") or {}
    need(target.get("uri")==base+"/healthz" and
         target.get("httpMethod")=="GET" and
         oidc.get("serviceAccountEmail")==SA and
         oidc.get("audience")==base,
         "JOB_HEALTH_OIDC_DRIFT")
    need((job.get("retryConfig") or {}).get("retryCount",0)==0,
         "JOB_RETRY_CONFIG_DRIFT")
    need(bool(job.get("lastAttemptTime")),
         "JOB_ATTEMPT_NOT_RECORDED_STOP_BEFORE_DELETE")

def check_service(service,base):
    need(service.get("name")==SERVICE and service.get("uid")==SERVICE_UID,
         "CLOUD_RUN_UID_DRIFT")
    need(service.get("ingress")=="INGRESS_TRAFFIC_INTERNAL_ONLY" and
         service.get("invokerIamDisabled",False) is False and
         service.get("defaultUriDisabled",False) is False and
         service.get("uri")==base,"GATEWAY_INGRESS_OR_DEFAULT_URI_DRIFT")
    tpl=service.get("template") or {}
    cs=tpl.get("containers") or []
    need(tpl.get("serviceAccount")==GATEWAY_SA and len(cs)==1 and
         isinstance(cs[0],dict) and cs[0].get("image")==IMAGE and
         ("OLDX_H2U_MODE","OFF") in {
         (v.get("name"),v.get("value")) for v in cs[0].get("env",[])
         if isinstance(v,dict)},"GATEWAY_OFF_IMAGE_OR_RUNTIME_DRIFT")

def check_policy(policy,expected):
    bs=policy.get("bindings") or []
    need(len(bs)==1 and isinstance(bs[0],dict) and
         bs[0].get("role")=="roles/run.invoker"
         and "condition" not in bs[0] and
         isinstance(bs[0].get("members"),list)
         and set(bs[0]["members"])==set(expected)
         and len(bs[0]["members"])==len(expected)
         and isinstance(policy.get("etag"),str) and bool(policy["etag"]),
         "DIRECT_GATEWAY_POLICY_NOT_EXACT_EXPECTED")

def check_sa(sa,disabled):
    # ProtoJSON may omit a scalar boolean in its default False state.
    # Still require exact email and immutable numeric UID before any write.
    need(sa.get("email")==SA and str(sa.get("uniqueId"))==SA_UID,
         "PROBE_SA_EMAIL_OR_NUMERIC_UID_DRIFT")
    raw=sa.get("disabled",False)
    need(type(raw) is bool and raw is disabled,
         "PROBE_SA_ACTUAL_DISABLED_STATE_DRIFT")

def check_finished_logs(token):
    query={"resourceNames":["projects/"+PROJECT],
           "filter":LOG_FILTER,"orderBy":"timestamp desc","pageSize":100}
    st,doc=call("POST",LOGS,token,query)
    need(st==200,"SCHEDULER_ATTEMPT_LOG_GET_HTTP_"+str(st))
    rows=doc.get("entries",[])
    need(isinstance(rows,list) and not doc.get("nextPageToken"),
         "INCOMPLETE_SCHEDULER_EXECUTION_LOGS")
    start=0;finish=0;values=[]
    for row in rows:
        if not isinstance(row,dict):continue
        labels=(row.get("resource") or {}).get("labels") or {}
        if not isinstance(labels,dict) or labels.get("job_id")!=JOBID or labels.get("location")!=REGION:continue
        data=row.get("jsonPayload") or {}
        if not isinstance(data,dict):continue
        typ=str(data.get("@type") or "")
        if typ.endswith(".AttemptStarted"):start+=1
        if typ.endswith(".AttemptFinished"):
            finish+=1
            status=data.get("status")
            values.append(status)
    print("H2AF_EXISTING_EXACT_ATTEMPT_STARTED="+str(start))
    print("H2AF_EXISTING_EXACT_ATTEMPT_FINISHED="+str(finish))
    print("H2AF_FINISHED_STATUS="+str(values[0]) if values else "H2AF_FINISHED_STATUS=MISSING")
    need(start==1 and finish==1 and values==["NOT_FOUND"],
         "ATTEMPT_NOT_CONCLUSIVELY_FINISHED_AS_EXPECTED")
    return True

def append(line):
    with MARK.open("a",encoding="utf-8") as f:f.write(line+"\n")

def main():
    os.umask(0o077)
    token,base=token_base()
    st,job=call("GET",JURL,token)
    need(st==200,"JOB_PREDELETE_READ_HTTP_"+str(st))
    check_job(job,base)
    st,service=call("GET",SURL,token)
    need(st==200,"SERVICE_UID_PREDELETE_GET_HTTP_"+str(st))
    check_service(service,base)
    st,policy=call("GET",POLICY,token)
    need(st==200,"OWNER_PLUS_PROBE_POLICY_GET_HTTP_"+str(st))
    check_policy(policy,[OWNER_M,SA_M])
    st,sa=call("GET",SA_URL,token)
    need(st==200,"PROBE_SA_GET_HTTP_"+str(st))
    check_sa(sa,False)
    print("H2AF_SA_PREWRITE_EMAIL_UID_ENABLED=VERIFIED")
    print("H2AF_SA_DISABLED_FIELD_PRESENT="+str("disabled" in sa).upper())
    check_finished_logs(token)
    fd=os.open(str(MARK),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT="+PROJECT+
                "\nJOB="+JOB+"\nGATEWAY_UID="+SERVICE_UID+
                "\nSA_UID="+SA_UID+"\n")
    print("H2AF_MARKER=CONSUMED_NO_REPEAT",flush=True)
    append("JOB_DELETE_ABOUT_TO_BE_SENT=TRUE")
    print("H2AF_STAGE=DELETE_EXACT_PAUSED_JOB",flush=True)
    st,_=call("DELETE",JURL,token)
    need(st in (200,204),"EXACT_JOB_DELETE_HTTP_"+str(st)+"_NO_RETRY")
    st,_=call("GET",JURL,token)
    need(st==404,"EXACT_JOB_POST_DELETE_NOT_404")
    append("JOB_DELETE_READBACK_404=TRUE")
    print("H2AF_JOB=DELETED_404_VERIFIED")

    st,pol=call("GET",POLICY,token)
    need(st==200,"POLICY_BEFORE_REVOKE_GET_"+str(st))
    check_policy(pol,[OWNER_M,SA_M])
    payload={"policy":{"etag":pol["etag"],"version":1,
                      "bindings":[{"role":"roles/run.invoker",
                                   "members":[OWNER_M]}]}}
    append("EXACT_PROBE_INVOKER_REMOVE_ABOUT_TO_BE_SENT=TRUE")
    print("H2AF_STAGE=REMOVE_ONLY_PROBE_INVOKER_PRESERVE_OWNER",flush=True)
    st,changed=call("POST",SETPOLICY,token,payload)
    need(st==200,"OWNER_ONLY_POLICY_SET_HTTP_"+str(st)+"_NO_RETRY")
    check_policy(changed,[OWNER_M])
    st,readback=call("GET",POLICY,token)
    need(st==200,"OWNER_POLICY_READBACK_GET_"+str(st))
    check_policy(readback,[OWNER_M])
    append("DIRECT_INVOCATION_OWNER_ONLY=TRUE")
    print("H2AF_GATEWAY_INVOKER=OWNER_ONLY_VERIFIED")

    st,readsa=call("GET",SA_URL,token)
    need(st==200,"SA_BEFORE_DISABLE_GET_"+str(st))
    check_sa(readsa,False)
    append("EXACT_UID_SA_DISABLE_ABOUT_TO_BE_SENT=TRUE")
    print("H2AF_STAGE=DISABLE_TEMP_SA_UID",flush=True)
    st,_=call("POST",DISABLE,token,{})
    need(st in (200,204),"TEMP_SA_DISABLE_HTTP_"+str(st)+"_NO_RETRY")
    st,disabled=call("GET",SA_URL,token)
    need(st==200,"SA_AFTER_DISABLE_GET_"+str(st))
    check_sa(disabled,True)
    append("TEMP_SA_DISABLED_VERIFIED=TRUE")
    print("H2AF_PROBE_SA=DISABLED_UID_VERIFIED")

    # Last phase is explicitly the same dedicated temporary identity, by
    # numeric immutable UID, NEVER a gateway runtime/signing account.
    append("EXACT_UID_SA_DELETE_ABOUT_TO_BE_SENT=TRUE")
    print("H2AF_STAGE=DELETE_SAME_TEMP_SA_NUMERIC_UID",flush=True)
    st,_=call("DELETE",SA_UID_URL,token)
    need(st in (200,204),"TEMP_SA_DELETE_HTTP_"+str(st)+"_NO_RETRY")
    st,_=call("GET",SA_URL,token)
    need(st==404,"TEMP_SA_DELETE_READBACK_NOT_404")
    append("TEMP_SA_DELETE_READBACK_404=TRUE")
    append("RESULT=EXACT_PAUSED_JOB_OWNER_ONLY_IAM_AND_TEMP_SA_CLEANUP_PASS")
    print("H2AF_PROBE_SA=DELETED_404_VERIFIED")
    print("H2AF_CLOUD_RUN_GATEWAY_INGRESS_IMAGE=UNMODIFIED")
    print("H2AF_OTHER_IAM_KMS_FIRESTORE_PRODUCT_WRITES=NONE")
    print("H2AF_HTTP_HEALTH=NOT_VERIFIED_NOT_RETRIED")
    print("H2AF_H2_PRODUCTION=NO_GO")
    print("H2AF_DO_NOT_REPEAT=TRUE")
    print("H2AF_RESULT=EXACT_TEMP_JOB_PROBE_INVOKER_SA_CLEANUP_PASS")

if __name__=="__main__":
    try:main()
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyError) as ex:
        print("H2AF_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_PARTIAL_CLEANUP")
        print("H2AF_REASON="+(str(ex) if isinstance(ex,Stop) else type(ex).__name__))
        print("H2AF_ACTION=DO_NOT_RERUN_RECONCILE_EXACT_STAGE_AND_UID")
        print("H2AF_H2_PRODUCTION=NO_GO")
        sys.exit(2)
