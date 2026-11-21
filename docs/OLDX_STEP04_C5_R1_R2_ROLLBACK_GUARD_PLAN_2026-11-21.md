# OLDX Step 04 — C5 R1/R2 guarded rollback plan (SOURCE-ONLY)

## 21 Nov 2026 — OWNER R1 + R2 narrow conditional execution approvals RECORDED (NEW LATEST)

User expressly replied `ha manjuri chhe` to **two separate specific rollback scopes**: **R1** remove *only* future `ownerreadv2` tag after it is created, leaving `healthcheck` and `step3rc14` intact; **R2** restore original `oldx-owner-read-00001-8kr=100%` main only if unexpected traffic drift is established and a fresh exact-state safety review permits it; R2 is **NO-OP** when old 100% main/tags remain. [Owner R1/R2 consent packet](docs/OLDX_STEP04_R1_R2_OWNER_CONDITIONAL_APPROVAL_2026-11-21.md). `R1_OWNER_CONDITIONAL_CONSENT=YES`, `R2_OWNER_CONDITIONAL_CONSENT=YES`, prior `B1_OWNER_CONDITIONAL_CONSENT=YES`. **Still NOT permission for immediate blind cloud execution**: fresh immediate pre-write service-state guard, exact final B1 CLI flags, environment/identity/secret diff, inherited IAM scope review, no public invocation, source digest, post-state/recovery plan needed. R1 tag removal does **not** revert latest template/revision. G4-A three GET snapshot ~17:48 `PASS_WITH_LIMITS` **consumed; do not rerun for status**. C4/G8 OFF-only risk accepted with limits; G2 independent builder provenance UNKNOWN, G4 other-db/exclusive invocation NOT PROVEN. `B1_R1_R2_EXECUTED=NO`, `STEP04=HOLD`, production NO-GO.

Date: 21 Nov 2026. **NOT AN EXECUTABLE AUTHORIZATION.** Branch `security-hardening-review`.

## Evidence frozen; DO NOT REPEAT
Actual owner screenshot ~17:24 IST: three revision-specific read-only GETs completed and `C5_CACHED_PREIMAGE=MATCH`. Root/main 100% `oldx-owner-read-00001-8kr` untagged; tagged `oldx-owner-read-00002-tid` = `healthcheck`; tagged `oldx-owner-read-00003-nus` = `step3rc14`. Three revision identities/resources:
- 00001-8kr image container digest `sha256:e5ad2ae1ae23b9f2...`; 1CPU/512Mi, concurrency1, timeout300, revision max1/min NOT_SET, **both relevant flags MISSING**.
- 00002-tid image container digest `sha256:5abd5e7b1b3d3cf2...`; 1CPU/512Mi, concurrency1, timeout300, revision max1/min NOT_SET, **both flags MISSING**.
- 00003-nus image container digest `sha256:eabe4207e307d1e4...`; 1CPU/512Mi, concurrency1, timeout30, revision max1/min NOT_SET, both flags **EXACT_FALSE**.
All three specific GETs finished with `C5_REVISION_PREIMAGE_READ_ONLY=COMPLETE` and `C5_DEPLOYMENT=NOT_STARTED`. Cached root traffic is not a live lock; missing flags do not show globally disabled code. Latest service template image and new npm-free index are distinct from old 100%-traffic revision. No additional cloud queries are justified to re-prove this evidence.

## Strict protection invariant (expected before B1)
Project `oldx-staging`; region `asia-south1`; service `oldx-owner-read`.
- Root 100% on **exact** `oldx-owner-read-00001-8kr`, untagged, and no root share on other revisions.
- Existing tags preserved exactly: `healthcheck` → `oldx-owner-read-00002-tid`, `step3rc14` → `oldx-owner-read-00003-nus` (no hyphen in `step3rc14`).
- Prospective new tag `ownerreadv2` is **not yet created**. New B1 revision name cannot be inferred or hard-coded ahead of deployment.
- All other tags/traffic entries must be independently considered, and any unexpected entry or tag is a **STOP**, not an invitation to erase it.
- No public IAM grant, activation flag, Firestore/Auth/Logging request, or traffic migration authorized.

