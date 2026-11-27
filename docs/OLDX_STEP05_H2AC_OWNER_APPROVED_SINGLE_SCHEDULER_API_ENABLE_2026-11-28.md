# BAJUTO / OLDX Step05 H2AC — Owner APPROVED one Cloud Scheduler API enable (not executed)

## Owner approval received: 28 Nov 2026, after H2AB actual state read

The Owner explicitly answered **"ha manjuri chhe"** to the narrowly scoped proposal to enable **only** `cloudscheduler.googleapis.com` for Google Cloud project **`oldx-staging`** (project number `38472235077`). This authorizes the H2AC guarded script's one Service Usage API enable action, **not** a Scheduler job, service-account creation, IAM grant, Cloud Run/Compute/VPC change, hosted HTTP request, production release, KMS signing, or Firestore access. No API write or Google Cloud execution was performed through this documentation commit.

Predecessor H2AB is **actual PASS_WITH_LIMITS**: Owner root Ubuntu WSL screenshot `H2AB_CLOUD_SCHEDULER_API=DISABLED`, `H2AB_RESULT=ONE_NEW_SCHEDULER_API_STATE_READ_PASS_WITH_LIMITS`; H2AB marker already consumed. Never rerun H2AB, H2AA, H2Z, H2W, H2X/H2Y, prior image build/push/test/KMS probes or delete their one-time markers.

## Frozen approved source and direct operation scope

- Source `scripts/step05_h2ac_approved_single_scheduler_api_enable_once_20261128.py`
- Immutable creation commit `6f1397678ae78c9984bfcccc5e5aff538de22791`.
- Verified Git blob SHA-1 `0152009468f7cd02967852f8b0ef722be5bf2149` after owner's approval, with allowlist/method/one-shot checks PASS.
- Fresh single Service Usage state GET; if already ENABLED, **do not write**. Otherwise one **POST `/v1/projects/38472235077/services/cloudscheduler.googleapis.com:enable`**, up to 12 bounded GET polls of the resulting operation, one exact filtered readback. Source has no retry of the enable POST.
- Owner isolated native SDK (root Ubuntu WSL), previous H2AB consumed marker as prerequisite; new H2AC one-shot marker `/root/.oldx-step05-h2ac-scheduler-api-enable-approved-once-20261128` consumed before any authorized POST. If STOP after the marker, **do not rerun or reset the marker**; cloud operation might still have succeeded.
- No Scheduler job/dispatch, no IAM/service-account change, no Cloud Run update, no Compute API enable or VPC; product stays OFF, H2/production NO-GO.
- **Source prepared, Owner execution NOT YET OBSERVED**. Do not claim H2AC PASS until Owner's terminal output/receipt.

## Single approved root WSL command

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ac-owner-enable.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ac.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/6f1397678ae78c9984bfcccc5e5aff538de22791/scripts/step05_h2ac_approved_single_scheduler_api_enable_once_20261128.py' &&
test "$(git hash-object "$d/h2ac.py")" = '0152009468f7cd02967852f8b0ef722be5bf2149' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ac.py" &&
python3 -B "$d/h2ac.py" --h2ac-owner-approved-one-scheduler-api-enable-once
```

On success expect `H2AC_RESULT=PASS_EXACT_SCHEDULER_API_ENABLED` with `H2AC_SCHEDULER_API_STATE=ENABLED`, or `ALREADY_ENABLED_NO_WRITE` if it changed independently. This is **not a prediction**; actual output could be STOP and must be preserved without retry. Do not publish Owner OAuth, private SDK configuration or raw IAM.

## After actual H2AC readback — next authorization is separate

Cloud Scheduler may call the **default run.app host** of same-project internal-only Cloud Run, but only with a suitable OIDC service-account identity and **target-only** `roles/run.invoker`. The H2W Gateway currently has a previously verified Owner-only direct Invoker binding and no proved Scheduler-specific Invoker, so a job will require separately approved least-privilege IAM and one guarded create/run/disable/delete plan, with cost review and actual endpoint checks. Cloud Scheduler jobs are recurring resources; don't create/activate a permanent schedule casually. Do not enable VPC/Compute or loosen internal ingress as a shortcut.

**Checkpoint:** `H2AC=OWNER_APPROVED_SOURCE_PINNED_NOT_RUN`; `H2AB=ACTUAL_PASS_DISABLED_CONSUMED`; `H2_HOSTED_HTTP=NOT_TESTED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
