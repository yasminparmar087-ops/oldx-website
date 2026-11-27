#!/usr/bin/env bash
# Step05 H2S: recover exactly ONE previously NOT STARTED offline focused test.
# Reuse exact local already-fetched, hash-verified source, no download/build/pull.
# Inspect pinned image's original absolute Node entrypoint: never assume PATH.
set -Eeuo pipefail
umask 077

IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
SOURCE='bb3ea2fe1a581f00683c08f01a2a3c52d9637764'
RUN_DIR='/root/oldx-h2s-focused-offline.0Mh9HZuX'
SRC="$RUN_DIR/src"
MARKER="$RUN_DIR/h2s-node24-new-focused-test-attempt.marker"
TEST_STARTED=FALSE
PASS=FALSE
finish(){
  code=$?
  trap - EXIT
  if [[ "$PASS" == TRUE && "$code" == 0 ]]; then
    echo 'OLDX_H2S_NEW_FOCUSED_TESTS=PASS_3_GROUPS'
  else
    echo 'OLDX_H2S_NEW_FOCUSED_TESTS=STOP'
    echo "OLDX_H2S_TEST_STARTED=$TEST_STARTED"
  fi
  echo "OLDX_H2S_SOURCE_COMMIT=$SOURCE"
  echo "OLDX_H2S_LOCAL_EVIDENCE=$RUN_DIR"
  echo 'OLDX_H2S_CLOUD_WRITES=NONE'
  echo 'OLDX_H2S_BUILDS_PULLS_SCANS=NONE'
  echo 'OLDX_H2S_H2_PRODUCTION=NO_GO'
  exit "$code"
}
trap finish EXIT

[[ "$(id -u)" == 0 ]] || { echo 'STOP_ROOT_WSL_REQUIRED'; exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease || { echo 'STOP_WSL_REQUIRED'; exit 2; }
for tool in git docker sha256sum grep; do
  command -v "$tool" >/dev/null || { echo "STOP_TOOL_MISSING_$tool"; exit 2; }
done
[[ -d "$RUN_DIR" && ! -L "$RUN_DIR" && -d "$SRC" && ! -L "$SRC" ]] ||
  { echo 'STOP_EXISTING_SOURCE_DIR_MISSING_DO_NOT_REDOWNLOAD'; exit 2; }
[[ ! -e "$MARKER" && ! -L "$MARKER" ]] ||
  { echo 'STOP_NEW_FOCUSED_TEST_ALREADY_ATTEMPTED'; exit 2; }
[[ -f "$RUN_DIR/source.tar.gz" && ! -L "$RUN_DIR/source.tar.gz" ]] ||
  { echo 'STOP_OLD_SOURCE_ARCHIVE_MISSING'; exit 2; }
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
  { echo 'STOP_CACHED_IMAGE_MISSING_NO_PULL'; exit 2; }

verify(){
  local file="$1" expected="$2" actual
  [[ -f "$SRC/$file" && ! -L "$SRC/$file" ]] ||
    { echo "STOP_SOURCE_FILE_MISSING $file"; return 2; }
  actual=$(git hash-object "$SRC/$file") || return 2
  [[ "$actual" == "$expected" ]] ||
    { echo "STOP_SOURCE_BLOB_MISMATCH $file"; return 2; }
}
verify 'scripts/c2-h2-gateway-kms-synthetic-transport.mjs' 'b00d0af565775f4b26084e85b148eb99c5d2f89c'
verify 'scripts/c2-h2-private-gateway-signing-composition.mjs' 'a166160adf4062769231d8f2c17468911a51c7a2'
verify 'functions/staging-marketplace/c2-h2-gateway-host-source.mjs' '08d2e270818fe50bfe2bc62691bb15563f4de754'
verify 'scripts/c2-h2-gateway-signing-source.test.mjs' '5b87730f26335daf0efd845fc85d38b3dc1d197f'
verify 'scripts/c2-kms-request-signing.mjs' '0a37278834629ab16d6baf4adbf89099cf687348'

# Entrypoint comes from the cached image's configuration, not a guess or PATH.
# Distroless Node images commonly use /nodejs/bin/node; the actual local image
# must declare a safe absolute executable path ending in /node.
NODE_ENTRY=$(docker image inspect "$IMAGE" \
  --format '{{if .Config.Entrypoint}}{{index .Config.Entrypoint 0}}{{end}}')
case "$NODE_ENTRY" in
  /node|/*/node|/*/nodejs) ;;
  *)
    echo 'STOP_NODE_ENTRYPOINT_NOT_CONFIRMED'
    docker image inspect "$IMAGE" \
      --format 'IMAGE_ENTRYPOINT={{json .Config.Entrypoint}} IMAGE_CMD={{json .Config.Cmd}}'
    exit 2
    ;;
esac
echo "OLDX_H2S_NODE_ENTRYPOINT=$NODE_ENTRY"

container(){
  docker run --rm --pull never --network none --read-only \
    --cap-drop ALL --security-opt no-new-privileges \
    --pids-limit 64 --memory 512m --cpus 1 \
    --user 65532:65532 \
    --mount "type=bind,src=$SRC,dst=/work,readonly" \
    --workdir /work --entrypoint "$NODE_ENTRY" "$IMAGE" "$@"
}
container -e "const [major,minor]=process.versions.node.split('.').map(Number);
  console.log('OLDX_H2S_NODE_VERSION='+process.versions.node);
  if(major<24||(major===24&&minor<12))process.exit(44);" ||
  { echo 'STOP_CACHED_NODE_BELOW_REQUIRED_24_12'; exit 2; }

# One new targeted test only; marker persisted BEFORE test starts.
( set -C; printf 'H2S_NEW_FOCUSED_TEST_ATTEMPT_CONSUMED=TRUE\nSOURCE_COMMIT=%s\n' "$SOURCE" > "$MARKER" ) ||
  { echo 'STOP_TEST_ATTEMPT_MARKER_ALREADY_EXISTS'; exit 2; }

echo 'OLDX_H2S_ONLY_TEST=scripts/c2-h2-gateway-signing-source.test.mjs'
TEST_STARTED=TRUE
container --test scripts/c2-h2-gateway-signing-source.test.mjs \
  2>&1 | tee "$RUN_DIR/new-h2s-focused-recovered-node24.log"

# Exact 3 new cases, not prior 11 suites; fail closed on changed TAP summary.
for expected in '# tests 3' '# pass 3' '# fail 0' '# skipped 0' '# todo 0'; do
  grep -Fxq "$expected" "$RUN_DIR/new-h2s-focused-recovered-node24.log" ||
    { echo "STOP_TAP_SUMMARY_MISMATCH $expected"; exit 2; }
done
sha256sum "$RUN_DIR/new-h2s-focused-recovered-node24.log" |
  awk '{print "OLDX_H2S_FOCUSED_LOG_SHA256="$1}'
PASS=TRUE
