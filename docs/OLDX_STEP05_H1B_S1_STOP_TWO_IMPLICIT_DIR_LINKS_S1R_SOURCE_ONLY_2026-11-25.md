# OLDX Step05 H1B S1 STOP — two implicit directory symlinks; S1R offline recovery source ready

**25 Nov 2026 IST.** Source-only recovery preparation. Read [original approved S1 packet](OLDX_STEP05_H1B_NATIVE_LINUX_GCLOUD_S1_OWNER_APPROVED_SOURCE_RECEIPT_2026-11-25.md), actual user terminal screenshots and canonical Issue #17. Branch `security-hardening-review`. **Original S1 is STOP/CONSUMED. S1R is NOT YET APPROVED OR EXECUTED on owner WSL.**

## Actual owner screenshots (no inference of SDK startup)

The original S1 script completed fresh Google official docs and one exact archive download, then printed:
```
S1_RESULT=STOP
S1_STOP_REASON=ARCHIVE_DANGLING_LINK
S1_VERSION=594.0.1
S1_EXPECTED_SHA256=c6fdba4cb1551b0da7c1d744eb0dfaf68b59861238d6a6b5ef6bad1ba596b567
S1_EVIDENCE=/root/oldx-h1b-native-gcloud-s1-20261124T210443Z
S1_CLOUD_OR_GCLOUD_ACTION=NONE
```
One initial read-only manually written follow-up used an incorrect evidence-folder timestamp and stopped `ARCHIVE_NOT_FOUND_OR_UNSAFE`; no SHA result from that attempt. A corrected **read-only offline** inspection then selected the exact local evidence directory from the consumed original S1 marker. Actual output:
```
EVIDENCE_FOLDER= oldx-h1b-native-gcloud-s1-20261124T210443Z
ARCHIVE_SHA256=MATCH
TOTAL_MEMBERS=36776
UNLISTED_LINK_TARGETS=2
TYPE=IMPLICIT_DIR
LINK=google-cloud-sdk/platform/gsutil/third_party/requests/tests/certs/mtls/client/ca
TARGET=google-cloud-sdk/platform/gsutil/third_party/requests/tests/certs/expired/ca
TYPE=IMPLICIT_DIR
LINK=google-cloud-sdk/platform/gsutil/third_party/requests/tests/certs/valid/ca
TARGET=google-cloud-sdk/platform/gsutil/third_party/requests/tests/certs/expired/ca
DIAGNOSIS=READ_ONLY_COMPLETE
```
**Conclusions with limits:** exact local compressed archive bytes matched the previously frozen Google-official checksum; 36,776 tar members. The two unmatched symlink targets are **implicit parent directories** inside the archive tree, not evidence of outside-root/missing directories. The original validator's demand for an *explicit tar member* for every symlink target was unnecessarily strict for this verified archive. **No extraction has yet succeeded; archive content does not itself prove SDK executability, identity or Cloud privileges.** Both S1 and follow-up diagnostics consumed their intended actions; do not rerun the original S1 one-shot marker or re-download.

## New independent S1R recovery source (NOT execution consent)

Prepared `scripts/step05-h1b-s1r-offline-extract-once-20261125.py`:
- First-containing commit [e237de6](https://github.com/yasminparmar087-ops/oldx-website/commit/e237de69206170112a202d466cb7b2f59c8eee81), full Git **blob** `c162c38e1281e83dd2abb6fd75020d3d48178b97`, independently locally tested **SHA256** `34af0511c08093d7a402f86641f44d82306c3b4fefa13837b37775b44954344c`; exact GitHub blob read-back matched locally tested source.
- Reads only exact original consumed S1 marker and private original `receipt.json` (requires STOP + exact reason + checksum + no gcloud/Cloud actions). Root WSL amd64 Python>=3.12, native Linux filesystem, >=2GiB free, empty target and fresh S1R one-shot marker prerequisite. **No download, gcloud execution, login/auth, global PATH, Windows SDK configuration changes or Cloud API.**
- Opens the *existing* local archive only; independent SHA256 validation, full 36,776-member structural review with size/special/path/duplicate/cycle/parent guard, and allows **only two exact frozen** implicit-directory symlink name->target pairs from the real read-only receipt. Does **not** broadly waive unknown dangling links. Tar extraction uses Python `filter='data'` into a fresh 0700 Linux-only *incomplete* directory, confirms native `bin/gcloud` and bundled Python file metadata, then atomically renames into `/root/oldx-tools/native-gcloud-594.0.1` on success. Does **not** execute extracted code.
- Creates a **distinct** marker `/root/.oldx-h1b-native-gcloud-s1r-offline-extract-once-20261125` before extraction, never deletes/reuses original S1 marker. On any STOP, retains incomplete private destination for review; no automatic rerun, retry, bypass or unrelated cleanup. Running may fail due to as-yet-unverified runtime extraction conditions and would consume the new marker. The runner is **prepared only**; the owner has NOT yet approved executing this new S1R attempt.

## New focused verification

New test `tests/integration/test_step05_h1b_s1r_offline.py`, first commit [ba100e1](https://github.com/yasminparmar087-ops/oldx-website/commit/ba100e1b9690abd4e8f2ba6eca964d29b94d123a), Git blob `9be04178a87490d8018bb3a45a4e99b9a19ad911`. Exact locally verified remote-source blobs for runner/test matched the GitHub readbacks. New isolated local Python test command `python3 -B tests/integration/test_step05_h1b_s1r_offline.py` in matching root layout: **6 PASS, 0 FAIL**. Cases: one approved implicit parent, outside-root link, truly missing target, unapproved implicit link, traversal and no-flags STOP. Python syntax compile both PASS. This is **synthetic tar** testing only; did not use owner's real 94.8MB archive or WSL, and does NOT prove full 36,776-file extraction will pass. No prior H1A/Docker/Syft/Grype, H1B preflight/version probes or Step04 work repeated.

## Next ONE decision; preserve existing trial limits

**Separate exact owner choice to execute S1R once:** reuse only existing local verified archive; allow only the two exact symlinks; perform one guarded extraction to fresh Linux filesystem private destination with isolated S1R marker; NO download/CLI invocation/Cloud write. Upon explicit approval, supply an immutable GitHub SHA256-checked one-paste source bootstrap with exact flag `--recover-existing-archive-once`. Do not issue/run this as already authorized by the consumed S1 consent. If owner refuses/doesn't reply, maintain HOLD.

`H1B_S1=STOP_ARCHIVE_DANGLING_LINK_CONSUMED`; `S1R=SOURCE_ONLY_PREPARED_NOT_APPROVED`; `S2/S3=NOT_AUTHORIZED`; `W1–W6/H2/PRODUCTION=NO_GO`. H1A scanned local image retained and marker consumed. Old C1A IAM-private default-OFF service has separate retention approval **through 28 Nov 2026 23:19 IST**, with no automatic extension or cleanup. No old resources changed in this source-only work.
