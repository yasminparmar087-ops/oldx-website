# OLDX FAST TRACK — Current resume checkpoint

**Updated 27 Nov 2026, H2L actual PASS and H2M guarded source prepared (NOT run).**
Repository: `yasminparmar087-ops/oldx-website`. Branch: **`security-hardening-review`** ONLY.

Follow [permanent fast-track policy](OLDX_FAST_TRACK_POLICY.md), [AGENTS.md](../AGENTS.md), [master 15-step plan](OLDX_SINGLE_EXECUTION_PLAN_2026-11-13.md) and the newest dated actual evidence. Old entries superseded here remain in Git history and linked canonical receipts. Avoid the 570K+ historical AGENTS read unless a relevant specific detail is missing. No concurrency/force push/main modification.

## ONE current critical-path action

**27 Nov 2026 ~00:20 IST Owner H2L ACTUAL PASS — complete KMS key-ring metadata list is EMPTY in `oldx-staging/asia-south1`.** `OLDX_H2L_RESULT=KMS_POST_ENABLE_METADATA_READ_WITH_LIMITS`, `RING_LIST=COMPLETE_VISIBLE_PAGE`, `RING_COUNT=0`, `RING_NAMES=NONE`, no KMS key/versions or any cloud writes. This is the first *post-activation* ring check; H2K had successfully enabled `cloudkms.googleapis.com`. **All H2R/H2P/H2E/H2F/H2K/H2L one-shots consumed; never rerun or delete markers.**

**Next action = explicit owner approval for NEW KMS resources; H2M guarded SOURCE ALREADY PREPARED and GitHub-readback verified (NOT RUN):** proposed ONE key ring `oldx-c2-h2-signing` plus ONE `oldx-c2-attestation-rs256` KMS CryptoKey with purpose `ASYMMETRIC_SIGN`, algorithm `RSA_SIGN_PKCS1_2048_SHA256`, protection `SOFTWARE`, one initial key version, only in `oldx-staging/asia-south1`. The existing C2 signing source supports exactly this algorithm. Key version has recurring usage cost (USD list rate about $0.06/month per active SOFTWARE version, plus cryptographic operations), and creation is a real new Cloud write. **NOT APPROVED OR CREATED**. Do not use the old KMS API enable consent to create keys, make IAM grants or sign. Exact one-shot Owner WSL source file at [H2M source + scoped one-paste](OLDX_STEP05_H2M_SOURCE_READY_ONE_NEW_KMS_SIGNING_KEY_2026-11-27.md), source commit `dbe9de386f865d828aeb81d0ba61791d54f956dd`, Git blob `c6939b54eb54412bc4e23fdc2411cf962dcdb949`. Separate consent still absent. It creates nothing merely by existing in GitHub; one ring + one key + initial SOFTWARE RSA version are the *only proposed* Cloud writes. New source has no Python AST/runtime verification yet. [Actual H2L receipt and H2M decision](OLDX_STEP05_H2L_ACTUAL_ZERO_KMS_RINGS_H2M_APPROVAL_2026-11-27.md). Other H2 identity, Firebase/media/budget/approval/image/rollback and hosted Product gates still open, H2/production NO-GO.

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
