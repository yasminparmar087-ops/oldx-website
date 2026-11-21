# OLDX Step04 G2 A7 — dedicated builder identity and minimally scoped access proposal (NO WRITE AUTHORIZATION)

Date: 21 November 2026 after A6 real screenshot (~19:55 IST). Repo `yasminparmar087-ops/oldx-website`; branch `security-hardening-review`; project `oldx-staging`.

## 0. Consumed source of truth

- A6 owner-run one-read result: `G2_A6_DEDICATED_BUILDER_ID=NOT_PRESENT`, `G2_A6_OTHER_ACCOUNT_IAM=NOT_EVALUATED`, `G2_A6_COMPUTE_DEFAULT_PERMISSIONS=NOT_CHECKED`, `G2_A6_CLOUD_BUILD_JOB=NOT_STARTED`, `G2_A6_CLOUD_WRITES=NONE`, `G2_A6_EXISTENCE_READ=COMPLETE_WITH_LIMITS`. No STOP. [A6 receipt](OLDX_STEP04_G2_A6_DEDICATED_BUILD_SA_EXISTENCE_READ_ONLY_2026-11-21.md) **CONSUMED**, do not repeat inventory for reassurance.
- A5 default Cloud Build SA = `COMPUTE_DEFAULT`, exact effective IAM **NOT CHECKED**. Avoid silently using this project default. Keep runtime `oldx-product-read-staging` SA separate; do not give it build/registry writer roles.
- A2 `cloudbuild.googleapis.com` ENABLED/VERIFIED once; A3 0 v2 connections in `asia-south1`, A4 supported direct public Git URL + future pinned full commit SHA, no GitHub App/connection needed merely to try this future lane.
- No new build was started or signed attestation created; original 1 CRITICAL/5 HIGH frozen severe findings, original builder provenance UNKNOWN, G4 other-DB/Cloud Run invoker still unverified. `STEP04=HOLD`; production `NO_GO`.
- Existing project's **restricted Artifact Registry repository** `projects/oldx-staging/locations/asia-south1/repositories/oldx-staging-images` was previously independently verified; old published image/digest and B1/R1 remain **immutable and consumed**. No default-wide roles or unsafe inherited SA sharing.

## 1. Recommended one bounded identity setup — NOT YET APPROVED

**Create exactly one user-managed service account** `oldx-step04-build@oldx-staging.iam.gserviceaccount.com` (account ID `oldx-step04-build`) *only after fresh exact-existence prewrite guard*. Never create a JSON key, token file, secret, workload identity pool, Cloud Run service, GitHub OAuth connection, Cloud Build trigger or another API under A7. Reuse the separately reviewed original source-only Dockerfile and new future immutable release artifact; **A7 does not authorize any build**.

**Proposed IAM minimum, with actual access checked at mutation time:**

| Target principal | Resource scope | Proposed minimum role | Why | Constraint |
|---|---|---|---|---|
| New builder service account | **only** `oldx-staging/asia-south1/oldx-staging-images` repository | `roles/artifactregistry.writer` | Push **new immutable release image**, use authenticated repository | No project-wide Artifact Registry Writer, no repository delete/admin, no change to previous images |
| Same builder SA | Project `oldx-staging` Cloud Logging service | `roles/logging.logWriter` | User-managed Cloud Build with `options.logging: CLOUD_LOGGING_ONLY` | This IAM role is project-scoped; it can write logs broadly, so log retention/cost and build-specific traffic require separate operator review; no log admin/config writer |
| Owner `yasminparmar087@gmail.com` | **only** the new builder SA resource | `roles/iam.serviceAccountUser` **only if absent** | `iam.serviceAccounts.actAs` for a later separately approved manual Cloud Build submission | No project-wide `serviceAccountUser`; no grants to former owner; no Token Creator blanket grants |

**Do not manually add Cloud Build Service Agent or Token Creator roles without verifying an exact missing permission.** Google says the Cloud Build service agent normally has `iam.serviceAccounts.getAccessToken` through `roles/cloudbuild.serviceAgent` in the same project. A7 does **not** authorize granting this broad service-agent role to any human or ordinary builder. A future user-managed SA build must set `serviceAccount` explicitly and store logs in Cloud Logging (`CLOUD_LOGGING_ONLY`) or an approved user-owned bucket, not Google's Cloud-owned default bucket.

