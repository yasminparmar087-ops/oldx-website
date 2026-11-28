#!/usr/bin/env python3
"""H2AO future selective continuation. Default OFF. Never invokes H2AM/H2AN."""
from __future__ import annotations
import argparse,configparser,hashlib,json,os,platform,re,secrets,shutil,sys,time
from pathlib import Path

# Reuse only exact reviewed immutable helpers; importing H2AM does NOT run cli().
FROZEN={"step05_h2am_acceptance_support.py":"b9b57daa9a5b5f0304afc9cfc758630793454c07",
 "step05_h2am_selective_acceptance_once_20261128.py":"3adfb06ca66d6175f089ea797df21ca767779cca"}
for _name,_expected in FROZEN.items():
    _p=Path(__file__).with_name(_name)
    if _p.is_symlink():raise RuntimeError("FROZEN_HELPER_SYMLINK")
    _b=_p.read_bytes()
    if hashlib.sha1(b"blob "+str(len(_b)).encode()+b"\0"+_b).hexdigest()!=_expected:
        raise RuntimeError("FROZEN_REUSE_SOURCE_DRIFT")
import step05_h2am_selective_acceptance_once_20261128 as old
from step05_h2am_acceptance_support import (
 Stop,Store,Session,Commands,read_private,atomic_json,exclusive_json,sha256,digest,sanitized,classify_oom,not_found)
from step05_h2ao_oci_identity import bind,manifest_config,local_contract,object_json

ROOT=Path("/root");PINS=old.PINS;REFS=old.REFS;fail=old.fail
PROBE=old.PROBE
SCOPE="oldx.h2ao.exact-child-config-selective.v1"
MARKER=ROOT/".oldx-step05-h2ao-selective-continuation-once-20261129"
PREFLIGHT_MARKER=ROOT/".oldx-step05-h2ao-local-readonly-preflight-once-20261129"
GET_MARKER=ROOT/".oldx-step05-h2ao-one-mediator-manifest-get-once-20261129"
GLOBAL=ROOT/".oldx-step05-h2ao-image-evidence-20261129"
AM_EVIDENCE=ROOT/"oldx-h2am-selective-20261128T183527Z-2ae92ca2"
AM_GLOBAL=ROOT/".oldx-step05-h2am-image-evidence-20261128"
AN_MARKER=ROOT/".oldx-step05-h2an-three-pinned-preloads-once-20261128"
AM_SUMMARY_SHA="99a455c5bedd435c0f72b0c9aacadcb96d8949db9cb1d2bff518416ca1b18e958f"
OWNER="yasminparmar087@gmail.com";PROJECT="oldx-staging"
OWNER_CONFIG=ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"
GRYPE=ROOT/"oldx-tools/grype-v0.122.1/grype"
DB=ROOT/".cache/grype/db"
def plan_digest():return sha256(json.dumps({"scope":SCOPE,"refs":REFS,"priorSummary":AM_SUMMARY_SHA},sort_keys=True).encode())
def private_dir(path):
    p=Path(path);st=p.stat()
    fail(p.is_dir() and not p.is_symlink() and st.st_uid==os.geteuid() and not st.st_mode&0o077,
         "PRIVATE_DIRECTORY_REQUIRED")
    return p
