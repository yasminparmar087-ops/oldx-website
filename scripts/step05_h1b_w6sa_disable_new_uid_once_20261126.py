#!/usr/bin/env python3
"""OLDX Step05 W6SA: safely disable ONLY the new test SA, no deletion.

Requires actual successful four-probe W3W6 marker and confirmed prior
service cleanup. Checks fresh service 404 + exact SA numeric UID/email,
permissions to disable AND re-enable; one POST disable, readback. No old
resources, keys, broad IAM binding, registry, service or SA deletion.
Follow Google's recommended >=24h observation before any later SA deletion.
No repeat after attempt marker consumed, including ambiguous network failure.
"""
from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error
import json
import os
import platform
import re
import ssl
import subprocess
import sys

OWNER="yasminparmar087@gmail.com"
PROJECT="oldx-staging"
REGION="asia-south1"
EMAIL="oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com"
UID="115445220422157278526"
RUN_UID="83d724b3-fcf0-4607-8107-f111a2eacc31"
ROOT=Path("/root")
SDK=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
GCLOUD=SDK/"bin/gcloud"
PY=SDK/"platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
W1=ROOT/".oldx-h1b-w1-new-no-key-sa-create-once-20261126"
W3W6=ROOT/".oldx-h1b-w3w6-private-off-once-20261126"
MARKER=ROOT/".oldx-h1b-w6sa-exact-new-sa-disable-once-20261126"
SERVICE=f"https://run.googleapis.com/v2/projects/{PROJECT}/locations/{REGION}/services/oldx-c2-website-mediator"
SA=f"https://iam.googleapis.com/v1/projects/{PROJECT}/serviceAccounts/{UID}"
IAMTEST=SA+":testIamPermissions"
DISABLE=SA+":disable"

class Stop(Exception):pass
def must(ok,reason):
    if not ok:raise Stop(reason)
def lines(p):
    must(p.is_file() and not p.is_symlink() and p.stat().st_uid==0,
         "PRIOR_MARKER_NOT_TRUSTED")
    return p.read_text(encoding="utf-8").splitlines()
def run_gcloud(env,args):
    try:
        r=subprocess.run([str(GCLOUD)]+args,env=env,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25,check=False)
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_GCLOUD_TIMEOUT") from None
    must(r.returncode==0,"ISOLATED_GCLOUD_FAILED")
    return r.stdout.decode("utf-8","replace").strip()

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())

def api(method,url,token,payload=None):
    must((method=="GET" and url in (SERVICE,SA)) or
         (method=="POST" and url in (IAMTEST,DISABLE)),
         "API_TARGET_OR_METHOD_OUTSIDE_SCOPE")
    headers={"Authorization":"Bearer "+token,"Accept":"application/json",
             "User-Agent":"OLDX-H1B-W6SA-disable-new-only/1"}
    data=None
    if method=="POST":
        data=(json.dumps(payload,sort_keys=True,separators=(",",":")).encode("utf-8")
              if payload is not None else b"")
        headers["Content-Type"]="application/json"
    try:
        with OPENER.open(request.Request(url,data=data,method=method,headers=headers),
                         timeout=35) as resp:
            raw=resp.read(262145)
            must(len(raw)<=262144,"API_PAYLOAD_TOO_LARGE")
            parsed=json.loads(raw) if raw else {}
            must(isinstance(parsed,dict),"API_RESPONSE_SCHEMA")
            return resp.status,parsed
    except error.HTTPError as exc:
        st=exc.code
        exc.close()
        return st,{}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("CLOUD_API_NETWORK_OR_TIMEOUT_NO_RETRY") from None

def preflight():
    must(sys.argv[1:]==["--w6sa-disable-exact-new-sa-once"],
         "EXACT_ARGUMENT_REQUIRED")
    must(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"OWNER_ROOT_WSL_REQUIRED")
    must(not MARKER.exists() and not MARKER.is_symlink(),
         "W6SA_ONESHOT_MARKER_ALREADY_CONSUMED")
    must(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,
         "NATIVE_SDK_MISMATCH")
    must(GCLOUD.is_file() and not GCLOUD.is_symlink() and
         GCLOUD.stat().st_uid==0 and os.access(GCLOUD,os.X_OK),
         "NATIVE_GCLOUD_MISMATCH")
    py=PY.resolve(strict=True)
    must(py.is_relative_to(SDK.resolve(strict=True)) and py.is_file() and
         py.stat().st_uid==0 and os.access(py,os.X_OK),
         "NATIVE_PYTHON_MISMATCH")
    must(CONFIG.is_dir() and not CONFIG.is_symlink() and CONFIG.stat().st_uid==0,
         "ISOLATED_CLOUDSDK_CONFIG_MISSING")

    w1=lines(W1)
    must("SA_UID="+UID in w1 and
         "RESULT=NEW_NO_KEY_SA_CREATED_RIGHTS_PASS_WITH_LIMITS" in w1,
         "W1_EXACT_NEW_SA_RECEIPT_MISMATCH")
    w3=lines(W3W6)
    must("SERVICE_UID="+RUN_UID in w3 and
         "SERVICE_CLEANUP=NEW_ONLY_RUN_SERVICE_DELETED_CONFIRMED" in w3 and
         "RESULT=PRIVATE_OFF_FOUR_PROBES_PASS_CLEANUP_PENDING" in w3 and
         "REASON=EXPECTED_403_200_503_404" in w3,
         "W3W6_FOUR_PROBES_AND_SERVICE_DELETE_RECEIPT_MISMATCH")

    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":str(SDK/"bin")+":/usr/bin:/bin",
         "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
         "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
         "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
         "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    must(run_gcloud(env,["auth","list","--filter=status:ACTIVE",
          "--format=value(account)"])==OWNER,"GOOGLE_ACTIVE_OWNER_MISMATCH")
    must(run_gcloud(env,["config","get-value","project"])==PROJECT,
         "ISOLATED_PROJECT_MISMATCH")
    token=run_gcloud(env,["--quiet","--account="+OWNER,"auth","print-access-token"])
    must(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)),
         "ISOLATED_OWNER_TOKEN_UNAVAILABLE")

    st,_=api("GET",SERVICE,token)
    must(st==404,"NEW_RUN_SERVICE_NOT_CONFIRMED_ABSENT_HTTP_"+str(st))
    st,sa=api("GET",SA,token)
    must(st==200 and sa.get("email")==EMAIL and
         str(sa.get("uniqueId"))==UID and sa.get("disabled") is not True,
         "EXACT_NEW_SA_UID_EMAIL_STATUS_MISMATCH")
    st,p=api("POST",IAMTEST,token,
         {"permissions":["iam.serviceAccounts.disable",
                         "iam.serviceAccounts.enable"]})
    must(st==200 and
         {"iam.serviceAccounts.disable","iam.serviceAccounts.enable"}.issubset(
             set(p.get("permissions",[]))),
         "SA_DISABLE_AND_ROLLBACK_RIGHTS_UNCONFIRMED")
    # No claim that this inventory covers resources outside this exact trial.
    return token

