#!/usr/bin/env python3
"""OLDX H2L: NEW read-only KMS ring/key metadata after H2K API activation.

Only oldx-staging/asia-south1. One ring listing GET and <=3 existing ring
cryptoKeys listing GETs. No key versions, private/public key bytes, signing,
key or IAM create/update/delete, Auth/Firestore/Storage/Run, or API changes.
Prior H2K marker and success MUST be present. One-shot; no repeat after marker.
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
from urllib import request, error

ROOT = Path("/root")
OWNER = "yasminparmar087@gmail.com"
PROJECT = "oldx-staging"
LOCATION = "asia-south1"
SDK = ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
GCLOUD = SDK/"bin/gcloud"
PY = SDK/"platform/bundledpythonunix/bin/python3"
CONFIG = ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2K = ROOT/".oldx-step05-h2-kms-api-enable-owner-once-20261127"
MARKER = ROOT/".oldx-step05-h2-postenable-kms-rings-keys-readonly-once-20261127"
BASE = f"https://cloudkms.googleapis.com/v1/projects/{PROJECT}/locations/{LOCATION}/keyRings"
RINGS_URL = BASE + "?pageSize=100"
RING_PATTERN = re.compile(
    rf"projects/{PROJECT}/locations/{LOCATION}/keyRings/[A-Za-z0-9_-]{{1,63}}")
KEY_PATTERN = re.compile(
    rf"projects/{PROJECT}/locations/{LOCATION}/keyRings/[A-Za-z0-9_-]{{1,63}}/cryptoKeys/[A-Za-z0-9_-]{{1,63}}")
class Stop(Exception): pass
def need(cond, reason):
    if not cond: raise Stop(reason)
def cli(env, args):
    try:
        x = subprocess.run([str(GCLOUD)] + args, env=env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=25, check=False)
    except subprocess.TimeoutExpired:
        raise Stop("ISOLATED_GCLOUD_TIMEOUT") from None
    need(x.returncode == 0, "ISOLATED_GCLOUD_FAILED")
    return x.stdout.decode("utf-8", "replace").strip()
def token_for_owner():
    need(sys.argv[1:] == ["--h2-postenable-kms-rings-and-signing-key-metadata-once"],
         "EXACT_FLAG_REQUIRED")
    need(platform.system() == "Linux" and os.geteuid() == 0
         and "microsoft" in platform.release().lower(),
         "OWNER_ROOT_WSL_REQUIRED")
    need(not MARKER.exists() and not MARKER.is_symlink(),
         "H2L_MARKER_ALREADY_CONSUMED")
    need(H2K.is_file() and not H2K.is_symlink() and H2K.stat().st_uid == 0,
         "H2K_RECEIPT_NOT_TRUSTED")
    lines = H2K.read_text(encoding="utf-8").splitlines()
    need("ATTEMPT_CONSUMED=TRUE" in lines
         and "PROJECT=" + PROJECT in lines
         and "SERVICE=cloudkms.googleapis.com" in lines
         and "RESULT=PASS_KMS_API_ENABLED_EXACT_PROJECT_VERIFIED" in lines,
         "H2K_EXACT_PROJECT_KMS_SUCCESS_NOT_CONFIRMED")
    need(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid == 0,
         "NATIVE_SDK_UNVERIFIED")
    need(GCLOUD.is_file() and not GCLOUD.is_symlink()
         and GCLOUD.stat().st_uid == 0 and os.access(GCLOUD,os.X_OK),
         "NATIVE_GCLOUD_UNVERIFIED")
    py = PY.resolve(strict=True)
    need(py.is_relative_to(SDK.resolve(strict=True)) and py.is_file()
         and py.stat().st_uid == 0 and os.access(py,os.X_OK),
         "NATIVE_PYTHON_UNVERIFIED")
    need(CONFIG.is_dir() and not CONFIG.is_symlink()
         and CONFIG.stat().st_uid == 0,"ISOLATED_CONFIG_UNVERIFIED")
    env = dict(os.environ)
    env.update({"HOME":str(ROOT),"PATH":str(SDK/"bin")+":/usr/bin:/bin",
        "CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    need(cli(env,["auth","list","--filter=status:ACTIVE",
        "--format=value(account)"]) == OWNER,"OWNER_IDENTITY_MISMATCH")
    need(cli(env,["config","get-value","project"]) == PROJECT,
         "PROJECT_MISMATCH")
    token = cli(env,["--quiet","--account="+OWNER,"auth","print-access-token"])
    need(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)),
         "OWNER_TOKEN_UNAVAILABLE")
    return token
class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs): return None
OPENER = request.build_opener(
    request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())
def metadata_get(url, token):
    keys = url.startswith(BASE+"/") and url.endswith("/cryptoKeys?pageSize=25")
    if keys:
        parent=url[len("https://cloudkms.googleapis.com/v1/"):].split("/cryptoKeys?")[0]
        need(bool(RING_PATTERN.fullmatch(parent)), "KMS_RING_REQUEST_OUTSIDE_SCOPE")
    else:
        need(url == RINGS_URL, "KMS_URL_OUTSIDE_SCOPE")
    req=request.Request(url,method="GET",headers={
        "Authorization":"Bearer "+token, "Accept":"application/json",
        "User-Agent":"OLDX-H2L-postenable-GET-metadata-only/1"})
    try:
        with OPENER.open(req,timeout=35) as response:
            raw=response.read(131073)
            need(response.status == 200 and len(raw)<=131072,
                 "KMS_METADATA_UNEXPECTED_RESPONSE_SIZE")
            obj=json.loads(raw) if raw else {}
            need(isinstance(obj,dict), "KMS_METADATA_RESPONSE_SCHEMA")
            return 200,obj,"OK"
    except error.HTTPError as exc:
        status=exc.code
        raw=exc.read(4097)
        exc.close()
        reason="UNKNOWN"
        if len(raw)<=4096:
            try:
                error_obj=json.loads(raw).get("error",{})
                s=error_obj.get("status","UNKNOWN")
                if isinstance(s,str) and re.fullmatch(r"[A-Z_]{3,60}",s):
                    reason=s
            except (ValueError,TypeError,AttributeError): pass
        return status,{},reason
    except (error.URLError,TimeoutError,ssl.SSLError):
        return 0,{},"NETWORK_OR_TIMEOUT"
def item_list(status,obj,field,reason):
    if status != 200:
        return {"state":"UNKNOWN_HTTP_"+str(status) if status else
                "UNKNOWN_NETWORK_OR_TIMEOUT","reason":reason}
    rows=obj.get(field,[])
    need(isinstance(rows,list), "KMS_"+field.upper()+"_SCHEMA")
    if obj.get("nextPageToken"):
        return {"state":"PARTIAL_PAGINATED","first_page_count":len(rows)}
    return {"state":"COMPLETE_VISIBLE_PAGE","count":len(rows),"items":rows}
def main():
    os.umask(0o077)
    try: token=token_for_owner()
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as e:
        print("OLDX_H2L_RESULT=STOP_BEFORE_REQUEST")
        print("OLDX_H2L_REASON="+(str(e) if isinstance(e,Stop) else type(e).__name__))
        print("OLDX_H2L_RESOURCE_WRITES=NONE")
        return 2
    evid=ROOT/("oldx-h2-kms-metadata-"+
               datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    try:
        evid.mkdir(mode=0o700)
        fd=os.open(MARKER,os.O_CREAT|os.O_EXCL|os.O_WRONLY|
                   getattr(os,"O_NOFOLLOW",0),0o600)
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            f.write("ATTEMPT_CONSUMED=TRUE\nEVIDENCE="+str(evid)+"\n")
    except OSError:
        print("OLDX_H2L_RESULT=STOP_MARKER")
        return 2
    result="STOP_AFTER_MARKER"
    reason="UNKNOWN"
    summary={}
    try:
        status,obj,why=metadata_get(RINGS_URL,token)
        rings=item_list(status,obj,"keyRings",why)
        summary["rings"]={k:v for k,v in rings.items() if k!="items"}
        summary["signing_keys"]=[]
        if rings["state"]=="COMPLETE_VISIBLE_PAGE":
            names=[]
            for x in rings["items"]:
                need(isinstance(x,dict) and
                     bool(RING_PATTERN.fullmatch(x.get("name",""))),
                     "KMS_RING_RESOURCE_ID_UNEXPECTED")
                names.append(x["name"])
            need(len(set(names))==len(names),"KMS_RING_RESOURCE_DUPLICATE")
            summary["ring_names"]=[name.rsplit("/",1)[-1] for name in names]
            if len(names)>3:
                summary["keys_scope"]="PARTIAL_TOO_MANY_RINGS_FOR_BOUNDED_CHECK"
            else:
                for name in names:
                    key_url=("https://cloudkms.googleapis.com/v1/"+name+
                             "/cryptoKeys?pageSize=25")
                    st,data,err=metadata_get(key_url,token)
                    keys=item_list(st,data,"cryptoKeys",err)
                    entry={"ring":name.rsplit("/",1)[-1],"state":keys["state"]}
                    if keys["state"]=="COMPLETE_VISIBLE_PAGE":
                        found=[]
                        for k in keys["items"]:
                            need(isinstance(k,dict) and
                                 bool(KEY_PATTERN.fullmatch(k.get("name",""))),
                                 "KMS_KEY_RESOURCE_ID_UNEXPECTED")
                            if k.get("purpose")=="ASYMMETRIC_SIGN":
                                found.append(k["name"].rsplit("/",1)[-1])
                        entry["signing_key_names"]=found
                        entry["first_page_keys_count"]=keys["count"]
                    else:
                        entry["reason"]=keys.get("reason","PARTIAL")
                        entry["first_page_keys_count"]=keys.get("first_page_count")
                    summary["signing_keys"].append(entry)
        result="KMS_POST_ENABLE_METADATA_READ_WITH_LIMITS"
        reason="BOUNDED_GET_ONLY_NOT_H2_APPROVAL"
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as e:
        reason=str(e) if isinstance(e,Stop) else type(e).__name__
    finally:
        try:
            (evid/"sanitized-kms-ring-key-metadata.json").write_text(json.dumps({
                "project":PROJECT,"location":LOCATION,"summary":summary,
                "h2":"NO_GO","production":"NO_GO","resource_writes":False},
                indent=2,sort_keys=True)+"\n",encoding="utf-8")
            with MARKER.open("a",encoding="utf-8") as f:
                f.write("RESULT="+result+"\nREASON="+reason+"\n")
        except OSError:result="STOP_EVIDENCE_WRITE"
        print("OLDX_H2L_RESULT="+result)
        print("OLDX_H2L_REASON="+reason)
        rings=summary.get("rings",{})
        print("OLDX_H2L_RING_LIST="+rings.get("state","UNKNOWN_NOT_COMPLETED"))
        if "count" in rings: print("OLDX_H2L_RING_COUNT="+str(rings["count"]))
        if "reason" in rings: print("OLDX_H2L_RING_LIST_REASON="+rings["reason"])
        if "ring_names" in summary:
            print("OLDX_H2L_RING_NAMES="+(",".join(summary["ring_names"]) or "NONE"))
        if "keys_scope" in summary:
            print("OLDX_H2L_KEY_LIST_SCOPE="+summary["keys_scope"])
        for item in summary.get("signing_keys",[]):
            print("OLDX_H2L_KEY_RING_"+item["ring"]+"="+item["state"]+
                  "_SIGNING_KEYS_"+(",".join(item.get("signing_key_names",[]))
                                   if "signing_key_names" in item else "UNKNOWN"))
        print("OLDX_H2L_KMS_KEY_OR_VERSION_CREATED=FALSE")
        print("OLDX_H2L_RESOURCE_WRITES=NONE")
        print("OLDX_H2L_H2_ENABLED=NOT_ATTEMPTED")
        print("OLDX_H2L_DO_NOT_REPEAT=TRUE")
    return 0 if result=="KMS_POST_ENABLE_METADATA_READ_WITH_LIMITS" else 2
if __name__=="__main__": sys.exit(main())
