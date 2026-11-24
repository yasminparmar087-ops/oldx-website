# OLDX Step05 — LATEST one-free-local-image-evidence handoff (24 Nov 2026)

**OWNER APPROVAL (ACTUAL):** "ha manjuri chhe" in direct response to "one limited, cost-free NEW OFF-only Gateway image build, SBOM/security scan and Linux Node24 smoke, with NO cloud deployment, Registry upload, IAM change or paid resource." C1A deploy, C1B hosted requests and C2 enabled use are **NOT approved**.

**Previously verified remote HEAD:** `e74082d7a216550a54cebfc61ead8ea931966459`; last 84 DISTINCT focused synthetic/offline PASS receipts remain historical. Neither 84 cases nor old A8 image builds/scans/Cloud/Vercel/IAM investigations were rerun.

**Actual work THIS turn:** Created and updated source-only `scripts/step05-gateway-off-local-one-shot.sh` on `security-hardening-review`, with pinned Git blobs of ONLY the new Gateway OFF-server/Dockerfile/deny-all Docker context. The script performs a single local Docker Linux/AMD64 Node24 nonroot readonly network-none build/smoke, one SHA256-verified official Syft1.57.1 CycloneDX SBOM, and one SHA256-verified official Grype0.121.3 vulnerability scan, computing distinct HIGH/CRITICAL IDs. No automatic retries, source drift or duplicate build; a HOME one-shot marker is set only after preflight and before local build; exact new local container/image and binaries are cleaned up, small reports retained.

**Blocked runtime:** assistant container has no Docker, Podman, Buildah, daemon or gcr.io DNS. No actual new image was built. Bash syntax of a corresponding locally authored draft PASSED; the GitHub script itself was not executed in Linux/Docker here. Do not claim SBOM/Grype/Linux Node24 smoke passed. GitHub public standard runners would be free but adding a push-triggered workflow would automatically repeat old unconditional Safety CI; deliberately NOT done. No GitHub CI or cloud service was invoked.

**One owner Cloud Shell action, only if existing FREE Cloud Shell has Docker and >=4GiB scratch (script checks both):**
```bash
d=$(mktemp -d /tmp/oldx-step05-build.XXXXXX) && git clone --quiet --depth 1 --single-branch --branch security-hardening-review https://github.com/yasminparmar087-ops/oldx-website.git "$d" && cd "$d" && bash scripts/step05-gateway-off-local-one-shot.sh
```

Share only the final `summary.txt` and, if failed, one concise STOP reason. Do not repeat an attempted build after a failure without an explicit scoped decision; do not reveal tokens or upload raw secrets.

**Technical note:** `docs/OLDX_CURRENT_HANDOFF.md` has grown beyond GitHub Contents API's supported content retrieval size and is returned empty by the connector in this turn. It was **NOT overwritten or truncated**. This small checkpoint is the authoritative newer pointer, linked from Step05's single master-plan row and the canonical [C1A owner manifest](OLDX_STEP05_OWNER_SELECTED_OPTION_C_C0_AND_MINIMAL_C1A_MANIFEST_2026-11-24.md).

**Security/launch HOLD:** new image local build/SBOM/scan/Node24 execution UNVERIFIED; even if passed, publisher signature, exact derived image immutable registry digest, C1A operator/tester/ingress and finite INR cost/cleanup, effective IAM, Step04 enabled 15 CVEs and media remain unresolved. `OPTION_C=C0_OWNER_SELECTED`, `STEP05_LOCAL_IMAGE_EVIDENCE=OWNER_APPROVED_ONE_ATTEMPT_NOT_RUN`, `STEP05_HOSTED=BLOCKED`, `STEP05=NOT_DONE`, `PRODUCTION=NO_GO`.


## 24 Nov 2026 — Owner Cloud Shell first one-shot ATTEMPT PARTIAL PASS, STOP at Syft SBOM

**This replaces the earlier “NOT RUN” state for the exact one-shot build.** Owner provided Cloud Shell screenshot for the already-approved local script. Exact transcript visible:

- `HEAD=10a486e27a75fa79d0c90fbea7c7017cfb15a020` (the previous review-branch source checkpoint).
- `EVIDENCE=/home/yasminparmar087/oldx-step05-gateway-evidence-20261124T111007Z`.
- `LINUX_NODE24_NONROOT_READONLY=PASS`.
- `OFF_ONLY_LINUX_CONTAINER=PASS`.
- `LINUX_SIGTERM_EXIT=PASS`.
- SHA256 of the downloaded `syft_1.57.1_linux_amd64.tar.gz` reported `OK`.
- Final line: `STOP: New image SBOM failed`, shell returned to prompt.

**Evidence interpretation:** A NEW derived Gateway image WAS locally built (necessary for those real container smoke checks), Linux Node24/nonroot/read-only, disabled API/health and Linux SIGTERM checks passed. The image was NOT uploaded or deployed. Syft extraction and SBOM operation were reached but the scan command returned nonzero; screenshot alone does NOT establish why (source mismatch, image deleted before scan, Syft error, timeout, disk, etc. not yet diagnosed). **No valid SBOM or Grype CVE scan PASS**; Grype was not reached. Script trap cleans only its new temporary container/image and scan scratch and retains the evidence directory; the one-time marker is consumed. Do **NOT** rerun the build or any old 84 offline tests / Step04 A8 scans under this spent approval. A new build needs a distinct scoped decision. New test-case count unchanged at 84; Linux container smoke results are reported separately, not automatically added to historical Node offline totals.

**Next action: read-only evidence inspection, no repeated build/scan** from existing Cloud Shell (exact known evidence path):

