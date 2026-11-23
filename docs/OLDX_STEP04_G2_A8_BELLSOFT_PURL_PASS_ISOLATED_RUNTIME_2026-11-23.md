# OLDX Step 04 G2 A8 — BellSoft APK PURL namespace confirmed; one isolated local runtime candidate

## Actual owner screenshot — 23 Nov 2026 ~20:48 IST

Cloud Shell executed the read-only saved-private-Grype report inspector. Output, quoted without credentials or raw private JSON:
```text
A8_PRIVATE_REPORT_SHA256=PASS
A8_IMMUTABLE_IMAGE_DIGEST=PASS
A8_PACKAGE=glibc|VERSION=2.43.0-r14|PURL_NAMESPACE=bellsoft-hardened-containers
A8_PACKAGE=libcrypto3|VERSION=3.5.9-r1|PURL_NAMESPACE=bellsoft-hardened-containers
A8_PACKAGE=libssl3|VERSION=3.5.9-r1|PURL_NAMESPACE=bellsoft-hardened-containers
A8_PACKAGE=sqlite-libs|VERSION=3.54.1-r0|PURL_NAMESPACE=bellsoft-hardened-containers
A8_PACKAGE_PROVENANCE=SCANNER_METADATA_ONLY
A8_NEW_SCAN=NONE
A8_CLOUD_ACTIONS=NONE
```

The reported namespace is **BellSoft Hardened Containers for all four exact severe-package families** in the private immutable image. It corroborates the vendor stream and versions used in the earlier [15-severe-CVE vendor comparison](OLDX_STEP04_G2_A8_15_SEVERE_CVE_VENDOR_DISPOSITION_2026-11-23.md), including the seven *vendor-fixed-version candidate* CVEs. It is **scanner-generated PURL metadata only** and **NOT a package vendor signature/independent origin proof**. Don't mark those seven cryptographically verified fixed without additional proof, and do not erase existing 46 Grype matches (1 CRITICAL / 23 HIGH / 19 MEDIUM / 3 LOW, with 15 distinct severe CVE IDs). No more scan/build/SLSA retries.

## Useful next task — real local execution of exact new image with outbound network DISABLED

**PREPARED NOT RUN by owner**: [scripts/step04-a8-isolated-runtime-one-shot.sh](../scripts/step04-a8-isolated-runtime-one-shot.sh), GitHub first-containing commit `e6350642530b5b5afdf3a592eaba5f9db2513a2e`, Git blob `ea2494900755d37e1decad8bf8773c2746a6c7e4`; SHA256 of exact source `060d7f02cf2e8cf9c0a031180cdd0ce9d670fd3b72ab84020f5e2d315d52ce9d`, syntax-checked by `bash -n` and GitHub blob identity matched. It is distinct from all historical Cloud Run/B1/R1 activity and is a **local Cloud Shell Docker container only**, not a new Cloud Run deployment, Firebase test, staging write, or production action.

Before any write, script checks linux/amd64 host, Docker command/daemon, Docker storage root >=2500MiB free and no existing marker/workdir/container. Makes one durable no-repeat marker `$HOME/.oldx-a8-runtime-isolated-once-2506826f`, private TMP workdir `/tmp/oldx-a8-runtime-isolated-once-2506826f`. Pulls one image from existing private Artifact Registry using configured helper and **exact immutable digest `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`** (`timeout 600`; Docker registry transfer may entail data egress cost). Confirms RepoDigest and that actual image config User is `appuser` *before* execution. One local container: `--network none`, `--read-only`, `--cap-drop ALL`, `--security-opt no-new-privileges`, pids64, memory256MiB, cpus0.5, tmpfs16MiB, no host ports, no volumes, no Cloud credentials/mounts, **EXPLICIT staging activate/ADC false**. Node loopback-only health endpoint must return HTTP 200; protected owner POST must return 503; Node exec uid must be nonzero. No external network exists from this container. Trap stops the known named test container on exit, and `--rm` removes it; local image cache/workdir/marker intentionally preserved for incident reconciliation. Does not start database/Firestore, live IAM, auth, cross-DB, full vulnerability reachability, HTTPS/QUIC or host Cloud Run tests.

**Owner's one short Cloud Shell command, prepared NOT executed:**

```bash
(
  set -e
  p='/tmp/oldx-a8-runtime-source-2506826f.sh'
  if [ -e "$p" ]; then echo 'STOP_A8_RUNTIME_SOURCE_PATH_ALREADY_USED'; exit 1; fi
  curl --fail --location --silent --show-error --retry 0 --connect-timeout 15 --max-time 60 \
    'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/e6350642530b5b5afdf3a592eaba5f9db2513a2e/scripts/step04-a8-isolated-runtime-one-shot.sh' -o "$p"
  echo '060d7f02cf2e8cf9c0a031180cdd0ce9d670fd3b72ab84020f5e2d315d52ce9d  /tmp/oldx-a8-runtime-source-2506826f.sh' | sha256sum -c -
  bash "$p"
)
```

**STOP and do not retry** if preflight, pull, image identity, runtime/nonroot/loopback checks fail. Keep marker, private logs and evidence, reconcile exact symptom before another resource action. Expected successful markers: `A8_RUNTIME_EXACT_DIGEST_PULL=PASS`, `A8_RUNTIME_REGISTRY_DIGEST=PASS`, `A8_RUNTIME_CONFIG_USER=APPUSER`, `A8_RUNTIME_NETWORK=NONE`, `A8_RUNTIME_ROOTFS=READ_ONLY`, `A8_RUNTIME_NONROOT=true`, `A8_RUNTIME_HEALTH_STATUS=200`, `A8_RUNTIME_DISABLED_OWNER_STATUS=503`, `A8_RUNTIME_ISOLATED_LOCAL_TEST=PASS_WITH_LIMITS`. This would close only **G2 local OFF-only start/runtime gate WITH LIMITS**; hosted runtime, effective other-Firestore-DB denial/invoker (G4), project-wide spend hard-stop (G8) and owner residual CVE decision remain OPEN. Do not claim 100% Step 04 or launch eligibility.

Ref: Docker official isolated run flags https://docs.docker.com/reference/cli/docker/container/run/ ; Google Cloud Shell Docker preinstalled https://docs.cloud.google.com/artifact-registry/docs/docker/store-docker-container-images .
