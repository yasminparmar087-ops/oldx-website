# OLDX Step05 H1B — gcloud local WSL startup timeout: diagnosis boundary and source handoff

## 25 Nov 2026 — H1B S0 native Linux gcloud ISOLATED SETUP-PLAN PREPARED SOURCE-ONLY; S1 NOT AUTHORIZED

Fresh verified starting HEAD `83145a33c94c16d73dca61199f50f9437a0e8dae`, original passive launcher/Issue17 real evidence consumed, no repeat. CONFIRMED Windows-mounted regular `gcloud` launcher `#!/bin/sh`, 6494B/212 lines/0CRLF/no symlink, Linux bundled Python missing and installed Windows SDK's interpreter probe; native Linux `python3` found but exact SDK stall UNKNOWN. One 40s `auth list` and one 12s `--version` previously timed out124, corresponding markers CONSUMED. No credentials/IAM fault proven, no operator/project/Registry/new service/SA target readbacks yet. Passive SHA256SUMS `61e4990035bce90923fefce882566170ba0d94d005188a5052d2d0f9c3aabd70` preserved privately.

NEW [canonical isolated native Linux gcloud SDK setup-plan](docs/OLDX_STEP05_H1B_NATIVE_LINUX_GCLOUD_ISOLATED_SETUP_PLAN_2026-11-25.md) on this branch; **S0=SOURCE_ONLY_PLAN_PREPARED**, **S1=NOT_APPROVED/NOT_EXECUTED**. Proposed official Google Linux x86_64 bundled-Python archive ~94.8MB; Google official 25Nov-reviewed page labels v594.0.1 SHA256 `c6fdba4cb1551b0da7c1d744eb0dfaf68b59861238d6a6b5ef6bad1ba596b567` (frozen doc data, actual archive NOT downloaded, dynamic filename may change; verify current official exact release+matching hash before extraction, STOP on drift). New private `/root/oldx-tools/native-gcloud-594.0.1` on WSL Linux filesystem, no `sudo apt`/snap/Windows SDK replacement or `/mnt/c` mount; no global PATH/installer/init/credential/config migration. Proposed S1 permits only one future owner-approved verified download/archive structural safety/extraction, **no executable gcloud probe**. S2 separate local `--version` approval, S3 separate operator/project/target read-only approval, W1–W6 H1B Cloud writes separately prohibited until exact consent. Installation may not resolve original root cause and will not automatically inherit credentials.

No script/download/install/SDK process/auth/preflight/Docker/Syft/Grype/Cloud push/deploy/IAM/Firebase/KMS/production action occurred. H1A PASS_WITH_LIMITS old image retained, all markers consumed. Option B only 12 HIGH PRIVATE/OFF/no-real-data max24h risk accepted, H1B operational NOT authorized, H2/production NO-GO. Old C1A private OFF retention expires **28 Nov 2026 23:19 IST** without automatic extension/cleanup. **ONE next OWNER decision:** approve/refuse only S1 official archive download, hash/structure validation and isolated Linux extraction, NO CLI invocation.

## 25 Nov 2026 — ONE passive launcher inspection complete; mixed Windows-SDK/WSL startup implicated, exact stall UNKNOWN

Start remote HEAD `4a5a47c268145f3174b7ff4849cd05b1b6ef645a`; latest AGENTS/current diagnosis/Issue17 read. **Strictly passive local evidence, no SDK launcher/Python interpreter executed.** A single35s-bounded shell inspection completed exit0 in existing owner `OLDX-Ubuntu-24.04`. Source capture limited to installed212-line6494B launcher and a bounded excerpt of6579B gcloud.py (each capped20KB/260lines), path/symlink/file metadata and candidate executable resolution only. Later reading already-captured evidence added no live inspection. Existing consumed markers/credentials/config/PATH/WSL settings untouched; new passive inspection marker preserved. Dirty repo files/.firebaserc unchanged; intended documentation only.

