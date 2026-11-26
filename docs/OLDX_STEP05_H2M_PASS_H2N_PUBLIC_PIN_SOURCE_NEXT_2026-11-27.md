# OLDX Step05 — H2M owner actual PASS and H2N limited read-only public SPKI pin

**27 Nov 2026 ~00:30 IST**, latest Owner screenshot verifies H2M actual result `PASS_ONE_NEW_RING_KEY_SOFTWARE_VERSION_VERIFIED`, exact project oldx-staging, region asia-south1, ring oldx-c2-h2-signing, signing key oldx-c2-attestation-rs256 and version /1. Owner confirmed both create attempts + readbacks. **H2M one-shot consumed, never repeat.** Earlier H2L/H2K and all older one-shot checks also consumed. [Updated H2M owner evidence](OLDX_STEP05_H2M_SOURCE_READY_ONE_NEW_KMS_SIGNING_KEY_2026-11-27.md).

## Next new H2N source — PREPARED / NOT EXECUTED

**Scope:** exactly two new Google Cloud KMS read-only HTTPS GETs, in order:
1. GET https://cloudkms.googleapis.com/v1/projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1
2. GET the exact same version + /publicKey

No repeat of earlier broad inventory, no create/write/sign, no IAM/policy, KMS private key export, Firebase, Cloud Run, image, billing, H2 activation or production. H2N requires H2M actual successful local marker + exact saved sanitized evidence, Yasmin isolated native WSL gcloud credentials, only exact URLs with no redirects/retries and exclusive new one-shot marker.

Checks: version name, ENABLED state, SOFTWARE protection, RSA_SIGN_PKCS1_2048_SHA256 algorithm; PEM public key format, built-in strict DER SubjectPublicKeyInfo parse, 2048-bit RSA modulus, exponent 65537, RSA OID; CRC32C of PEM when Google returns optional pemCrc32c; SHA256 of canonical SPKI DER matching the existing source signer pin contract. Stores local public PEM + sanitized JSON with the resulting pin; prints fingerprint, never OAuth token. **403/partial/timeout STOP, not permission for grants or retry.** Optional checksum absent is recorded as NOT_PROVIDED_BY_API, not claimed verified.

- Source-only commit: c43bc3757436e916be999ea49d2c355cc25ad4d8
- Git blob verified: 8321bfd03fc81762478576648d929069e6ce242d
- Path: scripts/step05_h2n_kms_public_spki_pin_readonly_once_20261127.py
- Source statically inspected (GET-only, exact URL, H2M marker, no repeat); **Python AST parse and new actual WSL execution not yet verified**.
- Official KMS API: https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/getPublicKey

## 27 Nov 2026 — OWNER EXPLICITLY APPROVED THE TWO READ-ONLY H2N GETs (NOT EXECUTED)

Prior H2M approval covered new KMS resource creation and bounded post-create readbacks, **not a new getPublicKey/pin stage**. Owner explicitly replied **"ha manjuri chhe"** to precisely these two new read-only KMS GET requests and local public SPKI SHA256 calculation/storage. This approval is NOW RECEIVED, limited to the two listed exact URLs, under the existing isolated Owner WSL. No IAM, signing, key creation, resource changes, hosted H2 or production authorized. Execution remains **NOT ATTEMPTED**; do not infer a Google API PASS. No additional Cloud resource creation or IAM roles needed by this source; API may still report 403, which remains UNKNOWN.

### One paste for Owner WSL root — under now-approved H2N read-only scope

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2n-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2n.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/c43bc3757436e916be999ea49d2c355cc25ad4d8/scripts/step05_h2n_kms_public_spki_pin_readonly_once_20261127.py' &&
test "$(git hash-object "$d/h2n.py")" = '8321bfd03fc81762478576648d929069e6ce242d' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2n.py" &&
python3 -B "$d/h2n.py" --owner-approved-exact-h2n-two-public-gets-once
~~~

Success marker: `OLDX_H2N_RESULT=PASS_PUBLIC_SPKI_PIN_VERIFIED_READONLY`. Reports exact version, lowercase SHA256 fingerprint, and CRC status. Partial/STOP means **no repeat**; do not clear one-shot. Do not paste OAuth token, private receipt, or full cloud error message into public GitHub.

**Next after H2N PASS:** independent signer-only IAM decision and real H2 provider bindings; H2/production remain NO-GO. OLDX internal identifiers remain unchanged; BAJUTO public brand decision independent.

## 27 Nov 2026 ~00:36 IST — OWNER ACTUAL H2N PASS (latest, overrides earlier NOT EXECUTED)

Owner WSL screenshot shows the previously SHA-verified source was executed for the two exact newly approved read-only Google Cloud KMS GETs. The actual terminal output is:

~~~text
OLDX_H2N_RESULT=PASS_PUBLIC_SPKI_PIN_VERIFIED_READONLY
OLDX_H2N_REASON=EXACT_VERSION_RSA2048_AND_SHA256_CONFIRMED
OLDX_H2N_VERSION=projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1
OLDX_H2N_SPKI_SHA256=69a50e43b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba
OLDX_H2N_PEM_CRC32C=VERIFIED
OLDX_H2N_CLOUD_WRITES=NONE
OLDX_H2N_SIGN_IAM_H2_PRODUCTION=NOT_ATTEMPTED
OLDX_H2N_DO_NOT_REPEAT=TRUE
~~~

**ACTUAL verified by owner screenshot:** exact /1 version state/algorithm/protection match in H2N source, 2048-bit RSA public key strict DER/PEM parse, Google-reported PEM CRC32C verified, public SPKI DER SHA-256 pinned to `69a50e43b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`. This **public** fingerprint is safe to retain in GitHub; no OAuth tokens, private keys or local private receipts uploaded. `public-spki.pem` remains on owner WSL in its private evidence directory, not in GitHub. H2N actual PASS does not imply KMS asymmetricSign was called, signer runtime has access, Firebase/Auth/media data is configured, hosted Product works, or production is ready.

**DO NOT repeat H2N** or reset `/root/.oldx-step05-h2n-public-spki-pin-readonly-once-20261127` and any H2M/H2L/H2K/earlier one-shot markers. Step05 remains ACTIVE, H2/production NO-GO. Next *independent* gate: ground exact signer-only runtime principal and permissions/IAM attachment scope and separate targeted owner consent before any new Cloud IAM write or signing. Do not automatically enable the disabled prior H1B experimental Service Account UID 115445220422157278526, remove old SA/image, or activate H2.

