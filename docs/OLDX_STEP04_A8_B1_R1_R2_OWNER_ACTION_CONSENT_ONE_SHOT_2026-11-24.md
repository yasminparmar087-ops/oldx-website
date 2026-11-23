# OLDX Step 04 — NEW A8 private OFF-only B1/R1/R2 action-level approval and one-shot handoff

Date: **24 Nov 2026**, continuation of the actual owner screenshot with `A8_PREWRITE=PASS_WITH_LIMITS`. Repo `yasminparmar087-ops/oldx-website`; ONLY branch `security-hardening-review`. This document is **an authorization ledger and source-only runbook, not proof of an A8 deployment**.

## Fresh exact owner consent — B1, R1 and R2, each separate

The owner explicitly answered **"ha manjuri chhe"** to the three-item question following one real owner-operated A8 Section 3 prewrite. The three consented actions, limited to **one** A8 private, 0%-main, default-OFF trial supervised for up to **20 minutes**, are:

1. **A8 B1:** One Cloud Run revision deployment only, `oldx-staging`/`asia-south1`/`oldx-owner-read`, pinned immutable A8 image `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`; tag `a8off23nov`, `--no-traffic`, activation/ADC EXACT FALSE, runtime SA `oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com`, CPU1/512Mi/concurrency1/timeout30/min0/max1, CPU throttled, no deploy health check. Explicitly preserve `00001-8kr=100%` main and existing `healthcheck`/`step3rc14` tags. No public access/IAM change. Existing tag might remain callable by authorized principal and incur costs.
2. **A8 R1:** Once actual new A8 tagged revision has been independently verified, and only after a separate fresh preimage confirms correct tag/revision and old root/tags, allow **removing ONLY `a8off23nov`**. Tag-only cleanup does not delete the revision, remove template, guarantee zero cost, or restore old latestReadyRevisionName. Do not use old consumed `ownerreadv2` R1 script.
3. **A8 R2:** **NO-OP** if old main traffic remains `00001-8kr=100%` and old tags intact. On unexpected main/tag drift: STOP, inspect precise current state and ask an additional **incident-specific** consent before any correction. The current owner approval is **NOT** blanket permission for `--to-latest`, broad traffic replacement or old template restoration.

## Prewrite, current proof and hard stops

One actual screenshot on **24 Nov ~00:25 IST** showed `A8_PREWRITE_SERVICE_AND_TRAFFIC=PASS`, `A8_PREWRITE_EXISTING_LATEST=00010_ZUD`, `A8_PREWRITE_OLD_ROOT_AND_TAGS=PRESERVED`, `A8_PREWRITE_NEW_TAG=a8off23nov_ABSENT`, `A8_PREWRITE_DIRECT_IAM=NO_PUBLIC_ONE_NAMED_INVOKER`, `A8_PREWRITE_INHERITED_IAM=UNVERIFIED`, `A8_PREWRITE_EFFECTIVE_OTHER_DB_DENIAL=UNVERIFIED`, `A8_PREWRITE=PASS_WITH_LIMITS`, `A8_NEW_CLOUD_RUN_DEPLOY=NONE`. This **consumed** the earlier full read-only prewrite. The new deployment script carries only a **necessary immediate fresh state/permission drift guard** before its write, not a repeat of old Grype, signed build, Docker runtime, Cloud Asset, Billing, B1 or R1 investigations.

**Owner released guarded exact A8 B1 script:** [`scripts/step04-a8-b1-owner-supervised-one-shot.ps1`](../scripts/step04-a8-b1-owner-supervised-one-shot.ps1). Source audit facts:
- Uses **current** 2-read Cloud Run service/direct IAM drift guard, checks current `00010-zud` latest, old npm-free image, 2 FALSE vars, no secret/volumes, old 100% root+tags, absence of old/new trial tags, direct no-public and one Invoker. On mismatch STOP and DO NOT deploy.
- Uses `FileMode.CreateNew` local **one-shot marker** `oldx-step04-a8-b1-attempt-20261124.marker` before actual Cloud Run write; prevents silent replay after uncertain CLI results. Do not delete marker to force a second deploy. This marker itself is a local file write and is not a Cloud action.
- Executes **one** `gcloud.cmd run deploy` attempt with the pinned immutable **A8** digest, new distinct tag `a8off23nov`, zero main traffic, all flags above. Does NOT use `--allow-unauthenticated`, `--no-invoker-iam-check`, `--to-latest`, or broad IAM/Rules/Billing flags. Does NOT invoke a hosted URL, run data-plane or auto-run R1/R2.
- Successful CLI exit means **`A8_B1_DEPLOY_CLI=EXIT_ZERO_POSTCHECK_REQUIRED`**, not a hosted PASS. Next is a **separate one-target new-revision/service/direct-IAM sanitized postwrite verification** based on the ACTUAL new revision name and actual image digest. If the CLI fails, stalls or status is ambiguous: **STOP no automatic retry**; inspect live state before a new write.
- Operator supervises the bounded session; code DOES **NOT** guarantee automatic shutdown in 20 minutes, and the new private tagged URL **remains invokable** while present. R1 tagged cleanup must be explicitly verified and separately performed, not assumed. No unconditional cost maximum.

