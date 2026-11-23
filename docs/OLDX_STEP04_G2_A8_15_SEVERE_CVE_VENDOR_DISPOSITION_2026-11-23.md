# OLDX Step04 G2 A8 — 15 severe CVEs: owner Grype report + official vendor disposition (23 Nov 2026)

## Actual owner screenshot — one LOCAL-ONLY existing report inspection, 20:31 IST

From the saved immutable A8 private gzip report `$HOME/oldx-a8-grype-new-digest-2506826f.json.gz` in Google Cloud Shell, the pinned triage script passed its source checksum, existing report raw SHA256, target immutable digest, 46 matches (1 CRITICAL, 23 HIGH, 19 MEDIUM, 3 LOW). These are 46 **package-vulnerability matches**, NOT 46 separate CVEs; there are **15 distinct severe (CRITICAL/HIGH) CVE IDs** among 24 severe package matches. Grype distro shown as `alpine`, version `stream`, package versions:
- `glibc 2.43.0-r14`
- `libcrypto3 3.5.9-r1`
- `libssl3 3.5.9-r1`
- `sqlite-libs 3.54.1-r0`

Fix summary from Grype was `UNKNOWN=19`, `UNREPORTED=5` (severe match counts). That means **no fix can be confirmed from the raw Grype field alone**; it emphatically does **NOT** mean no fixes exist. Actual output `A8_NO_SCAN_OR_CLOUD_ACTIONS=TRUE`, `A8_STEP04=HOLD`. No other scan, build, signed verifier or Cloud action should be rerun. Raw report stays private. New immutable subject digest `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`, source Git SHA `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`, pinned Cloud Build and independent SLSA PASS remain consumed.

## Official cross-check: 15 unique severe IDs — version-specific STATUS, not an auto-clearance

### A. Seven BellSoft Stream/Hardened Containers CVEs with fixed-version matching installed packages (vendor-fixed **candidate**, requires exact APK source provenance and effective fix audit)

| CVE | Package/version in NEW A8 image | BellSoft official vendor fix status |
|---|---|---|
| CVE-2026-0861 | glibc 2.43.0-r14 | Stream fixed since 2.39.0-r6; new branch version is later |
| CVE-2026-19499 | glibc 2.43.0-r14 | Stream fixed since 2.43.0-r6 |
| CVE-2026-84243 | glibc 2.43.0-r14 | Hardened Containers Stream fixed at 2.43.0-r14 |
| CVE-2026-107496 | libcrypto3/libssl3 3.5.9-r1 | Hardened Containers Stream openssl fixed at 3.5.9-r1 |
| CVE-2026-88823 | libcrypto3/libssl3 3.5.9-r1 | Hardened Containers Stream openssl fixed at 3.5.9-r1 |
| CVE-2026-95691 | libcrypto3/libssl3 3.5.9-r1 | Hardened Containers Stream openssl fixed at 3.5.9-r1 |
| CVE-2026-95692 | libcrypto3/libssl3 3.5.9-r1 | Hardened Containers Stream openssl fixed at 3.5.9-r1 |

Authoritative official BellSoft CVE pages, read 23 Nov 2026:
https://docs.bell-sw.com/security/cves/CVE-2026-0861
https://docs.bell-sw.com/security/cves/CVE-2026-19499
https://docs.bell-sw.com/security/cves/CVE-2026-84243
https://docs.bell-sw.com/security/cves/CVE-2026-107496/
https://docs.bell-sw.com/security/cves/CVE-2026-88823
https://docs.bell-sw.com/security/cves/CVE-2026-95691
https://docs.bell-sw.com/security/cves/CVE-2026-95692

**Important:** Grype classified distro `alpine stream`, while installed package versions and BellSoft official database are for BellSoft Hardened Containers/Alpaquita Stream APK packages. This classification mismatch likely explains some false-positive-like Grype findings, but DO NOT overwrite Grype results, assert all seven have been physically remediated, or infer zero CVEs without verifying the APK origin/version/image package provenance. The developer/source owner should accept BellSoft's patched-version assessments only after binding the packages to the exact signed image provenance and vendor release line.

### B. Two historic CRITICAL/HIGH glibc entries are officially *disputed* / context-dependent, not automatically a release blocker or automatically dismissed

- CVE-2019-1010022: Grype CRITICAL. Upstream description disputes a stack-guard mitigation bypass as a concrete security issue; Ubuntu classifies ignored and Debian “unimportant” in some release contexts. Do not call a fixed package or assume exploitable from a server alone.
  Sources: https://ubuntu.com/security/CVE-2019-1010022 , https://security-tracker.debian.org/tracker/CVE-2019-1010022
