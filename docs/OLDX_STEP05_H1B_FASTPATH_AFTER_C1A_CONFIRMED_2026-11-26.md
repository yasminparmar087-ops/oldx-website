# OLDX Step 05 — FASTPATH: H1B G1 permission preflight, keep residual C1A assets untouched

**26 Nov 2026 IST. SOURCE-ONLY + new read-only diagnostic source; no Google Cloud or WSL execution by assistant.** Repo `yasminparmar087-ops/oldx-website` branch `security-hardening-review`.

## Latest actual Owner endpoint

Latest Cloud Shell owner screenshot after C1A Option B service deletion `DONE_NO_ERROR` + service GET `404_NOT_FOUND` yielded:
```text
C1A_SA=EXACT_UID_PRESENT
C1A_IMAGE=METADATA_READ_OK
C1A_OTHER_REFERENCES=NOT_YET_CHECKED
CLOUD_WRITES=NONE
```
C1A old service cleanup is **COMPLETE**. The exact separate C1A SA and image exist and their other dependencies have NOT been checked; **retain them** rather than delaying H1B for optional destructive cleanup. Shared `oldx-staging-images` repository, old `oldx-owner-read`, other services and data untouched. Both C1A service DELETE and readback markers consumed—never repeat.

Owner now said **"ok aagal vadho, pan zadapi rasta shodho"** (continue, find a quicker path). This permits source-only preparation and a bounded read-only G1 inquiry, NOT a new H1B deployment/IAM grant/Registry push or H2/production activation.

## No-repeat progress preserved

[Canonical H1B fastpath G0–G6](OLDX_STEP05_H1B_FASTPATH_FINAL_OPERATION_AND_C1A_DECISION_2026-11-26.md) and [H1B prior bounded operation proposal](OLDX_STEP05_H1B_PRIVATE_OFF_ONE_SHOT_PREFLIGHT_AND_OPERATION_PACKET_2026-11-25.md) established:
- H1A frozen **ONE** owner WSL linux/amd64 candidate Docker image `oldx-h1a-c2-mediator-off:local-20261124t195244z`, local Docker image ID `sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`. Local child `sha256:2e555bd98424d29b32a7bb3409a45e2c257569ff632085e4ff0e3a9ab4413b5f`, config `sha256:c71c7268e08f9ed91a92fd4e82e499a7331c3a071985cebcede7d76efbdf5b71`. These **are not remote image digests**.
- H1A SBOM 15 packages, saved Grype 12 distinct HIGH/0 Critical, OFF/nonroot loopback tests PASS_WITH_LIMITS; Owner accepted **only** bounded max 24h IAM-private compiled-OFF, no-real-data risk (not a production image approval). **No rebuild, no rescan, no Docker cleanup of retained local image.**
- WSL isolated native Linux SDK 594.0.1 smoke S2 PASS_WITH_LIMITS; **WSL fresh CloudSDK config did not inherit authenticated Owner Cloud Shell tokens**. Do not copy token databases or generate service account keys. Original WSL Windows SDK timeouts/S1/S1R/S2 and owner Shell S3/S3B markers all CONSUMED.
- S3B actual scoped Owner Cloud Shell result `S3B_SERVICE=ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS`, `S3B_SA=ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS`; proposed new `oldx-c2-website-mediator` and `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` absent at that previous snapshot. **Not proof they can now be created or are still absent.** Avoid repeating earlier lists until immediately before any approved resource creation.
- Existing shared Registry in `oldx-staging/asia-south1` previously verified. No new H1B image has been pushed; **no remote immutable digest**, no H1B service/SA/IAM Cloud writes performed.

## New shortest safe next step: G1 owner effective permissions (two read-only method calls)

Created `scripts/step05_h1b_fastpath_g1_effective_permissions_readonly_once_20261126.py`:
- pinned first commit: `373c5d6002f50bb588c58a7c2ca16ab0b3828992`
- Git blob (exact GitHub source readback): `5c3742c5ca9bb5c90895fae6ad64b5e91b4bc77d`
- new one-shot marker: `~/.oldx-step05-h1b-g1-effective-permissions-readonly-once-20261126`, consumed on any execution; **not yet run in owner Cloud Shell**.
- Requires nonroot Linux, an existing `gcloud` executable, and explicit already-authenticated Yasmin Owner account for access token. Uses two official read-only `testIamPermissions` REST methods, despite their HTTP `POST` verb: (1) Project `oldx-staging` Cloud Resource Manager permissions `iam.serviceAccounts.create/delete/actAs`, `run.services.create/delete/setIamPolicy/get`; (2) existing `oldx-staging-images` Registry repository `artifactregistry.repositories.uploadArtifacts/downloadArtifacts/get`, `artifactregistry.versions.delete`. Fails closed on HTTP, schema, timeout, unknown permission or missing set; does not print token/IAM policies. Saves restricted sanitized summary and prints permission status as `RETURNED` or `NOT_RETURNED`.
- `H1B_G1_RESULT=READ_ONLY_WITH_LIMITS` only when required **project SA create, Cloud Run create + project-scoped delete and Registry upload/get** are returned by the test calls. This still **does not certify** future service account's `actAs` (resource does not exist yet), authenticated WSL image transport, effective future Cloud Run service IAM, cleanup ability for every future resource, or H1B GO; `NOT_RETURNED` means absent from *this response*, not a complete diagnosis of global permissions.
- Only source and static safety properties checked; **not live-run nor claiming tests passed**. No Cloud writes, IAM mutations, API enablement, Registry image push, Docker build, hosted HTTP, SA creation, service creation or deletion.

