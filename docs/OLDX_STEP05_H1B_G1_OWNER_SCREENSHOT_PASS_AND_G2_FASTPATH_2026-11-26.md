# OLDX Step 05 — H1B G1 ACTUAL OWNER RESULT, next G2 fast-path (26 Nov 2026 IST)

Repository: `yasminparmar087-ops/oldx-website`; branch: `security-hardening-review`.
Evidence: screenshot supplied by owner in OLDX Task 27, showing Google Cloud Shell on `oldx-staging` after executing pinned G1 source from commit `373c5d6002f50bb588c58a7c2ca16ab0b3828992`, Git blob `5c3742c5ca9bb5c90895fae6ad64b5e91b4bc77d`. This document is a transcription/review of that screenshot and repository source; assistant did not execute Cloud commands or upload private evidence. Keep source receipt private in the owner Cloud Shell.

## Actual G1 screenshot — no rerun

```text
H1B_G1_PROJECT_SA_CREATE=RETURNED
H1B_G1_PROJECT_SA_DELETE_PROJECT=RETURNED
H1B_G1_PROJECT_SA_ACTAS_PROJECT=RETURNED
H1B_G1_PROJECT_RUN_CREATE=RETURNED
H1B_G1_PROJECT_RUN_DELETE_PROJECT=RETURNED
H1B_G1_PROJECT_RUN_SET_IAM_PROJECT=RETURNED
H1B_G1_PROJECT_RUN_GET=RETURNED
H1B_G1_REPO_UPLOAD=RETURNED
H1B_G1_REPO_DOWNLOAD=RETURNED
H1B_G1_REPO_GET=RETURNED
H1B_G1_REPO_VERSION_DELETE=RETURNED
H1B_G1_FUTURE_NEW_SA_ACTAS=NOT_YET_TESTABLE
H1B_G1_WSL_AUTH=NOT_CONFIGURED
H1B_G1_RESULT=READ_ONLY_WITH_LIMITS
H1B_G1_REASON=PROJECT_AND_REPOSITORY_PERMISSIONS_TESTED
H1B_G1_CLOUD_RESOURCE_WRITES=NONE
```

**Interpretation:** Both read-only `testIamPermissions` calls returned the expected permissions, satisfying the bounded G1 preflight exactly as encoded by the script. This is **not** a guarantee for a future new service account's resource-level `actAs`, WSL Google OAuth credentials, Docker/Registry transport, remote image digest, a deployment, Invoker accessibility, or cleanup authorization. HTTP `POST` here was to read-only test endpoints, NOT a project/Registry resource write. Exact owner one-shot marker `~/.oldx-step05-h1b-g1-effective-permissions-readonly-once-20261126` is CONSUMED; **never rerun, reset the marker, or use another G1 invocation**. Screenshot Cloud Shell banner shows HOME disk usage **100%**, so no build/image export/download/cache in Cloud Shell.

## No-repeat boundaries preserved

- C1A original `oldx-step05-gateway` Cloud Run service removal already independently `CONFIRMED_REMOVED`; do not delete/readback/reprobe it. The separate C1A service account exact UID `102194769236111252832` and pinned image `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a` still exist, dependencies unknown: **RETAIN**.
- H1A local WSL image `oldx-h1a-c2-mediator-off:local-20261124t195244z` with local image ID `sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`; source, one build, SBOM 15 packages, Grype 12 HIGH/0 Critical and offline runtime smoke already saved; **NO rebuild, rescan, repull, export to Cloud Shell or deletion of local image**.
- Existing WSL native Linux Cloud SDK S2 version startup PASS_WITH_LIMITS, but G1's Owner Cloud Shell authentication is NOT inherited by WSL. Original Windows-mounted SDK timeout, WSL S1/S1R/S2, Owner S3/S3B and all prior H1A/C1A one-shot markers remain consumed. No rework.

## Fastest next genuinely new gate: H1B G2, supervised WSL-only authentication and retained image transport

1. **Before any credential change or push, obtain separate narrow owner consent** for a single native-WSL Google OAuth login (isolated `CLOUDSDK_CONFIG`), an isolated Docker auth configuration restricted to `asia-south1-docker.pkg.dev`, and ONE Registry push of the retained exact H1A image into the existing shared repository at a unique NEW H1B image name/tag. No key file, Windows-to-WSL token copy, other registry login, Cloud Shell image transfer, new build or scan.
2. Confirm installed *native Linux* WSL `gcloud` path and preexisting isolated config without printing tokens; inspect existing frozen local image ID/config without re-running prior tests. On an authorized login, verify Google identity is exactly Yasmin's Owner and project `oldx-staging`; Docker helper only for the single Registry host. STOP on auth ambiguity, missing image, existing tag or denied upload.
3. Reuse frozen local H1A image; push once only with pre-declared unique new name/tag, capture actual remote immutable manifest/index plus linux/amd64 config/digest and verify against retained H1A custody. Local Docker image ID, local BuildKit child digest, and old C1A image digest are NOT the new Registry image digest. Do not deploy on mismatch.
4. W1–W6 still need distinct explicit finite owner approval and verified **new-SA resource-level** `actAs` and new-only cleanup feasibility: at most one new no-key SA, one private compiled-OFF Cloud Run service, optional service-level Owner Invoker only, up to four new-only authenticated/anonymous HTTP probes, supervised same-session guarded cleanup. Owner Option B accepts 12 HIGH only for an IAM-private/off/no-real-user-data experiment, max 24h from activation; production/H2 and Firebase rules remain NO-GO. Do not silently convert G1 into W1–W6 authority.
5. Do not spend time on optional residual C1A SA/image deletion now; inventory separately before any destructive action. Cloud Shell HOME is full, reinforcing the WSL-to-Registry route (no new Cloud Shell large workloads).

**Present checkpoint:** `H1B_G1=READ_ONLY_WITH_LIMITS_ACTUALLY_RUN_CONSUMED`; `H1B_G2=AWAITING_EXPLICIT_OWNER_WSL_LOGIN_AND_PUSH_CONSENT`; `H1B_REMOTE_IMAGE_DIGEST=UNKNOWN`; `H1B_NEW_CLOUD_WRITES=NONE`; `H1B_W1-W6=NO_GO`; `STEP05=NOT_COMPLETE`; `H2/PRODUCTION=NO_GO`.

Canonical preceding source: [G1 fastpath preparation](OLDX_STEP05_H1B_FASTPATH_AFTER_C1A_CONFIRMED_2026-11-26.md); [G0–G6 guardrails](OLDX_STEP05_H1B_FASTPATH_FINAL_OPERATION_AND_C1A_DECISION_2026-11-26.md). No GitHub `main` changes, cloud changes, SDK authentication, build/push/deploy, or runtime probes were performed by the assistant in this review.
