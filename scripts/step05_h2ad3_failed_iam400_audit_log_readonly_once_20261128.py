#!/usr/bin/env python3
"""BAJUTO/OLDX H2AD3: ONE read-only Admin Activity log lookup for H2AD1 IAM400.
No replay of H2AD1/H2AD2, no IAM read/write, no service account mutation,
no Scheduler job, no production or enablement. Does not print private log bodies.
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
PROJECT="oldx-staging"
OWNER="yasminparmar087@gmail.com"
SERVICE="oldx-c2-h2-private-gateway"
SERVICE_UID="2d87153f-155e-409f-a418-463c785d8467"
PROBE_SA="oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
SA_UID="110217058111344002447"
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2AD2=ROOT/".oldx-step05-h2ad2-after-400-reconcile-readonly-once-20261128"
MARKER=ROOT/".oldx-step05-h2ad3-iam400-admin-activity-logs-once-20261128"
URL="https://logging.googleapis.com/v2/entries:list"
FILTER=('logName="projects/oldx-staging/logs/cloudaudit.googleapis.com%2Factivity" '
        'AND timestamp>="2026-11-27T18:35:00Z" '
        'AND timestamp<="2026-11-27T19:25:00Z" '
        'AND protoPayload.methodName:"SetIamPolicy"')
QUERY={"resourceNames":["projects/oldx-staging"],"filter":FILTER,
       "orderBy":"timestamp desc","pageSize":30}

class Stop(Exception):pass
def need(ok,why):
    if not ok:raise Stop(why)
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(
    request.ProxyHandler({}),request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect())

def owner_token():
    need(sys.argv[1:]==["--h2ad3-iam400-exact-admin-activity-readonly-once"],
         "EXACT_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(),"H2AD3_ALREADY_CONSUMED")
    need(H2AD2.is_file() and not H2AD2.is_symlink() and
         H2AD2.stat().st_uid==0,"H2AD2_CONSUMED_MARKER_MISSING")
    old=H2AD2.read_text(encoding="utf-8").splitlines()
    for x in ("ATTEMPT=H2AD2_DISTINCT_POST_HTTP400_READONLY_RECONCILIATION",
              "PROJECT="+PROJECT,"SERVICE_UID="+SERVICE_UID,
              "EXPECTED_SA_UID="+SA_UID):
        need(x in old,"H2AD2_PRIOR_IDENTITY_MISMATCH")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK)
         and PY.resolve(strict=True).is_file() and CONFIG.is_dir()
         and not CONFIG.is_symlink(),"ISOLATED_NATIVE_SDK_MISSING")
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
    need(p.returncode==0 and p.stdout.strip(),"OWNER_OAUTH_NOT_AVAILABLE")
    token=p.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)!=None,
         "OWNER_TOKEN_FORMAT_UNKNOWN")
    return token

def get_category(msg):
    if not isinstance(msg,str):return "NO_MESSAGE"
    low=msg.lower()
    if ("service account" in low or "serviceaccount" in low or
        PROBE_SA.lower() in low) and any(x in low for x in
          ("not found","does not exist","unknown","invalid","not yet")):
        return "PROBE_SERVICE_ACCOUNT_PRINCIPAL_REJECTED"
    if any(x in low for x in ("allowedpolicymemberdomains","allowed policy member domains",
                              "organization policy","org policy","constraint")):
        return "ORG_POLICY_RESTRICTION"
    if "etag" in low or "concurrent" in low:
        return "ETAG_OR_CONCURRENCY"
    if "version" in low and "policy" in low:
        return "POLICY_VERSION"
    if "condition" in low:
        return "CONDITIONAL_POLICY"
    if "permission" in low or "denied" in low:
        return "PERMISSION_REJECTION"
    if "principal" in low or "member" in low:
        return "POLICY_MEMBER_VALIDATION"
    if "invalid" in low or "bad request" in low or "malformed" in low:
        return "INVALID_ARGUMENT_UNCLASSIFIED"
    return "UNCLASSIFIED_NO_RAW_LOG_PRINTED"

def main():
    os.umask(0o077)
    token=owner_token()
    fd=os.open(str(MARKER),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT=ONE_NEW_CLOUD_LOGGING_IAM400_READONLY_LIST\n")
        f.write("PROJECT="+PROJECT+"\nSERVICE_UID="+SERVICE_UID+
                "\nPROBE_SA_UID="+SA_UID+"\n")
    print("H2AD3_MARKER=CONSUMED_NO_REPEAT",flush=True)
    req=request.Request(
        URL,method="POST",
        headers={"Authorization":"Bearer "+token,"Accept":"application/json",
                 "Content-Type":"application/json",
                 "User-Agent":"OLDX-H2AD3-readonly-audit-IAM400/1"},
        data=json.dumps(QUERY,separators=(",",":")).encode("utf-8"))
    try:
        with OPENER.open(req,timeout=35) as r:
            need(r.status==200,"LOG_ENTRIES_LIST_NOT_200")
            raw=r.read(262145)
            need(len(raw)<=262144,"LOG_ENTRIES_RESPONSE_TOO_LARGE")
    except error.HTTPError as e:
        code=e.code
        e.close()
        raise Stop("LOG_ENTRIES_READ_HTTP_"+str(code))
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("LOG_ENTRIES_NETWORK_OR_TLS_STOP")
    data=json.loads(raw)
    need(isinstance(data,dict),"LOG_ENTRIES_RESPONSE_NOT_OBJECT")
    rows=data.get("entries",[])
    need(isinstance(rows,list) and len(rows)<=30,"LOG_ENTRIES_LIST_INVALID")
    target=[]
    for row in rows:
        if not isinstance(row,dict):continue
        pp=row.get("protoPayload")
        if not isinstance(pp,dict):continue
        resource=str(pp.get("resourceName") or "")
        labels=(row.get("resource") or {}).get("labels") or {}
        service_label=labels.get("service_name") if isinstance(labels,dict) else None
        if SERVICE not in resource and service_label!=SERVICE:
            continue
        method=pp.get("methodName","")
        if "setiampolicy" not in str(method).lower():continue
        status=pp.get("status") or {}
        if not isinstance(status,dict):status={}
        code=status.get("code","UNKNOWN")
        msg=status.get("message","")
        if not isinstance(code,int):code="UNKNOWN"
        # Never print unredacted error messages, identities or log entries.
        target.append({"code":code,"category":get_category(msg)})
    print("H2AD3_AUDIT_LOG_QUERY=ONE_BOUNDED_ADMIN_ACTIVITY_READ")
    print("H2AD3_ENTRIES_RETURNED="+str(len(rows)))
    print("H2AD3_MORE_LOG_PAGES="+str(bool(data.get("nextPageToken"))).upper())
    print("H2AD3_EXACT_GATEWAY_ENTRIES="+str(len(target)))
    for i,x in enumerate(target[:5]):
        print("H2AD3_MATCH_"+str(i+1)+"_CODE="+str(x["code"]))
        print("H2AD3_MATCH_"+str(i+1)+"_CATEGORY="+x["category"])
    print("H2AD3_RAW_MESSAGES_AND_PRINCIPALS=NOT_PRINTED")
    print("H2AD3_IAM_RETRY_AND_CLOUD_WRITES=NONE")
    print("H2AD3_HOSTED_HTTP=NOT_TESTED")
    print("H2AD3_H2_PRODUCTION=NO_GO")
    print("H2AD3_DO_NOT_REPEAT=TRUE")
    print("H2AD3_RESULT=ADMIN_ACTIVITY_READ_WITH_LIMITS_NOT_ROOT_CAUSE_PROOF")

if __name__=="__main__":
    try:main()
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as e:
        print("H2AD3_RESULT=STOP_BEFORE_OR_DURING_READONLY_AUDIT")
        print("H2AD3_REASON="+(str(e) if isinstance(e,Stop) else type(e).__name__))
        print("H2AD3_CLOUD_WRITES=NONE")
        print("H2AD3_DO_NOT_REPEAT_IF_MARKER_EXISTS=TRUE")
        print("H2AD3_H2_PRODUCTION=NO_GO")
        sys.exit(2)
