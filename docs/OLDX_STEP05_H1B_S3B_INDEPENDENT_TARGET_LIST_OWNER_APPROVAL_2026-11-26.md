# OLDX Step05 H1B S3B — separate Owner-approved NEW target list confirmation

## 26 Nov 2026 — S3B ACTUAL OWNER CLOUD SHELL READ_ONLY_PASS_WITH_LIMITS; TWO NEW TARGET NAMES ABSENT FROM SUCCESSFUL LISTS

The user's latest owner Cloud Shell screenshot confirms the **CORRECTED bootstrap** was executed after the earlier Bash-parse-only failure, without rerunning original S3. It shows:
```text
S3B_SERVICE=ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS
S3B_SA=ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS
S3B_RESULT=READ_ONLY_PASS_WITH_LIMITS
S3B_REASON=BOTH_TARGETS_ABSENT_IN_SUCCESSFUL_SCOPED_LISTS
S3B_CLOUD_WRITES=NONE
```
**Actual interpretation, no overclaim:** one successful `gcloud run services list --region=asia-south1 --project=oldx-staging` (explicit Owner account) did not list the candidate `oldx-c2-website-mediator`, and one successful `gcloud iam service-accounts list --project=oldx-staging` did not list `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`. Both are **point-in-time negative scoped list evidence**, not proof of future collision-freedom, effective IAM, ability to create resources, or permission to deploy. Original S3 owner/project #38472235077/Registry source data were verified from original private evidence offline; they were not queried again. No IAM, Registry, Cloud Run deployment, Firebase, Firestore, KMS, billing or production mutation was authorized or done by S3B.

The old first S3B pasted heredoc had a Bash parse error **before Python**, not a consumed S3B run; the screenshot then shows the corrected second bootstrap with actual S3B PASS. Now the distinct `~/.oldx-h1b-s3b-target-list-once-20261126` marker is **CONSUMED**. Do NOT rerun S3B or consumed original S3/S1/S1R/S2/H1A preflights/tests/scans. The frozen S3B source is `scripts/step05_h1b_s3b_cloudshell_exact_target_lists_once_20261126.py` at commit `4a8f1e8f54c1cc9df76a1f5da772ac52858573dd`, SHA256 `872b9ffa97b82d568bd2913f76b34186fdd324a13fac3e72932161d005fca244`; previously completed 20 new focused synthetic/offline tests remain evidence, no rerun necessary.

**Next milestone**: prepare (source-only) one finite H1B IAM-private compiled-OFF no-real-data deployment and new-only guarded cleanup decision packet; independently verify needed project/target IAM, exact retained H1A artifact/image digest and tag collision, residual 12 HIGH risk window, cost scope and dependable same-session cleanup prior to any cloud writes. **W1–W6 NOT AUTHORIZED; H2/production NO-GO.** Existing C1A private default-OFF separate retention authority ends **28 Nov 2026 23:19 IST**; an explicit bounded extension or guarded **C1A-only** cleanup decision is needed before the deadline, no auto renewal/cleanup.

> **26 Nov 2026 — OWNER CLOUD SHELL SCREENSHOT: S3B BOOTSTRAP SHELL PARSE ERROR BEFORE RESULT, NOT S3B CLOUD STOP.** Screenshot displays `bash: line 6: unexpected EOF while looking for matching \`)\`` and returned directly to Cloud Shell prompt; there are **no `S3B_` status lines** and no evidence that Python S3B ran or that either API list request occurred. On the screenshot the `d=` `mktemp` line appears to have incorrectly ordered/missing nested quotation around command substitution. The safest **corrected bootstrap line** is `d=$(mktemp -d "$HOME/oldx-h1b-s3b-source.XXXXXXXX")` (remove the unnecessary outer double quotes), without changing the pinned Python S3B script/commit or original consumed S3 marker. Complete corrected Bash heredoc was checked by `bash -n` **PASS** in isolated assistant-local syntax-only test; test of `mktemp` line PASS; no GitHub fetch/Cloud commands executed in this syntax-only test. If the S3B marker is **absent**, the original separately approved one-shot target-list attempt remains available; if marker already exists, DO NOT rerun—inspect its receipt. Avoid claiming the marker is absent without local inspection. Owner should retry the **corrected bootstrap only once** under the already-approved S3B scope, and return S3B result/screenshot; any S3B STOP consumes the marker and must not be retried. No new IAM/deploy/Registry action is approved.

