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