```bash
OUT="$HOME/oldx-step05-gateway-evidence-20261124T111007Z"
printf '\n=== SUMMARY ===\n'; cat "$OUT/summary.txt"
printf '\n=== FILES ===\n'; ls -lh "$OUT"
printf '\n=== SBOM BYTES ===\n'; wc -c "$OUT/sbom.cdx.json" 2>/dev/null || true
printf '\n=== BUILD ERRORS (IF ANY) ===\n'; grep -Ei 'error|fail|warning' "$OUT/build.log" | tail -n 12 || true
```

Inspect output before any new action or download. Note that the original Syft stderr was not explicitly redirected to a retained log in the one-shot script, so the exact exit reason might be unavailable; do not infer it. Preserve `summary.txt`, `node24-runtime.txt`, `off-scenario.txt`, `shutdown.txt`, `build.log` and any partial SBOM without exposing credentials. **Next consent scope:** if evidence cannot resolve failure, propose a minimal scan-only recovery or distinct one-time new build based on whether an immutable locally accessible image remains. No Cloud Build, Registry push or deploy automatically.

**Status:** `C1A_LOCAL_NEW_IMAGE_BUILD=PASS_WITH_LIMITS`; `LINUX_NODE24_OFF_SMOKE=PASS`; `SYFT_SBOM=FAILED`; `GRYPE_NOT_RUN`; `C1A_IMAGE_SECURITY=BLOCKED`; `STEP05_HOSTED=BLOCKED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — SECOND owner screenshot: saved evidence inspected, 0-byte SBOM, no Syft stderr

Owner ran the requested **READ-ONLY** Cloud Shell evidence inspection; second screenshot confirms:
- Evidence directory `/home/yasminparmar087/oldx-step05-gateway-evidence-20261124T111007Z` exists; summary shows `STATUS=ATTEMPT_STARTED`, exact historical HEAD `10a486e27a75fa79d0c90fbea7c7017cfb15a020`, `PLATFORM=linux/amd64`, `USER=65532:65532`, and a locally derived Docker image ID. The screenshot does NOT show a completed image/scan summary.
- Saved files: `build.log` (~18 KiB), `node24-runtime.txt`, `off-scenario.txt`, `shutdown.txt`, `summary.txt` and **`sbom.cdx.json` (0 bytes)**. No `grype-report.json`, `report-sha256.txt` or saved Syft error log. Build warnings grep reports only `1 warning found (use docker --debug to expand)`, not a build failure.
- Previous screenshot already showed Linux Node24 NONROOT READONLY, OFF-only container and SIGTERM all PASS, then successful Syft tarball SHA256 check and `STOP: New image SBOM failed`. **The cause of Syft's nonzero exit is UNKNOWN** from retained artifacts: no stderr was saved. A zero-byte SBOM is NOT a security report; Grype never ran.
- The one-shot script has a cleanup trap that attempts to remove the new locally tagged image on failure. The status of the exact image ID **has not yet been checked**. Do not assume it exists or assert Docker cached image layers can reconstruct an immutable derivation.
- No older 84 Node tests, A8 image build, Dockerfile review, Vercel or IAM checks were rerun. The one-shot approval remains consumed. No cloud resource/IAM/billing/deploy has changed.

**NEXT ONE READ-ONLY CHECK:** derive the image ID from the saved summary and inspect it without rebuilding, plus display scratch availability:

```bash
OUT="$HOME/oldx-step05-gateway-evidence-20261124T111007Z"
ID=$(sed -n 's/^DERIVED_LOCAL_IMAGE_ID=//p' "$OUT/summary.txt" | head -n 1)
if [ -z "$ID" ]; then
  echo "IMAGE_ID_MISSING_FROM_SAVED_SUMMARY"
elif docker image inspect "$ID" --format 'IMAGE_STILL_PRESENT={{.Id}} SIZE_BYTES={{.Size}}' 2>/dev/null; then
  echo "SCAN_ONLY_RECOVERY_MAY_BE_POSSIBLE_AFTER_REVIEW"
else
  echo "IMAGE_REMOVED_BY_CLEANUP_OR_UNAVAILABLE"
fi
df -h /tmp "$HOME"
```

This is read-only and uses no network/cloud. **If image still present**, consider a separately scoped **scan-only** diagnostic with Syft stderr preserved (no new image build). **If image absent**, STOP: first decide a separate new image build+scan approval after source-only repair/plan; do not rerun automatically or use a mutable base. If disk is depleted, do not delete any unknown Cloud Shell home files without user's approval. Security evidence remains BLOCKED until actual new-image SBOM/Grype plus publisher/provenance review.

`STEP05_IMAGE_BUILD=PASS_WITH_LIMITS`; `OFF_ONLY_LINUX_SMOKE=PASS`; `SYFT_SBOM=FAILED_0_BYTES_CAUSE_UNKNOWN`; `GRYPE=NOT_RUN`; `C1A/C1B=NOT_APPROVED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — THIRD screenshot: derived image absent; Cloud Shell HOME only 39 MiB free

The owner's THIRD screenshot of the requested read-only inspection shows **`IMAGE_REMOVED_OR_UNAVAILABLE`** for the exact `DERIVED_LOCAL_IMAGE_ID`; no matching local derived image is now inspectable. The one-shot local cleanup removed the image or made it unavailable; Docker layers/cache possibly remain but are **not** proof of an available runnable image. The same screenshot's `df -h /tmp "$HOME"` shows:
- root/overlay `/`: **119G total / 110G used / 9.8G available (92%)**.
- separate persistent `/home`: **4.8G total / 4.5G used / only 39M available (reported 100%)**.

