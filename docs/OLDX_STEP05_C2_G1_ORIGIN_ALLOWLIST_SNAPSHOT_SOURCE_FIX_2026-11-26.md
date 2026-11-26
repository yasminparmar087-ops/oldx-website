# OLDX Step 05 — Independent C2 G1 source-only origin allowlist hardening while W6SA on HOLD

**26 November 2026**, repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Owner instruction: "ok aagal vadho" after screenshot-verified reversible disable of the exact H1B test SA. Prior source, image/scan, Registry push, IAM/cloud probes, W0/W1/W3V/W3–W6/W6SA markers **all consumed** and are NOT repeated. **No live H2 enablement or production go**.

## Actual W6SA boundary (no redo)

Owner WSL actual status:
```text
H1B_W6SA_RESULT=PASS_EXACT_NEW_SA_DISABLED_UID_VERIFIED_24H_HOLD
H1B_W6SA_SA_UID=115445220422157278526
H1B_W6SA_DISABLED_AT_UTC=2026-11-26T16:44:17.346536+00:00
H1B_W6SA_SA_DELETED=FALSE
H1B_W6SA_DO_NOT_REPEAT=TRUE
```
Earliest **review** after >=24h is **27 Nov 2026 22:14:17 IST**, NOT automatic permanent deletion. The new H1B test Run service was already UID/etag-deleted, four 403/200/503/404 tests PASS, the standalone G2B image remains retained, older C1A resources untouched. Canonical [owner W6SA exact receipt](OLDX_STEP05_H1B_W6SA_ACTUAL_DISABLED_24H_HOLD_2026-11-26.md).

## Genuinely new SOURCE-ONLY C2 G1 issue found and fixed

Inspected actual current source `functions/staging-marketplace/c2-website-node-http.mjs` (original blob `7e14cf4ae4eba4cfc75d234daedf56f2648138d0`) and existing four-case `tests/integration/step05-c2-website-node-http.test.mjs` (blob `b2468d6fb3529f1cb4a9c8de24e95daf1135d848`). The source checks `allowedOrigins` *once* at factory construction but used the **same mutable input array** in requests and CORS response filtering thereafter. If the embedding application mutated its array after constructing the handler, an additional unreviewed origin could be admitted. The preexisting C2 website mediator factory already cloned its allowed origins, but the Node HTTP adapter did not; this is a specific source-level trust-boundary inconsistency, not proof of a hosted exploit.

**Fixed `functions/staging-marketplace/c2-website-node-http.mjs`:**
- New construction-time `approvedOrigins = Object.freeze([...allowedOrigins])` **only after** bounded array and exact HTTPS origin validations.
- Readiness check and every per-request origin/CORS allowlist lookup use `approvedOrigins`, not the caller's mutable `allowedOrigins`.
- Existing default-OFF, IAM header rejection, trusted website origin, request/body/response limits, HTTPS and no implicit SDK/token/network provider unchanged.

Source commit `e75c180d2b020861554a42e34e31e76ce5cbe324`, **GitHub verified new blob `14b111c25fb08282f5fa5616f318f2f436910213`**.

**Added one NEW focused regression** `tests/integration/step05-c2-origin-snapshot.test.mjs`: after constructing a source-only Node loopback handler, mutates the caller-owned allowed origins array to add an evil origin and remove a formerly permitted one; expects **newly added evil Origin blocked 403 with zero mediator dispatches** and **originally permitted site still accepted 200 exactly once**. New test file commit `8c12450fc01e7a6fec288a142728626550fb57f4`, verified GitHub blob `dc0f768d251520bd668f1cc40b9a1cd72ac6896f`.

### Verification truth

- GitHub fetch of BOTH exact changed files completed; expected static implementation, test source and blob identities verified.
- `node --test` for the NEW test is **NOT EXECUTED in the owner environment yet**. No PASS/FAIL is claimed from syntax inspection alone, and none of the historical 4 G1 / 7 C2-S1 / 84 old source test groups was rerun.
- GitHub commit messages contain `[skip ci]`, no repeated broad CI or live GCP/billing/SDK operation requested. No source-based correction enables any live H2/G3–G6 gate.
- There is no local checkout of this private repository in the assistant execution container; owner can run ONE exact, bounded isolated test from these immutable Git blobs. No need for Codex, Cloud Shell, Docker or Firebase.

### One focused test on owner WSL (new code only; no old suites)

```bash
umask 077
d=$(mktemp -d /root/oldx-c2-origin-source.XXXXXXXX) &&
mkdir -p "$d/functions/staging-marketplace" "$d/tests/integration" &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/functions/staging-marketplace/c2-website-node-http.mjs" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/8c12450fc01e7a6fec288a142728626550fb57f4/functions/staging-marketplace/c2-website-node-http.mjs' &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/tests/integration/step05-c2-origin-snapshot.test.mjs" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/8c12450fc01e7a6fec288a142728626550fb57f4/tests/integration/step05-c2-origin-snapshot.test.mjs' &&
test "$(git hash-object "$d/functions/staging-marketplace/c2-website-node-http.mjs")" = '14b111c25fb08282f5fa5616f318f2f436910213' &&
test "$(git hash-object "$d/tests/integration/step05-c2-origin-snapshot.test.mjs")" = 'dc0f768d251520bd668f1cc40b9a1cd72ac6896f' &&
node --test "$d/tests/integration/step05-c2-origin-snapshot.test.mjs"
```
Expected if fixed behavior is correct: `tests 1`, `pass 1`, `fail 0`. This is a *prediction*, **not a measured result**. If Node unavailable, script cannot be said to pass. On error stop; do not alter GitHub main, old CI or Cloud.

## Real Step05 exit remains open

The master Step05 requirement is **one genuine hosted Product seller/buyer vertical slice including authenticated owner write/publish/withdraw, denied routes, buyer read, quota/retry and exact synthetic cleanup**. The earlier private compiled-OFF H1B (503) is a useful safety proof, **not enabled Product acceptance**. Existing G1 source-only website host is not approved as an H2 active public/website endpoint; G2 real signing key/runtime identity and request proof, G3 Firebase/defaultDB least privilege, G4 media/publication, G5 durable nonce/TTL and cleanup and G6 enabled risk/rollback are genuinely open. Do not invent a mock PASS, enable an environment flag, grant public Invoker, provision KMS or modify Firebase/Rules without separate reviewed authority. The current task is one narrow C2 G1 source hardening change with no paid Cloud writes.

**Current:** `W6SA=ACTUAL_DISABLED_24H_HOLD`, `C2_G1_NODE_ALLOWLIST=FIX_COMMITTED_TEST_SOURCE_READY_NOT_EXECUTED`, `C2_H2_ENABLED=NO_GO`, `STEP05=ACTIVE_NOT_DONE`, `PRODUCTION=NO_GO`.
