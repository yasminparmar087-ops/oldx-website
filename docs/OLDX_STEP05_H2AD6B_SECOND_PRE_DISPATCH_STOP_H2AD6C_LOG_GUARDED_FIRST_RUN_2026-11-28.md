# BAJUTO / OLDX Step05 — H2AD6B second pre-dispatch STOP; H2AD6C one first run only if new independent guards pass

## Owner screenshot: 28 Nov 2026 ~00:47 IST — ACTUAL H2AD6B STOP

Owner downloaded pinned `scripts/step05_h2ad6b_status_aware_one_manual_paused_health_dispatch_once_20261128.py` source commit `1f50c4d3c94142341f3633c9c743b7a70ccd61e2`, Git blob `e44cc4721502ca0681b4103013461db30e9a49c6`, validated SHA and Python AST, executed once in root WSL. Actual:

```text
H2AD6B_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_ONE_RUN
H2AD6B_REASON=NONZERO_OR_UNEXPECTED_PREVIOUS_STATUS_CODE_ABORT
H2AD6B_ACTION=DO_NOT_REPEAT_OR_RESUME_OR_AUTOCLEANUP
H2AD6B_H2_PRODUCTION=NO_GO
```

**Source-based causal inference (strict):** H2AD6B preflight validated the paused exact job name/schedule/OIDC target and `lastAttemptTime` absence, then rejected nonzero/unexpected `job.status.code` within `benign_unattempted_status()`. The one-shot H2AD6B marker creation and single `POST jobs.run` occur only **after** this function returns. Neither appeared in stdout; **H2AD6B did not send a dispatch**. The earlier original H2AD6 likewise stopped at `PREEXISTING_STATUS_ABORT_NO_MORE_DISPATCH` before marker. Thus *neither assistant-supplied manual-run script sent `jobs.run`*, but that is not a whole-project audit or proof no third-party attempts occurred. Exact nonzero code `-1` vs `1`/other was NOT printed in the owner's screenshot and **is UNKNOWN**.

Do not rerun H2AD6/H2AD6B, H2AD5 job create/pause, H2AD4 IAM correction, H2AD3 logs, H2AD2 postwrite read, H2AD1 SA create, H2AD0 target read or any earlier H2W/H2Y/H2U/H2V/OCI probes, tests or builds. Preserve all consumed root-only markers; do not resume manually or add another Scheduler job. Last independently verified job state was `PAUSED`, internal Gateway OFF, direct Owner+probe Invoker existing. `STEP05=ACTIVE`; `H2_HOSTED_HTTP=NOT_TESTED`; `PRODUCTION=NO_GO`.

## Verification of possible PAUSED / status.code=-1 behavior and what it does NOT prove

