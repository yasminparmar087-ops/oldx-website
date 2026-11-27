#!/usr/bin/env bash
# NEW Step05 H2S one-sign ledger tests ONLY; does not re-run previous H2S suites.
# Owner root WSL, existing cached Node 24 Docker image, immutable Git snapshot.
# No real Firestore, Google Cloud, KMS, IAM or network inside test container.
set -Eeuo pipefail
umask 077
SOURCE_COMMIT='729722568a8af33a43c33e69935c690c51c3f803'
IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
RUN_DIR=''
TEST_STARTED=FALSE
PASSED=FALSE
finish(){
  local code=$?
  trap - EXIT
  if [[ "$code" == 0 && "$PASSED" == TRUE ]]; then
    echo 'OLDX_H2S_ONE_SIGN_LEDGER_TESTS=PASS_3_GROUPS'
  else
    echo 'OLDX_H2S_ONE_SIGN_LEDGER_TESTS=STOP'
    echo "OLDX_H2S_ONE_SIGN_LEDGER_TEST_STARTED=$TEST_STARTED"
  fi
  [[ -z "$RUN_DIR" ]] || echo "OLDX_H2S_ONE_SIGN_LOCAL_EVIDENCE=$RUN_DIR"
  echo 'OLDX_H2S_ONE_SIGN_CLOUD_WRITES=NONE'
  echo 'OLDX_H2S_ONE_SIGN_BUILDS_PULLS_SCANS=NONE'
  echo 'OLDX_H2S_H2_PRODUCTION=NO_GO'
  exit "$code"
}
trap finish EXIT

[[ "$(id -u)" == 0 ]] || { echo 'STOP_ROOT_WSL_REQUIRED'; exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease || { echo 'STOP_WSL_REQUIRED'; exit 2; }
for cmd in git docker curl tar grep sha256sum; do
  command -v "$cmd" >/dev/null || { echo "STOP_TOOL_MISSING_$cmd"; exit 2; }
done
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
  { echo 'STOP_CACHED_NODE24_IMAGE_MISSING_NO_PULL'; exit 2; }
NODE_ENTRY=$(docker image inspect "$IMAGE" \
  --format '{{if .Config.Entrypoint}}{{index .Config.Entrypoint 0}}{{end}}')
case "$NODE_ENTRY" in
  /node|/*/node|/*/nodejs) ;;
  *) echo 'STOP_CACHED_NODE_ENTRYPOINT_UNTRUSTED'; exit 2;;
esac
RUN_DIR=$(mktemp -d /root/oldx-h2s-one-sign-ledger.XXXXXXXX)
mkdir -p "$RUN_DIR/src"
curl --fail --silent --show-error --location --retry 0 \
  --max-redirs 2 --max-time 150 --proto '=https' \
  --output "$RUN_DIR/source.tar.gz" \
  "https://codeload.github.com/yasminparmar087-ops/oldx-website/tar.gz/$SOURCE_COMMIT"
tar -xzf "$RUN_DIR/source.tar.gz" -C "$RUN_DIR/src" --strip-components=1
verify(){
  local path="$1" expected="$2"
  [[ -f "$RUN_DIR/src/$path" && ! -L "$RUN_DIR/src/$path" ]] ||
    { echo "STOP_SOURCE_MISSING $path"; return 2; }
  [[ "$(git hash-object "$RUN_DIR/src/$path")" == "$expected" ]] ||
    { echo "STOP_SOURCE_BLOB_MISMATCH $path"; return 2; }
}
verify scripts/c2-h2-firestore-one-sign-budget.mjs 'e7cd8fa7082da9dd2e097e8f03b3e82fff2fbabb'
verify scripts/c2-h2-firestore-one-sign-budget.test.mjs 'd380a817f50fa9bd693df5182ff548d8588ad92b'
verify scripts/staging-marketplace-context.mjs '614dd6124a7d6673c655823c37da21e859410989'
verify scripts/isolated-firestore-context.mjs '46b85e8bc64f469e8a5ac39f2af7c456dfe5dd3f'
verify scripts/provider-schema-v1.mjs 'c64cc0732c49f37083106ceab10f5a0e5dbc2db8'
verify tests/integration/fake-firestore-sdk.mjs '02927beae248725feb8244953b5c6570ad3b7cc2'
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
  console.log('OLDX_H2S_ONE_SIGN_NODE='+process.versions.node);
  if(major<24||(major===24&&minor<12))process.exit(44);" ||
  { echo 'STOP_NODE_BELOW_REQUIRED_24_12'; exit 2; }

printf 'CONSUMED_NEW_ONE_SIGN_TEST_SOURCE=%s\n' "$SOURCE_COMMIT" \
  > "$RUN_DIR/one-sign-focused-attempt.marker"
echo "OLDX_H2S_ONE_SIGN_SOURCE_COMMIT=$SOURCE_COMMIT"
echo 'OLDX_H2S_ONE_SIGN_ONLY_TEST=scripts/c2-h2-firestore-one-sign-budget.test.mjs'
TEST_STARTED=TRUE
container --test --test-reporter=tap \
  scripts/c2-h2-firestore-one-sign-budget.test.mjs \
  2>&1 | tee "$RUN_DIR/one-sign-ledger-new-three.log"
for line in '# tests 3' '# pass 3' '# fail 0' '# skipped 0' '# todo 0'; do
  grep -Fxq "$line" "$RUN_DIR/one-sign-ledger-new-three.log" ||
    { echo "STOP_TAP_SUMMARY_NOT_CONFIRMED=$line"; exit 2; }
done
sha256sum "$RUN_DIR/one-sign-ledger-new-three.log" |
  awk '{print "OLDX_H2S_ONE_SIGN_LOG_SHA256="$1}'
PASSED=TRUE
