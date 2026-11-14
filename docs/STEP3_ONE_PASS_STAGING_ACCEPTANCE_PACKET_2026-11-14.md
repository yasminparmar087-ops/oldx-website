# OLDX Step 3 — One-pass Staging Acceptance Decision Packet
Date: 2026-11-14
Branch: `security-hardening-review`
Status: **PREPARATION ONLY; STAGING NO-GO; PRODUCTION HOLD / NO-GO**

## Goal and invariant

Complete the Final Strategic Plan's Cloud Run-compatible Backend and Security Step 3 in the smallest evidence-supported number of sessions, without repeating already passed tests, expanding IAM to work around inconclusive diagnostics, changing production, or running unsafe fixtures. `LIVE_EXECUTION_ENABLED=false` remains invariant on review source. No live action is authorized by this document. Owner Yasmin must separately approve each currently unapproved cloud mutation, hosted activation and data-plane test after reviewing its *exact* version, operation, risk and cleanup.

## 1. Do NOT redo — reusable evidence

| Subgate | Evidence as of 2026-11-14 | What it does NOT prove |
|---|---|---|
| Local application packaging | Cloud Shell owner screenshot: Docker mirror `node:24-bookworm-slim` download succeeded; Docker BuildKit 13/13 FINISHED, `oldx-product-read-step3:local` local image; no source Dockerfile edit | Hosted revision deployment/activation |
| Local API fail-closed | Docker `--network none` run and in-container HTTP smoke: `/health` 200; `POST /api/staging/marketplace/owner` 503 `ENFORCEMENT_UNAVAILABLE`; `/unknown` 404; all PASS. Container cleaned via shell trap | Enabled owner read/Firestore IAM |
| Focused Node backend tests and production dependency audit | Owner Cloud Shell screenshot: 26/26 Node tests PASS, npm audit --omit=dev: 0 advisories. Separate 6/6 Auth fake integration PASS and earlier already documented offline runs | Any live permission or CRUD |
| Google Cloud configuration | Owner previously observed `--check-configuration` 10/10 MATCH; later `--cloud-preflight` progressed after correcting *local* gcloud active project to `oldx-staging`. One direct service invoker binding, 0 public bindings, pinned audience `https://oldx-owner-read-lqpaz3pd5a-el.a.run.app`, rollback baseline CONFIGURATION_MATCH | Effective invoker, inherited IAM or rollback execution |
| Anonymous edge denial | One pinned `healthcheck` tag anonymous GET returned Google frontend HTTP 403, HTML nonempty, no redirect | The verifier's correlated request log was `MISSING`, so `anonymousDenial.result=BLOCKED`; not logged-denial PASS |
| Runtime SA config | Enabled, 0 user-managed keys; `oldxProductReadFirestore` contains `datastore.databases.get`, `datastore.entities.get/create/update` and **no** entity delete. Binding limited by *configured* condition `resource.name == "projects/oldx-staging/databases/(default)"` | Actual effective Firestore condition, negative other-database boundary or entity delete denial |
| Operator token grant | Yasmin directly bound to narrow custom `iam.serviceAccounts.getAccessToken` role on exact runtime SA. Policy Troubleshooter direct Allow GRANTED; **overall UNKNOWN** due to PAB visibility | Actual access-token exchange, datastore operations or final effective access |
| Historical staging synthetic Auth | One separately authorized disabled/passwordless Auth probe was created, read, deleted and UID absence verified. Four target IDs previously observed absent in a dated, read-only preflight. | Current absence immediately before writes, four-resource CRUD/cleanup, enabled user sign-in/hosted acceptance |

## 2. Strict order; avoid rework

### Gate A — Source and evidence packet (no cloud resources)

