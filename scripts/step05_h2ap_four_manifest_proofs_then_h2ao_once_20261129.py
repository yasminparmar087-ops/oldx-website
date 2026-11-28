#!/usr/bin/env python3
"""H2AP future one-shot: four pinned proof GETs then separately approved unchanged H2AO."""
from __future__ import annotations
import argparse,hashlib,importlib,json,os,platform,re,secrets,shutil,ssl,subprocess,sys,time,urllib.error,urllib.request
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path("/root")
MARKER=ROOT/".oldx-step05-h2ap-four-child-manifests-and-h2ao-once-20261129"
SDK=ROOT/"oldx-tools/native-gcloud-594.0.1/google-cloud-sdk"
SDK_PY=SDK/"platform/bundledpythonunix/bin/python3"
TOKEN_BLOB="5922b9ca1b33d2a70bdc66cdf2c45ff3e9f2c163"
SOURCE="92a4529d3fe4de641898f9195634dfd2e9b8144e"
REPO="yasminparmar087-ops/oldx-website"
FROZEN={
 "scripts/step05_h2ao_selective_continuation_once_20261129.py":"5db17708caad89f0c49502eb343c71f3120b1260",
 "scripts/step05_h2ao_oci_identity.py":"b7f7eb42ba4a72fb6959ca06e52cff55b3b30ae5",
 "scripts/step05_h2am_acceptance_support.py":"b9b57daa9a5b5f0304afc9cfc758630793454c07",
 "scripts/step05_h2am_selective_acceptance_once_20261128.py":"3adfb06ca66d6175f089ea797df21ca767779cca",
 "deployment/four-role/h2aj-four-immutable-images-pinned-proposal.json":"c1cfcfa2f224e9a47dd6e896730c73e927b9b483"}
PINS={
 "mediator":("oldx-c2-mediator-h2ah","01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe"),
 "gateway":("oldx-c2-gateway-h2ah","921fbf4ff71b918c479e4a786868368640a494c16da08e54192f25e14dc1ec4d"),
 "backend":("oldx-c2-backend-h2ah","01ae540aa88ad0e3a6888994dd41b6b02b9d934a7a1d2e455f44b194f033b941"),
 "reader":("oldx-c2-kms-reader","822e2592b1010bfa94a1fe5bc75003712485abae0369f5252ece3863723eb077")}
PREFIX="asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/"
REFS={r:PREFIX+n+"@sha256:"+d for r,(n,d) in PINS.items()}
URLS={r:"https://asia-south1-docker.pkg.dev/v2/oldx-staging/oldx-staging-images/"+n+"/manifests/sha256:"+d for r,(n,d) in PINS.items()}
REPORT_SHA="e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92"
MED_CONFIG="sha256:44c8657a5aad46d7aa1192e73af0a338200c61720f47b0ebe8d19faa3613f1e2"
SCOPE="oldx.h2ap.four-exact-child-proofs.h2ao-once.v1"
class Stop(Exception):
    def __init__(self,code,status=None):self.code=code;self.status=status;super().__init__(code)
def need(ok,code):
    if not ok:raise Stop(code)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def syncdir(p):
    fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
def write_new(p,raw):
    fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,"wb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    syncdir(Path(p).parent)
def private_read(p,limit=1048576):
    p=Path(p);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        import stat
        st=os.fstat(fd)
        need(stat.S_ISREG(st.st_mode) and st.st_uid==os.geteuid() and not st.st_mode&0o077,"PRIVATE_FILE_OWNER_MODE")
        with os.fdopen(fd,"rb",closefd=False) as f:raw=f.read(limit+1)
        need(len(raw)<=limit,"PRIVATE_FILE_LIMIT");return raw
    finally:os.close(fd)
