# OLDX Step 04 — G4-A fresh read-only pre-B1 evidence, OWNER-OBSERVED PASS WITH LIMITS

## 21 November 2026 ~17:48 IST — completed, do not rerun

**Primary evidence:** Owner's actual Windows PowerShell screenshot in OLDX conversation, after running the exact single-block read-only script from [G4-A guarded preflight](OLDX_STEP04_G4A_SINGLE_READONLY_PREB1_GUARD_2026-11-21.md). Terminal returned to the `PS ...>` prompt after printing `G4A_READ_ONLY_PREB1=COMPLETE_WITH_LIMITS`. The transcript shows no `STOP_G4A_READ_ONLY_PREFLIGHT` in the executed output and no deployment command. Screenshot is the primary result; this record sanitizes it and does **not** re-run the calls.

```text
G4A_SERVICE_GET=PASS
G4A_SERVICE_IAM_GET=PASS
G4A_PROJECT_IAM_GET=PASS
G4A_PRIVATE_DIRECT_POLICY_GUARD=MATCH
G4A_TRAFFIC_PREIMAGE=MATCH
G4A_MAIN=oldx-owner-read-00001-8kr:100
G4A_EXISTING_TAGS=healthcheck,step3rc14
G4A_LATEST_TEMPLATE_TWO_ACTIVATION_FLAGS=EXACT_FALSE
G4A_SERVICE_INVOKER_MEMBERS=1
G4A_PROJECT_OWNER_MEMBERS=2 EDITOR_MEMBERS=1 PROJECT_INVOKER_MEMBERS=0
G4A_PARENT_INHERITED_IAM=NOT_VERIFIED
G4A_OTHER_DATABASE_EFFECTIVE_DENIAL=NOT_VERIFIED
G4A_EXCLUSIVE_OWNER_INVOCATION=NOT_PROVEN
G4A_DEPLOYMENT=NOT_STARTED
G4A_READ_ONLY_PREB1=COMPLETE_WITH_LIMITS
```

## Meaning and limitations

1. The three **distinct new GETs** succeeded in the same PowerShell run: `gcloud run services describe`, `gcloud run services get-iam-policy`, and `gcloud projects get-iam-policy` with owner-selected account/project/region. This is a point-in-time **current direct-policy and service-template drift check** at observed run time; not a permanent live lock.
2. Exact original root 100% traffic remains on revision `oldx-owner-read-00001-8kr`; the exact old tags `healthcheck` → `00002-tid` and `step3rc14` → `00003-nus` remain. The future `ownerreadv2` revision/tag is not proven created by this command.
3. Service latest *template* image, expected runtime SA, ingress, IAM-invoker-check annotation and **both exact FALSE product flags** satisfied the prepared guard; **do not infer the old 100%-traffic revision has the same code/flags** (C5 previous observed those old flags MISSING).
4. Direct service/project IAM policies show zero public members under the guard and unchanged member counts. **Do not call the service exclusive to Yasmin**: project Owner=2 / Editor=1, parent org/folder inheritance and custom grants/groups have not been exhaustively inspected; the IAM check could have other effective grants. No G4-B other-Firestore-database denied-access proof.
5. No source/code tests, Grype scan, OCI build, Registry push, signing, Firebase I/O, IAM/billing mutation, or Cloud Run deployment occurred as part of the reported preflight.

## Owner authorizations already recorded; decision still pending

- **C4:** Owner accepted residual six severe CVEs *only* for one **private, 0%-main, DEFAULT-OFF/503-only** staging trial. Original scanner 1 CRITICAL/5 HIGH unchanged.
- **G8:** Owner accepted remaining side-provider financial exposure *only* for that same limited private trial, not a guaranteed provider-wide hard cap.
- **B1:** Owner gave **conditional consent** for one new private `ownerreadv2` 0%-main revision, conditioned on G4-A and remaining limitations/rollback readiness. This read meets the **fresh direct-policy check with limits**, not all execution prerequisites.
- **R1/R2:** Individual execution approval **NOT YET RECORDED**; rollback plan source-only exists [here](OLDX_STEP04_C5_R1_R2_ROLLBACK_GUARD_PLAN_2026-11-21.md).
- **G2:** owner-local C3 signed OCI index `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79` cryptographically verified previously; independent trusted original-builder provenance remains UNKNOWN. No new verification required just to record this run.

## Next actionable gate, without repeating this check

**Prepare exact, reviewable B1 one-try execution-and-recovery packet** with offline/source-only safeguards: no existing 100%-main or old tag edits; no enabled flags; no service IAM changes; one private tagged 0%-main immutable npm-free image; finite time and zero data-plane requests; verify the planned Cloud Run command's traffic/tag semantics; pre/post receipts plus fail-closed STOP. Ask owner for explicit R1 tag-only removal and R2 conditional routing restoration approvals. If the actual write is not immediate and this ~17:48 evidence becomes stale, an **immediate fresh service-state drift check** is required at execution time rather than assuming this screenshot is a compare-and-swap. The historic G4-A script and C5 revision-description tests are **consumed; never rerun solely for another PASS**.

`G4A_FRESH_DIRECT_POLICY_PREFLIGHT=PASS_WITH_LIMITS`
`G4A_OWNER_SCREENSHOT_EVIDENCE=RECORDED`
`G4A_PARENT_INHERITED_IAM=NOT_VERIFIED`
`G4A_OTHER_DB_DENY=NOT_VERIFIED`
`C4_OWNER_OFF_ONLY_RISK_ACCEPTED=YES_WITH_LIMITS`
`G8_OWNER_OFF_ONLY_FINANCIAL_RISK_ACCEPTED=YES_WITH_LIMITS`
`B1_OWNER_CONDITIONAL_CONSENT=YES`
`B1_EXECUTION=NOT_STARTED`
`R1_R2_EXECUTION_CONSENT=NOT_RECORDED`
`STEP04=HOLD`
`PRODUCTION=NO_GO`