**Critical new diagnosis:** almost-full persistent HOME is a plausible contributor to scanner failure, but **not proven** because Syft stderr was not recorded. Do not attribute the failed 0-byte SBOM solely to storage. No valid SBOM/Grype report exists. No new build/scan/permission/spend and no old 84 tests were repeated in obtaining this screenshot; Step05 security approval remains HOLD. The single original owner-approved build is **consumed** and the exact derived image **unavailable**, so there is no scan-only recovery against that image. A new build is **NOT** automatically authorized.

**NEXT single READ-ONLY check before designing any recovery:** inspect what consumes persistent HOME disk without deleting any project/user data:

```bash
echo "=== HOME SPACE BY TOP-LEVEL DIRECTORY (READ-ONLY) ==="
du -x -h --max-depth=1 "$HOME" 2>/dev/null | sort -h | tail -n 18
echo "=== PERSISTENT HOME SPACE ==="
df -h "$HOME"
```

Review directories and find only provably disposable OLDX tool caches or scratch artifacts. Do NOT bulk-rm HOME/old project data, delete Docker images or run `docker system prune`, and do NOT rerun the one-shot build. Preserve evidence directory and old checkpoint files. Any space recovery requires exact path ownership and a narrowly scoped decision. If a source-only fix is possible, prepare a **new separate bounded build+scan-only action consent** (still no Cloud/deploy), explicitly redirect scanner cache/temporary files to `/tmp`, cap scratch use and save Syft stderr; obtain owner approval before executing a second build. Verify `/tmp` space remains sufficient without assuming 9.8G guarantees a full image+scanner peak. Cloud Build remains outside authorization.

**Frozen status:** `NEW_GATEWAY_BUILD=PASS_WITH_LIMITS_EARLIER`; `DERIVED_IMAGE=REMOVED_OR_UNAVAILABLE`; `HOME_SPACE=39M_FREE`; `SYFT_SBOM=FAILED_0_BYTES_CAUSE_UNPROVEN`; `GRYPE=NOT_RUN`; `ORIGINAL_ONE_SHOT_APPROVAL=CONSUMED`; `C1A/C1B/C2=NOT_APPROVED`; `STEP05_HOSTED=BLOCKED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — Owner approves ONE new Windows WSL2 local image build + SBOM + Grype scan (NO CLOUD)

After the earlier consumed Cloud Shell attempt (build/OFF smoke PASS, 0-byte Syft SBOM FAIL, Grype not run and image removed), the owner asked whether the personal Windows Laptop could be used. Owner screenshots confirm **Windows 10 / WSL2 `OLDX-Ubuntu-24.04` RUNS**, `docker version` Client **AND Server 29.10.0** `linux/amd64`, 3.3GiB WSL memory available, swap 4GiB, local Docker images ~1.226GiB, existing Docker cache ~821.6MiB, Windows C: 22GiB free, D: 72.5GiB free. The WSL `df` reported a sparse **virtual** 941GiB free; do NOT misrepresent as physical disk. The owner expressly replied **"ha manjuri chhe"** to **ONE NEW FREE LOCAL Laptop/WSL** build + SBOM + Grype scan, still NO Cloud Build, IAM, Firebase, Registry push/deploy, Billing or old A8 re-run. This is a fresh narrowly scoped build permission for the laptop, distinct from the consumed Cloud Shell one.

**New prepared execution source:** `scripts/step05-gateway-off-wsl-one-shot.sh` on `security-hardening-review`. It verifies unchanged NEW Gateway 3 exact committed Git blob IDs, correct branch/remote, WSL2+AMD64, LOCAL default Docker daemon with no `DOCKER_HOST`, C: >=10GiB free, /tmp>=8GiB free, WSL available RAM >=1.5GiB before consuming a unique laptop-specific **one-shot marker**. It invokes exactly ONE immutable-base new OFF Gateway image build with network-none Dockerfile RUN, and performs one Linux Node24 nonroot/readonly/OFF-only/health/SIGTERM smoke of THIS NEW image only. It then `docker save` exports that same image into a local temporary **docker-archive** and runs checksum-pinned Syft v1.57.1 generating **both Syft JSON and CycloneDX JSON**, validating non-empty parseable SBOM. Grype v0.121.3 then scans the Syft JSON with a current online vulnerability DB, computing distinct severe IDs; reports, stdout/stderr, exact derived local image ID, report hashes and stage of failure persist under a newly timestamped WSL HOME evidence folder. Syft/Grype artifacts are downloaded only from official upstream release and checked against historical exact official release SHA256s; scanning does NOT require live Firebase or remote container registry access. The prior Cloud Shell failure cause was never determined; archive scanning and logs reduce diagnostic blind spots but do not guarantee scan success.

**Critical recovery difference:** On scanner failure the newly built local image is deliberately **RETAINED** for a future no-build scan-only diagnosis. Temp archive, scanner binaries, and only the exact NEW synthetic test container are cleaned up. It never runs `docker push`, `gcloud`, `docker system prune`, generic deletes, Cloud-hosted endpoints or historical 84 cases. No Docker image Build or scan was executed by the assistant in this chat's container; source script Bash syntax and both embedded Node smoke fragments syntax were checked in isolated assistant runtime. GitHub source invariant checks were also performed; these are **NOT new local image security PASS tests**. Historical 84 focused offline cases not rerun or incremented.

**One PowerShell command, owner to run ONCE ONLY:**

```powershell
wsl -d OLDX-Ubuntu-24.04 -- bash -lc 'd=$(mktemp -d /tmp/oldx-step05-wsl.XXXXXX) && git clone --quiet --depth 1 --single-branch --branch security-hardening-review https://github.com/yasminparmar087-ops/oldx-website.git "$d" && cd "$d" && bash scripts/step05-gateway-off-wsl-one-shot.sh'
```

Send **summary.txt**, not private credentials, and the last concise `STOP` line. If the new attempt fails, **do not repeat the one-shot**; next action will inspect retained scan error log and local image without another build. If Grype reports HIGH/CRITICAL IDs, that is a documented security disposition blocker, not automatic failure of syntax and not launch authorization. Initial C1A Cloud deployment and C1B/C2 real-host tests remain separately unapproved with IAM, full gross spend, publisher verification, media and prior severe-CVE enabled-scope gates unchanged.

**Status at time of this document:** `STEP05_WSL_BUILD=OWNER_APPROVED_ONE_ATTEMPT_SCRIPT_PREPARED_NOT_RUN`; `STEP05_OLD_CLOUD_SHELL_BUILD=PASS_WITH_LIMITS`; `OLD_CLOUD_SHELL_SYFT=FAILED_0_BYTES`; `NEW_WSL_SBOM/GRYPE=NOT_EXECUTED`; `C1A/C1B/C2=NOT_APPROVED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — WSL first invocation STOPPED BEFORE SCRIPT: clone/checkout file mismatch

