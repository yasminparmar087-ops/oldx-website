#!/usr/bin/env python3
"""OLDX Step05: read SAVED H2 inventory, test 2 NEW permission names ONCE.

Source-only preparation. Owner WSL executes with isolated native gcloud.
Exactly ONE resource-manager testIamPermissions POST (a read-only permission
query, NOT IAM update) after checking prior consumed metadata receipt.
Never repeats H2 GET inventory or touches H1B service account.
"""
import json
import os
import platform
import re
import ssl
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone
from urllib import request, error

ROOT=Path("/root")
PROJECT="oldx-staging"
OWNER="yasminparmar087@gmail.com"
SDK=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
GCLOUD=SDK/"bin/gcloud"
PY=SDK/"platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
PREVIOUS=ROOT/".oldx-step05-h2-provider-readonly-inventory-once-20261126"
MARKER=ROOT/".oldx-step05-h2-two-permission-readonly-once-20261126"
URL="https://cloudresourcemanager.googleapis.com/v1/projects/oldx-staging:testIamPermissions"
NEEDED=("cloudkms.keyRings.list","firebaseauth.configs.get")
class Stop(Exception):pass
def must(cond,label):
    if not cond: raise Stop(label)
def cli(args,env):
    try:
        r=subprocess.run([str(GCLOUD)]+args,env=env,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25,check=False)
    except subprocess.TimeoutExpired:
        raise Stop("GCLOUD_IDENTITY_TIMEOUT") from None
    must(r.returncode==0,"GCLOUD_IDENTITY_FAILED")
    return r.stdout.decode("utf-8","replace").strip()
def local_summary():
    must(PREVIOUS.is_file() and not PREVIOUS.is_symlink() and
         PREVIOUS.stat().st_uid==0,"OLD_METADATA_RECEIPT_NOT_TRUSTED")
    parts=PREVIOUS.read_text(encoding="utf-8").splitlines()
    must("RESULT=READ_ONLY_METADATA_WITH_LIMITS" in parts and
         "ATTEMPT_CONSUMED=TRUE" in parts,
         "OLD_METADATA_ACTUAL_PASS_MISSING")
    evidence=[s[9:] for s in parts if s.startswith("EVIDENCE=")]
    must(len(evidence)==1,"OLD_EVIDENCE_PATH_UNKNOWN")
    d=Path(evidence[0])
    must(d.parent==ROOT and
         re.fullmatch(r"oldx-h2-provider-readonly-\d{8}T\d{6}Z",d.name) is not None,
         "OLD_EVIDENCE_PATH_OUTSIDE_SCOPE")
    must(d.is_dir() and not d.is_symlink() and d.stat().st_uid==0,
         "OLD_EVIDENCE_DIR_NOT_TRUSTED")
    p=d/"sanitized-h2-metadata.json"
    must(p.is_file() and not p.is_symlink() and p.stat().st_uid==0 and
         p.stat().st_size<=65536,"OLD_JSON_NOT_TRUSTED")
    data=json.loads(p.read_text(encoding="utf-8"))
    must(isinstance(data,dict) and data.get("project")=="ACTIVE_IDENTITY_MATCH" and
         data.get("h2_status")=="NO_GO" and
         data.get("production_status")=="NO_GO","OLD_JSON_PROJECT_OR_STATUS_MISMATCH")
    summary={}
    for label in ("cloud_run","service_accounts","storage_buckets"):
        obj=data.get(label)
        must(isinstance(obj,dict),"OLD_JSON_"+label.upper()+"_SCHEMA")
        summary[label+"_list"]=obj.get("status","UNKNOWN")
        if obj.get("status")=="FIRST_PAGE_COMPLETE":
            count=obj.get("count")
            must(isinstance(count,int) and 0<=count<=100,
                 "OLD_JSON_"+label.upper()+"_COUNT")
            summary[label+"_count"]=count
    if summary["cloud_run_list"]=="FIRST_PAGE_COMPLETE":
        names=data["cloud_run"].get("h2_service_candidates",[])
        must(isinstance(names,list) and len(names)<=20 and all(
             isinstance(x,str) and re.fullmatch(r"[a-z][a-z0-9-]{0,62}",x)
             for x in names),"C2_SERVICE_NAMES_UNEXPECTED")
        summary["c2_service_candidates"]=names
    if summary["service_accounts_list"]=="FIRST_PAGE_COMPLETE":
        n=data["service_accounts"].get("c2_candidate_count")
        must(isinstance(n,int) and 0<=n<=100,"C2_SA_COUNT_UNEXPECTED")
        summary["c2_service_account_count"]=n
    must(data.get("kms_key_rings",{}).get("status")=="UNKNOWN_HTTP_403" and
         data.get("auth_config")=="UNKNOWN_HTTP_403",
         "CURRENT_TARGETED_PERMISSIONS_NOT_MATCHING_PRIOR_403")
    summary["kms_ring_list"]="UNKNOWN_HTTP_403_FROM_PRIOR_RUN"
    summary["auth_config"]="UNKNOWN_HTTP_403_FROM_PRIOR_RUN"
    summary["firestore_db"]="METADATA_VISIBLE_EXACT_FROM_PRIOR_RUN"
    return summary

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())
def scoped_project_permission_read(token):
    body=json.dumps({"permissions":list(NEEDED)},separators=(",",":")).encode()
    req=request.Request(URL,method="POST",data=body,headers={
        "Authorization":"Bearer "+token,"Content-Type":"application/json",
        "Accept":"application/json","User-Agent":"OLDX-H2-two-permission-readonly/1"})
    try:
        with OPENER.open(req,timeout=30) as r:
            raw=r.read(65537)
            must(r.status==200 and len(raw)<=65536,"PERMISSION_RESPONSE_INVALID")
            obj=json.loads(raw)
            must(isinstance(obj,dict) and isinstance(obj.get("permissions",[]),list),
                 "PERMISSION_SCHEMA_INVALID")
            got=obj.get("permissions",[])
            must(all(isinstance(x,str) and x in NEEDED for x in got),
                 "PERMISSION_UNEXPECTED_FIELD")
            return {"status":"PROJECT_TEST_200_WITH_LIMITS",
                    "kms_keyrings_list":("RETURNED_AT_PROJECT" if NEEDED[0] in got
                                         else "NOT_RETURNED_AT_PROJECT"),
                    "firebaseauth_configs_get":("RETURNED_AT_PROJECT" if NEEDED[1] in got
                                                else "NOT_RETURNED_AT_PROJECT")}
    except error.HTTPError as e:
        code=e.code;e.close()
        return {"status":"UNKNOWN_HTTP_"+str(code),
                "kms_keyrings_list":"UNKNOWN",
                "firebaseauth_configs_get":"UNKNOWN"}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("PERMISSION_CHECK_NETWORK_OR_TIMEOUT") from None

