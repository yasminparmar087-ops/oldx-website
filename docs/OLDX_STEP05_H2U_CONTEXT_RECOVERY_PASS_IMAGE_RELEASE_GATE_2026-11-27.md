# BAJUTO / OLDX Step05 H2U — Recovery actual PASS and digest-gated release template

## 27 November 2026 ~22:00 IST — Owner actual 65-file context recovery PASS_WITH_LIMITS

[Canonical recovery STOP + distinct actual PASS receipt](OLDX_STEP05_H2U_CONTEXT_EACCES_RECOVERY_2026-11-27.md). Owner root WSL screenshot:

- `OLDX_H2U_CONTEXT_PERMISSION_RECOVERY=PASS_SOURCE_ONLY_WITH_LIMITS`, after a **distinct** permission-only recovery. The original EACCES one-shot is an authentic historical STOP and **must not** be rerun.
- `OLDX_H2U_CONTEXT_RESULT=PASS_65_FILES_SOURCE_ONLY` (65 files; 349667 source bytes).
- Immutable pre-existing `source-closure.json` SHA256: `12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc`.
- New staged `SOURCE_SHA256SUMS` SHA256: `42081779fe50e3ea9bf8d47aa8613c09db33050d46027d757d24efc79a2f6ecc`.
- Screenshot-reported recovery log SHA256: `3ca6ca1aad1234a840d533fd8e1bea580b5addf471d3bf578f5cea22585d9f6e`.
- Owner-local staging evidence: `/root/oldx-h2u-context-permission-recovery.kANeYR1S`, containing `output/h2u-off-source-context/app` plus exact 65-file hashes, private ESM package metadata and non-Dockerfile release plan. Underlying local files are not uploaded/rehashed by ChatGPT.
- `OLDX_H2U_CONTEXT_OLD_MARKER=UNCHANGED`, `OLDX_H2U_CONTEXT_ORIGINAL_MANIFEST=UNCHANGED`, `CLOUD_WRITES=NONE`, `IMAGE_BUILDS_PULLS_SCANS=NONE`, `H2_PRODUCTION=NO_GO`.
- NEW recovery one-shot marker `/root/.oldx-step05-h2u-context-manifest-permission-recovery-once-20261127` is **CONSUMED**; do not repeat or delete any markers.

Previous H2U offline import scan 65 files, ESM link 174 edges, mock HTTP group 3/3, actual Docker-local OFF listener 200/503/404 all PASS. **Do not repeat any prior checks or rebuild/scan old H1A/H1B image.**

## The next RELEASE gate is base-image trust, not more OLD tests

New **source-only** `release/H2U_Containerfile_OFF_ONLY_UNVERIFIED.template` committed at `b08104b6c3eb956dd197f03d33e1922dec86d929`. This is deliberately **NOT** a buildable Containerfile. It names the candidate `gcr.io/distroless/nodejs24-debian13:nonroot` but uses a deliberately INVALID SHA256 digest sentinel. It requires an independently verified **linux/amd64** digest of the intended immutable base and source/architecture/provenance review before replacing the sentinel. It uses numeric `USER 65532:65532`, `COPY --chown=65532:65532` of only the previously staged `app/` (65 manifest-verified files) plus `package.json`, `NODE_ENV=production`, `OLDX_H2U_MODE=OFF`, `PORT=8080`, and `CMD ["scripts/c2-h2u-cloud-run-private-off-main.mjs"]`. Distroless Node24 provides a Node ENTRYPOINT, not a shell or npm process. No external npm dependency is assumed for this OFF-only source based on prior *static* zero external imports.

Official public sources: [Distroless supported tags and architectures](https://github.com/GoogleContainerTools/distroless), [Distroless Node.js image ENTRYPOINT and CMD](https://github.com/GoogleContainerTools/distroless/blob/main/nodejs/README.md). Availability of the named tag is **not** proof of the exact current immutable digest, signature, security fitness or suitability for H2; no digest or actual base-image choice has been verified here.

### Owner next local-only action (not yet executed or approved as a build)

Verify the exact image reference via **public registry metadata read-only**, preferably using a trusted registry client that exposes OCI index/child manifests without pulling the layers. Record actual `linux/amd64` digest, index digest, keyless signature/provenance and Node24 runtime/UID. Then replace the template sentinel in a **new reviewed, buildable release file** using those verified values. The new release file must fail closed if any mismatch. Protect the staged `SOURCE_SHA256SUMS` SHA and keep the source context immutable.

Only after those facts are grounded should the owner be asked for **one scoped local build/verification approval**, and separately for **one specific Cloud registry push/new default-OFF Cloud Run service** with image digest, known Gateway SA UID `107238619872767759560`, private Invoker identity/audience and ingress. Cloud Run's auth layer must enforce access before requests reach the OFF-only HTTP handler. [Cloud Run authentication overview](https://docs.cloud.google.com/run/docs/authenticating/overview). An OFF-only process does not enable Product operations; fresh independent KMS status reader, Firestore permanent one-sign ledger and one synthetic signing authorization remain separately pending.

**No build, registry fetch/pull, deploy, IAM edit, Firestore transaction or KMS signing has been performed as part of this source-only template work.**

**Checkpoint:** `H2U_CONTEXT_RECOVERY=ACTUAL_PASS_CONSUMED`, `H2U_OFF_CONTEXT=STAGED_65_FILES`, `H2U_DISTROLESS_NODE24_TEMPLATE=SOURCE_ONLY_DIGEST_UNVERIFIED`, `H2U_IMAGE=NOT_BUILT`, `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`.
