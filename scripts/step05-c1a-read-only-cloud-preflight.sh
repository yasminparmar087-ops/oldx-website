#!/usr/bin/env bash
# OLDX Step05 C1A: owner-approved target-only Google Cloud READ-ONLY preflight.
# No create/update/delete/deploy, APIs enabled, HTTP invocation, tokens printed, or repeated A8 checks.
set -Eeuo pipefail
umask 077
PROJECT='oldx-staging'
REGION='asia-south1'
SERVICE='oldx-step05-gateway'
RUNTIME_SA='oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com'
REGISTRY='oldx-staging-images'
for x in gcloud python3 mktemp timeout; do command -v "$x" >/dev/null || { echo "STOP: missing $x"; exit 1; }; done
ACTUAL_PROJECT="$(gcloud config get-value project 2>/dev/null)" || { echo "STOP: cannot read active project"; exit 1; }
[[ "$ACTUAL_PROJECT" == "$PROJECT" ]] || { echo "STOP: wrong active project (expected oldx-staging)"; exit 1; }
ACTIVE="$(gcloud auth list --filter='status:ACTIVE' --format='value(account)' 2>/dev/null | head -n1)" || true
[[ -n "$ACTIVE" ]] || { echo 'STOP: No active gcloud identity; no login or credential change will be attempted'; exit 1; }
SCRATCH="$(mktemp -d /tmp/oldx-step05-c1a-preflight.XXXXXXXX)"
trap 'rm -rf -- "$SCRATCH"' EXIT
OUT="$HOME/oldx-step05-c1a-readonly-$(date -u +%Y%m%dT%H%M%SZ).txt"
mask="$(python3 - "$ACTIVE" <<'PY'
import sys
s=sys.argv[1]
if '@' not in s:print('NON_EMAIL_PRINCIPAL_REDACTED')
else:
 user,dom=s.rsplit('@',1)
 print(user[:2]+'***@'+dom)
PY
)"
printf 'PROJECT=%s\nREGION=%s\nACTIVE_OPERATOR_ACCOUNT_HINT=%s\n' "$PROJECT" "$REGION" "$mask" > "$OUT"
printf 'ACTIVE_OPERATOR_EXACT_EMAIL=PRIVATE_NOT_IN_REPORT\nTESTER_ACCOUNT=UNSELECTED_BY_OWNER\n' >> "$OUT"
STATUS='UNVERIFIED'
# Every remote call below is a METADATA GET; no token printing, no mutation, no generic A8 inventory.
read_only(){
 local label="$1"
 shift
 local stderr="$SCRATCH/$label.err"
 if timeout 90s gcloud --quiet "$@" --format=json >"$SCRATCH/$label.json" 2>"$stderr"; then
   STATUS='OK'
 else
   local rc="$?"
   if grep -Eqi 'not found|NOT_FOUND|does not exist|cannot find service' "$stderr"; then
     STATUS='NOT_FOUND_REPORTED'
   elif grep -Eqi 'PERMISSION_DENIED|permission denied|does not have permission|403|forbidden' "$stderr"; then
     STATUS='UNVERIFIED_PERMISSION_DENIED'
   elif [[ "$rc" == 124 ]]; then
     STATUS='UNVERIFIED_TIMEOUT'
   else
     STATUS='UNVERIFIED_OTHER_ERROR'
   fi
 fi
 printf '%s_QUERY=%s\n' "$label" "$STATUS" >> "$OUT"
}
read_only PROJECT_METADATA projects describe "$PROJECT"
if [[ "$STATUS" != 'OK' ]]; then
  printf 'STATUS=STOP_PROJECT_NOT_CONFIRMED\nNO_CLOUD_MUTATIONS=TRUE\n' >> "$OUT"
  cat "$OUT"
  exit 0
fi
python3 - "$SCRATCH/PROJECT_METADATA.json" "$OUT" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
with open(sys.argv[2],'a') as o:
 o.write('PROJECT_LIFECYCLE_STATE='+str(d.get('lifecycleState','UNKNOWN'))+'\n')
PY

# These TWO exact NEW resources are only proposals. Existing names are collision STOPs.
read_only NEW_GATEWAY_SERVICE run services describe "$SERVICE" --project="$PROJECT" --region="$REGION"
if [[ "$STATUS" == 'OK' ]]; then
  printf 'C1A_SERVICE_NAME_COLLISION=YES_STOP\n' >> "$OUT"
elif [[ "$STATUS" == 'NOT_FOUND_REPORTED' ]]; then
  printf 'C1A_SERVICE_NAME_COLLISION=NOT_FOUND_REPORTED_NOT_FINAL_PROOF\n' >> "$OUT"
