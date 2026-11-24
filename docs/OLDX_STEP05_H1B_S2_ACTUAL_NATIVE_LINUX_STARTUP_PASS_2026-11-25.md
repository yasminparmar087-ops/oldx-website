# OLDX Step 05 H1B — Actual S2 native Linux Google Cloud CLI startup PASS_WITH_LIMITS

**Owner WSL screenshot received 25 November 2026 ~02:53 IST.** Exact scope: ONE owner-approved native Google Cloud CLI v594.0.1 local `gcloud --version` through the newly extracted Linux SDK on `OLDX-Ubuntu-24.04`. GitHub branch `security-hardening-review`.

## Actual evidence, NOT inference of Cloud authority

Screenshot terminal displays `wsl -d OLDX-Ubuntu-24.04 -u root` followed by the SHA256-checked pinned script invocation with heredoc delimiter `OLDX_S2` and the following actual status:
```
S2_RESULT=STARTUP_PASS_WITH_LIMITS
S2_REASON=NONE
S2_VERSION_EXPECTED=594.0.1
S2_NO_AUTH_OR_CLOUD_RESOURCE_COMMANDS=TRUE
```
The success is an **owner-reported real local startup result**. Under the reviewed source, PASS requires new Linux SDK executable to exit 0 AND report exact `Google Cloud SDK 594.0.1` in saved private stdout; 15-second maximum process wait. The screen does not show the full private stdout or a measured duration, so we do NOT claim a specific elapsed time or independently audit child process traces. No separate command for owner account, login, project, resource, IAM, Registry, Firebase, Firestore or Cloud Run occurred. Existing Windows mounted SDK's old timeout is not retroactively resolved—it is bypassed by working native Linux SDK.

**Source used:** `scripts/step05-h1b-native-gcloud-s2-version-once-20261125.py` at pinned GitHub commit `156e49b3abac01adc7ec1b62c73e9b9370e14d44`, Git blob `4ae5cd31a59ae97bf406d00149e22a0a87722d21`, SHA256 `1316872eb539fab1da33bfc6a58629592ec18eb416a9376aef2aa05e70b6f7ff`. Corrected private config parent guard was fixed BEFORE owner execution. Script uses absolute path `/root/oldx-tools/native-gcloud-594.0.1/google-cloud-sdk/bin/gcloud`, matching bundled Linux Python and a NEW private `/root/oldx-tools/native-gcloud-594.0.1-s2-isolated-config`, disables update/telemetry/metadata checks, and only invokes `--version`. S2 marker `/root/.oldx-h1b-native-gcloud-s2-version-once-20261125` is now **CONSUMED** following observed successful owner execution. Do not delete or retry.

## No-repeat/permissions accounting

- Original mixed Windows-SDK WSL `auth list` 40s timeout and version 12s timeout were each already consumed. Neither was rerun. Exact root cause of the Windows-mounted SDK stall remains unknown. 
- Original S1 failed on two implicit-directory tar symlinks after successful checksum, **consumed**. S1R one-pass offline recovery extracted archive and returned `S1R_COMPLETE_NO_CLI_EXECUTION`, **consumed**. Neither repeated.
- H1A Linux/amd64 container build, SBOM, Grype and isolated runtime already consumed. 12 distinct HIGH CVEs accepted **only** for potential future IAM-private compiled-OFF no-real-data max-24h staging experiment. That risk acceptance does not authorize H1B image push, new SA, IAM/Cloud Run deployment or activation.
- User has NOT authorized S3 operator/project/Registry/new-service/new-SA checks, any sign-in or credential migration, Cloud Run/Registry IAM changes, hosted Product, H2, or production. S2 only proves **CLI startup**, NOT authentication/permissions/Cloud readiness.

## Next bounded decision, NOT YET EXECUTED

Source-only planning can now determine an **S3 read-only account/project/target preflight** without repeating consumed historical WSL gcloud scripts. Important: S2 deliberately used a **fresh empty CLOUDSDK_CONFIG** and did not migrate Windows credentials; a working CLI **does not imply an active authenticated principal**. Resolve the principal source and secure isolated authentication in separate owner supervision or use an already-authorized authenticated Cloud Shell session for resource readbacks. Do not silently reuse old credential DBs, run interactive `gcloud auth login`, change default SDK or execute Cloud IAM changes. Confirm scope and a fresh owner approval before any S3 command.

Existing C1A private/default-OFF service retention expires **28 November 2026 at 23:19 IST** absent new owner cleanup/extension decision. No automatic cleanup or production launch approval.

**Current status:** `H1B_NATIVE_SDK_S2=ACTUAL_STARTUP_PASS_WITH_LIMITS`, `S1/S1R/S2_ONESHOT=CONSUMED`, `S3_AUTH_PRINCIPAL=UNVERIFIED`, `H1B_W1_W6=NOT_AUTHORIZED`, `H2/PRODUCTION=NO_GO`.
