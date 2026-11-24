#!/usr/bin/env python3
"""Owner-approved H1A only. No cloud commands/push/install/prune/retries."""
import argparse, datetime, hashlib, json, os, pathlib, platform, shutil, subprocess, sys, time
from step05_h1a_offline_manifest_receipt import EVIDENCE_FOLDER, verify_recorded_base
P=pathlib.Path
BASE="gcr.io/distroless/nodejs24-debian13:nonroot@sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec"
SOURCE="1ece3a1e004bea7b0157bf04b6fd26f0e793d976"
EXPECTED={
 "functions/staging-marketplace/Dockerfile.c2-mediator-off":"ec36707fce197150e3f5f1b4bd1d0f30d8cbf7fa",
 "functions/staging-marketplace/Dockerfile.c2-mediator-off.dockerignore":"fc1944d7165bccc1bef5c06901841792724f751d",
 "functions/staging-marketplace/c2-mediator-off-server.mjs":"68e65e2e1cdce5994780a5588c8a02da3e1f4be7"}
MARKER=P.home()/".oldx-h1a-c2-mediator-once-20261125"
TOOLS=P.home()/"oldx-step05-scan-recovery-20261124T123515Z/tools"
parser=argparse.ArgumentParser()
parser.add_argument("--execute",action="store_true")
parser.add_argument("--confirm-h1a-resume",action="store_true",
 help="Separate owner decision required after prior H1A preflight STOP; never inferred from valid manifest")
parser.add_argument("--source-root",type=P,required=True)
a=parser.parse_args()
os.umask(0o077)
if not a.execute or not a.confirm_h1a_resume:
 print("HOLD: H1A remains BLOCKED. Source-only preflight correction is not resumed-build approval.");sys.exit(0)
stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
e=P.home()/("oldx-h1a-evidence-"+stamp);e.mkdir(mode=0o700)
report={"sourceCommit":SOURCE,"approvalCheckpoint":"4470c6b880b9c41bcb46ae835da1ccb7987cd30b",
 "status":"PREFLIGHT","build":"NOT_STARTED","sbom":"NOT_STARTED","scan":"NOT_STARTED","runtime":"NOT_STARTED",
 "evidenceDirectory":str(e),"base":BASE,"startedUtc":stamp,"noCloudOperations":True}
env={"PATH":"/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin","HOME":str(P.home()),
 "DOCKER_HOST":"unix:///var/run/docker.sock","DOCKER_CONFIG":str(e/"docker-config"),
 "SYFT_CHECK_FOR_APP_UPDATE":"false","GRYPE_CHECK_FOR_APP_UPDATE":"false",
 "GRYPE_DB_CACHE_DIR":str(e/"grype-db"),"GRYPE_DB_UPDATE_DOWNLOAD_TIMEOUT":"5m"}
(e/"docker-config").mkdir();(e/"docker-config/config.json").write_text("{}\n")
(e/"scanner-config.yaml").write_text("{}\n")  # No inherited ignore/config rules.
D=["docker","--host","unix:///var/run/docker.sock"]
container=None;stopped=False;created=False
def save():
 (e/"receipt.json").write_text(json.dumps(report,indent=2)+"\n")
def fail(reason):
 raise RuntimeError(reason)
def run(name,args,seconds=30,json_output=False):
 (e/(name+".command.json")).write_text(json.dumps(args)+"\n")
 with (e/(name+".stdout")).open("wb") as out,(e/(name+".stderr")).open("wb") as err:
  try:r=subprocess.run(args,stdout=out,stderr=err,env=env,timeout=seconds,check=False)
  except subprocess.TimeoutExpired:
   fail(name+"_TIMEOUT_NO_RETRY")
 if r.returncode:fail(name+"_EXIT_"+str(r.returncode)+"_NO_RETRY")
 data=(e/(name+".stdout")).read_text()
 return json.loads(data) if json_output else data
