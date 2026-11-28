# BAJUTO Step05 H2AM — actual source repair and focused offline evidence

Date: 2026-11-28 IST. Branch: security-hardening-review only.
Starting remote HEAD: 9aa6aa7200d4f7e6f7d7d3c3fccd8f98f45e186d.
Verified source commit: 040bdec66abdfcb266ca8c4db82aeb82761bd2ae. Documentation commit is its child.
Status: SOURCE_IMPLEMENTED_OFFLINE_VERIFIED; FUTURE_EXECUTION_NOT_AUTHORIZED_OR_RUN.
Step05 ACTIVE; G2/G4/G8 and hosted acceptance HOLD; production OFF / NO-GO.

## Scope and preservation

Read AGENTS.md, current Handoff, H2AM consolidated task, H2AL actual receipt, H2AJ receipt, Issue #17, consumed H2AK runner, frozen four-role source, Dockerfiles and package/closure manifests. This repairs the acceptance harness only. No application, Dockerfile, lockfile, image digest, service-account pin or consumed runner was changed.
Owner checkout was behind 358 with modified Handoff and untracked .firebaserc. It was left intact. New source was tested in a separate temporary directory and saved through GitHub tree/commit APIs with a fast-forward expected-HEAD lease, review branch only, [skip ci]. No reset, force push or main change.

Added:
- scripts/step05_h2am_acceptance_support.py — bounded subprocess evidence, private durable receipts, sanitization, scan schema/identity validation.
- scripts/step05_h2am_selective_acceptance_once_20261128.py — separate default-OFF one-shot, per-image scan/runtime receipts and explicit unattempted-only resume.
- tests/integration/step05_h2am_selective_acceptance_new_test.py — 19 distinct NEW mocked offline cases.
Updated this receipt, existing H2AM plan, AGENTS.md and current Handoff. Issue #17 records final remote SHA.

## Historical evidence preserved, not rescanned

Mediator: COMPLETE historical Grype evidence = 57 package findings, Critical 0, High 18, Medium 20, Low 6, Negligible 11, Unknown 2. These are match counts, not a claim of 57 unique CVEs.
Only bounded local metadata/schema reads of the existing private JSON were made; no Grype process was run.
Existing raw report SHA256: e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92.
Actual source.type=image; imageID=sha256:44c8657a5aad46d7aa1192e73af0a338200c61720f47b0ebe8d19faa3613f1e2.
Actual userInput identifies the exact frozen Mediator child 01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe.
The report's manifestDigest is different (31285b477845b9e10f76c4b7df425d200fa15db0e615b0cb4b639e4c3fc7aae4); the parser therefore requires explicit original child reference OR exact matching manifest, and separately binds the local config image ID. It never conflates manifest/config/index identities.
Grype version 0.122.1; actual DB metadata is nested at descriptor.db.status (built, from, path, schemaVersion, valid); providers count27. Parser allowlists identity/time/version/valid fields, never copies configuration, DB path or source; missing fields remain UNKNOWN. New test19 covers this exact structural variant.
No private raw report, credentials or config were uploaded. Future imported raw evidence stays private; public documentation contains checksums and bounded identity only.

## Static findings before future execution

Frozen build source f567aa6ccef7a71b6032dc1bdb9f2bcf0a8587d4 was reviewed. All four current Dockerfiles, package manifests and closure manifests match its Git blobs. Four closures contain84 files each (87 distinct across roles); lexical static import audit found229 relative references per role, zero missing relative paths and zero missing Docker COPY entries. Unchanged older local files were reused only after frozen Git-blob match; missing/new files were read by frozen Git blob. This is source inspection, not actual image filesystem verification or a Node import execution test.
All five bare imports are dynamic in firebase-native.mjs: firebase-admin/app, firebase-admin/auth, @google-cloud/firestore, @google-cloud/storage, google-auth-library. OFF bootstrap returns before runtime bindings/SDK loader, metadata or config reads. Mediator's enabled loader uses only Firebase app/auth; its manifest pins firebase-admin14.5.1. Backend additionally pins Firestore9.4.1, Storage8.4.0 and google-auth-library9.15.1. Gateway/Reader have no installed external dependencies and must never enter Firebase loader; role guard enforces that source path.
Static imports still resolve in OFF mode, so file presence matters even when a live binding is disabled. Source closure findings do not prove installed SDK/native contents or the four built images healthy.
Node24 explicit /nodejs/bin/node entrypoint, /app working directory, 65532:65532 ownership/user, read-only source copies and SIGTERM are in frozen Dockerfiles. OFF server source binds 0.0.0.0:8080, GET /healthz returns200 stateOFF/productReadyfalse, other routes return503 before request-body/real-host handling. No OFF write requirement was found.
Docker network none retains IPv4 loopback; use127.0.0.1 inside the container, no published host ports. Official reference: https://docs.docker.com/engine/network/drivers/none/.
SIGTERM source closes listener/connections and runtime; actual container shutdown remains unverified.
Old main exit1 and exec137 are CONFIRMED historical events. OOM, missing import, resource pressure, ESM probe parse failure and startup timing are NOT proven root causes. Old --rm removed recoverable container logs. A second Node process under512MiB/0.5CPU could contend, but this is only a hypothesis. New bounds are768MiB with equal swap limit,1CPU,pids128 and one minimal explicit-ESM exec; not an assertion that these limits guarantee success.

