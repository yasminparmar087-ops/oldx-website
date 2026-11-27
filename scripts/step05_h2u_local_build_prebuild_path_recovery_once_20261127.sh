#!/usr/bin/env bash
# BAJUTO / OLDX STEP05 H2U: Owner-approved ONE NEW LOCAL IMAGE BUILD
# plus NEW image-specific isolated nonroot OFF-mode runtime smoke.
# 27 Nov 2026. No previous test replay, no Cloud, no push/deploy/IAM/KMS.
set -Eeuo pipefail
umask 077

CTX='/root/oldx-h2u-context-permission-recovery.kANeYR1S/output/h2u-off-source-context'
ORIG='/root/oldx-h2u-import-closure.2oCNZVHV/source-closure.json'
ORIG_SHA='12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc'
SUM_SHA='42081779fe50e3ea9bf8d47aa8613c09db33050d46027d757d24efc79a2f6ecc'
CONTAINERFILE_SHA='4b85cbe44dc7e141f6934d99a91d8ec31cf2868c'
INDEX='sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121'
TAG='oldx-h2u-private-off:local-20261127-one'
MARK='/root/.oldx-step05-h2u-local-image-build-once-20261127'
DIR=''
CID=''
STARTED=FALSE
PASSED=FALSE

finish(){
  local rc=$?
  trap - EXIT
  if [[ -n "$CID" ]]; then
    docker rm -f "$CID" >/dev/null 2>&1 || true
  fi
  if [[ "$rc" -eq 0 && "$PASSED" == TRUE ]]; then
    echo 'OLDX_H2U_LOCAL_IMAGE_RESULT=PASS_NEW_BUILD_AND_OFF_RUNTIME_WITH_LIMITS'
  else
    echo 'OLDX_H2U_LOCAL_IMAGE_RESULT=STOP'
    echo "OLDX_H2U_LOCAL_BUILD_STARTED=$STARTED"
  fi
  [[ -z "$DIR" ]] || echo "OLDX_H2U_LOCAL_IMAGE_EVIDENCE=$DIR"
  echo 'OLDX_H2U_LOCAL_IMAGE_CLOUD_WRITES=NONE'
  echo 'OLDX_H2U_LOCAL_IMAGE_REGISTRY_PUSH=NONE'
  echo 'OLDX_H2U_LOCAL_IMAGE_CLOUD_RUN_DEPLOY=NONE'
  echo 'OLDX_H2U_LOCAL_IMAGE_OLD_TESTS_REPEATED=NONE'
  echo 'OLDX_H2U_H2_PRODUCTION=NO_GO'
  exit "$rc"
}
trap finish EXIT
[[ "$(id -u)" -eq 0 ]] || { echo STOP_ROOT_WSL_REQUIRED;exit 2; }
grep -qi microsoft /proc/sys/kernel/osrelease ||
  { echo STOP_WSL_REQUIRED;exit 2; }
for cmd in python3 docker git curl sha256sum find cut;do
  command -v "$cmd" >/dev/null ||
    { echo "STOP_MISSING_TOOL=$cmd";exit 2; }
done
[[ ! -e "$MARK" && ! -L "$MARK" ]] ||
  { echo STOP_ONE_SHOT_BUILD_MARKER_ALREADY_CONSUMED;exit 2; }
# Locate exactly one existing SHA-pinned context/manifest in Owner /root.
# Previous STOP was PRE-BUILD: do not repeat the old runner.
ctx_matches=()
for p in /root/oldx-h2u-context-permission-recovery.*/output/h2u-off-source-context;do
  [[ -d "$p" && ! -L "$p" && -f "$p/SOURCE_SHA256SUMS" && ! -L "$p/SOURCE_SHA256SUMS" ]] || continue
  [[ "$(sha256sum "$p/SOURCE_SHA256SUMS" | cut -d' ' -f1)" == "$SUM_SHA" ]] || continue
  ctx_matches+=("$p")
