# BAJUTO / OLDX Step05 H2W — first STOP before Cloud writes, exact 20-hex H2V tag correction

## 27 Nov 2026 ~23:13 IST: actual Owner WSL screenshot

~~~text
H2W_RESULT=STOP_BEFORE_CLOUD_WRITES
H2W_REASON=H2V_EXACT_REMOTE_IMAGE_RECEIPT_NOT_PASS
H2W_CREATE_ATTEMPTED=FALSE
H2W_IAM_WRITE_ATTEMPTED=FALSE
H2W_H2_PRODUCTION=NO_GO
~~~

**Root cause confirmed by visual screenshot and source code:** H2V earlier Registry push actually PASSED with 20-character random tag `h2v-off-20261127-793639b6b8d15e55ea4a`. Original H2W script erroneously transcribed **19 hex** `h2v-off-20261127-793639b68d15e55ea4a` (missing one `b`) into its `marker_lines(H2V)` predecessor check. This fails even with an intact successful H2V marker. It is a **source literal typo**, not H2V image verification/Registry failure. Do not rerun H2V upload or rebuild Docker.

The **original H2W script stopped before one-shot marker creation and before ANY Cloud Run create or IAM write**. It performed only local preflight; `H2W_CREATE_ATTEMPTED=FALSE` and `IAM_WRITE_ATTEMPTED=FALSE`. The pre-existing Owner approval for one private staging new service + one service-only Owner Invoker binding remains **unused**.

## New correction — source only, no Cloud write performed by assistant

- **Corrected script:** `scripts/step05_h2w_one_new_internal_off_gateway_cloudrun_receipt_tag_fix_once_20261127.py`
- **Immutable creation commit:** `e55857f4600f2a152a93fdc3ac1bec201bed7cad`.
- **Readback verified Git blob hash:** `a6986708b2fe0ac67aa214b544ca977244cf131d`.
- Byte-for-byte **identical to original H2W** except the one H2V predecessor-tag literal corrected to the screenshot's exact 20-hex tag (GitHub fetch and string comparison PASS). No permissions, target service, SA, image, ingress, IAM, marker or operation changed.
- Original H2W script remains immutable in GitHub, but must **NOT** be rerun. New script uses same unused marker `/root/.oldx-step05-h2w-new-internal-off-cloudrun-service-once-20261127` and same Owner's existing scope. No pre-existing marker should be cleared.
- Frozen immutable H2U remote index: `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`, verified child `sha256:c165e671e2b231b5b6210f867dacc085d4a53b69fae2998a712019d9b6575243`, config `sha256:56b7a9601702e80286c80089e33fe13049b6fa7d3fbbcb98e4f775c9d31ace25`.
- Still requires live new H2W preflight: Owner account/project, matching enabled SA `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` UID `107238619872767759560`, rights, exact new target service `oldx-c2-h2-private-gateway` GET 404. Only if all pass, at most one new Cloud Run service by frozen image; `INGRESS_TRAFFIC_INTERNAL_ONLY`, IAM enforced, min0 max1, CPU1/512Mi, OFF env, exact service-only Owner Invoker binding, UID/config/etag readback. No external WSL HTTP probe because internal ingress; inherited IAM still independent. No KMS/Firestore, registry push, local image rebuild, production or unrelated service writes.

## One corrected root Ubuntu WSL command (do NOT run old H2W again)

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2w-tagfix-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/deploy.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/e55857f4600f2a152a93fdc3ac1bec201bed7cad/scripts/step05_h2w_one_new_internal_off_gateway_cloudrun_receipt_tag_fix_once_20261127.py' &&
test "$(git hash-object "$d/deploy.py")" = 'a6986708b2fe0ac67aa214b544ca977244cf131d' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/deploy.py" &&
python3 -B "$d/deploy.py" --h2w-owner-approved-one-internal-off-gateway-service-create-once
~~~

Expected success (only if actually executed on Owner machine, no PASS claimed now):
~~~text
H2W_CREATE_ATTEMPTED=TRUE
H2W_IAM_WRITE_ATTEMPTED=TRUE
H2W_OWNER_INVOKER=EXACT_OWNER_ONLY_DIRECT_BINDING_VERIFIED
H2W_INGRESS=INTERNAL_ONLY
H2W_RESULT=PASS_NEW_INTERNAL_OFF_SERVICE_AND_OWNER_DIRECT_INVOKER_WITH_LIMITS
H2W_H2_PRODUCTION=NO_GO
~~~

If `STOP_BEFORE_CLOUD_WRITES`, no cloud write; provide screenshot. **If marker exists or CREATE_ATTEMPTED=TRUE, never rerun.** Cloud Run could have been created partially even on STOP; must reconcile safely without blind retry or delete. No existing H2V/H2U/H1B tests, uploads, scans or consumed marker resets.

**Checkpoint:** `H2V_REGISTRY_PUSH=ACTUAL_PASS_CONSUMED`; `H2W_PREVIOUS_ATTEMPT=STOP_BEFORE_CLOUD_WRITES_TAG_TYPO`; `H2W_FIX=SOURCE_READY_NOT_RUN`; `H2W_ONESHOT_CREATE_APPROVAL=UNUSED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
