#!/usr/bin/env python3
"""OLDX H1B W3-W6: guarded one-new-service private OFF trial + same-session rollback.

Never touch other Cloud Run services, Firebase, C1A, shared Registry or old SAs.
One new Cloud Run create, optional ONE owner-only Invoker grant, <=4 HTTP probes,
one etag-protected delete of this exact new service. Fail closed on any mismatch.
Do not rerun this script after its new one-shot marker is consumed.
"""
from __future__ import annotations
import json
import os
import platform
import re
import secrets
import ssl
import subprocess
import sys
import time
from datetime import datetime,timezone
from pathlib import Path
from urllib import request,error,parse

OWNER="yasminparmar087@gmail.com"
PROJECT="oldx-staging"
REGION="asia-south1"
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
W3V=ROOT/".oldx-h1b-w3-private-validate-only-once-20261126"
G2B=ROOT/".oldx-h1b-g2b-retained-single-push-once-20261126"
MARKER=ROOT/".oldx-h1b-w3w6-private-off-once-20261126"
PARENT=f"projects/{PROJECT}/locations/{REGION}"
SNAME=f"{PARENT}/services/{SERVICE}"
SURL=f"https://run.googleapis.com/v2/{SNAME}"
SCREATE=f"https://run.googleapis.com/v2/{PARENT}/services?serviceId={SERVICE}"
SAR=f"https://iam.googleapis.com/v1/projects/{PROJECT}/serviceAccounts/{SA}"
SA_TEST=SAR+":testIamPermissions"
IAMTEST=f"https://cloudresourcemanager.googleapis.com/v1/projects/{PROJECT}:testIamPermissions"
POLICY=SURL+":getIamPolicy"
SETPOLICY=SURL+":setIamPolicy"
RUN_PERMISSIONS={"run.services.create","run.services.delete","run.services.get","run.services.setIamPolicy"}
class Stop(Exception):pass
def require(ok,why):
    if not ok:raise Stop(why)
def now():return datetime.now(timezone.utc).isoformat()
def marker_lines(path):
    require(path.is_file() and not path.is_symlink() and path.stat().st_uid==0,"EVIDENCE_MARKER_MISSING")
    return path.read_text(encoding="utf-8").splitlines()
def save_atomic(path,content):
    with path.open("x",encoding="utf-8") as f:f.write(content)
def append_marker(line):
    with MARKER.open("a",encoding="utf-8") as f:f.write(line+"\n")
def shell(cmd,env,limit=25):
    try:
        out=subprocess.run(cmd,env=env,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=limit,check=False)
    except subprocess.TimeoutExpired:
        raise Stop("LOCAL_GCLOUD_TIMEOUT") from None
    require(out.returncode==0,"LOCAL_GCLOUD_FAILED")
    return out.stdout.decode("utf-8","replace").strip()

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None
OPENER=request.build_opener(request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())
ALLOWED_POST={SCREATE,IAMTEST,SA_TEST,SETPOLICY}
ALLOWED_GET={SURL,SAR,POLICY}
def api(method,url,token,payload=None):
    valid=(method=="GET" and url in ALLOWED_GET) or \
          (method=="POST" and url in ALLOWED_POST) or \
          (method=="DELETE" and url.startswith(SURL+"?etag="))
    if not valid and method=="GET" and url.startswith(f"https://run.googleapis.com/v2/{PARENT}/operations/"):
        valid=bool(re.fullmatch(re.escape(f"https://run.googleapis.com/v2/{PARENT}/operations/")+r"[A-Za-z0-9_-]+",url))
    require(valid,"URL_OR_METHOD_OUTSIDE_SCOPE")
    hdr={"Authorization":"Bearer "+token,"Accept":"application/json",
         "User-Agent":"OLDX-H1B-private-off-one-session/1"}
    body=None
    if payload is not None:
        body=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
        hdr["Content-Type"]="application/json"
    req=request.Request(url,data=body,method=method,headers=hdr)
    try:
        with OPENER.open(req,timeout=35) as response:
            raw=response.read(262145)
            require(len(raw)<=262144,"API_RESPONSE_TOO_LARGE")
            parsed=json.loads(raw) if raw else {}
            require(isinstance(parsed,dict),"INVALID_API_JSON")
            return response.status,parsed
    except error.HTTPError as exc:
        status=exc.code;exc.close()
        return status,{}
    except (error.URLError,TimeoutError,ssl.SSLError):
        raise Stop("GOOGLE_API_NETWORK_OR_TIMEOUT") from None
