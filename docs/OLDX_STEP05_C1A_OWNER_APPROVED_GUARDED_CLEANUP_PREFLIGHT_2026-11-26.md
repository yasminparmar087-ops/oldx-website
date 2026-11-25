# OLDX Step05 C1A — Owner-approved guarded cleanup; FIRST exact-resource read-only preflight

**26 November 2026 IST, source-only preparation, owner Cloud Shell has NOT run preflight/deletion.** GitHub: `yasminparmar087-ops/oldx-website`, `security-hardening-review`. This handoff is newer than the prior 28-Nov retention recommendation in [H1B and C1A final decision packet](OLDX_STEP05_H1B_FASTPATH_FINAL_OPERATION_AND_C1A_DECISION_2026-11-26.md).

## Owner decision, permitted scope and current actual state

Owner responded **"ha manjuri chhe"** to the exact proposal to **clean up ONLY the existing C1A private OFF gateway's newly created resources**, subject to validating exact resource identity, current IAM/traffic and no dependencies, stopping before any deletion on mismatch. This is **NOT permission** to touch existing `oldx-owner-read`, any other old service/revision, future H1B `oldx-c2-website-mediator`, existing shared Registry repository, Firebase/Auth/Firestore/Rules, domain/website, billing or production. It is NOT consent to broaden identity, rerun consumed historic build/C1A/B/Step04 tests, or blanket delete resources.

C1A prior retention is explicitly through **28 Nov 2026 23:19 Asia/Kolkata** (no auto cleanup). Owner's new cleanup decision allows a staged **exact-resource guarded cleanup** before the deadline. Current evidence contains historic C1A UIDs and immutable image; not fresh deletion authorization if live identities differ. **No Cloud write or deletion has happened in this assistant response.**

## Historical frozen C1A identities — require live readback before any delete

| C1A only | Expected exact frozen identity |
| --- | --- |
| Project / region | `oldx-staging` / `asia-south1`; project numeric `38472235077` previously owner-verified in S3 |
| Owner principal | `yasminparmar087@gmail.com` as verified in owner S3 |
| Cloud Run service | `oldx-step05-gateway`, UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b` |
| Only expected ready/created revision | `oldx-step05-gateway-00001-thd` |
| Runtime SA | `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com`, uniqueId `102194769236111252832` |
| Exact immutable image | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step05-gateway-off@sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a` |
| Expected service traffic/IAM | 100% only to frozen revision, no traffic tags, mandatory IAM check, no direct policy bindings, no provider secrets/env/mounted volumes |
| Protected (not targets) | `oldx-owner-read` and all its tags/revisions/IAM, future H1B mediator and SA, all shared repo or other images |

Latest S3/S3B proven owner/project/Registry checks are already consumed. Do **not** repeat them; current C1A-only readback is necessary for destructive-action safety and not a replay of prior HTTP/image build/tests.

## New prepared read-only preflight — NO DELETE

`scripts/step05_c1a_guarded_cleanup_preflight_once_20261126.py` pinned source commit `19cb68afe4ec2cf33a630d8167a2393b7877ed66`, Git blob `f9b591d061bdd1db050e608c675934c1da07e6ee`, independently computed actual GitHub file SHA256 `d9095afd47926c111d7183883d8b044288c4cfbd4d466eecb0b356cfea81b6e0`. This script was source-read back from the exact immutable GitHub commit. **Do not describe it as Cloud-executed or offline-test-PASS.** Runtime Cloud Shell results remain UNKNOWN.

The script performs at most **four NEW C1A-only READ calls** under exact Owner and project (`--quiet --account=... --project=...`, each max20s, no retry):
1. `run services describe oldx-step05-gateway --region=asia-south1` — checks exact v1 Service schema, UID/name, ready+created revision, 100% one-revision untagged traffic, expected runtime SA, exact immutable image digest, no service env/volumes, no `invoker-iam-disabled=true`.
2. `run services get-iam-policy oldx-step05-gateway --region=asia-south1` — service direct bindings empty.
3. `run revisions list --service=oldx-step05-gateway --region=asia-south1` — exactly historic revision, no newly created revision.
4. `iam service-accounts describe oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com` — exact email and uniqueId, not disabled.

