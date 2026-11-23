# OLDX Step 04 — A8 new private OFF-only trial: fresh owner scope consent and separate prewrite gate

**23 November 2026 — SOURCE-ONLY, not a cloud execution receipt.** Use only repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Latest known baseline before this packet: `3abf3f440e2b33499d0965e265b1d3652da5edf0`.

## 1. Actual new owner consent — narrow scope, no blanket technical PASS

The owner replied **"ha manjuri chhe"** to a specific request to proceed with **one NEW A8 immutable-image, PRIVATE, zero-main-traffic, DEFAULT-OFF staging trial**, at most one attempt, at most 20 minutes of direct supervision, with exactly the known unresolved 15 unique severe Grype CVE IDs, potential inherited Project Owner/Editor Cloud Run invocation and non-guaranteed side-provider charges explicitly disclosed. The response authorized proceeding **within this bounded trial planning/risk scope**. It did **not** select the earlier proposed Step04 "decision-only" Option B; Step04 retains its original technical exit.

**Distinguish operational consent:** This approval permits making a source-only operator packet and a specifically scoped **fresh read-only prewrite check**. It does not automatically authorize blind deployment, any trial URL invocation, or separately mutating Cloud Run tag/traffic/template under R1/R2. **Before actual A8 B1 deployment**, obtain explicit action-level approval for the exact candidate B1, plus separate specifically described conditional R1 and R2 rollback operations (old 21-Nov B1/R1/R2 authorization is fully consumed by the earlier image). Do not infer unlimited spend or an all-provider cap.

## 2. Pinned A8 target and historical invariants

- Project: `oldx-staging`; region: `asia-south1`; service: `oldx-owner-read`; operator: `yasminparmar087@gmail.com`.
- **New A8 immutable image (NOT the historic B1 image):** `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`.
- Exact A8 signed build source Git SHA `31888e7a6c3e402ea55fb7dc5ff5b70a0ddecc71`, trusted-source/builder/subject SLSA and new-image Docker local no-network nonroot default-OFF /healthz=200, protected POST=503 **PASS_WITH_LIMITS**. No rebuild/SLSA rerun/Grype/rescan/registry push.
- Historic B1 on DIFFERENT `npmfree-20261121-a1` OCI index `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79` created revision `oldx-owner-read-00010-zud`, which remains the last verified `latestReadyRevisionName` and service template after its R1 tag cleanup. Do not assume restored old template. Historic R1 removed `ownerreadv2`; not a full rollback.
- Last verified routing: `oldx-owner-read-00001-8kr` **100% main**, `oldx-owner-read-00002-tid` tag `healthcheck` 0%, `oldx-owner-read-00003-nus` tag `step3rc14` 0%. Old `ownerreadv2` tag absent. Current state MUST be read anew only as **immediate prewrite**; these are not current-state guarantees.
- For new A8 trial, choose **distinct unused tag** `a8off23nov` to avoid resurrecting the formerly callable `ownerreadv2` tag URL. No tag is yet created. If A8 tag is present or conflicts, **STOP**; do not retag a prior revision.
- Intended deploy properties (NOT RUN): `--no-traffic --tag=a8off23nov`; both environment flags `OLDX_PRODUCT_READ_ACTIVATE_STAGING=false` and `OLDX_PRODUCT_READ_STAGING_ADC=false` exactly; runtime SA `oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com`; 1 CPU, 512Mi, concurrency 1, 30s timeout, min instances 0/max 1, request CPU throttling, no deploy health probe, no new IAM/secret/billing/Firestore access. The **tag URL is callable by authorized principals despite 0%-main**. No hosted Product/Firestore/Auth API request under this consent.
- Cost controls are risk bounding, NOT a guaranteed hard global ₹2,000 limit. G2 severe-CVE risk remains unresolved; G4 effective exclusive invoker and hypothetical cross-DB denial UNVERIFIED; G8 all-provider hard stop UNPROVEN. `PRODUCTION=NO_GO`.

## 3. ONE fresh Windows PowerShell READ-ONLY prewrite check (only when owner is ready for possible new B1)

This reads **just existing Cloud Run service metadata and direct service IAM policy** once in the same supervised prewrite window. It performs **ZERO Cloud changes, URL calls, Firebase access, Grype, billing or tests**, and prints **only sanitized PASS/STOP labels** (no URLs, raw IAM JSON or secrets). It reuses the **already successfully owner-executed** 21-Nov B1 service/R1 checks, but updates the last known `00010-zud` template and new unique tag. The exact previous service/latest revision is a **required invariant**, not a prediction. On any drift/denial/error, **STOP without repeating** and bring only the label/screenshot back; do not guess a new live image/revision or edit IAM.