- Google official [Cloud Scheduler Job REST](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs) describes `status` as the last execution status and `lastAttemptTime` as the last attempt start. Mere presence of a `status` object is not evidence an HTTP dispatch happened.
- A [Google Developer forum thread dated Oct 2026](https://discuss.google.dev/t/cloud-scheduler-reports-status-code-1-despite-http-200-attempts/406371) records another PAUSED job with `status.code=-1` and **no lastAttemptTime**, despite successful attempts in that OTHER project. The participants explicitly note absence of a definitive published guarantee. **This is background only; it is NOT evidence the BAJUTO job has code -1 or that code -1 is always harmless.**
- Google official [View logs](https://docs.cloud.google.com/scheduler/docs/viewing-logs) says Cloud Scheduler publishes logs when starting/ending executions; use a scoped `cloudscheduler.googleapis.com/executions` log query for the exact job as extra independent negative evidence.
- Cloud Scheduler is at-least-once; a single `jobs.run` API call does not guarantee one delivered HTTP request or a successful HTTP 200. `/healthz` is a GET and the Gateway remains default OFF.

## New H2AD6C source — scoped first run, NO Owner execution so far

`scripts/step05_h2ad6c_scheduler_paused_minus1_log_guard_one_run_once_20261128.py`
- Creation commit `61797095d7d857f1f5373d79bacf574f4808f5d9`.
- Verified Git blob SHA-1 `5994f1c3f7370c913c50d558ca07e1596587e1ab`, source readback and static guards PASS. **Owner cloud result NOT claimed.**
- Owner previously approved ONE manual read-only OFF health dispatch; neither earlier script got to the POST, so this is the **first possible authorized attempt**, not a replay of committed action. The new source explicitly requires no old H2AD6/H2AD6B one-shot dispatch markers. If any exists, STOP before new POST.
- Exact frozen H2AD5 `PAUSED` job name `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128`, existing SA UID `110217058111344002447`, default `run.app` base, `GET /healthz`, OIDC audience, retry0, 30s deadline and UTC far-future Feb 29 schedule; root WSL isolated Owner SDK. No service-account or IAM changes.
- **NEW strict job GET:** require `PAUSED`, all exact frozen fields, no `lastAttemptTime`, status **exact integer `-1`** with no nonempty message/details or unexpected fields. If code is anything else, including `1`, STOP before run. This is a limited hypothesis gate, not proof of benign Scheduler behavior.
- **NEW one read-only execution log query:** `POST https://logging.googleapis.com/v2/entries:list` (a **read-only log listing despite HTTP POST**) for exactly `projects/oldx-staging`, `cloudscheduler.googleapis.com/executions`, `cloud_scheduler_job`, matching location and job ID, timestamp >= `2026-11-27T18:45:00Z` (prior to job creation). If log API forbidden, pagination present, any log record found or malformed response, STOP. **Empty log result alone is not whole-project proof of no execution**, hence combines no-lastAttempt and immutable job guards.
- Re-read exact paused job once immediately after log query and assert the same `-1`/no attempt evidence. Only THEN create a new root one-time marker `/root/.oldx-step05-h2ad6c-minus1-log-guard-one-manual-run-once-20261128` BEFORE one `POST ...:run` with empty JSON `{}` request. No retries and no `:resume` or `:pause`/other Cloud write. If POST succeeds, at most five subsequent exact job GET observations; do not infer target HTTP 200 from acceptance.
- A successful `H2AD6C_RESULT=ONE_MANUAL_RUN_ACCEPTED_REQUIRES_HTTP_PROOF` **only demonstrates one API dispatch acceptance**; H2AD7 distinct bounded Scheduler AttemptFinished + Cloud Run HTTP request logs and exact cleanup remain pending. If STOP before or after one-shot marker, do not rerun/recreate/delete/clear markers or make a second manual dispatch; preserve job PAUSED and reconcile.
- This is an **explicitly narrower implementation** of the previous Owner-approved one health dispatch: no new approvals for additional resources/identities or broader rights are inferred. It may still STOP safely if the code is not exactly `-1`.

### Exactly ONE owner Ubuntu root WSL paste for new H2AD6C

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad6c-first-run.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad6c.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/61797095d7d857f1f5373d79bacf574f4808f5d9/scripts/step05_h2ad6c_scheduler_paused_minus1_log_guard_one_run_once_20261128.py' &&
test "$(git hash-object "$d/h2ad6c.py")" = '5994f1c3f7370c913c50d558ca07e1596587e1ab' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad6c.py" &&
python3 -B "$d/h2ad6c.py" --h2ad6c-first-manual-off-health-run-minus1-log-guard-once
```

**Interpret strictly:** `H2AD6C_MARKER=CONSUMED_NO_REPEAT` appears only when one `jobs.run` is about to be attempted. If result `STOP` without marker, no API dispatch by H2AD6C. If marker exists, a dispatch may already have taken place even if API STOP—do not retry. If accepted, NEXT is independent HTTP result read, not another run. Never assume 200 from `jobs.run`.

## H2AD cleanup and Step05 still open

After actually reconciled delivery, use exact UID/etag guarded cleanup of the temporary job (must be paused/no active invocation), remove only the temporary probe from Gateway direct IAM while preserving Owner binding, then delete/disable the temporary SA with immutable UID verification. All of these resources are transient and approved for cleanup, not permanent infrastructure. Real Product hosted G2-G6 KMS/Firebase/Firestore/media/synthetic seller-to-buyer acceptance is still OPEN and cannot be declared complete by OFF-only health.
