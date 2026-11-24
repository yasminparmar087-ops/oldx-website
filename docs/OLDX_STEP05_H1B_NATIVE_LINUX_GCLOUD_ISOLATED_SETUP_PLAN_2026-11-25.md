# OLDX Step05 H1B — isolated native-Linux Google Cloud CLI setup plan

> **25 Nov 2026 LATEST S1 OWNER DECISION:** Owner has NOW explicitly authorized **S1 ONLY** (one official archive download, fresh dual-document version/checksum verification, safe tar inspection and isolated WSL Linux extraction). The older statements below saying S1 "NOT APPROVED" record the **historical S0 proposal**, not current consent. Actual owner-local S1 execution **NOT YET VERIFIED**. The exact immutable one-shot source/test hashes, safe one-line owner-WSL command, result/STOP markers and S2/S3/W1–W6 separate restrictions are in [the current S1 approved handoff](OLDX_STEP05_H1B_NATIVE_LINUX_GCLOUD_S1_OWNER_APPROVED_SOURCE_RECEIPT_2026-11-25.md). No gcloud, auth, Cloud writes or old probe retries are authorized by S1.

**25 November 2026, source-only PLAN PREPARED. No download, install, login, auth retry, project read, IAM, image, Cloud write, or H1B deployment is authorized or executed by this document.**

## 1. Established local evidence and purpose

