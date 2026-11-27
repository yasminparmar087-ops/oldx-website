#!/usr/bin/env python3
"""BAJUTO Step05 H2AD0 — NEW read-only preflight for approved one-off
Cloud Scheduler -> internal Cloud Run OFF /healthz probe.

Checks only *new decision facts*: the service's canonical run.app URI and
collision-free exact NEW probe service account + Scheduler job names. Does
NOT repeat consumed H2Y readiness/IAM/Compute checks. No Cloud writes.
"""
from __future__ import annotations
import json
import os
import platform
import re
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error, parse

ROOT = Path("/root")
PROJECT = "oldx-staging"
REGION = "asia-south1"
OWNER = "yasminparmar087@gmail.com"
SERVICE = f"projects/{PROJECT}/locations/{REGION}/services/oldx-c2-h2-private-gateway"
SERVICE_UID = "2d87153f-155e-409f-a418-463c785d8467"
GATEWAY_SA = "oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
IMAGE = ("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
         "oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2")
PROBE_SA = "oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com"
PROBE_JOB = f"projects/{PROJECT}/locations/{REGION}/jobs/oldx-h2ad-off-healthz-20261128"
CLI = ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY = ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG = ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2AC = ROOT/".oldx-step05-h2ac-scheduler-api-enable-approved-once-20261128"
H2W = ROOT/".oldx-step05-h2w-new-internal-off-cloudrun-service-once-20261127"
MARKER = ROOT/".oldx-step05-h2ad0-scheduler-target-preflight-once-20261128"
URL_SERVICE = "https://run.googleapis.com/v2/" + SERVICE
URL_SA = "https://iam.googleapis.com/v1/projects/" + PROJECT + "/serviceAccounts/" + PROBE_SA
URL_JOB = "https://cloudscheduler.googleapis.com/v1/" + PROBE_JOB

class Stop(Exception):
    pass

def need(ok, msg):
    if not ok:
        raise Stop(msg)

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

OPENER = request.build_opener(
    request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect())

def oauth():
    need(sys.argv[1:] == ["--h2ad0-owner-approved-probe-exact-target-readonly-once"],
         "EXACT_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(), "ROOT_UBUNTU_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(), "H2AD0_ALREADY_CONSUMED")
    for old in (H2AC, H2W):
        need(old.is_file() and not old.is_symlink() and old.stat().st_uid == 0,
             "OLD_APPROVED_RECEIPT_MISSING")
    ac = H2AC.read_text(encoding="utf-8").splitlines()
    for item in ("ATTEMPT_CONSUMED=TRUE", "PROJECT=oldx-staging",
                 "SERVICE=cloudscheduler.googleapis.com",
                 "RESULT=PASS_EXACT_SCHEDULER_API_ENABLED"):
        need(item in ac, "H2AC_ACTUAL_PASS_MARKER_MISMATCH")
    w = H2W.read_text(encoding="utf-8").splitlines()
    for item in ("RESULT=PASS_NEW_INTERNAL_OFF_SERVICE_AND_OWNER_DIRECT_INVOKER_WITH_LIMITS",
                 "SERVICE_UID="+SERVICE_UID, "IMAGE="+IMAGE):
        need(item in w, "H2W_ACTUAL_PASS_MARKER_MISMATCH")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK)
         and PY.resolve(strict=True).is_file() and CONFIG.is_dir()
         and not CONFIG.is_symlink(), "ISOLATED_OWNER_SDK_MISSING")
    env = dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":str(CLI.parent)+":/usr/bin:/bin",
                "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
                "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
                "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
                "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    try:
        p = subprocess.run([str(CLI),"--quiet","--account="+OWNER,
                            "--project="+PROJECT,"auth","print-access-token"],
                           env=env, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                           check=False,timeout=35)
    except subprocess.TimeoutExpired:
        raise Stop("OWNER_OAUTH_TIMEOUT")
    need(p.returncode == 0 and p.stdout.strip(),"OWNER_OAUTH_UNAVAILABLE")
    token = p.stdout.decode("utf-8","strict").strip()
    need(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token) is not None,
         "OWNER_OAUTH_FORMAT_INVALID")
    return token

def get(token,url,size=131072):
    need(url in (URL_SERVICE,URL_SA,URL_JOB),"URL_NOT_ALLOWLISTED")
    req = request.Request(url,method="GET",headers={
        "Authorization":"Bearer "+token,"Accept":"application/json",
        "User-Agent":"OLDX-H2AD0-unique-Scheduler-OIDC-probe-preflight/1"})
    try:
        with OPENER.open(req,timeout=35) as r:
            need(r.status == 200,"UNEXPECTED_GET_STATUS")
            raw = r.read(size+1)
            need(len(raw)<=size,"GET_RESPONSE_CAP")
    except error.HTTPError as exc:
        status=exc.code
        exc.close()
        return status, {}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("GET_NETWORK_OR_TLS_UNKNOWN")
    obj=json.loads(raw)
    need(isinstance(obj,dict),"GET_JSON_NOT_OBJECT")
    return 200,obj

