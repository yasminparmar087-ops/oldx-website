# OLDX Step 04 G2 A8 — ONE source-pinned trusted Cloud Build candidate / owner decision

Date: 22 November 2026. **SOURCE-ONLY PREPARED, NO CLOUD BUILD SUBMITTED, NO OWNER APPROVAL FOR A8 YET.** Branch `security-hardening-review`; repo `yasminparmar087-ops/oldx-website`.

## 1. Why this distinct step is needed; reused evidence
- A7 S1–S4 is **COMPLETE_WITH_EVIDENCE_LIMITS / CONSUMED**: dedicated keyless builder account `oldx-step04-build@oldx-staging.iam.gserviceaccount.com` exists; exact repository `roles/artifactregistry.writer` direct unconditional exists; project `roles/logging.logWriter` direct unconditional exists; owner Yasmin's `iam.serviceAccounts.actAs` was effectively VERIFIED via one real `testIamPermissions` without any new role grant. NEVER rerun S1–S4.
- A2 Cloud Build API ENABLED already; A3 0 v2 GitHub connections in `asia-south1` consumed; A4 public direct GitSource with full Git SHA is a documented candidate; A5 default account category Compute default is consumed, **never use it as silent fallback**. No new GitHub OAuth/trigger/connection.
- Local `oldx-bellsoft-npmfree:20261120-a1`, from SHA `fcc96574b6388dc441a0b5d3eade48e79c7ebb24`, has already completed ONE isolated owner-local runtime and Grype assessment: **1 CRITICAL + 5 HIGH + 12 MEDIUM + 2 LOW**; local image is NOT a published private Registry image and lacks independently trusted builder/source provenance. Keep both local and old private deployed digest distinct.
- GitHub `compare_commits(fcc965... => 0354b855...)`: 272 later commits, 67 changed paths, but only **one existing runtime Docker COPY input differs**: `scripts/staging-marketplace-context.mjs` line16 now requires `adminFirestore.databaseId==='(default)'` when not emulator. Earlier local image/runtime PASS cannot be transferred to this **different** source. Dockerfile, `package.json`, `package-lock.json`, and all other Docker COPY input files unchanged in that bounded comparison.
- Do NOT rerun the old local build, old Grype, old C1–C5, old B1/R1, G4 one-doc/Analyzer, A1–A7 or broad CI/billing solely to cross a checkpoint.

## 2. Proposed A8 precise frozen source and configuration
**Immutable GitSource source SHA (not moving branch name):**
```text
31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71
```
The SHA is the commit that added the following inert config. A later docs-only commit will not alter its source. Before future single execution, only check whether this exact 40-hex commit is accessible and config matches; do not substitute HEAD/main/latest or recalculate an owner approval to a different SHA.

- Git remote: `https://github.com/yasminparmar087-ops/oldx-website` (known public at source review; actual Cloud Build fetch not yet attempted).
- Cloud Build YAML: `cloudbuild.step04-g2-npmfree-one-shot.yaml`, pinned at the **same SHA**, Git blob SHA `8518c2b6607e2ea4b867e4cf410d449de82aea1b`. It is **NOT executable automatically** and deliberately has no default `_IMAGE` substitution.
- Dockerfile: `Dockerfile.product-read.bellsoft-npm-free`, Git blob `c833e8372324cbdf80f6497bf3968ac421cadfc4`, uses digest-pinned `node:24-bookworm-slim@sha256:dc26ae92...` and `bellsoft/hardened-nodejs@sha256:ef00ba8e...`. Only `linux/amd64`. Existing Dockerfile-specific allowlist `Dockerfile.product-read.bellsoft-npm-free.dockerignore` blob `c70b39451363a89f81c99738c60bd2c5b92621f0`. `package-lock.json` blob `26b039f82887ff63ccdd2e163b68d5bf5d6726db`.
- New runtime `scripts/staging-marketplace-context.mjs` blob `614dd6124a7d6673c655823c37da21e859410989` includes a later default-DB fail-closed guard. **The new source requires a focused post-build runtime check**; prior fcc965 local runtime PASS not inherited.
- Build context Dockerfile explicitly chosen, no generated `Dockerfile` default, no registry upload via separate push step. YAML `images: ['${_IMAGE}']` drives output/push and provenance. `options.requestedVerifyOption: VERIFIED` asks for attestations but **a build success alone is not independent source/builder verification**.

### Proposed one brand-new private output, only if independently approved
```text
asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1:one-shot
```
This is a **proposed future name, NOT an existing artifact**. Before write, require absence of this exact image/package to avoid overwriting anything, and one checked source/config digest. After a successful push, identify by its resolved immutable `@sha256:` digest, never deploy or attest by tag alone. No update of `oldx-owner-read` or old image/tag.

