#!/usr/bin/env bash
# H2U P1: exactly one NEW recovery for previous EACCES on manifest mount.
# Does NOT rerun old consumed wrapper, import scan, ESM link, HTTP smoke,
# cloud probes, Docker build or KMS/Firestore. Original root-owned evidence,
# old one-shot marker and old 65 source files are READ-ONLY/UNCHANGED.
set -Eeuo pipefail
umask 077
SOURCE='/root/oldx-h2u-import-closure.2oCNZVHV'
OLD_MARK='/root/.oldx-step05-h2u-off-context-stage-once-20261127'
NEW_MARK='/root/.oldx-step05-h2u-context-manifest-permission-recovery-once-20261127'
IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
MANIFEST_SHA='12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc'
STAGER_SHA='ce9d4514b1fdffc1280854ed4443e896a719fb2d'
TEMP=''
STARTED=FALSE
PASSED=FALSE
finish(){
  local ec=$?
  trap - EXIT
  if [[ "$ec" -eq 0 && "$PASSED" == TRUE ]]; then
    echo 'OLDX_H2U_CONTEXT_PERMISSION_RECOVERY=PASS_SOURCE_ONLY_WITH_LIMITS'
  else
    echo 'OLDX_H2U_CONTEXT_PERMISSION_RECOVERY=STOP'
    echo "OLDX_H2U_CONTEXT_RECOVERY_STARTED=$STARTED"
  fi
  [[ -z "$TEMP" ]] || echo "OLDX_H2U_CONTEXT_RECOVERY_EVIDENCE=$TEMP"
  echo 'OLDX_H2U_CONTEXT_OLD_MARKER=UNCHANGED'
  echo 'OLDX_H2U_CONTEXT_ORIGINAL_MANIFEST=UNCHANGED'
  echo 'OLDX_H2U_CONTEXT_RECOVERY_CLOUD_WRITES=NONE'
  echo 'OLDX_H2U_CONTEXT_RECOVERY_BUILDS_PULLS_SCANS=NONE'
  echo 'OLDX_H2U_H2_PRODUCTION=NO_GO'
  exit "$ec"
}
trap finish EXIT
[[ "$(id -u)" == 0 ]] || { echo 'STOP_ROOT_WSL_REQUIRED'; exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease ||
  { echo 'STOP_WSL_REQUIRED'; exit 2; }
for cmd in git curl docker sha256sum cp chmod chown grep; do
  command -v "$cmd" >/dev/null || { echo "STOP_TOOL_MISSING=$cmd"; exit 2; }
done
[[ -f "$OLD_MARK" && ! -L "$OLD_MARK" ]] ||
  { echo 'STOP_PREVIOUS_CONSUMED_MARKER_MISSING'; exit 2; }
[[ ! -e "$NEW_MARK" && ! -L "$NEW_MARK" ]] ||
  { echo 'STOP_RECOVERY_ALREADY_ATTEMPTED'; exit 2; }
[[ -d "$SOURCE/source" && ! -L "$SOURCE/source" &&
   -f "$SOURCE/source-closure.json" &&
   ! -L "$SOURCE/source-closure.json" ]] ||
  { echo 'STOP_PREVIOUS_SOURCE_OR_MANIFEST_MISSING'; exit 2; }
echo "$MANIFEST_SHA  $SOURCE/source-closure.json" | sha256sum --check --status ||
  { echo 'STOP_PREVIOUS_MANIFEST_HASH_DRIFT'; exit 2; }
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
  { echo 'STOP_CACHED_NODE_IMAGE_MISSING_NO_PULL'; exit 2; }
NODE=$(docker image inspect "$IMAGE" \
  --format '{{if .Config.Entrypoint}}{{index .Config.Entrypoint 0}}{{end}}')
case "$NODE" in
  /node|/*/node|/*/nodejs) ;;
  *) echo 'STOP_UNTRUSTED_NODE_ENTRYPOINT'; exit 2 ;;
esac

