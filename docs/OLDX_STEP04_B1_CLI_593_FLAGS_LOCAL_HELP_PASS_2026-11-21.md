# OLDX Step 04 — B1 local CLI 593 deployment-flag help VERIFIED, source-only release caveats

Date: 21 November 2026 ~17:57 IST. Branch: `security-hardening-review`. **Owner-observed local-help evidence; NO Cloud API calls/deployment.**

## Owner's actual screen evidence (do not repeat)

In Windows PowerShell the owner executed the previously prepared *local help only* command:

```powershell
gcloud.cmd run deploy --help | Select-String -Pattern '--no-traffic','--tag','--image','--service-account','--cpu','--memory','--concurrency','--timeout','--min-instances','--max-instances','--set-env-vars'
```

The screenshot returned matching local SDK 593.0.0 help, including:
- `[--tag=TAG] [--timeout=TIMEOUT] [--no-traffic]`
- `[--concurrency=CONCURRENCY]`
- `[--min-instances=MIN_INSTANCES]` and `[--max-instances=MAX_INSTANCES]`
- `--service-account=SERVICE_ACCOUNT`
- `--cpu=CPU`, `--memory=MEMORY`
- `--set-env-vars=[KEY=VALUE,...]`
- `--image=IMAGE`.

The returned `PS C:\Users\Yasmin Parmar>` prompt proves the help command completed. Matches were from synopsis and examples; an example `--image=us-docker.pkg.dev/project/image` is not a real OLDX deployment target. **No `gcloud run deploy` without `--help` was executed**, no API request, code build, scan, Registry push/sign or Cloud Run write occurred.

`B1_CLI_VERSION=593.0.0`
`B1_LOCAL_HELP_TARGET_FLAGS=OBSERVED_AVAILABLE`
`B1_LOCAL_HELP_ONESHOT=COMPLETE_DO_NOT_REPEAT`
`B1_DEPLOYMENT=NOT_STARTED`

## NEW material hazards revealed by official Google Cloud Run reference research

1. [Cloud Run service environment variables](https://docs.cloud.google.com/run/docs/configuring/services/environment-variables): **`--set-env-vars` replaces/removes previously configured environment variables** omitted from the new list. `--update-env-vars` retains other variables and can retain unreviewed dangerous defaults. Do not select either without a scoped complete latest template env-key/secret-reference inventory (redacted, no values), source allowed-key decision and exact new revision diff. This is a *new revision configuration* and does not rewrite old immutable revisions, but the latest service template will change.
2. [`gcloud run deploy` reference](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy): **`--deploy-health-check` is enabled by default** and creates a single new instance to run a startup probe; `--no-deploy-health-check` opts out. A zero-hosted-invocation/zero-startup trial must review/verify the latter's availability and impact on owner-installed 593.0.0. A 0%-main tagged URL is still invokable by an authorized principal. `--no-deploy-health-check` is not proof of zero costs or zero future startup.
3. The provider describes **`--min-instances` and `--max-instances` as revision-level**, and `--min` and `--max` as service-level, so do not conflate them. `--cpu-throttling` controls request-based billing behavior. Its local help support has not been separately captured in the owner screenshot; official reference describes it.
4. `--no-traffic` can affect subsequent service **LATEST** routing default; it keeps the just-created revision out of main traffic but does NOT prove that tagged URL cannot be called. Even R1 tag removal leaves new revision/latest template; R2 old-main restoration is usually NO-OP and is not a full configuration rollback. Avoid `--to-latest` and `--clear-tags`.
5. `--[no-]invoker-iam-check` affects service access; do not turn it off. Owner's 17:48 G4-A PASS with limits confirms only exact direct service/project policy at that time. Parent inherited IAM, other-db effective denial, and exclusive owner invocation remain unverified.

## B1 source-only operator choices still needed

- Prove the actual *same-window* service/environment/secret references and all specified flags; do not print real secrets. The 17:48 G4-A checks two false flags but **not** a complete env/secret allowlist.
- Choose the exact scope of the 0%-main `ownerreadv2` revision against immutable private index `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`, one old service/runtime account, 1 CPU/512Mi, concurrency 1, timeout30, min0/max1, no public grant, no Cloud Run IAM/billing edits, no Firestore/Auth/Storage calls.
- Review the default deploy startup probe and whether `--no-deploy-health-check` is available in the owner-installed CLI. **Do not issue a live deploy before deciding**. If the exact immutable image's startup behavior remains unverified, do not claim an observed hosted 503.
- Preserve `oldx-owner-read-00001-8kr=100%` root main and old tags `healthcheck` and exact `step3rc14`. Conditional owner B1 and R1/R2 approvals already recorded but are **not automatic permission to bypass failed or stale gates**. R1 remove only new `ownerreadv2`; R2 restore old root only on incident with fresh-state review; otherwise NO-OP.

## Recommended next single minimal local-only check

**Only if necessary to complete deploy command syntax review, not a repeat of last search:**

```powershell
gcloud.cmd run deploy --help | Select-String -Pattern '--no-deploy-health-check','--cpu-throttling','--invoker-iam-check'
```

This is a materially distinct test of a **deployment startup side effect** and IAM safety, which the previous search did not cover. It does **not** call Cloud services. If these flags are absent in SDK 593.0.0 or ambiguous, STOP and decide a source-only alternative; do not update SDK merely because components have updates.

**After this:** Finalize a single B1 **nonexecuting** draft and a selective fresh pre-mutation service state/env-key safety guard. No repeat of G4-A three GET or C5 revision GETs just for a new green result. Still `G4_INHERITED_ACCESS=OPEN`, `G4_OTHER_DB_DENIAL=OPEN`, `G2_INDEPENDENT_BUILDER=UNKNOWN`, `STEP04=HOLD`, production NO-GO.
