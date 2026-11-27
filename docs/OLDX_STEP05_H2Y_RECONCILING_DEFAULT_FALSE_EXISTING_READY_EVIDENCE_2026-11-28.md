# BAJUTO / OLDX Step05 H2Y — Existing readback establishes hosted revision READY_WITH_LIMITS, no repeated GET

**Actual Owner screenshot:** 28 Nov 2026 ~00:02 IST, root WSL. **No Cloud writes.** This record distinguishes the **raw script result** from a subsequent source/API-semantic evaluation. Nothing was redeployed or re-queried.

## Raw actual H2Y output — preserve, do not rewrite

Owner executed exact source `scripts/step05_h2y_h2x_optional_false_invoke_diagnostic_readonly_once_20261127.py`, commit `b5dce880ece441ba0078a829a21bfc2703593fb7`, Git blob `df563e0aaf16812b6b6f26a09f6b62a62684d8e0`. The latest Owner terminal screenshot shows:

~~~text
H2Y_OBSERVED_INGRESS=INGRESS_TRAFFIC_INTERNAL_ONLY
H2Y_INVOKER_IAM_DISABLED_JSON=ABSENT_DEFAULT_FALSE
H2Y_SERVICE_UID=2d87153f-155e-409f-a418-463c785d8467
H2Y_GENERATION=1
H2Y_OBSERVED_GENERATION=1
H2Y_LATEST_CREATED_REVISION=projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway/revisions/oldx-c2-h2-private-gateway-00001-wrw
H2Y_LATEST_READY_REVISION=projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway/revisions/oldx-c2-h2-private-gateway-00001-wrw
H2Y_TERMINAL_CONDITION=CONDITION_SUCCEEDED
H2Y_RECONCILING=UNKNOWN
H2Y_TRAFFIC_TOTAL_PERCENT=100
H2Y_NEW_HOSTED_REVISION_READY=NOT_VERIFIED
H2Y_CLOUD_READ=ONE_EXACT_SERVICE_GET
H2Y_DIRECT_IAM=H2W_PREVIOUS_PASS_NOT_REPEATED
H2Y_INHERITED_IAM=NOT_AUDITED
H2Y_HOSTED_HTTP=NOT_TESTED
H2Y_CLOUD_WRITES=NONE
H2Y_BUILD_PUSH_DEPLOY=NONE
H2Y_H2_PRODUCTION=NO_GO
H2Y_RESULT=STOP_NEW_REVISION_READY_NOT_VERIFIED
~~~

**Important:** `H2Y_RESULT=STOP_NEW_REVISION_READY_NOT_VERIFIED` is the actual script result and MUST NOT be misreported as a raw PASS. The script computed `recon=service.get("reconciling","UNKNOWN")`; `H2Y_RECONCILING=UNKNOWN` specifically means the field was **absent** from this JSON response (not explicitly `true` or `null`), and it then required `recon is False`, which incorrectly rejects an omitted default-false proto3 bool. All other readiness fields meet the strict check, including created==ready revision, observed==generation, terminal succeeded and traffic=100%.

## Authoritative semantics and existing-evidence evaluation

- Official [Google Cloud Run V2 Service protobuf](https://docs.cloud.google.com/go/docs/reference/cloud.google.com/go/run/latest/apiv2/runpb) declares `Reconciling bool ` with `json:"reconciling,omitempty"` (proto3). This is a scalar default-false boolean; omitted `reconciling` **represents false by default**.
- The official [ProtoJSON format](https://protobuf.dev/programming-guides/json/) explains that implicit-presence fields with default values are omitted from the serialized JSON by default. This covers `false` boolean fields.
- The official [Google Cloud Run Service readiness semantics](https://docs.cloud.google.com/php/docs/reference/cloud-run/latest/V2.Service): reconciliation `false` with matching observed/generation, latest ready/created revision, traffic status and `CONDITION_SUCCEEDED` gives successful control-plane reconciliation. The screenshot contains all these facts.

**Defensible derived conclusion from this same existing readback (no new Cloud request):**
`H2Y_EXISTING_SERVICE_READBACK_EVALUATION=CONTROL_PLANE_READY_PASS_WITH_LIMITS`.
This is a **post-hoc interpretation**, not a new test execution or a changed H2Y stdout result. The reported original `H2Y_NEW_HOSTED_REVISION_READY=NOT_VERIFIED` is a script false-negative from treating an omitted proto3 default-false scalar as `UNKNOWN`. Do not rerun H2X/H2Y just to convert the cosmetic stdout status. The actual Cloud service could change subsequently; the conclusion is only for the captured 28 Nov readback.

### Exact resource identity pinned

- New **service UID** `2d87153f-155e-409f-a418-463c785d8467` — different from Gateway runtime SA UID `107238619872767759560`.
- New service `projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway`.
- Matching latest created/ready revision `oldx-c2-h2-private-gateway-00001-wrw`.
- Immutable H2U remote registry index `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`.
- Internal-only ingress and IAM Invoker check enforced (optional absent `invokerIamDisabled` default false), Owner **direct** new service Invoker policy had already passed H2W and is NOT repeated.
- Site/Buyer Product activity stays OFF. No hosted HTTP request has occurred; no direct or inherited IAM change; no other Cloud mutation.

## NEXT required Step05 work — not repeated

**A. Effective/inherited IAM visibility:** Scope a **new** read-only audit of possible project/folder/org inherited `run.invoker` role and conditional grants, **not another H2W direct service policy set** and not an unjustified blanket claim of effective IAM. Respect Owner's policy that other accounts should not receive extra permissions. Determine whether there is any accidental broader path by which an internal-origin principal could invoke.

**B. Actual hosted OFF-only HTTP verification:** Current ingress `INGRESS_TRAFFIC_INTERNAL_ONLY` intentionally rejects public desktop WSL origin. Google [Cloud Run ingress docs](https://docs.cloud.google.com/run/docs/securing/ingress) explain that **Cloud Run to Cloud Run** calls to internal-only targets must route through an accepted VPC. Verify whether an existing **same-project private VPC** and suitable internal-origin probe already exist before creating anything. A new Cloud Run Job/VM/VPC/network or service invoker grants are NOT covered by H2W approval and require separately scoped Owner consent; never set `INGRESS_TRAFFIC_ALL` for convenience.

**C. Remaining independent Step05 H2 blockers:** KMS exact KeyVersion status reader, Firestore durable one-sign non-TTL transaction, independently scoped synthetic KMS sign, derived release-image security/provenance disposition. No production enablement.

**One-shot/do-not-repeat:** H2U local image build, H2V Registry push, H2W service create+direct Owner IAM, H2X and H2Y existing readiness GETs, earlier 65-file source tests/ESM checks and H1B/H2S/H2T/H2N/H2R audits must NOT be rerun. No marker resets/deletes.

**Checkpoint:** `H2W_NEW_PRIVATE_GATEWAY=ACTUAL_PASS`; `H2Y_RAW_SCRIPT=STOP_FALSE_NEGATIVE_RECONCILING_ABSENT`; `H2Y_EXISTING_READBACK=CONTROL_PLANE_READY_PASS_WITH_LIMITS`; `H2_HOSTED_HTTP=NOT_TESTED`; `H2_INHERITED_IAM=NOT_AUDITED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
