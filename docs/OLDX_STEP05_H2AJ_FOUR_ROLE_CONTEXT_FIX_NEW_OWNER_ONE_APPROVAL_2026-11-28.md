# BAJUTO / OLDX Step05 H2AJ — source FIX COMPLETE, one fresh narrowly scoped Owner approval NEXT (28 Nov 2026)

## Actual H2AI consumed attempt — never replay

Owner's screenshot exact 28 Nov ~20:48 IST:

```text
H2AI_MARKER=CONSUMED_NO_REPEAT
H2AI_BUILD_PUSH_START=mediator
H2AI_RESULT=STOP_AFTER_MARKER_POSSIBLE_PARTIAL_REGISTRY_WRITES
H2AI_REASON=APPROVED_COMMAND_FAILED_NO_RETRY
H2AI_PRIVATE_EVIDENCE=/root/oldx-h2ai-four-builds-20261128T151519Z-09e4fd
```

Owner's local sanitized build log showed the **actual first command error**:

```text
ERROR: failed to build: resolve : lstat deployment: no such file or directory
```

**Root cause confirmed in source**: H2AI passed the relative `--file deployment/four-role/Dockerfile.mediator` while invoking Docker from Owner WSL's current `/mnt/c/Users/Yasmin Parmar` directory, rather than from the prepared source-bundle context. Docker tried to resolve `deployment` at the wrong working directory. Docker's `-f/--file` accepts the absolute Dockerfile pathname; its COPY paths continue to resolve against the explicitly supplied build context, and the Dockerfile-specific adjacent `.dockerignore` is used. Official reference: https://docs.docker.com/build/concepts/context/ .

This error occurred while resolving Dockerfile before any successful image build/registry digest; **no image push is proven**. Strict owner status is still **POSSIBLE PARTIAL / unknown registry readback**, do not delete or assume absence of any artifact. Gateway/Backend/Reader were NOT attempted. **Old marker CONSUMED** and must NEVER be deleted or reset. Old H2AG/H2AF/earlier tests all remain do-not-repeat.

## Fixes made NOW — no Cloud change

**1. `scripts/step05-h2aj-build-context-preflight.mjs`**:
- Pure SOURCE/FILESYSTEM-only, zero Docker/registry/Cloud commands.
- Requires each unique role bundle under its canonical absolute path, Dockerfile exactly inside the context; outputs `dockerfileAbsolutePath`, used verbatim by the future runner.
- Verifies four exact Linux AMD64 pinned Node24/distroless FROM stages, exact nonroot/readonly policy, the explicit Node24 builder-stage package COPY for Mediator/Backend, distinct local JSON COPY count **87** for each role and **84** expected ESM source files, exactly matching `copy-closure.json` and role entrypoint.
- Verifies source-provenance revision, all imported source/file/package/lock/Dockerfile/dockerignore/manifest hashes, manifest `executionAllowed:false`, exact Dockerfile-specific `.dockerignore` exclusions and 104-item root/parent/file allowlist per role; rejects symlink/parent escapes, missing files, added path or wrong base.
- Verified 4/4 real GitHub role Dockerfile+COPY/ignore inventories statically: each had 87 local JSON COPY files, 84 closure files, 104 exact ignore allowlist lines, no mismatches. Validator's exact GitHub JS logic was V8 syntax-checked and tested in a synthetic read-only in-memory filesystem for **four positive role fixtures PASS**, using stubbed file bytes/hash. This is **NOT a real Docker build or a Node check on Owner's WSL filesystem**; code still performs these actual checks before future write.

**2. `scripts/step05_h2aj_four_off_images_reconciled_once_20261128.py`**:
- NEW separately approvable H2AJ one-shot script derived from H2AI but **NOT a replay** of the consumed H2AI command.
- New exclusive attempt marker `/root/.oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128`; old `/root/.oldx-step05-h2ai-four-off-build-push-once-20261128` remains untouched.
- BEFORE any new marker, reads the exact old H2AI consumed marker, exact old private summary and first Mediator log; demands exactly the failed `lstat deployment` error, exactly the first Mediator role only and no registry readback. Any mismatch stops with zero new build/push.
- Reuses exact approved immutable source ancestor `5d5a621d7a9d9015b5068077b914fef3d6fb9925`, role locks/ignores/Dockerfiles unchanged. Only known new build runners/preflight scripts may differ; no approved source image drift. It clones into one new isolated checkout, never resets Owner local files.
- Runs **all FOUR actual context/closure/ignore and provenance read-only checks** before creating new H2AJ marker, checking independent validator result hash against source bundle hash.
- **Corrected actual Buildx argument** is `--file bundles[role]["dockerfileAbsolutePath"]` plus that role's same verified absolute source-bundle `context`. No relative `deployment/...` passed as Dockerfile CLI path.
- Same exact four role targets and no mutable old tag overwrite; fresh random tag. Max ONE new linux/amd64 Buildx `--provenance=true --sbom=true --push` attempt per approved role; index and child digests retained on successful readback; stop after first unknown failure. Does not retry or delete old/partial images.
- H2AJ flag requires **new, separate explicit Owner approval**. Code is PREPARED, and the new H2AJ marker has NOT been consumed by this assistant. No test, build, push, IAM, Cloud Run, KMS, Firebase or production action was made.

## Exactly ONE Owner approval after source fix

For `oldx-staging`, registry `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images`, authorize a **NEW H2AJ single one-shot batch** after the known H2AI local Dockerfile path resolution failure. Scope: at most one **new local Linux/AMD64 build and one private push** for each of the FOUR existing, source-identical OFF targets:
- `oldx-c2-mediator-h2ah` (fresh attempt because first H2AI attempt failed before Dockerfile resolution);
- `oldx-c2-gateway-h2ah` (H2AI never attempted);
- `oldx-c2-backend-h2ah` (H2AI never attempted);
- `oldx-c2-kms-reader` (H2AI never attempted).

No old marker reset, no old tag deletion, no Cloud Run deployment/enable, no IAM/secret/VPC change, no KMS signing or metadata GET, no Firebase writes or synthetic Product activity, no new old-version Docker tests/scans. This may incur normal local CPU/disk and registry transfer/storage charges. Exact consumed/partial H2AI status must remain in permanent receipts. **IF** new preflight evidence, Docker image digest, source/lock, Owner identity or private registry diverges, STOP before writing; if H2AJ marker consumed, STOP and do not retry. Any registry orphan should be reviewed read-only later, not deleted without new approval.

**This document is NOT the approval and does not authorize running H2AJ.** Only after the user replies explicitly to this single exact scope may the immutable, SHA-checked new H2AJ runner be supplied for ONE WSL execution.

**Current accurate state**: `H2AI=CONSUMED_FIRST_MEDIATOR_BUILD_DOCKERFILE_RESOLUTION_FAILED`; `H2AJ=SOURCE_FIX_PUSHED_APPROVAL_PENDING`; `FOUR_ACTUAL_NEW_IMAGES=NOT_VERIFIED`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
