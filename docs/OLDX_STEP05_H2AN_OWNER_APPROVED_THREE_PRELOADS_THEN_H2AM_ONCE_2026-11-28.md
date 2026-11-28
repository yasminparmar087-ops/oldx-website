# BAJUTO Step05 H2AN — Owner approval, exact THREE private child preloads then ONE H2AM OFF-only acceptance

Date: 28 November 2026 IST. Branch: `security-hardening-review`.

## Actual permission and latest local evidence

User approved the exact single two-phase scope in `docs/OLDX_STEP05_H2AM_LOCAL_PREFLIGHT_3_MISSING_IMAGES_ONE_APPROVAL_2026-11-28.md` with **"ha manjuri chhe"**.

The prior Owner read-only WSL preflight actually found:
- H2AM marker **NOT CONSUMED**; Mediator child image local PRESENT; Gateway, Backend and Reader not confirmed locally.
- Grype v0.122.1 available; local DB directory present; /root 929GiB free (reported); no new scanner/runtime/pulls run in that preflight.
- H2AJ **actual four private image registry push PASS**, consumed; H2AK consumed partial with original Mediator Grype raw report complete **57 findings (18 High / 0 Critical)**, H2AL read-only captured prior main exit1/exec137 (cause still UNKNOWN). NEVER rebuild H2AJ or rescan Mediator.

Owner now authorized exactly:
1. Fresh **temporary private** Docker registry auth based on isolated, existing Owner native gcloud identity `yasminparmar087@gmail.com` / project `oldx-staging`, with no global config change.
2. At most **ONE** Linux/AMD64 `docker pull` for each of the THREE missing, PREVIOUSLY BUILT private immutable child refs, Gateway, Backend and Reader; verify local RepoDigests, architecture, nonroot config. Do not pull Mediator.
3. Only after four local refs and Grype DB verified, one **existing source H2AM** OFF-only selective acceptance attempt: first Mediator runtime **WITHOUT re-scanning** original 57-findings report, then if PASS one Grype scan and OFF runtime each for Gateway, Backend and Reader. Stop immediately on error, preserve private receipts, no retries/marker resetting.
4. **No** images build/push, IAM/KMS/Firebase operations, real users, Cloud Run deployment, production activation, automatic DB updates, old tests/CI/scans. Registry read/egress may incur usual charges. Residual security findings remain HOLD for separate risk disposition.

## New H2AN one-pass orchestrator

Pushed `scripts/step05_h2an_three_pinned_preloads_then_h2am_once_20261128.py`. Its exact Git blob is `f20025ada53ee8be6d22d9ec7e063633cd0cb514`, immutable creation commit `6a224823050e130dad96e21f70c6ab108b03dd39`.

Guards:
- Prewrite verifies root WSL, old H2AJ and H2AK consumed markers, new H2AM/H2AN markers absent, original Mediator raw Grype report's exact SHA256 `e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92`, isolated active Owner project, Docker Linux, existing native Grype executable+DB `grype db status -o json` with auto-update disabled and at least 4GiB private root space.
- Downloads ONLY the **three exact immutable GitHub files** from commit `8f5df51075d6cc42f0d32ad0c730b14611c03f87` into a freshly created root-private `source/scripts/` and `source/deployment/four-role/`: runner Git blob `3adfb06ca66d6175f089ea797df21ca767779cca`, support `b9b57daa9a5b5f0304afc9cfc758630793454c07`, proposal `c1cfcfa2f224e9a47dd6e896730c73e927b9b483`. Confirms git object SHA1 for all and Python syntax compile (does NOT repeat the already completed 19 focused tests); frozen image/role pins OFF.
- Inspects already-local exact child images read-only. Only when a missing child is confirmed does it obtain ONE short-lived Owner OAuth token and `docker login --password-stdin` in its own isolated `DOCKER_CONFIG`. Creates a **new separate exclusive H2AN preload marker** `/root/.oldx-step05-h2an-three-pinned-preloads-once-20261128` BEFORE the first pull; records each one attempt and digest readback. On ambiguous/failed pull after marker, STOP; **NEVER rerun, force-delete or reset marker**. Does not call any Docker push/build/delete.
- Removes ONLY its own temporary Docker auth config, independently verifies ALL FOUR local child references and only then launches the separately approved **unchanged** H2AM one-shot, no pull/auth flags. H2AM maintains its own distinct existing marker `/root/.oldx-step05-h2am-selective-off-runtime-three-scans-once-20261128`, and can fail with durable receipts. No H2AN auto-retry if H2AM stops.
- No live cloud service mutation. The Owner must run this locally; GitHub push does not perform it.

## ONE WSL root copy-paste — execute only once

```bash
umask 077
test ! -e /root/.oldx-step05-h2an-three-pinned-preloads-once-20261128 &&
test ! -e /root/.oldx-step05-h2am-selective-off-runtime-three-scans-once-20261128 &&
d=$(mktemp -d /root/oldx-h2an-approved.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2an.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/6a224823050e130dad96e21f70c6ab108b03dd39/scripts/step05_h2an_three_pinned_preloads_then_h2am_once_20261128.py' &&
test "$(git hash-object "$d/h2an.py")" = 'f20025ada53ee8be6d22d9ec7e063633cd0cb514' &&
python3 -B -c 'import ast,sys;ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2an.py" &&
python3 -B "$d/h2an.py" --owner-approved-exact-three-preloads-then-one-h2am-off-only
```

If preflight fails before H2AN marker, **no pull has started**. If `H2AN_PRELOAD_MARKER=CONSUMED_NO_REPEAT` appears, **DO NOT RERUN**, even on subsequent failure. If `H2AN_H2AM=START_ONE_APPROVED_SELECTIVE_ATTEMPT` appears, H2AM may consume its own marker and run selective runtime/scans, also never rerun. A new failure requires reading the exact local receipt, not re-executing this command.

**Status at authoring:** `H2AN=OWNER_APPROVED_SOURCE_READY_NOT_RUN`; `THREE_LOCAL_PULLED=NOT_VERIFIED`; `H2AM=NOT_EXECUTED`; `MEDIATOR_OLD_SCAN=COMPLETE_NO_REPEAT`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
