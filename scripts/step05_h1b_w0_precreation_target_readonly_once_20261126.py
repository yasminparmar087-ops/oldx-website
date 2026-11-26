#!/usr/bin/env python3
"""OLDX Step05 H1B W0: strictly new-target pre-creation read-only gate.

Only 3 bounded Google REST GET requests: project identity, exact candidate Cloud Run
service, exact candidate service account. No broad IAM re-audit or old image check.
No Cloud resource write, deploy, IAM change, Registry upload or cleanup.
Expected owner: root in OLDX-Ubuntu-24.04, isolated native gcloud already authenticated.
A consumed one-shot marker is never reset or repeated.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import re
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from urllib import request, error

OWNER="yasminparmar087@gmail.com"
PROJECT="oldx-staging"
NUMBER="38472235077"
REGION="asia-south1"
SERVICE="oldx-c2-website-mediator"
SA="oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com"
REMOTE_DIGEST="sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e"
REMOTE_TAG="h1b-g2b-20261126-dc07d8c3bd01d5310ae1"
ROOT=Path("/root")
BASE=ROOT/"oldx-tools"
SDK=BASE/"native-gcloud-594.0.1/google-cloud-sdk"
CLI=SDK/"bin/gcloud"
PY=SDK/"platform/bundledpythonunix/bin/python3"
CONFIG=BASE/"oldx-h1b-g2-20261126-cloudsdk-config"
G2B_MARKER=ROOT/".oldx-h1b-g2b-retained-single-push-once-20261126"
W0_MARKER=ROOT/".oldx-h1b-w0-new-target-readonly-once-20261126"
SERVICE_URL=f"https://run.googleapis.com/v2/projects/{PROJECT}/locations/{REGION}/services/{SERVICE}"
SA_URL=f"https://iam.googleapis.com/v1/projects/{PROJECT}/serviceAccounts/{SA}"
PROJECT_URL=f"https://cloudresourcemanager.googleapis.com/v1/projects/{PROJECT}"
class Stop(Exception):
    pass

def require(ok,why):
    if not ok:
        raise Stop(why)

def valid_local_file(p):
    return p.is_file() and not p.is_symlink() and p.stat().st_uid==0

def env_and_identity():
    require(sys.argv[1:]==["--w0-new-target-readonly-once"],"EXACT_FLAG_REQUIRED")
    require(platform.system()=="Linux" and os.geteuid()==0 and
        "microsoft" in platform.release().lower(),"OWNER_WSL_ROOT_REQUIRED")
    require(not W0_MARKER.exists() and not W0_MARKER.is_symlink(),"W0_ONESHOT_CONSUMED")
    require(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,"SDK_DIRECTORY_UNVERIFIED")
    require(valid_local_file(CLI) and os.access(CLI,os.X_OK),"NATIVE_GCLOUD_UNVERIFIED")
    py=PY.resolve(strict=True)
    require(py.is_relative_to(SDK.resolve(strict=True)) and
        py.is_file() and os.access(py,os.X_OK) and py.stat().st_uid==0,
        "BUNDLED_PYTHON_UNVERIFIED")
    require(CONFIG.is_dir() and not CONFIG.is_symlink() and CONFIG.stat().st_uid==0,
        "ISOLATED_CONFIG_UNVERIFIED")
    require(valid_local_file(G2B_MARKER),"G2B_ONESHOT_EVIDENCE_MISSING")
    saved=G2B_MARKER.read_text(encoding="utf-8").splitlines()
    require("ATTEMPT_CONSUMED=TRUE" in saved and
        "RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED" in saved and
        "TAG="+REMOTE_TAG in saved,
        "G2B_FROZEN_REMOTE_DIGEST_CUSTODY_UNVERIFIED")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":f"{SDK}/bin:/usr/bin:/bin",
        "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    for command,expected,why in [
       ([str(CLI),"auth","list","--filter=status:ACTIVE","--format=value(account)"],OWNER,"ACTIVE_OWNER_MISMATCH"),
       ([str(CLI),"config","get-value","project"],PROJECT,"ISOLATED_PROJECT_MISMATCH")
    ]:
        try:
            result=subprocess.run(command,env=env,stdin=subprocess.DEVNULL,
              stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25,check=False)
        except subprocess.TimeoutExpired:
            raise Stop("GCLOUD_IDENTITY_TIMEOUT") from None
        require(result.returncode==0 and result.stdout.decode("utf-8","replace").strip()==expected,why)
    return env

def owner_token(env):
    try:
        result=subprocess.run([str(CLI),"--quiet","--account="+OWNER,
            "auth","print-access-token"],env=env,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25,check=False)
    except subprocess.TimeoutExpired:
        raise Stop("OWNER_TOKEN_TIMEOUT") from None
    token=result.stdout.decode("ascii","ignore").strip()
    require(result.returncode==0 and bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)),
        "OWNER_TOKEN_UNAVAILABLE")
    return token

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        return None

def cloud_get(url,token):
    require(url in (PROJECT_URL,SERVICE_URL,SA_URL),"UNEXPECTED_API_URL")
    req=request.Request(url,method="GET",headers={
        "Authorization":"Bearer "+token,"Accept":"application/json",
        "User-Agent":"OLDX-H1B-W0-new-target-readonly/1"})
    opener=request.build_opener(request.ProxyHandler({}),
        request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())
    try:
        with opener.open(req,timeout=30) as res:
            require(res.status==200,"API_NON200_SUCCESS")
            raw=res.read(262145)
            require(len(raw)<=262144,"API_RESPONSE_TOO_LARGE")
            try:
                data=json.loads(raw)
            except (ValueError,UnicodeError):
                raise Stop("API_MALFORMED_JSON") from None
            require(isinstance(data,dict),"API_MALFORMED_SCHEMA")
            return 200,data
    except error.HTTPError as exc:
        code=exc.code
        exc.close()
        return code,{}

def main():
    os.umask(0o077)
    try:
        env=env_and_identity()
        token=owner_token(env)
    except (Stop,OSError,ValueError) as exc:
        print("H1B_W0_RESULT=STOP_LOCAL_PREFLIGHT")
        print("H1B_W0_REASON="+(str(exc) if isinstance(exc,Stop) else type(exc).__name__))
        print("H1B_W0_CLOUD_RESOURCE_WRITES=NONE")
        return 2
    evidence=ROOT/("oldx-h1b-w0-new-target-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evidence.mkdir(mode=0o700)
        with W0_MARKER.open("x",encoding="utf-8") as f:
            f.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE="+str(evidence)+"\n")
        os.chmod(W0_MARKER,0o600)
    except OSError:
        print("H1B_W0_RESULT=STOP_MARKER_COLLISION")
        print("H1B_W0_CLOUD_RESOURCE_WRITES=NONE")
        return 2
    outcome="STOP_WITH_LIMITS"
    reason="UNVERIFIED"
    results={}
    try:
        st,project=cloud_get(PROJECT_URL,token)
        require(st==200,"PROJECT_GET_HTTP_"+str(st))
        require(project.get("projectId")==PROJECT and
                str(project.get("projectNumber"))==NUMBER and
                project.get("lifecycleState")=="ACTIVE","PROJECT_IDENTITY_MISMATCH")
        results["project"]="ACTIVE_EXACT"
        for label,url in (("service",SERVICE_URL),("new_sa",SA_URL)):
            status,_=cloud_get(url,token)
            require(status==404,label.upper()+"_NOT_CONFIRMED_ABSENT_HTTP_"+str(status))
            results[label]="ABSENT_404_WITH_LIMITS"
        outcome="READ_ONLY_NEW_TARGETS_ABSENT_WITH_LIMITS"
        reason="PROJECT_AND_TWO_NEW_EXACT_RESOURCES_CHECKED"
    except (Stop,OSError,ValueError,TypeError) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        try:
            (evidence/"sanitized-result.json").write_text(
                json.dumps({"result":outcome,"reason":reason,"targets":results,
                 "remote_image_digest_from_prior_G2B":REMOTE_DIGEST,
                 "cloud_resource_writes":False,
                 "new_resource_actas":"NOT_TESTABLE_UNTIL_SA_CREATION",
                 "operation_cleanup":"NOT_EXECUTED"},indent=2,sort_keys=True)+"\n")
            with W0_MARKER.open("a",encoding="utf-8") as f:
                f.write("RESULT="+outcome+"\nREASON="+reason+"\n")
        except OSError:
            outcome="STOP_EVIDENCE_IO"
        print("H1B_W0_PROJECT="+results.get("project","NOT_CONFIRMED"))
        print("H1B_W0_SERVICE="+results.get("service","NOT_CONFIRMED"))
        print("H1B_W0_NEW_SA="+results.get("new_sa","NOT_CONFIRMED"))
        print("H1B_W0_IMAGE=PRIOR_G2B_REMOTE_DIGEST_FROZEN_NO_REPEAT")
        print("H1B_W0_NEW_SA_ACTAS=NOT_YET_TESTABLE")
        print("H1B_W0_RESULT="+outcome)
        print("H1B_W0_REASON="+reason)
        print("H1B_W0_CLOUD_RESOURCE_WRITES=NONE")
        print("H1B_W0_DO_NOT_REPEAT=TRUE")
    return 0 if outcome=="READ_ONLY_NEW_TARGETS_ABSENT_WITH_LIMITS" else 2

if __name__=="__main__":
    sys.exit(main())
