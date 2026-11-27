# BAJUTO / OLDX Step05 — H2AD owner-approved OFF health probe; remaining Step05 exit gates (28 Nov 2026)

## Owner authorization, scope and factual checkpoint

Owner explicitly said **"ha manjuri chhe"** after proposed H2AD limited plan: create a dedicated short-lived Scheduler probe service account, add exactly that identity as `roles/run.invoker` on the exact private OFF Gateway only, create one paused/future-scheduled Scheduler job, manually dispatch a **single GET /healthz**, inspect evidence, remove only those newly created bindings/resources with UID/etag guards; no public ingress or production enable. This is authorization for **that bounded pilot**, not for enabled Product publication, real Firebase writes, KMS asymmetricSign or other projects/services. Price/free-tier eligibility is not guaranteed; Scheduler job and Cloud Run invocation may incur charges.

Latest **H2AC actual PASS** in owner WSL screenshot: `H2AC_SCHEDULER_API_STATE=ENABLED`, `H2AC_RESULT=PASS_EXACT_SCHEDULER_API_ENABLED`, `H2AC_ENABLE_ATTEMPTED=TRUE`, `H2AC_JOBS_IAM_COMPUTE_VPC_CLOUDRUN_WRITES=NONE`, `H2AC_DO_NOT_REPEAT=TRUE`. No jobs, IAM grants, Gateway changes or hosted HTTP test in H2AC. Do not rerun any previous consumed H2AC/H2AB/H2AA/H2Z/H2Y/H2W/H2U/H2V/H2S/H1B one-shots or code tests.

## Current exact 5 substantive Step05 exit gaps — NOT 80/90% complete

Canonical 26 Nov source evidence: [G2–G6 source implementation and provider blockers](OLDX_STEP05_C2_SOURCE_ONLY_ENABLED_SLICE_GAP_AND_ONE_PASS_IMPLEMENTATION_PACKET_2026-11-24.md); [latest hosted OFF Gateway evidence](OLDX_STEP05_H2AC_ACTUAL_PASS_H2AD_SCHEDULER_PROBE_PREPARATION_2026-11-28.md).

1. **H2AD OFF-only hosted HTTP**: verify one real OIDC-authenticated Scheduler -> default `run.app` `GET /healthz` from same project, Cloud Scheduler delivery 2xx and independent sanitized server-side evidence where available; do not mistake jobs.run accepted for target 200. Cleanup only exact new SA/job/binding. **NOT TESTED yet**.
2. **G2/G3 real hosted identities + crypto/Auth**: website/Gateway/backend mutually authenticated exact Invoker audiences, independent KMS KeyVersion status reader, one explicitly authorized real bounded signing path and Firebase Auth + Firestore `(default)` least-privilege runtime binding; prior mocks and KMS public key/signing IAM do not establish actual signing.
3. **G4 real managed image/review + full Product publication**: one approved managed-photo provider with correct ownership/revocation, moderated publication/withdraw behavior, no cross-user media reads. Source-only tests are not hosted media validation.
4. **G5 real durable run budget/nonce/retention**: prove atomic cross-instance finite quotas, permanent one-sign ledger without TTL on consumed marker, idempotency/partial-failure cleanup and exact synthetic scope using real Firestore rules/transactions; no automatic data deletion.
5. **G6 end-to-end synthetic seller/buyer release acceptance**: independent approved authority, immutable actual enabled release image/provenance and security disposition, real sign-in/save/publish/buyer-read/edit/withdraw, rollback/monitoring and exit decision. Default-OFF source must remain OFF until all gates independently accepted; production still NO-GO.

These are **five workstreams**, not five commands or five equivalent-sized stages. A meaningful percentage/guaranteed completion date is not derivable from the documented evidence. H2AD health success is only the first gate and will NOT close Step05.

## H2AD0: NEW read-only preflight SOURCE committed, NOT run

To minimize write failures and avoid recreating earlier resources, the first approved-operation preflight is deliberately **three fresh, uniquely purposed metadata GETs**, with no writes:
- exact H2W Cloud Run service GET **for its previously unrecorded default `https://*.run.app` URI** and fresh service UID/ingress/IAM-enforced/OFF runtime SA/image validation, **not** another H2Y readiness or H2W IAM test;
- exact intended NEW Scheduler probe SA `oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com` GET, must be 404 (collision fails closed);
- exact intended NEW Scheduler job `projects/oldx-staging/locations/asia-south1/jobs/oldx-h2ad-off-healthz-20261128` GET, must be 404 (collision fails closed).

`asia-south1` (Mumbai) is an officially supported Cloud Scheduler location: https://docs.cloud.google.com/scheduler/docs/locations . Cloud Scheduler calls to same-project default run.app with internal ingress are supported, but IAM OIDC and correct audience are mandatory: https://docs.cloud.google.com/run/docs/securing/ingress and https://docs.cloud.google.com/run/docs/triggering/using-scheduler .

- Script: `scripts/step05_h2ad0_private_gateway_scheduler_probe_readonly_preflight_once_20261128.py`
- Creation commit: `63c63934080da8ba7140b86df7b85c748f703d8d`
- GitHub-verified script blob: `1addb78a91a2524461fcc6961894a060a2e2de44`
- Static source scope/no-write/marker guards PASS; Owner Python AST and Cloud APIs **NOT EXECUTED** as of this document.
- Owner root Ubuntu WSL with isolated native SDK and exact prior successful H2AC/H2W markers. New marker `/root/.oldx-step05-h2ad0-scheduler-target-preflight-once-20261128` consumed **before any Google GET**. On STOP preserve marker; do not rerun old one-shots or broaden privileges.
- Successful preflight stores safe target URL and exact future resource names under `/root/oldx-h2ad0-scheduler-readonly-<UTC>/sanitized-preflight.json`, root-private. Never paste OAuth tokens, unredacted IAM, service-account secrets or private auth config.
- **Even PASS does not create job or perform hosted HTTP.** After actual preflight owner output, construct one combined tightly guarded H2AD write/dispatch/cleanup sequence against exact observed URL and resources, within the already approved scope. Avoid blind cleanup on ambiguous `jobs.run` or delayed delivery.

### One exact root Ubuntu WSL paste for NEW H2AD0 only

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad0-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad0.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/63c63934080da8ba7140b86df7b85c748f703d8d/scripts/step05_h2ad0_private_gateway_scheduler_probe_readonly_preflight_once_20261128.py' &&
test "$(git hash-object "$d/h2ad0.py")" = '1addb78a91a2524461fcc6961894a060a2e2de44' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad0.py" &&
python3 -B "$d/h2ad0.py" --h2ad0-owner-approved-probe-exact-target-readonly-once
```

Expected (NOT achieved until screenshot): `H2AD0_RESULT=READONLY_TARGET_URI_AND_RESOURCE_ABSENCE_PASS_WITH_LIMITS`. STOP/403 or missing default URL is not a pass. H2AD0 is only a *new*, scoped, no-write gate; it cannot enable production.

**Checkpoint**: `H2AC=OWNER_ACTUAL_PASS_AND_CONSUMED`; `H2AD=OWNER_APPROVED`; `H2AD0=SOURCE_READY_NOT_EXECUTED`; `STEP05=ACTIVE`; `H2_HOSTED_HTTP=NOT_TESTED`; `H2/PRODUCTION=NO_GO`.
