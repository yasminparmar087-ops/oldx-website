# BAJUTO / OLDX Step05 — G2–G6 new source assembly (first direct feature-integration progress after H2AF)

## 28 November 2026 — source code actually added and pushed

Owner has required that time be prioritized, no repeated checks, direct progress toward Seller→Buyer staging features, and only new necessary tests. This packet continues from the **actual H2AF cleanup PASS** checkpoint [here](OLDX_STEP05_H2AF_OWNER_ACTUAL_CLEANUP_PASS_AND_HOSTED_HTTP_NOT_FOUND_2026-11-28.md) and the prior [consolidated G2–G6 task](OLDX_STEP05_H2AF_PASS_NEXT_SINGLE_CODEX_ENABLED_HOST_BINDINGS_2026-11-28.md).

**New actual source implementation, not just a plan:**
- `functions/staging-marketplace/c2-g2g6-enabled-host-source-assembly.mjs`
- Source creation commit `e653e1a5ddc2adf39fd6df3feb192fd11d86a8c8`
- GitHub readback blob SHA1 `e2b84babf0b837ee70f2fe0a555b523a9aadc94b`.

This new source-only, default-OFF host assembly **reuses existing actual source factories**:
- `createC2WebsiteMediator` and `createC2WebsiteNodeHandler` for the website-to-private-Gateway path;
- `createC2H2MetadataBoundPrivateGatewayHostSource` for trusted Cloud Run Gateway metadata identity, signing and KMS transport;
- `createC2EnabledProductBackend` with `requireC2EnabledReleaseControl` for the independently approved synthetic Product backend.

It pins the three previously Owner-observed runtime service accounts and immutable UIDs:
- Mediator: `oldx-c2-web-mediator@oldx-staging.iam.gserviceaccount.com` / `100779414920484819274`;
- Gateway: `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` / `107238619872767759560`;
- Backend: `oldx-c2-product-backend@oldx-staging.iam.gserviceaccount.com` / `106984791114720194680`.

It rejects old OFF image digests as candidate enabled images, requires three distinct immutable new image digests, consistent Gateway/Mediator origins and identity, and the real non-forgeable `createC2EnabledReleaseControl` object. The Gateway binder still refuses missing trusted KMS version/PEM/workload identity/signing/budget. It deliberately leaves the existing immutable H2U OFF deployment untouched and NEVER substitutes an in-process call for the actual Cloud Run IAM transport. Source composition does **NOT** constitute hosted readiness or release approval.

**New targeted tests authored, not reusing/rerunning old tests:**
- `tests/integration/step05-c2-g2g6-new-host-assembly.test.mjs`
- Test creation commit `3fc7c64e0b986f71901edd402ba2d1209a77cdcc`
- GitHub readback blob SHA1 `1d4d369423a73fcb5655ae634f9ade311f0263dc`
- Four NEW tests: default OFF/503, forged release control denied, approved release alone cannot replace independent missing Gateway key/host providers, and old OFF image / numeric UID drift denied.
- GitHub exact content/allowlist static scope check PASS; both files' JavaScript bodies syntactically parsed in isolated V8 after stripping imports/exports. **These four actual Node tests have NOT yet been run; do not call them PASS.** The local Node test command below is the one new test operation to run next, not all older tests.

```bash
node --test tests/integration/step05-c2-g2g6-new-host-assembly.test.mjs
```

## Still not achieved — exact remaining hosted blockers

No real Google Cloud G2–G6 hosted Product API, Firebase Auth, Firestore transaction, budget, media, KMS signing or Cloud Run IAM end-to-end has been proven by the new source. No deploy, new IAM/KMS/SA/Job, image build/push/scan or production work occurred in this change. Existing H2AD9 single Scheduler attempt ended `NOT_FOUND` with 0 Cloud Run request logs; temporary job/probe IAM/SA were subsequently deleted by H2AF, so **do not repeat those tests** or falsely mark HTTP health as passed.

Remaining trusted-host contracts for the exact minimal 1-Product/1-photo/2-synthetic-actor/20-request/20-minute run:
1. Independently verified KeyVersion `ENABLED` state and public RSA SPKI pin; not derivable from signer-only SA.
2. Real separately approved attached mediator/gateway/backend runtime identities, image digests, Cloud Run service IAM and audience, valid Cloud Run-to-Cloud Run HTTPS transport (no public ingress relax).
3. Actual host-bound cross-instance Firestore one-sign and run-budget atomic transactions with least-privilege backend SA, Auth verification, nonce, media controls and exact synthetic cleanup/rollback.
4. New focused tests for the enabled source assembly/protected host ports, then separately approved hosted staging-only synthetic seller save→publish→buyer read→edit→withdraw. Do not treat mocked source tests as live acceptance.

## Next single efficient Codex action

Codex should read this document and `AGENTS.md`; **first run ONLY the above 4 NEW focused tests**. If any new case fails, edit only related code and rerun just that newly failing case. Then extend the newly committed assembly **without duplicating source factories** to bind the missing independent trusted-host provider ports (KMS version reader, backend Firestore durable authority, release evidence, media cleanup), keeping every dangerous operation default-OFF until actual separately scoped Owner cloud approval. Write new receipt for only the new tests, paths/SHAs, exact still-unknown live gates. Commit/push only `security-hardening-review`, never `main`. Do not re-run H2AF, H2AD, existing H2S/H1B/OCI scans or older Step05 test suites. No Google Cloud API call or deployment in this source-only next action.

**Checkpoint:** `H2AF=OWNER_ACTUAL_CLEANUP_PASS`; `G2G6_SOURCE_ASSEMBLY=NEW_CODE_PUSHED_STATIC_VERIFIED`; `NEW_FOCUSED_TESTS=AUTHORED_NOT_RUN`; `HOSTED_SELLER_BUYER=NOT_VERIFIED`; `STEP05=ACTIVE`; `PRODUCTION=NO_GO`.
