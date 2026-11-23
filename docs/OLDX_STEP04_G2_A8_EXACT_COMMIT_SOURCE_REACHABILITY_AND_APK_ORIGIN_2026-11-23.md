# OLDX Step04 G2 A8 — exact-built source runtime reachability audit and one offline package-namespace check

**Date:** 23 November 2026. **Scope:** source-only GitHub audit of the exact source revision used for Cloud Build, plus no-new-scan preparation. **No server, registry, IAM, API, Firebase, Cloud Run, billing, file or deployment changes** made by this audit.

## Source identity and coverage

The immutable new A8 image was built from Git commit `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`, build `2506826f-ab8d-41a6-a60c-3f2ea3e74bd5`, image digest `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`. Owner's prior one-shot SLSA verifier result and decoded signed material source/image/builder consistency are PASS. Historical operations have been consumed; no reruns.

**Actual inspected source at this exact Git commit**, not merely a current moving branch: `Dockerfile.product-read.bellsoft-npm-free`, `functions/staging-marketplace/product-read-server.mjs`, `functions/staging-marketplace/runtime.mjs`, `package.json`, `cloudbuild.step04-g2-npmfree-one-shot.yaml`, and all **27 JavaScript module files** explicitly copied by the Dockerfile (nine `functions/` and `features/` together, plus scripts). The 27 files were fetched and checked for direct patterns `node:quic`, `node:tls`, `node:sqlite`, `sqlite3`, `.recover`, `ldd`, `child_process`, `spawn`, `execFile`, `DANE`, `CMS_verify`, `PKCS7`, `PEM_X509_INFO_read_bio_ex`, `createSecureServer`. This is a **bounded static string/API scan**, not exhaustive data-flow analysis or complete third-party package/node-native analysis.

### Positive source findings (actual code, not runtime proof)

- `product-read-server.mjs` imports `createServer` from **`node:http`**, creates an HTTP server at the owner's API route and two health paths, with 10,000ms request/header timeouts, 16,384-byte max header and 32,768-byte body. It does not construct a QUIC or HTTPS listener; Cloud Run's managed frontend may terminate HTTPS independently.
- `main()` activates staging only when `OLDX_PRODUCT_READ_ACTIVATE_STAGING==='true'` and other strict scope checks pass. Otherwise protected owner route returns 503, health remains 200. Do NOT confuse source default OFF with currently hosted revision environment proof.
- The staging initializer checks `oldx-staging` project, `(default)` Firestore ID, metadata project, compute identity email, rate limits and rejects credential/proxy/emulator environment overrides. This is source code gating, not an effective IAM permission-denial test for other databases.
- Dockerfile pins the BellSoft hardened-nodejs base by OCI digest; build-time `USER 0` removes npm after strict identity/version check, then switches final `USER appuser`, and runs `product-read-server.mjs`. Final actual image runtime user/permissions MUST still be independently observed; Dockerfile directives do not constitute hosted runtime evidence.
- Direct `node:crypto` imports in copied app files are restricted to `createHash` and `randomUUID` on inspected sources; no high-risk low-level OpenSSL PEM/CMS/DANE/QUIC invocation was observed in those app modules.
- `package.json` brings in `firebase-admin 14.5.1`, `sharp 0.35.5`, `qrcode 1.5.4`. Native/dependency/Node internals are not covered by those negative direct-source scans. When enabled, Firebase Admin SDK communicates externally and may use TLS indirectly; this does not establish OpenSSL DANE/PEM/CMS exploitability or absence.

### Risk interpretation by CVE entry point

- OpenSSL CVE-2026-107494 and CVE-2026-124709 require QUIC-specific paths; **no directly opened QUIC listener found in 27 inspected application modules**. Cannot claim absence from all dependencies or from other deployed services.
- CVE-2026-84786 DANE-enabled client and CVE-2026-121482 CMS/PKCS#7 with CRL verification: **no direct API invocation found** in copied JS modules; unexamined native transitive paths remain unverified.
- CVE-2026-107493 non-NULL existing PEM stack: no direct call in copied JS, but Node/SDK/native implementation reachability is not proven absent. Upstream OpenSSL describes this as condition-specific (severity Low upstream on its 3.5 bulletin), whereas Grype report calls the package finding High; both classifications must be kept with provenance, not silently overwritten.
- SQLite CVE-2026-119586 uses sqlite CLI `.recover` workflow (as recorded in earlier vendor disposition); no command invocation in copied JS modules, but **presence of sqlite executable or OS-level invocation in immutable container is NOT proven absent**. A `sqlite-libs` package vulnerability match alone is not proof the CLI path runs.
- CVE-2019-1010023 `ldd` supplied binaries likewise has no `ldd` invocation in copied JS files; this is not a signed negative runtime proof.

**Do not conclude five CVEs fully cleared, all seven BellSoft candidate fixes installed, or G2 PASS.** BellSoft's package-vendor branch must be positively bound to the private immutable image.

