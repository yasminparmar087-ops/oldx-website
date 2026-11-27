#!/usr/bin/env bash
# H2U ONLY: exactly 3 NEW OFF-only Gateway HTTP/PORT tests, never old suites.
# Existing owner WSL root, cached Node 24 Docker image, pinned GitHub archive.
# NO Docker build/pull/push/scan, Google Cloud call, API enablement or deployment.
set -Eeuo pipefail
umask 077
SOURCE='b0b3d04fb6726bad138e02bb8a38c217c0ad3124'
IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
MARKER='/root/.oldx-step05-h2u-off-http-three-focused-once-20261127'
RUN_DIR=''
STARTED=FALSE
PASS=FALSE
finish(){
  local code=$?
  trap - EXIT
  if [[ "$code" -eq 0 && "$PASS" == TRUE ]]; then
    echo 'OLDX_H2U_OFF_HTTP_NEW_TESTS=PASS_3_GROUPS'
  else
    echo 'OLDX_H2U_OFF_HTTP_NEW_TESTS=STOP'
    echo "OLDX_H2U_OFF_HTTP_TEST_STARTED=$STARTED"
  fi
  [[ -z "$RUN_DIR" ]] || echo "OLDX_H2U_OFF_HTTP_EVIDENCE=$RUN_DIR"
  echo 'OLDX_H2U_OFF_HTTP_CLOUD_WRITES=NONE'
  echo 'OLDX_H2U_OFF_HTTP_BUILDS_PULLS_SCANS=NONE'
  echo 'OLDX_H2U_H2_PRODUCTION=NO_GO'
  exit "$code"
}
trap finish EXIT
[[ "$(id -u)" == 0 ]] || { echo 'STOP_ROOT_WSL_REQUIRED';exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease ||
  { echo 'STOP_WSL_REQUIRED';exit 2; }
for command in git curl tar docker sha256sum grep;do
  command -v "$command" >/dev/null ||
    { echo "STOP_MISSING_TOOL=$command";exit 2; }
done
[[ ! -e "$MARKER" && ! -L "$MARKER" ]] ||
  { echo 'STOP_ALREADY_ATTEMPTED_DO_NOT_REPEAT';exit 2; }
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
  { echo 'STOP_CACHED_NODE24_IMAGE_MISSING_NO_PULL';exit 2; }
NODE_ENTRY=$(docker image inspect "$IMAGE" \
  --format '{{if .Config.Entrypoint}}{{index .Config.Entrypoint 0}}{{end}}')
case "$NODE_ENTRY" in
  /node|/*/node|/*/nodejs) ;;
  *) echo 'STOP_UNVERIFIED_NODE_ENTRYPOINT';exit 2;;
esac
RUN_DIR=$(mktemp -d /root/oldx-h2u-off-http-new.XXXXXXXX)
mkdir -p "$RUN_DIR/src"
curl --fail --location --silent --show-error --retry 0 --max-redirs 2 \
  --max-time 150 --proto '=https' --output "$RUN_DIR/source.tar.gz" \
  "https://codeload.github.com/yasminparmar087-ops/oldx-website/tar.gz/$SOURCE"
tar -xzf "$RUN_DIR/source.tar.gz" -C "$RUN_DIR/src" --strip-components=1
verify(){
  local path="$1" expected="$2"
  [[ -f "$RUN_DIR/src/$path" && ! -L "$RUN_DIR/src/$path" ]] ||
    { echo "STOP_SOURCE_MISSING=$path";return 2; }
  [[ "$(git hash-object "$RUN_DIR/src/$path")" == "$expected" ]] ||
    { echo "STOP_SOURCE_HASH_MISMATCH=$path";return 2; }
}
verify functions/staging-marketplace/c2-h2u-private-off-http.mjs '704ba162a1fa60c5379d4fee6126ddeb86ae02c8'
verify scripts/c2-h2u-cloud-run-private-off-main.mjs '3df3405459a6d9ac504ae10fc7e56caee657f8ca'
verify scripts/c2-h2u-private-off-http.test.mjs 'b568f99c481460410995773f30dbd20f1d35f1f3'
chmod -R a+rX "$RUN_DIR/src"
container(){
  docker run --rm --pull never --network none --read-only \
    --cap-drop ALL --security-opt no-new-privileges \
    --pids-limit 64 --memory 512m --cpus 1 \
    --user 65532:65532 \
    --mount "type=bind,src=$RUN_DIR/src,dst=/work,readonly" \
    --workdir /work --entrypoint "$NODE_ENTRY" "$IMAGE" "$@"
}
container -e "const [a,b]=process.versions.node.split('.').map(Number);
  console.log('OLDX_H2U_NODE_VERSION='+process.versions.node);
  if(a<24||(a===24&&b<12))process.exit(44);" ||
  { echo 'STOP_NODE_VERSION_BELOW_24_12';exit 2; }
( set -C; printf 'H2U_OFF_NEW_TEST_ATTEMPT_CONSUMED=TRUE\nSOURCE_COMMIT=%s\n' "$SOURCE" > "$MARKER" ) ||
  { echo 'STOP_TEST_ATTEMPT_MARKER_CONFLICT';exit 2; }
echo "OLDX_H2U_OFF_HTTP_SOURCE_COMMIT=$SOURCE"
echo 'OLDX_H2U_OFF_HTTP_ONLY_TEST=scripts/c2-h2u-private-off-http.test.mjs'
STARTED=TRUE
container --test --test-reporter=tap scripts/c2-h2u-private-off-http.test.mjs \
  2>&1 | tee "$RUN_DIR/three-new-h2u-off-http.log"
for line in '# tests 3' '# pass 3' '# fail 0' '# cancelled 0' '# skipped 0' '# todo 0';do
  grep -Fxq "$line" "$RUN_DIR/three-new-h2u-off-http.log" ||
    { echo "STOP_TAP_SUMMARY_NOT_CONFIRMED=$line";exit 2; }
done
sha256sum "$RUN_DIR/three-new-h2u-off-http.log" |
  awk '{print "OLDX_H2U_OFF_HTTP_LOG_SHA256="$1}'
PASS=TRUE
