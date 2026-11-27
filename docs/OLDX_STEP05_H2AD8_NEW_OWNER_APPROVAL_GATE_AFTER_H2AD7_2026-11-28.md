# BAJUTO / OLDX Step05 — H2AD8 exact existing-job resume/run/pause is SOURCE-ONLY; new Owner approval needed

## Actual H2AD7 owner result and frozen state

Read canonical [H2AD7 actual post-Run400 reconciliation](OLDX_STEP05_H2AD7_ACTUAL_FAILED_PRECONDITION_PAUSED_JOB_RECOVERY_DECISION_2026-11-28.md) before H2AD8. 28 Nov 2026 owner screenshot: exact Scheduler job still PAUSED, lastAttemptTime missing, status.code=-1, two target RunJob **Admin Activity** entries reported code 9 = FAILED_PRECONDITION, zero Scheduler execution logs, and **no verified hosted HTTP**. The earlier H2AD6C *attempted* one :run from PAUSED, got HTTP400, local marker consumed. DO NOT rerun H2AD6C or any old one-shot.

The absence of execution logs and missing lastAttemptTime do NOT prove absence of activity in all systems, and code 9 proves a precondition failure but not its precise cause. It is plausible the PAUSED state blocked jobs.run; the old POST also sent JSON `{}` while official `jobs.run` requires an empty body. BOTH possible differences are addressed by the new guarded H2AD8, with no claim which was the real root cause.

## Owner decision — NOT YET GRANTED

Request explicit separate new permission for **exactly** the following temporary cloud changes within existing `oldx-staging` only:
1. On the same existing job `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128`, **one `jobs.resume`** (PAUSED -> ENABLED).
2. **One additional `jobs.run`** with a truly **zero-byte request body**, to the pre-existing authorized OIDC `GET /healthz` of only the exact unchanged internal-only OFF Cloud Run Gateway.
3. Immediately **one `jobs.pause` containment attempt**, even if run returns an error, followed by read-only PAUSED status verification. If pause fails or state cannot be verified PAUSED, stop and report the possibility of an ENABLED temporary Scheduler job for prompt independent manual recovery. No repeated run or pause in the script.

No new job/SA, no broad or additional IAM grants, no API enable, no Compute/VPC, Cloud Run ingress/deploy, KMS/Firestore/Product writes or production activation. The old Owner permission for the prior RunJob attempt was consumed by H2AD6C; this is a new state-changing sequence. It may incur Scheduler/Cloud Run usage cost; the far-future February 29 schedule protects against imminent cron execution but is NOT an indefinite safety guarantee. One manually requested dispatch can still deliver more than once under Scheduler semantics.

If Owner does NOT approve H2AD8: do not run the source; plan exact paused job + temporary Invoker/SA cleanup only, respecting UID/etag, after confirming no in-flight attempts. Preserve the failed health gate honestly as NOT TESTED/NOT VERIFIED.

## NEW frozen source on GitHub, only static checked, NO cloud execution

- Source path `scripts/step05_h2ad8_owner_approved_one_resume_run_pause_once_20261128.py`.
- Creation commit `1f8d0a1dc66bc9da05475537f0094627af2aa64e`.
- GitHub verified source blob SHA-1 `2fe7abcad66c394bc80779005944d6f0a377a349`.
- Static guards readback pass: one resume POST, one zero-byte-body jobs.run POST, one containment pause POST, no IAM/job creation/deletion or Product/KMS writes. A new one-shot owner-local marker precedes the first new cloud write.
- Marker if **subsequently approved and run:** `/root/.oldx-step05-h2ad8-one-resume-run-pause-once-20261128`. Never clear/reuse after any attempt.
- Prereqs: root Ubuntu WSL isolated native gcloud Owner config; consumed H2AD5/H2AD6C/H2AD7 markers exact project/job and frozen Gateway UID `2d87153f-155e-409f-a418-463c785d8467`, probe SA UID `110217058111344002447`, default `run.app` base. Fresh GET job requires exact PAUSED/OIDC GET healthz/far-future cron/retry0/30sec and no prior `lastAttemptTime`. One-shot marker before resume.
- After resume must observe the **same** job ENABLED and no new `lastAttemptTime`, before sending exactly one RunJob POST. Regardless of run outcome, finally containment checks exact job and attempts pause **at most once**, with a final readback. If unknown or enabled state remains: H2AD8 STOP, do not retry a call blindly, prepare targeted containment.
- If run API returns HTTP200 and pause readback PAUSED, `H2AD8_RESULT=ONE_MANUAL_RUN_ACCEPTED_AND_JOB_REPAUSED_WITH_LIMITS` means **only** Scheduler accepted the request and the job was re-paused. HTTP 200/JSON mode OFF at the Cloud Run target still requires independent *new* Scheduler delivery/Cloud Run request evidence. No cleanup until in-flight delivery is reconciled.
- This file is **source ready pending approval**. Local Python AST and live runtime have NOT been verified by Owner; do NOT claim H2AD8 PASS or job changes.

## After approval, the frozen source can be invoked in ONE root Ubuntu WSL command

Do not offer this command to owner until explicit consent to the above temporary resume/run/pause cloud mutations. When approved, use the immutable commit path and Git blob hash check, AST guard and exact consent flag `--h2ad8-new-owner-approved-one-resume-run-pause-once`. Do not give an unpinned mutable branch script.

## Canonical exit constraints

`H2AD7=ACTUAL_READ_PASS_CODE9_AND_ZERO_EXECUTION_LOGS`;`
H2AD8=SOURCE_READY_AWAITING_NEW_OWNER_APPROVAL`;`
SCHEDULER_JOB=PAUSED_LAST_READ`;`
PRIVATE_GATEWAY=INTERNAL_ONLY_OFF`;`
H2_HOSTED_HTTP=NOT_VERIFIED`;`
STEP05=ACTIVE`;`
H2/PRODUCTION=NO_GO`.
