# BAJUTO / OLDX Step05 H2S — independently trusted KMS KeyVersion status source (27 Nov 2026)

## Confirmed prior work — do not repeat

The owner screenshot at ~21:03 IST shows **real Node24.22.3 offline one-sign ledger mock tests PASS 3/3 / fail 0**, `OLDX_H2S_ONE_SIGN_LEDGER_TESTS=PASS_3_GROUPS`, and log SHA256 `bfa15cef660b8ebf109fda99e18696d361d56258ca31ca822598fb42fcfe90f8`. [Full actual receipt and consumed marker](OLDX_STEP05_H2S_ONE_SIGN_PERMANENT_LEDGER_SOURCE_2026-11-27.md). Earlier H2S OAuth metadata 3/3 and synthetic KMS mock transport 3/3 are also completed; **no repeat of any completed tests, H2R/H2Q/H2N/H2P2 one-shots, builds, scans or IAM writes**.

H2N already performed exactly 2 previously approved read-only KMS GETs and established at that time:
- Version `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1`
- `state=ENABLED`, `algorithm=RSA_SIGN_PKCS1_2048_SHA256`, `protectionLevel=SOFTWARE`
- Public SPKI SHA256 `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba` (RSA2048)
- H2N one-shot **consumed**. Its point-in-time result must **NOT** be interpreted as a future live Gateway status read; no repeat H2N.

## New source-only KMS-status verification

| Artifact | Verified Git blob | Purpose |
| --- | --- | --- |
| `scripts/c2-h2-independent-kms-version-status.mjs` | `58dd2c656b8e3eff60367eaa731fe6982c97ac23` | **Default OFF** independent status/pinned-public-key verifier. Requires injected exact Version GET and publicKey GET callbacks from an **independently trusted, authorized reader**; never imports credentials or sends network requests |
| `scripts/c2-h2-independent-kms-version-status.test.mjs` | `d12cf0356953ce5d152b4b8798f077c1adc4f9d5` | 3 NEW offline groups: default OFF/invalid time/name; correct exact version metadata vs disabled/algorithm/HSM/name drift; rejected malformed public PEM/CRC, aborted and repeated attempts. **New tests not yet run** |
| `scripts/step05_h2s_version_status_new_three_offline_once_20261127.sh` | `db8033c1f7d9bbb5507ab4d8eba56dabd6132913` | Exact NEW 3-test local runner using previously cached Node24 Docker image, immutable source snapshot `5c1245658dce41a65dd78ee3c2ef4b84eb01e4a4`, three source blob checks, `--network none`, nonroot read-only execution and explicit TAP summary |

Source module behavior: requires exact version `/1`, `ENABLED`, RSA_PKCS1_2048_SHA256 and SOFTWARE. Checks public key is RSA2048 e=65537, recalculates Google-returned PEM CRC32C, hashes its DER SPKI and compares with the exact pinned H2N SHA256. It accepts version and public-key responses only inside a <=120-second approved time window, enforces a 600-ms single-read pair deadline, allows only a single call per adapter instance, fail-closes on error, and produces the normalized fields expected by the existing `createC2KmsRequestSigning`. The callbacks must be bound to exact HTTP endpoints and real independent IAM/transport by a **future trusted private host**. **No real Cloud calls, status reader account, IAM grant, deployed host, signer, Firestore, or production action is created.** Static source checks/readback PASS only.

**Important test limitation:** The previous real H2N public PEM remains in owner's private WSL evidence, **not** committed. These new mocks test positive *metadata* conditions and negative/abort public-key checks, **not** an end-to-end successful full pinned SPKI verification. Never invent a matching PEM or weaken the production SHA pin to make a mock pass. Actual Cloud Run status-provider availability and trust still require independently authorized runtime validation.

