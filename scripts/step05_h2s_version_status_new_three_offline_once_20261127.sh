#!/usr/bin/env bash
# Step05 H2S — NEW exact KeyVersion status-verifier focused tests ONLY.
# Existing cached Node24 Docker image, pinned H2S source, no Cloud requests.
set -Eeuo pipefail
umask 077
SOURCE='5c1245658dce41a65dd78ee3c2ef4b84eb01e4a4'
IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
ROOT=''
STARTED=FALSE
PASS=FALSE
finish(){
 local rc=$?; trap - EXIT
 if [[ "$rc" -eq 0 && "$PASS" == TRUE ]];then
   echo 'OLDX_H2S_VERSION_STATUS_NEW_TESTS=PASS_3_GROUPS'
 else
   echo 'OLDX_H2S_VERSION_STATUS_NEW_TESTS=STOP'
   echo "OLDX_H2S_VERSION_STATUS_STARTED=$STARTED"
 fi
 [[ -z "$ROOT" ]] || echo "OLDX_H2S_VERSION_STATUS_EVIDENCE=$ROOT"
 echo 'OLDX_H2S_VERSION_STATUS_CLOUD_WRITES=NONE'
 echo 'OLDX_H2S_VERSION_STATUS_BUILDS_PULLS_SCANS=NONE'
 echo 'OLDX_H2S_H2_PRODUCTION=NO_GO'
 exit "$rc"
}
trap finish EXIT
[[ $(id -u) == 0 ]] || { echo STOP_NOT_ROOT; exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease || { echo STOP_NOT_WSL; exit 2; }
for bin in docker git curl tar sha256sum;do command -v "$bin" >/dev/null ||
 { echo "STOP_MISSING_$bin";exit 2;};done
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
 { echo STOP_CACHED_IMAGE_MISSING_NO_PULL;exit 2;}
NODE=$(docker image inspect "$IMAGE" --format '{{if .Config.Entrypoint}}{{index .Config.Entrypoint 0}}{{end}}')
case "$NODE" in /node|/*/node|/*/nodejs) ;; *)
  echo STOP_UNVERIFIED_NODE_ENTRYPOINT;exit 2;; esac
ROOT=$(mktemp -d /root/oldx-h2s-version-status-new.XXXXXXXX)
mkdir -p "$ROOT/src"
curl --fail --silent --show-error --retry 0 --location --max-redirs 2 \
  --max-time 150 --proto '=https' --output "$ROOT/source.tar.gz" \
  "https://codeload.github.com/yasminparmar087-ops/oldx-website/tar.gz/$SOURCE"
tar -xzf "$ROOT/source.tar.gz" -C "$ROOT/src" --strip-components=1
verify(){
 local path="$1" blob="$2"
 [[ -f "$ROOT/src/$path" && ! -L "$ROOT/src/$path" ]] ||
   { echo "STOP_SOURCE_MISSING=$path";return 2; }
 [[ "$(git hash-object "$ROOT/src/$path")" == "$blob" ]] ||
   { echo "STOP_SOURCE_HASH_MISMATCH=$path";return 2; }
}
verify scripts/c2-h2-independent-kms-version-status.mjs '58dd2c656b8e3eff60367eaa731fe6982c97ac23'
verify scripts/c2-h2-independent-kms-version-status.test.mjs 'd12cf0356953ce5d152b4b8798f077c1adc4f9d5'
verify scripts/c2-kms-request-signing.mjs '0a37278834629ab16d6baf4adbf89099cf687348'
chmod -R a+rX "$ROOT/src"
container(){
 docker run --rm --pull never --network none --read-only --cap-drop ALL \
 --security-opt no-new-privileges --pids-limit 64 --memory 512m --cpus 1 \
 --user 65532:65532 \
 --mount "type=bind,src=$ROOT/src,dst=/work,readonly" \
 --workdir /work --entrypoint "$NODE" "$IMAGE" "$@"
}
container -e "const [a,b]=process.versions.node.split('.').map(Number);
 console.log('OLDX_H2S_VERSION_STATUS_NODE='+process.versions.node);
 if(a<24||(a===24&&b<12))process.exit(44);" ||
 { echo STOP_NODE_BELOW_24_12;exit 2; }
printf 'NEW_VERSION_STATUS_TEST_ATTEMPT=%s\n' "$SOURCE" > "$ROOT/one-shot-attempt.marker"
echo "OLDX_H2S_VERSION_STATUS_SOURCE=$SOURCE"
echo 'OLDX_H2S_ONLY_TEST=scripts/c2-h2-independent-kms-version-status.test.mjs'
STARTED=TRUE
container --test --test-reporter=tap \
 scripts/c2-h2-independent-kms-version-status.test.mjs \
 2>&1 | tee "$ROOT/version-status-new-three.log"
for expected in '# tests 3' '# pass 3' '# fail 0' '# skipped 0' '# todo 0';do
 grep -Fxq "$expected" "$ROOT/version-status-new-three.log" ||
   { echo "STOP_TAP_MISMATCH=$expected";exit 2; }
done
sha256sum "$ROOT/version-status-new-three.log" |
 awk '{print "OLDX_H2S_VERSION_STATUS_LOG_SHA256="$1}'
PASS=TRUE