~~~powershell
& {
  try {
    $common = @('--project=oldx-staging','--region=asia-south1','--account=yasminparmar087@gmail.com','--format=json','--quiet')
    $serviceRaw = & gcloud.cmd run services describe oldx-owner-read @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $serviceRaw) { throw 'SERVICE_READ_FAILED' }
    $s = $serviceRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    if ([string]$s.metadata.name -cne 'oldx-owner-read' -or
        [string]$s.status.latestReadyRevisionName -cne 'oldx-owner-read-00010-zud' -or
        [string]$s.spec.template.spec.serviceAccountName -cne 'oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com') {
      throw 'SERVICE_OR_LATEST_DRIFT'
    }
    if ([string]$s.metadata.annotations.'run.googleapis.com/ingress' -cne 'all' -or
        [string]$s.metadata.annotations.'run.googleapis.com/invoker-iam-disabled' -notin @('','false')) {
      throw 'IAM_CHECK_OR_INGRESS_DRIFT'
    }
    $containers = @($s.spec.template.spec.containers | Where-Object { $null -ne $_ })
    if ($containers.Count -ne 1) { throw 'CONTAINER_COUNT_DRIFT' }
    $c = $containers[0]
    $prev = 'asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-npmfree-20261121-a1@sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79'
    if ([string]$c.image -cne $prev) { throw 'PREVIOUS_TEMPLATE_IMAGE_DRIFT' }
    $envs = @($c.env | Where-Object { $null -ne $_ })
    if ($envs.Count -ne 2) { throw 'PREVIOUS_ENV_COUNT_DRIFT' }
    foreach ($key in @('OLDX_PRODUCT_READ_ACTIVATE_STAGING','OLDX_PRODUCT_READ_STAGING_ADC')) {
      if (@($envs | Where-Object {
        [string]$_.name -ceq $key -and [string]$_.value -ceq 'false' -and $null -eq $_.valueFrom
      }).Count -ne 1) { throw 'PREVIOUS_ENV_DRIFT' }
    }
    if (@($s.spec.template.spec.volumes | Where-Object { $null -ne $_ }).Count -ne 0 -or
        @($c.volumeMounts | Where-Object { $null -ne $_ }).Count -ne 0 -or
        [string]$s.spec.template.metadata.annotations.'run.googleapis.com/secrets' -ne '') {
      throw 'EXISTING_SECRET_OR_VOLUME_DRIFT'
    }
    $tr = @($s.status.traffic | Where-Object { $null -ne $_ })
    $m = @($tr | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00001-8kr' })
    $h = @($tr | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00002-tid' })
    $old = @($tr | Where-Object { $_.revisionName -ceq 'oldx-owner-read-00003-nus' })
    if ($tr.Count -ne 3 -or $m.Count -ne 1 -or $h.Count -ne 1 -or $old.Count -ne 1 -or
        [string]$m[0].percent -cne '100' -or [string]$m[0].tag -ne '' -or
        [string]$h[0].tag -cne 'healthcheck' -or [string]$old[0].tag -cne 'step3rc14' -or
        [string]$h[0].percent -notin @('','0') -or
        [string]$old[0].percent -notin @('','0') -or
        @($tr | Where-Object { $_.tag -cin @('ownerreadv2','a8off23nov') }).Count -ne 0) {
      throw 'ROOT_TAG_OR_TRAFFIC_DRIFT'
    }
    $iamRaw = & gcloud.cmd run services get-iam-policy oldx-owner-read @common 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $iamRaw) { throw 'SERVICE_IAM_READ_FAILED' }
    $policy = $iamRaw | Out-String | ConvertFrom-Json -ErrorAction Stop
    $public = @($policy.bindings | ForEach-Object { $_.members } |
      Where-Object { $_ -cin @('allUsers','allAuthenticatedUsers') }).Count
    $directInvoker = @($policy.bindings | Where-Object {
      [string]$_.role -ceq 'roles/run.invoker'
    } | ForEach-Object { $_.members } | Where-Object { $_ }).Count
    if ($public -ne 0 -or $directInvoker -ne 1) { throw 'SERVICE_DIRECT_IAM_DRIFT' }
    'A8_PREWRITE_SERVICE_AND_TRAFFIC=PASS'
    'A8_PREWRITE_EXISTING_LATEST=00010_ZUD'
    'A8_PREWRITE_OLD_ROOT_AND_TAGS=PRESERVED'
    'A8_PREWRITE_NEW_TAG=a8off23nov_ABSENT'
    'A8_PREWRITE_DIRECT_IAM=NO_PUBLIC_ONE_NAMED_INVOKER'
    'A8_PREWRITE_INHERITED_IAM=UNVERIFIED'
    'A8_PREWRITE_EFFECTIVE_OTHER_DB_DENIAL=UNVERIFIED'
    'A8_PREWRITE=PASS_WITH_LIMITS'
    'A8_NEW_CLOUD_RUN_DEPLOY=NONE'
  } catch {
    $reason = [string]$_.Exception.Message
    if ($reason -cnotmatch '^[A-Z_]+$') { $reason = 'UNEXPECTED_ERROR' }
    'STOP_A8_PREWRITE_NO_AUTOMATIC_RETRY'
    "REASON=$reason"
    'A8_PREWRITE=NOT_CLEARED'
    'A8_NEW_CLOUD_RUN_DEPLOY=NONE'
  }
}
~~~