**26 November 2026 IST.** Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Source-only preparation; **no S3B Cloud Shell API calls have been executed** by this assistant. Do not confuse the new S3B with original S3's consumed one-shot.

## Actual owner consent, narrowly scoped

After S3's original actual result `S3_RESULT=STOP / TARGET_STATUS_UNRESOLVED_STOP` and one additional offline reading of saved `new-service.stderr`, Owner replied **"ha manjuri chhe"** to exactly **one new, separately guarded, read-only confirmation of the proposed NEW Cloud Run service and NEW no-key service account**. No authorization to rerun Owner/project/Registry calls already completed in S3; no authorization to login, switch account, fix IAM, create SA, push image, deploy Cloud Run, change Firebase/Firestore/Rules, billing, Cloud Run or production.

Original actual S3 Cloud Shell readbacks:
- **Owner:** `EXPECTED_OWNER_ACTIVE`; **project:** `oldx-staging` number `38472235077` ACTIVE; **registry:** `oldx-staging-images` DOCKER in `asia-south1` — PASS, NEVER repeat casually.
- **NEW service** `oldx-c2-website-mediator`: original `gcloud run services describe` exit1; saved `stderr` exact `Cannot find service [oldx-c2-website-mediator]`; negative text evidence but original parser did not recognize it. Do NOT rewrite original S3 STOP as PASS or infer raw HTTP404.
- **NEW SA** `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`: original `API_NOT_FOUND_REPORTED_REVIEW_REQUIRED`, not definitive IAM/existence proof.
- No writes; S3 marker `~/.oldx-h1b-s3-cloudshell-readonly-once-20261125` **CONSUMED**; no re-run, marker deletion or new `gcloud auth list`.

## S3B new method: TWO LIST requests max, once per target type

Google's official references confirm `gcloud run services list --region=... --project=...` and `gcloud iam service-accounts list --project=...` are list/read operations: [Cloud Run CLI](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/list), [IAM CLI](https://docs.cloud.google.com/sdk/gcloud/reference/iam/service-accounts/list).

