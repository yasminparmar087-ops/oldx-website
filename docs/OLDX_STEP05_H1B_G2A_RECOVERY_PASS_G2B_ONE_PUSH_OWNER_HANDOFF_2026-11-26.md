# OLDX Step 05 — G2A recovery actual PASS; G2B ONE already-approved frozen H1A Registry push (26 Nov 2026 IST)

Project `oldx-staging`, repo `yasminparmar087-ops/oldx-website`, **branch `security-hardening-review` only**.

## Latest owner WSL terminal result — ACTUAL

Owner's latest pasted terminal text after separate /dev/tty G2A recovery:
```text
You are now logged in as [yasminparmar087@gmail.com].
Your current project is [None].
Updated property [core/project].
H1B_G2R_OWNER=VERIFIED
H1B_G2R_PROJECT=OLDX_STAGING_ISOLATED_CONFIG
H1B_G2R_DOCKER_HELPER=ONLY_ASIA_SOUTH1
H1B_G2R_REGISTRY_PUSH=NOT_ATTEMPTED
H1B_G2R_CLOUD_RESOURCE_WRITES=NONE
H1B_G2R_RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY
```
**Interpretation:** Google CLI login is verified for Yasmin in **isolated** native WSL Cloud SDK config, and `oldx-staging` was set and verified *after* OAuth, even though the gcloud login message temporarily said `Your current project is [None]`. Isolated Docker config is exactly one `asia-south1-docker.pkg.dev` credential helper. No Registry image has yet been pushed, and no IAM/Cloud Run/Firebase/production modifications were requested by G2A recovery. Prior G2A v2 EOF failure and old v2 one-shot marker remain unchanged; G2A recovery separate one-shot is now **consumed and successful**. NEVER rerun G2A recovery, alter markers, re-login unnecessarily or copy Windows SDK tokens.

## Previously approved G2B scope

Owner explicitly approved in earlier chat: **ONE unique new image tag push** of the retained H1A compiled-OFF `linux/amd64` image from owner WSL, into the existing Artifact Registry `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images`, then read back actual immutable remote manifest/index and child/config, comparing with frozen local custody. This action is a real metered Registry storage write; user authorized it. It is NOT new Service Account creation, Cloud Run deployment, IAM Invoker grant, hosted API calls, Firebase data, H2 or production.

DO NOT repeat original H1A one-shot build, SBOM/Grype scan (15 packages, 12 distinct HIGH, 0 CRITICAL), isolated runtime smoke, SDK S1/S2, S3/S3B, G1 read-only permission tests, C1A delete/readback, or G2A OAuth. Local frozen image and artifact IDs:
- Original `oldx-h1a-c2-mediator-off:local-20261124t195244z`.
- Frozen local Docker image/index ID `sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`.
- Frozen saved linux/amd64 BuildKit child `sha256:2e555bd98424d29b32a7bb3409a45e2c257569ff632085e4ff0e3a9ab4413b5f`.
- Frozen image config `sha256:c71c7268e08f9ed91a92fd4e82e499a7331c3a071985cebcede7d76efbdf5b71`.
These local digests **must not be labelled a remote image digest**. C1A old Registry remote digest `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a` is unrelated and must not be reused.

## New G2B source (prepared, NOT executed)

`scripts/step05_h1b_g2b_retained_image_single_push_verify_once_20261126.py`, first pinned commit `02435f6d30617287d6d73e04dbb9e839101360ce`, GitHub **exact blob SHA** `03f0af269b7b7e2ecfa2c2ac27c43636890cd2f8`.

One-shot marker `/root/.oldx-h1b-g2b-retained-single-push-once-20261126`, distinct from all consumed originals; created before local `docker tag` and a **single** real `docker push` attempt. On any failure after marker, **NO RETRY, NO MARKER DELETION, NO SECOND PUSH**. Private evidence directory `/root/oldx-h1b-g2b-evidence-<UTC>`, `umask 077`. Source is reviewed/read back from GitHub, not run on owner WSL yet; owner invocation will syntax-check it with `ast.parse` first. No claims of successful hosted push or tests.

