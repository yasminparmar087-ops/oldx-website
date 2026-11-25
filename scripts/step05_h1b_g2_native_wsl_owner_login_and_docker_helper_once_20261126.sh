#!/usr/bin/env bash
# OLDX H1B G2A: one supervised WSL Google owner OAuth login and isolated, single-host
# Docker credential-helper configuration. NO push, IAM/cloud resource change or build.
set -Eeuo pipefail
umask 077

OWNER='yasminparmar087@gmail.com'
PROJECT='oldx-staging'
HOST='asia-south1-docker.pkg.dev'
BASE='/root/oldx-tools'
SDK="$BASE/native-gcloud-594.0.1/google-cloud-sdk"
CLI="$SDK/bin/gcloud"
BUNDLED_PY="$SDK/platform/bundledpythonunix/bin/python3"
G2_CONFIG="$BASE/oldx-h1b-g2-20261126-cloudsdk-config"
G2_DOCKER="$BASE/oldx-h1b-g2-20261126-docker-config"
MARKER='/root/.oldx-h1b-g2-wsl-owner-login-once-20261126'
LOCAL_IMAGE='oldx-h1a-c2-mediator-off:local-20261124t195244z'
FROZEN_ID='sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e'

stop() { printf 'H1B_G2A_RESULT=STOP\nH1B_G2A_REASON=%s\n' "$1"; exit 2; }
if [[ "$#" -ne 1 || "$1" != '--h1b-g2-owner-wsl-login-once' ]]; then
  stop 'EXACT_FLAG_REQUIRED'
fi
[[ "$(id -u)" -eq 0 ]] || stop 'ROOT_IN_OWNER_WSL_REQUIRED'
[[ "$(uname -s)" == Linux && "$(uname -r | tr '[:upper:]' '[:lower:]')" == *microsoft* ]] ||
  stop 'OWNER_WSL_REQUIRED'
[[ -d "$BASE" && ! -L "$BASE" ]] || stop 'BASE_NOT_PRESENT_OR_SYMLINK'
[[ -f "$CLI" && -x "$CLI" && ! -L "$CLI" ]] || stop 'NATIVE_LINUX_GCLOUD_NOT_PRESENT'
[[ -f "$BUNDLED_PY" && -x "$BUNDLED_PY" && ! -L "$BUNDLED_PY" ]] ||
  stop 'BUNDLED_PYTHON_NOT_PRESENT'
[[ ! -e "$MARKER" && ! -L "$MARKER" ]] || stop 'ONESHOT_ALREADY_CONSUMED'
[[ ! -e "$G2_CONFIG" && ! -L "$G2_CONFIG" ]] || stop 'CLOUDSDK_CONFIG_COLLISION'
[[ ! -e "$G2_DOCKER" && ! -L "$G2_DOCKER" ]] || stop 'DOCKER_CONFIG_COLLISION'
command -v docker >/dev/null 2>&1 || stop 'DOCKER_NOT_AVAILABLE'
image_id="$(docker image inspect --format '{{.Id}}' "$LOCAL_IMAGE" 2>/dev/null)" ||
  stop 'RETAINED_LOCAL_IMAGE_NOT_FOUND'
[[ "$image_id" == "$FROZEN_ID" ]] || stop 'RETAINED_IMAGE_ID_MISMATCH'

mkdir -m 700 -- "$G2_CONFIG" "$G2_DOCKER"
# Consumed before OAuth attempt; a failed/partial attempt is never silently retried.
if ! (set -C; printf 'ATTEMPT_CONSUMED=TRUE\nG2_CONFIG=%s\nG2_DOCKER=%s\n' \
   "$G2_CONFIG" "$G2_DOCKER" > "$MARKER"); then
  stop 'ONESHOT_MARKER_CREATION_FAILED'
fi
chmod 600 -- "$MARKER"
on_failure() {
  local rc="$?"
  if [[ "$rc" -ne 0 ]]; then
    printf 'H1B_G2A_RESULT=STOP_AFTER_MARKER\n'
    printf 'H1B_G2A_REASON=INSPECT_LOCAL_EVIDENCE_DO_NOT_REPEAT_OR_DELETE_MARKER\n'
  fi
}
trap on_failure EXIT

export HOME='/root'
export CLOUDSDK_CONFIG="$G2_CONFIG"
export CLOUDSDK_PYTHON="$BUNDLED_PY"
export CLOUDSDK_CORE_DISABLE_USAGE_REPORTING=1
export CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK=1
export PATH="$SDK/bin:/usr/bin:/bin"
export DOCKER_CONFIG="$G2_DOCKER"
unset CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE GOOGLE_APPLICATION_CREDENTIALS

printf 'H1B_G2A_STAGE=GOOGLE_BROWSER_SIGN_IN_REQUIRED\n'
printf 'H1B_G2A_NOTICE=DO_NOT_SHARE_OAUTH_URL_OR_CODE_OR_TOKENS\n'
# Interactive; use the owner's own trusted Google browser, never copy codes to a chat.
"$CLI" auth login "$OWNER" --no-launch-browser
active="$("$CLI" auth list --filter='status:ACTIVE' --format='value(account)')"
[[ "$active" == "$OWNER" ]] || stop 'GOOGLE_ACTIVE_ACCOUNT_MISMATCH'
"$CLI" --quiet config set project "$PROJECT" >/dev/null
configured_project="$("$CLI" config get-value project 2>/dev/null)"
[[ "$configured_project" == "$PROJECT" ]] || stop 'PROJECT_CONFIG_MISMATCH'

# The documented gcloud credential helper is used ONLY for Mumbai registry.
# This does not mutate ~/.docker/config.json, other registries, or credentials.
printf '{"credHelpers":{"%s":"gcloud"}}\n' "$HOST" > "$G2_DOCKER/config.json"
chmod 600 -- "$G2_DOCKER/config.json"
python3 - "$G2_DOCKER/config.json" "$HOST" <<'PY'
import json, sys
with open(sys.argv[1], encoding='utf-8') as f:
    config = json.load(f)
assert config == {"credHelpers": {sys.argv[2]: "gcloud"}}
PY

printf 'RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY\n' >> "$MARKER"
trap - EXIT
printf 'H1B_G2A_OWNER=VERIFIED\n'
printf 'H1B_G2A_PROJECT=OLDX_STAGING_ISOLATED_CONFIG\n'
printf 'H1B_G2A_DOCKER_HELPER=ONLY_ASIA_SOUTH1\n'
printf 'H1B_G2A_LOCAL_IMAGE_ID=FROZEN_MATCH\n'
printf 'H1B_G2A_REGISTRY_PUSH=NOT_ATTEMPTED\n'
printf 'H1B_G2A_CLOUD_RESOURCE_WRITES=NONE\n'
printf 'H1B_G2A_RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY\n'
