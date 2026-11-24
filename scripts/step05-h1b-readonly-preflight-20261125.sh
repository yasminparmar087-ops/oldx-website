#!/usr/bin/env bash
# H1B P-phase ONLY: one bounded read-only Cloud account/project/target check.
# NEVER create SA, tag/push image, grant IAM, deploy or contact Cloud Run endpoints.
set -Eeuo pipefail
if [[ "$#" -ne 1 || "$1" != '--read-only-once' ]]; then
  echo 'HOLD: expected exactly --read-only-once. No Cloud operation performed.' >&2
  exit 2
fi
for tool in gcloud python3 timeout sha256sum; do
  command -v "$tool" >/dev/null 2>&1 || { echo "STOP: missing $tool" >&2; exit 2; }
done
umask 077
export CLOUDSDK_CORE_DISABLE_PROMPTS=1 CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK=1
PROJECT=oldx-staging
REGION=asia-south1
EXPECTED_PROJECT_NUMBER=38472235077
REPO=oldx-staging-images
NEW_SERVICE=oldx-c2-website-mediator
NEW_SA=oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com
MARKER="$HOME/.oldx-h1b-readonly-preflight-once-20261125"
if [[ -e "$MARKER" ]]; then
  echo 'STOP: H1B read-only preflight marker already consumed; inspect saved evidence, do not repeat.' >&2
  exit 2
fi
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
EVIDENCE="$HOME/oldx-h1b-readonly-preflight-$stamp"
mkdir -m 0700 -- "$EVIDENCE"
if ! ( set -C; printf '%s\n' "$EVIDENCE" > "$MARKER" ); then
  echo 'STOP: concurrent/existing one-shot preflight marker' >&2
  exit 2
fi
run_read() {
  local name="$1"; shift
  printf '%q ' "$@" > "$EVIDENCE/$name.command"
  printf '\n' >> "$EVIDENCE/$name.command"
  local rc=0
  timeout 40s "$@" > "$EVIDENCE/$name.stdout" 2> "$EVIDENCE/$name.stderr" || rc=$?
  printf '%s\n' "$rc" > "$EVIDENCE/$name.exit"
  return "$rc"
}
finish() {
  (cd "$EVIDENCE" && sha256sum -- *.command *.exit *.stdout *.stderr > SHA256SUMS) || true
  echo "PRIVATE_EVIDENCE=$EVIDENCE"
  echo "ONE_SHOT_MARKER=$MARKER"
}
trap finish EXIT

run_read active-operator gcloud auth list '--filter=status:ACTIVE' '--format=value(account)' || {
  echo 'STOP: cannot read active gcloud operator; no other lookup attempted'; exit 2;
}
if [[ ! -s "$EVIDENCE/active-operator.stdout" ]]; then
  echo 'STOP: no active operator'; exit 2
fi
run_read project gcloud projects describe "$PROJECT" '--format=json' || {
  echo 'STOP: project read failed; no target lookup attempted'; exit 2;
}
python3 - "$EVIDENCE/project.stdout" "$PROJECT" "$EXPECTED_PROJECT_NUMBER" <<'PY'
import json,sys
with open(sys.argv[1],encoding='utf-8') as file: data=json.load(file)
if data.get('projectId')!=sys.argv[2] or str(data.get('projectNumber'))!=sys.argv[3] or data.get('lifecycleState')!='ACTIVE':
    raise SystemExit('STOP: project identity not proven; no targets queried')
PY
run_read existing-registry gcloud artifacts repositories describe "$REPO" \
  '--project=oldx-staging' '--location=asia-south1' '--format=json' || {
  echo 'STOP: existing registry lookup failed; no target lookup attempted'; exit 2;
}
python3 - "$EVIDENCE/existing-registry.stdout" <<'PY'
import json,sys
with open(sys.argv[1],encoding='utf-8') as file: data=json.load(file)
if data.get('format')!='DOCKER' or not data.get('name','').endswith('/repositories/oldx-staging-images'):
    raise SystemExit('STOP: existing Registry repository does not match expected Docker repository')
PY
# These are only candidate exact-target readbacks. A nonzero result is NOT
# automatically NOT_FOUND: could be IAM403, transient failure or other status.
run_read candidate-new-service gcloud run services describe "$NEW_SERVICE" \
  '--project=oldx-staging' '--region=asia-south1' '--format=json' || true
run_read candidate-new-sa gcloud iam service-accounts describe "$NEW_SA" \
  '--project=oldx-staging' '--format=json' || true
if [[ "$(cat "$EVIDENCE/candidate-new-service.exit")" == 0 || "$(cat "$EVIDENCE/candidate-new-sa.exit")" == 0 ]]; then
  echo 'H1B_READONLY_RESULT=EXISTING_TARGET_COLLISION_STOP'
else
  echo 'H1B_READONLY_RESULT=TARGET_LOOKUPS_UNRESOLVED_MANUAL_404_VS_403_REVIEW'
fi
echo 'NO_IMAGE_PUSH_NO_CLOUD_WRITE_NO_DEPLOYMENT_NO_IAM_MUTATION'
echo 'H1B_OPERATIONAL_APPROVAL_STILL_REQUIRED'