- CVE-2019-1010023: Grype HIGH. Issue concerns calling `ldd` on attacker-supplied binaries, a code path the OLDX HTTP application does not currently show; upstream is cited as not treating it as a security vulnerability. Confirm no operational invocation of `ldd` on untrusted uploaded binaries.
  Sources: https://ubuntu.com/security/CVE-2019-1010023 , https://security-tracker.debian.org/tracker/CVE-2019-1010023

### C. One sqlite-libs entry is CLI-only exposure candidate; check CLI presence/use before ruling out

- CVE-2026-119586: Grype HIGH against `sqlite-libs 3.54.1-r0`; upstream SQLite explicitly states this is **not a bug in core SQLite library**. Exploitation requires the sqlite command-line shell `.recover` on an untrusted database with its output piped into a second shell without `--safe`; merely including the shared `sqlite-libs` package does not establish applicability. Check whether the immutable runtime image even contains the sqlite CLI or application performs this workflow; otherwise record mitigated/not reachable **with evidence**, not blindly fixed.
  Official SQLite: https://www.sqlite.org/cves.html (CVE-2026-119586)

### D. Five OpenSSL CVEs need actual call-path/reachability and vendor package disposition; NOT cleared

| CVE | Trigger/conditional attack path | Official evidence / current status |
|---|---|---|
| CVE-2026-107493 | App must pass existing non-NULL stack to `PEM_X509_INFO_read_bio_ex` and then parse bad PEM | OpenSSL 3.5.0 - <3.5.10 upstream affected; 3.5.9-r1 A8 version *may remain exposed* absent BellSoft backport |
| CVE-2026-107494 | OpenSSL QUIC connection-ID handling; QUIC protocol path | BellSoft lists Vulnerable for affected Stream/25 lines; must check if Node app opens QUIC listeners |
| CVE-2026-121482 | CMS/PKCS#7 SignedData verification with CRL checking on untrusted data | BellSoft lists Vulnerable; Node app reachability not proven |
| CVE-2026-124709 | OpenSSL QUIC **server** reject/reset stream handling, remote slow-memory DoS | Upstream OpenSSL 3.5.0 - <3.5.10 vulnerable; BellSoft lists Vulnerable; requires actual QUIC server use |
| CVE-2026-84786 | OpenSSL DANE-enabled TLS client and unusual certificate/TLSA inputs | BellSoft lists Vulnerable; needs DANE-enabled TLS client evidence |

Sources:
https://www.openssl-library.org/news/vulnerabilities-3.5/index.html
https://docs.bell-sw.com/security/cves/CVE-2026-107494
https://docs.bell-sw.com/security/cves/CVE-2026-121482
https://docs.bell-sw.com/security/cves/CVE-2026-124709
https://docs.bell-sw.com/security/cves/CVE-2026-84786

**Limited repo source audit in SAME branch:** `functions/staging-marketplace/product-read-server.mjs` imports Node `createServer` from `node:http` and calls `createServer` to accept HTTP requests. `Dockerfile.product-read.bellsoft-npm-free` uses BellSoft pinned base `docker.io/bellsoft/hardened-nodejs@sha256:ef00ba8e...`, sets `USER appuser`, and starts this Node server. No direct QUIC listener was observed in this entry point. This does **not** prove all transitive Node/Firebase/TLS/CLI/native paths non-reachable, nor replace running new image safely; conservative interpretation only.

## Decision — no immediate rebuild or repeated scans

- Categories presently: **7 vendor-fixed-version candidates + 2 disputed upstream + 1 CLI-only reachability candidate + 5 OpenSSL conditional/potentially vulnerable = 15 distinct severe CVEs**. This is a triage *categorization*, not proof only five actual vulnerabilities remain. Final risk must be based on actual package vendor origin and runtime call paths.
- Focus next on **source-only runtime reachability + exact package origin** with minimum work. Need a targeted read-only inspection of existing image/SBOM vs BellSoft security tracker, and bounded runtime/nonroot/Firestore default DB access evidence. Avoid recreating already verified builds/scans/provenance, enabling additional API, changing IAM/Cloud Run or production.
- If the five OpenSSL items remain unresolved and no vendor fix is yet present, document affected APIs, why not directly exposed (if proven), mitigations (private Cloud Run, invoker restrictions, resource/time limits, only TLS via managed edge, no QUIC/CMS/DANE application features) and formal owner residual-risk acceptance. Never assume a fix that is not in the installed package. An owner may choose a risk-accepted launch later, separate from Step04 passing on strict zero-severe criteria.
- Other separate gates G4 (effective invoker/other Firestore DB), G8 (project-wide spend/rollback/STOP), focused runtime new-image tests remain OPEN. STEP04 HOLD / production NO_GO.

No commands in this document are preapproved to mutate Cloud resources. This is source-only evidence and planning.
