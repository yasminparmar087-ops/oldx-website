# OLDX Strategic Step 3 — one-pass Staging Acceptance decision packet

**Prepared:** 2026-11-14 · **Branch:** `security-hardening-review` · **Owner/operator:** Yasmin Parmar · **Target:** `oldx-staging` only.

**Purpose:** minimize setup, paid time and repeated tests while closing Step 3 (Cloud Run-compatible backend + security) *without bypassing safety/approval gates*. This document is a plan, **not authority** to change IAM, deploy, activate revisions, mint tokens, create/modify/delete Auth/Firestore records, or change billing, Firebase Rules, DNS or production. Current status: **STAGING NO-GO / PRODUCTION HOLD / NO-GO**.

## 1. Evidence already collected — never repeat without a relevant change

| Gate | Evidence and disposition | Do not infer |
|---|---|---|
| Repository focused Node backend tests | Owner Cloud Shell 26/26 PASS, 0 failures; npm production audit 0 reported vulnerabilities (2026-11-14) | Hosted success or no undiscovered vulnerabilities |
| Four-ID fixture journal/recovery/fake transport | Multiple focused offline suites PASS; hard gate `LIVE_EXECUTION_ENABLED=false` | Live CRUD or safe automatic cleanup |
| One disabled Auth proof | Owner-supervised exact UID create → verify → delete → absent **succeeded once**, no residue observed (2026-11-14) | Authorization for the original four resources or guaranteed Auth delete on future attempts |
| Original four-ID preflight | Two Auth UIDs and two Firestore documents ABSENT **at time of earlier preflight**, exact synthetic paths recorded | Current absence or creation consent; recheck only immediately before separately approved writes |
| Service-account/IAM configuration | Runtime and invoker keyless configurations, narrow `getAccessToken` binding, database condition exact string and four Firestore permissions observed; one direct service invoker, zero public bindings | Effective Firestore database restriction, inherited policy/PAB resolution, named invocation |
| Policy Troubleshooter | Allow binding GRANTED for operator runtime token creator; **overall outcome UNKNOWN** owing to Principal Access Boundary visibility. Database tuple diagnostic previously inconclusive | A universal IAM PASS or need to add a duplicate IAM grant |
| Cloud Run read-only preflight | Active operator/project corrected; expected service audience/revision; rollback **CONFIGURATION_MATCH**; anonymous GET returned Google-frontend HTTP 403; request-log trace **MISSING** so `anonymousDenial.result=BLOCKED` | Correlated logged denial PASS, actual hosted authorized-owner behavior |
| Local Docker | `mirror.gcr.io/library/node:24-bookworm-slim` pulled, local image built 13/13 FINISHED; network-none Docker container smoke PASS: `/health` 200, owner route 503, unknown path 404 | Cloud Run deployed revision acceptance or runtime database behavior |

**Do not repeat any of the above** merely because a new Cloud Shell session starts. Local project unset in one new Shell was resolved by setting only the local gcloud project; first establish active account and project in any specifically authorized future session. The missing conversation-only `oldx_auth_probe_recovery_readonly.py` does not exist in the newer checkout and is not needed; never repeat that ENOENT command.

## 2. Remaining *distinct* acceptance gates (not a testing backlog)

1. **Actual keyless runtime access:** precisely scoped expected runtime Firestore GET/CREATE/UPDATE and DELETE-denial, plus database isolation or an explicit recorded inability to prove it. Static role/condition and an unknown Policy Troubleshooter result cannot close this. Don't broaden permissions or claim that database-level IAM restricts document IDs.
2. **Invoker and hosted edge:** named `oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com` keyless ID-token path, service-only `roles/run.invoker`, an unauthorized-principal/anonymous denial, and genuine authorized invocation on an approved tagged staging revision. The anonymous 403 already observed is useful but its matching log was absent; do not loop repeated requests just to force a log result.
3. **Privacy and application acceptance:** separate Google invoker and Firebase end-user identities; synthetic owner success and foreign buyer denial, revocation/invalid audience/project denial, bounded quotas and exact safe DTO. Existing offline fake acceptance is not live proof.
4. **Controlled fixture and cleanup:** fixed two enabled Auth UIDs `synthetic-seller-a`, `synthetic-buyer-b` and two Firestore docs `marketplaceActors_v1/synthetic-seller-a`, `marketplacePrivate_v1/product_synthetic-phase-b-read-01`; known-only provenance, owner-supervised journal, exact create-only writes and conditional Firestore delete. Auth deletion has **no atomic UID-generation precondition**. Fail closed on collision, timeout, changed evidence or incomplete cleanup; preserve receipt and require separately reviewed exact-ID recovery. No bulk or automatic destructive cleanup.
5. **Cloud Run isolation and rollback:** immutable image digest and reviewed enabled-tagged revision at **0% main traffic** (main disabled baseline remains 100%), constrained CPU/memory/instances/request/time budget, responsible operator, separately approved deployment/activation, and verified restore to disabled baseline plus exact fixture absence.

