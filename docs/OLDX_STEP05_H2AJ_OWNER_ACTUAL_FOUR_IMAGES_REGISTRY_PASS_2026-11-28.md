# BAJUTO / OLDX — Step05 H2AJ ACTUAL OWNER PASS: FOUR private OFF Linux/AMD64 images

Date: 2026-11-28 IST (~21:13). Owner WSL-root screenshot. Branch: `security-hardening-review` only.

## Actual SUCCESS (not a simulated source test)

After the H2AI first attempted Mediator build failed before Dockerfile resolution (`lstat deployment`) and permanently consumed the H2AI one-shot marker, Owner approved and executed the DISTINCT H2AJ one-shot with verified immutable source. The new H2AJ runner corrected Dockerfile paths to **absolute locations within individually prepared contexts**, passed fresh **read-only** checks for the four role bundles, and executed exactly one Buildx Linux/AMD64 build+push invocation for each of four PRIVATE, future-default-OFF Artifact Registry image targets.

Exact Owner screenshot:

```text
H2AJ_PREFLIGHT=OWNER_PROJECT_REPOSITORY_NODE_DOCKER_DISK_PASS
H2AJ_SOURCE_BUNDLES=FOUR_READY_EXACT_APPROVED_SOURCE
H2AJ_MARKER=CONSUMED_NO_REPEAT
H2AJ_BUILD_PUSH_START=mediator
H2AJ_IMAGE_PUSH_AND_AMD64_DIGEST_VERIFIED=mediator sha256:01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe
H2AJ_BUILD_PUSH_START=gateway
H2AJ_IMAGE_PUSH_AND_AMD64_DIGEST_VERIFIED=gateway sha256:921fbf4ff71b918c479e4a786868368640a494c16da08e54192f25e14dc1ec4d
H2AJ_BUILD_PUSH_START=backend
H2AJ_IMAGE_PUSH_AND_AMD64_DIGEST_VERIFIED=backend sha256:01ae540aa88ad0e3a6888994dd41b6b02b9d934a7a1d2e455f44b194f033b941
H2AJ_BUILD_PUSH_START=reader
H2AJ_IMAGE_PUSH_AND_AMD64_DIGEST_VERIFIED=reader sha256:822e2592b1010bfa94a1fe5bc75003712485abae0369f5252ece3863723eb077
H2AJ_RESULT=PASS_FOUR_NEW_PRIVATE_OFF_IMAGES
H2AJ_SOURCE_REVISION=f567aa6ccef7a71b6032dc1bdb9f2bcf0a8587d4
H2AJ_PRIVATE_EVIDENCE=/root/oldx-h2aj-four-builds-20261128T153103Z-721b5d
H2AJ_DOCKER_CONFIG=TEMPORARY_NOT_GLOBAL
H2AJ_CLOUD_RUN_IAM_KMS_FIRESTORE_DEPLOYMENT=NONE
H2AJ_H2_PRODUCTION=NO_GO
H2AJ_DO_NOT_REPEAT=TRUE
H2AJ_REASON=NONE
```

**Note:** These SHA256 values are the derived **Linux/AMD64 child image manifest digests**, not necessarily the OCI multi-platform root/index digests. The private root-owned evidence contains per-role Buildx metadata for BOTH `registryIndexDigest` and `linuxAmd64ChildDigest`, sanitized per-role source provenance, and build log hashes. The screenshot establishes runner's SUCCESS and verified registry readback at execution time; it is not a fresh independent registry inspection by ChatGPT.

| Role | Exact private repository image | Verified Linux/AMD64 child digest |
| --- | --- | --- |
| Mediator | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-h2ah` | `sha256:01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe` |
| Gateway | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-gateway-h2ah` | `sha256:921fbf4ff71b918c479e4a786868368640a494c16da08e54192f25e14dc1ec4d` |
| Backend | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-backend-h2ah` | `sha256:01ae540aa88ad0e3a6888994dd41b6b02b9d934a7a1d2e455f44b194f033b941` |
| Independent KMS Reader | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-kms-reader` | `sha256:822e2592b1010bfa94a1fe5bc75003712485abae0369f5252ece3863723eb077` |