The new S3B runner validates the ORIGINAL S3 marker and saved Owner/project/registry JSON **offline**, checks exact Owner `yasminparmar087@gmail.com` and project `oldx-staging` #`38472235077`, but **does not reissue their original Cloud API calls**. Then, on Owner's Cloud Shell only, it performs at most:
1. **ONE** `gcloud --quiet --account=yasminparmar087@gmail.com --project=oldx-staging run services list --region=asia-south1 --format=json`, checking the exact NEW `oldx-c2-website-mediator` name.
2. **ONE** `gcloud --quiet --account=yasminparmar087@gmail.com --project=oldx-staging iam service-accounts list --format=json`, checking exact NEW `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, **only if first list succeeded without the target**.

If the response is unsuccessful, wrong schema, unauthorized/403, incomplete, timeout (>20s per command), unexpected warning, or the exact candidate is present, **STOP** and do not treat it as absent. Lists are read-only and may disclose metadata to the authenticated user; full outputs stay in private Owner Cloud Shell evidence, NOT GitHub. `READ_ONLY_PASS_WITH_LIMITS` can only mean the TWO candidate names were **not in two successful lists at that point in time**; it is not a guarantee against races, permissions outside these lists or a deployment approval.

## New source and offline test receipts

- NEW `scripts/step05_h1b_s3b_cloudshell_exact_target_lists_once_20261126.py`, first-containing/pinned commit **`4a8f1e8f54c1cc9df76a1f5da772ac52858573dd`**, exact Git blob `cea59d54362104dba12c07d1ea58ce0b057231bd`, independently SHA256 of Git-blob-identical local source **`872b9ffa97b82d568bd2913f76b34186fdd324a13fac3e72932161d005fca244`**. Github fetched-back blob matches locally syntax-checked and tested source.
- NEW `tests/integration/test_step05_h1b_s3b_cloudshell_target_lists_20261126.py`, first commit **`a4f9639eaf359ae7cec9f414aa785d73f0c68459`**, Git blob `21aed1deca1f5334290c0eadcd585ff7b62e52e4`, independent exact content SHA256 **`20a01832994749a87ed1f4390b9e0fc318282d1787f2e85f13a4bf6181b024ce`**. Exact GitHub test file bytes matched after normalized double-quote spelling; same test implementation re-run locally.
- **20 NEW focused offline tests PASS, 0 failed** under Python 3.x; positive/negative JSON list examples, exact-service/SA collision, 403/unknown/incomplete/invalid schemas, old S3 marker evidence, Owner/project mismatch, symlink rejection, no flags STOP, one local fake CLI invocation with explicit project/account/region. Python syntax check PASS. Tests use synthetic fixture data and an inert local shell script; **no real Google API, no prior H1A builds/scans or S1/S1R/S2/S3 retried**.

## Exact owner Cloud Shell one paste — S3B only

Use current **Owner Google Cloud Shell**, not Windows CMD or WSL. One paste exactly, no surrounding `(` or `)`:

```bash
bash -euo pipefail <<'OLDX_S3B'
umask 077
d="$(mktemp -d "$HOME/oldx-h1b-s3b-source.XXXXXXXX")"
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/s3b.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/4a8f1e8f54c1cc9df76a1f5da772ac52858573dd/scripts/step05_h1b_s3b_cloudshell_exact_target_lists_once_20261126.py'
printf '%s  %s\n' '872b9ffa97b82d568bd2913f76b34186fdd324a13fac3e72932161d005fca244' "$d/s3b.py" | sha256sum --check --status
python3 -B "$d/s3b.py" --new-target-lists-once
OLDX_S3B
```

The bootstrap fetches only the immutable GitHub Python **source**, verifies SHA256 before execution and does NOT download any SDK/archive or install software. The new S3B script creates a **NEW distinct one-shot marker** `~/.oldx-h1b-s3b-target-list-once-20261126` BEFORE Cloud calls, with new private `0700` evidence folder and per-call stdout/stderr/exit stored there. If STOP occurs after marker creation, marker is **CONSUMED**, do not rerun S3B or delete/rename it. If source fetch/check fails, script never started and report error rather than bypass checks. At any unexpected Cloud authorization prompt, stop and report; do not improvise login/permission changes.

Expected successful classification (NOT actual outcome yet):
```text
S3B_SERVICE=ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS
S3B_SA=ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS
S3B_RESULT=READ_ONLY_PASS_WITH_LIMITS
S3B_REASON=BOTH_TARGETS_ABSENT_IN_SUCCESSFUL_SCOPED_LISTS
S3B_CLOUD_WRITES=NONE
```
Any STOP is a genuine reportable outcome, and the result cannot be predicted before the owner runs it. Share only nonsensitive last `S3B_` terminal lines/screenshot; never upload full private output/token/credential files to GitHub.

## Boundaries and next milestone

S3B **is not** pre-write effective IAM/cost/image digest confirmation. Even if both are absent in the two new listings, H1B W1–W6 requires a **separate explicit finite deployment + exact NEW-only cleanup/rollback consent** and checks of effective IAM/roles, current Registry tag/digest, min/max OFF-only configuration, operator identity and exposure. Existing H1A owner-accepted 12 HIGH CVEs only narrow **max24h IAM-private, compiled-OFF, no-user-data** future experiment; this acceptance alone never permits Cloud creation. H2/C2-enabled/production remain NO-GO.

The existing C1A `oldx-step05-gateway` separate private/OFF service retention permission ends **28 Nov 2026 23:19 IST**, not extended or automatically cleaned by S3B; obtain separate guarded cleanup or bounded new retention decision before expiry. No old IAM/resources, original S3 marker or historical completed tests are to be altered.

**Checkpoint status as of preparation:** `S3=ACTUAL_STOP_CONSUMED`, `S3B=OWNER_APPROVED_SOURCE_TESTED_NOT_EXECUTED`, `S3B_NEW_MARKER=NOT_YET_VERIFIED_ON_OWNER_CLOUD_SHELL`, `H1B_WRITES/H2/PRODUCTION=NO_GO`.