If any above cannot be proven safely, leave **STAGING ACCEPTANCE = NO** and record the precise blocker rather than changing IAM/Rules or retrying blindly.

## 3. Fastest safe dependency order

**Gate A — No-change preparation (repo-only, now).** Freeze and record the exact review SHA, executable command preview and approved roles; reuse existing runner, release/rollback checklists, tests and evidence. Inspect actual command/source contract for the proposed *tagged* revision and identity. Only fix genuine code gaps in the review branch with focused tests. **Avoid a speculative new feature, broad refactor, or another full suite.**

**Gate B — Owner one-time scoped decision (before any new Cloud action).** Present one bounded action-specific consent packet listing precisely: project, names, region, image digest/runner SHA, signer/operator, identities, all intended *reads*, token mint, hosted calls, any IAM write, image publication/deployment/tag/env toggles, exact four-resource Auth/Firestore creates/updates/deletes, password sign-ins, quota-counter writes, limits, fees, session start/cutoff, recovery owner and rollback commands. Separate YES/NO for *read-only*, *token mint/invocation*, *data writes/cleanup*, and *revision/traffic changes*. **Do not infer new approval from “continue”.** Existing historical approvals for source-only work, the fifth-user proof and concept of a four-fixture session do not silently authorize runtime activation or amendments to a hard-off runner.

**Gate C — Single bounded supervised staging session (only after Gate B explicitly approved, no automated run from this document).**
- Reconfirm active operator/project and immutable revision/digest once.
- Confirm cleanup/rollback access and absence before create; STOP on mismatch or unavailable tools. A clean status is time-bound, not a lock.
- Validate effective runtime access *only through separately approved limited operations* and, where feasible, dedicated invoker token and denial proof. If IAM/PAB/log evidence remains inconclusive, record pending; do not bypass.
- Provision exact four fixtures only when immediate, independently verified cleanup is feasible; preserve secure journal, ephemeral secrets, privacy and fail-closed behavior.
- Exercise only approved zero-main-traffic tagged hosted Owner Read checks and bounded quota/cost envelope; no prod.
- Supervised individual cleanup; record final four ABSENT; return to disabled default and compare rollback baseline; stop on any ambiguity and escalate for exact-ID manual recovery under separate consent.

**Gate D — Closure decision.** Mark **SOURCE-READY** for independently verified local source/Docker checks. Mark **STAGING-ACCEPTED** only if every required hosted/security/cleanup evidence is positively and independently documented. If Gate C isn't approved or fails, progress other separately safe repo-only strategic tasks while preserving the Step 3 blocker. Production launch remains independently NO-GO.

## 4. Explicit stop conditions (no retries or improvisation)

- Active project/account, revision, service audience, token claims, source SHA, baseline, or any exact target differs.
- IAM permission/API/Policy Troubleshooter fails or overall result remains UNKNOWN and an effective grant is mandatory for this test.
- Missing verified invoker / deny policy, public grant present, changed ingress or unintended main-traffic shift.
- Missing owner consent for a particular operation or unreviewed hard-gate edit.
- Unknown/create-timeout/delete-timeout, Auth UID reuse/createdAt discrepancy, changed Firestore updateTime, journal missing/invalid, uncertain cleanup, quota/cost limit reached.
- Hosted denial log missing or uncorrelated where correlated log is a required acceptance criterion.
- Any secrets, real user data or private fixture payload appear in stdout, issue, PR or screenshots: STOP and follow approved secure incident process.

## 5. Immediate next no-change task

Do **not** rerun Docker or preflight. Review the existing **actual hosted tagged-revision command contract** plus the current gated runner to establish a concise immutable proposed command sequence for the owner, including bounded costs/rollback and which parts cannot be completed without code gate revision. Report any missing prerequisites in a **single owner decision**, not one-by-one cloud trial-and-error. Cloud Shell remains preferred for routine read-only commands; Codex only if a real multi-file bug demands it. No operation in this document was executed against cloud.

## 6. Hosted revision and rollback command contract — source review (2026-11-14)

