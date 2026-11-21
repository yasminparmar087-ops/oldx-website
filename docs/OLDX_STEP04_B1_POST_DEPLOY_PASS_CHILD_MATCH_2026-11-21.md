# OLDX Step04 B1 — owner-observed post-deploy metadata PASS and immutable child digest MATCH

## 21 Nov 2026 ~18:20 IST — one-shot B1 post-deploy verification COMPLETE

**Owner Windows PowerShell screenshot** after one previously authorized private `--no-traffic --tag=ownerreadv2` Cloud Run create of `oldx-owner-read-00010-zud`. This is **reported observed output**, not a rerun of any cloud call by this document. Three exactly scoped read-only GETs, now consumed:

```text
B1_POST_SERVICE_READ=PASS
B1_POST_REVISION_READ=PASS
B1_POST_SERVICE_IAM_READ=PASS
B1_POST_OLD_MAIN_AND_TAGS=MATCH
B1_POST_NEW_TAG_ZERO_MAIN=MATCH
B1_POST_SERVICE_TEMPLATE_IMAGE_INDEX=MATCH
B1_POST_REVISION_RESOLVED_DIGEST=sha256:3150d898c8e013c833bac8b7f8adb8411023449093658d5c5c478a55d7ec28d1
B1_POST_REVISION_IMAGE=RESOLVED_DIGEST_REQUIRES_FROZEN_CHILD_MATCH
B1_POST_REVISION_ENV=EXACT_TWO_FALSE
B1_POST_REVISION_RESOURCES=CPU1_MEM512Mi_CONCURRENCY1_TIMEOUT30
B1_POST_REVISION_SCALING=MIN_ZERO_OR_UNSET_MAX_ONE
B1_POST_SERVICE_DIRECT_IAM=NO_PUBLIC_MEMBER_ONE_INVOKER
B1_POST_PARENT_EFFECTIVE_IAM=NOT_FULLY_PROVEN
B1_POST_OTHER_DATABASE_DENY=UNVERIFIED
B1_POST_HOSTED_PRODUCT_REQUESTS=NOT_PERFORMED
B1_POST_METADATA=PASS_WITH_LIMITS
```

No `STOP_B1_POST_DEPLOY_VERIFICATION` was seen in executed output; PowerShell returned to prompt. `G4A` earlier direct project/service IAM policy read is historical; this new postcheck confirmed service-level direct IAM not public and unchanged count (1). No tagged URL was opened, no Firestore/Auth data plane run or write, no IAM/billing/production/config changes made by the check itself.

## Previously frozen C2 evidence resolves the index→child digest mismatch without new scans

**Authoritative previous repo evidence:** [OLDX npm-free no-rebuild custody and C2 alignment](OLDX_STEP04_NPMFREE_NO_REBUILD_CUSTODY_ROUTE_2026-11-21.md), section “Resolved discrepancy”:
- **OCI index** pinned in B1 `--image`: `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`.
- Frozen registry **Linux/AMD64 child manifest**: `sha256:3150d898c8e013c833bac8b7f8adb8411023449093658d5c5c478a55d7ec28d1`.
- Child's separate Docker config: `sha256:a5933c5665af3aeb1190f7bd74e41308dd595d61db5eb299d64f1780d2cf9524`.
- **Actual new Cloud Run revision resolved digest is byte-for-byte identical to the frozen AMD64 child**. `B1_POST_RESOLVED_CHILD_DIGEST=MATCH`. These digest types naturally differ; do not mislabel as mismatch or rebuild/redeploy. C2 itself recorded exact local-vs-remote OCI index descriptor, ordered 10/10 RootFS Diff IDs, and child/config metadata alignment PASS WITH LIMITS.

## B1 exact scope verified / caveats

- Main 100% remains on original `oldx-owner-read-00001-8kr`; existing `healthcheck` and exact `step3rc14` tags intact. New revision `oldx-owner-read-00010-zud` under tag `ownerreadv2` is 0%-main.
- New revision exact two `false` activation flags. Resources CPU1/512Mi, concurrency1, timeout30, min0 or unset max1. Direct service IAM policy has no public principal, one named Invoker; `ingress=all` does not itself prove public access.
- Source-level OFF-only Product API guard previously reviewed and original C4 1 CRITICAL + 5 HIGH scanner remains; frozen analysis NOT a new scanner PASS or guarantee of no vulnerabilities.
- Project Owner/Editor authorized principals may still invoke; service/project effective IAM exclusivity NOT proven. Project parent `NO_PARENT_REPORTED` was previously observed. Other Firestore database effective denied access UNVERIFIED and Product API enabled route NO-GO.
- `--no-deploy-health-check` prevents default deploy-time probe; **it does not guarantee never started, no charges or uninvokable tagged URLs**.
- New service latest template/revision persists even if later R1 tag is removed. R1 does not undo template image or delete revision; R2 is traffic NO-OP if original main 100% is intact.
- Existing owner C4 six severe CVE, G8 residual costs and B1/R1/R2 conditional consents cover this exact **one supervised private OFF-only trial**, not production, enabled data plane or blank-check future deployments.

## Next precise action — FINISH supervised B1 without repeated discovery

The owner-approved **R1 tag-only removal** is appropriate when ending this short-lived private tagged trial. Before any tag mutation, inspect a **fresh exact service traffic preimage** (main `00001-8kr=100%`, `healthcheck`→`00002-tid`, `step3rc14`→`00003-nus`, `ownerreadv2`→`00010-zud` 0%-main, no unexpected entries) and ensure operator is prepared. Then run one supervised `gcloud run services update-traffic ... --remove-tags=ownerreadv2` only; follow with one targeted service read to verify main and old tags remain. **R2 is NO-OP** while old main/tags remain, as already confirmed. If any mismatch, STOP, no automatic reruns/rollbacks. Removal does NOT remove latest revision and must not be claimed as full rollback. Do not open tagged URL or invoke any hosted endpoint. No G4A/C5 new check/scan/build/re-sign.

`B1_DEPLOYMENT=CREATED_ONCE_SUCCESS`
`B1_POST_METADATA=PASS_WITH_LIMITS`
`B1_POST_RESOLVED_CHILD_DIGEST=MATCH_PREVIOUS_FROZEN_C2`
`B1_OFF_ONLY_TRIAL=VERIFIED_WITH_LIMITS`
`R1_TAG_REMOVAL=NOT_EXECUTED`
`R2_TRAFFIC_RESTORE=NOT_NEEDED_AS_OF_18_20_SNAPSHOT`
`STEP04=HOLD`
`PRODUCTION=NO_GO`
