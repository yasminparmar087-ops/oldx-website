#!/usr/bin/env python3
"""OLDX H2E: exact two Service Usage GETs for observed KMS/Auth API 403.

Owner WSL isolated gcloud; strictly read-only and once. The previous H2R/H2P
checks are consumed and MUST NOT run again. Does not list services, read KMS
keys, Auth config/users, service accounts, IAM policies or Firebase data.
A 403/404/timeout is UNKNOWN, NEVER absence or a reason to grant roles.
"""
from datetime import datetime,timezone
from pathlib import Path
from urllib import request,error
import json
import os
import platform
import re
import ssl
import subprocess
import sys

OWNER="yasminparmar087@gmail.com"
PROJECT="oldx-staging"
NUMBER="38472235077"
ROOT=Path("/root")
SDK=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI=SDK/"bin/gcloud"
PY=SDK/"platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2P=ROOT/".oldx-step05-h2-two-permission-readonly-once-20261126"
MARKER=ROOT/".oldx-step05-h2-exact-api-enablement-get-once-20261126"
BASE=f"https://serviceusage.googleapis.com/v1/projects/{NUMBER}/services/"
APIS=("cloudkms.googleapis.com","identitytoolkit.googleapis.com")
ALLOWED={BASE+name for name in APIS}
class Stop(Exception):pass
def must(ok,reason):
    if not ok:raise Stop(reason)
def run_cli(env,args):
    try:
        res=subprocess.run([str(CLI)]+args,env=env,
             stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,timeout=25,check=False)
    except subprocess.TimeoutExpired:
        raise Stop("LOCAL_GCLOUD_TIMEOUT") from None
    must(res.returncode==0,"LOCAL_GCLOUD_FAILED")
    return res.stdout.decode("utf-8","replace").strip()
def verify_owner():
    must(sys.argv[1:]==["--h2-two-api-states-readonly-once"],
         "EXACT_FLAG_REQUIRED")
    must(platform.system()=="Linux" and os.geteuid()==0
         and "microsoft" in platform.release().lower(),
         "OWNER_ROOT_WSL_REQUIRED")
    must(not MARKER.exists() and not MARKER.is_symlink(),
         "H2E_ONESHOT_ALREADY_CONSUMED")
    must(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,
         "NATIVE_SDK_UNVERIFIED")
    must(CLI.is_file() and not CLI.is_symlink() and
         CLI.stat().st_uid==0 and os.access(CLI,os.X_OK),
         "NATIVE_GCLOUD_UNVERIFIED")
    bundled=PY.resolve(strict=True)
    must(bundled.is_relative_to(SDK.resolve(strict=True)) and
         bundled.is_file() and bundled.stat().st_uid==0
         and os.access(bundled,os.X_OK),"NATIVE_PYTHON_UNVERIFIED")
    must(CONFIG.is_dir() and not CONFIG.is_symlink()
         and CONFIG.stat().st_uid==0,"ISOLATED_CONFIG_UNVERIFIED")
    must(H2P.is_file() and not H2P.is_symlink()
         and H2P.stat().st_uid==0,"PRIOR_H2P_EVIDENCE_NOT_TRUSTED")
    old=H2P.read_text(encoding="utf-8").splitlines()
    must("ATTEMPT_CONSUMED=TRUE" in old and
         "RESULT=LOCAL_EVIDENCE_AND_TWO_PERMISSION_HINTS_WITH_LIMITS" in old,
         "PRIOR_H2P_SUCCESS_NOT_CONFIRMED")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),
       "PATH":str(SDK/"bin")+":/usr/bin:/bin",
       "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
       "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
       "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
       "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    must(run_cli(env,["auth","list","--filter=status:ACTIVE",
         "--format=value(account)"])==OWNER,"OWNER_PRINCIPAL_MISMATCH")
    must(run_cli(env,["config","get-value","project"])==PROJECT,
         "ISOLATED_PROJECT_MISMATCH")
    token=run_cli(env,["--quiet","--account="+OWNER,"auth","print-access-token"])
    must(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)),
         "OWNER_OAUTH_TOKEN_MISSING")
    return token

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect())
def get_state(url,token):
    must(url in ALLOWED,"URL_OUTSIDE_TWO_SERVICES")
    req=request.Request(url,method="GET",headers={
       "Authorization":"Bearer "+token,
       "Accept":"application/json",
       "User-Agent":"OLDX-H2E-exact-api-states-readonly/1"})
    try:
        with OPENER.open(req,timeout=30) as response:
            data=response.read(65537)
            must(response.status==200 and len(data)<=65536,
                 "UNEXPECTED_SERVICE_USAGE_RESPONSE")
            doc=json.loads(data)
            must(isinstance(doc,dict),"SERVICE_USAGE_NOT_OBJECT")
            expected=url.removeprefix("https://serviceusage.googleapis.com/v1/")
            must(doc.get("name")==expected,"SERVICE_USAGE_NAME_MISMATCH")
            state=doc.get("state")
            must(state in ("ENABLED","DISABLED"),
                 "SERVICE_USAGE_UNKNOWN_STATE")
            return "API_"+state
    except error.HTTPError as exc:
        code=exc.code
        exc.close()
        return "UNKNOWN_HTTP_"+str(code)
    except (error.URLError,TimeoutError,ssl.SSLError):
        return "UNKNOWN_NETWORK_OR_TIMEOUT"
