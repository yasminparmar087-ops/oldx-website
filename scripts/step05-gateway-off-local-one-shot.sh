#!/usr/bin/env bash
# OLDX Step05: single NO-CLOUD local build/SBOM/security scan for NEW OFF Gateway.
set -Eeuo pipefail
umask 077
fatal(){ printf 'STOP: %s\n' "$*" >&2; exit 1; }
for tool in git docker python3 curl sha256sum; do command -v "$tool" >/dev/null || fatal "Missing $tool: no paid Cloud Build fallback"; done
ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || fatal 'Not an OLDX checkout'
cd "$ROOT"
test "$(git branch --show-current)" = security-hardening-review || fatal 'Review branch ONLY'
test "$(git config --get remote.origin.url)" = 'https://github.com/yasminparmar087-ops/oldx-website.git' || fatal 'Use the fresh public OLDX checkout'
for pair in \
 'functions/staging-marketplace/cloud-run-gateway-off-server.mjs:25d2679bd4ea970c8b8a32a778fb26eb347bcdd6' \
 'functions/staging-marketplace/Dockerfile.gateway-off:f1bbfc65c0f593c2f54a338b323b7f7cd4dbdbc1' \
 'functions/staging-marketplace/Dockerfile.gateway-off.dockerignore:53da9bb7a2d12b143feae9de71a245ac31693111'; do
 path=$(printf '%s' "$pair" | cut -d: -f1); expected=$(printf '%s' "$pair" | cut -d: -f2)
 test "$(git rev-parse "HEAD:$path")" = "$expected" || fatal "Source changed: $path"
 test -z "$(git status --porcelain -- "$path")" || fatal "Dirty source: $path"
done
docker info >/dev/null 2>&1 || fatal 'Local Docker daemon missing; no remote builder fallback'
free_kib=$(df -Pk /tmp | awk 'NR==2 {print $4}')
test "$free_kib" -ge 4194304 || fatal 'Less than 4GiB scratch'
test "$(uname -m)" = x86_64 || fatal 'Requires Linux AMD64 host'
OUT="$HOME/oldx-step05-gateway-evidence-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -m 700 "$OUT" || fatal 'Evidence directory failed'
TMP=$(mktemp -d /tmp/oldx-step05-image.XXXXXXXX)
IMAGE="oldx-step05-gateway-off:one-shot-$$"
CONTAINER="oldx-step05-off-$$"
cleanup(){ docker rm -f "$CONTAINER" >/dev/null 2>&1 || true; docker image rm "$IMAGE" >/dev/null 2>&1 || true; rm -rf "$TMP"; }
trap cleanup EXIT
printf 'HEAD=%s\nEVIDENCE=%s\n' "$(git rev-parse HEAD)" "$OUT"
printf 'STATUS=ATTEMPT_STARTED\nHEAD=%s\n' "$(git rev-parse HEAD)" > "$OUT/summary.txt"
LOCK="$HOME/.oldx-step05-new-gateway-image-build-consumed"
( set -C; printf '%s\n' "$(date -u +%FT%TZ)" > "$LOCK" ) 2>/dev/null || fatal 'One-shot approval already consumed; do not repeat'
# Only NEW Gateway image. No Cloud Build, Artifact Registry, Firebase or old A8.
DOCKER_BUILDKIT=1 docker build --platform linux/amd64 --no-cache --network none \
 -f functions/staging-marketplace/Dockerfile.gateway-off -t "$IMAGE" . > "$OUT/build.log" 2>&1 || fatal "Build failed: $OUT/build.log"
image_id=$(docker image inspect -f '{{.Id}}' "$IMAGE")
platform=$(docker image inspect -f '{{.Os}}/{{.Architecture}}' "$IMAGE")
user=$(docker image inspect -f '{{.Config.User}}' "$IMAGE")
test "$platform" = linux/amd64 && test "$user" = '65532:65532' || fatal 'Unexpected platform/user'
printf 'DERIVED_LOCAL_IMAGE_ID=%s\nPLATFORM=%s\nUSER=%s\n' "$image_id" "$platform" "$user" >> "$OUT/summary.txt"
docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges \
 --pids-limit 64 --memory 256m --entrypoint /nodejs/bin/node "$IMAGE" -e '
const fs=require("node:fs"),assert=require("node:assert/strict");
assert.equal(process.getuid(),65532);
assert.equal(process.versions.node.split(".")[0],"24");
assert.equal(fs.statSync("/app/server.mjs").mode & 0o222,0);
console.log("LINUX_NODE24_NONROOT_READONLY=PASS");
' | tee "$OUT/node24-runtime.txt"
docker run -d --name "$CONTAINER" --network none --read-only --cap-drop ALL \
 --security-opt no-new-privileges --pids-limit 64 --memory 256m \
 -e PORT=8080 -e OLDX_PRODUCT_READ_ACTIVATE_STAGING=true \
 -e OLDX_STAGING_PUBLICATION_ENABLED=true "$IMAGE" >/dev/null || fatal 'OFF container start failed'
