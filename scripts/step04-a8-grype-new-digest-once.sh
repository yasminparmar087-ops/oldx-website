(
  set -Eeuo pipefail
  umask 077
  image='asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc'
  work='/tmp/oldx-a8-grype-new-digest-2506826f'
  marker="$HOME/.oldx-a8-grype-new-digest-2506826f-attempted"
  saved="$HOME/oldx-a8-grype-new-digest-2506826f.json.gz"
  archive="$work/grype_0.122.1_linux_amd64.tar.gz"
  expected='f1ba7e2917ee1395618de20a98da0aa7c0fb1788927797651047c50502a37538'

  if [ "$(uname -s)" != Linux ] || [ "$(uname -m)" != x86_64 ]; then
    echo 'STOP_A8_NEEDS_LINUX_AMD64'; exit 1
  fi
  if [ -e "$work" ] || [ -e "$marker" ] || [ -e "$saved" ]; then
    echo 'STOP_A8_GRYPE_EXISTING_ATTEMPT_NO_RETRY'; exit 1
  fi
  free_mib="$(df -Pk /tmp | awk 'NR==2 {print int($4/1024)}')"
  if [ "$free_mib" -lt 3000 ]; then
    echo 'STOP_A8_TMP_SCRATCH_TOO_SMALL'; exit 1
  fi
  if ! mkdir -m 700 "$work"; then
    echo 'STOP_A8_TMP_WORKDIR_CREATE_FAILED'; exit 1
  fi
  mkdir -m 700 "$work/db" "$work/cache" "$work/tmp"
  printf '{}\n' > "$work/empty.yaml"
  echo 'A8_GRYPE_NEW_RELEASE=v0.122.1'
  echo 'A8_DOWNLOAD_TO_TMP_ONLY=YES'

  if ! curl --fail --location --silent --show-error --retry 0 \
    --connect-timeout 20 --max-time 600 \
    'https://github.com/anchore/grype/releases/download/v0.122.1/grype_0.122.1_linux_amd64.tar.gz' \
    --output "$archive"; then
    echo 'STOP_A8_GRYPE_RELEASE_DOWNLOAD'; exit 1
  fi
  actual="$(sha256sum "$archive" | cut -d' ' -f1)"
  if [ "$actual" != "$expected" ]; then
    echo 'STOP_A8_GRYPE_RELEASE_SHA256_MISMATCH'; exit 1
  fi
  echo 'A8_OFFICIAL_GRYPE_ARCHIVE_SHA256=PASS'
  if ! tar -xzf "$archive" -C "$work" grype; then
    echo 'STOP_A8_GRYPE_TARBALL_CONTENT'; exit 1
  fi
  chmod 700 "$work/grype"
  export GRYPE_DB_CACHE_DIR="$work/db"
  export XDG_CACHE_HOME="$work/cache"
  export TMPDIR="$work/tmp"
  export GRYPE_DB_AUTO_UPDATE=true
  export GRYPE_CHECK_FOR_APP_UPDATE=false
  export DOCKER_CONFIG="$HOME/.docker"
  "$work/grype" version > "$work/scanner-version.txt" 2>&1

  if ! mkdir -m 700 "$marker"; then
    echo 'STOP_A8_GRYPE_MARKER_CREATE_FAILED'; exit 1
  fi
  echo 'A8_NEW_DIGEST_GRYPE_ATTEMPT=STARTED_ONCE'
  echo 'A8_IMAGE_SOURCE=PRIVATE_REGISTRY_IMMUTABLE_DIGEST'

  if timeout --signal=TERM --kill-after=30s 1800 \
    "$work/grype" --config "$work/empty.yaml" "registry:$image" \
      --scope squashed --output json > "$work/report.json" 2> "$work/scan.stderr"; then
    echo 'A8_GRYPE_SCAN_COMMAND_EXIT_CODE=0'
  else
    echo 'STOP_A8_NEW_IMAGE_GRYPE_SCAN_FAILED_NO_RETRY'
    echo 'A8_PRIVATE_ERROR_LOG=TMP_ONLY'
    exit 1
  fi

  if ! python3 - "$work/report.json" "$image" <<'PY'
import collections, hashlib, json, pathlib, sys
path=pathlib.Path(sys.argv[1]); image=sys.argv[2]
r=json.loads(path.read_text(encoding='utf-8'))
if not isinstance(r.get('matches'),list) or not isinstance(r.get('source'),dict):
    raise SystemExit('A8_GRYPE_REPORT_SCHEMA_INVALID')
target=r['source'].get('target') or {}
ref=str(target.get('userInput',''))
identity=image in ref or image in str(target.get('manifestDigest',''))
counts=collections.Counter(str((m.get('vulnerability') or {}).get('severity','UNKNOWN')).upper()
    for m in r['matches'])
ids=sorted({str((m.get('vulnerability') or {}).get('id','')) for m in r['matches']
    if str((m.get('vulnerability') or {}).get('severity','')).upper() in ('CRITICAL','HIGH')})
db=(r.get('descriptor') or {}).get('db') or {}
print('A8_GRYPE_REPORT_SCHEMA=PASS')
print('A8_GRYPE_SOURCE_IMAGE_REFERENCE_MATCH='+str(identity))
print('A8_GRYPE_MATCH_TOTAL='+str(len(r['matches'])))
for sev in ['CRITICAL','HIGH','MEDIUM','LOW','NEGLIGIBLE','UNKNOWN']:
    print('A8_GRYPE_'+sev+'='+str(counts.get(sev,0)))
print('A8_GRYPE_SEVERE_UNIQUE_IDS='+str(len(ids)))
print('A8_GRYPE_SEVERE_IDS_FIRST_25='+','.join(ids[:25]))
print('A8_GRYPE_DB_BUILT='+str(db.get('built','UNREPORTED')))
print('A8_GRYPE_REPORT_SHA256='+hashlib.sha256(path.read_bytes()).hexdigest())
print('A8_VULNERABILITY_TRIAGE=REQUIRED_NOT_AUTOMATIC_PASS')
PY
  then
    echo 'STOP_A8_GRYPE_REPORT_PARSE_NO_RETRY'; exit 1
  fi

  gzip -n -c "$work/report.json" > "$work/report.json.gz"
  bytes="$(stat -c %s "$work/report.json.gz")"
  avail_kib="$(df -Pk "$HOME" | awk 'NR==2 {print $4}')"
  if [ "$bytes" -lt "$((avail_kib*1024 - 8*1024*1024))" ]; then
    cp -n "$work/report.json.gz" "$saved"
    chmod 600 "$saved"
    echo 'A8_PRIVATE_FULL_REPORT=HOME_COMPRESSED_SAVED'
  else
    echo 'A8_PRIVATE_FULL_REPORT=TMP_ONLY_HOME_CAPACITY_LIMIT'
  fi
  echo 'A8_NEW_IMAGE_SCAN=ONE_COMPLETED_REPORT'
  echo 'A8_CLOUD_WRITES=NONE'
  echo 'A8_BUILD_AND_SLSA_RERUN=NONE'
  echo 'A8_STEP04=HOLD_PENDING_FINDINGS_AND_RUNTIME'
)