def history():
    raw,historic=old.prerequisites()
    summary_raw=read_private(AM_EVIDENCE/"summary.json")
    fail(sha256(summary_raw)==AM_SUMMARY_SHA,"PRIOR_H2AM_SUMMARY_SHA_DRIFT")
    summary=object_json(summary_raw);marker=object_json(read_private(old.MARKER))
    fail(summary.get("scope")==old.SCOPE and summary.get("planDigest")==old.plan_digest() and
         summary.get("outcome")=="STOP_PARTIAL_NO_AUTOMATIC_RETRY" and
         summary.get("failure",{}).get("code")=="MEDIATOR_HISTORIC_LOCAL_CONFIG_MISMATCH" and
         summary.get("roles")=={"mediator":{"stage":"IMAGE_BINDING"}},"PRIOR_H2AM_NOT_EXACT_PRE_RUNTIME_FAILURE")
    fail(marker.get("started") is True and marker.get("scope")==old.plan_digest() and
         re.fullmatch(r"[a-f0-9]{32}",marker.get("attempt","")) is not None,"H2AM_CONSUMED_MARKER_INVALID")
    for base in (AM_EVIDENCE,AM_GLOBAL):private_dir(base)
    for role in PINS:
        for stage in ("scan","runtime"):
            file=AM_EVIDENCE/(role+"-"+stage+".json")
            ledger=AM_GLOBAL/(PINS[role][1]+"-"+stage+".json")
            if role=="mediator" and stage=="scan":
                value=object_json(read_private(file));claim=object_json(read_private(ledger))
                for x in (value,claim):
                    fail(x.get("status")=="COMPLETE" and x.get("rawSha256")==old.HISTORIC_RAW_SHA256 and
                         x.get("ref")==REFS[role] and x.get("imageId")==historic["imageId"] and
                         x.get("scope")==old.SCOPE and x.get("role")==role,"PRIOR_IMPORTED_SCAN_DRIFT")
                fail(claim.get("attempt")==marker["attempt"] and claim.get("evidence")==str(AM_EVIDENCE),
                     "PRIOR_LEDGER_ATTEMPT_DRIFT")
                raw_file=claim.get("rawFile")
                fail(isinstance(raw_file,str) and Path(raw_file).name==raw_file,"PRIOR_SCAN_PATH_DRIFT")
                fail(sha256(read_private(AM_EVIDENCE/raw_file))==old.HISTORIC_RAW_SHA256,"PRIOR_IMPORTED_BYTES_DRIFT")
            else:
                fail(not file.exists() and not file.is_symlink() and not ledger.exists() and not ledger.is_symlink(),
                     "PRIOR_SCAN_OR_RUNTIME_ALREADY_ATTEMPTED")
    an=read_private(AN_MARKER,32768).decode().splitlines()
    fail("ATTEMPT_CONSUMED=TRUE" in an and
         "SOURCE=8f5df51075d6cc42f0d32ad0c730b14611c03f87" in an and
         "ALL_FOUR_CHILDREN_VERIFIED" in an,"H2AN_CONSUMED_FOUR_LOCAL_PROOF_REQUIRED")
    for role in ("gateway","backend","reader"):
        fail("ROLE="+role+" PULL_ATTEMPT_STARTED" in an and
             len([x for x in an if re.fullmatch("ROLE="+role+r" VERIFIED_IMAGE_ID=sha256:[a-f0-9]{64}",x)])==1,
             "H2AN_ROLE_PRELOAD_RECEIPT_DRIFT")
    # Snapshot only existing files; never append/change an old marker or ledger.
    protected=[old.H2AJ,old.H2AK,AN_MARKER,old.MARKER,AM_EVIDENCE/"summary.json",
               old.HISTORIC,AM_GLOBAL/(PINS["mediator"][1]+"-scan.json")]
    return raw,historic,{str(p):sha256(read_private(p)) for p in protected}
def owner_scope():
    private_dir(OWNER_CONFIG)
    active=read_private(OWNER_CONFIG/"active_config",200).decode().strip()
    fail(active=="default","ISOLATED_OWNER_CONFIG_NOT_DEFAULT")
    text=read_private(OWNER_CONFIG/"configurations/config_default",16384).decode()
    cfg=configparser.ConfigParser(interpolation=None);cfg.read_string(text)
    fail(cfg.get("core","account",fallback="")==OWNER and cfg.get("core","project",fallback="")==PROJECT and
         not cfg.get("auth","impersonate_service_account",fallback="") and
         not cfg.get("auth","credential_file_override",fallback=""),"LOCAL_OWNER_PROJECT_SCOPE_DRIFT")
    return {"ownerScope":"EXISTING_LOCAL_CONFIG_ONLY_NOT_LIVE_IAM_PROOF","project":PROJECT}
