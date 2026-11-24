#!/usr/bin/env bash
# OLDX Step05 C1B: owner-approved ONE bounded hosted HTTP test against NEW private OFF Gateway.
# 3 HTTP requests (maximum authorized 6 total / 20 min): anonymous 401/403,
# authenticated Owner /healthz 200, authenticated Product POST 503.
# No Cloud resource/IAM writes, Firebase, backend, tests, Docker build, scan, token printing.
set -Eeuo pipefail
umask 077
set +x
fail(){ printf 'C1B_STOP=%s\n' "$*" >&2; exit 1; }
TARGET="https://oldx-step05-gateway-38472235077.asia-south1.run.app"
SCRIPT_LOCK="$HOME/.oldx-step05-c1b-off-hosted-once-20261124"
OUT="$HOME/oldx-step05-c1b-off-hosted-result-20261124.txt"
EXPECTED_BRANCH="security-hardening-review"
EXPECTED_SERVER_BLOB="25d2679bd4ea970c8b8a32a778fb26eb347bcdd6"
START="$(date +%s)"
N=0

[[ ! -e "$SCRIPT_LOCK" ]] || fail "ALREADY_ATTEMPTED_NO_REPEAT_READ_PREVIOUS_REPORT=$OUT"
for cmd in git curl date; do
  command -v "$cmd" >/dev/null 2>&1 || fail "MISSING_LOCAL_TOOL_$cmd"
done
[[ "$(git branch --show-current)" == "$EXPECTED_BRANCH" ]] || fail "WRONG_BRANCH"
[[ "$(git rev-parse HEAD:functions/staging-marketplace/cloud-run-gateway-off-server.mjs)" == "$EXPECTED_SERVER_BLOB" ]] || fail "OFF_SERVER_SOURCE_DRIFT"
[[ -z "$(git status --porcelain -- functions/staging-marketplace/cloud-run-gateway-off-server.mjs)" ]] || fail "OFF_SERVER_SOURCE_DIRTY"
[[ "$(uname -s)" == "Linux" ]] || fail "NOT_LINUX"
[[ -d /mnt/c ]] || fail "NOT_OWNER_WSL"
[[ -t 0 ]] && fail "NO_STDIN_IDENTITY_TOKEN"
# Read only one ephemeral ID token from Windows gcloud via stdin, never print or save it.
IFS= read -r -t 40 OWNER_ID_TOKEN || [[ -n "${OWNER_ID_TOKEN:-}" ]] || fail "NO_ID_TOKEN"
[[ "$OWNER_ID_TOKEN" =~ ^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$ ]] || fail "INVALID_ID_TOKEN_FORMAT"
[[ ! -e "$SCRIPT_LOCK" ]] || fail "RACE_LOCK_EXISTS"
( set -C; printf '%s\n' "C1B_FIRST_ATTEMPT_UTC=$(date -u +%FT%TZ)" > "$SCRIPT_LOCK" ) 2>/dev/null || fail "ONE_SHOT_LOCK_COLLISION"
{
  printf 'SCOPE=NEW_PRIVATE_OFF_GATEWAY_ONLY\n'
  printf 'OWNER_AUTH=EPHEMERAL_ID_TOKEN_NOT_LOGGED\n'
  printf 'TARGET=%s\n' "$TARGET"
  printf 'APPROVED_MAX_HTTP=6\n'
  printf 'APPROVED_WINDOW_SECONDS=1200\n'
  printf 'SOURCE_OFF_SERVER_GIT_BLOB=%s\n' "$EXPECTED_SERVER_BLOB"
  printf 'STATUS=STARTED\n'
} > "$OUT"
check_budget(){
  (( N < 6 )) || fail "HTTP_COUNT_LIMIT_REACHED"
  (( $(date +%s) - START < 1200 )) || fail "TWENTY_MINUTE_WINDOW_EXPIRED"
}
call_anon(){
  check_budget
  N=$((N+1))
  printf 'HTTP_ATTEMPT_%s=ANONYMOUS_GET_HEALTHZ\n' "$N" >> "$OUT"
  local code
  code="$(curl --silent --show-error --proto '=https' --tlsv1.2 --connect-timeout 10 --max-time 20 --retry 0 --max-redirs 0 --output /dev/null --write-out '%{http_code}' --request GET --url "$TARGET/healthz")" || fail "ANON_TRANSPORT_OR_TLS_FAILURE_NO_RETRY"
  printf 'HTTP_%s_CODE=%s\n' "$N" "$code" >> "$OUT"
  if [[ "$code" != "401" && "$code" != "403" ]]; then
    fail "ANONYMOUS_UNEXPECTED_HTTP_$code_NO_FURTHER_REQUESTS"
  fi
  echo "ANONYMOUS_GET_HEALTHZ=$code PASS"
}
call_owner(){
  local method="$1" path="$2" expected="$3" label="$4"
  check_budget
  N=$((N+1))
  printf 'HTTP_ATTEMPT_%s=%s\n' "$N" "$label" >> "$OUT"
  local code
  # Feed the Authorization header through curl's stdin configuration, NOT a
  # command-line argument, so a short-lived token is not exposed in process argv.
  # Do not enable curl --verbose, curl tracing, redirects, or Bash xtrace.
  if [[ "$method" == "POST" ]]; then
    code="$(printf 'header = "Authorization: Bearer %s"\n' "$OWNER_ID_TOKEN" |
      curl --config - --silent --show-error --proto '=https' --tlsv1.2 \
        --connect-timeout 10 --max-time 20 --retry 0 --max-redirs 0 \
        --output /dev/null --write-out '%{http_code}' \
        --request POST --header 'Content-Type: application/json' \
        --data-binary '{}' --url "$TARGET$path")" || fail "$label TRANSPORT_OR_TLS_FAILURE_NO_RETRY"
  else
    code="$(printf 'header = "Authorization: Bearer %s"\n' "$OWNER_ID_TOKEN" |
      curl --config - --silent --show-error --proto '=https' --tlsv1.2 \
        --connect-timeout 10 --max-time 20 --retry 0 --max-redirs 0 \
        --output /dev/null --write-out '%{http_code}' \
        --request GET --url "$TARGET$path")" || fail "$label TRANSPORT_OR_TLS_FAILURE_NO_RETRY"
  fi
  printf 'HTTP_%s_CODE=%s\n' "$N" "$code" >> "$OUT"
  [[ "$code" == "$expected" ]] || fail "$label EXPECTED_$expected_GOT_$code_NO_FURTHER_REQUESTS"
  echo "$label=$code PASS"
}
call_anon
call_owner GET /healthz 200 OWNER_GET_HEALTHZ
call_owner POST /api/staging/marketplace/owner 503 OWNER_POST_API_OFF
unset OWNER_ID_TOKEN
printf 'STATUS=PASS_WITH_LIMITS\nHTTP_REQUESTS_SENT=%s\nNO_IAM_CLOUD_WRITES_OR_DATA_CALLS=TRUE\n' "$N" >> "$OUT"
echo "C1B_HOSTED_OFF_TEST=PASS_WITH_LIMITS"
echo "REQUEST_COUNT=$N/6"
echo "NO_CLOUD_CONFIG_WRITE=TRUE"
echo "REPORT=$OUT"