def main():
    os.umask(0o077)
    try:
        token=verify_owner()
    except (Stop,OSError,UnicodeError,ValueError,TypeError) as exc:
        print("OLDX_H2E_RESULT=STOP_BEFORE_REQUEST")
        print("OLDX_H2E_REASON="+(str(exc) if isinstance(exc,Stop)
               else type(exc).__name__))
        print("OLDX_H2E_CLOUD_RESOURCE_WRITES=NONE")
        return 2
    outdir=ROOT/("oldx-h2-api-states-"+datetime.now(timezone.utc)
         .strftime("%Y%m%dT%H%M%SZ"))
    try:
        outdir.mkdir(mode=0o700)
        fd=os.open(MARKER,os.O_WRONLY|os.O_CREAT|os.O_EXCL
                   |getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            f.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE="+str(outdir)+"\n")
    except OSError:
        print("OLDX_H2E_RESULT=STOP_MARKER")
        return 2
    result={}
    state="STOP_AFTER_MARKER"
    reason="UNKNOWN"
    try:
        for name in APIS:
            result[name]=get_state(BASE+name,token)
        state="EXACT_TWO_API_STATES_READ_WITH_LIMITS"
        reason="SERVICE_USAGE_METADATA_ONLY_NOT_H2_AUTHORITY"
    except (Stop,OSError,UnicodeError,ValueError,TypeError) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        try:
            (outdir/"sanitized-api-states.json").write_text(json.dumps({
                "project":PROJECT,"api_states":result,
                "kms_direct_resource_403_from_previous":"UNRESOLVED",
                "auth_config_403_from_previous":"UNRESOLVED",
                "h2":"NO_GO","production":"NO_GO",
                "resource_writes":False},indent=2,sort_keys=True)+"\n")
            with MARKER.open("a",encoding="utf-8") as f:
                f.write("RESULT="+state+"\nREASON="+reason+"\n")
        except OSError:
            state="STOP_EVIDENCE_WRITE"
        print("OLDX_H2E_RESULT="+state)
        print("OLDX_H2E_REASON="+reason)
        print("OLDX_H2E_KMS_API="+result.get(APIS[0],"UNKNOWN_NOT_CHECKED"))
        print("OLDX_H2E_AUTH_API="+result.get(APIS[1],"UNKNOWN_NOT_CHECKED"))
        print("OLDX_H2E_H2_ENABLED=NOT_ATTEMPTED")
        print("OLDX_H2E_CLOUD_RESOURCE_WRITES=NONE")
        print("OLDX_H2E_NO_IAM_KMS_FIREBASE_CHANGES=TRUE")
        print("OLDX_H2E_DO_NOT_REPEAT=TRUE")
    return 0 if state=="EXACT_TWO_API_STATES_READ_WITH_LIMITS" else 2
if __name__=="__main__":
    sys.exit(main())
