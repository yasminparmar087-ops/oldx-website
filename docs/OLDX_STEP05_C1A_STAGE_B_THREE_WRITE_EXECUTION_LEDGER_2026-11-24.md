# OLDX Step05 C1A Stage B — owner-approved exact three-write supervised execution ledger

**Date:** 24 November 2026 IST. **Code branch:** `security-hardening-review`. **Source of owner consent:** latest [C1A fastpath ledger](OLDX_STEP05_C1A_FASTPATH_OWNER_DECISION_AND_PROVENANCE_2026-11-24.md), section “OWNER EXPRESS C1A STAGE B AUTHORIZATION”. Owner said **"ha manjuri chhe"** directly when asked to approve (1) one new no-key unprivileged service account; (2) one existing scanned WSL image push and remote digest capture; (3) one new private default-OFF Cloud Run Gateway; plus exact NEW-resource-only supervised cleanup. **Approval does not imply execution.**

## Consumed existing results (DO NOT REPEAT)
- Prior 84 focused synthetic Node cases, previous Step04 A8 signed build/SLSA/Syft/Grype/B1/R1, backend traffic/IAM/default DB results.
- Existing Windows WSL built **NEW** Gateway image local Docker ID `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`, local tag `oldx-step05-gateway-off:wsl-once-20261124-801`; previously Linux amd64, Node24 nonroot `65532:65532`, read-only, health200/API503/SIGTERM, Syft JSON/CycloneDX valid, Grype 55 package matches incl 12 distinct HIGH CVE IDs. No new scan/rebuild. 12-HIGH owner accepted only for the new IAM private OFF-only C1A with limits.
- ONE Google Distroless immutable **BASE PARENT** keyless signature successfully verified by owner's CMD/WSL screenshot: `INDEX_SIGNATURE=PASS_PINNED_PARENT_ONLY`. Parent index SHA256 `39b0407357c9fadf1a9708d22088f02de21f0e1e8a688474eea2d8701e7d5693` historically contains exact Dockerfile-pinned linux/amd64 child SHA256 `49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec`. Not proof of signature/attestation for derived image; local Docker image ID is NOT remote manifest digest.
- Old Step05 scoped Cloud preflight: proposed new SA and `oldx-step05-gateway` service `NOT_FOUND_REPORTED` then; `oldx-staging-images` Docker registry exists in `asia-south1`, project active, billing linked, direct project 2 Owner/1 Editor members, active operator Owner; effective inherited IAM not fully proven. These are historical and must not be needlessly rerun; just-in-time **exact object collision and operator/project proof before a write** are allowed and mandatory.

## Proposed resource identifiers — owner authorized, NOT created as of this ledger
- Project `oldx-staging`, numeric project ID from prior evidence `38472235077`; region `asia-south1`.
- NEW dedicated `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com` with no role/key/data-API permissions.
- Existing Registry `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images`. Proposed **NEW image name** `oldx-step05-gateway-off`. Push just one existing local derived image, record exact remote `@sha256:` after comparing readback. No Cloud Build.
- NEW Cloud Run `oldx-step05-gateway` ONLY, image pinned by resulting real remote digest; `--no-allow-unauthenticated --invoker-iam-check --ingress=all` (network reachable, IAM-required), `--cpu=1 --memory=512Mi --min-instances=0 --max-instances=1 --concurrency=1 --timeout=5s --no-cpu-boost`, request-based, new dedicated SA, no secrets, env activation, Firebase/KMS/backend grant; no HTTP C1A probes.
- Preserve **ALL** old `oldx-owner-read` revisions, root 100%, A8 0%, tags, IAM and all Firebase/Auth/Firestore/billing settings. No allUsers or allAuthenticatedUsers.
- Finite <=24h supervised OFF trial, only exact newly created resources may be cleaned after ownership/digest/no-dependency check; not an automatic scheduled clean. C1B calls/turn-on/C2/production are NOT in this permission. No hard rupee cap/billing form per newer owner instruction; keep min0/max1 and avoid extra billed services.

## Runbook sequence — ONE new write at a time, no blind retries

**P0 (now, local preflight, read-only; NOT repeat of old image tests):** User CMD shell must show `gcloud` availability, active owner account and configured project, and **just local** WSL Docker image digest/platform/user for exact preexisting tag. Recommended one command:

```cmd
where gcloud & gcloud auth list --filter="status:ACTIVE" --format="value(account)" & gcloud config get-value project & wsl -d OLDX-Ubuntu-24.04 -- docker image inspect --format "{{.Id}} {{.Os}}/{{.Architecture}} {{.Config.User}}" oldx-step05-gateway-off:wsl-once-20261124-801
```

Expected exactly `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a linux/amd64 65532:65532`; project `oldx-staging`, active intended owner. If Windows CMD lacks `gcloud`, use existing Windows **Google Cloud SDK Shell** instead; do NOT install another SDK or create a new login/key. If output differs, STOP; no Cloud writes.

**P1 (after P0 PASS, narrow JIT Cloud checks):** exact project-number/active identity match, `gcloud run services describe oldx-step05-gateway --project=oldx-staging --region=asia-south1` must return *unambiguous NOT_FOUND*, exact SA describe must return NOT_FOUND, existing Registry must report correct project `asia-south1` and Docker format, target NEW image name/tag must be absent. Permission denied/error is **STOP** not `not found`. No full IAM/audit, project-wide billing report, old backend audit, or existing image rescan.

**B1 approved first Cloud write:** `gcloud iam service-accounts create oldx-step05-gateway --project=oldx-staging --display-name="OLDX Step05 OFF-only Gateway"`. Record created exact SA email+uniqueId and readback. If no privileges/identity mismatch, STOP without grant. Do not repeat if created.