def receipt(p,value):
    p=Path(p)
    if p.exists():private_read(p)
    need(not p.is_symlink(),"RECEIPT_SYMLINK")
    tmp=p.with_name("."+p.name+"."+secrets.token_hex(8))
    write_new(tmp,(json.dumps(value,sort_keys=True,indent=2)+"\n").encode())
    os.replace(tmp,p);syncdir(p.parent)
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):raise Stop("HTTP_REDIRECT_NO_RETRY",code)
def opener():
    return urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect,
        urllib.request.HTTPSHandler(context=ssl.create_default_context()))
def read_body(response,limit):
    deadline=time.monotonic()+20;parts=[];size=0
    while True:
        need(time.monotonic()<deadline,"HTTP_BODY_DEADLINE")
        part=response.read1(min(16384,limit+1-size))
        if not part:break
        size+=len(part);need(size<=limit,"HTTP_BODY_OVERSIZE");parts.append(part)
    return b"".join(parts)
def get_manifest(role,token):
    # Only this closed role map can form an authenticated request.
    need(role in URLS,"ROLE_NOT_APPROVED")
    request=urllib.request.Request(URLS[role],headers={"Authorization":"Bearer "+token,
        "Accept":"application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json",
        "Accept-Encoding":"identity"},method="GET")
    http_status=None
    try:
        with opener().open(request,timeout=10) as response:
            http_status=response.status
            need(response.status==200,"HTTP_STATUS_NOT_200")
            need(response.headers.get("Content-Encoding","identity")=="identity","HTTP_CONTENT_ENCODING")
            raw=read_body(response,524288)
            return raw,{"status":response.status,"type":response.headers.get("Content-Type",""),
                "digest":response.headers.get("Docker-Content-Digest")}
    except Stop as e:
        if e.status is None:e.status=http_status
        raise
    except urllib.error.HTTPError as e:raise Stop("HTTP_ERROR_NO_RETRY",e.code) from None
    except (urllib.error.URLError,TimeoutError,OSError):raise Stop("HTTP_AUTH_DNS_TLS_OR_TIMEOUT_NO_RETRY") from None
    finally:request.remove_header("Authorization")
def public_source(path):
    need(path in FROZEN,"SOURCE_PATH_NOT_APPROVED")
    url="https://raw.githubusercontent.com/"+REPO+"/"+SOURCE+"/"+path
    try:
        with opener().open(urllib.request.Request(url,headers={"Accept-Encoding":"identity"}),timeout=10) as response:
            need(response.status==200 and response.headers.get("Content-Encoding","identity")=="identity","FROZEN_SOURCE_HTTP")
            raw=read_body(response,100000)
    except (urllib.error.URLError,TimeoutError,OSError):raise Stop("FROZEN_SOURCE_DOWNLOAD_FAILED_NO_RETRY") from None
    need(blob(raw)==FROZEN[path],"FROZEN_SOURCE_BLOB_MISMATCH");return raw
def verify_bundle(root):
    for path,expected in FROZEN.items():
        need(blob(private_read(root/path,100000))==expected,"FROZEN_H2AO_SOURCE_DRIFT")
def prepare_bundle(evidence):
    root=evidence/"source";root.mkdir(mode=0o700)
    local=Path(__file__).resolve().parents[1]
    for path,expected in FROZEN.items():
        source=local/path
        if source.exists():
            need(not source.is_symlink(),"LOCAL_SOURCE_SYMLINK")
            raw=source.read_bytes();need(blob(raw)==expected,"LOCAL_SOURCE_BLOB_DRIFT")
        else:raw=public_source(path)
        dest=root/path;dest.parent.mkdir(mode=0o700,parents=True,exist_ok=True);write_new(dest,raw)
    verify_bundle(root);return root
def assert_fresh(ao,include_h2ap=True):
    paths=([MARKER] if include_h2ap else [])+[ao.MARKER,ao.PREFLIGHT_MARKER,ao.GET_MARKER,ao.GLOBAL]
    for p in paths:
        need(not p.exists() and not p.is_symlink(),"CONSUMED_MARKER_OR_LEDGER_NO_REPLAY")