- Existing single-run H1B read-only preflight **STOPPED on its first** `timeout 40s gcloud auth list --filter=status:ACTIVE` (exit **124**, stdout/stderr 0 bytes). No operator/project/Registry/new service/new SA lookups occurred; collisions UNKNOWN. Original one-shot marker is CONSUMED.
- The separately approved one-shot local `gcloud --version` startup check **also TIMED OUT after 12s** (exit **124**, script2). Its one-shot marker is CONSUMED.
- Later one **strictly passive**, gcloud/Python-free launcher inspection CONFIRMED the `gcloud` source is a regular **Windows-mounted SDK launcher** (6494 bytes, `#!/bin/sh`, no CRLF/symlink), Linux bundled Python missing, Windows bundle present, launcher attempts silent versioned PATH Python candidates and ultimately imports SDK Python modules from the mounted Windows tree. **Likely** Windows/WSL mixed-layout interpreter/module-loading delay; **UNKNOWN** exact selected Python and root cause. Passive evidence `SHA256SUMS` SHA256 **`61e4990035bce90923fefce882566170ba0d94d005188a5052d2d0f9c3aabd70`**; see [canonical actual diagnostic](OLDX_STEP05_H1B_GCLOUD_LOCAL_STARTUP_TIMEOUT_DIAGNOSIS_2026-11-25.md) and [Issue #17 result](https://github.com/yasminparmar087-ops/oldx-website/issues/17#issuecomment-7143994970).
- **Goal:** isolate the CLI's OS filesystem and interpreter, retaining OLDX work and ALL Windows SDK/auth/WSL configs unchanged. **Not a guarantee** that a native Linux CLI will launch correctly or be authenticated.
- Prior owner Option B acceptance applies **only** to the known 12 HIGH CVEs on the retained H1A candidate for a future at-most-24-hour IAM-private, compiled-OFF, no-real-user-data H1B experiment. This does **not** authorize any registry image push, new Cloud Run/SA/IAM/service/hosted probe, or production.

## 2. Official-source method preferred over global APT/snap

**Use a Google-official Linux archive, not `sudo apt`, `snap`, a GitHub mirror, modified Windows SDK, or global PATH modification.**

Google's [Cloud CLI installation](https://docs.cloud.google.com/sdk/docs/install-sdk) and [versioned archive installation](https://docs.cloud.google.com/sdk/docs/downloads-versioned-archives) documents confirm Linux x86_64 archives ship with a bundled interpreter and can be extracted to a separate directory. At the time the official versioned archive page was consulted (25 Nov 2026; page updated 22 Nov), it lists release **594.0.1**, Linux 64-bit x86_64 `google-cloud-cli-linux-x86_64.tar.gz`, approximate download **94.8MB**, **published SHA256 `c6fdba4cb1551b0da7c1d744eb0dfaf68b59861238d6a6b5ef6bad1ba596b567`**. This is a **time-stamped public checksum, NOT an already downloaded/validated file**. The generic filename is a potentially moving 'latest' target; never assume it still maps to the same bytes/version on the day of execution.

### Future separately approved LOCAL setup scope: one artifact, no Cloud APIs

1. In owner `OLDX-Ubuntu-24.04`, check **passively** (no gcloud execution) current `uname -m` and free space on WSL *Linux filesystem*, official download tools availability, planned destination collision/ownership and dedicated **setup** marker status. Expected platform for this candidate x86_64/amd64, **actual platform readback pending**. If WSL architecture is different, STOP instead of silently choosing another archive.
2. Set a distinct *new* private Linux-only destination, e.g. `/root/oldx-tools/native-gcloud-594.0.1/` (NOT under `/mnt/c`, `/mnt/d`, the repo or existing `$HOME/.config/gcloud`). If directory preexists, STOP instead of overwriting. Use `umask 077`, private evidence, enough reserved Linux scratch and a separately named one-shot marker. Preserve all original H1A/H1B/launcher diagnosis markers and WSL-local evidence.
3. Download only from the **exact official `dl.google.com` Linux x86_64 archive link** listed in Google's current official docs. Verify TLS and destination hostname, bounded single download/size, no automatic retry or alternate mirror. Read current official **matching release and checksum** in the same owner-reviewed session. If package/version/checksum differs from this frozen 594.0.1 expectation, STOP for review—do not auto 'fix' or fetch a different release.
4. Before extraction, compare archive SHA256 with the **matching official checksum** and validate archive structure: root confined to `google-cloud-sdk/`, no absolute/../traversal members, no symlinks/hardlinks escaping target, no special/device entries or unsafe modes. Reject unsafe/inconsistent archives. **Never extract untrusted bytes** or run `curl | bash`.
5. Extract once inside the NEW dedicated Linux-only directory after successful archive validation. The versioned archive is self-contained: **no `install.sh` needed for this source-only packaging plan**, no `gcloud init`, no global profile/PATH, no shell completion, no `sudo`, no default SDK overwrite. Preserve Windows SDK as-is. Capture local archive checksum + exact resulting `bin/gcloud` path, bundled Python path class and file metadata. Do not print full private home/SDK paths into public issue comments.
6. For any future explicit startup verification, call **the new native executable via absolute path** and use a separately isolated configuration directory (`CLOUDSDK_CONFIG` within the new private destination) to prevent even CLI-side config/log writes into existing `~/.config/gcloud`. **Startup execution is NOT included in this setup-plan approval**; a separate precise single-process, bounded owner permission is needed if the owner wants a `--version` smoke. A successful `--version` will prove **only** local startup—not account validity, credentials, project access, IAM, or H1B collision status.
7. Preserve private evidence, checksum, success/STOP state and dedicated one-shot marker. No cleanup of original SDK or consumed markers. If official source unavailable, mismatched, disk insufficient, archive unsafe, collision or unexpected process/network actions: `STOP_MANUAL_REVIEW`, no repeat/repair/alternative automatic install.

**Official checksum drift warning:** A downloadable file named `google-cloud-cli-linux-x86_64.tar.gz` is not immutable. Verify against the actual documented release/checksum before using it; NEVER rely on filename alone. The exact version and platform need readback at time of owner-approved execution. Do not invent a pinned version URL.

## 3. Proposed phased owner permissions — must remain separate

| Phase | Current state | What a later explicit owner decision may authorize |
|---|---|---|
| S0 — Source-only setup plan | **COMPLETE** | This document and recommended boundaries only; no local software change yet |
| S1 — Isolated native archive setup | **NOT APPROVED / NOT EXECUTED** | One official download + integrity/structure check + extraction into isolated Linux-only directory, no CLI execution or credential/config migration |
| S2 — Native local startup check | **NOT APPROVED / NOT EXECUTED** | At most one scoped, bounded absolute-path `gcloud --version` using the NEW isolated config, after S1 evidence |
| S3 — Operator/project/target read-only checks | **NOT APPROVED / NOT EXECUTED** | A NEW separately bounded workflow only after S2 and verified authorized principal; do not rerun original consumed H1B preflight script |
| W1–W6 — H1B operational Cloud changes | **NOT APPROVED** | Requires subsequent exact new-only service/SA/image-push/IAM/cost/UID/rollback/cleanup consent; risk Option B by itself is insufficient |

**NO Credential migration:** Do not copy or point to existing credential DBs, change logged-in accounts, run `auth list`/login/refresh, set persistent `PATH`, `CLOUDSDK_PYTHON` or `CLOUDSDK_CONFIG`, or edit shell dotfiles in S1. Even native CLI succeeding with a fresh empty config would initially have **no authenticated account**; any future authentication must be separately supervised and may not reuse WSL user accounts automatically.

## 4. Keep launch progress and no-repeat custody

While H1B tool-chain access is blocked, continue independent G2–G5 **source-only** development. No need to rescan H1A (image ID `sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`, Syft15 packages, Grype55 matches/12 distinct HIGH, local runtime PASS_WITH_LIMITS; all markers consumed). Site/Product/production remain **NO-GO** until independent actual launch gates are satisfied; accepting CVE risk for 24h H1B OFF-only experiment is not production authorization.

**Existing C1A private OFF-only Cloud service separate retention expires 28 Nov 2026 at 23:19 Asia/Kolkata.** Do not assume this document extends that approval or schedules automatic cleanup.

**ONE next owner decision:** explicitly approve or reject **S1 ONLY** — one Google-official, verified Linux x86_64 SDK archive download and extraction to a separate private WSL-Linux folder, with current Windows CLI/auth/config/PATH unchanged, no actual gcloud invocation or Cloud calls. If approved, implement a small one-shot script only within that consent; do not bundle S2/S3/Cloud writes silently. Document practical disk cost rather than promising ₹0 cloud charges; an official archive download uses local bandwidth/storage but no new Cloud Run/Registry resource by itself.

Status: `H1B_LAUNCHER_PASSIVE=CONFIRMED_WINDOWS_MOUNT`, `H1B_NATIVE_SDK_PLAN=S0_PREPARED`, `H1B_NATIVE_SDK_DOWNLOAD_INSTALL=S1_NOT_AUTHORIZED`, `H1B_READONLY_ORIGINAL=STOP_TIMEOUT_CONSUMED`, `H1B_NEW_CLOUD_WRITES=NOT_AUTHORIZED`, `H2/PRODUCTION=NO_GO`.
