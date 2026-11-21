## UPDATE 21 Nov 2026 ~20:27 IST — S3 RECONCILED; NO REPEAT

Owner's actual single targeted read-only PowerShell screenshot returned:

```text
S3_UNCONDITIONAL_COUNT=1
S3_CONDITIONAL_COUNT=0
S3=PRESENT_VERIFIED_AFTER_STOP
S3_NO_WRITE_PERFORMED
S3_WRITE_RETRY=PROHIBITED
```

**Verified:** the exact builder principal `serviceAccount:oldx-step04-build@oldx-staging.iam.gserviceaccount.com` currently has one direct **unconditional** `roles/logging.logWriter` binding on project `oldx-staging`. This last reconciliation issued no writes. The earlier S3 mutation may have succeeded before the ambiguous PowerShell exception, but actor/timing and preservation of every unrelated project IAM binding are **not independently proven**. Mark `A7_S3=COMPLETE_WITH_LIMITS_CONSUMED`. NEVER replay S3 grant or reconciling read. S1/S2 also consumed.

**Next distinct A7 S4**, already approved only if needed: determine whether owner `yasminparmar087@gmail.com` already effectively has `iam.serviceAccounts.actAs` on only the dedicated builder SA. The **Project Owner** role typically includes this permission; avoid duplicating resource-level IAM bindings if existing effective permission passes. The one authorized live operator action is a **read-only** `projects.serviceAccounts.testIamPermissions` request as owner for exactly `iam.serviceAccounts.actAs`, using a local token that is never printed. It is a POST but does not modify IAM. If granted, S4 is no-write satisfied with limits; if missing/unknown, STOP and plan a separately guarded SA-resource-only binding under existing A7 consent (no blind grant). See [S4 exact read-only preparation](OLDX_STEP04_G2_A7_S4_EFFECTIVE_ACTAS_READ_ONLY_2026-11-21.md). No Cloud Build, Registry, Cloud Run, Firebase, billing or production action. G2 original scan and origin, G4 and G8 gates remain OPEN; Step04 HOLD / PRODUCTION NO_GO.

---

# OLDX Step04 G2 A7 S3 STOP reconciliation — 2026-11-21 ~20:22 IST

Owner's actual PowerShell screenshot from Task 22 (Task 21 S3 command result):
```
G2_A7_S3_PREIMAGE=TARGET_LOGGING_WRITER_ABSENT
STOP_G2_A7_S3_NO_AUTOMATIC_RETRY
STAGE=WRITE
REASON=S3_UNEXPECTED_ERROR
G2_A7_S3_CONFIRM_LIVE_PROJECT_IAM_BEFORE_ANY_NEW_WRITE
```
A fresh pre-write project IAM read saw no direct builder roles/logging.logWriter. The WRITE-stage PowerShell exception is ambiguous: a Google IAM mutation may have succeeded before the exception. No exit-zero or post-policy delta proof. **Never rerun the S3 grant.** S4 is blocked until a one-time independent, targeted READ-ONLY project IAM reconciliation. Preserve S1 account verified, S2 exact repo writer present with limits, and all consumed A1–A6/C1–C5/B1/R1/G4/CI/Grype. Existing A7 scope approval remains; no new approval needed for already authorized A7 actions. No new Cloud Build, Registry upload, Cloud Run, Firebase, production or other IAM mutation is authorized.

## Next exact action
Run ONE owner PowerShell `gcloud.cmd projects get-iam-policy oldx-staging --account=yasminparmar087@gmail.com --format=json --quiet` read. Locally count direct `roles/logging.logWriter` membership for `serviceAccount:oldx-step04-build@oldx-staging.iam.gserviceaccount.com` split by conditional/unconditional. Print only counts and outcome, no raw policy. If 1 unconditional and 0 conditional, mark current grant PRESENT_WITH_LIMITS, no write; unrelated project bindings were not independently shown unchanged. If both zero, grant ABSENT_AT_READ only; do not auto-retry or infer previous write never happened. Multiple/conditional/error => STOP manual review. No S4 until reconciled. STEP04 HOLD and production NO_GO remain.