**B2 approved one remote image upload:** in existing WSL local Docker, first verify exact source tag/image ID/user/platform, use scoped non-persistent Docker Registry authentication via current owner `gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://asia-south1-docker.pkg.dev` (Google's supported method; ensure credentials **never printed or written to repo**, prefer temporary DOCKER_CONFIG). Tag that **same** exact local image to one new immutable one-off tag under `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off` and push **once** (no rebuild). Read exact remote tag metadata using `gcloud artifacts docker images describe ...:tag --format=json`, require actual `sha256` digest before B3. Do not assume derived local Docker image ID equals remote manifest digest; no repeat on ambiguous push without targeted readback.

**B3 approved new isolated Cloud Run create:** use that exact **remote digest** (not tag/local ID), explicit `--no-allow-unauthenticated --invoker-iam-check --ingress=all --min-instances=0 --max-instances=1 --concurrency=1 --cpu=1 --memory=512Mi --timeout=5s --no-cpu-boost --service-account=...` and project/region. Cloud CLI local help/version must expose flags; no auto update/extra API enable/roles. Immediately read back the exact new service revision, image pinned digest, flags, attached SA, effective direct IAM public bindings, new resource identity and isolated traffic. If inherited owner invocation broader than known historical limits, STOP future tests until reviewed. **No HTTP requests** under C1A.

**Recovery:** if B1 succeeded but later stage failed, do not recreate the SA or push another tag; preserve exact receipt. Cleanup only exact NEW service (after checking service UID and no unexpected dependencies), exact new image digest (ensure unreferenced and target tag belongs to this run), exact new SA uniqueId (after service deletion/no other use). Never touch registry repository itself, other images or old product service. Single cleanup authority granted, but no automatic deletion without exact-ID preimage and user-observed timestamp. Preserve receipts in GitHub source-only text, no tokens/account secrets.

## Status at this write
`STAGE_B_OWNER_CONSENT=APPROVED` / `STAGE_B_P0=AWAITING_LOCAL_COMMAND` / `B1_SA=NOT_EXECUTED` / `B2_IMAGE_PUSH=NOT_EXECUTED` / `B3_PRIVATE_RUN=NOT_EXECUTED` / `C1B_HOSTED=NOT_AUTHORIZED` / `C2_AND_PRODUCTION=NO_GO`.


## 24 Nov 2026 ~22:00 IST — Owner CMD screenshot: actual P0 local preflight PASS, NO cloud writes

**Actual observed CMD commands and results from user screenshot** (not a fresh assistant-authenticated cloud login):

- `where gcloud`: Windows SDK in `D:\\Temp\\google-cloud-sdk\\bin\\gcloud` and `gcloud.cmd`; installed, no need to install/relogin.
- `gcloud auth list --filter="status:ACTIVE" --format="value(account)"`: exact intended Yasmin owner account **MATCH**, email retained privately in screenshot, not reproduced in public handoff.
- `gcloud config get-value project`: **`oldx-staging`**.
- `wsl -d OLDX-Ubuntu-24.04 -- docker image inspect --format "{{.Id}} {{.Os}}/{{.Architecture}} {{.Config.User}}" oldx-step05-gateway-off:wsl-once-20261124-801`: **`sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a linux/amd64 65532:65532`** — exact reviewed/prebuilt image, no rebuild/scan needed.

**P0 outcome: `P0_OWNER_PROJECT_LOCAL_IMAGE=PASS`.** Owner has authorized Stage B three writes and exact new-resource cleanup; *none yet performed*. The Cosign pinned parent signature remains **CONSUMED/PASS** and derived remote manifest **NONE**. JIT resource no-collision checks are still REQUIRED before B1 (and B3), with no attempt to rerun the whole historical C1A inventory. Image remote path/name conflict check only immediately before B2. Do NOT create resource on a PERMISSION_DENIED, ambiguous failure or existing name.

**NEXT single user CMD P1 strictly READ-ONLY:**
```cmd
gcloud projects describe oldx-staging --format="value(projectNumber)" & gcloud iam service-accounts describe oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com --project=oldx-staging --format="value(uniqueId)" & gcloud run services describe oldx-step05-gateway --project=oldx-staging --region=asia-south1 --format="value(metadata.name)"
```
Expected project number `38472235077` and two **explicit NOT_FOUND** outputs. `&` is intentional to display all three independent read-only statuses; NOT an all-pass detector. If any exact new resource EXISTS or results are PERMISSION_DENIED/ambiguous, **STOP**. Check screenshot before creating B1. Avoid repeating P0, builder, scanner, Cosign, old service/IAM/Registry/Billing checks.

Current: `P0=PASS`, `P1_NEW_RESOURCE_COLLISION=AWAITING_OWNER_OUTPUT`, `B1/B2/B3=NOT_EXECUTED`, `C1B/C2/PRODUCTION=NO_GO`.


## 24 Nov 2026 ~22:27 IST — Owner CMD actual P1 JIT exact new resource name/number checks PASS

New screenshot from owner CMD shows exactly:
- `gcloud projects describe oldx-staging --format="value(projectNumber)"` => `38472235077`, matching original approved project number.
- `gcloud iam service-accounts describe oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com --project=oldx-staging --format="value(uniqueId)"` => `NOT_FOUND: Unknown service account` with current intended owner identity. This is explicit absence at lookup, **not** a 403 permission-denied.
- `gcloud run services describe oldx-step05-gateway --project=oldx-staging --region=asia-south1 --format="value(metadata.name)"` => `Cannot find service [oldx-step05-gateway]`. This is explicit absence at lookup, **not** a 403 permission-denied.

**No service account creation, Registry push, Cloud Run deploy, IAM grants, Cloud-hosted request, Firebase/Rules or production action performed as part of this screenshot.** These checks establish `P1_PROJECT_NUMBER=PASS`, `P1_NEW_SA_NAME=NOT_FOUND_CONFIRMED_AT_CHECK`, `P1_NEW_RUN_SERVICE=NOT_FOUND_CONFIRMED_AT_CHECK`. Exact P0 owner/project/WSL existing image ID/amd64/nonroot had already passed; do not rerun P0/P1 just for reassurance. Historic 84 tests, build/scan, parent Cosign and old project audit are consumed.

**NEXT authorized B1 — ONE write, then targeted readback ONLY:**
```cmd
gcloud iam service-accounts create oldx-step05-gateway --project=oldx-staging --display-name="OLDX Step05 OFF-only Gateway" && gcloud iam service-accounts describe oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com --project=oldx-staging --format="value(email,uniqueId)"
```

The last `describe` is read-only and executes only after creation command succeeds. Google IAM docs note newly created service-account read visibility can lag; if create returns success but immediate describe reports NOT_FOUND, **DO NOT re-create**. Freeze and inspect single creation result, with later one precisely scoped readback if necessary. If create returns `ALREADY_EXISTS` or `PERMISSION_DENIED`, **STOP/no retry**. No `roles/` assignment, `keys create`, project IAM, Firebase, Artifact Registry or Cloud Run write under B1. B2 image push and B3 new private Cloud Run remain separately sequenced within the already approved Stage B scope and require actual B1 receipt to proceed.

**Actual status here**: `P0=PASS`, `P1=PASS`, `B1_SA_CREATE=OWNER_APPROVED_AWAITING_EXECUTION`, `B2_IMAGE_PUSH=NOT_EXECUTED`, `B3_RUN_CREATE=NOT_EXECUTED`, `C1B/C2/PRODUCTION=NO_GO`.


## 24 Nov 2026 ~22:33 IST — B1 CLOUD WRITE SUCCESS (user-observed screenshot), never repeat

Actual owner CMD screenshot shows `gcloud iam service-accounts create oldx-step05-gateway --project=oldx-staging --display-name="OLDX Step05 OFF-only Gateway"` returned `Created service account [oldx-step05-gateway]`. Chained exact `gcloud iam service-accounts describe oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com --project=oldx-staging --format="value(email,uniqueId,disabled)"` returned email with **uniqueId `102194769236111252832`** and no disabled=true value visible. This is evidence of **ONE real new Cloud write** and readback, not just a plan.

**B1 status: `NEW_SA_CREATE=PASS`, `NEW_SA_READBACK=PASS`, `NEW_SA_UNIQUE_ID=102194769236111252832`. DO NOT run Service Account CREATE again**, do not issue keys/roles/project IAM grants, do not touch other existing SAs. Owner's Stage B narrow consent remains for B2 one existing local scanned OFF image push to the already existing regional Registry, B3 one new private disabled Cloud Run service and guarded exact new-resource-only cleanup. As of this screenshot **no B2 push or B3 deployment performed**. Previously verified WSL local `oldx-step05-gateway-off:wsl-once-20261124-801` => `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`, `linux/amd64`, user `65532:65532`. Historical parent signature PASS; local image scan 12 HIGH owner-accepted limited OFF-only. No repeat local Docker build/SBOM/Grype/Cosign or old 84 tests. User no hard ₹ cap/no billing forms, but avoid extra cloud resources. **Important: existing Owner Cloud Run deployer may still need `iam.serviceAccounts.actAs`; do not grant project roles to fix without fresh consent.**

**Next B2 ONLY:** choose exactly one unique derived-image Registry tag, check exact target collision/read permission (read-only; do not redo entire Registry/Project metadata), then use the preexisting WSL Docker image with owner-authenticated short-lived registry token, a temporary isolated Docker config, and ONE push. Capture actual `sha256` remote manifest digest (not Docker local image ID). After any ambiguous timeout, inspect exact remote tag only; NO blind second push. B3 Cloud Run deploy requires observed B2 remote digest. `C1B_HOSTED_HTTP=NOT_AUTHORIZED`; `C2/PRODUCTION=NO_GO`.


## 24 Nov 2026 ~22:33 IST — B2 one-shot existing-local-image push prepared in source, NOT RUN

After B1 actual CREATE/READBACK success, added [single-image guarded WSL Registry upload script](../scripts/step05-c1a-stage-b-one-image-push-once-20261124.sh). This does not mean B2 is executed. The script uses *only* previously built/source-locked WSL local image ID `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a` and local tag `oldx-step05-gateway-off:wsl-once-20261124-801`, checked again only as a guard, requires local linux/amd64/nonroot and default Docker daemon. The sole intended new Artifact Registry image/tag is **`asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off:c1a-off-20261124-801`**; pre-image exact remote tag needs a single JIT NOT_FOUND verification before running, NOT another full Registry inventory. Reuses Windows gcloud authenticated owner short-lived token piped into WSL Docker `login --password-stdin` with isolated temporary Docker credential config, never prints token, no gcloud in WSL, no Docker build, Syft, Grype, Cosign, cloud service/IAM/Firebase/Run changes. Creates one owner-WSL pre-push one-shot marker before the first remote push (so no blind retries) and one small local evidence folder; records Docker-reported manifest digest separate from local image ID. After B2 success, remote `gcloud artifacts docker images describe` must **independently verify the actual registry digest** before B3. This preparation is not authentication, remote write or proof of push.

**Next ONE Windows CMD exact-target READ-ONLY collision check**:
```cmd
gcloud artifacts docker images describe asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off:c1a-off-20261124-801 --project=oldx-staging --format="json"
```
Expected **explicit NOT_FOUND** only (no matching tag/image); if image exists or PERMISSION_DENIED/timeout/other ambiguous error, STOP, do not push. Does not repeat old A8 or previous registry-wide read. Once result confirmed, proposed ONE command from Windows CMD to push, after updating existing stable clone with only `git pull --ff-only`:
```cmd
wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && git pull --ff-only"
gcloud auth print-access-token | wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && bash scripts/step05-c1a-stage-b-one-image-push-once-20261124.sh"
```
These two lines are **future** steps only after exact remote target absence confirmation; no cloud write has been executed merely by adding the script. If push is ambiguous, run only targeted new-tag readback and STOP, no second push. Never share auth tokens or old resources. `B1=PASS`, `B2=PREPARED_AWAITING_JIT_TARGET_ABSENCE`, `B3=NOT_EXECUTED`, `C1B/C2/PRODUCTION=NO_GO`.


## 24 Nov 2026 ~22:37 IST — B2 exact-tag JIT registry absence CONFIRMED, ONE PUSH NOW APPROVED TO EXECUTE

Owner CMD screenshot shows single scoped exact-tag `gcloud artifacts docker images describe asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off:c1a-off-20261124-801 --project=oldx-staging --format=json` returned **`ERROR: (gcloud.artifacts.docker.images.describe) Image not found.`**, not PERMISSION_DENIED. This is expected for NEW exact image/tag; the accompanying generic syntax help is not a second failure. `B2_REMOTE_TARGET_COLLISION=NOT_FOUND_CONFIRMED_AT_CHECK`. Previously verified B1 actual service account exists with uniqueId `102194769236111252832`, and local WSL approved image exact ID/amd64/nonroot already PASS. **No B2 push occurred in this screenshot.**

**NEXT execute existing guarded B2 script once, from Windows CMD, two commands**, no rebuild:
```cmd
wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && git pull --ff-only"
gcloud auth print-access-token | wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && bash scripts/step05-c1a-stage-b-one-image-push-once-20261124.sh"
```
The `gcloud` command uses active intended Yasmin account to pass short-lived credentials exclusively via stdin (NEVER paste/print token), in accordance with official Artifact Registry access-token Docker login guidance https://docs.cloud.google.com/artifact-registry/docs/docker/authentication. WSL script uses `docker login --password-stdin`, temporary Docker credential config, exact local SHA check, one-shot marker before first push, no Docker build/rescan, creates limited log under `$HOME/oldx-step05-c1a-b2-push-20261124/`. **Do not re-run the second command** after any ambiguous error, timeout, or even apparent success; inspect only exact saved summary and targeted new registry tag before proceeding. If `git pull` fails, STOP; no push.

**After successful owner-reported B2 push:** record printed Docker-reported digest separately from local Docker image ID, and use one new targeted `gcloud artifacts docker images describe <exact new tag>` read to verify remote `sha256` before B3 Cloud Run. B3 remains authorized but NOT EXECUTED; no C1B HTTP, C2/production. No old 84 tests, source image build/Syft/Grype, Cosign, old C1A Registry inventory repeated.


## 24 Nov 2026 ~23:13 IST — OWNER-OBSERVED B2 ONE PUSH SUCCEEDED; REMOTE REGISTRY READBACK STILL REQUIRED

Owner Windows CMD screenshot after authorized B2 shows:

- WSL existing stable clone `git pull --ff-only` fast-forward success `f68fc2a..0597772`. The B2 one-shot source and ledger were retrieved. No build/scan rerun.
- `gcloud auth print-access-token | wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && bash scripts/step05-c1a-stage-b-one-image-push-once-20261124.sh"` executed ONCE. It reported `AUTH=SHORT_LIVED_OWNER_TOKEN_FROM_STDIN`, `DOCKER_LOGIN=PASS_TEMPORARY_CONFIG`, `ONE_REMOTE_PUSH=STARTED`, **`B2_PUSH_SUCCESS_UNVERIFIED_REMOTE_READBACK`**.
- Intended tag `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off:c1a-off-20261124-801`.
- Script stdout `REMOTE_DIGEST=sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`. **CAUTION:** this happens to be identical to previously verified local Docker image ID. Do NOT assume it is the remote OCI manifest digest merely from this matching value. Could reflect image-store semantics or a reporting ambiguity; independently verify registry's actual remote digest before any B3.
- WSL private report `/root/oldx-step05-c1a-b2-push-20261124/summary.txt` (not extracted/reviewed by assistant). The one-shot B2 marker is consumed; **NEVER run B2 push again** automatically.
- No Cloud Run B3 create, no C1B hosted HTTP, no C2 Product enabling, no Firebase/Rules/other IAM/backend changes observed.

**Next ONE CMD read-only independently sourced remote digest check (same exact tag, now AFTER observed push):**

```cmd
gcloud artifacts docker images describe asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off:c1a-off-20261124-801 --project=oldx-staging --format="json"
```

Require successful Artifact Registry tag/digest evidence, correct project/repository/architecture; preserve actual returned `sha256` value as the **remote** immutable deployment input. If registry readback is missing, permission-denied, returns an unrelated image/tag, or ambiguous, STOP and inspect saved B2 logs/manifest, **not a second push**. Do not deploy by tag or local Docker image ID before this. `B1_SA=PASS`, `B2_DOCKER_PUSH=SUCCESS_REPORTED_PENDING_INDEPENDENT_REGISTRY_READBACK`, `B3_PRIVATE_RUN=NOT_EXECUTED`, `C1B/C2/PRODUCTION=NO_GO`.


## 24 Nov 2026 ~23:15 IST — B2 REGISTRY INDEPENDENT REMOTE DIGEST READBACK PASS (owner screenshot)

Owner CMD screenshot of **ONE targeted post-push remote** `gcloud artifacts docker images describe asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off:c1a-off-20261124-801 --project=oldx-staging --format=json` returned `image_summary`:
- `registry: asia-south1-docker.pkg.dev`, `repository: oldx-staging-images`.
- **`digest: sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`**.
- `fully_qualified_digest: asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off@sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`.
- **`slsa_build_level: unknown`**; this readback DOES NOT certify SLSA/derived signed attestation. Distroless **BASE PARENT** official Cosign signature PASS was consumed separately; new image includes previously accepted 12 distinct HIGH CVEs for isolated PRIVATE DEFAULT-OFF C1A only.

Remote digest happens to equal the local image ID; independent GCP registry metadata **confirmed** this exact value. It is now valid to use the registry's own immutable `fully_qualified_digest` in the B3 Cloud Run deploy command. This is a distinct B2 result; **do NOT repeat tag lookup/push/build/Syft/Grype/Cosign**, and do not falsely claim all vulnerabilities fixed or production certified.

**B2 FINAL:** `B1_NEW_SA=PASS` uniqueId `102194769236111252832`; `B2_ONE_PUSH=PASS`; `B2_INDEPENDENT_REMOTE_DIGEST=PASS`; `B3_NEW_PRIVATE_OFF_SERVICE=AUTHORIZED_NOT_YET_EXECUTED`; `C1B_HOSTED_HTTP/C2/PRODUCTION=NO_GO`. Existing Owner tester/inherited 2 Owner+1 Editor potential access (NOT sole invoker) accepted only for OFF C1A, no public binding, new runtime SA has no newly assigned roles.

**Next:** one just-in-time check of exact NEW `oldx-step05-gateway` Cloud Run service absence and local CLI `gcloud run deploy` supported flags if necessary (different write and ~1 hour after original P1 service name check). Then execute ONE owner-approved `gcloud run deploy` with **the verified immutable digest** only, explicit `--invoker-iam-check --no-allow-unauthenticated --ingress=all --min-instances=0 --max-instances=1 --concurrency=1 --cpu=1 --memory=512Mi --timeout=5s --no-cpu-boost --port=8080`, new dedicated SA `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com`, no Product/Firebase/KMS backend and no hosted HTTP user probes. Exactly read back newly created service/traffic/IAM after the one deploy; if partial/ambiguous STOP, **NO blind repeat**. No existing `oldx-owner-read` permissions/traffic/tags or project IAM changes. <=24h owner-supervised new-resource-only cleanup remains authorized separately from any unrelated deletion.


## 24 Nov 2026 ~23:15 IST — PREPARED ONE B3 PRIVATE OFF-ONLY CREATE COMMAND (NOT RUN)

Verified current official Google CLI help for `gcloud run deploy`: supports `--invoker-iam-check --no-allow-unauthenticated --ingress --min-instances --max-instances --concurrency --cpu --memory --timeout --no-cpu-boost --cpu-throttling --port --service-account --image`. References: https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy, https://docs.cloud.google.com/run/docs/securing/managing-access. The approved source code is isolated OFF-only Node24 HTTP service: health GET200 and Product API503, no Firebase, KMS, backend client or secrets. NOTE: local WSL Docker `--read-only` testing does **not** prove Cloud Run root filesystem is read-only. No claim of signed derived-image attestation (`slsa_build_level=unknown`). Previous new-image 12 HIGH CVE risk owner-accepted for this limited PRIVATE default-OFF C1A ONLY.

**Exact B3 immediate prewrite ONLY (not a full old-asset re-audit):**
```cmd
gcloud run services describe oldx-step05-gateway --project=oldx-staging --region=asia-south1 --format="value(metadata.name)"
```
Only **`Cannot find service [oldx-step05-gateway]`** is acceptable to proceed. Any existing service, permission error or other unclear status STOP. This is justified by the time interval since earlier P1; no repeat old A8/IAM/Registry/SA/source scan. Old SA B1 and remote Registry B2 already confirmed.

**ONE owner-approved B3 deployment only after clean new-service NOT_FOUND, Windows CMD single long line:**
```cmd
gcloud --quiet run deploy oldx-step05-gateway --project=oldx-staging --region=asia-south1 --image=asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off@sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a --service-account=oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com --ingress=all --invoker-iam-check --no-allow-unauthenticated --min-instances=0 --max-instances=1 --concurrency=1 --cpu=1 --memory=512Mi --timeout=5s --port=8080 --cpu-throttling --no-cpu-boost
```

WARNING: this command is a **real Google Cloud billed resource write**, not read-only; approved by owner only for one NEW service. Ingress `all` is internet-addressable but MUST be IAM authenticated; historic 2Owners/1Editor possible inherited Invokers accepted as not exclusive. May fail due to `iam.serviceAccounts.actAs`, quota, project/org, runtime incompatibility, or CLI flags; **do not auto-enable APIs, grant IAM, repeat deploy, alter old service, bypass authentication, tag old A8 or start HTTP probes**. After any apparent success or ambiguous failure, perform one **read-only exact new service describe/iam-policy verification**, preserve actual revision, traffic, image digest, SA, min/max/concurrency/memory/cpu/timeout, ingress and required IAM flag. STOP if any mismatch, notify owner for narrowly scoped recovery. Exactly newly created resources only may be guarded-cleaned within owner consent; <=24h supervised trial, not automatic expiration.

**Current before owner runs B3:** `B1=PASS`; `B2_REMOTE_DIGEST=PASS`; `B3_PRIVATE_GATEWAY_DEPLOY=NOT_YET_EXECUTED`; `C1B/C2/PRODUCTION=NO_GO`.


## 24 Nov 2026 ~23:19 IST — B3 NEW CLOUD RUN SERVICE DEPLOYED: OWNER SCREENSHOT SUCCESS, CONFIG/IAM READBACK NEXT

Owner's current Windows CMD screenshot shows:
- JIT NEW name lookup `gcloud run services describe oldx-step05-gateway --project=oldx-staging --region=asia-south1 --format="value(metadata.name)"` -> **`Cannot find service [oldx-step05-gateway]`** before the one allowed deployment. This is a clean new-name prewrite check.
- The one previously approved immutable digest deploy ran:
  `gcloud --quiet run deploy oldx-step05-gateway --project=oldx-staging --region=asia-south1 --image=asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off@sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a --service-account=oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com --ingress=all --invoker-iam-check --no-allow-unauthenticated --min-instances=0 --max-instances=1 --concurrency=1 --cpu=1 --memory=512Mi --timeout=5s --port=8080 --cpu-throttling --no-cpu-boost`.
- CLI output `OK Deploying new service... Done.`, `OK Creating Revision...`, `OK Routing traffic...`, `Done.`, followed by **`Service [oldx-step05-gateway] revision [oldx-step05-gateway-00001-thd] has been deployed and is serving 100 percent of traffic.`** The **100% refers to NEW Gateway service routing only**, NOT the existing Product `oldx-owner-read` root/A8 traffic. Output new service URL `https://oldx-step05-gateway-38472235077.asia-south1.run.app` but DO NOT invoke it: C1B hosted HTTP remains separately gated.
- This is evidence that **the THIRD approved B3 CLOUD WRITE WAS PERFORMED ONCE AND REPORTED SUCCESS**. It is **NOT proof** of actual postwrite IAM binding, invoker-iam-disabled effective flag, ingress, deployed image digest, new SA attachment, min/max, CPU/memory, readiness at invocation, or service source 503 under hosted traffic. Stage B independent configuration/IAM metadata readback is the next permitted read-only action.
- No old A8/root/tag IAM traffic changes, Firebase Auth/Firestore/Rules, Product enablement or C1B HTTP are demonstrated by the screenshot. Do NOT assert they were independently checked now. Existing local image Syft/Grype 12 HIGH risk still accepted only for bounded isolated private OFF-only C1A. Derived image SLSA remains `unknown`. Owner no-hard-cost-cap/no-Billing-form preference unchanged; new Cloud Run resource may incur ordinary charges. Trial planned supervised <=24h; no automatic shutdown timer was actually installed.

**NEXT one narrowly scoped READ-ONLY postwrite B3 configuration and direct service IAM inspection** in same Windows CMD (two independent GET commands, no token/HTTP, no repeats of existing inventory):

```cmd
gcloud run services describe oldx-step05-gateway --project=oldx-staging --region=asia-south1 --format="yaml(metadata.name,metadata.uid,metadata.annotations,spec.template.metadata.annotations,spec.template.spec,status.latestReadyRevisionName,status.traffic)"
gcloud run services get-iam-policy oldx-step05-gateway --project=oldx-staging --region=asia-south1 --format="yaml(bindings,etag)"
```

Evaluate live metadata for exact revision `oldx-step05-gateway-00001-thd`, immutable `@sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`, intended new service identity, `ingress=all`, invoker IAM **ENABLED** (i.e. skip-invoker-iam NOT set), `min0/max1`, CPU1/512MiB, concurrency1, timeout5s, port8080, no activation env/secrets and 100% routed to only this new revision. Exact service direct IAM must contain NO `allUsers` or `allAuthenticatedUsers`; inherited 2 Owner/1 Editor project access remains previously accepted, not exclusive. If missing fields due to CLI output projection, run only a narrowly targeted read of same service, not a second deployment or blanket IAM audit. If any unexpected mismatch, STOP and do not call hosted URL. Targeted postwrite GETs do not imply that C1B hosted tests are approved.

**Actual current:** `STAGE_B_OWNER_APPROVED=YES`; `B1_SA_CREATE_READBACK=PASS` uniqueId `102194769236111252832`; `B2_SINGLE_UPLOAD_REMOTE_DIGEST_READBACK=PASS`; `B3_CREATE_DEPLOY_CLI=SUCCESS`; `B3_SERVICE_IAM_CONFIG_READBACK=AWAITING`; `C1B_HOSTED_HTTP=NOT_AUTHORIZED`; `C2_ENABLED/PRODUCTION=NO_GO`. **DO NOT REPEAT B1/B2/B3 writes, build, scan, base Cosign or old 84 tests.** New-only cleanup remains previously owner authorized after exact resource identity/dependency safety checks.


## 24 Nov 2026 ~23:24 IST — B3 ONE-TIME POSTWRITE CONFIG AND DIRECT IAM READBACK: PASS WITH LIMITS

**Owner-supplied TWO actual screenshots** of the exact previously requested `gcloud run services describe` and `gcloud run services get-iam-policy` READ-ONLY commands. No cloud write or hosted HTTP performed:

- New service `metadata.name=oldx-step05-gateway`, **new service UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`**, creator/last modifier current intended Yasmin account.
- `run.googleapis.com/ingress=all`, `ingress-status=all` (internet network reachability; NOT anonymous invocation).
- `metadata.annotations["run.googleapis.com/maxScale"]="20"` **SERVICE-LEVEL** cap, but `spec.template.metadata.annotations["autoscaling.knative.dev/maxScale"]="1"` is the SINGLE live **REVISION-LEVEL** cap, and `status.traffic=100%` to the sole new revision. Official Google Cloud Run max-instance docs confirm when both are set the effective max for a revision is **the lesser number**, hence **effective ONE** for CURRENT new revision, not 20. See https://docs.cloud.google.com/run/docs/configuring/max-instances, section "Use both service-level and revision-level minimum or maximum instances". No config change needed now. A FUTURE new revision without revision max 1 could have a higher ceiling; require separate later review, never imply permanent hard cap.
- Revision-specific `cpu-throttling=true`, `startup-cpu-boost=false`, `containerConcurrency=1`, image **`asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off@sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`** (matches independently read remote digest), port8080, CPU `1`, memory `512Mi`, request `timeoutSeconds=5`, serviceAccountName `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com`; no `env`, secret mounts, data/backend grant or activation var shown in projected spec. `startupProbe` displays TCP port 8080 with 240-second timeout/period, separate from request timeout 5s.
- `status.latestReadyRevisionName=oldx-step05-gateway-00001-thd`, `status.traffic` only this revision `percent=100`. This 100% is **new service only** and does not demonstrate direct observation of old backend's traffic.
- Service IAM returned **`etag: ACAB` only**, **NO direct `bindings`**. Thus no direct public `allUsers`/`allAuthenticatedUsers` IAM grant. No `run.googleapis.com/invoker-iam-disabled` annotation in shown service metadata, the approved deployment explicitly used `--invoker-iam-check --no-allow-unauthenticated`, and Google docs state Invoker IAM check **enforced by default**. This supports required IAM/private check, but is not a token-based effective runtime probe and **does not eliminate inherited project/org IAM** (previous 2 Owner,1 Editor accepted nonexclusive). See https://docs.cloud.google.com/run/docs/authenticating/public.
- No minScale annotation shown; Google defaults minimum instances to 0 when not set, consistent with approved min0. See https://docs.cloud.google.com/run/docs/configuring/min-instances. Not a cloud cost hard cap. Current resource max1 effective based on revision only.
- Source previously OFF-only HTTP health 200/API 503 locally; **HOSTED 200/503, 401/403 and effective token invocation are NOT tested**. Existing gateway 12 distinct HIGH CVEs are unresolved, with owner limited private default-OFF risk consent; derived image `slsa_build_level=unknown` and no separate derived signature/attestation, only signed base parent. Production NO-GO.

**CONCLUSION:** `C1A_B1_SA_CREATE_AND_READBACK=PASS`; `C1A_B2_ONE_PUSH_REMOTE_DIGEST_READBACK=PASS`; `C1A_B3_ONE_PRIVATE_GATEWAY_DEPLOY=PASS`; `C1A_B3_POSTWRITE_CONFIG=PASS`; `C1A_DIRECT_IAM_NO_PUBLIC_BINDINGS=PASS`; `C1A=PASS_WITH_LIMITS` for **NEW private default-OFF service infrastructure only**. **No repeat B1/B2/B3, old 84 tests, Docker build/Syft/Grype, publisher Cosign, old Cloud inventory or current postwrite metadata readback.**

**Next decision:** separate, not yet granted **C1B** owner approval for a tightly bounded PRIVATE hosted OFF-only 20-minute test, max SIX HTTP calls TOTAL (authenticated GET `/healthz`, authenticated POST one `/api/staging/marketplace/owner` 503, one unauthenticated probe expecting 401/403; additional only if specifically justified), no retries, no Firebase/Firestore/Cloud KMS/backend/token printing, no project IAM change, no current old service traffic changes. Must check actual identity invocation without public binding; if unexpected response STOP. After C1B, separately guarded cleanup of ONLY new service UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`, B1 SA unique ID `102194769236111252832`, B2 image exact remote digest may be considered under earlier approved new-only cleanup, not automatic. Original <=24h supervision expected by ~25 Nov 2026 23:19 IST, but NO automated cleanup scheduled and deletion does not happen unless explicitly run; no overall hard INR cap per owner.


## 24 Nov 2026 — OWNER EXPRESSLY APPROVES ONLY C1B BOUNDED OFF-ONLY HOSTED HTTP (NOT YET EXECUTED)

**Actual user reply "ha manjuri chhe"** immediately following explicit request to approve one C1B private-hosted test restricted to:
- **At most SIX total HTTP requests within ONE 20-minute supervised window** to only NEW `https://oldx-step05-gateway-38472235077.asia-south1.run.app` service. To save time prefer only THREE (one unauthorized GET `/healthz` expected 401/403, one authorized Owner GET `/healthz` expected 200, one authorized POST `/api/staging/marketplace/owner` expected 503).
- Use existing interactive Yasmin project Owner identity and freshly minted short-lived `gcloud auth print-identity-token` passed via stdin to existing WSL curl; do NOT print or store token, create credentials/service account keys, change IAM/roles, install tools, use Cloud Run proxy or invoke other services.
- No automatic retries; strict fail-stop on unexpected response/timeout or lack of token. No credentials or data/nonce/media sent. No Firebase/Firestore/Auth/KMS/old Product-backend calls or other cloud resource writes. No Product activation, C2/production launch.
- The existing Cloud Run Gateway has already been proved C1A `PASS_WITH_LIMITS` by source, digest, service config and no direct service public IAM bindings. C1B actual hosted outcomes **remain unknown until owner executes**. C1B approval does NOT extend 12 HIGH CVE limited risk into production or approve using this gateway for buyer traffic.

**Status after consent:** `C1B_OWNER_CONSENT=APPROVED_MAX_6_HTTP_20_MIN`; `C1B_HTTP_REQUESTS_ACTUALLY_SENT=0_OBSERVED`; `C1B_HOSTED_AUTH_200_API_503_ANON_401_403=NOT_YET_VERIFIED`; `B1/B2/B3_CLOUD_WRITES=ALREADY_COMPLETED_DO_NOT_REPEAT`; `C2/PRODUCTION=NO_GO`. A single new source-only fail-closed one-shot WSL probe script may be prepared/committed and run only once from the already cloned owner checkout; no need for old tests, old build/scan, Cosign or cloud re-audit.


## 24 Nov 2026 — C1B owner approval recorded; 3-request one-shot script SAVED (NOT EXECUTED)

Owner explicitly said `ha manjuri chhe` to the earlier C1B proposal: at most SIX PRIVATE hosted OFF-only requests within 20 minutes; no retries; IAM, Firebase, old backend, Product activation, C2/production unchanged. **This is a distinct authorization from C1A Stage B and does not authorize new resource writes or a public launch.**

**Source-only script:** [`scripts/step05-c1b-private-off-http-once-20261124.sh`](../scripts/step05-c1b-private-off-http-once-20261124.sh) (`git blob 5ae169af7be95d9fbe686475c680e99b6f33aa16` at creation). It checks the stable existing branch and immutable OFF server blob `25d2679bd4ea970c8b8a32a778fb26eb347bcdd6`, requires a token passed by stdin, never prints/saves the token, creates a one-attempt marker **before** the first HTTP call, requires HTTPS/TLS, disables redirects and retries, sets max 20s per request and 20-minute overall window. Sends only these THREE calls to the known NEW Gateway URL: anonymous GET `/healthz` expect 401 or 403; Owner-authenticated GET `/healthz` expect 200; Owner-authenticated POST `/api/staging/marketplace/owner` body `{}` expect 503. It stops immediately on any unexpected code/timeout. Remaining authorized 3 calls are intentionally **unused**, not automatic backup or retry. Logs only numbered request statuses, no token, response body or credentials to `$HOME/oldx-step05-c1b-off-hosted-result-20261124.txt`. **Not run at GitHub source creation; no live hosted result exists yet.**

**Fastest two CMD steps using already cloned WSL repo** (first only updates small source and syntax checks; second actually sends bounded hosted HTTP):

```cmd
wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && git pull --ff-only && bash -n scripts/step05-c1b-private-off-http-once-20261124.sh"
gcloud auth print-identity-token | wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && bash scripts/step05-c1b-private-off-http-once-20261124.sh"
```

If first fails, DO NOT run the second. Second command requires installed existing Windows gcloud with correct Owner account and WSL curl, uses Google-recommended short-lived developer user identity token for Cloud Run (https://docs.cloud.google.com/run/docs/authenticating/developers). No `gcloud auth login`, IAM token creator grants, service-account impersonation or IAM change. **Do not repeat the second command even on error**, because the one-shot marker may already have been created; read only saved report and screenshot. No attempts to invoke other services, no old tests, no deployment.

**Status:** `C1B_OWNER_CONSENT=YES`; `C1B_SCRIPT=PREPARED_NOT_RUN`; `C1B_HOSTED_HTTP_RESULT=UNKNOWN`; `C1A=PASS_WITH_LIMITS_CONSUMED`; `C2=HOLD`; `PRODUCTION=NO_GO`; `NEW_ONLY_CLEANUP=SEPARATELY_PREVIOUSLY_APPROVED_EXACT_UID_GUARDED_NOT_AUTOMATIC`.


**24 Nov 2026 C1B no-repeat tool detail:** WSL script was minimally improved SOURCE-ONLY for Windows CMD `gcloud.cmd` CRLF stdout: strip exactly one trailing `\\r` from in-memory ephemeral ID token before JWT validation; does not log/store it or alter the HTTP scope. Final reviewed script Git blob **`6fdb001c5bd20b20a40f13d6d687cf2d01b1f27d`**; replaces the initial blob `5ae169af...`. Final command remains unchanged, **C1B HTTP NOT EXECUTED**. No previous tests rerun.


## 24 Nov 2026 ~23:31 IST — C1B OWNER COMMAND STOPPED BY MALFORMED SCRIPT; NO RETRY; local marker/readback FIRST

**Actual owner CMD screenshot:** `git pull --ff-only` fast-forward to `eb5ca77` and `bash -n scripts/step05-c1b-private-off-http-once-20261124.sh` completed without visible syntax error. The one C1B `gcloud auth print-identity-token | wsl ... bash ...` invocation immediately reported **`scripts/step05-c1b-private-off-http-once-20261124.sh: line 57: $1: unbound variable`** and returned to CMD. Screenshot contains **NO** anonymous401/403/auth200/api503 or request count PASS. **Do not infer Cloud Run hosted failure or any successful HTTP response, and DO NOT automatically repeat the C1B command.** Sensitive ID token was piped, not printed.

**Source root cause established by direct GitHub file inspection:** the initial CRLF-handling source update corrupted the Bash parameter expansion at original line31 and included a duplicate tail at original line95-159, which a basic `bash -n` did not detect as an execution-time failure. Source-only repair saved in `scripts/step05-c1b-private-off-http-once-20261124.sh` at **Git blob `8e5f684f218be026ebd5506c2a76bee9d7eb2a92`, commit `689bb27225921e4d4aecab591d2e09c771e66505`**: correct single `OWNER_ID_TOKEN="${OWNER_ID_TOKEN%$'\\r'}"` trim, remove duplicate tail, preserve exactly three ordered HTTP requests, no credential logging, fail-closed when either original one-attempt marker OR prior report exists. This fixes source only; does NOT itself authorize blindly rerunning previous C1B request or establish no HTTP was sent.

**NEXT and ONLY NEXT owner CMD action, READ-ONLY local evidence (NO gcloud/token/HTTP):**
```cmd
wsl -d OLDX-Ubuntu-24.04 -- bash -lc "if [ -e /root/.oldx-step05-c1b-off-hosted-once-20261124 ]; then echo C1B_MARKER=PRESENT; else echo C1B_MARKER=ABSENT; fi; if [ -e /root/oldx-step05-c1b-off-hosted-result-20261124.txt ]; then echo C1B_REPORT=PRESENT; grep -E '^(STATUS|HTTP_ATTEMPT_|HTTP_[0-9]+_CODE|HTTP_REQUESTS_SENT|APPROVED_MAX_HTTP)' /root/oldx-step05-c1b-off-hosted-result-20261124.txt || true; else echo C1B_REPORT=ABSENT; fi"
```
If marker/report PRESENT, do NOT rerun; review exact status/counted requests and 20-minute/6-call boundary first. If both ABSENT, no marker/report recorded by script, strongly suggests original failed before guarded HTTP section, but still review actual source flow/time constraints before new owner token. **Do NOT** run C1A B1/B2/B3 cloud changes, old tests, Docker build/Grype/Cosign or deploy; no IAM/Firebase/production changes. `C1A=PASS_WITH_LIMITS`; `C1B_HTTP=ERROR_UNKNOWN_REQUEST_COUNT_PENDING_MARKER_REPORT`; `C2/PRODUCTION=NO_GO`.


## 24 Nov 2026 ~23:35 IST — OWNER C1B ONE-SHOT MARKER/REPORT READBACK **BOTH ABSENT**, previous shell failure BEFORE HTTP

Latest owner screenshot from existing WSL running the specifically requested **READ-ONLY** marker/report probe returned **`C1B_MARKER=ABSENT`** and **`C1B_REPORT=ABSENT`**. Prior faulty C1B script enters its marker/write-report block only after the corrupted line31 parameter expansion; documented prior `line 57: $1: unbound variable` therefore failed **before** the original file's first HTTP block and before the one-shot marker. The screenshot shows no 401/403, 200 or 503. Together with the original GitHub source flow, this strongly establishes `C1B_PREVIOUS_HOSTED_REQUEST_COUNT=0` for that script invocation; it is **NOT a server-side request log audit**, so do not claim universal absence of all possible external HTTP traffic. The owner-approved maximum six C1B calls remain unused, and the prior shell failure did not count as an HTTP retry.

Final corrected script currently confirmed from GitHub blob `8e5f684f218be026ebd5506c2a76bee9d7eb2a92` with exactly ONE valid `OWNER_ID_TOKEN="${OWNER_ID_TOKEN%$'\\r'}"` line, no duplicate script tail, only 3 ordered calls, no tokens printed/saved, proper fail-closed if `SCRIPT_LOCK` or `OUT` exists. **This corrected code has NOT yet been executed**. A SINGLE owner-consented FIRST hosted test is now available; no second run after marker creation or an unexpected response.

**NEXT two existing Windows CMD commands (not a repeat of the faulty old code):**

```cmd
wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && git pull --ff-only && bash -n scripts/step05-c1b-private-off-http-once-20261124.sh"
gcloud auth print-identity-token | wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && bash scripts/step05-c1b-private-off-http-once-20261124.sh"
```

Run the SECOND only if the FIRST succeeded; do not print/store the identity token; allow one 20-minute test window, no HTTP retries. If any failure STOP and report result/marker, do not re-run script or change IAM/Firebase/Cloud Run. Expected statuses: anonymous GET /healthz -> 401 or 403, Owner ID-token GET /healthz -> 200, Owner ID-token POST /api/staging/marketplace/owner -> 503. New service only. C1A already PASS_WITH_LIMITS, three Cloud writes/IAM config consumed. `C1B_ATTEMPT_1=FAILED_BEFORE_HTTP`; `C1B_ACTUAL_HOSTED_STATUS=PENDING_NEW_CORRECTED_ONE_SHOT`; `C2/PRODUCTION=NO_GO`.


## 24 Nov 2026 ~23:38 IST — C1B ONE ANONYMOUS HTTP RESULT UNEXPECTED, SAFE STOP; EXACT CODE MUST BE READ LOCALLY

**Latest owner screenshot:** Git pull fetched the repaired (then-current) C1B script; next one-time `gcloud auth print-identity-token | wsl ... bash scripts/step05-c1b-private-off-http-once-20261124.sh` exited **`line 56: code_NO_FURTHER_REQUESTS: unbound variable`**. Unlike the previous failed attempt (no marker/report), direct inspection of the exact original git blob `8e5f684f218be026ebd5506c2a76bee9d7eb2a92` confirms this time execution progressed THROUGH the FIRST anonymous `GET /healthz`: `curl` exited successfully, `HTTP_ATTEMPT_1=ANONYMOUS_GET_HEALTHZ` and **`HTTP_1_CODE=<actual code>`** were appended to the local report, then the script entered `if code !=401 && code !=403` and aborted on Bash nounset while expanding the wrongly concatenated `$code_NO_FURTHER_REQUESTS`. Therefore **exactly ONE HTTP request from this second run is evidenced**; it produced an unexpected status other than 401/403, but the numeric status remains **UNKNOWN** pending local report. Owner GET200 and POST503 were NOT attempted. **DO NOT classify C1B as PASS; potential anonymous access issue must be triaged.**
  
**Source-only error-reporting fix** saved at commit `15cec40c90d50b6322f89b30704f81fa3b391e89` (script blob `052cbad75188dfd3ac88e6a455e019fcde6d31b4`): changed strings to `${code}` and `${label}_EXPECTED_${expected}_GOT_${code}` so unexpected HTTP errors can be printed without unbound-variable shell abort. **This patch does NOT authorize new hosted requests or change the result of the already-sent request.** Original one-attempt marker now SHOULD exist; do NOT delete it, edit report, re-run script, `gcloud auth print-identity-token` or Cloud Run deploy.

**NEXT only, one local read-only CMD query of original marker/status report (NO token, HTTP, Google Cloud mutation):**

```cmd
wsl -d OLDX-Ubuntu-24.04 -- bash -lc "if [ -e /root/.oldx-step05-c1b-off-hosted-once-20261124 ]; then echo C1B_MARKER=PRESENT; else echo C1B_MARKER=ABSENT; fi; if [ -f /root/oldx-step05-c1b-off-hosted-result-20261124.txt ]; then grep -E '^(STATUS|HTTP_ATTEMPT_[0-9]+|HTTP_[0-9]+_CODE|HTTP_REQUESTS_SENT)' /root/oldx-step05-c1b-off-hosted-result-20261124.txt; else echo C1B_REPORT=ABSENT; fi"
```

Do not request a repeat HTTP even if the returned code is unexpected; first determine whether it was 200/public bypass, 404/not-found, 3xx/redirect or an auth/proxy-related error. Corrective decisions and any extra HTTP requests require a narrowly reviewed security path and remaining 20-minute original window (possibly expired), not blanket "retry". Cloud Run direct IAM showed no public bindings but private access behavior remains UNVERIFIED and this anonymous response is potentially material. All C1A prior B1/B2/B3, signed-base checks, scans/tests already consumed and must NOT be repeated. `C1B=STOP_UNEXPECTED_ANON_STATUS`, `C1B_HTTP_SENT=1`, `C1B_OWNER_AUTH_CALLS_SENT=0`, `PRODUCTION/C2=NO_GO`.


## 24 Nov 2026 ~23:41-23:44 IST — C1B anonymous `/healthz` HTTP **404** actual evidence; official Cloud Run reserved-path cause identified; bounded **/health** continuation prepared NOT EXECUTED

Owner CMD screenshot of exact local-only original one-shot marker/report read returned:
```text
C1B_MARKER=PRESENT
STATUS=STARTED
HTTP_ATTEMPT_1=ANONYMOUS_GET_HEALTHZ
HTTP_1_CODE=404
```
Exactly **ONE** C1B HTTP request was sent, returned **404**, **NOT** 200, and no Owner GET/POST attempt is logged. The shell script stopped on source `$code_NO_FURTHER_REQUESTS` nounset formatting bug after writing the observed 404; that formatting was fixed SOURCE ONLY (the original one-shot MUST NEVER be repeated). Do NOT claim successful anonymous application access or 401/403 rejection. `C1B=HOLD_PARTIAL` until valid-path private enforcement is shown.

**Newly discovered MATERIAL official Google evidence:** Google [Cloud Run Known Issues — Reserved URL paths](https://docs.cloud.google.com/run/docs/known-issues) (updated 18 Nov 2026) explicitly states `/_ah/` paths and **some paths ending in `z`** are reserved; it recommends avoiding all paths ending in `z`. Thus `/healthz` is an unsuitable discriminator for Cloud Run IAM behaviour, and Google frontend returning 404 *before* reaching the application is a credible explanation; not independently proven for this exact request by server-side logs. The already-built immutable OFF-only server at repo Git blob `25d2679bd4ea970c8b8a32a778fb26eb347bcdd6` supports both `GET /healthz` and **`GET /health`** returning 200 locally. The latter does NOT end in z, so a one-time `/health` test needs **NO Docker rebuild, Registry push, Cloud Run deployment, IAM change, API enablement or source edit**.

**Source-only NEW safe continuation:** [`scripts/step05-c1b-health-reserved-path-continuation-20261124.sh`](../scripts/step05-c1b-health-reserved-path-continuation-20261124.sh), final Git blob `91385ba0a49778042f6de03672d5a816295d7f9e`. It requires ORIGINAL marker/report present and EXACT `HTTP_1_CODE=404`, precisely 1 prior anonymous request, no prior subsequent requests; enforces original first-attempt marker's <=20 minute clock (does not reset approved 20m horizon), exactly 3 ADDITIONAL HTTP calls (#2 anonymous GET `/health` expected 401/403; #3 Owner GET `/health` expected 200; #4 Owner POST `/api/staging/marketplace/owner` expected 503), overall **4 of max6**, no redirects/retries and strict fail-stop. New one-shot marker placed BEFORE HTTP, token from Windows `gcloud auth print-identity-token` piped via WSL stdin and never printed or saved, same approved Owner-only identity. Its own report uses `$HOME/oldx-step05-c1b-health-continuation-result-20261124.txt`. Do not delete previous report or original marker. **Creation of script in GitHub is not execution; NO new HTTP sent by assistant.**

**NEXT owner Windows CMD (ONLY if within original 20min window, otherwise script STOPs):**
```cmd
wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && git pull --ff-only && bash -n scripts/step05-c1b-health-reserved-path-continuation-20261124.sh"
gcloud auth print-identity-token | wsl -d OLDX-Ubuntu-24.04 -- bash -lc "cd ~/oldx-c1a-proof-stable-20261124 && bash scripts/step05-c1b-health-reserved-path-continuation-20261124.sh"
```
Run second only if first succeeded; second one use ONLY and do NOT retry on any STOP including time expiry, any anonymous response other than 401/403, permission error, or token transport problem. If original 20-minute window already expired, request fresh narrowly scoped owner authorization rather than resetting or reusing the old marker. No C1A B1/B2/B3 rework, old 84 tests, image scan/signature, Firebase/KMS/old backend change. No C2 or production GO. Cleanup of exact new resource identities before previously planned supervised deadline remains separate and not scheduled automatically.

**Current actual:** `C1A=PASS_WITH_LIMITS`; `C1B_OLD_ANON_HEALTHZ=404`; `C1B_HTTP_TOTAL_OBSERVED=1`; `C1B_HEALTH_CONTINUATION=PREPARED_NOT_RUN`; `C2/PRODUCTION=NO_GO`.


## 24 Nov 2026 ~23:47 IST — ACTUAL C1B HOSTED PRIVATE/OFF END-TO-END PASS_WITH_LIMITS (OWNER CMD SCREENSHOT); CONSUMED — DO NOT REPEAT

**Owner's latest Windows CMD screenshot** of the single previously approved `scripts/step05-c1b-health-reserved-path-continuation-20261124.sh` run shows:
```text
ANON_GET_HEALTH=403 PASS
OWNER_GET_HEALTH=200 PASS
OWNER_POST_API_OFF=503 PASS
C1B_CONTINUATION=PASS_WITH_LIMITS
HTTP_TOTAL=4/6
NO_CLOUD_WRITE=TRUE
REPORT=/root/oldx-step05-c1b-health-continuation-result-20261124.txt
```
The prior preserved original first one-shot report had `HTTP_1_CODE=404` from anonymous `GET /healthz`; official Cloud Run docs note paths ending `z` can be reserved. This makes **four HTTP requests in total**, not five: #1 anon /healthz 404, #2 anon /health 403, #3 authenticated Owner GET /health 200, #4 authenticated Owner POST /api/staging/marketplace/owner 503. Owner-approved max six in original 20min period was not exceeded. **This is the first actual hosted validation of IAM rejection + authorized health success + default-OFF Product API enforcement**. The token stayed piped over stdin; screenshot does not expose it. No Cloud Run resource write is reported by the test, no old service/Firestore/Auth/KMS/Product enablement command.

**Interpretation:** private Cloud Run Invoker IAM is enforced for the tested anonymous endpoint (403) while authenticated Owner access reaches OFF Gateway (200/503). Separate C1A infrastructure B1 SA uniqueId `102194769236111252832`, B2 immutable Registry remote `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a` and B3 private new Cloud Run service UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`, revision `oldx-step05-gateway-00001-thd`, resource/IAM metadata all previously PASS_WITH_LIMITS. **Classification: `C1A=PASS_WITH_LIMITS`; `C1B=PASS_WITH_LIMITS`; `C1B_HTTP_COUNT=4/6`; `C1B_PRIVATE_OFF_GUARD=PASS_FOR_TESTED_PATHS`.** This is NOT blanket endpoint pen-test, not a derived image SLSA attestation, not a fix for 12 new Gateway HIGH CVEs, and **NOT C2/production authorization**. Existing Product Cloud Run root/A8 traffic/IAM was not re-read now and is not claimed proven unchanged by screenshot (no command touched it).

**CRITICAL no-repeat:** Both original C1B one-shot marker/report and continuation one-shot marker/report are consumed. **DO NOT re-run** `gcloud auth print-identity-token` with either C1B script; no more HTTP tests unless a separate later scoped decision requires them. Do NOT rebuild Docker/re-scan Syft/Grype/reverify parent Cosign, recreate SA, push Registry, redeploy Cloud Run, redo original 84 cases or prior IAM audit. Owner requests rapid work/no repeated cost forms/no rupee hard cap, while controlling waste with min0/effective max1 and no new services. Existing C1A/C1B evidence is sufficient for a bounded private-OFF endpoint validation.

**NEXT:** Step05 C1B complete; prepare C2 risk/decision scope from existing plan/source WITHOUT activation. C2 will need distinct approval for enabled Product/backend/data access and separate security risk disposition—none granted. NEW-only cleanup of private supervised C1A test resources was previously consented only with exact UID+digest+no-dependency safety checks; this is **not automatic**. Original approx <=24h supervised stage trial from 24 Nov ~23:19 IST implies owner should decide retention or guarded cleanup by **25 Nov ~23:19 IST**. Do not delete `oldx-owner-read`, existing Registry repository, other images or SAs. `C2/PRODUCTION=NO_GO`.
