# BAJUTO / OLDX Step05 — H2AM LOCAL PREFLIGHT: 3 missing child images; one consolidated Owner approval NEXT

Date 2026-11-28 ~23:52 IST. Source: Owner WSL-root actual screenshot of **read-only** preflight. Branch `security-hardening-review`.

## Actual Owner preflight results — no changes

```text
H2AM_MARKER=NOT_CONSUMED
mediator=LOCAL_IMAGE_PRESENT
gateway=LOCAL_IMAGE_NOT_CONFIRMED
backend=LOCAL_IMAGE_NOT_CONFIRMED
reader=LOCAL_IMAGE_NOT_CONFIRMED
GRYPE=AVAILABLE
GRYPE_DB_DIRECTORY=PRESENT
/dev/sdd 1007G 28G 929G 3% /
=== PREFLIGHT FINISHED: NO SCANS OR WRITES ===
```

These are local Docker image inspect results, **not a registry 404 or missing cloud image**. H2AJ proved four image digest pushes PASS; Docker Buildx `--push` did not load the other three into the local Docker image store. Prior H2AK pulled the Mediator digest and scanned it. Disk appears ample (929GB on the reported filesystem); local Grype DB directory exists but **usable schema/cache status has not yet been independently verified**. H2AM is NOT CONSUMED. H2AJ/H2AK consumed markers untouched. No new Docker pull, scan, runtime execution or Cloud operation in this preflight.

## Confirmed H2AM execution hazard before writing

Verified remote HEAD `8f5df51075d6cc42f0d32ad0c730b14611c03f87`; `scripts/step05_h2am_selective_acceptance_once_20261128.py` Git blob `3adfb06ca66d6175f089ea797df21ca767779cca`; support `b9b57daa9a5b5f0304afc9cfc758630793454c07`, pinned proposal `c1cfcfa2f224e9a47dd6e896730c73e927b9b483`.

The H2AM runner creates an exclusive marker before it calls `Acceptance.local_image()`. It can pull missing exact images via `--allow-missing-exact-pulls`, but demands a pre-existing root-only private Docker auth JSON and does **not** create/refresh credentials. H2AJ's private auth config was explicitly deleted after its one-time build/push. Running H2AM now without fresh credentials or with a missing image would consume the new marker and STOP before completing acceptance.

## ONE efficient, controlled two-phase plan — not executed, requires explicit Owner consent

**A. Pre-H2AM local preparation (under new exact authorization):**
- Use already-installed native WSL gcloud SDK with already-verified Owner account `yasminparmar087@gmail.com`, project `oldx-staging`; create ONLY an isolated temporary Docker registry login based on a short-lived Owner OAuth token for `asia-south1-docker.pkg.dev`; NEVER overwrite global Docker config or print/share token.
- Pin the four role image references from `deployment/four-role/h2aj-four-immutable-images-pinned-proposal.json`; no mutable tags, new builds, registry pushes or other projects.
- **Pull only the three locally missing images, at most once each, by exact Linux/AMD64 child digest:** Gateway `sha256:921fbf4ff71b918c479e4a786868368640a494c16da08e54192f25e14dc1ec4d`; Backend `sha256:01ae540aa88ad0e3a6888994dd41b6b02b9d934a7a1d2e455f44b194f033b941`; Reader `sha256:822e2592b1010bfa94a1fe5bc75003712485abae0369f5252ece3863723eb077`. Do not pull or re-scan Mediator.
- Verify that all FOUR exact references exist in local Docker `image inspect` with matching RepoDigests/architecture/source role identity. If any pull is unknown or fails, STOP and report what completed; **no automatic retry or H2AM execution**.
- Check existing native `grype` and Grype cached DB status with app/DB auto-update disabled; do NOT download/rebuild database or rerun previous scan. No need to re-run 19 completed H2AM offline tests. If DB invalid/missing, STOP **before** H2AM marker.
- Download only three immutable GitHub source files (runner/support/proposal) into a fresh isolated root-private tree matching runner's `scripts/` and `deployment/four-role/` relative paths. Verify exact Git blobs `3adfb06ca66d6175f089ea797df21ca767779cca`, `b9b57daa9a5b5f0304afc9cfc758630793454c07`, `c1cfcfa2f224e9a47dd6e896730c73e927b9b483`. Keep Owner's older local checkout and untracked files untouched.
- Clear ONLY the freshly created temporary Docker OAuth config when done. No other local deletions.

**B. ONE existing H2AM attempt, after all prereqs PASS:**
- Launch exactly reviewed existing H2AM script with `--execute-h2am-once --owner-approved-selective-off-only` **without** optional pull/auth flags (all four exact images preloaded). Keep local Grype DB configured, no app/DB update, no registry access during scan.
- H2AM first imports already complete Mediator Grype JSON **57 matches, 18 HIGH, 0 Critical**, then runs Mediator **OFF runtime only**; this is the FIRST new runtime attempt and should capture original startup error, inspect actual OOMKilled, preserve logs and cleanup. **Never rescan Mediator**.
- ONLY after Mediator runtime PASS, run ONE Grype scan and OFF runtime each for Gateway, Backend and Reader, in that order. Per-role scan receipts durably saved before runtime; STOP on first failure/unknown, keep completed results, no automatic repeat/rescan. Local Docker containers are `--network none`, nonroot/read-only, no exposed port/credentials. No real KMS/Firebase/Cloud Run/prod operations.
- H2AM has a distinct one-time marker. Once marker is written, never rerun. Preserve H2AK/H2AJ/H2AI consumed markers and full evidence.

**Security and costs:** private registry reads/transfer may incur charges. H2AM is local-only; no Cloud Run service/deployment, IAM/KMS/Firebase writes, image push, source build, real user content, production or CVE acceptance. Previous 18 HIGH findings remain security HOLD pending disposition.

**No Owner approval to execute this future combined operation has yet been given in this turn.** When the Owner confirms this ONE scope, supply one SHA-validated WSL root command, with pre-marker checks and temporary auth cleanup, that prepares three exact images then calls the unchanged H2AM runner. Avoid a separate Grype-only roundtrip. Do not create a brand-new image or repeat existing CI/tests/builds/scans.

## Accurate checkpoint

`H2AJ=FOUR_REGISTRY_PASS`; `H2AK=CONSUMED_MEDIATOR_SCAN_COMPLETE_57_18HIGH`; `H2AL=READ_ONLY_DONE`; `H2AM_SOURCE=19_NEW_OFFLINE_PASS`; `H2AM_MARKER=NOT_CONSUMED`; `LOCAL_MEDIATOR_PRESENT`; `LOCAL_GATEWAY_BACKEND_READER=ABSENT_OR_NOT_CONFIRMED`; `GRYPE=AVAILABLE`; `GRYPE_DB_DIR=PRESENT_NOT_STATUS_VERIFIED`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
