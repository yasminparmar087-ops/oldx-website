#!/usr/bin/env bash
# OLDX Step05: user-approved ONE free LOCAL Windows WSL2 OFF Gateway build + Syft/Grype.
# Never invoke Cloud Build, Registry push, deployment, Firebase, IAM or old A8.
set -Eeuo pipefail
umask 077
fatal(){ printf 'STOP: %s\n' "$*" >&2; exit 1; }
log(){ printf '%s\n' "$*"; }
for tool in bash git docker curl sha256sum tar python3 timeout df awk; do
 command -v "$tool" >/dev/null || fatal "Missing $tool (no automatic installation)"
done
[[ "$(uname -s)" == Linux && "$(uname -m)" == x86_64 ]] || fatal 'Linux AMD64 only'
grep -qiE 'microsoft|wsl' /proc/sys/kernel/osrelease || fatal 'This one-shot is for approved WSL2 only'
[[ -d /mnt/c ]] || fatal 'Windows C: mount missing; cannot validate host disk reserve'
ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || fatal 'Run inside a fresh OLDX clone'
cd "$ROOT"
[[ "$(git branch --show-current)" == security-hardening-review ]] || fatal 'Review branch only'
[[ "$(git config --get remote.origin.url)" == 'https://github.com/yasminparmar087-ops/oldx-website.git' ]] || fatal 'Wrong GitHub remote'
for pair in \
 'functions/staging-marketplace/cloud-run-gateway-off-server.mjs:25d2679bd4ea970c8b8a32a778fb26eb347bcdd6' \
 'functions/staging-marketplace/Dockerfile.gateway-off:f1bbfc65c0f593c2f54a338b323b7f7cd4dbdbc1' \
 'functions/staging-marketplace/Dockerfile.gateway-off.dockerignore:53da9bb7a2d12b143feae9de71a245ac31693111'; do
 path=${pair%%:*}; expected=${pair##*:}
 [[ "$(git rev-parse "HEAD:$path")" == "$expected" ]] || fatal "Changed/unverified source: $path"
 [[ -z "$(git status --porcelain -- "$path")" ]] || fatal "Dirty source: $path"
done
[[ "$(docker context show)" == default ]] || fatal 'Non-default Docker context: remote builder not allowed'
[[ -z "${DOCKER_HOST:-}" ]] || fatal 'DOCKER_HOST override not permitted'
docker info --format '{{.OSType}}/{{.Architecture}}' 2>/dev/null | grep -Eq '^linux/(x86_64|amd64)$' || fatal 'Local Linux AMD64 Docker daemon unavailable'
free_kib=$(df -Pk /tmp | awk 'NR==2 {print $4}')
c_kib=$(df -Pk /mnt/c | awk 'NR==2 {print $4}')
[[ "$free_kib" =~ ^[0-9]+$ && "$c_kib" =~ ^[0-9]+$ ]] || fatal 'Unable to read free disk'
(( free_kib >= 8388608 && c_kib >= 10485760 )) || fatal 'Need >=8GiB WSL scratch and >=10GiB free on Windows C:; STOP without cleanup'
avail_mem=$(awk '/MemAvailable:/ {print $2}' /proc/meminfo)
[[ "$avail_mem" =~ ^[0-9]+$ ]] && (( avail_mem >= 1572864 )) || fatal 'Need >=1.5GiB available Linux RAM'
OUT="$HOME/oldx-step05-laptop-evidence-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -m 700 "$OUT" || fatal 'Unable to create evidence folder'
TMP=$(mktemp -d /tmp/oldx-step05-wslscan.XXXXXXXX) || fatal 'Unable to allocate scratch'
IMAGE="oldx-step05-gateway-off:wsl-once-$(date -u +%Y%m%d)-$$"
CONTAINER="oldx-step05-wsl-off-$$"
LOCK="$HOME/.oldx-step05-laptop-one-shot-consumed"
STATUS=PRECHECK
cleanup(){
 local exit_code=$?
 trap - EXIT
 docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
 # Preserve the new local image if a scan fails; NO repeat build required for diagnosis.
 rm -rf -- "$TMP"
 if (( exit_code != 0 )); then
  printf 'STATUS=FAILED_AT_%s\n' "$STATUS" >> "$OUT/summary.txt" 2>/dev/null || true
  printf 'STOP: %s. Image remains local if built; do NOT rerun this one-shot.\n' "$STATUS" >&2
  printf 'EVIDENCE=%s\n' "$OUT" >&2
 fi
 exit "$exit_code"
}
trap cleanup EXIT
printf 'SOURCE_SHA=%s\nEVIDENCE=%s\nMODE=WSL2_LOCAL_ONLY\n' "$(git rev-parse HEAD)" "$OUT" | tee "$OUT/summary.txt"
printf 'C_DRIVE_AVAILABLE_GIB=%s\nWSL_AVAILABLE_GIB=%s\n' "$((c_kib/1048576))" "$((free_kib/1048576))" >> "$OUT/summary.txt"
( set -C; printf '%s\n' "$(date -u +%FT%TZ)" > "$LOCK" ) 2>/dev/null || fatal 'Laptop one-shot already consumed: STOP; no auto repeat'
STATUS=DOCKER_BUILD
log 'STEP: one NEW OFF gateway image build (no A8, no push)'
DOCKER_BUILDKIT=1 docker build --platform linux/amd64 --no-cache --network none \
 -f functions/staging-marketplace/Dockerfile.gateway-off -t "$IMAGE" . > "$OUT/build.log" 2>&1 || fatal "Build failed; see $OUT/build.log"
IMAGE_ID=$(docker image inspect --format '{{.Id}}' "$IMAGE")
PLATFORM=$(docker image inspect --format '{{.Os}}/{{.Architecture}}' "$IMAGE")
USER=$(docker image inspect --format '{{.Config.User}}' "$IMAGE")
[[ "$PLATFORM" == linux/amd64 && "$USER" == 65532:65532 ]] || fatal 'Wrong image platform or user'
printf 'DERIVED_LOCAL_IMAGE_ID=%s\nPLATFORM=%s\nUSER=%s\n' "$IMAGE_ID" "$PLATFORM" "$USER" | tee -a "$OUT/summary.txt"
STATUS=NODE24_OFF_SMOKE
log 'STEP: NEW Gateway Linux Node24 nonroot and OFF-only validation'
docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges \
 --pids-limit 64 --memory 256m --entrypoint /nodejs/bin/node "$IMAGE" -e '
const assert=require("node:assert/strict"),fs=require("node:fs");
assert.equal(process.getuid(),65532);
assert.equal(process.versions.node.split(".")[0],"24");
assert.equal(fs.statSync("/app/server.mjs").mode&0o222,0);
console.log("LINUX_NODE24_NONROOT_READONLY=PASS");
' > "$OUT/runtime.log" 2>&1 || fatal 'Node24 runtime check failed'
docker run -d --name "$CONTAINER" --network none --read-only --cap-drop ALL \
 --security-opt no-new-privileges --pids-limit 64 --memory 256m \
 -e PORT=8080 -e OLDX_PRODUCT_READ_ACTIVATE_STAGING=true \
 -e OLDX_STAGING_PUBLICATION_ENABLED=true "$IMAGE" > "$OUT/container.id" 2> "$OUT/container.stderr.log" || fatal 'OFF container did not start'
docker exec "$CONTAINER" /nodejs/bin/node -e '
(async()=>{
 const assert=require("node:assert/strict");
 let ready=false;
 for(let i=0;i<20;i++){
  try{const r=await fetch("http://127.0.0.1:8080/healthz",{signal:AbortSignal.timeout(200)});if(r.status===200){ready=true;break}}catch{}
  await new Promise(resolve=>setTimeout(resolve,100));
 }
 assert.equal(ready,true,"Gateway never ready");
 for(const [p,method,status] of [["/healthz","GET",200],["/api/staging/marketplace/save","POST",503],["/api/staging/marketplace/list","POST",503]]){
  const r=await fetch("http://127.0.0.1:8080"+p,{method,headers:{authorization:"Bearer fake.fake.fake",'"'"'x-serverless-authorization'"'"':"Bearer fake.fake.fake"},...(method==="POST"?{body:"{}"}:{}) ,signal:AbortSignal.timeout(1500)});
  assert.equal(r.status,status,p);
  if(status===503)assert.equal((await r.json()).error.code,"ENFORCEMENT_UNAVAILABLE");
 }
 console.log("OFF_ONLY_LINUX_CONTAINER=PASS");
})().catch(e=>{console.error(e.message);process.exitCode=1});
' > "$OUT/off.log" 2>&1 || fatal 'OFF HTTP routes failed'
docker stop --time 8 "$CONTAINER" > "$OUT/stop.log" 2>&1 || fatal 'SIGTERM stop failed'
[[ "$(docker inspect -f '{{.State.ExitCode}}' "$CONTAINER")" == 0 ]] || fatal 'SIGTERM exit was nonzero'
[[ "$(docker inspect -f '{{.State.OOMKilled}}' "$CONTAINER")" == false ]] || fatal 'Container was OOM-killed'
printf 'LINUX_NODE24_NONROOT_READONLY=PASS\nOFF_ONLY_HTTP=PASS\nLINUX_SIGTERM=PASS\n' | tee -a "$OUT/summary.txt"
STATUS=DOCKER_ARCHIVE
log 'STEP: export the exact new image to a local tar (not push)'
docker save -o "$TMP/image.tar" "$IMAGE" > "$OUT/docker-save.stdout.log" 2> "$OUT/docker-save.stderr.log" || fatal 'Local image archive save failed'
[[ -s "$TMP/image.tar" ]] || fatal 'Empty local image archive'
sha256sum "$TMP/image.tar" > "$OUT/image-archive.sha256"
STATUS=SYFT_DOWNLOAD
log 'STEP: download and checksum-verify Syft release'
curl -fLsS --retry 0 --connect-timeout 10 --max-time 120 \
 -o "$TMP/syft.tgz" https://github.com/anchore/syft/releases/download/v1.57.1/syft_1.57.1_linux_amd64.tar.gz \
 > "$OUT/syft-download.stdout.log" 2> "$OUT/syft-download.stderr.log" || fatal 'Syft download failed'
printf '%s  %s\n' bf52519eb57f675d47c07d43213cb6dff6449f3d6d1147ff6701ed91f44eef0c "$TMP/syft.tgz" | sha256sum -c - > "$OUT/syft.sha256.log" || fatal 'Syft checksum mismatch'
tar -xzf "$TMP/syft.tgz" -C "$TMP" syft || fatal 'Syft extraction failed'
chmod 700 "$TMP/syft"
STATUS=SYFT_SBOM
log 'STEP: new-image SBOM from local Docker archive; preserve stderr'
export TMPDIR="$TMP" SYFT_CHECK_FOR_APP_UPDATE=false GOMAXPROCS=2 GOMEMLIMIT=1400MiB
mkdir -p "$TMP/syft-cache"
timeout --signal=TERM --kill-after=5s 300 "$TMP/syft" "docker-archive:$TMP/image.tar" \
 -o "syft-json=$OUT/sbom.syft.json" -o "cyclonedx-json=$OUT/sbom.cdx.json" \
 > "$OUT/syft.stdout.log" 2> "$OUT/syft.stderr.log" || fatal 'Syft SBOM failed; inspect syft.stderr.log, do not rebuild'
python3 - "$OUT/sbom.syft.json" "$OUT/sbom.cdx.json" <<'PY'
import json,sys,os
assert all(os.path.getsize(p)>0 for p in sys.argv[1:]), 'Zero-byte SBOM'
syft=json.load(open(sys.argv[1])); cdx=json.load(open(sys.argv[2]))
assert isinstance(syft.get('artifacts'),list),'Not a Syft JSON SBOM'
assert cdx.get('bomFormat')=='CycloneDX','Not CycloneDX'
print('SYFT_SBOM_VALID=PASS')
PY
printf 'SYFT_SBOM_VALID=PASS\n' | tee -a "$OUT/summary.txt"
STATUS=GRYPE_DOWNLOAD
log 'STEP: download and checksum-verify Grype release'
curl -fLsS --retry 0 --connect-timeout 10 --max-time 120 \
 -o "$TMP/grype.tgz" https://github.com/anchore/grype/releases/download/v0.121.3/grype_0.121.3_linux_amd64.tar.gz \
 > "$OUT/grype-download.stdout.log" 2> "$OUT/grype-download.stderr.log" || fatal 'Grype download failed'
printf '%s  %s\n' e9da18cc1429e786722e32161288103600efffd8e483c90761f90485bd1bec85 "$TMP/grype.tgz" | sha256sum -c - > "$OUT/grype.sha256.log" || fatal 'Grype checksum mismatch'
tar -xzf "$TMP/grype.tgz" -C "$TMP" grype || fatal 'Grype extraction failed'
chmod 700 "$TMP/grype"
STATUS=GRYPE_SCAN
log 'STEP: one Grype vulnerability scan of new SBOM (never old A8)'
export GRYPE_DB_CACHE_DIR="$TMP/grype-db" GRYPE_CHECK_FOR_APP_UPDATE=false
mkdir -p "$GRYPE_DB_CACHE_DIR"
timeout --signal=TERM --kill-after=5s 300 "$TMP/grype" "sbom:$OUT/sbom.syft.json" -o json \
 > "$OUT/grype-report.json" 2> "$OUT/grype.stderr.log" || fatal 'Grype scan failed; inspect grype.stderr.log, do not rebuild'
python3 - "$OUT/grype-report.json" "$OUT/summary.txt" <<'PY'
import collections,json,sys,os
p=sys.argv[1];assert os.path.getsize(p)>0,'Empty Grype report'
data=json.load(open(p));m=data.get('matches');assert isinstance(m,list),'Invalid Grype matches'
sev=collections.Counter(v.get('vulnerability',{}).get('severity','UNKNOWN') for v in m)
ids=sorted({v.get('vulnerability',{}).get('id') for v in m if v.get('vulnerability',{}).get('severity') in ('High','Critical') and v.get('vulnerability',{}).get('id')})
s=f"GRYPE_SCAN=VALID\nMATCHES={len(m)}\nSEVERITIES={dict(sev)}\nDISTINCT_HIGH_CRITICAL_CVE_IDS={len(ids)}\nHIGH_CRITICAL_CVE_IDS={','.join(ids)}\n"
print(s);open(sys.argv[2],'a').write(s)
PY
sha256sum "$OUT/sbom.syft.json" "$OUT/sbom.cdx.json" "$OUT/grype-report.json" > "$OUT/reports.sha256"
STATUS=COMPLETE
printf 'STATUS=BUILD_AND_SCAN_COMPLETED_NOT_HOSTED_OR_RELEASE_APPROVAL\nNO_CLOUD_PUSH_DEPLOY_IAM_FIREBASE=TRUE\n' | tee -a "$OUT/summary.txt"
log "DONE: evidence=$OUT; local image deliberately RETAINED for scan-only diagnosis/owner review"
