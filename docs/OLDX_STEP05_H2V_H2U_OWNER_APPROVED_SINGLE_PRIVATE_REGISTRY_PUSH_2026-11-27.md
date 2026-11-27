# BAJUTO / OLDX Step05 H2V — owner-approved ONE existing H2U image push into private Artifact Registry

**Date:** 27 Nov 2026 ~22:40 IST. Branch `security-hardening-review`. Source-only preparation by assistant; no WSL or Cloud push executed from chat.

## Exactly scoped Owner approval

After first H2U local new image build passed, owner explicitly said **"ha manjuri chhe"** to: push **that one already-built** H2U Gateway OFF image once to a private `oldx-staging` Artifact Registry and verify its immutable remote digest. This **does not** authorize another Docker build, Cloud Run service creation/deployment, IAM changes, Firestore writes, KMS signing or Production publication. Registry upload is a genuine billable Cloud storage write, unlike previous H2U no-cloud source and local tests.

## Existing destination (NO repository creation)

Prior H1B WSL one-push **ACTUAL PASS**, [exact evidence](OLDX_STEP05_H1B_G2B_ACTUAL_PUSH_PASS_REMOTE_DIGEST_AND_W1_W6_GATE_2026-11-26.md), verified the existing private Docker Artifact Registry repository:
- Project: **`oldx-staging`**
- Location: **`asia-south1`**
- Existing shared repository: **`oldx-staging-images`**, host **`asia-south1-docker.pkg.dev`**
- **New separate image name**: `oldx-c2-h2-gateway-off`
- Unique new tag minted once by script: `h2v-off-20261127-<20-hex>`.
- No reuse, mutation or deletion of existing `oldx-c2-mediator-off`, `oldx-step05-gateway-off`, `oldx-owner-read`, Cloud Run services, service accounts, or other repository contents.

Earlier H1B G2A isolated WSL Owner OAuth configuration is preserved and reused **read-only** for auth, but old H1B G2A/G2B scripts, tests and Registry push are **not repeated**. If those credentials are missing/expired/invalid, this NEW script fails preflight without attempt. Do not request or print OAuth codes, credentials, tokens or browser URLs.

## Exact local image and immutable pins — owner screenshot

- Local image: `oldx-h2u-private-off:local-20261127-one`
- Frozen **local image/index ID** `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`
- BuildKit-exported **linux/amd64 child manifest** `sha256:c165e671e2b231b5b6210f867dacc085d4a53b69fae2998a712019d9b6575243`
- BuildKit-exported **image config** `sha256:56b7a9601702e80286c80089e33fe13049b6fa7d3fbbcb98e4f775c9d31ace25`
- Node runtime `24.22.3`, User 65532, OFF real loopback 200/503/404 previously actual PASS. [Actual local build receipt](OLDX_STEP05_H2U_ONE_LOCAL_IMAGE_BUILD_ACTUAL_PASS_2026-11-27.md).
- One-local-build consumed marker `/root/.oldx-step05-h2u-local-image-build-once-20261127`, **never reset or rerun build**.

These digests are from Owner's actual build stdout; this assistant has not directly inspected Owner's local Docker image. The new upload script will verify exact current local ID and config *before* remote mutation.

## New separate H2V upload source: READY, NOT EXECUTED

**Script** `scripts/step05_h2v_one_existing_h2u_image_private_registry_push_once_20261127.py`, immutable creation commit **`7e593e57157afa4b0ca9fd509548bf0c56ed0078`**, Git blob **`19e153d6993d1955d134d7f33a14c6180d497e99`**. Adapted from the previously successful H1B G2B verified one-shot push implementation, but with **new H2V marker, separate image name, distinct immutable H2U hashes and no new build**.