## 2. Mandatory fail-closed checks before a future write

A single **staged, owner-supervised** creation/grant script, prepared only after owner's exact approval, must:

1. Confirm active `oldx-staging`, owner `yasminparmar087@gmail.com`, target account ID and no existing account; halt if name occupied or source state ambiguous. The already consumed A6 list proves only earlier absence; one fresh exact prewrite guard is permitted, not a generic IAM rerun.
2. Confirm exact existing **repository name/location** from the frozen previous evidence and use **repository-level** IAM update. Do not rewrite/mutate any existing policy bindings except the exact intended additive member+role. Verify current policy preimage once if required by Google API; no widening any old principal.
3. Create the SA once, no keys, confirm identity matches expected. If the create fails or returns uncertain result, **STOP, no automatic retry**, and inspect actual state before any further change.
4. Verify each proposed role binding and only add when absent, using least scope. Since each policy binding is a separate change, **a partial failure leaves partial setup**, not permission for unattended rollback/retry. Document actual receipts after each operation. Do not grant `roles/editor`, `roles/owner`, `roles/artifactregistry.admin` or project-wide `roles/artifactregistry.writer`.
5. Return `A7_ACCOUNT_CREATED_WITH_SCOPED_ROLES` *only* when exact identity and all approved bindings are verified; otherwise `A7_INCOMPLETE_STOP_MANUAL_RECONCILIATION`. No image, scanner, build, Cloud Run, GitHub trigger or runtime activation under A7.

**One new build still requires separate owner authorization after A7** for exact Git SHA/source provenance, `images` plus `requestedVerifyOption: VERIFIED`, one unique private output, bounded machine/disk/run time, logs retention/charges, source sanitization and the new image's focused scan/runtime review. The Cloud Build API enable did **not** grant build execution permission. A restricted builder SA cannot itself prove trusted provenance or remove 1 CRITICAL/5 HIGH.

## 3. Cost and scope

Google IAM service account/role setup does not launch a billable Cloud Build job. Nevertheless this is a **security-affecting live IAM mutation**; future builds, registry storage, Cloud Logging and scanning could incur charges, with no proven provider-wide ₹2,000 hard ceiling. Do not infer that free-tier Cloud Build minutes cover Registry/Logging. No spend or billing settings change under this plan.

## 4. Specific owner decision still REQUIRED

Ask for one exact consent: **“Approve creation of only `oldx-step04-build` on `oldx-staging`, Artifact Registry Writer only on `oldx-staging-images`, Logs Writer on staging project for Cloud Logging, and Service Account User only for Yasmin on this exact new builder SA (only if missing); no keys, no build, no deployment, no other IAM changes?”** If consent is not explicit, leave A7 `DESIGN_ONLY_NOT_APPROVED` and continue only source review. Do not treat generic `ok aagal vadho` as IAM consent without scope.

## Verified current sources (21 Nov 2026)

- Google [Run builds with a user-managed service account](https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts): user-provided SA, `iam.serviceAccounts.actAs`, same-project Cloud Build service agent token, Cloud Logging Writer, log destination constraint.
- Google [Connect to Cloud Build from Artifact Registry](https://docs.cloud.google.com/artifact-registry/docs/configure-cloud-build): new builder needs Artifact Registry writer scoped to target repository.
- Google [Cloud Build submit](https://docs.cloud.google.com/sdk/gcloud/reference/builds/submit) and [Build provenance](https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance).
- Google [IAM service accounts CLI](https://docs.cloud.google.com/sdk/gcloud/reference/iam/service-accounts).

**Checkpoint:** `A6=COMPLETE_NOT_PRESENT`, `A7=DESIGN_ONLY_NOT_APPROVED`, `A7_CLOUD_WRITES=NONE`, `G2_TRUSTED_BUILDER=UNKNOWN`, `G2_CVE_1_CRITICAL_5_HIGH=OPEN`, `STEP04=HOLD`, `PRODUCTION=NO_GO`.
