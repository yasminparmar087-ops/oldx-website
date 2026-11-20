# OLDX Step 04 — C4 source-only residual-risk decision packet
**Prepared 21 November 2026 after C3 LOCAL signature verification. Source-only; no automatic waiver, deployment, IAM, Registry write, scan or cost approval.**

## A. Frozen C1→C3 evidence — do not repeat

- Target **private** Artifact Registry OCI **index**, pinned: `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-npmfree-20261121-a1@sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`. Already read-only verified local Docker's `.Descriptor` matches remote OCI index SHA256/mediaType/856B; remote AMD64 manifest and config SHA/size, 10/10 ordered local vs remote RootFS `diff_ids`, ten remote compressed-layer HEAD/advertised-size responses, and pinned runtime user/entrypoint/CMD passed. These checks are frozen and have individual documented limits; full compressed-layer byte hash independently not performed.
- Original C1 single-push script printed `STOP_C1_OUTCOME_POSSIBLY_REMOTE_CHANGED` and its one-shot journal was consumed. Later successful targeted read-only remote reconciliation does **NOT** rewrite that runner's original `STOP` into `SUCCESS`. Never rerun C1 `--execute`, reupload, retag, rebuild or rescan merely to make a green result.
- **C3 local keyless signed custody**: owner already approved public disclosure of Yasmin Google signing identity. Cosign **v3.1.4** ran `sign --upload=false --bundle=<owner-local file> IMAGE@sha256:<index>` once, created the local 6,947-byte **Sigstore v0.3 DSSE** bundle `D:\OLDX\G2\c3-cosign-v3.1.4\oldx-c3-index-20261121-a1.sigstore.json` with SHA256 **`1ce7427b1d5dbb3b1c13cfd9a97b690d5c94d20f3509516c8014259c933d896`**, retained exclusive journal `oldx-c3-sign-20261121-a1.attempt.txt`, and cleaned temporary WSL Docker credentials. Local bundle content has exact single subject index SHA256, Fulcio cert and one tlog entry.
- **21 Nov ~04:30 IST actual owner screenshot:** `cosign verify-blob-attestation --bundle <this exact local bundle> --certificate-identity yasminparmar087@gmail.com --certificate-oidc-issuer https://accounts.google.com --digest 0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79 --digestAlg sha256 --type https://sigstore.dev/cosign/sign/v1` returned **`Verified OK`**. Valid exact certificate identity/issuer, cryptographic DSSE signature, signed subject digest, predicate, transparency verification under default safe Cosign policy. **C3_LOCAL_SIGNED_INDEX_BUNDLE=PASS**, not a Registry-hosted signature.
- **No signature/referrer was uploaded to Artifact Registry** (`--upload=false`). Future C5 verifier must either securely receive this exact local bundle with exact trusted signer policy, or separately obtain owner approval for narrow Registry attachment and associated storage/network cost. No standing permission for OCI attach. No retrospective trusted builder SLSA or complete byte-chain proof is created by signing.

