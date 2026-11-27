# BAJUTO / OLDX Step05 H2S — permanent single-sign Firestore ledger, source-only (27 Nov 2026)

## Actual baseline — preserved, no repeats

Previous new OAuth metadata groups actually ran on Owner's offline Node `24.22.3` WSL Docker: `OLDX_H2S_METADATA_NEW_TESTS=PASS_3_GROUPS`, **3 pass/0 fail**, log SHA256 `c3690a533fff72d598691701c46c6dd29091ab8dad16d4e82e6b7f75d79e9289`. Source commit `27d5ae3c19ce769d5e802c5e02d2b71648be00ff`; see [actual evidence](OLDX_STEP05_H2S_METADATA_OAUTH_SOURCE_AND_NEW_TESTS_2026-11-27.md). Even earlier H2S KMS mock 3/3 PASS (its shell wrapper only had a reporter-format STOP); **never rerun** those, H2R/H2Q/H2P2/H2P1/H2O/H2N/H2M, existing CI, builds or scans. H2R real CryptoKey-level `roles/cloudkms.signer` policy readback PASS for verified Gateway UID `107238619872767759560`; **no actual Gateway-runtime KMS `asymmetricSign` has happened**.

## New source-only 1-sign durable budget

- `scripts/c2-h2-firestore-one-sign-budget.mjs`, **Git blob `e7cd8fa7082da9dd2e097e8f03b3e82fff2fbabb`**; committed on `security-hardening-review`. Independently new contract, **not** the `createC2StagingRunBudget` Product quota.
- `scripts/c2-h2-firestore-one-sign-budget.test.mjs`, **blob `d380a817f50fa9bd693df5182ff548d8588ad92b`**: three NEW focused cases authored (default-OFF/invalid contract; independent simulated instances racing fixed record; failed transaction and expired/different approval/nonce cannot reset). **NOT RUN**.
- Existing `createStagingMarketplaceBinding` / `requireStagingMarketplaceBinding` source and Firestore transaction wrapper reused, targeting existing allowed `marketplaceRateLimits_v1` collection in staging `(default)` database. No SDK initialization, no new collection/Firestore Rules, no Google calls and no IAM adjustments.
- Unique **permanent global document ID is deterministically fixed** to `oldx-staging`, verified Gateway UID and pinned KMS KeyVersion `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1`. Run ID, `approvedPlanSha256`, nonce digest or a later time window **do not** enter this record ID and cannot restart quota. Uses actual trusted Firestore transaction adapter's `runTransaction(...,{maxAttempts:3})`; transaction reads the fixed record and writes one permanent consumed/timestamp/receipt record **only when missing**. Otherwise `allowed:false`; ambiguous commit error fails closed.
- Sign window <=120 seconds and explicit approval/nonce digest *matching* guards. The digest fields are NOT cryptographic authorization by themselves: independently signed/verified Owner authorization is still required. No `expiresAtMs` or Firestore TTL timestamp field is written in the consumed tombstone: deleting/TTL-expiring the record could erroneously re-enable the same KMS sign, so **no automatic cleanup, manual deletion or TTL for this record**. The record is deliberately persistent across host instances and restart. The source is not an operational guarantee if an administrator deletes the tombstone, if rules/permissions are later changed, or if two independent deployments are allowed to bypass this adapter.
- The KMS transport already consumes budget BEFORE obtaining metadata token and before attempting KMS. **If KMS fails or its response is ambiguous after budget consumption, the budget stays consumed; there is NO automatic retry, rollback, overwrite, reset or re-use of the one-sign grant.** Manual read-only reconciliation and a newly scoped Owner decision would be needed. Google documents transactions as atomic and possible retry on conflicts <https://firebase.google.com/docs/firestore/manage-data/transactions>. Google Firestore TTL only applies to documents with the configured timestamp field <https://firebase.google.com/docs/firestore/ttl>.
- Any future hosted use must separately confirm the Gateway service account has precisely scoped access to this one document; current Cloud IAM/Firestore authorization is **NOT verified**. A role grant/deploy is a new live operation and requires a separately scoped approval. Do NOT alter staging deny-all rules or use Owner WSL OAuth as a shortcut.

## Exactly three NEW local mock tests — SOURCE READY / NOT EXECUTED

Runner `scripts/step05_h2s_one_sign_new_three_focused_offline_once_20261127.sh` at immutable commit `7e112c44eadf0c3806919745acf50107fc4877c4`; Git blob **`aade1023b8467f280edbcb999fe90c6d65a01271`**.

It pins tested source commit `729722568a8af33a43c33e69935c690c51c3f803`, verifies six exact Git blobs, reuses cached local image `oldx-h1a-c2-mediator-off:local-20261124t195244z` and its configured absolute `/nodejs/bin/node` (without assuming PATH), sets Docker `--network none`, read-only mount/rootfs, nonroot UID, no pull/build/scan, and invokes **only** `node --test --test-reporter=tap scripts/c2-h2-firestore-one-sign-budget.test.mjs`. Requires exact TAP tests 3/pass 3/fail 0/skipped 0/todo 0; private local stdout and SHA256 retained. No prior H2S group is invoked. The input Firestore is a local fake SDK, not the real or emulator Firestore.

