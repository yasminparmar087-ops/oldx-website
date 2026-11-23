# OLDX Step 04 after A8 — exact technical-exit reality and owner option A/B choice

**24 Nov 2026, ~01:19 IST — source-only; NO cloud operation, no owner change of the original Step04 exit.** Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. This **NEW post-A8 checkpoint** supersedes the obsolete factual state of 23-Nov Task23 option discussions: as of 24 Nov, the actual signed A8 image has been hosted privately and removed from the tag, and all THREE owner G2/G4/G8 *limited* risk decisions are now recorded. This is a decision document, NOT a new test, an exit acceptance, or release GO.

## 1. Exact owner-locked requirements versus actual completed evidence

**Original Step04 exit from `docs/OLDX_SINGLE_EXECUTION_PLAN_2026-11-13.md` Section 0:**
> Independently authorize and evidence a private tagged staging revision, immutable source/image and real IAM/Rules/invoker/default-OFF 503, current gross-cost STOP and independent verified R1/R2 recovery. A default-OFF B1 alone cannot prove data-plane Firestore CREATE/UPDATE or cross-DB denial; keep this explicit remaining gate without silently moving or waiving it.

| Original technical gate | 24 Nov actual evidence | Remaining claim/status |
|---|---|---|
| Immutable source/image builder/revision | **PASS_WITH_LIMITS**: one signed A8 Cloud Build/SLSA source/subject/builder verification for `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`. Real private Cloud Run A8 `oldx-owner-read-00012-vib` deployed ONE time at 0%-main; postwrite service AND revision image exactly match new A8 digest. | **CONSUMED**. Do not rebuild, re-sign, rescan, redeploy or repeat metadata for another pass |
| NEW A8 live default-OFF container logic | Local isolated nonroot/network-none/read-only A8 `GET /healthz=200`; protected `POST /api/staging/marketplace/owner=503` PASS_WITH_LIMITS. Actual A8 hosted flags are both `false` and resources/SA verified. | **NEW A8 hosted HTTP 503 not actually invoked/tested**; thus original hosted receipt missing. Do not confuse old 100%-main service with new A8 |
| Private IAM/least privilege | Actual postwrite direct service IAM zero public members + one named Invoker, IAM check not disabled. Historic project two Owners and one Editor potentially invoke. Corrected single Cloud Asset runtime SA allow analysis: one exact conditional `(default)` DB binding for 4 entity perms in that query, zero unconditional in that query. Exactly one real default DB, zero others. | **Effective exclusive Invoker and hypothetical other-DB denial still UNVERIFIED**; conditions + direct membership are not full effective proof |
| Rollback | A8 new `a8off23nov` tag removed in one owner-approved R1, post-R1 service read confirmed old `00001-8kr=100%` root with `healthcheck` and `step3rc14` old tags intact, R2 NO-OP. | **R1 COMPLETE_WITH_LIMITS**; tag-only removal retains A8 `00012-vib` revision/latest service template, not full image/template rollback |
| Security CVEs | Grype 46 matches, 15 distinct severe IDs; vendor 7 fixed-version candidates + 2 disputed + 1 SQLite CLI-only + 5 BellSoft OpenSSL affected source-line; actual bounded code path reviewed. Owner **G2_ACCEPTED_WITH_LIMITS current OFF-only**. | Not patched/unreachable proof, cannot transfer to enabled API/production |
| G4 owner decision | Owner **G4_ACCEPTED_WITH_LIMITS for existing OFF-only A8** potential inherited access and no non-default DB test. | Not a technical G4 PASS; enabled real authorization must be verified later |
| Gross-cost STOP | Owner **G8_ACCEPTED_WITH_LIMITS** current default-OFF; ₹1,000 pre-new-paid-operation manual review/STOP trigger, ₹2,000 planning/risk-budget goal, service-only cap+alerts. | **Guaranteed all-service ₹2,000 hard stop NOT available/NOT PROVEN.** Doesn't become PASS by owner acceptance |
| Step04 / Step05 / prod | Current source and operator screenshots | **Step04 original exit ACTIVE_HOLD**, `03/15 DONE`, Step05 NOT AUTHORIZED, production NO-GO |