**Review result:** The reviewed Cloud Run entrypoint `functions/staging-marketplace/product-read-server.mjs` runs disabled by default, with `GET /health` returning HTTP 200 and `POST /api/staging/marketplace/owner` returning HTTP 503 unless explicit staging activation gates, ADC identity, target project/database and rate policy all match. `Dockerfile.product-read` uses `node:24-bookworm-slim`, installs production dependencies from the lockfile, runs as `node`, exposes 8080 and handles SIGTERM. These are source facts, not a hosted-readiness assertion. The network-none local container smoke already passed. Source's startup guard also rejects various credential/environment overrides and requires platform-supplied `K_SERVICE` when activating.

**REVIEW-ONLY placeholders; NEVER paste this section as a runnable deployment script.** Current local image `oldx-product-read-step3:local` is **not** an Artifact Registry image and no immutable registry digest was captured, so it cannot be used as `--image` for a Cloud Run deploy. No existing approved registry image digest matching the current review HEAD has been established. The exact release source SHA should be frozen separately at session approval; document HEAD at review was `abdbaa5ec274e223e2f7fb118a70a3648d9a03b7` *before* this documentation change. Do not equate a moving branch HEAD or local image tag with a pinned artifact.

### A. First freeze candidate and safe baseline (not executed here)

- Confirm signed-in active operator `yasminparmar087@gmail.com`, project `oldx-staging`, Cloud Run region `asia-south1`, service `oldx-owner-read`, approved runtime service account `oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com`, approved tester invoker `oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com`, and database `(default)`. Match the existing repository/image input to its **immutable SHA**.
- Capture `gcloud run services describe oldx-owner-read --project=oldx-staging --region=asia-south1 --format=json` in a **private local** report and inspect only approved nonsecret fields; never publish raw revision env/secret references to GitHub/chat. Freeze the existing disabled revision `oldx-owner-read-00001-8kr` at 100% main traffic and the disabled `healthcheck` revision `oldx-owner-read-00002-tid` at 0% in the permissioned operator's plan. If drift occurs, stop.
- Obtain separately authorized immutable Artifact Registry image digest and scan/sign-off that image's Docker contents and no embedded credentials; the local smoke build's success cannot substitute for a registry digest or provenance.

### B. Planned *new* tagged 0%-main-traffic revision — requires a **specific new approval**, **NOT EXECUTABLE YET**

Cloud Run docs confirm that the form `gcloud run deploy SERVICE --image IMAGE_URL --no-traffic --tag TAG` creates a testable tagged revision without shifting main traffic, and that `--service-account` and `--set-env-vars` set the runtime identity and environment. Official docs: https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration and https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy . Exact proposed arguments, subject to separately approved identity/cost/rollback and complete resource configuration:

| Parameter | Proposed value or release gate |
|---|---|
| `--project`, `--region`, service | `oldx-staging`, `asia-south1`, `oldx-owner-read` |
| `--image` | **BLOCKED** until independently verified repository URI + immutable `@sha256:...` digest, permission to push or reuse image and cost approval |
| `--no-traffic --tag` | `--no-traffic` and separately approved unique disposable tag, **never** move the 100% main disabled baseline |
| `--service-account` | `oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com` (confirm effective permission and `actAs` under the reviewed deployer) |
| `--cpu --memory --min-instances --max-instances --concurrency` | Proposed `1`, `512Mi`, `0`, `1`, `1`; final bounds/pricing to approve |
| Activation env | **ONLY** separately approved tagged revision: `OLDX_PRODUCT_READ_ACTIVATE_STAGING=true`, `OLDX_PRODUCT_READ_STAGING_ADC=true`, `OLDX_FIREBASE_ENV=staging`, `OLDX_FIREBASE_PROJECT_ID=oldx-staging`, `OLDX_PRODUCT_READ_DATABASE_ID=(default)`, `OLDX_PRODUCT_READ_SERVICE_ACCOUNT=oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com`, `OLDX_RATE_WINDOW_MS=60000`, `OLDX_RATE_ACTOR_LIMIT=10`, `OLDX_RATE_GLOBAL_LIMIT=100`. No key files, emulator vars, proxy overrides or app secrets. |
| Ingress | Keep current IAM enforcement and recorded ingress; no policy relaxation or public invoker |
| Limits | Existing owner proposal: **at most 200 attempted requests / 60 minutes / 1,000 billed instance-seconds**; count retries; monitor actual billable usage, Firestore and log volume, stop on unknown billing. Budget email alerts are **not a spending cap**. |

**Do not execute the tagged revision merely on the basis of this table.** Deployment can incur spending and alter service revision configuration even at 0% traffic. Exact flags/settings, initial baseline snapshot, deployer roles and fees must be approved, and a controlled runner release must first address the hard-off `LIVE_EXECUTION_ENABLED=false` gate without weakening the default safety model. No blanket activation permission is implied by source-only continuation.

### C. Read/execute/rollback sequencing — approval required for each affected category

