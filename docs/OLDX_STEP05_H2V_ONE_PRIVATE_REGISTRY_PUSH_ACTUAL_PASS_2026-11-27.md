# BAJUTO / OLDX Step05 H2V — actual owner single private Artifact Registry push PASS (27 Nov 2026)

## Actual Owner screenshot at ~23:02 IST, 27 Nov 2026

The Owner executed the scoped, hash-verified one-shot `scripts/step05_h2v_one_existing_h2u_image_private_registry_push_once_20261127.py` at immutable commit `7e593e57157afa4b0ca9fd509548bf0c56ed0078`, Git blob `19e153d6993d1955d134d7f33a14c6180d497e99`, using native root Ubuntu WSL. **The exact intended new H2U private Artifact Registry push actually succeeded** and remote index, amd64 child and image config digests matched the previously built local H2U artifact:

~~~text
H2V_STAGE=ONE_AUTHORIZED_H2U_PUSH_ATTEMPT
H2V_REMOTE_DIGEST=sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2
H2V_REMOTE_AMD64_CHILD=sha256:c165e671e2b231b5b6210f867dacc085d4a53b69fae2998a712019d9b6575243
H2V_REMOTE_CONFIG=sha256:56b7a9601702e80286c80089e33fe13049b6fa7d3fbbcb98e4f775c9d31ace25
H2V_TAG=h2v-off-20261127-793639b6b8d15e55ea4a
H2V_PUSH_ATTEMPTED=TRUE
H2V_RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED
H2V_REASON=ONE_PUSH_VERIFIED
H2V_CLOUD_RUN_OR_IAM_WRITES=NONE
H2V_REGISTRY_WRITE=ONE_PUSH_ATTEMPTED
H2V_LOCAL_IMAGE_BUILD=NONE
H2V_H2_PRODUCTION=NO_GO
H2V_DO_NOT_REPEAT=TRUE
~~~

**Exact immutable remote image locator (H2 Gateway OFF, not mediator):**

`asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`

The unique mutable tag is `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-h2-gateway-off:h2v-off-20261127-793639b6b8d15e55ea4a`. **Future deploys must use the immutable digest, not the tag.**

### What was actually done and what remains unknown

- Exactly **one real private Artifact Registry upload/storage write** in existing project `oldx-staging`, region `asia-south1`, repository `oldx-staging-images`. Upload may incur storage cost. Not a zero-cloud-write operation.
- The new `oldx-c2-h2-gateway-off` image is distinct from previous H1B `oldx-c2-mediator-off` image and C1A `oldx-step05-gateway-off`; neither was retagged/pushed, removed or modified.
- Pre-existing local H2U image ID `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2` matches freshly reported **remote OCI index digest**. Child and config match the immutable previous local build output. This is an actual remote digest check performed by Owner's script and reported by screenshot, not a second independent registry query by ChatGPT.
- **No Docker image rebuild**, no fresh scan, no Cloud Run service creation, no IAM, no Firestore, no KMS signing, no Product activation or production deployment was performed by this upload.
- Existing one-push H2V marker `/root/.oldx-step05-h2v-one-immutable-local-image-push-once-20261127` is now **CONSUMED**. Do not retry source, run any old H1B/ H2U/ H2V one-shot, remove marker, perform another upload, rebuild/rescan older images or repeat prior auth/Cloud audits. Preserve Owner-local private evidence from H2V source if later needed.
- Signed parent Node24 OCI image and isolated OFF-only local runtime Node `24.22.3` UID65532 with HTTP 200/503/404 actual PASS previously; the newly derived/pushed image has **not** been independently signed as a release and is not yet reviewed for current CVEs.

## Next decision — new private Cloud Run H2 Gateway hosting; not yet approved

A new, separately authorized stage can deploy **one new private default-OFF H2 Gateway Cloud Run service** from **the immutable remote locator above**. Never repurpose existing H1B or `oldx-owner-read` Cloud Run services. First complete fresh exact-target, read-only service and service-account existence/UID/roles preflight and verify operator authorization. Project `oldx-staging`, region `asia-south1`, desired Gateway runtime service account already recorded elsewhere with immutable UID `107238619872767759560`. A suggested **new unique service name** should be checked for collision before create. Require Cloud Run IAM Invoker/auth, restrictive ingress and audience, default-OFF only, min0 max1, constrained CPU/memory/timeout, traceable rollback/cleanup, and no public access. Service creation, IAM binding or cloud upload repeat is **not authorized** by prior H2V approval. Only after new scoped Owner permission should any such Cloud writes occur.

Independent KMS KeyVersion status reader, real Firestore durable one-sign transaction/no TTL and a separate Owner-approved synthetic signing are still unresolved; no H2/Product production activation.

**Checkpoint** `H2V_PRIVATE_REGISTRY_PUSH=ACTUAL_PASS_ONE_CONSUMED`, `H2U_REMOTE_INDEX_DIGEST=sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`, `H2_GATEWAY_CLOUD_RUN=NOT_DEPLOYED`, `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`.
