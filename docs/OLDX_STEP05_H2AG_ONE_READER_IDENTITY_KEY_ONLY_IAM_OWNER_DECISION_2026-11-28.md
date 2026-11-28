# BAJUTO / OLDX Step05 — H2AG minimal dedicated KMS metadata reader; exact Owner decision

Date: 28 Nov 2026. GitHub branch only `security-hardening-review`. Latest direct source/test preparation: one exact key reader policy intent and **5 new locally executed PASS** under Node22.16.0, remote tested-byte Git hashes:
- `scripts/c2-h2-kms-reader-key-policy.mjs` blob `c7c320caff1b9172f3eaa41921e0c01b6ff62a38`
- `tests/integration/step05-c2-h2-kms-reader-key-policy-new.test.mjs` blob `757a74519154f2fa485efdc99e90669fb1a0bb54`.
Tests are **pure source review**, NOT Cloud IAM execution, not KeyVersion status / public PEM reading, not Seller–Buyer hosted acceptance.

**Current factual basis:** Source-only 18 distinct new lifecycle tests PASS in prior Codex receipt at `d2740c48b3336e664cce2fb5acf3b6615b16ac76`. Existing three runtime SAs and UIDs are historically verified (mediator `100779414920484819274`, Gateway `107238619872767759560`, backend `106984791114720194680`). Existing exact CryptoKey has historically one direct signer binding for `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`, H2R actual PASS; NOT proof of immutable present IAM state. Old H2AD9 internal HTTP `NOT_FOUND` unresolved, temporary resources H2AF cleanup PASS. NO earlier evidence confirms another distinct KMS version/public reader identity with full effective permission and immutable UID. Do not recreate deleted probe SA or reuse Gateway signer identity as a reader.

## Proposed H2AG exact smallest new reader identity + IAM scope (NOT YET OWNER APPROVED)

1. Create **only if name is absent** exactly ONE `oldx-c2-kms-reader@oldx-staging.iam.gserviceaccount.com`, project `oldx-staging`, display name `BAJUTO C2 KMS metadata reader`, NO downloadable JSON keys, NO project IAM grant, no owner/Editor, no impersonation.
2. Verify its returned immutable numeric `uniqueId` via exact readback and require `disabled=false` (including omitted default false); check NOT one of existing three workload numeric UIDs or deleted H2AD probe UID. If collision/403/timeout, STOP without setting key IAM; no repeated create.
3. Read **only** the existing exact CryptoKey IAM policy with ETag immediately before write: `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256`. Expect exactly pre-existing nonconditional `roles/cloudkms.signer` member `serviceAccount:oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`; if any changed policy/condition/other grant/ETag mismatch STOP and request separate reconciliation instead of replacing other members. Earlier H2R receipt is not a substitute for fresh preimage.
4. Add **only two key-scoped read-only predefined roles** to the new reader with one ETag-guarded `setIamPolicy` on that exact CryptoKey:
   - `roles/cloudkms.viewer` to read `cloudkms.cryptoKeyVersions.get` (KeyVersion state/algorithm metadata; also other read metadata within exact key).
   - `roles/cloudkms.publicKeyViewer` to read `cloudkms.cryptoKeyVersions.viewPublicKey` (public PEM).
   Preserve the signer role and original ETag/preimage. Verify exact key-level IAM policy by fresh GET; no second IAM write/retry on ambiguous result.
5. Do NOT grant `signerVerifier`, `signer`, `cryptoOperator`, Admin, roles at project/keyring, or Firebase/Firestore/Storage/Cloud Run Invoker to this reader. Do not create cryptoKeys/versions, call KMS signing, read any private key, use Owner OAuth or SA JSON keys for runtime, create a Cloud Run reader service, change gateway ingress, deploy an enabled image, run synthetic data, or activate production.
6. Local operator must be previously verified Yasmin Owner on isolated native WSL SDK/project; one dedicated marker BEFORE any Cloud mutation; strict exact API allowlist, stage-intent receipts, no loops/retry, no partial cleanup auto-execution. If SA is created but key IAM write fails, STOP, retain it disabled or intact for exact later reconciliation under separately approved cleanup. No blind re-create. Source policy helper is only a NONEXECUTABLE review intent, not an authorized API writer.

Google authoritative source:
- KMS Version GET requires `cloudkms.cryptoKeyVersions.get`: https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/get
- Public PEM GET requires `cloudkms.cryptoKeyVersions.viewPublicKey`: https://docs.cloud.google.com/kms/docs/retrieve-public-key
- KMS viewer/publicKeyViewer roles: https://docs.cloud.google.com/iam/docs/roles-permissions/cloudkms
- Cloud Run internal-to-internal egress can require additional private networking (possible H2AD9 404 cause, NOT proven): https://docs.cloud.google.com/run/docs/securing/private-networking

**Approval status:** `H2AG_SOURCE_READY_NOT_APPROVED_NOT_RUN`. The Owner can expressly approve just this exact new reader SA and these TWO existing-key-only read grants/readbacks. No broader cloud consent is presumed from generic 'continue'.

## After H2AG

Still need real reader Cloud Run workload attachment and token access via narrowly authorized host, current ENABLED state and public SPKI verification, three NEW enabled image digests and source security, Firebase/media/durable budgets, exact private networking/hops and hosted six-stage test. A new SA with key-read IAM DOES NOT itself prove server identity or complete Step05.

`STEP05=ACTIVE`; `PRODUCTION=OFF/NO_GO`. Avoid repeated earlier tests, scans, Cloud probes, H2AD/H2AF cleanups.
