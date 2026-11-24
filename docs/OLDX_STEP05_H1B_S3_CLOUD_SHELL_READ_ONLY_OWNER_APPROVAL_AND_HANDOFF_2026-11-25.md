# OLDX Step05 H1B S3 — Owner-approved Cloud Shell READ-ONLY new-target preflight

**25 November 2026 IST.** Branch `security-hardening-review`, repository `yasminparmar087-ops/oldx-website`.

## 1. Actual owner authorization and START state

After actual owner-WSL `S2_RESULT=STARTUP_PASS_WITH_LIMITS` for the newly extracted v594.0.1 Linux SDK, the owner explicitly replied **"ha manjuri chhe"** to the proposal for **S3 read-only** checks only: active Owner account, exact `oldx-staging` project, existing Artifact Registry, proposed **NEW** private Cloud Run website mediator and proposed **NEW** no-key service account collision status. No IAM, billing, Firebase, Firestore, Cloud Run, Artifact Registry writes, login or deployment consent was granted.

Since S2 intentionally used a NEW **empty** `CLOUDSDK_CONFIG` on WSL, a successful local `gcloud --version` proves startup, **not usable authenticated Owner credentials**. Use the *already logged-in Google Cloud Shell* in the Owner account for this one S3 read-only attempt, rather than guessing/copied credentials or invoking `gcloud auth login` in WSL. Google Cloud Shell normally offers gcloud and account session (official docs [launch](https://docs.cloud.google.com/shell/docs/launching-cloud-shell), [auth](https://docs.cloud.google.com/shell/docs/auth)); a separate Cloud Shell authorization prompt may appear. The runner **never automatically authorizes**, switches account or logs in. If existing owner credentials are not usable, STOP; do not retry or silently authorize.

**ACTUAL EXECUTION FACT:** This assistant only prepared, tested and pushed source. It has NOT accessed the owner's Cloud Shell or made any Google Cloud API calls. `S3=OWNER_APPROVED_SOURCE_READY_NOT_EXECUTED`.

## 2. Exact targets and five permitted read-only commands

These values come from [the existing H1B operational packet](OLDX_STEP05_H1B_PRIVATE_OFF_ONE_SHOT_PREFLIGHT_AND_OPERATION_PACKET_2026-11-25.md); none is automatically assumed current until fresh readback.

| Ordered check | Expected target | Stop rule |
| --- | --- | --- |
| Owner | one active `yasminparmar087@gmail.com` account | wrong/multiple/no Owner => STOP before project |
| Project | `oldx-staging` / number `38472235077` / ACTIVE | mismatch => STOP |
| Existing Docker registry | `oldx-staging-images`, `asia-south1`, format DOCKER | mismatch/error => STOP |
| Proposed NEW service | `oldx-c2-website-mediator` in `oldx-staging/asia-south1` | exists => collision STOP; 403/unknown => unresolved |
| Proposed NEW service account | `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` | exists => collision STOP; 403/unknown => unresolved |

Only one call per entry and max20s per call, no retry, no broad IAM inventory. A `NOT_FOUND` or 404 result is **negative API evidence ONLY**, not conclusive nonexistence/effective access; even two reported 404s yield `READ_ONLY_PASS_WITH_LIMITS` and still require an independent pre-write target/access/cost review. 403/unauthenticated/transient errors never count as missing. Exact protected old `oldx-owner-read` and existing C1A `oldx-step05-gateway` are not queried or changed here.

## 3. Pinned source, exact minimal test receipt

New read-only script `scripts/step05_h1b_s3_cloudshell_readonly_once_20261125.py`, first-containing immutable commit **`475e0b9a22e56736a592cbe098f908bf5d6881c8`**, Git blob **`fb2dd41a54c3cf4632914dbb91c27591221b9dae`**, locally verified SHA256 **`915ad19df632565a67e12fed5e1a9913d57f503b7561d1d07b7dfc82b9acd70e`**. GitHub exact blob readback matched the locally tested bytes.

New `tests/integration/test_step05_h1b_s3_cloudshell_readonly_once_20261125.py`, first-containing commit **`50fc56c85b301ae5d902ff371a10c075ce0648e6`**, Git blob **`194ad2b02cd1ea52fe971858e15e6caf866eaf98`**, local SHA256 **`3acab3e781b2a8df210b47b6caab79c26d4f1549d8232d4fd953256115447b3f`**. Exact GitHub readback matched test file; isolated local `python3 ...` **11 new synthetic/offline tests PASS, 0 FAIL** plus Python syntax check PASS. These cover Owner active/wrong/multiple, project number mismatch, Registry identity, 403 vs 404, unknown response and existing service/SA. No real Google account/Cloud resource was queried in these tests; no previous H1A/S1/S1R/S2/redundant CI scan replayed.

The runner requires Linux **nonroot** and not a WSL Microsoft kernel, an existing `gcloud` executable, unique new S3 marker `~/.oldx-h1b-s3-cloudshell-readonly-once-20261125`; it creates that marker before any read requests and saves private `0700` evidence with per-call stdout/stderr/exit codes, summary and STOP reason. Only short nonsensitive result classifications appear on screen. Existing Cloud Shell CLI configuration may create standard command logs/cache, but the script does not modify active account or project configuration. If S3 marker is consumed (even STOP), no retry or marker deletion is approved.

## 4. Owner execution — Google Cloud Shell only, ONE paste

Open [Google Cloud Console project oldx-staging](https://console.cloud.google.com/home/dashboard?project=oldx-staging) in the intended **Owner Google account**, click **Activate Cloud Shell** terminal (NOT Windows CMD, NOT WSL). When the Cloud Shell `username@cloudshell:` prompt is ready, paste the entire block below, with no surrounding parentheses:

```bash
bash -euo pipefail <<'OLDX_S3'
umask 077
d="$(mktemp -d "$HOME/oldx-h1b-s3-source.XXXXXXXX")"
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/s3.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/475e0b9a22e56736a592cbe098f908bf5d6881c8/scripts/step05_h1b_s3_cloudshell_readonly_once_20261125.py'
printf '%s  %s\n' '915ad19df632565a67e12fed5e1a9913d57f503b7561d1d07b7dfc82b9acd70e' "$d/s3.py" | sha256sum --check --status
python3 -B "$d/s3.py" --s3-cloudshell-readonly-once
OLDX_S3
```

Source retrieval is a single immutable GitHub code GET and checksum verification, independent of the five Cloud read-only commands. No installer, Docker or provider write. If source download/hash fails, do not modify URLs or bypass; S3 process did not run. If any `S3_RESULT=STOP` or `STOP_PREFLIGHT`, do not rerun or delete the S3 marker; return terminal screenshot. If Cloud Shell presents a *separate* authorization prompt, stop rather than improvising authentication during this one-shot scope.

On successful verified Owner/project/Registry and both candidate target API-reported 404, `S3_RESULT=READ_ONLY_PASS_WITH_LIMITS` (NOT approval to create). Otherwise `S3_RESULT=STOP` and a specific reason. Share only `S3_OWNER`, `S3_PROJECT`, `S3_EXISTING_REGISTRY`, `S3_NEW_SERVICE`, `S3_NEW_SA`, `S3_RESULT`, `S3_REASON` screenshot; do NOT upload private Cloud Shell logs or credentials.

## 5. Unchanged gates and time limit

Original H1B WSL `auth list` 40s timeout and `--version` 12s timeout markers **CONSUMED**. New native SDK `S1` STOP on implicit tar link, `S1R` extraction PASS, `S2` native local `gcloud --version` PASS all one-shot markers **CONSUMED**; no repeat. H1A image build/Syft/Grype runtime also consumed. `S3` is a new bounded Cloud Shell workflow, NOT retry of the old consumed WSL preflight. H1A 12 HIGH CVE risk acceptance remains limited to future IAM-private compiled-OFF/no-data max24h. No new H1B image push, SA, Cloud Run, IAM, hosted probes, cleanup, H2 or production authority arises from these read-only results; W1–W6 remain distinct not authorized.

Existing C1A private/OFF retention through **28 November 2026 at 23:19 IST**, no automatic cleanup/extension. Need owner-approved new-only guarded cleanup or fresh limited retention decision before expiry; S3 itself does not change C1A.
