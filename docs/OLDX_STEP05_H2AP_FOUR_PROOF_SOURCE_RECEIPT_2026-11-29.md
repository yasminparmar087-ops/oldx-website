# BAJUTO Step05 H2AP — actual source-only four-proof acquisition and H2AO handoff

Date: 2026-11-29 IST. Branch ONLY security-hardening-review.
Starting remote HEAD: a89f3589476d32fc573366307af60577eae38ca9.
Verified source commit: 1b643487824739290839124269195c32fa7c850d; documentation commit follows.
Status: SOURCE_IMPLEMENTED_OFFLINE_VERIFIED / NO ACTUAL GET, SDK AUTH, DOCKER OR SCAN.
Step05 ACTIVE; G2/G4/G8/security/hosted gates HOLD; production OFF / NO-GO.

## Preservation and exact files

Read current AGENTS, Handoff, H2AP owner inventory/task, H2AO identity/runner/receipt, frozen proposal, prior H2AK/H2AM/H2AN evidence and latest Issue #17 checkpoints. The owner inventory found no exact manifest bytes among188 eligible files in its bounded evidence scope. This is NOT registry-image absence, nor whole-filesystem absence. No inventory was repeated.
Added:
- scripts/step05_h2ap_four_manifest_proofs_then_h2ao_once_20261129.py — default-OFF one-shot proof workflow and separate approved unchanged H2AO handoff.
- scripts/step05_h2ap_cached_owner_token.py — bounded native-SDK memory-only credential IPC with no refresh, network, disk cache mutation or token logging.
- tests/integration/step05_h2ap_four_proof_handoff_new_test.py —21 distinct NEW offline cases.
Updated this actual receipt, existing H2AP task checkpoint, AGENTS.md and living Handoff; Issue #17 records final verified HEAD.
No H2AO/H2AM/H2AN/H2AJ/H2AK source/tests/markers/evidence, app/features, Dockerfiles/locks, immutable image/SA pins, Firebase/Cloud settings or main changed. Local owner Handoff modification and untracked .firebaserc preserved; repository remains behind358 locally. Isolated temporary source was tested; intended7 files saved through GitHub expected-HEAD fast-forward APIs, [skip ci], no reset/force push.

## Implemented workflow

Default OFF unless BOTH --owner-approved-four-manifest-gets-once and --owner-approved-h2ao-selective-once. No dependency/source downloads, SDK process or HTTP before those flags. Separate fresh owner approval is required, not inherited from consumed H2AN/H2AM.
Root existing WSL only; fresh H2AP marker and H2AO runtime/preflight/GET/global-ledger absence. Before GETs: exact frozen source/proposal verification, existing local owner/project config, old H2AJ success, H2AK original pinned scan, consumed H2AN three preload/four-local evidence, exact consumed H2AM IMAGE_BINDING summary and no new runtime/other scans (unchanged H2AO history verifier), native tool owner/ELF metadata, existing private DB and>=4GiB local evidence free disk. Four current local image inspections/valid DB query occur ONCE in H2AO after proof completion, not duplicated by H2AP.
Root-owned0700 evidence/proof dirs,0600 exclusive files, file+parent fsync and atomic receipts. Marker:
.oldx-step05-h2ap-four-child-manifests-and-h2ao-once-20261129
is exclusive/durable BEFORE first registry request. It is never removed/reset. Each role has durable ATTEMPTED then COMPLETE or FAILED, safe ref/HTTP status/raw SHA/config digest/file fields; ambiguity never permits replay. Failed/current raw response retained when fully received; successful prior proofs always retained. No extra request after first failure, receipt-write failure or unknown state.