- Verify exact reviewed branch SHA, repository cleanliness and current default-off `Dockerfile.product-read` / server.
- Treat Docker and unchanged focused suites as completed evidence; no image rebuild, repeat tests or repeated custom-role screenshots unless source or provider configuration materially changes.
- Compare documented missing items to code. **Do not interpret a cloud IAM Role containing create/update as read-only**; supported quota-counter transactions require narrow write authority.
- Identify exact requirements for the positive and negative hosted tests (owner, foreign buyer, unauthenticated, wrong-project/expired token; quota/audit, safe DTO), short-lived named invoker identity, and exact cleanup evidence.
- The latest GUI evidence supersedes older **missing getAccessToken grant** proposals in older sections of `docs/PHASE_B_PERMISSION_AND_APPROVAL_MATRIX.md`. Do not create another grant.

### Gate B — Non-mutating operator-ready preflight (no repeated exploratory probes)

- Owner-approved named operator/project only: `yasminparmar087@gmail.com` / `oldx-staging`.
- Confirm the specific current revision's service URL, tag, main traffic and IAM binding by reusing the latest valid record. Re-read *only if changed*.
- The last `--cloud-preflight` was `BLOCKED` **solely for anonymous log-correlation evidence** despite HTTP 403. Do not endlessly repeat the request. Determine whether a trustworthy log entry for this particular edge rejection is necessarily available. This is an evidence-design issue, not proof that the service is open or a reason to grant permissions. If the verifier's strict log check cannot be satisfied, keep that gate BLOCKED and propose an independently reviewable alternative; do not silently weaken a security test.
- For Firestore IAM, the configured (default) resource condition and PAB-incomplete allow result are **not proof** of true database isolation; avoid the previously rejected Policy Troubleshooter Firestore tuple. Define only a narrowly scoped, separately authorized runtime proof capable of establishing the needed positive permission, and preserve UNVERIFIED for negative scope when untestable.

### Gate C — Exact owner approval packet, *before* any staging changes

One compact decision bundle, with *separate lines/consents* for:
1. **Identity/token/invocation evidence:** exact operator, existing dedicated `oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com`, service, audience, token acquisition and *whether* one bounded hosted invocation is approved; no unreviewed token display.
2. **Runtime/Firestore evidence:** which exact `(default)` database operations, with any disposable ID needed and its own delete-denial risk; positive and negative expectations, and how condition isolation will or cannot be demonstrated.
3. **Cloud Run activation:** immutable code/image digest, tagged revision and env/identity, **0% main traffic**, allowed temporary IAM/revision operations, cost envelope, monitoring and complete manual rollback; approval not inferred from earlier conditional invoker setup.
4. **Fixture lifecycle and user auth:** exact two enabled Auth UIDs and two Firestore paths, two sign-ins, key handling, exclusive persisted journal, reviewed runner, fresh create-only preflight, cleanup operator and controlled same-session deletion. Prior *planning* consent and earlier one-user probe are not approval to bypass the source hard-off gate.
5. **Quotas/budget/traffic:** bounded 200-request / 60-minute / 1,000 billed-instance-second operational stop limits only if still compatible with the reviewed packet, **not** a guarantee of cloud billing cap, plus rate-limit counter ownership/cleanup and failure recovery.

Only relevant subsets should be requested once the exact executable evidence and risks are ready. A generic "continue" is not authorization for these mutations. No `--execute`, toggles, tagging, token mint, API enablement, service-account/IAM/Rules/Billing change or live Firebase read/write until the specific approvals.

### Gate D — One supervised acceptance session (not yet authorized)

Only after all Gate C exact scopes and rollback are approved:
- Fresh exact-ID collision read before create (previous absence is stale); stop on any EXISTS/UNKNOWN.
- Snapshot original 0%-traffic/tag/disabled baseline, private journal and runtime budgets; no unexpected service traffic.
- Fixed exact create-only Auth/Firestore, owner/buyer sign-in and two-identity invocation through specifically approved keyless invoker; record only redacted response decisions. The runner must preserve tokens only transiently and fail closed.
- Verify authorized owner's bounded projected DTO, foreign-buyer denial, unauthenticated and wrong identity denial, revocation/token behavior and rate/quota/audit expectations. A disabled GET test is not enabled owner-read acceptance.
- Cleanup under reviewed exact provenance and Firestore `updateTime` preconditions; Auth UID deletion lacks CAS/generation guard so an unexpected UID change or unknown receipt requires STOP and supervised human resolution. No retries after ambiguous remote writes. Re-verify all four exact paths absent and counter state.
- Explicit authorized tagged rollback, verify original disabled revision/100% main traffic and previously agreed denial health; record cost/limits, no secret data.

### Gate E — Closure judgment

Record **SOURCE-READY** only for proven source/local packaging/checks. Record **STAGING-ACCEPTED** only for full gated live evidence and cleanup/rollback. Keep status NO-GO for any missing IAM boundary, invoker, logging, fixture or rollback evidence; distinguish BLOCKED and UNVERIFIED rather than hiding them. Production remains HOLD / NO-GO pending independent release authorization.

## 3. Shortest next action

**No additional Cloud Shell command is needed immediately.** Existing container build and smoke evidence are successful. First prepare a narrow approval-ready *diff* of Gate C exact changes (if genuinely required) and flag any unready recovery/code paths, **source-only**, on `security-hardening-review`. Present Yasmin with one decision (as few individually scoped approvals as genuinely necessary), not a repeated command per diagnostic. If the documentation-only decision cannot be made safe, park that subgate and continue only independent repository-only work, without calling Step 3 staging complete.

This plan deliberately makes no changes to Dockerfile, code gate, IAM, Firebase data, Rules, Cloud Run, Billing or Production.

## 4. 2026-11-15 — minimum unblocking diff after owner-approved source-only continuation

This is a **source-only release decision**, no live action authorized by generic continuation. The owner specifically requested **only necessary checks** and consented to preparation of one safe, supervised Step 3 staging acceptance session. Previous Docker build/audit, Artifact Registry OCI index `c5fc856b...` (linux/amd64 manifest `eabe4207...`), 0%-main-traffic default-OFF tagged revision `oldx-owner-read-00003-nus` (`step3rc14`), anonymous 403+403, authorized Google health 200 and disabled owner 503, runtime SA token+one GET 404, operator two GET 404 and Auth GET/DELETE policy `CAN_ACCESS` are already documented. Do not rerun unchanged checks.

**Minimal concrete blockers found by source reading:**

1. **Source Gate A — actual runner hard OFF:** `scripts/phase-b-fixture-session-v1.mjs` declares `LIVE_EXECUTION_ENABLED=false` and `scripts/phase-b-owner-read-acceptance.mjs` declares `LIVE_HOSTED_ACCEPTANCE_ENABLED=false`. This is intentional and should remain default-off. A future *distinct, immutable, owner-reviewed activation mechanism* may allow only one exact staging session. Approval to prepare or previous 0% default-off deploy does **not** authorize flipping either switch.
2. **Source Gate B — OCI digest acceptance bug:** `inspectPhaseBConfiguration(...,{hostedTarget})` checks `value.status?.imageDigest?.endsWith('@' + hostedTarget.digest)` (near lines 589–595 of fixture script). Real `oldx-owner-read-00003-nus` Cloud Run revision reports child **linux/amd64 platform manifest** `sha256:eabe4207e307d1e487a30e4afd3abe8cda3792883a752864a5d6f80c45cd082c`, while verified pinned Artifact Registry image URL is parent **OCI index** `sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc`. A direct equality requirement against the wrong digest type would incorrectly report a mismatch. Before any live runner approval, patch the verifier narrowly to require a verified provenance relation between the immutable registry index and Cloud Run's exact chosen platform manifest (or an explicitly pinned and separately verified platform digest), without accepting arbitrary suffixes. Add **focused** positive index→manifest and negative unrelated-manifest offline regressions; do not rerun the whole suite.
3. **Source Gate C — cleanup after early failures is supervised, not automatic:** `runSession` has normal-flow conditional Firestore exact-ID deletion and Auth UID deletion, but `finally` only drops volatile credentials and closes the journal. A failure after some creates can leave partial fixtures; journal states `CREATE_UNKNOWN`, `UPDATE_UNKNOWN`, `DELETE_UNKNOWN` must trigger STOP and private operator-reviewed recovery, **not retry, broad delete or automatic cleanup claim**. Confirm exclusive private journal availability and a real named recovery path before creating any data. Firestore conditional delete only if session marker, createTime, updateTime match. Auth deletion must freshly verify UID/email/creationTime; no atomic generation guard.
4. **Configuration Gate D — default-OFF tagged revision is NOT enabled Owner Read acceptance:** the only approved new tag `step3rc14` currently has `OLDX_PRODUCT_READ_ACTIVATE_STAGING=false` and `OLDX_PRODUCT_READ_STAGING_ADC=false`. Authorized test 503 is expected. Enabled owner/buyer testing requires a **new** separately approved immutable staging-tagged revision with explicit activation env and 0% main traffic and an independent rollback, not mutation/redeployment of `step3rc14` or promotion of main traffic. Scope minimum 0/1 instances, concurrency 1, CPU 1/512Mi, bounded request rates and time/cost, existing private Cloud Run invoker and runtime SA, no IAM/Rules/Billing changes without a distinct approval.
5. **Runtime/cleanup Gate E:** operator GET on two exact docs and Auth policy GET/DELETE `CAN_ACCESS` exist, but operator effective Firestore DELETE, runtime CREATE/UPDATE, runtime DELETE denial and cross-database isolation remain unverified. The failed Firestore Policy Troubleshooter tuple HTTP 400 is **inconclusive**. No speculative DELETE on absent resources. Prove cleanup capability through narrowly reviewed policy evidence and only under a distinctly approved exact fixture lifecycle; if effective delete remains uncertain, **do not create fixtures**.

