#!/usr/bin/env python3
"""OLDX Step05 H2 metadata-only inventory, single bounded owner WSL execution.

No resource changes, IAM policies, signing, Firestore documents, Auth users,
Storage objects, Cloud Run invocation, build, scan, push, or rechecking the
disabled H1B SA. Outputs coarse status; private JSON holds sanitized metadata.
A 403/timeout/pagination never means a resource is absent or approved.
"""
import json
import os
import platform
import re
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error

OWNER="yasminparmar087@gmail.com"
PROJECT="oldx-staging"
NUMBER="38472235077"
REGION="asia-south1"
ROOT=Path("/root")
SDK=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
GCLOUD=SDK/"bin/gcloud"
BUNDLED=SDK/"platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
MARKER=ROOT/".oldx-step05-h2-provider-readonly-inventory-once-20261126"
PROJECT_URL=f"https://cloudresourcemanager.googleapis.com/v1/projects/{PROJECT}"
RUN_URL=f"https://run.googleapis.com/v2/projects/{PROJECT}/locations/{REGION}/services?pageSize=100"
IAM_URL=f"https://iam.googleapis.com/v1/projects/{PROJECT}/serviceAccounts?pageSize=100"
KMS_URL=f"https://cloudkms.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/keyRings?pageSize=100"
DB_URL=f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)"
AUTH_URL=f"https://identitytoolkit.googleapis.com/admin/v2/projects/{PROJECT}/config"
BUCKET_URL=f"https://storage.googleapis.com/storage/v1/b?project={PROJECT}&maxResults=100"
STATIC=(PROJECT_URL,RUN_URL,IAM_URL,KMS_URL,DB_URL,AUTH_URL,BUCKET_URL)
KMS_PREFIX=f"https://cloudkms.googleapis.com/v1/projects/{PROJECT}/locations/{REGION}/keyRings/"
class Stop(Exception):pass
def must(ok,reason):
    if not ok:raise Stop(reason)
def cli(env,args):
    try:
        p=subprocess.run([str(GCLOUD)]+args,env=env,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,check=False)
    except subprocess.TimeoutExpired:
        raise Stop("OWNER_CLI_TIMEOUT") from None
    must(p.returncode==0,"OWNER_CLI_FAILED")
    return p.stdout.decode("utf-8","replace").strip()
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())
def get(url,token):
    must(url in STATIC or (url.startswith(KMS_PREFIX) and url.endswith("/cryptoKeys?pageSize=100")
         and re.fullmatch(re.escape(KMS_PREFIX)+r"[a-zA-Z0-9_-]{1,63}/cryptoKeys[?]pageSize=100",url)),
         "URL_OUTSIDE_READONLY_ALLOWLIST")
    try:
        with OPENER.open(request.Request(url,method="GET",headers={
            "Authorization":"Bearer "+token,
            "Accept":"application/json","User-Agent":"OLDX-H2-readonly-inventory/1"}),
            timeout=35) as resp:
            must(resp.status==200,"UNEXPECTED_SUCCESS_STATUS")
            raw=resp.read(524289)
            must(len(raw)<=524288,"METADATA_RESPONSE_TOO_LARGE")
            val=json.loads(raw) if raw else {}
            must(isinstance(val,dict),"METADATA_SCHEMA_NOT_OBJECT")
            return 200,val
    except error.HTTPError as exc:
        status=exc.code;exc.close()
        return status,{}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("METADATA_NETWORK_OR_TIMEOUT") from None
def preflight():
    must(sys.argv[1:]==["--h2-provider-metadata-readonly-once"],"EXACT_FLAG_REQUIRED")
    must(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"OWNER_ROOT_WSL_REQUIRED")
    must(not MARKER.exists() and not MARKER.is_symlink(),"ONESHOT_ALREADY_CONSUMED")
    must(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,
         "NATIVE_SDK_UNVERIFIED")
    must(GCLOUD.is_file() and not GCLOUD.is_symlink() and GCLOUD.stat().st_uid==0 and
         os.access(GCLOUD,os.X_OK),"NATIVE_GCLOUD_UNVERIFIED")
    py=BUNDLED.resolve(strict=True)
    must(py.is_relative_to(SDK.resolve(strict=True)) and
         py.is_file() and py.stat().st_uid==0 and os.access(py,os.X_OK),
         "NATIVE_PYTHON_UNVERIFIED")
    must(CONFIG.is_dir() and not CONFIG.is_symlink() and CONFIG.stat().st_uid==0,
         "ISOLATED_OWNER_CONFIG_MISSING")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":str(SDK/"bin")+":/usr/bin:/bin",
         "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(BUNDLED),
         "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
         "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
         "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    must(cli(env,["auth","list","--filter=status:ACTIVE",
         "--format=value(account)"])==OWNER,"WRONG_OWNER")
    must(cli(env,["config","get-value","project"])==PROJECT,"WRONG_PROJECT")
    token=cli(env,["--quiet","--account="+OWNER,"auth","print-access-token"])
    must(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)),
         "OWNER_OAUTH_TOKEN_UNAVAILABLE")
    return token
def list_state(code,data,field):
    if code!=200:return {"status":"UNKNOWN_HTTP_"+str(code)}
    rows=data.get(field,[])
    if not isinstance(rows,list):return {"status":"UNKNOWN_SCHEMA"}
    if data.get("nextPageToken"):return {"status":"PARTIAL_PAGINATED","first_page_count":len(rows)}
    return {"status":"FIRST_PAGE_COMPLETE","count":len(rows)}
def collect(token):
    result={}
    st,project=get(PROJECT_URL,token)
    must(st==200 and project.get("projectId")==PROJECT and
         str(project.get("projectNumber"))==NUMBER and
         project.get("lifecycleState")=="ACTIVE","PROJECT_IDENTITY_NOT_VERIFIED")
    result["project"]="ACTIVE_IDENTITY_MATCH"
    st,run=get(RUN_URL,token)
    result["cloud_run"]=list_state(st,run,"services")
    if result["cloud_run"]["status"]=="FIRST_PAGE_COMPLETE":
        ss=run.get("services",[])
        result["cloud_run"]["h2_service_candidates"]=[
            s.get("name","").rsplit("/",1)[-1] for s in ss
            if isinstance(s,dict) and "oldx-c2" in s.get("name","")]
    st,iam=get(IAM_URL,token)
    result["service_accounts"]=list_state(st,iam,"accounts")
    if result["service_accounts"]["status"]=="FIRST_PAGE_COMPLETE":
        result["service_accounts"]["c2_candidate_count"]=sum(
            isinstance(sa,dict) and "c2" in sa.get("email","").lower()
            for sa in iam.get("accounts",[]))
    st,rings=get(KMS_URL,token)
    result["kms_key_rings"]=list_state(st,rings,"keyRings")
    result["kms_signing_keys"]="NOT_ESTABLISHED"
    if result["kms_key_rings"]["status"]=="FIRST_PAGE_COMPLETE":
        names=[x.get("name","") for x in rings.get("keyRings",[]) if isinstance(x,dict)]
        valid=[s for s in names if re.fullmatch(
            rf"projects/{PROJECT}/locations/{REGION}/keyRings/[A-Za-z0-9_-]{{1,63}}",s)]
        if len(valid)!=len(names):
            result["kms_signing_keys"]="UNKNOWN_RING_SCHEMA"
        elif len(valid)>3:
            result["kms_signing_keys"]="BOUNDED_INVENTORY_INCOMPLETE_MORE_THAN_3_RINGS"
        else:
            key_rows=[]
            for name in valid:
                url="https://cloudkms.googleapis.com/v1/"+name+"/cryptoKeys?pageSize=100"
                s,obj=get(url,token)
                key_state=list_state(s,obj,"cryptoKeys")
                ring_name=name.rsplit("/",1)[-1]
                row={"ring":ring_name,**key_state}
                if key_state["status"]=="FIRST_PAGE_COMPLETE":
                    row["asymmetric_sign_key_count"]=sum(
                        isinstance(k,dict) and k.get("purpose")=="ASYMMETRIC_SIGN"
                        for k in obj.get("cryptoKeys",[]))
                key_rows.append(row)
            result["kms_signing_keys"]=key_rows
    st,db=get(DB_URL,token)
    result["firestore_default_db"]={
        "status":("METADATA_VISIBLE_EXACT" if st==200 and
                  db.get("name")==f"projects/{PROJECT}/databases/(default)"
                  else "UNKNOWN_HTTP_"+str(st) if st!=200 else "UNKNOWN_IDENTITY"),
        "database_type":db.get("type","UNKNOWN") if st==200 else "UNKNOWN"}
    st,auth=get(AUTH_URL,token)
    email=(auth.get("signIn") or {}).get("email") if st==200 else None
    result["auth_config"]=(
        "EMAIL_PASSWORD_ENABLED_METADATA" if isinstance(email,dict) and email.get("enabled") is True
        else "VISIBLE_EMAIL_PASSWORD_NOT_ENABLED" if isinstance(email,dict) and email.get("enabled") is False
        else "UNKNOWN_HTTP_"+str(st) if st!=200 else "UNKNOWN_SCHEMA")
    st,buckets=get(BUCKET_URL,token)
    result["storage_buckets"]=list_state(st,buckets,"items")
    result["h2_bindings"]="NOT_SELECTED_OR_INDEPENDENTLY_VERIFIED"
    result["enabled_image"]="NOT_SELECTED_OR_SECURITY_VERIFIED"
    result["approval_verifier"]="NOT_BOUND_OR_INDEPENDENTLY_VERIFIED"
    result["media_approval"]="NOT_ESTABLISHED"
    result["ttl_and_durable_cleanup"]="NOT_ESTABLISHED"
    result["h2_status"]="NO_GO"
    result["production_status"]="NO_GO"
    return result