Authenticated endpoints are a closed four-role map; fixed host asia-south1-docker.pkg.dev, project oldx-staging, repository oldx-staging-images, and exact immutable child digests:
Mediator01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe;
Gateway921fbf4ff71b918c479e4a786868368640a494c16da08e54192f25e14dc1ec4d;
Backend01ae540aa88ad0e3a6888994dd41b6b02b9d934a7a1d2e455f44b194f033b941;
Reader822e2592b1010bfa94a1fe5bc75003712485abae0369f5252ece3863723eb077.
At most ONE authenticated GET per role, exact /v2/oldx-staging/oldx-staging-images/<role-artifact>/manifests/sha256:<child>. No mutable tag, HEAD, pull/layer/export/build/push or arbitrary URL option. TLS CA validation, no proxies/redirects/retries;10s socket timeout,20s cumulative body read deadline (a blocked read may take up to remaining socket timeout beyond deadline),512KiB maximum per manifest. HTTP200, identity encoding, accepted exact OCI/Docker schema-2 child media type, optional digest header absent or exact match. Tokens removed from Request headers in finally.
Hash unaltered bytes, never JSON reserialization. Reuse original H2AO manifest_config(raw,exact_ref): config descriptor/layers valid, no index/artifact/foreign-layer URL. Private file persisted/fsynced before COMPLETE. Wrong media/header/hash/schema/config STOP, retain partial receipts, no handoff.
Mediator additionally binds original report SHA e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92, exact ref, base64-decoded config SHA44c8657a5aad46d7aa1192e73af0a338200c61720f47b0ebe8d19faa3613f1e2 and32372-byte length to manifest config.digest/size, role/nonroot/platform/entrypoint and original57-match severity contract. NO Mediator scanner invocation. The old converted31285... manifest is not substituted.
After ALL four COMPLETE: independently reread/rehash each proof, repeat manifest/config checks and five frozen source Git-blob checks, check protected old-evidence snapshots and H2AO marker freshness again.

## Credential custody — source preparation, no actual credential access

A normal SDK refresh can automatically cache refreshed tokens. Narrow passive reads of the already-installed native SDK source (not its interpreter/gcloud) confirmed Load(prevent_refresh=True,allow_account_impersonation=False) and automatic caching on refresh. Official CLI reference: https://docs.cloud.google.com/sdk/gcloud/reference/auth/print-access-token . No SDK version/auth command, actual credential-store read or token retrieval ran now.
New helper runs only later in the pinned existing native SDK bundled Python, -I -B, isolated allowlisted environment. Parent verifies helper Git blob and native root-owned ELF. Explicit existing Owner user account, local oldx-staging config verified by frozen H2AO owner_scope. No ADC, impersonation, environment/file-token override, new credentials or SDK installation.
SDK's existing credentials.db/access_tokens.db connections are forced mode=ro&immutable=1; Python audit hook denies file writes/mutations, sockets/DNS and subprocesses. No native SDK credential refresh/network fallback. Credential must be a Google USER credential with an existing valid token and expiry180..3700 seconds ahead. It goes only through captured anonymous process IPC; helper refuses terminal/file stdout, no token argv/env/file/Docker config/log/receipt. Parent captures safe allowlisted error codes only; unexpected SDK error text/output is never published or retained. Token variable released before H2AO child starts; no guarantee of cryptographic RAM erasure.
IMPORTANT availability limit: an absent/expired/too-short cached token, read-only-cache/WAL compatibility problem, missing library or blocked SDK write causes STOP BEFORE H2AP marker and all registry requests. This workflow deliberately does NOT refresh credentials to make progress. Actual cached-token/native-SDK readiness is UNKNOWN; no promise the future command will pass. A fresh login/refresh would require separate explicit scope, not an automatic retry or silent cache mutation. Immutable SQLite reads may miss uncheckpointed newer token data; safe failure is intentional.
Credential expiry and safe diagnostics tested with doubles. Native SDK runtime compatibility has NOT been exercised.

## Frozen H2AO reuse, exact separate handoff

