#!/usr/bin/env bash
# Step05 H2U SOURCE IMPORT CLOSURE AUDIT (not a test, Docker build or deploy).
# Immutable GitHub source + cached Node24 Docker; Docker NETWORK NONE.
set -Eeuo pipefail
umask 077
SOURCE='176a8e39e5fa8a1b3e2016f5938b3a569152f34d'
IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
MARK='/root/.oldx-step05-h2u-import-closure-audit-once-20261127'
DIR=''
STARTED=FALSE
DONE=FALSE
finish(){
  local code=$?
  trap - EXIT
  if [[ "$code" -eq 0 && "$DONE" == TRUE ]];then
    echo 'OLDX_H2U_IMPORT_CLOSURE=STATIC_AUDIT_PASS_WITH_LIMITS'
  else
    echo 'OLDX_H2U_IMPORT_CLOSURE=STOP'
    echo "OLDX_H2U_IMPORT_AUDIT_STARTED=$STARTED"
  fi
  [[ -z "$DIR" ]] || echo "OLDX_H2U_IMPORT_CLOSURE_EVIDENCE=$DIR"
  echo 'OLDX_H2U_CLOUD_WRITES=NONE'
  echo 'OLDX_H2U_BUILDS_PULLS_SCANS=NONE'
  echo 'OLDX_H2U_H2_PRODUCTION=NO_GO'
  exit "$code"
}
trap finish EXIT
[[ "$(id -u)" == 0 ]] || { echo 'STOP_NOT_ROOT_WSL';exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease ||
  { echo 'STOP_NOT_WSL';exit 2; }
for cmd in curl tar docker git python3 sha256sum;do
  command -v "$cmd" >/dev/null ||
    { echo "STOP_MISSING_TOOL=$cmd";exit 2; }
done
[[ ! -e "$MARK" && ! -L "$MARK" ]] ||
  { echo 'STOP_H2U_CLOSURE_MARKER_ALREADY_CONSUMED';exit 2; }
docker image inspect "$IMAGE" --format '{{.Id}}' >/dev/null 2>&1 ||
  { echo 'STOP_CACHED_NODE_IMAGE_MISSING_NO_PULL';exit 2; }
NODE=$(docker image inspect "$IMAGE" \
  --format '{{if .Config.Entrypoint}}{{index .Config.Entrypoint 0}}{{end}}')
case "$NODE" in /node|/*/node|/*/nodejs) ;; *)
  echo 'STOP_UNVERIFIED_NODE_ENTRYPOINT';exit 2;; esac
DIR=$(mktemp -d /root/oldx-h2u-import-closure.XXXXXXXX)
mkdir -p "$DIR/source"
curl --fail --location --silent --show-error --retry 0 --max-redirs 2 \
  --max-time 150 --proto '=https' --output "$DIR/source.tar.gz" \
  "https://codeload.github.com/yasminparmar087-ops/oldx-website/tar.gz/$SOURCE"
tar -xzf "$DIR/source.tar.gz" -C "$DIR/source" --strip-components=1
verify(){
  local f="$1" sha="$2"
  [[ -f "$DIR/source/$f" && ! -L "$DIR/source/$f" ]] ||
    { echo "STOP_MISSING_SOURCE=$f";return 2; }
  [[ "$(git hash-object "$DIR/source/$f")" == "$sha" ]] ||
    { echo "STOP_SOURCE_HASH_MISMATCH=$f";return 2; }
}
verify scripts/c2-h2u-source-import-closure-audit.mjs '654d66ebf5088d2f9169ea5811098c4d89f77114'
verify scripts/c2-h2u-cloud-run-private-off-main.mjs '3df3405459a6d9ac504ae10fc7e56caee657f8ca'
verify functions/staging-marketplace/c2-h2u-private-off-http.mjs '704ba162a1fa60c5379d4fee6126ddeb86ae02c8'
verify functions/staging-marketplace/c2-h2-gateway-host-source.mjs '08d2e270818fe50bfe2bc62691bb15563f4de754'
chmod -R a+rX "$DIR/source"
docker run --rm --pull never --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --pids-limit 64 --memory 512m --cpus 1 \
  --user 65532:65532 \
  --mount "type=bind,src=$DIR/source,dst=/work,readonly" \
  --workdir /work --entrypoint "$NODE" "$IMAGE" \
  -e "const a=process.versions.node.split('.').map(Number);
  console.log('OLDX_H2U_CLOSURE_NODE='+process.versions.node);
  if(a[0]<24||(a[0]===24&&a[1]<12))process.exit(44);" ||
  { echo 'STOP_NODE_BELOW_24_12';exit 2; }
( set -C; printf 'SOURCE_COMMIT=%s\nATTEMPT_CONSUMED=TRUE\n' "$SOURCE" > "$MARK" ) ||
  { echo 'STOP_MARKER_CREATION_FAILED';exit 2; }
echo "OLDX_H2U_CLOSURE_SOURCE_COMMIT=$SOURCE"
STARTED=TRUE
docker run --rm --pull never --network none --read-only \
  --cap-drop ALL --security-opt no-new-privileges \
  --pids-limit 64 --memory 512m --cpus 1 \
  --user 65532:65532 \
  --mount "type=bind,src=$DIR/source,dst=/work,readonly" \
  --workdir /work --entrypoint "$NODE" "$IMAGE" \
  scripts/c2-h2u-source-import-closure-audit.mjs \
  > "$DIR/source-closure.json"
python3 -B - "$DIR/source-closure.json" <<'PY'
import json,sys
with open(sys.argv[1],encoding='utf-8') as f: d=json.load(f)
assert d['checkpoint']=='H2U_OFF_SOURCE_ONLY_IMPORT_CLOSURE'
assert d['noCloudActions'] is True and d['noDockerBuild'] is True
assert d['fileCount']==len(d['files'])
print('OLDX_H2U_CLOSURE_FILES='+str(d['fileCount']))
print('OLDX_H2U_CLOSURE_SOURCE_BYTES='+str(d['totalSourceBytes']))
print('OLDX_H2U_CLOSURE_EXTERNAL_IMPORTS='+str(len(d['barePackageImports'])))
for item in d['barePackageImports'][:20]:
 print('OLDX_H2U_CLOSURE_EXTERNAL_NAME='+item['specifier'])
print('OLDX_H2U_CLOSURE_CONCLUSION='+d['conclusion'])
PY
sha256sum "$DIR/source-closure.json" |
  awk '{print "OLDX_H2U_CLOSURE_MANIFEST_SHA256="$1}'
DONE=TRUE
