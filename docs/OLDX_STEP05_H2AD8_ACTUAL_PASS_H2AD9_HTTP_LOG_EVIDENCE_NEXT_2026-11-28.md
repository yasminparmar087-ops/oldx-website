# BAJUTO / OLDX Step05 — H2AD8 actual resume/run/pause PASS; H2AD9 independent delivery evidence

## Owner actual screenshot — 28 November 2026 ~01:00 IST

Owner ran the previously explicitly approved, pinned `scripts/step05_h2ad8_owner_approved_one_resume_run_pause_once_20261128.py`, creation commit `1f8d0a1dc66bc9da05475537f0094627af2aa64e`, frozen Git blob `2fe7abcad66c394bc80779005944d6f0a377a349`, with hash check and Python AST validation in root Ubuntu WSL. Screenshot shows actual:

```text
H2AD8_MARKER=CONSUMED_NO_REPEAT
H2AD8_STAGE=ONE_JOB_RESUME
H2AD8_STAGE=ONE_EMPTY_BODY_MANUAL_RUN
H2AD8_JOBS_RUN_API=HTTP_200_ACCEPTED_NOT_TARGET_PROOF
H2AD8_STAGE=ONE_CONTAINMENT_PAUSE
H2AD8_RESUME_ATTEMPTED=TRUE
H2AD8_RUN_ATTEMPTED=TRUE
H2AD8_RUN_API_ACCEPTED=TRUE
H2AD8_PAUSE_ATTEMPTED=TRUE
H2AD8_FINAL_JOB_PAUSED_VERIFIED=TRUE
H2AD8_JOB_HTTP_TARGET_STATUS=NOT_INDEPENDENTLY_VERIFIED
H2AD8_SA_IAM_JOB_CREATE_DELETE_WRITES=NONE
H2AD8_H2_PRODUCTION=NO_GO
H2AD8_DO_NOT_REPEAT=TRUE
H2AD8_RESULT=ONE_MANUAL_RUN_ACCEPTED_AND_JOB_REPAUSED_WITH_LIMITS
H2AD8_NEXT=INDEPENDENT_SCHEDULER_AND_CLOUD_RUN_DELIVERY_READ
```

**Correct scope:** H2AD8 successfully called Scheduler `:resume`, then exactly one manually approved `:run` with zero-byte request body (Google Scheduler API **HTTP 200 accepted**), then the distinct `:pause` and final readback verified the **same job PAUSED**. Scheduler API HTTP 200 means acceptance of manual dispatch instruction; it is **NOT** hosted Gateway response HTTP 200, OFF JSON body verification, or an exactly-once delivery guarantee.

No new Scheduler job, SA, IAM grant, Cloud Run redeploy, KMS signing, Firestore/media/Product write or production activation. Existing Gateway image stays immutable default-OFF with internal-only ingress. H2AD8 consumed `/root/.oldx-step05-h2ad8-one-resume-run-pause-once-20261128`. Do **NOT** rerun H2AD8, old H2AD7/H2AD6C/H2AD6B/H2AD6/H2AD5/H2AD4/H2AD1 or earlier Cloud/CI/build/registry commands, and do not reset/delete their one-shot markers.

## Exact existing H2AD scope

- Cloud project `oldx-staging`, region `asia-south1`.
- One job `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128`, currently **PAUSED** at last readback, far-future `0 0 29 2 *` UTC, OIDC `GET /healthz`, audience exact saved default run.app base, no manual second `:run`.
- Target private Cloud Run `oldx-c2-h2-private-gateway`, immutable service UID `2d87153f-155e-409f-a418-463c785d8467`, `INGRESS_TRAFFIC_INTERNAL_ONLY` and `OLDX_H2U_MODE=OFF`, frozen H2U image. Source handler `functions/staging-marketplace/c2-h2u-private-off-http.mjs` returns `GET /healthz` HTTP 200 JSON `{ok:true, service:"oldx-c2-private-gateway", mode:"OFF"}` if actually reached.
- Existing temporary OIDC probe SA `oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`, numeric UID `110217058111344002447`, has only target Cloud Run direct Invoker beside Owner, verified by H2AD4. No broadened IAM or new identity.
- Clean up later once no delivery is in flight: delete only exact job, remove only temporary probe Invoker from this service while retaining Owner, disable/delete exact probe SA with UID+ETag controls. No cleanup writes were made by H2AD8.

## H2AD9 — new source-only read-only proof prepared, not Owner executed yet

