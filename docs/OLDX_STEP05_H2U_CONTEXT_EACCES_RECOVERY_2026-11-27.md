# BAJUTO / OLDX Step05 H2U — source context manifest EACCES, one focused recovery

**27 November 2026 ~21:55 IST. The Owner supplied a root WSL screenshot.**

## Actual result — STOP, not an H2U source failure

Previously created H2U source-only staging wrapper `scripts/step05_h2u_stage_exact_off_source_context_once_20261127.sh`, source commit `9c60c66fb97346c36a1fdbcd982207c9188ccd9d`, blob `9a93184ca69037e4f7fd89f82bea011b477a089d`, ran once and emitted:

~~~text
OLDX_H2U_OFF_CONTEXT_CACHED_NODE=TRUE
OLDX_H2U_OFF_CONTEXT_OLD_MANIFEST=12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc
Error: EACCES: permission denied, open '/evidence/source-closure.json'
Node.js v24.22.3
OLDX_H2U_OFF_CONTEXT_STAGE=STOP
OLDX_H2U_OFF_CONTEXT_ATTEMPT_STARTED=TRUE
OLDX_H2U_OFF_CONTEXT_CLOUD_WRITES=NONE
OLDX_H2U_OFF_CONTEXT_IMAGE_BUILDS_PULLS_SCANS=NONE
OLDX_H2U_H2_PRODUCTION=NO_GO
~~~

The wrapper verified the manifest SHA on **Owner WSL as root**, but then bind-mounted the original root-private `source-closure.json` directly into a Docker container running as nonroot UID `65532:65532`. That read failed before 65-file context generation. This is an **access mode issue on the manifest**, not proof that its content/source code is defective. The earlier 65-file import scan PASS, 174 ESM edges PASS and real OFF listener 200/503/404 PASS are preserved and must NOT be repeated.

**Original consumed one-shot marker:** `/root/.oldx-step05-h2u-off-context-stage-once-20261127`. **DO NOT rerun the old wrapper, remove the marker, chmod/chown original manifest, or delete local evidence.** The old output is NOT PASS and should not be treated as a prepared OCI context. The screenshot did not demonstrate any Cloud, registry, Docker image build/pull/scan, KMS, Firestore or IAM action.

## New narrow recovery only — source READY, NOT EXECUTED

New source-only recovery wrapper `scripts/step05_h2u_context_manifest_permission_recovery_once_20261127.sh`:
- Immutable source commit `1dbf8514d5d500f601e146eb6a3fb106985f36a6`.
- Git blob SHA1 `67afe4b1bea0aac3672fa95f9d1cd0bcbb73c604`, independently fetched back from GitHub.
- Requires the original consumed marker, validates the original manifest SHA256 `12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc`, preserves original evidence untouched.
- Creates **a new private root-owned temp folder** and copies just that manifest to `private-manifest/source-closure.json`, applies mode `0644` to the **copy only**, verifies its exact SHA again; nonroot container receives that copy as a read-only bind mount instead of the unreadable original.
- Reuses the exact previous pinned H2U 65-file staging program blob `ce9d4514b1fdffc1280854ed4443e896a719fb2d` with no change to verified import closure or old tests. Existing 65 source files are mounted read-only; output is a completely **new separate** writable local context folder owned by UID 65532. No modification of prior failed output or source evidence.
- Uses **only cached local Node24 Docker image**, `--network none`, `--pull never`, read-only rootfs, nonroot UID, no image build, pull, push, scan, Cloud API call or app listener.
- Creates one distinct new marker `/root/.oldx-step05-h2u-context-manifest-permission-recovery-once-20261127` **before new recovery attempt**. STOP means preserve the marker/evidence and diagnose; never blindly repeat. No previous one-shot marker is reset.
- Source review/GitHub readback PASS only. **Recovery has not been executed and is not yet a PASS.**

### One NEW root Ubuntu WSL command — focused EACCES recovery only

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2u-permission-recovery-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/recover.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/1dbf8514d5d500f601e146eb6a3fb106985f36a6/scripts/step05_h2u_context_manifest_permission_recovery_once_20261127.sh' &&
test "$(git hash-object "$d/recover.sh")" = '67afe4b1bea0aac3672fa95f9d1cd0bcbb73c604' &&
bash -n "$d/recover.sh" &&
bash "$d/recover.sh"
~~~

