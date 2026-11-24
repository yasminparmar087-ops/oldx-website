# OLDX Step 05 H1B — single preflight and private OFF-only deployment operational packet

## 25 Nov 2026 — actual one-shot H1B read-only preflight STOP: operator lookup timed out; targets NOT queried

Starting remote HEAD `7358fbc3da718a88e84b2ab31aebe9330bcd4f6b`. Latest AGENTS, this packet and Issue17 latest7143376032 read first. Script `scripts/step05-h1b-readonly-preflight-20261125.sh` Git blob **`14703d1257c99701e4873be598b5aedc0d5c33b4`** matched exact isolated local bytes. Local dirty Handoff and untracked.firebaserc preserved, no reset/force/pull. No source script change.

Owner-local `OLDX-Ubuntu-24.04`: separate marker `/root/.oldx-h1b-readonly-preflight-once-20261125` independently ABSENT before run; `bash -n <isolated>/scripts/step05-h1b-readonly-preflight-20261125.sh` **PASS exit0**, no Cloud request. Then exactly ONE invocation:
`bash scripts/step05-h1b-readonly-preflight-20261125.sh --read-only-once`.
The first bounded command, `timeout 40s gcloud auth list --filter=status:ACTIVE --format=value(account)`, saved **exit124 (timeout)** with **stdout0B/stderr0B**. Script reported `STOP: cannot read active gcloud operator; no other lookup attempted`; outer WSL process exit1 observed. No retry, login/token creation, SDK install, account switch or permission change. The cause of the silent timeout is UNVERIFIED; not proof of expired credentials, missing access, network failure or missing resources.

| Requested check | Actual result |
| --- | --- |
| Active Google Cloud operator | **UNVERIFIED — first lookup timed out**, no identity printed |
| Project oldx-staging / expected38472235077 | **NOT QUERIED**; expected values remain proposal/config, not fresh proof |
| Existing asia-south1 oldx-staging-images Registry | **NOT QUERIED** |
| NEW service oldx-c2-website-mediator collision | **UNKNOWN — NOT QUERIED** |
| NEW SA oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com collision | **UNKNOWN — NOT QUERIED** |
| Effective inherited IAM, push/create/cleanup rights, cost | **UNVERIFIED**, outside successful evidence |

No403/404 response was obtained and **no collision-free/nonexistence claim** is made. Marker now PRESENT/CONSUMED; never delete or rerun script. Only first active-operator gcloud command attempted; no project/Registry/Cloud Run/SA describe commands executed, no hosted endpoint request.

### Private evidence custody
Directory `/root/oldx-h1b-readonly-preflight-20261124T202258Z` (25Nov2026 ~01:52:58IST start), umask077/private:
- `SHA256SUMS` SHA256 **`22b2f89ffc7c70be6ad82398e64d8c42170c646669d5399ae4c44622d96d5b1e`**.
- `active-operator.command` SHA256 `3624b2dd5a2803e238c36e7a26cfaded66d4263605f51a849980b508ea74492a`.
- `active-operator.exit` SHA256 `ca2ebdf97d7469496b1f4b78958f9dc8447efdcb623953fee7b6996b762f6fff`.
- stdout/stderr both empty, SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Marker retains exact evidence location. Full private evidence/operator output not uploaded, only nonsensitive timeout/status/checksum summary. No images built/scanned/pushed, service/SA/IAM/Firebase/Billing/traffic/deployment/credentials changed. Existing H1A retained image/scans/tests and C1A untouched.

**H1B_READONLY_PREFLIGHT=STOP_OPERATOR_TIMEOUT; H1B_WRITES=NOT_AUTHORIZED; H2=HOLD; PRODUCTION=NO_GO.** OptionB acceptance remains ONLY the exact known candidate's private/OFF/no-data risk for max24h from future actual activation; no activation/start/end clock here, no operational authority. Existing C1A retention deadline28Nov2026 23:19IST unchanged.

