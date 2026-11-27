# BAJUTO / OLDX Step05 H2U — Owner actual Distroless Node24 index cosign verification

## 27 Nov 2026 ~22:14 IST — ACTUAL COSIGN INDEX SIGNATURE VERIFICATION PASS

Owner supplied root WSL terminal screenshot after using a pre-existing absolute-path Cosign executable (not on normal PATH). The output explicitly shows:

~~~text
cosign: A tool for Container Signing, Verification and Storage in an OCI registry
GitVersion: v3.1.4
Platform: linux/amd64

Verification for gcr.io/distroless/nodejs24-debian13@sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121 --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - Existence of the claims in the transparency log was verified offline
  - The code-signing certificate was verified using trusted certificate authority certificates
~~~

Verified certificate **issuer**: `https://accounts.google.com`. Verified **subject identity**: `keyless@distroless.iam.gserviceaccount.com`. The output's JSON payload contains a signed `docker-manifest-digest` exactly matching the immutable index digest above. The long signature payload and certificate JWT have **not** been copied into GitHub docs to avoid noisy duplication; this receipt transcribes only the checks and identities visible in the screenshot. The screenshot is owner-provided evidence; this assistant did **not** rerun Cosign, query registry signature again, or independently parse its full signature payload.

**Exact verified OCI object:** Multi-platform **index** `sha256:675c532423b908f9e56f9d60a4e62309b63cd2a3175acb90a46b96f7ee68e121`. Earlier separate read-only Docker Buildx index listing reported **linux/amd64 child manifest** `sha256:774b396818c5dbc4d9aba312b84d548045939ca6efdadc840a928f205116fc74`; do **not** confuse index digest with child digest. Those two facts jointly establish (at their checked times) publisher-signed index and a selected amd64 child referenced by that index, not a separately child-signed image or in-depth image inspection. [Prior OCI index/amd64 child receipt](OLDX_STEP05_H2U_NODE24_OCI_INDEX_AMD64_ACTUAL_READONLY_2026-11-27.md).

**NO REPEAT / no install:** Pre-existing verified Cosign v3.1.4 succeeded via absolute path; do not reinstall, change global PATH, rerun prior BellSoft signature checks, rerun this exact index Cosign verification, rerun tag lookup or the many prior completed H2U/H2S/H2T/H2R/H2N tests and Cloud probes. No Docker layer pull/build/push/scan, Cloud Run deployment, IAM edit, Firebase/Firestore or KMS signing has occurred in this signature-only command.

## Next smallest distinct release gate — OCI amd64 image configuration only

A signature confirms the signed OCI index identity and its claims, **not** the runtime entrypoint, effective nonroot user, binary version, KMS/Firestore access, or a vulnerability-free image. Prior source-context 65/65 and real OFF listener smoke 200/503/404 are completed; avoid redoing.

Use Docker's officially documented `docker buildx imagetools inspect --format '{{json .Image}}'` against the **immutable linux/amd64 child digest** (not mutable tag) to read remote OCI image configuration. This is a distinct registry **metadata-only** read, not a layer pull/build or source test. Validate `os=linux`, `architecture=amd64`, exact entrypoint, user UID, and CMD. Source: https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/

~~~bash
set -o pipefail
docker buildx imagetools inspect \
  --format '{{json .Image}}' \
  'gcr.io/distroless/nodejs24-debian13@sha256:774b396818c5dbc4d9aba312b84d548045939ca6efdadc840a928f205116fc74' |
python3 -c '
import json, sys
d = json.load(sys.stdin)
c = d.get("config") or {}
os_name = d.get("os", "UNKNOWN")
arch = d.get("architecture", "UNKNOWN")
user = c.get("User", c.get("user", "UNKNOWN"))
entry = c.get("Entrypoint", c.get("entrypoint", "UNKNOWN"))
cmd = c.get("Cmd", c.get("cmd", "UNKNOWN"))
print("OLDX_H2U_BASE_OS="+str(os_name))
print("OLDX_H2U_BASE_ARCH="+str(arch))
print("OLDX_H2U_BASE_USER="+str(user))
print("OLDX_H2U_BASE_ENTRYPOINT="+str(entry))
print("OLDX_H2U_BASE_CMD="+str(cmd))
if os_name != "linux" or arch != "amd64" or not isinstance(user, str) or not user or not isinstance(entry,list) or not entry:
    print("OLDX_H2U_BASE_CONFIG=STOP_REVIEW_REQUIRED")
    sys.exit(2)
print("OLDX_H2U_BASE_CONFIG=READ_ONLY_PASS_WITH_LIMITS")
print("OLDX_H2U_BASE_IMAGE_BUILDS_PULLS_SCANS=NONE")
print("OLDX_H2U_H2_PRODUCTION=NO_GO")
'
~~~

If the result is incomplete, an unexpected user/entrypoint, or an error, STOP and review; **do not** assume success or execute the source image. A digest-pinned immutable configuration read is **not** a Node24 runtime launch/version test or base image signature re-verification. The source-only `release/H2U_Containerfile_OFF_ONLY_UNVERIFIED.template` retains its intentionally-invalid digest sentinel until configuration and release boundaries are documented and reviewed.

### Important H2 remaining boundaries

- Source context actual PASS: 65 SHA-pinned files, 349667 source bytes, staged locally at `/root/oldx-h2u-context-permission-recovery.kANeYR1S`, original source marker preserved. No need to restage.
- Gateway release image **not built**, not scanned, not pushed. No owner approval for a new image build/push/Cloud Run creation or IAM change has been requested on the basis of this single metadata check.
- Gateway SA UID `107238619872767759560` verified previously but not attached to any actual H2 Cloud Run revision. Private IAM Invoker/audience, independent authorized KMS KeyVersion public-status reader, permitted immutable Firestore one-sign transaction/no TTL and one new owner-bounded synthetic KMS sign remain pending.
- Security watch/previous accepted CVEs do not transform this into production readiness.
- **Status:** `H2U_COSIGN_INDEX_SIGNATURE=ACTUAL_PASS`; `H2U_AMD64_IMAGE_CONFIG=NOT_CHECKED`; `H2U_IMAGE=NOT_BUILT`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
