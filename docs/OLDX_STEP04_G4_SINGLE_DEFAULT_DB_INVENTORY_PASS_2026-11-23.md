# OLDX Step 04 — G4 actual inventory 1 default DB, 0 other DB; decision gate without test DB creation

**Observed on 23 Nov 2026 ~22:21 IST, owner Google Cloud Shell, project `oldx-staging`.** The user ran the distinct read-only `gcloud firestore databases list --project=oldx-staging --account=yasminparmar087@gmail.com --format=json` with checked JSON shape. The result screenshot contains:

```text
G4_EXISTING_DATABASE_INVENTORY=READ_ONLY_PASS
G4_DATABASE_COUNT=1
G4_DEFAULT_DB_PRESENT=True
G4_OTHER_DATABASE_COUNT=0
G4_EFFECTIVE_OTHER_DB_ACCESS_DENIAL=UNVERIFIED
G4_NEW_DATABASE_CREATED=NO
G4_IAM_FIRESTORE_WRITES=NONE
A8_BUILD_SCAN_SLSA_RUNTIME_RERUN=NONE
```

**Meaning:** At this inventory time, there was exactly one Firestore database `(default)` and **zero other existing database targets** in `oldx-staging`. The test was done under the owner account and says nothing about the runtime service account's effective ability to access any hypothetical **future** Firestore database. No new DB shall be created only to manufacture a negative test without separate authorization. This inventory is **COMPLETE**, do not repeat solely for another PASS. The output does not prove other-DB denial.

## Reuse already consumed security evidence, do not rerun

- The corrected one-time 21-Nov Cloud Asset `analyze-iam-policy` returned 1 allow binding for the selected `oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com` and 4 Firestore entity permissions GET/CREATE/UPDATE/DELETE; exact IAM condition `resource.name == "projects/oldx-staging/databases/(default)"`. It had 0 unconditional and 0 other-conditioned matches **in that selected query only**. Scope is allow-policy snapshot, not full effective other-DB negative denial, IAM deny/PAB or exhaustive invoker access.
- Source `functions/staging-marketplace/runtime.mjs` and exact immutable A8 pinned new image fail closed on nonmatching project/default-DB and require two explicit flags to activate the Product API. One actual no-network Docker runtime on the **NEW image** has PASSED nonroot, read-only rootfs, `/healthz=200`, disabled owner API `503`. This proves local default-OFF runtime under one test configuration, not hosted enabled Firebase access.
- Historical default-DB synthetic one-doc positive create/verify/update and negative delete `403` were observed and closed, don't repeat for this checkpoint.
- Historical B1 single *private, 0%-main, default-OFF* Cloud Run revision `oldx-owner-read-00010-zud` was deployed and R1 only removed its tag, with original `oldx-owner-read-00001-8kr` at 100% main and previous tags preserved; R2 no-op. **Do not deploy, retag or repeat B1/R1.**
- Earlier project IAM metadata had 2 Owners, 1 Editor and one direct service invoker; exclusive effective Cloud Run invocation remains NOT PROVEN. No parent reported by project metadata, not a blanket negative IAM assertion.
- G2 new-image Grype exactly one immutable digest scan complete: 46 package-CVE matches (1 CRITICAL, 23 HIGH, 19 MEDIUM, 3 LOW), 15 distinct severe IDs. Seven BellSoft fixed-version candidates have PURL `bellsoft-hardened-containers` in scanner metadata; some disputed/conditional CVEs remain **not blanket cleared**. Source-only reachability audit and signed source/subject/builder provenance done; no reruns.
- G8 had narrowly accepted residual cost risk for **consumed single OFF-only B1 trial**, but NOT an all-provider hard ₹2,000 stop, enabled API, or future production acceptance. Cloud Run spend caps do not cover Firestore/Artifact Registry/general costs; alerts alone are not hard stops.

## Decision recommendation — no artificial blocker-busting test

**G4 existing DB inventory = COMPLETE**, and prior default-DB IAM allow-policy inventory = PASS WITH LIMITS. **G4 actual other-DB negative denial = UNVERIFIED / NOT CURRENTLY TESTABLE ON EXISTING RESOURCE**, because no other DB exists. Do not call that denial PASS, but do not create a disposable DB merely to say Step04 is "100%". If additional DB is introduced in future, it is a *new security event* requiring a distinct targeted effective permission check before enabling Product API against it.

**G4 default-OFF staging risk containment:** already supported with limits by exact-new-image local sandbox 503, limited allow-policy condition and historic B1/R1 receipts. No further staging action warranted at this point just for this inventory.

**Enabled API / public launch separate gate:** Keep **HOLD** pending a defined effective invoker/IAM and Firestore resource scope, dynamic authorization/integration testing in an approved environment, treatment or expressly authorized residual exposure for 15 unique severe CVE IDs, measurable cost/rollback controls and explicit owner GO. An owner can choose a documented risk-accepted launch later; that is not the same as claiming all CVEs or G4/G8 become technical PASS. This decision must not silently expand historic OFF-only consent.

**Next most useful Step04 work without tools or new reads:** consolidate **one explicit Step04 closeout/conditional owner risk-decision packet** with (a) completed proof, (b) technical limits, (c) minimum controls before an enabled trial, (d) exact scope of any risk acceptance, (e) financial limits/rollback. Do not repeat G4 analyzer, current inventory, B1/R1, scan, build, SLSA, IAM reads or old billing checks. If no further live actions are justified, hold the Step04 hosted enabled exit instead of creating more tests.

Official docs (checked 23 Nov 2026):
- https://firebase.google.com/docs/firestore/manage-databases (database-scoped conditional IAM and Console caveat).
- https://firebase.google.com/docs/firestore/security/rules-conditions (server SDK bypasses Firestore Rules).
- https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps (single-project + eligible single-service spend caps).
- https://docs.cloud.google.com/billing/docs/how-to/budgets (alerts-only budgets not stop).

**Exact current labels:** `G4_EXISTING_DATABASE_INVENTORY=COMPLETE_ONE_DEFAULT_ONLY`; `G4_NONDEFAULT_DB_EXISTING=NONE`; `G4_ALLOW_POLICY=ONE_DEFAULT_CONDITIONAL_WITH_LIMITS`; `G4_EFFECTIVE_OTHER_DB_DENIAL=UNVERIFIED`; `G4_INVOCATION_EXCLUSIVITY=NOT_PROVEN`; `G8_PROVIDER_WIDE_HARD_STOP=NOT_PROVEN`; `G2_A8_LOCAL_RUNTIME=PASS_WITH_LIMITS`; `STEP04=HOLD`; `PRODUCTION=NO_GO`.