def state_info(result,name,binding,attempt,role):
    if result.code!=0:
        if not_found(result):return None
        raise Stop("CONTAINER_STATE_UNKNOWN",result.error("CONTAINER_INSPECT"))
    result.need("CONTAINER_INSPECT")
    rows=object_json(b'{"rows":'+result.stdout.encode()+b'}')["rows"]
    fail(isinstance(rows,list) and len(rows)==1,"CONTAINER_STATE_SCHEMA")
    x=rows[0];labels=x.get("Config",{}).get("Labels",{})
    fail(x.get("Name")=="/"+name and
         x.get("Image") in (binding["canonicalConfigDigest"],binding["approvedChildManifestDigest"]) and
         labels.get("oldx.h2ao.attempt")==attempt and labels.get("oldx.h2ao.role")==role,
         "CONTAINER_OWNERSHIP_OR_CANONICAL_ID_DRIFT_NO_CLEANUP")
    return x

class Acceptance:
    def __init__(self,store,session,commands,global_dir,images,mediator_binding,manifests=None):
        self.store=store;self.session=session;self.commands=commands;self.global_dir=Path(global_dir)
        self.images=images;self.bindings={"mediator":mediator_binding};self.manifests=manifests or {}
    def claim_path(self,role,stage):return self.global_dir/(PINS[role][1]+"-"+stage+".json")
    def claim(self,role,stage):
        exclusive_json(self.claim_path(role,stage),{"scope":SCOPE,"role":role,"ref":REFS[role],"stage":stage,
            "status":"ATTEMPTED","evidence":str(self.store.path),"attempt":self.session.attempt})
    def save_stage(self,role,stage,receipt):
        receipt={**receipt,"scope":SCOPE,"role":role,"ref":REFS[role]}
        self.store.put(role+"-"+stage+".json",receipt)
        atomic_json(self.claim_path(role,stage),{**receipt,"evidence":str(self.store.path),"attempt":self.session.attempt})
        return receipt
    def previous(self,role,stage):
        # H2AO is one-shot. A consumed stage is never retried or silently resumed.
        fail(not self.claim_path(role,stage).exists(),"H2AO_STAGE_ALREADY_CONSUMED_NO_REPLAY")
        return None
    def scan(self,role):
        fail(role in ("gateway","backend","reader"),"MEDIATOR_RESCAN_FORBIDDEN")
        fail(role in self.manifests,"ROLE_PINNED_RAW_CHILD_MANIFEST_REQUIRED_BEFORE_NEW_SCAN")
        manifest_config(self.manifests[role],REFS[role])
        self.claim(role,"scan")
        self.store.put(role+"-scan.json",{"status":"ATTEMPTED","role":role,"ref":REFS[role]})
        path=self.store.path/(role+"-grype.json")
        # Exact local Docker provider reference; NOT an ambiguous Docker .Id as scan identity.
        result=self.commands.call(["grype","docker:"+REFS[role],"--output","json","--config",
            str(self.store.path/"grype-config.json")],timeout=1000,stdout_file=path)
        result.need("GRYPE_"+role.upper())
        raw=read_private(path);value=object_json(raw)
        # Preserve captured scan even when identity validation STOPs. Never scan it again.
        self.store.put(role+"-scan.json",{"status":"CAPTURED_IDENTITY_PENDING","rawFile":path.name,
            "rawSha256":sha256(raw),"role":role,"ref":REFS[role]})
        manifest=self.manifests[role]
        binding=bind(manifest,raw,self.images[role],role,REFS[role])
        self.bindings[role]=binding
        self.store.put(role+"-identity.json",binding)
        return self.save_stage(role,"scan",{**binding,"rawFile":path.name,"imageId":binding["canonicalConfigDigest"]})
    def runtime(self,role,image_id):
        prior=self.previous(role,"runtime")
        if prior:
            fail(prior.get("imageId")==image_id,"RUNTIME_LOCAL_IMAGE_DRIFT");return prior
        self.claim(role,"runtime")
        name="oldx-h2ao-"+role+"-"+self.session.attempt[:16]
        receipt={"status":"ATTEMPTED","name":name,"imageId":image_id,"primaryFailure":None,
                 "cleanup":{"status":"NOT_ATTEMPTED"},"diagnostics":[]}
        self.store.put(role+"-runtime.json",receipt)
        state=None;owned=False;persisted=True;diagnostics_complete=False
        def command(args,stage,timeout=30,**kwargs):
            return self.commands.call(args,timeout=timeout,**kwargs).need(stage)
        def inspect():
            result=self.commands.call(["docker","inspect",name])
            return state_info(result,name,self.bindings[role],self.session.attempt,role)
        try:
            cid=command(["docker","run","--detach","--pull=never","--name",name,
                "--label","oldx.h2am.attempt="+self.session.attempt,"--label","oldx.h2am.role="+role,
                "--network","none","--read-only","--cap-drop","ALL","--security-opt","no-new-privileges",
                "--pids-limit","128","--memory","768m","--memory-swap","768m","--cpus","1",
                "--user","65532:65532","-e","OLDX_H2AH_ENABLED=false",REFS[role]],"CONTAINER_START",70).strip()
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
                    receipt["containerImageId"]=state.get("Image")
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

    def run(self,historic_raw,historic_binding):
        summary={"scope":SCOPE,"planDigest":plan_digest(),"roles":{},"outcome":"PARTIAL_UNKNOWN","mediatorRescanForbidden":True}
        try:
            p=self.store.path/"mediator-historic-grype.json"
            with open(p,"xb") as f:
                os.chmod(p,0o600);f.write(historic_raw);f.flush();os.fsync(f.fileno())
            self.claim("mediator","scan")
            self.save_stage("mediator","scan",{**historic_binding,"rawFile":p.name,"historicalImported":True})
            for role in PINS:
                summary["roles"][role]={"stage":"SCAN_IMPORTED" if role=="mediator" else "SCAN"}
                self.store.put("summary.json",summary)
                if role!="mediator":self.scan(role)
                summary["roles"][role]["scan"]="COMPLETE";summary["roles"][role]["stage"]="RUNTIME"
                self.store.put("summary.json",summary)
                self.runtime(role,self.images[role]["Id"])
                summary["roles"][role]["runtime"]="COMPLETE"
            summary["outcome"]="COMPLETE_OFF_EVIDENCE_SECURITY_REVIEW_REQUIRED"
        except Exception as error:
            summary["outcome"]="STOP_PARTIAL_NO_AUTOMATIC_RETRY"
            summary["failure"]={"code":getattr(error,"code",type(error).__name__),"detail":getattr(error,"detail",{})}
        finally:self.store.put("summary.json",summary)
        return summary