**One consolidated proposed decision AFTER source bug fix + focused offline tests:** owner separately reviews immutable runner SHA and enabled-revision image digest, explicit new unique 0%-main-traffic tag and nonsecret env, fixed two Auth UIDs `synthetic-seller-a`/`synthetic-buyer-b`, exactly two fixed Firestore documents `marketplaceActors_v1/synthetic-seller-a`/`marketplacePrivate_v1/product_synthetic-phase-b-read-01`, two transient sign-ins, fixed private owner read and buyer denial probes, and same-session operator conditional cleanup of precisely these four fixtures. Exact limits and abort/recovery ownership must be frozen. Require four-ID preflight **only immediately before approved create**, no repeated earlier checks; explicitly separate consent to staging revision deployment/activation from Firebase creates/updates/deletes and final tag removal/rollback. If cleanup is not safely recoverable, do not proceed even if generic approval was given.

**Currently permitted next work:** repository-only narrow verifier bug fix and minimal focused tests on `security-hardening-review`; record outcomes and ask for exact live-scoped approval later. No cloud request or mutation was performed by this document update. **STAGING NO-GO / PRODUCTION HOLD / NO-GO**.


## 2026-11-15 — Hosted Owner/Buyer 0%-traffic rollout and complete rollback packet (REVIEW ONLY)

**Status: SOURCE REVIEW ONLY; no live deployment, configuration change, or cloud-write approval.** Existing 04:03 IST focused hosted four-row/fixture canonical image test PASS 2/2. This supplement supersedes any older suggestion that the already disabled Step 3 tag can be enabled or used for actual Owner/Buyer acceptance.

### Verified historical baseline, not a fresh before-snapshot

- Project oldx-staging, region asia-south1, service oldx-owner-read. Yasmin operator yasminparmar087@gmail.com. Runtime service identity oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com. Named private invoker oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com; do not grant public invoker access.
- Main oldx-owner-read-00001-8kr untagged at 100% and disabled; oldx-owner-read-00002-tid tag healthcheck at 0%; oldx-owner-read-00003-nus tag step3rc14 at 0% and disabled. All three entries are protected.
- Pinned published immutable image index: asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-owner-read-step3-rc@sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc. Independently verified linux/amd64 child: sha256:eabe4207e307d1e487a30e4afd3abe8cda3792883a752864a5d6f80c45cd082c.
- All three source execution gates remain FALSE (fixture-only, hosted runner, hosted acceptance). Previously completed fixture journal at $HOME/.oldx-phase-b-fixtures-v1 must not be reused or removed. Separate future hosted journal at $HOME/.oldx-phase-b-hosted-v1 has passed two offline isolation/recovery tests; no hosted session occurred.