def task_op(name,token):
    require(isinstance(name,str) and
            bool(re.fullmatch(re.escape(PARENT)+r"/operations/[A-Za-z0-9_-]+",name)),
            "CLOUD_RUN_OPERATION_NAME_OUT_OF_SCOPE")
    return api("GET","https://run.googleapis.com/v2/"+name,token)
def wait_op(name,token):
    for _ in range(35):
        status,body=task_op(name,token)
        require(status==200,"OPERATION_READ_HTTP_"+str(status))
        if body.get("done") is True:
            require(not body.get("error"),"OPERATION_COMPLETED_ERROR")
            return body
        time.sleep(8)
    raise Stop("OPERATION_TIMEOUT_NO_RETRY")

def service_body(session):
    return {
       "description":"Temporary OLDX H1B private compiled-OFF no-real-user-data staging only",
       "labels":{"oldx-h1b":"off-private","oldx-session":session},
       "ingress":"INGRESS_TRAFFIC_ALL",
       "invokerIamDisabled":False,
       "scaling":{"minInstanceCount":0,"maxInstanceCount":1,"scalingMode":"AUTOMATIC"},
       "template":{
          "serviceAccount":SA,"timeout":"5s","maxInstanceRequestConcurrency":1,
          "executionEnvironment":"EXECUTION_ENVIRONMENT_GEN2",
          "containers":[{"image":IMAGE,"ports":[{"containerPort":8080}],
                        "resources":{"limits":{"cpu":"1","memory":"512Mi"},
                                     "cpuIdle":True,"startupCpuBoost":False}}]
       }
    }
def inspect_service(s,session,expected_uid=None):
    require(s.get("name")==SNAME,"NEW_SERVICE_NAME_MISMATCH")
    uid=s.get("uid")
    require(isinstance(uid,str) and bool(re.fullmatch(r"[0-9a-fA-F-]{20,64}",uid)),
            "NEW_SERVICE_UID_NOT_VERIFIED")
    if expected_uid is not None:
        require(uid==expected_uid,"NEW_SERVICE_UID_CHANGED")
    require(s.get("labels",{}).get("oldx-session")==session,"SESSION_LABEL_MISMATCH")
    require(s.get("invokerIamDisabled") is False,"IAM_INVOKER_CHECK_DISABLED")
    require(s.get("ingress")=="INGRESS_TRAFFIC_ALL","INGRESS_MISMATCH")
    template=s.get("template") or {}
    require(template.get("serviceAccount")==SA,"RUNTIME_SA_MISMATCH")
    require(template.get("timeout")=="5s" and
            template.get("maxInstanceRequestConcurrency")==1,
            "RUNTIME_LIMITS_MISMATCH")
    containers=template.get("containers",[])
    require(len(containers)==1 and containers[0].get("image")==IMAGE,
            "EXACT_IMMUTABLE_IMAGE_MISMATCH")
    require((containers[0].get("resources") or {}).get("limits",{}).get("cpu")=="1" and
            (containers[0].get("resources") or {}).get("limits",{}).get("memory")=="512Mi",
            "CPU_MEMORY_LIMITS_MISMATCH")
    scale=s.get("scaling",{})
    require(scale.get("minInstanceCount",0)==0 and scale.get("maxInstanceCount")==1,
            "SERVICE_SCALING_MISMATCH")
    require(s.get("etag"),"MISSING_SERVICE_ETAG")
    return uid

