NaN scratch Grype one-shot (PREPARED, NOT EXECUTED)

## Actual owner Cloud Shell screenshot — 23 November 2026 ~20:08–20:09 IST

Owner's previous preflight (same Google Cloud Shell, project `oldx-staging`) reported:

```text
A8_HOME_FREE_MIB=39
A8_HOME_FILESYSTEM_ID=2065
A8_TMP_FREE_MIB=10160
A8_TMP_FILESYSTEM_ID=67
A8_REGISTRY_HELPER_CONFIGURED=True
A8_CONFIGURED_HELPER_EXISTS=True
A8_NEW_SCAN_STARTED=NO
A8_CLOUD_ACTIONS=NONE
A8_BUILD_AND_SLSA_RERUN=NONE
```

Meaning: HOME has only 39 MiB free, while `/tmp` is a **distinct** filesystem with 10,160 MiB (~9.92 GiB) free at time checked, and the exact host `asia-south1-docker.pkg.dev` has a configured and installed Docker credential helper. Grype absent in Cloud Shell, but existing `curl`, `tar`, and helper are present from earlier preflight. This is sufficient to TRY a single new-image Grype registry scan with large temporary files in `/tmp`, NOT a guarantee of peak resource or successful package vulnerability coverage. Do not re-run past Cloud Build/SLSA/on-demand unsupported scan, nor update IAM/billing/Firebase/Cloud Run/production.

## Authoritative one-shot Grype script, source-only

- Committed on branch `security-hardening-review`: [scripts/step04-a8-grype-new-digest-once.sh](../scripts/step04-a8-grype-new-digest-once.sh).
- **Immutable first-containing source commit:** `4143923068933523bb62a16cb16eff997431d736`.
- **Script Git blob SHA1:** `d7ac05021e0d20ff2e23629ca981007e64f8e997`, verified by GitHub fetch against local source.
- **Script SHA256:** `3670c7157ace87ac66e21ab6259c890c660f9cc351c466b0ace1bb48d3abdc47`, computed locally for that same blob.
- **Scanner:** official Anchore Grype Linux x86_64 **v0.122.1**, released 18 Nov 2026. Original official release asset `grype_0.122.1_linux_amd64.tar.gz` with independent GitHub release API SHA256 `f1ba7e2917ee1395618de20a98da0aa7c0fb1788927797651047c50502a37538`; verification mandatory BEFORE binary extraction/execution. Official GitHub release URL only.
- **Image exact immutable digest:** `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`.
- Scratch exclusively `/tmp/oldx-a8-grype-new-digest-2506826f`, scanner DB/config/cache/temp also `/tmp`; no root package install or Docker daemon required; `registry:` image source uses the existing private Docker credential helper. No access token printed; any Grype output JSON kept private.
- Durable **no-repeat marker** created **immediately before one actual Grype invocation**: `$HOME/.oldx-a8-grype-new-digest-2506826f-attempted`. If marker or workdir already exists, STOP; NEVER remove marker or blindly rerun after ambiguous scan attempt. `timeout` 1800 seconds, no automatic retry. `--scope squashed` scans packages in final image, not all historical deleted layers. DB auto-updated only within TMP on first use. Do not claim a fresh DB until real DB result is captured.
- Raw JSON and stderr private in TMP; script prints sanitized severity match counts / up to first 25 CRITICAL/HIGH IDs, source userInput match, report hash, DB built date if available. Grype counts are package/vulnerability MATCHES, not unique CVE count. Even zero matches does not imply secure image if BellSoft distro advisory coverage is weak. On completion, gzip full report and copy to `$HOME/oldx-a8-grype-new-digest-2506826f.json.gz` **only if at least 8 MiB free remains**; otherwise the report is TMP-only and MUST be transferred privately before Cloud Shell reset.
- No IAM/API/billing settings, Cloud Run/Firestore, production/deploy, Registry upload, Google scan or build/verifier reruns. Remote Registry read/data egress and public Grype DB downloads may have associated costs; ₹100 was a soft incremental planning target, **not a hard provider cap**.

## Exact owner-run command — Cloud Shell Linux ONLY, prepared NOT run

Fetch exact immutable GitHub script source and verify its SHA256 BEFORE executing:

```bash
(
  set -e
  p='/tmp/oldx-a8-grype-source-2506826f.sh'
  if [ -e "$p" ]; then echo 'STOP_A8_SCRIPT_PATH_ALREADY_USED'; exit 1; fi
  curl --fail --location --silent --show-error --retry 0 --connect-timeout 15 --max-time 60 \
    'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/4143923068933523bb62a16cb16eff997431d736/scripts/step04-a8-grype-new-digest-once.sh' -o "$p"
  echo '3670c7157ace87ac66e21ab6259c890c660f9cc351c466b0ace1bb48d3abdc47  /tmp/oldx-a8-grype-source-2506826f.sh' | sha256sum -c -
  bash "$p"
)
```

This command is one-shot: `STOP` means pause and diagnose **without rerunning this whole command or deleting markers**. Distinguish `A8_GRYPE_SCAN_COMMAND_EXIT_CODE=0` plus `A8_GRYPE_REPORT_SCHEMA=PASS` and `A8_GRYPE_SOURCE_IMAGE_REFERENCE_MATCH=True` from an unproven image, and triage all actual severe findings. If `A8_PRIVATE_FULL_REPORT=TMP_ONLY_HOME_CAPACITY_LIMIT`, collect it through a separately safe private transfer before TMP resets. Previous old local Grype report 1 CRITICAL/5 HIGH/12 MEDIUM/2 LOW is DIFFERENT image and must never be substituted.

## Authoritative references

- Anchore private registry credentials: https://oss.anchore.com/docs/guides/private-registries/
- Anchore registry: source, `--scope squashed`: https://oss.anchore.com/docs/reference/grype/cli/
- Release identity: https://github.com/anchore/grype/releases/tag/v0.122.1

**Status:** `A8_GRYPE_ONE_SHOT_SOURCE_PREPARED_NOT_RUN`; `STEP04=HOLD`, `PRODUCTION=NO_GO`. Other outstanding gates: new-image scan + CVE fixability, focused runtime/default DB guard, G4 other DB/effective invoker, G8 gross spend / rollback and owner launch decision.