def fetch_one_mediator_manifest(token_fd,destination,marker=GET_MARKER):
    # Optional separate approval: supplied unexpired Owner token, never auth refresh/login.
    import ssl,stat,select,urllib.request,urllib.error
    fail(type(token_fd) is int and token_fd>2 and stat.S_ISFIFO(os.fstat(token_fd).st_mode),"OAUTH_ANONYMOUS_PIPE_REQUIRED")
    fail(not Path(destination).exists() and not marker.exists() and not marker.is_symlink(),"MANIFEST_GET_ALREADY_CONSUMED")
    fail(os.readlink("/proc/self/fd/"+str(token_fd)).startswith("pipe:["),"ANONYMOUS_PIPE_REQUIRED")
    receipt_path=Path(destination).parent/"mediator-manifest-get-receipt.json"
    receipt={"scope":SCOPE,"ref":REFS["mediator"],"status":"ATTEMPTED","httpStatus":None,"noRetry":True}
    exclusive_json(marker,{"scope":SCOPE,"ref":REFS["mediator"],"operation":"ONE_AUTHENTICATED_HTTPS_GET_NO_RETRY"})
    atomic_json(receipt_path,receipt)
    req=None;token=None
    try:
        fail(bool(select.select([token_fd],[],[],20)[0]),"OAUTH_PIPE_TIMEOUT")
        token=os.read(token_fd,4097).strip()
        fail(40<=len(token)<=4096 and re.fullmatch(rb"[A-Za-z0-9._~+-]+",token) is not None,"OAUTH_TOKEN_FORMAT")
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*args,**kwargs):raise Stop("MANIFEST_REDIRECT_STOP_NO_RETRY")
        url="https://asia-south1-docker.pkg.dev/v2/oldx-staging/oldx-staging-images/"+PINS["mediator"][0]+"/manifests/sha256:"+PINS["mediator"][1]
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect,
            urllib.request.HTTPSHandler(context=ssl.create_default_context()))
        req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token.decode("ascii"),
            "Accept":"application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json",
            "Accept-Encoding":"identity"},method="GET")
        with opener.open(req,timeout=10) as response:
            receipt["httpStatus"]=response.status
            fail(response.status==200 and response.headers.get("Content-Encoding","identity")=="identity",
                 "MANIFEST_HTTP_STATUS_OR_ENCODING")
            deadline=time.monotonic()+20;parts=[];size=0
            while True:
                fail(time.monotonic()<deadline,"MANIFEST_TOTAL_READ_TIMEOUT")
                part=response.read1(min(16384,524289-size))
                if not part:break
                size+=len(part);fail(size<=524288,"MANIFEST_TOO_LARGE");parts.append(part)
            raw=b"".join(parts)
            receipt["rawSha256"]=sha256(raw)
            # Keep bounded private raw response even if identity validation fails.
            with open(destination,"xb") as f:
                os.chmod(destination,0o600);f.write(raw);f.flush();os.fsync(f.fileno())
            m=manifest_config(raw,REFS["mediator"])
            typ=response.headers.get("Content-Type","").split(";")[0].strip()
            fail(typ==m["mediaType"],"MANIFEST_CONTENT_TYPE_DRIFT")
            header=response.headers.get("Docker-Content-Digest")
            fail(header is None or header==REFS["mediator"].rsplit("@",1)[1],"MANIFEST_DIGEST_HEADER_DRIFT")
        receipt.update(status="COMPLETE_HASH_VERIFIED",rawFile=Path(destination).name)
        return raw
    except urllib.error.HTTPError as error:
        receipt.update(status="FAILED",httpStatus=error.code,reason="MANIFEST_HTTP_FAILURE_NO_RETRY")
        raise Stop("MANIFEST_NETWORK_AUTH_TLS_FAILURE_NO_RETRY") from None
    except (urllib.error.URLError,TimeoutError,OSError):
        receipt.update(status="FAILED",reason="MANIFEST_NETWORK_AUTH_TLS_FAILURE_NO_RETRY")
        raise Stop("MANIFEST_NETWORK_AUTH_TLS_FAILURE_NO_RETRY") from None
    except Stop as error:
        receipt.update(status="FAILED",reason=error.code);raise
    finally:
        if req is not None:req.remove_header("Authorization")
        token=None
        try:atomic_json(receipt_path,receipt)
        except OSError:
            if receipt["status"]=="COMPLETE_HASH_VERIFIED":raise Stop("MANIFEST_RECEIPT_NOT_DURABLE_NO_RUNTIME") from None