## Implemented controls

No import-time external IO. Without BOTH --execute-h2am-once and --owner-approved-selective-off-only, CLI returns OFF before old evidence or commands. A NEW exclusive marker is written and fsynced before any Docker/Grype/optional registry pull. Old H2AJ/H2AK markers and consumed runner are untouched.
Filesystem-only prerequisites require exact frozen proposal Git blob, build-source revision, four child/SA/UID pins, successful H2AJ marker, consumed Mediator-only partial H2AK marker, original private report's pinned raw SHA256 and exact57 severity counts, no newly appearing old three-role scans, native existing Linux ELF tools, existing private Grype DB and >=4GiB local free evidence disk. Current tools/engine/DB/disk readiness was NOT executed or certified.
Historical Mediator raw bytes and receipt are durable BEFORE Docker info or any runtime. Mediator is forbidden in scan(). Mediator runtime is first; failure stops before all three new scans.
Gateway/Backend/Reader scan at most once each from local Docker config image ID, only after RepoDigests binds exact frozen child and linux/amd64/user/entrypoint/config checks. Successful JSON+SHA+image ID+severity/advisory-ID counts+available DB metadata is persisted before runtime. Scan completion is not CVE acceptance.
Per-child permanent scan/runtime ledgers are claimed before side effects. Successful scan survives unrelated runtime failure. Completed roles and scans are reused. Failed/ATTEMPTED/ambiguous stages cannot be replayed. Offline --inspect-resume outputs summary SHA and unattempted-only plan; a separate explicit resume approval, matching SHA and fresh exclusive derived marker are mandatory. No marker deletion or generic retry flag.
Containers are unique named, no --rm, --pull=never, no mounts/host ports, networknone, read-only, capdropALL, no-new-privileges, nonroot65532, flagfalse. One Node24 explicit --input-type=module probe does bounded IPv4 startup wait, <=2048-byte health body, health200/OFF and Product POST503. No production/user/KMS/Firebase requests.
First failure, exact CLI exit status/timeout and bounded sanitized stdout/stderr are durable before diagnostics/cleanup. Inspect saves only allowlisted state/ownership/image fields, never full Env. Logs use tail100 and64KiB capture. Main-exit-before-exec is tested. OOM requires actual boolean State.OOMKilled;137 alone stays UNKNOWN.
Unknown ownership/state, missing/truncated logs or inability to durably preserve failure retains the container; separate cleanup uncertainty never overwrites first failure. Known owned running container gets at most one bounded SIGTERM stop, then inspection; known exited container gets at most one non-force rm. No blind retries/kill/prune. Runtime COMPLETE requires exact OFF probe, exit0, OOMKilledfalse and verified own-container cleanup. Failed complete diagnostics can be removed only after durable evidence; uninspected evidence is retained.
Command output is drained boundedly; Grype raw JSON streams into a private file capped64MiB; timeout and unknown child-exit states preserve partial evidence. Reports0600/directories0700, fsync+atomic receipts, secret/credential/JWT/config redaction. Existing private local DB only; auto-update and app-update checks disabled. No credentials passed into containers.
Optional --allow-missing-exact-pulls additionally requires an existing private root-owned0600 Docker config for only the exact registry, no credential helpers/store. At most one exact immutable linux/amd64 pull per missing role. No login, refresh, helper, credential creation, DB download, build, push, cloud API or deployment is implemented. Without this separate approved option missing local image STOPs.

## Actual NEW offline test results

Executed in owner's existing OLDX-Ubuntu-24.04 Python3.12, using isolated temporary source. Every external process/Docker/Grype call in tests is mocked. No previous OLDX suites or 23 older H2AH cases repeated.

Common directory: tests/integration in isolated verified source.
1. python3 -B -m unittest discover -s <isolated-source>/tests/integration -p step05_h2am_selective_acceptance_new_test.py -v
   Initial16 NEW cases:16/16PASS,7.742s,exit0.
2. Same discover command with -k test_17_:1/1PASS,0.824s,exit0 (missing/truncated diagnostics retained).
3. Same with -k test_18_:1/1PASS,0.098s,exit0 (historical receipt durable before commands).
4. python3 -B -m unittest step05_h2am_selective_acceptance_new_test.H2AM.test_02_historic_counts_are_exact_imported_and_mediator_never_scanned step05_h2am_selective_acceptance_new_test.H2AM.test_03_scan_metadata_is_durable_before_runtime_and_kept_on_failure step05_h2am_selective_acceptance_new_test.H2AM.test_04_startup_exit_one_no_exec_logs_kept_before_cleanup step05_h2am_selective_acceptance_new_test.H2AM.test_08_one_explicit_esm_probe_network_none_no_rm_or_ports step05_h2am_selective_acceptance_new_test.H2AM.test_09_resume_only_unattempted_stages_never_rechecks_completed_roles_or_scans step05_h2am_selective_acceptance_new_test.H2AM.test_16_primary_receipt_failure_retains_container_instead_of_destroying_evidence -v
   Only six affected NEW cases after diagnostic hardening:6/6PASS,5.764s,exit0.
