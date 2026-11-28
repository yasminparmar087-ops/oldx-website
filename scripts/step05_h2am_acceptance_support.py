"""H2AM private evidence support. Importing this module performs no IO."""
from __future__ import annotations
import hashlib
import json
import os
import re
import secrets
import subprocess
import threading
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

CAPTURE_LIMIT=65536
REPORT_LIMIT=64*1024*1024
SENSITIVE=re.compile(r"""authorization|access.?token|refresh.?token|id.?token|password|secret|api.?key|credential|private.?key|signed.?payload|signature|envelope|(?:configuration|config|env)["']?\s*[=:]|(?:OLDX_|GOOGLE_|CLOUDSDK_)\w*\s*=""",re.I)
def sanitized(value,limit=CAPTURE_LIMIT):
    text=str(value or "")[:limit]
    text=re.sub(r"-----BEGIN [^-]*(?:PRIVATE KEY)[^-]*-----.*?(?:-----END [^-]*PRIVATE KEY-----|$)","[REDACTED_PRIVATE_KEY]",text,flags=re.S)
    text=re.sub(r"Bearer\s+[^\s\"'\\]+","Bearer [REDACTED]",text,flags=re.I)
    text=re.sub(r"\b[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}\.[A-Za-z0-9_-]{6,}\b","[REDACTED_JWT]",text)
    text=re.sub(r"\bya29\.[A-Za-z0-9._~-]+","[REDACTED_OAUTH]",text)
    text=re.sub(r"\b[A-Za-z0-9_+/=-]{96,}\b","[REDACTED_OPAQUE_PAYLOAD]",text)
    text=re.sub(r"/(?:root|home|mnt)/[^\s\"':]*","[PRIVATE_PATH]",text)
    return "\n".join("[REDACTED_SENSITIVE_LINE]" if SENSITIVE.search(line) else line for line in text.splitlines())
def sha256(data):return hashlib.sha256(data).hexdigest()
def digest(value):return isinstance(value,str) and re.fullmatch(r"sha256:[a-f0-9]{64}",value) is not None
class Stop(Exception):
    def __init__(self,code,detail=None):
        self.code=code;self.detail=detail or {}
        super().__init__(code)

def read_private(path,limit=REPORT_LIMIT):
    path=Path(path)
    fd=os.open(path,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0))
    try:
        st=os.fstat(fd)
        if not __import__("stat").S_ISREG(st.st_mode) or st.st_uid!=os.geteuid() or st.st_mode&0o077:
            raise Stop("PRIVATE_FILE_OWNER_MODE_REQUIRED")
        with os.fdopen(fd,"rb",closefd=False) as f:data=f.read(limit+1)
        if len(data)>limit:raise Stop("PRIVATE_FILE_TOO_LARGE")
        return data
    finally:os.close(fd)
def fsync_dir(path):
    if os.name=="posix":
        fd=os.open(path,os.O_RDONLY|getattr(os,"O_DIRECTORY",0))
        try:os.fsync(fd)
        finally:os.close(fd)
def atomic_json(path,value):
    path=Path(path)
    if path.is_symlink():raise Stop("RECEIPT_SYMLINK")
    if path.exists():read_private(path)
    tmp=path.with_name("."+path.name+"."+secrets.token_hex(8))
    fd=os.open(tmp,os.O_CREAT|os.O_EXCL|os.O_WRONLY|getattr(os,"O_NOFOLLOW",0),0o600)
    try:
        with os.fdopen(fd,"w",encoding="utf8") as f:
            json.dump(value,f,sort_keys=True,indent=2);f.write("\n");f.flush();os.fsync(f.fileno())
        os.replace(tmp,path);fsync_dir(path.parent)
    finally:
        if tmp.exists():tmp.unlink() # Only this exclusive temporary file.
def exclusive_json(path,value):
    fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY|getattr(os,"O_NOFOLLOW",0),0o600)
    with os.fdopen(fd,"w",encoding="utf8") as f:
        json.dump(value,f,sort_keys=True);f.write("\n");f.flush();os.fsync(f.fileno())
    fsync_dir(Path(path).parent)