### Classified actual findings
| Classification | Evidence / meaning |
| --- | --- |
| **CONFIRMED** | Resolved gcloud launcher is a regular6494B file on a Windows-mounted SDK, **0 symlink hops**; not a native-Linux SDK root. Full private path/chain saved locally, not published |
| **CONFIRMED** | Shebang `#!/bin/sh`; 212lines, **0CRLF**. No observed CRLF/shebang line-ending fault. Native Linux sh/bash candidates present; no interpreter executed |
| **CONFIRMED** | Launcher defines its own SDK-root resolver/Python setup; final line212 execs selected `CLOUDSDK_PYTHON` plus args and root-relative `lib/gcloud.py`. That6579B Python entrypoint exists, prepends SDK lib/third_party to sys.path and imports googlecloudsdk modules |
| **CONFIRMED** | Linux bundled `platform/bundledpythonunix/bin/python3` absent; Windows bundled `platform/bundledpython/python.exe` and `bin/gcloud.cmd` present. Their mere presence does NOT prove either ran |
| **CONFIRMED** | With CLOUDSDK_PYTHON unset and no Linux bundle selected, launcher optionally sources an enabled SDK config virtualenv, then tries `python3.14, python3.13, python3.12, python3, python3.11, python3.10, python` in that order. Each candidate invokes a silent `-c` version check (accepted3.9–3.14); output redirected to /dev/null, no per-candidate timeout in source |
| **CONFIRMED** | Passive current PATH lookup finds native-Linux `python3`, no `python`, and Windows-mounted `python.exe`. Does NOT establish native python3's version or which earlier versioned candidates exist/execute |
| **CONFIRMED** | Launcher refs include CLOUDSDK_ROOT_DIR/PYTHON/PYTHON_ARGS/PYTHON_SITEPACKAGES/GSUTIL_PYTHON/BQ_PYTHON/CONFIG/ENCODING, PYTHONHOME, VIRTUAL_ENV, PYTHONIOENCODING and optional CLOUDSDK_USE_GOCLOUD. This is STATIC variable-name logic, not printed runtime values. Old approved metadata showed no CLOUDSDK_PYTHON/config/PYTHONPATH override |
| **CONFIRMED** | Hypothetical `bin/bootstrapping/bootstrapping.sh` file is absent, but captured launcher is self-contained and does not reference that helper. **Not evidence of a required missing dependency** |
| **LIKELY** | Using a Windows SDK tree from WSL, lacking its Linux bundle, exposes automatic interpreter selection/possible virtualenv startup and SDK module loading from mounted Windows storage. This mixed-layout startup path is the leading hypothesis for the earlier silent12s version/40s auth-list timeouts, rather than a demonstrated Cloud API error |
| **UNKNOWN** | Actual selected Python, each versioned-candidate resolution, SDK virtualenv enabled state, exact syscall/import/interop at stall, config/module/dependency completeness, filesystem/AV latency and supported native-Python version. No performance trace or new execution allowed, so no definitive root cause |
| **UNKNOWN** | Account/credential validity, operator/project/Registry/new SA/service collision and IAM. This passive evidence establishes NONE of them |

Do **NOT** claim Windows bundled python.exe was automatically selected: the observed shell source tests Linux bundled locations and PATH names, not that Windows executable. Do not blame CRLF, missing optional bootstrapping helper, credentials or IAM from this evidence. Most likely startup stage is before/during interpreter selection or mounted-SDK module imports, but exact stage remains UNKNOWN.

### Safest/quickest proposed fix — not performed
Prefer a **separate native Linux Cloud SDK placed on WSL's Linux filesystem with its matching supported/bundled Linux Python**, invoked via explicit path. This removes the observed Windows-mounted tree and missing-Linux-bundle mismatch without overwriting the working Windows SDK. It should reduce these startup risks, **not a proven cure**. Do not copy credential DBs, reauthenticate, globally change PATH/CLOUDSDK_PYTHON, replace SDK config or migrate accounts under this finding. Download/source-integrity/platform selection and any installation are a **new explicit owner-approved setup scope**, not this passive task; no software installed/switched now. Even successful local native startup later would not authorize auth-list/preflight repetition or Cloud writes.

A process-scoped existing-native-Python binding could bypass the source's automatic candidate loop without installation, but would still load the Windows-mounted SDK and native Python compatibility is unverified; it is not presented as a proven permanent repair or executed here.