Owner's local Windows PowerShell screenshot after authorized WSL command shows the exact error `bash: scripts/step05-gateway-off-wsl-one-shot.sh: No such file or directory`. The preceding command used `git clone --quiet --depth 1 --single-branch --branch security-hardening-review`, then `cd "$d"`, then `bash scripts/step05-gateway-off-wsl-one-shot.sh`. There is no new build/scan/script output; the NEW WSL-only one-shot itself **DID NOT START**, the per-WSL approval marker was not set by that script, no derived image/scan created and no old cases rerun. This is a clone/checkout/path problem, **not evidence of a Docker/Syft failure**.

GitHub connector independently verified at the time of this screenshot that current remote branch HEAD is `05cb784a8cf7ad757b7ae73f92805a68cd701f14` and the required exact file **DOES exist** on branch: `scripts/step05-gateway-off-wsl-one-shot.sh`, Git blob `4487b23109c77ca8b4c6f23e131cde3c2bb7fb5b`, size 10865 bytes. Do not assume why local clone lacks it until reading local clone branch/HEAD/tree.

**NEXT ONE READ-ONLY WSL action** from PowerShell, inspect the already cloned repo(s) without another clone or build:

```powershell
wsl -d OLDX-Ubuntu-24.04 -- bash -lc 'for d in /tmp/oldx-step05-wsl.*; do [ -d "$d/.git" ] || continue; echo "=== $d ==="; git -C "$d" branch --show-current; git -C "$d" rev-parse HEAD; git -C "$d" ls-files scripts/step05-gateway-off-wsl-one-shot.sh; ls -l "$d/scripts/step05-gateway-off-wsl-one-shot.sh" 2>&1; done'
```

Do not rerun the whole command until the precise local checkout mismatch is understood; no cloud actions/deployment/paid build. `STEP05_WSL_ONE_SHOT=NOT_STARTED`; `STEP05_OLD_CLOUD_SHELL_LOCAL_IMAGE=PASS_WITH_LIMITS_AND_IMAGE_REMOVED`; `NEW_WSL_SBOM_GRYPE=NOT_RUN`; `C1A/C1B/C2=UNAPPROVED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — Local WSL2 NEW gateway image PASS, download Syft FAIL, image RETAINED

Owner's screenshot of the first **authorized** WSL2 one-shot run in a directly opened Ubuntu/root shell confirms the guarded script was located and executed from `/tmp/oldx-step05-wsl.1gqReU`; reported Git `SOURCE_SHA=1a31f7d3c7512e0acf6efb24653fc2fcbc116bea`. Evidence retained in **`/root/oldx-step05-laptop-evidence-20261124T115031Z`**. This supersedes the older local PowerShell/Bash quoting and stale/missing-clone screenshots: current working clone successfully runs the correct script.

**Verified screenshot checkpoints:** NEW immutable-base image locally built `linux/amd64` user `65532:65532`; `LINUX_NODE24_NONROOT_READONLY=PASS`, `OFF_ONLY_HTTP=PASS`, `LINUX_SIGTERM=PASS`. The script proceeded to `STEP: export the exact new image to a local tar (not push)`, then attempted the official pinned Syft asset download and reported **`STOP: Syft download failed`**, `STOP: SYFT_DOWNLOAD. Image remains local if built; do NOT rerun this one-shot.` This does not verify successful SBOM or Grype, and **no CVE counts are available**. The new image is intentionally preserved by script logic on scan failure; do not claim actual Docker inspect still exists until checked, and archive scratch was deleted by the failure trap. GitHub CI, old 84 offline tests, old A8 build/scan, Cloud resource/deploy/push/IAM/billing remain untouched. Laptop one-shot approval is now CONSUMED.

**Exact NEXT ONE read-only owner command in the already-open Ubuntu (root) shell:**

```bash
OUT=/root/oldx-step05-laptop-evidence-20261124T115031Z
echo '=== SYFT DOWNLOAD ERROR ==='
cat "$OUT/syft-download.stderr.log"
echo '=== NEW IMAGE ==='
docker images --no-trunc --filter 'reference=oldx-step05-gateway-off:*' --format '{{.ID}} {{.Repository}}:{{.Tag}} {{.Size}}'
echo '=== SUMMARY ==='
cat "$OUT/summary.txt"
```

No retries, downloads, builds, installs, deletes, scans, cloud actions or paid operations in this read-only command. If the asset failed due to a network/SSL/release URL or desktop proxy problem, plan a separately scoped **scan-only recovery** on the **SAME saved local image**, with trusted pinned release asset checksum and retained stderr; seek approval if download/network/install changes are needed. Do not attempt another build; do not delete local Docker state. `STEP05_WSL_BUILD=PASS_WITH_LIMITS`; `STEP05_WSL_NODE24_OFF=PASS`; `STEP05_WSL_SYFT_DOWNLOAD=FAILED_REASON_PENDING_LOG`; `STEP05_WSL_SBOM_GRYPE=NOT_EXECUTED`; `C1A/C1B/C2=NOT_APPROVED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — WSL Syft download root cause confirmed: 120-second transfer timeout, retained image

