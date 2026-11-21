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
