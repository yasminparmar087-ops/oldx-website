# OLDX Step 05 H1B — W3V actual Owner dry-run PASS (26 Nov 2026 ~22:00 IST)

Owner screenshot from root WSL in `OLDX-Ubuntu-24.04` executing pinned `scripts/step05_h1b_w3_off_private_validate_only_once_20261126.py` at commit `8679d110ea36b9706129a00c742676afa5f46ce7`, Git blob `62ca63d02167c3b8988759cc4cf6891d0213326e`. This record is screenshot-based; assistant has **not** executed Google Cloud API or Owner WSL.

## Exact result
```text
H1B_W3V_NEW_SA_UID=FROZEN_MATCH
H1B_W3V_NEW_SERVICE=ABSENT_404_BEFORE_VALIDATE
H1B_W3V_IMAGE=FROZEN_REMOTE_G2B_DIGEST
H1B_W3V_RESULT=VALIDATE_ONLY_ACCEPTED_WITH_LIMITS
H1B_W3V_REASON=NEW_PRIVATE_OFF_CLOUD_RUN_CONFIG_VALIDATED_NO_CREATION
H1B_W3V_CLOUD_RESOURCE_WRITES=NONE
H1B_W3V_NEW_CLOUD_RUN_SERVICE=NOT_CREATED
H1B_W3V_DO_NOT_REPEAT=TRUE
```

**Meaning:** Google Cloud Run v2 `create?validateOnly=true` API accepted one proposed private compiled-OFF configuration. It did not persist a Cloud Run service; it does **NOT** prove runtime boot, HTTP health, inherited IAM/public invoker status, future create authority, readiness or subsequent cleanup. New SA `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, immutable `uniqueId=115445220422157278526`, remained verified. Prior one-push remote image `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e` was referenced; **not re-pushed**. Current new Cloud Run service name `oldx-c2-website-mediator` was absent HTTP404 immediately before validation. No actual Run/IAM writes occurred in W3V.

**Consumed exact marker:** `/root/.oldx-h1b-w3-private-validate-only-once-20261126`. Do NOT retry/reset it or W1/G2B/W0/G1/H1A/S1/S2/S3B/C1A markers.

## Next fastest safe NEW-only stage

Previously explicit owner approval remains in force for one strictly supervised staging-only **W3 actual private OFF deployment, optional W4 exact Yasmin service-level Invoker, W5 at most four private new-service-only HTTP probes, W6 same-session guarded deletion of exactly that NEW Run service, and new SA only if UID/dependencies can be verified**. The image W2 is already in Registry. Prepare a bounded one-session execution with:
- a distinct preflight and one-shot marker, current exact NEW service 404, exact new SA UID and image, targeted delete and Invoker rights
- capture operation name, service UID, etag, revision and direct IAM; no `allUsers`/`allAuthenticatedUsers`; reject inherited/public access if anonymous GET is not 403
- no real data, keys, provider credentials, Firebase, external business endpoints, or existing service edits
- independent exact new-only rollback in finally (Cloud Run delete with fresh verified UID/etag) even when tests fail; if uncertain/partial creation, STOP_MANUAL_RECOVERY and retain evidence rather than guessing identity, never delete old services
- no promise of automatic cleanup if operator closes WSL, network fails, or service identity drifts; any resource not confirmed deleted must be explicitly recorded

Google official APIs verified on 26 Nov: https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/create , https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/delete , https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/getIamPolicy , https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.operations/get . IAM service account delete is destructive; Google recommends disable then a 24h observation period; do not assume safe immediate deletion simply because newly created if references are uncertain: https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/delete .

**State:** W3V `ACTUAL_PASS_CONSUMED`; W1 `ACTUAL_PASS_NEW_SA_UID`; G2B `ACTUAL_PASS_REMOTE_IMAGE`; W3/W4/W5/W6 `NOT YET EXECUTED`; Step05 `IN_PROGRESS`; H2/production `NO_GO`.