### Private evidence and no-repeat custody
Private directory `/root/oldx-h1b-passive-launcher-20261124T204131Z` (~25Nov02:11:31IST), umask077/0700. Exact resolved paths and interpreter candidates only in private files, not stdout/GitHub. No credential/account/environment values read or published.
- `SHA256SUMS` SHA256 **`61e4990035bce90923fefce882566170ba0d94d005188a5052d2d0f9c3aabd70`**.
- Captured complete launcher `source-bin_gcloud.txt` SHA256 `03d163265c038e9a67b0760ed98de9b5970c4c9d172dbfec03384939d02d4800`.
- Captured `source-lib_gcloud.py.txt` SHA256 `c8acc602cebef4ca64ecfdb4f531718dd2dce85a86c735a52530f9555eb02962`.
- `summary.txt` SHA256 `861c748e7f7332a9aa62a7591eb32925cd97cd48450802c194370acc28a93589`.
Source snippet/metadata files stay private. Passive marker `/root/.oldx-h1b-passive-launcher-inspection-once-20261125` retained. No previous scripts/probes run; no gcloud/interpreter/Python version execution, auth/login/Cloud API, Docker/scanners, installs/config/credential/environment/IAM/Billing changes.

**ONE next owner action:** approve/reject an **isolated native-Linux SDK setup plan** (official-source integrity/platform verification, separate WSL-Linux directory, existing Windows SDK/auth/config left intact; no login, Cloud/preflight execution). Any later startup verification is a distinct bounded approved step, not automatic under this passive result. No repair executed.
H1B OPERATIONAL=HOLD / H2=HOLD / production NO-GO; OptionB exact private/OFF max24h risk only unchanged, no activation. C1A retention28Nov2026 23:19IST unchanged, no auto cleanup. Final pushed/read-back SHA is in accompanying Issue17 checkpoint and containing docs commit.


## 25 Nov 2026 — actual ONE owner-WSL local gcloud diagnostic: VERSION TIMEOUT124, no Cloud query

Starting remote HEAD `2624c88d61b1e441cee42ca103343e4ea47b7f9a`. Read latest AGENTS, this diagnosis document and Issue17 checkpoint7143708788. Approved script Git blob **`59e9d20d4d82ec6d0783cabeec5f358af89e3b8e`** matched exact isolated local bytes; `bash -n` PASS exit0 without Cloud request. Dedicated marker initially ABSENT; original preflight/H1A markers not modified.

Ran exactly ONCE in owner `OLDX-Ubuntu-24.04`:
`bash scripts/step05-h1b-gcloud-local-timeout-diagnosis-once-20261125.sh --diagnose-local-once`.
Only passive local metadata + one `timeout --signal=TERM --kill-after=2s 12s gcloud --version`. **Saved version.exit=124 (timeout)**; version stdout0B/stderr0B. Script emitted `H1B_GCLOUD_STARTUP=VERSION_TIMEOUT_OR_KILLED_STOP`, `H1B_LOCAL_DIAG_EXIT=2`; outer WSL wrapper exit1 observed. Distinguish inner SDK-probe timeout124 from diagnostic script2. No retry or second SDK process. Marker now CONSUMED `/root/.oldx-h1b-gcloud-startup-diagnosis-once-20261125`; never remove/rerun.

### Actual passive findings and interpretation
- `gcloud_executable_found=YES`, install path class **WINDOWS_MOUNT_PATH**; regular launcher file6494B. WSL2 kernel6.18.58.1-microsoft-standard-WSL2. Raw installed path not published.
- CLOUDSDK_CONFIG / CLOUDSDK_PYTHON / active-configuration / PYTHONPATH override presence allNO; HTTP(S)/NO_PROXY presence allNO. These are presence checks only, not exported environment values.
- Default SDK config directory present; credential/token DB files present mode600; only stat metadata inspected, **no contents/auth validity/account identity read**. Presence does not prove usable credentials. No matching process names recorded by pre-probe snapshot; not proof of absence of transient startup children later.
- **Possible cause, explicitly unconfirmed:** WSL resolving a Windows-mounted SDK launcher may involve cross-filesystem startup or launcher/interpreter path behavior. This observation does NOT establish the root cause, wrong credentials, invalid account, permissions, network issue or corrupt SDK. Generic SDK startup itself failed to finish within12s; original40s auth-list timeout is still unresolved.
- No auth list/login/refresh/token/config change/install or Cloud project/Registry/service/SA/IAM/hosted endpoint query. Original consumed preflight NOT repeated; all operator/project/collision findings remain UNKNOWN. No builds/scans/push/deploy/Cloud writes.

