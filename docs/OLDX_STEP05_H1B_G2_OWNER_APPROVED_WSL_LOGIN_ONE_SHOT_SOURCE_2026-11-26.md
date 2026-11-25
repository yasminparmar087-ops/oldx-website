# OLDX Step05 H1B G2 — owner approval received for ONE WSL login, registry auth and later ONE retained-image push

**26 Nov 2026 IST. Prepared SOURCE ONLY by assistant. Owner reply: "ha manjuri chhe" explicitly accepted the prior narrowly scoped G2 plan** (Yasmin WSL OAuth login in new isolated config, Docker credentials only for `asia-south1-docker.pkg.dev`, one push of the already-built H1A image into existing `oldx-staging-images`, then immutable digest verification). This approval does NOT authorize H1B new SA/Cloud Run/IAM changes W1–W6, Firebase, H2 or production. Save/read this checkpoint before any new chat. No Cloud/WSL execution by assistant.

Prior owner Cloud Shell G1 actual result `READ_ONLY_WITH_LIMITS`, 11 requested permissions returned, future new SA actAs unknown, WSL auth not configured, no Cloud resource writes: [canonical screenshot record](OLDX_STEP05_H1B_G1_OWNER_SCREENSHOT_PASS_AND_G2_FASTPATH_2026-11-26.md). G1 single-run consumed. Do NOT repeat. No H1A Docker build/Grype/Syft/S2/S3B/C1A repeats.

## G2A: exact prepared new one-shot — OAuth and isolated Docker helper ONLY

- Script `scripts/step05_h1b_g2_native_wsl_owner_login_and_docker_helper_once_20261126.sh`.
- Pinned first commit `4e0a4a99fb163f32fac29b3e3d0da74c161c666a`.
- Verified GitHub blob `5f574b57f91b726f82ae71ec830376dde602b24e`.
- Runs ONLY as root inside previously used `OLDX-Ubuntu-24.04`, not Cloud Shell/Windows PowerShell. Native Linux CLI `/root/oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud` and bundled Python absolute path; no previous Windows SDK.
- Before login, reads `docker image inspect` **once** (not a build or runtime test) to confirm retained H1A tag exactly matches frozen local image ID `sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`. Any mismatch STOP before OAuth.
- Requires unused paths `/root/oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config` and `/root/oldx-tools/oldx-h1b-g2-20261126-docker-config`; leaves all S2 config, existing credentials and default `~/.docker/config.json` untouched. Restricted `umask 077`.
- New distinct consumed-at-attempt marker: `/root/.oldx-h1b-g2-wsl-owner-login-once-20261126`; don't reset/re-run after a failure. Only source-only isolated recovery may be planned from saved output. No OAuth data/password/codes in GitHub or screenshots.
- Interactive **`gcloud auth login yasminparmar087@gmail.com --no-launch-browser`**. Owner opens Google URL in trusted local browser and enters code into local terminal only. Script verifies exact active account; sets `oldx-staging` on NEW isolated gcloud config (local-only configuration write).
- Dedicated Docker config `{"credHelpers":{"asia-south1-docker.pkg.dev":"gcloud"}}`; no credential files, persistent service account keys, other registry host, or cloud resource writes. No `docker push` in this first script.
- Expected final safe status `H1B_G2A_RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY` with `REGISTRY_PUSH=NOT_ATTEMPTED`. STOP or interruption is NOT a success; report only sanitized `H1B_G2A_*` fields, not browser URL/code/access token.

## One paste: run from **Windows CMD into WSL**, never Google Cloud Shell

First enter the correct WSL (from Windows CMD):

```bat
wsl -d OLDX-Ubuntu-24.04 -u root
```

Then paste ONLY inside Ubuntu terminal:

```bash
bash -euo pipefail <<'OLDX_H1B_G2A'
umask 077
d=$(mktemp -d /root/oldx-h1b-g2a-source.XXXXXXXX)
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/g2a.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/4e0a4a99fb163f32fac29b3e3d0da74c161c666a/scripts/step05_h1b_g2_native_wsl_owner_login_and_docker_helper_once_20261126.sh'
test "$(git hash-object "$d/g2a.sh")" = '5f574b57f91b726f82ae71ec830376dde602b24e' || { echo 'STOP: SOURCE_HASH_MISMATCH'; exit 2; }
bash -n "$d/g2a.sh"
bash "$d/g2a.sh" --h1b-g2-owner-wsl-login-once
OLDX_H1B_G2A
```

The Git object hash/ Bash syntax are checked **on the owner's system before executing**. Because this source is not executed by assistant, don't claim real local tests passed. If code cannot download/hash, STOP with no login. Do not bypass SHA, change owner/project/registry, or repeat if consumed.

## G2B next — owner approval already scoped, NOT YET PUSHED

After actual G2A status, prepare exact separate one-shot **reuse-and-push** for `oldx-h1a-c2-mediator-off:local-20261124t195244z` into a fresh unoccupied `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off:<unique-G2-run-tag>`. Must: verify same local ID, authenticated user+project, local Docker credential helper host, do an exact remote tag collision check that does not misread 403 as absence, push one time, read actual remote OCI index/linux-amd64/config and reconcile with frozen BuildKit child `sha256:2e555bd98424d29b32a7bb3409a45e2c257569ff632085e4ff0e3a9ab4413b5f` and config `sha256:c71c7268e08f9ed91a92fd4e82e499a7331c3a071985cebcede7d76efbdf5b71` (media type conversion may need fail-closed review), and preserve immutable resulting remote digest. No rebuild/rescan, repo deletion, old C1A image reuse, Cloud Shell export, IAM, Cloud Run, Firebase or production. Cloud Shell HOME was 100% full on last owner screenshot; do not move image there.

Owner consent includes exactly one NEW G2 push; no approval again is needed if scope remains exactly as recorded, but proceed to push only on G2A success and tested safe B script. H1B future W1–W6 requires independent precise finite authorization and new-SA actAs/cleanup. Original C1A service is `CONFIRMED_REMOVED`; leftover C1A SA/image references unknown, **RETAIN**.

Google official documentation verified 26 Nov 2026:
- https://docs.cloud.google.com/sdk/gcloud/reference/auth/login
- https://docs.cloud.google.com/artifact-registry/docs/docker/authentication
- https://docs.cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling
