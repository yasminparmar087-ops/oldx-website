# OLDX Step05 C1A — Task25 Stage A approved: ONE new read-only evidence checklist

**Date:** 24 November 2026 IST. **Branch:** `security-hardening-review`. **Consent:** owner replied **"ha manjuri chhe"** to combined five-term Stage A decision; see [canonical acceptance](OLDX_STEP05_C1A_FASTPATH_OWNER_DECISION_AND_PROVENANCE_2026-11-24.md). No Google Cloud write, paid action or hosted HTTP has been approved or performed in this Task25 work.

## Consumed; DO NOT REPEAT
- Historical 84 local Node cases, old Step04 A8 build/sign/SBOM/Grype, B1/postwrite/R1, IAM and default DB inventory, actual old A8 Cloud Run 0%-main revision; historical 15 distinct severe IDs.
- NEW Step05 WSL derived OFF Gateway local build `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`, HTTP health200/API503/SIGTERM/nonroot/read-only, Syft/Grype 55 package matches and 12 distinct HIGH CVEs.
- Previous Step05 C1A targeted Cloud Shell project, exact proposed service `NOT_FOUND_REPORTED`, proposed new runtime SA `NOT_FOUND_REPORTED`, Mumbai Registry, billing account LINK, direct project IAM metadata. **No requery of these.**

## Stage A facts confirmed from OFFICIAL PUBLIC documentation in this turn

1. Google's distroless publisher states keyless Cosign certificate identity `keyless@distroless.iam.gserviceaccount.com` and OIDC issuer `https://accounts.google.com`: https://github.com/GoogleContainerTools/distroless#how-do-i-verify-distroless-images. This is policy identification ONLY, not a successful verification of the pinned image.
2. Google Cloud Run documentation says project Owner and Editor roles can invoke Cloud Run resources by default: https://docs.cloud.google.com/run/docs/securing/managing-access. The Owner-based testing path may inherit other invokers and must not be labelled exclusive.
3. Google Cloud Billing Reports show current month by Service, but default report totals may include credits/savings; Cost breakdown report explicitly has a **Usage cost** gross line, and invoice-level taxes can appear only for invoiced billing periods, not current Usage/Charge-period snapshots. References:
   - https://docs.cloud.google.com/billing/docs/how-to/reports
   - https://docs.cloud.google.com/billing/docs/how-to/cost-breakdown
4. Gross C1A risk ceiling agreed by owner is **₹100 incremental C1A manual review/STOP trigger**, NOT an enforced platform cap. Existing ₹1,000 monthly owner manual-review threshold and ₹2,000 non-guaranteed goal unchanged. Future upload/Cloud Run execution not permitted just because billing-link status had been enabled.

## New metadata ONLY: exact missing information and evidence route

### A. Actual current gross charges / region prices (user must read privately in own Cloud console; NOT obtained)

Open **Google Cloud Console → Billing → Reports** with `oldx-staging` selected, this current month, select that project, all Services. If gross before credits is not visible in Reports, use **Billing → Cost breakdown** and record **Usage cost**; do NOT record the net credit-reduced bill as gross. Note screen date/currency, covered time period, freshness/reporting lag if displayed. The current-month chart may not include taxes not yet invoiced; mark `TAX_PENDING=YES/UNKNOWN` rather than guessing. For account-specific regional charges, use **Billing → Pricing / Pricing table** (or approved public pricing reference) for Cloud Run request-based CPU/memory and Artifact Registry Mumbai `asia-south1`, noting data transfer/storage/logging and any additional charges. Only read; do NOT enable Billing export/BigQuery (would create paid resources), configure alerts, change credits or switch billing accounts.

Minimal private receipt (DO NOT share account IDs, emails, keys, or payment details):
```
PROJECT=oldx-staging
AS_OF_IST=<date time>
BILLING_CURRENCY=INR_OR_OTHER
GROSS_USAGE_THIS_MONTH_BEFORE_CREDITS=<observed amount or UNKNOWN>
TAX_AND_UNPOSTED_CHARGES=<amount or UNKNOWN>
PRICING_CLOUD_RUN_ASIA_SOUTH1=<confirmed reference or UNKNOWN>
PRICING_ARTIFACT_REGISTRY_ASIA_SOUTH1=<confirmed reference or UNKNOWN>
LAG_AND_REMAINING_TRIAL_CREDIT=<observed or UNKNOWN>
```

### B. NEW publisher keyless signature — prepared, NOT executed

Single-try no-install/read-only script: [step05-c1a-stage-a-cosign-parent-once-20261124.sh](../scripts/step05-c1a-stage-a-cosign-parent-once-20261124.sh).
- Works from an existing clean `security-hardening-review` checkout with **already installed** `cosign`. No Docker, Syft, Grype, billing, IAM or Cloud Run command.
- Reuses historical immutable index-to-amd64-child mapping and exact reviewed Dockerfile base pin, without repeating metadata index fetch. Checks only the previously unverified **publisher keyless signature on immutable parent index** `sha256:39b0407357c9fadf1a9708d22088f02de21f0e1e8a688474eea2d8701e7d5693`, with required issuer and identity; never checks a mutable tag.
- Marker before network call prevents blind repeat. If `cosign` missing, signature remains UNVERIFIED and script stops without installing tools. If verify fails, STOP and keep report, no automatic retries.
- A verified signed base parent does NOT imply the locally DERIVED Gateway image is signed/attested or equals an as-yet nonexistent remote Artifact Registry manifest digest. Keep the latter UNKNOWN pending Stage B authorized immutable upload/receipt.

### C. Required decision before Stage B

Reconcile actual observed gross + lag/taxes plus pricing and one-off new image storage/creation/24h resource envelope against ₹100 manual threshold; if unknown or exceeded, STOP. Verify the signed publisher result (or preserve explicit blocker), exact immutable local source/evidence and resource-time bounds. Recheck exact proposed new name collisions and effective deployer actAs permissions only **as part of an independently approved Stage B prewrite**; never rerun old full audits. Obtain one **distinct exact write consent** for up to (1) new no-role runtime SA, (2) one approved derived image pushed to existing registry, (3) one new OFF-only private Cloud Run service, preserving existing backend. Separate explicit C1B hosted request and cleanup authorizations required as scoped by owner packet.

## Current truth
`STAGE_A_OWNER_CONSENT=APPROVED`; `NEW_GROSS_INR_REPORT=NOT_RETURNED`; `PUBLISHER_COSIGN_RESULT=NOT_EXECUTED`; `DERIVED_REMOTE_MANIFEST=NONE`; `C1A_STAGE_B_WRITES=NOT_APPROVED`; `C1B/C2=NOT_APPROVED`; `STEP04_TECHNICAL_HOLD=CARRIED`; `PRODUCTION=NO_GO`.

This checklist is reusable for the NEXT chat. No test, build, scan, Cloud API, payer-account action or provider write was performed when creating it.
