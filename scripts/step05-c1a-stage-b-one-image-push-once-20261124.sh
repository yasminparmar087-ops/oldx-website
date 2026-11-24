#!/usr/bin/env bash
# OLDX Step05 C1A B2: ONE owner-approved push of the ALREADY BUILT WSL OFF-only image.
# Prerequisite: owner has seen exact new remote tag NOT_FOUND from target-only gcloud preflight.
# Authentication token comes via stdin from Windows gcloud; never echo it.
# NO Docker build, Syft, Grype, Cosign rerun, service/IAM/Firebase/Cloud Run writes.
set -Eeuo pipefail
umask 077
die(){ printf 'STOP_B2: %s\n' "$*" >&2; exit 1; }
LOCAL_TAG='oldx-step05-gateway-off:wsl-once-20261124-801'
EXPECTED_ID='sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a'
REMOTE='asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off:c1a-off-20261124-801'
LOCK="$HOME/.oldx-step05-c1a-b2-image-push-once-20261124"
for tool in docker mktemp grep date; do command -v "$tool" >/dev/null 2>&1 || die "Missing $tool"; done
[[ "$(uname -s)" == Linux && "$(uname -m)" == x86_64 ]] || die 'Wrong machine: local Linux x86_64 required'
grep -qiE 'microsoft|wsl' /proc/sys/kernel/osrelease || die 'Owner WSL context required'
[[ -z "${DOCKER_HOST:-}" && "$(docker context show)" == default ]] || die 'Remote/non-default Docker disallowed'
docker info --format '{{.OSType}}/{{.Architecture}}' | grep -Eq '^linux/(x86_64|amd64)$' || die 'Local linux/amd64 daemon unavailable'
ID="$(docker image inspect --format '{{.Id}}' "$LOCAL_TAG")" || die 'Approved local image not present'
USER_ID="$(docker image inspect --format '{{.Config.User}}' "$LOCAL_TAG")" || die 'Cannot read user'
PLATFORM="$(docker image inspect --format '{{.Os}}/{{.Architecture}}' "$LOCAL_TAG")" || die 'Cannot read platform'
[[ "$ID" == "$EXPECTED_ID" && "$USER_ID" == '65532:65532' && "$PLATFORM" == 'linux/amd64' ]] || die 'Source image ID/platform/nonroot mismatch'
[[ ! -e "$LOCK" ]] || die 'One push already attempted; read remote tag instead of retrying'

# If local target tag exists, it must refer to the exact same source ID; never overwrite a different local image.
if docker image inspect "$REMOTE" >/dev/null 2>&1; then
 [[ "$(docker image inspect --format '{{.Id}}' "$REMOTE")" == "$EXPECTED_ID" ]] || die 'Local target tag already refers to different image'
fi
OUT="$HOME/oldx-step05-c1a-b2-push-20261124"
mkdir -p -m 700 "$OUT" || die 'Cannot create report folder'
CFG="$(mktemp -d /tmp/oldx-b2-dockercfg.XXXXXXXX)" || die 'Cannot create isolated Docker auth config'
export DOCKER_CONFIG="$CFG"
cleanup(){ rm -f -- "$CFG/config.json" "$CFG/config.json.tmp" 2>/dev/null || true; rmdir -- "$CFG" 2>/dev/null || true; }
trap cleanup EXIT
printf 'STAGE_B_B2=PREPARED\nSOURCE_ID=%s\nSOURCE_TAG=%s\nTARGET=%s\nNO_BUILD_SCAN_DEPLOY=TRUE\n' "$EXPECTED_ID" "$LOCAL_TAG" "$REMOTE" > "$OUT/summary.txt"
echo 'AUTH=SHORT_LIVED_OWNER_TOKEN_FROM_STDIN'
if ! docker login --username oauth2accesstoken --password-stdin https://asia-south1-docker.pkg.dev >/dev/null 2>"$OUT/login-error.txt"; then
  die 'Docker Registry login failed. No push attempted; check error privately.'
fi
echo 'DOCKER_LOGIN=PASS_TEMPORARY_CONFIG'

# The exact new target tag must have been confirmed absent separately in the owner CMD preflight.
# Once this marker is set, never retry a failed/partial push blindly.
( set -C; printf 'B2_STARTED=%s\nTARGET=%s\nSOURCE=%s\n' "$(date -u +%FT%TZ)" "$REMOTE" "$EXPECTED_ID" > "$LOCK" ) 2>/dev/null || die 'One-shot marker conflict'
docker tag "$LOCAL_TAG" "$REMOTE" || die 'Local tagging failed; no remote push'
echo 'ONE_REMOTE_PUSH=STARTED'
if ! docker push "$REMOTE" > "$OUT/push.log" 2>&1; then
  printf 'STAGE_B_B2=PUSH_FAILED_OR_AMBIGUOUS_STOP\n' >> "$OUT/summary.txt"
  die "DO NOT retry. Read exact remote tag in Google Cloud; evidence at $OUT"
fi
digest="$(grep -Eo 'digest: sha256:[0-9a-f]{64}' "$OUT/push.log" | tail -1 | awk '{print $2}')" || true
[[ "$digest" =~ ^sha256:[0-9a-f]{64}$ ]] || die "Push returned success but remote digest could not be parsed; no repeat, inspect $OUT/push.log"
printf 'STAGE_B_B2=PUSH_SUCCESS_PENDING_REMOTE_READBACK\nREMOTE_MANIFEST_DIGEST=%s\nIMMUTABLE_REMOTE_REFERENCE=%s@%s\n' "$digest" "${REMOTE%:*}" "$digest" >> "$OUT/summary.txt"
printf 'B2_PUSH_SUCCESS_UNVERIFIED_REMOTE_READBACK\n%s\nREMOTE_DIGEST=%s\nREPORT=%s\n' "$REMOTE" "$digest" "$OUT/summary.txt"
