#!/usr/bin/env bash
# Distinct NEW OFF-only H2U local listening HTTP smoke.
# Uses existing accepted 65-file Owner-local source and manifest.
# Cached Node24 image only; Docker network:none (loopback), no published port.
# No earlier tests/scanner/linker, no Cloud/API/IAM/Firestore/KMS, no build/pull.
set -Eeuo pipefail
umask 077
OLD='/root/oldx-h2u-import-closure.2oCNZVHV'
IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
OLD_HASH='12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc'
MARK='/root/.oldx-step05-h2u-off-listener-smoke-once-20261127'
TMP=''
STARTED=FALSE
PASS=FALSE
finish(){
 local rc=$?
 trap - EXIT
 if [[ "$rc" -eq 0 && "$PASS" == TRUE ]];then
   echo 'OLDX_H2U_OFF_LISTENER_ONE_SHOT=PASS_WITH_LIMITS'
 else
   echo 'OLDX_H2U_OFF_LISTENER_ONE_SHOT=STOP'
   echo "OLDX_H2U_OFF_LISTENER_STARTED=$STARTED"
 fi
 [[ -z "$TMP" ]] || echo "OLDX_H2U_OFF_LISTENER_EVIDENCE=$TMP"
 echo 'OLDX_H2U_OFF_LISTENER_CLOUD_WRITES=NONE'
 echo 'OLDX_H2U_OFF_LISTENER_BUILDS_PULLS_SCANS=NONE'
 echo 'OLDX_H2U_H2_PRODUCTION=NO_GO'
 exit "$rc"
}
trap finish EXIT
[[ "$(id -u)" == 0 ]] || { echo STOP_ROOT_REQUIRED;exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease ||
 { echo STOP_WSL_REQUIRED;exit 2; }
for bin in git curl docker sha256sum grep;do
 command -v "$bin" >/dev/null ||
 { echo "STOP_MISSING_TOOL=$bin";exit 2; }
done
[[ ! -e "$MARK" && ! -L "$MARK" ]] ||
 { echo STOP_ONE_SHOT_ALREADY_CONSUMED;exit 2; }
[[ -d "$OLD/source" && ! -L "$OLD/source" &&
   -f "$OLD/source-closure.json" && ! -L "$OLD/source-closure.json" ]] ||
 { echo STOP_PREVIOUS_SOURCE_OR_MANIFEST_MISSING;exit 2; }
echo "$OLD_HASH  $OLD/source-closure.json" |
 sha256sum --check --status ||
 { echo STOP_PREVIOUS_MANIFEST_DRIFT;exit 2; }
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
 { echo STOP_CACHED_IMAGE_MISSING;exit 2; }
NODE=$(docker image inspect "$IMAGE" \
 --format '{{if .Config.Entrypoint}}{{index .Config.Entrypoint 0}}{{end}}')
case "$NODE" in /node|/*/node|/*/nodejs) ;; *)
 echo STOP_IMAGE_NODE_UNVERIFIED;exit 2;;esac
TMP=$(mktemp -d /root/oldx-h2u-off-listener.XXXXXXXX)
mkdir -p "$TMP/audit"
curl --fail --silent --show-error --retry 0 --max-redirs 0 \
 --max-time 40 --proto '=https' \
 --output "$TMP/audit/smoke.mjs" \
 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/ff4648fff1d2ba7d0c814e2f27c5f67c3af65f70/scripts/c2-h2u-new-off-http-local-listener-smoke-once_20261127.mjs'
[[ "$(git hash-object "$TMP/audit/smoke.mjs")" == \
 '6d03c523abbc1550f0260749ce878d5836d5cf79' ]] ||
 { echo STOP_NEW_SMOKE_SOURCE_HASH_MISMATCH;exit 2; }
cp -- "$OLD/source-closure.json" "$TMP/manifest.json"
chmod 755 "$TMP/audit"
chmod 644 "$TMP/audit/smoke.mjs" "$TMP/manifest.json"
( set -C
 printf 'ONE_NEW_OFF_LOCAL_HTTP_SMOKE_CONSUMED=TRUE\nMANIFEST_SHA256=%s\n' \
 "$OLD_HASH" > "$MARK"
) || { echo STOP_NEW_MARKER_CONFLICT;exit 2; }
echo 'OLDX_H2U_OFF_LISTENER_NODE_IMAGE=CACHED_NO_PULL'
echo "OLDX_H2U_OFF_LISTENER_MANIFEST_SHA256=$OLD_HASH"
STARTED=TRUE
docker run --rm --pull never --network none --read-only \
 --cap-drop ALL --security-opt no-new-privileges \
 --pids-limit 64 --memory 512m --cpus 1 \
 --user 65532:65532 \
 --mount "type=bind,src=$OLD/source,dst=/source,readonly" \
 --mount "type=bind,src=$TMP/manifest.json,dst=/evidence/source-closure.json,readonly" \
 --mount "type=bind,src=$TMP/audit,dst=/audit,readonly" \
 --workdir /source --entrypoint "$NODE" "$IMAGE" \
 /audit/smoke.mjs 2>&1 | tee "$TMP/h2u-off-listener.log"
for line in \
 'OLDX_H2U_OFF_RUNTIME_SMOKE=PASS_LOCAL_LISTENER_WITH_LIMITS' \
 'OLDX_H2U_OFF_RUNTIME_SOURCE_FILES=65' \
 'OLDX_H2U_OFF_RUNTIME_HEALTH_STATUS=200_OFF' \
 'OLDX_H2U_OFF_RUNTIME_SAVE_STATUS=503_DISABLED' \
 'OLDX_H2U_OFF_RUNTIME_UNKNOWN_STATUS=404' \
 'OLDX_H2U_OFF_RUNTIME_NETWORK=DOCKER_LOOPBACK_ONLY';do
 grep -Fxq "$line" "$TMP/h2u-off-listener.log" ||
 { echo "STOP_SMOKE_RESULT_MISSING=$line";exit 2; }
done
sha256sum "$TMP/h2u-off-listener.log" |
 awk '{print "OLDX_H2U_OFF_LISTENER_LOG_SHA256="$1}'
PASS=TRUE