1. **Read-only preflight** (new scoped approval if touching live Auth/Firestore): exact four-resource absence, approved policy/identity visibility, rollback owner, successful cleanup capability; no speculative retries if evidence is missing.
2. **Keyless credential/invoker** (separately approved): issue tokens only for the intended service and principal, never print or save, then verify authenticated/anonymous/foreign invoker handling. A PAB/Policy Troubleshooter UNKNOWN or missing log correlation is **NOT PASS**. No repeat IAM listing just to reconfirm prior static grants.
3. **Synthetic data** (separately approved): exactly two Auth accounts and two specified Firestore documents. Runner remains hard-off, so this **cannot be run yet**. Each create/mutation must have a reviewed immutable candidate, private journal and verified same-session operator cleanup. Negative deletion probe on an exact synthetic document has destructive side effect risk and needs explicit scope. No data-wide operations.
4. **Hosted owner-read acceptance** (separately approved zero-traffic tag): app owner success and buyer/foreign-project/invalid-token denials, no private DTO leak, no-store, bounded quota-counter writes/retries and observable records. A Cloud Run 403 from Google frontend alone cannot prove backend security acceptance.
5. **Rollback/closeout** (separately approved): stop probes; individually clean approved four synthetic resources; verify four ABSENT; restore/confirm disabled baseline and `0%` trial traffic before removing the **specific approved test tag**. Cloud Run docs support `gcloud run services update-traffic oldx-owner-read --remove-tags TAG --project=oldx-staging --region=asia-south1`. Never `--clear-tags` indiscriminately; preserve pre-existing `healthcheck` tag. Confirm exact original traffic mapping and disabled owner 503 (or independently verified deny), while retaining reviewed logs and release audit. Official docs: https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration .

### D. The **one owner decision** still required

Obtain explicit separate authorization for (i) live read-only identity/target preflight, (ii) token mint / named hosted invocation, (iii) immutable image publication plus zero-main-traffic tagged deployment with actual spend envelope and rollback, (iv) precise fixture create/update/delete, Auth sign-in, quota writes and supervised cleanup, and (v) an independently code-reviewed narrowly enabled runner revision. Present the exact image digest and runner SHA **before** deployment or writes; no valid placeholder can satisfy those fields. If any category is not approved or technically ready, keep Step 3 **SOURCE-PROGRESS / STAGING NO-GO** and work on later independent repo-only tasks without bypass.

**Audit:** This is documentation/source review only. No images pushed, no live API called, no tokens minted, no runner activated, no IAM/Rules/Billing/traffic modified, and no Docker or old tests rerun.

## 7. Source-to-hosted gap found in the existing runner (2026-11-14)

**Concrete source inspection:** The current `scripts/phase-b-fixture-session-v1.mjs` keeps `LIVE_EXECUTION_ENABLED=false`; `--execute` fails before acquiring a Web API key, minting a token or using the data plane. Its `runSession(api, openJournal, afterSignIn, runtime, budget)` supports an optional `afterSignIn` callback; the separate exported `simulateFixtureAcceptance` uses that callback to run `runOwnerReadAcceptance` with *fake* transports and receives results only after all four resources are absent. However the **actual CLI `--execute` code** calls `runSession(transport(...), openJournal, undefined, runtimeFixtureTransport(...), budget)` — its **third argument is `undefined`**, so the proposed real four-resource mutation session, even if a later approved version enabled it, would **NOT test a deployed Cloud Run Owner Read route**. It is a fixed-identity Auth sign-in + direct Firestore runtime create/update/cleanup probe only; the Firebase end-user ID tokens are discarded without hosted invocation.

**Non-negotiable closure consequence:** Never label `--execute` alone as hosted acceptance, and never approve a blanket unsafe gate flip to “finish all Step 3”. The safe design is to preserve independent checks: (a) owner-approved exact four-resource creation/cleanup runner with fail-closed journal and owner recovery; (b) a separate *versioned and independently reviewed* zero-main-traffic tagged Cloud Run owner-read acceptance adapter using short-lived named Google invocation token + two transient Firebase end-user tokens; (c) explicit coordination and cleanup despite hosted failures, with token/session deadlines and no automatic ambiguous deletion retries. Reuse already existing `runOwnerReadAcceptance` and `simulateFixtureAcceptance` contract; no duplicate design or new wide IAM role. Before any real run, require a concrete reviewed secure code change, targeted offline regression tests, immutable runnable SHA, exact image digest, explicit owner approval for *each* class of operation, and a backup exact-ID cleanup path. The currently approved work does not include implementation or live activation of this missing composition. No cloud operation or code toggle was made in this review. Staging NO-GO and production HOLD / NO-GO.
