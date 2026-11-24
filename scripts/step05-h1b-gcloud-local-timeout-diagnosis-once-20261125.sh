#!/usr/bin/env bash
# OLDX H1B: LOCAL-ONLY gcloud startup timeout diagnosis. NOT the consumed preflight.
# One bounded --version probe; no auth, network API, credential reads or writes.
set -Eeuo pipefail
if [[ "$#" -ne 1 || "$1" != '--diagnose-local-once' ]]; then
  echo 'HOLD: exactly --diagnose-local-once is required; no probe performed.' >&2
  exit 2
fi
for tool in timeout stat sha256sum date readlink ps; do
  command -v "$tool" >/dev/null 2>&1 || { echo "STOP: missing $tool" >&2; exit 2; }
done
umask 077
MARKER="$HOME/.oldx-h1b-gcloud-startup-diagnosis-once-20261125"
if [[ -e "$MARKER" || -L "$MARKER" ]]; then
  echo 'STOP: dedicated diagnosis marker exists. Do not repeat/remove it.' >&2
  exit 2
fi
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
EVIDENCE="$HOME/oldx-h1b-gcloud-startup-diagnosis-$stamp"
mkdir -m 0700 -- "$EVIDENCE"
if ! ( set -C; printf '%s\n' "$EVIDENCE" > "$MARKER" ); then
  echo 'STOP: concurrent marker or write failure, no probe performed.' >&2
  exit 2
fi
finish() {
  local status=$?
  trap - EXIT
  (
    cd -- "$EVIDENCE"
    sha256sum -- *.txt *.exit *.stdout *.stderr > SHA256SUMS 2>/dev/null || true
  )
  printf 'H1B_LOCAL_DIAG_EXIT=%s\n' "$status"
  printf 'PRIVATE_EVIDENCE=%s\n' "$EVIDENCE"
  printf 'DIAG_MARKER_CONSUMED=%s\n' "$MARKER"
  exit "$status"
}
trap finish EXIT

# File and directory metadata only; NEVER open credential contents or SQLite DB.
{
  printf 'started_utc=%s\n' "$stamp"
  printf 'wsl_kernel=%s\n' "$(uname -r)"
  printf 'gcloud_executable_found=%s\n' "$(command -v gcloud >/dev/null 2>&1 && echo YES || echo NO)"
  printf 'sdk_config_env_override=%s\n' "$( [[ -v CLOUDSDK_CONFIG ]] && echo YES || echo NO )"
  printf 'sdk_python_env_override=%s\n' "$( [[ -v CLOUDSDK_PYTHON ]] && echo YES || echo NO )"
  printf 'sdk_active_configuration_env_override=%s\n' "$( [[ -v CLOUDSDK_ACTIVE_CONFIG_NAME ]] && echo YES || echo NO )"
  printf 'pythonpath_override=%s\n' "$( [[ -v PYTHONPATH ]] && echo YES || echo NO )"
  printf 'http_proxy_present=%s\n' "$( [[ -v HTTP_PROXY || -v http_proxy ]] && echo YES || echo NO )"
  printf 'https_proxy_present=%s\n' "$( [[ -v HTTPS_PROXY || -v https_proxy ]] && echo YES || echo NO )"
  printf 'no_proxy_present=%s\n' "$( [[ -v NO_PROXY || -v no_proxy ]] && echo YES || echo NO )"
  printf 'gcloud_install_path_class=' 
  sdk="$(type -P gcloud || true)"
  if [[ -z "$sdk" ]]; then echo NOT_INSTALLED; elif [[ "$sdk" == /mnt/* ]]; then echo WINDOWS_MOUNT_PATH; else echo LINUX_PATH; fi
  if [[ -n "$sdk" && -e "$sdk" ]]; then
    stat -c 'gcloud_link_or_file_type=%F;perm=%a;size=%s;mtime=%y' -- "$sdk"
    resolved="$(readlink -f -- "$sdk" || true)"
    if [[ -n "$resolved" && -e "$resolved" ]]; then
      stat -c 'gcloud_resolved_type=%F;perm=%a;size=%s;mtime=%y' -- "$resolved"
    fi
  fi
  config="${CLOUDSDK_CONFIG:-$HOME/.config/gcloud}"
  for name in configdir credentials.db access_tokens.db active_config; do
    case "$name" in
      configdir) p="$config";;
      *) p="$config/$name";;
    esac
    if [[ -e "$p" ]]; then
      stat -c "${name}_type=%F;perm=%a;size=%s;mtime=%y" -- "$p"
    else
      printf '%s_status=NOT_PRESENT\n' "$name"
    fi
  done
} > "$EVIDENCE/local-metadata.txt" 2> "$EVIDENCE/local-metadata.stderr"
# Only process names; no args, account names, tokens or full environment.
ps -eo pid,ppid,stat,comm --no-headers | awk '$4 ~ /^(gcloud|python|python3|kubectl)$/ {print $1, $2, $3, $4}' > "$EVIDENCE/process-names.txt" || true
printf '%s\n' 'local_gcloud_version_only_no_auth_no_remote_api' > "$EVIDENCE/version-scope.txt"
if ! command -v gcloud >/dev/null 2>&1; then
  echo 'NOT_FOUND' > "$EVIDENCE/version.exit"
  : > "$EVIDENCE/version.stdout"
  : > "$EVIDENCE/version.stderr"
  echo 'STOP: gcloud not found; no CLI process started.'
  exit 2
fi
export CLOUDSDK_CORE_DISABLE_PROMPTS=1
export CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK=1
export CLOUDSDK_CORE_DISABLE_USAGE_REPORTING=1
code=0
# One and only one bounded LOCAL gcloud --version process; never auth list.
timeout --signal=TERM --kill-after=2s 12s gcloud --version \
  > "$EVIDENCE/version.stdout" 2> "$EVIDENCE/version.stderr" || code=$?
printf '%s\n' "$code" > "$EVIDENCE/version.exit"
case "$code" in
  0) echo 'H1B_GCLOUD_STARTUP=VERSION_OK_AUTH_AND_CLOUD_ID_UNVERIFIED' ;;
  124|137) echo 'H1B_GCLOUD_STARTUP=VERSION_TIMEOUT_OR_KILLED_STOP' ;;
  *) echo 'H1B_GCLOUD_STARTUP=VERSION_ERROR_STOP' ;;
esac
# Exit NONZERO for abnormal result. Even 0 never authorizes preflight retry.
if [[ "$code" -eq 0 ]]; then exit 0; else exit 2; fi