Owner's next screenshot (read-only inspection from root Ubuntu shell) independently shows **`curl: (28) Operation timed out after 119351 milliseconds with 2882408 out of 31432061 bytes received`** in `/root/oldx-step05-laptop-evidence-20261124T115031Z/syft-download.stderr.log`. This conclusively explains failure of the **Syft release archive download** at the prior scripted `--max-time 120`; it does **not** establish permanent internet failure or prove that an archive checksum would pass. **No Syft binary executed, no SBOM and no Grype scan** in this WSL attempt.

The same screenshot shows the NEW locally derived Gateway image **still in Docker**:
`sha256:612f3c02806a93d991127f87e34391646edf9bad251bb2b8aace90a434bc30a`; tag `oldx-step05-gateway-off:wsl-once-20261124-801`; size shown **215 MB**. It is a **local Docker image ID**, not a pushed registry digest or publisher signature. Linux Node24 nonroot/readonly, OFF-only HTTP and SIGTERM had passed earlier and are preserved without replay. The prior script removed its temporary scanner tarball on failure; no claim that partial 2.88MB download remains.

**Next authorized action status:** the **one-shot build was executed and consumed**. Do NOT rebuild it, rerun the one-shot, delete the image, or rerun old 84 tests/A8/Cloud scans. A narrow **scan-only recovery** using this existing immutable identified local image, longer bounded release download with official SHA256 verification and saved Syft/Grype stderr, followed by SBOM+Grype, is the smallest sensible next step; seek action-specific owner approval before doing any new network/download/install/scan. It can leave all existing Docker images/volumes untouched, no Cloud Build/Registry push/deploy/IAM/Firebase. A timestamped report directory should be preserved for future chat. Avoid treating successful local scan as C1A/production GO.

