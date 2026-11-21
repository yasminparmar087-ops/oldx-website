# OLDX Step 04 G2 — A1 observed Cloud Build API OFF; next minimum owner decision

Date: 21 November 2026, ~19:14 IST (owner Windows PowerShell screenshot). Branch: `security-hardening-review`; staging project: `oldx-staging`. Evidence is the **owner-shared actual terminal output**, not a purported direct GCP read by ChatGPT.

## A1 read-only result — verified from owner screenshot; CONSUMED

```text
G2_CLOUD_BUILD_API=NOT_ENABLED
G2_BUILD_PREFLIGHT=STOP_NO_API_ACTIVATION
G2_CLOUD_WRITES=NONE
PS C:\Users\Yasmin Parmar>
```

- The previously prepared guarded A1 script successfully got an enabled-services list for project `oldx-staging`, found **no `cloudbuild.googleapis.com` entry**, and deliberately returned before connection discovery.
- Thus `G2_CLOUD_BUILD_API=DISABLED_AT_A1`; `G2_GITHUB_CONNECTION_ASIA_SOUTH1=NOT_CHECKED`; `G2_BUILDER_SERVICE_ACCOUNT=NOT_CHECKED`; `G2_BUILD_SUBMISSION=NOT_STARTED`; `G2_CLOUD_WRITES=NONE`. There is **NO evidence of a connection failure** because `builds connections list` was never called.
- Do not rerun A1, enable Cloud Build API via a side path, create IAM roles, grant service accounts, or submit a build under generic 'continue' approval.
- This outcome is an expected fail-closed prerequisite, not evidence that G2 CVEs or previous B1/R1 became unsafe.

## Two possible future routes, evaluated against the existing project

### Route A — ONE separately approved Cloud Build API enable (preferred continuity, not approved)

Official setup requires enabling `cloudbuild.googleapis.com`, which is a **project configuration mutation** that requires `serviceusage.services.enable`. Enabling the API **does not itself submit a build** or promise zero provider charges; Cloud Build execution, registry storage, logs and source connector remain separate cost and permission decisions. Once explicitly approved, enable only that single API in `oldx-staging` as Yasmin (no extra APIs or grants). Verify its enabled status **once**; then check the single region-specific GitHub connection previously skipped, and stop if unavailable. Do not infer a connection exists; if absent, separately design narrow external GitHub linkage, dedicated builder identity and log handling; do not use default broad service identities silently.

**Why favored:** Existing OLDX has private Artifact Registry staging image and a Cloud Run runtime in `asia-south1`, and its source-only route already selected Cloud Build for independently observed *future* source-to-image provenance. It preserves single-provider image custody and avoids making GitHub Packages a new artifact transport. It still requires separately approved *new* one-shot build, verified builder statement, pinned SHA/base digests, new-image-only scanner/runtime acceptance, and no automatic deployment.

**An API enable approval here authorizes only `gcloud services enable cloudbuild.googleapis.com --project=oldx-staging --account=yasminparmar087@gmail.com` ONCE and one scoped post-enable read**. It does NOT authorize a GitHub connection, Cloud Build submit, Artifact Registry write, IAM/SA edit, Source Repo, billing/cap changes, secret creation, live Firebase, Cloud Run, main routing, or production.

### Route B — public-repository GitHub Actions artifact attestation (credible fallback, not activated)

GitHub REST repository metadata inspected from owner GitHub connection: `yasminparmar087-ops/oldx-website` is **`private=false`, `visibility=public`** on 21 Nov. GitHub's official documentation says artifact attestations on Free/Pro/Team plans are available for **public** repositories, and the standard hosted runners are **free and unlimited for public repo use**. So the GitHub public-repo attestation capability is an actual candidate that **does not require the Cloud Build API**.

However the existing `.github/workflows/oldx-step04-npm-free-source.yml` is source-only; it **does not** build/sign/register an image; `oldx-step04-distroless-one-shot.yml` was consumed and hard-disabled. A new manually invoked, owner-approved trusted GitHub Actions build workflow would need to bind the approved source commit and OCI output digest, verify the cryptographic attestation, avoid any automatic deploy, and establish an approved *private* GHCR/Artifact Registry path plus keyless identity/permissions. Direct Registry upload to Google would require a separately approved secure federated credential path; a GHCR-only image would require an additional approved import/publish path before use in the existing Google Cloud Run environment. No token, IAM, workflow edit, package registry, builder or disk budget is approved.

**Capacity caution:** GitHub's standard Linux runner is described with a **14 GB total** disk, not guaranteed 14 GiB **free scratch**. OLDX's earlier conservative peak **14 GiB shared scratch** for combined BuildKit + Grype + image import is larger than that total: do not reenable an old workflow or presume source-only job can successfully perform new build-plus-scan. Splitting jobs, lowering build footprint, or preflight just the relevant disk budget would require its own deliberate design. Also `free runner` does not mean GHCR/private package transfer/storage or the new artifact assessment is necessarily free.

**Decision:** Hold B as fallback if owner does not approve Route A or if A's permissions/cost exceed limits; neither route gets a build approval today.

## Final next-action checkpoint

- **Completed and never rerun:** old C1–C5/OCI Grype/cosign, B1 default-OFF one-shot Cloud Run deployment, R1 tag cleanup, old G4 Firestore one-doc plus corrected Cloud Asset allow-policy query. Original 100%-main and tags last verified preserved at R1. Existing G2 daily Security Watch monitors official CVE evidence; do not create a duplicate.
- **A1=COMPLETE_STOP_API_DISABLED**, **GITHUB_CONNECTION=NOT_CHECKED**, **BUILD_ACCOUNT=NOT_CHECKED**, **NEW_IMAGE=NOT_BUILT**, **G2_CVE_1_CRITICAL_5_HIGH=OPEN**, **ORIGINAL_BUILDER_SLSA=UNKNOWN**, **G4_EFFECTIVE_OTHER_DB_DENY=UNVERIFIED**, **STEP04=HOLD**, **PRODUCTION=NO_GO**.
- **NEXT operator decision (not an automatic action):** Ask Yasmin explicitly whether she approves *only* enabling `cloudbuild.googleapis.com` on `oldx-staging`, without starting any build or changing IAM/billing/deployment. If YES, issue one narrowly guarded enable command and one minimal verification under her direct control. If NO, continue source-only Route B feasibility and owner-approval gate preparation; do not repeat consumed A1.

Official current sources used:
- https://docs.cloud.google.com/build/docs/set-up
- https://docs.cloud.google.com/service-usage/docs/reference/rest/v1/services/enable
- https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts
- https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- https://docs.docker.com/build/metadata/attestations/
- https://cloud.google.com/build/pricing

**No GCP command, build or security test was executed by the author while creating this source-only GitHub checkpoint.**