## Next: ONE compressed-private-Grype offline package PURL evidence check (PREPARED, NOT RUN)

We already scanned the exact image once with Grype v0.122.1; the old report is still at `$HOME/oldx-a8-grype-new-digest-2506826f.json.gz` in Google Cloud Shell HOME. Its original decompressed SHA256 from owner's screenshot: `d5dab942824a3bf48c2680e879699e51af7a30142e4e23a52e13493de5e60783`. This **purely local** command verifies report hash/image match/counts, prints only `apk` PURL namespace and type/version for four severe package names. It reads no credential material or raw report content to terminal. A Grype-produced PURL is SCANNER METADATA, not a signed proof of BellSoft APK origin; if it says Alpine, do not treat its vendor advisory as a positive BellSoft package binding. If absent/unexpected, do not force a conclusion.

```bash
python3 - <<'PY'
from pathlib import Path
import gzip, hashlib, json, re

path = Path.home() / 'oldx-a8-grype-new-digest-2506826f.json.gz'
want_hash = 'd5dab942824a3bf48c2680e879699e51af7a30142e4e23a52e13493de5e60783'
want_image = ('asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/'
              'oldx-step04-g2-cloudbuild-20261122-a1@'
              'sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc')
names = ('glibc', 'libcrypto3', 'libssl3', 'sqlite-libs')

try:
    with gzip.open(path, 'rb') as f:
        raw = f.read()
    if hashlib.sha256(raw).hexdigest() != want_hash:
        raise ValueError('RAW_REPORT_SHA_MISMATCH')
    report = json.loads(raw)
    target = (report.get('source') or {}).get('target') or {}
    if want_image not in str(target.get('userInput', '')):
        raise ValueError('IMAGE_IDENTITY_MISMATCH')
    matches = report.get('matches')
    if not isinstance(matches, list) or len(matches) != 46:
        raise ValueError('MATCH_COUNT_MISMATCH')
    print('A8_PRIVATE_GRYPE_REPORT=VERIFIED_READ_ONLY')
    print('A8_ORIGINAL_IMAGE_DIGEST=PASS')
    for name in names:
        artifacts = {(m.get('artifact') or {}).get('id'): (m.get('artifact') or {})
                     for m in matches if (m.get('artifact') or {}).get('name') == name}
        if not artifacts:
            print('A8_PACKAGE_' + name.upper().replace('-', '_') + '=NOT_FOUND')
            continue
        for a in artifacts.values():
            purl = str(a.get('purl') or '')
            match = re.match(r'^pkg:apk/([^/@?]+)/', purl, re.I)
            ns = match.group(1) if match else 'NOT_ESTABLISHED'
            ns = re.sub(r'[^A-Za-z0-9_.-]', '_', ns)[:55]
            ver = re.sub(r'[^A-Za-z0-9_.+-]', '_', str(a.get('version') or 'UNKNOWN'))[:55]
            typ = re.sub(r'[^A-Za-z0-9_.-]', '_', str(a.get('type') or 'UNKNOWN'))[:30]
            print('A8_PKG=' + name + '|VERSION=' + ver + '|TYPE=' + typ +
                  '|PURL_NAMESPACE=' + ns)
    print('A8_PURL_NAMESPACE_IS_SCANNER_METADATA_NOT_SIGNATURE_PROOF')
    print('A8_CLOUD_READS_WRITES=NONE')
    print('A8_BUILD_SCAN_SLSA_RERUN=NONE')
except Exception as e:
    print('STOP_A8_OFFLINE_PACKAGE_ORIGIN_CHECK')
    print('A8_PRIVATE_REPORT=NOT_PROVEN_BY_THIS_CHECK')
    print('A8_CLOUD_READS_WRITES=NONE')
PY
```

After the owner result, if BellSoft origin is still uncertain, prefer one **read-only artifact/SBOM package provenance** method rather than a new build or re-scan, subject to available existing evidence. Use vendor status only within the correct Stream distribution. Next G2 runtime/nonroot/default-DB guard, then G4 effective other-DB/Cloud Run invoker and G8 provider-wide spend risk. A future owner can accept unresolved CVE risk under separately documented scope, not erase scanner findings.

**State:** `A8_SOURCE_REACHABILITY_STATIC_CHECK=BOUNDED_COMPLETED`; `A8_PACKAGE_ORIGIN_POSITIVE_PROOF=OPEN`; `A8_RUNTIME_HOSTED_PROOF=OPEN`; `STEP04=HOLD`; `PRODUCTION=NO_GO`.

Official external reference: https://www.openssl-library.org/news/vulnerabilities-3.5/index.html ; vendor/CVE linkage and 15-ID inventory already collected in [prior document](OLDX_STEP04_G2_A8_15_SEVERE_CVE_VENDOR_DISPOSITION_2026-11-23.md).