**Status:** `STEP05_NEW_LOCAL_IMAGE_BUILD=PASS_WITH_LIMITS`; `EXACT_IMAGE=RETAINED_215MB`; `DOWNLOAD_FAILURE=OFFICIAL_SYFT_RELEASE_120S_TIMEOUT`; `SYFT_SBOM=NOT_RUN`; `GRYPE=NOT_RUN`; `NEW_BUILD_PERMISSION=CONSUMED`; `C1A/C1B/C2=UNAPPROVED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — Owner explicitly APPROVED separate scan-only recovery on existing retained WSL image

Owner explicitly replied **"ha manjuri chhe"** to the request to resume the free download and run ONLY Syft SBOM and Grype on the EXISTING locally retained **Step05 OFF Gateway** image (no re-build). Scope is separate from, and does NOT renew, the already CONSUMED local WSL image-build approval. Image from screenshot remains `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb2b8aace90a434bc30a`, tag `oldx-step05-gateway-off:wsl-once-20261124-801`, 215 MB, `linux/amd64`, nonroot65532, Linux Node24 OFF/health/SIGTERM prior PASS.

**New source-only execution file:** `scripts/step05-gateway-off-scan-recovery.sh` on `security-hardening-review`. Prepared in the assistant runtime and checked via `bash -n` (syntax only, **not a scan PASS**). This guarded one-shot checks WSL Linux AMD64, local default Docker daemon, **exact existing immutable image ID AND tag**, image user/platform, actual Windows C and WSL disk reserves; it uses a distinct scan-recovery one-shot marker and performs NO `docker build`, image pull, registry push, IAM/cloud/API credentials, Firebase writes, deployment or old A8 checks. It exports that same existing image locally into a retained Docker archive, and performs only NEW image Syft SBOM generation and Grype vulnerability assessment.

**Partial network recovery:** the previous Syft download failed after 2,882,408/31,432,061 bytes due to a 120-second timeout; that earlier partial tarball was removed by prior script's trap. The new one-shot starts a NEW archive download, retaining **its own** incomplete files in `$HOME/oldx-step05-scan-recovery-*/assets/`, using `curl -C -` within a finite maximum **5 x 600-second** per-release transfer window, SHA256 checking the already-pinned official Syft v1.57.1 and Grype v0.121.3 release archives BEFORE extracting/executing. If resume/server/network/sha mismatches, STOP and preserve evidence, never silently use corrupted assets. Syft gets one explicit `docker-archive:` scan, emits nonempty JSON, then converts that SBOM to CycloneDX without rescanning image; Grype scans the Syft JSON once with its own bounded 1,200-second database/scan window, reports CVE counts and unique HIGH/CRITICAL CVE IDs. Real Grype DB fetch is separate and may still fail on low bandwidth; do not claim success until logs exist. Individual `*-download.log`, Syft/Grype stderr, JSON, report hashes, image tar and stage summary stay in a new private root HOME evidence directory on any failure; existing Docker image and other images/volumes are never deleted. The official source supports `docker-archive:` from `docker save`, and Grype supports `sbom:` Syft JSON.

**One owner execution command (paste in ALREADY OPEN ROOT UBUNTU shell, NOT PowerShell):**

```bash
cd /tmp/oldx-step05-wsl.1gqReU &&
git pull --ff-only origin security-hardening-review &&
git ls-files --error-unmatch scripts/step05-gateway-off-scan-recovery.sh &&
bash -n scripts/step05-gateway-off-scan-recovery.sh &&
bash scripts/step05-gateway-off-scan-recovery.sh
```

`git pull` only refreshes the temporary review-branch clone; it does not change user's independent Windows project or cloud resources. The new scan-only source is separate from old `step05-gateway-off-wsl-one-shot.sh` (NEVER rerun that earlier build script). Stop on any error and share only final `summary.txt`, last `STOP` and relevant small stderr, not credentials or raw full scanner output; no second manual run under this permission.

**Status:** `EXISTING_WSL_IMAGE_BUILT_AND_OFF_SMOKE=PASS_WITH_LIMITS`; `PREVIOUS_SYFT_DOWNLOAD=120S_TIMEOUT`; `SCAN_ONLY=OWNER_APPROVED_PREPARED_NOT_EXECUTED`; `SBOM=NOT_YET_VERIFIED`; `GRYPE_CVE_COUNT=UNKNOWN`; `NO_NEW_BUILD`; `C1A/C1B/C2=NOT_APPROVED`; `PRODUCTION=NO_GO`. Previous 84 focused offline cases and Step04 A8 Build/Scan not repeated. Passing local scan alone does not satisfy hosted IAM/security/cost/media gates.


## 24 Nov 2026 — Owner scan-only attempt STOP at exact Docker image identity preflight (no download/scan)

Owner's Ubuntu screenshot shows actual `git pull --ff-only origin security-hardening-review` succeeded, latest `9b22ff1b248a76b76eb7b11da7d243aca96e31db`, `bash -n` succeeded, and the NEW `scripts/step05-gateway-off-scan-recovery.sh` STOPPED at its initial exact-image guard:

```
STOP: The exact previously approved image/tag is missing or differs; DO NOT BUILD
```

This occurs **before** the scan-only one-shot `LOCK="$HOME/.oldx-step05-existing-image-scan-recovery-consumed"` creation in the source, and before `docker save`, any Syft/Grype download, SBOM or scan. Thus no image was rebuilt and the scan-only approval is not consumed by the script. The actual cause (image tag absent, tag points to a different digest, Docker host state changed, or an earlier screenshot-to-source transcription mismatch) **is not yet known**. Do not relax the exact pin or declare that the image was removed without observing Docker output.

**One next READ-ONLY command in the already-open Ubuntu root terminal:**
```bash
echo '=== EXACT TAG INSPECT ==='
docker image inspect oldx-step05-gateway-off:wsl-once-20261124-801 --format 'ID={{.Id}} USER={{.Config.User}} OS={{.Os}} ARCH={{.Architecture}}' || echo 'TAG_NOT_AVAILABLE'
echo '=== ALL NEW GATEWAY TAGS ==='
docker images --no-trunc --filter 'reference=oldx-step05-gateway-off:*' --format 'ID={{.ID}} TAG={{.Repository}}:{{.Tag}} SIZE={{.Size}}'
echo '=== APPROVED SOURCE PIN ==='
grep -E '^(PIN|TAG)=' scripts/step05-gateway-off-scan-recovery.sh
echo '=== SCAN-ONLY MARKER ==='
if test -e /root/.oldx-step05-existing-image-scan-recovery-consumed; then echo 'MARKER_EXISTS'; else echo 'MARKER_NOT_CREATED'; fi
```

Only after exact actual image ID and tag are established may the source pin be corrected under SOURCE-ONLY scope if transcription error is demonstrated. Do NOT rebuild, retag/repoint local images, delete Docker state, bypass the SHA256 guard or rerun historical 84 tests. Grype CVE findings remain UNKNOWN. The original WSL image build/Linux OFF-only prior PASS evidence remains, but current Docker identity needs read-only verification. C1A/B/C2 remain UNAPPROVED; production NO-GO.


## 24 Nov 2026 — Root cause RESOLVED: scan-only source PIN typo (63 vs 64 hex digits)

Owner's new exact read-only screenshot shows the local Docker `image inspect` output and existing image list both match:

- Local Docker image ID **`sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`** (exactly 64 hexadecimal digest digits).
- Tag **`oldx-step05-gateway-off:wsl-once-20261124-801`**.
- User **`65532:65532`**; platform **`linux/amd64`**.

The older scan-only script used **`sha256:612f3c02806a93d991127f87e34391646edf9bad251bb2b8aace90a434bc30a`** (only 63 hex digits), missing ONE `2` in `...251bb22b8...`. This was a **source transcription typo**, not an unknown local-image change or a Docker failure. The initial exact-image guard correctly denied further action; no scanner downloads, image rebuild, Grype/Syft or cloud activity occurred, and the script's one-shot marker had not been created at that preflight.

**SOURCE-ONLY FIX:** Changed ONLY the `PIN=` value in `scripts/step05-gateway-off-scan-recovery.sh` to the verified exact 64-digit image ID, commit `eb2ce1b5f82f43820b4a8489262ffc0cee9c0e42`. The fixed PIN and tag are literal immutable approved values; **do not remove/relax SHA matching, retag, rebuild or rescan historical work**. One scope remains: previously owner-approved scan-only SBOM/Grype on that same local image.

**NEXT SINGLE Ubuntu-shell command**, in the already checked-out local `/tmp/oldx-step05-wsl.1gqReU` folder:

```bash
git pull --ff-only origin security-hardening-review && bash -n scripts/step05-gateway-off-scan-recovery.sh && bash scripts/step05-gateway-off-scan-recovery.sh
```

If the scan-only lock exists or a new STOP occurs, DO NOT repeat; preserve image/assets and read `summary.txt` and stage-specific error log. The previous 84 historical Node focused cases have not been rerun. **Status:** `WSL_IMAGE_BUILD/OFF_SMOKE=PASS_WITH_LIMITS`; `PIN_TYPO=FIXED_SOURCE_ONLY`; `SCAN_ONLY=AUTHORIZED_NOT_YET_STARTED`; `SBOM/GRYPE=NOT_VERIFIED`; `C1A/C1B/C2=NOT_APPROVED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — NEW OFF Gateway WSL scan-only RECOVERY COMPLETE, 12 distinct High-severity CVE IDs