try:
 if sys.platform!="linux" or platform.machine() not in ("x86_64","amd64"):fail("WSL_LINUX_AMD64_REQUIRED")
 if MARKER.exists():fail("ONE_SHOT_MARKER_ALREADY_PRESENT_NO_RETRY")
 for tool in [TOOLS/"syft",TOOLS/"grype"]:
  if not tool.is_file() or not os.access(tool,os.X_OK):fail("REQUIRED_SCANNER_MISSING_"+tool.name)
 # Conservative 12GiB peak plus4GiB free reserve, both virtual and physical Windows volume.
 memory=int(next(x.split()[1] for x in P("/proc/meminfo").read_text().splitlines() if x.startswith("MemAvailable:")))*1024
 if memory<2*1024**3:fail("AVAILABLE_RAM_BELOW_2_GIB")
 disks={str(p):shutil.disk_usage(p).free for p in [P.home(),P("/mnt/c")]}
 if min(disks.values())<16*1024**3:fail("FREE_DISK_BELOW_16_GIB_NO_PRUNE")
 report["diskPlan"]={"freeBytes":disks,"peakBudgetGiB":12,"reserveGiB":4,"availableMemoryBytes":memory,
  "componentsGiB":{"baseAndBuilderLayers":4,"derivedImageAndTemporaryLayers":2,"grypeDatabaseAndDownload":3,
   "sbomReportsAndLogs":1,"temporaryCopiesAndMargin":2}}
 info=run("docker-info",D+["info","--format","{{json .}}"],json_output=True)
 if info.get("OSType")!="linux" or info.get("Architecture") not in ("x86_64","amd64"):fail("LOCAL_DOCKER_PLATFORM_MISMATCH")
 report["dockerVersion"]=run("docker-version",D+["version","--format","{{.Client.Version}} {{.Server.Version}}"]).strip()
 report["syftVersion"]=run("syft-version",[str(TOOLS/"syft"),"version"]).strip()
 report["grypeVersion"]=run("grype-version",[str(TOOLS/"grype"),"version"]).strip()
 root=a.source_root.resolve()
 context=e/"source";context.mkdir()
 manifest=[]
 for path,wanted in EXPECTED.items():
  b=(root/path).read_bytes()
  got=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
  if got!=wanted:fail("SOURCE_BLOB_DRIFT_"+path)
  target=context/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
  manifest.append({"path":path,"gitBlob":got,"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)})
 # Minimal repository-root layout contains exactly the3 approved files, no owner/credential context.
 raw=json.dumps(manifest,sort_keys=True,separators=(",",":")).encode()
 (e/"context-manifest.json").write_bytes(raw)
 report["sourceFiles"]=manifest;report["contextManifestSha256"]=hashlib.sha256(raw).hexdigest()
 # No Docker CLI manifest inspect retry: original CLI error remains unexplained.
 # Inspect the already consumed owner's private diagnostic evidence OFFLINE.
 # Exact raw SHA256 and header/receipt/marker bindings are mandatory.
 # This is content-addressability evidence only, NOT layer/config/platform proof.
 base_evidence=verify_recorded_base(P.home()/EVIDENCE_FOLDER)
 if base_evidence["manifestSha256"]!=BASE.rsplit("@",1)[-1]:
  fail("APPROVED_BASE_DIGEST_AND_EVIDENCE_DISAGREE")
 report["baseIntegrityEvidence"]=base_evidence
 report["baseManifestCliFailure"]="UNEXPLAINED_NOT_RETRIED"
 report["basePlatform"]="NOT_VERIFIED_BEFORE_BUILD_BUILDKIT_AND_RUNTIME_MUST_VERIFY"
 save()
 tag="oldx-h1a-c2-mediator-off:local-"+stamp.lower()
 container="oldx-h1a-c2-mediator-"+stamp.lower()
 # The exclusive marker consumes authority BEFORE first build. Never removed.
 with MARKER.open("x") as marker:marker.write(json.dumps({"evidence":str(e),"tag":tag,"source":SOURCE,"utc":stamp})+"\n")
 report["localTag"]=tag;report["containerName"]=container
 report["build"]="STARTED";save()
 run("build",D+["build","--platform=linux/amd64","--network=none","--no-cache",
  "--file",str(context/"functions/staging-marketplace/Dockerfile.c2-mediator-off"),"--tag",tag,str(context)],seconds=600)
 report["build"]="PASS"
 image=run("image-inspect",D+["image","inspect",tag],json_output=True)[0]
 report["localImageId"]=image["Id"];report["imageSizeBytes"]=image["Size"]
 report["imagePlatform"]=image["Os"]+"/"+image["Architecture"]
 if report["imagePlatform"]!="linux/amd64" or image["Config"]["User"]!="65532:65532":fail("IMAGE_PLATFORM_OR_USER")
 report["remoteDerivedRegistryDigest"]="NONE_NOT_PUSHED";save()
 report["sbom"]="STARTED";save()
 run("syft", [str(TOOLS/"syft"),"--config",str(e/"scanner-config.yaml"),"scan","docker:"+tag,"--scope","squashed","-o","syft-json"],seconds=600)
 sbom=e/"syft.stdout";s=json.loads(sbom.read_text())
 if not isinstance(s.get("artifacts"),list) or not s["artifacts"]:fail("INCOMPLETE_SBOM")
 if s.get("source",{}).get("type")!="image":fail("SBOM_NOT_FULL_IMAGE_SOURCE")
 report["sbomPackages"]=len(s["artifacts"]);report["sbom"]="PASS"
 report["scan"]="STARTED";save()
 run("grype",[str(TOOLS/"grype"),"--config",str(e/"scanner-config.yaml"),"sbom:"+str(sbom),"-o","json"],seconds=600)
 g=json.loads((e/"grype.stdout").read_text())
 if not isinstance(g.get("matches"),list) or not isinstance(g.get("descriptor",{}).get("db"),dict):fail("INCOMPLETE_GRYPE_REPORT_OR_DB")
 report["grypeDb"]=g["descriptor"]["db"];report["packageMatches"]=len(g["matches"])
 severities={};cves={};severe=[]
 for m in g["matches"]:
  v=m.get("vulnerability",{});artifact=m.get("artifact",{});sev=v.get("severity","Unknown");vid=v.get("id","UNKNOWN")
  severities[sev]=severities.get(sev,0)+1
  if vid.startswith("CVE-"):cves.setdefault(sev,set()).add(vid)
  if sev.upper() in ("CRITICAL","HIGH"):severe.append({"id":vid,"severity":sev,"package":artifact.get("name"),"version":artifact.get("version"),"type":artifact.get("type"),"fix":v.get("fix",{})})
 report["severityPackageMatches"]=severities;report["distinctCvesBySeverity"]={k:sorted(v) for k,v in cves.items()}
 report["criticalHighFindings"]=severe;report["scan"]="PASS_EVIDENCE_ONLY_NO_RISK_ACCEPTANCE";save()
 report["runtime"]="STARTED";save()
 # Only loopback host publish. Application has no outbound client/provider code.
 # This is a local bridge, NOT a network-egress sandbox; no cloud endpoint is contacted.
 cid=run("container-start",D+["run","--detach","--name",container,"--pull=never","--read-only",
  "--user=65532:65532","--cap-drop=ALL","--security-opt=no-new-privileges:true",
  "--memory=256m","--memory-swap=256m","--cpus=1","--pids-limit=32",
  "--publish=127.0.0.1::8080","--env=PORT=8080",tag]).strip();created=True
 ci=run("container-inspect",D+["inspect",container],json_output=True)[0]
 if ci["Image"]!=image["Id"] or ci["HostConfig"]["ReadonlyRootfs"] is not True or ci["Config"]["User"]!="65532:65532":fail("RUNTIME_IDENTITY_OR_READONLY")
 bindings=ci["NetworkSettings"]["Ports"].get("8080/tcp",[])
 if not bindings or any(b["HostIp"]!="127.0.0.1" for b in bindings):fail("NON_LOOPBACK_PUBLISH")
 smoke=r"""
const a=require('node:assert/strict'),fs=require('node:fs');
(async()=>{
 a.equal(process.versions.node.split('.')[0],'24');a.equal(process.getuid(),65532);a.equal(process.getgid(),65532);
 for(const path of ['/app/h1a-write-probe','/tmp/h1a-write-probe']){
  a.throws(()=>fs.writeFileSync(path,'probe'),e=>e.code==='EROFS');
 }
 const calls=[
 ['GET','/health',200,{}],['HEAD','/health',200,{}],
 ['POST','/api/staging/marketplace/owner',503,{'x-serverless-authorization':'Bearer SYNTHETIC_STRIPPED_IAM'}],
 ['POST','/api/staging/marketplace/list',503,{origin:'https://synthetic.invalid'}],
 ['POST','/api/staging/marketplace/detail',503,{}],['GET','/unknown',404,{}],
 ['POST','/api/staging/marketplace/save',403,{'x-oldx-gateway-request-proof':'SYNTHETIC_FORGED_PROOF'}]
 ];
 for(const [method,path,status,headers] of calls){
  const r=await fetch('http://127.0.0.1:8080'+path,{method,headers,redirect:'error',signal:AbortSignal.timeout(1500)});
  const body=await r.text();a.equal(r.status,status,path);
  a.equal(r.headers.get('access-control-allow-origin'),null);
  a.ok(!body.includes('SYNTHETIC_'));console.log(method+' '+path+' '+status+' PASS');
 }
 console.log('NODE24_UID_GID_READONLY_CORS_NO_TOKEN_LEAK: PASS');
})().catch(()=>{console.error('RUNTIME_VALIDATION_FAILED');process.exitCode=1});
"""
 time.sleep(0.3)
 run("runtime-smoke",D+["exec",container,"/nodejs/bin/node","-e",smoke],seconds=25)
 start=time.monotonic()
 run("sigterm",D+["stop","--signal=SIGTERM","--time=9",container],seconds=15);stopped=True
 state=run("container-stopped",D+["inspect",container,"--format","{{json .State}}"],json_output=True)
 report["sigtermSeconds"]=round(time.monotonic()-start,3)
 if state.get("ExitCode")!=0 or state.get("OOMKilled") or state.get("Running") or report["sigtermSeconds"]>12:fail("SIGTERM_NOT_CLEAN")
 report["runtime"]="PASS";report["status"]="PASS_WITH_LIMITS"
 report["limits"]=["No remote derived manifest/publisher provenance","CVE acceptance NOT granted","No hosted IAM/Firebase proof","Local bridge is not egress sandbox","No H1B/H2/production authority"]
except Exception as ex:
 report["stopReason"]=str(ex)
 report["status"]="STOP_PARTIAL" if MARKER.exists() else "BLOCKED_BEFORE_BUILD"
 for k in ["build","sbom","scan","runtime"]:
  if report[k]=="STARTED":report[k]="FAIL_OR_INCOMPLETE"
finally:
 if created:
  try:
   if not stopped:run("cleanup-stop-exact-container",D+["stop","--time=9",container],seconds=15)
   run("cleanup-remove-exact-container",D+["rm",container])
  except Exception as ex:report["containerCleanupError"]=str(ex)
 report["completedUtc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
 save()
 hashes={}
 for path in sorted(e.rglob("*")):
  if path.is_file() and "grype-db" not in path.parts and "docker-config" not in path.parts:
   hashes[str(path.relative_to(e))]=hashlib.sha256(path.read_bytes()).hexdigest()
 (e/"sha256-manifest.json").write_text(json.dumps(hashes,indent=2)+"\n")
 print(json.dumps({"status":report["status"],"build":report["build"],"sbom":report["sbom"],"scan":report["scan"],"runtime":report["runtime"],"stopReason":report.get("stopReason"),"evidence":str(e),"localImageId":report.get("localImageId"),"packages":report.get("sbomPackages"),"matches":report.get("packageMatches"),"severityMatches":report.get("severityPackageMatches"),"distinctCveCounts":{k:len(v) for k,v in report.get("distinctCvesBySeverity",{}).items()}},indent=2))
sys.exit(0 if report["status"]=="PASS_WITH_LIMITS" else 1)
