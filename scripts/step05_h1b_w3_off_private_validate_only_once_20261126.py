#!/usr/bin/env python3
"""OLDX Step05 W3: One validateOnly=true Cloud Run v2 PRIVATE/OFF request.

Never creates a Service. Readonly exact W1 SA uid, exact new service collision,
targeted run create/delete/setIamPolicy permissions, then Cloud Run create validateOnly.
The existing G2B remote image is reused, never rebuilt/re-scanned/pushed.
Real deployment is deliberately gated on this validated payload and a separate
same-session UID/etag-guarded rollback script; no hosted tests or resource writes here.
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
from datetime import datetime, timezone
from urllib import request,error,parse

PROJECT="oldx-staging"
REGION="asia-south1"
OWNER="yasminparmar087@gmail.com"
SERVICE="oldx-c2-website-mediator"
SA="oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com"
SA_UID="115445220422157278526"
IMAGE=("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
       "oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e")
ROOT=Path("/root")
SDK=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI=SDK/"bin/gcloud"
PY=SDK/"platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
W1=ROOT/".oldx-h1b-w1-new-no-key-sa-create-once-20261126"
G2B=ROOT/".oldx-h1b-g2b-retained-single-push-once-20261126"
MARKER=ROOT/".oldx-h1b-w3-private-validate-only-once-20261126"
SA_URL=f"https://iam.googleapis.com/v1/projects/{PROJECT}/serviceAccounts/{SA}"
PARENT=f"projects/{PROJECT}/locations/{REGION}"
SERVICE_URL=f"https://run.googleapis.com/v2/{PARENT}/services/{SERVICE}"
PROJECT_TEST=f"https://cloudresourcemanager.googleapis.com/v1/projects/{PROJECT}:testIamPermissions"
CREATE_VALIDATE=f"https://run.googleapis.com/v2/{PARENT}/services?serviceId={SERVICE}&validateOnly=true"
REQUIRED={"run.services.create","run.services.delete","run.services.get","run.services.setIamPolicy"}

class Stop(Exception):pass
def check(ok,reason):
    if not ok:raise Stop(reason)
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())

def call(method,url,token,payload=None):
    check(url in {SA_URL,SERVICE_URL,PROJECT_TEST,CREATE_VALIDATE},"UNEXPECTED_URL")
    body=None
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",
             "User-Agent":"OLDX-H1B-W3-validateOnly/1"}
    if payload is not None:
        body=json.dumps(payload,sort_keys=True,separators=(",",":")).encode("utf-8")
        headers["Content-Type"]="application/json"
    try:
        with OPENER.open(request.Request(url,data=body,headers=headers,method=method),
                         timeout=35) as response:
            raw=response.read(262145)
            check(len(raw)<=262144,"API_RESPONSE_TOO_LARGE")
            obj=json.loads(raw) if raw else {}
            check(isinstance(obj,dict),"API_NOT_JSON_OBJECT")
            return response.status,obj
    except error.HTTPError as exc:
        status=exc.code;exc.close()
        return status,{}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("NETWORK_TIMEOUT_STOP") from None

def shell_env():
    check(sys.argv[1:]==["--w3-off-private-validate-only-once"],"EXACT_FLAG_REQUIRED")
    check(platform.system()=="Linux" and os.geteuid()==0 and
          "microsoft" in platform.release().lower(),"OWNER_WSL_ROOT_REQUIRED")
    check(not MARKER.exists() and not MARKER.is_symlink(),"W3_VALIDATE_MARKER_CONSUMED")
    check(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,
          "NATIVE_SDK_MISMATCH")
    check(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK),
          "NATIVE_GCLOUD_MISSING")
    py=PY.resolve(strict=True)
    check(py.is_relative_to(SDK.resolve(strict=True)) and py.is_file() and
          py.stat().st_uid==0 and os.access(py,os.X_OK),"BUNDLED_PYTHON_MISMATCH")
    check(CONFIG.is_dir() and not CONFIG.is_symlink() and CONFIG.stat().st_uid==0,
          "ISOLATED_CONFIG_MISSING")
    for marker,required in ((W1,("RESULT=NEW_NO_KEY_SA_CREATED_RIGHTS_PASS_WITH_LIMITS",
                                "SA_UID="+SA_UID)),
                            (G2B,("RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED",))):
        check(marker.is_file() and not marker.is_symlink() and marker.stat().st_uid==0,
              "PRIOR_EVIDENCE_MARKER_MISSING")
        lines=marker.read_text(encoding="utf-8").splitlines()
        check(all(s in lines for s in required),"PRIOR_EVIDENCE_MISMATCH")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":str(SDK/"bin")+":/usr/bin:/bin",
                "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    def gcloud(args):
        try:
            p=subprocess.run([str(CLI)]+args,env=env,stdin=subprocess.DEVNULL,
                 stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25,check=False)
        except subprocess.TimeoutExpired:
            raise Stop("GCLOUD_LOCAL_TIMEOUT") from None
        check(p.returncode==0,"GCLOUD_LOCAL_FAILED")
        return p.stdout.decode("utf-8","replace").strip()
    check(gcloud(["auth","list","--filter=status:ACTIVE",
           "--format=value(account)"])==OWNER,"WRONG_OWNER")
    check(gcloud(["config","get-value","project"])==PROJECT,"WRONG_PROJECT")
    token=gcloud(["--quiet","--account="+OWNER,"auth","print-access-token"])
    check(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)),"TOKEN_UNAVAILABLE")
    return token

def service_payload():
    return {
        "description":"Temporary OLDX H1B private compiled-OFF no-user-data staging only",
        "labels":{"oldx-h1b":"off-private"},
        "ingress":"INGRESS_TRAFFIC_ALL",
        "invokerIamDisabled":False,
        "scaling":{"minInstanceCount":0,"maxInstanceCount":1,"scalingMode":"AUTOMATIC"},
        "template":{
            "serviceAccount":SA,
            "timeout":"5s",
            "maxInstanceRequestConcurrency":1,
            "executionEnvironment":"EXECUTION_ENVIRONMENT_GEN2",
            "containers":[{
                "image":IMAGE,
                "ports":[{"containerPort":8080}],
                "resources":{"limits":{"cpu":"1","memory":"512Mi"},
                             "cpuIdle":True,"startupCpuBoost":False}
            }]
        }
    }

def main():
    os.umask(0o077)
    try:
        token=shell_env()
        sa_status,sa=call("GET",SA_URL,token)
        check(sa_status==200 and sa.get("email")==SA and
              str(sa.get("uniqueId"))==SA_UID and sa.get("disabled") is not True,
              "NEW_SA_UID_NO_LONGER_MATCHES")
        run_status,_=call("GET",SERVICE_URL,token)
        check(run_status==404,"NEW_SERVICE_NOT_CONFIRMED_ABSENT_HTTP_"+str(run_status))
        perm_status,perms=call("POST",PROJECT_TEST,token,{"permissions":sorted(REQUIRED)})
        check(perm_status==200 and REQUIRED.issubset(set(perms.get("permissions",[]))),
              "NEW_SERVICE_CREATION_OR_CLEANUP_PERMISSIONS_UNVERIFIED")
    except (Stop,OSError,ValueError,UnicodeError,TypeError) as exc:
        print("H1B_W3V_RESULT=STOP_PREFLIGHT")
        print("H1B_W3V_REASON="+(str(exc) if isinstance(exc,Stop) else type(exc).__name__))
        print("H1B_W3V_CLOUD_RESOURCE_WRITES=NONE")
        return 2
    evidence=ROOT/("oldx-h1b-w3-validate-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd=os.open(MARKER,os.O_CREAT|os.O_EXCL|os.O_WRONLY|
                   getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"w") as f:f.write("ATTEMPT_CONSUMED=TRUE\n")
    except OSError:
        print("H1B_W3V_RESULT=STOP_MARKER")
        return 2
    outcome="STOP_VALIDATE_WITH_LIMITS"
    reason="UNKNOWN"
    try:
        status,reply=call("POST",CREATE_VALIDATE,token,service_payload())
        check(status==200,"CREATE_VALIDATE_ONLY_HTTP_"+str(status))
        check(not reply.get("error"),"VALIDATE_ONLY_OPERATION_ERROR")
        check(not (reply.get("name") and not
                   str(reply["name"]).startswith(PARENT+"/operations/")),
              "VALIDATE_ONLY_OPERATION_NAME_MISMATCH")
        outcome="VALIDATE_ONLY_ACCEPTED_WITH_LIMITS"
        reason="NEW_PRIVATE_OFF_CLOUD_RUN_CONFIG_VALIDATED_NO_CREATION"
        (evidence/"validated-exact-service-request.json").write_text(
           json.dumps(service_payload(),indent=2,sort_keys=True)+"\n",encoding="utf-8")
    except (Stop,OSError,ValueError,UnicodeError,TypeError) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        with MARKER.open("a",encoding="utf-8") as f:
            f.write("RESULT="+outcome+"\nREASON="+reason+"\n")
        print("H1B_W3V_NEW_SA_UID=FROZEN_MATCH")
        print("H1B_W3V_NEW_SERVICE=ABSENT_404_BEFORE_VALIDATE")
        print("H1B_W3V_IMAGE=FROZEN_REMOTE_G2B_DIGEST")
        print("H1B_W3V_RESULT="+outcome)
        print("H1B_W3V_REASON="+reason)
        print("H1B_W3V_CLOUD_RESOURCE_WRITES=NONE")
        print("H1B_W3V_NEW_CLOUD_RUN_SERVICE=NOT_CREATED")
        print("H1B_W3V_DO_NOT_REPEAT=TRUE")
    return 0 if outcome=="VALIDATE_ONLY_ACCEPTED_WITH_LIMITS" else 2

if __name__=="__main__":sys.exit(main())
