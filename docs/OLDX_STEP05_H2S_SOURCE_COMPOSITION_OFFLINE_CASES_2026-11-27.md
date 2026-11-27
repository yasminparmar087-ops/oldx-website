# OLDX Step05 H2S — New default-OFF Gateway KMS composition source (27 Nov 2026)

**Current actual baseline:** Owner H2R KMS CryptoKey IAM grant **PASS**, verified one binding and etag readback. [H2R actual evidence and prior H2S initial source](OLDX_STEP05_H2R_ACTUAL_PASS_H2S_GATEWAY_SIGNING_SOURCE_NEXT_2026-11-27.md). Step05 still ACTIVE, H2/production NO-GO; no KMS asymmetricSign or private Gateway runtime has ever been accepted. No older H2R/H2Q/H2P2/H2P1/H2O/H2N/H2M one-shot should be rerun, markers removed, images rebuilt, or Cloud scans repeated.

## New source-only implementation in this batch

Four files are current and GitHub readback verified on `security-hardening-review`:

| File | Git blob | What changed |
| --- | --- | --- |
| `scripts/c2-h2-gateway-kms-synthetic-transport.mjs` | `b00d0af565775f4b26084e85b148eb99c5d2f89c` | Hardened initial one-shot signing transport; mandatory cross-instance durable atomic sign budget, strict fixed KMS endpoint, metadata-bound injected credential, CRC32C, bounded JSON body/redirect rejection |
| `scripts/c2-h2-private-gateway-signing-composition.mjs` | `a166160adf4062769231d8f2c17468911a51c7a2` | Composes the existing `createC2KmsRequestSigning` (which does real RSA-SHA256 verification) with H2S transport; exact KMS Version /1, public SPKI fingerprint and verified Gateway UID; requires independently trusted key-version status provider |
| `functions/staging-marketplace/c2-h2-gateway-host-source.mjs` | `d07ee96c55cee3388be930b787f0da4453dd1f30` | Uses **existing** `createC2PrivateGatewayHost`; pins Mediator numeric UID, Gateway UID, source image format, IAM audiences, private origins and trusted ports; remains default-OFF and creates no listener |
| `scripts/c2-h2-gateway-signing-source.test.mjs` | `5b87730f26335daf0efd845fc85d38b3dc1d197f` | Three focused OFF/fail-closed, synthetic injected mock sign with CRC and one-shot, and tampering/atomic-budget denial tests; no real credentials or Cloud calls |

**Source gate:** Each file fetched from GitHub and static security checks passed. This is **source-only / not Node runtime tested**. Repo engine requires Node >=24.12.0; the model's separate tool runtime is Node22 and is not a verified substitute. The new focused test command on a suitable existing Node24+ checkout is:

~~~bash
node --test scripts/c2-h2-gateway-signing-source.test.mjs
~~~

This is a **new narrowly scoped test**, not a repeat of the previous 11 G2–G6 PASS groups, Cloud scans, builds or older one-shots.

## Exact trust boundary and remaining source gaps

- The code and tests **never call Google Cloud or change the environment on import**. `enabled=false` by default. No public website route, H2 enabled Product publishing, new SA key or KMS IAM write. No Cloud Run service created or redeployed. Mark **H2S SOURCE PREPARED; not Cloud verified**.
- The intended signer is **only** `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`, UID `107238619872767759560`, for `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1`. KMS public DER SHA-256 from the owner H2N screenshot: `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`. The original PEM remains in private owner WSL evidence, not committed. The existing RSA verifier blocks any unrelated PEM even if injected by a host.
- **Required host ports not yet bound:** independently verified runtime identity and image digest, Cloud Run metadata access token for attached Gateway SA (no Owner OAuth/SA JSON keys/impersonation shortcut), HTTPS KMS transport, **durable transactionally consumed one-sign budget shared across instances**, independent trusted Key Version ENABLED status / fingerprint provider, private Invoker and audiences. Returning a matching `principal/uid` label from a callback is not cryptographic attestation. Runtime IAM and image must be verified separately against actual deployed revision.
- A CryptoKey-level `roles/cloudkms.signer` grant **does not** authorize status/public-key get. The independent status provider is mandatory; do not fake it or grant broader `signerVerifier` to bypass it.
- `consumeDurableSignBudget` is mandatory even though the synthetic transport tracks one attempt per *process*: many Cloud Run instances otherwise permit repeated signs. A local Map test stub can only support offline tests and never a real hosted trial.
- Signature response integrity is limited to KMS response checks at the transport layer, then the existing `createC2KmsRequestSigning` verifies the signature cryptographically with the pinned public key. A static source ready flag does not mean the private host is actually authenticated.
- Before any real H2S probe: verify Node24+ focused tests, binder and trusted metadata/status providers, immutable image provenance, Cloud Run configured runtime SA and authorized Invoker, independent synthetic run authorization and expiry, cleanup/rollback, **then** request a separately scoped owner approval for a private staging-only runtime and exactly one KMS `:asymmetricSign`. No LIVE H2S consent exists in this checkpoint.

**Checkpoint:** `H2R=ACTUAL_PASS_CONSUMED`; `H2S=SOURCE_ONLY_STATIC_READBACK_PASS_TESTS_NOT_RUN`; `STEP05=ACTIVE`; `H2=NO_GO`; `PRODUCTION=NO_GO`. The website brand is BAJUTO; unchanged internal technical names OLDX.
