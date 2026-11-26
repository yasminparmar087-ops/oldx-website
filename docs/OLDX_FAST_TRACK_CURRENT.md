# OLDX FAST TRACK — Current resume checkpoint

**Updated 26 Nov 2026, latest H2 G2–G6 provider-readiness preparation.**
Repository: `yasminparmar087-ops/oldx-website`. Branch: **`security-hardening-review`** ONLY.

Follow [permanent fast-track policy](OLDX_FAST_TRACK_POLICY.md), [AGENTS.md](../AGENTS.md), [master 15-step plan](OLDX_SINGLE_EXECUTION_PLAN_2026-11-13.md) and the newest dated actual evidence. Old entries superseded here remain in Git history and linked canonical receipts. Avoid the 570K+ historical AGENTS read unless a relevant specific detail is missing. No concurrency/force push/main modification.

## ONE current critical-path action

**H2E OWNER ACTUAL STOP_AFTER_MARKER, NOT AN API-disabled result.** 26 Nov ~23:19 IST owner WSL screenshot: `OLDX_H2E_RESULT=STOP_AFTER_MARKER`, `REASON=UNEXPECTED_SERVICE_USAGE_RESPONSE`; KMS and Auth states `UNKNOWN_NOT_CHECKED`. **H2E CONSUMED, never rerun or clear marker.** The original H2E code rejected a full Service Usage GET response >64KiB; likely large full-service config, but exact cause unconfirmed. It made the first GET attempt and no resource writes. Both prior project permissions `cloudkms.keyRings.list`, `firebaseauth.configs.get` RETURNED, while direct KMS/Auth metadata 403 remains unresolved.

**Next NEW one-shot (READ-ONLY, not old H2E repeat):** `scripts/step05_h2_exact_two_api_states_fields_recovery_once_20261126.py`, pinned source commit `f228b02cfbbbe4dab8d67cd5398615ca2e56408d`, verified blob `362ffb697ab316e7ed3152cb613c3db5e35e8b6c`. Exactly two fixed partial-response Service Usage GETs with `?fields=name%2Cstate`, old stop-marker guarded and 8KiB cap, new distinct one-shot marker; no old 7 GETs/H2P permission check, IAM, KMS signing, Firebase user or Cloud resource writes. **SOURCE READY NOT OWNER EXECUTED**. [Actual H2E screenshot interpretation and H2F exact operator paste](OLDX_STEP05_H2E_ACTUAL_STOP_RESPONSE_CAP_H2F_TWO_FIELDS_RECOVERY_2026-11-26.md). `H2/PRODUCTION=NO_GO`.

## Verified actual status (latest evidence first)

- **Codex G2–G6 source batch pushed and GitHub HEAD confirmed** at `45f20e8ba0dcc84e4106c998060f4639cbe3ce5e` before the later documentation/readiness commits. Eleven **distinct** new focused test groups PASS *in aggregate* on local Node26, after targeted fixes; **not** full hosted H2 acceptance or one last 11-group run. [Detailed receipt](OLDX_STEP05_C2_SOURCE_ONLY_ENABLED_SLICE_GAP_AND_ONE_PASS_IMPLEMENTATION_PACKET_2026-11-24.md). Default-OFF source contract, independent approval/budget requirements, reused Product lifecycle, IAM/Auth/media/cleanup interfaces; existing legacy backend still publication-OFF. No web UI new public route, cloud enablement, KMS or real media binding. G2–G6 active provider blockers documented.
- **C2 G1 Origin immutable-snapshot source fix + focused regression actual 1 PASS, 0 FAIL** in the previously retained Node24 Docker image, no Node install/new image. [Actual receipt](OLDX_STEP05_C2_G1_ORIGIN_SNAPSHOT_ACTUAL_TEST_PASS_2026-11-26.md). No repeat.
- **H1B private compiled-OFF Cloud Run trial actual PASS**: one new service created, Owner-only Invoker, four HTTP statuses anonymous403/owner200/owner API503/off/unmatched404, same-session exact service UID/etag-guarded deletion CONFIRMED. [Actual receipt](OLDX_STEP05_H1B_W3_W6_ACTUAL_PRIVATE_PROBES_PASS_SERVICE_DELETED_2026-11-26.md).
- New test SA `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, immutable UID `115445220422157278526`, **DISABLED**, NOT deleted, exact readback on **26 Nov 2026 22:14:17 IST**. [Actual receipt](OLDX_STEP05_H1B_W6SA_ACTUAL_DISABLED_24H_HOLD_2026-11-26.md). Earliest separate 24h dependency-review **27 Nov 2026 22:14:17 IST**, not automatic deletion. Do not touch it during present H2 inventory beyond broad project SA listing.
- Frozen H1B G2B verified image `sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e` remains retained. H1A build/SBOM/Grype/runtime PASS_WITH_LIMITS; 12 HIGH in scoped private OFF experiment, not H2 risk acceptance. Older C1A Run service already deleted; C1A SA/image retained with unknown external references. Do not modify them.
- **H2 enabled hosted seller/buyer Product vertical slice NOT VERIFIED**; source-only local synthetic create/publish/buyer/edit/withdraw works within fixtures but real KMS/Auth/Firebase/media/TTL/IAM/provenance and independent approval binding missing. `STEP05=IN_PROGRESS`, `H2=NO_GO`, `PRODUCTION=NO_GO`.

## Provider bindings to decide after real metadata inventory

Exactly three distinct runtime principals, trusted server host and audience/Invoker edges; dedicated `asia-south1` KMS ASYMMETRIC_SIGN RSA-SHA256 version and pinned public key; real Firestore `(default)`/Auth and least-privilege runtimes; managed moderated single photo and cleanup; durable atomic run/nonce/TTL with exact dependent-resource cleanup; independently verified owner authorization and enabled-image security/rollback. No H2 pilot without separate new narrowly bounded owner consent.

## BAJUTO public brand (independent)

Owner working public name **BAJUTO** (બાજુટો / बाजुटो), internal technical IDs remain OLDX. Domain `bajuto.in` **not confirmed purchased**; previous owner intent was purchase in 1–2 days. [Brand decision](OLDX_BAJUTO_REBRAND_PLAN.md). No DNS, trademark, rebrand deployment or product route change based on that intent.

## Strict no-repeat and two lanes

- Never repeat consumed H1A build/scan, G1/G2A/G2B, W0/W1/W3V/W3–W6/W6SA, C2 Origin test, old C1A deletion, old source suites, Cloud billing checks or IAM testing without distinct new evidence and consent. Never reset markers. Preserve private local receipts/credentials in Owner WSL; GitHub only sanitized status/hashes.
- While H2 metadata decision awaits Owner, approved independent source-only P0 website work may continue as long as no conflicting code writer or live/cloud authorization is inferred. Keep Gujarati/Hindi/English UI and Capacitor compatibility. Step05 technical exit remains gated by real authenticated enabled hosted product flow. Steps13/14 separate launch decision and Step15 Android.
