# BAJUTO Step05 H2AO — actual OCI identity repair / NEW offline evidence

Date: 2026-11-29 IST. Review branch ONLY security-hardening-review.
Start remote HEAD: 4e717ef55d5afcfb9d5d13e9c9ba02125cef1f57.
Source commit: 6493f7bc3544c7c8fbec60ee65ba960ea32a2c38. Final documentation commit follows it.
Status: SOURCE_IMPLEMENTED_OFFLINE_VERIFIED / ACTUAL_EXECUTION_NOT_AUTHORIZED_OR_RUN.
Step05 ACTIVE; security and G2/G4/G8/hosted gates HOLD; production OFF / NO-GO.

## Changed files and preservation

Added scripts/step05_h2ao_oci_identity.py; scripts/step05_h2ao_selective_continuation_once_20261129.py; tests/integration/step05_h2ao_identity_continuation_new_test.py.
Updated this receipt, AGENTS.md, living Handoff and existing confirmed H2AO task checkpoint; Issue #17 records the final remote SHA.
No original H2AM/H2AN source, tests, markers, evidence, app source, Dockerfiles, locks, immutable images, role/SA pins or Cloud settings changed. The existing local worktree remains behind358 with owner-modified Handoff and untracked .firebaserc; neither was overwritten. Isolated source was tested; GitHub commit/tree API saves intended files only with an expected-HEAD fast-forward lease and [skip ci].
Read AGENTS/latest Handoff, current confirmed H2AO task, H2AM source/support/tests/receipt, frozen proposal, H2AN source and actual receipts, Issue #17 latest checkpoints, and H2AJ source to inspect what historical manifests were retained. Old H2AJ retained readback hashes/index metadata, not reliably saved exact child raw bytes; no missing child proof is invented.

## Correct identity model and newly observed actual format

Docker containerd .Id may name the approved child manifest, while historical Grype imageID names the config. The old equality assumed identical digest semantics. The new verifier does NOT remove identity checks or equate unrelated digests.

Required chain:
approved role/ref + exact raw child SHA256 -> child manifest config.digest/config.size -> exact decoded raw config SHA256/size -> Grype source.target.imageID + exact source userInput -> linux/amd64, nonroot, role ENTRYPOINT/CMD/Env and rootfs.diff_ids -> local Docker RootFS and Config fields. Local Docker .Id must equal either this VERIFIED child digest or this VERIFIED config digest. Container inspect .Image may likewise equal only these two verified identifiers for its own role, with exact unique name/attempt/role labels. Actual identifiers are retained distinctly; no raw evidence is rewritten.
Reject indexes, artifacts, duplicate JSON keys, invalid media/config/layer descriptors, wrong bytes, wrong SHA/size/ref/role/platform/nonroot/rootfs/runtime fields, malformed schemas, truncated inspection and unproven IDs. Raw config contents/Env are never copied into public receipts.

Historical immutable evidence remains57 matches /18High /0Critical (other severities20Medium/6Low/11Negligible/2Unknown). Mediator Grype is forbidden in the new scan method.
Old report SHA256 e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92 is mandatory. Exact approved Mediator child is01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe; old Grype manifest31285b477845b9e10f76c4b7df425d200fa15db0e615b0cb4b639e4c3fc7aae4 is NOT substituted for it.

NEW bounded read-only schema inspection of the already-pinned private historical report found source.target.config is a BASE64 byte string, not literal JSON. First metadata snippet attempted JSON decoding and exited1 with JSONDecodeError; corrected only that metadata read, with no scanner/Docker/Cloud action. Decoded32372-byte config SHA256 is44c8657a5aad46d7aa1192e73af0a338200c61720f47b0ebe8d19faa3613f1e2, exactly the recorded Grype imageID. Its safe contract facts are linux/amd64,65532:65532, expected Node entrypoint/Mediator CMD and111 diff IDs. Decoder now supports strict base64 byte fields and literal JSON byte strings; neither representation is reserialized before hashing. New test24 covers actual encoding, including rejection of invalid base64.
This confirms the report config bytes only. The approved child's config descriptor has STILL NOT been obtained/verified; no child->config equivalence or healthy runtime is claimed yet.

