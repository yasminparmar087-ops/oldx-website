# BAJUTO / OLDX Step05 — Actual H2Z partial IAM PASS + VPC 403, H2AA new independent diagnostic

## Owner actual WSL screenshot 28 Nov 2026 ~00:08 IST — preserve as is

Source originally committed: `scripts/step05_h2z_project_iam_vpc_readonly_once_20261128.py` commit `41ea6a02da650fdcc6389fe62b54249f0b7f6e7f`, Git blob `92f01b55d16d89672c0cc95760df6bd0569043b6`. Owner's screenshot explicitly shows the source downloaded, source Git hash check passed, Python AST parse executed, and the H2Z one-shot run reached **read-only Google APIs**.

Exact extracted result:
```text
H2Z_MARKER=CONSUMED_NO_RETRY
H2Z_REQUEST_PLAN=ONE_PROJECT_GET_IAM_POLICY_READ_POST_AND_TWO_COMPUTE_GETS
H2Z_PROJECT_IAM_POLICY=READ_COMPLETE_VERSION_3
H2Z_PROJECT_DIRECT_RUN_INVOKER_BINDINGS=0
H2Z_PROJECT_DIRECT_OWNER_EDITOR_BINDINGS=2
H2Z_PROJECT_DIRECT_PUBLIC_INVOKER_MEMBERS=0
H2Z_PROJECT_CONDITIONAL_BINDINGS=1
H2Z_PROJECT_IAM_PRINCIPAL_IDENTITIES=NOT_PRINTED
H2Z_RESULT=STOP_PARTIAL_OR_BEFORE_READ_ONLY_AUDIT
H2Z_REASON=HTTP_403
H2Z_EFFECTIVE_IAM_AND_INTERNAL_ROUTING=NOT_VERIFIED
H2Z_CLOUD_WRITES=NONE
H2Z_H2_PRODUCTION=NO_GO
H2Z_DO_NOT_REPEAT_IF_MARKER_EXISTS=TRUE
```

**Precise interpretation:** `projects/oldx-staging:getIamPolicy` (HTTP POST but readonly) returned version 3 and the sanitized project **direct binding** counts above. This was an **actual project-policy read success**, not an IAM effective/ancestor analysis. In particular one conditional binding was seen, but its exact condition/effect is not assessed. No exposed `run.invoker` project-level binding was seen; do NOT assert inherited/service-level grants are absent. The **first** Compute global `networks.list` read returned HTTP403. Since source aborts sequentially on error, the proposed regional `subnetworks.list` was **NOT ATTEMPTED**. Cloud Compute API state, IAM reason, VPC inventory, and private HTTP origin remain unknown. 403 might indicate disabled API, permission denial or another rejected request; the script intentionally did not read/log raw error body, so do not assert exact cause.

**H2Z one-shot marker consumed:** `/root/.oldx-step05-h2z-project-iam-vpc-readonly-once-20261128`. No deletion/reset/retry. Do not repeat earlier H2W service creation/IAM, H2X/H2Y revisions, H2U image build, H2V registry push, H2T/H1B/old cloud probes or saved local source tests. No Cloud writes in this H2Z operation. H2 and production remain NO-GO.

## New H2AA: **NOT YET EXECUTED**, only new read-only source committed

Distinct source: `scripts/step05_h2aa_compute_service_state_permission_hint_once_20261128.py`
- Creation commit `a680630c453b77add54e80496d1c0688b658900d`
- Verified Git blob SHA `a04ec5a2b4572f2cf0c634b41ab168f0a8444c25`
- GitHub static allowlist/marker/method-scope checks PASS; **Owner Python execution and live response NOT YET TESTED**.
- Exact preflight: current root Ubuntu WSL, existing isolated Owner native SDK, owner identity `yasminparmar087@gmail.com` / project `oldx-staging`, owner-root H2Z consumed marker exact UID/project. No new gcloud install/interactive login, and do not modify config.
- Single-use new marker `/root/.oldx-step05-h2aa-compute-state-permission-hint-once-20261128`, created before the **first new Google API**. If STOP, never reset or blindly rerun.
- FIRST **new** read-only request: `GET https://serviceusage.googleapis.com/v1/projects/38472235077/services/compute.googleapis.com?fields=name%2Cstate`. This checks **Compute Engine API ENABLED/DISABLED state**; does not call Compute network list, enable or disable API.
- Only if state is ENABLED, SECOND **new** read-only permission-query POST: `https://cloudresourcemanager.googleapis.com/v1/projects/oldx-staging:testIamPermissions` with exactly `compute.networks.list` and `compute.subnetworks.list`. Despite POST method, `:testIamPermissions` is a no-write permission test, not an IAM policy update; a returned permission is a **project-level hint** only, and does NOT establish effective permission for individual network resources. A missing permission/403 might have multiple explanations.
- At most **two new** metadata calls, <=8192-byte JSON body cap each, no retries, no pagination. Prints API state and sanitized permission names present/absent only, **no identities, raw policy, bearer credentials or error body**. No Compute `networks.list` redo, no `subnetworks.list`, no IAM policy GET repeat, no Cloud resource write, no KMS sign, no Cloud Run/host HTTP.
- If compute service is DISABLED, stop at that state; enabling it is **a new Cloud project write** and would require separate exact approval, not automatic.
- Even if API enabled and project permission hints returned, original 403 reason may remain unexplained, so don't grant broad roles or retry the same consumed endpoint without new evidence.

Official references:
- https://docs.cloud.google.com/service-usage/docs/reference/rest/v1/services/get
- https://docs.cloud.google.com/resource-manager/reference/rest/v1/projects/testIamPermissions
- https://docs.cloud.google.com/run/docs/securing/private-networking

### One exact new root WSL paste (after this source creation)

```bash
umask 077
d=$(mktemp -d /root/oldx-h2aa-once.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2aa.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/a680630c453b77add54e80496d1c0688b658900d/scripts/step05_h2aa_compute_service_state_permission_hint_once_20261128.py' &&
test "$(git hash-object "$d/h2aa.py")" = 'a04ec5a2b4572f2cf0c634b41ab168f0a8444c25' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2aa.py" &&
python3 -B "$d/h2aa.py" --h2aa-compute-state-and-two-permission-hints-readonly-once
```

**Interpret output before next decision:** If `H2AA_COMPUTE_API=DISABLED`, no new VPC GET may be forced; exact user consent needed for Compute API enablement if truly necessary. If `ENABLED`, inspect both project permission hints; do **not** assume they establish effective network access or explain earlier 403. If HTTP403 again, respect one-shot STOP, preserve diagnostic, seek alternative controlled path. `H2AA_RESULT=SERVICE_STATE_AND_OPTIONAL_PROJECT_PERMISSION_HINTS_PASS_WITH_LIMITS` is only a successful new metadata diagnostic, not product enablement. No public Gateway ingress change is allowed.

**Checkpoint:** `H2Z=PROJECT_IAM_PARTIAL_PASS_VPC_403_CONSUMED`; `H2AA=SOURCE_READY_NOT_RUN`; `H2W=PRIVATE_GATEWAY_CREATED_OFF`; `H2Y_EXISTING_CONTROL_PLANE=READY_WITH_LIMITS`; `H2_HOSTED_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