def load_token(helper):
    need(blob(helper.read_bytes())==TOKEN_BLOB and not helper.is_symlink(),"TOKEN_HELPER_BLOB_DRIFT")
    native=SDK_PY.resolve(strict=True)
    need(native.is_relative_to(SDK.resolve(strict=True)) and native.stat().st_uid==0 and
         not native.stat().st_mode&0o022 and os.access(native,os.X_OK),"NATIVE_SDK_PYTHON_UNTRUSTED")
    with native.open("rb") as f:need(f.read(4)==b"\x7fELF","NATIVE_SDK_PYTHON_NOT_ELF")
    env={"PATH":"/usr/bin:/bin","HOME":"/root","LANG":"C.UTF-8","PYTHONDONTWRITEBYTECODE":"1",
        "CLOUDSDK_CONFIG":str(ROOT/"oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config"),
        "CLOUDSDK_CORE_CHECK_GCE_METADATA":"false","CLOUDSDK_CORE_DISABLE_USAGE_REPORTING":"1",
        "CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK":"1"}
    # Child refuses terminal/files: only captured anonymous IPC, no token logs.
    try:
        p=subprocess.run([str(native),"-I","-B",str(helper),"--h2ap-cached-owner-token-to-pipe-only"],
            stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,timeout=20,check=False)
    except (OSError,subprocess.TimeoutExpired):raise Stop("CACHED_OWNER_TOKEN_LOAD_FAILED_NO_RETRY") from None
    if p.returncode!=0:
        codes={"SDK_WRITE_FORBIDDEN","SDK_NETWORK_OR_MUTATION_FORBIDDEN","SDK_SQLITE_NOT_READONLY",
            "SDK_CACHE_FILE_SCOPE","OWNER_USER_CREDENTIAL_REQUIRED","CACHED_TOKEN_MISSING","CACHED_EXPIRY_MISSING",
            "CACHED_TOKEN_EXPIRED_OR_INSUFFICIENT_NO_REFRESH"}
        message=p.stderr[:200].decode("ascii","replace")
        code=message.removeprefix("H2AP_TOKEN_STOP=")
        raise Stop("OWNER_TOKEN_"+code if code in codes else "CACHED_OWNER_TOKEN_UNAVAILABLE_NO_REFRESH")
    need(0<len(p.stdout)<=8192,"CACHED_OWNER_TOKEN_IPC_LIMIT")
    try:packet=json.loads(p.stdout)
    except ValueError:raise Stop("CACHED_TOKEN_IPC_SCHEMA") from None
    need(isinstance(packet,dict) and set(packet)=={"token","expiresAt"} and isinstance(packet["token"],str) and
         re.fullmatch(r"[A-Za-z0-9._~+-]{40,4096}",packet["token"]) is not None and
         type(packet["expiresAt"]) is int and 180<=packet["expiresAt"]-time.time()<=3700,"CACHED_TOKEN_INVALID_OR_TOO_OLD")
    return packet["token"]
def mediator_config(raw,manifest,identity):
    need(sha(raw)==REPORT_SHA,"HISTORICAL_MEDIATOR_REPORT_SHA_NO_RESCAN")
    report=identity.object_json(raw);target=report.get("source",{}).get("target",{})
    need(target.get("userInput") in (REFS["mediator"],"docker:"+REFS["mediator"]) and
         target.get("imageID")==MED_CONFIG,"HISTORICAL_MEDIATOR_REF_OR_ID_DRIFT")
    decoded=identity.config_bytes(report)
    need(identity.hashed(decoded)==MED_CONFIG and len(decoded)==32372 and
         manifest["config"]["digest"]==MED_CONFIG and manifest["config"]["size"]==len(decoded),
         "MEDIATOR_MANIFEST_HISTORICAL_CONFIG_MISMATCH")
    identity.config_contract(decoded,"mediator")
    # Preserve the established57 counts, never invoke scanner.
    from step05_h2am_acceptance_support import scan_report
    scan_report(raw,REFS["mediator"],image_id=MED_CONFIG,historical=True)
class Workflow:
    def __init__(self,evidence,marker,identity,historic,*,fetch=None):
        self.evidence=Path(evidence);self.marker=Path(marker);self.identity=identity;self.historic=historic;self.fetch=fetch or get_manifest
        self.proofs=self.evidence/"proofs";self.proofs.mkdir(mode=0o700)
        self.summary={"scope":SCOPE,"outcome":"NOT_STARTED","roles":{},"handoff":{"status":"NOT_ATTEMPTED"},
            "mediatorScan":"HISTORICAL_57_NO_RESCAN","security":"HOLD","production":"OFF_NO_GO"}
    def save(self):receipt(self.evidence/"summary.json",self.summary)
    def acquire(self,token):
        # Never accept token in marker/receipt/env/argv. Exclusive one-shot before request.
        write_new(self.marker,(json.dumps({"scope":SCOPE,"refs":REFS,"evidence":str(self.evidence)})+"\n").encode())
        self.summary["outcome"]="ATTEMPT_CONSUMED";self.save()
        for role in PINS:
            status={"status":"ATTEMPTED","ref":REFS[role],"requestCount":1,"httpStatus":None}
            self.summary["roles"][role]=status
            receipt(self.evidence/(role+"-receipt.json"),status);self.save()
            try:
                raw,headers=self.fetch(role,token)
                status["httpStatus"]=headers["status"];need(headers["status"]==200,"HTTP_STATUS_NOT_200")
                need(isinstance(raw,bytes) and 0<len(raw)<=524288,"HTTP_BODY_SIZE_INVALID")
                file=self.proofs/(role+"-child-manifest.json");write_new(file,raw)
                status.update(rawFile=file.name,rawSha256=sha(raw))
                manifest=self.identity.manifest_config(raw,REFS[role])
                need(headers["type"].split(";")[0].strip()==manifest["mediaType"],"HTTP_MEDIA_TYPE_MISMATCH")
                need(headers["digest"] is None or headers["digest"]==REFS[role].rsplit("@",1)[1],"HTTP_DIGEST_HEADER_MISMATCH")
                if role=="mediator":mediator_config(self.historic,manifest,self.identity)
                status.update(status="COMPLETE",canonicalConfigDigest=manifest["config"]["digest"],persisted=True)
                receipt(self.evidence/(role+"-receipt.json"),status);self.save()
            except Exception as e:
                status.update(status="FAILED",failureCode=getattr(e,"code",type(e).__name__),
                    httpStatus=getattr(e,"status",None) or status["httpStatus"])
                # A receipt-write error must not trigger another request or handoff.
                try:receipt(self.evidence/(role+"-receipt.json"),status);self.save()
                except OSError:pass
                raise
        self.summary["outcome"]="FOUR_PROOFS_COMPLETE";self.save()
    def verify_proofs(self):
        need(set(self.summary["roles"])==set(PINS),"FOUR_ROLE_PROOFS_REQUIRED")
        for role in PINS:
            value=self.summary["roles"][role];need(value.get("status")=="COMPLETE","ROLE_PROOF_NOT_COMPLETE")
            raw=private_read(self.proofs/(role+"-child-manifest.json"),524288)
            need(sha(raw)==value["rawSha256"],"PROOF_CHANGED_AFTER_ACQUISITION")
            manifest=self.identity.manifest_config(raw,REFS[role])
            if role=="mediator":mediator_config(self.historic,manifest,self.identity)
    def handoff(self,bundle,approved,invoke):
        need(approved is True,"SEPARATE_H2AO_APPROVAL_REQUIRED")
        self.verify_proofs();verify_bundle(bundle)
        need(self.summary["handoff"]["status"]=="NOT_ATTEMPTED","H2AO_HANDOFF_ALREADY_ATTEMPTED")
        self.summary["handoff"]={"status":"ATTEMPTED"};self.save()
        result=invoke(bundle,self.proofs,self.evidence)
        self.summary["handoff"]=result
        need(result.get("exitCode")==0 and result.get("outcome")=="COMPLETE_OFF_EVIDENCE_SECURITY_REVIEW_REQUIRED",
             "H2AO_STOP_NO_RETRY")
        self.summary["outcome"]="PROOFS_AND_OFF_EVIDENCE_COMPLETE_SECURITY_HOLD";self.save()