def main():
    os.umask(0o077)
    try:
        token=preflight()
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as exc:
        print("H1B_W6SA_RESULT=STOP_BEFORE_DISABLE")
        print("H1B_W6SA_REASON="+(str(exc) if isinstance(exc,Stop)
              else type(exc).__name__))
        print("H1B_W6SA_SA_DISABLE_ATTEMPTED=FALSE")
        return 2
    evidence=ROOT/("oldx-h1b-w6sa-disable-"+datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        fd=os.open(MARKER,os.O_CREAT|os.O_EXCL|os.O_WRONLY|
                   getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            f.write("ATTEMPT_CONSUMED=TRUE\nSA_UID="+UID+
              "\nPRIOR_RUN_UID="+RUN_UID+"\nEVIDENCE="+str(evidence)+"\n")
    except OSError:
        print("H1B_W6SA_RESULT=STOP_MARKER_CREATE")
        return 2

    outcome="STOP_AFTER_MARKER"
    reason="UNKNOWN"
    attempted=False
    disabled_at=""
    try:
        attempted=True
        print("H1B_W6SA_STAGE=ONE_EXACT_NEW_SA_REVERSIBLE_DISABLE",flush=True)
        st,_=api("POST",DISABLE,token)
        must(st==200,"EXACT_NEW_SA_DISABLE_HTTP_"+str(st))
        st,sa=api("GET",SA,token)
        must(st==200 and sa.get("email")==EMAIL and
             str(sa.get("uniqueId"))==UID and sa.get("disabled") is True,
             "DISABLE_READBACK_MISMATCH")
        disabled_at=datetime.now(timezone.utc).isoformat()
        (evidence/"sanitized-disabled-new-sa.json").write_text(json.dumps({
            "project":PROJECT,"service_account":EMAIL,"exact_uid":UID,
            "disabled_at_utc":disabled_at,"new_run_service":"ABSENT_404",
            "previous_run_service_uid":RUN_UID,
            "observed_disabled":True,
            "service_account_deleted":False,
            "registry_image_deleted":False,
            "next":"OBSERVE_AT_LEAST_24H_THEN_SEPARATE_GUARDED_SA_DELETE_DECISION",
            "dependency_scope":"EXACT_NEW_H1B_RUN_ONLY_NOT_GLOBAL_USAGE_INVENTORY"
        },indent=2,sort_keys=True)+"\n",encoding="utf-8")
        outcome="PASS_EXACT_NEW_SA_DISABLED_UID_VERIFIED_24H_HOLD"
        reason="EXACT_UID_DISABLED_READBACK_CONFIRMED"
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        try:
            with MARKER.open("a",encoding="utf-8") as f:
                f.write("RESULT="+outcome+"\nREASON="+reason+
                        "\nDISABLED_AT_UTC="+disabled_at+"\n")
        except OSError:
            outcome="STOP_EVIDENCE_WRITE_MANUAL_REVIEW"
        print("H1B_W6SA_SA_UID="+UID)
        print("H1B_W6SA_RUN_SERVICE=ABSENT_404_AT_PREFLIGHT")
        print("H1B_W6SA_SA_DISABLE_ATTEMPTED="+str(attempted).upper())
        print("H1B_W6SA_RESULT="+outcome)
        print("H1B_W6SA_REASON="+reason)
        print("H1B_W6SA_DISABLED_AT_UTC="+disabled_at)
        print("H1B_W6SA_SA_DELETED=FALSE")
        print("H1B_W6SA_CLOUD_RUN_AND_REGISTRY_WRITES=NONE")
        print("H1B_W6SA_DO_NOT_REPEAT=TRUE")
    return 0 if outcome=="PASS_EXACT_NEW_SA_DISABLED_UID_VERIFIED_24H_HOLD" else 2

if __name__=="__main__":
    sys.exit(main())