Fastpath safeguards:
1. Must run as root in WSL with unchanged native Linux SDK and isolated G2 configs; recovery marker `RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY`, exact Yasmin account, local project `oldx-staging`; Docker helper config exactly single Mumbai host. No prior credentials/marker reset.
2. Read-only `docker image inspect` exact saved local image ID and `linux/amd64`. Fresh isolated Google OAuth token captured in memory, never printed. Existing Registry's official API GET must confirm repository name/type `DOCKER` in `asia-south1`.
3. Generate unpredictable unique `h1b-g2b-20261126-<random>` new tag for **new image name `oldx-c2-mediator-off`**. Exact Registry manifest HEAD must return **404** (tag absent) after separately confirmed repository GET 200. Any 401/403/5xx/200/mismatch STOP, never treat permission denied as absent. Check tag again immediately before push. No pre-existing image overwrite intended.
4. After marker, local Docker tag existing image (no build) and **one** authorised `docker push`, with bounded 900-second single attempt and private stdout/stderr logs. No CI/build/scan/other registry host/cloud writes. DO NOT repeat if transient failure.
5. Independently GET returned remote manifest/index and linux/amd64 child, compare content digest header and actual bytes, require exact frozen child and config digests. Unsupported or changed media type/config/image digest STOP **after push** (never silently deploy). On match, print new immutable remote digest and `PASS_REMOTE_FROZEN_DIGEST_VERIFIED`. Remote image pushes may be stored before a subsequent verification STOP; preserve evidence and resolve via distinct read-only inspection, **not a second push**.

Google official references inspected 26 Nov: https://docs.cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling ; https://docs.cloud.google.com/artifact-registry/docs/docker/authentication ; https://docs.cloud.google.com/artifact-registry/docs/docker/manage-images ; https://docs.cloud.google.com/artifact-registry/docs/docker/names .

## ONE paste in existing owner Ubuntu WSL terminal (NOT Google Cloud Shell)

```bash
umask 077
d=$(mktemp -d /root/oldx-h1b-g2b-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/g2b.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/02435f6d30617287d6d73e04dbb9e839101360ce/scripts/step05_h1b_g2b_retained_image_single_push_verify_once_20261126.py' &&
test "$(git hash-object "$d/g2b.py")" = '03f0af269b7b7e2ecfa2c2ac27c43636890cd2f8' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/g2b.py" &&
python3 -B "$d/g2b.py" --h1b-g2b-retained-image-push-once
```

Expected successful status:
```text
H1B_G2B_STAGE=ONE_AUTHORIZED_PUSH_ATTEMPT
H1B_G2B_REMOTE_DIGEST=sha256:...
H1B_G2B_REMOTE_AMD64_CHILD=sha256:...
H1B_G2B_REMOTE_CONFIG=sha256:...
H1B_G2B_TAG=h1b-g2b-20261126-...
H1B_G2B_PUSH_ATTEMPTED=TRUE
H1B_G2B_RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED
H1B_G2B_REASON=ONE_PUSH_VERIFIED
H1B_G2B_CLOUD_RUN_OR_IAM_WRITES=NONE
H1B_G2B_DO_NOT_REPEAT=TRUE
```

If `STOP_PREFLIGHT`, no Registry push attempted. If `STOP_AFTER_MARKER` and `PUSH_ATTEMPTED=TRUE`, the push might have succeeded even if digest readback failed; only bounded read-only recovery later. Never rerun or delete marker. Share **only sanitized `H1B_G2B_*` status** and no tokens, auth codes, internal saved logs, or private credential files.

## Next after actual output

Only after G2B actual remote manifest verified: separate bounded *future* H1B W1–W6 operational consent/checks (new no-key SA, one private compiled-OFF Cloud Run by immutable remote digest, optional new-service-only Invoker, <=4 new-only HTTP probes, same-session guarded NEW-only cleanup). **W1–W6 remains NOT authorised here**, as do H2, production, existing Firebase rules and C1A residual SA/image deletion. No other Cloud writes authorized.
