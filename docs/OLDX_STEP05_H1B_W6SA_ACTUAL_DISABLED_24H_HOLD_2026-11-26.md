# OLDX Step05 — ACTUAL W6SA disabled, new test SA on 24-hour observation (26 Nov 2026)

**Canonical latest checkpoint** for `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Source is the real owner WSL terminal screenshot at approximately 22:14 IST on 26 Nov 2026. The assistant reviewed the supplied screenshot and original pinned script; it did not execute Owner WSL/Google Cloud operations independently.

## Exact actual owner output, W6SA (verbatim)
```text
H1B_W6SA_STAGE=ONE_EXACT_NEW_SA_REVERSIBLE_DISABLE
H1B_W6SA_SA_UID=115445220422157278526
H1B_W6SA_RUN_SERVICE=ABSENT_404_AT_PREFLIGHT
H1B_W6SA_SA_DISABLE_ATTEMPTED=TRUE
H1B_W6SA_RESULT=PASS_EXACT_NEW_SA_DISABLED_UID_VERIFIED_24H_HOLD
H1B_W6SA_REASON=EXACT_UID_DISABLED_READBACK_CONFIRMED
H1B_W6SA_DISABLED_AT_UTC=2026-11-26T16:44:17.346536+00:00
H1B_W6SA_SA_DELETED=FALSE
H1B_W6SA_CLOUD_RUN_AND_REGISTRY_WRITES=NONE
H1B_W6SA_DO_NOT_REPEAT=TRUE
```

This is one **actual Google IAM resource write** to **disable, NOT delete**, only the NEW test service account `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, immutable numeric UID `115445220422157278526`. Script read back exact UID+email and `disabled=true` after the disable call. Its original new Cloud Run service `oldx-c2-website-mediator` returned 404 during preflight, consistent with previous exact UID/etag-guarded deletion confirmed at W3–W6. No Cloud Run creation, hosted re-probes, Registry image push or Registry delete happened in this W6SA step. This **does not** establish universal dependency-free status or permanent SA deletion.

Operator-executed W6SA source, previously pinned commit `3fbf984a5601a7d92055ecb1e5aab42cc35e9ca9`, Git blob `5d7dd786af6d2acd804afcdf328bbd78e3042a8a`:
`scripts/step05_h1b_w6sa_disable_new_uid_once_20261126.py`.
One-shot marker `/root/.oldx-h1b-w6sa-exact-new-sa-disable-once-20261126` is **CONSUMED**. **DO NOT REPEAT**, delete marker, re-disable, re-enable without new necessity, re-create a deleted Cloud Run service, re-run old W3–W6/HTTP tests, W3V, W1, W0, G2A/B, G1, H1A image build/scan or old C1A checks. Keep all private local evidence/markers and unchanged shared Registry/older cloud resources.

## Exact bounded observation window

- Disabled at `2026-11-26T16:44:17.346536+00:00` = **26 Nov 2026 22:14:17 IST**.
- **Earliest review AFTER at least 24h:** `2026-11-27T16:44:17.346536+00:00` = **27 Nov 2026 22:14:17 IST**. This is a lower-bound review time, **not permission to automatically delete**.
- Google IAM recommends first disabling an SA and waiting at least 24h to detect unexpected dependencies before deleting: https://docs.cloud.google.com/iam/docs/service-accounts-disable-enable ; https://docs.cloud.google.com/iam/docs/service-accounts-delete-undelete .
- After the observation window, only a **new and separately documented UID-bound dependency/use check and guarded deletion decision**; if references/errors unknown, keep disabled. No automatic background deletion/undeclared scheduled action, and don't promise universal dependency scan.
- OLDX feature/source-only work or other separately approved, independent work may continue in parallel; no indefinite waiting for Step05 development.

## Retained resources and frozen successes

| Item | Actual state after this owner result | No-repeat boundary |
|---|---|---|
| ONE H1B private Cloud Run service `oldx-c2-website-mediator`, UID `83d724b3-fcf0-4607-8107-f111a2eacc31` | W3–W6 owner script reported **private four-probe PASS** (anonymous 403, owner 200, OFF owner API 503, unmatched 404), exact UID/etag/session-guarded delete completed; W6SA separately observed exact service GET 404 | Never re-create, re-probe or delete again |
| ONE H1B test Service Account `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, UID `115445220422157278526` | **DISABLED, readback confirmed**, NOT DELETED | Do not re-disable/delete immediately, 24h observation then dependency guard |
| Frozen new H1B Registry image | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e` retained | No rebuild/rescan/push/automatic delete, no sharing destructive Registry command |
| Old C1A residual service account/image | Separately retained; references not fully known, NOT part of this cleanup | Do NOT touch under H1B consent |
| Firestore/Firebase Rules/KMS/H2/production | Unchanged by H1B W6SA | No launch inference; H2 and production remain NO-GO |

## Interpretation and next plan

**The bounded H1B IAM-private compiled-OFF experiment passed with documented limits:** one frozen remote image, one new no-key SA, one private service creation, expected four HTTP statuses, exact service deletion, and reversible SA disable/readback. This does **not** mean all Step05/15 gates or website deployment are complete. Known 12 HIGH CVEs were risk-accepted for this strictly private OFF/no-real-data experiment only, NOT for H2 or production.

For speed: treat the H1B one-session execution and safe reversible closeout as accomplished; do not repeat or block unrelated Step05 source work during the observation period. Next genuinely new actions: (a) record this owner receipt in canonical handoff, (b) pursue independent Step05 source-only or separately approved future stage without reworking G1/G2/W0/W1/W3, (c) review **this exact disabled SA** only on/after 27 Nov 2026 22:14:17 IST for dependencies and separate guarded permanent-deletion decision. If no evidence of dependencies cannot be established, leave SA disabled and document residual rather than deleting by guess.

**Status:** `H1B_W3-W6_TEST=ACTUAL_PASS`; `H1B_CLOUD_RUN_SERVICE=DELETED_CONFIRMED`; `H1B_NEW_SA=ACTUAL_DISABLED_UID_VERIFIED_24H_HOLD`; `H1B_REGISTRY_IMAGE=RETAINED`; `SA_PERMANENT_DELETE=NOT_DONE`; `STEP05=IN_PROGRESS`; `H2/PRODUCTION=NO_GO`.
