#!/usr/bin/env bash
# OLDX H1B G2A: recover the consumed v2 OAuth attempt after heredoc stdin EOF.
# Only existing isolated Owner WSL config; no builds, push, deployment or Cloud IAM writes.
set -Eeuo pipefail
umask 077

OWNER='yasminparmar087@gmail.com'
PROJECT='oldx-staging'
REGISTRY_HOST='asia-south1-docker.pkg.dev'
BASE='/root/oldx-tools'
SDK="$BASE/native-gcloud-594.0.1/google-cloud-sdk"
CLI="$SDK/bin/gcloud"
BUNDLED_PY="$SDK/platform/bundledpythonunix/bin/python3"
G2_CONFIG="$BASE/oldx-h1b-g2-20261126-cloudsdk-config"
G2_DOCKER="$BASE/oldx-h1b-g2-20261126-docker-config"
OLD_MARKER='/root/.oldx-h1b-g2-wsl-owner-login-once-20261126'
RECOVERY_MARKER='/root/.oldx-h1b-g2a-terminal-stdin-recovery-once-20261126'

stop() {
  printf 'H1B_G2R_RESULT=STOP\nH1B_G2R_REASON=%s\n' "$1"
  exit 2
}
[[ "$#" == 1 && "$1" == '--h1b-g2a-terminal-stdin-recovery-once' ]] || stop 'EXACT_FLAG_REQUIRED'
[[ "$(id -u)" == 0 && "$(uname -s)" == 'Linux' ]] || stop 'OWNER_WSL_ROOT_REQUIRED'
[[ "$(uname -r | tr '[:upper:]' '[:lower:]')" == *microsoft* ]] || stop 'NOT_WSL'
[[ -d "$SDK" && ! -L "$SDK" && "$(stat -c %u "$SDK")" == 0 ]] || stop 'SDK_CHANGED'
[[ -f "$CLI" && -x "$CLI" && ! -L "$CLI" ]] || stop 'CLI_MISSING'
resolved="$(readlink -e -- "$BUNDLED_PY")" || stop 'BUNDLED_PYTHON_MISSING'
sdk_real="$(readlink -e -- "$SDK")" || stop 'SDK_CANONICAL_PATH_MISSING'
[[ "$sdk_real" == "$SDK" && "$resolved" == "$sdk_real/"* && -f "$resolved" && -x "$resolved" ]] || stop 'PYTHON_SDK_BOUNDARY_FAILED'
[[ "$(stat -c %u "$resolved")" == 0 ]] || stop 'PYTHON_OWNER_MISMATCH'
[[ -f "$OLD_MARKER" && ! -L "$OLD_MARKER" && "$(stat -c %u "$OLD_MARKER")" == 0 ]] || stop 'OLD_ATTEMPT_MARKER_NOT_FOUND'
grep -Fxq 'ATTEMPT_CONSUMED=TRUE' "$OLD_MARKER" || stop 'OLD_MARKER_NOT_CONSUMED'
grep -Fxq "G2_CONFIG=$G2_CONFIG" "$OLD_MARKER" || stop 'OLD_MARKER_CONFIG_MISMATCH'
grep -Fxq "G2_DOCKER=$G2_DOCKER" "$OLD_MARKER" || stop 'OLD_MARKER_DOCKER_MISMATCH'
if grep -Fq 'RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY' "$OLD_MARKER"; then
  stop 'OLD_ATTEMPT_ALREADY_SUCCEEDED'
fi
[[ -d "$G2_CONFIG" && ! -L "$G2_CONFIG" && "$(stat -c %u "$G2_CONFIG")" == 0 ]] || stop 'OLD_ISOLATED_CONFIG_NOT_FOUND'
[[ -d "$G2_DOCKER" && ! -L "$G2_DOCKER" && "$(stat -c %u "$G2_DOCKER")" == 0 ]] || stop 'OLD_ISOLATED_DOCKER_CONFIG_NOT_FOUND'
[[ ! -e "$RECOVERY_MARKER" && ! -L "$RECOVERY_MARKER" ]] || stop 'RECOVERY_ONESHOT_CONSUMED'
[[ ! -e "$G2_DOCKER/config.json" && ! -L "$G2_DOCKER/config.json" ]] || stop 'DOCKER_CONFIG_ALREADY_EXISTS_REVIEW'
command -v timeout >/dev/null 2>&1 || stop 'TIMEOUT_MISSING'
# Require a real controlling terminal; the previous heredoc exhausted stdin.
if ! exec {tty_fd}</dev/tty; then stop 'NO_CONTROLLING_TERMINAL'; fi
[[ -t "$tty_fd" ]] || stop 'NO_INTERACTIVE_TTY'

