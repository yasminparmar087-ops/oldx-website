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