Owner screenshot at ~19:02 IST (24 Nov 2026) shows **SUCCESSFUL completion** of the once-approved scan-only recovery on the *same exact existing local* OFF Gateway Docker image, with **NO new image build, no registry push/deploy, IAM/Firebase modifications, paid cloud action, old A8 scan or old 84 tests repeated**. Preserve this as the latest status, superseding the prior "NOT EXECUTED" and 120-second Syft failure records. Image local ID: `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`, tag `oldx-step05-gateway-off:wsl-once-20261124-801` (NOT a remotely pushed registry digest or publisher signature); the earlier build/Node24 nonroot/OFF-only/SIGTERM PASS remains valid.

**Source-run evidence:** `MODE=SCAN_ONLY_NO_BUILD`; new evidence directory `/root/oldx-step05-scan-recovery-20261124T123515Z`; Syft attempts 1–3 completed with resumable partials (15,103,086 then 15,758,446 bytes noted); `SYFT_SHA256=VERIFIED`; `SYFT_SBOM_JSON=VALID`, `SYFT_SBOM=PASS`, `CYCLONEDX_SBOM=VALID`, `CYCLONEDX_SBOM=PASS`; Grype attempts 1–3 completed with resumable partials (10,858,666 then 28,548,257 bytes); `GRYPE_SHA256=VERIFIED`; `GRYPE_REPORT_VALID=PASS`. Final status `STATUS=SCAN_ONLY_COMPLETE_PENDING_SECURITY_REVIEW` and `NO_BUILD_NO_PUSH_NO_CLOUD_NO_IAM=TRUE`. Raw reports remain **only on owner's local WSL**, and the screenshot is not an independently downloaded/inspected Grype JSON.

**Measured Grype summary for NEW image:** **55 total package vulnerability matches**: HIGH **18**, MEDIUM **20**, LOW **6**, NEGLIGIBLE **11**; no CRITICAL match shown in the printed severity summary; **12 distinct High/Critical CVE IDs** (distinct from 18 HIGH package matches). The screenshot prints 12 IDs, but **do not derive package-fix or runtime exploitability claims from IDs alone**. Treat this as **scan completed but security disposition still HOLD**, not launch/enablement clearance. Old Step04 A8 scan 15 severe IDs is a DIFFERENT image and must not be blended or re-scanned to compute a new single count.

**NEXT one READ-ONLY user action (NO scanner rerun):** derive a compact grouped **CVE -> package/version/fix availability** list from the ALREADY SAVED Grype JSON. In the root Ubuntu terminal (no network, build, scan, installation or cleanup):

```bash
python3 - <<'PY'
import json
p='/root/oldx-step05-scan-recovery-20261124T123515Z/grype-report.json'
r=json.load(open(p))
rows={}
for m in r.get('matches',[]):
 v=m.get('vulnerability',{})
 if v.get('severity') not in ('High','Critical'): continue
 a=m.get('artifact',{})
 k=(v.get('id'),a.get('name'),a.get('version'))
 rows[k]={
  'fixed': ','.join(v.get('fix',{}).get('versions',[]) or []) or 'NONE_LISTED',
  'type':a.get('type','?')
 }
print('NEW_OFF_GATEWAY_IMAGE_SEVERE_PACKAGE_MATCHES=',len(rows))
for (cve,name,version),detail in sorted(rows.items()):
 print(cve,'|',name,'|',version,'|',detail['type'],'| fixed:',detail['fixed'])
PY
```

Require reporter review of the returned full package-level mappings, then group duplicate package matches by CVE and consult current official Debian/vendor fixes **ONLY for new image severe rows**, without repeating the old 84 tests, new-image scan, old A8 scans or Cloud inventory. Publisher authenticity/provenance, 12 severe dispositions, exact C1A IAM/operator/tester and INR budget, cleanup and subsequent finite hosted acceptance remain pending separately approved actions.

**Authoritative status:** `NEW_GATEWAY_LINUX_NODE24_OFF_SMOKE=PASS`; `NEW_GATEWAY_SYFT_SBOM=PASS`; `NEW_GATEWAY_CYCLONEDX=PASS`; `NEW_GATEWAY_GRYPE_SCAN=PASS_WITH_12_DISTINCT_HIGH_CVE_IDS`; `GATEWAY_IMAGE_SECURITY_ACCEPTANCE=HOLD`; `C1A/C1B/C2_CLOUD_DEPLOY=NOT_APPROVED`; `STEP05_HOSTED=BLOCKED`; `PRODUCTION=NO_GO`.


## 24 Nov 2026 — OFF Gateway 12 High CVEs grouped, Debian official source reviewed, no repeat scan

Owner ran the previously requested Python **READ-ONLY extraction from saved WSL Grype JSON**, resulting in **18 HIGH package matches / 12 distinct CVE IDs** and every row `Fix: NONE_LISTED`. Exact grouping: **2 gcc-14 source CVEs** (`CVE-2026-102010`, `CVE-2026-95619`) each reported on four runtime binaries `gcc-14-base`, `libgcc-s1`, `libgomp1`, `libstdc++6`, versions `14.2.0-19` (**8 matches**); **9 openssl source CVEs** (`107493`, `107494`, `107496`, `121482`, `124709`, `84786`, `88823`, `95691`, `95692`) on `libssl3t64 3.5.9-1~deb13u1` (**9 matches**); **1 glibc CVE** (`CVE-2026-84243`) on `libc6 2.41-12+deb13u5` (**1 match**). The Grype `NONE_LISTED` fixed versions are scanner metadata, not proof of no patches. Verified relevant official Debian Security Tracker CVE entries show inspected Trixie versions vulnerable, while some GCC fixes exist in newer Debian releases; do not replace the immutable base with a mutable or unstable image without owner approval.

**NEW canonical detailed triage:** [NEW Gateway 12 High CVE source-only package and Debian callpath worksheet](OLDX_STEP05_NEW_GATEWAY_12_HIGH_CVE_TRIAGE_2026-11-24.md). Current OFF-only Node server exposes no explicit QUIC, CMS, DANE, AES-GCM-SIV, gettext `LANGUAGE` or privileged Product routes, but native dynamic linkage and runtime reachability are NOT established. Individual CVE labels `HIGH` do not mean every flaw is practically triggerable through this server. **C1A PRIVATE OFF-only risk acceptance is NOT granted**, nor any C1B hosted traffic or C2 enablement. Do not repeat Syft/Grype, 84 Node cases, A8 build/scan, IAM checks or Cloud scans.

**Next one task:** source-only review actual image/Node native dependencies and the C1A limited OFF-only risk-acceptance packet, using existing SBOM and repo source, never new build/scan or cloud action. C1A still blocked by publisher/provenance, effective IAM, named invoker/operator, finite INR costs and rollback; Step05 hosted BLOCKED; production NO-GO.


## 24 Nov 2026 — New native Node sharedObjects inspection completed; no repeat needed

Owner's local Ubuntu screenshot of **ONE NEW** narrow `docker run --rm --network none --read-only --cap-drop ALL --security-opt no-new-privileges --entrypoint /nodejs/bin/node oldx-step05-gateway-off:wsl-once-20261124-801 -e ...process.report.getReport().sharedObjects` shows `libstdc++.so.6`, `libgcc_s.so.1` and `libc.so.6` **loaded**, along with `libdl.so.2`, `libm.so.6`, `libpthread.so.0`, loader and linux-vdso. **No libssl or libcrypto dynamic object is listed in that Node -e process snapshot.** These are PROCESS-LINKAGE observations, NOT proof of library omission from the image, no static embedding, or of unreachable CVEs. The 18 HIGH Grype matches, **12 distinct High IDs** remain unchanged: 2 GCC runtime CVEs (8 package matches), 9 OpenSSL CVEs (9), 1 glibc CVE (1). No image build, SBOM, Grype scan, prior 84 tests, IAM or Cloud action repeated. Full [native-linkage/security-risk worksheet](OLDX_STEP05_NEW_GATEWAY_12_HIGH_CVE_TRIAGE_2026-11-24.md), section 6, commit `454ec7f1b54f0269f9d4f7ca85a473461f87d62e`.

**Owner next:** NO further local verification required at present. Continue SOURCE-ONLY C1A private/OFF-only formal risk-disposition and finite resource/IAM/ingress/gross-cost/rollback packet. Do not change original `oldx-owner-read` A8/root, start any deployment, switch Product ON, retag image or claim OpenSSL risk eliminated. C1A/C1B/C2 remain UNAPPROVED; Step05 HOSTED BLOCKED; Production NO-GO.


## 24 Nov 2026 — C1A formal limited OFF-only risk and IAM/cost/rollback packet COMPLETE in SOURCE (no Cloud authorization)

Owner said "ok aagal vadho" after the completed single-process GCC/glibc/OpenSSL dynamic-link inspection. The assistant performed **only source/document/official-public-doc review**, NO Google Cloud API, IAM, Firebase, image build/scan/CI, old 84 tests, A8 verification, registry publish or paid work. [NEW formal C1A PRIVATE/OFF-only guarded risk & resource/IAM/spend/rollback packet](OLDX_STEP05_C1A_PRIVATE_OFF_ONLY_FINAL_RISK_AND_FINITE_ACTION_PACKET_2026-11-24.md) is canonical.

**Decision state:** 12 distinct HIGH new Gateway CVE IDs grouped 2 GCC/9 OpenSSL/1 glibc remain valid and **not accepted by owner for C1A**; GCC/glibc libs loaded, no dynamic libssl/libcrypto seen in one Node -e snapshot (NOT proof of no OpenSSL use). New Gateway has proven source default-OFF and earlier local Linux nonroot/readonly/health200/API503/SIGTERM & Syft/CycloneDX/Grype PASS_WITH_LIMITS, but the 12 new risk dispositions and publisher identity **remain open**. Old A8 15 severe IDs and its earlier owner limited acceptances are **separate** and NOT transferred. Proposed new project/region `oldx-staging/asia-south1`; one new service `oldx-step05-gateway`, one new dedicated runtime SA, one local-WSL-derived image to publish to already existing repository **ONLY WHEN separately approved**; max1/min0/concurrency1/1vCPU512MiB/request-based; no Auth/Firestore/KMS/back-end invoker. Proposed ingress=all + REQUIRED IAM acknowledges public network reachability; named tester/deployer and inherited IAM **UNVERIFIED**. Local image Docker ID is **NOT** an immutable remote registry manifest digest. Regional gross INR/FX/tax/free-tier, publisher signature, resource collision, exact owner-consent spend ceiling and new-resource-only cleanup permission **UNFILLED**. No C1A HTTP calls in future creation-only C1A; separate future C1B six OFF-only probes/20min; C2 ENABLED remains blocked. Neither Cloud Shell nor Vercel existing earlier discovery repeated.

**Single next milestone:** narrow **read-only** current account/project/entitlement/cost/preimage preflight only AFTER its own specific owner permission; until then source packet is prepared, deployment is NOT permitted. `C1A_RISK=PROPOSED_NOT_OWNER_ACCEPTED`; `C1A/C1B/C2_WRITE_OR_HOSTED_CONSENT=NO`; `STEP05_HOSTED=BLOCKED`, `PRODUCTION=NO_GO`.