docker exec "$CONTAINER" /nodejs/bin/node -e '
(async()=>{
 const assert=require("node:assert/strict");
 let ready=false;
 for(let i=0;i<20;i++){
  try{const check=await fetch("http://127.0.0.1:8080/healthz",{signal:AbortSignal.timeout(250)});if(check.status===200){ready=true;break;}}catch{}
  await new Promise(resolve=>setTimeout(resolve,100));
 }
 assert.equal(ready,true,"OFF gateway never became ready");
 for(const [path,expected,method] of [["/healthz",200,"GET"],["/api/staging/marketplace/save",503,"POST"],["/api/staging/marketplace/list",503,"POST"]]){
  const r=await fetch("http://127.0.0.1:8080"+path,{method,signal:AbortSignal.timeout(2000),headers:{authorization:"Bearer fake.fake.fake","x-serverless-authorization":"Bearer fake.fake.fake"},...(method==="POST"?{body:"{}"}:{})});
  assert.equal(r.status,expected,path);
  if(expected===503)assert.equal((await r.json()).error.code,"ENFORCEMENT_UNAVAILABLE");
 }
 console.log("OFF_ONLY_LINUX_CONTAINER=PASS");
})().catch(e=>{console.error(e.message);process.exitCode=1});
' | tee "$OUT/off-scenario.txt"
docker stop --time 8 "$CONTAINER" >/dev/null || fatal 'SIGTERM stop failed'
test "$(docker inspect -f '{{.State.ExitCode}}' "$CONTAINER")" = 0 || fatal 'SIGTERM exit code nonzero'
test "$(docker inspect -f '{{.State.OOMKilled}}' "$CONTAINER")" = false || fatal 'Container OOM'
echo 'LINUX_SIGTERM_EXIT=PASS' | tee "$OUT/shutdown.txt"
# Published release artifacts with exact GitHub-advertised SHA256 pins, no curl|bash.
curl -fLsS --retry 0 --connect-timeout 10 --max-time 90 -o "$TMP/syft.tgz" \
 https://github.com/anchore/syft/releases/download/v1.57.1/syft_1.57.1_linux_amd64.tar.gz || fatal 'Syft download blocked'
printf '%s  %s\n' bf52519eb57f675d47c07d43213cb6dff6449f3d6d1147ff6701ed91f44eef0c "$TMP/syft.tgz" | sha256sum -c - || fatal 'Syft checksum mismatch'
tar -xzf "$TMP/syft.tgz" -C "$TMP" syft || fatal 'Syft extraction failed'
chmod 700 "$TMP/syft"
timeout 180 "$TMP/syft" "docker:$IMAGE" -o cyclonedx-json > "$OUT/sbom.cdx.json" || fatal 'New image SBOM failed'
curl -fLsS --retry 0 --connect-timeout 10 --max-time 90 -o "$TMP/grype.tgz" \
 https://github.com/anchore/grype/releases/download/v0.121.3/grype_0.121.3_linux_amd64.tar.gz || fatal 'Grype download blocked'
printf '%s  %s\n' e9da18cc1429e786722e32161288103600efffd8e483c90761f90485bd1bec85 "$TMP/grype.tgz" | sha256sum -c - || fatal 'Grype checksum mismatch'
tar -xzf "$TMP/grype.tgz" -C "$TMP" grype || fatal 'Grype extraction failed'
chmod 700 "$TMP/grype"
export GRYPE_DB_CACHE_DIR="$TMP/grype-db"
timeout 180 "$TMP/grype" "sbom:$OUT/sbom.cdx.json" -o json > "$OUT/grype-report.json" || fatal 'New image Grype scan unavailable'
python3 - "$OUT/grype-report.json" "$OUT/summary.txt" <<'PY'
import collections,json,sys
scan=json.load(open(sys.argv[1])); matches=scan.get('matches',[])
sev=collections.Counter(m.get('vulnerability',{}).get('severity','UNKNOWN') for m in matches)
ids=sorted({m.get('vulnerability',{}).get('id') for m in matches if m.get('vulnerability',{}).get('severity') in ('High','Critical') and m.get('vulnerability',{}).get('id')})
summary=f"SCAN_MATCHES={len(matches)}\nSCAN_SEVERITIES={dict(sev)}\nSCAN_DISTINCT_HIGH_CRITICAL_IDS={len(ids)}\nSCAN_HIGH_CRITICAL_IDS={','.join(ids)}\nSTATUS=LOCAL_BUILD_SCAN_COMPLETE_NOT_DEPLOY_APPROVAL\n"
print(summary,end='');open(sys.argv[2],'a').write(summary)
PY
sha256sum "$OUT/sbom.cdx.json" "$OUT/grype-report.json" > "$OUT/report-sha256.txt"
printf 'NO_DEPLOY_NO_PUSH_NO_IAM_NO_FIRESTORE=TRUE\n' >> "$OUT/summary.txt"
echo "DONE: NEW local image only. Evidence directory: $OUT"