def cli(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--execute-h2ao-once",action="store_true")
    p.add_argument("--owner-approved-selective-off-only",action="store_true")
    p.add_argument("--manifest-directory",type=Path)
    p.add_argument("--allow-one-mediator-manifest-get",action="store_true")
    p.add_argument("--oauth-token-fd",type=int)
    args=p.parse_args(argv)
    if not args.execute_h2ao_once or not args.owner_approved_selective_off_only:
        print("H2AO=OFF_NO_DOCKER_GRYPE_REGISTRY_OR_CLOUD_OPERATIONS");return 0
    fail(platform.system()=="Linux" and os.geteuid()==0 and
         "microsoft" in platform.release().lower(),"EXISTING_OWNER_ROOT_WSL_REQUIRED")
    os.umask(0o077)
    for mark in (MARKER,PREFLIGHT_MARKER):
        fail(not mark.exists() and not mark.is_symlink(),"H2AO_ALREADY_CONSUMED_NO_RERUN")
    fail(not GLOBAL.exists() and not GLOBAL.is_symlink(),"H2AO_LEDGER_EXISTS_NO_REPLAY")
    proposal=Path(__file__).resolve().parents[1]/"deployment/four-role/h2aj-four-immutable-images-pinned-proposal.json"
    fail(not proposal.is_symlink(),"PROPOSAL_SYMLINK")
    old.proposal_check(proposal.read_bytes())
    historic_raw,historic,snapshots=history();scope=owner_scope()
    fail(shutil.disk_usage(ROOT).free>=4*1024**3,"LOCAL_DISK_BELOW_4_GIB")
    private_dir(DB)
    binaries={}
    for tool,value in (("docker",shutil.which("docker")),("grype",str(GRYPE))):
        fail(value is not None,"EXISTING_NATIVE_TOOL_REQUIRED")
        path=Path(value).resolve()
        fail(path.stat().st_uid==0 and not path.stat().st_mode&0o022 and os.access(path,os.X_OK),
             "NATIVE_TOOL_OWNER_MODE")
        with path.open("rb") as f:fail(f.read(4)==b"\x7fELF","NATIVE_ELF_TOOL_REQUIRED")
        binaries[tool]=str(path)
    manifests={}
    if args.manifest_directory:
        directory=private_dir(args.manifest_directory)
        for role in PINS:
            file=directory/(role+"-child-manifest.json")
            if file.exists():
                manifests[role]=read_private(file,524288);manifest_config(manifests[role],REFS[role])
    for role in ("gateway","backend","reader"):
        fail(role in manifests,"SAVED_"+role.upper()+"_PINNED_CHILD_PROOF_REQUIRED_NO_EXTRA_GET_AUTHORIZED")
    # No Docker read or runtime marker if the required Mediator OCI proof is unavailable.
    if "mediator" not in manifests:
        fail(args.allow_one_mediator_manifest_get and args.oauth_token_fd is not None,
             "MEDIATOR_PINNED_RAW_CHILD_MANIFEST_REQUIRED_BEFORE_RUNTIME_MARKER")
    else:
        fail(not args.allow_one_mediator_manifest_get and args.oauth_token_fd is None,
             "SAVED_PROOF_PRESENT_NO_EXTRA_GET")
    attempt=secrets.token_hex(16)
    evidence=ROOT/("oldx-h2ao-selective-"+time.strftime("%Y%m%dT%H%M%SZ",time.gmtime())+"-"+attempt[:8])
    evidence.mkdir(mode=0o700);store=Store(evidence)
    if "mediator" not in manifests:
        manifests["mediator"]=fetch_one_mediator_manifest(args.oauth_token_fd,evidence/"mediator-child-manifest.json")
    # Hash/descriptor -> original Grype config must match even before local inspection.
    from step05_h2ao_oci_identity import config_bytes,hashed
    m=manifest_config(manifests["mediator"],REFS["mediator"])
    raw_cfg=config_bytes(object_json(historic_raw))
    fail(m["config"]["digest"]==historic["imageId"] and hashed(raw_cfg)==historic["imageId"] and
         len(raw_cfg)==m["config"]["size"],"MEDIATOR_OCI_CONFIG_UNBOUND_BEFORE_RUNTIME_MARKER")
    home=evidence/"empty-home";home.mkdir(mode=0o700)
    docker_config=evidence/"empty-docker-config";docker_config.mkdir(mode=0o700)
    atomic_json(docker_config/"config.json",{"auths":{}})
    env={"PATH":"/usr/local/bin:/usr/bin:/bin","LANG":"C.UTF-8","HOME":str(home),
         "DOCKER_HOST":"unix:///var/run/docker.sock","DOCKER_CONFIG":str(docker_config),
         "DOCKER_DEFAULT_PLATFORM":"linux/amd64","GRYPE_CHECK_FOR_APP_UPDATE":"false",
         "GRYPE_DB_AUTO_UPDATE":"false","GRYPE_DB_CACHE_DIR":str(DB),"SYFT_CHECK_FOR_APP_UPDATE":"false"}
    atomic_json(evidence/"grype-config.json",{"check-for-app-update":False,"db":{"auto-update":False,"cache-dir":str(DB)}})
    pre=Session.consume(PREFLIGHT_MARKER,attempt,plan_digest())
    commands=Commands(pre,store,env,binaries=binaries)
    try:
        fail(commands.call(["docker","info","--format","{{.OSType}}"]).need("LOCAL_ENGINE").strip()=="linux","LOCAL_ENGINE_NOT_LINUX")
        db=object_json(commands.call(["grype","db","status","-o","json","--config",str(evidence/"grype-config.json")]).need("EXISTING_DB"))
        status=db.get("status") if isinstance(db.get("status"),dict) else db
        fail(status.get("valid") is True,"EXISTING_DB_NOT_EXPLICITLY_VALID_NO_DOWNLOAD")
        images={}
        for role in PINS:
            result=commands.call(["docker","image","inspect",REFS[role]])
            rows=json.loads(result.need("FOUR_EXISTING_LOCAL_REFS_NO_PULL"))
            fail(isinstance(rows,list) and len(rows)==1,"LOCAL_IMAGE_SCHEMA")
            images[role]=local_contract(rows[0],role,REFS[role])
            descriptor=manifest_config(manifests[role],REFS[role])["config"]
            fail(images[role]["Id"] in (REFS[role].rsplit("@",1)[1],descriptor["digest"]),
                 "LOCAL_DOCKER_ID_UNBOUND_TO_VERIFIED_CHILD_CONFIG")
        binding=bind(manifests["mediator"],historic_raw,images["mediator"],"mediator",REFS["mediator"],
            historical=True,raw_report_sha=old.HISTORIC_RAW_SHA256)
        # Verify any additional saved role proofs against local IDs later with its new scan.
        store.put("mediator-identity.json",binding)
        for role,raw in manifests.items():
            target=evidence/(role+"-verified-child-manifest.json")
            with open(target,"xb") as f:os.chmod(target,0o600);f.write(raw);f.flush();os.fsync(f.fileno())
        for path,expected in snapshots.items():fail(sha256(read_private(path))==expected,"OLD_EVIDENCE_CHANGED_DURING_PREFLIGHT")
        store.put("preflight.json",{"scope":SCOPE,"status":"COMPLETE","oldEvidenceSha256":snapshots,
            "ownerProject":scope,"mediatorIdentity":binding,
            "localImages":{r:{"ref":REFS[r],"dockerImageId":images[r]["Id"]} for r in PINS}})
        # ALL prior-state/local-image/DB/Mediator-identity gates precede runtime marker.
        session=Session.consume(MARKER,attempt,plan_digest());GLOBAL.mkdir(mode=0o700)
        commands=Commands(session,store,env,binaries=binaries)
        acceptance=Acceptance(store,session,commands,GLOBAL,images,binding,manifests)
        outcome=acceptance.run(historic_raw,binding)
    except Exception as error:
        outcome={"scope":SCOPE,"planDigest":plan_digest(),"outcome":"STOP_PARTIAL_NO_AUTOMATIC_RETRY",
            "failure":{"code":getattr(error,"code",type(error).__name__),"detail":getattr(error,"detail",{})}}
        store.put("summary.json",outcome)
    store.put("source-hashes.json",{p.name:sha256(p.read_bytes()) for p in
        [Path(__file__),Path(__file__).with_name("step05_h2ao_oci_identity.py"),
         *[Path(__file__).with_name(n) for n in FROZEN]]})
    print("H2AO_OUTCOME="+outcome["outcome"])
    print("H2AO_SUMMARY_SHA256="+sha256(read_private(evidence/"summary.json")))
    imported=(evidence/"mediator-scan.json").exists()
    print("H2AO_MEDIATOR_SCAN="+("IMPORTED_57_NEVER_RESCANNED" if imported else "HISTORICAL_ONLY_NOT_IMPORTED_NO_RESCAN"))
    print("H2AO_PRIVATE_EVIDENCE="+str(evidence))
    print("H2AO_PRODUCTION=OFF_NO_GO")
    return 0 if outcome["outcome"]=="COMPLETE_OFF_EVIDENCE_SECURITY_REVIEW_REQUIRED" else 2
if __name__=="__main__":
    try:sys.exit(cli())
    except Exception as error:
        print("H2AO_STOP="+sanitized(getattr(error,"code",type(error).__name__),200));sys.exit(2)
