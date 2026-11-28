#!/usr/bin/env python3
"""Future owner-approved H2AM only. Default OFF; never imports/reruns H2AK."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import sys
import time
from pathlib import Path
from step05_h2am_acceptance_support import (
    Stop,Result,Store,Session,Commands,atomic_json,exclusive_json,read_private,
    scan_report,sha256,sanitized,digest,not_found,classify_oom)

PREFIX="asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
PINS={
 "mediator":("oldx-c2-mediator-h2ah","01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe","oldx-c2-web-mediator","100779414920484819274"),
 "gateway":("oldx-c2-gateway-h2ah","921fbf4ff71b918c479e4a786868368640a494c16da08e54192f25e14dc1ec4d","oldx-c2-private-gateway","107238619872767759560"),
 "backend":("oldx-c2-backend-h2ah","01ae540aa88ad0e3a6888994dd41b6b02b9d934a7a1d2e455f44b194f033b941","oldx-c2-product-backend","106984791114720194680"),
 "reader":("oldx-c2-kms-reader","822e2592b1010bfa94a1fe5bc75003712485abae0369f5252ece3863723eb077","oldx-c2-kms-reader","107336955065718475994"),
}
REFS={r:PREFIX+p[0]+"@sha256:"+p[1] for r,p in PINS.items()}
ROOT=Path("/root")
H2AJ=ROOT/".oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128"
H2AK=ROOT/".oldx-step05-h2ak-four-pinned-image-acceptance-once-20261128"
HISTORIC_RAW_SHA256="e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92"
HISTORIC=ROOT/"oldx-h2ak-images-20261128T160610Z-42e006/mediator-grype.json"
MARKER=ROOT/".oldx-step05-h2am-selective-off-runtime-three-scans-once-20261128"
GLOBAL=ROOT/".oldx-step05-h2am-image-evidence-20261128"
PROPOSAL_BLOB="c1cfcfa2f224e9a47dd6e896730c73e927b9b483"
SCOPE="oldx.h2am.mediator-runtime-only.three-new-scans.v1"
def plan_digest():return sha256(json.dumps({"scope":SCOPE,"refs":REFS},sort_keys=True).encode())
def fail(condition,code):
    if not condition:raise Stop(code)
def proposal_check(raw):
    blob=hashlib.sha1(("blob "+str(len(raw))+"\0").encode()+raw).hexdigest()
    fail(blob==PROPOSAL_BLOB,"FROZEN_PROPOSAL_BLOB_DRIFT")
    value=json.loads(raw)
    fail(value.get("imageBuildSourceRevision")=="f567aa6ccef7a71b6032dc1bdb9f2bcf0a8587d4","BUILD_SOURCE_DRIFT")
    fail(set(value.get("roles",{}))==set(PINS),"ROLE_SET_DRIFT")
    for role,p in PINS.items():
        r=value["roles"][role]
        fail(r.get("image")==REFS[role] and r.get("serviceAccount")==p[2]+"@oldx-staging.iam.gserviceaccount.com" and
             r.get("serviceAccountUid")==p[3] and r.get("enabled") is False,"IMAGE_OR_SA_DRIFT")
    return value
def prerequisites(root=ROOT,h2aj=H2AJ,h2ak=H2AK,historic=HISTORIC):
    a=read_private(h2aj,32768).decode().splitlines();k=read_private(h2ak,32768).decode().splitlines()
    fail("RESULT=PASS_FOUR_NEW_PRIVATE_OFF_IMAGES" in a,"H2AJ_SUCCESS_REQUIRED")
    for role,p in PINS.items():
        rows=[x for x in a if x.startswith("ROLE="+role+" REGISTRY_INDEX=")]
        fail(len(rows)==1 and re.fullmatch(r"ROLE="+role+r" REGISTRY_INDEX=sha256:[a-f0-9]{64} AMD64_CHILD=sha256:"+p[1],rows[0]),
             "H2AJ_ROLE_DIGEST_DRIFT")
    fail("RESULT=STOP_PARTIAL_LOCAL_READ_ONLY_ACCEPTANCE" in k and
         "ROLE=mediator ABOUT_TO_CHECK" in k and
         not any(x.startswith("ROLE="+r+" ") for x in k for r in ("gateway","backend","reader")),
         "H2AK_CONSUMED_MEDIATOR_ONLY_FAILURE_REQUIRED")
    raw=read_private(historic)
    fail(sha256(raw)==HISTORIC_RAW_SHA256,"HISTORICAL_RAW_CHECKSUM_DRIFT_NO_RESCAN")
    imported=scan_report(raw,REFS["mediator"],historical=True)
    for role in ("gateway","backend","reader"):
        fail(not (Path(historic).parent/(role+"-grype.json")).exists(),"H2AL_OTHER_SCAN_STATE_CHANGED")
    return raw,imported

# One minimal exec process, explicit ESM, bounded startup wait inside that SAME
# process. No repeated docker exec, host port, shell, HTTP body/config dump.
PROBE=r"""
import {setTimeout as wait} from 'node:timers/promises';
const role=process.argv[2],end=Date.now()+10000;
let health,status,error='NOT_READY';
while(Date.now()<end){
 try{
  const r=await fetch('http://127.0.0.1:8080/healthz',{signal:AbortSignal.timeout(800)});
  status=r.status;const reader=r.body.getReader(),parts=[];let size=0;
  try{for(;;){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;
   if(size>2048)throw Error('HEALTH_BODY_LIMIT');parts.push(Buffer.from(value));}}
  finally{await reader.cancel().catch(()=>{});}
  health=JSON.parse(Buffer.concat(parts).toString('utf8'));
  if(status!==200||health.ok!==true||health.role!==role||health.state!=='OFF'||health.productReady!==false){
   error='HEALTH_CONTRACT';break;
  }
  error=null;break;
 }catch{error='LOOPBACK_STARTUP_NOT_READY';await wait(150);}
}
let product;
if(error===null){
 try{const r=await fetch('http://127.0.0.1:8080/api/staging/marketplace/save',
  {method:'POST',body:'{}',signal:AbortSignal.timeout(1500)});
 product=r.status;await r.body?.cancel();if(product!==503)error='PRODUCT_NOT_OFF';
 }catch{error='PRODUCT_UNKNOWN';}
}
const result={health:status??null,product:product??null,state:health?.state==='OFF'?'OFF':'UNKNOWN',
 role,uid:process.getuid(),nodeMajor:Number(process.versions.node.split('.')[0]),error};