5. python3 -B -m unittest step05_h2am_selective_acceptance_new_test.H2AM.test_19_actual_grype_nested_db_schema_and_explicit_child_binding -v
   First invocation failed during collection with IndentationError because new method was appended after module main guard; corrected placement without weakening assertions. Then1/1PASS,0.004s,exit0.
6. python3 -B -m unittest step05_h2am_selective_acceptance_new_test.H2AM.test_14_bounded_command_timeout_preserves_exact_code_and_partial_stderr_without_real_process -v
   Only affected NEW timeout case after final bounded drain/child-exit correction:1/1PASS,0.050s,exit0.

7. python3 -B -m unittest step05_h2am_selective_acceptance_new_test.H2AM.test_11_old_markers_untouched_and_historical_evidence_validated -v
   Only affected NEW original-report checksum pin case after final evidence hardening:1/1PASS,0.023s,exit0. Includes refusal of changed raw bytes and independent severity-count mismatch assertion.

Total19 DISTINCT NEW cases have passing evidence; not a claim of one19-case full-suite final invocation. No unresolved test failures. Windows Python alias unavailable; used existing WSL Python with sandbox permission for mocked tests only. No software installed.
Final tested Git blobs match uploaded source exactly:
support b9b57daa9a5b5f0304afc9cfc758630793454c07; runner3adfb06ca66d6175f089ea797df21ca767779cca; testsca86cc2d0451ee8b023d9703fd98f6d045d90993.
SHA256: support a8f5b40d0a51da21581af9484ea0eb052dae9d627451cbdc560bb725b9aa0f17; runner bab2779d8610c6d9cfe7e7afdc503a18604bdaf640214b25eb4313f311ebb6c5; tests84cfc1fc6a2c6af07ca08af9edad194952321ca916fbe448e25457ab5cad3e58.

## ONE next owner authorization packet — NOT executed

Approve ONE future local H2AM selective OFF-only attempt on this reviewed source:
1. Import existing Mediator57 report and verify ONLY its OFF runtime, no Mediator Grype.
2. Only if preceding role succeeds, ONE Grype+OFF-runtime for each Gateway, Backend and Reader.
3. Use only four frozen H2AJ child refs from unchanged proposal. Allow at most one exact missing-image pull per role ONLY with existing private authenticated config and explicit pull option. No auth bootstrap/refresh or new credentials.
4. Existing local Grype DB only; no DB/app update. Max4 named isolated containers sequentially,1CPU/768MiB/pids128 each; scan timeout1000s each, optional pull600s each; runtime/start/cleanup commands bounded. At least4GiB local evidence space required; disk threshold is not a guarantee for all missing image sizes. STOP on insufficient storage, missing auth/DB, digest/source drift, scan/probe failure, unknown evidence/OOM/cleanup. No automatic retries; retain partial evidence and consumed markers.
5. Exact own-container stop/rm as above only; no unrelated images/files/markers removed. Keep private raw reports and sanitized diagnostics locally; publish only concise receipts/checksums.
6. No builds/pushes, Cloud Run/IAM/KMS/Firebase/Billing changes, hosted traffic, production activation or CVE acceptance. No cloud storage. Optional registry reads may have provider egress/usage implications; no zero-cost guarantee for future pulls. No new cloud spend in this source-only task.

Future command (requires that NEW owner approval and existing private paths; do not run now):
```sh
python3 scripts/step05_h2am_selective_acceptance_once_20261128.py --execute-h2am-once --owner-approved-selective-off-only --allow-missing-exact-pulls --private-docker-config <existing-private-registry-config-directory> --grype-db-cache <existing-private-grype-db-directory>
```
If all images already local, omit both pull/config options. A runtime/source defect found in existing immutable images requires a separate justified repair/new-build decision, not silent rebuild or digest substitution.

## Remaining unknowns / gates

Mediator OFF health, actual Node24 container runtime, root cause of old exit1/137 and actual OOM status remain UNKNOWN. Three other image scan findings and all four new isolated-runtime results remain NOT RUN. Actual installed/native SDK contents, private DB usability/freshness, local image availability and private registry auth remain unverified in this source-only pass. Image references preserve history; source harness tests do not repair image CVEs.
Hosted IAM/principal proof, role attachment, real Firebase/KMS boundaries, enabled acceptance and rollback gates remain separate HOLD. Do not repeat H2AG grants/H2AF, old H2AJ builds/H2AK scans/H2AL probes. Step05 is not DONE and production remains NO-GO.
