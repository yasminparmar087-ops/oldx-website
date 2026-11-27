# BAJUTO / OLDX Step05 H2U — local build preflight path STOP, zero build attempts, SHA-pinned path recovery

## 27 Nov 2026 ~22:29 IST — actual Owner screenshot

The one Owner-approved local H2U image runner `scripts/step05_h2u_once_local_signed_index_image_build_off_smoke_20261127.sh` (immutable commit `621af10374ce9912b3a0f2f72eaff33223a7a37f`, Git blob `8f7edbfca4420656e67f59e1a97a4a1962c78c13`) was downloaded and invoked once. It STOPPED **before the prebuild marker and before any image build**:

~~~text
STOP_OLD_SOURCE_CONTEXT_OR_MANIFEST_MISSING
OLDX_H2U_LOCAL_IMAGE_RESULT=STOP
OLDX_H2U_LOCAL_BUILD_STARTED=FALSE
OLDX_H2U_LOCAL_IMAGE_CLOUD_WRITES=NONE
OLDX_H2U_LOCAL_IMAGE_REGISTRY_PUSH=NONE
OLDX_H2U_LOCAL_IMAGE_CLOUD_RUN_DEPLOY=NONE
OLDX_H2U_LOCAL_IMAGE_OLD_TESTS_REPEATED=NONE
OLDX_H2U_H2_PRODUCTION=NO_GO
~~~

**Interpretation:** The old runner requires hard-coded `CTX`, `CTX/SOURCE_SHA256SUMS` and `ORIG` paths and rejects absence, symlink or unexpected type; screenshot does not distinguish **which** predicate failed. Do not claim a missing or corrupted source until real on-disk discovery. The **single approved local build attempt remains unused** (`BUILD_STARTED=FALSE`; the durable marker `/root/.oldx-step05-h2u-local-image-build-once-20261127` is created only immediately before an actual build and should be absent). No image was created by this attempt, no need for new build consent. **Do NOT rerun the old pinned wrapper** or repeat historical staging, source tests/scans, OCI metadata or Cosign.

## New focused recovery — uses same one-build approval only

New full runner `scripts/step05_h2u_local_build_prebuild_path_recovery_once_20261127.sh`, immutable commit `d49426a092dc5a6064937389b432bd1a581c1b40`, verified Git blob `cf43fed7599d0f298c68e9c4be9e795611470201`.

Only change to old runner: before its existing 65-file source and manifest preflight, enumerate **local existing** `/root/oldx-h2u-context-permission-recovery.*/output/h2u-off-source-context` and `/root/oldx-h2u-import-closure.*/source-closure.json` candidates; accept exactly one non-symlink source context whose `SOURCE_SHA256SUMS` SHA256 matches `42081779fe50e3ea9bf8d47aa8613c09db33050d46027d757d24efc79a2f6ecc` and exactly one existing manifest with SHA256 `12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc`. If none or multiple, output `STOP_CONTEXT_MATCHES=N` or `STOP_MANIFEST_MATCHES=N` and **STOP before build and marker**; preserve evidence and diagnose. Reject drift, ambiguous evidence, missing files or symlinks—**no restaging, copying, changing permissions, clearing markers or old test reruns**.

Once unique paths are resolved, original preflight still performs exact 65 source-file hashes/349667 byte check, no unlisted files, minimal private package metadata; downloads only the immutable previously reviewed source Containerfile, checks Git blob `4b85cbe44dc7e141f6934d99a91d8ec31cf2868c`, immutable signed Node24 index `sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121`, then consumes **the SAME one-build marker immediately before exactly one `docker buildx build --load`**. New image-specific nonroot Node24, OFF-only loopback `200/503/404`, no public ports or Cloud. No repeat of earlier tests. No registry push, Cloud Run, IAM, Firestore, KMS or production. No new image result can be claimed before actual Owner WSL execution.

### One new WSL root command (not yet executed)

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2u-build-path-recovery-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/build.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/d49426a092dc5a6064937389b432bd1a581c1b40/scripts/step05_h2u_local_build_prebuild_path_recovery_once_20261127.sh' &&
test "$(git hash-object "$d/build.sh")" = 'cf43fed7599d0f298c68e9c4be9e795611470201' &&
bash -n "$d/build.sh" &&
bash "$d/build.sh"
~~~

**On any STOP** report terminal screenshot and new local evidence if shown, do not retry after marker, never delete markers. One approved build is only consumed once `OLDX_H2U_LOCAL_BUILD_STARTED=TRUE` appears or the durable marker exists. If path discovery fails, that approval is still unused.

**Status:** `H2U_PREVIOUS_LOCAL_BUILD=STOP_BEFORE_BUILD`, `H2U_APPROVED_BUILD_BUDGET=ONE_UNUSED`, `H2U_NEW_PATH_RECOVERY=SOURCE_READY_NOT_EXECUTED`, `H2/PRODUCTION=NO_GO`.