def main():
    os.umask(0o077)
    try: token=preflight()
    except (Stop,OSError,ValueError,UnicodeError,TypeError) as exc:
        print("OLDX_H2R_RESULT=STOP_LOCAL_PREFLIGHT")
        print("OLDX_H2R_REASON="+(str(exc) if isinstance(exc,Stop) else type(exc).__name__))
        print("OLDX_H2R_CLOUD_RESOURCE_WRITES=NONE")
        return 2
    base=ROOT/("oldx-h2-provider-readonly-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        base.mkdir(mode=0o700)
        fd=os.open(MARKER,os.O_CREAT|os.O_EXCL|os.O_WRONLY|getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"w") as f:f.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE="+str(base)+"\n")
    except OSError:
        print("OLDX_H2R_RESULT=STOP_MARKER")
        return 2
    result=None
    status="STOP_AFTER_MARKER";reason="UNKNOWN"
    try:
        result=collect(token)
        status="READ_ONLY_METADATA_WITH_LIMITS"
        reason="STATIC_INVENTORY_NOT_H2_AUTHORITY"
    except (Stop,OSError,ValueError,UnicodeError,TypeError,KeyError) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        try:
            if result is not None:
                (base/"sanitized-h2-metadata.json").write_text(
                   json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
            with MARKER.open("a") as f:f.write("RESULT="+status+"\nREASON="+reason+"\n")
        except OSError:status="STOP_EVIDENCE_IO"
        print("OLDX_H2R_RESULT="+status)
        print("OLDX_H2R_REASON="+reason)
        if result:
            for key in ("project","cloud_run","service_accounts","kms_key_rings",
                        "kms_signing_keys","firestore_default_db","auth_config",
                        "storage_buckets","h2_bindings","approval_verifier"):
                value=result[key]
                if isinstance(value,dict): value=value.get("status","UNKNOWN")
                elif isinstance(value,list): value="BOUNDED_RING_INVENTORY_"+str(len(value))
                print("OLDX_H2R_"+key.upper()+"="+str(value))
        print("OLDX_H2R_H2_ENABLED=NOT_ATTEMPTED")
        print("OLDX_H2R_SA_KMS_DB_STORAGE_WRITES=NONE")
        print("OLDX_H2R_NO_SIGNING_OR_KEYS_FETCHED=TRUE")
        print("OLDX_H2R_DO_NOT_REPEAT=TRUE")
    return 0 if status=="READ_ONLY_METADATA_WITH_LIMITS" else 2

if __name__=="__main__":sys.exit(main())
