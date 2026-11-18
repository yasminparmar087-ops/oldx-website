#!/usr/bin/env bash
# OLDX Step04: ONE conditional registry-only copy, explicitly approved by owner.
# No Docker build, Grype scan, Cloud Run, IAM, Rules, Billing, API or production changes.
# Once run, do NOT rerun even after an error: inspect Registry remotely first.
set -euo pipefail
umask 077

OWNER='yasminparmar087@gmail.com'
PROJECT='oldx-staging'
PACKAGE='oldx-step04-g2-d13818-a1'
REGISTRY='asia-south1-docker.pkg.dev'
REPO="${REGISTRY}/${PROJECT}/oldx-staging-images/${PACKAGE}"
DEST="${REPO}:g2-20261118-a1"
ARCHIVE='/mnt/d/OLDX/G2/g2-image-proof-d13818-a1/candidate.oci.tar'
ARCHIVE_SHA='44b2aae3c56cf3c93ab4aa1faa1839c2be6ace70a45c5a64404825752ba9ea5c'
INDEX='93b70b8b09255194974bc46c7e5942c81531261b81224bd80fa575330f7572e4'
AMD64='fde6b74beb8a62678fdc9df4598e5ef1affc2c8be0d89d3502938d4daac4fd68'
ORAS='/mnt/d/OLDX/G2/oras-v1.3.6-pinned-a1/oras'

stop() { printf '%s\n' "$1"; exit 1; }
[[ "$(gcloud config get-value account 2>/dev/null)" == "$OWNER" ]] || stop 'STOP_WRONG_OWNER'
[[ "$(gcloud config get-value project 2>/dev/null)" == "$PROJECT" ]] || stop 'STOP_WRONG_PROJECT'
impersonation="$(gcloud config get-value auth/impersonate_service_account 2>/dev/null || true)"
[[ -z "$impersonation" || "$impersonation" == '(unset)' ]] || stop 'STOP_IMPERSONATION'
[[ -f "$ARCHIVE" && -x "$ORAS" ]] || stop 'STOP_LOCAL_SOURCE_OR_ORAS_MISSING'
if printf '%s  %s\n' "$ARCHIVE_SHA" "$ARCHIVE" | sha256sum --status -c -; then
  echo 'PINNED_LOCAL_ARCHIVE_SHA256_MATCH'
else
  stop 'STOP_LOCAL_ARCHIVE_CHANGED'
fi

# One new package must be absent at the last read, but registry tagging is not
# an atomic "create only" operation. Stop on anything but an explicit 404.
if msg="$(gcloud artifacts packages describe "$PACKAGE" \
  --project="$PROJECT" --repository=oldx-staging-images --location=asia-south1 \
  --format='value(name)' 2>&1)"; then
  stop 'STOP_TARGET_PACKAGE_ALREADY_EXISTS'
else
  case "$msg" in
    *NOT_FOUND*|*'not found'*) echo 'TARGET_NAME_NOT_PRESENT_AT_WRITE_PREFLIGHT' ;;
    *) stop 'STOP_TARGET_ABSENCE_NOT_PROVEN' ;;
  esac
fi

# Keep the short-lived token in a temporary private auth config, not in D: or
# a process argument/history. Never print it. Remove it when this command ends.
TMP_AUTH_DIR="$(mktemp -d)" || stop 'STOP_PRIVATE_AUTH_DIRECTORY'
trap 'rm -rf -- "$TMP_AUTH_DIR"' EXIT
if gcloud auth print-access-token 2>/dev/null | "$ORAS" login \
  --username oauth2accesstoken --password-stdin \
  --registry-config "$TMP_AUTH_DIR/auth.json" "$REGISTRY" >/dev/null 2>&1; then
  echo 'ONE_COPY_PRIVATE_AUTH_PASS'
else
  stop 'STOP_PRIVATE_REGISTRY_LOGIN'
fi

# THIS is the one and only provider mutation. No --force, no platform filtering,
# no tag overwrite intentionally. Never retry after an ambiguous error.
echo 'ONE_REGISTRY_COPY_STARTED'
if "$ORAS" cp --from-oci-layout --no-tty \
  --to-registry-config "$TMP_AUTH_DIR/auth.json" \
  "$ARCHIVE@sha256:$INDEX" "$DEST" >/dev/null 2>&1; then
  echo 'ONE_REGISTRY_COPY_CLIENT_REPORTED_SUCCESS'
else
  stop 'STOP_COPY_OUTCOME_UNKNOWN_DO_NOT_RETRY'
fi

# Independently read back the remotely tagged root and the amd64 child.
# No subsequent write, image deletion, or automatic retry on any mismatch.
if remote_index="$("$ORAS" resolve --registry-config "$TMP_AUTH_DIR/auth.json" \
  "$DEST" 2>/dev/null)"; then
  [[ "$remote_index" == "sha256:$INDEX" ]] || stop 'STOP_REMOTE_INDEX_MISMATCH_DO_NOT_RETRY'
  echo 'REMOTE_INNER_INDEX_DIGEST_MATCH'
else
  stop 'STOP_REMOTE_INDEX_UNVERIFIED_DO_NOT_RETRY'
fi
if remote_amd64="$("$ORAS" manifest fetch --registry-config "$TMP_AUTH_DIR/auth.json" \
  --output - "$REPO@sha256:$AMD64" 2>/dev/null | sha256sum | cut -d' ' -f1)"; then
  [[ "$remote_amd64" == "$AMD64" ]] || stop 'STOP_REMOTE_AMD64_MISMATCH_DO_NOT_RETRY'
  echo 'REMOTE_AMD64_MANIFEST_DIGEST_MATCH'
else
  stop 'STOP_REMOTE_AMD64_UNVERIFIED_DO_NOT_RETRY'
fi

echo 'PRIVATE_REGISTRY_SINGLE_COPY_VERIFIED'
echo 'REGISTRY_SOURCE_INDEX=sha256:'"$INDEX"
echo 'CVE_RISK=9_HIGH_UNRESOLVED'
echo 'CLOUD_RUN_AND_PRODUCTION=NOT_CHANGED'