### Private evidence / checksum
Directory `/root/oldx-h1b-gcloud-startup-diagnosis-20261124T203450Z` (25Nov2026 ~02:04:50IST start), private0700/umask077, saved outputs retained:
- `SHA256SUMS` SHA256 **`bd3826284e9c103cd1a3b8e05a6871f777a5eda71d66ce103f078128a56d8df1`**.
- `local-metadata.txt` SHA256 `9ea1423fa53fc07201e8543c709b550884077a6c66d60f1253e3d1e03ae78ab9`.
- `version.exit` SHA256 `ca2ebdf97d7469496b1f4b78958f9dc8447efdcb623953fee7b6996b762f6fff`.
- version stdout/stderr both empty SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Only nonsensitive result/path-class/hash summary saved in GitHub, not full private SDK metadata/log/credential contents. Dirty local Handoff/untracked.firebaserc preserved; intended documentation only.

**Next ONE action:** separately scoped read-only inspection of the resolved Windows-mounted gcloud launcher and its interpreter selection, **without starting gcloud again**, changing environment/config/credentials, installing software or querying Cloud. This is a proposed different diagnosis, not authorized/executed by this consumed probe. Do not infer permission to lengthen timeout, retry --version/auth list or rerun original preflight.
`H1B_LOCAL_DIAG=VERSION_TIMEOUT124_CONSUMED`; `H1B_CLOUD_WRITES=NOT_AUTHORIZED`; `H2=HOLD`; Step05 NOT DONE / production NO-GO. OptionB private/OFF max24h risk only unchanged, no activation. C1A retention through28Nov2026 23:19IST unchanged, no auto cleanup. Final pushed/read-back SHA in Issue17 checkpoint and containing documentation commit.


## 25 Nov 2026 — OWNER APPROVAL FOR ONE LOCAL-ONLY DIAGNOSTIC (NOT RUN YET)

The owner explicitly answered **"ha manjuri chhe"** to the exact question whether to run **ONE** 12-second maximum local `gcloud --version` startup diagnosis in the existing owner WSL environment. This supersedes the historical "not yet approved" status **for this diagnostic only**. Scope: `scripts/step05-h1b-gcloud-local-timeout-diagnosis-once-20261125.sh`, source Git blob `59e9d20d4d82ec6d0783cabeec5f358af89e3b8e`, exactly **`--diagnose-local-once`**; execute at most once after checking dedicated diagnostic marker ABSENT. Read ONLY local SDK executable/config/credential-file **metadata** without contents, environment override presence and process names; start only a bounded local `gcloud --version` process; save private WSL evidence/exit/status/checksums. Never delete the old consumed `~/.oldx-h1b-readonly-preflight-once-20261125` marker. No original `gcloud auth list` replay, project/SA/Cloud Run/Registry lookup, account login/logout, credentials or config change, CLI install/upgrade, IAM/Cloud writes, image/push/build/scan, or hosted calls. If initial dedicated marker exists or tool fails/timeouts, **STOP** with actual evidence; no retry. `gcloud --version` success proves local startup only, never account validity or target collision.

**Current execution fact:** this ChatGPT tool environment is not the owner's Windows WSL session; neither this diagnosis nor any Cloud operation was executed here. No synthetic-only test result is a live result. Next action is one owner-local Codex/WSL invocation with the exact approved script and Git blob verification, then preserve private evidence and update Issue #17 with safe status only. `H1B_LOCAL_DIAGNOSTIC=APPROVED_NOT_EXECUTED`, `H1B_READONLY_ORIGINAL=STOP_TIMEOUT_CONSUMED`, `H1B_WRITES/H2/PRODUCTION=NOT_AUTHORIZED`. C1A independent OFF-only retention deadline remains **28 Nov 2026 23:19 IST**.

**25 November 2026 IST — preparation SOURCE-ONLY; no owner authorization for the NEW local diagnostic yet.**

## Frozen actual H1B P-phase STOP

