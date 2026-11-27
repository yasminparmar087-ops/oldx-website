# BAJUTO / OLDX Step05 H2U — one approved local immutable image build ACTUAL PASS

**Evidence date:** 27 November 2026 ~22:35 IST (owner's Ubuntu root WSL screenshot).

## Actual result: SUCCESS; one-build authorization CONSUMED

The owner ran the **distinct prebuild-path-recovery runner**
`scripts/step05_h2u_local_build_prebuild_path_recovery_once_20261127.sh`, immutable creation commit `d49426a092dc5a6064937389b432bd1a581c1b40`, verified Git blob `cf43fed7599d0f298c68e9c4be9e795611470201`. This was necessary because the prior runner had STOPPED before build due to missing/hardcoded source context or manifest path. The corrected runner selected existing evidence paths by exact SHA, then used the previous **one approved build**.

Owner terminal output (visible in screenshot):

~~~text
#7 [3/4] COPY --chown=65532:65532 app/ /app/                  DONE
#8 [4/4] COPY --chown=65532:65532 package.json /app/package.json   DONE
#9 exporting to image                                                  DONE
#9 exporting manifest sha256:c165e671e2b231b5b6210f867dacc085d4a53b69fae2998a712019d9b6575243
#9 exporting attestation manifest sha256:e7e790590127630dcc90b39c8018b035b6d2770e59d941d42285cf4d5040f5b8
#9 exporting manifest list sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2
#9 naming docker.io/library/oldx-h2u-private-off:local-20261127-one     DONE
#9 unpacking to docker.io/library/oldx-h2u-private-off:local-20261127-one DONE
1 warning found: FromPlatformFlagConstDisallowed (constant linux/amd64 in FROM --platform)
OLDX_H2U_LOCAL_IMAGE_CONFIG=PASS_NONROOT_AMD64_OFF
OLDX_H2U_LOCAL_IMAGE_NODE_VERSION=24.22.3
OLDX_H2U_LOCAL_IMAGE_RUNTIME_UID=65532
OLDX_H2U_LOCAL_IMAGE_HTTP=PASS_OFF_200_503_404
OLDX_H2U_LOCAL_IMAGE_LOOPBACK=DOCKER_NETWORK_NONE
OLDX_H2U_LOCAL_IMAGE_IID=sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2
OLDX_H2U_LOCAL_IMAGE_RESULT=PASS_NEW_BUILD_AND_OFF_RUNTIME_WITH_LIMITS
OLDX_H2U_LOCAL_IMAGE_EVIDENCE=/root/oldx-h2u-first-local-image.As8Trzvn
OLDX_H2U_LOCAL_IMAGE_CLOUD_WRITES=NONE
OLDX_H2U_LOCAL_IMAGE_REGISTRY_PUSH=NONE
OLDX_H2U_LOCAL_IMAGE_CLOUD_RUN_DEPLOY=NONE
OLDX_H2U_LOCAL_IMAGE_OLD_TESTS_REPEATED=NONE
OLDX_H2U_H2_PRODUCTION=NO_GO
~~~

Owner screenshot also printed three distinct local log digests (not independently rehashed by ChatGPT):

~~~text
build.log SHA256=e4c4fe177f13aaac3db89ac92883405632184a3d853a13b5b509a285f887caea
node-and-uid.log SHA256=20b864bceda4d1f7027dfeb119fac742c44cde56b019c1bb2b3cab68ed84ce0a
image-off-http.log SHA256=54605cdcdd7045f2ffef8e55d73f3bb82548be0d6aaef52287d243b43fa4327f
~~~

These logs remain **Owner-local** and the screenshot-derived SHA256 strings have not been independently recomputed by the assistant.

- **One local image exists only on owner's Docker host**, named `oldx-h2u-private-off:local-20261127-one`.
- **Exact image IID** printed by the runner: `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`. The build output calls this an exported **manifest list** digest. Do **not** assume the local IID is already a remote registry digest or that a registry push has occurred.
- BuildKit emitted an attestation manifest, but this alone does **not** establish that derived-image provenance, signed attestations, and supply-chain requirements have been independently verified.
- Constant platform in Dockerfile produced **one non-fatal lint warning** `FromPlatformFlagConstDisallowed`. This does not negate current PASS; any cleanup is future source-only and must **not** trigger a second build under the consumed one-shot authorization.
- Exact new image-specific config check PASSED, Node binary reported **v24.22.3**, nonroot **UID 65532**. Offline container had `--network none`, read-only root, no port publication; actual HTTP health **200 OFF**, synthetic Save **503 DISABLED**, unknown **404**.
- The **one-build marker** `/root/.oldx-step05-h2u-local-image-build-once-20261127` is **CONSUMED**. Never run either build wrapper again, delete the marker, restage prior sources or re-run previous source, KMS, Cloud inventory, cosign, registry digest queries, image builds or old tests.
- **No Cloud service, registry push, IAM edits, Firestore writes, KMS signing, production or external user access** was performed by this local build.

## Inputs retained: exact source / signed base

Local staged 65 files / 349667 bytes from previously accepted owner-local source context, SHA256SUMS `42081779fe50e3ea9bf8d47aa8613c09db33050d46027d757d24efc79a2f6ecc`, original manifest `12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc`, immutable source Containerfile Git blob `4b85cbe44dc7e141f6934d99a91d8ec31cf2868c`. Parent publisher-signed Distroless Node24 OCI INDEX `sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121`, amd64 child `sha256:774b396818c5dbc4d9aba312b84d548045939ca6efdadc840a928f205116fc74`.

## Next critical path — staged hosting, no new write approval implied

**Next required decision** is an explicitly bounded one-time private staging image upload/Cloud Run H2U Gateway deployment plan. Prepare *source-only* commands and preflight first, do not push/deploy automatically:

1. Choose exact target Artifact Registry repository, region and service name, then validate ownership/billing and policy safely. Do not assume prior Cloud Run `oldx-owner-read` is an H2U Gateway service or repurpose it.
2. Push **the existing locally built image** only after separate owner approval. Do not rebuild it. Verify a *remote registry* immutable manifest digest and ensure its image ID corresponds to the local approved artifact; do not conflate a local IID with a pushed registry digest.
3. Private Cloud Run staging: service `H2U` default-OFF only, authenticated Invoker audience/identity and private ingress, minimum IAM, exact Gateway SA UID `107238619872767759560`, image by remote digest, no public exposure, and controlled rollback/cleanup.
4. Independent KeyVersion status reader, real Firestore durable one-sign budget/no TTL, token/identity mediation and *one separately owner-approved synthetic sign* are distinct remaining H2 blockers. Do **not** enable live Product operations as a side effect.
5. A new derived-image-specific security/provenance check is outstanding; the owner previously accepted some residual CVE risk for launch, but no claimed scan result exists for this newly built image.

**Checkpoint:** `H2U_FIRST_LOCAL_IMAGE_BUILD=ACTUAL_PASS_CONSUMED`; `H2U_IMAGE_SPECIFIC_OFF_RUNTIME=PASS_200_503_404`; `H2U_REMOTE_REGISTRY=NOT_PUSHED`; `H2U_CLOUD_RUN_GATEWAY=NOT_DEPLOYED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
