# OLDX Step 05 C1A — Actual Eventarc permission denial and least-privilege recovery decision

**26 Nov 2026 IST, source-only follow-up; NO IAM or Cloud resource write.** Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. This is the newest checkpoint after the [previous CLI diagnostic handoff](OLDX_STEP05_C1A_DELETE_V2_NO_WRITE_CLI_READ_STOP_AND_NEXT_DIAG_2026-11-26.md).

## 1. ACTUAL owner Cloud Shell evidence (latest screenshot)

The owner executed the separately pinned, one-shot diagnostic `scripts/step05_c1a_cli_read_failure_diagnostic_once_20261126.py` (source commit `5faa602e8bce504553bcf91a52e6430fcab769b2`), yielding:
```text
C1A_READ_DIAG_IAM=NO_DIRECT_BINDINGS
C1A_READ_DIAG_EVENTARC=PERMISSION_DENIED
C1A_READ_DIAG_RESULT=STOP
C1A_READ_DIAG_REASON=IAM_OR_EVENTARC_DIAG_NEEDS_REVIEW
C1A_CLOUD_WRITES=NONE
C1A_RESOURCE_DELETED=NO
```
The C1A Cloud Run **direct service-level IAM policy** read succeeded and had no direct bindings. This does **not** by itself establish absence of inherited project/org IAM. The subsequent Eventarc regional trigger `gcloud eventarc triggers list --location=asia-south1` was denied in the Owner Cloud Shell. This **explains** the prior generalized `C1A_LIVE_CLI_READ_FAILED`. The CLI error classification is grounded in the screenshot; no raw unredacted stderr from private evidence was independently inspected. It establishes no permission to proceed with destructive deletion, and it does **not prove the absence of Eventarc triggers or that any trigger exists**.

The diagnostic's distinct one-shot marker `~/.oldx-step05-c1a-cli-read-failure-diagnostic-once-20261126` is now **CONSUMED**. Previously consumed: C1A read-only preflight; first delete STOP/no-write `C1A_RECONCILING_OR_UNKNOWN`; separate v2 field diagnostic `reconciling=ABSENT` with CONDITION_SUCCEEDED; second delete v2 STOP/no-write `C1A_LIVE_CLI_READ_FAILED`. Do **not** rerun or remove any markers, or repeat completed SDK/H1A/S3/S3B scans/builds/readbacks. **No C1A DELETE request has ever been sent in these guarded attempts; C1A service, image and runtime SA remain.**

## 2. Why a small access change may be needed, and boundaries

Google's documented Eventarc list method requires **`eventarc.triggers.list`** on the trigger parent collection: https://docs.cloud.google.com/eventarc/docs/reference/rest/v1/projects.locations.triggers/list and https://docs.cloud.google.com/eventarc/docs/reference/rpc/google.cloud.eventarc.v1 .

Google's predefined project-scoped **Eventarc Viewer `roles/eventarc.viewer`** includes `eventarc.triggers.list`, but also numerous other **read-only** Eventarc permissions, and is broader than just the single required action: https://docs.cloud.google.com/eventarc/standard/docs/access-control . An even more restrictive project custom role with only the needed list permission could be prepared if supported under current IAM setup; it requires IAM administration and role lifecycle work. **Neither role is already verified granted**, and the previous owner's approval for C1A exact guarded cleanup did **not** authorize new IAM grants or temporary escalation. DO NOT run `gcloud projects add-iam-policy-binding`, create roles, switch to a different Google user, impersonate, grant Editor/Admin, or bypass Eventarc checks without a separate exact owner decision.

Possible grounded paths:
- **Preferred zero-IAM-change path**, if an *already authorized, owner-approved* principal can read all project Eventarc trigger metadata without taking privileges away from/adding privileges to another account: use its existing permission for one supervised read-only dependency check. Do not assume such a principal is available, or use the old user slated for removal implicitly.
- **If no such principal exists**, request **explicit separate approval** to temporarily grant the Owner `yasminparmar087@gmail.com` limited **read-only Eventarc access on `oldx-staging` only**; prefer a minimally scoped custom role limited to `eventarc.triggers.list` if feasible, or the built-in `roles/eventarc.viewer` with the acknowledged broader Eventarc metadata visibility. Only an IAM administrator with existing policy-edit permissions may execute the approved grant. Track the exact policy change and **explicit supervised revocation** after the one-time list (no assumption of automatic expiry). No new IAM write is performed in this packet.
- Without reliable permission, preserve the STOP; do **not** fabricate an empty list, remove the dependency guard, or delete anyway.

## 3. Corrected next read scope — all Eventarc locations in this project

Google CLI officially documents:
```bash
gcloud eventarc triggers list --location=- --project=oldx-staging --format=json
```
It aggregates **all Eventarc locations**, including global: https://docs.cloud.google.com/sdk/gcloud/reference/eventarc/triggers/list . A check limited to `asia-south1` was **not sufficient** to rule out a global or cross-region trigger targeting a service in `asia-south1`. The eventual new **separate, newly approved one-shot read-only** script must authenticate the same approved principal, use `--location=-`, require complete successful list/pagination (no partial/unreachable results), check every destination's Cloud Run target and destination region for `oldx-step05-gateway`, and stop on any match, missing metadata, permission error, or ambiguity. Do not assume the command alone proves absence of every other type of dependency.

Even a complete successful negative Eventarc list **does not by itself authorize deletion**; the new guarded service-only write must again check fresh exact C1A UID, ETag, ready/revision, image, runtime SA, traffic, direct/inherited IAM and available dependency evidence, use Cloud Run v2 `validateOnly`, then at most ONE conditional DELETE if all gates pass. A delete response is async, requiring a different read-only confirmation. C1A service account and pinned image remain separate no-reference cleanup decisions, never deleted with the service or shared repository.

## 4. Owner decision needed; current status and deadline

**NEXT**: Choose whether to allow an existing authorized operator to conduct the bounded all-locations Eventarc read, or authorize **temporary Owner-only, project-only Eventarc read role** (and later explicit revocation). A temporary grant is a **distinct IAM mutation** from the previously approved C1A cleanup. Do not start any new IAM grant or Cloud DELETE until user explicitly approves its exact scope.

Original C1A private/OFF retention approval expires **28 Nov 2026 23:19 IST**. There is no scheduled/automatic cleanup or extension. If unable to resolve Eventarc permission by then, obtain a new explicit finite retention decision or escalate to a supervised administrator; do not assume that a deadline permits bypassing safety gates.

**Exact current status:** `C1A_CLI_IAM=NO_DIRECT_BINDINGS_PASS`; `C1A_EVENTARC=PERMISSION_DENIED`; `C1A_CLI_DIAGNOSTIC=STOP_CONSUMED`; `C1A_DELETE_REQUESTS_SENT=ZERO`; `C1A_SERVICE/SA/IMAGE=NOT_DELETED`; `C1A_CLEANUP=BLOCKED_ON_DEPENDENCY_VISIBILITY`; `H1B_W1-W6/H2/PRODUCTION=NO_GO`.
