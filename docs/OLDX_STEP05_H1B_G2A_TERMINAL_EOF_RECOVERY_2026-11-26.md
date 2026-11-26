# OLDX Step 05 — G2A verification-code EOF recovery, owner WSL, 26 Nov 2026

## Actual owner endpoint (after first corrected v2 source)
Owner supplied terminal text:
```
Once finished, enter the verification code provided in your browser:
ERROR: gcloud crashed (EOFError): EOF when reading a line
H1B_G2A_RESULT=STOP_AFTER_MARKER
H1B_G2A_REASON=INSPECT_LOCAL_EVIDENCE_DO_NOT_REPEAT_OR_DELETE_MARKER
```
This is a **G2A interactive stdin failure**, not evidence of a Firebase, IAM, Registry, permission or Google account denial. The v2 shell script was launched under outer `bash -euo pipefail <<'OLDX_H1B_G2A_V2'`, which delivered source to stdin. By the time the nested interactive `gcloud auth login --no-launch-browser` read from inherited stdin, it was exhausted, so Python raised `EOFError`. This specific causation is strongly supported by command design and exact traceback, not a claim of successful authorization. Google official manual code-paste authentication: https://docs.cloud.google.com/sdk/gcloud/reference/auth/login

The v2 one-shot marker `/root/.oldx-h1b-g2-wsl-owner-login-once-20261126` is **CONSUMED** (G2A printed STOP_AFTER_MARKER). The script had already made NEW root-only isolated config directories; it had not finished owner login, local project config, Docker helper config or printed success. No `docker push`, deploy, IAM or Cloud resource writes exist in this G2A source. Do not delete marker, rerun v1/v2, repeat G1/S1/S2/S3/H1A/C1A checks, or send Google OAuth code/URL/token into ChatGPT/GitHub.

## New isolated recovery — source-only READY, not owner executed
- Script: `scripts/step05_h1b_g2a_recover_terminal_stdin_once_20261126.sh`
- Pinned first commit `90b03e2bd1f3e0b850c053b6382ad46cb5ee8a87`
- GitHub blob SHA `1e325acc6c3479b4c516857634ac63e82c055f46` fetched and verified from the repository after commit
- New one-shot marker `/root/.oldx-h1b-g2a-terminal-stdin-recovery-once-20261126`. Prior marker must exist, must contain `ATTEMPT_CONSUMED=TRUE` and exact original config paths and must NOT contain a success result. It will NOT be reset or removed. Recovery only uses the same previously established isolated G2 Cloud SDK and Docker directories.
- Operator remains native `OLDX-Ubuntu-24.04` root; the same native Linux Google SDK v594.0.1 and bundled Python path with SDK-boundary checks, account `yasminparmar087@gmail.com`, project `oldx-staging`. No credentials copied from Windows or Cloud Shell, no downloaded service account keys.
- **Critical fix:** opens `/dev/tty` as a real controlling terminal FD before consuming the fresh recovery marker, then invokes `gcloud auth login OWNER --no-launch-browser <&tty_fd`. This explicitly avoids the exhausted heredoc stdin. If an active exact Owner login already exists in this isolated config, it skips new OAuth and checks identity; other identity means STOP.
- On successful Owner login, sets project only in the isolated CloudSDK configuration, writes isolated Docker `config.json` credential helper only for `asia-south1-docker.pkg.dev`, then prints sanitized `H1B_G2R_*` success. No Docker push, new build/scan, Cloud IAM/Run/Registry resource mutation, H2 or production.
- If new marker is consumed even with failure, DO NOT retry/delete either marker. Review only sanitized error and plan a distinct bounded resolution. No direct WSL execution or OAuth by assistant; local syntax is checked by `bash -n` before owner runs. This narrow recovery is within already granted G2 login authorization, not expansion to W1–W6.

## One verified-source paste in EXISTING Ubuntu WSL terminal

```bash
bash -euo pipefail <<'OLDX_G2R'
umask 077
d=$(mktemp -d /root/oldx-h1b-g2r-source.XXXXXXXX)
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' \
  --output "$d/recovery.sh" \
  'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/90b03e2bd1f3e0b850c053b6382ad46cb5ee8a87/scripts/step05_h1b_g2a_recover_terminal_stdin_once_20261126.sh'
test "$(git hash-object "$d/recovery.sh")" = '1e325acc6c3479b4c516857634ac63e82c055f46' || { echo 'STOP: SOURCE_HASH_MISMATCH'; exit 2; }
bash -n "$d/recovery.sh"
bash "$d/recovery.sh" --h1b-g2a-terminal-stdin-recovery-once
OLDX_G2R
```

Owner action: when prompted, open the **new** Google browser URL in the trusted local browser, use only Yasmin's account, copy verification code into the Ubuntu terminal (never into this chat), press Enter, and share only last sanitized `H1B_G2R_*` status lines, not the authentication URL/code. The old URL/code from aborted login must not be reused. Any STOP means do not rerun.

Expected:
```
H1B_G2R_OWNER=VERIFIED
H1B_G2R_PROJECT=OLDX_STAGING_ISOLATED_CONFIG
H1B_G2R_DOCKER_HELPER=ONLY_ASIA_SOUTH1
H1B_G2R_REGISTRY_PUSH=NOT_ATTEMPTED
H1B_G2R_CLOUD_RESOURCE_WRITES=NONE
H1B_G2R_RESULT=LOGIN_AND_ISOLATED_DOCKER_HELPER_READY
```

## Next step
After observed recovery success only, prepare G2B single retained-H1A image tag/push and remote digest reconciliation **within previously explicit owner G2 consent**, with collision/identity/digest fail-closed controls. No G2B push has yet occurred. Separate H1B W1–W6 approval remains mandatory; old C1A residual SA/image remain retained; H2/production NO-GO.