def invoke_h2ao(bundle,proofs,evidence):
    command=[sys.executable,"-B",str(bundle/"scripts/step05_h2ao_selective_continuation_once_20261129.py"),
        "--manifest-directory",str(proofs),"--execute-h2ao-once","--owner-approved-selective-off-only"]
    # Deliberately NO optional GET flag or token-FD. Empty auth environment.
    env={"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":"/root","LANG":"C.UTF-8","PYTHONDONTWRITEBYTECODE":"1"}
    log=evidence/"private-h2ao-output.log";p=None;timed=False
    with open(log,"xb") as out:
        os.chmod(log,0o600)
        try:
            p=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=out,stderr=out,env=env)
            deadline=time.monotonic()+4200
            while p.poll() is None:
                if time.monotonic()>deadline or log.stat().st_size>65536:
                    timed=True;p.kill();break # Own CLI only; never clean unknown Docker resources.
                time.sleep(0.1)
            p.wait(timeout=5)
        except (OSError,subprocess.TimeoutExpired):raise Stop("H2AO_CHILD_STATE_UNKNOWN_NO_RETRY") from None
        finally:out.flush();os.fsync(out.fileno())
    result={"status":"STOP" if timed or p.returncode else "RETURNED","exitCode":p.returncode,"timedOutOrOutputLimit":timed,
        "outputSha256":sha(private_read(log,131072)),"outcome":"UNKNOWN"}
    receipt(evidence/"private-h2ao-child-result.json",result)
    if timed or p.returncode:return result
    text=private_read(log,65536).decode("utf8","replace")
    paths=re.findall(r"^H2AO_PRIVATE_EVIDENCE=(/root/oldx-h2ao-selective-[0-9]{8}T[0-9]{6}Z-[a-f0-9]{8})$",text,re.M)
    hashes=re.findall(r"^H2AO_SUMMARY_SHA256=([a-f0-9]{64})$",text,re.M)
    need(len(paths)==len(hashes)==1,"H2AO_SUMMARY_LOCATION_NOT_VERIFIED")
    raw=private_read(Path(paths[0])/"summary.json")
    need(sha(raw)==hashes[0],"H2AO_SUMMARY_SHA_MISMATCH")
    summary=json.loads(raw)
    need(summary.get("scope")=="oldx.h2ao.exact-child-config-selective.v1" and
         set(summary.get("roles",{}))==set(PINS) and
         all(v.get("runtime")=="COMPLETE" and v.get("scan")=="COMPLETE" for v in summary["roles"].values()),
         "H2AO_COMPLETE_ROLE_EVIDENCE_MISSING")
    return {**result,"status":"COMPLETE_OFF_EVIDENCE","outcome":summary.get("outcome"),"summarySha256":hashes[0]}