- Source path `scripts/step05_h2ad9_actual_delivery_cloudrun_logs_readonly_once_20261128.py`.
- Source creation commit `b0d8a7d417c5ca726b6ae7cf3ae5df5d41a948a7`.
- GitHub source verified blob SHA1 `4e0fba4a193be86a4759a99c2932f4ada9e671c8`; static read-only scope, exact marker, source identity and no dispatch/cleanup checks PASS. No live results claimed.
- Root Ubuntu WSL existing isolated native Owner SDK; exact previous H2AD5 and H2AD8 root-owned markers; frozen job/service/SA UID and saved `run.app` base. New one-shot marker `/root/.oldx-step05-h2ad9-post-accepted-run-readonly-delivery-once-20261128` created before cloud reads. Never clear/retry on STOP.
- Exactly **three new reads for post-dispatch evidence**:
  1. `GET https://cloudscheduler.googleapis.com/v1/<exact job>`: validate final PAUSED, same OIDC `GET /healthz` target, far-future schedule/retry and summarize lastAttemptTime/status.
  2. `POST https://logging.googleapis.com/v2/entries:list` **read-only**, bounded 100 entries/no pagination, exact `oldx-staging` Cloud Scheduler `executions` log for that job (new after H2AD8, not redoing H2AD7 pre-dispatch inquiry); print sanitized `AttemptStarted` and `AttemptFinished` status names, never raw payloads.
  3. Another read-only `entries:list` for Cloud Run request logs `run.googleapis.com/requests`, exact `cloud_run_revision` service `oldx-c2-h2-private-gateway`, method GET, after `2026-11-27T18:45:00Z`. Locally match only exact default `run.app` `/healthz` URL (no query/fragment) and print only integer `httpRequest.status` values.
- **Interpretation**: a Cloud Run request log exact `GET /healthz` HTTP200 is strong server-side evidence that the private hosted Gateway returned HTTP 200; it **does not** expose response body `mode:OFF`, so do not claim actual body validation solely from that log. Scheduler `AttemptFinished SUCCESS` without Cloud Run exact request match is supportive but not equivalent to server-side HTTP 200. No logs, permission denial, pagination or unrecognized fields => mark incomplete/STOP, not success. A manual request could still be delivered more than once, even if only one jobs.run API call was made.
- No new `:run`, `:resume`, `:pause`, IAM grant, SA/job create/delete, KMS, Firestore or prod changes; no unredacted logs, OAuth, URLs, etags or IAM policy lists printed.
- Official references:
  - https://docs.cloud.google.com/scheduler/docs/viewing-logs
  - https://docs.cloud.google.com/run/docs/logging
  - https://docs.cloud.google.com/logging/docs/api/platform-logs
  - https://docs.cloud.google.com/scheduler/docs/reference/rest/v1/projects.locations.jobs

### Exactly one NEW Owner Ubuntu root WSL command for H2AD9

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad9-readonly.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad9.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/b0d8a7d417c5ca726b6ae7cf3ae5df5d41a948a7/scripts/step05_h2ad9_actual_delivery_cloudrun_logs_readonly_once_20261128.py' &&
test "$(git hash-object "$d/h2ad9.py")" = '4e0fba4a193be86a4759a99c2932f4ada9e671c8' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad9.py" &&
python3 -B "$d/h2ad9.py" --h2ad9-independent-off-http-delivery-readonly-once
```

A read-only successful result `H2AD9_RESULT=ONE_INDEPENDENT_DELIVERY_LOG_READ_PASS_WITH_LIMITS` must be interpreted alongside `H2AD9_INDEPENDENT_DELIVERY_VERDICT`, **not alone**. No claim of source/body verification unless independent evidence supports it. STOP => do not rerun old jobs.run, preserve markers and current PAUSED job. After delivery reconciliation, prepare one scoped UID/etag-guarded cleanup of the temporary H2AD job, exact Invoker and probe SA to limit ongoing cost/privilege and avoid stale test infrastructure.

**Current checkpoint:** `H2AD8=OWNER_ACTUAL_ONE_MANUAL_RUN_ACCEPTED_REPAUSED_PASS_WITH_LIMITS_CONSUMED`; `H2AD9=SOURCE_PREPARED_UNRUN`; `H2_HOSTED_HTTP_200=NOT_YET_VERIFIED`; `STEP05=ACTIVE`; `PRODUCTION=NO_GO`. G2–G6 hosted KMS/Firebase/media/seller→buyer release gates remain open after any OFF health test.