class Store:
    def __init__(self,path):
        self.path=Path(path);self.sequence=0
    def put(self,name,data):atomic_json(self.path/name,{**data,"recordedAtUnixNs":time.time_ns()})
    def get(self,name):return json.loads(read_private(self.path/name))
    def command(self,record):
        self.sequence+=1;self.put("command-%04d.json"%self.sequence,record)
class Session:
    def __init__(self,marker,attempt):
        self.marker=Path(marker);self.attempt=attempt
    def require(self):
        if json.loads(read_private(self.marker)).get("attempt")!=self.attempt:
            raise Stop("FRESH_APPROVAL_MARKER_REQUIRED")
    @classmethod
    def consume(cls,marker,attempt,scope):
        exclusive_json(marker,{"attempt":attempt,"scope":scope,"started":True})
        return cls(marker,attempt)
@dataclass
class Result:
    code:int|None
    stdout:str=""
    stderr:str=""
    timed_out:bool=False
    truncated:bool=False
    def error(self,stage):
        return {"stage":sanitized(stage,200),"exitCode":self.code,"timedOut":self.timed_out,
                "stdout":sanitized(self.stdout),"stderr":sanitized(self.stderr),
                "truncated":self.truncated}
    def need(self,stage):
        if self.code!=0 or self.timed_out or self.truncated:
            raise Stop("COMMAND_FAILED",self.error(stage))
        return self.stdout

class Commands:
    """No shell, hidden retry, version/login/API calls or unbounded pipe buffer."""
    def __init__(self,session,store,env,binaries=None):
        self.session=session;self.store=store;self.env=env;self.binaries=binaries or {}
    def call(self,args,*,timeout=30,input_bytes=None,stdout_file=None):
        self.session.require()
        if args[0] not in ("docker","grype"):raise Stop("COMMAND_OUTSIDE_SCOPE")
        args=[self.binaries.get(args[0],args[0]),*args[1:]]
        started=time.monotonic();out=bytearray();err=bytearray();overflow=[False]
        output=None;p=None;timed_out=False;reason=None;threads=[]
        def drain(pipe,target):
            try:
                while True:
                    part=pipe.read(4096)
                    if not part:break
                    remaining=CAPTURE_LIMIT-len(target)
                    target.extend(part[:max(0,remaining)])
                    if len(part)>remaining:overflow[0]=True
            finally:pipe.close()
        try:
            if stdout_file:
                output=open(stdout_file,"xb")
                os.chmod(stdout_file,0o600)
            p=subprocess.Popen(args,stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
                stdout=output or subprocess.PIPE,stderr=subprocess.PIPE,env=self.env,shell=False)
            if not output:
                t=threading.Thread(target=drain,args=(p.stdout,out),daemon=True);t.start();threads.append(t)
            t=threading.Thread(target=drain,args=(p.stderr,err),daemon=True);t.start();threads.append(t)
            if input_bytes is not None:
                try:p.stdin.write(input_bytes);p.stdin.close()
                except BrokenPipeError:pass
            while p.poll() is None:
                if time.monotonic()-started>=timeout:
                    timed_out=True;reason="TIMEOUT";p.kill();break
                if stdout_file and Path(stdout_file).stat().st_size>REPORT_LIMIT:
                    reason="REPORT_SIZE_LIMIT";p.kill();break
                time.sleep(0.02)
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            timed_out=True;reason="CHILD_EXIT_UNKNOWN"
        except OSError:
            reason="OS_ERROR"
        finally:
            if output:output.flush();os.fsync(output.fileno());output.close()
            for t in threads:
                t.join(timeout=2)
                if t.is_alive():overflow[0]=True
        result=Result(p.returncode if p else None,out.decode("utf8","replace"),
            err.decode("utf8","replace"),timed_out,overflow[0] or reason is not None)
        # Structured/image inspect output may contain Env; redact it entirely.
        logged=result.error(" ".join(args[:3]))
        if "inspect" in args:logged["stdout"]="[STRUCTURED_INSPECT_SAVED_AS_ALLOWLIST_ONLY]"
        logged.update({"elapsedMs":int((time.monotonic()-started)*1000),
            "reason":reason,"outputFile":Path(stdout_file).name if stdout_file else None})
        self.store.command(logged) # Persist command outcome before caller cleanup.
        return result

