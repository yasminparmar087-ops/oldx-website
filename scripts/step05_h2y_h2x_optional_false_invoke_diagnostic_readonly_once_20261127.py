#!/usr/bin/env python3
"""BAJUTO/OLDX Step05 H2X: ONE NEW hosted revision readiness READ-ONLY.
New information only after H2W actual create; NO Cloud Run mutation, IAM,
network probe, registry, KMS, Firestore or old test re-execution.
"""
import json
import os
import platform
import ssl
import subprocess
import sys
from pathlib import Path
from urllib import request, error

ROOT=Path("/root")
OWNER="yasminparmar087@gmail.com"
PROJECT="oldx-staging"
SERVICE="projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway"
UID="2d87153f-155e-409f-a418-463c785d8467"
SA="oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
IMAGE=("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
       "oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2")
CLI=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud"
PY=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2W=ROOT/".oldx-step05-h2w-new-internal-off-cloudrun-service-once-20261127"
URL="https://run.googleapis.com/v2/"+SERVICE

class Stop(Exception): pass
def need(cond,msg):
    if not cond: raise Stop(msg)

def main():
    need(sys.argv[1:]==["--h2y-corrected-h2x-false-default-readonly-once"],"EXACT_FLAG_REQUIRED")
    need(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"ROOT_WSL_REQUIRED")
    need(H2W.is_file() and not H2W.is_symlink() and H2W.stat().st_uid==0,
         "H2W_ACTUAL_PASS_MARKER_MISSING")
    lines=H2W.read_text(encoding="utf-8").splitlines()
    for expected in ("RESULT=PASS_NEW_INTERNAL_OFF_SERVICE_AND_OWNER_DIRECT_INVOKER_WITH_LIMITS",
                     "SERVICE_UID="+UID,"IMAGE="+IMAGE):
        need(expected in lines,"H2W_MARKER_RECEIPT_MISMATCH")
    need(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK),
         "NATIVE_GCLOUD_MISSING")
    need(PY.resolve(strict=True).is_file() and CONFIG.is_dir() and
         not CONFIG.is_symlink(),"ISOLATED_AUTH_MISSING")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"CLOUDSDK_CONFIG":str(CONFIG),
                "CLOUDSDK_PYTHON":str(PY),
                "PATH":str(CLI.parent)+":/usr/bin:/bin",
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
    except subprocess.TimeoutExpired: raise Stop("ISOLATED_TOKEN_TIMEOUT")
    need(p.returncode==0 and p.stdout.strip(),"ISOLATED_OWNER_TOKEN_NOT_AVAILABLE")
    token=p.stdout.decode("utf-8").strip()
    need(40<len(token)<8192 and "\n" not in token,"TOKEN_FORMAT_REJECTED")
    opener=request.build_opener(request.ProxyHandler({}),
        request.HTTPSHandler(context=ssl.create_default_context()))
    req=request.Request(URL,headers={"Authorization":"Bearer "+token,
                       "Accept":"application/json",
                       "User-Agent":"OLDX-H2X-one-new-revision-readiness-readonly/1"},
                       method="GET")
    try:
        with opener.open(req,timeout=35) as r:
            need(r.status==200,"SERVICE_GET_HTTP_NOT_200")
            raw=r.read(262145)
            need(len(raw)<=262144,"SERVICE_GET_TOO_LARGE")
    except error.HTTPError as e:
        status=e.code
        e.close()
        raise Stop("EXACT_SERVICE_GET_HTTP_"+str(status))
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("EXACT_SERVICE_GET_NETWORK_STOP")
    service=json.loads(raw)
    need(isinstance(service,dict),"INVALID_SERVICE_JSON")
    need(service.get("name")==SERVICE and service.get("uid")==UID,
         "SERVICE_UID_OR_NAME_DRIFT")
    ingress=service.get("ingress","ABSENT")
    raw=service.get("invokerIamDisabled","ABSENT")
    print("H2Y_OBSERVED_INGRESS="+str(ingress))
    print("H2Y_INVOKER_IAM_DISABLED_JSON="+("ABSENT_DEFAULT_FALSE" if raw=="ABSENT" else "TRUE" if raw is True else "FALSE" if raw is False else "UNEXPECTED"))
    need(ingress=="INGRESS_TRAFFIC_INTERNAL_ONLY","INGRESS_ACTUAL_DRIFT")
    need(service.get("invokerIamDisabled",False) is False,"IAM_INVOKER_ACTUAL_DRIFT")
    template=service.get("template") or {}
    container=(template.get("containers") or [{}])[0]
    need(template.get("serviceAccount")==SA and
         container.get("image")==IMAGE,"RUNTIME_IDENTITY_OR_IMAGE_DRIFT")
    need(("OLDX_H2U_MODE","OFF") in
         {(e.get("name"),e.get("value")) for e in container.get("env",[])},
         "GATEWAY_DEFAULT_OFF_DRIFT")
    gen=str(service.get("generation") or "")
    observed=str(service.get("observedGeneration") or "")
    latest=str(service.get("latestReadyRevision") or "")
    created=str(service.get("latestCreatedRevision") or "")
    term=(service.get("terminalCondition") or {}).get("state","UNKNOWN")
    recon=service.get("reconciling","UNKNOWN")
    statuses=service.get("trafficStatuses") or []
    percentages=[v.get("percent",0) for v in statuses if isinstance(v,dict)]
    ready=(gen.isdigit() and observed==gen and bool(latest) and
           latest==created and recon is False and term=="CONDITION_SUCCEEDED" and
           bool(statuses) and all(isinstance(v,int) for v in percentages) and
           sum(percentages)==100)
    print("H2Y_SERVICE_UID="+UID)
    print("H2Y_GENERATION="+gen)
    print("H2Y_OBSERVED_GENERATION="+observed)
    print("H2Y_LATEST_CREATED_REVISION="+created)
    print("H2Y_LATEST_READY_REVISION="+latest)
    print("H2Y_TERMINAL_CONDITION="+str(term))
    print("H2Y_RECONCILING="+str(recon).upper())
    print("H2Y_TRAFFIC_TOTAL_PERCENT="+str(sum(v for v in percentages if isinstance(v,int))))
    print("H2Y_NEW_HOSTED_REVISION_READY="+("VERIFIED" if ready else "NOT_VERIFIED"))
    print("H2Y_CLOUD_READ=ONE_EXACT_SERVICE_GET")
    print("H2Y_DIRECT_IAM=H2W_PREVIOUS_PASS_NOT_REPEATED")
    print("H2Y_INHERITED_IAM=NOT_AUDITED")
    print("H2Y_HOSTED_HTTP=NOT_TESTED")
    print("H2Y_CLOUD_WRITES=NONE")
    print("H2Y_BUILD_PUSH_DEPLOY=NONE")
    print("H2Y_H2_PRODUCTION=NO_GO")
    print("H2Y_RESULT="+("READ_ONLY_NEW_REVISION_READY_PASS_WITH_LIMITS"
                       if ready else "STOP_NEW_REVISION_READY_NOT_VERIFIED"))
    return 0 if ready else 2

if __name__=="__main__":
    try:
        sys.exit(main())
    except (Stop,ValueError,TypeError,KeyError,OSError) as e:
        print("H2Y_RESULT=STOP_BEFORE_OR_DURING_READ_ONLY_GET")
        print("H2Y_REASON="+(str(e) if isinstance(e,Stop) else type(e).__name__))
        print("H2Y_CLOUD_WRITES=NONE")
        print("H2Y_H2_PRODUCTION=NO_GO")
        sys.exit(2)
