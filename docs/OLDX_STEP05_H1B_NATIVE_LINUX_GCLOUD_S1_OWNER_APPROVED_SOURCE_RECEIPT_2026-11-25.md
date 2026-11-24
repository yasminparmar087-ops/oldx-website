# OLDX Step05 H1B S1 — owner approval and exact isolated setup runner

**25 Nov 2026 IST.** Branch `security-hardening-review`. This checkpoint supersedes prior S1 NOT APPROVED entries only for the precise **S1 LOCAL SETUP** scope below. It does not supersede historical results, restore used one-shot markers, or authorize any additional task.

## Owner decision and current execution distinction

The owner replied **"ha manjuri chhe"** immediately to the proposal "H1B S1 — સુરક્ષિત Linux SDK ડાઉનલોડ અને અલગ ઇન્સ્ટોલેશન" after reviewing the S0 plan. This is permission for **ONE** Google-official x86_64 Linux archive download, current-version/checksum verification, archive structural safety check and separate extraction into WSL **Linux** storage only. It is NOT consent for S2 `gcloud --version`, S3 active account/project/Registry/service/SA preflight, auth/login/token refresh, Windows SDK/config/credential migration, `install.sh`, global PATH, `sudo apt`/snap, Cloud Run/SA/IAM/Registry/image writes, Firebase/Firestore/KMS, H2 or production.

**Current ACTUAL:** owner WSL has **not** run the new runner as part of this assistant response. S1 is **APPROVED / SOURCE_AND_OFFLINE_TEST_PREPARED / LOCAL_EXECUTION_PENDING**. This assistant cannot access the owner's WSL filesystem. No archive has been fetched or extracted on that machine by this response.

## Official artifact frozen and source audit

