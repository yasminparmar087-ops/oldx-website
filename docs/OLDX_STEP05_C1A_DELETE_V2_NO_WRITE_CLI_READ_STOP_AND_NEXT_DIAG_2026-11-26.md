# OLDX Step05 C1A — Actual second service DELETE STOP, zero write, diagnose exact CLI read failure

**26 Nov 2026 IST.** Repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. This document supersedes any instruction to rerun the first or second C1A delete source.

## 1. Actual owner Google Cloud Shell evidence — NO RESOURCE DELETED

Screenshot after running exact pinned corrected C1A delete-v2 source `f4e6cf371629192f99eb34f246e2b1b3fe67d708` prints:

```text
C1A_LOCAL_GUARDS=PASS_SYNTHETIC_NO_CLOUD
C1A_SERVICE_DELETE_RESULT=STOP
C1A_REASON=C1A_LIVE_CLI_READ_FAILED
C1A_WRITE_ATTEMPTED=FALSE
C1A_SERVICE_ACCOUNT_DELETED=NO
C1A_REGISTRY_IMAGE_DELETED=NO
C1A_UNRELATED_RESOURCES_CHANGED=NONE_REQUESTED
```

The preceding distinct C1A v2 READ-only field diagnostic `READ_ONLY_DIAG_COMPLETE` established exact service UID, omitted protobuf false `reconciling`, `terminalCondition=CONDITION_SUCCEEDED`, observed/generation match, expected image/SA/revision, etag and traffic field presence; this overcame the *earlier* `C1A_RECONCILING_OR_UNKNOWN` issue. **Current STOP is different:** the v2 code successfully passed its local synthetic guards and got past fresh v2 service field validation, but `cli_json` raised its generic `C1A_LIVE_CLI_READ_FAILED` from either (a) exact `gcloud run services get-iam-policy oldx-step05-gateway --region=asia-south1 --format=json`, or (b) subsequent `gcloud eventarc triggers list --location=asia-south1 --format=json`. The screenshot/source does **not** establish which subcommand failed or the HTTP/CLI error; the old code captured stdout/stderr only in memory and did not save a per-stage error receipt. Do not claim permissions denied, API disabled, or Eventarc no dependencies without actual evidence. A read-only CLI command could have nonzero exit, output-size failure, etc.

**Decisive limitation:** `WRITE_ATTEMPTED=FALSE` means neither `DELETE?validateOnly=true` nor the REAL etag-conditional DELETE was reached. The original first C1A delete STOP marker and **second** delete-v2 marker `~/.oldx-step05-c1a-conditional-service-delete-v2-once-20261126` are both **CONSUMED**, with no deletion. DO NOT replay, edit/delete markers, or issue another DELETE without resolving exact CLI/read dependency and a new fully guarded source/action. The existing C1A service, its SA and its image therefore remain subject to separate owner retention/cleanup action, not automatically removed.

## 2. NEW distinct read-only, fail-closed CLI failure diagnosis

New Python source `scripts/step05_c1a_cli_read_failure_diagnostic_once_20261126.py` at immutable first-containing commit `5faa602e8bce504553bcf91a52e6430fcab769b2`, Git blob `2ac725c9f6d65b031680a7f0e389c3363da52aea`, independent SHA256 of exact GitHub source text `06ed355ef68271cb6438832db5eabebc877f2a51ec6881547a3efb8634b1b44a`. Source read back; **no actual owner Cloud Shell run or standalone offline test result** at preparation time.

The script requires an actual Owner Cloud Shell Linux nonroot and verifies the consumed second delete marker contains `ATTEMPT_CONSUMED`, `RESULT=STOP`, `REASON=C1A_LIVE_CLI_READ_FAILED`, `WRITE_ATTEMPTED=False`. It makes a new one-shot private marker `~/.oldx-step05-c1a-cli-read-failure-diagnostic-once-20261126` and evidence folder (mode0700) BEFORE any Cloud request. No reuse of historic S1/S1R/S2/S3/S3B/C1A markers.