### One Ubuntu root WSL paste (only if ready to run NEW offline tests)

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2s-one-sign-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/test.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/7e112c44eadf0c3806919745acf50107fc4877c4/scripts/step05_h2s_one_sign_new_three_focused_offline_once_20261127.sh' &&
test "$(git hash-object "$d/test.sh")" = 'aade1023b8467f280edbcb999fe90c6d65a01271' &&
bash -n "$d/test.sh" &&
bash "$d/test.sh"
~~~

Only when Owner's actual output explicitly says `OLDX_H2S_ONE_SIGN_LEDGER_TESTS=PASS_3_GROUPS` together with TAP `# tests 3/# pass 3/# fail 0`, record this NEW offline test PASS. On STOP do not rerun/delete its marker; inspect output/evidence for a focused source fix.

## Still open (H2S is NOT a hosted release)

- **KeyVersion status authority:** a separately trusted `getTrustedKeyVersionStatus` callback must independently confirm KeyVersion **/1 is ENABLED**, exact `RSA_SIGN_PKCS1_2048_SHA256` algorithm, pinned DER SPKI SHA256 `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`. Gateway `roles/cloudkms.signer` alone does **not** authorize status/public-key viewing; no fake `ENABLED` status or broader KMS IAM grant as workaround.
- **Actual Cloud Run Gateway**: immutable image and private revision, attached Gateway UID `107238619872767759560`, exact Invoker/audience, metadata OAuth token source, a true authorized `oldx-staging/(default)` Firestore transaction binding, atomic ledger retention/cleanup boundary, and ability to reconcile an uncertain KMS sign. None verified live.
- **No live action authorized here:** no IAM/RBAC changes, Firestore/TTL/Rules writes, cloud deployment, `:asymmetricSign`, enabled Product publication or production GO.

**Checkpoint:** `H2R=ACTUAL_PASS`; `H2S_METADATA_TESTS=ACTUAL_PASS_3_0_CONSUMED`; `H2S_ONE_SIGN_LEDGER=SOURCE_READY_STATIC_READBACK_PASS_TESTS_NOT_RUN`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`. Public brand BAJUTO; OLDX technical names remain unchanged.

## 27 Nov 2026 ~21:03 IST — OWNER ACTUAL ONE-SIGN LEDGER OFFLINE 3/3 PASS

Owner supplied Ubuntu WSL screenshot of the *new* pinned `scripts/step05_h2s_one_sign_new_three_focused_offline_once_20261127.sh` (script source commit `7e112c44eadf0c3806919745acf50107fc4877c4`, Git blob `aade1023b8467f280edbcb999fe90c6d65a01271`). Actual stdout shows:

~~~text
OLDX_H2S_ONE_SIGN_NODE=24.22.3
OLDX_H2S_ONE_SIGN_SOURCE_COMMIT=729722568a8af33a43c33e69935c690c51c3f803
OLDX_H2S_ONE_SIGN_ONLY_TEST=scripts/c2-h2-firestore-one-sign-budget.test.mjs
TAP version 13
ok 1 - NEW H2S one-sign budget default OFF, invalid approval and input never write
ok 2 - NEW H2S one-sign Firestore transaction allows one across independent instances
ok 3 - NEW H2S one-sign budget fails closed on transaction failure, window and expired tombstone
# tests 3
# pass 3
# fail 0
# cancelled 0
# skipped 0
# todo 0
OLDX_H2S_ONE_SIGN_LOG_SHA256=bfa15cef660b8ebf109fda99e18696d361d56258ca31ca822598fb42fcfe90f8
OLDX_H2S_ONE_SIGN_LEDGER_TESTS=PASS_3_GROUPS
OLDX_H2S_ONE_SIGN_LOCAL_EVIDENCE=/root/oldx-h2s-one-sign-ledger.uKAmJcKp
OLDX_H2S_ONE_SIGN_CLOUD_WRITES=NONE
OLDX_H2S_ONE_SIGN_BUILDS_PULLS_SCANS=NONE
OLDX_H2S_H2_PRODUCTION=NO_GO
~~~

**Actual scope:** ALL THREE new mock-based Firestore transaction tests PASS and runner PASS on cached Node 24.22.3, 0 failures. SHA256 is copied from the Owner screenshot; underlying WSL log is private and was not independently rehashed from this chat. This is NOT a live Firestore write, Cloud Run invocation or real KMS signing. Earlier metadata token 3/3 and synthetic KMS transport 3/3 remain separately completed, NOT rerun.

**Consumed one-shot:** `/root/oldx-h2s-one-sign-ledger.uKAmJcKp/one-sign-focused-attempt.marker`; **NEVER rerun** the ledger test runner, earlier accepted tests or H2R/H2Q/H2P2 etc. Never clear markers, reset the global signer tombstone, rebuild or scan previous images for this check. The offline test only establishes code behavior with a fake Firestore transaction double. **No Cloud IAM, Firestore, Cloud Run, KMS or production changes.**

**Next:** independently trusted KMS KeyVersion /1 status and public SPKI source; actual private Gateway runtime image/attached UID/Invoker; Firestore least-privilege authorization and tombstone no-TTL proof; separate owner-scoped approval for any real Cloud calls. `STEP05=ACTIVE; H2/PRODUCTION=NO_GO`.