def main():
    os.umask(0o077)
    token=oauth()
    evidence = ROOT/("oldx-h2ad0-scheduler-readonly-"+
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    evidence.mkdir(mode=0o700)
    fd=os.open(str(MARKER),os.O_WRONLY|os.O_CREAT|os.O_EXCL|
               getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("ATTEMPT_CONSUMED=TRUE\nPROJECT="+PROJECT+
                "\nH2W_SERVICE_UID="+SERVICE_UID+"\nEVIDENCE="+str(evidence)+"\n")
    print("H2AD0_MARKER=CONSUMED_NO_REPEAT")
    code,service=get(token,URL_SERVICE)
    need(code == 200,"FRESH_H2W_SERVICE_GET_HTTP_"+str(code))
    need(service.get("name")==SERVICE and service.get("uid")==SERVICE_UID,
         "FRESH_GATEWAY_SERVICE_UID_DRIFT")
    need(service.get("ingress")=="INGRESS_TRAFFIC_INTERNAL_ONLY",
         "FRESH_GATEWAY_NOT_INTERNAL_ONLY")
    need(service.get("invokerIamDisabled",False) is False,
         "FRESH_GATEWAY_INVOKER_IAM_DISABLED")
    need(service.get("defaultUriDisabled",False) is False,
         "FRESH_GATEWAY_RUN_APP_URL_DISABLED")
    template=service.get("template") or {}
    cs=template.get("containers") or []
    need(template.get("serviceAccount")==GATEWAY_SA and len(cs)==1
         and isinstance(cs[0],dict) and cs[0].get("image")==IMAGE,
         "FRESH_GATEWAY_RUNTIME_IDENTITY_OR_IMAGE_DRIFT")
    need(("OLDX_H2U_MODE","OFF") in
         {(e.get("name"),e.get("value")) for e in cs[0].get("env",[])
          if isinstance(e,dict)}, "FRESH_GATEWAY_NOT_OFF")
    base=service.get("uri")
    need(isinstance(base,str) and len(base)<400,"DEFAULT_RUN_APP_URI_MISSING")
    url=parse.urlsplit(base)
    need(url.scheme=="https" and url.hostname
         and url.hostname.endswith(".run.app") and
         url.username is None and url.password is None and
         url.port is None and url.path in ("","/") and
         not url.query and not url.fragment,"DEFAULT_URI_NOT_EXACT_RUN_APP")
    base=base.rstrip("/")
    need(base.startswith("https://") and
         re.fullmatch(r"https://[A-Za-z0-9.-]+\.run\.app",base) is not None,
         "DEFAULT_URI_SHAPE_UNEXPECTED")
    # Newly needed collision checks, NOT earlier project-wide inventory.
    sa_status,_=get(token,URL_SA,32768)
    need(sa_status==404,"PROBE_SA_NAME_NOT_CONFIRMED_UNUSED_HTTP_"+str(sa_status))
    job_status,_=get(token,URL_JOB,32768)
    need(job_status==404,"PROBE_JOB_NAME_NOT_CONFIRMED_UNUSED_HTTP_"+str(job_status))
    result={
        "project":PROJECT,"region":REGION,"target_service":SERVICE,
        "service_uid":SERVICE_UID,"image":IMAGE,
        "default_run_app_base_uri":base,"test_path":"/healthz",
        "scheduler_probe_sa":PROBE_SA,"scheduler_probe_job":PROBE_JOB,
        "new_sa_http":404,"new_job_http":404,
        "direct_service_iam_rechecked":False,
        "effective_inherited_iam_verified":False,"hosted_http_tested":False,
        "cloud_writes":False,"h2":"NO_GO","production":"NO_GO"
    }
    (evidence/"sanitized-preflight.json").write_text(
        json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    with MARKER.open("a",encoding="utf-8") as f:
        f.write("RESULT=READONLY_TARGET_URI_AND_RESOURCE_ABSENCE_PASS_WITH_LIMITS\n")
    print("H2AD0_TARGET_RUN_APP_BASE="+base)
    print("H2AD0_HEALTH_PATH=/healthz")
    print("H2AD0_NEW_PROBE_SA=ABSENT_404")
    print("H2AD0_NEW_SCHEDULER_JOB=ABSENT_404")
    print("H2AD0_GATEWAY_UID_INGRESS_OFF_IMAGE=VERIFIED_AT_READ")
    print("H2AD0_EVIDENCE="+str(evidence))
    print("H2AD0_HOSTED_HTTP=NOT_TESTED")
    print("H2AD0_CLOUD_WRITES=NONE")
    print("H2AD0_PRODUCTION_H2=NO_GO")
    print("H2AD0_DO_NOT_REPEAT=TRUE")
    print("H2AD0_RESULT=READONLY_TARGET_URI_AND_RESOURCE_ABSENCE_PASS_WITH_LIMITS")

if __name__=="__main__":
    try:
        main()
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyError) as exc:
        print("H2AD0_RESULT=STOP_BEFORE_OR_DURING_READONLY_PREFLIGHT")
        print("H2AD0_REASON="+(str(exc) if isinstance(exc,Stop) else type(exc).__name__))
        print("H2AD0_CLOUD_WRITES=NONE")
        print("H2AD0_DO_NOT_REPEAT_IF_MARKER_EXISTS=TRUE")
        print("H2AD0_H2_PRODUCTION=NO_GO")
        sys.exit(2)