def preflight():
    must(sys.argv[1:]==["--saved-h2-and-two-permissions-once"],"EXACT_FLAG_REQUIRED")
    must(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"ROOT_OWNER_WSL_REQUIRED")
    must(not MARKER.exists() and not MARKER.is_symlink(),"ONESHOT_CONSUMED")
    must(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,
         "NATIVE_SDK_NOT_VERIFIED")
    must(GCLOUD.is_file() and not GCLOUD.is_symlink() and os.access(GCLOUD,os.X_OK),
         "NATIVE_CLI_NOT_VERIFIED")
    py=PY.resolve(strict=True)
    must(py.is_relative_to(SDK.resolve(strict=True)) and py.is_file() and
         os.access(py,os.X_OK) and py.stat().st_uid==0,"NATIVE_PYTHON_NOT_VERIFIED")
    must(CONFIG.is_dir() and not CONFIG.is_symlink() and CONFIG.stat().st_uid==0,
         "ISOLATED_GCLOUD_CONFIG_NOT_VERIFIED")
    summary=local_summary()
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":str(SDK/"bin")+":/usr/bin:/bin",
        "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    must(cli(["auth","list","--filter=status:ACTIVE","--format=value(account)"],env)==OWNER,
         "WRONG_OWNER")
    must(cli(["config","get-value","project"],env)==PROJECT,"WRONG_PROJECT")
    token=cli(["--quiet","--account="+OWNER,"auth","print-access-token"],env)
    must(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)),
         "NO_OWNER_TOKEN")
    return summary,token

def main():
    os.umask(0o077)
    try: summary,token=preflight()
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as ex:
        print("OLDX_H2P_RESULT=STOP_LOCAL_PREFLIGHT")
        print("OLDX_H2P_REASON="+(str(ex) if isinstance(ex,Stop) else type(ex).__name__))
        print("OLDX_H2P_CLOUD_RESOURCE_WRITES=NONE")
        return 2
    outdir=ROOT/("oldx-h2-two-permission-readonly-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        outdir.mkdir(mode=0o700)
        fd=os.open(MARKER,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"w") as f:
            f.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE="+str(outdir)+"\n")
    except OSError:
        print("OLDX_H2P_RESULT=STOP_MARKER_COLLISION")
        return 2
    state="STOP_AFTER_MARKER";reason="UNKNOWN";permission={"status":"NOT_COMPLETED"}
    try:
        permission=scoped_project_permission_read(token)
        state="LOCAL_EVIDENCE_AND_TWO_PERMISSION_HINTS_WITH_LIMITS"
        reason="NO_RESOURCE_OR_IAM_CHANGE"
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as ex:
        reason=str(ex) if isinstance(ex,Stop) else type(ex).__name__
    finally:
        try:
            (outdir/"sanitized-two-permissions-and-existing-inventory.json").write_text(
              json.dumps({"previous_inventory":summary,"scoped_project_permissions":permission,
                         "h2":"NO_GO","production":"NO_GO","cloud_resource_writes":False},
                         indent=2,sort_keys=True)+"\n",encoding="utf-8")
            with MARKER.open("a") as f:f.write("RESULT="+state+"\nREASON="+reason+"\n")
        except OSError:
            state="STOP_EVIDENCE_IO"
        print("OLDX_H2P_RESULT="+state)
        print("OLDX_H2P_REASON="+reason)
        for key in sorted(summary):
            value=summary[key]
            if isinstance(value,list): value=",".join(value) if value else "NONE"
            print("OLDX_H2P_"+key.upper()+"="+str(value))
        print("OLDX_H2P_PROJECT_PERMISSION_TEST="+permission["status"])
        print("OLDX_H2P_KMS_LIST_PERMISSION="+permission.get("kms_keyrings_list","UNKNOWN"))
        print("OLDX_H2P_AUTH_CONFIG_PERMISSION="+permission.get("firebaseauth_configs_get","UNKNOWN"))
        print("OLDX_H2P_H2_ENABLED=NOT_ATTEMPTED")
        print("OLDX_H2P_CLOUD_RESOURCE_WRITES=NONE")
        print("OLDX_H2P_DO_NOT_REPEAT=TRUE")
    return 0 if state=="LOCAL_EVIDENCE_AND_TWO_PERMISSION_HINTS_WITH_LIMITS" else 2

if __name__=="__main__":sys.exit(main())
