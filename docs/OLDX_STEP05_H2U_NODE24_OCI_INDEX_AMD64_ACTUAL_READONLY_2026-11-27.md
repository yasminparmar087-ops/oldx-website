# BAJUTO / OLDX Step05 H2U — actual public Distroless Node24 OCI index/amd64 child receipt

## 27 November 2026 ~22:06 IST — Owner actual read-only registry metadata result

Owner root WSL screenshot after exactly:

~~~bash
docker buildx version &&
docker buildx imagetools inspect gcr.io/distroless/nodejs24-debian13:nonroot
~~~

Results transcribed from the screenshot, **not an independently retrieved/rehashed public registry record**:

| Evidence | Actual observed value |
| --- | --- |
| Docker buildx | `v0.39.0` |
| Public registry image | `gcr.io/distroless/nodejs24-debian13:nonroot` |
| OCI index media type | `application/vnd.oci.image.index.v1+json` |
| OCI **multi-platform index digest** | `sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121` |
| OCI **linux/amd64 child manifest digest** | `sha256:774b396818c5dbc4d9aba312b84d548045939ca6efdadc840a928f205116fc74` |
| amd64 child media type | `application/vnd.oci.image.manifest.v1+json` |
| Also present | `linux/arm64/v8`, `linux/s390x`, `linux/ppc64le` |
| Image build/pull/push or Cloud writes | **None reported by metadata-only command** |

**Important:** The index digest and the child digest are different immutable objects. For the eventual platform-specific Gateway, the recorded `linux/amd64` child can be addressed by its exact digest, after full release trust gates. The **index** digest is the appropriate default target for Sigstore/cosign verification of the publisher-signed multi-architecture image; membership of the child digest in that index was read in the same one-shot response. This does not mean the child or the index has been signature/provenance verified yet.

## Official source and next narrow trust gate

Distroless official documentation:
- <https://github.com/GoogleContainerTools/distroless> describes Node24 Debian13 nonroot, architectures and **keyless cosign** signature identity `keyless@distroless.iam.gserviceaccount.com` with issuer `https://accounts.google.com`.
- <https://github.com/GoogleContainerTools/distroless/blob/main/nodejs/README.md> documents that the Node.js image's default ENTRYPOINT is Node and application script path belongs in CMD.

**One new read-only signature verification** (not performed): If trusted `cosign` is already installed in the Owner's root WSL, check its version then verify the exact **immutable index digest** with the official identity/issuer. No need to re-run previous buildx metadata query.

~~~bash
if command -v cosign >/dev/null 2>&1; then
  cosign version &&
  cosign verify \
    --certificate-oidc-issuer 'https://accounts.google.com' \
    --certificate-identity 'keyless@distroless.iam.gserviceaccount.com' \
    'gcr.io/distroless/nodejs24-debian13@sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121'
else
  echo 'OLDX_H2U_COSIGN=NOT_INSTALLED_STOP_BEFORE_VERIFY'
fi
~~~

This only reads/validates signatures/remote certificate/transparency metadata and does not pull layers, build, deploy, edit IAM or touch OLDX Google Cloud projects. **DO NOT claim a PASS before actual Owner output.** If `cosign` is absent or the signature cannot be verified, STOP at that precise blocker; no guessed signature or hasty trust bypass, no repeated old checks. If signature PASS, still verify pinned Node runtime version, default nonroot UID, signed artifact/provenance where available, and approved production policies before a NEW Gateway image build.

## Release recipe boundary

Previously committed `release/H2U_Containerfile_OFF_ONLY_UNVERIFIED.template` deliberately retains an **INVALID DIGEST SENTINEL**. Do not edit that template into a buildable release artifact merely because registry metadata succeeded. The Owner already has an exactly staged 65-file OFF source context and screenshot SHA256SUMS manifest `42081779fe50e3ea9bf8d47aa8613c09db33050d46027d757d24efc79a2f6ecc`, from `/root/oldx-h2u-context-permission-recovery.kANeYR1S`, which must be preserved. Old one-shots (H2U context recovery, ESM link, HTTP listener, tests, H2S/H2T/H2R/H2N) are **CONSUMED, DO NOT REPEAT**. The official public registry metadata lookup need not be repeated.

No base signature verification, new release OCI build, registry push, Cloud Run service creation, Invoker/ingress IAM, Firestore transaction or real KMS sign has occurred. `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.

**Current:** `H2U_NODE24_INDEX_DIGEST=METADATA_READ_ONLY_CONFIRMED_FROM_OWNER_SCREENSHOT`, `H2U_NODE24_AMD64_CHILD=METADATA_READ_ONLY_CONFIRMED_FROM_OWNER_SCREENSHOT`, `H2U_SIGNATURE=NOT_CHECKED`, `H2U_BASE_RUNTIME_UID=NOT_VERIFIED`, `H2U_SOURCE_CONTEXT=STAGED_65`, `H2U_NEW_IMAGE=NOT_BUILT`, `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`.
