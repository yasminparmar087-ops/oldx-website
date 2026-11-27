#!/usr/bin/env bash
# Step05 H2U: one NEW, OFFLINE Node ESM LINK-ONLY audit on ALREADY-SAVED
# owner H2U import closure evidence. No previous audit or test rerun,
# no GitHub source archive re-download, image build/pull/scan or Cloud API.
set -Eeuo pipefail
umask 077
OLD='/root/oldx-h2u-import-closure.2oCNZVHV'
MARK='/root/.oldx-step05-h2u-esm-link-only-once-20261127'
IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
EXPECTED='12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc'
TMP=''
STARTED=FALSE
PASSED=FALSE
finish(){
  local ec=$?
  trap - EXIT
  if [[ "$ec" == 0 && "$PASSED" == TRUE ]]; then
    echo 'OLDX_H2U_ESM_LINK_AUDIT=PASS_SOURCE_LINK_ONLY_WITH_LIMITS'
  else
    echo 'OLDX_H2U_ESM_LINK_AUDIT=STOP'
    echo "OLDX_H2U_ESM_LINK_STARTED=$STARTED"
  fi
  [[ -z "$TMP" ]] || echo "OLDX_H2U_ESM_LINK_EVIDENCE=$TMP"
  echo 'OLDX_H2U_ESM_LINK_CLOUD_WRITES=NONE'
  echo 'OLDX_H2U_ESM_LINK_BUILDS_PULLS_SCANS=NONE'
  echo 'OLDX_H2U_H2_PRODUCTION=NO_GO'
  exit "$ec"
}
trap finish EXIT
[[ "$(id -u)" == 0 ]] ||
  { echo STOP_ROOT_WSL_REQUIRED;exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease ||
  { echo STOP_WSL_REQUIRED;exit 2; }
for bin in git curl docker sha256sum chmod cp grep;do
  command -v "$bin" >/dev/null ||
    { echo "STOP_MISSING_TOOL=$bin";exit 2; }
done
[[ ! -e "$MARK" && ! -L "$MARK" ]] ||
  { echo STOP_ALREADY_ATTEMPTED;exit 2; }
[[ -d "$OLD" && ! -L "$OLD" && -d "$OLD/source" &&
   ! -L "$OLD/source" && -f "$OLD/source-closure.json" &&
   ! -L "$OLD/source-closure.json" ]] ||
  { echo STOP_OLD_MANIFEST_OR_SOURCE_MISSING;exit 2; }
echo "$EXPECTED  $OLD/source-closure.json" | sha256sum --check --status ||
  { echo STOP_OLD_MANIFEST_PIN_MISMATCH;exit 2; }
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
  { echo STOP_CACHED_NODE24_IMAGE_MISSING_NO_PULL;exit 2; }
NODE=$(docker image inspect "$IMAGE" \
  --format '{{if .Config.Entrypoint}}{{index .Config.Entrypoint 0}}{{end}}')
case "$NODE" in /node|/*/node|/*/nodejs) ;; *)
  echo STOP_IMAGE_NODE_ENTRYPOINT_UNVERIFIED;exit 2;; esac
TMP=$(mktemp -d /root/oldx-h2u-esm-link-only.XXXXXXXX)
mkdir -p "$TMP/audit" "$TMP/manifest"
# A clean, readable manifest COPY only: original evidence remains unchanged.
cp -- "$OLD/source-closure.json" "$TMP/manifest/source-closure.json"
chmod 755 "$TMP/audit" "$TMP/manifest"
chmod 644 "$TMP/manifest/source-closure.json"
curl --fail --silent --show-error --retry 0 --max-redirs 0 \
  --max-time 40 --proto '=https' \
  --output "$TMP/audit/link.mjs" \
  'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/d8f214f5d706707236d32139c3524a46ce698902/scripts/c2-h2u-verify-existing-manifest-esm-link-only_20261127.mjs'
[[ "$(git hash-object "$TMP/audit/link.mjs")" == \
 'df458b5d7f3847a94f035204c43098bc141380bd' ]] ||
  { echo STOP_LINK_VERIFIER_HASH_MISMATCH;exit 2; }
chmod 644 "$TMP/audit/link.mjs"
( set -C
  printf 'H2U_NEW_ESM_LINK_ATTEMPT_CONSUMED=TRUE\nMANIFEST_SHA256=%s\n' \
    "$EXPECTED" > "$MARK"
) || { echo STOP_NEW_LINK_MARKER_CONFLICT;exit 2; }
echo 'OLDX_H2U_ESM_LINK_NODE_IMAGE=CACHED_NO_PULL'
echo "OLDX_H2U_ESM_LINK_OLD_MANIFEST_SHA256=$EXPECTED"
STARTED=TRUE
docker run --rm --pull never --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --pids-limit 64 --memory 512m --cpus 1 \
  --user 65532:65532 \
  --mount "type=bind,src=$OLD/source,dst=/evidence/source,readonly" \
  --mount "type=bind,src=$TMP/manifest/source-closure.json,dst=/evidence/source-closure.json,readonly" \
  --mount "type=bind,src=$TMP/audit,dst=/audit,readonly" \
  --workdir /evidence/source \
  --entrypoint "$NODE" "$IMAGE" \
  --experimental-vm-modules /audit/link.mjs \
  2>&1 | tee "$TMP/esm-link-only.log"
for expected in \
  'OLDX_H2U_ESM_LINK_RESULT=PASS_SOURCE_LINK_ONLY' \
  'OLDX_H2U_ESM_LINK_SOURCE_FILES=65' \
  'OLDX_H2U_ESM_LINK_EXTERNAL_IMPORTS=0' \
  'OLDX_H2U_ESM_SOURCE_EVALUATED=FALSE';do
  grep -Fxq "$expected" "$TMP/esm-link-only.log" ||
    { echo "STOP_LINK_SUMMARY_MISMATCH=$expected";exit 2; }
done
sha256sum "$TMP/esm-link-only.log" |
  awk '{print "OLDX_H2U_ESM_LINK_LOG_SHA256="$1}'
PASSED=TRUE
