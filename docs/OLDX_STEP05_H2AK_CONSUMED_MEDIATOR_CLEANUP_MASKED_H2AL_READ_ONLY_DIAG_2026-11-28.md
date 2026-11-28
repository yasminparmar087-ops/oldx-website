# BAJUTO Step05 — H2AK consumed partial OFF-runtime acceptance: STOP SCANNING; read-only H2AL diagnostics first

28 November 2026, Owner WSL screenshot ~21:42 IST. GitHub branch `security-hardening-review`.

## Actual screenshot — what happened, with no assumptions

Owner verified official Linux Grype `v0.122.1` installer SHA256 and launched previously pinned H2AK one-shot. Terminal:

```text
H2AK_MARKER=CONSUMED_NO_REPEAT
H2AK_START=mediator
H2AK_RESULT=STOP_PARTIAL_LOCAL_READ_ONLY_ACCEPTANCE
H2AK_PRIVATE_EVIDENCE=/root/oldx-h2ak-images-20261128T160610Z-42e006
H2AK_H2AJ_MARKER=UNTOUCHED
H2AK_CLOUD_RUN_IAM_KMS_FIREBASE_WRITES=NONE
H2AK_PRODUCTION=NO_GO
H2AK_DO_NOT_REPEAT=TRUE
H2AK_REASON=LOCAL_CONTAINER_CLEANUP_UNKNOWN
```

**DO NOT REPEAT H2AK.** Its marker `/root/.oldx-step05-h2ak-four-pinned-image-acceptance-once-20261128` is **CONSUMED**; preserve it and ALL H2AJ/H2AI/H2AG markers and receipts. H2AJ four distinct immutable registry image builds/pushes previously PASS; not affected. H2AK only began `mediator`, and Gateway/Backend/Reader scans or OFF runtime checks did NOT start. `H2AK_PASS=mediator` was not printed, so Mediator OFF runtime is NOT VERIFIED. No Cloud Run, Firebase, KMS or IAM operations were performed.

## Deeper GitHub source audit — multiple definite defects; exact container failure still UNKNOWN

Read original `scripts/step05_h2ak_four_pinned_new_images_scan_offhealth_once_20261128.py` blob `f9b6f2f15cd1c5a59405d33f09e158434b7c2773` and existing four-role OFF server and Dockerfiles.

1. **Exception masking — confirmed source defect.** Function `smoke()` calls `docker stop --time 3 CID` inside its `finally` and immediately raises `LOCAL_CONTAINER_CLEANUP_UNKNOWN` if this stop is nonzero. This overrides the *original* smoke error or may override a successful HTTP check, so observed result alone **does not identify root cause**.
2. **`--rm` after exit — confirmed diagnostic weakness.** The container is started with `docker run --detach --rm`. If the Node process exits on startup or after a failure, Docker can auto-remove it, so the later `docker stop` may return nonzero and its logs can be unavailable. Do not assume the application crashed; inspect surviving Docker evidence first.
3. **Hidden stderr — confirmed source defect.** The subprocess wrapper captures STDERR and checks exit code, but discards STDERR on nonzero results. The original Node/Docker error is neither printed nor durably recorded.
4. **Scan receipt lost from summary — confirmed source defect.** `grype --output json` is invoked and `mediator-grype.json` is written and parsed BEFORE `smoke()`. `result.roles.mediator` is updated with scan severities only AFTER smoke returns. Any smoke failure therefore prevents severity counts in `sanitized-h2ak-summary.json`. The mediator Grype file **should** exist if the sequence reached `smoke`, but this MUST be verified from the owner filesystem; no claim that Grype has zero CVEs or is complete yet.
5. **Scan and runtime conflation.** A failed one-shot runtime test blocks preservation of already-generated scan status and prevents later roles. Future corrections must separate persistent per-role scan completion from runtime readiness and support bounded selective continuation without rescanning completed Mediator or deleting markers.
6. The OFF server's source checks `/healthz` HTTP 200 `state:OFF` and non-health 503 when not ready; the base Dockerfile uses nonroot and Node24. This does not prove actual container startup/exit or identify whether `--network none`, read-only root, resources, module loading, or process startup caused the first failure.