**Only if actually observed:** `OLDX_H2U_CONTEXT_RESULT=PASS_65_FILES_SOURCE_ONLY` and `OLDX_H2U_CONTEXT_PERMISSION_RECOVERY=PASS_SOURCE_ONLY_WITH_LIMITS` mean the local source packaging was staged. No actual Dockerfile/Containerfile, immutable Node24 base-image digest, image build/push or Cloud Run deployment is created; `H2/PRODUCTION=NO_GO`.

The approval for source-only local preparation does **not** include live Cloud Run, KMS signing, Firestore permission, IAM role edits, image push or new spend. Later image base/provenance and separately authorized Gateway deployment remain unresolved.

**Current checkpoint:** `H2U_ORIGINAL_CONTEXT_STAGE=STOP_EACCES_CONSUMED`, `H2U_PERMISSION_RECOVERY=SOURCE_READY_UNRUN`, `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`.

## 27 Nov 2026 ~22:00 IST — OWNER ACTUAL PERMISSION RECOVERY PASS (CONSUMED)

Owner screenshot of root WSL after executing the **new** exact recovery wrapper commit `1dbf8514d5d500f601e146eb6a3fb106985f36a6`, verified Git blob `67afe4b1bea0aac3672fa95f9d1cd0bcbb73c604`:

~~~text
OLDX_H2U_CONTEXT_RECOVERY_CAUSE=NONROOT_MANIFEST_READ_EACCES
OLDX_H2U_CONTEXT_RECOVERY_MANIFEST_SHA256=12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc
OLDX_H2U_CONTEXT_RECOVERY_MANIFEST_COPY_MODE=0644_PRIVATE_PARENT
OLDX_H2U_CONTEXT_RESULT=PASS_65_FILES_SOURCE_ONLY
OLDX_H2U_CONTEXT_FILE_COUNT=65
OLDX_H2U_CONTEXT_SOURCE_BYTES=349667
OLDX_H2U_CONTEXT_MANIFEST_SHA256=12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc
OLDX_H2U_CONTEXT_SHA256SUMS_SHA256=42081779fe50e3ea9bf8d47aa8613c09db33050d46027d757d24efc79a2f6ecc
OLDX_H2U_CONTEXT_PACKAGE_JSON=PRIVATE_MODULE_NO_DEPS
OLDX_H2U_CONTEXT_CONTAINERFILE=NOT_GENERATED
OLDX_H2U_CONTEXT_BASE_DIGEST=NOT_SELECTED
OLDX_H2U_CONTEXT_CLOUD_WRITES=NONE
OLDX_H2U_CONTEXT_IMAGE_BUILDS_PULLS_SCANS=NONE
OLDX_H2U_H2_PRODUCTION=NO_GO
OLDX_H2U_CONTEXT_RECOVERY_LOG_SHA256=3ca6ca1aad1234a840d533fd8e1bea580b5addf471d3bf578f5cea22585d9f6e
OLDX_H2U_CONTEXT_PERMISSION_RECOVERY=PASS_SOURCE_ONLY_WITH_LIMITS
OLDX_H2U_CONTEXT_RECOVERY_EVIDENCE=/root/oldx-h2u-context-permission-recovery.kANeYR1S
OLDX_H2U_CONTEXT_OLD_MARKER=UNCHANGED
OLDX_H2U_CONTEXT_ORIGINAL_MANIFEST=UNCHANGED
OLDX_H2U_CONTEXT_RECOVERY_CLOUD_WRITES=NONE
OLDX_H2U_CONTEXT_RECOVERY_BUILDS_PULLS_SCANS=NONE
OLDX_H2U_H2_PRODUCTION=NO_GO
~~~

**Verified observation scope:** exactly 65 existing hash-pinned source files staged into an isolated local OFF-only source context (349667 aggregate bytes). Minimal private ESM package metadata and SHA256SUMS produced. The copied manifest was readable to nonroot Docker; original manifest and consumed older marker remained untouched. No Dockerfile/Containerfile, release base-image digest, Docker image build, scan, registry push or Cloud Run host has been produced. Reported output hashes and evidence folder are owner screenshot-derived; their underlying files were not uploaded or rehashed here. The new recovery attempt marker `/root/.oldx-step05-h2u-context-manifest-permission-recovery-once-20261127` is **CONSUMED; DO NOT REPEAT**. Prior EACCES STOP remains an accurate historic record, but is superseded by this separate recovery PASS.

**Next critical path:** new immutable trusted Node24 base-image digest and minimal nonroot Containerfile/release-plan source; then separately scoped owner approval for any actual build/push/Cloud Run deploy, IAM, Firestore or real KMS signing. No new Cloud authorization is inferred from offline recovery. `STEP05=ACTIVE; H2/PRODUCTION=NO_GO`.
