# OLDX Step 04 — B1 installed Google Cloud CLI version (OWNER-OBSERVED)

**Date:** 21 Nov 2026 ~17:54 IST. **Status: Windows PowerShell version check complete; no cloud write.**

## Actual owner evidence

The owner's screenshot shows their previously completed G4-A read-only output `G4A_READ_ONLY_PREB1=COMPLETE_WITH_LIMITS`; then **one new purely local** `gcloud.cmd --version` command returned and PowerShell resumed at `PS C:\Users\Yasmin Parmar>`:

```text
Google Cloud SDK 593.0.0
bq 2.1.42
core 2026.11.06
gcloud-crc32c 1.0.0
gsutil 5.38
Updates are available for some Google Cloud CLI components.
```

No `gcloud components update` requested or authorized. **Do not update CLI for this checkpoint** and do not repeat version command or G4-A three-GET/C5 scans/builds/uploads.

## Official release-flag references researched, not executed

- Google [gcloud run deploy reference](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy) shows `--image`, `--no-traffic`, `--tag`, `--service-account`, `--cpu`, `--memory`, `--concurrency`, `--timeout`, `--min-instances`, `--max-instances`, `--set-env-vars`, `--no-invoker-iam-check` and IAM flags; do **not** use the disabler or grant-public options.
- Google [Cloud Run traffic guide](https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration) shows `--no-traffic --tag TAG` creates an addressable tagged revision even at 0%-main.
- Google [gcloud run services update-traffic](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/update-traffic) shows narrowly targeted `--remove-tags` and `--to-revisions`, but no implicit compare-and-swap.

**Version string and Google current reference are not proof that all of these flags were tested on owner's exact installed 593.0.0 executable.** If required immediately before a separately authorized live B1, use **one local-help-only check** (no cloud calls, and do not run deployment):

```powershell
gcloud.cmd run deploy --help | Select-String -Pattern '--no-traffic','--tag','--image','--service-account','--cpu','--memory','--concurrency','--timeout','--min-instances','--max-instances','--set-env-vars'
```

No reason to repeat local help once the target flag help is captured; no reason to update SDK just because the CLI prints an available-update notice.

## Still open before B1

- Owner gave **conditional consent for exactly one private DEFAULT-OFF/503, 0%-main** `ownerreadv2` B1, and separate **conditional specific** R1 tag-only/R2 main-root-on-incident consents. C4/G8 OFF-only residual-risk decisions already recorded. No unconditional B1 write permission.
- G4-A direct service/project IAM and historical traffic snapshot PASS WITH LIMITS at 17:48. Inherited org/folder/custom-role/service-account access and other-DB denial **NOT VERIFIED**. Do not claim exclusive invoker or enable product/Firestore routes.
- **New final executable command preflight** must guard service template/environment **complete** values and `--set-env-vars` potential replacement, existing old traffic/tags, actual service account, IAM restrictions, immutable npm-free index digest, private tag no-public/no-main and min0/max1 constraints. Do not alter existing sensitive environment or secrets implicitly or log them.
- Both activation flags must be literal `false`. Root traffic 100% on `oldx-owner-read-00001-8kr`, historical tags `healthcheck`, exact `step3rc14` preserved; fail closed on stale snapshot or drift. R1 removal does not automatically restore the changed service template.
- This is a version/command-reference evidence checkpoint only. **NO Cloud Run deploy/traffic, IAM, Billing, Firebase, Registry or CI activity.**

`B1_INSTALLED_CLI_VERSION=593.0.0`
`B1_CLI_VERSION_READ=COMPLETE`
`B1_CLI_TARGET_FLAGS_LOCAL_HELP=NOT_YET_CAPTURED`
`G4A_DIRECT_IAM_PREB1=PASS_WITH_LIMITS`
`B1_EXACT_EXECUTION_COMMAND=SOURCE_REVIEW_PENDING`
`B1_R1_R2_EXECUTED=NO`
`STEP04=HOLD`
`PRODUCTION=NO_GO`