Current exact source baselines: [actual signed A8 B1/postwrite/R1](OLDX_STEP04_A8_B1_R1_R2_OWNER_ACTION_CONSENT_ONE_SHOT_2026-11-24.md); [G2 actual owner acceptance](OLDX_STEP04_G2_OWNER_LIMITED_RISK_ACCEPTANCE_2026-11-24.md); [G4 actual owner acceptance](OLDX_STEP04_G4_DEFAULT_OFF_IAM_OWNER_DECISION_PROPOSAL_2026-11-24.md); [G8 actual owner acceptance](OLDX_STEP04_G8_POST_A8_GROSS_COST_STOP_OWNER_DECISION_PROPOSAL_2026-11-24.md); [G2/G4/G8 consolidated ledger](OLDX_STEP04_G2_G4_G8_POST_A8_TRIAL_RISK_DISPOSITION_2026-11-24.md).

## 2. Technical-path A — preserve original Step04 exit unchanged (owner's previous baseline)

**Strict result remains HOLD.** To improve *one* distinct gap, an **additional** operator-supervised new tagged live HTTP test of the already deployed `00012-vib` might be separately authorized. This is NOT a B1 repeat, because no rebuild/deploy/revision creation would be needed; it is a new hosted request demonstration against the exact A8 revision and new temporary tag. HOWEVER the earlier A8 tag `a8off23nov` has ALREADY BEEN REMOVED. **Cloud Run documented routing semantics**: an untagged 0%-main revision cannot be selected via ordinary service URL; service URL still routes to historic old `00001-8kr=100%`. The only tag safe path is **a FRESH UNIQUE tag** for `00012-vib`, checked as absent, tied to this exact revision at 0%, with root/old tags unchanged. Using `--set-tags` can replace existing tags; use `--update-tags` (add one only), NOT `--to-latest`, `--clear-tags`, or a full redeploy.

**Not authorized or executed by this packet:** one new unique A8-only tagged traffic write, then **finite** hosted data-plane HTTP requests (at most one unauthenticated access-denial observation; one authenticated GET `/healthz` expected 200 and one authenticated POST `/api/staging/marketplace/owner` expected 503), then ONE guarded removal of ONLY the new tag and independent root/tag verification. Before any such trial: an exact fresh owner-approved **cost preflight** under ₹1,000 manual review threshold with expected gross all-provider costs/time/recovery and explicit action-level write+request+R1 consent. Actual owner ID token must be protected in memory, **never logged/pasted/reproduced**; use Cloud Run **base service URL as ID-token audience** even when calling a traffic-tag URL. The unauthenticated result proves only that specific request denied (401/403 depending frontend), not that all project Owners/Editors lack permission. Request count/duration and stage are bounded. **The tag is callable by authorized principals even when 0% main** until removed. Complete template rollback/registry cleanup must not be inferred from tag-only removal.

Even after such a hosted 503 result, **effective G4 inherited Invoker + hypothetical other DB denial remain UNVERIFIED and all-provider cost hard ₹2,000 guarantee remains unsupported**. A genuinely strict original technical Step04 completion CANNOT be declared solely by this hosted probe.

**Google authoritative descriptions current 24 Nov:**
- https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration (traffic tags target a 0% revision without root traffic migration)
- https://docs.cloud.google.com/sdk/gcloud/reference/run/services/update-traffic (`--update-tags` vs `--set-tags` / `--remove-tags`)
- https://docs.cloud.google.com/run/docs/authenticating/service-to-service (on traffic-tag endpoint, base service URL remains token audience)
- https://docs.cloud.google.com/run/docs/securing/managing-access (project Owners/Editors may invoke)
- https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps (service-scoped caps and latency)

This path may add one valid hosted assurance but by itself does **NOT** give Step04 `DONE`. Do not execute it merely to tick a box before deciding whether it is worth cost/new tag exposure.

## 3. Decision-only-path B — explicit revision of Step04 workflow EXIT, **NOT YET OWNER-APPROVED**

