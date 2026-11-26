# OLDX Step05 C2 G1 — ACTUAL new Origin snapshot regression PASS

**26 Nov 2026 ~22:26 IST — Owner WSL screenshot.** Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Actual command was executed by Owner on `OLDX-Ubuntu-24.04` root in Docker from the **already retained** Node24 H1A image `oldx-h1a-c2-mediator-off:local-20261124t195244z`. The assistant did not execute the Owner's runtime or access Google Cloud.

## Actual screenshot evidence

- Earlier WSL `node --test` failed because `node` was not installed in WSL. That was **not a test failure**.
- The same shell had ALREADY downloaded and Git-hash-verified two pinned exact files; they were NOT redownloaded for the Docker test:
  - `functions/staging-marketplace/c2-website-node-http.mjs` at blob `14b111c25fb08282f5fa5616f318f2f436910213`.
  - `tests/integration/step05-c2-origin-snapshot.test.mjs` at blob `dc0f768d251520bd668f1cc40b9a1cd72ac6896f`.
- Owner invoked `docker image inspect` of the retained local H1A tag and a single `docker run --rm --pull never --network none --read-only --cap-drop ALL --security-opt no-new-privileges --user 0 --pids-limit 64 --memory 256m` using only the read-only bind-mounted previously downloaded test directory. There was **no new Docker build, image pull, vulnerability scan, Registry push, hosted HTTP, Firebase, Cloud Run or IAM action**.
- New test stdout:
```text
C2 G1: post-setup mutation cannot broaden the trusted Origin allowlist (184.357332ms)
tests 1
suites 0
pass 1
fail 0
cancelled 0
skipped 0
todo 0
duration_ms 392.604018
```
- **Actual narrow result: PASS 1 / FAIL 0.** Confirms the source fix's regression expectations: an Origin injected into the caller-owned array *after handler construction* is denied (403, no mediator dispatch) and an originally permitted Origin remains permitted (200). This does not demonstrate that the H2 enabled host, KMS proof, Firebase privilege, media publication, shared nonce or full Step05 Product seller/buyer lifecycle is ready.

## No-repeat boundary and next actual work

- **Do not rerun this test**, redownload the same two files, reinstall Node merely for it, rebuild/scan the retained H1A Node24 image, repush G2B, repeat any G1/W0/W1/W3V/W3-W6/W6SA one-shots or rerun old 4/7/84-case suites.
- Both source fix and new test are committed to `security-hardening-review` (source commit `e75c180d2b020861554a42e34e31e76ce5cbe324`, test commit `8c12450fc01e7a6fec288a142728626550fb57f4`).
- H1B private OFF four-probe trial previously passed; exact new Run service deleted. H1B SA UID `115445220422157278526` was **disabled**, not deleted, at 26 Nov 2026 22:14:17 IST; earliest 24-hour UID/dependency-guarded deletion *review* is 27 Nov 2026 22:14:17 IST, **not automatic deletion**. Frozen Registry image remains retained, old C1A leftovers untouched.
- **Step05 still IN PROGRESS:** true ENABLED authenticated Product owner/seller write+publish+withdraw, denied routes, buyer read, quota/retry and guarded synthetic cleanup have not been demonstrated on a hosted staging transport. C2 G2 real trusted host/identity/request-proof, G3 Firebase least privilege, G4 media/publication, G5 durable quota/nonce/cleanup and G6 enabled release/rollback remain separately gated. Existing owner approvals covered the PRIVATE OFF H1B experiment, not public or H2 enablement. Production remains NO-GO.
- Fast path now: work on **new source-only enabled Product contract/identity/cleanup gaps**, without repeating proven private OFF security checks or requesting real resource writes before an explicit narrow H2 approval.

**Status:** `C2_G1_NODE_ORIGIN_SNAPSHOT=ACTUAL_PASS_1_0_CONSUMED`, `NODE_WSL_MISSING=WORKAROUND_REUSED_EXISTING_OFFLINE_DOCKER`, `H1B_SA=DISABLED_24H_HOLD`, `STEP05=IN_PROGRESS`, `H2/PRODUCTION=NO_GO`.
