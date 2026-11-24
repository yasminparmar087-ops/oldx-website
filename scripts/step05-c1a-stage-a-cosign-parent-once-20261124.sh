#!/usr/bin/env bash
# OLDX Step05 Stage A: ONE narrowly consented publisher-signature public metadata check.
# NO cloud IAM/Billing/service/registry read or write. NO build/push/deploy/scan/test.
# Run from existing security-hardening-review worktree with cosign ALREADY installed.
set -Eeuo pipefail
umask 077
BRANCH="security-hardening-review"
PARENT="sha256:39b0407357c9fadf1a9708d22088f02de21f0e1e8a688474eea2d8701e7d5693"
CHILD="sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec"
INDEX="gcr.io/distroless/nodejs24-debian13:nonroot@${PARENT}"
DOCKERFILE="functions/staging-marketplace/Dockerfile.gateway-off"
MARKER="$HOME/.oldx-step05-stage-a-cosign-parent-attempted-20261124"
OUT="$HOME/oldx-step05-stage-a-publisher-proof-20261124.txt"

if [[ -e "$MARKER" ]]; then
  echo "STOP_ALREADY_ATTEMPTED: Do not repeat. Read the prior local report: $OUT"
  exit 0
fi
for exe in git grep cosign timeout date; do
  command -v "$exe" >/dev/null 2>&1 || { echo "STOP_MISSING_TOOL: $exe (do not auto-install)"; exit 0; }
done
[[ "$(git branch --show-current)" == "$BRANCH" ]] || { echo "STOP_WRONG_BRANCH"; exit 1; }
[[ -f "$DOCKERFILE" ]] || { echo "STOP_SOURCE_NOT_FOUND"; exit 1; }
grep -Fq "gcr.io/distroless/nodejs24-debian13:nonroot@${CHILD}" "$DOCKERFILE" || {
 echo "STOP_PINNED_CHILD_CHANGED"; exit 1;
}
git diff --quiet -- "$DOCKERFILE" || { echo "STOP_DOCKERFILE_DIRTY"; exit 1; }

# Only this new lookup is permitted by owner's Stage A.
# Existing parent-index -> linux/amd64 child metadata result is CONSUMED and NOT rerun.
{
 printf 'STAGE_A_READ_ONLY=true\n'
 printf 'SOURCE_BRANCH=%s\n' "$BRANCH"
 printf 'PINNED_CHILD=%s\n' "$CHILD"
 printf 'SIGNED_PARENT_INDEX=%s\n' "$PARENT"
 printf 'CHILD_IN_PARENT=HISTORICAL_CONSUMED_NOT_RERUN\n'
 printf 'DERIVED_IMAGE_LOCAL_ID=sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a\n'
 printf 'DERIVED_REGISTRY_DIGEST=NONE\n'
 printf 'DERIVED_IMAGE_SIGNATURE=NOT_PROVEN\n'
 printf 'SOURCE_COMMIT=%s\n' "$(git rev-parse HEAD)"
 printf 'PUBLISHER_POLICY=https://accounts.google.com|keyless@distroless.iam.gserviceaccount.com\n'
 printf 'SIGNATURE_RESULT=ATTEMPT_IN_PROGRESS\n'
} > "$OUT"
: > "$MARKER"  # one-attempt marker immediately before the network verification
set +e
# Verify pinned IMMUTABLE parent digest, NOT a moving tag, using official keyless identity.
# Capture command output privately; do not disclose full certificates/tokens.
timeout 150s cosign verify "$INDEX" \
 --certificate-oidc-issuer "https://accounts.google.com" \
 --certificate-identity "keyless@distroless.iam.gserviceaccount.com" \
 > "$OUT.cosign.json" 2> "$OUT.cosign.err"
RC=$?
set -e
if [[ "$RC" -eq 0 ]] && [[ -s "$OUT.cosign.json" ]]; then
 sed -i 's/SIGNATURE_RESULT=ATTEMPT_IN_PROGRESS/SIGNATURE_RESULT=PASS_PINNED_PARENT_ONLY/' "$OUT"
 echo "INDEX_SIGNATURE=PASS_PINNED_PARENT_ONLY"
else
 sed -i 's/SIGNATURE_RESULT=ATTEMPT_IN_PROGRESS/SIGNATURE_RESULT=UNVERIFIED_STOP/' "$OUT"
 echo "INDEX_SIGNATURE=UNVERIFIED_STOP (exit $RC)"
fi
echo "DERIVED_GATEWAY_SIGNATURE_AND_REMOTE_DIGEST=NOT_PROVEN"
echo "NO_CLOUD_WRITE=TRUE"
echo "REPORT=$OUT"