Sources: [C2/C3 packet](OLDX_STEP04_C2_C3_NO_REUPLOAD_RELEASE_GATE_2026-11-21.md), [canonical no-rebuild custody route](OLDX_STEP04_NPMFREE_NO_REBUILD_CUSTODY_ROUTE_2026-11-21.md), [owner's Issue #17 audit](https://github.com/yasminparmar087-ops/oldx-website/issues/17). No secrets, login URLs or authorization codes are stored.

## B. Frozen npm-free image scan: remaining **1 CRITICAL + 5 HIGH** (plus 12 MEDIUM, 2 LOW)

Historical **one-shot** frozen npm-free derived-image Grype scan is `CRITICAL=1; HIGH=5; MEDIUM=12; LOW=2` on offline DB snapshot, not a live scanner view. Its private unfiltered report and local source artifacts remain owner-local **D:**; previously verified report SHA256 `142e52449a4c610d79c2cefd8193f70c671bb58c643710a3fe64a7c85bf03a89`, source SHA `fcc96574b6388dc441a0b5d3eade48e79c7ebb24`, summary SHA256 `e263d56102bc0a5656a704d952eb4e35be8d7b9310ac66f8a53bd3d704125bea`. Existing nonroot / Node / Sharp / Firebase / health-200 / default-off-503 / shutdown local runtime smoke was completed at original one-shot execution. **No new scan or runtime test is authorized or needed merely to prepare this packet.**

The [BellSoft nine-severe evidence tracker](OLDX_BELLSOFT_9_CVE_TRACKER_2026-11-19.md) identifies the following six **remaining** APK `nvd:cpe` matched IDs in the npm-free report after three earlier nested `npm/undici` GHSA findings were removed via npm-free runtime design. The mapping below is a **source-only cross-reference**, not a fresh parsed scan or a new vendor VEX:

| CVE | Package in frozen report | Severity | Known bounded evidence | CURRENT disposition / decision needed |
| --- | --- | --- | --- | --- |
| `CVE-2019-1010022` | glibc `2.43.0-r14` | **CRITICAL** | Earlier Red Hat / Ubuntu notes dispute security classification; still shows as Grype CPE match | **OPEN**; no BellSoft-index-bound signed NON_AFFECTED VEX / independent qualified acceptance. Do not dismiss automatically |
| `CVE-2019-1010023` | glibc `2.43.0-r14` | HIGH | Reported vulnerability is executing `ldd` against crafted ELF; runtime exposure not proven | **OPEN**, path-specific candidate low reachability, not confirmed non-affected |
| `CVE-2026-0861` | glibc `2.43.0-r14` | HIGH | Prior BellSoft advisory/fixed-version evidence notes r14 floor; generic `nvd:cpe` scanner match remains | **OPEN**, require precise vendor version/scope mapping or signed VEX; don't erase report |
| `CVE-2026-19499` | glibc `2.43.0-r14` | HIGH | Same prior BellSoft fixed-version evidence, scanner CPE match | **OPEN**, source-conditional risk review |
| `CVE-2026-84243` | glibc `2.43.0-r14` | HIGH | Same prior BellSoft advisory fixed r14 evidence, scanner CPE match | **OPEN**, source-conditional risk review |
| `CVE-2026-119586` | sqlite-libs `3.54.1-r0` | HIGH | Official SQLite advisory associates exposure with particular CLI `.recover` followed by unsafe second command, not ordinary SQLite library API; `sqlite3` executable presence and reachability unproved | **OPEN**, bounded code-path/CLI availability decision needed |

Source: [BellSoft nine-CVE tracker — latest severe triage](OLDX_BELLSOFT_9_CVE_TRACKER_2026-11-19.md), [one-shot npm-free frozen evidence](OLDX_STEP04_NPMFREE_LOCAL_ONESHOT_2026-11-20.md). The tracker explicitly cautions that `nvd:cpe` matches, fixed-version advisories and application-specific exposure are distinct; absence of a visible exploit path or a publisher advisory alone is **not** proof of universal safety. Do **not** claim six CVEs fixed, zero HIGH, or G2 PASS.

## C. C4 controls and exact next bounded decisions

1. **C4 Risk register:** preserve each exact CVE, detected package, severity, source-specific advisory, version/package mapping, route reachability, compensating controls, owner acceptance or STOP, and reviewer/date. Owner's earlier desire to launch eventually even if vendor patch is unavailable does **not** automatically waive C4, authentication/privacy or live protection checks.
2. **Provenance:** Record separately: `LOCAL_OWNER_WSL_BUILD=KNOWN` and runtime smoke/Grype scan evidence frozen; `INDEPENDENT_TRUSTED_ORIGINAL_BUILDER_SLSA=UNVERIFIED`, `REMOTE_COMPRESSED_LAYER_BYTES_FULL_SHA=NOT_INDEPENDENTLY_CHECKED`, `C3_LOCAL_SIGNED_CUSTODY=VERIFIED`, `C3_REGISTRY_SIGNATURE_ATTACHMENT=NOT_DONE`. Signing cannot retroactively change original build provenance.
3. **Verification transport:** Decide if guarded C5 can verify **the existing local bundle** under an exact owner certificate/issuer allowlist, or whether Registry-hosted signature/referrer is a mandatory operational dependency. **Do not** upload a Registry signature solely because C3 local PASS; separate costs and operator approval would be required.
4. **C4 release decision:** Keep `C4_RISK_ACCEPTANCE=PENDING` until the six severe findings have individual dispositions and practical mitigations tied to exact frozen digest plus qualified reviewer/owner decision. Future new fix is an alternative, not a reason to alter the frozen OCI or rerun existing tests now.
5. **G4/G8 independently:** effective Firestore access limitation on other databases remains OPEN; all-provider financial hard stop not yet proven. A verified signature does not bypass either. C5 private/default-OFF staging (503, min0 etc) must stay non-activated until actual scoped guarded release gate, rollback, spend/retention and explicit approval; production remains NO-GO.

## D. Current milestone and next work

```text
C1_REMOTE_INDEX_CHILD_CONFIG_ROOTFS_BLOB_AVAILABILITY=PASS_WITH_DOCUMENTED_LIMITS
C2_LOCAL_REMOTE_INDEX_DESCRIPTOR_IDENTITY=PASS
C3_OWNER_LOCAL_KEYLESS_SIGNED_INDEX=CRYPTOGRAPHICALLY_VERIFIED_PASS
C3_REGISTRY_SIGNATURE_REFERRER=NOT_ATTACHED
C4_RESIDUAL_CRITICAL_HIGH_RISK_ACCEPTANCE=PENDING
G2_SECURITY_CLEARANCE=HOLD
G4_CROSS_DATABASE_IAM=OPEN
G8_ALL_PROVIDER_SPEND_STOP=OPEN
C5_STAGING_RELEASE=NOT_AUTHORIZED
STEP04=HOLD
PRODUCTION=NO_GO
```

**Next source-only task:** Independent, bounded six-CVE disposition matrix review with exact BellSoft advisories and freeze-safe original Grype locations, then a real scoped owner decision on compensating controls and the necessity of Registry signature attachment. No old C1/C2/C3 operations or scans rerun; don't leak original raw local report into public GitHub. As new official security evidence arrives, evaluate *only material deltas* through the existing scheduled G2 watch, not repeated full research.