**IAM boundary:** Google Cloud official role definition: `roles/cloudkms.signer` contains `cloudkms.cryptoKeyVersions.useToSign` but **not** `cloudkms.cryptoKeyVersions.get` nor `viewPublicKey`. See [official KMS roles](https://docs.cloud.google.com/iam/docs/roles-permissions/cloudkms), [Version GET](https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/get), [PublicKey GET](https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/getPublicKey). Separate reader identity, least-privilege exact status read authority and signed/verified private runtime identity are **pending**, with new owner approval needed before any IAM/cloud change. Never broaden Gateway signer role to `signerVerifier` merely for this verification. Callback-supplied values by themselves are **not** independent cryptographic proof of reader identity. No Owner OAuth sign or SA JSON keys.

## Exactly one NEW offline WSL command — not run yet

Only if proceeding with the *new* status code. Already completed H2S mock suites MUST remain untouched.

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2s-version-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/test.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/73c5e2b4959b78f33863d807df5b02bca7b59ad2/scripts/step05_h2s_version_status_new_three_offline_once_20261127.sh' &&
test "$(git hash-object "$d/test.sh")" = 'db8033c1f7d9bbb5507ab4d8eba56dabd6132913' &&
bash -n "$d/test.sh" &&
bash "$d/test.sh"
~~~

Success only when exact `OLDX_H2S_VERSION_STATUS_NEW_TESTS=PASS_3_GROUPS` and TAP 3 tests/3 pass/0 fail/0 skipped/0 todo. On STOP, preserve evidence and do not blindly repeat or clear its marker. The test image remains the previously cached `oldx-h1a-c2-mediator-off:local-20261124t195244z`; no new build, pull, scan or other suites.

## Remaining critical hosted gate

Independent authenticated status reader (new approval required for access), exact private Gateway runtime revision attached to verified Gateway service-account UID `107238619872767759560`, immutable image digest, Invoker + audience, real Firestore one-sign tombstone writer and permanent retention/no TTL, and one separately approved synthetic KMS `:asymmetricSign` under **Gateway** credentials; all currently **unverified/unexecuted**. Avoid treating source readiness or mock tests as proof of hosted availability.

**Status:** `H2S_STATUS_VERIFIER_SOURCE_READY_TESTS_NOT_RUN`, `H2R_ACTUAL_IAM_PASS`, `H2S_LEDGER_NODE24_3_OF_3_PASS`, `STEP05_ACTIVE`, `H2_PRODUCTION_NO_GO`.

## 27 Nov 2026 ~21:14 IST — ACTUAL NEW KeyVersion status tests PASS 3/3

Owner supplied screenshot from one-shot `scripts/step05_h2s_version_status_new_three_offline_once_20261127.sh` (source commit `73c5e2b4959b78f33863d807df5b02bca7b59ad2`, blob `db8033c1f7d9bbb5507ab4d8eba56dabd6132913`):

~~~text
OLDX_H2S_VERSION_STATUS_NODE=24.22.3
OLDX_H2S_VERSION_STATUS_SOURCE=5c1245658dce41a65dd78ee3c2ef4b84eb01e4a4
OLDX_H2S_ONLY_TEST=scripts/c2-h2-independent-kms-version-status.test.mjs
TAP version 13
ok 1 - NEW H2S status: default OFF, invalid time and name never read
ok 2 - NEW H2S status: exact version metadata accepts pinned policy, rejects drift
ok 3 - NEW H2S status: wrong public PEM/CRC fails closed; no caching or repeat
# tests 3
# pass 3
# fail 0
# cancelled 0
# skipped 0
# todo 0
OLDX_H2S_VERSION_STATUS_LOG_SHA256=1c6b40e893af416c4499e0a293a3c279205f909769ee3b28bd1841647939edce
OLDX_H2S_VERSION_STATUS_NEW_TESTS=PASS_3_GROUPS
OLDX_H2S_VERSION_STATUS_EVIDENCE=/root/oldx-h2s-version-status-new.6Zj1UPbh
OLDX_H2S_VERSION_STATUS_CLOUD_WRITES=NONE
OLDX_H2S_VERSION_STATUS_BUILDS_PULLS_SCANS=NONE
OLDX_H2S_H2_PRODUCTION=NO_GO
~~~

**Result:** all THREE new focused Node24 mock tests PASS, 0 fail; shell wrapper PASS. The SHA256 is screenshot-transcribed, not independently rehashed from the private WSL log. No real KMS GET, signed response, new IAM, Cloud Run or Firestore action. Status tests validate positive *metadata* and negative public-key/CRC scenarios, **not** a successful live pinned public-key positive. H2N historical owner two-GET fingerprint remains valid point-in-time evidence and its one-shot is consumed.

**NO REPEAT:** Local marker `/root/oldx-h2s-version-status-new.6Zj1UPbh/one-shot-attempt.marker` CONSUMED. No rerun this suite, older H2S groups, H2N/H2R/H2Q/H2P2/Cloud one-shots, scans, builds or marker clearing. Next: independently authorized fresh key-status reader, real private Gateway revision identity/Invoker, and Firestore one-sign document authority; separately scoped approval for actual live cloud checks/signing.