export HOME=/root
export PATH="$SDK/bin:/usr/bin:/bin"
export CLOUDSDK_CONFIG="$G2_CONFIG"
export CLOUDSDK_PYTHON="$BUNDLED_PY"
export CLOUDSDK_CORE_DISABLE_USAGE_REPORTING=1
export CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK=1
export CLOUDSDK_CORE_CHECK_GCE_METADATA=false
export DOCKER_CONFIG="$G2_DOCKER"
unset CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE GOOGLE_APPLICATION_CREDENTIALS

# Fresh scoped one-shot marker, atomically before new cloud auth checks.
if ! (set -C; printf 'ATTEMPT_CONSUMED=TRUE\nOLD_MARKER_RETAINED=TRUE\n' > "$RECOVERY_MARKER"); then
  stop 'RECOVERY_MARKER_CREATE_FAILED'
fi
chmod 600 "$RECOVERY_MARKER"
on_failure() {
  local code="$?"
  if [[ "$code" -ne 0 ]]; then
    printf 'H1B_G2R_RESULT=STOP_AFTER_RECOVERY_MARKER\n'
    printf 'H1B_G2R_REASON=DO_NOT_RERUN_OR_RESET_MARKERS\n'
  fi
}
trap on_failure EXIT

# Native SDK and only prior G2 isolated credentials; no prior consumed tests rerun.
existing="$(timeout 30 "$CLI" auth list --filter='status:ACTIVE' --format='value(account)')" ||
  stop 'ISOLATED_AUTH_LIST_FAILED'
if [[ -n "$existing" && "$existing" != "$OWNER" ]]; then
  stop 'UNEXPECTED_ACTIVE_ACCOUNT'
fi
if [[ "$existing" != "$OWNER" ]]; then
  printf 'H1B_G2R_STAGE=INTERACTIVE_OWNER_GOOGLE_LOGIN\n'
  printf 'H1B_G2R_NOTICE=DO_NOT_SHARE_OAUTH_URL_OR_VERIFICATION_CODE\n'
  # THIS fixes the prior EOFError: /dev/tty, not inherited heredoc stdin.
  "$CLI" auth login "$OWNER" --no-launch-browser <&"$tty_fd"
fi
active="$(timeout 30 "$CLI" auth list --filter='status:ACTIVE' --format='value(account)')" ||
  stop 'ACTIVE_ACCOUNT_READ_FAILED'
[[ "$active" == "$OWNER" ]] || stop 'ACTIVE_OWNER_NOT_VERIFIED'
"$CLI" --quiet config set project "$PROJECT" >/dev/null
configured="$("$CLI" config get-value project 2>/dev/null)"
[[ "$configured" == "$PROJECT" ]] || stop 'LOCAL_PROJECT_MISMATCH'

# Isolated Docker helper configuration for exactly one Registry host.
( set -C; printf '{"credHelpers":{"%s":"gcloud"}}\n' "$REGISTRY_HOST" > "$G2_DOCKER/config.json" ) ||
  stop 'DOCKER_CONFIG_CREATE_FAILED'
chmod 600 "$G2_DOCKER/config.json"
python3 - "$G2_DOCKER/config.json" "$REGISTRY_HOST" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    got=json.load(f)
assert got == {"credHelpers": {sys.argv[2]: "gcloud"}}
PY

printf 'RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY\n' >> "$RECOVERY_MARKER"
trap - EXIT
printf 'H1B_G2R_OWNER=VERIFIED\n'
printf 'H1B_G2R_PROJECT=OLDX_STAGING_ISOLATED_CONFIG\n'
printf 'H1B_G2R_DOCKER_HELPER=ONLY_ASIA_SOUTH1\n'
printf 'H1B_G2R_REGISTRY_PUSH=NOT_ATTEMPTED\n'
printf 'H1B_G2R_CLOUD_RESOURCE_WRITES=NONE\n'
printf 'H1B_G2R_RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY\n'