On 25 Nov 2026 the Google-official [versioned archive page](https://docs.cloud.google.com/sdk/docs/downloads-versioned-archives) and [install guide](https://docs.cloud.google.com/sdk/docs/install-sdk) both show current `594.0.1`, Linux x86_64 archive `google-cloud-cli-linux-x86_64.tar.gz` at `https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz`, ~94.8 MB, SHA256 **`c6fdba4cb1551b0da7c1d744eb0dfaf68b59861238d6a6b5ef6bad1ba596b567`**. This generic download name may move; the runner makes fresh HTTPS reads of the TWO official documentation pages and requires exactly this release, official link and checksum **before the ONE archive download**. If drift/redirect/net failure occurs, STOP; never auto choose another release.

Exact source runner [`scripts/step05-h1b-native-linux-gcloud-s1-once-20261125.py`](../scripts/step05-h1b-native-linux-gcloud-s1-once-20261125.py): first-containing commit **`d8ba8ce3e927edc352b496184bd18fb8e55d4dfd`**, exact Git blob **`76b04cac78481a8ec9b80248db7656499a1375f6`**, independent local SHA256 **`21aef1ff5e4475b0744de027f223725fd00cdf2db171eca67a7ad051f4928622`**. The GitHub file was read back and matched the exact local test source. No running of scripts in owner WSL or Cloud is asserted.

**One-time behavior:**
- Exact flag `--setup-local-once`, WSL Linux amd64/root/Python>=3.12/2GiB+ free Linux storage and destination/marker collision checks. No WSL/Windows SDK replacement; no global profile or authentication access. Private one-shot marker `/root/.oldx-h1b-native-gcloud-s1-once-20261125`, created **before network** and retained on PASS or STOP. Don't delete/retry marker on failure.
- Official docs HTTPS and exactly one archive HTTPS GET, no redirect/proxy/retry/mirror and bounded downloads (docs 2MiB each; archive 130MiB; time-bound). Private `/root/oldx-h1b-native-gcloud-s1-<UTC>/receipt.json` and downloaded archive retained. Does not print tokens or contents of existing config.
- SHA256 before tar structural inspection; reject traversal, escaping/dangling/cyclic links, devices, duplicates, excessive sizes. Uses Python `tarfile` strict `filter='data'` to extract into **fresh private incomplete staging folder**. Checks `bin/gcloud` and bundled Linux Python exist and have execute bits; moves into **`/root/oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/`** only after validation. Does not **execute** the SDK, `install.sh` or Python found within archive. On STOP, leave private evidence/incomplete staging for manual audit, with no blind retry.
- This guards source and basic archive safety; does **not** establish SDK startup, owner account validity, target IAM or that extracted SDK is sufficient for H1B Cloud use. Main H1A/H1B consumed markers/Cloud resources untouched.

## Exact new test evidence

Focused test [`tests/integration/step05-h1b-native-gcloud-s1-offline.test.py`](../tests/integration/step05-h1b-native-gcloud-s1-offline.test.py), commit **`63b8a40d9269655a21e47a3adca72929f7875e55`**, Git blob **`d046fc36170ac68379d7c8e57092a737fdae61c0`**. Independently tested same exact Git-source bytes in isolated local Python with command `python3 tests/integration/step05-h1b-native-gcloud-s1-offline.test.py` → **5 NEW PASS, 0 FAIL**: valid fake official HTML and release/hash/URL drift, benign fake tar with data-filter extraction, traversal rejection, escaping symlink rejection, and missing flag refusing before any action. `python3 -m py_compile` source PASS. **Synthetic fixtures only:** no real Google archive, WSL install, Cloud, or gcloud test happened in the assistant's container.

## One command for owner WSL (S1 ONLY)

Enter **existing** `OLDX-Ubuntu-24.04` as root. The next **single paste** obtains the immutable pinned GitHub script into a NEW private WSL Linux temp folder, requires the locally tested SHA256 to match, then performs exactly one S1 attempt:

```bash
set -euo pipefail; umask 077; d="$(mktemp -d /root/oldx-h1b-s1-source.XXXXXXXX)"; curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/s1.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/d8ba8ce3e927edc352b496184bd18fb8e55d4dfd/scripts/step05-h1b-native-linux-gcloud-s1-once-20261125.py'; printf '%s  %s\n' '21aef1ff5e4475b0744de027f223725fd00cdf2db171eca67a7ad051f4928622' "$d/s1.py" | sha256sum --check --status; python3 -B "$d/s1.py" --setup-local-once
```

If immutable GitHub source fetch/check fails, local S1 runner never starts and S1 marker stays unused; STOP and report exact error rather than retyping a different URL or switching accounts. If S1 runner prints `S1_RESULT=STOP` (or any STOP code), marker will be consumed and no second run is approved. Retain local evidence privately; only share `S1_RESULT`, `S1_STOP_REASON`, `S1_EXPECTED_SHA256`, local receipt hash, without credentials or private path dumps. `S1_RESULT=S1_COMPLETE_NO_CLI_EXECUTION` means extraction succeeded, **NOT S2 PASS**.

## Next independent boundaries and expiry

- **S2 requires separate consent** for at most one isolated absolute-path `.../google-cloud-sdk/bin/gcloud --version`, separate `CLOUDSDK_CONFIG` and bounded diagnostic, *after actual S1 receipt*. **S3 requires separately authorized** owner/project/Registry/new-only collision reads and correct selected credential. **W1–W6 remain entirely NOT AUTHORIZED.** No original one-shot 40s auth-list / 12s version timeout retries, no original H1A build/Syft/Grype/runtime repeats.
- H1A exact local image PASS_WITH_LIMITS, owner Option B still only the twelve known HIGH findings during future **max24h**, IAM-private, compiled-OFF, no-data H1B risk. New Cloud image, SA, service, IAM, hosted calls, runtime enablement NOT approved. H2 and production NO-GO.
- Prior C1A separate private/OFF retention permission expires **28 Nov 2026 23:19 Asia/Kolkata**; no automatic extension or cleanup. Guarded NEW-only cleanup or fresh retention decision must be made by then, without touching protected old services/assets.

**Canonical state:** `H1B_NATIVE_SDK_S0=COMPLETE`; `S1=OWNER_APPROVED_SOURCE_READY_NOT_RUN_IN_WSL`; `S2/S3=NOT_AUTHORIZED`; `H1B_W1-W6=NOT_AUTHORIZED`; `STEP05=ACTIVE_HOLD`; `PRODUCTION=NO_GO`. All source/files/docs pinned to the review branch, no reset/rebase/force, no historic execution redo.
