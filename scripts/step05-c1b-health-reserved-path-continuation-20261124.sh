#!/usr/bin/env bash
# OLDX Step05 C1B continuation after ONE /healthz 404 on Google-reserved path.
# Under existing owner max6 HTTP/20min consent: exactly 3 ADDITIONAL calls to /health and OFF-only API.
# NO retry of /healthz, no Cloud writes, no IAM modification, no token logging.
set -Eeuo pipefail
set +x
umask 077
fail() { printf 'C1B_CONTINUE_STOP=%s\n' "$*" >&2; exit 1; }
TARGET="https://oldx-step05-gateway-38472235077.asia-south1.run.app"
PRIOR_MARK="$HOME/.oldx-step05-c1b-off-hosted-once-20261124"
PRIOR_REPORT="$HOME/oldx-step05-c1b-off-hosted-result-20261124.txt"
LOCK="$HOME/.oldx-step05-c1b-health-continuation-once-20261124"
REPORT="$HOME/oldx-step05-c1b-health-continuation-result-20261124.txt"
SERVER_BLOB="25d2679bd4ea970c8b8a32a778fb26eb347bcdd6"
for cmd in git grep sed curl date; do command -v "$cmd" >/dev/null 2>&1 || fail "MISSING_$cmd"; done
[[ "$(git branch --show-current)" == "security-hardening-review" ]] || fail WRONG_BRANCH
[[ "$(git rev-parse HEAD:functions/staging-marketplace/cloud-run-gateway-off-server.mjs)" == "$SERVER_BLOB" ]] || fail SOURCE_DRIFT
[[ -z "$(git status --porcelain -- functions/staging-marketplace/cloud-run-gateway-off-server.mjs)" ]] || fail SOURCE_DIRTY
[[ "$(uname -s)" == Linux && -d /mnt/c ]] || fail NOT_LOCAL_OWNER_WSL
[[ ! -e "$LOCK" && ! -e "$REPORT" ]] || fail ALREADY_ATTEMPTED_NO_REPEAT
[[ -f "$PRIOR_MARK" && -f "$PRIOR_REPORT" ]] || fail PRIOR_RECEIPT_MISSING
grep -Fxq 'HTTP_ATTEMPT_1=ANONYMOUS_GET_HEALTHZ' "$PRIOR_REPORT" || fail PRIOR_METHOD_MISMATCH
grep -Fxq 'HTTP_1_CODE=404' "$PRIOR_REPORT" || fail PRIOR_CODE_NOT_404
grep -Fxq 'STATUS=STARTED' "$PRIOR_REPORT" || fail PRIOR_STATUS_UNEXPECTED
if grep -Eq '^HTTP_ATTEMPT_[2-9]|^HTTP_[2-9]_CODE=' "$PRIOR_REPORT"; then fail PRIOR_ADDITIONAL_CALL_FOUND; fi
prior_utc="$(sed -n 's/^C1B_FIRST_ATTEMPT_UTC=//p' "$PRIOR_MARK")"
[[ -n "$prior_utc" ]] || fail PRIOR_TIMESTAMP_MISSING
prior_epoch="$(date -u -d "$prior_utc" +%s)" || fail PRIOR_TIMESTAMP_INVALID
now="$(date +%s)"
(( now >= prior_epoch && now - prior_epoch < 1200 )) || fail ORIGINAL_20MIN_WINDOW_EXPIRED
# Token from owner Windows gcloud stdin, never echoed or written.
[[ ! -t 0 ]] || fail TOKEN_STDIN_REQUIRED
IFS= read -r -t 40 ID_TOKEN || [[ -n "$ID_TOKEN" ]] || fail TOKEN_NOT_RECEIVED
ID_TOKEN="${ID_TOKEN%$'\r'}"
[[ "$ID_TOKEN" =~ ^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$ ]] || fail INVALID_ID_TOKEN
# One-use lock BEFORE new HTTP calls. Do NOT erase/retry on any outcome.
( set -C; printf 'START_UTC=%s\nPRIOR_HTTP=1\n' "$(date -u +%FT%TZ)" > "$LOCK" ) 2>/dev/null || fail LOCK_COLLISION
printf 'SCOPE=NEW_PRIVATE_OFF_GATEWAY_ONLY\nPRIOR_HTTP=1\nHTTP_LIMIT=6\nWINDOW_SECONDS=1200\nRESULT=STARTED\n' > "$REPORT"
check() {
  now="$(date +%s)"
  (( now >= prior_epoch && now - prior_epoch < 1200 )) || fail ORIGINAL_WINDOW_EXPIRED_NO_RETRY
}
check
printf 'HTTP_ATTEMPT_2=ANON_GET_HEALTH\n' >> "$REPORT"
anon="$(curl --silent --show-error --proto '=https' --tlsv1.2 --connect-timeout 10 --max-time 20 --retry 0 --max-redirs 0 --output /dev/null --write-out '%{http_code}' --request GET --url "$TARGET/health")" || fail ANON_HEALTH_TRANSPORT_FAILURE
printf 'HTTP_2_CODE=%s\n' "$anon" >> "$REPORT"
if [[ "$anon" != 401 && "$anon" != 403 ]]; then fail "ANON_HEALTH_UNEXPECTED_HTTP_$anon"; fi
echo "ANON_GET_HEALTH=$anon PASS"
owner_call() {
  local seq="$1" label="$2" method="$3" path="$4" expected="$5" actual
  check
  printf 'HTTP_ATTEMPT_%s=%s\n' "$seq" "$label" >> "$REPORT"
  # ID token is piped to curl config on stdin; never in argv, logs, or output.
  if [[ "$method" == POST ]]; then
    actual="$(printf 'header = "Authorization: Bearer %s"\n' "$ID_TOKEN" |
      curl --config - --silent --show-error --proto '=https' --tlsv1.2 --connect-timeout 10 --max-time 20 --retry 0 --max-redirs 0 --output /dev/null --write-out '%{http_code}' --request POST --header 'Content-Type: application/json' --data-binary '{}' --url "$TARGET$path")" || fail "$label TRANSPORT_FAILURE"
  else
    actual="$(printf 'header = "Authorization: Bearer %s"\n' "$ID_TOKEN" |
      curl --config - --silent --show-error --proto '=https' --tlsv1.2 --connect-timeout 10 --max-time 20 --retry 0 --max-redirs 0 --output /dev/null --write-out '%{http_code}' --request GET --url "$TARGET$path")" || fail "$label TRANSPORT_FAILURE"
  fi
  printf 'HTTP_%s_CODE=%s\n' "$seq" "$actual" >> "$REPORT"
  [[ "$actual" == "$expected" ]] || fail "$label EXPECTED_$expected GOT_$actual"
  printf '%s=%s PASS\n' "$label" "$actual"
}
owner_call 3 OWNER_GET_HEALTH GET /health 200
owner_call 4 OWNER_POST_API_OFF POST /api/staging/marketplace/owner 503
unset ID_TOKEN
printf 'RESULT=PASS_WITH_LIMITS\nHTTP_TOTAL=4_OF_6\nNO_CLOUD_MUTATION=TRUE\n' >> "$REPORT"
echo "C1B_CONTINUATION=PASS_WITH_LIMITS"
echo "HTTP_TOTAL=4/6"
echo "NO_CLOUD_WRITE=TRUE"
echo "REPORT=$REPORT"
