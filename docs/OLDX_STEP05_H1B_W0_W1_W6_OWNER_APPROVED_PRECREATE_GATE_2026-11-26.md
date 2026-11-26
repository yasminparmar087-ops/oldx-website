# OLDX Step 05 H1B — owner W1–W6 staging-only approval; W0 exact-resource precreation gate

**26 November 2026 IST.** Repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. New owner message **"ha manjuri chhe"** expressly approves the combined previously described W1–W6 **staging-only** controlled operation, limited as below. Assistant did **not** execute any Google Cloud W0/W1–W6 action from the conversation; owner must run the verified source in their already-authenticated WSL. This document is source preparation, not evidence of cloud access.

## Frozen G2B actual success — no repetition

Actual Owner WSL screenshot on 26 Nov ~21:40 IST shows `H1B_G2B_PUSH_ATTEMPTED=TRUE`, `H1B_G2B_RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED`, `H1B_G2B_REASON=ONE_PUSH_VERIFIED` and `H1B_G2B_DO_NOT_REPEAT=TRUE`. One actual Docker push to existing Mumbai Artifact Registry succeeded.

Immutable **remote index digest**:
`sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`

Canonical image locator:
`asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`

Frozen amd64 child `sha256:2e555bd98424d29b32a7bb3409a45e2c257569ff632085e4ff0e3a9ab4413b5f`, config `sha256:c71c7268e08f9ed91a92fd4e82e499a7331c3a071985cebcede7d76efbdf5b71`, tag `h1b-g2b-20261126-dc07d8c3bd01d5310ae1`. **W2 image push already complete and consumed**, never repeat it, rebuild, rescan, delete local receipts, refresh old G1/S2/S3B or C1A checks. Prior G1 `READ_ONLY_WITH_LIMITS` confirmed needed project/Registry permissions at its timestamp (not an unconditional guarantee for future resource-level actAs).

## Exact NEW operational approval and limits

Owner now approves **one supervised, staging-only, IAM-private, compiled-OFF, zero-user-data H1B session** in project `oldx-staging`, region `asia-south1`; at most one NEW no-key runtime SA `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, one NEW Cloud Run service `oldx-c2-website-mediator` **by the exact remote immutable digest**, optional one service-level `roles/run.invoker` binding **only** for authenticated Yasmin, at most 4 specific service-only HTTP probes, then same-session **guarded NEW-only cleanup**. No project-wide/public Invoker, no `allUsers`/`allAuthenticatedUsers`, no real/synthetic Firebase Auth users, Firestore/media/KMS, no production/H2, no other services/old C1A assets or shared Artifact Registry repository changes. Cloud Run config intended: compiled OFF/default 503 for Product API, IAM Invoker check enforced, min 0/max 1, concurrency 1, 1 CPU/512MiB, 5s timeout, container port 8080, nonroot. Earlier Option B risk acceptance covers known 12 HIGH in private OFF/no-data experiment for no more than 24h after activation; prefer same-session cleanup. Any effective permission, unexpected inherited access, wrong service/image/SA/UID, missing cleanup ability or inaccessible runtime → STOP before first unsafe new resource write, and `STOP_MANUAL_RECOVERY` on any post-write unknown. Do not promise automatic cleanup.

A single combined owner consent does **not** eliminate necessary fail-closed runtime preconditions. The safest fast route is one fresh **W0 only** new-target collision check, then create/verify W1, use prior W2 digest as-is, and run the strictly guarded W3–W6 packet. Avoid repeating all broad earlier tests.

## New W0 read-only script — SOURCE PREPARED, not owner-executed

File: `scripts/step05_h1b_w0_precreation_target_readonly_once_20261126.py` 
Immutable initial commit: `0d94be8bf2fb13489e911310ea98303db95c7bca`
Verified exact GitHub blob: `9239d4774c25233021766a7ea6252134a0152c46`

Owner context: native `OLDX-Ubuntu-24.04` WSL root, existing **isolated** Google SDK config under `/root/oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config`; previously authenticated Owner `yasminparmar087@gmail.com`, project `oldx-staging`. Requires the consumed G2B marker with actual `PASS_REMOTE_FROZEN_DIGEST_VERIFIED` and exact saved unique tag. One **new** marker `/root/.oldx-h1b-w0-new-target-readonly-once-20261126`; on first Google request marker is consumed. W0 uses **only 3 HTTPS GETs**, not a repeat of G1 testIamPermissions, S3B old collision-list, or G2B image verification:
- Google Resource Manager project GET: exact `oldx-staging` active, project number `38472235077`.
- Cloud Run v2 **exact NEW** `asia-south1/oldx-c2-website-mediator` GET must return status **404**.
- IAM v1 **exact NEW** `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` GET must return status **404**.

A **200** for either new target means collision; **403/401/5xx/timeout** is unknown, NEVER inferred absent. Even two confirmed 404s are a *time-limited absence observation* and **not** new-SA `iam.serviceAccounts.actAs` proof (impossible before SA creation), effective new service IAM policy, current Cloud Run image pull authority, or automatic cleanup guarantee. Freeze W0 receipt; check creation collision and unique IDs at W1/W3. No W0 cloud resource writes, no image push or scans, no IAM changes.

## One exact paste — existing Ubuntu WSL root prompt, no Google Cloud Shell

```bash
umask 077
d=$(mktemp -d /root/oldx-h1b-w0-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/w0.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/0d94be8bf2fb13489e911310ea98303db95c7bca/scripts/step05_h1b_w0_precreation_target_readonly_once_20261126.py' &&
test "$(git hash-object "$d/w0.py")" = '9239d4774c25233021766a7ea6252134a0152c46' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/w0.py" &&
python3 -B "$d/w0.py" --w0-new-target-readonly-once
```

Expected successful **limits-aware** status:
```text
H1B_W0_PROJECT=ACTIVE_EXACT
H1B_W0_SERVICE=ABSENT_404_WITH_LIMITS
H1B_W0_NEW_SA=ABSENT_404_WITH_LIMITS
H1B_W0_IMAGE=PRIOR_G2B_REMOTE_DIGEST_FROZEN_NO_REPEAT
H1B_W0_NEW_SA_ACTAS=NOT_YET_TESTABLE
H1B_W0_RESULT=READ_ONLY_NEW_TARGETS_ABSENT_WITH_LIMITS
H1B_W0_REASON=PROJECT_AND_TWO_NEW_EXACT_RESOURCES_CHECKED
H1B_W0_CLOUD_RESOURCE_WRITES=NONE
H1B_W0_DO_NOT_REPEAT=TRUE
```
On STOP, do not replay, clear marker or bypass 403. Share only `H1B_W0_*` lines; don't share OAuth token/credentials. No registry push, service creation, IAM grant or cleanup was attempted by this W0 source.

## Next only after owner W0 output

Using this Owner approval and the actual W0 receipt, build/commit the **distinct W1–W6 bounded execution script** that performs precise new-only resource operations and same-session guarded cleanup; it must explicitly verify cleanup permissions before any write and check newly created SA `actAs` and absence of public IAM before service activation. If not possible, STOP before cloud writes. Never treat an old 404 snapshot as proof that the new names are still absent at creation time, nor the G2B image digest as proof of successful Cloud Run startup. **W1–W6 not yet run.**

Official APIs consulted 26 Nov 2026: https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services ; https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts ; https://docs.cloud.google.com/resource-manager/reference/rest/v1/projects/testIamPermissions ; https://docs.cloud.google.com/run/docs/managing/services .
