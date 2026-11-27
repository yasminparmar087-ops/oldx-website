# BAJUTO / OLDX Step05 — H2AD6 pre-dispatch STOP, status-aware H2AD6B first manual attempt

## Owner actual WSL screenshot, 28 Nov 2026 ~00:43 IST

Owner downloaded the pinned previous `scripts/step05_h2ad6_one_paused_job_manual_off_health_dispatch_once_20261128.py` source from immutable commit `0bf8d4be4e4ded465757b40fef12c0e9b6532ee8`, verified Git blob `4afd1cc3d3f29a3e664e0e107d21f76d59f4ee28`, checked Python AST, and executed exactly once. Screenshot shows:

```text
H2AD6_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_ONE_DISPATCH
H2AD6_REASON=PREEXISTING_STATUS_ABORT_NO_MORE_DISPATCH
H2AD6_ACTION=NO_RERUN_NO_RESUME_NO_AUTOMATIC_CLEANUP
H2AD6_H2_PRODUCTION=NO_GO
```

**Key causal source inspection:** In H2AD6 `inspect_job`, the exact paused GET /healthz target/schedule/OIDC checks passed. The `need(not doc.get("lastAttemptTime"))` assertion **also passed**, then `need(not doc.get("status"))` failed because the response had a **nonempty `status` object**. The script reaches its one-shot `H2AD6_MARKER=CONSUMED_NO_REPEAT` and only `jobs.run` **AFTER** these assertions. **No H2AD6 marker printed, no `POST jobs.run` sent by this invocation, no Gateway hosted HTTP proven.** We have not read the exact `status.code/message/details` values; never claim they were benign or indicative of a prior execution. Original H2AD6 invocation should **NEVER be repeated**. Script code is retained as failed evidence, not edited in place.

The previously actual successful H2AD5 job create+pause stays the last verified write; exact job `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128` was PAUSED and used existing probe SA UID `110217058111344002447` and internal Gateway UID `2d87153f-155e-409f-a418-463c785d8467`. The original H2AD6's immediate GET showed PAUSED and exact read-only OIDC URI; no external actors were audited. Distinguish **source-proven no dispatch by H2AD6** from system-wide proof that nobody else has attempted the job.

Official [Cloud Scheduler Job REST](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs): `lastAttemptTime` is the time a job attempt began and `status` is target's last-execution status; presence of a status object alone is not enough to infer why lastAttemptTime is absent, and nonzero status cannot safely be ignored. [RunJob REST](https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs/run) is ONE action that forces dispatch; a successful HTTP200 **from jobs.run** is NOT proof the Cloud Run target returned 200. The request body is empty; new source uses zero-byte POST rather than JSON `{}`.

## H2AD6B — source-only guard for FIRST actual paused/manual health request (not executed)

Owner previously approved **one** Scheduler manual `GET /healthz` in H2AD scope. H2AD6 pre-dispatch STOP made **zero** such API requests, so H2AD6B is the first potential attempt under that scope, not an extra retry of a committed write. If any original H2AD6 marker is actually found, H2AD6B STOPs before dispatch. Never delete any marker.

- New script: `scripts/step05_h2ad6b_status_aware_one_manual_paused_health_dispatch_once_20261128.py`
- Immutable creation commit `1f50c4d3c94142341f3633c9c743b7a70ccd61e2`.
- Verified Git blob `e44cc4721502ca0681b4103013461db30e9a49c6`.
- GitHub readback and static one-POST/marker/target/identity and no-other-write checks PASS. **No actual Owner Python invocation, API result, or HTTP target proof claimed yet.**
- Uses exact Owner root Ubuntu WSL isolated native SDK and old H2AD5 frozen marker, exact SA UID `110217058111344002447`, Cloud Scheduler job and immutable default `run.app` base. It verifies the original H2AD6 one-shot marker is **absent**, and new H2AD6B marker is **absent**.
- One **fresh exact job GET** (a new dispatch-time purpose, not repeating H2AD5 create/pause). Fail closed unless `PAUSED`, exact `GET /healthz` and OIDC SA/audience, far-future UTC schedule, retry0, 30s deadline and **no `lastAttemptTime`**.
- **Corrected guard:** Optional `status` is allowed only if omitted, empty, or a **default OK** status object `code=0` with no nonempty `message` or `details`, no unexpected keys. Nonzero code, message/details or lastAttemptTime => STOP **before new marker/POST**. This is a tight operational compromise, not evidence proving no prior executions system-wide. Source prints sanitized pre-status category. It neither erases/rewrites a prior status nor constructs an OAuth/ID token on its own.
- If and only if all new guards pass: create `/root/.oldx-step05-h2ad6b-status-aware-manual-health-run-once-20261128` **BEFORE** one `POST .../jobs/oldx-h2ad-off-healthz-20261128:run` with an empty request body. No retries even if 400/timeout; do not resume or create another job. After accepted response, at most five GET observations of the exact same PAUSED job, no second run.
- `jobs.run` HTTP200 and job lastAttemptTime/status are dispatch evidence **only**, not independent target HTTP200 nor body `mode:OFF`. Separate H2AD7 Scheduler AttemptFinished and Cloud Run sanitized request logs or other trustworthy server evidence required. Clean up the one job + target-only Invoker binding + probe SA UID only after dispatch outcome and in-flight work are reconciled; prior approval covers exact guarded cleanup but not blind deletion.
- If any STOP before/after POST, do not replay H2AD6B, do not resume paused job and do not auto-cleanup on ambiguity. Product OFF, H2/production NO-GO.

### Exactly one new Ubuntu WSL root command, H2AD6B only

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad6b-status-aware.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad6b.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/1f50c4d3c94142341f3633c9c743b7a70ccd61e2/scripts/step05_h2ad6b_status_aware_one_manual_paused_health_dispatch_once_20261128.py' &&
test "$(git hash-object "$d/h2ad6b.py")" = 'e44cc4721502ca0681b4103013461db30e9a49c6' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad6b.py" &&
python3 -B "$d/h2ad6b.py" --h2ad6b-owner-approved-status-aware-one-health-run-once
```

Interpretation: If `H2AD6B_RESULT=ONE_PAUSED_MANUAL_RUN_ACCEPTED_WITH_LIMITS`, it only means accepted one dispatch. If `H2AD6B_RESULT=STOP_BEFORE_OR_AFTER_POSSIBLE_ONE_RUN` and `H2AD6B_MARKER` absent, no POST issued by this new source. If marker present and STOP, outcome could be ambiguous; no repeat. In ALL cases remain `H2_HOSTED_HTTP` unproven until independent log check, and `STEP05=ACTIVE`, `PRODUCTION=NO_GO`.

**No repeats:** H2AD0/1/2/3/4/5 and original H2AD6, H2U/V/W/X/Y/Z, H2AA/AB/AC, old H1B/KMS and local tests; do not change branch `main` or regrant IAM.
