# OLDX Step05 — Owner expressly approves C1A Option B, exact service-only guarded deletion

**26 Nov 2026 IST — SOURCE PREPARED; no new owner Cloud Shell cleanup execution yet.** Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Refer to [latest Service Usage readback](OLDX_STEP05_C1A_EVENTARC_NOT_IN_ENABLED_LIST_OWNER_SCREENSHOT_2026-11-26.md) and original [C1A v2 guarded script/historic status](OLDX_STEP05_C1A_RECONCILING_ABSENT_CONFIRMED_AND_GUARDED_DELETE_V2_2026-11-26.md).

## 1. Exact new explicit Owner decision

After being shown the choice of (A) enabling previously unused/disabled Eventarc API for inventory, (B) **accepting UNKNOWN historical Eventarc dependency risk for EXACT C1A-only guarded cleanup**, or (C) limited retention extension, Owner replied **"vikalp b manjur chhe"**. This is **positive explicit acceptance of the unknown Eventarc-trigger/integration dependency risk**, including the possibility that a historic integration referencing C1A becomes broken. It is **NOT** a factual claim of no Eventarc triggers. It authorizes **only** the old C1A IAM-private compiled-OFF Cloud Run service cleanup subject to existing other current UID/etag/revision/image/runtime-SA/IAM/traffic/health safety gates, one request and no retries. This is a scoped **exception to the Eventarc-visibility gate only**, NOT to the entire guarded-cleanup policy.

No new IAM grant, Eventarc API enablement/disablement, old-account role changes, production deployment or H1B W1–W6 authorization follows. C1A separate runtime service account and Artifact Registry image/repository are **NOT part of this service-only delete**, even if service deletion later succeeds; they each require later independent no-other-reference checks. Never touch `oldx-owner-read`, other Cloud Run services, Firebase/Firestore/KMS, billing, production or new H1B mediator resources.

## 2. Grounding from existing completed evidence — DO NOT REPEAT

