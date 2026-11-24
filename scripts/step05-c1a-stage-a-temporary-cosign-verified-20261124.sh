#!/usr/bin/env bash
# OLDX Task25 Step05 Stage A: fix ONLY missing cosign binary without system installation.
# Reuse previously cloned clean source; no Docker build, scan, Cloud metadata, IAM, billing, push or deploy.
# Official sigstore/cosign v3.1.5 Linux amd64 release asset sha256 pinned to GitHub official release API,
# read 2026-11-24; https://github.com/sigstore/cosign/releases/tag/v3.1.5
set -Eeuo pipefail
umask 077
SCRIPT="scripts/step05-c1a-stage-a-cosign-parent-once-20261124.sh"
MARKER="$HOME/.oldx-step05-stage-a-cosign-parent-attempted-20261124"
EXPECTED="912502def4baf810eaf36b210a4f51e1da214f9f6d664e2a9a2154cfc67ee0d6"
URL="https://github.com/sigstore/cosign/releases/download/v3.1.5/cosign-linux-amd64"
[[ -f "$SCRIPT" ]] || { echo "STOP: run from reviewed Step05 repo root"; exit 1; }
if [[ -e "$MARKER" ]]; then
  echo "STOP_ALREADY_ATTEMPTED: old signature attempt marker found; do not repeat"
  exit 0
fi
for x in bash git; do command -v "$x" >/dev/null || { echo "STOP_MISSING_TOOL: $x"; exit 1; }; done
# Existing installed cosign (if located later) is not silently replaced.
if command -v cosign >/dev/null 2>&1; then
  echo "USING_EXISTING_COSIGN=TRUE"
  exec bash "$SCRIPT"
fi
for x in curl sha256sum mktemp chmod; do
 command -v "$x" >/dev/null 2>&1 || { echo "STOP_MISSING_TOOL: $x"; exit 1; }
done
DIR="$(mktemp -d /tmp/oldx-cosign-stage-a.XXXXXXXX)"
trap 'rm -f -- "$DIR/cosign"; rmdir -- "$DIR" 2>/dev/null || true' EXIT
echo "COSIGN_SYSTEM_INSTALL=NO"
echo "COSIGN_RELEASE=OFFICIAL_SIGSTORE_V3.1.5"
echo "COSIGN_DOWNLOAD=ONE_CHECKSUM_PINNED_BINARY"
# No shell piping; downloaded executable is never run until its byte hash matches.
if ! curl --fail --location --silent --show-error --retry 0 --connect-timeout 20 --max-time 300 "$URL" -o "$DIR/cosign"; then
 echo "STOP_COSIGN_DOWNLOAD_FAILED_NO_SIGNATURE_ATTEMPT"
 exit 1
fi
if ! printf '%s  %s\n' "$EXPECTED" "$DIR/cosign" | sha256sum --check --status; then
 echo "STOP_COSIGN_CHECKSUM_MISMATCH_NOT_EXECUTED"
 exit 1
fi
chmod 700 "$DIR/cosign"
echo "COSIGN_OFFICIAL_RELEASE_SHA256=VERIFIED"
PATH="$DIR:$PATH" bash "$SCRIPT"