Original one-shot preflight from source Git blob `14703d1257c99701e4873be598b5aedc0d5c33b4` was invoked exactly once in owner `OLDX-Ubuntu-24.04` and STOPPED at first `timeout 40s gcloud auth list --filter=status:ACTIVE --format=value(account)` with **exit124 and zero-byte stdout/stderr**. No project/Registry/Cloud Run service/SA read, no 403/404, collisions UNKNOWN, no operator identity proven, no Cloud writes. Original marker `/root/.oldx-h1b-readonly-preflight-once-20261125` is **PRESENT/CONSUMED**. Never delete/reset or invoke the original preflight again. Original private evidence `/root/oldx-h1b-readonly-preflight-20261124T202258Z`, `SHA256SUMS` SHA256 `22b2f89ffc7c70be6ad82398e64d8c42170c646669d5399ae4c44622d96d5b1e`. [Original Issue #17 H1B STOP receipt](https://github.com/yasminparmar087-ops/oldx-website/issues/17#issuecomment-7143540822).

A timeout alone does NOT prove bad credentials, IAM issues, missing account, network, broken SDK or service collision. [Google Cloud documentation](https://docs.cloud.google.com/sdk/gcloud/reference/auth/list) describes `gcloud auth list` as listing stored credentialed accounts and the active account; it is distinct from hosted resource checks. Do not immediately reauthenticate/revoke or switch accounts.

## NEW source-only bounded local diagnosis (not executed on owner's WSL)

NEW `scripts/step05-h1b-gcloud-local-timeout-diagnosis-once-20261125.sh` **exact Git blob `59e9d20d4d82ec6d0783cabeec5f358af89e3b8e`**.

- Requires **one new separate owner approval** to run, with exact single flag `--diagnose-local-once`. An unrelated `ok aagal vadho` or previous original preflight approval is not authority to execute it.
- Distinct diagnostic one-shot marker `~/.oldx-h1b-gcloud-startup-diagnosis-once-20261125` refuses repeat (old H1B P-phase marker is untouched).
- Collects only local SDK executable **path class** (Linux vs Windows mount), file types, modes, sizes, mtime, presence flags for Cloud SDK/Python/proxy overrides (NO actual values), metadata of Cloud SDK config dir / auth DB files (NO contents), and matching local process **names**, not process arguments.
- Starts at most **one** bounded `timeout --signal=TERM --kill-after=2s 12s gcloud --version`, with prompts/updates/usage reporting disabled; does **NOT** run `gcloud auth list`, `gcloud auth login`, token refresh, `gcloud projects describe`, repository/SA/Cloud Run APIs, network/hosted checks, installed-component update or any Cloud write.
- Preserves private `0700` home evidence directory, local text outputs, SHA256SUMS and separate consumed marker. No credential/account email/token/SDK config content is read, copied or published. `--version` can initialize SDK local logs/cache; it is NOT asserted to be a zero-local-write probe.
- If `--version` exits0, the core SDK can start within twelve seconds **under that invocation only**. This does not prove `auth list` works or identify account/project/resources. If exit124/137 or other error, STOP with type and private stderr; no retries or auto fixes. Do not assume cause or permission state.
- Exact source file locally verified with `bash -n` PASS, no-args exit2 PASS, **ONE synthetic fake-gcloud `--version` invocation PASS**, and fake second invocation denied by consumed marker (exit2) PASS. Local source Git blob and GitHub read-back matched. These were *synthetic tests only*, NOT live WSL / actual Google SDK operation.

## Next decision and non-repeat custody

**Next one owner approval (not yet given):** one LOCAL read-only metadata + one `gcloud --version` max12s check on owner WSL using the exact Git-blob-approved script, without any active operator/resource request, login, credential/SDK install/config change or Cloud write. If approved, execute exactly once using **existing isolated verified repo**:

`bash scripts/step05-h1b-gcloud-local-timeout-diagnosis-once-20261125.sh --diagnose-local-once`

After actual run, save only status/exit code, private evidence checksum and accurate limitations to GitHub branch `security-hardening-review` / Issue #17. **Never** share private SDK config/database/log content. If local root cause remains unknown, schedule a different limited diagnosis only after separate owner decision. **Do not rerun original H1B preflight automatically** on any diagnosis outcome.

**Separate H1B operational W1–W6 cloud writes remain unauthorized.** Owner's H1B Option B risk acceptance covers only 12 known HIGH CVEs, the exact private OFF-only no-data candidate, max24h *if later activated*. Existing H1A image/scan/runtime and H1B P-phase run all consumed; do not rerun. Existing C1A OFF-only service retention ends **28 November 2026 23:19 IST** independently; no automatic cleanup/extension. `H1B_READONLY=STOP_OPERATOR_TIMEOUT`, `H1B_LOCAL_DIAGNOSTIC=PREPARED_NOT_APPROVED_OR_RUN`, `H1B_WRITES=NOT_AUTHORIZED`, `H2/STEP05_LIVE/PRODUCTION=HOLD_OR_NO_GO`.