Google official references: Cloud Resource Manager `projects.testIamPermissions` https://docs.cloud.google.com/resource-manager/reference/rest/v1/projects/testIamPermissions ; Artifact Registry `repositories.testIamPermissions` https://docs.cloud.google.com/artifact-registry/docs/reference/rest/v1/projects.locations.repositories/testIamPermissions . Both are permission-query APIs, not policy mutations. Project tests do not replace new-SA `actAs`/new-service identity readbacks.

## One paste — Owner Google Cloud Shell ONLY

```bash
bash -euo pipefail <<'OLDX_H1B_G1_FAST'
umask 077
d=$(mktemp -d "$HOME/oldx-h1b-g1-fast-source.XXXXXXXX")
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/g1.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/373c5d6002f50bb588c58a7c2ca16ab0b3828992/scripts/step05_h1b_fastpath_g1_effective_permissions_readonly_once_20261126.py'
test "$(git hash-object "$d/g1.py")" = '5c3742c5ca9bb5c90895fae6ad64b5e91b4bc77d' || { echo 'STOP: SOURCE_HASH_MISMATCH'; exit 2; }
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/g1.py"
python3 -B "$d/g1.py" --h1b-g1-effective-permissions-readonly-once
OLDX_H1B_G1_FAST
```

Any completed script invocation consumes this distinct marker, including failure. **Never rerun/remove marker, bypass hash validation, switch accounts or print token.** Return only `H1B_G1_*` lines/screenshot. If no `READ_ONLY_WITH_LIMITS`, do not proceed to any H1B write; instead classify specific permission status and choose least-privilege remediation separately.

## G2 quickest credible path — ONLY after G1 and specific owner login approval

Avoid a new build or exporting a ~205MiB local image to Cloud Shell. Reuse existing owner WSL native Linux SDK at its installed absolute path with its isolated `CLOUDSDK_CONFIG`; make ONE explicit supervised **`gcloud auth login --no-launch-browser`** for Yasmin on WSL (without copying tokens/config between machines), then configure Docker authentication **only for `asia-south1-docker.pkg.dev`** using an isolated Docker config/credential helper, and push the **already-built** frozen H1A image *once* to a unique new Registry tag. This creates local OAuth credentials and Docker config and later a metered Registry image push, so **requires new explicit H1B operation/login/push consent**, and verified push+pull rights first. Google official basis: https://docs.cloud.google.com/sdk/gcloud/reference/auth/login ; https://docs.cloud.google.com/artifact-registry/docs/docker/authentication ; https://docs.cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling .

Before any H1B deployment: obtain the actual immutable registry OCI/index and linux/amd64 config/digest, match frozen local custody, provision only one fresh no-key SA, verify `actAs` and invoker effective IAM, deploy one new compiled-OFF private no-data Cloud Run, run at most 4 authorized new-only probes, then same-session guarded new-only cleanup. **Do not start H1B W1–W6 until the entire new-only cleanup path is feasible and the owner separately approves the exact limited writes.** Existing C1A SA/image may be left untouched with `PARTIAL_CLEANUP_WITH_LIMITS` and does not block H1B readiness.

## Present status

`C1A_CLOUD_RUN_SERVICE=CONFIRMED_REMOVED`; `C1A_LEFTOVER_SA_IMAGE=PRESENT_REFERENCES_UNKNOWN_RETAIN`; `H1A_LOCAL_IMAGE=PASS_WITH_LIMITS_CONSUMED`; `H1B_S3B=PASS_WITH_LIMITS_CONSUMED`; `H1B_G1_PERMISSIONS_SOURCE=READY_NOT_EXECUTED`; `H1B_G2_WSL_AUTH=NOT_APPROVED_OR_DONE`; `H1B_W1-W6=NO_GO`; `H2/PRODUCTION=NO_GO`. Continue from this checkpoint, not previous historic H1B/C1A planning documents.