**Do not run more scans, builds, image pulls, Docker exec/run/stop/rm or cloud probes until existing evidence is read.** No new deployment permission has been implied. Any old H2AK retry remains prohibited.

## NEW source-only read-only diagnostic helper

Added `scripts/step05_h2al_read_only_h2ak_failed_mediator_triage_20261128.py` at immutable commit `436e4d2dab27b02b2f80698d884f3ee470405893`, verified Git blob `162f9bad3da82b5f66db6c822697e282e08829fc`. It:
- Reads only previous root-owned H2AK marker, exact `sanitized-h2ak-summary.json`, Mediator `mediator-grype.json` (prints just aggregate severity counts, not raw CVE list) and checks if other 3 Grype JSON files exist.
- Uses **LOCAL Docker read-only `ps -a`, `image inspect`, optionally `logs` of retained Mediator containers and bounded historical `events` (only past ~16:06–16:13 UTC)** to find exit status. Does not stop, remove, pull, run, exec, build, push or scan any Docker object; no network or Cloud commands.
- Redacts obvious bearer/token/password/secret patterns from any retained logs and prints only a short excerpt, not private Docker config or credentials.

The source was read back and its Docker method allowlist/source guards statically reviewed; **no H2AL execution result or runtime root cause has yet been observed**. After screenshot of its output, reconcile the exact underlying error and adjust source before any separately approved targeted scans. Do NOT falsely label the current H2AK partial as a full scan PASS.

### ONE WSL root read-only command (NOT a scan)

```bash
umask 077
test -f /root/.oldx-step05-h2ak-four-pinned-image-acceptance-once-20261128 &&
d=$(mktemp -d /root/oldx-h2al-readonly.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2al.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/436e4d2dab27b02b2f80698d884f3ee470405893/scripts/step05_h2al_read_only_h2ak_failed_mediator_triage_20261128.py' &&
test "$(git hash-object "$d/h2al.py")" = '162f9bad3da82b5f66db6c822697e282e08829fc' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2al.py" &&
python3 -B "$d/h2al.py"
```

No repeated scans, no new one-shot write marker, no new registry or Cloud requests. The `curl` only retrieves the immutable GitHub Python helper. If Docker events/logs have already disappeared, the helper will report insufficient Docker evidence; do not guess the underlying exit cause. We can then design one NEW instrumented non-scanning local OFF-runtime probe using immutable existing Mediator image with retained logs and idempotent cleanup, and only after Owner approval.

## Subsequent correction plan — SOURCE FIRST, then one consolidated approval

1. Use H2AL output to ascertain whether original Mediator Grype JSON is complete, capture actual severity counts once, inspect any retained local runtime/exit evidence; do not redo that scan if complete.
2. Fix future tool **source-only** to preserve first exception and sanitized stderr/exit code, avoid `--rm` masking, use unique retained named container for diagnostic phase with exact cleanup only after logs/exit recorded, make cleanup idempotent on already-deleted resources, separate scan and runtime per-role receipts and stop-on-unknown, require owner-approved bounded selective continuation.
3. Run NEW offline/unit tests for changed exception paths only. Do not rerun previous 23 integration tests, four builds/pushes, H2AG, H2AJ, Grype Mediator scan or older CI.
4. Present ONE fresh scoped Owner decision for any genuinely new local container/run and scans not yet completed for Gateway/Backend/Reader. Cloud Run and production remain OFF.

**Checkpoint:** `H2AJ=ACTUAL_FOUR_PRIVATE_REGISTRY_PASS_DO_NOT_REPEAT`; `H2AK=CONSUMED_PARTIAL_AFTER_MEDIATOR_SCAN_PHASE`; `MEDIATOR_GRYPE_JSON=NEEDS_READBACK`; `MEDIATOR_CONTAINER_ROOT_CAUSE=UNKNOWN_MASKED`; `OTHER_THREE_SCANS=NOT_STARTED`; `H2AL=READ_ONLY_SOURCE_PREPARED`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