**Fastest way to preserve every real safety requirement while beginning the next source-only workstream**, since G2/G4/G8 current OFF-only owner decisions are now complete and the old live A8 private trial + R1 actually happened.

Proposed owner-authorized **administrative exit ONLY**:
`STEP04=04/15 DONE — DECISION-ONLY HOLD HANDOFF WITH TECHNICAL GATES OPEN`.
`STEP05=NEXT/SOURCE-ONLY AND BLOCKED FOR LIVE ENABLED EXECUTION`.
`PRODUCTION=NO-GO`.

This **revises only the Step04 exit definition**, like the owner-approved workflow-only exit revisions for Steps 02/03. All technical requirements stay open as **hard go/no-go gates at Step05/13 and before production**:
1. Actual hosted HTTP default-OFF 503 and independent new-tag cleanup if one is later authorized (not faked now).
2. Effective Cloud Run Invoker authorization, including project Owners/Editor, group/ancestor, IAM Deny/PAB, anonymous vs unauthorized principals, and actual private hosted authorization.
3. Runtime service-account exact Firestore `oldx-staging/(default)` least privilege, positive/negative authenticated synthetic tests and guarded cleanup, any non-default DB future negative proof IF a genuine second DB later exists, not an artificial one.
4. G2 15 scanner severe CVEs / five OpenSSL affected vendor lines and explicit NEXT ENABLED scope risk mitigation; G2 limited OFF-only consent is not a waiver for enabled.
5. G8 actual new paid-work all-provider cost review, ₹1,000 manual STOP/review trigger, ₹2,000 risk target but no guaranteed project-wide hard cap, finite calls/time, recovery and explicit owner release.
6. Preserve old main 100% and tags, no unapproved IAM, billing, Rules, Firebase/ADC, external public access, app feature reduction, or production activation.
7. Step05 live authenticated Product owner/buyer integration and tests cannot run until new scoped approvals and actual gating. Administrative closeout **is not permission to deploy or activate**.

**EXACT permission requested separately**: “I approve revising Step04 only as `DONE — DECISION-ONLY HOLD HANDOFF`, carry *all* missing Step04 security and real hosted/financial checks forward as mandatory release gates for Step05/13, and permit continuing Step05 source-only planning and code review. I do NOT declare Step04 technical PASS, accept enabled/production residual risk, or approve a new tag/request, deployment, IAM, billing, Firebase, or production action.”

No such **exact NEW Step04 exit-change consent** is recorded in the current task as of creation; the owner's ordinary “ok aagal vadho” authorizes research/planning only, not silent Step04 exit rewrite or paid Cloud action. Therefore the 15-step master tracker remains **03/15 DONE**, Step04 `ACTIVE_HOLD_ORIGINAL_EXIT`, Step05 `NOT_AUTHORIZED`, production NO-GO until owner selects.

## 4. Next response and no-repeat instruction

Ask owner for ONE direct A/B decision. Recommend **B** to avoid a new billable traffic-tag cycle that cannot resolve all remaining strict gates, while preserving all technical controls. If B approved, change only the master Step04 administrative exit and handoff/Issue #17, explicitly keep future enabled+production technical checks open. If A retained, prepare a separate exact scoped hosted-tag/cost test *only after fresh action-level approval*, with no redeploy, no repeat old R1. NO Cloud writes/tokens/billing/IAM/firebase modifications now.

**Current frozen labels:** `G2_OWNER_OFF_ONLY=ACCEPTED_WITH_LIMITS`, `G4_OWNER_OFF_ONLY=ACCEPTED_WITH_LIMITS`, `G8_OWNER_OFF_ONLY=ACCEPTED_WITH_LIMITS`, `A8_B1_POSTCHECK_R1=CONSUMED`, `A8_HOSTED_503=NOT_TESTED`, `G4_EFFECTIVE_IAM=UNVERIFIED`, `G8_ALL_PROVIDER_HARD_STOP=NOT_PROVEN`, `STEP04=ORIGINAL_TECHNICAL_EXIT_ACTIVE_HOLD`, `STEP05=NOT_AUTHORIZED`, `PRODUCTION=NO_GO`.
