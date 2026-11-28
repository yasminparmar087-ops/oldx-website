#!/usr/bin/env python3
"""H2AK READ-ONLY registry acceptance for exactly four H2AJ images.

No build/push/deploy, IAM, KMS, Firebase or production access.
New-image vulnerability scans + nonroot, OFF-only localhost runtime smoke.
One attempt per image; never replay a completed image check automatically.
Private receipts stay under /root; no tokens written to logs/GitHub.
"""
from __future__ import annotations

import json
import os
import re
import secrets
import shutil
import ssl
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path("/root")
PROJECT="oldx-staging"
OWNER="yasminparmar087@gmail.com"
REGISTRY="asia-south1-docker.pkg.dev"
PREFIX=REGISTRY+"/"+PROJECT+"/oldx-staging-images/"
IMAGES={
 "mediator":("oldx-c2-mediator-h2ah","01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe"),
 "gateway":("oldx-c2-gateway-h2ah","921fbf4ff71b918c479e4a786868368640a494c16da08e54192f25e14dc1ec4d"),
 "backend":("oldx-c2-backend-h2ah","01ae540aa88ad0e3a6888994dd41b6b02b9d934a7a1d2e455f44b194f033b941"),
 "reader":("oldx-c2-kms-reader","822e2592b1010bfa94a1fe5bc75003712485abae0369f5252ece3863723eb077"),
}
SDK=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
GCLOUD=SDK/"bin/gcloud"
PY=SDK/"platform/bundledpythonunix/bin/python3"
CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
H2AJ_MARKER=ROOT/".oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128"
MARK=ROOT/".oldx-step05-h2ak-four-pinned-image-acceptance-once-20261128"
FLAG="--h2ak-four-h2aj-images-scan-offhealth-local-only-once"
EXPECTED_BLOB="H2AJ_RESULT=PASS_FOUR_NEW_PRIVATE_OFF_IMAGES"
class Stop(Exception):pass
def need(ok,code):
 if not ok:raise Stop(code)
def run(args,*,env=None,timeout=35,input_bytes=None):
 try:
  p=subprocess.run(args,input=input_bytes,stdout=subprocess.PIPE,
   stderr=subprocess.PIPE,stdin=None if input_bytes is not None else subprocess.DEVNULL,
   timeout=timeout,env=env,check=False)
 except subprocess.TimeoutExpired:raise Stop("TIMEOUT_UNKNOWN_NO_AUTO_RETRY") from None
 except OSError:raise Stop("BINARY_UNAVAILABLE") from None
 need(p.returncode==0,"COMMAND_NONZERO_"+str(args[0]))
 need(len(p.stdout)<=10_000_000,"OUTPUT_TOO_LARGE")
 return p.stdout.decode("utf-8","strict").strip()
def preflight():
 need(os.geteuid()==0 and sys.argv[1:]==[FLAG],"ROOT_EXACT_FLAG_REQUIRED")
 need(not MARK.exists() and not MARK.is_symlink(),"H2AK_ALREADY_CONSUMED")
 need(H2AJ_MARKER.is_file() and not H2AJ_MARKER.is_symlink()
      and H2AJ_MARKER.stat().st_uid==0,"H2AJ_SUCCESS_MARKER_NOT_FOUND")
 marker=H2AJ_MARKER.read_text()
 need(EXPECTED_BLOB in marker,"H2AJ_SUCCESS_NOT_RECORDED")
 need(all("ROLE="+role+" REGISTRY_INDEX=" in marker for role in IMAGES),
      "H2AJ_FOUR_ROLE_EVIDENCE_MISSING")
 for role,(_,d) in IMAGES.items():
  need((" AMD64_CHILD=sha256:"+d) in marker,"H2AJ_DIGEST_NOT_MATCHING")
 for program in ("docker","grype","git"):
  need(shutil.which(program) is not None,"MISSING_LINUX_"+program.upper())
 need(SDK.is_dir() and GCLOUD.is_file() and PY.resolve().is_file()
   and CONFIG.is_dir(),"ISOLATED_NATIVE_SDK_MISSING")
 env=dict(os.environ)
 env.update({"CLOUDSDK_CONFIG":str(CONFIG),"CLOUDSDK_PYTHON":str(PY),
  "CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
  "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1",
  "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false","HOME":str(ROOT),
  "GRYPE_CHECK_FOR_APP_UPDATE":"false","GRYPE_DB_AUTO_UPDATE":"true"})
 env.pop("GOOGLE_APPLICATION_CREDENTIALS",None)
 env.pop("CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE",None)
 def gcloud(args):
  return run([str(GCLOUD),"--quiet",*args],env=env,timeout=45)
 need(gcloud(["auth","list","--filter=status:ACTIVE","--format=value(account)"])==OWNER,
      "WRONG_OWNER_ACCOUNT")
 need(gcloud(["config","get-value","project"])==PROJECT,"WRONG_PROJECT")
 need(run(["docker","info","--format","{{.OSType}}"],env=env)=="linux",
      "DOCKER_ENGINE_NOT_LINUX")
 need(shutil.disk_usage(ROOT).free>=4*1024**3,"LESS_THAN_FOUR_GIB_FREE")
 version=run(["grype","version"],env=env,timeout=15)
 need("Version" in version or "version" in version or "grype" in version.lower(),
      "GRYPE_VERSION_UNRECOGNIZED")
 return env,gcloud,version[:200]