def cli(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--owner-approved-four-manifest-gets-once",action="store_true")
    p.add_argument("--owner-approved-h2ao-selective-once",action="store_true")
    args=p.parse_args(argv)
    if not args.owner_approved_four_manifest_gets_once or not args.owner_approved_h2ao_selective_once:
        print("H2AP=OFF_FRESH_COMBINED_OWNER_APPROVAL_REQUIRED");return 0
    need(platform.system()=="Linux" and "microsoft" in platform.release().lower() and os.geteuid()==0,"OWNER_ROOT_WSL_REQUIRED")
    os.umask(0o077)
    need(not MARKER.exists() and not MARKER.is_symlink(),"H2AP_ALREADY_CONSUMED")
    evidence=ROOT/("oldx-h2ap-proofs-"+time.strftime("%Y%m%dT%H%M%SZ",time.gmtime())+"-"+secrets.token_hex(4))
    evidence.mkdir(mode=0o700);workflow=None;token=None
    try:
        bundle=prepare_bundle(evidence)
        sys.path.insert(0,str(bundle/"scripts"))
        ao=importlib.import_module("step05_h2ao_selective_continuation_once_20261129")
        identity=importlib.import_module("step05_h2ao_oci_identity")
        assert_fresh(ao);ao.owner_scope()
        historic,_old,snapshots=ao.history()
        ao.old.proposal_check(private_read(bundle/"deployment/four-role/h2aj-four-immutable-images-pinned-proposal.json"))
        need(ao.REFS==REFS,"FROZEN_ROLE_REF_DRIFT")
        ao.private_dir(ao.DB);need(shutil.disk_usage(ROOT).free>=4*1024**3,"LOCAL_EVIDENCE_DISK_BELOW_4_GIB")
        for value in (shutil.which("docker"),str(ao.GRYPE)):
            need(value is not None,"EXISTING_NATIVE_TOOL_MISSING");native=Path(value).resolve()
            need(native.stat().st_uid==0 and not native.stat().st_mode&0o022 and os.access(native,os.X_OK),"NATIVE_TOOL_OWNER_MODE")
            with native.open("rb") as f:need(f.read(4)==b"\x7fELF","NATIVE_TOOL_NOT_ELF")
        helper=Path(__file__).with_name("step05_h2ap_cached_owner_token.py")
        token=load_token(helper) # BEFORE H2AP marker; no refresh/network or credential writes.
        assert_fresh(ao)
        for path,expected in snapshots.items():need(sha(private_read(path))==expected,"OLD_EVIDENCE_CHANGED")
        receipt(evidence/"source-and-preflight.json",{"scope":SCOPE,"frozenBlobs":FROZEN,"tokenHelperBlob":TOKEN_BLOB,
            "runnerSha256":sha(Path(__file__).read_bytes()),"oldEvidenceSha256":snapshots,"project":"oldx-staging",
            "ownerProject":"LOCAL_CONFIG_CHECKED_NOT_LIVE_IAM_PROOF","token":"CACHED_MEMORY_ONLY_VALUE_NOT_RETAINED"})
        workflow=Workflow(evidence,MARKER,identity,historic)
        try:workflow.acquire(token)
        finally:token=None
        workflow.verify_proofs();verify_bundle(bundle);assert_fresh(ao,include_h2ap=False)
        for path,expected in snapshots.items():need(sha(private_read(path))==expected,"OLD_EVIDENCE_CHANGED")
        workflow.handoff(bundle,args.owner_approved_h2ao_selective_once,invoke_h2ao)
        return 0
    except Exception as error:
        state=workflow.summary if workflow else {"scope":SCOPE,"roles":{},"handoff":{"status":"NOT_ATTEMPTED"}}
        state.update({"outcome":"STOP_NO_AUTOMATIC_RETRY","failureCode":getattr(error,"code",type(error).__name__),
            "security":"HOLD","production":"OFF_NO_GO"})
        receipt(evidence/"summary.json",state);return 2
    finally:
        token=None
        summary=evidence/"summary.json"
        print("H2AP_SUMMARY_SHA256="+(sha(private_read(summary)) if summary.exists() else "UNAVAILABLE"))
        print("H2AP_PRIVATE_EVIDENCE="+str(evidence))
        print("H2AP_PRODUCTION=OFF_NO_GO_NO_CVE_ACCEPTANCE")
if __name__=="__main__":
    try:sys.exit(cli())
    except Exception as error:
        print("H2AP_STOP="+getattr(error,"code",type(error).__name__));sys.exit(2)
