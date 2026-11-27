# BAJUTO / OLDX Step05 H2W — new internal-only OFF Cloud Run Gateway actual PASS

**Evidence:** Owner root WSL screenshot at **27 Nov 2026 ~23:20 IST**. GitHub branch `security-hardening-review`. Source receipt and WSL screenshots are owner-provided; the assistant did not independently issue Cloud Run API calls or download the root-only evidence directory.

## Owner actual one-shot output (new service created)

The Owner used the **new corrected** (single predecessor tag fix) exact H2W runner:
`scripts/step05_h2w_one_new_internal_off_gateway_cloudrun_receipt_tag_fix_once_20261127.py`, immutable commit `e55857f4600f2a152a93fdc3ac1bec201bed7cad`, previously readback Git blob `a6986708b2fe0ac67aa214b544ca977244cf131d`. Screenshot shows:

~~~text
H2W_STAGE=ONE_NEW_INTERNAL_OFF_GATEWAY_SERVICE_CREATE_ATTEMPT
H2W_STAGE=ONE_OWNER_ONLY_NEW_SERVICE_INVOKER_POLICY
H2W_SERVICE_NAME=projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway
H2W_SERVICE_UID=2d87153f-155e-409f-a418-463c785d8467
H2W_GATEWAY_SA_UID=107238619872767759560
H2W_IMMUTABLE_IMAGE=asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2
H2W_CREATE_ATTEMPTED=TRUE
H2W_IAM_WRITE_ATTEMPTED=TRUE
H2W_OWNER_INVOKER=EXACT_OWNER_ONLY_DIRECT_BINDING_VERIFIED
H2W_INGRESS=INTERNAL_ONLY
H2W_HTTP_PROBES=NOT_ATTEMPTED_INTERNAL_ONLY
H2W_SERVICE_ROLLBACK=NOT_EXECUTED_UID_ETAG_GUARD_REQUIRED
H2W_OTHER_CLOUD_RUN_SA_REGISTRY_WRITES=NONE
H2W_KMS_FIRESTORE_WRITES=NONE
H2W_H2_PRODUCTION=NO_GO
H2W_RESULT=PASS_NEW_INTERNAL_OFF_SERVICE_AND_OWNER_DIRECT_INVOKER_WITH_LIMITS
H2W_REASON=ONE_SERVICE_CREATED_NO_HTTP_PROBES
H2W_EVIDENCE=/root/oldx-h2w-internal-gateway-h2w-bec776af3eccdd9da9
H2W_DO_NOT_REPEAT=TRUE
~~~

This is a **real Cloud Run create and one new-service IAM policy write** on project `oldx-staging`, region `asia-south1`, service `oldx-c2-h2-private-gateway`; these may incur usage charges. Not a simulated or source-only PASS. The returned **unique service UID** is `2d87153f-155e-409f-a418-463c785d8467`; the runtime SA **numeric immutable unique ID** is `107238619872767759560`, a different resource identity. Do not mix up these two IDs.

## Scope that the owner's script readback established

H2W source `inspect_service` required this new exact name, matching new immutable service UID on the final GET, creation session label, `oldx-h2=off-private`, `ingress=INGRESS_TRAFFIC_INTERNAL_ONLY`, `invokerIamDisabled=false`, runtime service account `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`, exactly pinned image digest above, `OLDX_H2U_MODE=OFF`, `NODE_ENV=production`, timeout `5s`, max concurrency 1, 1 CPU, 512 MiB, min instances 0, max instances 1 and nonblank service etag. After create it read the direct service IAM policy and applied/verified exactly one direct `roles/run.invoker` binding for `user:yasminparmar087@gmail.com`, with no other **direct** service bindings.

**Limits:** The Owner has not run an actual HTTP request against this newly deployed service, and status of new revision's live health/ready conditions is not confirmed by this output. Internal-only ingress restricts direct external WSL access; do not assume a publicly accessible URL should work. The **direct IAM policy check does not audit inherited project/folder/org grants** or effective reachability. The base-image publisher signature and previously completed Docker-local OFF health 200 / disabled 503 / unknown 404 checks are real past evidence but are **not** proof of hosted HTTP responses. Derived H2U release image still lacks independent release signature/CVE disposition.

## Preservation/no-repeat and rollback

- Single-use **H2W marker** `/root/.oldx-step05-h2w-new-internal-off-cloudrun-service-once-20261127` is **CONSUMED**. The old first H2W runner previously stopped before writes due a 19/20-hex predecessor tag typo, but the corrected runner has now done the **only** approved new service create/IAM write. Never rerun either H2W, reuse its marker, or delete the marker.
- Owner-local sensitive evidence `/root/oldx-h2w-internal-gateway-h2w-bec776af3eccdd9da9` contains sanitized result and service etag/session details. **Do not paste tokens, JSON configs, Cloud auth or unredacted sensitive evidence into GitHub.** Keep this directory for later guarded rollback/reconciliation.
- No service cleanup or rollback performed; service is intentionally retained for later private staged verification. Future deletion requires a **new separate targeted owner decision** and fresh exact service UID/etag/session checks. Existing `oldx-owner-read`, prior deleted H1B trial, legacy services, registry, service accounts and other resources remain outside this authorization. H2V image push and H2U local build were each executed once previously; **DO NOT repeat**.

## Next critical path

**Prefer new, source-only plan for two unsatisfied dimensions without repeating any old tests:**
1. New hosted revision readiness/traffic/config status and **inherited/ancestor IAM** inspection focused solely on this H2W service and project. A separate read-only check should not re-run the already completed H2W direct policy check except when essential to correlate conditions.
2. An **actual internal-network-origin HTTP verification**, only after verifying that the chosen internal client source is supported by Cloud Run ingress routing. Do not switch ingress to `ALL` for test convenience and do not relax auth. A new job, network, or Cloud resource requires separately scoped Owner approval.

Other live gates: independent KMS KeyVersion **status-reader** permission, durable non-TTL Firestore one-sign budget transaction and single bounded synthetic sign approval; no enablement of Product production. Potential image security and provenance assessment remains pending.

**Checkpoint:** `H2W_NEW_PRIVATE_RUN=ACTUAL_PASS_SERVICE_CREATED`, `H2W_DIRECT_OWNER_INVOKER=ACTUAL_PASS`, `H2W_SERVICE_UID=2d87153f-155e-409f-a418-463c785d8467`, `H2W_OFF_HOSTED_HTTP=NOT_TESTED`, `H2W_INHERITED_IAM=NOT_AUDITED`, `H2W_ONE_SHOT=CONSUMED`, `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`.
