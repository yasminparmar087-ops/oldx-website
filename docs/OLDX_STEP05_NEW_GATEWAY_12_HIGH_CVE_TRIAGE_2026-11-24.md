# OLDX Step05 — NEW OFF Gateway 12 HIGH CVEs / 18 package-match source-only triage

**As of:** 2026-11-24 IST; **branch:** `security-hardening-review`; **state:** `SOURCE_REVIEW_ONLY`, `GATEWAY_IMAGE_SECURITY_ACCEPTANCE=HOLD`, `C1A/C1B/C2_NOT_AUTHORIZED`, `PRODUCTION_NO_GO`.

## 1. Evidence, scope and no-repeat rule

Owner's local WSL screenshot shows completed Syft JSON + CycloneDX + Grype scan of the **same newly built** OFF-only Gateway (not old A8), pinned local Docker image ID `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`, tag `oldx-step05-gateway-off:wsl-once-20261124-801`. Original base: `gcr.io/distroless/nodejs24-debian13:nonroot@sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec`. Owner's local saved machine reports (not uploaded to GitHub) are in `/root/oldx-step05-scan-recovery-20261124T123515Z/`; this note is a **screenshot-based package triage**, not a fresh Grype run or independently inspected raw report.

Grype summary: **55 total package matches** = HIGH18, MEDIUM20, LOW6, NEGLIGIBLE11; **12 distinct high/critical CVE IDs** (no Critical matches reported), not 55 unique CVEs. Owner's next screenshot extracted and confirmed the *exact 18 high package matches* and Grype listed **`NONE_LISTED` fixes for all**. `NONE_LISTED` is scanner metadata, not proof of no upstream fix. **Do not rerun the scanner/build/old 84 offline tests, old A8 CVEs, Google Cloud IAM, Vercel or hosted probes.**

## 2. Exact distinct CVE grouping from owner's NEW-image Grype screenshot

| Source family, binary packages in image | Image version | Distinct CVE IDs | Package matches |
|---|---|---|---:|
| `gcc-14` runtime: `gcc-14-base`, `libgcc-s1`, `libgomp1`, `libstdc++6` | `14.2.0-19` | `CVE-2026-102010`, `CVE-2026-95619` | 8 (4 for each CVE) |
| `openssl` binary `libssl3t64` | `3.5.9-1~deb13u1` | `CVE-2026-107493`, `CVE-2026-107494`, `CVE-2026-107496`, `CVE-2026-121482`, `CVE-2026-124709`, `CVE-2026-84786`, `CVE-2026-88823`, `CVE-2026-95691`, `CVE-2026-95692` | 9 |
| `glibc` binary `libc6` | `2.41-12+deb13u5` | `CVE-2026-84243` | 1 |
| **TOTAL** | | **12 distinct** | **18 HIGH matches** |

The exact Grype screenshot **does not** show that the nine OpenSSL issues are all reachable in the actual running Node HTTP gateway; similarly GCC and glibc presence does not prove exploitability or nonexploitability.

## 3. Official Debian Security Tracker check (24 Nov 2026)

Source packages and inspected `trixie` versions at official tracker remain **vulnerable** for these cases; do not claim Debian 13 has a fixed replacement merely because upstream/newer Debian releases have fixes. URLs below are stable official CVE records, not a claim of newly scanned software.

