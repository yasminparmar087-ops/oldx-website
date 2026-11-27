#!/usr/bin/env bash
# One NEW local H2U 65-file staging only. Reuses existing successful
# closure/ESM/loopback source, no rerun. No OCI build/push, Cloud Run, KMS or IAM.
set -Eeuo pipefail
umask 077
ROOT='/root/oldx-h2u-import-closure.2oCNZVHV'
IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
PIN='12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc'
MARKER='/root/.oldx-step05-h2u-off-context-stage-once-20261127'
DIR=''
ATTEMPT=FALSE
PASS=FALSE
finish(){
 local rc=$?
 trap - EXIT
 if [[ "$rc" == 0 && "$PASS" == TRUE ]];then
  echo 'OLDX_H2U_OFF_CONTEXT_STAGE=PASS_SOURCE_ONLY_WITH_LIMITS'
 else
  echo 'OLDX_H2U_OFF_CONTEXT_STAGE=STOP'
  echo "OLDX_H2U_OFF_CONTEXT_ATTEMPT_STARTED=$ATTEMPT"
 fi
 [[ -z "$DIR" ]] || echo "OLDX_H2U_OFF_CONTEXT_EVIDENCE=$DIR"
 echo 'OLDX_H2U_OFF_CONTEXT_CLOUD_WRITES=NONE'
 echo 'OLDX_H2U_OFF_CONTEXT_IMAGE_BUILDS_PULLS_SCANS=NONE'
 echo 'OLDX_H2U_H2_PRODUCTION=NO_GO'
 exit "$rc"
}
trap finish EXIT
[[ "$(id -u)" == 0 ]] || { echo STOP_NOT_ROOT_WSL;exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease ||
 { echo STOP_NOT_WSL;exit 2; }
for cmd in git curl docker sha256sum chmod chown grep;do
 command -v "$cmd" >/dev/null || { echo "STOP_MISSING_$cmd";exit 2; }
done
[[ ! -e "$MARKER" && ! -L "$MARKER" ]] ||
 { echo STOP_CONTEXT_STAGE_ALREADY_ATTEMPTED;exit 2; }
[[ -d "$ROOT/source" && ! -L "$ROOT/source" &&
   -f "$ROOT/source-closure.json" && ! -L "$ROOT/source-closure.json" ]] ||
 { echo STOP_OLD_SOURCE_OR_MANIFEST_MISSING;exit 2; }
echo "$PIN  $ROOT/source-closure.json" | sha256sum --check --status ||
 { echo STOP_OLD_MANIFEST_MISMATCH;exit 2; }
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
 { echo STOP_CACHED_NODE24_IMAGE_MISSING;exit 2; }
NODE=$(docker image inspect "$IMAGE" \
 --format '{{if .Config.Entrypoint}}{{index .Config.Entrypoint 0}}{{end}}')
case "$NODE" in /node|/*/node|/*/nodejs) ;; *)
 echo STOP_NODE_ENTRYPOINT_UNVERIFIED;exit 2;;esac
DIR=$(mktemp -d /root/oldx-h2u-off-context.XXXXXXXX)
mkdir -p "$DIR/audit" "$DIR/output" "$DIR/evidence"
chown 65532:65532 "$DIR/output"
chmod 755 "$DIR/output" "$DIR/audit" "$DIR/evidence"
curl --fail --silent --show-error --retry 0 --max-redirs 0 \
 --max-time 40 --proto '=https' \
 --output "$DIR/audit/stage.mjs" \
 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/18d013cd53c1ca9553617ec550e7a0ee8e7e7264/scripts/c2-h2u-stage-exact-off-source-context_20261127.mjs'
[[ "$(git hash-object "$DIR/audit/stage.mjs")" == \
 'ce9d4514b1fdffc1280854ed4443e896a719fb2d' ]] ||
 { echo STOP_STAGE_SCRIPT_GIT_BLOB_CHANGED;exit 2; }
chmod 644 "$DIR/audit/stage.mjs"
( set -C
 printf 'H2U_CONTEXT_ONE_SHOT_CONSUMED=TRUE\nMANIFEST_SHA256=%s\n' \
 "$PIN" > "$MARKER"
) || { echo STOP_ATTEMPT_MARKER_CONFLICT;exit 2; }
echo 'OLDX_H2U_OFF_CONTEXT_CACHED_NODE=TRUE'
echo "OLDX_H2U_OFF_CONTEXT_OLD_MANIFEST=$PIN"
ATTEMPT=TRUE
docker run --rm --pull never --network none --read-only \
 --cap-drop ALL --security-opt no-new-privileges \
 --pids-limit 64 --memory 512m --cpus 1 \
 --user 65532:65532 \
 --mount "type=bind,src=$ROOT/source,dst=/evidence/source,readonly" \
 --mount "type=bind,src=$ROOT/source-closure.json,dst=/evidence/source-closure.json,readonly" \
 --mount "type=bind,src=$DIR/audit,dst=/audit,readonly" \
 --mount "type=bind,src=$DIR/output,dst=/out" \
 --workdir /evidence/source --entrypoint "$NODE" "$IMAGE" \
 /audit/stage.mjs 2>&1 | tee "$DIR/evidence/stage.log"
for line in \
 'OLDX_H2U_CONTEXT_RESULT=PASS_65_FILES_SOURCE_ONLY' \
 'OLDX_H2U_CONTEXT_FILE_COUNT=65' \
 'OLDX_H2U_CONTEXT_SOURCE_BYTES=349667' \
 'OLDX_H2U_CONTEXT_CONTAINERFILE=NOT_GENERATED' \
 'OLDX_H2U_CONTEXT_IMAGE_BUILDS_PULLS_SCANS=NONE';do
 grep -Fxq "$line" "$DIR/evidence/stage.log" ||
 { echo "STOP_STAGE_OUTPUT_MISSING=$line";exit 2; }
done
[[ -f "$DIR/output/h2u-off-source-context/SOURCE_SHA256SUMS" &&
   -f "$DIR/output/h2u-off-source-context/package.json" &&
   ! -e "$DIR/output/h2u-off-source-context/Dockerfile" ]] ||
 { echo STOP_STAGED_CONTEXT_STRUCTURE;exit 2; }
sha256sum "$DIR/evidence/stage.log" |
 awk '{print "OLDX_H2U_OFF_CONTEXT_LOG_SHA256="$1}'
PASS=TRUE