def inspect_off_image(ref,env):
 a=json.loads(run(["docker","image","inspect",ref],env=env,timeout=45))
 need(isinstance(a,list) and len(a)==1,"IMAGE_INSPECT_MISSING")
 x=a[0]
 need(x.get("Os")=="linux" and x.get("Architecture")=="amd64",
      "IMAGE_ARCH_DRIFT")
 c=x.get("Config",{})
 need(c.get("User")=="65532:65532","IMAGE_NOT_NONROOT")
 need(c.get("WorkingDir")=="/app" and
      c.get("Entrypoint")==["/nodejs/bin/node"],"IMAGE_RUNTIME_DRIFT")
 need("OLDX_H2AH_ENABLED=true" not in c.get("Env",[]),
      "IMAGE_ENABLED_UNEXPECTED")
 return x.get("Id")
def smoke(ref,role,env):
 # Network completely disabled: Docker exec runs node inside SAME container,
 # checks container loopback without mapping or exposing any host TCP port.
 name="oldx-h2ak-"+role+"-"+secrets.token_hex(3)
 cid=None
 js=("const role=process.argv[1];"
     "const base='http://127.0.0.1:8080';"
     "const ctrl=()=>({signal:AbortSignal.timeout(2000)});"
     "const health=await fetch(base+'/healthz',ctrl());"
     "const body=await health.json();"
     "if(health.status!==200||body.ok!==true||body.role!==role||"
     "body.state!=='OFF'||body.productReady!==false)process.exit(13);"
     "const r=await fetch(base+'/api/staging/marketplace/save',"
     "{method:'POST',body:'{}',...ctrl()});"
     "if(r.status!==503)process.exit(14);"
     "process.stdout.write('OFF_200_503');")
 try:
  cid=run(["docker","run","--detach","--rm","--name",name,
   "--network","none","--read-only","--cap-drop","ALL",
   "--security-opt","no-new-privileges","--pids-limit","64",
   "--memory","512m","--cpus","0.5","--user","65532:65532",
   "-e","OLDX_H2AH_ENABLED=false",ref],env=env,timeout=70)
  need(re.fullmatch(r"[a-f0-9]{64}",cid) is not None,"CONTAINER_ID_INVALID")
  last="UNKNOWN"
  for delay in (0.1,0.2,0.4,0.8,1.2,1.7):
   time.sleep(delay)
   try:
    result=run(["docker","exec",cid,"/nodejs/bin/node","-e",js,role],
      env=env,timeout=9)
    need(result=="OFF_200_503","LOCAL_OFF_RESPONSE_DRIFT")
    return "PASS_ISOLATED_OFF_HEALTH_200_AND_PRODUCT_503"
   except Stop as ex:
    last=str(ex)
    if last=="LOCAL_OFF_RESPONSE_DRIFT":raise
  raise Stop("ISOLATED_LOCAL_OFF_HEALTH_FAILED_"+last)
 finally:
  if cid:
   try:run(["docker","stop","--time","3",cid],env=env,timeout=16)
   except Stop:raise Stop("LOCAL_CONTAINER_CLEANUP_UNKNOWN") from None
