# BAJUTO / OLDX Step05 H2AI — Owner's 2nd PREWRITE STOP, fixed a single mistyped immutable builder pin

Date: 2026-11-28 IST. Branch: `security-hardening-review` ONLY.

## Actual Owner WSL screenshot (after prior Node missing prewrite STOP)

```text
github.com/docker/buildx v0.39.0 ...
node-v24.22.3-linux-x64.tar.xz: OK
v24.22.3
H2AI_PREFLIGHT=OWNER_PROJECT_REPOSITORY_NODE_DOCKER_DISK_PASS
H2AI_RESULT=STOP_BEFORE_ANY_BUILD_OR_PUSH
H2AI_REASON=DEPENDENCY_BUILDER_PIN_CHANGED
H2AI_NO_REGISTRY_BUILD_OR_PUSH=TRUE
```

This was a **second H2AI STOP BEFORE ANY BUILD OR PUSH**. The previous six distinct H2AI offline tests already passed on the owner's first run (do NOT repeat). Owner downloaded official Linux Node v24.22.3 and verified SHA256. Docker Buildx v0.39.0 and preliminary Owner/project/repository/Node/Docker/disk preflight PASS. Source bundles reached the pin consistency gate, but the one-shot H2AI build marker had NOT yet been created. No registry write, build/push, Cloud Run, IAM/KMS or Firebase operation took place.

## Exact root cause and only fix

Existing frozen Dockerfiles are correct:
- `deployment/four-role/Dockerfile.mediator` blob `12808d606068265d80d8abe3a743a9763d182f25`;
- `deployment/four-role/Dockerfile.backend` blob `7f79e582524d69c555b702da361d8081b5231ab1`;
- both FROM Node24 dependency builder `node:24-bookworm-slim@sha256:dc26ae92c9fb15cf6b1d63e20f0944b2efe0f115b20e00be48fb23fceb061c54`.

The H2AI guarded *runner's constant* had an incorrect digest `dc26ae92c9fb15cf6b1d63e20e00be48fb23fceb061c54` (missing an `f0944b2` segment). Code compared the wrong constant to the correctly pinned Dockerfile and STOPped. No Dockerfile/source/lock drift existed. The wrong runner preflight was a bug, not a sign of a changed approved base image.

**Changed only the runner's `IMMUTABLE_BUILDER` literal** to exactly match both frozen Dockerfiles. GitHub one-file commit **`839f6c98a568999e44d7d9c7dd75454bb0f2c1a2`**, fixed runner Git blob **`85eb2b61d6e5e86e4980e192e50884470cef00ed`**. Original frozen source `5d5a621d7a9d9015b5068077b914fef3d6fb9925`, owner approval, four role image target list, one attempt per image, no retries after marker, login/project and exact Git source controls all unchanged. No older Node/H2AG tests, builds or scans were repeated as a result of this one-character-scope source correction.

## Single safe OWNER WSL root resume — same H2AI consent, exact corrected immutable runner

As long as the *same WSL root machine* still has `/root/oldx-tools/node-v24.22.3-linux-x64/bin/node` and Docker engine, run **ONE** script download and hash validation followed directly by the approved runner. The earlier `$d/runner.py` is the OLD buggy version; **DO NOT execute it again**. Earlier command used a `( subshell )` so the Node24 PATH export does NOT persist.

```bash
umask 077
export PATH="/root/oldx-tools/node-v24.22.3-linux-x64/bin:$PATH"
test "$(node --version)" = "v24.22.3" &&
test ! -e /root/.oldx-step05-h2ai-four-off-build-push-once-20261128 &&
d=$(mktemp -d /root/oldx-h2ai-fixed.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/runner.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/839f6c98a568999e44d7d9c7dd75454bb0f2c1a2/scripts/step05_h2ai_four_off_images_build_push_once_20261128.py' &&
test "$(git hash-object "$d/runner.py")" = '85eb2b61d6e5e86e4980e192e50884470cef00ed' &&
python3 -B "$d/runner.py" --h2ai-owner-approved-four-local-amd64-off-builds-private-push-once
```

DO NOT rerun the original 6 H2AI offline tests. The fixed runner still re-prepares source bundles in an exclusive directory because that is a new, prewrite, independently checked input for the first build; it does not repeat old CI or Cloud probes. A source provenance mismatch or new unknown error before marker stops with no registry writes. **After `H2AI_MARKER=CONSUMED_NO_REPEAT` appears, NEVER rerun this command regardless of subsequent success or failure; collect terminal and private exact evidence for a separate reconciliation.**

Expected only after four successful new pushes: `H2AI_RESULT=PASS_FOUR_NEW_PRIVATE_OFF_IMAGES`. All four linux/amd64 child OCI digests remain **UNKNOWN until actual registry output**. The new images are OFF and not deployed. Build+push does NOT prove CVE safety, runtime cloud identity, health or Step05 completion.

**Checkpoint**: `H2AI_SIX_NEW_TESTS=ALREADY_PASS`, `NATIVE_NODE24_INSTALLED`, `BUILD_AND_PUSH_ATTEMPT_MARKER=NOT_CONSUMED_AT_OWNER_SCREENSHOT`, `BUILDER_PIN_TYPO=FIXED_IN_GITHUB`, `H2AI_IMAGES=NOT_BUILT`, `STEP05=ACTIVE`, `PRODUCTION=OFF_NO_GO`. 