**PASS_WITH_LIMITS is NOT authorization to deploy.** A checked current direct IAM policy cannot prove exclusive effective invocation; previous project Owners/Editor may still have rights. Do not paste historical 21-Nov B1 deploy/R1 commands unchanged: they target the **wrong image and old tag**.

## 4. Outstanding separate B1/R1/R2 operator decision and no-repeat sequence

Before issuing any executable A8 deployment command, record separate A8-specific owner approval of all **three** distinct operational scopes:

- **A8 B1:** Exactly **one** supervised new revision using the exact above A8 immutable image and new unique `a8off23nov` tag; **0% main**, private, no Auth/Firestore access; operator window at most 20 minutes; exact flags/resources, fresh preimage PASS; no retries. New revision/tag may persist and incur cost even without public traffic.
- **A8 R1:** If the new `a8off23nov` tag is actually created, **only** remove that tag once after checking the exact new revision and unchanged old root/tags. Never remove `healthcheck` or `step3rc14`; tag removal does **NOT** restore old latest template or delete the revision.
- **A8 R2:** **NO-OP** if original `00001-8kr=100%` main and both old tags remain. If they have changed unexpectedly, **STOP**, collect a fresh state and seek incident-specific owner authorization before traffic restore to exact original revision. No blind `--to-latest` or `--clear-tags`. Template restoration, rev deletion and IAM changes are **out of scope**.

After A8 prewrite and exact action-level approvals, source-review one A8-specific deploy command (do not reuse old `ownerreadv2` command); if genuinely executed, verify **fresh new revision identity**, exact immutable resolved image/index-to-amd64 relation, both flags FALSE, 0%-main, 100% old main/tags, IAM and CPU/RAM. Do not claim success from a command merely prepared. R1 tag-only cleanup with independent actual evidence is separate; R2 remains no-op absent drift.

**Do NOT** create second Firestore DB or run obsolete A1–A8 build/sign/scan/runtime/B1/R1/CI/Rules/billing snapshots. No enablement of Product API, ADC, public access, Firebase data, production, or rollout via alternate console. **`STEP04=ACTIVE/HOLD`, `A8_RISK_SCOPE_OWNER_CONSENT=YES`, `A8_PREWRITE=PREPARED_NOT_RUN`, `A8_B1_R1_R2_EXACT_RELEASE=AWAITING_DISTINCT_APPROVAL_AND_FRESH_PREWRITE`, `PRODUCTION=NO_GO`.**

References: [Original Step04 master exit](OLDX_SINGLE_EXECUTION_PLAN_2026-11-13.md), [A8 isolated runtime observed](OLDX_STEP04_G2_A8_ISOLATED_RUNTIME_PASS_G4_G8_NEXT_2026-11-23.md), [historic R1 tag removal](OLDX_STEP04_R1_TAG_ONLY_COMPLETE_2026-11-21.md), [current G4/G8 decision packet](OLDX_STEP04_G4_G8_BOUNDARIES_AFTER_SINGLE_DB_2026-11-23.md), and current Google [Cloud Run CLI flags](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy) / [traffic+tags](https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration).