The runner stops on mismatch, permission error, malformed JSON, timeout or unknown schema. Creates a **NEW separate** once-only marker `~/.oldx-step05-c1a-cleanup-readonly-once-20261126`, with private `0700` evidence, simple nonsecret summary and no credentials copied. Do not rerun after any attempt; preserve stdout/stderr privately. This script has no `gcloud delete`, `update`, `set-iam-policy`, image push or Cloud invocation of H1B and cannot delete anything.

**Sufficient preflight status for continuation only**:
```text
C1A_VERIFIED_STAGES=service,service_iam,revisions,runtime_sa
C1A_CLEANUP_PREFLIGHT=READ_ONLY_PASS_WITH_LIMITS
C1A_REASON=EXACT_HISTORIC_C1A_IDENTIFIERS_MATCH
C1A_CLOUD_WRITES=NONE
C1A_RESOURCE_DELETED=NO
```
If `STOP`, do NOT delete or modify anything or re-run marker; inspect the saved C1A-specific receipt. A PASS is **not** permission to delete SA/image without further **fresh dependency checks**; it only permits proceeding to design and execute exact guarded cleanup under the owner's existing scoped decision.

## Exact one-paste Owner Google Cloud Shell command (bootstrap only), once

Must use **Owner Google Cloud Shell**, not Windows CMD/WSL. Paste all lines from `bash -euo pipefail <<'OLDX_C1A_PREFLIGHT'` through closing `OLDX_C1A_PREFLIGHT` with no extra parentheses. Avoid the earlier S3B `d=` quote mismatch; use the literal correct `d=$(mktemp ...)` below.

```bash
bash -euo pipefail <<'OLDX_C1A_PREFLIGHT'
umask 077
d=$(mktemp -d "$HOME/oldx-c1a-cleanup-source.XXXXXXXX")
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/c1a.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/19cb68afe4ec2cf33a630d8167a2393b7877ed66/scripts/step05_c1a_guarded_cleanup_preflight_once_20261126.py'
printf '%s  %s\n' 'd9095afd47926c111d7183883d8b044288c4cfbd4d466eecb0b356cfea81b6e0' "$d/c1a.py" | sha256sum --check --status
python3 -B "$d/c1a.py" --c1a-cleanup-preflight-once
OLDX_C1A_PREFLIGHT
```

Source bootstrap is exactly one immutable GitHub content GET plus SHA256, not a new binary or Docker pull. If download/hash fails, source runner did NOT execute and the C1A marker should remain unused; do not bypass checksum. If script STOPs, marker is consumed: do not delete or rerun. Share only last `C1A_` status lines screenshot, not full IAM metadata or credential/log files.

## After owner screenshot: staged exact-resource cleanup (not yet run)

On a PASS, a **separately prepared** owner-guarded final write phase will re-read service UID/status immediately before delete; delete **only** exact `oldx-step05-gateway` service, never the similarly named `oldx-owner-read` or H1B. Verify deletion completion through targeted read. The old C1A runtime SA uniqueId and image digest must then each be checked for other attachments/references and deleted **only if safe**; stop/retain otherwise, with a clearly stated partial cleanup rather than fabricated full completion. No blind `--delete-tags` or shared Registry deletion. Existing owner consent is for the **guarded** C1A cleanup; don't request the same decision again, but don't execute unsafe changes when guard proof is missing.

No automatic cleanup is scheduled or running. If user does not execute or preflight STOPs, C1A remains until further owner action; prior retention approval expires at 28 Nov 2026 23:19 IST. C1A cleanup does not authorize H1B W1–W6, H2/production; `H1B=HOLD`.