else
  printf 'C1A_SERVICE_NAME_COLLISION=UNKNOWN_STOP\n' >> "$OUT"
fi
read_only NEW_RUNTIME_SA iam service-accounts describe "$RUNTIME_SA" --project="$PROJECT"
if [[ "$STATUS" == 'OK' ]]; then
  printf 'C1A_SA_NAME_COLLISION=YES_STOP\n' >> "$OUT"
elif [[ "$STATUS" == 'NOT_FOUND_REPORTED' ]]; then
  printf 'C1A_SA_NAME_COLLISION=NOT_FOUND_REPORTED_NOT_FINAL_PROOF\n' >> "$OUT"
else
  printf 'C1A_SA_NAME_COLLISION=UNKNOWN_STOP\n' >> "$OUT"
fi

# Reuse only the exact prior Registry candidate; never inspect/push other artifacts.
read_only PROPOSED_EXISTING_REGISTRY artifacts repositories describe "$REGISTRY" --location="$REGION" --project="$PROJECT"
if [[ "$STATUS" == 'OK' ]]; then
  python3 - "$SCRATCH/PROPOSED_EXISTING_REGISTRY.json" "$OUT" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
with open(sys.argv[2],'a') as o:
 o.write('EXISTING_REGISTRY_FORMAT='+str(d.get('format','UNKNOWN'))+'\n')
 o.write('EXISTING_REGISTRY_LOCATION='+str(d.get('name','UNKNOWN').split('/locations/')[-1].split('/')[0])+'\n')
PY
fi

# Billing linkage != current spend or permission to incur cost. Never reveal account ID.
read_only PROJECT_BILLING_LINK billing projects describe "$PROJECT"
if [[ "$STATUS" == 'OK' ]]; then
  python3 - "$SCRATCH/PROJECT_BILLING_LINK.json" "$OUT" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
with open(sys.argv[2],'a') as o:
 o.write('BILLING_ENABLED='+str(d.get('billingEnabled','UNKNOWN'))+'\n')
 o.write('BILLING_ACCOUNT_LINK_PRESENT='+str(bool(d.get('billingAccountName')))+'\n')
PY
fi

# Narrow NEW C1A direct project-binding snapshot, not the prior Step04 IAM audit.
# No usernames other than the active operator are emitted, and no org/folder inherited roles are inferred.
read_only C1A_DIRECT_PROJECT_IAM projects get-iam-policy "$PROJECT"
if [[ "$STATUS" == 'OK' ]]; then
  python3 - "$SCRATCH/C1A_DIRECT_PROJECT_IAM.json" "$OUT" "$ACTIVE" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
active=sys.argv[3]
roles=set()
owner_count=editor_count=0
for b in d.get('bindings',[]):
 members=b.get('members',[])
 role=b.get('role','')
 if role=='roles/owner':owner_count+=len(members)
 if role=='roles/editor':editor_count+=len(members)
 if 'user:'+active in members or 'serviceAccount:'+active in members:roles.add(role)
with open(sys.argv[2],'a') as o:
 o.write('DIRECT_PROJECT_OWNER_BINDING_MEMBER_COUNT='+str(owner_count)+'\n')
 o.write('DIRECT_PROJECT_EDITOR_BINDING_MEMBER_COUNT='+str(editor_count)+'\n')
 o.write('ACTIVE_OPERATOR_DIRECT_PROJECT_ROLE_HINTS='+(','.join(sorted(roles)) or 'NONE_OBSERVED')+'\n')
 o.write('EFFECTIVE_INHERITED_AND_CONDITIONAL_IAM=NOT_PROVEN\n')
PY
fi
printf 'CURRENT_GROSS_PROVIDER_SPEND_INR=UNVERIFIED_NOT_RETURNED_BY_LINKAGE\n' >> "$OUT"
printf 'REGIONAL_SKU_AND_TAX_INR=UNVERIFIED\n' >> "$OUT"
printf 'GATEWAY_IMAGE_REMOTE_REGISTRY_DIGEST=NOT_PUBLISHED\n' >> "$OUT"
printf 'C1A_12_HIGH_CVE_OWNER_ACCEPTANCE=NOT_GRANTED\n' >> "$OUT"
printf 'C1A_WRITES_AND_HOSTED_CALLS=NOT_AUTHORIZED\n' >> "$OUT"
printf 'STEP05_HOSTED=BLOCKED\nPRODUCTION=NO_GO\nNO_CLOUD_MUTATIONS=TRUE\n' >> "$OUT"
printf '=== SAFE C1A READ-ONLY PREFLIGHT SUMMARY ===\n'
cat "$OUT"
printf '=== SUMMARY FILE ===\n%s\n' "$OUT"
