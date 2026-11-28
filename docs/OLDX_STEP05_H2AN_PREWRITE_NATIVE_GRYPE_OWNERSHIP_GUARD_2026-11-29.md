# BAJUTO / OLDX Step05 — H2AN first Owner PRE-PULL STOP (NATIVE_GRYPE_MISSING), guarded local binary ownership correction

Date: 2026-11-29 ~00:00 IST; Owner Windows 10 WSL-root screenshot. Branch `security-hardening-review`.

## Actual output / execution state

The owner executed the previously approved SHA-pinned H2AN preload+H2AM one-pass runner. The screenshot shows:

```text
H2AN_RESULT=STOP_BEFORE_ANY_PRELOAD
H2AN_REASON=NATIVE_GRYPE_MISSING
```

Previous earlier-in-screenshot read-only H2AM preflight had reported `GRYPE=AVAILABLE` and `GRYPE_DB_DIRECTORY=PRESENT`, Mediator image locally available, other 3 images not confirmed. Owner H2AK previously executed **installed Grype v0.122.1 linux/amd64** and checked official release tarball SHA256. Therefore this is not proof that Grype was uninstalled.

**IMPORTANT:** H2AN stopped BEFORE its new preload marker, before any Docker image pull, scan, Grype DB update, container execution, H2AM marker, Cloud writes or deployment. Old H2AJ four image push PASS, original Mediator Grype 57 findings/18 HIGH/0 Critical, H2AK consumed, H2AL read-only and the Codex 19 H2AM offline tests remain unchanged. Do NOT repeat any prior Docker builds or scans. H2AN and H2AM markers were NOT consumed according to this screenshot.

## Exact code reason, verified immutable GitHub blob

`scripts/step05_h2an_three_pinned_preloads_then_h2am_once_20261128.py` Git blob `f20025ada53ee8be6d22d9ec7e063633cd0cb514`:

```python
GRYPE=ROOT/'oldx-tools/grype-v0.122.1/grype'
# in preflight()
require(GRYPE.is_file() and os.access(GRYPE,os.X_OK)
        and GRYPE.stat().st_uid==0,'NATIVE_GRYPE_MISSING')
```

This is a **combined predicate**: missing file, nonexecutable file, OR non-root ownership give the SAME failure. Earlier successful `grype version` establishes a working binary on `PATH` at that time, **not the exact file ownership**. One plausible cause is default root GNU `tar` behavior preserving the archive's source UID during extraction; it is not proven without `stat`. Official GNU tar manual: https://www.gnu.org/software/tar/manual/tar.html .

Do not change the old one-shot runner or its preflight without evidence. Use the existing, already-downloaded official Linux Grype binary. Correct **only root owner/group** on this exact validated native executable if UID isn't 0. Keep the file path/version/bytes unchanged. No reinstall, download of Grype, re-scan, new credentials or marker reset.

## ONE standalone WSL-root command: guarded local fix then same approved H2AN once

```bash
umask 077
G=/root/oldx-tools/grype-v0.122.1/grype
test -f "$G" && test ! -L "$G" && test -x "$G" &&
"$G" version | grep -F '0.122.1' &&
echo "GRYPE_OWNER_BEFORE=$(stat -c '%u:%g' "$G")" &&
{ test "$(stat -c '%u' "$G")" = 0 || chown root:root -- "$G"; } &&
test "$(stat -c '%u' "$G")" = 0 &&
echo "GRYPE_OWNER_AFTER=$(stat -c '%u:%g' "$G")" &&
test ! -e /root/.oldx-step05-h2an-three-pinned-preloads-once-20261128 &&
test ! -e /root/.oldx-step05-h2am-selective-off-runtime-three-scans-once-20261128 &&
d=$(mktemp -d /root/oldx-h2an-grype-fixed.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2an.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/6a224823050e130dad96e21f70c6ab108b03dd39/scripts/step05_h2an_three_pinned_preloads_then_h2am_once_20261128.py' &&
test "$(git hash-object "$d/h2an.py")" = 'f20025ada53ee8be6d22d9ec7e063633cd0cb514' &&
python3 -B "$d/h2an.py" --owner-approved-exact-three-preloads-then-one-h2am-off-only
```

This is a **prewrite correction after a prewrite STOP**, not a replay of a consumed pull or scan attempt. If a precheck fails, the chain stops before H2AN. If H2AN prints `H2AN_PRELOAD_MARKER=CONSUMED_NO_REPEAT`, DO NOT rerun on subsequent failure; record the outcome and preserve original markers/evidence. If `H2AN_H2AM=START_ONE_APPROVED_SELECTIVE_ATTEMPT`, the separate H2AM marker may be consumed; likewise never repeat.

If file is actually missing or not executable, the command reports failure before trying any pull; do not invent a different installation. If UID was nonroot and becomes root, that confirms the likely diagnosis.

No production enablement, Cloud Run, IAM, KMS, Firebase, new Docker image build or registry push approved. Only the previously approved three digest-pinned registry *reads/pulls* and selective local OFF-only acceptance follow, if all guards pass. Grype database `status` is checked without auto-updating.

**Current:** `H2AN=FIRST_PREPULL_STOP_NATIVE_GRYPE_CHECK`, `H2AM=NOT_STARTED`, `THREE_PRIVATE_PULLS=NOT_STARTED`, `H2AJ_REGISTRY_4=PASS`, `MEDIATOR_OLD_GRYPE=COMPLETE`, `STEP05=ACTIVE`, `PRODUCTION=OFF_NO_GO`.
