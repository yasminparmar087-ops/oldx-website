# OLDX Step04 — historical cached service env: exactly two FALSE, zero secrets

Owner-observed Windows PowerShell screenshot 21 Nov 2026 ~18:04 IST. Read-only local inspection of cached `$svc`, **no fresh Cloud API calls**.

```text
B1_ENV_FROM_CACHED_SERVICE=YES_HISTORICAL
B1_ENV_NAME_COUNT=2
B1_ENV_OTHER_NAMES=
B1_ENV_SECRET_REFERENCE_COUNT=0
B1_ENV_FLAGS=EXACT_FALSE
B1_ENV_VALUES_OR_SECRETS_PRINTED=NO
B1_ENV_LOCAL_INSPECTION=COMPLETE
```

The two exact env keys are `OLDX_PRODUCT_READ_ACTIVATE_STAGING` and `OLDX_PRODUCT_READ_STAGING_ADC`, both plain literal `false`. No other env *keys* and no env-key secret references were present in the **historical latest service template**, according to this cached object; names only, not secret values, were displayed.

**What this proves:** a candidate new B1 revision can propose `--set-env-vars=OLDX_PRODUCT_READ_ACTIVATE_STAGING=false,OLDX_PRODUCT_READ_STAGING_ADC=false` without dropping any other **historically observed env keys**. Google docs define `--set-env-vars` as destructive toward omitted keys, so a **fresh immediate pre-write exact env-key/secret/volume-and-template guard is still necessary**. It cannot prove the current live service has no added keys or hidden secret volume mounts, that older traffic-serving revisions had the same flags, or that B1 startup has already been tested.

**Do not repeat** cached `$svc` inspection, SDK `--help`, previous G4-A GETs/C5 revision GETs, Grype scans, build, OCI upload or signing.

## B1 no-execute deployment command DRAFT (for review only)

This is an example of the concrete *intended one new revision* and **MUST NOT BE PASTED AS A LIVE COMMAND NOW**; the owner has only conditional B1/R1/R2 consents and has not observed the fresh imminent pre-write gate or verified final service-template/IAM inheritance. One-shot command should be issued *only after* those gates pass and a separate final human release decision confirms an operator is ready.

```powershell
# REVIEW ONLY — DO NOT RUN (would create a revision and could incur cost)
gcloud.cmd run deploy oldx-owner-read `
  --project=oldx-staging `
  --account=yasminparmar087@gmail.com `
  --region=asia-south1 `
  --image=asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-npmfree-20261121-a1@sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79 `
  --service-account=oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com `
  --no-traffic --tag=ownerreadv2 `
  --no-deploy-health-check --cpu-throttling `
  --cpu=1 --memory=512Mi --concurrency=1 --timeout=30 `
  --min-instances=0 --max-instances=1 `
  --set-env-vars=OLDX_PRODUCT_READ_ACTIVATE_STAGING=false,OLDX_PRODUCT_READ_STAGING_ADC=false
```

**Safety choices and limitations:**
- Do not include `--no-invoker-iam-check` (would weaken service-level auth), `--allow-unauthenticated`, `--to-latest`, `--clear-tags`, `--async`, `--quiet`, IAM/billing/Rules modifications, or production route changes. The actual request uses `--no-traffic --tag` which leaves its tagged URL callable **to authorized invokers**.
- Avoid `--invoker-iam-check` in this draft because it is a service-level access mode configuration toggle: require it already **enabled** in immediate pre-write guard instead of changing it during B1.
- Request-based CPU throttling and skipping deployment health check *reduce* operational scope, but do NOT guarantee zero instance startups, no possible invocation by other permitted principals, or zero charges.
- `--min-instances=0 --max-instances=1` are **revision-level** settings and must not be confused with service-level `--min/--max`.
- Exact expected two env keys are known from historical `$svc` and require fresh pre-write matching; any unexpected env keys, service volumes/mounts, secret refs, IAM/ingress drift, or tag mismatch => STOP; do not blindly overwrite.
- Deployment still changes latest service revision/template even with 0%-main. Conditional owner-approved R1 removes only the *new* tag, R2 is traffic NO-OP if old 100% main/tags intact; these **do not restore latest service template or delete the new revision**. A further restore would require independent approved plan.
- Verify the exact previously signed index digest and local Sigstore receipt without repeating build/upload/scan. Independent original trusted-builder provenance remains UNKNOWN.
- C4 six severe scanner CVEs risk accepted **for OFF-only**; G8 additional financial risk accepted **for OFF-only**; G4 inherited IAM and other-db effective denial still UNKNOWN, Product API activation not permitted.

## One distinct pending **read-only** decision before an actual release

Project may have no organization parent (previous account setup suggests so) but **G4 parent inherited IAM currently UNVERIFIED**. One read-only `gcloud projects describe oldx-staging` with **redacted parent status** can determine if an organization/folder parent exists before the final service-state gate. Do not print project numbers or full policy. A project with parent needs separate parent/IAM review; a project with no parent still does not prove custom/project principal exclusivity. No new database, IAM, Cloud Run or registry write.

Status:
`B1_HISTORICAL_ENV_LOCAL_CHECK=COMPLETE`
`B1_HISTORICAL_ENV_KEYS=2_EXACT_FALSE`
`B1_HISTORICAL_ENV_SECRET_REFS=0`
`B1_DEPLOY_DRAFT=SOURCE_ONLY_PREPARED_NOT_EXECUTED`
`B1_FRESH_PREWRITE=NOT_EXECUTED`
`G4_PARENT_INHERITANCE=UNVERIFIED`
`B1_R1_R2_OWNER_CONDITIONAL_CONSENT=RECORDED`
`STEP04=HOLD`
`PRODUCTION=NO_GO`

Official guidance:
- https://docs.cloud.google.com/run/docs/configuring/services/environment-variables
- https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy
- https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration
