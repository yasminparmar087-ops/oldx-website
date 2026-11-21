# OLDX Step 04 — B1 one-try owner execution packet after service prewrite PASS

Date: 21 November 2026 ~18:12 IST. This is a **conditional owner-authorized private staging revision create**, NOT a production release. **This command has not yet been executed.**

## Actual owner screenshot, read-only service prewrite complete (DO NOT REPEAT)

Actual Windows PowerShell screenshot displays following output and restored prompt `PS C:\Users\Yasmin Parmar>`, without STOP:

```text
B1_FINAL_SERVICE_READ=PASS
B1_FINAL_SERVICE_IDENTITY=MATCH
B1_FINAL_LATEST_TEMPLATE=MATCH_OLD
B1_FINAL_ENV=EXACT_TWO_FALSE
B1_FINAL_SECRET_AND_VOLUME_REFS=ZERO
B1_FINAL_ROOT_AND_OLD_TAGS=MATCH
B1_FINAL_OWNERREADV2_TAG=ABSENT
B1_FINAL_POLICY_PROOF=HISTORICAL_G4A_WITH_LIMITS
B1_FINAL_DEPLOYMENT=NOT_STARTED
B1_FINAL_SERVICE_PREWRITE=PASS_WITH_LIMITS
```

This was one Cloud Run service GET with exact expected image template, service account, ingress/IAM-invoker-check annotation, **2 false env keys**, **0 secret/volumes**, **existing 100% main root** `oldx-owner-read-00001-8kr`, tags `healthcheck` and `step3rc14`, and no new `ownerreadv2`. It is **as-of-screenshot**, NOT a permanent lock or an effective IAM authorization proof. Direct project/service IAM 17:48 prior G4A `PASS_WITH_LIMITS`, project-parent metadata 18:08 `NO_PARENT_REPORTED` are earlier **consumed** evidence. Parent/inherited/custom/project IAM exclusivity and other-DB effective deny remain UNVERIFIED. Do not repeat G4A/C5, local help, build/upload/scan/signing.

## Source and CLI reviewed for one bounded OFF-only release

- Exact existing private OCI index image `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-npmfree-20261121-a1@sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`, C3 local signed bundle previously PASS. No new image build or publication.
- Google Cloud SDK **593.0.0**, owner's local help verified `--no-traffic`, `--tag`, `--image`, exact resource flags, `--set-env-vars`, `--no-deploy-health-check`, `--cpu-throttling`, `--invoker-iam-check` support. No update needed.
- Previous exact cached env inspection found 2 flags, 0 other keys, 0 env secret refs. Latest fresh B1 service GET confirms this, plus 0 secret volumes. Plain string `false` for both flags prevents product data-plane activation by pinned source gate; no hosted 503 confirmation is implied.
- A candidate command with `--no-traffic --tag=ownerreadv2`, 1 CPU/512Mi, concurrency1, timeout30, min0/max1, `--cpu-throttling`, `--no-deploy-health-check` aims to avoid main traffic and deployment startup health probe. Tagged URLs still invokable by permitted principals and may incur cost; `--no-deploy-health-check` doesn't ban all future startups. No IAM-change flags supplied.
- **Approval ledger:** Owner explicitly gave one B1 conditional staging-only, C4 limited six-CVE, G8 limited other-provider exposure, R1 only remove new tag, R2 only when main traffic changed and after exact-state check. G4A partial IAM and absence of project parent reduce but do not eliminate access risk. No enabled Product API, production, billing/IAM mutation, second database or hosted smoke calls authorized.

## ONE executable B1 command for supervised owner Windows PowerShell — NOT YET RUN

Only run once in the same supervised window as the fresh B1 prewrite screen (if delayed/drift, STOP rather than assume old snapshot), after understanding limited potential costs and template side effect:

```powershell
gcloud.cmd run deploy oldx-owner-read `
  --project=oldx-staging `
  --account=yasminparmar087@gmail.com `
  --region=asia-south1 `
  --image=asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-npmfree-20261121-a1@sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79 `
  --service-account=oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com `
  --no-traffic `
  --tag=ownerreadv2 `
  --no-deploy-health-check `
  --cpu-throttling `
  --cpu=1 `
  --memory=512Mi `
  --concurrency=1 `
  --timeout=30 `
  --min-instances=0 `
  --max-instances=1 `
  --set-env-vars=OLDX_PRODUCT_READ_ACTIVATE_STAGING=false,OLDX_PRODUCT_READ_STAGING_ADC=false
```

**Do not add** `--no-invoker-iam-check`, `--allow-unauthenticated`, `--to-latest`, `--clear-tags`, `--async` or IAM/Billing changes. Do not echo/token/share raw IAM or service JSON. If CLI unexpectedly asks for public access or migration of main traffic, STOP. If ambiguous/failure, do NOT rerun deploy blindly.

## Immediately after B1 owner runs (only if actually executed)

Pause further writes and save the sanitized output. Before claiming any success, use one **targeted read-only post-create Cloud Run service+new revision** check of:
- Main root still `oldx-owner-read-00001-8kr=100%`; both old tag bindings preserved.
- Exactly one new `ownerreadv2` **tagged 0%-main** revision and its fresh revision name, pinned immutable image digest.
- Both exact literal `false` activation flags, expected runtime service account, 1 CPU/512Mi/concurrency1/timeout30, min0/max1, no public invoker IAM or runtime URL invocation.
- No unexpected secondary revisions, traffic drift, IAM changes. Any drift -> STOP, do not auto retry.
- R1 and R2 conditional approvals are recorded: **R1** remove only `ownerreadv2` if necessary after guard. **R2** original main restore only if unexpectedly changed; otherwise NO-OP. Neither tag removal nor 0%-traffic means new latest template/revision has been deleted. Any full-service template restore requires separate incident-specific authorization.
- If B1 not run, leave all fields NOT EXECUTED, no fabricated successful release.

**Current:** `B1_FINAL_SERVICE_PREWRITE=PASS_WITH_LIMITS`, `B1_OWNER_CONDITIONAL_APPROVAL=YES`, `R1_R2_OWNER_CONDITIONAL_APPROVAL=YES`, `B1_COMMAND=REVIEWED_READY_FOR_OWNER_ONE_ATTEMPT`, `B1_EXECUTED=NO`, `G4_ENABLED_API=NO_GO`, `STEP04=HOLD`, `PRODUCTION=NO_GO`.

References: [Google Cloud Run Deploy](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy), [Cloud Run traffic tags](https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration), [Cloud Run health check](https://docs.cloud.google.com/run/docs/deploying).