**ONE next owner approval required:** one narrowly scoped **read-only diagnosis of the timed-out local WSL gcloud startup/operator lookup**, without repeating consumed preflight, changing credentials/IAM or making resource writes. Do not seek/execute W1–W6 on unverified operator/collisions. Actual target checks need later individually bounded continuation only after the cause is understood; no automatic retry, new marker or longer timeout here. Existing future W1–W6 packet stays PROPOSED/NOT_AUTHORIZED and is not executable on this failed preflight.
Final pushed/read-back SHA is in Issue17 checkpoint and containing documentation commit.


**25 November 2026 IST. SOURCE-ONLY document, NOT operational approval.** Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. The owner chose **Option B**: accepts precisely the twelve known HIGH CVEs and explicitly disclosed unsigned/uncertified *derived publisher* provenance risk **ONLY** for one **future**, strictly IAM-private, compiled-OFF, no-real-user-data H1B mediator staging experiment of **up to 24 hours from activation**. Actual Cloud creation, image push, IAM write, metered resource activation, hosted HTTP and cleanup have **not** been authorized by that risk decision or the subsequent generic “ok aagal vadho”; this packet prepares them. Existing C1A has a **separate** retention deadline, **28 Nov 2026 23:19 IST**.

## 1. Frozen evidence; no repeat

- **H1A already consumed:** one owner-WSL linux/amd64 image build, one Syft inventory **15 packages**, one Grype scan **55 matches, 12 distinct HIGH IDs, 0 CRITICAL**, one local secure runtime smoke PASS and SIGTERM exit0 at 0.507s. Image and reports remain locally; never rebuild, rescan, reset or remove consumed `/root/.oldx-h1a-c2-mediator-once-20261125`. Existing C1A/Step04 scans/probes also consumed.
- Local image tag `oldx-h1a-c2-mediator-off:local-20261124t195244z`. Local Docker image/index ID `sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`; BuildKit child manifest `sha256:2e555bd98424d29b32a7bb3409a45e2c257569ff632085e4ff0e3a9ab4413b5f`; config `sha256:c71c7268e08f9ed91a92fd4e82e499a7331c3a071985cebcede7d76efbdf5b71`. **None is to be assumed equal to the future *pushed registry* digest.**
- Approved immutable base `sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec`. H1A BuildKit accepted it, prior standalone Docker manifest-client discrepancy remains unexplained. Do not substitute base, skip integrity checks, or reuse C1A image.
- Local private evidence `/root/oldx-h1a-evidence-20261124T195244Z`; `receipt.json` SHA256 `9be77e292585d30aa859c50cf1bc5112c631c615c89697e4928604171283a560`; SBOM `09159b10490fe3ba072c0f53dadc49c428e8a4c1e0a940de1d939a8c4a2c235a`; Grype `2fbfc099009a6e1153f438e77f9724dff5e81884ba326953ae1a5fa2cdc0680a`. Only hashes and summarized findings go into GitHub; full private reports remain local.
- Owner accepted the listed 12 HIGH for **private/OFF/no-data**, not any new CVE, image mismatch, production use or G2–G5 enablement. [Exact 12 CVEs and owner risk-scope source](OLDX_STEP05_H1B_NEW_PRIVATE_MEDIATOR_IMAGE_RISK_AND_OWNER_DECISION_2026-11-25.md).

## 2. Phase P: one bounded read-only preflight BEFORE operational approval

**Candidate resource locators (not existence claims):**