KNOWN={"critical":"Critical","high":"High","medium":"Medium","low":"Low","negligible":"Negligible","unknown":"Unknown"}
HISTORIC_COUNTS={"Critical":0,"High":18,"Medium":20,"Low":6,"Negligible":11,"Unknown":2}
def scan_report(raw,expected_ref,*,image_id=None,historical=False):
    try:report=json.loads(raw)
    except (ValueError,UnicodeError):raise Stop("SCAN_JSON_INVALID") from None
    if not isinstance(report,dict):raise Stop("SCAN_SCHEMA_UNKNOWN")
    matches=report.get("matches")
    source=report.get("source")
    if not isinstance(source,dict) or source.get("type")!="image":raise Stop("SCAN_SCHEMA_UNKNOWN")
    target=source.get("target",{})
    if not isinstance(matches,list) or not isinstance(target,dict):raise Stop("SCAN_SCHEMA_UNKNOWN")
    actual=target.get("imageID") or target.get("imageId")
    if not digest(actual) or image_id is not None and actual!=image_id:
        raise Stop("SCAN_IMAGE_ID_MISMATCH_OR_UNKNOWN")
    if historical:
        # Require explicit linkage to the original child, not a similar image.
        repo_digests=target.get("repoDigests") or []
        if not isinstance(repo_digests,list):raise Stop("SCAN_SCHEMA_UNKNOWN")
        references=[target.get("userInput"),*repo_digests]
        if not (expected_ref in references or "docker:"+expected_ref in references or
                target.get("manifestDigest")==expected_ref.rsplit("@",1)[1]):
            raise Stop("HISTORICAL_SCAN_DIGEST_UNBOUND")
    counts=Counter();ids=set();high=set();valid_ids=True
    for match in matches:
        if not isinstance(match,dict) or not isinstance(match.get("vulnerability"),dict):
            raise Stop("SCAN_MATCH_INVALID")
        vulnerability=match["vulnerability"]
        counts[KNOWN.get(str(vulnerability.get("severity","Unknown")).lower(),"Unknown")]+=1
        value=vulnerability.get("id")
        if isinstance(value,str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,159}",value):
            ids.add(value)
            if str(vulnerability.get("severity","")).lower()=="high":high.add(value)
        else:valid_ids=False
    severity={key:counts[key] for key in HISTORIC_COUNTS}
    if historical and (len(matches)!=57 or severity!=HISTORIC_COUNTS):
        raise Stop("HISTORICAL_MEDIATOR_COUNTS_MISMATCH")
    descriptor=report.get("descriptor",{})
    if not isinstance(descriptor,dict):descriptor={}
    db=descriptor.get("db") or descriptor.get("dbStatus")
    if not isinstance(db,dict):db={}
    # Grype 0.122.1 retains database identity under descriptor.db.status.
    if isinstance(db.get("status"),dict):db=db["status"]
    metadata={k:sanitized(db[k],300) if isinstance(db.get(k),str) else db[k]
              for k in ("built","checksum","schemaVersion","version","dbVersion","age","valid") if isinstance(db.get(k),(str,int))}
    return {"status":"COMPLETE","historicalImported":historical,"ref":expected_ref,
        "imageId":actual,"rawSha256":sha256(raw),"matches":len(matches),"severity":severity,
        "uniqueVulnerabilityIds":len(ids) if valid_ids else None,
        "uniqueHighIds":len(high) if valid_ids else None,
        "scannerVersion":sanitized(descriptor.get("version","UNKNOWN"),100),
        "database":metadata or {"status":"UNKNOWN_NOT_INFERRED"},"securityDisposition":"HOLD_NOT_ACCEPTED"}
def classify_oom(state):
    if not isinstance(state,dict) or not isinstance(state.get("OOMKilled"),bool):return "UNKNOWN"
    return "DOCKER_STATE_TRUE" if state["OOMKilled"] else "DOCKER_STATE_FALSE"
def not_found(result):
    return bool(re.search(r"No such (?:container|object)|not found",result.stderr,re.I))