### Proposed new revision: exact scope to review later, NOT yet authorized

- Create ONE additional 0%-general-traffic tagged **enabled staging revision**, never reuse or mutate old step3rc14, never shift general traffic, never rebuild or replace the immutable image. Proposed unique tag ownerbuyertrial is merely a candidate: read-only verify it is unused before approving. Cloud Run assigns the new immutable revision ID; it must be captured after creation and separately pinned before any hosted data-plane acceptance. With the candidate created, require precisely four service traffic rows: old disabled main 100%, healthcheck 0%, step3rc14 0%, new tag 0%.
- Only the new revision would use these exact non-secret env settings: OLDX_PRODUCT_READ_ACTIVATE_STAGING=true; OLDX_PRODUCT_READ_STAGING_ADC=true; OLDX_FIREBASE_ENV=staging; OLDX_FIREBASE_PROJECT_ID=oldx-staging; OLDX_PRODUCT_READ_DATABASE_ID=(default); OLDX_PRODUCT_READ_SERVICE_ACCOUNT=oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com; OLDX_RATE_WINDOW_MS=60000; OLDX_RATE_ACTOR_LIMIT=10; OLDX_RATE_GLOBAL_LIMIT=50. Rate numbers are proposed, not deployed facts. Keep publication disabled and emulator off. No file-backed ADC, key JSON, unexpected env variable, secret ref, metadata override or proxy override. K_SERVICE is injected by Cloud Run; DO NOT manually set it.
- Proposed bounded resources (pending exact provider-flag and inherited-template check): minimum instances 0 at both applicable scopes, maximum instances 1, concurrency 1, CPU 1, 512MiB memory and bounded timeout. Verify billing status/budget and request caps before any deployment; these settings do not enforce a hard cost ceiling.
- Preserve existing service IAM, fixed runtime SA and tag mappings. A 0% tagged revision CAN STILL RECEIVE requests at its tagged URL; don't mislabel it as inaccessible.

### Before deployment: freeze a private evidence snapshot

Before any separately approved mutation, Yasmin must review a fresh READ-ONLY snapshot of the current service spec.template (including disabled flags), image digest, identity, ingress, min/max instances, traffic tags and exact percentages, latest ready revision, policy invoker binding and requested cost/risk envelope. Stop on drift or ambiguity. Preserve a private copy of the original disabled service template needed to restore it, without printing env secrets. Confirm exact code/image SHA and unmodified review branch. No need to repeat historical emulator, Docker, identity or fixture PASS tests without change.

Only after separately approved deployment: verify Ready, exact pinned runtime digest, both enabling settings in the NEW revision, named invoker restrictions, 100/0/0/0 traffic and no public IAM. Any mismatch means STOP and rollback; it does not authorize a hosted fixture session or production traffic.

### Rollback must restore BOTH access and the disabled service template

IMPORTANT: Removing a tag or leaving 100% on old main DOES NOT restore the previous desired service template. The newly enabled template may otherwise be inherited by a future deployment.

Required separately authorized rollback envelope:
1. Stop invocations; preserve redacted logs and any existing hosted journal, without blind mutation retry.
2. Remove ONLY the new trial tag; verify its tagged URL no longer routes, old disabled main remains 100% and the old healthcheck and step3rc14 tags stay 0%. Don't promote the newly enabled revision.
3. Restore the snapshot of the ORIGINAL disabled service template, including activation flags false, prior runtime settings, identity and resource constraints. Restoring a template can create ANOTHER immutable disabled revision and change latestReadyRevisionName; this possibility must be included explicitly in the approval and checked afterward. Never assume removing a tag restores that template.
4. Re-verify IAM enforced, permitted disabled-route 503 and health 200, traffic percent and tags, latest ready revision, no unintended min-instances or recurring cost. Only remove a new revision if separately approved and safe. If any state/receipt is unknown, STOP and request owner-guided recovery rather than delete or repeat.

Official Cloud Run docs for the 0%-tag deployment and rollback behavior: https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration and https://docs.cloud.google.com/run/docs/managing/revisions. The docs explain that revision tags are directly invocable at 0% traffic and that revision-level minimum instances can incur cost.

