# BAJUTO / OLDX Step05 — H2AK four pinned NEW image security scans and isolated OFF runtime checks

Date: 28 Nov 2026. Branch `security-hardening-review`.

## Actual H2AJ predecessor — never repeat

Owner's H2AJ screenshot at ~21:13 IST: four actual private Linux/AMD64 image build/pushes PASS. H2AJ marker `/root/.oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128` consumed; no more build/push or marker reset. Canonical receipt: `docs/OLDX_STEP05_H2AJ_OWNER_ACTUAL_FOUR_IMAGES_REGISTRY_PASS_2026-11-28.md`. This operation did not deploy or enable a Cloud Run service; hosted Seller→Buyer still UNVERIFIED.

**Verified Linux/AMD64 child manifest SHA256, not root OCI index:**

| Role | Exact immutable image |
|---|---|
| Mediator | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-h2ah@sha256:01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe` |
| Gateway | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-gateway-h2ah@sha256:921fbf4ff71b918c479e4a786868368640a494c16da08e54192f25e14dc1ec4d` |
| Backend | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-backend-h2ah@sha256:01ae540aa88ad0e3a6888994dd41b6b02b9d934a7a1d2e455f44b194f033b941` |
| Reader | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-kms-reader@sha256:822e2592b1010bfa94a1fe5bc75003712485abae0369f5252ece3863723eb077` |

Immutable non-executable role/image/SA/UID freeze: `deployment/four-role/h2aj-four-immutable-images-pinned-proposal.json`; Git blob `c1cfcfa2f224e9a47dd6e896730c73e927b9b483`. Preserves four existing distinct runtime SA UID pins and explicit unknown Cloud Run origins, VPC/subnet/Invoker and trusted secret custody.

## New actual source-only work — prepared, NOT EXECUTED in Owner WSL

Added `scripts/step05_h2ak_four_pinned_new_images_scan_offhealth_once_20261128.py`; exact verified Git blob `d970ec1463c252bebbec3fe019c092b6a1313f2c`, created in commit `051eb3fcf8cd8d70de0ce5f151fb2813f5f6eb61` (subsequent fix in commit `832f6ca69c49eedf559175355fc5cf756943040b`). Readback source guards inspected statically, **NOT real local tests or actual image scans**.

When the Owner executes in native WSL root, this script:

1. Requires exact previously successful H2AJ consumed marker, all FOUR matching child digests, correct isolated Owner native gcloud project `oldx-staging`, Docker Linux, Linux Grype binary and root disk capacity. Does not repeat old IAM/Cloud probes or any old tests.
2. Uses a temporary private `DOCKER_CONFIG` with short-lived Owner OAuth to **pull exactly the four pinned images**, never build/push/delete or mutate Artifact Registry.
3. Exactly one local Grype JSON vulnerability scan per image. Keeps private complete JSON and prints severity count of Critical/High per role. A completed scan is evidence, **not a claim that all vulnerabilities are fixed, nor security GO**.
4. Runs each image as nonroot `65532:65532`, read-only root filesystem, no capabilities, no new privileges, **`--network none` and no port publication**, explicit `OLDX_H2AH_ENABLED=false`. Uses `docker exec /nodejs/bin/node` within the same isolated network namespace to verify `GET /healthz` returns `{ok:true,role,state:'OFF',productReady:false}` with HTTP200 and a synthetic POST returns **503** without touching Firebase/KMS/Cloud. Stops/removes the temporary local container.
5. Saves private `/root/oldx-h2ak-images-...` sanitized receipt with per-role image ID, Grype JSON and counts plus OFF-health result. Exclusive H2AK marker `/root/.oldx-step05-h2ak-four-pinned-image-acceptance-once-20261128` records consumed one-shot checks. On first failure, STOP, keep receipts; **do not blindly rerun**. Never clear H2AJ/H2AI/H2AG markers.

**If Grype is absent**: preflight STOP *before* H2AK marker. Resolve a verified native Linux scanner locally rather than using Windows executable or making a second image build. If Grype database/scan/health fails after H2AK marker, inspect exact private evidence and reconcile only remaining read-only checks; don't delete marker. No cloud resources or production services are changed by H2AK.

## ONE native WSL root command — execute only if Docker + Grype exist

```bash
umask 077
test -f /root/.oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128 &&
test ! -e /root/.oldx-step05-h2ak-four-pinned-image-acceptance-once-20261128 &&
d=$(mktemp -d /root/oldx-h2ak-approved.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ak.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/832f6ca69c49eedf559175355fc5cf756943040b/scripts/step05_h2ak_four_pinned_new_images_scan_offhealth_once_20261128.py' &&
test "$(git hash-object "$d/h2ak.py")" = 'd970ec1463c252bebbec3fe019c092b6a1313f2c' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ak.py" &&
python3 -B "$d/h2ak.py" --h2ak-four-h2aj-images-scan-offhealth-local-only-once
```

This has not yet been run; do not claim scan/nonroot OFF-health PASS. Success would be `H2AK_RESULT=PASS_FOUR_NEW_IMAGE_SECURITY_AND_OFF_RUNTIME_RECEIPTS` with four `H2AK_PASS=` lines, but security severity counts require explicit risk assessment rather than being automatically ignored. Grype source documentation: https://oss.anchore.com/docs/reference/grype/cli/ ; Docker exec in-container: https://docs.docker.com/reference/cli/docker/container/exec .

## Next *real* launch milestone after these new-image checks

No more old scans/builds. Prepare ONE exact immutable four-role OFF-only private Cloud Run staging deployment approval packet using the pinned child digests; investigate only new VPC/Direct VPC egress, private Invoker, actual runtime SA/UID evidence and controller-config-secret custody; avoid making any false claims that `internal` ingress is reachable without proper routing. Production stays OFF. Once approved and deployed private staging OFF-only, verify hosted `/healthz` and security identities, THEN separately guarded one synthetic six-stage Seller→Buyer flow with real Auth/Firestore/Storage/KMS. Previously accepted CVE residual risk should be explicitly documented, not a reason to indefinitely block practical feature work.

**Status at doc authoring:** `H2AJ=FOUR_REGISTRY_PASS_CONSUMED`; `H2AK=SOURCE_READY_NOT_RUN`; `CLOUD_RUN_PRIVATE_HOSTED=NOT_VERIFIED`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
