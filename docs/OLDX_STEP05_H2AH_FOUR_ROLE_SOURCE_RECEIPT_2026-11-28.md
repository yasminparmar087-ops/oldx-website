# BAJUTO / OLDX Step05 — H2AH four-role source implementation and actual test receipt
28 November 2026 IST. Branch `security-hardening-review` only.

## Actual result

Started from remote `2bc68c161fa9c9988883a5b9dee64bb2cf1b3424`. Implementation `dbc7b5fa6544ce54038aeecacaa598999097ac5e`, final tested source `b8ed873aff7c93a43dc13f163a0f7dda1fe9911d` (distinct-derived-image guard). Documentation follows this source. All commits use `[skip ci]`; branch publication uses expected-HEAD fast-forward, never main/reset/force.

**FOUR_ROLE_SOURCE_IMPLEMENTED / PACKAGING_PREPARED /23 DISTINCT NEW CASES HAVE PASS EVIDENCE.** This is source packaging and local evidence, NOT built images, deployment readiness acceptance, real IAM/network/KMS/Firebase acceptance, Step05 DONE or Production GO.

H2AG Reader SA `oldx-c2-kms-reader@oldx-staging.iam.gserviceaccount.com`, UID `107336955065718475994`, and exact-key viewer/publicKeyViewer grants are prior OWNER ACTUAL PASS. No H2AG/IAM audit/regrant was repeated. Reader runtime attachment/URI/image remains unproven. Prior12+7+18 tests, H2AF cleanup and all consumed operations/markers remain unchanged; H2AD9 NOT_FOUND/zero health logs is unresolved.

## Completed code, not just a plan

- Four independent Node entrypoints: `functions/staging-marketplace/four-role/{mediator,gateway,backend,reader}.mjs`; shared bounded server, exact `GET /healthz`, OFF503 endpoints, no secret diagnostics, SIGTERM handler and connection-close backstop. Expired authority reports OFF and cannot dispatch. Health always says `productReady:false`.
- Four immutable-base linux/amd64 nonroot Dockerfiles, deny-first dockerignore files, per-role package+lock files and exact84-file ESM COPY closures. Runtime base reused unchanged: `gcr.io/distroless/nodejs24-debian13:nonroot@sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec`. Dependency builder reused: `node:24-bookworm-slim@sha256:dc26ae92c9fb15cf6b1d63e20f0944b2efe0f115b20e00be48fb23fceb061c54`. No mutable FROM, secret build args or default enabling.
- Gateway/Reader have zero npm runtime dependencies. Mediator locks Firebase Admin14.5.1 (optional data SDKs omitted at image install). Backend locks Firebase Admin14.5.1, native Firestore9.4.1, Storage8.4.0 and google-auth-library9.15.1. Transitive resolved/integrity records are reused from the existing root lock, not newly researched/upgraded. Root package files unchanged. The verified call closure uses already-processed managed-photo metadata/approved byte reads, not Sharp/raw upload/QR generation; existing whole-app features, Sharp dependency and original images were not removed.
- A source-only bundle CLI enforces a clean isolated review checkout, immutable Git HEAD, exclusive outside-checkout destination and explicit closure. It copies no Git credentials/private config, runs no npm/Docker/registry/Cloud command, and records source revision plus file SHA256. Bootstrap requires matching per-role provenance; the checked-in UNKNOWN placeholder cannot enable anything.
- Controller-signed exact runtime authority checks fixed four SA/UIDs, fresh lease, source, independent attachment evidence, exact four different derived image digests (base/builder/old image digests rejected), four different run.app origins and internal/VPC topology. No arbitrary `authorized:true` callback substitutes for this authority.
- Every private HTTP RPC carries target IAM token AND a separate FULL Google RS256 identity assertion. Its signed audience cryptographically binds canonical short-lived stage context, body hash, source/target/path/policy/reservation and ≤15-second validity. UID/email/audience/body are verified before use. A stripped IAM header is presence/routing only, never authentication proof.
- Cross-process durable ledger RPC keeps native Firestore on Backend. Branded remote proxies cannot substitute in-memory counters or plain callback objects. Backend permits Mediator reserve/finish/guest admission, Gateway sign claims, Reader read-slot consumption; it does not expose generic transactions or arbitrary paths.
- Reader runs separately under its own H2AG identity, not impersonation/sidecar/shared Gateway credentials. Fresh cryptographically verified OWN metadata ID identity precedes its own email/OAuth acquisition. Incoming Gateway/Backend signed context is role/usage-bound; native read slot commits on Backend before exact KMS GET. At most four slots/stage,24 globally; ambiguity, credential failure, concurrency and new client creation do not renew a slot. Reader only returns bounded public version/public-key fields; validates metadata/public-PEM/CRC/RSA shape and refuses disguised private PEM. Caller still validates the immutable historical SPKI. No KMS sign capability on Reader.
- Native runtime plumbing reuses existing mediator/private Gateway/backend, lifecycle approval/stage controller, canonical proof, Firebase actor, owner/privacy, photo/moderation/revision, nonce, cursor, public/run/guest rate and cleanup contracts. ALS holds request-local context ONLY; durable authority stays in Firestore. Mediator independently verifies the synthetic Firebase actor for all six stages, removes Firebase auth for public backend reads, and never forwards browser identity as IAM.
- Genuine Cloud Run header compatibility fixed: Mediator **discards** platform-forwarded signature-stripped X-Serverless-Authorization, rather than rejecting it or trusting it. Independent platform IAM, Firebase user verification, downstream Google assertion and canonical per-request signature remain separate. Header-only/wrong-actor calls cause no stage/sign/KMS activity.
- Real SDK integration avoids the actual Admin Firestore incompatibility with custom Auth credentials: native `@google-cloud/firestore` uses explicit Compute-only GoogleAuth, exact oldx-staging/default database; Admin Auth uses only verified OWN metadata credential; Storage uses explicit Compute auth, no automatic retries. No local ADC/Owner-key/impersonation fallback. Gateway/Reader cannot initialize Firebase SDKs.
- Storage approved-byte adapter is read-only, exact signed provider/bucket/object/generation/size/digest constrained, no upload/delete/provider migration. Missing actual provider/photo mapping remains OFF; native existing Firestore photo/moderation checks still govern publication.
- Single `deployment/four-role/manifest.json` contains four OFF Cloud Run service templates, exact roles, unknown child digests/real URIs, all-traffic Direct VPC + Private Google Access, internal-only ingress, scale0..1 and no old-service mutation. Extra control-plane edges Mediator→Backend and Reader→Backend are explicitly disclosed: necessary to avoid Firestore privileges on those roles, NOT granted here.
- Separate read-only numeric-version config/trust/cursor mounts: `/run/oldx/config/runtime.json`, `/run/oldx/trust/controller-spki.sha256`, Backend-only `/run/oldx/cursor/cursor-key`. Trust-anchor write custody must be independent. Secret names/versions/access grants are UNKNOWN and unapproved; no key, secret or credential was created/imported. Config example is deliberately nonexecutable.

