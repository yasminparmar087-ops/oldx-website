# BAJUTO / OLDX Step05 — H2AB Scheduler API enablement read-only, source prepared

**Latest actual owner:** 28 Nov 2026 ~00:10 IST, H2AA `SERVICE_STATE_AND_OPTIONAL_PROJECT_PERMISSION_HINTS_PASS_WITH_LIMITS`, `COMPUTE_API=DISABLED`; no Compute API enable, VPC checks repeated, permission grants or Cloud resource writes. H2AA one-shot consumed; do not rerun, and preserve H2Z 403 and prior H2W/H2Y/OCI receipts. See [H2AA actual and Scheduler route](OLDX_STEP05_H2AA_ACTUAL_COMPUTE_API_DISABLED_AND_SCHEDULER_ROUTE_2026-11-28.md).

## Google verified no-VPC alternative

Same-project Cloud Scheduler targeting the Cloud Run service's *default* `run.app` URL is eligible as internal ingress source. A Cloud Run-to-Cloud Run client is different and may require VPC. One existing H2W private service has only direct Owner user Invoker, not a Scheduler OIDC service-account binding. Cloud Scheduler HTTP delivery therefore would need separate narrowly scoped permissions and explicit cloud resource write/cost approval; **not authorized at this step**.

Sources:
- https://docs.cloud.google.com/run/docs/securing/ingress
- https://docs.cloud.google.com/scheduler/docs/creating
- https://docs.cloud.google.com/run/docs/triggering/using-scheduler
- https://docs.cloud.google.com/scheduler/docs/http-target-auth

## H2AB new script: source READY only

- `scripts/step05_h2ab_cloudscheduler_api_state_readonly_once_20261128.py`
- Creation commit `ab2c24a872525052d493987c9b850ef1b768e101`
- Verified Git blob `4ee2c66c9586b6fbc5ee4fbd0a2881491b7ee270`.
- Owner WSL execution **NOT YET DONE**. GitHub fetch/readback and static scope checks pass. Do not claim live result/AST pass until actual owner execution.
- Preflight: Ubuntu root WSL, isolated native SDK and owner OAuth, exact prior H2AA consumed marker and `oldx-staging`; creates distinct one-shot marker `/root/.oldx-step05-h2ab-cloudscheduler-api-state-once-20261128` before Google GET.
- At most **ONE** new read-only API call: `GET https://serviceusage.googleapis.com/v1/projects/38472235077/services/cloudscheduler.googleapis.com?fields=name%2Cstate`.
- Only prints `ENABLED` or `DISABLED` if exact returned service identity matches; 403, network, output cap or parse mismatch is STOP, not an inferred state. Never retry a consumed one-shot.
- Does NOT enable any API, create or list Scheduler jobs, grant IAM, touch the old Compute/VPC network GET/Cloud Run H2W/H2Y, send hosted HTTP, sign KMS or write Firestore. H2 and production remain NO-GO.

### Exactly one new WSL root paste

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ab-readonly-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ab.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/ab2c24a872525052d493987c9b850ef1b768e101/scripts/step05_h2ab_cloudscheduler_api_state_readonly_once_20261128.py' &&
test "$(git hash-object "$d/h2ab.py")" = '4ee2c66c9586b6fbc5ee4fbd0a2881491b7ee270' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ab.py" &&
python3 -B "$d/h2ab.py" --h2ab-scheduler-api-state-readonly-once
```

### Next after receiving H2AB actual output

- If `DISABLED`, request **new explicitly scoped owner consent** before enablement of *only* `cloudscheduler.googleapis.com`, plus a separate bounded one-off Scheduler OIDC/Invoker/job create/run/cleanup sequence. Do NOT enable Compute API, VPC or open Cloud Run ingress.
- If `ENABLED`, omit API enable and inspect only the relevant exact job name and role prerequisites before requesting the scoped one-off action approval.
- In either case, an OFF-only `/health` HTTP probe proves only hosted OFF behavior, not live Product/KMS/Firestore completion. Use only a target-specific, least-privilege Scheduler OIDC identity with Invoker granted on exactly the one H2W Gateway (never allUsers/allAuthenticatedUsers); a paused/guarded job with manual single dispatch and cleanup. Schedule/response may be asynchronously delivered; do not claim success until evidence. Require rollback and resource/cost awareness.

**Checkpoint:** `H2AA=ACTUAL_PASS_COMPUTE_DISABLED_CONSUMED`; `H2AB=SOURCE_READY_UNRUN`; `H2_HOSTED_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `H2=NO_GO`; `PRODUCTION=NO_GO`.
