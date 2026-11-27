#!/usr/bin/env bash
# OLDX Step05 H2S: exactly NEW three focused groups; fully offline Docker test.
# Uses previously retained local Node24 image, pinned GitHub commit archive.
# Never builds/pulls/pushes a Docker image, runs old tests or calls Google Cloud.
set -Eeuo pipefail
umask 077

REPO='yasminparmar087-ops/oldx-website'
SOURCE_COMMIT='bb3ea2fe1a581f00683c08f01a2a3c52d9637764'
IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
RUN_DIR=''
TEST_STARTED=FALSE
DONE=FALSE
status(){
  code=$?
  trap - EXIT
  if [[ "$DONE" == TRUE && "$code" -eq 0 ]]; then
    echo "OLDX_H2S_NEW_FOCUSED_TESTS=PASS_3_GROUPS"
  else
    echo "OLDX_H2S_NEW_FOCUSED_TESTS=STOP"
    echo "OLDX_H2S_TEST_STARTED=$TEST_STARTED"
  fi
  [[ -z "$RUN_DIR" ]] || echo "OLDX_H2S_LOCAL_EVIDENCE=$RUN_DIR"
  echo "OLDX_H2S_CLOUD_WRITES=NONE"
  echo "OLDX_H2S_BUILDS_PULLS_SCANS=NONE"
  echo "OLDX_H2S_H2_PRODUCTION=NO_GO"
  exit "$code"
}
trap status EXIT

[[ "$(id -u)" == 0 ]] || { echo 'STOP_ROOT_WSL_REQUIRED'; exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease || { echo 'STOP_WSL_REQUIRED'; exit 2; }
command -v docker >/dev/null && command -v git >/dev/null &&
  command -v curl >/dev/null && command -v tar >/dev/null ||
  { echo 'STOP_TOOL_MISSING'; exit 2; }
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
  { echo 'STOP_EXPECTED_CACHED_NODE24_IMAGE_MISSING_NO_PULL'; exit 2; }

RUN_DIR=$(mktemp -d /root/oldx-h2s-focused-offline.XXXXXXXX)
mkdir -p "$RUN_DIR/src"
curl --fail --location --silent --show-error --retry 0 \
  --max-redirs 2 --max-time 150 --proto '=https' \
  --output "$RUN_DIR/source.tar.gz" \
  "https://codeload.github.com/$REPO/tar.gz/$SOURCE_COMMIT"
tar -xzf "$RUN_DIR/source.tar.gz" -C "$RUN_DIR/src" --strip-components=1

verify_blob(){
  local actual
  actual=$(git hash-object "$RUN_DIR/src/$1") || return 2
  if [[ "$actual" != "$2" ]]; then
    echo "STOP_SOURCE_BLOB_MISMATCH $1"
    return 3
  fi
}
verify_blob 'scripts/c2-h2-gateway-kms-synthetic-transport.mjs' 'b00d0af565775f4b26084e85b148eb99c5d2f89c'
verify_blob 'scripts/c2-h2-private-gateway-signing-composition.mjs' 'a166160adf4062769231d8f2c17468911a51c7a2'
verify_blob 'functions/staging-marketplace/c2-h2-gateway-host-source.mjs' '08d2e270818fe50bfe2bc62691bb15563f4de754'
verify_blob 'scripts/c2-h2-gateway-signing-source.test.mjs' '5b87730f26335daf0efd845fc85d38b3dc1d197f'
verify_blob 'scripts/c2-kms-request-signing.mjs' '0a37278834629ab16d6baf4adbf89099cf687348'
chmod -R a+rX "$RUN_DIR/src"

# Containers are deliberately offline, read-only and non-privileged. Nothing
# is installed or written within the repo; test stdout is retained on WSL.
container(){
  docker run --rm --pull never --network none --read-only \
    --cap-drop ALL --security-opt no-new-privileges \
    --pids-limit 64 --memory 512m --cpus 1 \
    --user 65532:65532 \
    --mount "type=bind,src=$RUN_DIR/src,dst=/work,readonly" \
    --workdir /work --entrypoint node "$IMAGE" "$@"
}
container -e "const [major,minor]=process.versions.node.split('.').map(Number);
  console.log('OLDX_H2S_NODE_VERSION='+process.versions.node);
  if(major<24||(major===24&&minor<12))process.exit(44);" ||
  { echo 'STOP_NODE_VERSION_BELOW_REPO_ENGINE'; exit 2; }

echo "OLDX_H2S_TEST_SOURCE_COMMIT=$SOURCE_COMMIT"
echo 'OLDX_H2S_ONLY_TEST=scripts/c2-h2-gateway-signing-source.test.mjs'
TEST_STARTED=TRUE
container --test scripts/c2-h2-gateway-signing-source.test.mjs \
  2>&1 | tee "$RUN_DIR/new-h2s-focused-tests.log"

# Require exactly THREE new passing test groups, zero failures/skip/todo.
# Exit fails closed if Node's summary changes or tests silently do not run.
grep -Eq '^# tests 3 "$RUN_DIR/new-h2s-focused-tests.log" |
  awk '{print "OLDX_H2S_FOCUSED_TEST_LOG_SHA256="$1}'
DONE=TRUE
 "$RUN_DIR/new-h2s-focused-tests.log"
grep -Eq '^# pass 3 "$RUN_DIR/new-h2s-focused-tests.log" |
  awk '{print "OLDX_H2S_FOCUSED_TEST_LOG_SHA256="$1}'
DONE=TRUE
 "$RUN_DIR/new-h2s-focused-tests.log"
grep -Eq '^# fail 0 "$RUN_DIR/new-h2s-focused-tests.log" |
  awk '{print "OLDX_H2S_FOCUSED_TEST_LOG_SHA256="$1}'
DONE=TRUE
 "$RUN_DIR/new-h2s-focused-tests.log"
grep -Eq '^# skipped 0 "$RUN_DIR/new-h2s-focused-tests.log" |
  awk '{print "OLDX_H2S_FOCUSED_TEST_LOG_SHA256="$1}'
DONE=TRUE
 "$RUN_DIR/new-h2s-focused-tests.log"
grep -Eq '^# todo 0 "$RUN_DIR/new-h2s-focused-tests.log" |
  awk '{print "OLDX_H2S_FOCUSED_TEST_LOG_SHA256="$1}'
DONE=TRUE
 "$RUN_DIR/new-h2s-focused-tests.log"
sha256sum "$RUN_DIR/new-h2s-focused-tests.log" |
  awk '{print "OLDX_H2S_FOCUSED_TEST_LOG_SHA256="$1}'
DONE=TRUE