process.stdout.write(JSON.stringify(result));
if(error!==null||result.uid!==65532||result.nodeMajor!==24)process.exitCode=17;
"""
STATE_FORMAT="{{json .}}"
def image_info(result,role):
    result.need("IMAGE_INSPECT")
    rows=json.loads(result.stdout)
    fail(isinstance(rows,list) and len(rows)==1,"LOCAL_IMAGE_INSPECT_SCHEMA")
    x=rows[0];c=x.get("Config",{})
    fail(digest(x.get("Id")) and REFS[role] in x.get("RepoDigests",[]),"LOCAL_IMAGE_DIGEST_NOT_BOUND")
    fail(x.get("Os")=="linux" and x.get("Architecture")=="amd64","LOCAL_IMAGE_ARCH_DRIFT")
    fail(c.get("User")=="65532:65532" and c.get("WorkingDir")=="/app" and
         c.get("Entrypoint")==["/nodejs/bin/node"] and
         c.get("Cmd")==["functions/staging-marketplace/four-role/"+role+".mjs"],"LOCAL_ENTRYPOINT_DRIFT")
    fail(not any(v.startswith("OLDX_") and v.endswith("=true") for v in c.get("Env",[])),"LOCAL_IMAGE_ENABLED")
    return x["Id"]
def state_info(result,name,image_id,attempt,role):
    if result.code!=0:
        if not_found(result):return None
        raise Stop("CONTAINER_STATE_UNKNOWN",result.error("CONTAINER_INSPECT"))
    rows=json.loads(result.stdout)
    fail(isinstance(rows,list) and len(rows)==1,"CONTAINER_STATE_SCHEMA")
    x=rows[0];labels=x.get("Config",{}).get("Labels",{})
    fail(x.get("Name")=="/"+name and x.get("Image")==image_id and
         labels.get("oldx.h2am.attempt")==attempt and labels.get("oldx.h2am.role")==role,
         "CONTAINER_OWNERSHIP_DRIFT_NO_CLEANUP")
    return x

class Acceptance:
    def __init__(self,store,session,commands,global_dir,*,allow_missing_pulls=False):
        self.store=store;self.session=session;self.commands=commands;self.global_dir=Path(global_dir)
        self.allow_missing_pulls=allow_missing_pulls
    def claim_path(self,role,stage):return self.global_dir/(PINS[role][1]+"-"+stage+".json")
    def claim(self,role,stage):
        exclusive_json(self.claim_path(role,stage),{"scope":SCOPE,"role":role,"ref":REFS[role],
            "stage":stage,"status":"ATTEMPTED","evidence":str(self.store.path),"attempt":self.session.attempt})
    def save_stage(self,role,stage,receipt):
        receipt={**receipt,"role":role,"ref":REFS[role],"scope":SCOPE}
        self.store.put(role+"-"+stage+".json",receipt)
        atomic_json(self.claim_path(role,stage),{**receipt,"evidence":str(self.store.path),"attempt":self.session.attempt})
        return receipt
    def previous(self,role,stage):
        p=self.claim_path(role,stage)
        if not p.exists():return None
        value=json.loads(read_private(p))
        fail(value.get("scope")==SCOPE and value.get("ref")==REFS[role] and value.get("role")==role,
             "GLOBAL_RECEIPT_SCOPE_DRIFT")
        fail(value.get("status")=="COMPLETE","PRIOR_ATTEMPT_UNKNOWN_OWNER_RECONCILIATION_REQUIRED")
        if stage=="scan":
            raw=read_private(Path(value["evidence"])/value["rawFile"])
            fail(sha256(raw)==value.get("rawSha256"),"COMPLETED_SCAN_FILE_CHANGED_NO_RESCAN")
        if stage=="runtime":
            fail(value.get("cleanup",{}).get("status")=="REMOVED" and value.get("shutdown",{}).get("exitCode")==0,
                 "PRIOR_RUNTIME_CLEANUP_UNKNOWN")
        self.store.put(role+"-"+stage+".json",{**value,"reused":True})
        return value
    def local_image(self,role):
        result=self.commands.call(["docker","image","inspect",REFS[role]])
        if result.code!=0 and re.search(r"No such image",result.stderr,re.I):
            fail(self.allow_missing_pulls,"LOCAL_IMAGE_ABSENT_PULL_NOT_APPROVED")
            self.commands.call(["docker","pull","--platform","linux/amd64",REFS[role]],timeout=600).need("ONE_EXACT_PULL")
            result=self.commands.call(["docker","image","inspect",REFS[role]])
        image_id=image_info(result,role)
        self.store.put(role+"-image.json",{"ref":REFS[role],"imageId":image_id,"os":"linux","architecture":"amd64",
            "user":"65532:65532","sourceRevision":"f567aa6ccef7a71b6032dc1bdb9f2bcf0a8587d4",
            "serviceAccountPin":PINS[role][2]+"@oldx-staging.iam.gserviceaccount.com",
            "serviceAccountUidPin":PINS[role][3],"actualCloudIdentity":"NOT_CHECKED_OR_ATTACHED"})
        return image_id
    def scan(self,role,image_id):
        fail(role in ("gateway","backend","reader"),"MEDIATOR_RESCAN_FORBIDDEN")
        prior=self.previous(role,"scan")
        if prior:
            fail(prior["imageId"]==image_id,"SCAN_LOCAL_IMAGE_ID_DRIFT")
            return prior
        self.claim(role,"scan")
        self.store.put(role+"-scan.json",{"status":"ATTEMPTED","role":role,"ref":REFS[role],"imageId":image_id})
        path=self.store.path/(role+"-grype.json")
        result=self.commands.call(["grype","docker:"+image_id,"--output","json","--config",str(self.store.path/"grype-config.json")],
            timeout=1000,stdout_file=path)
        # Raw file exists even on partial failure; completed receipt NEVER waits
        # for runtime or cleanup. A failed attempt is NOT automatically scanned again.
        result.need("GRYPE_"+role.upper())
        raw=read_private(path)
        receipt=scan_report(raw,REFS[role],image_id=image_id)
        return self.save_stage(role,"scan",{**receipt,"rawFile":path.name})
    def runtime(self,role,image_id):
        prior=self.previous(role,"runtime")
        if prior:
            fail(prior.get("imageId")==image_id,"RUNTIME_LOCAL_IMAGE_DRIFT");return prior
        self.claim(role,"runtime")
        name="oldx-h2am-"+role+"-"+self.session.attempt[:16]
        receipt={"status":"ATTEMPTED","name":name,"imageId":image_id,"primaryFailure":None,
                 "cleanup":{"status":"NOT_ATTEMPTED"},"diagnostics":[]}
        self.store.put(role+"-runtime.json",receipt)
        state=None;owned=False;persisted=True;diagnostics_complete=False
        def command(args,stage,timeout=30,**kwargs):
            return self.commands.call(args,timeout=timeout,**kwargs).need(stage)
        def inspect():
            result=self.commands.call(["docker","inspect",name])
            return state_info(result,name,image_id,self.session.attempt,role)
        try:
            cid=command(["docker","run","--detach","--pull=never","--name",name,
                "--label","oldx.h2am.attempt="+self.session.attempt,"--label","oldx.h2am.role="+role,
                "--network","none","--read-only","--cap-drop","ALL","--security-opt","no-new-privileges",
                "--pids-limit","128","--memory","768m","--memory-swap","768m","--cpus","1",
                "--user","65532:65532","-e","OLDX_H2AH_ENABLED=false",image_id],"CONTAINER_START",70).strip()
            fail(re.fullmatch(r"[a-f0-9]{64}",cid) is not None,"CONTAINER_ID_UNKNOWN")
            receipt["containerId"]=cid
            state=inspect();fail(state is not None,"CONTAINER_VANISHED")
            owned=True
            fail(state.get("Id")==cid,"CONTAINER_ID_DRIFT")
            h=state.get("HostConfig",{})
            fail(h.get("NetworkMode")=="none" and h.get("ReadonlyRootfs") is True and
                 not h.get("PortBindings") and not h.get("Binds") and not state.get("Mounts") and
                 h.get("Memory")==768*1024*1024 and h.get("NanoCpus")==1_000_000_000 and
                 h.get("PidsLimit")==128 and "ALL" in h.get("CapDrop",[]) and
                 any(x in ("no-new-privileges","no-new-privileges:true") for x in h.get("SecurityOpt",[])),"CONTAINER_ISOLATION_DRIFT")
            fail(state.get("State",{}).get("Running") is True,"MAIN_EXIT_BEFORE_PROBE")
            raw=command(["docker","exec","-i",cid,"/nodejs/bin/node","--input-type=module","-",role],
                "OFF_PROBE",18,input_bytes=PROBE.encode())
            probe=json.loads(raw)
            fail(probe=={"health":200,"product":503,"state":"OFF","role":role,"uid":65532,"nodeMajor":24,"error":None},
                 "OFF_HTTP_CONTRACT_FAILED")
            receipt["probe"]=probe
        except Exception as error:
            receipt["primaryFailure"]={"code":error.code,"detail":error.detail} if isinstance(error,Stop) else {
                "code":"RUNTIME_EXCEPTION","type":type(error).__name__}
            # MUST be durable before diagnostics/stop/rm can fail.
            try:self.store.put(role+"-runtime.json",receipt)
            except OSError:
                persisted=False;receipt["persistenceError"]="PRIMARY_RECEIPT_WRITE_FAILED_RETAIN_CONTAINER"
        finally:
            try:
                state=inspect()
                if state is not None:owned=True
                if state is not None:
                    s=state.get("State",{})
                    receipt["state"]={k:sanitized(s[k],400) if k=="Error" else s.get(k)
                        for k in ("ExitCode","OOMKilled","Error","Running","Pid")}
                    receipt["oomEvidence"]=classify_oom(s)
                    logs=self.commands.call(["docker","logs","--tail","100",name],timeout=15)
                    receipt["logs"]={"exitCode":logs.code,"stdout":sanitized(logs.stdout),"stderr":sanitized(logs.stderr),
                        "timedOut":logs.timed_out,"truncated":logs.truncated}
                    diagnostics_complete=logs.code==0 and not logs.timed_out and not logs.truncated
                else:
                    receipt["state"]={"status":"CONFIRMED_ABSENT"}
                    receipt["oomEvidence"]="UNKNOWN"
                self.store.put(role+"-runtime.json",receipt)
            except Exception as error:
                state=None;owned=False
                receipt["diagnostics"].append({"stage":"INSPECT_LOGS","code":getattr(error,"code",type(error).__name__)})
            if not persisted:
                receipt["cleanup"]={"status":"UNKNOWN","noRetry":True,"reason":"EVIDENCE_NOT_DURABLE_CONTAINER_RETAINED"}
            elif state is None:
                receipt["cleanup"]={"status":"ABSENT" if receipt.get("state",{}).get("status")=="CONFIRMED_ABSENT" else "UNKNOWN",
                    "noRetry":True}
            elif owned and not diagnostics_complete:
                receipt["cleanup"]={"status":"UNKNOWN","noRetry":True,"reason":"DIAGNOSTICS_INCOMPLETE_CONTAINER_RETAINED"}
            elif owned:
                try:
                    if state.get("State",{}).get("Running") is True:
                        stop=self.commands.call(["docker","stop","--time","3",name],timeout=15)
                        stop.need("CLEANUP_STOP")
                        state=inspect();fail(state is not None,"CONTAINER_DISAPPEARED_DURING_CLEANUP")
                    fail(state.get("State",{}).get("Running") is False,"CLEANUP_RUNNING_STATE_UNKNOWN")
                    final=state["State"]
                    receipt["shutdown"]={"exitCode":final.get("ExitCode"),"oomEvidence":classify_oom(final)}
                    self.commands.call(["docker","rm",name],timeout=15).need("CLEANUP_RM")
                    receipt["cleanup"]={"status":"REMOVED","stopAtMostOnce":True,"rmAtMostOnce":True}
                except Exception as error:
                    receipt["cleanup"]={"status":"UNKNOWN","noRetry":True,"code":getattr(error,"code",type(error).__name__),
                        "detail":getattr(error,"detail",{})}
            if receipt["primaryFailure"] is None and (receipt["cleanup"]["status"]!="REMOVED" or
                receipt.get("shutdown",{}).get("exitCode")!=0):
                receipt["primaryFailure"]={"code":"CLEANUP_OR_SHUTDOWN_UNKNOWN","detail":{}}
            if receipt["primaryFailure"] is None and (receipt.get("oomEvidence")!="DOCKER_STATE_FALSE" or
                receipt.get("shutdown",{}).get("oomEvidence")!="DOCKER_STATE_FALSE"):
                receipt["primaryFailure"]={"code":"OOM_STATE_TRUE_OR_UNKNOWN","detail":{}}
            receipt["status"]="COMPLETE" if receipt["primaryFailure"] is None else "FAILED"
            try:self.save_stage(role,"runtime",receipt)
            except OSError:
                receipt["persistenceError"]="FINAL_RECEIPT_WRITE_FAILED"
                if receipt["primaryFailure"] is None:receipt["primaryFailure"]={"code":"RECEIPT_WRITE_FAILED","detail":{}}
                receipt["status"]="FAILED"
        if receipt["status"]!="COMPLETE":raise Stop("RUNTIME_STOP",{"role":role,"primaryFailure":receipt["primaryFailure"],
            "cleanup":receipt["cleanup"]})
        return receipt
    def import_historic(self,historic_raw,historic):
        path=self.store.path/"mediator-historic-grype.json"
        if not self.previous("mediator","scan"):
            with open(path,"xb") as f:os.chmod(path,0o600);f.write(historic_raw);f.flush();os.fsync(f.fileno())
            self.save_stage("mediator","scan",{**historic,"rawFile":path.name})
    def run(self,historic_raw,historic):
        summary={"scope":SCOPE,"planDigest":plan_digest(),"roles":{},"outcome":"PARTIAL_UNKNOWN","mediatorRescanForbidden":True}
        try:
            # Import original bytes/counts, never invoke Mediator Grype.
            self.import_historic(historic_raw,historic)
            for role in PINS:
                old_scan=self.previous(role,"scan");old_runtime=self.previous(role,"runtime")
                if old_scan and old_runtime:
                    summary["roles"][role]={"scan":"COMPLETE_REUSED","runtime":"COMPLETE_REUSED"}
                    self.store.put("summary.json",summary);continue
                summary["roles"][role]={"stage":"IMAGE_BINDING"};self.store.put("summary.json",summary)
                image_id=self.local_image(role)
                if role=="mediator":
                    fail(image_id==historic["imageId"],"MEDIATOR_HISTORIC_LOCAL_CONFIG_MISMATCH")
                    summary["roles"][role]["scan"]="IMPORTED_HISTORICAL_57_NO_RESCAN"
                else:
                    summary["roles"][role]["stage"]="SCAN";self.store.put("summary.json",summary)
                    self.scan(role,image_id);summary["roles"][role]["scan"]="COMPLETE"
                summary["roles"][role]["stage"]="RUNTIME";self.store.put("summary.json",summary)
                self.runtime(role,image_id);summary["roles"][role]["runtime"]="COMPLETE"
            summary["outcome"]="COMPLETE_OFF_EVIDENCE_SECURITY_REVIEW_REQUIRED"
        except Exception as error:
            summary["outcome"]="STOP_PARTIAL_NO_AUTOMATIC_RETRY"
            summary["failure"]={"code":getattr(error,"code",type(error).__name__),"detail":getattr(error,"detail",{})}
        finally:self.store.put("summary.json",summary)
        return summary


def inspect_resume(evidence,global_dir=GLOBAL):
    """Offline plan only. Failed/ambiguous attempts cannot be replayed."""
    raw=read_private(Path(evidence)/"summary.json");summary=json.loads(raw)
    fail(summary.get("scope")==SCOPE and summary.get("planDigest")==plan_digest(),"RESUME_SCOPE_DRIFT")
    tasks=[];blocked=[]
    for role in PINS:
        for stage in ("scan","runtime"):
            path=Path(global_dir)/(PINS[role][1]+"-"+stage+".json")
            if not path.exists():
                if role=="mediator" and stage=="scan":raise Stop("HISTORICAL_IMPORT_MISSING")
                tasks.append({"role":role,"stage":stage});continue
            value=json.loads(read_private(path))
            fail(value.get("scope")==SCOPE and value.get("ref")==REFS[role],"RESUME_PIN_DRIFT")
            if value.get("status")!="COMPLETE":
                blocked.append({"role":role,"stage":stage,"reason":"ATTEMPT_ALREADY_CONSUMED_UNKNOWN"})
            elif stage=="scan":
                raw_scan=read_private(Path(value["evidence"])/value["rawFile"])
                fail(sha256(raw_scan)==value.get("rawSha256"),"RESUME_COMPLETED_SCAN_CHANGED")
            elif value.get("cleanup",{}).get("status")!="REMOVED":
                blocked.append({"role":role,"stage":stage,"reason":"CLEANUP_RECONCILIATION_REQUIRED"})
    return {"summarySha256":sha256(raw),"scope":SCOPE,"unattemptedOnly":tasks,"blocked":blocked,
            "status":"BLOCKED_NO_EXECUTION" if blocked else "FRESH_OWNER_APPROVAL_REQUIRED"}

def cli(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-h2am-once",action="store_true")
    parser.add_argument("--owner-approved-selective-off-only",action="store_true")
    parser.add_argument("--inspect-resume")
    parser.add_argument("--resume-from")
    parser.add_argument("--resume-summary-sha256")
    parser.add_argument("--owner-approved-unattempted-resume",action="store_true")
    parser.add_argument("--allow-missing-exact-pulls",action="store_true")
    parser.add_argument("--private-docker-config")
    parser.add_argument("--grype-db-cache",default="/root/.cache/grype/db")
    args=parser.parse_args(argv)
    if args.inspect_resume:
        fail(not args.execute_h2am_once,"PLAN_IS_READ_ONLY")
        print(json.dumps(inspect_resume(args.inspect_resume),sort_keys=True));return 0
    if not args.execute_h2am_once or not args.owner_approved_selective_off_only:
        print("H2AM=OFF_NEW_OWNER_APPROVAL_REQUIRED_NO_EXTERNAL_OPERATIONS");return 0
    # Everything until Session.consume is FILESYSTEM ONLY.
    fail(os.name=="posix" and os.geteuid()==0,"OWNER_LINUX_ROOT_REQUIRED")
    os.umask(0o077)
    proposal_path=Path(__file__).resolve().parents[1]/"deployment/four-role/h2aj-four-immutable-images-pinned-proposal.json"
    fail(not proposal_path.is_symlink(),"PROPOSAL_SYMLINK")
    proposal_check(proposal_path.read_bytes())
    historic_raw,historic=prerequisites()
    marker=MARKER
    if args.resume_from:
        fail(args.owner_approved_unattempted_resume and MARKER.is_file(),"NEW_RESUME_APPROVAL_REQUIRED")
        resume=inspect_resume(args.resume_from)
        fail(args.resume_summary_sha256==resume["summarySha256"] and not resume["blocked"],"RESUME_BLOCKED_OR_HASH_DRIFT")
        marker=ROOT/(".oldx-step05-h2am-resume-"+resume["summarySha256"]+".once")
    else:fail(not GLOBAL.exists(),"EXISTING_GLOBAL_STATE_REQUIRES_EXPLICIT_RESUME")
    fail(not marker.exists() and not marker.is_symlink(),"H2AM_ALREADY_CONSUMED")
    fail(shutil.disk_usage(ROOT).free>=4*1024**3,"LOCAL_EVIDENCE_DISK_BELOW_4_GIB")
    db=Path(args.grype_db_cache)
    fail(db.is_dir() and not db.is_symlink() and db.stat().st_uid==0,"EXISTING_GRYPE_DB_REQUIRED_NO_DOWNLOAD")
    binaries={}
    for tool in ("docker","grype"):
        value=shutil.which(tool);fail(value is not None,"EXISTING_TOOL_REQUIRED_"+tool.upper())
        executable=Path(value).resolve()
        with executable.open("rb") as f:fail(f.read(4)==b"\x7fELF","NATIVE_LINUX_TOOL_REQUIRED")
        binaries[tool]=str(executable)
    config=None
    if args.allow_missing_exact_pulls:
        fail(args.private_docker_config is not None,"PREEXISTING_PRIVATE_AUTH_REQUIRED")
        config=Path(args.private_docker_config)
        value=json.loads(read_private(config/"config.json",65536))
        fail(not value.get("credsStore") and not value.get("credHelpers") and
             isinstance(value.get("auths"),dict) and set(value["auths"])=={"asia-south1-docker.pkg.dev"} and
             isinstance(value["auths"]["asia-south1-docker.pkg.dev"].get("auth"),str),"NO_AUTH_HELPERS_REFRESH_OR_OTHER_REGISTRIES")
    attempt=secrets.token_hex(16)
    session=Session.consume(marker,attempt,plan_digest())
    evidence=ROOT/("oldx-h2am-selective-"+time.strftime("%Y%m%dT%H%M%SZ",time.gmtime())+"-"+attempt[:8])
    evidence.mkdir(mode=0o700);GLOBAL.mkdir(mode=0o700,exist_ok=True)
    fail(not GLOBAL.is_symlink() and GLOBAL.stat().st_uid==0 and not GLOBAL.stat().st_mode&0o077,"GLOBAL_STATE_PRIVATE_REQUIRED")
    store=Store(evidence)
    store.put("source-hashes.json",{"runnerSha256":sha256(Path(__file__).read_bytes()),
        "supportSha256":sha256(Path(__file__).with_name("step05_h2am_acceptance_support.py").read_bytes()),
        "proposalBlob":PROPOSAL_BLOB,"scope":SCOPE,"historicalRawSha256":historic["rawSha256"]})
    if config is None:
        config=evidence/"empty-docker-config";config.mkdir(mode=0o700);atomic_json(config/"config.json",{"auths":{}})
    home=evidence/"empty-home";home.mkdir(mode=0o700)
    env={"PATH":os.environ.get("PATH","/usr/bin:/bin"),"LANG":"C.UTF-8","HOME":str(home),
         "DOCKER_HOST":"unix:///var/run/docker.sock","DOCKER_CONFIG":str(config),"DOCKER_DEFAULT_PLATFORM":"linux/amd64",
         "GRYPE_CHECK_FOR_APP_UPDATE":"false","GRYPE_DB_AUTO_UPDATE":"false","GRYPE_DB_CACHE_DIR":str(db),
         "SYFT_CHECK_FOR_APP_UPDATE":"false"}
    atomic_json(evidence/"grype-config.json",{"check-for-app-update":False,"db":{"auto-update":False,"cache-dir":str(db)}})
    commands=Commands(session,store,env,binaries=binaries)
    acceptance=Acceptance(store,session,commands,GLOBAL,allow_missing_pulls=args.allow_missing_exact_pulls)
    # Offline historical import is durable BEFORE even Docker info may fail.
    acceptance.import_historic(historic_raw,historic)
    try:
        fail(commands.call(["docker","info","--format","{{.OSType}}"]).need("LOCAL_ENGINE").strip()=="linux",
             "LOCAL_ENGINE_NOT_LINUX")
        outcome=acceptance.run(historic_raw,historic)
    except Exception as error:
        outcome={"scope":SCOPE,"planDigest":plan_digest(),"outcome":"STOP_PARTIAL_NO_AUTOMATIC_RETRY",
            "failure":{"code":getattr(error,"code",type(error).__name__),"detail":getattr(error,"detail",{})}}
        store.put("summary.json",outcome)
    print("H2AM_OUTCOME="+outcome["outcome"])
    print("H2AM_SUMMARY_SHA256="+sha256(read_private(evidence/"summary.json")))
    print("H2AM_PRIVATE_EVIDENCE="+str(evidence))
    print("H2AM_MEDIATOR_SCAN=IMPORTED_NOT_RESCANNED")
    print("H2AM_CLOUD_KMS_FIREBASE_DEPLOYMENT=NONE_PRODUCTION_NO_GO")
    return 0 if outcome["outcome"]=="COMPLETE_OFF_EVIDENCE_SECURITY_REVIEW_REQUIRED" else 2

if __name__=="__main__":
    try:sys.exit(cli())
    except Exception as error:
        print("H2AM_STOP="+sanitized(getattr(error,"code",type(error).__name__),200));sys.exit(2)