Network choice follows [official internal Cloud Run networking](https://docs.cloud.google.com/run/docs/securing/private-networking): same-project Direct VPC, all-traffic and subnet Private Google Access, default run.app HTTPS. IAM alone is not a network path. Mount template follows [official version/file-path schema](https://docs.cloud.google.com/run/docs/configuring/services/secrets). No conclusion about H2AD9 root cause is claimed.

## Exact source/test/package files and tested-byte Git blobs

- `functions/staging-marketplace/four-role/contract.mjs` — `4198f44550430b52de6a6c75920f41efa2ed2fac`
- `functions/staging-marketplace/four-role/protocol.mjs` — `9e1a8689f253177c0e1b45335ccd11abd7e7cd8c`
- `scripts/c2-h2-lifecycle-stage-ledger.mjs` — `d67984c983ddd7100b0e11c0912f6fef420175cf`
- `functions/staging-marketplace/four-role/ledger-rpc.mjs` — `ea4c66ff7dfd2b3bc3092818930956bc021d6e67`
- `functions/staging-marketplace/four-role/reader-host.mjs` — `da35e01e2e328269af1c7dd15e88eeaae9d3757e`
- `functions/staging-marketplace/four-role/remote-status.mjs` — `a18f35b382cdbb05e4d762c77b10a38965414be9`
- `functions/staging-marketplace/four-role/metadata-oauth.mjs` — `7c85c05f225f73f6973f058f60e45ba30a6854bd`
- `functions/staging-marketplace/four-role/kms-transport.mjs` — `550b32859a79d32a53bbde3d97dc3c6591c685ed`
- `functions/staging-marketplace/four-role/firebase-native.mjs` — `06e151d0453362901ccdda53c1f6f212d1aa7e05`
- `functions/staging-marketplace/four-role/bindings.mjs` — `6a543b2485dc0fa22ea13719e21ac3e8542b079a`
- `functions/staging-marketplace/four-role/bootstrap.mjs` — `2916d16580c79b7b435cf28959878512ee6b932e`
- `functions/staging-marketplace/four-role/server.mjs` — `d1d4fc630308160c4951fb55bd3f2bd18090ecf9`
- `functions/staging-marketplace/four-role/mediator.mjs` — `d1fdef433d1f81d13f1320e0a290d0010614699c`
- `functions/staging-marketplace/four-role/gateway.mjs` — `434388059f53c273fccd8dd82a19119a1c309373`
- `functions/staging-marketplace/four-role/backend.mjs` — `8dbc83bd77580f6fa486129bb2e916bc66fcc72e`
- `functions/staging-marketplace/four-role/reader.mjs` — `2cfec4fc3ad3913c6d6428be24ff33e00d6d1d0f`
- `deployment/four-role/mediator/package.json` — `14aa1002056ea11fe310630c04a7e2fdda07b341`
- `deployment/four-role/mediator/package-lock.json` — `79b5190f551d33749cca3b9dc6a1d9a4549d098a`
- `deployment/four-role/gateway/package.json` — `9ee124d4f79c66830808dbed7f22ab5b2a95c465`
- `deployment/four-role/gateway/package-lock.json` — `64081f29ff3144d93079f36449971b9507c4dec4`
- `deployment/four-role/backend/package.json` — `aa2935a3e0a1756a19b0526efb824ca81910a7f5`
- `deployment/four-role/backend/package-lock.json` — `eb29ef2c2e8c0658b6f723ada893120ace3aac8d`
- `deployment/four-role/reader/package.json` — `ddff76ab05f815afa01dbe5861374ae6d8684e47`
- `deployment/four-role/reader/package-lock.json` — `34528b2accfcbe8b803c687761d9b2c3eb460de4`
- `deployment/four-role/source-provenance.json` — `6d13fb1ef9403dc1a9a8580f13f7cfd346d68128`
- `deployment/four-role/manifest.json` — `aa442a629563fe690350387ee6f6e15eea3256bb`
- `scripts/step05-h2ah-source-package.mjs` — `65e88e57a9ca2fa892a084360512be0e9a932eab`
- `deployment/four-role/Dockerfile.mediator` — `12808d606068265d80d8abe3a743a9763d182f25`
- `deployment/four-role/Dockerfile.mediator.dockerignore` — `7c32ba16eea145bd2ba9efaf55ed67ee3a221e0c`
- `deployment/four-role/mediator/copy-closure.json` — `b00bd880f3045a30166b4c4d77a75b81647e8cb0`
- `deployment/four-role/Dockerfile.gateway` — `621303b6050e12dedc9a075094c058f94dc7475d`
- `deployment/four-role/Dockerfile.gateway.dockerignore` — `3e311a54031ae42f115579e37b1e80d3d759a425`
- `deployment/four-role/gateway/copy-closure.json` — `431e4b5405a409eae6ef70a031df4cf7c6773b5e`
- `deployment/four-role/Dockerfile.backend` — `7f79e582524d69c555b702da361d8081b5231ab1`
- `deployment/four-role/Dockerfile.backend.dockerignore` — `956943df6b254b4cea9c8a35e23406a57ec3c211`
- `deployment/four-role/backend/copy-closure.json` — `9a47f7e1721e76ec8d8b15d7cab6c01e975e72fd`
- `deployment/four-role/Dockerfile.reader` — `f3c03232e0ebea998203b8a6f3401a0aca44cbcb`
- `deployment/four-role/Dockerfile.reader.dockerignore` — `1b7e4b06ff654fcd5aafc889a9605c1aa36830d3`
- `deployment/four-role/reader/copy-closure.json` — `1d78f15fde331b98368e83cc57294c1f570c8e54`
- `tests/integration/step05-lifecycle-http-fixture.mjs` — `d2b720ceeefe73f55a75971e1986264543ddcf83`
- `tests/integration/step05-h2ah-reader-child-fixture.mjs` — `3aede992cbcfb657be70b8068942c28f75315828`
- `tests/integration/step05-h2ah-four-role-fixture.mjs` — `bb5a41255c589af8a4a876842f30fc8672c8c847`
- `tests/integration/step05-h2ah-four-role-runtime-new.test.mjs` — `101e2f366d59e4456a96e5f7d8013ac8c7c1cbf3`
- `deployment/four-role/runtime-config.example.json` — `84b2dda7d0cd389f46c7912e84953b1605fa7165`

Only two existing code/test files were extended: native stage ledger (authenticated remote proxy) and local test fixture (optional identity/status hooks). Other implementation/package/test files above are new. Original H2U server/image and original one-sign/status controls untouched.

## Actual NEW tests, exact limits of evidence

Existing Node `v26.13.0`; existing dependencies, no installation/build/pull/scan/CI. The requested first command ran BEFORE other tests:
`node --test --test-isolation=none tests/integration/step05-c2-h2ag-reader-metadata-source-new.test.mjs`
**6PASS /0FAIL /0SKIP /0CANCEL, exit0,137.4974ms.** Direct repository imports, not the earlier stubbed imports.

New file: `tests/integration/step05-h2ah-four-role-runtime-new.test.mjs`,17 distinct cases. All have passing evidence; no blanket rerun was used after changes. Commands below share `node --test --test-isolation=none` and that NEW file:
- Initial12-case attempt: visible4PASS/8FAIL; process cases hit sandbox spawn EPERM and a context fixture accidentally reused an aborted client signal. The attempt was stopped (exit1), not called PASS. Owned fixture cleanup and independent server-signal fixture were fixed.
- `--test-name-pattern="NEW H2AH full Google"`:1PASS,847.4208ms.
- Local-process access for ONLY affected cases: `--test-name-pattern="NEW H2AH (four executable|Reader process|Reader rejects|wrong Reader|missing Reader|exact real SPKI|six Seller)"`:7PASS,7149.3965ms.
- `--test-name-pattern="NEW H2AH (full Google|expired runtime)"`:2PASS,696.8287ms.
- Local process cases `--test-name-pattern="NEW H2AH (Reader cannot expose|concurrent signed|six Seller)"`:3PASS,3489.3776ms.
- Package/lock closure `--test-name-pattern="NEW H2AH role COPY"`:1PASS,895.7962ms.
- Added actual installed-SDK case initially failed because its test-only resolver hook recursively resolved itself; pre-resolved URLs fixed it. Constructor case then1PASS,9245.6986ms. Extended network-instrumented final `--test-name-pattern="NEW H2AH actual installed"`:1PASS,2144.3127ms (existing SDK root supplied through temporary test-process env). **0 credential acquisitions and0 attempted HTTP/HTTPS/socket/TLS calls** during actual client initialization/close. Local installed versions14.5.1/9.4.1/8.4.0/9.15.1 match role locks. This is not Auth token/Firestore/Storage operation acceptance.
- After correcting numeric-version separate mount templates: `--test-name-pattern="NEW H2AH (bootstrap and|role COPY)"`:2PASS,758.5077ms.
- After genuine forwarded-IAM compatibility fix, local process `--test-name-pattern="NEW H2AH (Mediator never|six Seller)"`:2PASS,2815.9178ms.
- Final derived-image guard `--test-name-pattern="NEW H2AH signed host authority"`:1PASS,589.9083ms.

All passing selections exit0/0FAIL/0SKIP/0CANCEL. Repeated affected cases are NOT added as new coverage: **6 requested +17 distinct new =23 distinct passing cases this batch**. Prior12+7+18 suites and consumed Cloud work were not rerun. Syntax checks applied to new code. No npm ci or container image verification was executed.

Four entrypoints each ran in its own local child process: OFF health200, Product/internal routes503, owned process termination. Windows termination is NOT Linux-container graceful SIGTERM/nonroot evidence.

Positive journey used FOUR actual localhost HTTP roles; Reader was in a separate child process, other three were separate local servers. New production Mediator runtime/Reader host/protocol/remote ledger were exercised with locally generated Google/controller RSA identities and SDK-shaped Auth/Firestore/KMS doubles. Existing Gateway/backend factories used a generated LOCAL intent key. Native transactions are serialized test doubles, not Emulator or real Firestore conflict evidence. Six stages passed (draft→one approved managed photo publish→Buyer list/detail with private fields excluded→edit→withdraw),6 signatures,24 Reader KMS-GET doubles, ledger COMPLETE, public view absent. Concurrent duplicate GET allowed only one native slot; ambiguity/private PEM/wrong UID/missing OAuth were denied.

The real historical PEM was not available. Production pinned signer/backend key resolver correctly REFUSE the generated substitute. Thus this is NOT successful activation of the full real-pin production bootstrap, actual KMS signing or hosted Seller–Buyer proof.

## ONE concrete next owner packet — SOURCE + FOUR NEW OFF IMAGE BUILDS/PUSH ONLY

**Prepared for owner decision, NOT executed/implicitly authorized by source consent.** Approve one consolidated local execution from `b8ed873aff7c93a43dc13f163a0f7dda1fe9911d` (or exact later documentation-only descendant verified to retain these source blobs):
1. Use existing local WSL/Docker and private Windows evidence storage; verified clean isolated review checkout, sufficient local disk, no Cloud Shell/Cloud Build/GitHub Actions. Do not reset owner's dirty checkout, install new paid tools or clear any consumed marker.
2. Generate FOUR exclusive source bundles with the included source-only command, one per role:
   `node scripts/step05-h2ah-source-package.mjs --prepare-source-only ROLE PRIVATE_NEW_CONTEXT_DIRECTORY`.
   It records exact Git revision/closure/lock SHA256; no image command is hidden inside it.
3. At most ONE linux/amd64 build and ONE private registry push per exact target:
   - `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-h2ah`
   - `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-gateway-h2ah`
   - `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-backend-h2ah`
   - `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-kms-reader`
   Use their exact dedicated Dockerfiles/locks and immutable builder/runtime pins above; unique new artifact refs, no old tag mutation. Register four exclusive NEW attempt records before action; never delete/reset them. STOP on any build/push/digest/network/unexpected activity failure; retain partial evidence and no automatic retry.
4. Retain private logs, source/lock/file hashes, BuildKit provenance, pushed index digest (if attestations) AND distinct persistent linux/amd64 child image digest/config ID, size and exact registry ref. A base digest or source Dockerfile hash is NOT a derived-image digest. All FOUR child digests are currently **UNKNOWN_UNBUILT**. No security elimination/PASS is inferred.
5. No Cloud Run creation/deploy/enablement, VPC/subnet/Secret Manager/Invoker change, SA/key/version/credential work, H2AG regrant, live KMS GET/sign, Firebase/Storage data, Rules/Billing, hosted Product execution or CVE-risk acceptance in this build-only packet. No old tests/scans/probes/H2AG/H2AF. Existing security HOLDs persist; later newly built-image vulnerability/runtime evidence needs its separately scoped authority.

Local builds use existing hardware; registry storage/transfer and any external builder usage can cost money. No “free hosted” or new monetary cap is invented. Owner must approve exact build/push usage/retention limits before execution; otherwise STOP rather than upgrade or spend. This source batch itself initiated no paid resource/usage.

## Only remaining real hosted gates

- Four new images/build/runtime provenance/security evidence; Linux Node24/nonroot/certificates/health/SIGTERM/actual SDK install verification. Dependency install and OCI build remain unexecuted.
- Actual Reader service URI/revision/attached H2AG SA UID/image; other three new candidate service/revision/image bindings; independent signed controller evidence/trust-anchor custody and exact lifecycle/release approvals. Do not mistake a prospective signed config or environment string for a verified runtime attachment.
- Exact same-project VPC/subnet/PGA/internal route and six destination-scoped Invoker relations. Existing H2AG key grants DONE, no repeat. Extra ledger RPC edges are NEW future approval scope, not already granted.
- Independently approved read-only configuration/trust mounts and Backend cursor secret/version custody; required Auth revocation-read authority for Mediator/Backend, Backend native default-DB permissions and existing approved photo/provider/generation mappings. No Reader Firestore role, no signer metadata-read broadening and no public endpoint.
- Fresh synthetic actors/photo/moderation/revision/cleanup manifest, real latencies within existing bounded deadlines, and separately authorized6-sign/24-GET/20-request/20-minute hosted acceptance. Permanent ledger/old tombstones remain retained on ambiguity; no retry/reset/deletion. Exact cleanup and rollback need action-specific consent.
- H2AD9 private health routing remains NOT_FOUND/unresolved; no new probe/retry. H2AF cleanup PASS preserved. Initial templates stay OFF; zero-traffic tags can still be invoked/incur costs, so no implicit safety claim.

Owner's local dirty Handoff/untracked .firebaserc, history, all old evidence and strict15-step sequence preserved. Step05 ACTIVE; G2/G4/G8 HOLD and H2/production OFF / NO-GO.
