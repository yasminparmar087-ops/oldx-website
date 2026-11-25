#!/usr/bin/env python3
"""OLDX C1A v2 reconciling diagnostic: one read-only GET, no deletion.

Only after actual C1A service-delete STOP with WRITE_ATTEMPTED=False.
This script does NOT restart the consumed deletion attempt.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import re
import shutil
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from urllib import request, error

OWNER = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
REGION = "asia-south1"
SERVICE = "oldx-step05-gateway"
FULL = f"projects/{PROJECT}/locations/{REGION}/services/{SERVICE}"
UID = "bf441d37-e39b-4afd-b4c8-0e6edee7269b"
REV = "oldx-step05-gateway-00001-thd"
SA = "oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com"
IMAGE = ("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
         "oldx-step05-gateway-off@sha256:"
         "612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a")
PREV = ".oldx-step05-c1a-conditional-service-delete-once-20261126"
MARK = ".oldx-step05-c1a-v2-reconciling-readonly-once-20261126"
MAX_BYTES = 256 * 1024

class Stop(Exception): pass
def require(condition, code):
    if not condition: raise Stop(code)

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def classify(v):
    """Only nonsensitive, narrow status fields. Missing is NOT mapped to false."""
    require(isinstance(v,dict), "SERVICE_RESPONSE_NOT_OBJECT")
    require(v.get("name")==FULL and v.get("uid")==UID, "LIVE_SERVICE_NAME_OR_UID_CHANGED")
    rv=v.get("reconciling","__MISSING__")
    reconcile=("ABSENT" if rv=="__MISSING__" else
               "EXPLICIT_FALSE" if rv is False else
               "EXPLICIT_TRUE" if rv is True else "INVALID_OR_NULL")
    gen=v.get("generation")
    observed=v.get("observedGeneration")
    generations="MATCH" if gen is not None and observed is not None and str(gen)==str(observed) else "UNKNOWN_OR_MISMATCH"
    condition=v.get("terminalCondition")
    state=condition.get("state") if isinstance(condition,dict) else None
    state=state if isinstance(state,str) and re.fullmatch(r"[A-Z_]{3,60}",state) else "UNKNOWN"
    revision_status="MATCH" if (str(v.get("latestReadyRevision","")).rsplit("/",1)[-1]==REV and
                                str(v.get("latestCreatedRevision","")).rsplit("/",1)[-1]==REV) else "MISMATCH"
    template=v.get("template")
    template=template if isinstance(template,dict) else {}
    containers=template.get("containers")
    image=(containers[0].get("image") if isinstance(containers,list) and len(containers)==1
           and isinstance(containers[0],dict) else None)
    details={
        "reconciling":reconcile,
        "generation":generations,
        "terminal_condition":state,
        "revision_pair":revision_status,
        "service_account":"MATCH" if template.get("serviceAccount")==SA else "MISMATCH_OR_UNKNOWN",
        "image":"MATCH" if image==IMAGE else "MISMATCH_OR_UNKNOWN",
        "etag":"PRESENT" if isinstance(v.get("etag"),str) and bool(v["etag"]) else "ABSENT",
        "traffic":"PRESENT" if isinstance(v.get("traffic"),list) else "ABSENT",
        "traffic_statuses":"PRESENT" if isinstance(v.get("trafficStatuses"),list) else "ABSENT",
        "reconciling_root_cause":
          "MISSING_FIELD_CAUSED_STRICT_FALSE_GUARD" if reconcile=="ABSENT" else
          "TRUE_RECONCILING" if reconcile=="EXPLICIT_TRUE" else
          "UNKNOWN_FIELD_TYPE" if reconcile=="INVALID_OR_NULL" else
          "GUARD_RESULT_INCONSISTENT_REVIEW"
    }
    return details

def main():
    os.umask(0o077)
    if sys.argv[1:] != ["--inspect-existing-v2-once"]:
        print("C1A_DIAG_RESULT=STOP_FLAG_REQUIRED")
        return 2
    home=Path.home()
    try:
        require(platform.system()=="Linux" and "microsoft" not in platform.release().lower()
                and os.geteuid()!=0 and home.is_dir() and not home.is_symlink(),
                "OWNER_CLOUD_SHELL_NONROOT_REQUIRED")
        prev=home/PREV
        require(prev.is_file() and not prev.is_symlink() and prev.stat().st_uid==os.geteuid(),
                "PREVIOUS_DELETE_MARKER_UNVERIFIED")
        lines=prev.read_text(encoding="utf-8").splitlines()
        require({"ATTEMPT_CONSUMED","RESULT=STOP","REASON=C1A_RECONCILING_OR_UNKNOWN",
                 "WRITE_ATTEMPTED=False"}.issubset(set(lines)),
                "PREVIOUS_DELETE_STOP_NOT_EXACTLY_VERIFIED")
        marker=home/MARK
        require(not marker.exists() and not marker.is_symlink(),"DIAGNOSTIC_ALREADY_CONSUMED")
        cli=shutil.which("gcloud")
        require(cli and Path(cli).is_file() and not cli.startswith("/mnt/"),
                "GCLOUD_NOT_FOUND")
        output=home/("oldx-c1a-v2-reconciling-diagnostic-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
        require(not output.exists() and not output.is_symlink(),"EVIDENCE_COLLISION")
    except (Stop,OSError) as e:
        print("C1A_DIAG_RESULT=STOP_PREFLIGHT")
        print("C1A_DIAG_REASON="+(str(e) if isinstance(e,Stop) else type(e).__name__))
        return 2

    output.mkdir(mode=0o700)
    fd=os.open(marker,os.O_CREAT|os.O_EXCL|os.O_WRONLY|getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        f.write("READ_ONLY_DIAG_ATTEMPT_CONSUMED\n")
    result,reason,details="STOP","UNDETERMINED",{}
    try:
        cmd=[cli,"--quiet","--account="+OWNER,"auth","print-access-token"]
        token_result=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True,timeout=20)
        require(token_result.returncode==0,"OWNER_TOKEN_READ_FAILED")
        token=token_result.stdout.decode("ascii","strict").strip()
        require(bool(re.fullmatch(r"[A-Za-z0-9._~-]{40,4096}",token)),"OWNER_TOKEN_INVALID")
        url="https://run.googleapis.com/v2/"+FULL
        req=request.Request(url,method="GET",headers={"Authorization":"Bearer "+token,
                             "Accept":"application/json","User-Agent":"OLDX-C1A-v2-readonly/1"})
        opener=request.build_opener(request.ProxyHandler({}),
                 request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())
        try:
            with opener.open(req,timeout=20) as resp:
                require(resp.status==200,"SERVICE_GET_HTTP_NOT_200")
                raw=resp.read(MAX_BYTES+1)
        except error.HTTPError as e:
            raise Stop("SERVICE_GET_HTTP_"+str(e.code))
        except (error.URLError,TimeoutError) as e:
            raise Stop("SERVICE_GET_NETWORK_"+type(e).__name__)
        require(0<len(raw)<=MAX_BYTES,"SERVICE_GET_INVALID_LENGTH")
        details=classify(json.loads(raw))
        result,reason="READ_ONLY_DIAG_COMPLETE","EXACT_SERVICE_UID_MATCH"
    except (Stop,OSError,UnicodeError,ValueError,TypeError,subprocess.TimeoutExpired) as e:
        reason=str(e) if isinstance(e,Stop) else type(e).__name__
    finally:
        with marker.open("a",encoding="utf-8") as f:
            f.write("RESULT="+result+"\nREASON="+reason+"\n")
        (output/"sanitized-diagnostic.json").write_text(
            json.dumps({"result":result,"reason":reason,"details":details,
                        "cloud_writes":False,"deleted":False},
                       sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("C1A_DIAG_RESULT="+result)
    print("C1A_DIAG_REASON="+reason)
    for key,value in details.items():
        print("C1A_V2_"+key.upper()+"="+value)
    print("C1A_DIAG_CLOUD_WRITES=NONE")
    print("C1A_RESOURCE_DELETED=NO")
    return 0 if result=="READ_ONLY_DIAG_COMPLETE" else 2

if __name__=="__main__":
    sys.exit(main())