Five exact files from immutable source92a4529d3fe4de641898f9195634dfd2e9b8144e:
runner5db17708caad89f0c49502eb343c71f3120b1260;
identity b7f7eb42ba4a72fb6959ca06e52cff55b3b30ae5;
H2AM support b9b57daa9a5b5f0304afc9cfc758630793454c07;
H2AM module3adfb06ca66d6175f089ea797df21ca767779cca;
proposal c1cfcfa2f224e9a47dd6e896730c73e927b9b483.
Reuse local bytes if exact; otherwise at most one fixed public GitHub source GET per file, no redirect/retry/auth,<=100KiB each, in a fresh isolated tree. Any existing local drift STOPs instead of being overwritten. These source downloads precede credential access and H2AP marker, under the NEW combined approval only. No old runner executed.
Separate handoff approval flag mandatory; H2AP records ATTEMPTED durably before exactly one child invocation:
python3 -B <verified-source>/scripts/step05_h2ao_selective_continuation_once_20261129.py --manifest-directory <verified-private-proofs> --execute-h2ao-once --owner-approved-selective-off-only
NO optional Mediator GET flag or token FD is passed. H2AO source remains unchanged and owns its own strict preflight/runtime marker gates.
Only Mediator OFF runtime first, NEVER its old57-finding scan. Then, only after its PASS, one new scan/OFF-runtime each Gateway/Backend/Reader; existing H2AO controls require exact canonical identity/nonroot/read-only/networknone/health200/Product503/OOM/log/SIGTERM/cleanup evidence. Stop/no retry at any unknown/failure.
Child runs in tokenless minimal environment;4200s total child limit,64KiB output guard. Only own CLI may be killed on limit, never unrelated/unknown Docker resources. Exact exit code and private output hash retained before result validation. Exit0 alone insufficient: verify child private summary path/hash, scope, all four scan/runtime completion records and expected OFF-evidence outcome. COMPLETE still SECURITY HOLD, not CVE acceptance/G2 PASS/Step05 DONE. Partial child state stays unknown and consumed; no automatic cleanup or replay by H2AP.

## Actual NEW focused offline verification

ALL external HTTP/SDK/H2AO/Docker/Grype actions in tests are doubles. No actual registry request, SDK interpreter/auth command, Docker, scanner, build/pull, Cloud change or production action occurred. Only local native SDK SOURCE inspection and isolated filesystem/Node-independent Python tests. No old26 H2AO/19 H2AM or completed CI/scans/tests repeated.
Common module M=step05_h2ap_four_proof_handoff_new_test.H2AP; isolated tests/integration under new temporary source.
1. python3 -B -m unittest discover -s <isolated-source>/tests/integration -p step05_h2ap_four_proof_handoff_new_test.py -v
   Initial20 NEW cases:19PASS/1ERROR,11.004s,exit1. Case17 mock named its first argument uri, colliding with sqlite3's uri=True keyword; production sqlite3 parameter is database. Corrected fixture parameter without weakening checks.
2. python3 -B -m unittest M.test_17_sdk_sandbox_forces_readonly_sqlite_and_denies_network_or_writes -v
   1/1PASS,0.047s,exit0.
3. python3 -B -m unittest M.test_15_token_loader_captures_only_memory_and_never_puts_token_in_env_or_argv M.test_21_token_failure_reports_only_allowlisted_code_never_captured_secret -v
   Only affected/new token diagnostic cases:2/2PASS,0.133s,exit0.
4. bash -n <isolated-source>/future-approved-command.sh
   Syntax-only exit0. No commands inside the future script ran.
Total21 DISTINCT NEW test methods have passing evidence via initial/affected selections, including per-role failure subcases. Not a claimed final one-shot21-case suite. No unresolved failures. M abbreviates the exact module/class above; WSL invocations used -B and isolated paths. No software installed.
Coverage: defaultOFF/dual approval, fixed4 URLs/one GET each, every role partial failure/no retry,401/DNS/TLS/timeout/redirect/encoding/oversize/media/header/hash/invalid/index/config/scan SHA rejection, private modes/fsync retention, consumed markers, source/proof tampering, all4 rehash before exactly-one separate H2AO call, child STOP/no second call, token expiry/user-only/IPC/no leakage/read-only cache audit, token-before-marker ordering and receipt-write failure.

Verified local tested-file Git blobs equal uploaded content:
helper5922b9ca1b33d2a70bdc66cdf2c45ff3e9f2c163 / SHA256cfa6e3849be35949c2059d221ecd728eff0bae8484454ab6124b6a08cbf3b1a9;
wrapper cfbb37d59603dd6cab1abe44a266380f4df00aa6 / SHA25659b50c7f97a2653d43270441e1c247f61c8858875d2f1e09b9d3ed236829a78b;
tests20c1207bdfb6ed2f687554d81153fd199e4d8f2f / SHA256b8b92f0707a78beade11a8d0055a83da8418713c26a0f8ae82140c91e25ee946.

## ONE consolidated future owner approval — NOT granted or executed now

Approve ONE local H2AP attempt on source1b643487824739290839124269195c32fa7c850d:
- Two hash-verified bootstrap GitHub source downloads plus five exact frozen GitHub files if absent; no mutable branch download/execution.
- Existing native SDK read-only cached Owner-token retrieval to private IPC; NO refresh/login/new credential/config change. Missing valid cached token STOP before registry attempt marker.
- At most FOUR authenticated immutable Artifact Registry child-manifest GETs, exactly one per role; no retry/redirect/HEAD/layers/pulls/build/push. Max2MiB total manifest bodies. Stop on first error; preserve partial private evidence and all old/new markers.
- Only after all four proofs, original Mediator config binding and independent source/proof verification, ONE unchanged H2AO selective local OFF acceptance: Mediator runtime ONLY then one scan/runtime per remaining role conditional on earlier success. Existing cached Grype DB, no updates. At most4 sequential isolated768MiB/1CPU containers,3 scans<=1000s each; source/GET/child bounds above.
- Exact H2AO-owned container cleanup/private evidence retention only. NO Cloud Run/IAM/KMS/Firebase/Billing/production changes, real users, cloud storage, CVE acceptance or old attempt replay.

Current blockers remain actual four child proof bytes/config bindings, actual cached-token/native SDK availability, current local Docker images/DB/tools and all actual runtime/other-three security evidence. The known FOUR missing-proof prerequisite now has implemented source acquisition; it is no longer solved by hoping three cached files exist. Source/offline PASS does not establish actual proof availability or runtime PASS.
No cloud spend incurred here. Future registry GET transfer may incur ordinary provider charges; local scans/runtime use existing machine resources, no new paid service/provisioning. No paid operation is automatically authorized.

## ONE WSL-root command — ONLY after the above new approval

Paste this ONE command in the existing OLDX-Ubuntu-24.04 ROOT terminal. It was syntax-checked only, not executed. Consumed/fresh markers are checked before bootstrap; script and helper are hash-verified before Python runs. No flag is pre-authorized by this document.

```bash
bash -lc 'set -euo pipefail
umask 077
test "$(id -u)" = "0"
for f in /root/.oldx-step05-h2ap-four-child-manifests-and-h2ao-once-20261129 /root/.oldx-step05-h2ao-selective-continuation-once-20261129 /root/.oldx-step05-h2ao-local-readonly-preflight-once-20261129 /root/.oldx-step05-h2ao-one-mediator-manifest-get-once-20261129 /root/.oldx-step05-h2ao-image-evidence-20261129; do
  test ! -e "$f"
  test ! -L "$f"
done
d=$(mktemp -d /root/oldx-h2ap-approved.XXXXXXXX)
mkdir -m 700 "$d/scripts"
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto "=https" --output "$d/scripts/step05_h2ap_four_manifest_proofs_then_h2ao_once_20261129.py" "https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/1b643487824739290839124269195c32fa7c850d/scripts/step05_h2ap_four_manifest_proofs_then_h2ao_once_20261129.py"
test "$(git hash-object "$d/scripts/step05_h2ap_four_manifest_proofs_then_h2ao_once_20261129.py")" = "cfbb37d59603dd6cab1abe44a266380f4df00aa6"
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto "=https" --output "$d/scripts/step05_h2ap_cached_owner_token.py" "https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/1b643487824739290839124269195c32fa7c850d/scripts/step05_h2ap_cached_owner_token.py"
test "$(git hash-object "$d/scripts/step05_h2ap_cached_owner_token.py")" = "5922b9ca1b33d2a70bdc66cdf2c45ff3e9f2c163"
python3 -I -B "$d/scripts/step05_h2ap_four_manifest_proofs_then_h2ao_once_20261129.py" --owner-approved-four-manifest-gets-once --owner-approved-h2ao-selective-once'
```

If any failure/marker consumption occurs: do NOT rerun or delete markers. Use the printed private evidence path and summary SHA to inspect that attempt. A token/preflight STOP before marker is still a real blocker, not permission to login/refresh or repeat diagnostics. Preserve15-step sequence, all image/rollback history and HOLD / NO-GO.
