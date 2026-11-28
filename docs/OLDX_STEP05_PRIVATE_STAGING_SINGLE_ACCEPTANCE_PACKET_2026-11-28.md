# BAJUTO / OLDX Step05 — SINGLE bounded private-staging Seller–Buyer acceptance packet

Status 28 Nov 2026: SOURCE-PREPARED; CLOUD NOT APPROVED; NOT EXECUTABLE. Branch security-hardening-review only.

## 1. Actual basis, do not repeat

- Verified remote HEAD before this packet: d2740c48b3336e664cce2fb5acf3b6615b16ac76. Source implementation d13e16296343284a3c5049011497e8055ff149a2.
- Canonical evidence: docs/OLDX_STEP05_BOUNDED_LIFECYCLE_SOURCE_INTEGRATION_RECEIPT_2026-11-28.md. 18 DISTINCT NEW local Node26 cases PASS by selectively rerunning only affected tests; old 12+7 NOT repeated.
- Three LOCAL HTTP hops simulated exactly six ordered phases: Seller draft save, approved photo publish, Buyer list/detail, Seller edit, Seller withdraw. RSA proofs were local; Firebase, Google, Firestore and KMS providers were simulated. This is NOT live Cloud acceptance.
- Historic H2AD9 single hosted health attempt was NOT_FOUND with zero Cloud Run request logs. H2AF successfully removed temporary Scheduler job, probe Invoker and probe SA; DO NOT rerun or recreate that probe.
- Original permanent one-sign tombstone remains unchanged; new global multi-sign lifecycle ledger is separate and permanently retained. Neither ledger can be reset, deleted or renewed by new run IDs.

## 2. Fixed source identities and cryptographic pins

| Required item | Exact value / status |
|---|---|
| Project / region / database | oldx-staging / asia-south1 / Firestore (default) |
| Mediator SA / UID | oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com / 100779414920484819274 |
| Gateway signer SA / UID | oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com / 107238619872767759560 |
| Product backend SA / UID | oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com / 106984791114720194680 |
| Existing KMS KeyVersion | projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256/cryptoKeyVersions/1 |
| Crypto algorithm | RSA_SIGN_PKCS1_2048_SHA256 |
| Pinned SPKI SHA256 | 69a50043b9979b8b695ca4dc426bcb58d14666b0dc2da27ce823f57f53d46aba |
| Historical Cloud Run OFF service | projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway |
| Historical OFF image | sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2 — NEVER reuse as enabled image |
| Independent KMS reader SA and numeric UID | UNKNOWN — need actual existing eligible identity or separately approved dedicated reader |
| Independent reader IAM | UNKNOWN — require narrow existing-CryptoKey get version metadata plus public key read, no signing, broad Admin or signerVerifier |
| Independently held operator approval public RSA SPKI PIN and exact signed multi-sign policy digest | UNKNOWN — no fabricated approval or credentials |
| Three distinct NEW enabled mediator/gateway/backend OCI image child digests and source/SBOM/rollback evidence | UNKNOWN — no fresh built/pinned images |
| New actual Cloud Run service/revision UID, private URL, audience, invoker binding | UNKNOWN — historical OFF service is NOT a verified enabled target |
| Synthetic Firebase seller/buyer UID, Product/managed photo ID/revision, cleanup manifest | UNKNOWN — future exact scoped records only |

An historical identity pin or key digest is NOT proof of present service attachment, KMS ENABLED, or current IAM. Backend, mediator and signer SAs CANNOT serve as the separate KMS reader. Do not use Owner OAuth, SA JSON keys or deleted H2AD probe SA as a shortcut.

## 3. ONE future synthetic run, hard bounds

- Maximum SIX separately approved real Cloud KMS asymmetricSign attempts, precisely one fresh canonical RSA proof per phase; historical ONE-sign global tombstone NEVER changed.
- Maximum TWENTY-FOUR exact KMS GET read slots, four per phase: sign-version, sign-public, verify-version, verify-public, via independent reader and permanent atomic budget. No ENABLED cache/fake provider.
- Maximum TWENTY Product requests within TWENTY minutes, exactly TWO synthetic actors, ONE Product, ONE approved managed photo; no real users.
- Ordered phases exactly: seller-save; seller-publish; buyer-list; buyer-detail; seller-edit; seller-withdraw. Match Firebase actor, account/session, request path/body/hash, nonce, correct owner, signed audience and atomic global stage ledger on every stage.
- NO automatic retries after unknown sign, credential, network, read, Firestore transaction or Product write outcomes. Preserve permanent replay/audit receipts and known hashes.