| Resource | Exact candidate / restriction |
|---|---|
| Project | `oldx-staging`, expected number `38472235077`; must confirm actual authenticated operator and project identity |
| Region | `asia-south1` (Mumbai) |
| Existing shared Artifact Registry repository (READ-only first) | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images`; never create/delete this repository |
| Proposed new image name/tag | `oldx-c2-mediator-off:<unique-H1B-run-id>`, NOT yet selected or pushed |
| Proposed NEW no-key runtime SA | `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, no blanket project roles |
| Proposed NEW Cloud Run service | `oldx-c2-website-mediator`, no old-service traffic, no domain or public invocation |
| Protected old resources | `oldx-owner-read` (all revisions/tags/traffic/IAM), existing C1A private `oldx-step05-gateway` UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b` and SA UID `102194769236111252832` unchanged |
| H1B duration | Prefer **one supervised short session** and guarded cleanup in the same session, at most **24 elapsed hours** from actual activation; exact UTC/IST start/end required after creation |
| User data | ZERO real or synthetic Auth users, Product documents, media, Firebase/Firestore transactions |
| IAM | Keep Invoker IAM **ON**, no `allUsers`, `allAuthenticatedUsers`, public browser access, service-to-service Invoker grants to old Gateway or new data provider |

**Prepared read-only script:** `scripts/step05-h1b-readonly-preflight-20261125.sh`. On owner-authenticated WSL, it may check exactly active account, project identity, target-new-service collision, target-new-SA collision, and the existing Registry repository. It does **not** create/push/deploy/grant, refresh old IAM inventories, or touch tests/scans. Result of `gcloud ... describe` error is `UNKNOWN_UNTIL_DISTINGUISHED` — **403 and transient failures must NEVER count as NOT_FOUND**. If the target exists or ownership/permissions are ambiguous, **STOP**; do not adopt, update or delete it. Private evidence only; final concise readback to Issue #17. This preparation phase is **not** H1B execution.

**Preflight explicitly NOT yet observed:** actual operator identity; new SA/service collision status; repo config/tag immutability; available exact non-colliding new tag; effective inherited IAM; image push/write privileges; Cloud Run service Agent/artifact access; billing/current region SKU/cost and cleanup executor. These remain `UNVERIFIED`; historical information does not satisfy a fresh target-specific check. A clean preflight is necessary, never sufficient by itself.

## 3. Phase W: separate owner operational consent is MANDATORY before any write

For a future **second explicit owner approval**, bundle the following into **ONE finite H1B one-shot execution packet**. The owner must approve the resources, gross budget review threshold, operator, actual window, permissions and **guarded cleanup**; consent to Option B CVE risk is insufficient.

| Step | Proposed write (count) | Strong stop/readback boundary |
|---|---|---|
| W1 | Create **ONE** NEW user-managed no-key SA (max1) after exact collision-not-found proof | Record new SA `uniqueId`, creation time, attached policy and inherited rights; no JSON keys, no Auth/Firestore/KMS/other service Invoker permissions. If existing or mismatched, STOP |
| W2 | Tag **retained LOCAL** exact H1A candidate to **ONE** new uniquely named image in existing registry, and **ONE image push** | No Docker build/rescan; inspect **actual pushed OCI manifest and linux/amd64 child/config**, compare layer/source linkage to H1A receipt; independent remote digest capture. If tag collision or digest/config mismatch, STOP before any Cloud Run deploy. Clean up exact new pushed object only under later fresh reference checks |
| W3 | Deploy **ONE NEW** Cloud Run OFF-only service using **real remote immutable registry digest**, new runtime SA | Explicit `--no-allow-unauthenticated`, `--invoker-iam-check`, request-based CPU, min0/max1, 1CPU/512MiB, concurrency1, timeout5s, Node configured port8080. Explicit `--ingress=all` only if required for private authenticated owner probes: **network reachability ≠ public IAM access**. No public Invoker, no Firebase/Auth/Firestore/KMS service permissions, no domain/traffic migration. Record service UID/revision/identity/image and exact active configuration; STOP on unexpected effective policy |
| W4 | **Only if separately included in approval:** grant the exact authenticated owner principal `roles/run.invoker` on **new H1B service only** if necessary; no project-wide IAM grants | Require precise email/principal and explicit confirmation; STOP if inherited roles/policy differ. Do not grant mediator SA Invoker to existing C1A or Product backend. Owner can decline this binding and leave private negative-only probes |
| W5 | **Only in approved supervised window:** max FOUR exact hosted calls (no retries): anonymous `GET /health` expected 403; explicitly authenticated `GET /health` expected 200; authenticated `POST /api/staging/marketplace/owner` expected 503; authenticated malformed path expected 404 | Never use `/healthz` reserved Cloud Run route. Each actual response is evidence, not a promise; no real user data; no automatic web probe, repeated C1A calls, or public Product API. Any unexpected result stops subsequent calls |
| W6 | Guarded **NEW-only** disable/cleanup in the same supervised session, or by separately approved bounded deadline | Verify exact new service UID/revision/IAM, no other tags/users/dependencies; remove **only** NEW service, NEW image version if unreferenced, NEW SA if its uniqueId matches and unused; NEVER shared registry/old services/C1A data. If dependency/mismatch => `STOP_MANUAL_RECOVERY`, retain evidence and require immediate owner intervention |

**Do not assume an owner can successfully invoke a private Cloud Run service without a role**, or that direct `all` ingress exposes public unauthenticated access. Cloud Run IAM is a distinct, mandatory boundary. Official references: [Cloud Run deploy](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy), [IAM access](https://docs.cloud.google.com/run/docs/securing/managing-access), [Ingress](https://docs.cloud.google.com/run/docs/securing/ingress), [Artifact Registry push](https://docs.cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling).

**New-resource cleanup cannot be asserted automatic.** The 24-hour Option B acceptance is a **maximum** and does not require keeping an OFF service up for a full day. Recommended execution is **much shorter**, with same-session guarded cleanup. If supervised cleanup/disable and the responsible operator cannot be guaranteed, do **NOT** begin H1B creation merely to meet a schedule.

## 4. Cost/limits and evidence controls

- H1B image approximately **214,841,702 local bytes (~205 MiB)**. Registry charges track actually stored compressed layer bytes and existing free-tier/other use; do **not** pretend local image size equals billed registry size. No verified region-specific tax/FX/account commitment is available in this packet.
- Proposed operational spending **review threshold ₹100 gross new H1B charge** (not an automatically enforced billing cap or estimate). If the operator cannot reasonably bound exposure or the owner declines it, **STOP before W1**. Verify actual pricing/account/billing for Mumbai and existing Registry; no new billing account/plan/change. Max1/min0 limits are not hard cost caps; logs, storage, network and unauthorized traffic can still consume billable resources. Official [Cloud Run pricing](https://cloud.google.com/run/pricing), [Artifact Registry pricing](https://cloud.google.com/artifact-registry/pricing).
- Preserve private WSL evidence with restricted permissions, command counts and UTC+IST timestamps, Cloud Audit/IAM and digest readbacks, locally checked report SHA256. No tokens, service-account keys or full private scanner reports in GitHub. Stop on image mismatch/new CVE/collision/unexpected IAM/error, and on missing cleanup access. New writes maximum: ONE new no-key SA, ONE new image push into **existing** repository, ONE new Cloud Run service; at most ONE exact service-level Invoker grant if explicitly approved. No Cloud Build/Syft/Grype/real users/Firestore/KMS.
- Existing C1A trial private OFF-only retention **ends 28 November 2026 at 23:19 Asia/Kolkata**. H1B choice neither extends it nor authorizes touching C1A. A separate decision is necessary for its safe retention or guarded cleanup before deadline.

## 5. Next single owner step and G1–G6 progress

**Current:** `H1A_LOCAL=PASS_WITH_LIMITS_CONSUMED`; `H1B_OPTION_B_CVE_RISK=ACCEPTED_NARROW_24H`; `H1B_READONLY_PREFLIGHT=PREPARED_NOT_EXECUTED`; `H1B_CLOUD_WRITE/DEPLOY/HTTP=NOT_AUTHORIZED`; `H2/PRODUCT/PRODUCTION=NO_GO`.

**Next single operator step:** one read-only owner-WSL H1B collision/project/registry/account preflight, no resource mutation. **After that** request the separately scoped W1–W6 owner operational consent using real identifiers/role findings and a 24-hour maximum risk window with same-session cleanup. No other source/image work needs repeating. G2 signing provider, G3 runtime default DB/Auth least-privilege, G4 media, G5 nonce TTL cleanup, G6 enabled-image risk remain independent blockers to C2/website launch; H1B OFF test by itself does not complete those gates.
