# BAJUTO / OLDX Step05 H2U — Owner actual 65-file import closure, NEW ESM link-only gate (27 Nov 2026)

## Owner actual static result, no repeats

Owner WSL screenshot at ~21:39 IST shows the previously approved **one-shot static source import closure PASS_WITH_LIMITS** on cached Node `24.22.3`:

~~~text
OLDX_H2U_CLOSURE_SOURCE_COMMIT=176a8e39e5fa8a1b3e2016f5938b3a569152f34d
OLDX_H2U_CLOSURE_FILES=65
OLDX_H2U_CLOSURE_SOURCE_BYTES=349667
OLDX_H2U_CLOSURE_EXTERNAL_IMPORTS=0
OLDX_H2U_CLOSURE_CONCLUSION=STATIC_IMPORT_SCAN_ONLY_NOT_LINKER_OR_RUNTIME_VERIFIED
OLDX_H2U_CLOSURE_MANIFEST_SHA256=12a52acef6548e2e356a3b28aa045ed15924bca31fa09df2c32c375686d87acc
OLDX_H2U_IMPORT_CLOSURE=STATIC_AUDIT_PASS_WITH_LIMITS
OLDX_H2U_IMPORT_CLOSURE_EVIDENCE=/root/oldx-h2u-import-closure.2oCNZVHV
OLDX_H2U_CLOUD_WRITES=NONE
OLDX_H2U_BUILDS_PULLS_SCANS=NONE
OLDX_H2U_H2_PRODUCTION=NO_GO
~~~

[Source scan implementation and original one-shot](OLDX_STEP05_H2U_OFF_HTTP_PASS_IMPORT_CLOSURE_NEXT_2026-11-27.md). The manifest is **local to Owner's WSL**; ChatGPT did not receive the 65 filenames or verify each file in that manifest, nor independently recompute the SHA. **Do not invent a COPY list from the aggregate numbers.** Old marker `/root/.oldx-step05-h2u-import-closure-audit-once-20261127` is CONSUMED. Previous H2U OFF HTTP 3/3 focused tests and prior H2S/H2T/H2N/H2R work are also completed; **never rerun old checks or clear markers**.

## New distinct source-only ESM link verifier: READY, NOT EXECUTED

New `scripts/c2-h2u-verify-existing-manifest-esm-link-only_20261127.mjs` source commit **`d8f214f5d706707236d32139c3524a46ce698902`**, Git blob **`df458b5d7f3847a94f035204c43098bc141380bd`**. This checker accepts **only** the screenshot-pinned existing `source-closure.json` SHA256, requires exactly 65 files / 349667 bytes / zero bare external imports, verifies every listed file's size, SHA256, safe path and non-symlink status, and builds Node `vm.SourceTextModule` objects without module evaluation. It then performs **static ESM linkage** (including named imports/exports) of the OFF Cloud Run entrypoint and each file in the manifest against the exact pinned set. Node built-ins are represented as unexecuted `vm.SyntheticModule` stubs; no third-party module is accepted. Missing/unlisted imports or named exports, source drift, parser errors, manifest drift, extra dependencies or linker failure must STOP. It never calls `evaluate()`, starts an HTTP listener, imports the actual H2U application module through Node runtime, builds an image, contacts Google or reads credentials.

A minimal *new* Node22 synthetic verifier/link check was performed locally to confirm that the VM `.link()` API is available and linking two synthetic modules leaves them at `linked` status; this is **NOT** a test of Owner's 65-file manifest or OLDX source. Actual H2U link outcome still unknown.

New one-shot WSL runner `scripts/step05_h2u_new_existing_manifest_esm_link_only_once_20261127.sh`, source commit **`5d1bfd83a14bfb38a1aff4fd159be35f276fae37`**, Git blob **`2ec0ec65b5a50bc889476d71b172410f09bca5f3`**. Reuses the existing owner-local `/root/oldx-h2u-import-closure.2oCNZVHV/source/` and `source-closure.json` without re-downloading the 65-file archive or replaying the previous scanner. Uses the same cached Node24 Docker image, nonroot UID, read-only mounts, network none and `--pull never`. Downloads only the **new** Git-blob-verified small verifier source, copies only the manifest to an isolated readable location, validates its fixed SHA, then launches Node24 with `--experimental-vm-modules` to **link, never evaluate** the 65 modules. Output log and SHA256 are retained in a new root-private evidence directory. This is NOT an OCI build, HTTP server smoke test, KMS API, Firestore transaction, IAM grant or Cloud Run deploy. A new distinct one-shot marker `/root/.oldx-step05-h2u-esm-link-only-once-20261127` is created immediately before the new linker invocation.

### One exact root Ubuntu WSL command — NEW linker audit only

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2u-link-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/link.sh" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/5d1bfd83a14bfb38a1aff4fd159be35f276fae37/scripts/step05_h2u_new_existing_manifest_esm_link_only_once_20261127.sh' &&
test "$(git hash-object "$d/link.sh")" = '2ec0ec65b5a50bc889476d71b172410f09bca5f3' &&
bash -n "$d/link.sh" &&
bash "$d/link.sh"
~~~

Success only if `OLDX_H2U_ESM_LINK_AUDIT=PASS_SOURCE_LINK_ONLY_WITH_LIMITS`, `OLDX_H2U_ESM_LINK_SOURCE_FILES=65`, `OLDX_H2U_ESM_SOURCE_EVALUATED=FALSE`, and `CLOUD_WRITES=NONE`. No success claimed before owner executes. If STOP, do not rerun/reset marker, inspect local new evidence and correct the **new** verifier/packaging boundary only.

## What this does NOT authorize or prove

Even a successful link-only audit does **not** imply runtime evaluation, listening HTTP server, correct library behavior, dynamic import behavior, security of the artifact, complete OCI provenance, KMS signature, or Cloud Run IAM-private deployment. A separate **new source-only** exact 65-file manifest-driven COPY plan and standalone offline image test may be prepared after this outcome, but no image build/push, Cloud Run service creation, IAM changes, Firebase/Firestore writes, KMS GET/sign or production activation has been authorized. Maintain `STEP05=ACTIVE`, `H2/PRODUCTION=NO_GO`.