Authoritative references inspected narrowly, no repeated broad research:
- OCI manifest config digest and single-platform child: https://github.com/opencontainers/image-spec/blob/main/manifest.md
- Config bytes/diff IDs: https://github.com/opencontainers/image-spec/blob/main/config.md
- Docker maintainers' containerd ID distinction: https://github.com/docker/cli/issues/5526

## Separate H2AO continuation and guards

Default OFF unless BOTH --execute-h2ao-once and --owner-approved-selective-off-only. Never invokes either consumed old cli(), H2AN, H2AM, builds, login, pull/push, gcloud, KMS, Firebase, deployment or hosted endpoints.
Exact frozen H2AM support blob b9b57daa9a5b5f0304afc9cfc758630793454c07 and module blob3adfb06ca66d6175f089ea797df21ca767779cca are checked before importing their safe constants/helpers; no old runner is executed. Tested bounded runtime lifecycle is reused/adapted with H2AO names/labels and canonical identity handling.

Filesystem-only prior gates pin H2AM summary SHA99a455c5bedd435c0f72b0c9aacadcb96d8949db9cb1d2bff518416ca1b18e958f, exact failure MEDIATOR_HISTORIC_LOCAL_CONFIG_MISMATCH at Mediator IMAGE_BINDING, consumed H2AM marker/attempt, COMPLETE imported Mediator scan/bytes/ledger, no old runtime or other-role scan claims, consumed H2AN successful three preloads, old H2AJ/H2AK prerequisites and exact frozen proposal image/SA/UID/project/source pins. Any changed/extra prior stage STOPs.
Owner/project scope is checked from the existing private isolated local SDK configuration only; not live principal/IAM proof, no auth command. Existing root WSL/native ELF ownership/mode checks, >=4GiB local evidence free disk and private cached DB required. No readiness claim based on historical checks alone.
All raw child proof files must hash to their frozen role child. Mediator missing proof STOPs before runtime marker unless the separate one-GET option is explicitly approved. Gateway/Backend/Reader proofs MUST already be supplied from existing saved bytes; there is no approval/code to request three extra remote manifests. Missing any of those STOPs BEFORE network/Docker/preflight/runtime markers, rather than spend a scan to discover the known ambiguity again.
Only after initial proof/history/scope checks: new exclusive H2AO local-readonly-preflight marker precedes bounded docker info, existing cached Grype DB status (valid=true, updates disabled), and four exact local docker image inspect calls. No pull fallback. All four Docker IDs are bound to verified manifest/config descriptors before runtime marker; Mediator full scan/config/rootfs binding additionally verified. Preflight failure has private summary; no new runtime marker.
Only after preflight: NEW exclusive .oldx-step05-h2ao-selective-continuation-once-20261129 marker and NEW per-image ledger. No marker deletion/replay. Old markers/evidence snapshots are checked unchanged before execution.
Import original Mediator scan first, then its OFF runtime only. If PASS, one fresh scan/runtime for Gateway, Backend, Reader sequentially. Each Grype uses docker:<EXACT_IMMUTABLE_ROLE_REF>, not ambiguous bare Docker ID; local provider and empty registry config. Each new scan is verified against its separately hash-verified saved child descriptor and raw config. No dependence on potentially transformed Grype manifestDigest. Capture raw scan+SHA independently BEFORE identity validation; if binding fails retain CAPTURED_IDENTITY_PENDING and attempted ledger, never rescan. Verified scan COMPLETE receipt is durable BEFORE runtime.
Runtime uses immutable role ref, --pull=never, unique oldx-h2ao names, no --rm, networknone, read-only,65532, capdropALL/no-new-privileges, no mounts/host ports,768MiB/equal swap/1CPU/pids128. One explicit Node24 ESM health probe requires200/OFF, Product503, UID65532. Durable primary error/exit code/timeout/bounded sanitized logs before scoped at-most-one stop/rm. Real OOMKilled boolean only, not exit137 inference. Unknown ownership/state, missing/truncated logs or evidence-write failure retains container, cleanup uncertainty separate. Runtime COMPLETE requires exit0/non-OOM/owned cleanup. No default-OFF or launch setting changed.
A preflight STOP now prints HISTORICAL_ONLY_NOT_IMPORTED_NO_RESCAN instead of falsely implying H2AO already imported the scan. Local private evidence directory and summary checksum are printed for owner retention.

