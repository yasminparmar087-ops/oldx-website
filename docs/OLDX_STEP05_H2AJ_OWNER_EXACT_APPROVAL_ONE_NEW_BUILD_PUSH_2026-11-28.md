# BAJUTO Step05 H2AJ — explicit Owner approval; prepared one-time WSL execution, NOT YET RUN

Date 28 November 2026 (IST). GitHub branch `security-hardening-review`.

Owner explicitly answered **"ha manjuri chhe"** to the exact four-image H2AJ proposal in [the original scope packet](OLDX_STEP05_H2AJ_FOUR_ROLE_CONTEXT_FIX_NEW_OWNER_ONE_APPROVAL_2026-11-28.md).

## Authorized maximum, no other write
- One new attempt each for four new OFF linux/amd64 images in private `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images`: `oldx-c2-mediator-h2ah`, `oldx-c2-gateway-h2ah`, `oldx-c2-backend-h2ah`, `oldx-c2-kms-reader`.
- Fixed previously tested source ancestor `5d5a621d7a9d9015b5068077b914fef3d6fb9925`, Dockerfiles, COPY/source provenance pins; only docs and review-verified guard scripts added.
- First read exact failed consumed H2AI marker, log and receipt at `/root/oldx-h2ai-four-builds-20261128T151519Z-09e4fd`; old marker must remain unchanged and no H2AI script may be rerun. Guarded read-only checks of all four bundles and absolute Dockerfile paths **before** a fresh H2AJ marker.
- One Buildx build `--platform linux/amd64 --provenance=true --sbom=true --push` per role; new unique registry tags, permanent index and child digest receipts; **stop on first unknown/failure, no automatic retries or cleanup**. This consumes H2AJ marker before first build. Do not infer previously failed H2AI Mediator push/absence without independent readback.
- No Cloud Run deploy/ingress/traffic, KMS signing/GET, Firebase/Firestore/Storage writes, new IAM/key/SA/VPC, no production or reuse of old OFF image, no old suite/CI/scans/builds. Private registry storage may be billed.

## Immutable exact sources, verified GitHub readback

1. Runner `scripts/step05_h2aj_four_off_images_reconciled_once_20261128.py`, blob `9f3264aa47243a09187604c13eb8232aa6bc8c59`, available at immutable commit `6e4a1fa8908b47f720a3add961cf8ac2bb3aa1a6`.
2. Context/COPY/ignore/provenance validator `scripts/step05-h2aj-build-context-preflight.mjs`, blob `f5137df3af84de55c3fe1c0468b22e2446001f7d`. It is sourced by the runner's isolated immutable-source clone and cross-checked against source bundle hash.
3. All four role Dockerfile/COPY and Dockerfile-specific ignore inventories were source-compared; V8 validator body syntax and 4 in-memory filesystem fixtures succeeded, **NOT an actual owner WSL build**. The future runner performs real read-only filesystem checks before any build. Previously completed 23 source integration cases and six H2AI local tests are NOT rerun.

## Exact ONE user-side WSL root command (only after this Owner consent)

```bash
umask 077
export PATH="/root/oldx-tools/node-v24.22.3-linux-x64/bin:$PATH"
test "$(node --version)" = "v24.22.3" &&
test -f /root/.oldx-step05-h2ai-four-off-build-push-once-20261128 &&
test ! -e /root/.oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128 &&
d=$(mktemp -d /root/oldx-h2aj-approved.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2aj.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/6e4a1fa8908b47f720a3add961cf8ac2bb3aa1a6/scripts/step05_h2aj_four_off_images_reconciled_once_20261128.py' &&
test "$(git hash-object "$d/h2aj.py")" = '9f3264aa47243a09187604c13eb8232aa6bc8c59' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2aj.py" &&
python3 -B "$d/h2aj.py" --h2aj-owner-new-approval-four-amd64-off-builds-corrected-context-once
```

**Never rerun after `H2AJ_MARKER=CONSUMED_NO_REPEAT` appears.** Even if build aborts/partial push, preserve private evidence, collect screenshot and run only separately scoped read-only reconciliation. Current `H2AJ_NEW_EXECUTION=NOT_YET_OBSERVED`, `STEP05=ACTIVE`, `PRODUCTION=OFF_NO_GO`.