One bounded **C1A-only service IAM policy read** is first (20-second timeout, no retry); if successful, an exact scoped **asia-south1 Eventarc triggers LIST** is next (at most one call, also20s). Eventarc list requires `eventarc.triggers.list` according to the [official API IAM documentation](https://docs.cloud.google.com/eventarc/docs/reference/rest/v1/projects.locations.triggers/list), but do not assume that permission exists. Each call is explicitly pinned to `yasminparmar087@gmail.com` and `oldx-staging` without changing account/project configuration. On first read failure or changed IAM, the subsequent call is not executed. Failed CLI status is classified as `PERMISSION_DENIED`, `AUTH_UNAVAILABLE`, `API_DISABLED`, `CLI_COMMAND_OR_FLAG_ERROR`, `TARGET_NOT_FOUND_REPORTED`, `TIMEOUT`, `NONZERO_OTHER`, invalid schema or limit. Raw CLI stdout/stderr is stored privately in owner Cloud Shell only, not printed or uploaded to GitHub. Do not treat error classifications as absolute root cause until reviewed.

**No `DELETE`, `update`, `set-iam-policy`, `enable api`, `auth login`, service-account delete, Registry image delete, H1B Cloud writes or additional builds/tests/scans.** If list successfully returns no Eventarc triggers targeting this service, that is only **regional point-in-time** dependency evidence; it is not a grant of delete permission or complete proof of all dependencies.

## 3. Exact owner Google Cloud Shell command — new diagnosis only

Use existing `yasminparmar087@cloudshell` in project `oldx-staging` (NOT WSL/CMD). Paste exact block with no surrounding parentheses:

```bash
bash -euo pipefail <<'OLDX_C1A_CLI_DIAG'
umask 077
d=$(mktemp -d "$HOME/oldx-c1a-cli-diag-source.XXXXXXXX")
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/diag.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/5faa602e8bce504553bcf91a52e6430fcab769b2/scripts/step05_c1a_cli_read_failure_diagnostic_once_20261126.py'
printf '%s  %s\n' '06ed355ef68271cb6438832db5eabebc877f2a51ec6881547a3efb8634b1b44a' "$d/diag.py" | sha256sum --check --status
python3 -B "$d/diag.py" --diagnose-c1a-cli-reads-once
OLDX_C1A_CLI_DIAG
```

A one-time GitHub-source GET is SHA256 checked before the Python process. On download/hash failure, no Python call or S3/C1A changes; do not bypass the check. **On any attempted diagnosis, new marker is consumed even on STOP; do not run it again.** Report only `C1A_READ_DIAG_IAM`, `C1A_READ_DIAG_EVENTARC`, `C1A_READ_DIAG_RESULT`, `C1A_READ_DIAG_REASON`, `C1A_CLOUD_WRITES`, `C1A_RESOURCE_DELETED` from screenshot. Never upload raw private stderr/IAM data or credentials into GitHub.

## 4. Boundaries, deadline, next gate

Original C1A private/OFF retention authority through **28 Nov 2026 23:19 IST**, no timer or automatic extension/cleanup. Owner has approved **only guarded exact C1A new-resource cleanup**; another destructive source cannot be inferred approved on any unexpected dependency/permission result. If diagnostic STOPs, preserve markers and stop instead of bypassing IAM/Eventarc checks or deleting under uncertain safety. If it passes, separately plan next single exact-resource guarded deletion with fresh UID/etag and complete safety gates. Do not repeat successful C1A original v1/v2 or H1A/S3B tests. H1B W1–W6/H2/production remain NO-GO.

**Current:** `C1A_FIRST_DELETE=STOP_NO_WRITE_CONSUMED`, `C1A_SECOND_DELETE_V2=STOP_NO_WRITE_CONSUMED`, `C1A_CLI_READ_DIAG=SOURCE_READY_NOT_EXECUTED`, `C1A_SERVICE/SA/IMAGE=NOT_DELETED`.
