# BAJUTO / OLDX Step05 H2U — Node24 exact OCI config PASS; pinned OFF Gateway Containerfile candidate

## 27 November 2026 ~22:20 IST — Owner actual child configuration

The owner supplied WSL screenshot after the distinct **read-only** query to the previously verified `linux/amd64` OCI child `sha256:774b396818c5dbc4d9aba312b84d548045939ca6efdadc840a928f205116fc74`. Actual result:

~~~text
OLDX_H2U_BASE_OS=linux
OLDX_H2U_BASE_ARCH=amd64
OLDX_H2U_BASE_USER=65532
OLDX_H2U_BASE_ENTRYPOINT=['/nodejs/bin/node']
OLDX_H2U_BASE_CMD=UNKNOWN
OLDX_H2U_BASE_CONFIG=READ_ONLY_PASS_WITH_LIMITS
OLDX_H2U_BASE_IMAGE_BUILDS_PULLS_SCANS=NONE
OLDX_H2U_H2_PRODUCTION=NO_GO
~~~

The parent immutable **multi-platform OCI index digest** is `sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121`, and its publisher keyless Cosign v3.1.4 identity/issuer/signature was **ACTUALLY VERIFIED** earlier. [Full exact screenshot receipt and distinction between child/index](OLDX_STEP05_H2U_NODE24_AMD64_BASE_CONFIG_ACTUAL_PASS_2026-11-27.md). No layers pulled, new build executed, Docker image published or Cloud resources changed.

## New source-only candidate (COMMITTED, NOT BUILT)

`release/H2U_Containerfile_OFF_ONLY_SIGNED_INDEX_CANDIDATE_20261127`: created commit `a3e262a13425e29bf6bd683a3bf72f136459871d`, Git blob **`4b85cbe44dc7e141f6934d99a91d8ec31cf2868c`**; fetched back and statically checked on current branch.

- Uses `FROM --platform=linux/amd64 gcr.io/distroless/nodejs24-debian13@sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121` — **signed exact multi-platform INDEX pinned**. Docker selects its previously observed exact `linux/amd64` child, not mutable `:nonroot` tag.
- Does not inherit ambiguous base CMD: sets exact OFF app `CMD ["scripts/c2-h2u-cloud-run-private-off-main.mjs"]`; the verified Node base ENTRYPOINT `/nodejs/bin/node` is intentionally **not overridden**.
- Forces `USER 65532:65532`, `OLDX_H2U_MODE=OFF`, `PORT=8080`, `NODE_ENV=production`; `COPY --chown=65532:65532` of **only `app/` and `package.json`** from the previously hash-staged 65-file H2U source context. Does not add npm deps, source tarballs, Owner evidence, tokens or cloud keys.
- This candidate is a usable Dockerfile *source* but was **not executed**. The old sentinel `release/H2U_Containerfile_OFF_ONLY_UNVERIFIED.template` is deliberately preserved unchanged for history and must NOT be deployed by mistake.
- The above metadata confirms declared OCI user/entrypoint, not the **actual running Node binary version**, exact runtime file permissions, derived image vulnerabilities, supply-chain provenance or private Cloud Run IAM.

## Exact local context and next approval gate

Current verified Owner-local source context:
`/root/oldx-h2u-context-permission-recovery.kANeYR1S/output/h2u-off-source-context`, containing `app/`, `package.json`, `SOURCE_SHA256SUMS`, and `RELEASE_PLAN_NOT_A_DOCKERFILE.txt`. Source manifest 65 files, 349667 aggregate bytes, SHA256SUMS file digest `42081779fe50e3ea9bf8d47aa8613c09db33050d46027d757d24efc79a2f6ecc`.

**Proposed one new bounded local build (REQUIRES NEW SCOPED OWNER APPROVAL):** One new `linux/amd64` default-OFF Gateway image only, using above signed-index-pinned Dockerfile, exact existing context and immutable SHA pins; do not modify any source/evidence/marker; prepare a **separate** hash-verifying preflight to fail closed on source list/extra files and exact index/child. Pulling only the specified base layers from public registry would be permitted **after** explicit approval; no Cloud Registry push, no Cloud Run service creation or IAM change. Verify resulting image local digest, Node runtime version/UID, OFF health 200, Save 503, unknown 404, and record logs; old H1A/H1B images not reused as release. Avoid unrelated CI/old tests/scans unless a separate new risk-appropriate derived image scan is approved. **No local build was performed under this source-only step.**

**Future distinct consent:** after local result, one image push and new authenticated private staging Cloud Run Gateway service pinned to its image digest, attached Gateway SA UID `107238619872767759560`, private IAM Invoker/ingress; separately authorize KMS KeyVersion reader, Firestore one-sign durable ledger/no TTL, bounded synthetic sign. Even perfect OFF-only image is not an enabled marketplace pipeline.

## One current decision

Ask the owner for consent for **exactly one local linux/amd64 image build plus new image-specific OFF runtime verification**. Do not automatically imply owner consent for registry push, production, KMS signing or changes to project IAM. If approval is received, author a **single** hash-pinned WSL runner that verifies existing context, downloads only candidate Containerfile, builds exactly once and runs a new image-specific local nonroot OFF smoke. Preserve every old marker and evidence. 

**Checkpoint:** `H2U_BASE_INDEX_COSIGN=ACTUAL_PASS`, `H2U_CHILD_CONFIG=ACTUAL_PASS_WITH_LIMITS`, `H2U_OFF_RELEASE_CANDIDATE=SOURCE_READY_NOT_BUILT`, `H2U_BUILD_APPROVAL=NOT_GRANTED`, `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`.
