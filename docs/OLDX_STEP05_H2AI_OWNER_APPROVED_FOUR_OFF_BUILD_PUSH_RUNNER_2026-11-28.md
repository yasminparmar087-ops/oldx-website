# BAJUTO / OLDX Step05 — H2AI Owner-approved FOUR OFF image builds/private pushes: one-shot runner READY, CLOUD/REGISTRY NOT RUN

Date: 28 November 2026 IST. GitHub branch ONLY `security-hardening-review`.

## Exact owner approval and frozen source

Owner explicitly replied **"ha manjuri chhe"** to the consolidated four-image source+local build/private registry push proposal in `docs/OLDX_STEP05_H2AH_FOUR_ROLE_SOURCE_RECEIPT_2026-11-28.md`.

Scope is only FOUR new private **default-OFF** linux/amd64 images from previously tested remote code `5d5a621d7a9d9015b5068077b914fef3d6fb9925` (or descendant with bit-for-bit unchanged `features/`, `functions/`, `deployment/four-role/` and all existing `scripts/` implementation):
- `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-h2ah`
- `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-gateway-h2ah`
- `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-backend-h2ah`
- `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-kms-reader`

Maximum **one** Buildx linux/amd64 build+push invocation PER image. Uses existing Dockerfiles, exact existing pinned Node24 dependency builder and Distroless nonroot base. New random tag per run avoids intentionally overwriting any old image. Use preexisting laptop WSL/Docker and isolated native Owner gcloud; no Cloud Shell, Cloud Build, Actions, old checks/scans. New per-image provenance/SBOM attestation emitted as part of the same Buildx push, NOT a separate vulnerability scan. Private storage/transfer and local Docker cache can incur costs/resources; existing Owner approval applies only to this limited usage.

**Excluded:** Cloud Run service/revision/deployment/activation, IAM/Invoker/Reader SA changes (H2AG actual PASS consumed), VPC/subnet/Secret creation, KMS signing/GET, Firebase/Auth/Firestore/Storage writes, Product synthetic flow, registry deletion, production enable, updating old H2U images, or any old test/scan/retry. No cleanup of historical one-time markers.

## Exact code and safety state

- New one-shot WSL Python runner: `scripts/step05_h2ai_four_off_images_build_push_once_20261128.py`; SHA1 Git blob `4691b6dd459a1e297f3d80697a77fcc5cae16e3d` (remote readback verified).
- New six PURE LOCAL offline safety cases: `tests/integration/step05-h2ai-four-off-registry-new.test.py`; Git blob `1abbd248dd5693dafb7ebdac9938671434e972c8` (remote readback verified).
- **These six tests have been authored, not yet executed in user WSL**. They verify fixed target/approved source, one exact AMD64 manifest child, reject duplicate/wrong arch, root WSL requirement, subprocess failure stop and only one Buildx invocation. Run them before actual build, not all old suites.
- Requires WSL root, exact native isolated Owner login `yasminparmar087@gmail.com`, project `oldx-staging`, repository `oldx-staging-images`, existing Node24+, Docker CLI + Buildx Linux engine, Git, >=6GiB free on WSL root (not a Docker storage guarantee).
- One new isolated clone from `security-hardening-review`; if tested implementation source/lock/Docker closure changed since `5d5a621d...`, STOP. Uses `scripts/step05-h2ah-source-package.mjs` to prepare 4 unique outside-checkout bundles from clean clone, never resetting Owner's dirty repo.
- Verifies project/repository/owner and Docker preflight BEFORE consuming the build attempt marker. Uses a **temporary isolated DOCKER_CONFIG**, `gcloud auth print-access-token` via native SDK and `docker login --password-stdin` (no global credential helper change).
- One exclusive marker `/root/.oldx-step05-h2ai-four-off-build-push-once-20261128` created BEFORE first Buildx --push. Records each role `ONE_BUILD_AND_PUSH_ABOUT_TO_START=TRUE` before its sole invocation, no automatic retry. A failure/timeout/ambiguous registry outcome **consumes the marker**; never delete marker/rerun blindly.
- Saves root-owned private logs, source and package provenance hashes, BuildKit `containerimage.digest`, registry readback's distinct linux/amd64 child manifest digest, SHA256 of manifest and logs, sanitized summary. Base and historical OFF digests explicitly rejected as derived child proof.
- If any image fails, STOP and retain all partial pushes/evidence. Do not rerun or automatically rollback. A new exact reconciliation/approval is required for a partial state. Existing H2AG/H2R/H2AF one-shots are untouched.
- The script only runs on the **Owner's own WSL**; preparing it via GitHub is NOT a Cloud/Registry execution result.

## Owner's ONE WSL root command — COPY ALL LINES AT ONCE

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ai-approved.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/runner.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/5416a76ced19bcbfbf6f9d00bf3348d0a4786c75/scripts/step05_h2ai_four_off_images_build_push_once_20261128.py' &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/test_runner.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/5416a76ced19bcbfbf6f9d00bf3348d0a4786c75/tests/integration/step05-h2ai-four-off-registry-new.test.py' &&
test "$(git hash-object "$d/runner.py")" = '4691b6dd459a1e297f3d80697a77fcc5cae16e3d' &&
test "$(git hash-object "$d/test_runner.py")" = '1abbd248dd5693dafb7ebdac9938671434e972c8' &&
python3 -B "$d/test_runner.py" &&
python3 -B "$d/runner.py" --h2ai-owner-approved-four-local-amd64-off-builds-private-push-once
```

The code intentionally stops without registry writes if Docker/buildx is unavailable, Node24+ missing, disk too small or credentials/project/repository/source drift. If a STOP occurs **before** marker, no image build/push occurred. If `H2AI_MARKER=CONSUMED_NO_REPEAT` appears, NEVER rerun the command even if later build/push fails; inspect the exact private evidence instead.

**Only if all four succeed**, expect `H2AI_RESULT=PASS_FOUR_NEW_PRIVATE_OFF_IMAGES` plus four `H2AI_IMAGE_PUSH_AND_AMD64_DIGEST_VERIFIED=ROLE sha256:...` lines; these are NEW registry artifacts, still NOT deployed nor scanned for new vulnerabilities. A failed/partial attempt cannot be advertised as all four PASS.

## What is left AFTER real four-image PASS

At minimum: source/OCI security scan and Linux nonroot runtime verification of the actual four derived digests, exact Cloud Run service/attached SA UID/Reader routing/internal ingress/Direct VPC/Invoker bindings, independent configuration/controller-trust/cursor secret custody, native Firebase/photo/synthetic actor runtime privileges, owner approval for a later staged OFF deployment and one bounded 6-sign/24-KMS-GET/20-Product-request end-to-end acceptance and cleanup. Existing H2AD9 previous NOT_FOUND is unresolved; H2AF cleanup PASS preserved. No step05 or production GO should be claimed from registry push.

**As of document creation:** `H2AI_OWNER_APPROVED_RUNNER_PUSHED`; `H2AI_NEW_UNIT_TESTS_AUTHORED_NOT_RUN`; `H2AI_LOCAL_BUILDS=NOT_OBSERVED`; `H2AI_REGISTRY_PUSHES=NOT_OBSERVED`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
