# BAJUTO / OLDX Step05 H2U — ONE Owner-approved local image build + new OFF image runtime (27 Nov 2026)

## Explicit scoped Owner consent

Owner replied **"ha manjuri chhe"** to the immediately preceding proposal: **one local** `linux/amd64` default-OFF Gateway Docker image build, necessary public immutable base-layer fetch, and **new image-specific** Node runtime UID/version and OFF HTTP 200/503/404 check. Approval **does not** include registry push, Cloud Run service deploy, IAM changes, Firebase/Firestore writes, live KMS operations, main branch edits, production enablement, repeated old tests or previous CVE rescans.

## Immutable and previously accepted inputs — DO NOT REPEAT

- Source-context staging actually completed 65 verified files / 349667 bytes; Owner-local path `/root/oldx-h2u-context-permission-recovery.kANeYR1S/output/h2u-off-source-context`. Its `SOURCE_SHA256SUMS` file SHA256 `42081779fe50e3ea9bf8d47aa8613c09db33050d46027d757d24efc79a2f6ecc`; original scan manifest SHA256 `12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc`. Previous permission recovery marker and all earlier consumed one-shots remain unchanged.
- Signed immutable Distroless Node24 Debian13 **multi-arch index** `sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121` had Owner Cosign v3.1.4 actual signature PASS, issuer `https://accounts.google.com`, identity `keyless@distroless.iam.gserviceaccount.com`. It references `linux/amd64` child `sha256:774b396818c5dbc4d9aba312b84d548045939ca6efdadc840a928f205116fc74`; child config actual read-only PASS: `linux`, `amd64`, `User=65532`, `Entrypoint=['/nodejs/bin/node']`. Original unspecified base CMD overridden explicitly in the new candidate. **No repeat** of registry, cosign or metadata checks.
- Exact new release source `release/H2U_Containerfile_OFF_ONLY_SIGNED_INDEX_CANDIDATE_20261127`, Git blob `4b85cbe44dc7e141f6934d99a91d8ec31cf2868c`, immutable source commit `a3e262a13425e29bf6bd683a3bf72f136459871d`. Old invalid digest sentinel template intentionally unchanged.
- Previous H2U offline 65-file scan, 174 ESM link, 3/3 HTTP mocks and real OFF-only local listener responses 200/503/404 already PASS. This build checks behavior of a **new image**; it is not an old test rerun.

## One new owner-scoped WSL runner — source READY, NOT EXECUTED

New source `scripts/step05_h2u_once_local_signed_index_image_build_off_smoke_20261127.sh`:
- Immutable creation commit `621af10374ce9912b3a0f2f72eaff33223a7a37f` and verified Git blob `8f7edbfca4420656e67f59e1a97a4a1962c78c13`.
- **Preflight before consuming marker:** check original manifest and staged SHA256SUMS, count exactly 65; verify each listed source path/file SHA256, bytes=349667, no unlisted/symlink files, and minimal `package.json`; check tag does not already exist; download only this new candidate Containerfile at its immutable commit and verify exact blob. No prior tests run.
- **One-shot marker**, created immediately BEFORE the image build: `/root/.oldx-step05-h2u-local-image-build-once-20261127`. If the build or smoke stops for any reason, do **NOT** rerun or delete marker; inspect the new local evidence folder and diagnose exact failure first.
- **Exactly one `docker buildx build` invocation**: immutable signed OCI index as base, `--platform linux/amd64 --network none --pull --load` and explicit context path, new tag `oldx-h2u-private-off:local-20261127-one`, capture IID and build log in separate root-private evidence folder. Public base layers may be fetched as authorized; no push. Old H1A/H1B images remain unmodified.
- New image configuration check: OS linux/amd64, `User=65532:65532`, Node entrypoint, exact OFF app CMD and `OLDX_H2U_MODE=OFF`, PORT8080. Then run **new image-specific** Node major 24 and UID65532 check without network. Run only that newly built image in Docker `--network none` with no port publish and no credentials; exercise localhost HTTP health 200 OFF, fake-enabled Save 503, unknown 404; stop/remove only the ephemeral test container. Image persists locally with its exact new ID and evidence.
- Explicitly no registry push, Cloud Run deployment, IAM, Firestore, KMS, production activation or previous tests/scans.
- Running this command may download new Distroless **base layers** and consume local disk/CPU for this one approved build. The script itself is not run by GitHub and is not background work. A PASS is **not** claimed before the owner executes it.

### One WSL root terminal command, new only

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2u-local-build-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/build.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/621af10374ce9912b3a0f2f72eaff33223a7a37f/scripts/step05_h2u_once_local_signed_index_image_build_off_smoke_20261127.sh' &&
test "$(git hash-object "$d/build.sh")" = '8f7edbfca4420656e67f59e1a97a4a1962c78c13' &&
bash -n "$d/build.sh" &&
bash "$d/build.sh"
~~~

Expected success includes:
~~~text
OLDX_H2U_LOCAL_PREFLIGHT=PASS_65_IMMUTABLE_SOURCES
OLDX_H2U_LOCAL_IMAGE_CONFIG=PASS_NONROOT_AMD64_OFF
OLDX_H2U_LOCAL_IMAGE_RUNTIME_UID=65532
OLDX_H2U_LOCAL_IMAGE_HTTP=PASS_OFF_200_503_404
OLDX_H2U_LOCAL_IMAGE_IID=sha256:...
OLDX_H2U_LOCAL_IMAGE_RESULT=PASS_NEW_BUILD_AND_OFF_RUNTIME_WITH_LIMITS
OLDX_H2U_LOCAL_IMAGE_CLOUD_WRITES=NONE
OLDX_H2U_LOCAL_IMAGE_REGISTRY_PUSH=NONE
OLDX_H2U_LOCAL_IMAGE_CLOUD_RUN_DEPLOY=NONE
OLDX_H2U_H2_PRODUCTION=NO_GO
~~~

**If STOP:** do not rerun the one-shot or clear marker. Keep local new `/root/oldx-h2u-first-local-image.XXXXXXXX` receipt and the exact printed failure; build might have completed even if image-specific smoke failed. A single scoped new diagnosis/fix then required, not a second build without fresh consent.

## Future non-covered steps

Even one successful local image build+smoke does not prove signed derived-image provenance, new image CVE status, effective Cloud Run IAM/Invoker/private ingress, verified Gateway runtime SA UID `107238619872767759560`, independent KMS version-status reader permission, persistent one-sign Firestore ledger or a live KMS signing grant/test. Any image push and private staging Cloud Run new service require **distinct Owner permission**. H2 remains OFF and production NO_GO.

**Current checkpoint:** `H2U_LOCAL_IMAGE_BUILD=APPROVED_ONE_ATTEMPT_SOURCE_READY_UNRUN`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