## Optional exactly ONE manifest GET — source only, NOT executed

Only Mediator, exact fixed HTTPS registry/repository/sha256 URL; no tags, arbitrary URLs, HEAD, layers, redirects, retries, extra role requests or auth bootstrap.
Separate exclusive .oldx-step05-h2ao-one-mediator-manifest-get-once-20261129 marker, before token/request. Existing valid short-lived Owner OAuth token supplied via anonymous pipe FD>2 only; bounded20s pipe wait, no token argv/env/file/log/receipt, no token refresh/login/new credentials. HTTPS CA validation and no proxy auto-discovery;10s socket timeout,20s read deadline,512KiB cap. Auth token removed from request after operation. Existing isolated owner config and project still mandatory; no claim the opaque token's principal is independently verified locally.
HTTP401/other error, redirect, DNS/TLS/timeout, unexpected encoding/type/header digest or raw SHA/config mismatch STOP with no retry. Private bounded response (if available), HTTP status, raw checksum and safe failure receipt retained; no credential or response-body error logging. Runtime marker stays absent on missing/unbound proof. A consumed GET is never repeated.
Actual network/auth/registry behavior is NOT tested; HTTPS tests are mocks.

## Actual NEW offline tests, exact commands/results

Run in existing OLDX-Ubuntu-24.04 Python3.12 from isolated source. ALL Docker/Grype/HTTPS/process operations in tests are doubles; no containers, scanner, image request/build/pull, registry operation or Cloud call ran. The two existing-report metadata reads above are local filesystem reads only. No old19 H2AM tests, H2AN/H2AJ/H2AK, Step04 or broad CI groups repeated.

Module M=step05_h2ao_identity_continuation_new_test.H2AO; isolated test directory tests/integration.
1. python3 -B -m unittest discover -s <isolated-source>/tests/integration -p step05_h2ao_identity_continuation_new_test.py -v
  19 initial cases:18PASS/1ERROR,2.427s,exit1. Test12 fake rm wrongly failed Mediator cleanup when intended fault role was Gateway. Corrected fixture to fail only target role, no assertion weakened.
2. python3 -B -m unittest M.test_12_completed_new_scan_is_durable_before_failed_runtime_no_replay -v
   1/1PASS,0.684s,exit0.
3. python3 -B -m unittest M.test_18_single_authenticated_manifest_get_mocked_and_marker_never_reset M.test_19_http_401_stops_one_request_no_saved_token_or_retry M.test_20_consumed_h2ao_marker_stops_before_any_command M.test_21_missing_other_saved_manifest_blocks_before_any_marker_or_scan M.test_22_wrong_historical_config_blocks_before_runtime_or_docker_preflight M.test_23_get_hash_mismatch_keeps_private_raw_and_failure_receipt_no_retry -v
   4PASS/2FAIL,0.460s,exit1. New21/22 synthetic ELF fixture had literal backslash-x bytes, so the native-tool gate correctly stopped earlier. Corrected fixture to byte127+ELF.
4. python3 -B -m unittest M.test_21_missing_other_saved_manifest_blocks_before_any_marker_or_scan M.test_22_wrong_historical_config_blocks_before_runtime_or_docker_preflight -v
   2/2PASS,0.067s,exit0.
5. python3 -B -m unittest M.test_01_containerd_manifest_id_and_grype_config_id_bound_without_conflation M.test_02_legacy_config_id_uses_same_cryptographic_chain M.test_10_mediator_import_then_only_three_exact_ref_scans_and_four_runtime M.test_12_completed_new_scan_is_durable_before_failed_runtime_no_replay M.test_24_actual_grype_base64_config_bytes_match_manifest_descriptor -v
   After actual base64 decoding fix, only one new and four affected NEW cases:5/5PASS,2.061s,exit0.
6. python3 -B -m unittest M.test_14_container_inspect_image_may_be_verified_config_or_child_only M.test_25_malformed_source_and_truncated_inspect_are_explicit_stops -v
   2/2PASS,0.020s,exit0.
