#!/usr/bin/env bash
# ONE owner-approved WSL2 scan-only recovery of the EXACT already built OLDX Step05 OFF gateway.
# Never builds, uploads, deploys, deletes images, touches IAM/Firebase, or scans old A8.
set -Eeuo pipefail
umask 077
say(){ printf '%s\n' "$*"; }
fail(){ printf 'STOP: %s\n' "$*" >&2; exit 1; }
PIN='sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a'
TAG='oldx-step05-gateway-off:wsl-once-20261124-801'
SYFT_SHA='bf52519eb57f675d47c07d43213cb6dff6449f3d6d1147ff6701ed91f44eef0c'
GRYPE_SHA='e9da18cc1429e786722e32161288103600efffd8e483c90761f90485bd1bec85'
SYFT_URL='https://github.com/anchore/syft/releases/download/v1.57.1/syft_1.57.1_linux_amd64.tar.gz'
GRYPE_URL='https://github.com/anchore/grype/releases/download/v0.121.3/grype_0.121.3_linux_amd64.tar.gz'
for exe in docker git curl sha256sum tar python3 timeout df awk; do
 command -v "$exe" >/dev/null 2>&1 || fail "Required command unavailable: $exe"
done
[[ "$(uname -s)" == Linux && "$(uname -m)" == x86_64 ]] || fail 'WSL Linux AMD64 required'
grep -qiE 'microsoft|wsl' /proc/sys/kernel/osrelease || fail 'WSL2 only'
[[ "$(docker context show)" == default && -z "${DOCKER_HOST:-}" ]] || fail 'Default local Docker daemon required'
[[ "$(docker info --format '{{.OSType}}/{{.Architecture}}' 2>/dev/null)" == linux/x86_64 || "$(docker info --format '{{.OSType}}/{{.Architecture}}' 2>/dev/null)" == linux/amd64 ]] || fail 'Local Linux AMD64 Docker Engine unavailable'
[[ "$(docker image inspect "$TAG" --format '{{.Id}}' 2>/dev/null)" == "$PIN" ]] || fail 'The exact previously approved image/tag is missing or differs; DO NOT BUILD'
[[ "$(docker image inspect "$PIN" --format '{{.Config.User}}' 2>/dev/null)" == '65532:65532' ]] || fail 'Unexpected image user'
[[ "$(docker image inspect "$PIN" --format '{{.Os}}/{{.Architecture}}' 2>/dev/null)" == 'linux/amd64' ]] || fail 'Wrong image platform'
[[ -d /mnt/c ]] || fail 'Windows C: mount unavailable'
wsl_avail=$(df -Pk /tmp | awk 'NR==2 {print $4}')
win_avail=$(df -Pk /mnt/c | awk 'NR==2 {print $4}')
[[ "$wsl_avail" =~ ^[0-9]+$ && "$win_avail" =~ ^[0-9]+$ ]] || fail 'Disk information unavailable'
(( wsl_avail >= 5242880 && win_avail >= 8388608 )) || fail 'Need 5GiB WSL scratch and 8GiB actual C: free, no cleanup'
OUT="$HOME/oldx-step05-scan-recovery-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -m 700 "$OUT" || fail 'Cannot create evidence folder'
LOCK="$HOME/.oldx-step05-existing-image-scan-recovery-consumed"
# No repeated scans permitted on this approval; resume is internal to ONE download step.
( set -C; printf 'START=%s IMAGE=%s\n' "$(date -u +%FT%TZ)" "$PIN" > "$LOCK" ) 2>/dev/null || fail 'This separate scan-only approval was already consumed'
STAGE='START'
on_exit(){
 local rc=$?
 trap - EXIT
 if ((rc != 0)); then
  printf 'STATUS=STOP_AT_%s\n' "$STAGE" >> "$OUT/summary.txt" 2>/dev/null || true
  say "STOP at $STAGE; image and evidence preserved. Do NOT rerun one-shot."
  say "EVIDENCE=$OUT"
 fi
 exit "$rc"
}
trap on_exit EXIT
printf 'MODE=SCAN_ONLY_NO_BUILD\nPINNED_LOCAL_IMAGE=%s\nEXISTING_TAG=%s\nEVIDENCE=%s\n' "$PIN" "$TAG" "$OUT" | tee "$OUT/summary.txt"
mkdir -m 700 "$OUT/assets" "$OUT/tools" "$OUT/temp" "$OUT/grype-db"

# Partial files are retained in OUT/assets between timed attempts. Downloads do not re-run scans.
# Original 120-second timeout is replaced by bounded 10-minute resumable segments.
resumable_download(){
 local label="$1" url="$2" expect="$3" target="$4" count=0
 local log="$OUT/$label-download.log"
 : > "$log"
 while ((count < 5)); do
  count=$((count+1))
  printf '%s attempt %s/5 (resume partial, bounded 600s)\n' "$label" "$count" | tee -a "$log"
  if curl --proto '=https' --tlsv1.2 -fLsS -C - --retry 0 \
       --connect-timeout 25 --max-time 600 -o "$target" "$url" >>"$log" 2>&1; then
   if printf '%s  %s\n' "$expect" "$target" | sha256sum -c - >>"$log" 2>&1; then
    printf '%s_SHA256=VERIFIED\n' "$label" | tee -a "$OUT/summary.txt"
    return 0
   fi
   fail "$label checksum did not match official release digest; do not execute"
  fi
  if [[ -s "$target" ]]; then
   printf 'PARTIAL_%s_BYTES=%s\n' "$label" "$(wc -c < "$target")" | tee -a "$log"
  fi
  if ((count < 5)); then sleep 2; fi
 done
 fail "$label download did not finish within five bounded resume attempts; inspect $log"
}

