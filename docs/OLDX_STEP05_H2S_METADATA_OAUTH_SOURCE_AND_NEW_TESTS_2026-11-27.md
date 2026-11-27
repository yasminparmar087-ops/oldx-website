# OLDX Step05 H2S — Cloud Run Gateway OAuth metadata access token, source-only

**27 Nov 2026 — current new work on `security-hardening-review`.** BAJUTO remains the public brand; OLDX internal technical IDs stay unchanged. First preserve actual prior H2S Node v24.22.3 **three focused test groups PASS / fail 0** (with a shell **wrapper-only** TAP reporter mismatch STOP); details in [canonical previous H2S receipt](OLDX_STEP05_H2S_SOURCE_COMPOSITION_OFFLINE_CASES_2026-11-27.md). Previous `h2s-node24-new-focused-test-attempt.marker` is **CONSUMED**. NEVER rerun/reset old H2S/H2R/H2Q/H2P2/H2P1/H2O/H2N/H2M one-shots, old builds/scans or original H2S three test groups.

## Distinct identity types

The existing `scripts/c2-cloud-run-metadata-identity.mjs` fetches **Google ID tokens** intended for Cloud Run IAM invocation and Google-signed attestation (audience-bound). They are NOT OAuth bearer access tokens for KMS. To use `:asymmetricSign`, future *actual private Gateway revision* must obtain an **OAuth access token** through its attached service-account metadata endpoint. Google documentation: [Cloud Run service identity](https://docs.cloud.google.com/run/docs/securing/service-identity), [REST access tokens from metadata](https://docs.cloud.google.com/docs/authentication/rest), [KMS asymmetricSign](https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/asymmetricSign). External documentation is not evidence that the OLDX Gateway workload is deployed.

## New source-only modules (NO Google API or runtime execution)

| GitHub path | Verified Git blob | Purpose |
| --- | --- | --- |
| `scripts/c2-h2-cloud-run-gateway-access-token.mjs` | `95c2681c2e589dea3dccef6197531315fa4b5c62` | New **default-OFF** metadata OAuth token provider, exact two metadata URL GETs (service-account email then token), strict Gateway email `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`, UID pin `107238619872767759560`, strict Google flavor/URL/no redirect/size/JSON/expiry, 1.5-sec deadline, single attempt |
| `functions/staging-marketplace/c2-h2-gateway-runtime-credential-source.mjs` | `8b981bcb54af1a42ff2f486f715c8dbab14998e0` | Default-OFF source binder reuses existing private Gateway host; rejects caller credential overrides, accessor/symbol host config, missing trusted providers; no listener or deployment |
| `scripts/c2-h2-cloud-run-gateway-access-token.test.mjs` | `32c264cca30ef2967e4cd9527f0c4a314ad2b0e9` | **Three NEW** mock-based tests (OFF/no metadata, exact email+OAuth one attempt, wrong identity/token/credential injection rejection); **AUTHORED, NOT EXECUTED** |
| `scripts/step05_h2s_metadata_new_three_focused_offline_once_20261127.sh` | `7e41e6f4102187b015ceadb524ba87f4da7d401a` | One separate local root WSL Node24 runner; cached Docker image, immutable branch-source commit, 7 Git blob guards, explicit `--test-reporter=tap`, no Docker network, source read-only, no build/pull/scan or Cloud |

**Immutable source snapshot for the seven imported files:** `27d5ae3c19ce769d5e802c5e02d2b71648be00ff`. All seven files were fetched using this exact source commit and their Git blob hashes verified before preparing the runner. Old H2S components and accepted old three tests remain unchanged.

The token provider accepts **injected** `fetchMetadata`; it does not open network by default, create an SDK/credential, authenticate Google itself, use Owner WSL OAuth, download SA JSON keys or impersonate. It validates the observed metadata **email**, but the `uid` returned is an immutable **previously verified control-plane mapping**, not cryptographic identity proof from an OAuth bearer token. A fabricated injected callback can mimic responses: **before live use, independently verify actual Cloud Run service and immutable revision attach the exact Gateway SA, image digest, nonpublic Invoker and service audience**, and enforce host-only metadata transport. This is a source-contract boundary, NOT live attestation.

The signer `roles/cloudkms.signer` on ONE CryptoKey is already H2R IAM **actual PASS**, but Google `cloudkms.cryptoKeyVersions.useToSign` permission alone does NOT supply trusted version-state metadata, authenticated public-key status or a durable transactional global signing budget. Required separate host ports remain `getTrustedKeyVersionStatus`, `consumeDurableSignBudget` (cross-instance, not an in-memory Map), `fetchKms`, pinned public key PEM matching SHA256 `69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba`, and actual private runtime image/identity/roll-back evidence. No change in Cloud IAM, Firebase, Cloud Run, billing, image, KMS key or production has occurred in this source batch.

## One NEW isolated WSL test only (not executed yet)

Use only the cached image `oldx-h1a-c2-mediator-off:local-20261124t195244z` and its inspected absolute Node entrypoint, source pinned by hash. The runner explicitly selects TAP reporter, avoiding the previous spec/TAP wrapper-only mismatch. This command runs **only the three new OAuth token-provider test cases**, never the previous H2S three groups or historical 11 C2 groups.

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2s-metadata-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/test.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/be39ceaf4fc7ae9a52905692444020655a345546/scripts/step05_h2s_metadata_new_three_focused_offline_once_20261127.sh' &&
test "$(git hash-object "$d/test.sh")" = '7e41e6f4102187b015ceadb524ba87f4da7d401a' &&
bash -n "$d/test.sh" &&
bash "$d/test.sh"
~~~

Only an actual `OLDX_H2S_METADATA_NEW_TESTS=PASS_3_GROUPS`, matching TAP tests3/pass3/fail0/skipped0/todo0, establishes this NEW mock-tested source gate. If STOP, keep the local evidence/marker; no blind retry. This is NOT hosted signing success.

**Current:** `H2R=ACTUAL_PASS`; `OLD_H2S_3_TESTS=ACTUAL_NODE_PASS_WRAPPER_STOP_CONSUMED`; `NEW_H2S_METADATA_SOURCE=GITHUB_STATIC_CHECKS_PASS_TESTS_UNRUN`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.

**Next single critical decision:** independently verify actual Cloud Run H2 private Gateway service/revision+attached SA and image, and a separate key-version status authority/durable sign budget. Do not conflate prior C1A `oldx-step05-gateway` OFF-only service/old SA with newly verified H2 `oldx-c2-private-gateway` runtime; no H2 private Gateway deployment has yet been proved.