## 4. Minimum preparation / approval sequence

PREPARE (source and existing receipts first): inspect prior evidence ONCE, then fill ONLY missing factual values in section 2. Do not replay completed IAM snapshots, KMS/Scheduler probes, old image scans/builds, tests or receipt writes.

A — Reader: determine whether any genuinely distinct suitable SA already exists with immutable UID and proven privileges. If not, request Owner approval for exactly ONE dedicated reader identity and minimum key-scoped IAM needed for BOTH cryptoKeyVersions.get and cryptoKeyVersions.viewPublicKey. Google CryptoKeyVersion does not have a per-version IAM policy; scope effective permissions on the exact existing CryptoKey and confirm the role/custom-role contents before action. Source-only independent reader is not live identity proof.

B — Approval: obtain independent approval public key provenance, pinned SPKI and OWNER-signed exact 6-sign policy, 20-minute window, 24 reads, 20 requests, two actor UIDs, photo and cleanup rules. Private signing material MUST stay in owner-controlled custody; never GitHub or logs.

C — Images: identify or produce separately approvable NEW immutable enabled mediator, Gateway and backend images; pin each linux/amd64 resolved child digest to source commit with once-only new-image security evidence and rollback. If image has not been built, write 'UNKNOWN' rather than invent digest. No activation of original H2U OFF image.

D — Runtime: bind each real workload metadata identity and exact Cloud Run revision to the corresponding SA+UID and image; real server-side Google RS256 attestation, Cloud Run Invoker, exact HTTPS audience and private ingress transport, native Firebase Auth + Firestore (default) + Storage/media + permanent stage/read/run/guest budgets. Keep OFF if any authority unverified. Private Cloud Run-to-Cloud Run hops may require network configuration beyond a matching project and ID token. H2AD9 NOT_FOUND remains an unresolved private routing gap; do NOT make service public or spin up another Scheduler probe.

E — Approval then one execution: present one Owner decision containing exact names/UIDs/URLs/new image digests/source and security evidence, existing KMS KeyVersion, minimally scoped IAM and new reader, one approved 6-stage synthetic flow with STOP/rollback; obtain separate approval for any preparatory write that cannot be defined with yet-unknown image digest. Deploy private staging only; no real traffic. New hosted health + authenticated service hop must pass before any Product writes. On 404/403/unknown STOP; never hide a failed stage.

F — Cleanup/retention: verify withdraw and buyer invisibility; if Owner separately approves, delete ONLY exact synthetic Product/media and temporary actors after exact-version/owner checks, and rollback to original OFF revision/IAM. Preserve permanent sign and read budgets, original one-sign tombstone, source receipts and logs. Partial outcomes require read-only reconciliation, NOT a retry.

## 5. Executable gate (current decision)

PACKET_STATUS = PREPARED_NOT_EXECUTABLE. Missing: reader SA+UID+effective key-only permission, independent approval signed key/policy, three exact new OCI child digests and real Cloud Run revisions, actual Firebase/media/Firestore host bindings, private IAM/network and hosted health proof, synthetic resource custody and rollback evidence. These values CANNOT be inferred from source-only PASS.

NEXT FAST ACTION: one concentrated host/provider provenance pass that uses existing GitHub receipts first and obtains ONLY unknown facts. Prepare one concise exact-scope Owner approval for unavoidable new reader/images/private staging setup. After approved inputs are concrete, execute one bounded hosted seller→buyer flow. NO new approval, deployment, KMS signing, Firebase writes, IAM mutation or builds occurred in making this document.

Current source modules: scripts/c2-h2-lifecycle-stage-ledger.mjs; scripts/c2-h2-lifecycle-approval.mjs; scripts/c2-h2-lifecycle-kms-status.mjs; scripts/c2-h2-independent-kms-reader-ports.mjs; scripts/c2-h2-independent-kms-version-status.mjs; functions/staging-marketplace/c2-future-role-hosts.mjs; functions/staging-marketplace/c2-g2g6-enabled-host-source-assembly.mjs; functions/staging-marketplace/secure-product-pipeline.mjs.

Google Cloud official references: https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/get ; https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys.cryptoKeyVersions/getPublicKey ; https://docs.cloud.google.com/run/docs/securing/private-networking.

Step05 ACTIVE; H2 hosted GO unverified; production OFF / NO-GO.
