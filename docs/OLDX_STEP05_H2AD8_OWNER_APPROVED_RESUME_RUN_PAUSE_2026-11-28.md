# BAJUTO / OLDX Step05 H2AD8 — explicit Owner approval; guarded one resume/run/pause not yet executed

## Scope and approval

On **28 November 2026**, following the Owner's screenshot of the **actual** H2AD7 read-only reconciliation and the explicit H2AD8 question, Owner replied **"ha manjuri chhe"**. This is **one separate explicit authorization** to perform the exact **H2AD8** three-action sequence on the single existing `oldx-staging` Scheduler job `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128`:

1. Exactly **one** `jobs.resume` of this PAUSED job (temporary ENABLED window).
2. Exactly **one new** `jobs.run` with an **empty, zero-byte POST body** for the existing read-only OIDC `GET /healthz` target.
3. A guarded **single containment `jobs.pause` attempt** if required, even if the run stage fails, with final read-only job PAUSED verification.

**Important caveat:** safety is not guaranteed if Google returns an ambiguous result or pause fails. In that case STOP, never rerun any of these operations automatically, and prioritize safe containment of the existing job through a new exact-state review. Cron remains the far-future `0 0 29 2 *` UTC, not an immediate schedule. The single API run acceptance does not prove actual HTTP 200 or one delivered HTTP request; separate H2AD9 logs needed. No deployment/ingress/SA/IAM/Product/KMS/Firestore/Compute/VPC/prod changes and no additional job or identity may be created in H2AD8. Scheduler/Cloud Run usage could incur cost.

The prior attempted run `H2AD6C` returned HTTP400, one-shot marker consumed. `H2AD7` Owner actual read-only response: job `PAUSED`, no `lastAttemptTime`, status `-1`, two exact RunJob audit records with google.rpc `code=9 FAILED_PRECONDITION`, zero exact Scheduler execution log entries. This does **not** prove the cause of 400; the temporary resume is a new limited recovery attempt, not an old command rerun. All old one-shot H2AD0–H2AD7, image builds, pushes, deployments, IAM corrections and source tests remain frozen/do-not-repeat.

## Immutable source reverified *after* explicit approval

- GitHub source path `scripts/step05_h2ad8_owner_approved_one_resume_run_pause_once_20261128.py`
- Frozen creation commit `1f8d0a1dc66bc9da05475537f0094627af2aa64e`
- Git blob SHA1 `2fe7abcad66c394bc80779005944d6f0a377a349` reverified using GitHub fetch after Owner approval.
- Static scope inspection PASS: one resume POST, one jobs.run POST, one pause POST max, POST body `b""`, one unique marker `/root/.oldx-step05-h2ad8-one-resume-run-pause-once-20261128` before any remote mutation, exact Owner Ubuntu root WSL isolated SDK/project/SA/Gateway/job/prior markers, far-future cron, OFF healthz/OIDC guard. A `finally` containment path attempts pause after resume attempt (up to once). No other cloud write method. **The script was NOT executed in Google Cloud from this documentation work.** GitHub static inspection is not an Owner Python runtime or live deployment test.

## One approved root Ubuntu WSL command (run only once)

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad8-once.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad8.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/1f8d0a1dc66bc9da05475537f0094627af2aa64e/scripts/step05_h2ad8_owner_approved_one_resume_run_pause_once_20261128.py' &&
test "$(git hash-object "$d/h2ad8.py")" = '2fe7abcad66c394bc80779005944d6f0a377a349' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad8.py" &&
python3 -B "$d/h2ad8.py" --h2ad8-new-owner-approved-one-resume-run-pause-once
```

### How to interpret Owner's eventual actual result

- `H2AD8_RESULT=ONE_MANUAL_RUN_ACCEPTED_AND_JOB_REPAUSED_WITH_LIMITS`: single scheduler API run accepted and final paused readback PASS; **NOT proof that Gateway returned 200**. Proceed to one NEW read-only H2AD9 delivery+Cloud Run HTTP logs, then exact cleanup.
- `H2AD8_RESULT=STOP_SAFE_PAUSED_MANUAL_RUN_NOT_PROVEN`: final job state PAUSED but attempted resume/run failed or was ambiguous; do not rerun or assume delivery failure.
- `H2AD8_RESULT=STOP_JOB_MAY_REMAIN_ENABLED_NEEDS_EXACT_RECOVERY` or any result with `H2AD8_FINAL_JOB_PAUSED_VERIFIED=FALSE`: **urgent** same-job state reconciliation and containment, **no second jobs.run**.
- If no marker printed, command may have stopped before attempting a new state-changing action. Still inspect error before any new action. If marker consumed, never delete/reset marker or invoke H2AD8 again.

**Checkpoint:** `H2AD7=ACTUAL_CODE9_NO_EXECUTION_CONSUMED`; `H2AD8=EXPLICIT_OWNER_APPROVED_SOURCE_READY_NOT_RUN`; `STEP05=ACTIVE`; `H2_HTTP=NOT_VERIFIED`; `H2/PRODUCTION=NO_GO`.
