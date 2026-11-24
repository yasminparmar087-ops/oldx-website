# OLDX Step05 H1B — gcloud local WSL startup timeout: diagnosis boundary and source handoff

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