### Separate data-plane permission gate AFTER rollout

Any later Owner/Buyer acceptance requires NEW specific consent, separately from revision deployment and its rollback. Only fixed Auth UIDs synthetic-seller-a and synthetic-buyer-b and fixed Firestore paths marketplaceActors_v1/synthetic-seller-a and marketplacePrivate_v1/product_synthetic-phase-b-read-01; fresh four-ID absence immediately before writes, private short-lived Firebase tokens, named keyless invoker, allowed owner response and buyer denial probes, completed separate hosted journal and original-updateTime guarded cleanup. The old accepted fixture journal is immutable evidence. Auth deletion still lacks atomic generation CAS. Effective runtime CREATE/UPDATE, DELETE denial and other-database isolation/PAB remain UNVERIFIED without supported separate proof. No IAM/Rules/Billing change follows from this packet.

**Decision today:** Hosted candidate deployment NOT AUTHORIZED, no new revision created, no future data-plane execution permitted, no production changes. Next owner decision should be ONE compact specific Cloud Run deployment + full rollback approval packet after confirming the precise snapshot and executable flags. Existing source-only work may continue; HOSTED STAGING NO-GO / PRODUCTION HOLD-NO-GO.


### 2026-11-15 04:17 IST — latest read-only scaling/ingress/tag evidence

Yasmin's Cloud Shell screenshot of an operator-scoped **READ-ONLY** gcloud service describe JSON projection at 04:17 IST reported the current Cloud Run service oldx-owner-read on oldx-staging/asia-south1:

| Screenshot field | Actual observed |
|---|---|
| SERVICE_MIN | UNSET |
| SERVICE_MAX | 20 |
| REVISION_MIN | UNSET |
| REVISION_MAX | 1 |
| TIMEOUT_SECONDS | 30 |
| INGRESS | all |
| MANUAL_SCALING | UNSET |
| TRIAL_TAG_UNUSED | True (tag ownerbuyertrial absent from status.traffic at check time) |

The previous **04:13 IST** independently observed disabled service template flags both false; runtime service-account exact match; one container, concurrency 1, CPU 1, memory 512Mi; three traffic entries main 100%, healthcheck 0%, step3rc14 0%, latest ready oldx-owner-read-00003-nus. These results agree and no mutation is evidenced.

**Interpretation and approval-critical protections:**

