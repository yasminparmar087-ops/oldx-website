# OLDX Step05 H1B G2A — Owner WSL pre-login STOP; safe Python symlink guard v2

**26 Nov 2026 ~21:23 IST.** User submitted screenshot after running the previously approved G2A first attempt within `OLDX-Ubuntu-24.04` as root. Screenshot: `H1B_G2A_RESULT=STOP`, `H1B_G2A_REASON=BUNDLED_PYTHON_NOT_PRESENT`, returned to `root@DESKTOP-6AUQN5U:/mnt/c/Users/Yasmin Parmar#`. Ubuntu MOTD warning `mv: cannot stat '/var/run/motd.new'` appeared on WSL startup but is unrelated to the reported script STOP; it does not prove a failed WSL launch.

## Exact evidence and bounded interpretation

- G2A v1 pinned commit `4e0a4a99fb163f32fac29b3e3d0da74c161c666a`, Git blob `5f574b57f91b726f82ae71ec830376dde602b24e`, ran and STOPPED at its line requiring `-f`, `-x`, and `! -L` for `.../platform/bundledpythonunix/bin/python3`.
- Prior successful S2 actual owner WSL proof used the *same absolute Python path* and a validated `path.is_file()`/`path.resolve().is_relative_to(SDK.resolve())`/`path.stat().st_uid==0`/executable guard. S2 accepted a safe symlink that resolved inside the extracted native SDK; G2A v1 unconditionally rejected **all** symlinks. This is a **plausible source-level mismatch**; screenshot alone does NOT reveal the actual `python3` symlink/target or prove it is safe. Do not assume Python was deleted or redownload/re-extract native SDK.
- v1 stopped **before** checking the one-shot marker, before creating any marker, before Docker image inspect, before creating G2 credential config directories and before issuing `gcloud auth login`. As per reviewed script path, this attempt made **zero requested Google OAuth, Registry push or Cloud resource writes**. This does not independently prove no external process created the same marker meanwhile; v2 still checks marker absence and refuses a consumed marker.
- DO NOT retry v1 pinned source, delete/reset G1/S1/S2/C1A/G2 markers, run another H1A build/scan, update Windows SDK, modify default Docker or Google credentials, or make Cloud Run/IAM changes.

## v2 fixed new source

- New script: `scripts/step05_h1b_g2_native_wsl_owner_login_and_docker_helper_once_v2_20261126.sh`.
- First immutable commit `8fc2fb5e32c828bc8c9d18330e436159318eaa5c`.
- Exact GitHub blob `2577a278a30e011bb1c6cab24171a9def981fd00`, independently fetched from GitHub branch.
- Changed **only** overly restrictive bundled-Python check: `readlink -e` must resolve the `python3` path; the final target must be **inside the identical root-owned canonical SDK directory**, be executable and root-owned. This permits safe in-SDK symlinks as the older S2 did, while forbidding dangling/outside-target/unowned or unexecutable symlinks. All existing project, Owner, local image ID, distinct root-only configs, single host Docker helper and exact one-shot marker fail-closed restrictions preserved.
- Same old unconsumed marker `/root/.oldx-h1b-g2-wsl-owner-login-once-20261126` is intentionally used, **not reset or deleted**. If marker/credential config already exists, v2 STOPs and must not be re-invoked or circumvented. G2A v2 does not push any image. It may launch ONE supervised owner Google OAuth browser-code flow only if all preflight checks pass. No real local owner WSL execution has yet occurred with v2.
- Syntax is validated on the owner's WSL with `bash -n` **before execution**; no claim that assistant tested against the owner's filesystem. No new Owner consent is needed for this narrow same-G2 pre-login guard correction (within earlier G2 consent).

## NEXT: ONE pinned safe owner Ubuntu WSL paste

You are **already at the Ubuntu root terminal** in screenshot, so do not open another WSL unless that terminal was closed.

```bash
bash -euo pipefail <<'OLDX_H1B_G2A_V2'
umask 077
d=$(mktemp -d /root/oldx-h1b-g2a-v2-source.XXXXXXXX)
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' \
  --output "$d/g2a-v2.sh" \
  'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/8fc2fb5e32c828bc8c9d18330e436159318eaa5c/scripts/step05_h1b_g2_native_wsl_owner_login_and_docker_helper_once_v2_20261126.sh'
test "$(git hash-object "$d/g2a-v2.sh")" = '2577a278a30e011bb1c6cab24171a9def981fd00' || {
  echo 'STOP: SOURCE_HASH_MISMATCH'
  exit 2
}
bash -n "$d/g2a-v2.sh"
bash "$d/g2a-v2.sh" --h1b-g2-owner-wsl-login-once
OLDX_H1B_G2A_V2
```

If `H1B_G2A_STAGE=GOOGLE_BROWSER_SIGN_IN_REQUIRED` appears, do Google OAuth only on a trusted owner browser. **Never share OAuth browser URLs/codes/passwords/tokens/screenshots containing them.** When finished, share only sanitized `H1B_G2A_RESULT`/reason lines. If STOP occurs before the marker, report precise reason; if STOP after marker, leave files/marker unchanged and request diagnosis, never replay.

Expected success `H1B_G2A_RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY` and `REGISTRY_PUSH=NOT_ATTEMPTED`. Then prepare later, separately guarded G2B one retained H1A image push within already granted scope and immutable remote digest validation; no W1–W6 Cloud writes, H2 or production.

**Current:** `G1=READ_ONLY_WITH_LIMITS_CONSUMED`; `G2A_V1=PRELOGIN_PREFLIGHT_STOP`; `G2A_V2=SOURCE_PREPARED_NOT_EXECUTED`; `H1B_CLOUD_WRITES=NONE_IN_G2A`; `G2B=NOT_EXECUTED`; `STEP05=NOT_COMPLETE`.
