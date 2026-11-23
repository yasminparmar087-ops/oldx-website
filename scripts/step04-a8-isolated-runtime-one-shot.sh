#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
image='asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'
mark="$HOME/.oldx-a8-runtime-isolated-once-2506826f"
work='/tmp/oldx-a8-runtime-isolated-once-2506826f'
name='oldx-a8-isolated-2506826f'
started=0
cleanup() {
  if [ "$started" -eq 1 ]; then
    docker stop --time 2 "$name" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

if [ "$(uname -s)" != Linux ] || [ "$(uname -m)" != x86_64 ]; then
  echo 'STOP_A8_RUNTIME_LINUX_AMD64_ONLY'; exit 1
fi
if [ -e "$mark" ] || [ -e "$work" ]; then
  echo 'STOP_A8_RUNTIME_ALREADY_ATTEMPTED_NO_RETRY'; exit 1
fi
if ! command -v docker >/dev/null 2>&1 || ! command -v timeout >/dev/null 2>&1; then
  echo 'STOP_A8_RUNTIME_DOCKER_OR_TIMEOUT_MISSING'; exit 1
fi
if ! docker info >/dev/null 2>&1; then
  echo 'STOP_A8_RUNTIME_DOCKER_ENGINE_UNAVAILABLE'; exit 1
fi
if docker container inspect "$name" >/dev/null 2>&1; then
  echo 'STOP_A8_RUNTIME_CONTAINER_NAME_IN_USE'; exit 1
fi
root="$(docker info --format '{{.DockerRootDir}}' 2>/dev/null)"
if [ -z "$root" ] || [ ! -d "$root" ]; then
  echo 'STOP_A8_RUNTIME_DOCKER_STORAGE_UNVERIFIED'; exit 1
fi
free_mib="$(df -Pk "$root" | awk 'NR==2 {print int($4/1024)}')"
if ! [[ "$free_mib" =~ ^[0-9]+$ ]] || [ "$free_mib" -lt 2500 ]; then
  echo 'STOP_A8_RUNTIME_DOCKER_STORAGE_TOO_SMALL'; exit 1
fi
if ! mkdir -m 700 "$work"; then
  echo 'STOP_A8_RUNTIME_SCRATCH_CREATE_FAILED'; exit 1
fi
if ! mkdir -m 700 "$mark"; then
  echo 'STOP_A8_RUNTIME_MARKER_CREATE_FAILED'; exit 1
fi
echo 'A8_RUNTIME_ONESHOT_ATTEMPT=CREATED'
echo 'A8_RUNTIME_SUBJECT=EXACT_IMMUTABLE_NEW_DIGEST'
if ! timeout 600 docker pull --platform linux/amd64 "$image" >"$work/pull.log" 2>&1; then
  echo 'STOP_A8_RUNTIME_EXACT_DIGEST_PULL_FAILED_NO_RETRY'; exit 1
fi
echo 'A8_RUNTIME_EXACT_DIGEST_PULL=PASS'
if ! docker image inspect --format '{{range .RepoDigests}}{{println .}}{{end}}' "$image" | grep -Fqx "$image"; then
  echo 'STOP_A8_RUNTIME_IMAGE_REPODIGEST_UNVERIFIED'; exit 1
fi
echo 'A8_RUNTIME_REGISTRY_DIGEST=PASS'
user="$(docker image inspect --format '{{.Config.User}}' "$image")"
if [ "$user" != 'appuser' ]; then
  echo 'STOP_A8_RUNTIME_CONFIG_USER_NOT_APPUSER'; exit 1
fi
echo 'A8_RUNTIME_CONFIG_USER=APPUSER'
if ! docker run --rm -d --pull never --platform linux/amd64 \
  --name "$name" --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --pids-limit 64 --memory 256m --cpus 0.5 \
  --tmpfs /tmp:rw,nosuid,nodev,size=16m \
  --env OLDX_PRODUCT_READ_ACTIVATE_STAGING=false \
  --env OLDX_PRODUCT_READ_STAGING_ADC=false \
  "$image" >"$work/run.cid" 2>"$work/run.err"; then
  echo 'STOP_A8_RUNTIME_SANDBOX_START_FAILED'; exit 1
fi
started=1
net="$(docker inspect --format '{{.HostConfig.NetworkMode}}' "$name")"
readonly="$(docker inspect --format '{{.HostConfig.ReadonlyRootfs}}' "$name")"
if [ "$net" != none ] || [ "$readonly" != true ]; then
  echo 'STOP_A8_RUNTIME_ISOLATION_MISMATCH'; exit 1
fi
echo 'A8_RUNTIME_NETWORK=NONE'
echo 'A8_RUNTIME_ROOTFS=READ_ONLY'
if ! docker exec "$name" /usr/bin/node -e '
const http = require("node:http");
const pause = n => new Promise(r => setTimeout(r,n));
async function local(path,method) {
 for(let i=0;i<12;i++) {
  try { return await new Promise((resolve,reject) => {
   const req=http.request({hostname:"127.0.0.1",port:8080,path,method,timeout:1200},res=>{res.resume();res.on("end",()=>resolve(res.statusCode));});
   req.on("error",reject);req.on("timeout",()=>req.destroy(new Error("TIMEOUT")));req.end();
  });} catch {await pause(350);}
 }
 throw Error("A8_LOCAL_SERVER_UNAVAILABLE");
}
(async()=>{
 const uid=process.getuid?.();
 const health=await local("/healthz","GET");
 const owner=await local("/api/staging/marketplace/owner","POST");
 console.log("A8_RUNTIME_NONROOT="+(Number.isInteger(uid)&&uid>0));
 console.log("A8_RUNTIME_HEALTH_STATUS="+health);
 console.log("A8_RUNTIME_DISABLED_OWNER_STATUS="+owner);
 console.log("A8_RUNTIME_FIREBASE_NETWORK=ISOLATED_NOT_TESTED");
 if(!(Number.isInteger(uid)&&uid>0&&health===200&&owner===503))process.exitCode=1;
})().catch(()=>{console.log("STOP_A8_RUNTIME_LOOPBACK_CHECK_FAILED");process.exitCode=1;});
' >"$work/loopback.out" 2>"$work/loopback.err"; then
  echo 'STOP_A8_RUNTIME_LOOPBACK_GUARD_FAILED'; exit 1
fi
cat "$work/loopback.out"
echo 'A8_RUNTIME_ISOLATED_LOCAL_TEST=PASS_WITH_LIMITS'
echo 'A8_RUNTIME_REAL_IAM_OTHER_DB=NOT_TESTED'
echo 'A8_CLOUD_RUN_DEPLOY=NONE'
echo 'A8_BUILD_SCAN_SLSA_RERUN=NONE'
echo 'A8_STEP04=HOLD_PENDING_G4_G8_AND_RISK'
