# BAJUTO / OLDX Step05 H2U — actual Node24 linux/amd64 OCI child config PASS (27 Nov 2026)

## Owner actual read-only metadata output (~22:20 IST)

Owner root WSL screenshot captured **new** read-only, digest-specific `docker buildx imagetools inspect --format '{{json .Image}}'` of **exact** `linux/amd64` child:
`gcr.io/distroless/nodejs24-debian13@sha256:774b396818c5dbc4d9aba312b84d548045939ca6efdadc840a928f205116fc74`.

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

**What PASS proves:** Child OCI image configuration declares OS linux, architecture amd64, numeric user 65532 and Node entrypoint `/nodejs/bin/node`. `CMD=UNKNOWN` is an **unspecified/unavailable default CMD from the inspected JSON**; it does not prove a broken image. The future H2U release recipe must supply its own explicit `CMD ["scripts/c2-h2u-cloud-run-private-off-main.mjs"]`, while preserving the base Node ENTRYPOINT. Screenshot did not show a runtime `node --version` from the base, base image layers, SBOM or CVE scan. **Do not claim actual Node24 binary/version execution or vulnerability resolution from OCI config.**

Earlier accepted, distinct read-only evidence:
- Immutable multiarch **OCI INDEX** `sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121`; that index references the above linux/amd64 child (and other architectures). [Child metadata receipt](OLDX_STEP05_H2U_NODE24_OCI_INDEX_AMD64_ACTUAL_READONLY_2026-11-27.md).
- **Cosign 3.1.4 index signature ACTUAL PASS** against exact immutable index, publisher `keyless@distroless.iam.gserviceaccount.com` and issuer `https://accounts.google.com`, including signature claims, offline transparency-log inclusion check and CA certificate verification. [Canonical signature receipt](OLDX_STEP05_H2U_DISTROLESS_NODE24_COSIGN_ACTUAL_PASS_CONFIG_NEXT_2026-11-27.md).

**Correct release pin:** `FROM --platform=linux/amd64 gcr.io/distroless/nodejs24-debian13@sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121` selects the signed immutable OCI index plus its linux/amd64 child. Child digest is a separate manifest object. An index signature is not proof of runtime security, nor a scan of a new derived image.

## Previous actual PASS and no-repeat policy

- H2U original manifest SHA256 `12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc`.
- Exact locally staged 65 source files / 349667 bytes, `SOURCE_SHA256SUMS` SHA256 `42081779fe50e3ea9bf8d47aa8613c09db33050d46027d757d24efc79a2f6ecc`, local source context `/root/oldx-h2u-context-permission-recovery.kANeYR1S/output/h2u-off-source-context/`.
- ESM 174 links and 3 built-ins, offline OFF-only real HTTP `/healthz=200 OFF`, synthetic save `503 DISABLED`, unknown `404`, all prior separate tests/evidence completed.
- Old single-use markers, H2S/H2T/H2N/H2R checks and all previous build/scans **DO NOT REPEAT**. New digest metadata read and Cosign should also not be rerun for the same immutable object.

## Boundaries and next

Prepare a **NEW source-only digest-index-pinned release candidate Containerfile** specifying the verified nonroot image, explicit application CMD and exact H2U 65-file context. Do not mutate the historical invalid sentinel template. **No image build, scan, pull, push, Cloud Run deployment, IAM, Firestore or KMS permission has been approved/executed by these metadata-only checks.** Before any new local image build, obtain the separately scoped Owner approval previously required and record one new immutable output digest, Node24 version, nonroot runtime/health OFF, then decide whether to upload to registry or deploy staging with separate scoped consent.

Cloud Run Gateway attached runtime, IAM Invoker/ingress and mediator identity, independently authorized KMS version reader, persistent one-sign Firestore budget access/no TTL and one bounded synthetic KMS sign remain **not tested**. `STEP05=ACTIVE; H2/PRODUCTION=NO_GO`.