done
if [[ ${#ctx_matches[@]} -ne 1 ]]; then
  echo "STOP_CONTEXT_MATCHES=${#ctx_matches[@]}";exit 2
fi
CTX="${ctx_matches[0]}"
orig_matches=()
for p in /root/oldx-h2u-import-closure.*/source-closure.json;do
  [[ -f "$p" && ! -L "$p" ]] || continue
  [[ "$(sha256sum "$p" | cut -d' ' -f1)" == "$ORIG_SHA" ]] || continue
  orig_matches+=("$p")
done
if [[ ${#orig_matches[@]} -ne 1 ]];then
  echo "STOP_MANIFEST_MATCHES=${#orig_matches[@]}";exit 2
fi
ORIG="${orig_matches[0]}"
echo "OLDX_H2U_SOURCE_CONTEXT_RESOLVED=$CTX"
echo "OLDX_H2U_ORIGINAL_MANIFEST_RESOLVED=$ORIG"

[[ -d "$CTX" && ! -L "$CTX" && -f "$CTX/SOURCE_SHA256SUMS" &&
   ! -L "$CTX/SOURCE_SHA256SUMS" && -f "$ORIG" && ! -L "$ORIG" ]] ||
  { echo STOP_OLD_SOURCE_CONTEXT_OR_MANIFEST_MISSING;exit 2; }
echo "$SUM_SHA  $CTX/SOURCE_SHA256SUMS" | sha256sum -c --status ||
  { echo STOP_CONTEXT_SHA256SUMS_FILE_CHANGED;exit 2; }
echo "$ORIG_SHA  $ORIG" | sha256sum -c --status ||
  { echo STOP_ORIGINAL_MANIFEST_CHANGED;exit 2; }

# This is NEW pre-build attestation only; do not replay old 65-file scanner.
# Verify exact existing staged file hashes, paths and absence of ANY extras.
python3 -B - "$CTX" "$SUM_SHA" <<'PY'
import hashlib,json,os,pathlib,re,stat,sys
root=pathlib.Path(sys.argv[1])
expected=sys.argv[2]
if root.is_symlink() or not root.is_dir():
    raise SystemExit('STOP_CONTEXT_ROOT')
sums=root/'SOURCE_SHA256SUMS'
if hashlib.sha256(sums.read_bytes()).hexdigest()!=expected:
    raise SystemExit('STOP_SUMS_PIN_MISMATCH')
lines=sums.read_text(encoding='utf-8').splitlines()
if len(lines)!=65 or len(set(lines))!=65:
    raise SystemExit('STOP_SUMS_NOT_EXACT_65')
files=set()
total=0
for line in lines:
    m=re.fullmatch(r'([0-9a-f]{64})  (app/(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+\.(?:mjs|js))',line)
    if not m or '..' in m[2].split('/'):
        raise SystemExit('STOP_UNSAFE_SUM_ENTRY')
    digest,rel=m.groups()
    if rel in files: raise SystemExit('STOP_DUPLICATE_FILE')
    files.add(rel)
    path=root/rel
    if path.is_symlink() or not path.is_file():
        raise SystemExit('STOP_SOURCE_NOT_REGULAR')
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=digest:
        raise SystemExit('STOP_SOURCE_CONTENT_CHANGED')
    total+=len(data)
if total!=349667 or len(files)!=65:
    raise SystemExit('STOP_SOURCE_COUNT_OR_BYTES')
expected_root={'SOURCE_SHA256SUMS','RELEASE_PLAN_NOT_A_DOCKERFILE.txt','package.json','app'}
if {p.name for p in root.iterdir()}!=expected_root:
    raise SystemExit('STOP_UNEXPECTED_TOP_LEVEL_CONTENT')
for directory,dirs,names in os.walk(root,followlinks=False):
    for name in dirs+names:
        item=pathlib.Path(directory)/name
        mode=item.lstat().st_mode
        if stat.S_ISLNK(mode) or not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
            raise SystemExit('STOP_UNSAFE_SPECIAL_PATH')
actual={str((pathlib.Path(dir)/name).relative_to(root)).replace(os.sep,'/')
        for dir,_,names in os.walk(root,followlinks=False) for name in names}
if actual!=files|{'SOURCE_SHA256SUMS','RELEASE_PLAN_NOT_A_DOCKERFILE.txt','package.json'}:
    raise SystemExit('STOP_UNLISTED_SOURCE_FILES')
pkg=json.loads((root/'package.json').read_text('utf-8'))
if pkg.get('private') is not True or pkg.get('type')!='module' or pkg.get('name')!='oldx-h2u-private-off-gateway' or any(
    k in pkg for k in ('dependencies','devDependencies','scripts','bin')
):
    raise SystemExit('STOP_UNEXPECTED_PACKAGE')
print('OLDX_H2U_LOCAL_PREFLIGHT=PASS_65_IMMUTABLE_SOURCES')
print('OLDX_H2U_LOCAL_PREFLIGHT_SOURCE_BYTES=349667')
PY

docker buildx version >/dev/null ||
  { echo STOP_BUILDX_UNAVAILABLE;exit 2; }
if docker image inspect "$TAG" >/dev/null 2>&1;then
  echo STOP_OUTPUT_IMAGE_TAG_ALREADY_EXISTS
  exit 2
fi

DIR=$(mktemp -d /root/oldx-h2u-first-local-image.XXXXXXXX)
curl --fail --silent --show-error --retry 0 --max-redirs 0 \
  --max-time 40 --proto '=https' \
  --output "$DIR/Containerfile" \
  'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/a3e262a13425e29bf6bd683a3bf72f136459871d/release/H2U_Containerfile_OFF_ONLY_SIGNED_INDEX_CANDIDATE_20261127'
[[ "$(git hash-object "$DIR/Containerfile")" == "$CONTAINERFILE_SHA" ]] ||
  { echo STOP_CONTAINERFILE_GIT_BLOB_MISMATCH;exit 2; }
grep -Fqx "FROM --platform=linux/amd64 gcr.io/distroless/nodejs24-debian13@$INDEX" "$DIR/Containerfile" ||
  { echo STOP_SIGNED_INDEX_PIN_CHANGED;exit 2; }
grep -Fqx 'USER 65532:65532' "$DIR/Containerfile" ||
  { echo STOP_NONROOT_DECLARATION_CHANGED;exit 2; }
grep -Fqx 'ENV OLDX_H2U_MODE=OFF' "$DIR/Containerfile" ||
  { echo STOP_OFF_MODE_CHANGED;exit 2; }
grep -Fqx 'CMD ["scripts/c2-h2u-cloud-run-private-off-main.mjs"]' "$DIR/Containerfile" ||
  { echo STOP_OFF_ENTRYPOINT_CHANGED;exit 2; }

# Durable marker BEFORE the only owner-approved build attempt.
( set -C; printf 'H2U_ONE_NEW_LOCAL_BUILD_CONSUMED=TRUE\nINDEX=%s\nTAG=%s\n' \
  "$INDEX" "$TAG" >"$MARK" ) ||
  { echo STOP_MARKER_CONFLICT;exit 2; }
echo "OLDX_H2U_LOCAL_IMAGE_SOURCE_INDEX=$INDEX"
echo "OLDX_H2U_LOCAL_IMAGE_TAG=$TAG"
echo 'OLDX_H2U_LOCAL_BUILD_ATTEMPTS_AUTHORIZED=1'
STARTED=TRUE

docker buildx build \
  --platform linux/amd64 --network none --pull --load \
  --progress plain --iidfile "$DIR/image.iid" \
  --file "$DIR/Containerfile" --tag "$TAG" "$CTX" \
  2>&1 | tee "$DIR/build.log"

[[ -s "$DIR/image.iid" ]] || { echo STOP_NO_NEW_IMAGE_ID;exit 2; }
IID=$(cat "$DIR/image.iid")
[[ "$IID" =~ ^sha256:[0-9a-f]{64}$ ]] ||
  { echo STOP_INVALID_NEW_IMAGE_ID;exit 2; }
python3 -B - "$IID" <<'PY'
import json,subprocess,sys
iid=sys.argv[1]
obj=json.loads(subprocess.check_output(['docker','image','inspect',iid],text=True))[0]
cfg=obj['Config']
assert obj.get('Os')=='linux' and obj.get('Architecture')=='amd64', 'STOP_IMAGE_ARCH'
assert cfg.get('User')=='65532:65532','STOP_IMAGE_USER'
assert cfg.get('Entrypoint')==['/nodejs/bin/node'],'STOP_IMAGE_ENTRYPOINT'
assert cfg.get('Cmd')==['scripts/c2-h2u-cloud-run-private-off-main.mjs'],'STOP_IMAGE_CMD'
env=set(cfg.get('Env',[]))
assert {'OLDX_H2U_MODE=OFF','PORT=8080','NODE_ENV=production'}<=env,'STOP_IMAGE_ENV'
print('OLDX_H2U_LOCAL_IMAGE_CONFIG=PASS_NONROOT_AMD64_OFF')
PY

docker run --rm --pull never --platform linux/amd64 \
  --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges --pids-limit 64 \
  --memory 512m --cpus 1 --user 65532:65532 \
  --entrypoint /nodejs/bin/node "$IID" \
  -e 'const ver=process.versions.node; if(process.getuid()!==65532||Number(ver.split(".")[0])!==24){process.exit(42)};console.log("OLDX_H2U_LOCAL_IMAGE_NODE_VERSION="+ver);console.log("OLDX_H2U_LOCAL_IMAGE_RUNTIME_UID="+process.getuid())' \
  2>&1 | tee "$DIR/node-and-uid.log"

CID=$(docker run --detach --rm --pull never --platform linux/amd64 \
  --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges --pids-limit 64 \
  --memory 512m --cpus 1 --user 65532:65532 \
  "$IID")
[[ "$CID" =~ ^[a-f0-9]{64}$ ]] ||
  { echo STOP_INVALID_ISOLATED_CONTAINER_ID;exit 2; }

# New image-specific real loopback check inside container: no published port,
# no prior test re-execution, no credentials. Container is removed by trap.
docker exec --user 65532:65532 "$CID" /nodejs/bin/node -e '
const assert=require("node:assert/strict");
const nap=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const base="http://127.0.0.1:8080";
  let health;
  for(let i=0;i<65;i++){
    try{health=await fetch(base+"/healthz",{signal:AbortSignal.timeout(900)});break}
    catch(e){await nap(100)}
  }
  assert(health,"SERVER_NOT_READY");
  assert.equal(health.status,200);
  const h=await health.json();
  assert.equal(h.mode,"OFF");
  const save=await fetch(base+"/api/staging/marketplace/save",{
    method:"POST",headers:{"x-oldx-enable":"true","authorization":"Bearer synthetic-test-only"},
    signal:AbortSignal.timeout(1500)
  });
  assert.equal(save.status,503);
  assert.equal((await save.json()).error.code,"H2_GATEWAY_DISABLED");
  const nope=await fetch(base+"/undefined",{signal:AbortSignal.timeout(1500)});
  assert.equal(nope.status,404);
  assert.equal((await nope.json()).error.code,"NOT_FOUND");
  console.log("OLDX_H2U_LOCAL_IMAGE_HTTP=PASS_OFF_200_503_404");
  console.log("OLDX_H2U_LOCAL_IMAGE_LOOPBACK=DOCKER_NETWORK_NONE");
})().catch(e=>{console.error("STOP_H2U_NEW_IMAGE_HTTP_"+e.message);process.exitCode=2});
' 2>&1 | tee "$DIR/image-off-http.log"

grep -Fq 'OLDX_H2U_LOCAL_IMAGE_HTTP=PASS_OFF_200_503_404' "$DIR/image-off-http.log" ||
  { echo STOP_IMAGE_RUNTIME_HTTP_MISMATCH;exit 2; }
grep -Fq 'OLDX_H2U_LOCAL_IMAGE_RUNTIME_UID=65532' "$DIR/node-and-uid.log" ||
  { echo STOP_IMAGE_RUNTIME_UID_MISMATCH;exit 2; }
echo "$ORIG_SHA  $ORIG" | sha256sum -c --status ||
  { echo STOP_PREVIOUS_MANIFEST_POST_BUILD_CHANGED;exit 2; }
echo "$SUM_SHA  $CTX/SOURCE_SHA256SUMS" | sha256sum -c --status ||
  { echo STOP_PREVIOUS_SOURCE_SUMS_POST_BUILD_CHANGED;exit 2; }

echo "OLDX_H2U_LOCAL_IMAGE_IID=$IID"
sha256sum "$DIR/build.log" "$DIR/node-and-uid.log" "$DIR/image-off-http.log" |
  awk '{print "OLDX_H2U_LOCAL_EVIDENCE_SHA256="$1" FILE="$2}'
PASSED=TRUE