1. According to Google Cloud Run official minimum-instances documentation (https://docs.cloud.google.com/run/docs/configuring/min-instances), unset service/revision minimum normally uses default 0 in autoscaling. However a missing annotation is not proof that no other autoscaling/billing mode/inherited configuration applies; new trial must explicitly preserve **zero minimum instances** at all applicable scopes. Min zero is not a total spend cap. Revision-level minimum >0 on a 0%-tagged revision can result in billing.
2. Existing **service MAX 20** and **template revision MAX 1** are different levels. The effective max for the currently reviewed revision is 1 as the lower of the two, but do NOT casually mutate service-level MAX 20 (could affect existing revisions) or assume a future revision will inherit the exact limit. The new approved candidate must independently assert revision MAX 1 and concurrency 1, without broadening all-service scaling. Provider CLI semantics and preserved settings must be checked in the exact executable command/diff before deployment.
3. Timeout is exactly 30 seconds and should remain 30 for the new candidate unless separately approved. Ingress all means internet-reachable but is not necessarily public by itself; access must stay restricted with existing private Cloud Run Invoker IAM and no unauthenticated/public principal. IAM snapshot required directly before a mutation; this screenshot did NOT check current IAM.
4. Proposed unique trial tag ownerbuyertrial was unused at the 04:17 IST snapshot, but MUST be checked immediately before any mutation. No new revision/traffic change is authorized. This check did not preserve the complete original service template or IAM policy for rollback; keep that distinct pre-deploy snapshot and restore requirement.
5. Keep current 100% on old disabled main, preexisting two 0% tags untouched. The new candidate's 0% tag can be directly invoked, so stop all trial requests and restore the **disabled service template** (not just traffic) during approved rollback. Do not roll back through unscoped revision/traffic deletion.

**Decision: no Cloud Run deployment authorization granted; HOSTED STAGING NO-GO, PRODUCTION HOLD/NO-GO.** The only necessary remaining preparatory work is a reviewed executable deployment + full restore diff based on privately captured pre-image and current IAM; no further old PASSED tests or four-fixture session rerun.


### 2026-11-15 04:21 IST — private service/IAM rollback snapshot completed; approval-stage safeguards

**Owner screenshot evidence, no deployment or cloud mutation:** Yasmin executed the project/region/account-scoped read-only Cloud Run service describe and get-iam-policy calls under a private 0700 directory with umask 077 at $HOME/.oldx-hosted-rollout-before. A shell-local Python projection returned exactly:

- PRIVATE_BACKUP: CREATED
- PUBLIC_IAM: PASS
- NAMED_INVOKER: PASS
- INVOCATION_IAM: PASS
- CLOUD_MUTATIONS: NONE

This proves the private JSON snapshot files were created and successfully parsed at check time, that the SERVICE-level Cloud Run policy did not explicitly include allUsers or allAuthenticatedUsers, that oldx-phase-b-invoker@oldx-staging.iam.gserviceaccount.com had roles/run.invoker there, and the checked invoker-IAM-disabled annotation was not true. The screenshot **does not prove** inherited IAM grants, all token audiences, successful rollback execution, resource version concurrency safety, or any runtime Firestore permission. Do not publish, paste or commit the private service.json/iam.json contents; they may contain configuration that must remain private. Do not delete or overwrite the backup.

**Required before actual deployment:**
1. Independently verify that backup files are nonempty valid JSON and contain the same exact service/disabled desired template and protected three-row traffic snapshot. A json-format service describe response is a **forensic before-image**, not directly an executable gcloud run services replace manifest. If using YAML restoration, prepare a separate private gcloud run services describe --format=export service YAML and review exact diff/provenance; never pipe raw service.json into replace or apply unsanitized server status/output. Keep the original private JSON immutable.
2. Preflight current cloud service generation, protected 100/0/0 traffic, disabled activation template flags, exact runtime identity, image digest, existing private IAM, budget status and proposed tag availability immediately before any approved mutation; stop on drift or collision. Preflight should print only verdict labels, not secrets.
3. A deployment would add exactly one separately approved hosted enabled tagged **0%-main-traffic** revision, reusing the verified registry digest and runtime identity. Proposed tag ownerbuyertrial remains available **only as of the earlier 04:17 check**; it must be rechecked. Preserve ingress all ONLY with the existing required private IAM and no public invoker. Never widen service-wide max (currently 20) and enforce new REVISION max 1, min 0, concurrency 1, timeout 30, CPU 1, memory 512Mi, nonsecret env limited to the reviewed nine settings.
4. Explicitly authorize complete rollback **as part of the deployment decision**, not after a failure: remove only new trial tag and confirm it no longer serves, protect original main revision 100% and prior healthcheck/step3rc14 0% tags, restore the pre-snapshot original DISABLED service template (may create an additional disabled revision and change latestReadyRevisionName), verify no public IAM or surprise min instances, and retain all private journals. No automatic rollback is guaranteed by the existing backup; an operator-supervised command diff is required.
5. Never confuse source-only 2/2 PASS and the completed prior fixture-only lifecycle with approval for enabled Owner/Buyer data-plane tests. A separate owner-scoped later consent and fresh four-ID collision preflight are required before any Auth/Firestore creation/cleanup. Existing hosted/source gates remain FALSE.

**Deployment approval not yet granted.** In order to respect the prior NO-GO and avoid speculative mutations, next prepare a private, exact exported YAML restoration diff and reviewed gcloud CLI steps *without executing them*. Only then request a single explicit Yasmin approval for the exact additional staging 0%-traffic enabled revision and its reversible removal/restoration. Any mismatch, inability to restore the template, cost ambiguity or unexpected IAM state means STOP. Keep Hosted staging NO-GO / Production HOLD-NO-GO.
