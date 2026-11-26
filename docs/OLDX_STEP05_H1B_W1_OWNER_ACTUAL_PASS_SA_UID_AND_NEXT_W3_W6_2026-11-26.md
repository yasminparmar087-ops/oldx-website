# OLDX Step05 H1B — W1 ACTUAL OWNER SUCCESS and new SA uniqueId frozen

**26 November 2026 ~21:54 IST — Owner Ubuntu WSL screenshot.** Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Source was previously pinned `scripts/step05_h1b_w1_no_key_sa_create_once_20261126.py` commit `3d8c1b54d10fd8b6f09c7ce3ff4d82aa259b9884`, blob `19ff960ff00666565d944c7f62354bb4c6cf64c9`.

## Observed exact W1 screenshot output

```text
H1B_W1_STAGE=ONE_APPROVED_NEW_SA_CREATE_ATTEMPT
H1B_W1_SA_UID=115445220422157278526
H1B_W1_SA_CREATE_ATTEMPTED=TRUE
H1B_W1_RESULT=NEW_NO_KEY_SA_CREATED_RIGHTS_PASS_WITH_LIMITS
H1B_W1_REASON=SA_UID_READBACK_AND_ACTAS_DELETE_PASS
H1B_W1_CLOUD_RUN_DEPLOY=NOT_ATTEMPTED
H1B_W1_IAM_BINDINGS_AND_KEYS=NONE_CREATED_BY_THIS_SCRIPT
H1B_W1_DO_NOT_REPEAT=TRUE
```

This verifies **ONE ACTUAL new IAM service account creation** (a Cloud resource write). Identity: `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, Google-returned frozen `uniqueId=115445220422157278526`. Script required exact resource GET readback and checked SA-level `iam.serviceAccounts.actAs` and `iam.serviceAccounts.delete` returned. `NO IAM_BINDINGS_AND_KEYS` means W1 did not CREATE user-managed credentials or grant bindings; inherited IAM remains separate (not proof of absence of every role). **Cloud Run deployment has NOT been attempted**, no endpoint tests/public exposure. W1 one-shot marker `/root/.oldx-h1b-w1-new-no-key-sa-create-once-20261126` consumed. DO NOT repeat/remove it, re-create SA, or rerun W0/G1/H1A/G2A/G2B/S1/S2/S3B/C1A.

Already verified remote image by ONE G2B push: `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`; linux/amd64 child `sha256:2e555bd98424d29b32a7bb3409a45e2c257569ff632085e4ff0e3a9ab4413b5f`, config `sha256:c71c7268e08f9ed91a92fd4e82e499a7331c3a071985cebcede7d76efbdf5b71`. **No new image push, scan or rebuild**.

## Current approved boundary

Owner previously approved **one supervised private compiled-OFF, no-real-user-data H1B W1–W6 trial**, same-session new-only guarded cleanup; known 12 HIGH accepted ONLY for this experiment, max 24h activation. Remaining:
- W3: verify exact service name absent immediately before creation, new SA **uniqueId** still matches, use immutable remote image digest for ONE new Cloud Run private service in `oldx-staging/asia-south1` (IAM Invoker check ON, no allUsers/allAuthenticatedUsers, min0/max1, concurrency1, 1CPU/512MiB, timeout5s, port8080, nonroot).
- W4/W5: optional one new-service-only Yasmin Invoker if necessary, max four defined new-only HTTP probes, no Firebase/Firestore/real data/provider calls.
- W6: first prepare/validate SAME-SESSION guarded new-only rollback: exact service/revision UID/IAM/identity checks; delete only service created in W3, then **only if unused and exact UID match** delete the new SA. Existing NEW G2B Registry image can be retained if other-reference verification is incomplete; never delete shared repository or older C1A assets. If mismatch/unknown permissions, STOP_MANUAL_RECOVERY; cleanup never assumed automatic.

One new SA presently exists until confirmed cleanup. DO NOT create a new service before the guarded W3–W6 script, rights and cleanup readiness are prepared. No production/H2/Firebase Rules activation, old `oldx-owner-read` and C1A leftovers untouched. W3–W6 not yet executed at this screenshot.

**Status:** `W1=ACTUAL_PASS_UID_115445220422157278526_CONSUMED`; `W2_G2B=ACTUAL_PASS_CONSUMED`; `W3-W6=READY_FOR_PREPARATION_NOT_EXECUTED`; `STEP05=IN_PROGRESS`; `H2/PRODUCTION=NO_GO`.
