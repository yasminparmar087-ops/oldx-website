#!/usr/bin/env python3
"""BAJUTO/OLDX H2W: owner-approved ONE new private/internal H2 Gateway OFF
Cloud Run staging service and exactly one new-service-only Owner Invoker binding.
No HTTP probes from WSL (internal-only ingress), no other service or IAM writes,
no KMS, Firestore, Firebase, Registry push, image rebuild or production.
Fail closed. Do not rerun after this one-shot marker is consumed.
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
SERVICE="oldx-c2-h2-private-gateway"
SA="oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com"
SA_UID="107238619872767759560"
IMAGE=("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
 "oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2")
ROOT=Path("/root")
SDK=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
CLI=SDK/"bin/gcloud"
PY=SDK/"platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2V=ROOT/".oldx-step05-h2v-one-immutable-local-image-push-once-20261127"
MARKER=ROOT/".oldx-step05-h2w-new-internal-off-cloudrun-service-once-20261127"
PARENT=f"projects/{PROJECT}/locations/{REGION}"
SNAME=f"{PARENT}/services/{SERVICE}"
SURL=f"https://run.googleapis.com/v2/{SNAME}"
SCREATE=f"https://run.googleapis.com/v2/{PARENT}/services?serviceId={SERVICE}"
SAR=f"https://iam.googleapis.com/v1/projects/{PROJECT}/serviceAccounts/{SA}"
SA_TEST=SAR+":testIamPermissions"
IAMTEST=f"https://cloudresourcemanager.googleapis.com/v1/projects/{PROJECT}:testIamPermissions"
POLICY=SURL+":getIamPolicy"
SETPOLICY=SURL+":setIamPolicy"
RUN_PERMISSIONS={"run.services.create","run.services.delete","run.services.get","run.services.setIamPolicy","run.services.getIamPolicy"}
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
          False
    if not valid and method=="GET" and url.startswith(f"https://run.googleapis.com/v2/{PARENT}/operations/"):
        valid=bool(re.fullmatch(re.escape(f"https://run.googleapis.com/v2/{PARENT}/operations/")+r"[A-Za-z0-9_-]+",url))
    require(valid,"URL_OR_METHOD_OUTSIDE_SCOPE")
    hdr={"Authorization":"Bearer "+token,"Accept":"application/json",
         "User-Agent":"BAJUTO-H2W-owner-internal-off-cloudrun/1"}
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
       "description":"BAJUTO/OLDX H2 private internal default-OFF Gateway staging, no user data",
       "labels":{"oldx-h2":"off-private","oldx-session":session},
       "ingress":"INGRESS_TRAFFIC_INTERNAL_ONLY",
       "invokerIamDisabled":False,
       "scaling":{"minInstanceCount":0,"maxInstanceCount":1,"scalingMode":"AUTOMATIC"},
       "template":{
          "serviceAccount":SA,"timeout":"5s","maxInstanceRequestConcurrency":1,
          "executionEnvironment":"EXECUTION_ENVIRONMENT_GEN2",
          "containers":[{"image":IMAGE,"ports":[{"containerPort":8080}],
                        "env":[{"name":"OLDX_H2U_MODE","value":"OFF"},
                               {"name":"NODE_ENV","value":"production"}],
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
    require(s.get("labels",{}).get("oldx-session")==session and
            s.get("labels",{}).get("oldx-h2")=="off-private","SESSION_LABEL_MISMATCH")
    require(s.get("invokerIamDisabled",False) is False,"IAM_INVOKER_CHECK_DISABLED")
    require(s.get("ingress")=="INGRESS_TRAFFIC_INTERNAL_ONLY","NOT_INTERNAL_ONLY_INGRESS")
    template=s.get("template") or {}
    require(template.get("serviceAccount")==SA,"RUNTIME_SA_MISMATCH")
    require(template.get("timeout")=="5s" and
            template.get("maxInstanceRequestConcurrency")==1,
            "RUNTIME_LIMITS_MISMATCH")
    containers=template.get("containers",[])
    require(len(containers)==1 and containers[0].get("image")==IMAGE,
            "EXACT_IMMUTABLE_IMAGE_MISMATCH")
    require({(v.get("name"),v.get("value")) for v in containers[0].get("env",[])} ==
            {("OLDX_H2U_MODE","OFF"),("NODE_ENV","production")},
            "OFF_ENV_MISMATCH")
    require((containers[0].get("resources") or {}).get("limits",{}).get("cpu")=="1" and
            (containers[0].get("resources") or {}).get("limits",{}).get("memory")=="512Mi",
            "CPU_MEMORY_LIMITS_MISMATCH")
    scale=s.get("scaling",{})
    require(scale.get("minInstanceCount",0)==0 and scale.get("maxInstanceCount")==1,
            "SERVICE_SCALING_MISMATCH")
    require(s.get("etag"),"MISSING_SERVICE_ETAG")
    return uid

def active_identity():
    require(sys.argv[1:]==["--h2w-owner-approved-one-internal-off-gateway-service-create-once"],"EXACT_FLAG_REQUIRED")
    require(platform.system()=="Linux" and os.geteuid()==0 and
            "microsoft" in platform.release().lower(),"OWNER_ROOT_WSL_REQUIRED")
    require(not MARKER.exists() and not MARKER.is_symlink(),"H2W_ONESHOT_ALREADY_CONSUMED")
    require(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid==0,
            "NATIVE_SDK_NOT_VERIFIED")
    require(CLI.is_file() and not CLI.is_symlink() and os.access(CLI,os.X_OK),
            "NATIVE_CLI_MISSING")
    py=PY.resolve(strict=True)
    require(py.is_relative_to(SDK.resolve(strict=True)) and py.is_file() and
            os.access(py,os.X_OK) and py.stat().st_uid==0,"BUNDLED_PYTHON_MISMATCH")
    require(CONFIG.is_dir() and not CONFIG.is_symlink() and CONFIG.stat().st_uid==0,
            "ISOLATED_CLOUDSDK_CONFIG_NOT_VERIFIED")
    old=marker_lines(H2V)
    require("RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED" in old and
            "TAG=h2v-off-20261127-793639b68d15e55ea4a" in old,
            "H2V_EXACT_REMOTE_IMAGE_RECEIPT_NOT_PASS")
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
        {"permissions":["iam.serviceAccounts.actAs"]})
    require(status==200 and "iam.serviceAccounts.actAs" in
         rights.get("permissions",[]),"GATEWAY_SA_ACTAS_RIGHTS_MISSING")

def direct_policy(token):
    st,obj=api("GET",POLICY,token)
    require(st==200,"NEW_SERVICE_POLICY_GET_HTTP_"+str(st))
    require(isinstance(obj.get("bindings",[]),list),"IAM_POLICY_SCHEMA_INVALID")
    return obj
def exact_owner_only(policy):
    bs=policy.get("bindings",[])
    return len(bs)==1 and bs[0].get("role")=="roles/run.invoker" and \
           bs[0].get("members")==["user:"+OWNER] and "condition" not in bs[0]

def main():
    os.umask(0o077)
    try:
        env,token=active_identity()
        preflight(token)
    except (Stop,OSError,ValueError,TypeError,UnicodeError) as exc:
        print("H2W_RESULT=STOP_BEFORE_CLOUD_WRITES")
        print("H2W_REASON="+(str(exc) if isinstance(exc,Stop) else type(exc).__name__))
        print("H2W_CREATE_ATTEMPTED=FALSE")
        print("H2W_IAM_WRITE_ATTEMPTED=FALSE")
        print("H2W_H2_PRODUCTION=NO_GO")
        return 2
    session="h2w-"+secrets.token_hex(9)
    evidence=ROOT/("oldx-h2w-internal-gateway-"+session)
    try:
        evidence.mkdir(mode=0o700)
        with MARKER.open("x",encoding="utf-8") as f:
            f.write("ATTEMPT_CONSUMED=TRUE\nSESSION="+session+
                    "\nEVIDENCE="+str(evidence)+"\nIMAGE="+IMAGE+"\n")
        os.chmod(MARKER,0o600)
    except OSError:
        print("H2W_RESULT=STOP_MARKER_OR_EVIDENCE_COLLISION")
        return 2
    create_attempted=False
    policy_attempted=False
    uid=None
    etag=None
    result="STOP_AFTER_MARKER"
    reason="UNKNOWN"
    invoker="NOT_ATTEMPTED"
    try:
        # One more exact-target GET 404 immediately before the first write.
        st,_=api("GET",SURL,token)
        require(st==404,"SERVICE_NAME_COLLISION_BEFORE_CREATE_HTTP_"+str(st))
        print("H2W_STAGE=ONE_NEW_INTERNAL_OFF_GATEWAY_SERVICE_CREATE_ATTEMPT",flush=True)
        create_attempted=True
        st,op=api("POST",SCREATE,token,service_body(session))
        require(st==200,"CREATE_RESPONSE_HTTP_"+str(st)+"_MAYBE_PARTIAL")
        op_name=op.get("name")
        require(isinstance(op_name,str),"CREATE_OPERATION_NAME_MISSING")
        append_marker("CREATE_OPERATION="+op_name)
        wait_op(op_name,token)
        st,service=api("GET",SURL,token)
        require(st==200,"CREATED_SERVICE_GET_HTTP_"+str(st))
        uid=inspect_service(service,session)
        etag=service.get("etag")
        append_marker("SERVICE_UID="+uid)
        append_marker("SERVICE_ETAG="+etag)
        # Existing project/folder IAM grants may be inherited. We verify
        # ONLY direct service policy and never claim inherited IAM is clear.
        pol=direct_policy(token)
        require(not pol.get("bindings",[]),"UNEXPECTED_DIRECT_SERVICE_IAM_BINDINGS")
        require(isinstance(pol.get("etag"),str) and bool(pol.get("etag")),
                "SERVICE_POLICY_ETAG_MISSING")
        print("H2W_STAGE=ONE_OWNER_ONLY_NEW_SERVICE_INVOKER_POLICY",flush=True)
        policy_attempted=True
        st,new_policy=api("POST",SETPOLICY,token,{
            "policy":{"etag":pol["etag"],"version":1,
                      "bindings":[{"role":"roles/run.invoker",
                                   "members":["user:"+OWNER]}]}})
        require(st==200 and exact_owner_only(new_policy),
                "OWNER_ONLY_DIRECT_POLICY_RESPONSE_MISMATCH")
        require(exact_owner_only(direct_policy(token)),
                "OWNER_ONLY_DIRECT_POLICY_READBACK_MISMATCH")
        invoker="EXACT_OWNER_ONLY_DIRECT_BINDING_VERIFIED"
        st,service=api("GET",SURL,token)
        require(st==200,"FINAL_SERVICE_READBACK_HTTP_"+str(st))
        inspect_service(service,session,uid)
        require(service.get("etag"),"FINAL_ETAG_UNKNOWN")
        etag=service["etag"]
        append_marker("SERVICE_POST_IAM_ETAG="+etag)
        # No direct HTTP probes: internal-only ingress intentionally blocks
        # owner requests coming from public WSL desktop network.
        result="PASS_NEW_INTERNAL_OFF_SERVICE_AND_OWNER_DIRECT_INVOKER_WITH_LIMITS"
        reason="ONE_SERVICE_CREATED_NO_HTTP_PROBES"
    except (Stop,OSError,ValueError,TypeError,UnicodeError,KeyboardInterrupt) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        # IMPORTANT: Never auto-delete on ambiguous partial create/readback.
        # Retain only this new service; UID/etag/session are rollback guards.
        try:
            with (evidence/"sanitized-result.json").open("x",encoding="utf-8") as fd:
                json.dump({"service":SNAME,"sa":SA,"sa_uid":SA_UID,
                           "image":IMAGE,"uid":uid,"etag":etag,
                           "session":session,"ingress":"INGRESS_TRAFFIC_INTERNAL_ONLY",
                           "create_attempted":create_attempted,
                           "iam_policy_attempted":policy_attempted,
                           "direct_owner_invoker":invoker,
                           "result":result,"reason":reason,
                           "cloudrun_http_probes":"NOT_ATTEMPTED_INTERNAL_ONLY",
                           "service_rollback":"UID_ETAG_GUARDED_NOT_EXECUTED",
                           "production":"NO_GO"},fd,indent=2,sort_keys=True)
                fd.write("\n")
            append_marker("RESULT="+result)
            append_marker("REASON="+reason)
        except OSError:
            result="STOP_LOCAL_EVIDENCE_WRITE_FAILED"
        print("H2W_SERVICE_NAME="+SNAME)
        print("H2W_SERVICE_UID="+(uid or "UNKNOWN"))
        print("H2W_GATEWAY_SA_UID="+SA_UID)
        print("H2W_IMMUTABLE_IMAGE="+IMAGE)
        print("H2W_CREATE_ATTEMPTED="+str(create_attempted).upper())
        print("H2W_IAM_WRITE_ATTEMPTED="+str(policy_attempted).upper())
        print("H2W_OWNER_INVOKER="+invoker)
        print("H2W_INGRESS=INTERNAL_ONLY")
        print("H2W_HTTP_PROBES=NOT_ATTEMPTED_INTERNAL_ONLY")
        print("H2W_SERVICE_ROLLBACK=NOT_EXECUTED_UID_ETAG_GUARD_REQUIRED")
        print("H2W_OTHER_CLOUD_RUN_SA_REGISTRY_WRITES=NONE")
        print("H2W_KMS_FIRESTORE_WRITES=NONE")
        print("H2W_H2_PRODUCTION=NO_GO")
        print("H2W_RESULT="+result)
        print("H2W_REASON="+reason)
        print("H2W_EVIDENCE="+str(evidence))
        print("H2W_DO_NOT_REPEAT=TRUE")
    return 0 if result=="PASS_NEW_INTERNAL_OFF_SERVICE_AND_OWNER_DIRECT_INVOKER_WITH_LIMITS" else 2

if __name__=="__main__":
    sys.exit(main())
