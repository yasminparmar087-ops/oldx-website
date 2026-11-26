# OLDX Step05 H1B W3–W6 — ACTUAL private OFF test passed; exact NEW Cloud Run service deleted

**Owner screenshot 26 Nov 2026 ~22:09 IST** from WSL `OLDX-Ubuntu-24.04` root. Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. The **owner executed** the single session script pinned at commit `9c6484836fbdd720ffe18659bc4b31ffd2264596`, Git blob `cb588678a1756fbc36cbd0b6a036c62b68f87858`, path `scripts/step05_h1b_w3_w6_new_only_one_session_20261126.py`. The assistant has NOT independently made Cloud API calls; claims below are exactly the screenshot/script-reported evidence.

## ACTUAL owner output (verbatim)
```text
H1B_W3W6_STAGE=ONE_NEW_PRIVATE_OFF_SERVICE_CREATE_ATTEMPT
H1B_W3W6_STAGE=FOUR_BOUNDED_NEW_SERVICE_ONLY_PROBES
H1B_W3W6_NEW_SA_UID=115445220422157278526
H1B_W3W6_SERVICE_UID=83d724b3-fcf0-4607-8107-f111a2eacc31
H1B_W3W6_CREATE_ATTEMPTED=TRUE
H1B_W3W6_OWNER_INVOKER=EXACT_OWNER_ONLY_BINDING_VERIFIED
H1B_W3W6_HTTP_PROBES_ATTEMPTED=4
H1B_W3W6_SERVICE_CLEANUP=NEW_ONLY_RUN_SERVICE_DELETED_CONFIRMED
H1B_W3W6_SA_CLEANUP=RETAIN_PENDING_DEPENDENCY_GUARDS
H1B_W3W6_REGISTRY_IMAGE=RETAIN_NOT_REPUSHED
H1B_W3W6_RESULT=PASS_PRIVATE_OFF_FOUR_PROBES_AND_SERVICE_DELETED_SA_RETAINED
H1B_W3W6_REASON=EXPECTED_403_200_503_404
H1B_W3W6_DO_NOT_REPEAT=TRUE
```

**Verified by output:** Actual ONE new private compiled-OFF Cloud Run service `projects/oldx-staging/locations/asia-south1/services/oldx-c2-website-mediator`, exact new `uid=83d724b3-fcf0-4607-8107-f111a2eacc31`, successfully created; one exact service-level `user:yasminparmar087@gmail.com` invoker binding verified, no anonymous Invoker. Exactly four status checks passed: anonymous `GET /health` **403**, Owner authenticated `GET /health` **200**, authenticated `POST /api/staging/marketplace/owner` **503** (compiled OFF), authenticated unknown path **404**. Same script then **confirmed deletion via exact service UID, nonce label, image, runtime SA, direct IAM and fresh etag**, operation completed and subsequent GET returned **404**. Thus **the new Cloud Run service is confirmed absent at cleanup time** and does not need another delete/readback one-shot; do not rerun previous W3–W6 operations or consume another verification.

**Distinct residual:** Newly created W1 no-user-key SA `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` exact `uniqueId=115445220422157278526` **remains enabled/disabled status unverified**, intentionally retained pending usage/dependency guard. Exact immutable G2B Registry image `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e` **remains stored** as approved; no second push or deletion. The old C1A SA/image resources are unrelated, reference status unknown: never delete them here.

## Next NEW-only closeout

1. Preserve exact W3–W6 marker `/root/.oldx-h1b-w3w6-private-off-once-20261126` as consumed; don't rerun/create/probe/delete this already removed service. Record latest operator identity, project, W1 UID and exact W3W6 success marker before a **new distinct** SA-closeout action.
2. Google's IAM guidance recommends **disable service account first**, monitor at least 24 hours for unintended dependencies, then consider deleting it. Newly created SA is for a bounded test, and the target Cloud Run service was confirmed deleted. However there is no comprehensive cross-project/other-service reference inventory in this screenshot; do not falsely assert fully unreferenced status.
3. Fastest SAFE next W6 SA step: one owner-approved, new-only, **reversible disable** of exactly W1 UID if a fresh exact SA UID GET, new service GET 404, and resource-level disable/enable rights return; preserve evidence and do **NOT** delete the SA immediately. That leaves a disabled residual until later identity/dependency-guarded cleanup decision. No update to any other SA, service, registry, IAM grants, Firebase or production. If any permission mismatch/unknown STOP without write.
4. Mark H1B private/OFF experiment **PASS with cleanup limits** only after the SA is safely disabled or its retention is explicitly accepted; do not claim entire Step05/15 or production launch complete. W3W6 service cleanup is **already complete**, not a long-running task.
5. Step04 C1A older residual separate approved retention ends 28 Nov 2026 23:19 IST; do not bundle unrelated cleanup with this new SA.

Official IAM disable-first guidance https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/disable ; Cloud Run delete API https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/delete .

## Current checkpoint
`G2B=ACTUAL_ONE_PUSH_VERIFIED`, `W0=PASS`, `W1=ACTUAL_NEW_SA_UID_FROZEN`, `W3V=PASS`, `W3-W6_CLOUD_RUN=PASS_FOUR_PROBES_AND_UID_GUARDED_SERVICE_DELETE_CONFIRMED`, `SA_CLEANUP=RETAINED_NOT_YET_DONE`, `H1B_IMMUTABLE_REGISTRY_IMAGE=RETAINED`, `H2/PRODUCTION=NO_GO`.