7. python3 -B -m unittest M.test_26_unbound_local_engine_id_stops_in_readonly_preflight_before_runtime_marker -v
   1/1PASS,0.194s,exit0. After correcting preflight import-status output, only this affected new case repeated:1/1PASS,0.182s,exit0. Printed STOP/summary/evidence were test-double output in a temporary fixture, NOT actual Docker/preflight execution.

Total26 DISTINCT NEW cases have passing evidence via affected-only selections; not a claimed final one-shot26-case full-suite run. No unresolved test failure. Production source blob IDs exactly matched locally tested files:
- identity b7f7eb42ba4a72fb6959ca06e52cff55b3b30ae5; SHA25645959ae1447b760204967bf88bb4c6daa646a4845affa99726ba1c3093c70a0b.
- runner5db17708caad89f0c49502eb343c71f3120b1260; SHA25686492f87283e2a474b66c02557b39f07d5eb2d79220489cda33b3517ed154f2e.
- tests2c74f45e8273373d2554ebdb88364ea57b198ffc; SHA25674a71953bede6309c8a322ddbe2cad89caef6a1edeb04874de0f722419fdbd8b.
M is an explicit abbreviation of the module/class above; prepend that exact module/class to listed method names. WSL commands used -B and --cd to isolated tests; no software installed.

## Remaining precise blockers / ONE consolidated future approval

NOT established: exact Mediator pinned raw child config descriptor; availability of saved Gateway/Backend/Reader raw child bytes; current local images/RootFS/owner-config permissions/native tools/valid cached DB; actual container health/exit/OOM, other three vulnerability findings and all hosted acceptance.
The safe parser's actual report config format/hash is verified; the proposed child->config match is STILL UNKNOWN. Distinct old Grype manifest cannot solve it. No CVEs fixed/accepted, no G2 PASS, no Step05 DONE.

ONE owner decision packet, NOT authorized by this source-only task:
Approve a single bounded local H2AO attempt on this source, preserving every consumed marker:
(a) locate/read only existing saved raw child proof files in an explicitly selected private directory, named mediator-child-manifest.json, gateway-child-manifest.json, backend-child-manifest.json, reader-child-manifest.json; verify each raw SHA against frozen child. No Docker export/pulls/rebuild or cloud discovery. If three non-Mediator proofs are absent, STOP without GET/scan/runtime. ONE Mediator GET cannot create missing evidence for other roles; any need for additional requests must be reported for a later separate scope, not silently expanded.
(b) only if Mediator bytes missing and other three proofs present, at most ONE fixed Mediator HTTPS manifest GET with an already-valid Owner token on anonymous FD; no auth refresh/login/credential creation. Missing usable token STOP. If saved Mediator proof present, no GET option.
(c) after all proof/history/owner/project/native/disk gates, one bounded read-only Docker/DB preflight, then ONE new H2AO selective runtime/scans: Mediator OFF runtime WITHOUT rescan first; only after its PASS, ONE Grype scan and OFF runtime each Gateway/Backend/Reader. Stop on first error/unknown; no automatic retry, no old/new consumed marker reset.
(d) scoped own-container cleanup/private evidence retention only. No builds/pulls/pushes, registry writes, Cloud Run/IAM/KMS/Firebase/Billing, real user data/hosted calls, production activation or CVE risk acceptance.

Future command ONLY after that approval, with verified isolated source containing the two frozen H2AM helper modules and unchanged proposal:
```sh
python3 -B scripts/step05_h2ao_selective_continuation_once_20261129.py --execute-h2ao-once --owner-approved-selective-off-only --manifest-directory <existing-private-proof-directory>
```
If and ONLY if Mediator proof missing, other three proofs present and one GET specifically approved: append --allow-one-mediator-manifest-get --oauth-token-fd <already-open-anonymous-pipe-fd>. Do not put tokens in arguments, environment, files or public output. No gcloud command/token acquisition is implemented or authorized by this packet automatically.
Limits: optional GET <=512KiB; four sequential runtime containers maximum768MiB/1CPU each; three scan commands maximum1000s each; no DB/app update; local evidence free disk>=4GiB (not a guarantee of resource sufficiency). No cloud spend incurred by this task; a future authenticated registry GET may have normal provider transfer charges, not guaranteed free. No paid tooling/service introduced.