STAGE='SAVE_SAME_LOCAL_IMAGE'
say 'STEP: export EXACT existing local image; NO docker build or registry access'
docker save -o "$OUT/gateway-image.tar" "$TAG" >"$OUT/docker-save.log" 2>&1 || fail 'Local docker save failed'
[[ -s "$OUT/gateway-image.tar" ]] || fail 'Saved local image archive is empty'
sha256sum "$OUT/gateway-image.tar" > "$OUT/image-tar.sha256"

STAGE='DOWNLOAD_SYFT'
resumable_download SYFT "$SYFT_URL" "$SYFT_SHA" "$OUT/assets/syft.tgz"
tar -xzf "$OUT/assets/syft.tgz" -C "$OUT/tools" syft || fail 'Syft archive extraction failed'
chmod 700 "$OUT/tools/syft"

STAGE='SYFT_SCAN'
say 'STEP: one Syft SBOM scan of saved NEW Gateway image archive'
export TMPDIR="$OUT/temp" GOMAXPROCS=2 GOMEMLIMIT=1400MiB SYFT_CHECK_FOR_APP_UPDATE=false
if ! timeout --signal=TERM --kill-after=10s 600 "$OUT/tools/syft" \
   "docker-archive:$OUT/gateway-image.tar" -o "syft-json=$OUT/sbom.syft.json" \
   >"$OUT/syft.stdout.log" 2>"$OUT/syft.stderr.log"; then
 fail 'Syft SBOM generation failed; inspect syft.stderr.log (image retained)'
fi
python3 - "$OUT/sbom.syft.json" <<'PY'
import json,sys,os
p=sys.argv[1]
assert os.path.getsize(p)>0, 'Empty SBOM'
r=json.load(open(p))
assert isinstance(r.get('artifacts'),list), 'Not Syft JSON SBOM'
print('SYFT_SBOM_JSON=VALID')
PY
printf 'SYFT_SBOM=PASS\n' | tee -a "$OUT/summary.txt"
STAGE='SYFT_CONVERSION'
if ! timeout --signal=TERM --kill-after=10s 120 "$OUT/tools/syft" convert \
 "$OUT/sbom.syft.json" -o "cyclonedx-json=$OUT/sbom.cdx.json" \
 >"$OUT/syft-convert.stdout.log" 2>"$OUT/syft-convert.stderr.log"; then
 fail 'CycloneDX conversion failed; original Syft JSON preserved'
fi
python3 - "$OUT/sbom.cdx.json" <<'PY'
import json,sys,os
p=sys.argv[1]
assert os.path.getsize(p)>0 and json.load(open(p)).get('bomFormat')=='CycloneDX'
print('CYCLONEDX_SBOM=VALID')
PY
printf 'CYCLONEDX_SBOM=PASS\n' | tee -a "$OUT/summary.txt"

STAGE='DOWNLOAD_GRYPE'
resumable_download GRYPE "$GRYPE_URL" "$GRYPE_SHA" "$OUT/assets/grype.tgz"
tar -xzf "$OUT/assets/grype.tgz" -C "$OUT/tools" grype || fail 'Grype archive extraction failed'
chmod 700 "$OUT/tools/grype"

STAGE='GRYPE_VULNERABILITY_SCAN'
say 'STEP: one Grype vulnerability scan of NEW Gateway Syft JSON SBOM'
export GRYPE_DB_CACHE_DIR="$OUT/grype-db" GRYPE_CHECK_FOR_APP_UPDATE=false
if ! timeout --signal=TERM --kill-after=10s 1200 "$OUT/tools/grype" \
 "sbom:$OUT/sbom.syft.json" -o json >"$OUT/grype-report.json" 2>"$OUT/grype.stderr.log"; then
 fail 'Grype scan failed; inspect Grype stderr and DB download error; image/SBOM retained'
fi
python3 - "$OUT/grype-report.json" "$OUT/summary.txt" <<'PY'
import collections,json,sys,os
p=sys.argv[1]
assert os.path.getsize(p)>0,'Empty Grype result'
r=json.load(open(p)); m=r.get('matches')
assert isinstance(m,list), 'No Grype matches array'
sev=collections.Counter(x.get('vulnerability',{}).get('severity','UNKNOWN') for x in m)
ids=sorted({x.get('vulnerability',{}).get('id') for x in m if x.get('vulnerability',{}).get('severity') in ('High','Critical') and x.get('vulnerability',{}).get('id')})
summary=(f'GRYPE_REPORT_VALID=PASS\nMATCH_COUNT={len(m)}\nSEVERITIES={dict(sev)}\n'
 f'DISTINCT_HIGH_CRITICAL_IDS={len(ids)}\nHIGH_CRITICAL_CVE_IDS={",".join(ids)}\n')
print(summary,end='');open(sys.argv[2],'a').write(summary)
PY
sha256sum "$OUT/sbom.syft.json" "$OUT/sbom.cdx.json" "$OUT/grype-report.json" > "$OUT/reports.sha256"
STAGE='DONE'
printf 'STATUS=SCAN_ONLY_COMPLETE_PENDING_SECURITY_REVIEW\nNO_BUILD_NO_PUSH_NO_CLOUD_NO_IAM=TRUE\n' | tee -a "$OUT/summary.txt"
say "DONE — same local image retained. SUMMARY=$OUT/summary.txt"