## Carryforward unchanged

15 distinct severe A8 Grype CVE IDs remain **OPEN** with risk recorded; BellSoft vendor-fixed package lines are not blanket signed-cure. Cloud Run inherited Owner/Editor invocation and runtime SA hypothetical other-db denial are UNVERIFIED; there is only one current `(default)` DB. Global hard ₹2,000 spend cap remains UNPROVEN. Historical npm-free B1 created `00010-zud` on DIFFERENT image and its `ownerreadv2` R1 was consumed—**do not rerun**. A8 local nonroot/readonly/no-network health200/off503 **PASS_WITH_LIMITS**, but **A8 Cloud Run hosted has not been executed as of writing**.

**No new cloud action as part of this documentation.** `A8_OWNER_RISK_SCOPE=APPROVED`; `A8_B1_R1_R2_NARROW_ACTION_APPROVAL=YES`; `A8_B1_SCRIPT=PREPARED_NOT_RUN`; `A8_B1_DEPLOY=NOT_EXECUTED`; `A8_R1=NOT_EXECUTED`; `A8_R2=NO_OP_UNLESS_NEW_INCIDENT_CONSENT`; `STEP04=ACTIVE_HOLD_ORIGINAL_EXIT`; `STEP05=NOT_AUTHORIZED`; `PRODUCTION=NO_GO`.

Official CLI sources reviewed 24 Nov 2026: https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy and https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration .


## 24 Nov 2026 ~00:37 IST — ACTUAL owner new A8 B1 one-shot CLI SUCCESS (NO R1 YET)

**Direct user screenshot from Windows PowerShell, observed text at bottom after shell prompt returned:**

```text
A8_B1_IMMEDIATE_PREWRITE=PASS_WITH_LIMITS
A8_B1_INHERITED_IAM=OWNER_ACCEPTED_LIMIT_NOT_PROVEN
A8_B1_A8_IMAGE=EXACT_PINNED_NEW_DIGEST
A8_B1_OLD_MAIN_AND_TAGS=PREWRITE_PRESERVED
A8_B1_ONE_SHOT_DEPLOY=BEGINNING
Deploying container to Cloud Run service [oldx-owner-read] in project [oldx-staging] region [asia-south1]
OK Deploying... Done.
  OK Creating Revision...
Done.
Service [oldx-owner-read] revision [oldx-owner-read-00012-vib] has been deployed and is serving 0 percent of traffic.
A8_B1_DEPLOY_CLI=EXIT_ZERO_POSTCHECK_REQUIRED
A8_B1_NEW_TAG=a8off23nov_NOT_YET_VERIFIED
A8_B1_POSTWRITE_TRAFFIC_AND_IMAGE=NOT_YET_VERIFIED
A8_B1_HOSTED_HTTP=NOT_INVOKED
A8_B1_R1_TAG_CLEANUP=NOT_EXECUTED
A8_B1_R2=NO_OP_UNLESS_DRIFT
A8_B1_NO_AUTOMATIC_RETRY=TRUE
PS C:\Users\Yasmin Parmar>
```

**Judgment:** The new immutable A8 image was submitted in the exactly approved one-shot command after its immediate service/direct-IAM drift guard passed; Google Cloud Run CLI completed zero-exit and reported **NEW revision `oldx-owner-read-00012-vib`, 0% main**. Console printed a reachable tagged URL `a8off23nov`; **do not reproduce public URL**, and its presence is not a hosted HTTP invocation or proof of public anonymous access. Service/revision/traffic/IAM postwrite metadata is **NOT YET independently verified**. No new A8 host URL invoke or Firebase data-plane test occurred; tag R1 and conditional R2 have NOT run. Private local one-shot marker was created by guarded script; DO NOT delete or rerun B1. This is a **NEW A8 distinct deployment**, NOT repeat of old 21 Nov `00010-zud` B1.

