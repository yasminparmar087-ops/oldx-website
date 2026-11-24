# OLDX Step05 H1B — gcloud local WSL startup timeout: diagnosis boundary and source handoff

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
