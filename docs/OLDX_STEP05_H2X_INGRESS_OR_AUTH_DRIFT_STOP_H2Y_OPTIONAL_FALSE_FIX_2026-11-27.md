# BAJUTO / OLDX Step05 H2X→H2Y — STOP on optional invoker IAM default, corrected exact read-only guard

**Owner actual screenshot: 27 Nov 2026 ~23:58 IST** from old H2X script `scripts/step05_h2x_new_h2w_hosted_revision_readiness_readonly_once_20261127.py`, commit `9913908772a301583c6921a9ef0a778264d69f9d` Git blob `e4c053baae63340bc721821899db667572d0ed8b`.

~~~text
H2X_RESULT=STOP_BEFORE_OR_DURING_READ_ONLY_GET
H2X_REASON=INGRESS_OR_AUTH_DRIFT
H2X_CLOUD_WRITES=NONE
H2X_H2_PRODUCTION=NO_GO
~~~

This combined STOP **does not establish actual ingress or Invoker permission drift**. H2X successfully got past the prior H2W marker and exact service name+UID checks, but its combined condition `service.get("ingress")=="INGRESS_TRAFFIC_INTERNAL_ONLY" and service.get("invokerIamDisabled") is False` failed. It does not report which component failed.

The earlier H2W **actual PASS** `scripts/step05_h2w_one_new_internal_off_gateway_cloudrun_receipt_tag_fix_once_20261127.py` explicitly accepted `s.get("invokerIamDisabled",False) is False`; H2X incorrectly required the optional false-valued field to be physically present in service GET JSON. Google Cloud Run V2 describes `invokerIamDisabled` as optional boolean; for omitted protobuf default false, using `.get("invokerIamDisabled",False)` is consistent with H2W and does not accept explicitly true, null or unexpected types. **This mismatch is a plausible cause, not proven from screenshot**; ingress may actually have drifted, so new check reports both values independently and fails closed on genuine drift.

## New source-only H2Y diagnostic/readiness, NOT executed yet

- File: `scripts/step05_h2y_h2x_optional_false_invoke_diagnostic_readonly_once_20261127.py`
- Creation commit: `b5dce880ece441ba0078a829a21bfc2703593fb7`
- Git blob `df563e0aaf16812b6b6f26a09f6b62a62684d8e0`, fetched/readback verified.
- All original exact H2W service UID `2d87153f-155e-409f-a418-463c785d8467`, project `oldx-staging`, region `asia-south1`, existing isolated Owner OAuth setup, image immutable digest `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2` and OFF-only safeguards preserved.
- Before acceptance, prints `H2Y_OBSERVED_INGRESS` and `H2Y_INVOKER_IAM_DISABLED_JSON`, with the latter either `TRUE`, `FALSE`, `ABSENT_DEFAULT_FALSE` or `UNEXPECTED`. If ingress not **`INGRESS_TRAFFIC_INTERNAL_ONLY`** STOP `INGRESS_ACTUAL_DRIFT`; if Invoker disabled is explicitly true or another unexpected value STOP `IAM_INVOKER_ACTUAL_DRIFT`.
- Only on passing actual safe service identity, ingress and auth checks does it display distinct latest created/ready revision, generations, reconciling, terminal condition, traffic and readiness status. A transient/incomplete control plane view is **not** a readiness PASS.
- One `GET https://run.googleapis.com/v2/projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway` to read **new exact hosted revision state**, no IAM read/write, Cloud Run create/update/deploy, Docker build/push or rerun old source tests. No public endpoint exposure. Exact H2W consumed marker unchanged. **Do not rerun the old H2X script; use this distinct corrected diagnostic only.**
- Passing service readiness still does **not** prove an internal origin hosted HTTP test, inherited/effective IAM audit, new image vulnerability risk, KMS status reader or Firestore signing ledger.

### Exact one paste in Owner root Ubuntu WSL

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2y-readiness-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/readiness.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/b5dce880ece441ba0078a829a21bfc2703593fb7/scripts/step05_h2y_h2x_optional_false_invoke_diagnostic_readonly_once_20261127.py' &&
test "$(git hash-object "$d/readiness.py")" = 'df563e0aaf16812b6b6f26a09f6b62a62684d8e0' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/readiness.py" &&
python3 -B "$d/readiness.py" --h2y-corrected-h2x-false-default-readonly-once
~~~

If `H2Y_RESULT=READ_ONLY_NEW_REVISION_READY_PASS_WITH_LIMITS`, this confirms control-plane revision readiness only; no live HTTP/traffic invocation proof. If STOP, do **not** change ingress/IAM or rerun previous H2W/registry steps; send H2Y output. Do not send Owner tokens or private SDK config.

**Status:** `H2W_NEW_GATEWAY_CLOUD_RUN=ACTUAL_PASS_CONSUMED`; `H2X_READINESS=STOP_INGRESS_OR_AUTH_COMBINED_CHECK_AMBIGUOUS`; `H2Y_READONLY_CORRECTION=SOURCE_READY_NOT_EXECUTED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