- Actual C1A read-only preflight: `READ_ONLY_PASS_WITH_LIMITS` on exact historic service UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`, expected revision `oldx-step05-gateway-00001-thd`, direct IAM bindings empty, dedicated runtime SA `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com` uniqueId `102194769236111252832`, exact image `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off@sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a`.
- First conditional DELETE script STOP `C1A_RECONCILING_OR_UNKNOWN`, `WRITE_ATTEMPTED=FALSE` due default-false absent JSON v2 `reconciling` field, with subsequent read-only diagnostic `RECONCILING=ABSENT`, `GENERATION=MATCH`, `TERMINAL_CONDITION=CONDITION_SUCCEEDED`, `REVISION_PAIR=MATCH`, `SA/IMAGE=MATCH`, `ETAG=PRESENT`.
- Second v2 conditional DELETE source STOP `C1A_LIVE_CLI_READ_FAILED`, `WRITE_ATTEMPTED=FALSE`: direct IAM succeeded, Eventarc read permission denied.
- Under separately approved temporary project-only Eventarc Viewer, one all-location Eventarc CLI LIST returned NONZERO with saved stderr: API unused or disabled; the conditional Viewer **was actually removed and verified via IAM readback**. All prior one-shot markers CONSUMED.
- Latest `gcloud services list --enabled` read-only Owner screenshot: `EVENTARC_API_STATE=NOT_IN_ENABLED_LIST`. **NO successful Eventarc trigger listing** was obtained. UNKNOWN dependencies remain ACCEPTED ONLY under Option B.
- These checks are historic evidence. No regeneration of old build/images/scans/SDK tests, S3/S3B or IAM grants.

## 3. NEW distinct, guarded Option B script — prepared, NOT Cloud-executed

GitHub source `scripts/step05_c1a_option_b_service_only_conditional_delete_once_20261126.py`
- first-containing immutable commit: **`388a485b72ebdb7885176dba3ceb839b0202fba8`**
- Git blob: **`aa2f2f54f8360e09caa7ec018d948c35c18458cf`**
- independent SHA256 of GitHub readback: **`595131d4c025506a74174f528eb33b38b7f998f87c95c0e00c9640565f62b109`**
- same previously prepared v2 guarded C1A source with NEW marker `~/.oldx-step05-c1a-option-b-conditional-service-delete-once-20261126` and flag `--delete-c1a-service-only-option-b-once`. The specific **live Eventarc trigger-list call alone** is removed in accordance with the approved risk exception. All other service safety guards, private previous evidence checks, current service IAM verification, v2 `validateOnly=true`, exact ETag conditional deletion and ONE no-retry attempt remain.
- additionally reads prior consumed second v2 **STOP/no-write** marker AND previous exact conditional Eventarc Viewer grant **REMOVED_AND_VERIFIED** marker + private JSON summary. It refuses operation if missing/mismatch, checks original retention deadline **28 November 2026 23:19 IST** (2026-11-28 17:49 UTC). It does not call Eventarc or regrant IAM.
- records `eventarc_dependency_inventory=UNVERIFIED_OWNER_ACCEPTED`, specifically never fabricates "no triggers" or all-dependencies-PASS. The script's embedded local synthetic guard checks execute in Owner Cloud Shell **before Cloud/marker**; do not claim tests executed in cloud now. Static GitHub source read-back and SHA256 verified.
- fresh **direct** v2 service GET must match full name, exact frozen UID, ETag, active or absent false `reconciling` **and** CONDITION_SUCCEEDED, generation/observedGeneration, ready+created revision, no env/volumes, same image/SA, one 100% no-tag traffic state, no Invoker-IAM bypass. Fresh direct IAM policy read must show no bindings (does not substitute for unknown inherited/project IAM). Any mismatch stops before write.
- one **validate-only DELETE** with exact fresh ETag, then at most one **real etag-conditional DELETE** of **only** `projects/oldx-staging/locations/asia-south1/services/oldx-step05-gateway` if every mandatory guard passed. It may be irreversible; Cloud Run service delete also removes revisions per Google docs. Any network error after write may mean unknown result — **never retry/delete one-shot marker**. An Operation receipt (accepted or done) is NOT service absence confirmation. A separate read-only operation/service state confirmation is required before describing deletion as complete.

Official v2 API: https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/delete describes required full resource name, `etag`, `validateOnly` and Operation response.

## 4. Exact one-paste command for Owner Cloud Shell

Use already authenticated `yasminparmar087@cloudshell` (Google Cloud project `oldx-staging`). This **can actually permanently delete the old C1A service and its revisions** if all safety checks pass. It does NOT delete SA/image/Registry and does not touch H1B. Paste every line, no outer parentheses.

```bash
bash -euo pipefail <<'OLDX_C1A_OPTION_B'
umask 077
d=$(mktemp -d "$HOME/oldx-c1a-option-b-source.XXXXXXXX")
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/cleanup.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/388a485b72ebdb7885176dba3ceb839b0202fba8/scripts/step05_c1a_option_b_service_only_conditional_delete_once_20261126.py'
printf '%s  %s\n' '595131d4c025506a74174f528eb33b38b7f998f87c95c0e00c9640565f62b109' "$d/cleanup.py" | sha256sum --check --status
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/cleanup.py"
python3 -B "$d/cleanup.py" --delete-c1a-service-only-option-b-once
OLDX_C1A_OPTION_B
```

If download/hash/syntax check fails, no script execution and no deletion attempt occurs; do not remove checksum or adjust SHA. If the Python script runs and STOPs, its unique marker is consumed. No repeat.

Output classes (not predicted): `C1A_SERVICE_DELETE_RESULT=STOP`, `WRITE_OUTCOME_UNKNOWN_STOP`, `DELETE_ACCEPTED_PENDING_COMPLETION`, `DELETE_OPERATION_DONE_NEEDS_READBACK`; `C1A_WRITE_ATTEMPTED=FALSE/TRUE`. If TRUE, **never issue another delete**; read the exact operation/status separately. Do not claim success merely from attempted DELETE, and do not upload access tokens/private policy JSON.

## 5. Final boundary

Original C1A retention permission expires **28 Nov 2026 23:19 Asia/Kolkata**; no auto-cleanup or auto-extension. Owner's approval of Option B is not an approval to extend expiry if execution STOPs. Actual at authoring: `C1A_OPTION_B=OWNER_APPROVED_SOURCE_PREPARED`, `C1A_CLOUD_RUN_SERVICE_DELETED=NO`, `C1A_SA_IMAGE_DELETED=NO`, `C1A_EVENTARC_DEPENDENCIES=UNKNOWN_ACCEPTED_FOR_SERVICE_ONLY`, `H1B_W1-W6/H2/PRODUCTION=NO_GO`.
