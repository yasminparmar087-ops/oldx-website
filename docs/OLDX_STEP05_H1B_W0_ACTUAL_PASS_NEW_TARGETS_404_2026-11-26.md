# OLDX Step05 — W0 actual owner terminal PASS; new SA and service absent (26 November 2026 ~21:47 IST)

Owner supplied real WSL screenshot from `OLDX-Ubuntu-24.04`, root, after executing pinned `scripts/step05_h1b_w0_precreation_target_readonly_once_20261126.py` from commit `0d94be8bf2fb13489e911310ea98303db95c7bca`, Git blob `9239d4774c25233021766a7ea6252134a0152c46`.

## Observed status (verbatim)
```text
H1B_W0_PROJECT=ACTIVE_EXACT
H1B_W0_SERVICE=ABSENT_404_WITH_LIMITS
H1B_W0_NEW_SA=ABSENT_404_WITH_LIMITS
H1B_W0_IMAGE=PRIOR_G2B_REMOTE_DIGEST_FROZEN_NO_REPEAT
H1B_W0_NEW_SA_ACTAS=NOT_YET_TESTABLE
H1B_W0_RESULT=READ_ONLY_NEW_TARGETS_ABSENT_WITH_LIMITS
H1B_W0_REASON=PROJECT_AND_TWO_NEW_EXACT_RESOURCES_CHECKED
H1B_W0_CLOUD_RESOURCE_WRITES=NONE
H1B_W0_DO_NOT_REPEAT=TRUE
```

**Interpretation:** `oldx-staging` identity/lifecycle verified by Resource Manager GET. Exact new Cloud Run service `projects/oldx-staging/locations/asia-south1/services/oldx-c2-website-mediator` and exact new no-key SA `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` were both absent (HTTP 404) when checked. This is point-in-time absence **WITH LIMITS**, not proof of future creation permission, new SA resource-specific `iam.serviceAccounts.actAs`, project-inherited effective permissions, post-create Cloud Run access, or ability to clean up new resources. No Cloud resource mutation. Do NOT rerun W0, G1, G2A/G2B, H1A/S1/S2/S3B or C1A checks. The W0 one-shot marker `/root/.oldx-h1b-w0-new-target-readonly-once-20261126` is CONSUMED, and all historical markers stay untouched.

## Frozen G2B image to reuse (no upload or new build)

Actual one-push PASS recorded separately: `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`. Frozen child `sha256:2e555bd98424d29b32a7bb3409a45e2c257569ff632085e4ff0e3a9ab4413b5f`; config `sha256:c71c7268e08f9ed91a92fd4e82e499a7331c3a071985cebcede7d76efbdf5b71`. Never rebuild, scan or re-push.

## Remaining owner authorization / next safe work

Owner's already recorded "ha manjuri chhe" covers one controlled PRIVATE/OFF/no-real-user-data H1B W1/W3/W4/W5/W6 staging-only session, including one new no-key SA, one new Cloud Run service by immutable image digest, optional Yasmin-only service-level Invoker, max 4 specific private HTTP probes and same-session guarded cleanup of NEW resources. Existing older C1A assets, shared registry, Firebase and production are protected. Known 12 HIGH CVEs only accepted for this bounded private experiment, max 24h after activation.

Next: prepare the exact new-only guarded W1 script and cleanup path BEFORE W1 cloud creation; perform a **fresh exact SA/service collision check immediately before any create**, verify local Owner and delete rights, capture new SA immutable uniqueId on create and test its *resource-level* `iam.serviceAccounts.actAs`/cleanup permission after creation. No access or policy change by the assistant as of this documentation checkpoint.

**Current state:** `H1B_G2B=ACTUAL_PASS`; `W0=ACTUAL_READ_ONLY_NEW_TARGETS_ABSENT_WITH_LIMITS_CONSUMED`; `W1_SA=NOT_CREATED`; `W3_RUN=NOT_DEPLOYED`; `W4/W5/W6=NOT_EXECUTED`; `STEP05=IN_PROGRESS`; `H2/PRODUCTION=NO_GO`.