### Proposed one-shot runtime/cost limits (planning safeguards, not a hard billing cap)
- Project `oldx-staging`; region `asia-south1`; **dedicated builder** `projects/oldx-staging/serviceAccounts/oldx-step04-build@oldx-staging.iam.gserviceaccount.com`; `CLOUD_LOGGING_ONLY`; no GCS logs bucket or custom pool; no default Compute builder.
- `E2_STANDARD_2` default pool (2 vCPU, 8 GiB RAM), 100 GB worker SSD, 20-minute build timeout, 10-minute queue TTL, one manual attempt, **NO retries** and NO trigger; one private tagged registry output; no Cloud Run deployment, Auth/Firestore/Rules/IAM/billing mutation.
- Google's published default-pool e2-standard-2 list price: **US$0.006 per build-minute**; at maximum 20 charged build minutes approx **US$0.12** before any available free allowance. Published promotional **2,500 free e2-standard-2 minutes / billing account / month**, availability/remaining quota NOT independently checked. First 100GB worker SSD included, but external network egress, Registry bytes, build logs, scans, provider taxes and persistent storage can still charge; **no verified rupee maximum or all-provider hard STOP**. Propose **₹100 incremental gross planning guard**, not a Google-enforced ceiling; owner must accept that provider charges can exceed the estimate before granting build consent.
- Explicit future API prerequisite: official Cloud Build provenance docs list Cloud Build, Container Analysis and Artifact Registry APIs. Cloud Build enable is historical PASS; Container Analysis API current enablement **NOT CHECKED**. DO NOT automatically enable any API; if missing, STOP and decide separately.
- The resource-scoped Artifact Registry writer may not cover all Cloud Build control-plane requirements; Cloud Build service-agent rights, access to remote public Git, availability of Docker builder image and exact region must be checked by provider during the single permitted run. If it fails, **STOP without broadening roles or retry**.

## 3. Distinct acceptance after any separately approved A8 execution
A successful build is not G2 PASS. Require *only new-artifact-specific* evidence:
1. Exact Cloud Build ID/region, authenticated source URI+full SHA, configured builder SA, build config, Dockerfile, one attempt; final state and 20m cap. Any missing SHA / mutable branch / unexpected build => STOP.
2. New Registry image digest and `linux/amd64` child are exact derived outputs, repository remains private; no overwrite, upload to other registry or Cloud Run traffic change.
3. Independent cryptographic provenance verification with SLSA verifier: exact image digest, approved GitHub source URI and full commit SHA, trusted Cloud Build builder ID, signed subject/materials; don't equate `requestedVerifyOption: VERIFIED` alone with acceptance. If Container Analysis/provenance unavailable, remain HOLD.
4. New-image-specific *ONE* focused complete vulnerability assessment with actual installed package versions and six existing severe-ID mapping, plus any newly introduced IDs. Prior Grype report is frozen and must not be relabeled as new artifact. Missing vendor-specific signed VEX/residual-risk clearance remains open. No automatic vulnerability waiver.
5. Focused `linux/amd64` runtime Node/Sharp/Firebase import + health, default-OFF 503, nonroot, SIGTERM and the new default-DB guard, one isolated bounded check using this exact new digest; no live Firebase/Cloud Run data-plane or unrelated CI.
6. Independently address separate G4 other-DB/effective invoker and G8 all-service cost/STOP/rollback decisions before ANY later Cloud Run candidate deployment. STEP04=HOLD; PRODUCTION=NO_GO.

## 4. Owner approval required only at execution boundary
The existing `ok aagal vadho` permits **source-only preparation**, not Cloud Build API job execution or a new private Registry write. Before sending ANY build command, explicitly ask owner Yasmin one bundled specific question:

> Approve ONE `asia-south1` `E2_STANDARD_2`, max20m / 100GB, exact Git commit `31888e7a...` + committed config, dedicated SA, Logging-only, new private output `oldx-step04-g2-cloudbuild-20261122-a1:one-shot`, soft ₹100 incremental spending envelope with no hard provider-wide cap, no automatic retry/deploy/IAM/API/billing changes, plus one new-artifact scan/provenance/runtime verification after the build? No change to OLDX main/production.

If approved, prepare and owner-run a **single guarded PowerShell block** with one fresh provider preflight for the exact new target and anchored config, then one gcloud build submit with `--git-source-revision` equal to the exact SHA, `--config` as locally downloaded **pinned same-commit** YAML, `--substitutions=_IMAGE=<the unique target>`, explicit project/account/region. Never use a local dirty folder source, omit `--git-source-revision`, use a moving branch, or allow an immediate second attempt after an ambiguous failure. If owner declines or conditions don't hold, keep source-only/prepared HOLD.

## Official references (verified 22 Nov 2026)
- Cloud Build submit exact GitSource: https://docs.cloud.google.com/sdk/gcloud/reference/builds/submit
- Cloud Build config options `requestedVerifyOption`, `images`, `CLOUD_LOGGING_ONLY`: https://docs.cloud.google.com/build/docs/build-config-file-schema
- User-managed builder: https://docs.cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts
- Provenance and SLSA verifier: https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance
- Current provider pricing: https://cloud.google.com/build/pricing

**Everything in A8 so far is GitHub source-only. No Google Cloud command/build/image/scan/deploy/permissions action was performed.**