Immutable source build checkpoint: `f567aa6ccef7a71b6032dc1bdb9f2bcf0a8587d4`, descended from approved source `5d5a621d7a9d9015b5068077b914fef3d6fb9925`. The script had verified original production source/Docker COPY closure unchanged. H2AJ exact runner was at Git commit `6e4a1fa8908b47f720a3add961cf8ac2bb3aa1a6`, Git blob `9f3264aa47243a09187604c13eb8232aa6bc8c59`; corrected preflight blob `f5137df3af84de55c3fe1c0468b22e2446001f7d`.

## Critical DO-NOT-REPEAT / safety state

- **H2AJ one-shot marker CONSUMED**: `/root/.oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128`. Never clear/reset or rerun H2AJ; four builds/pushes are ALREADY DONE. Preserve old H2AI consumed marker and all private evidence.
- Existing H2AG Reader service account `oldx-c2-kms-reader@oldx-staging.iam.gserviceaccount.com`, numeric UID `107336955065718475994`, KMS version/public-key GET roles on exact existing CryptoKey: actual Owner PASS, do not create or regrant.
- Previous **23 distinct focused source tests** and four-role six-stage LOCAL HTTP Seller→Buyer simulation were done before these images. No re-run necessary.
- These are **OFF source images in a private registry**. H2AJ did **NOT** create Cloud Run services/revisions, change ingress/Invoker/IAM/VPC, read/sign KMS, write Firebase/Firestore/Storage, run hosted Seller→Buyer test or enable production.
- New-image SBOM/provenance was requested by Buildx `--sbom=true --provenance=true`, but a real new-image vulnerability scan, fresh nonroot actual runtime health check and independent per-digest security disposition still remain **NOT VERIFIED**; don't infer security GO from registry push. Owner had previously accepted possible residual CVE risk for later monitored launch, but no automatic Step05/production GO.

## ONE fastest next milestone (without repeating old work)

Work against **these FOUR newly frozen digests only**, no rebuilding or re-pushing:
1. Recover **only new** root OCI index digests / manifest labels / new-image SBOM provenance from the private sanitized receipt as needed; use exact already-known child digests above. Avoid old H1/H2 scans and no full inventory.
2. Run ONE scoped new-image security scan and minimal nonroot OFF-health runtime checks for these exact four digests (reuse existing tools, bounded one-shot, not rebuild). Record residual findings for an explicit risk/launch decision; a scan may require security policy review but do not wait indefinitely for upstream patches.
3. Freeze a single complete **private-staging deployment/host approval** with immutable refs, four actual SA/UID attachments (Mediator `100779414920484819274`, Gateway `107238619872767759560`, Backend `106984791114720194680`, Reader `107336955065718475994`), separate invoker audiences and a legitimate **internal Cloud Run networking path** (historical H2AD9 NOT_FOUND remains unproven). Require trusted independent runtime controller/config/approval custody and native Firebase/Firestore/media/Stage-ledger privileges; do NOT invent those current Cloud values or silently turn OFF into ENABLED.
4. With separate exact Owner approval for necessary Cloud writes, deploy **private OFF-only revisions** using the frozen image refs, verify hosted `/healthz` and private IAM/network proof; only after that consider ONE separately guarded synthetic six-stage Seller save→publish→buyer list/detail→edit→withdraw verification. No real user writes. Production OFF until verified and approved.

**Status:** `H2AJ=FOUR_ACTUAL_REGISTRY_BUILD_AND_PUSH_PASS_DO_NOT_REPEAT`; `FOUR_AMD64_CHILD_DIGESTS=PINNED`; `CLOUD_RUN_HOSTED=NOT_DEPLOYED`; `NEW_IMAGE_SECURITY_RUNTIME=NOT_VERIFIED`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