def active_identity():
    require(sys.argv[1:]==["--w3-w6-private-off-single-session-once"],"EXACT_FLAG_REQUIRED")
    require(platform.system()=="Linux" and os.geteuid()==0 and
            "microsoft" in platform.release().lower(),"OWNER_ROOT_WSL_REQUIRED")
    require(not MARKER.exists() and not MARKER.is_symlink(),"W3W6_ONESHOT_CONSUMED")
    require(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,
            "NATIVE_SDK_NOT_VERIFIED")
    require(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK),
            "NATIVE_CLI_MISSING")
    py=PY.resolve(strict=True)
    require(py.is_relative_to(SDK.resolve(strict=True)) and py.is_file() and
            os.access(py,os.X_OK) and py.stat().st_uid==0,"BUNDLED_PYTHON_MISMATCH")
    require(CONFIG.is_dir() and not CONFIG.is_symlink() and CONFIG.stat().st_uid==0,
            "ISOLATED_CLOUDSDK_CONFIG_NOT_VERIFIED")
    old=marker_lines(W1)
    require("SA_UID="+SA_UID in old and
            "RESULT=NEW_NO_KEY_SA_CREATED_RIGHTS_PASS_WITH_LIMITS" in old,
            "W1_SA_RECEIPT_MISMATCH")
    require("RESULT=VALIDATE_ONLY_ACCEPTED_WITH_LIMITS" in marker_lines(W3V),
            "W3V_VALIDATE_ONLY_NOT_PASS")
    require("RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED" in marker_lines(G2B),
            "FROZEN_IMAGE_RECEIPT_NOT_PASS")
    env=dict(os.environ)
    env.update({"HOME":str(ROOT),"CLOUDSDK_CONFIG":str(CONFIG),
        "CLOUDSDK_PYTHON":str(PY),"PATH":str(SDK/"bin")+":/usr/bin:/bin",
        "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
        "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false"})
    env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
    env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
    require(shell([str(CLI),"auth","list","--filter=status:ACTIVE",
        "--format=value(account)"],env)==OWNER,"WRONG_OWNER")
    require(shell([str(CLI),"config","get-value","project"],env)==PROJECT,"WRONG_PROJECT")
    token=shell([str(CLI),"--quiet","--account="+OWNER,"auth","print-access-token"],env)
    require(bool(re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",token)),
            "OWNER_OAUTH_ACCESS_TOKEN_UNAVAILABLE")
    return env,token

def preflight(token):
    status,sa=api("GET",SAR,token)
    require(status==200 and sa.get("email")==SA and str(sa.get("uniqueId"))==SA_UID
            and sa.get("disabled") is not True,"EXACT_NEW_SA_IDENTITY_MISMATCH")
    status,_=api("GET",SURL,token)
    require(status==404,"EXACT_NEW_RUN_SERVICE_NOT_ABSENT_HTTP_"+str(status))
    status,perms=api("POST",IAMTEST,token,
        {"permissions":sorted(RUN_PERMISSIONS)})
    require(status==200 and RUN_PERMISSIONS.issubset(set(perms.get("permissions",[]))),
            "RUN_CREATE_DELETE_RIGHTS_NOT_CONFIRMED")
    status,rights=api("POST",SA_TEST,token,
        {"permissions":["iam.serviceAccounts.actAs","iam.serviceAccounts.delete"]})
    require(status==200 and {"iam.serviceAccounts.actAs","iam.serviceAccounts.delete"}.issubset(
         set(rights.get("permissions",[]))),"NEW_SA_ACTAS_DELETE_RIGHTS_MISSING")

def direct_policy(token):
    st,obj=api("GET",POLICY,token)
    require(st==200,"NEW_SERVICE_POLICY_GET_HTTP_"+str(st))
    require(isinstance(obj.get("bindings",[]),list),"IAM_POLICY_SCHEMA_INVALID")
    return obj
def exact_owner_only(policy):
    bs=policy.get("bindings",[])
    return len(bs)==1 and bs[0].get("role")=="roles/run.invoker" and \
           bs[0].get("members")==["user:"+OWNER] and "condition" not in bs[0]
def probe(url,method,identity=None):
    from urllib.parse import urlsplit
    parts=urlsplit(url)
    require(parts.scheme=="https" and parts.hostname is not None and
            parts.hostname.endswith(".run.app") and not parts.username and
            not parts.password and parts.port is None,"PROBE_ORIGIN_INVALID")
    hdr={"User-Agent":"OLDX-H1B-four-owner-only-probes"}
    if identity:hdr["Authorization"]="Bearer "+identity
    req=request.Request(url,headers=hdr,method=method)
    try:
        with OPENER.open(req,timeout=30) as r:
            r.read(8192)
            return r.status
    except error.HTTPError as e:
        code=e.code;e.close()
        return code
    except (error.URLError,ssl.SSLError,TimeoutError):
        raise Stop("HOSTED_PROBE_NETWORK_ERROR") from None

def cleanup_service(token,session,uid):
    """Exactly one DELETE attempt when current uid, label, etag, image and SA match."""
    if not uid:
        return "STOP_MANUAL_RECOVERY_NO_KNOWN_NEW_UID"
    try:
        st,service=api("GET",SURL,token)
        if st==404:
            return "SERVICE_ALREADY_ABSENT_404"
        require(st==200,"CLEANUP_RUN_GET_HTTP_"+str(st))
        inspect_service(service,session,uid)
        pol=direct_policy(token)
        require(not pol.get("bindings",[]) or exact_owner_only(pol),
                "UNEXPECTED_DIRECT_IAM_BINDINGS_STOP_DELETE")
        etag=service.get("etag")
        url=SURL+"?etag="+parse.quote(etag,safe="")
        st,operation=api("DELETE",url,token)
        require(st==200,"RUN_DELETE_RESPONSE_HTTP_"+str(st))
        wait_op(operation.get("name"),token)
        st,_=api("GET",SURL,token)
        require(st==404,"RUN_DELETION_NOT_CONFIRMED_HTTP_"+str(st))
        return "NEW_ONLY_RUN_SERVICE_DELETED_CONFIRMED"
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as e:
        return "STOP_MANUAL_RECOVERY_"+(str(e) if isinstance(e,Stop)
                                       else type(e).__name__)

def main():
    os.umask(0o077)
    try:
        env,token=active_identity()
        preflight(token)
    except (Stop,OSError,ValueError,TypeError) as exc:
        print("H1B_W3W6_RESULT=STOP_BEFORE_SERVICE_CREATE")
        print("H1B_W3W6_REASON="+(str(exc) if isinstance(exc,Stop) else type(exc).__name__))
        return 2
    session="h1b-"+secrets.token_hex(9)
    evidence=ROOT/("oldx-h1b-w3w6-"+session)
    try:
        evidence.mkdir(mode=0o700)
        with MARKER.open("x",encoding="utf-8") as f:
            f.write("ATTEMPT_CONSUMED=TRUE\nSESSION="+session+"\nEVIDENCE="+str(evidence)+"\n")
        os.chmod(MARKER,0o600)
    except OSError:
        print("H1B_W3W6_RESULT=STOP_MARKER_OR_EVIDENCE_COLLISION")
        return 2
    create_attempted=False
    uid=None
    outcome="STOP_AFTER_MARKER"
    reason="UNKNOWN"
    cleanup="NOT_STARTED"
    probes=0
    grant="NOT_ATTEMPTED"
    try:
        print("H1B_W3W6_STAGE=ONE_NEW_PRIVATE_OFF_SERVICE_CREATE_ATTEMPT",flush=True)
        create_attempted=True
        st,operation=api("POST",SCREATE,token,service_body(session))
        require(st==200,"CREATE_SERVICE_HTTP_"+str(st)+"_MAYBE_PARTIAL")
        name=operation.get("name")
        require(isinstance(name,str),"CREATE_OPERATION_NAME_MISSING")
        append_marker("CREATE_OPERATION="+name)
        wait_op(name,token)
        st,s=api("GET",SURL,token)
        require(st==200,"CREATE_SERVICE_NOT_READBACK_HTTP_"+str(st))
        uid=inspect_service(s,session)
        append_marker("SERVICE_UID="+uid)
        # Enforce a single fresh exact service IAM policy before any hosted probe.
        p=direct_policy(token)
        require(not p.get("bindings",[]),"UNEXPECTED_DIRECT_IAM_BINDINGS")
        require(isinstance(p.get("etag"),str) and p["etag"],
                "EMPTY_POLICY_ETAG_MISSING")
        # Optional Owner-only new-service Invoker grant, allowed by owner scope.
        grant="ATTEMPTED"
        st,policy=api("POST",SETPOLICY,token,
            {"policy":{"bindings":[{"role":"roles/run.invoker",
                  "members":["user:"+OWNER]}],"etag":p["etag"],"version":1}})
        require(st==200 and exact_owner_only(policy),
                "EXACT_OWNER_ONLY_INVOKER_GRANT_NOT_VERIFIED")
        require(exact_owner_only(direct_policy(token)),
                "OWNER_ONLY_INVOKER_POLICY_READBACK_FAILED")
        grant="EXACT_OWNER_ONLY_BINDING_VERIFIED"
        st,s=api("GET",SURL,token)
        require(st==200,"SERVICE_READBACK_AFTER_IAM_FAILED")
        inspect_service(s,session,uid)
        uri=s.get("uri")
        require(isinstance(uri,str) and bool(re.fullmatch(
           r"https://[a-z0-9-]+(?:-[a-z0-9-]+)*[.]run[.]app",uri)),
           "EXPECTED_RUN_APP_URI_UNVERIFIED")
        print("H1B_W3W6_STAGE=FOUR_BOUNDED_NEW_SERVICE_ONLY_PROBES",flush=True)
        # Four HTTP requests total; no HTTP retries, no real data/secret payload.
        code=probe(uri+"/health","GET");probes+=1
        require(code==403,"ANONYMOUS_403_REQUIRED_GOT_"+str(code))
        identity=shell([str(CLI),"auth","print-identity-token"],env)
        require(bool(re.fullmatch(r"[A-Za-z0-9_-]+[.][A-Za-z0-9_-]+[.][A-Za-z0-9_-]+",identity)),
                "IDENTITY_TOKEN_UNAVAILABLE")
        for method,path,expect in (("GET","/health",200),
                                   ("POST","/api/staging/marketplace/owner",503),
                                   ("GET","/unmatched-oldx-h1b-path",404)):
            code=probe(uri+path,method,identity);probes+=1
            require(code==expect,"HOSTED_RESPONSE_MISMATCH_"+str(probes)+"_"+str(code))
        outcome="PRIVATE_OFF_FOUR_PROBES_PASS_CLEANUP_PENDING"
        reason="EXPECTED_403_200_503_404"
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyboardInterrupt) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        # If a create operation succeeded but the first readback failed, we must
        # NOT delete a resource merely because the name matches.
        if create_attempted:
            cleanup=cleanup_service(token,session,uid)
        else:
            cleanup="NO_SERVICE_CREATE_ATTEMPT"
        try:
            with (evidence/"sanitized-result.json").open("x",encoding="utf-8") as f:
                json.dump({"session":session,"service":SNAME,"uid":uid,
                    "sa_uid":SA_UID,"source_image":IMAGE,"create_attempted":create_attempted,
                    "probes_attempted":probes,"owner_invoker":grant,
                    "result_before_cleanup":outcome,"reason":reason,"service_cleanup":cleanup,
                    "sa_cleanup":"RETAIN_PENDING_DEPENDENCY_GUARDED_DECISION",
                    "registry_image_cleanup":"RETAIN_SHARED_REPO_REFERENCE_NOT_PROVEN"},f,indent=2)
                f.write("\n")
            append_marker("SERVICE_UID="+str(uid))
            append_marker("SERVICE_CLEANUP="+cleanup)
            append_marker("RESULT="+outcome)
            append_marker("REASON="+reason)
        except OSError:
            cleanup="STOP_MANUAL_RECOVERY_LOCAL_EVIDENCE_WRITE_FAILED"
        print("H1B_W3W6_NEW_SA_UID="+SA_UID)
        print("H1B_W3W6_SERVICE_UID="+(uid or "UNKNOWN"))
        print("H1B_W3W6_CREATE_ATTEMPTED="+str(create_attempted).upper())
        print("H1B_W3W6_OWNER_INVOKER="+grant)
        print("H1B_W3W6_HTTP_PROBES_ATTEMPTED="+str(probes))
        print("H1B_W3W6_SERVICE_CLEANUP="+cleanup)
        print("H1B_W3W6_SA_CLEANUP=RETAIN_PENDING_DEPENDENCY_GUARDS")
        print("H1B_W3W6_REGISTRY_IMAGE=RETAIN_NOT_REPUSHED")
        print("H1B_W3W6_RESULT="+outcome)
        print("H1B_W3W6_REASON="+reason)
        print("H1B_W3W6_DO_NOT_REPEAT=TRUE")
    return 0 if outcome=="PRIVATE_OFF_FOUR_PROBES_PASS_CLEANUP_PENDING" and \
        cleanup=="NEW_ONLY_RUN_SERVICE_DELETED_CONFIRMED" else 2

if __name__=="__main__":
    sys.exit(main())