| CVE(s) | Official described vulnerability / triggered functionality | Trixie and practical source-only triage |
|---|---|---|
| [102010](https://security-tracker.debian.org/tracker/CVE-2026-102010) | libstdc++ `erase_if` binary heap use-after-free | `gcc-14 14.2.0-19` vulnerable in trixie, newer forky/sid fixed; actual OFF Gateway callpath **UNVERIFIED** |
| [95619](https://security-tracker.debian.org/tracker/CVE-2026-95619) | libstdc++ aligned `operator new` large-size overflow | Same trixie vulnerable; newer fixed; actual input-to-C++ allocation exposure **UNVERIFIED** |
| [107493](https://security-tracker.debian.org/tracker/CVE-2026-107493) | OpenSSL PEM_X509_INFO stack append use-after-free | trixie OpenSSL vulnerable; exact cert parser codepath **UNVERIFIED** |
| [107494](https://security-tracker.debian.org/tracker/CVE-2026-107494) | OpenSSL QUIC RETIRE_CONNECTION_ID unbounded queues | trixie vulnerable; current source uses Node built-in **HTTP**, not an explicit QUIC API; require runtime/native-linkage proof |
| [107496](https://security-tracker.debian.org/tracker/CVE-2026-107496) | OpenSSL CMS_encrypt with malformed EC certificate | trixie vulnerable; no CMS API in current OFF-only source; actual native path **UNVERIFIED** |
| [121482](https://security-tracker.debian.org/tracker/CVE-2026-121482) | OpenSSL CMS/PKCS#7 signed-data verification with CRL-check CPU DoS | trixie vulnerable; no CMS validation API in source; actual link/reachability **UNVERIFIED** |
| [124709](https://security-tracker.debian.org/tracker/CVE-2026-124709) | OpenSSL QUIC stream reset/rejection memory DoS | trixie vulnerable; no QUIC API in current OFF-only JS server; do not overclaim impossible |
| [84786](https://security-tracker.debian.org/tracker/CVE-2026-84786) | OpenSSL DANE client certificate/TLSA combination NULL dereference | trixie vulnerable; no DANE calls in OFF-only source; native/linked path **UNVERIFIED** |
| [88823](https://security-tracker.debian.org/tracker/CVE-2026-88823) | OpenSSL AES-GCM-SIV zero-length AAD mishandling | trixie vulnerable; no AES-GCM-SIV calls in JS source; native/linked path **UNVERIFIED** |
| [95691](https://security-tracker.debian.org/tracker/CVE-2026-95691) | OpenSSL QUIC CRYPTO retransmission use-after-free | trixie vulnerable; no explicit QUIC calls in source; native/linked path **UNVERIFIED** |
| [95692](https://security-tracker.debian.org/tracker/CVE-2026-95692) | OpenSSL AES-GCM-SIV invalid nonce length memory read / IV binding | trixie vulnerable; no explicit AES-GCM-SIV calls in source; native/linked path **UNVERIFIED** |
| [84243](https://security-tracker.debian.org/tracker/CVE-2026-84243) | glibc gettext via attacker-controlled LANGUAGE and crafted .mo file | `glibc 2.41-12+deb13u5` vulnerable; current OFF-only server does not set LANGUAGE or load catalogs; runtime environment/attacker-writeable paths **UNVERIFIED** |

Important nuance: Grype labels these 12 **HIGH**, while Debian/upstream may rate individual functional conditions differently. The label is a **scanner result**, not a confirmed remotely exploitable node-level vulnerability. The current Node24 OFF-only entrypoint imports only `node:http`, `node:events`, `node:path`, `node:url`; returns health200, Product API503, other paths404/405; only one source file is COPY'ed into nonroot distroless image, with no Firebase, crypto, CMS, QUIC, TLS server, DANE or user-provided `LANGUAGE` configuration. Still, **package presence and possible Node/native linked dependencies need confirmation** before any signed risk acceptance.

## 4. What can be concluded today

- The new image **successfully built**, real Linux Node24/nonroot/readonly/OFF-only/SIGTERM smoke PASS, verified scan archive SHA256s, Syft JSON/CycloneDX PASS, Grype report VALID. Previously stored screenshots support these claims; no repeat work.
- **Trixie package-level known vulnerabilities remain**. Do not describe `NONE_LISTED` as a permanent absence of patches.
- For an *initial C1A PRIVATE default-OFF* rehearsal only, narrow **limited runtime exposure** is a plausible hypothesis because the source has no Product write/publish or QUIC/CMS/DANE/AES-GCM-SIV routes. This **does not authorize** C1A; image publisher/provenance, exact effective IAM, operator/ingress, all-provider gross cost and explicit finite C1A approval remain required.
- Any *future C2 enabled seller/guest* scope is separate and requires positive runtime/callpath evidence, 12 specific CVE dispositions, separate old Step04 15 severe A8 CVE dispositions, Firebase/nonce TTL/media/cleanup/rollback, IAM and budget. No overriding blanket CVE exception is granted.
- **DO NOT** silently upgrade to Debian unstable, switch distros, replace pinned image, bypass scanners, delete the locally retained image, or rebuild/deploy without separate owner consent.

## 5. NEXT ONLY independent work (no scanner re-run)

1. **Source-only** map these twelve CVEs to the actual OFF-only entrypoint and Node/native dynamic links using **existing generated image/SBOM** already preserved in WSL; do not need a new image or network scanner. Mark each row `NO_EXPLICIT_PATH`, `LINKED_BUT_NOT_USED`, or `POSSIBLY_REACHABLE` only if supported by concrete evidence. A static source-only observation is not proof of nonreachability.
2. Complete exact **C1A PRIVATE default-OFF risk disposition/owner packet**, separately accounting for 12 NEW image distinct HIGH IDs and earlier 15 OLD A8 distinct severe IDs (never add the two counts as unique CVEs).
3. If owner wants to progress hosting, receive explicit finite C1A permission after identity/ingress/cost/rollback/provenance evidence; neither current consent nor passing scan is deployment permission.

**Status:** `STEP05_NEW_GATEWAY_SECURITY_SCAN=PASS_WITH_LIMITS_12_HIGH_IDS`; `CVE_PACKAGE_TRIAGE=SOURCE_ONLY_PRELIMINARY`; `C1A_READY_FOR_DEPLOY=NO`; `C1A/B/C2_NOT_APPROVED`; `STEP05_NOT_DONE`; `PRODUCTION_NO_GO`.


## 6. 24 Nov 2026 — NEW native linkage screenshot: GCC/glibc present, OpenSSL not in Node snapshot

Owner ran the requested **new narrow, local, OFF-only image library inspection** against `oldx-step05-gateway-off:wsl-once-20261124-801` with Linux read-only, network-none, `--cap-drop ALL`, `no-new-privileges`, and `/nodejs/bin/node -e` printing `process.report.getReport().sharedObjects`. The screenshot shows the following complete reported loaded-object list:

```
linux-vdso.so.1
/lib/x86_64-linux-gnu/libdl.so.2
/lib/x86_64-linux-gnu/libstdc++.so.6
/lib/x86_64-linux-gnu/libm.so.6
/lib/x86_64-linux-gnu/libgcc_s.so.1
/lib/x86_64-linux-gnu/libpthread.so.0
/lib/x86_64-linux-gnu/libc.so.6
/lib64/ld-linux-x86-64.so.2
```

This is **a snapshot of a separate `node -e` process in the same exact image**, NOT a complete trace of the actual long-running Gateway server under every request. It establishes which shared objects were loaded at the time of **this test**; it does not prove absence of static code linkage, deferred `dlopen`, changes on codepaths or any negative exploit proof.

### Mapping against the 12 distinct HIGH CVE IDs (NO fresh scanner run)

| Family / CVE IDs | New runtime evidence | Narrow source-only assessment |
|---|---|---|
| `gcc-14`: `CVE-2026-102010`, `CVE-2026-95619` (8 Grype matches across 4 binary package names) | `libstdc++.so.6` and `libgcc_s.so.1` **loaded** in Node process. `libgomp1` not explicitly shown; `gcc-14-base` is package metadata, not a separate loaded shared object. | **LINKED; FUNCTION-SPECIFIC EXPOSURE NOT YET DEMONSTRATED.** No evidence that `erase_if` or aligned allocation vulnerable paths are reachable from untrusted HTTP in OFF-only handler. Their mere presence is still an outstanding supply-chain risk, NOT an automatic acceptable exception. |
| `openssl`: `CVE-2026-107493`, `107494`, `107496`, `121482`, `124709`, `84786`, `88823`, `95691`, `95692` (9 package matches) | **Neither `libssl*.so` nor `libcrypto*.so` appears in the reported loaded-object snapshot.** `libssl3t64` remains present as confirmed by Grype packaging. | **NO DYNAMIC LOAD OBSERVED IN THIS PROCESS, NOT PROVED UNREACHABLE.** OFF-only JS source has no explicit TLS/QUIC/CMS/DANE/AES-GCM-SIV invocation. Node can use embedded crypto or lazily loaded code on other paths; inspect only if required for a formal enabled risk disposition. |
| `glibc`: `CVE-2026-84243` (1 package match) | `libc.so.6` **loaded** in Node process. | **LINKED; GETTEXT/LANGUAGE TRIGGER NOT YET DEMONSTRATED.** OFF-only JS does not load untrusted `.mo` files or set attacker-controlled `LANGUAGE`; the Linux base/runtime environment and library calls have not been conclusively traced. |

**Interpretation:** All 12 vulnerabilities remain valid *scanner findings*. This test narrows investigation, not a substitute for patching, publisher attestation or security-owner acceptance. Continue to treat the OFF-only PRIVATE Cloud Run C1A proposal as **RISK HOLD**, with any future public/ENABLED C2 depending on independently approved security proofs. Do not call `libssl` absent from the image—only absent from this one `sharedObjects` list.

**Next independent SOURCE-ONLY action:** prepare a tightly constrained C1A **private disabled 503-only** risk-disposition decision record from these existing facts: residual runtime/bundled package risks, mandatory ingress+IAM, approved exact operator/tester, non-production immutable-image provenance, incremental regional gross cost and new-service-only rollback. Request C1A-specific owner approval only after gaps can be filled. No repeated Grype/Syft, Docker build, old 84 tests, A8 scan, Vercel or Cloud inventory. **C1A hosted never approved here; PRODUCTION NO-GO.**
