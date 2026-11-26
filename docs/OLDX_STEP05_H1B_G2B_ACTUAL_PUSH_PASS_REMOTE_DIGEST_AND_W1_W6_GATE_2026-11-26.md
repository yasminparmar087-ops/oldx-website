# OLDX Step05 H1B — G2B ACTUAL OWNER PUSH PASS; frozen Registry digest; next NEW-only W1–W6 gate

**26 Nov 2026 ~21:40 IST.** Owner WSL screenshot supplied to current conversation. Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. This document transcribes the screenshot and compares it with prior retained source/receipts; assistant did **not** execute owner WSL, image upload, Cloud Run, IAM or hosted probes.

## 1. Actual G2B screenshot: PASS, one Registry write succeeded

Pinned owner-executed script from immutable commit `02435f6d30617287d6d73e04dbb9e839101360ce`: `scripts/step05_h1b_g2b_retained_image_single_push_verify_once_20261126.py`, verified Git blob `03f0af269b7b7e2ecfa2c2ac27c43636890cd2f8`.

```text
H1B_G2B_STAGE=ONE_AUTHORIZED_PUSH_ATTEMPT
H1B_G2B_REMOTE_DIGEST=sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e
H1B_G2B_REMOTE_AMD64_CHILD=sha256:2e555bd98424d29b32a7bb3409a45e2c257569ff632085e4ff0e3a9ab4413b5f
H1B_G2B_REMOTE_CONFIG=sha256:c71c7268e08f9ed91a92fd4e82e499a7331c3a071985cebcede7d76efbdf5b71
H1B_G2B_TAG=h1b-g2b-20261126-dc07d8c3bd01d5310ae1
H1B_G2B_PUSH_ATTEMPTED=TRUE
H1B_G2B_RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED
H1B_G2B_REASON=ONE_PUSH_VERIFIED
H1B_G2B_CLOUD_RUN_OR_IAM_WRITES=NONE
H1B_G2B_DO_NOT_REPEAT=TRUE
```

**Verified image locator by immutable actual remote index digest:**

```text
asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e
```

Tag evidence (not intended to be used as mutable deploy selector):
```text
asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off:h1b-g2b-20261126-dc07d8c3bd01d5310ae1
```

This screenshot's actual remote index digest happens to equal the previously frozen local Docker image/index ID `sha256:576a...`; **do not assume such equality in any unrelated image**. Raw remote manifest data and selected linux/amd64 child/config matched the frozen source under the G2B script's validation. This is not a second independent Cloud API query from the assistant and not a security re-scan of the remote registry image.

**Actual Registry write:** ONE `docker push` succeeded to a **new uniquely named tag** in the existing shared Artifact Registry. `H1B_G2B_CLOUD_RUN_OR_IAM_WRITES=NONE` means **no Cloud Run/IAM writes**, not `NO_CLOUD_WRITES`: the Registry push was a real storage write and may incur storage/egress charges.

One-shot marker `/root/.oldx-h1b-g2b-retained-single-push-once-20261126` is now **CONSUMED**; private evidence directory saved on Owner WSL by script. Do not rerun it, clear any consumed marker, rebuild/re-scan/push, or copy OAuth/credential logs to GitHub. Retain current image and pin this exact digest. G1 read-only, G2A recovery, G2B push, prior H1A image/SBOM/Grype/offline runtime, native SDK S1/S2 and S3/S3B must NOT repeat.

## 2. Fastest remaining Step05 H1B route — distinct, finite owner operational approval REQUIRED

The prior approval only covered supervised Owner WSL OAuth + **one image push and digest readback**, now completed. The earlier Option B known **12 HIGH** risk acceptance was limited to a compiled-OFF, private, no-real-data, max-24h experimental candidate; it was not an unconditional deployment approval. The following **NEW** operations remain **NOT EXECUTED / NOT YET AUTHORIZED**:

| Stage | Proposed narrowly scoped NEW action | Stop and proof boundary |
| --- | --- | --- |
| Pre-W1 | One focused live preflight for named operator, project `oldx-staging`, region `asia-south1`, **current** new mediator service and SA noncollision, exact immutable image digest readability, resource-level rights incl. future `actAs`, Cloud Run Invoker/access, and ability to perform guarded NEW-only cleanup | Historical G1/S3B not rerun; current names/resources must be checked immediately before writes; 403/unknown is not absence |
| W1 | Create **one** no-key NEW runtime SA `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` | Freeze uniqueId and current effective permissions. No Firebase/Firestore/Auth/KMS/media role, no old SA changes |
| W2 | **Already completed G2B image push**; use this image **by exact immutable remote digest** only | No second Docker push, tag mutation or old C1A image reuse |
| W3 | Deploy **one** NEW private compiled-OFF Cloud Run service `oldx-c2-website-mediator` on `oldx-staging/asia-south1`; new SA runtime; 1 vCPU/512 MiB, min0/max1, concurrency1, timeout 5s, port 8080, nonroot, IAM Invoker check ON | Explicit no unauthenticated/public Invoker, no Product route to real users, no real data or provider credentials, record service UID/revision/IAM/port/image |
| W4 | Only if necessary: one **exact new-service-only** `roles/run.invoker` binding for Yasmin Owner principal to run permitted private probes | No `allUsers`, `allAuthenticatedUsers`, project-wide or old-service Invoker change |
| W5 | At most four exact supervised **new H1B-only** HTTP probes: anonymous `GET /health` expected 403; Owner-authenticated `GET /health` 200; authenticated `POST /api/staging/marketplace/owner` 503; authenticated wrong path 404 | No real/synthetic Firebase users, Firestore, KMS, media, old C1A probe or retry; unexpected status STOP |
| W6 | Same-session rollback and guarded NEW-only cleanup: exact new Cloud Run service; new Registry image/tag only if unreferenced; new SA only if unused and matching uniqueId | If any identity/dependency mismatch, STOP_MANUAL_RECOVERY and document residuals; never delete shared Registry, old owner-read, old C1A SA/image or other services |

**Owner consent needed before any W1/W3/W4/W5/W6 write/probe.** Prefer one short supervised session and same-session guarded cleanup; 24h from any actual new staging activation is **upper bound**, not an obligation to leave resources running. Stop if safe cleanup unavailable. Real metered staging costs are possible. Owner waived a previous hard spending cap but did not approve unlimited unrelated changes. H2/production, Firebase Rules, real data, H1B service activation for public users, and C1A residual SA/image deletion remain NO-GO.

## 3. Precise next approval request (single combined packet for speed)

Owner can explicitly authorize this **one bounded H1B staging-only W1/W3/W4/W5/W6 supervised experiment** with the exact identity, one no-key SA, one new OFF-only private Cloud Run service, optional exact Owner-only service Invoker, <=4 new-service-only probes, same-session NEW-only guarded cleanup and stop/rollback boundaries listed above. The W2 image is **already pushed** and is read-only from now on. Until consent, prepare source/commands and validate local logic only; NO Cloud Run/IAM creation or hosted probes. Once consent arrives, construct the new-only guarded execution scripts with pinned hashes and no-repeat one-shot markers; verify cleanup path before running W1.

## 4. Protected/unchanged state

- Old `oldx-step05-gateway` C1A **Cloud Run service already CONFIRMED_REMOVED**, never delete it again. Residual C1A SA exact UID `102194769236111252832` and earlier old C1A pinned image `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a` still remain; other references unknown. RETAIN, never delete without separate complete scoped evidence/consent.
- Old `oldx-owner-read`, default-deny Firebase Rules, actual Firebase data, IAM roles and production unchanged by this G2B operation.
- `STEP05=IN_PROGRESS`, `H1B_IMAGE_REMOTE_DIGEST=ACTUAL_VERIFIED`, `H1B_W1_W6=NOT_EXECUTED`, `PRODUCTION=NO_GO`.

Sources in repository: [latest previous G2B prepared handoff](OLDX_STEP05_H1B_G2A_RECOVERY_PASS_G2B_ONE_PUSH_OWNER_HANDOFF_2026-11-26.md), [H1B G0–G6 scope](OLDX_STEP05_H1B_FASTPATH_FINAL_OPERATION_AND_C1A_DECISION_2026-11-26.md), [W1–W6 historical packet](OLDX_STEP05_H1B_PRIVATE_OFF_ONE_SHOT_PREFLIGHT_AND_OPERATION_PACKET_2026-11-25.md). The present screenshot supersedes those documents' outdated `NO_REMOTE_DIGEST` status but does not change any other historical evidence.
