#!/usr/bin/env bash
# OLDX Step05 H2S — only THREE NEW OAuth metadata-port tests (not old 3).
# SOURCE ONLY until Owner runs this on their existing root Ubuntu WSL.
# No Cloud API, credential, IAM, image build/pull/scan or production changes.
set -Eeuo pipefail
umask 077
SOURCE_COMMIT='27d5ae3c19ce769d5e802c5e02d2b71648be00ff'
IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
RUN_DIR=''
STARTED=FALSE
PASSED=FALSE
finish(){
  local code=$?
  trap - EXIT
  if [[ "$code" == 0 && "$PASSED" == TRUE ]];then
    echo 'OLDX_H2S_METADATA_NEW_TESTS=PASS_3_GROUPS'
  else
    echo 'OLDX_H2S_METADATA_NEW_TESTS=STOP'
    echo "OLDX_H2S_METADATA_TEST_STARTED=$STARTED"
  fi
  [[ -z "$RUN_DIR" ]] || echo "OLDX_H2S_METADATA_EVIDENCE=$RUN_DIR"
  echo 'OLDX_H2S_METADATA_CLOUD_WRITES=NONE'
  echo 'OLDX_H2S_METADATA_IMAGE_BUILDS_PULLS_SCANS=NONE'
  echo 'OLDX_H2S_H2_PRODUCTION=NO_GO'
  exit "$code"
}
trap finish EXIT
[[ "$(id -u)" == 0 ]] || { echo 'STOP_ROOT_WSL_REQUIRED'; exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease || { echo 'STOP_WSL_REQUIRED'; exit 2; }
for cmd in docker git curl tar grep sha256sum;do
  command -v "$cmd" >/dev/null || { echo "STOP_TOOL_MISSING_$cmd"; exit 2; }
done
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
  { echo 'STOP_LOCAL_IMAGE_MISSING_NO_PULL'; exit 2; }
NODE_ENTRY=$(docker image inspect "$IMAGE" \
  --format '{{if .Config.Entrypoint}}{{index .Config.Entrypoint 0}}{{end}}')
case "$NODE_ENTRY" in
  /node|/*/node|/*/nodejs) ;;
  *) echo 'STOP_UNVERIFIED_IMAGE_NODE_ENTRYPOINT'; exit 2;;
esac
RUN_DIR=$(mktemp -d /root/oldx-h2s-metadata-three.XXXXXXXX)
mkdir -p "$RUN_DIR/src"
curl --fail --location --silent --show-error --retry 0 --max-redirs 2 \
  --max-time 150 --proto '=https' --output "$RUN_DIR/source.tar.gz" \
  "https://codeload.github.com/yasminparmar087-ops/oldx-website/tar.gz/$SOURCE_COMMIT"
tar -xzf "$RUN_DIR/source.tar.gz" -C "$RUN_DIR/src" --strip-components=1
verify(){
  local path="$1" expected="$2"
  [[ -f "$RUN_DIR/src/$path" && ! -L "$RUN_DIR/src/$path" ]] ||
    { echo "STOP_SOURCE_MISSING_$path"; return 2; }
  [[ "$(git hash-object "$RUN_DIR/src/$path")" == "$expected" ]] ||
    { echo "STOP_SOURCE_BLOB_MISMATCH_$path"; return 2; }
}
verify scripts/c2-h2-cloud-run-gateway-access-token.mjs '95c2681c2e589dea3dccef6197531315fa4b5c62'
verify functions/staging-marketplace/c2-h2-gateway-runtime-credential-source.mjs '8b981bcb54af1a42ff2f486f715c8dbab14998e0'
verify scripts/c2-h2-cloud-run-gateway-access-token.test.mjs '32c264cca30ef2967e4cd9527f0c4a314ad2b0e9'
verify functions/staging-marketplace/c2-h2-gateway-host-source.mjs '08d2e270818fe50bfe2bc62691bb15563f4de754'
verify scripts/c2-h2-private-gateway-signing-composition.mjs 'a166160adf4062769231d8f2c17468911a51c7a2'
verify scripts/c2-h2-gateway-kms-synthetic-transport.mjs 'b00d0af565775f4b26084e85b148eb99c5d2f89c'
verify scripts/c2-kms-request-signing.mjs '0a37278834629ab16d6baf4adbf89099cf687348'
chmod -R a+rX "$RUN_DIR/src"
container(){
  docker run --rm --pull never --network none --read-only \
    --cap-drop ALL --security-opt no-new-privileges \
    --pids-limit 64 --memory 512m --cpus 1 \
    --user 65532:65532 \
    --mount "type=bind,src=$RUN_DIR/src,dst=/work,readonly" \
    --workdir /work --entrypoint "$NODE_ENTRY" "$IMAGE" "$@"
}
container -e "const [major,minor]=process.versions.node.split('.').map(Number);
  console.log('OLDX_H2S_METADATA_NODE='+process.versions.node);
  if(major<24||(major===24&&minor<12))process.exit(44);" ||
  { echo 'STOP_NODE_ENGINE_BELOW_24_12'; exit 2; }
printf 'CONSUMED_NEW_METADATA_THREE_TESTS_SOURCE=%s\n' "$SOURCE_COMMIT" \
  > "$RUN_DIR/one-shot-test-attempt.marker"
echo "OLDX_H2S_METADATA_SOURCE_COMMIT=$SOURCE_COMMIT"
echo 'OLDX_H2S_METADATA_ONLY_TEST=scripts/c2-h2-cloud-run-gateway-access-token.test.mjs'
STARTED=TRUE
container --test --test-reporter=tap \
  scripts/c2-h2-cloud-run-gateway-access-token.test.mjs \
  2>&1 | tee "$RUN_DIR/h2s-metadata-three.log"
# TAP reporter explicitly selected; distinguish Node PASS from shell wrapper.
for line in '# tests 3' '# pass 3' '# fail 0' '# skipped 0' '# todo 0';do
  grep -Fxq "$line" "$RUN_DIR/h2s-metadata-three.log" ||
    { echo "STOP_TAP_RESULT_NOT_CONFIRMED=$line"; exit 2; }
done
sha256sum "$RUN_DIR/h2s-metadata-three.log" |
  awk '{print "OLDX_H2S_METADATA_LOG_SHA256="$1}'
PASSED=TRUE