TEMP=$(mktemp -d /root/oldx-h2u-context-permission-recovery.XXXXXXXX)
mkdir -p "$TEMP/audit" "$TEMP/output" "$TEMP/evidence" "$TEMP/private-manifest"
chown 65532:65532 "$TEMP/output"
chmod 755 "$TEMP/output" "$TEMP/audit" "$TEMP/private-manifest"
# Original manifest remains root-only; copy is inside new private host folder
# but is deliberately readable to the nonroot Docker user through its bind.
cp -- "$SOURCE/source-closure.json" "$TEMP/private-manifest/source-closure.json"
chmod 644 "$TEMP/private-manifest/source-closure.json"
echo "$MANIFEST_SHA  $TEMP/private-manifest/source-closure.json" |
  sha256sum --check --status ||
  { echo 'STOP_PRIVATE_MANIFEST_COPY_DRIFT'; exit 2; }

curl --fail --silent --show-error --retry 0 --max-redirs 0 \
  --max-time 40 --proto '=https' \
  --output "$TEMP/audit/stage.mjs" \
  'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/18d013cd53c1ca9553617ec550e7a0ee8e7e7264/scripts/c2-h2u-stage-exact-off-source-context_20261127.mjs'
[[ "$(git hash-object "$TEMP/audit/stage.mjs")" == "$STAGER_SHA" ]] ||
  { echo 'STOP_STAGER_HASH_MISMATCH'; exit 2; }
chmod 644 "$TEMP/audit/stage.mjs"
( set -C
  printf 'NEW_CONTEXT_PERMISSION_RECOVERY_ATTEMPT=TRUE\nOLD_EACCES_MARKER_PRESERVED=TRUE\nMANIFEST_SHA256=%s\n' \
    "$MANIFEST_SHA" > "$NEW_MARK"
) || { echo 'STOP_RECOVERY_MARKER_CREATE_FAILED'; exit 2; }
echo 'OLDX_H2U_CONTEXT_RECOVERY_CAUSE=NONROOT_MANIFEST_READ_EACCES'
echo "OLDX_H2U_CONTEXT_RECOVERY_MANIFEST_SHA256=$MANIFEST_SHA"
echo 'OLDX_H2U_CONTEXT_RECOVERY_MANIFEST_COPY_MODE=0644_PRIVATE_PARENT'
STARTED=TRUE
docker run --rm --pull never --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --pids-limit 64 --memory 512m --cpus 1 \
  --user 65532:65532 \
  --mount "type=bind,src=$SOURCE/source,dst=/evidence/source,readonly" \
  --mount "type=bind,src=$TEMP/private-manifest/source-closure.json,dst=/evidence/source-closure.json,readonly" \
  --mount "type=bind,src=$TEMP/audit,dst=/audit,readonly" \
  --mount "type=bind,src=$TEMP/output,dst=/out" \
  --workdir /evidence/source --entrypoint "$NODE" "$IMAGE" \
  /audit/stage.mjs 2>&1 | tee "$TEMP/evidence/recovery-stage.log"

for expected in \
  'OLDX_H2U_CONTEXT_RESULT=PASS_65_FILES_SOURCE_ONLY' \
  'OLDX_H2U_CONTEXT_FILE_COUNT=65' \
  'OLDX_H2U_CONTEXT_SOURCE_BYTES=349667' \
  'OLDX_H2U_CONTEXT_CONTAINERFILE=NOT_GENERATED' \
  'OLDX_H2U_CONTEXT_IMAGE_BUILDS_PULLS_SCANS=NONE'; do
  grep -Fxq "$expected" "$TEMP/evidence/recovery-stage.log" ||
    { echo "STOP_RECOVERY_OUTPUT_MISMATCH=$expected"; exit 2; }
done
[[ -f "$TEMP/output/h2u-off-source-context/SOURCE_SHA256SUMS" &&
   -f "$TEMP/output/h2u-off-source-context/package.json" &&
   ! -e "$TEMP/output/h2u-off-source-context/Dockerfile" &&
   ! -e "$TEMP/output/h2u-off-source-context/Containerfile" ]] ||
   { echo 'STOP_RECOVERED_CONTEXT_STRUCTURE'; exit 2; }
echo "$MANIFEST_SHA  $SOURCE/source-closure.json" | sha256sum --check --status ||
  { echo 'STOP_ORIGINAL_MANIFEST_MODIFIED'; exit 2; }
sha256sum "$TEMP/evidence/recovery-stage.log" |
  awk '{print "OLDX_H2U_CONTEXT_RECOVERY_LOG_SHA256="$1}'
PASSED=TRUE
