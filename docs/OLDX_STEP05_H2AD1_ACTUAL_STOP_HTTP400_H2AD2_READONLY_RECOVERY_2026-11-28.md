# BAJUTO / OLDX Step05 H2AD1 — Owner ACTUAL partial WRITE STOP HTTP400; H2AD2 exact read-only reconciliation next

## Owner screenshot 28 Nov 2026 ~00:27 IST (root Ubuntu WSL)

Owner executed the **previously approved** immutable `scripts/step05_h2ad1_create_scoped_probe_sa_invoker_once_20261128.py`, commit `d51a3641cbaad0ae17085fb526d59f2b31f4bf57`, Git blob `ca99db3d52e4a44e2e3097a94094f94a98771906` after source hash/AST check. Original **actual** output:

```text
H2AD1_MARKER=CONSUMED_NO_REPEAT
H2AD1_STAGE=ONE_NEW_TEMP_PROBE_SA_CREATE
H2AD1_STAGE=ONE_SERVICE_ONLY_PROBE_INVOKER_ADDITION
H2AD1_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_PARTIAL_WRITE
H2AD1_REASON=INVOKER_SET_HTTP_OR_RESPONSE_MISMATCH_400
H2AD1_ACTION=DO_NOT_RERUN_OR_AUTOCLEANUP_ON_AMBIGUOUS_WRITE
H2AD1_H2_PRODUCTION=NO_GO
```

**DO NOT claim H2AD1 PASS.** Exact source execution sequence establishes that `iam.googleapis.com/v1/projects/oldx-staging/serviceAccounts` SA create returned HTTP200 with a new immutable numeric uniqueId and matching email, and that **subsequent exact new-SA GET validated the same UID, enabled state** before advancing to the IAM stage. The source recorded that UID in root-only H2AD1 marker; the screenshot did not print the UID. Thus **new temporary probe SA definitely exists at that readback**, but its current status must be reconciled. The source then successfully got a direct Owner-only IAM policy with ETag, and sent exactly ONE `POST https://run.googleapis.com/v2/projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway:setIamPolicy` with Owner+new probe-SA `roles/run.invoker`; Google replied **HTTP 400**. The original script discarded the response body, so the exact 400 reason is **UNKNOWN**. It might involve request validation, newly created principal propagation, constraints or another issue, but none is proven. Do not blindly edit IAM/version/etag or automatically add roles. Do not assume IAM unchanged without an actual post-write readback. Cloud Run v2 setIamPolicy is an actual cloud **write attempt**, not just a source-only operation.

No Scheduler Job create/run attempted by H2AD1; no Gateway application HTTP; Product and H2 remain OFF. No statement about a successful HTTP healthz test, buyer/seller functionality or production readiness is justified.

### One-shot rules, exact references

- H2AD1 one-shot marker `/root/.oldx-step05-h2ad1-probe-sa-and-exact-invoker-once-20261128` consumed and preserves exact new SA UID and `GATEWAY_INVOKER_SET_ABOUT_TO_BE_SENT=TRUE`. **NEVER rerun H2AD1 or reset/delete that marker.**
- H2AD0 (URI+name collision read-only), H2AC Scheduler API enable, H2AB/H2AA/H2Z, H2X/H2Y, H2W service create/Owner Invoker, H2U image build, H2V image push, earlier H2S/H1B and old tests likewise NEVER rerun.
- Do not create another probe SA, Job, bind project-wide Invoker, switch ingress to `ALL`, delete resources or retry failed IAM write before unique postwrite state and error diagnosis. Owner previously approved H2AD's bounded temporary workflow, but **the earlier IAM write attempt is consumed**; new write recovery scope should be checked separately after evidence.

Google authoritative:
- https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/setIamPolicy
- https://docs.cloud.google.com/run/docs/reference/rest/Shared.Types/Policy (etag/version)
- https://docs.cloud.google.com/iam/docs/access-change-propagation (general eventual consistency; **not proof of this HTTP400 reason**).

## New H2AD2: SOURCE ONLY, not executed yet

`scripts/step05_h2ad2_after_400_sa_iam_reconciliation_readonly_once_20261128.py`
- Immutable creation commit `3d91910dbb909eb99513f83bcd92a1047d18dd0f`
- Git blob SHA-1 `920f73f5cd022f1d30a4897452fdd7623a8a0a96`, fetched back and static scoped.
- Precondition exactly the consumed Owner root H2AD1 marker with verified numeric SA UID, exact project/service UID/probe-SA email and attempted IAM write. Isolated native WSL Owner SDK as before, no new installer/logins/config changes.
- Distinct H2AD2 one-shot marker `/root/.oldx-step05-h2ad2-after-400-reconcile-readonly-once-20261128` created **before first Google request**.
- Only **three new, purpose-scoped GETs**: (1) Cloud Run same service UID/ingress/OFF image post-write, (2) exact previously created new probe SA matching H2AD1 numeric UID and enabled, (3) exact service-level `:getIamPolicy` (no project IAM inventory, no SA policy read, no IAM write).
- Interpret direct service policy as:
  - `OWNER_ONLY_PROBE_NOT_GRANTED`: earlier role addition did not appear in latest direct policy, **but HTTP400's underlying reason remains unknown**.
  - `OWNER_AND_EXACT_PROBE_GRANTED`: role exists despite H2AD1's original HTTP400 (evidence of current direct state, still not effective IAM).
  - `OTHER_POLICY_NO_NEW_WRITE`: something unexpected; STOP before any write and inspect separately.
- No Scheduler job, no `jobs.run`, no Compute VPC, no IAM grant, no KMS/Auth/Firestore/Registry or Cloud Run create/update. Does not expose bearer token, full IAM policy/etag or private SDK to console/GitHub. Current state can change after readback; no stronger claims.
- Static GitHub scope guards passed; **no Owner execution or actual Google readback claimed yet**.

### Exactly one NEW owner Ubuntu WSL root paste (distinct recovery, no prior one-shot rerun)

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad2-reconcile.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad2.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/3d91910dbb909eb99513f83bcd92a1047d18dd0f/scripts/step05_h2ad2_after_400_sa_iam_reconciliation_readonly_once_20261128.py' &&
test "$(git hash-object "$d/h2ad2.py")" = '920f73f5cd022f1d30a4897452fdd7623a8a0a96' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad2.py" &&
python3 -B "$d/h2ad2.py" --h2ad2-after-h2ad1-http400-readonly-reconcile-once
```

On `H2AD2_RESULT=POST_HTTP400_READONLY_RECONCILIATION_PASS_WITH_LIMITS` interpret `H2AD2_DIRECT_GATEWAY_IAM` without assuming H2AD1 PASS. On STOP, retain marker, **do not rerun/retry writes or auto-delete SA**. If result is owner-only, next choose a single **separately approved** narrowly scoped correction based on the underlying HTTP400 reason; do not create a second probe SA. If owner+probe then no grant repetition; next Scheduler one-job phase requires fresh appropriate guards. The single Owner approval to H2AD doesn't authorize broader role escalation on failure.

**Checkpoint:** `H2AD1=ACTUAL_PARTIAL_SA_CREATED_IAM_WRITE_HTTP400_STOP`; `H2AD2=READONLY_SOURCE_PREPARED_UNRUN`; `H2AD_JOB=NOT_CREATED`; `H2_HOSTED_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
