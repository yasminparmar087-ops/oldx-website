# OLDX Step 04 — R1 owner-observed tag-only cleanup COMPLETE_WITH_LIMITS

Date: 21 Nov 2026 ~18:33 IST. Evidence: owner-provided Windows PowerShell terminal screenshot of the **previously approved** and **one-time executed** R1 guarded block from [the prepared R1 packet](OLDX_STEP04_B1_R1_TAG_ONLY_GUARDED_EXECUTION_2026-11-21.md).

## New completed observation (DO NOT RERUN)

The screenshot visibly contains the following actual console output (not merely a script pasted into a console):

```text
R1_FRESH_PREIMAGE=MATCH
R1_REMOVE_ONLY_TAG=ownerreadv2
OK Updating traffic... Done.
OK Routing traffic...
Done.
Traffic:
  100% oldx-owner-read-00001-8kr
    0% oldx-owner-read-00002-tid
       healthcheck: [tag URL shown by CLI; omitted]
    0% oldx-owner-read-00003-nus
       step3rc14: [tag URL shown by CLI; omitted]
R1_WRITE_CLI=EXIT_ZERO
R1_NEW_TAG=ABSENT
R1_OLD_MAIN_AND_TAGS=PRESERVED
R2_TRAFFIC_RESTORE=NOT_REQUIRED_NO_OP
R1_TAG_ONLY_REMOVAL=COMPLETE_WITH_LIMITS
PS C:\\Users\\Yasmin Parmar>
```

**Judgment:** The fresh exact R1 preimage guard PASSED; the one owner-run Cloud Run `update-traffic --remove-tags=ownerreadv2` command reported success; the one post-write read-only service metadata check passed. Original `oldx-owner-read-00001-8kr` remains 100% main traffic, old tags `healthcheck` -> `00002-tid` and `step3rc14` -> `00003-nus` preserved. New `ownerreadv2` tag absent in post-check. R2 is **NO-OP** and must not run. The screenshot showed printed Cloud Run URLs; that is **not evidence of a hosted URL invocation**. No authenticated Product/Firestore/health request is asserted.

## Exact cumulative state

- B1 was already deployed **once** on private staging: `oldx-owner-read-00010-zud` as 0%-main, `ownerreadv2` tag; B1 3 focused post-GETs = `PASS_WITH_LIMITS`. New revision's resolved Linux/AMD64 child digest `sha256:3150d898c8e013c833bac8b7f8adb8411023449093658d5c5c478a55d7ec28d1` matches the frozen C2 child under OCI index `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79` [B1 evidence](OLDX_STEP04_B1_POST_DEPLOY_PASS_CHILD_MATCH_2026-11-21.md).
- **R1 executed once and verified COMPLETE_WITH_LIMITS**. R1 changes tag routing only. It does **not** delete revision `00010-zud`, revert `latestReadyRevisionName`, restore the prior service template image/env, or independently certify no charges.
- C4 original severe scan results (1 CRITICAL + 5 HIGH) remain *unfixed* with only narrowly accepted OFF-only owner risk. Independent trustworthy original builder provenance remains UNKNOWN; G2 not fully PASS.
- G4 effective/exclusive Cloud Run IAM and Firestore other-database access denial are NOT PROVEN. Source-level flags OFF do not authorize enabling API. G8 residual costs accepted only within prior private OFF-only scope.
- `STEP04=HOLD`, `PRODUCTION=NO_GO`, `R2=NO_OP`. Do not turn on Product/Firestore data plane, make IAM grants, or route new revision to production/main as a result of this receipt.

## Future-chat continuation — required

**Start at this checkpoint, not at an earlier B1 or R1 prompt.** Read `AGENTS.md`, `docs/OLDX_CURRENT_HANDOFF.md` top entry, 15-step plan, and this receipt. No repeat B1 deployment, B1 post GETs, R1 tag cleanup, C1–C5 registry/build/sign/Grype, prior IAM/billing/CI checks for reassurance. Next Step04 work: separately analyze/close distinct remaining G2 independent builder provenance/security-disposition and G4 effective IAM / other-DB denial for any future enabled rollout, with narrowly scoped new evidence and owner approval where live writes/data-plane actions would be needed. Preserve original main 100%, original tags and all existing product features. Do not conflate private OFF-only test completion with production GO.

Recorded by ChatGPT from the user-shared screenshot. **No new cloud operation was run by this documentation change.**