def main():
 os.umask(0o077)
 try:
  env,cloud,grype=preflight()
 except (Stop,OSError,ValueError,TypeError) as e:
  print("H2AK_RESULT=STOP_BEFORE_IMAGE_READ")
  print("H2AK_REASON="+str(e));return 2
 stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
 evid=ROOT/("oldx-h2ak-images-"+stamp+"-"+secrets.token_hex(3))
 config=evid/"private-docker-config"
 result={"h2aj":"SUCCESS_CONSUMED_UNTOUCHED","project":PROJECT,"roles":{},
         "grypeVersion":grype,"outcome":"UNKNOWN_OR_PARTIAL"}
 try:
  evid.mkdir(mode=0o700);config.mkdir(mode=0o700)
  docker_env=dict(env,DOCKER_CONFIG=str(config),DOCKER_DEFAULT_PLATFORM="linux/amd64")
  token=cloud(["--account="+OWNER,"--project="+PROJECT,"auth","print-access-token"])
  need(re.fullmatch(r"[A-Za-z0-9._~+\-]{40,4096}",token) is not None,
      "OWNER_ACCESS_TOKEN_INVALID")
  run(["docker","login","--username","oauth2accesstoken","--password-stdin",
      "https://"+REGISTRY],env=docker_env,input_bytes=(token+"\n").encode(),timeout=50)
  token=None
  fd=os.open(str(MARK),os.O_CREAT|os.O_EXCL|os.O_WRONLY|
             getattr(os,"O_NOFOLLOW",0),0o600)
  with os.fdopen(fd,"w") as f:
   f.write("STARTED=TRUE\nH2AJ_MARKER_UNTOUCHED=TRUE\n")
  print("H2AK_MARKER=CONSUMED_NO_REPEAT",flush=True)
  for role,(name,digest) in IMAGES.items():
   ref=PREFIX+name+"@sha256:"+digest
   result["roles"][role]={"ref":ref,"attempted":True}
   with MARK.open("a") as f:f.write("ROLE="+role+" ABOUT_TO_CHECK\n")
   print("H2AK_START="+role,flush=True)
   run(["docker","pull","--platform","linux/amd64",ref],env=docker_env,timeout=540)
   image_id=inspect_off_image(ref,docker_env)
   output=evid/(role+"-grype.json")
   raw=run(["grype","docker:"+ref,"--output","json"],env=docker_env,timeout=1000)
   need(len(raw)>2 and raw[0]=="{","GRYPE_JSON_MISSING")
   output.write_text(raw,encoding="utf-8")
   findings=json.loads(raw)
   matches=findings.get("matches")
   need(isinstance(matches,list),"GRYPE_MATCHES_MISSING")
   sev=Counter(str(x.get("vulnerability",{}).get("severity","Unknown"))
       for x in matches if isinstance(x,dict))
   off=smoke(ref,role,docker_env)
   result["roles"][role].update({"sha256":digest,"imageId":image_id,
       "offHealth":off,"scannerMatches":len(matches),"severity":dict(sev),
       "grypeJsonSaved":output.name})
   with MARK.open("a") as f:f.write("ROLE="+role+" PASS\n")
   print("H2AK_PASS="+role+" OFF_HEALTH NONROOT GRYPE_MATCHES="+str(len(matches))+
     " CRITICAL="+str(sev.get("Critical",0))+" HIGH="+str(sev.get("High",0)),flush=True)
  result["outcome"]="PASS_FOUR_NEW_IMAGE_SECURITY_AND_OFF_RUNTIME_RECEIPTS"
 except (Stop,OSError,ValueError,TypeError,KeyError) as e:
  result["outcome"]="STOP_PARTIAL_LOCAL_READ_ONLY_ACCEPTANCE"
  result["reason"]=str(e) if isinstance(e,Stop) else type(e).__name__
 finally:
  try:
   (evid/"sanitized-h2ak-summary.json").write_text(
     json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
   if MARK.is_file():
    with MARK.open("a") as f:f.write("RESULT="+result["outcome"]+"\n")
  except OSError:
   result["outcome"]="STOP_RECEIPT_SAVE_FAILURE"
  shutil.rmtree(config,ignore_errors=True)
  print("H2AK_RESULT="+result["outcome"])
  print("H2AK_PRIVATE_EVIDENCE="+str(evid))
  print("H2AK_H2AJ_MARKER=UNTOUCHED")
  print("H2AK_CLOUD_RUN_IAM_KMS_FIREBASE_WRITES=NONE")
  print("H2AK_PRODUCTION=NO_GO")
  print("H2AK_DO_NOT_REPEAT=TRUE")
  if result.get("reason"):print("H2AK_REASON="+result["reason"])
 return 0 if result["outcome"].startswith("PASS_") else 2
if __name__=="__main__":sys.exit(main())
