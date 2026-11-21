# OLDX Step 04 — Owner approval for narrowly scoped R1/R2 rollback, 21 Nov 2026

## Owner decision — specific consent, conditional on future B1 and state

**Exact current-chat owner reply:** `ha manjuri chhe` ("Yes, approved") in response to the specific question containing two separate recovery actions:
- **R1:** Only if future B1 has created the new `ownerreadv2` traffic tag, remove **only that tag** when necessary; keep both pre-existing `healthcheck` and `step3rc14` tags unchanged.
- **R2:** **Only if original main traffic changes unexpectedly**, and only after fresh guarded evaluation of the actual live state, restore **100% of main traffic to `oldx-owner-read-00001-8kr`**, keeping preexisting tags preserved. If the original 100% root and tags are still intact, **R2 is a NO-OP**.

`R1_OWNER_CONDITIONAL_CONSENT=YES`
`R2_OWNER_CONDITIONAL_CONSENT=YES`
`B1_OWNER_CONDITIONAL_CONSENT=YES`
`B1_R1_R2_RELEASE_TO_EXECUTE_NOW=NO`
`B1_R1_R2_EXECUTED=NO`
`STEP04=HOLD`
`PRODUCTION=NO_GO`

**This approval is not blanket permission to execute a command without state verification**, disable checks, attempt repeated writes, remove old tags, restore stale full YAML, create extra revisions, delete old resources, change IAM/Billing/Firestore/Storage/Rules/DNS, invoke a hosted URL, activate product API or launch production. It is restricted to protecting the proposed **one private, 0%-main, DEFAULT-OFF/503 `ownerreadv2` B1** with previously accepted limited C4/G8 residual risks. If an unknown state, unexpected old revision/tag, concurrent edit, unknown impact, or new public access is observed, **STOP**; reconfirm exact incident-specific corrective action before any broad/multi-resource mutation.

## Previously verified preimage and current caveats

G4-A latest one-shot read-only at ~17:48 IST: `G4A_READ_ONLY_PREB1=COMPLETE_WITH_LIMITS`; original main `oldx-owner-read-00001-8kr=100%`, old `healthcheck` tag on `oldx-owner-read-00002-tid`, exact `step3rc14` on `oldx-owner-read-00003-nus`; latest service-template activation flags EXACT_FALSE; service direct named Invoker count 1; project Owners 2/Editors 1/project direct run.invoker 0; direct IAM guard MATCH. Read-only run has been consumed; do not repeat for status. **It is now historical, not a compare-and-swap lock**. Inherited parent IAM, exclusive invocation and other-database denial remain unverified, and original 100%-main revision's two feature flags were MISSING rather than proven false.

Proposed new OCI npm-free exact immutable index `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`. C3 local cryptographic bundle verification PASS, trusted independent original-builder provenance UNKNOWN. No repeat scan/build/upload/signature.

## Planned recovery sequence (not run)

1. Before single B1 attempt, operator reviews exact proposed deployment parameters and checks that new `ownerreadv2` does not already exist. Require **one fresh immediately pre-write service/traffic guard**; when relevant, recheck permissions/access materially changed since 17:48 without repeating the old 3-GET suite by habit. If anything deviates from authorized scope, STOP.
2. Keep root **100%** on `00001-8kr`; old named tags unchanged; new `ownerreadv2` only on actual freshly created B1 revision, initially **0%-main**; no public IAM/activation/env/data-plane change.
3. After an authorized B1, verify new revision exact image, no-main traffic, both false feature flags, no unauthorized IAM/ingress modifications, original old root/tags intact. Treat an ambiguous deploy or partial result as STOP, no automatic retry.
4. **R1 candidate** after fresh supervised state check: `gcloud run services update-traffic oldx-owner-read --project=oldx-staging --region=asia-south1 --remove-tags=ownerreadv2`. This removes a **tag only**, not new latest template/revision; the latter requires a separate explicit restoration plan if desired. Confirm post-state before claiming R1 success.
5. **R2 default NO-OP** when main 100% and tags remain unchanged. **Only for proven main drift**, review current traffic and exact consequences; official CLI supports candidate `--to-revisions=oldx-owner-read-00001-8kr=100`, but this is **not a generic auto-executing script**. Confirm it will not remove old tags, and use one supervised, state-specific correction. A new, broader traffic/tag mutation, uncertain revisions, service template restore or IAM change requires new independent specific approval.
6. Record separate sanitized receipts for each actually invoked action and whether stopped/no-op. No secret env, raw IAM policy, bearer tokens or credentials in public GitHub.

## Next technical task

Finalize B1 **source-only** exact one-attempt Windows PowerShell CLI command and fail-closed post-condition plan, and validate only installed CLI flag support (pure local help if needed, no cloud billing/test calls). Reconcile all **necessary** service-template/env/secret changes; review inherited IAM caveats for OFF-only/no-data-plane attempt. Do not prematurely interpret conditional B1/R1/R2 consent as unconditional deployment readiness. Keep existing 3-GET G4-A and C5 consumed snapshots as historical evidence; one scoped fresh **immediate pre-mutation** drift check is still needed when actually performing B1.

Provider docs checked 21 Nov 2026:
- [Cloud Run traffic update CLI](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/update-traffic)
- [Cloud Run deploy CLI](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy)
- [Rollout, traffic tag and rollback](https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration)
