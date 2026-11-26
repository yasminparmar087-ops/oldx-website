# OLDX Step05 H1B — W0 actual PASS, one NEW no-key W1 SA creation source, 26 November 2026

Repo: `yasminparmar087-ops/oldx-website`, branch: `security-hardening-review`. This checkpoint supersedes the old W0 source-ready state, not the original evidence or old security gates.

## 1. Owner actual W0 screenshot (do NOT repeat)

W0 actual real owner WSL terminal:
```text
H1B_W0_PROJECT=ACTIVE_EXACT
H1B_W0_SERVICE=ABSENT_404_WITH_LIMITS
H1B_W0_NEW_SA=ABSENT_404_WITH_LIMITS
H1B_W0_IMAGE=PRIOR_G2B_REMOTE_DIGEST_FROZEN_NO_REPEAT
H1B_W0_NEW_SA_ACTAS=NOT_YET_TESTABLE
H1B_W0_RESULT=READ_ONLY_NEW_TARGETS_ABSENT_WITH_LIMITS
H1B_W0_REASON=PROJECT_AND_TWO_NEW_EXACT_RESOURCES_CHECKED
H1B_W0_CLOUD_RESOURCE_WRITES=NONE
H1B_W0_DO_NOT_REPEAT=TRUE
```
Hence project `oldx-staging` exact and two future new target names absent HTTP404 **at W0's read time only**. New target IAM permissions/actAs and any cleanup after creation remain distinct. W0 one-shot marker `/root/.oldx-h1b-w0-new-target-readonly-once-20261126` CONSUMED. See [W0 actual verified evidence](OLDX_STEP05_H1B_W0_ACTUAL_PASS_NEW_TARGETS_404_2026-11-26.md).

Frozen earlier G2B ONE Registry push actual PASS, immutable `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`. NEVER rebuild, scan or push again. Old C1A service already removed; its separate SA/image remain retained, references unknown.

## 2. Owner consent

Owner explicitly answered `ha manjuri chhe` to **one finite supervised staging-only private compiled-OFF/no-user-data W1–W6 session**. Approval permits one NEW runtime SA, one new H1B private Cloud Run service using frozen image digest, optional exact Yasmin-only Invoker, <=4 H1B-only probes and same-session guarded NEW-only cleanup. Max 24 hours from actual activation, preferably much shorter; known 12 HIGH CVEs accepted for this private/OFF experiment only. No Firebase Rules/data, H2/production, project-wide/public Invoker, other service, or old C1A asset modification. W2 image upload is already complete. All old source/security/CI/cloud one-shot probes remain consumed.

## 3. W1 script: SOURCE READY, not run by assistant or owner yet

New `scripts/step05_h1b_w1_no_key_sa_create_once_20261126.py`:
- Pinned immutable source commit after bounded network-error guard fix: `3d8c1b54d10fd8b6f09c7ce3ff4d82aa259b9884`
- Exact verified GitHub blob `19ff960ff00666565d944c7f62354bb4c6cf64c9`
- Distinct one-shot marker `/root/.oldx-h1b-w1-new-no-key-sa-create-once-20261126`; used once only, including failure after first attempted create.
- Runs only as root in existing `OLDX-Ubuntu-24.04` with previously isolated Owner `yasminparmar087@gmail.com` credentials + project `oldx-staging`. Requires frozen G2B and successful W0 consumed markers; no re-run of W0 or broad tests.
- Before the actual SA creation: re-check only the exact NEW service and SA `404` (fresh collision guard), and one targeted **read-only** project `testIamPermissions` covering immediate new create/delete and Cloud Run create/delete/get rights. No public/browser IAM search, no historic G1 replay; if anything unknown, STOP with `SA_CREATE_ATTEMPTED=FALSE`.
- After passing preflight, one **actual IAM API POST write** creates ONLY `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` as a NEW user-managed runtime service account with description/display name, **no user-managed key requests and no IAM grant**. It is not an image build, container deployment, or staging traffic activation. Records returned stable numeric `uniqueId`, reads it back, tests resource-level `iam.serviceAccounts.actAs` and `iam.serviceAccounts.delete` (read-only `testIamPermissions` API despite HTTP POST). Success is `NEW_NO_KEY_SA_CREATED_RIGHTS_PASS_WITH_LIMITS` only, **not Cloud Run deployment GO**.
- Any ambiguous API timeout/partial result after create uses `STOP_AFTER_MARKER`: **NEVER rerun W1 or reset marker**. The new SA may have been created even on an error. Separate UID/readback and guarded cleanup must be planned before another write. A successful W1 resource creates no service and does not consume CPU; a new account itself is not public Product access.
- Private evidence `/root/oldx-h1b-w1-sa-<UTC>/created-sa-sanitized.json`, no OAuth tokens/API keys in GitHub. Assistant has NOT performed Cloud IAM write or verified new SA actually exists.

