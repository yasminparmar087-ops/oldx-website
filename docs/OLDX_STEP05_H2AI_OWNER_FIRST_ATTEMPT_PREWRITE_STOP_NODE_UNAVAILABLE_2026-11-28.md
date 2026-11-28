# BAJUTO / OLDX Step05 — H2AI first Owner WSL attempt: six new tests PASS, prewrite STOP due to missing Linux Node
Date: 2026-11-28, ~20:37 IST. Evidence: Owner screenshot in chat.
## Exact observed terminal output
```text
Ran 6 tests in 0.004s
OK
H2AI_RESULT=STOP_BEFORE_ANY_CLOUD_REGISTRY_WRITE
H2AI_REASON=NODE_UNAVAILABLE_WSL
H2AI_RETRY=NO_REGISTRY_WRITE_STARTED_CHECK_EXACT_ERROR_FIRST
```
All six NEW focused Python H2AI offline safety tests **PASS**. The H2AI Python runner's `preflight_docker` stopped on `shutil.which("node") is None` before invoking any build, any push, clone, source bundle, or one-shot marker. In the screenshot, NO `H2AI_MARKER=CONSUMED_NO_REPEAT` appeared. Its preflight earlier checked native WSL gcloud owner/project/repository read-only. This is NOT a build/push failure and cannot be advertised as any derived image evidence. Four image digests remain UNKNOWN.

**Do not rerun the six tests.** The existing downloaded, SHA-verified `$d/runner.py` remains in the same WSL root shell if the shell has not been restarted; the Owner can simply run that file once when Linux native Node24+ has been provisioned and Docker buildx availability confirmed. If shell was restarted, re-download exact previously pinned runner with hash validation; DO NOT recreate a consumed marker. Since the marker was NOT created in the observed attempt, this is a safe pre-write resume after fixing the environment, not a consumed cloud operation retry.

Recommended local-only fix: use pre-existing native Linux Node v24 in `/root/.nvm` or `/root/oldx-tools`, otherwise download official Node v24.22.3 linux-x64 tarball from `https://nodejs.org/download/release/v24.22.3/` with `SHASUMS256.txt` verification; install only under `/root/oldx-tools`, export that bin to PATH for current shell. Do not alter Windows Node, native SDK, IAM, H2AG/H2AF markers or project. Also verify `docker buildx version`, Linux Docker engine and root free disk. No new testing of OLDX source required.

Remaining permitted H2AI work is the exact Owner-approved one Buildx build/push per Mediator/Gateway/Backend/Reader with existing runner and frozen source `5d5a621d7a9d9015b5068077b914fef3d6fb9925`. On any subsequent post-marker STOP no retries. Step05 ACTIVE, production OFF/NO-GO. 