## R1: remove only the new tag — DRAFT, NOT EXECUTED
**Prerequisite:** later separate owner approval for B1 and *separate specific* approval for R1. B1 must have actually created exactly one new, uniquely identified revision and `ownerreadv2` tag on that revision, with zero main traffic. Never run R1 now when the tag does not exist.

**Fresh immediate preflight (read-only, limited to newly authorized window):** verify project/account/region/service; service generation/resourceVersion or etag if available; current latest ready revision and full traffic entries; observed new revision digest/config/flags; exactly one `ownerreadv2` tag associated with the approved revision; old 100% root revision and both original tags unchanged; no concurrent drift; permissions and stopped requests. Make a private, access-restricted pre-mutation snapshot with any secrets redacted from publication.

**Candidate provider operation, not an instruction to paste yet:**
`gcloud run services update-traffic oldx-owner-read --project=oldx-staging --region=asia-south1 --remove-tags=ownerreadv2`
This specific supported flag targets one tag; **do not combine it with `--clear-tags`, `--set-tags`, `--to-latest`, or traffic reallocation**. The CLI alone is not a compare-and-swap: a fresh preflight and supervised single attempt are necessary. If mismatch or unknown command outcome, STOP rather than automatic retry. Separately confirm post-operation exact original main and both old tags; do not assume success from exit status alone. A removed tag does not necessarily delete or stop the revision.

## R2: preserve or restore main routing — DRAFT, NOT EXECUTED
R2 is **conditional**: if main remains 100% on original `00001-8kr` and original tags are exact, **NO TRAFFIC WRITE** is the safest action. Always check after R1 or any incident. If B1 changed root traffic (unexpected), classify as incident; stop and obtain a **separately approved, current-state-based** restoration action. Do NOT blindly replay an old YAML, or imply that restoring traffic restores service template/config/IAM. A targeted `--to-revisions=oldx-owner-read-00001-8kr=100` is only a **review candidate** after verifying its behavior on the exact current service, handling tagged 0%-main entries and new revision; subsequent exact tag verification is mandatory. Never use `--to-latest` or `--clear-tags`.

Any full-service YAML replacement may create a revision and overwrite concurrent changes; it is **not** the default R2. If required at all, treat it as a different separately consented, reviewed transaction, based on the currently authorized safe restore artifact, current drift check, and written approval. Do not automatically execute either proposed R2 approach.

## Before B1/rollbacks (still OPEN)
1. C4 owner disposition of 1 CRITICAL + 5 HIGH frozen scanner findings; no scanner zero claim.
2. G2 trust/custody of exact candidate and signature; independent original builder provenance not automatically proven by local signing.
3. G4 IAM effective access: service/project/parent inherited invokers and other-database boundaries; existing 2 Owners/1 Editor are not exclusive invoker proof.
4. G8 all-provider financial exposure/STOP: Cloud Run-only cap does not bound Registry, Logging, Firestore/Auth; explicit owner risk/cost decision.
5. Explicit B1 **DEFAULT-OFF/503-only**, 0%-main, private, finite supervised trial scope; one-new-revision bounds; fresh LIVE service preimage immediately before write (the 17:03 cached `$svc` is historical).
6. Separate explicit R1 and R2 approvals with budget and responsible operator. A general "ok aagal vadho" is not any live mutation authorization.

## Handoff / outcome
`C5_THREE_REVISION_READ=COMPLETE`; `R1_PLAN=SOURCE_ONLY_PREPARED`; `R2_PLAN=SOURCE_ONLY_PREPARED`; `R1_EXECUTED=NO`; `R2_EXECUTED=NO`; `B1_EXECUTED=NO`; `STEP04=HOLD`; `PRODUCTION=NO_GO`. Do not repeat C1–C5 scans/builds/signings/uploads or previously captured service/IAM/billing snapshots without a distinct justified gate.

Provider references (read-only research): https://docs.cloud.google.com/sdk/gcloud/reference/run/services/update-traffic ; https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration .
