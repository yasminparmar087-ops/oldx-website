# BAJUTO / OLDX Step05 H2AK — Owner PRE-READ STOP, exact H2AJ marker format fixed

Date: 28 November 2026 (IST, ~21:25). Branch: `security-hardening-review`.

## Exact observed screenshot

Owner executed first SHA-pinned H2AK local reader/scanner script, and it printed:

```text
H2AK_RESULT=STOP_BEFORE_IMAGE_READ
H2AK_REASON=H2AJ_SUCCESS_NOT_RECORDED
```

The script stopped **during preflight** BEFORE any new H2AK marker, private image pull, Grype scan, temporary Docker container, image runtime health check, or Cloud write. H2AJ already **SUCCESSFULLY pushed four images**, as shown in the same screenshot's prior output `H2AJ_RESULT=PASS_FOUR_NEW_PRIVATE_OFF_IMAGES`. Do not rebuild/push, reset old markers or infer H2AJ reverted.

**Precise cause:** H2AJ writes the *marker file* as `RESULT=PASS_FOUR_NEW_PRIVATE_OFF_IMAGES` via `mark("RESULT="+result)`. It prints a separate **console** line `H2AJ_RESULT=PASS_FOUR_NEW_PRIVATE_OFF_IMAGES`. The H2AK preflight incorrectly demanded that console prefix inside the marker file, so a valid H2AJ marker was falsely rejected.

## Actual minimal code fix, no Cloud operation

Updated ONLY `scripts/step05_h2ak_four_pinned_new_images_scan_offhealth_once_20261128.py` with correct exact line `RESULT=PASS_FOUR_NEW_PRIVATE_OFF_IMAGES`, checked as a complete marker-file line, AND validated one and only one exact `ROLE=<role> REGISTRY_INDEX=sha256:<64-hex> AMD64_CHILD=sha256:<approved-64-hex>` marker line for each of the four pinned roles. Reject duplicate/incorrect/malformed digests; do NOT weaken the H2AJ proof. Fixed script creation commit `809197dc24e5aa389106dea715fa82fa6ffbb549`, readback Git blob `f9b6f2f15cd1c5a59405d33f09e158434b7c2773`.

New small *offline marker-format logic* checks: 4/4 PASS (valid H2AJ marker accepted; console-only result rejected; tampered child digest rejected; duplicated role record rejected). These exercise the fixed validation logic with synthetic marker lines, **not a live WSL integration test or image scan**. Dockerfile tail/entrypoint/nonroot defaults and source OFF server health behavior also reviewed; no image build or deployment was performed.

**Current H2AK one-shot marker is NOT CONSUMED from the user screenshot.** Only a later output `H2AK_MARKER=CONSUMED_NO_REPEAT` should be treated as consumed. Never reset either prior H2AI/H2AJ marker; H2AJ completed PASS and four images remain pinned. No earlier tests/builds/scans repeated.

## Owner one-paste WSL root continuation using corrected immutable runner — prewrite resume

```bash
umask 077
test -f /root/.oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128 &&
test ! -e /root/.oldx-step05-h2ak-four-pinned-image-acceptance-once-20261128 &&
d=$(mktemp -d /root/oldx-h2ak-marker-fixed.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ak.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/809197dc24e5aa389106dea715fa82fa6ffbb549/scripts/step05_h2ak_four_pinned_new_images_scan_offhealth_once_20261128.py' &&
test "$(git hash-object "$d/h2ak.py")" = 'f9b6f2f15cd1c5a59405d33f09e158434b7c2773' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ak.py" &&
python3 -B "$d/h2ak.py" --h2ak-four-h2aj-images-scan-offhealth-local-only-once
```

This one command checks for Grype and Docker before H2AK marker; if either is missing it stops with no image scans/marker. On success it will perform **only** four new digest-pinned read-only Docker pulls / Grype JSON scans / `--network none` nonroot OFF health, and store private receipts, no build/push. If `H2AK_MARKER=CONSUMED_NO_REPEAT` appears, do **not** rerun the script even if it stops: collect private evidence and reconcile. If Grype severity Critical/High findings appear, record and explicitly disposition rather than claim automatic security GO.

**Current checkpoint:** `H2AJ=ACTUAL_FOUR_PRIVATE_REGISTRY_PASS_CONSUMED_DO_NOT_REPEAT`; `H2AK=PREWRITE_FALSE_STOP_FIXED_SCRIPT_PUSHED_NOT_YET_RUN`; `H2AK_MARKER=NOT_CONSUMED_AS_SCREENSHOT`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
