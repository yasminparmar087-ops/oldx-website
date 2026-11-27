# BAJUTO / OLDX Step05 H2Z — no-repeat read-only PROJECT IAM + VPC origin discovery

## Confirmed prior endpoint (28 Nov 2026 ~00:02 IST)

- H2W one new private/internal-only OFF Cloud Run Gateway and one direct Owner Invoker IAM binding: **OWNER ACTUAL PASS**, consumed. Target service UID `2d87153f-155e-409f-a418-463c785d8467`; do not confuse this with attached Gateway SA UID `107238619872767759560`.
- H2Y raw script output: `STOP_NEW_REVISION_READY_NOT_VERIFIED` due **omitted protobuf default-false `reconciling` field**. The existing same response independently supports `CONTROL_PLANE_READY_PASS_WITH_LIMITS`, because observedGeneration matched generation 1, latest created==latest ready, terminalCondition succeeded and traffic status 100%. **This is a post-hoc evaluation, NOT a new HTTP test or raw H2Y PASS.** Do not rerun H2X/H2Y.
- Exact immutable remote H2U Gateway image `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`. New service ingress `INGRESS_TRAFFIC_INTERNAL_ONLY`, `OLDX_H2U_MODE=OFF`, default minimum 0.
- Actual authenticated **hosted HTTP OFF-only response is NOT tested**. Inherited/effective IAM, KMS real sign, Firestore durable one-sign budget, full derived-image security/provenance remain OPEN. Production and H2 = **NO-GO**.

## Why a different H2Z read, not repeating H2W/H2Y or opening ingress

Google Cloud Run official guidance says a Cloud Run-to-Cloud Run request to an internal-only destination requires suitable VPC routing; same-project identity alone cannot establish internal origin. There is no justification to switch ingress to ALL or loosen IAM simply to test. A VPC list is **inventory, not proof** a callable internal origin exists. IAM bindings on a service are not an effective project/ancestor IAM policy audit. References:
- https://docs.cloud.google.com/run/docs/securing/ingress
- https://docs.cloud.google.com/run/docs/securing/private-networking
- https://docs.cloud.google.com/resource-manager/reference/rest/v1/projects/getIamPolicy
- https://docs.cloud.google.com/compute/docs/reference/rest/v1/networks/list
- https://docs.cloud.google.com/compute/docs/reference/rest/v1/subnetworks/list

## New H2Z SOURCE-ONLY work created and checked in GitHub

- Script: `scripts/step05_h2z_project_iam_vpc_readonly_once_20261128.py`
- Creation commit: `41ea6a02da650fdcc6389fe62b54249f0b7f6e7f`
- Verified Git blob SHA-1: `92f01b55d16d89672c0cc95760df6bd0569043b6`
- Owner execution: **NOT ATTEMPTED**. Cloud writes: **NONE** by assistant. GitHub readback static source/scope checks PASS; actual Python AST/Ubuntu WSL/Cloud read outcome **NOT YET TESTED**. Old successful tests and builds deliberately not repeated.
- Guard: root Ubuntu WSL, previously isolated native Google Cloud SDK, exact Owner + project, verified old H2W PASS marker, immutable service UID/image, exact user-provided flag. Local marker `/root/.oldx-step05-h2z-project-iam-vpc-readonly-once-20261128` is created **before the FIRST Google API call**; if present, never reset/delete/retry.
- Exactly **THREE distinct read-only Google API methods**, no other resource GET and no hosted HTTP:
  1. **POST** `https://cloudresourcemanager.googleapis.com/v1/projects/oldx-staging:getIamPolicy` with policy version 3 — despite HTTP POST, this is a **getIamPolicy/read-only** operation, *not* `:setIamPolicy`.
  2. GET `https://compute.googleapis.com/compute/v1/projects/oldx-staging/global/networks?maxResults=100`
  3. GET `https://compute.googleapis.com/compute/v1/projects/oldx-staging/regions/asia-south1/subnetworks?maxResults=100`
- Caps: at most 3 API calls, <=256 KiB per response, <=100 network/subnet list items each, no pagination retry. Any HTTP403/disabled API, unexpected shape, response cap or next-page token yields STOP/UNKNOWN; do not infer absence.
- Output: sanitized counts of project-specific direct `roles/run.invoker`, Owner/Editor, public Invoker members, conditional bindings, visible networks/subnets, regional Private Google Access flags; **no principal emails/token/full policies**. This does **NOT** evaluate custom roles, conditional membership, ancestor grants, group memberships, deny policies, shared VPC routing or real reachability. Project-level IAM alone cannot conclusively establish effective `run.invoker` permission.
- No IAM grant, Compute API enable, VPC/subnet/job/VM creation, KMS, Firestore, Firebase, Cloud Run/Registry mutation or production activation.

## Exactly one new Ubuntu root WSL paste (only if proceeding with this scoped read)

```bash
umask 077
d=$(mktemp -d /root/oldx-h2z-readonly-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2z.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/41ea6a02da650fdcc6389fe62b54249f0b7f6e7f/scripts/step05_h2z_project_iam_vpc_readonly_once_20261128.py' &&
test "$(git hash-object "$d/h2z.py")" = '92f01b55d16d89672c0cc95760df6bd0569043b6' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2z.py" &&
python3 -B "$d/h2z.py" --h2z-owner-project-iam-vpc-readonly-once
```

**Expected success string (not claimed):**
`H2Z_RESULT=PROJECT_IAM_AND_VPC_READONLY_PASS_WITH_LIMITS` and `H2Z_CLOUD_WRITES=NONE_POST_GET_IAM_POLICY_IS_A_READ_METHOD`. Otherwise record `H2Z_RESULT=STOP_PARTIAL_OR_BEFORE_READ_ONLY_AUDIT` with its reason; no automatic retry. Keep root-only H2W/H2Z markers and don't paste raw tokens.

## Subsequent decision tree without inventing facts

If H2Z shows complete networks/subnets, **only** use those facts to evaluate whether a suitable, safe internal routing origin already exists. New Cloud Run Job/VM/VPC/network/permission change or an active authenticated internal synthetic probe **requires separate specific approval** and verified identity/data/budget/cleanup constraints. Never expose private Gateway publicly for expediency. Project IAM project-only flags are NOT an ancestor/effective audit; handle any ambiguous broader grants separately. If Compute network inventory is denied/disabled, do not enable API simply to force a result; plan alternative source-only routes.

Do not re-run H2U local build, H2V single registry push, H2W create/direct IAM, H2X/H2Y one-shot readiness GETs, H2T or previous signing/node tests, or old H1B resources. Maintain `STEP05=ACTIVE`, `H2=NO_GO`, `PRODUCTION=NO_GO`.

**Checkpoint:** `H2Z=SOURCE_READY_NOT_OWNER_RUN`; `H2Y_EXISTING_READBACK=CONTROL_PLANE_READY_PASS_WITH_LIMITS`; `H2_HOSTED_HTTP=NOT_TESTED`.
