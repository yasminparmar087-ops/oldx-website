# BAJUTO / OLDX Step05 — H2AE actual preflight STOP; H2AF new corrected guarded temporary cleanup

## Owner actual screenshot ~01:07 IST, 28 Nov 2026

Owner ran pinned H2AE `scripts/step05_h2ae_exact_temporary_scheduler_probe_cleanup_once_20261128.py` from creation commit `ac502f38998834dab7e538ac23d71a5e820d6b24`, verified Git blob `70ada14844cd999a5c0a0f729bfaa8d5a6aa7e8a`, with Python AST check. Actual result:

```text
H2AE_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_PARTIAL_CLEANUP
H2AE_REASON=PROBE_SA_UID_OR_DISABLED_STATE_DRIFT
H2AE_ACTION=DO_NOT_RERUN_RECONCILE_EXACT_STAGE_AND_UID
H2AE_H2_PRODUCTION=NO_GO
```

No `H2AE_MARKER=CONSUMED_NO_REPEAT` and no `H2AE_STAGE=...` output. Source inspection shows the failure occurred in **read-only preflight** (exact Probe SA `get` returned HTTP200 but `check_sa(sa,False)` failed), **before H2AE one-shot marker and before any job deletion/IAM grant modification/SA disabling/deletion**. Do not rerun H2AE or clear any older markers.

**Likely programming bug, not proven live IAM drift:** original `check_sa` used `sa.get("disabled") is False`. Google IAM ServiceAccount `disabled` is an output-only boolean, and Protobuf JSON may OMIT scalar fields with default `false`. `dict.get` would then return `None`, falsely causing `PROBE_SA_UID_OR_DISABLED_STATE_DRIFT` even if the email/UID matched and the account is enabled. This inference needs an actual fresh read to confirm: the earlier guard also checks email and UID in the same condition, so a true UID drift is still possible. Do NOT assert the cloud SA's exact current state before H2AF's fresh check.

Official references:
- https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts — `disabled` output-only bool and `uniqueId` stable numeric identity
- https://protobuf.dev/programming-guides/json/ — implicit default scalar fields may be omitted from JSON
- https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/disable — numeric UID is supported, request body must be empty

## H2AF new one-shot corrected preflight cleanup (SOURCE ONLY, NOT executed yet)

- New script `scripts/step05_h2af_exact_temp_cleanup_default_false_sa_guard_once_20261128.py`.
- Frozen commit `9a40a36ab0815758de4e3c051720f8582d6b1191`; GitHub verified new script Git blob `3f82e4c9bbbaad08aa9970657fba11784a80097b`.
- Source derived from inspected H2AE with only a distinct H2AF one-shot marker/labels; **requires previous H2AE marker ABSENT**, else STOP before any write because previous cleanup outcome would be ambiguous.
- Corrected `check_sa`: **FIRST** strict email `oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com` and immutable numeric UID `110217058111344002447` both match. **THEN** require `disabled` bool; absent treated as `False` on pre-disable read. After disabling, require positive explicit `True`; unexpected/null/wrong value STOP. Sanitized `H2AF_SA_DISABLED_FIELD_PRESENT` printed only after exact UID verified before any write.
- IAM `serviceAccounts.disable` sends empty zero-byte POST request body per Google REST documentation, not JSON `{}`.
- Before any mutation: check previous exact H2AD5/H2AD8/H2AD9 root markers, same PAUSED job with one completed attempt, same OFF/internal Gateway immutable UID and image, direct Owner+probe Invoker with ETag, exact SA UID/enabled, and one distinct complete Scheduler execution log read with exactly one AttemptStarted and one AttemptFinished status NOT_FOUND. If any precondition fails, **no cloud write**.
- If all preflight PASS, create root `/root/.oldx-step05-h2af-exact-temp-probe-cleanup-once-20261128` marker BEFORE cloud mutation. EXACT bounded stages: (1) one DELETE of exact paused synthetic Scheduler job and readback 404; (2) one target-service-specific IAM ETag update removing ONLY probe SA and retaining Owner `roles/run.invoker`, verified Owner-only; (3) one exact NUMERIC UID SA disable and fresh UID/disabled=True readback; (4) one numeric UID SA delete and 404 readback. All stage intents appended to root marker. No new HTTP dispatch, run/resume, SA creation, other IAM, Firebase, KMS, Product, Gateway ingress/image change or production enablement.
- On any ambiguous stage/STOP, DO NOT RERUN H2AF or old H2AE, preserve markers, inspect exact cloud state with a new narrowly scoped reconciliation. Cleanup is within the earlier Owner's explicitly approved temporary H2AD cleanup scope. Permanent Gateway service remains OFF. A completed cleanup does **not** convert the prior Scheduler NOT_FOUND HTTP health failure into a PASS.
- Google recommends disabling a service account before deletion and (especially for long-lived accounts) observing for a period. This account is an isolated short-lived synthetic probe and approved for exact cleanup; no inference is made about unrelated SA dependencies.

## One new Owner root Ubuntu WSL command (H2AF only, DO NOT RUN TWICE)

```bash
umask 077
d=$(mktemp -d /root/oldx-h2af-cleanup.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2af.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/9a40a36ab0815758de4e3c051720f8582d6b1191/scripts/step05_h2af_exact_temp_cleanup_default_false_sa_guard_once_20261128.py' &&
test "$(git hash-object "$d/h2af.py")" = '3f82e4c9bbbaad08aa9970657fba11784a80097b' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2af.py" &&
python3 -B "$d/h2af.py" --h2af-owner-approved-exact-temporary-probe-cleanup-once
```

**Only actual success output can prove cleanup**:
```text
H2AF_JOB=DELETED_404_VERIFIED
H2AF_GATEWAY_INVOKER=OWNER_ONLY_VERIFIED
H2AF_PROBE_SA=DISABLED_UID_VERIFIED
H2AF_PROBE_SA=DELETED_404_VERIFIED
H2AF_RESULT=EXACT_TEMP_JOB_PROBE_INVOKER_SA_CLEANUP_PASS
```

H2AF cloud execution **NOT done** at this commit. Most recent actual safe state is **H2AE preflight STOP, no H2AE marker/write**; H2AD9's last documented job state PAUSED; precise current SA disabled false field unknown. H2/production NO-GO. Step05 real G2–G6 hosted KMS, Firebase/Firestore, media, Seller–Buyer acceptance still remain; avoid repeating historical hardening checks.
