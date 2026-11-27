# BAJUTO / OLDX Step05 H2U — actual local OFF listener PASS; exact 65-file source context next

## Actual owner WSL result, 27 Nov 2026 ~21:48 IST

The owner executed **one new** hash-pinned H2U OFF HTTP listener smoke on the already-verified Owner-local 65-file source tree and its manifest. [Canonical H2U source/ESM/local listener history and actual PASS](OLDX_STEP05_H2U_ESM_LINK_ACTUAL_PASS_LOCAL_OFF_LISTENER_NEXT_2026-11-27.md).

~~~text
OLDX_H2U_OFF_LISTENER_NODE_IMAGE=CACHED_NO_PULL
OLDX_H2U_OFF_LISTENER_MANIFEST_SHA256=12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc
OLDX_H2U_OFF_RUNTIME_SMOKE=PASS_LOCAL_LISTENER_WITH_LIMITS
OLDX_H2U_OFF_RUNTIME_SOURCE_FILES=65
OLDX_H2U_OFF_RUNTIME_HEALTH_STATUS=200_OFF
OLDX_H2U_OFF_RUNTIME_SAVE_STATUS=503_DISABLED
OLDX_H2U_OFF_RUNTIME_UNKNOWN_STATUS=404
OLDX_H2U_OFF_RUNTIME_NETWORK=DOCKER_LOOPBACK_ONLY
OLDX_H2U_OFF_RUNTIME_CLOUD_WRITES=NONE
OLDX_H2U_OFF_RUNTIME_IMAGE_BUILD=NONE
OLDX_H2U_H2_PRODUCTION=NO_GO
OLDX_H2U_OFF_LISTENER_LOG_SHA256=a8fc994e9a9462e209032bfb650e41861eaa5b8dc5508d9c89827cef0e3b0775
OLDX_H2U_OFF_LISTENER_ONE_SHOT=PASS_WITH_LIMITS
OLDX_H2U_OFF_LISTENER_EVIDENCE=/root/oldx-h2u-off-listener.eFWd0haw
OLDX_H2U_OFF_LISTENER_CLOUD_WRITES=NONE
OLDX_H2U_OFF_LISTENER_BUILDS_PULLS_SCANS=NONE
OLDX_H2U_H2_PRODUCTION=NO_GO
~~~

**Result scope:** The real OFF-only H2U Node listener started inside isolated cached local Docker with no published port, answering loopback health 200 OFF, attempted synthetic-save 503 DISABLED and unknown 404. No Cloud writes, new image build/pull/scan, IAM, Firestore, KMS operation. The owner-screenshot SHA256 is not independently recalculated against the unuploaded local log. This does not establish a new OCI image or private Cloud Run deployment, public/private Invoker IAM or real signer readiness.

**NO REPEAT:** Already consumed marker `/root/.oldx-step05-h2u-off-listener-smoke-once-20261127`. Preserve it plus previously completed H2U ESM 65 modules/174 links, old 65-file scanner, HTTP 3/3 mock group and H2S/H2T/H2N/H2R one-shots. Never rerun old checks, clear markers, or rebuild H1A/H1B historical images.

## NEW work — build context STAGING ONLY; never build OCI image here

A full 65-entry manifest resides only on the owner's Ubuntu WSL at `/root/oldx-h2u-import-closure.2oCNZVHV/source-closure.json`; its screenshot-pinned SHA256 is `12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc`. ChatGPT does not know or invent its 65 individual paths.

New standalone JS `scripts/c2-h2u-stage-exact-off-source-context_20261127.mjs` Git blob **`ce9d4514b1fdffc1280854ed4443e896a719fb2d`**, source commit **`18d013cd53c1ca9553617ec550e7a0ee8e7e7264`**. On Owner-local cached Node24 only, it verifies manifest's exact hash, 65 entries / 349667 source bytes / no bare package imports, each file path (no traversal/symlink), source file size and SHA256. It then stages a separate NEW **source context** `h2u-off-source-context/app/` containing exactly those 65 files and a minimal `package.json` (`private:true`, `type:module`, no dependencies); also writes `SOURCE_SHA256SUMS` and `RELEASE_PLAN_NOT_A_DOCKERFILE.txt`. It verifies output hashes, rejects unexpected top-level files, and prints the staged manifest hash. **No Dockerfile/Containerfile or base image digest is selected**, and the output is **not** itself a deployable image or a live service.

New one-shot WSL wrapper `scripts/step05_h2u_stage_exact_off_source_context_once_20261127.sh`: Git blob **`9a93184ca69037e4f7fd89f82bea011b477a089d`**, source commit **`9c60c66fb97346c36a1fdbcd982207c9188ccd9d`**. This wrapper checks the prior on-disk manifest, reuses the cached Node24 Docker image, downloads **only the new small immutable staging source** at pinned Git blob, creates a new isolated output folder and a distinct one-shot marker, and runs with Docker `--network none`, `--pull never`, nonroot UID65532 and readonly source mounts. The separate output directory is a local writable bind mount to stage files; no old evidence is modified or re-executed. There are **zero** image builds/pulls/scans, registry pushes, Cloud calls, previous-test reruns or new Cloud permissions.

**H2U context status:** `SOURCE_PREPARED_NOT_RUN`. No staging PASS can be assumed until owner screenshot confirms actual new `OLDX_H2U_OFF_CONTEXT_STAGE=PASS_SOURCE_ONLY_WITH_LIMITS` and `OLDX_H2U_CONTEXT_FILE_COUNT=65`. The script has been statically read back by GitHub, NOT Node24 executed yet.

### One NEW approved-local-only Ubuntu root WSL command

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2u-context-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/context.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/9c60c66fb97346c36a1fdbcd982207c9188ccd9d/scripts/step05_h2u_stage_exact_off_source_context_once_20261127.sh' &&
test "$(git hash-object "$d/context.sh")" = '9a93184ca69037e4f7fd89f82bea011b477a089d' &&
bash -n "$d/context.sh" &&
bash "$d/context.sh"
~~~

On STOP preserve `/root/.oldx-step05-h2u-off-context-stage-once-20261127` and local evidence. No auto-rerun, marker reset, or repeated previous tests. The staged context is deliberately not buildable until an **independently verified, immutable Node24 nonroot base image digest and release recipe** are approved.

## Remaining critical hosted path

After local source context generation, choose only the verified Node24 base digest and create a reproducible *new* nonroot image recipe; do not reuse/relabel historical H1A/H1B image as the released Gateway. Actual image build/push/Cloud Run create requires new scoped owner approval. Cloud Run Gateway SA attachment UID `107238619872767759560`, authenticated private Invoker/ingress, independent fresh KMS KeyVersion reader, actual permitted Firestore one-sign durable tombstone/no TTL, Backend/Mediator controls and exactly one explicitly owner-approved synthetic signer operation remain unverified. **Step05 ACTIVE, H2/PRODUCTION NO_GO**.