### One paste in existing Ubuntu WSL root terminal

```bash
umask 077
d=$(mktemp -d /root/oldx-h1b-w1-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/w1.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/3d8c1b54d10fd8b6f09c7ce3ff4d82aa259b9884/scripts/step05_h1b_w1_no_key_sa_create_once_20261126.py' &&
test "$(git hash-object "$d/w1.py")" = '19ff960ff00666565d944c7f62354bb4c6cf64c9' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/w1.py" &&
python3 -B "$d/w1.py" --w1-single-new-no-key-sa-once
```

Success output (actual number unknown until Google creates the SA):
```text
H1B_W1_STAGE=ONE_APPROVED_NEW_SA_CREATE_ATTEMPT
H1B_W1_SA_UID=<numeric UID>
H1B_W1_SA_CREATE_ATTEMPTED=TRUE
H1B_W1_RESULT=NEW_NO_KEY_SA_CREATED_RIGHTS_PASS_WITH_LIMITS
H1B_W1_REASON=SA_UID_READBACK_AND_ACTAS_DELETE_PASS
H1B_W1_CLOUD_RUN_DEPLOY=NOT_ATTEMPTED
H1B_W1_IAM_BINDINGS_AND_KEYS=NONE_CREATED_BY_THIS_SCRIPT
H1B_W1_DO_NOT_REPEAT=TRUE
```
If `STOP_BEFORE_SA_CREATE`, no new SA created by script; if `STOP_AFTER_MARKER`, creation MAY have occurred and same-session guarded recovery is required, **not a second create**. Share only sanitized `H1B_W1_*` lines (numeric UID is not a secret); never show or share tokens or private evidence. Stop if anything differs.

## 4. Rollback / next gate — constrained and not falsely claimed complete

W1 only creates the new no-user-key SA; no Cloud Run service/traffic is started at this stage. Thus W1 cannot itself verify new Cloud Run service security or perform hosted probes. **Before any W3 deployment**, use the exact W1 UID + G2B immutable image and create a guarded W3–W6 execution/rollback packet: verify exact new SA resource actAs/delete, service 404 immediately before creation, effective project/run cleanup authority, compiled OFF container settings/no public Invoker, then one new private OFF Cloud Run deployment and same-session new-only cleanup if evidence matches. If W1 fails or W3 is declined, keep the new SA unused pending UID-and-dependency-guarded deletion; do not delete any old resource or assume automatic cleanup.

Cloud IAM/API sources used: https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/create ; https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/testIamPermissions ; https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/create ; https://docs.cloud.google.com/run/docs/managing/services .

**Status:** `W0=ACTUAL_PASS_CONSUMED`; `W1=SOURCE_READY_NOT_EXECUTED`; `W2_G2B=ACTUAL_PASS_CONSUMED`; `W3-W6=NOT_EXECUTED`; `H2/PRODUCTION=NO_GO`.