Preflight (before marker/push):
- Requires root in WSL, source run flag `--h2v-one-owner-approved-h2u-push-once`, unused new H2V marker, and prior H2U local-build consumed marker.
- Reuses existing native Linux SDK `/root/oldx-tools/native-gcloud-594.0.1/google-cloud-sdk` and prior **isolated** G2 Owner Google and Docker configs; checks exact activated owner `yasminparmar087@gmail.com`, project `oldx-staging`, registry helper scoped only to `asia-south1-docker.pkg.dev`. No login or reconfiguration.
- Checks frozen local Docker image ID, linux/amd64, nonroot 65532:65532, `/nodejs/bin/node` ENTRYPOINT, exact H2U OFF CMD and `OLDX_H2U_MODE=OFF`.
- GET of the exact **existing** repository metadata must be HTTP200, identity/location exact, format DOCKER. New random tag's remote HEAD must be 404 (not 403, 401 or unknown), and local remote-tag collision must be absent.
- Uses short-lived existing Owner OAuth access token internally only; does not print it or save it to GitHub.

One-shot write/verification:
- Creates `/root/.oldx-step05-h2v-one-immutable-local-image-push-once-20261127` and a new root-private evidence folder **BEFORE** any new Docker tag/push. On STOP keep both; never retry old or new scripts or delete markers.
- Exactly one local `docker tag` of the existing immutable image into new `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-h2-gateway-off:h2v-off-20261127-<new hex>`; re-check 404 exact tag; **one `docker push` only**. May upload blobs and manifest; this is one registry publication. No Docker build, no independent old test/scan, no new Cloud permissions/SA/Run.
- Reads immutable **remote tag manifest** and child manifest over authenticated HTTPS after upload; verifies SHA256 raw bytes/header, **remote index digest == frozen local image/index ID**, exactly one linux/amd64 child == frozen local child, and config digest == frozen local config. If mismatch/timeout/partial write, report STOP and preserve evidence; **do not retry**, since a registry write might already have occurred.
- Writes a private sanitized result receipt (remote immutable digests) without token or credentials and prints status fields.

### One exact Ubuntu root WSL command — ONE newly approved Registry write

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2v-registry-push-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/push.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/7e593e57157afa4b0ca9fd509548bf0c56ed0078/scripts/step05_h2v_one_existing_h2u_image_private_registry_push_once_20261127.py' &&
test "$(git hash-object "$d/push.py")" = '19e153d6993d1955d134d7f33a14c6180d497e99' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/push.py" &&
python3 -B "$d/push.py" --h2v-one-owner-approved-h2u-push-once
~~~

**Expected success only from actual owner run:**
~~~text
H2V_STAGE=ONE_AUTHORIZED_H2U_PUSH_ATTEMPT
H2V_REMOTE_DIGEST=sha256:...
H2V_REMOTE_AMD64_CHILD=sha256:...
H2V_REMOTE_CONFIG=sha256:...
H2V_PUSH_ATTEMPTED=TRUE
H2V_RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED
H2V_CLOUD_RUN_OR_IAM_WRITES=NONE
H2V_REGISTRY_WRITE=ONE_PUSH_ATTEMPTED
H2V_LOCAL_IMAGE_BUILD=NONE
H2V_H2_PRODUCTION=NO_GO
H2V_DO_NOT_REPEAT=TRUE
~~~

**If STOP**: only share the `H2V_RESULT` and `H2V_REASON` lines or sanitized screenshot; do not share OAuth tokens, credentials or entire Docker auth files. If `H2V_PUSH_ATTEMPTED=TRUE` or new marker exists, **do not rerun**. Preflight STOP means no push. No successful remote digest is claimed before owner executes.

## After registry upload

Only after actual H2V PASS will a **new owner decision** be requested for Cloud Run private H2 Gateway service staging, pinned to verified remote digest with Gateway SA UID `107238619872767759560`, Invoker/auth/ingress and precise cleanup/retention. Independent KeyVersion status reader and durable Firestore one-sign ledger, bounded synthetic signing and derived-image provenance/security remain distinct. Production remains NO_GO.

**Checkpoint:** `H2V_REGISTRY_PUSH=OWNER_APPROVED_SOURCE_READY_NOT_RUN`; `H2U_LOCAL_IMAGE_BUILD=ACTUAL_PASS_CONSUMED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