**Next minimum work:** ONE fresh owner-operated Cloud Run postwrite service describe + **exact NEW revision `00012-vib` describe** + direct service IAM read to verify root `00001-8kr=100%`, both old tags and new `a8off23nov` on `00012-vib` 0%-main, service A8 immutable image identity, revision's resolved image (may be child manifest vs index and must not mislabel mismatch), exact two false flags, runtime SA, no volume/secrets, CPU/RAM/timeout/concurrency/scaling, no direct public IAM. Only after those independent checks and fresh exact state does authorized R1 remove **just** `a8off23nov` tag once, with one post-R1 service state check. R2 NO-OP unless main unexpectedly drifts; then STOP and require new incident-specific authorization before traffic restore. No repeated B1, SLSA, Grype, Build, local runtime or database/old IAM snapshot. `STEP04=ACTIVE_HOLD_ORIGINAL_EXIT`, `PRODUCTION=NO_GO`.


## 24 Nov 2026 — NEXT prepared: ONE combined A8 postwrite CHECK then authorized R1 new-tag cleanup (NOT EXECUTED)

Owner-screenshot B1 CLI success for `oldx-owner-read-00012-vib` is already recorded above. A separate script has now been **created and fetched back from the review branch**, static safety predicates PASS: [`scripts/step04-a8-postcheck-and-r1-cleanup-once-20261124.ps1`](../scripts/step04-a8-postcheck-and-r1-cleanup-once-20261124.ps1). The file is **NOT a B1 redeploy**. It does one fresh postwrite service/EXACT new revision/direct service IAM read, verifies current `00012-vib`, exact A8 signed image on service latest template, revision resolved repository/digest format, expected service account, EXACT FALSE/FALSE, no secret volumes, scale/resources, 100% old root+both previous tags, new `a8off23nov` tag attached to `00012-vib` 0%-main, service IAM no public member/one direct Invoker. It explicitly does not treat a child manifest digest as equivalent to the original OCI index unless independently reconciled.

**Only if all checks pass**, script prints the preimage gates, creates one local exclusive R1 attempt marker, executes ONE owner-approved `gcloud run services update-traffic oldx-owner-read --remove-tags=a8off23nov`, and verifies fresh service traffic now consists of the original 100% main and precisely the old `healthcheck` / `step3rc14` tags. R2 remains **NO-OP** absent drift; old `00010-zud`/old `ownerreadv2` never touched. On any STOP, do **not** re-run script or delete marker; reconcile actual current state. R1 cannot delete latest revision/template or guarantee cost=0. No tagged URL is invoked, no ADC/data-plane, IAM, billing, Rules, Artifact Registry, Grype or build operations. It is intended for the already authorized single supervised trial, and **the operator must run it explicitly; nothing has been automatically sent to Cloud Run by GitHub**.

Current: `A8_B1_DEPLOY_CLI=SUCCESS_ONCE`; `A8_POSTWRITE=PREPARED_NOT_EXECUTED`; `A8_R1=PREPARED_NOT_EXECUTED`; `A8_R2=NO_OP_UNLESS_DRIFT`; `STEP04=ACTIVE_HOLD`; `PRODUCTION=NO_GO`.


## 24 November 2026 ~00:44 IST — ACTUAL A8 00012-vib postwrite PASS and guarded R1 tag-only cleanup COMPLETE_WITH_LIMITS

**Evidence:** actual user-provided Windows PowerShell screenshot, not a simulated or repeat cloud call by this document. Owner ran the EXACT NEW A8 one-shot `scripts/step04-a8-postcheck-and-r1-cleanup-once-20261124.ps1`. Console visibly returned to `PS C:\Users\Yasmin Parmar>`, with no STOP after the output lines:

```text
A8_POST_SERVICE_REVISION_IAM=PASS_WITH_LIMITS
A8_POST_NEW_REVISION=00012_VIB
A8_POST_SERVICE_IMAGE=EXACT_SIGNED_A8_INDEX
A8_POST_REVISION_IMAGE=EXACT_A8_DIGEST
A8_POST_NEW_TAG_0_PERCENT=VERIFIED
A8_POST_OLD_ROOT_AND_TAGS=VERIFIED
A8_POST_BOTH_FLAGS=EXACT_FALSE
A8_POST_DIRECT_IAM=NO_PUBLIC_ONE_NAMED_INVOKER
A8_POST_INHERITED_IAM=UNVERIFIED
A8_POST_OTHER_DB_DENIAL=UNVERIFIED
A8_POST_HOSTED_HTTP=NOT_INVOKED
A8_R1_EXACT_PREIMAGE=PASS
A8_R1_REMOVE_ONLY_TAG=a8off23nov
OK Updating traffic... Done.
OK Routing traffic...
Done.
A8_R1_WRITE_CLI=EXIT_ZERO
A8_R1_NEW_TAG=ABSENT
A8_R1_OLD_100_PERCENT_MAIN_AND_TAGS=PRESERVED
A8_R1_TAG_ONLY_CLEANUP=COMPLETE_WITH_LIMITS
A8_R2_TRAFFIC_RESTORE=NO_OP_NOT_REQUIRED
A8_NEW_REVISION_AND_LATEST_TEMPLATE=RETAINED_NOT_ROLLED_BACK
A8_STEP04=HOLD_PENDING_G2_G4_G8
A8_DEPLOY_R1_RETRY=PROHIBITED
```

**Verified actual new A8 B1+postcheck+R1 cumulative outcome:** the owner-deployed `oldx-owner-read-00012-vib` uses the exact *new* signed A8 private index `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`; new revision metadata's image matches the exact A8 digest (no child/index discrepancy for this observation). Two feature flags are EXACT FALSE, expected resources/scaling, no secret volumes; direct IAM has no public principal and one direct Invoker; **not** evidence that inherited effective IAM exclusivity is proven. Before R1, `a8off23nov` was on new revision at 0%-main and original `oldx-owner-read-00001-8kr=100%`, `healthcheck`/`step3rc14` intact. One owner-approved `update-traffic --remove-tags=a8off23nov` command exited 0 and one post-R1 service read verified **only old root 100% and two old tags remain**. `R2=NO_OP_NOT_REQUIRED`. The CLI printed URLs; this is not evidence the owner invoked an HTTP endpoint and URLs/tokens are intentionally not recorded here.

**Important limits:** R1 is tag-only cleanup. **A8 `00012-vib` revision and new latest service template still exist**, although trial tag is absent, and no automatic full template rollback or deletion was authorized/executed. Fresh private HTTP 503 response **NOT tested**, nor authenticated runtime IAM/Firestore data-plane. Current inherited invoker model, hypothetical other-database negative denial (no existing second DB), 15 severe Grype CVE risk disposition and whole-provider hard INR cost stop are still UNVERIFIED or unresolved. Acceptances were scoped to this now **consumed** private default-OFF trial; do not transfer to enabled product or production.

**Strong NO REPEAT checkpoint:** `A8_B1_DEPLOY=CLI_SUCCESS_ONCE`; `A8_POSTCHECK=PASS_WITH_LIMITS_CONSUMED`; `A8_R1_TAG_ONLY=COMPLETE_WITH_LIMITS_CONSUMED`; `A8_R2=NO_OP`; `A8_HOSTED_REQUEST=NONE`; `A8_REVISION_TEMPLATE_RETAINED=YES`; `A8_LOCAL_ONE_SHOT_MARKERS=RETAIN_DO_NOT_DELETE`; `STEP04=ACTIVE_HOLD_ORIGINAL_EXIT`; `STEP05=NOT_AUTHORIZED`; `PRODUCTION=NO_GO`. **Do not** rerun Cloud Build, SLSA, Grype, local runtime, prewrite, B1, A8 postwrite, R1 or old G4/DB/billing reads just to collect equivalent evidence.

**Next material Step 04 decision:** The narrow OFF-only hosted *metadata/trial* is finished. What remains is the explicit disposition of G2 15 severe CVEs, effective G4 inherited invoker and Firestore permissions/other-db limitation, and G8 bounded spending/STOP/rollback. Consider either formally risk-accepted **original Step04 technical exit with quantified remaining limitations** only if independent requirements are genuinely met, or the separately owner-approved decision-only administrative handoff without pretending any security clearance. Neither route is yet approved here. Fresh hosted HTTP, enabled API, IAM/billing and production actions require distinct approval and do not follow automatically from this complete R1.
