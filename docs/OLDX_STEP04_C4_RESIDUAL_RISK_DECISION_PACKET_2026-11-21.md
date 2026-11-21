# OLDX Step 04 — C4 source-only residual-risk decision packet

## 21 Nov 2026 ~17:07 IST — G4 existing in-memory service IAM/default-OFF settings review COMPLETE (LATEST)

**Actual owner screenshot** of a new **PowerShell-only in-memory** inspection of *already fetched* `$svc` and `$servicePolicy` from 17:03 cloud read; **NO additional GCP API calls, no mutation**:
```text
G4_INVOKER_IAM_CHECK=NOT_EXPLICITLY_DISABLED
SERVICE_MIN_SCALE=NOT_SET
REVISION_MIN_SCALE=NOT_SET
OLDX_PRODUCT_READ_ACTIVATE_STAGING=EXACT_FALSE
OLDX_PRODUCT_READ_STAGING_ADC=EXACT_FALSE
SERVICE_NAMED_INVOKER_MEMBERS=1
G4_CONFIGURATION_IN_MEMORY_REVIEW=COMPLETE
C5_DEPLOYMENT=NOT_STARTED
```
**Precise interpretation:** On the **latest service-template** snapshot, `run.googleapis.com/invoker-iam-disabled` was **not set**; this is consistent with Cloud Run default IAM-check-on but the snippet alone is not a complete effective/public access review. Service IAM policy from prior snapshot had **zero public members**, and now **one named `roles/run.invoker` binding member** (ID deliberately not printed). Previous project basic roles Owner=2/Editor=1 imply **potential extra authenticated invokers**; parent grants remain unreviewed. `INGRESS=all` means Internet network ingress possible, but not authentication bypass by itself. Google Cloud Run official docs https://docs.cloud.google.com/run/docs/securing/managing-access : public access can also come from an explicitly disabled Invoker IAM check. Avoid calling single named member “exclusive Yasmin access”. Both exact feature env flags are **explicitly false** in latest service template, not proof for every older 100%-traffic/tagged revision; do not infer uninspected other flags. `minScale` annotations `NOT_SET` means not explicitly provisioned at these levels; Google default is typically zero (https://docs.cloud.google.com/run/docs/configuring/min-instances), but **not an explicitly verified actual zero** or cost stop. `maxScale=1` came from preceding read-only snapshot.

**Still required before any hosted C5 B1 authorization:** get exact *current* preimage/rollback plan for tag + root traffic without changing it; verify proposed new npm-free OCI index as exact target and local Sigstore receipt, ensure latest/new revision flags and service IAM remain safe; confirm other effective access (parent/basic-role) expectations and service Invoker IAM-check policy; document scope for side-provider spend and explicit owner acceptance. **C4 six-CVE conditional technical triage prepared but OWNER RELEASE ACCEPTANCE PENDING**; historical scan 1 CRITICAL/5 HIGH persists. C3 LOCAL verified PASS and registry signature NOT attached. Existing G4 Owner/Editor nonexclusive limited-risk owner acceptance is for **one future separately authorized OFF-only trial**, not a deployment approval. **G8 billingEnabled=True only**, all-provider hard financial stop unproven. **No deploy, invoker call, new database, IAM edit, billing edit or new cloud request happened in this step**.

**Current gate:** `G4_IN_MEMORY_CONFIG_REVIEW=COMPLETE`, `G4_IAM_CHECK_NOT_EXPLICITLY_DISABLED=PASS_WITH_SCOPE`, `G4_NAMED_INVOKER_COUNT=1_NOT_EXCLUSIVE`, `G4_OTHER_DB=OPEN`; `G8_ALL_PROVIDER_SPEND_STOP=OPEN`; `C5_DEPLOYMENT=NOT_STARTED`, `G2_HOLD`, `STEP04_HOLD`, `PRODUCTION_NO_GO`. NEVER repeat completed C1/C2/C3/C4, single read-only Cloud snapshot or this in-memory check merely to produce another green result.

## 21 Nov 2026 ~17:03 IST — G4/G8 bounded current Cloud Run/IAM/Billing READ-ONLY snapshot COMPLETE; C5 preimage shows 3 revisions, new npm-free index NOT deployed (LATEST)

**Owner actual screenshot from correct Windows PowerShell** of the single previously owner-approved `gcloud.cmd` Cloud Run/IAM/billing-state read-only block (no mutation):
```text
G4_G8_READ_ONLY_START=YES
G4_SERVICE_READ=PASS
SERVICE_NAME=oldx-owner-read
LATEST_READY_REVISION=oldx-owner-read-00003-nus
RUNTIME_SERVICE_ACCOUNT=oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com
INGRESS=all
CURRENT_IMAGE=asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-owner-read-step3-rc@sha256:c5fc856b45b19ec995167753d0ab7449fea9550f7e06b1b75da025fe179928dc
MIN_SCALE=UNKNOWN
MAX_SCALE=1
TRAFFIC_ENTRY_COUNT=3
TRAFFIC_REVISION=oldx-owner-read-00001-8kr PERCENT=100 TAG=UNTAGGED
TRAFFIC_REVISION=oldx-owner-read-00002-tid PERCENT=UNKNOWN TAG=healthcheck
TRAFFIC_REVISION=oldx-owner-read-00003-nus PERCENT=UNKNOWN TAG=step3-rc14
G4_SERVICE_IAM_READ=PASS
SERVICE_PUBLIC_POLICY_MEMBERS=0
G4_PROJECT_IAM_READ=PASS
PROJECT_OWNER_MEMBER_COUNT=2
PROJECT_EDITOR_MEMBER_COUNT=1
PROJECT_RUN_INVOKER_MEMBER_COUNT=0
G8_BILLING_ENABLED=True
G8_SPEND_CAP_RECHECK=NOT_PERFORMED
G8_ALL_PROVIDER_HARD_STOP=NOT_PROVEN
G4_G8_READ_ONLY_SNAPSHOT=COMPLETE
```
**Important qualified conclusions:** Service **latest ready revision** `00003-nus` is **not** revision serving 100% main traffic (`00001-8kr`). `CURRENT_IMAGE` from `spec.template.spec.containers[0].image` is **latest service template** `oldx-owner-read-step3-rc@sha256:c5fc...` and not necessarily the 100%-traffic revision image. It is also **NOT** the newly frozen/signed npm-free OCI index `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`; this is expected before new C5 and no deploy was authorized. Tagged revisions' percent property was **absent** in the projected output -> `UNKNOWN` printed, not proof of exact zero. Existing GitHub earlier evidence describes old step3 revision with 0%, but distinguish historical from current projection. Max scale template=1; min scale `UNKNOWN`, not a proof that 0 is explicitly set. Project policy counts are direct returned policy bindings and omit potential parent-level roles; 2 Owners/1 Editor can potentially invoke, so **no exclusive-owner IAM claim**. Service policy has zero `allUsers` or `allAuthenticatedUsers`, but **not yet proof authentication IAM check is enabled**: Google Cloud Run may be made public by `run.googleapis.com/invoker-iam-disabled=true` even with zero public bindings. Need in-memory read-only check of that service annotation (no Cloud API retry) before asserting private access. `INGRESS=all` permits network reachability but is not equal to permission to invoke. Billing enabled does **not** prove Cloud Run-only ₹100 cap or all-provider hard-stop, which remains OPEN.

**NEXT only from existing PowerShell variables (no new gcloud calls):** user should inspect **already populated** `$svc.metadata.annotations.'run.googleapis.com/invoker-iam-disabled'` (print sanitized `TRUE_STOP` / `FALSE` / `NOT_SET`), service-level `run.googleapis.com/minScale` and template-level `autoscaling.knative.dev/minScale` (print `NOT_SET` on missing), `$svc.spec.template.spec.containers[0].env` for exact expected feature activation flags only (print `EXACT_FALSE` / `MISSING` / `NOT_FALSE_STOP`, never raw values/secret environment variables), and from already-loaded `$servicePolicy.bindings` print only **named** `roles/run.invoker` binding count/member count (no members). Fail closed if `$svc` or `$servicePolicy` no longer in memory; do not automatically fetch again without a new limited decision. No copies of raw Cloud IAM or secrets uploaded to GitHub.

**State:** `G4_G8_READ_ONLY_SNAPSHOT=COMPLETE` limited scope; `G4_EFFECTIVE_EXCLUSIVE_IAM=NOT_PROVEN`; `G4_INVOKER_IAM_CHECK=NOT_YET_INSPECTED`; `G4_OTHER_DB_ISOLATION=OPEN`; `G8_BILLING_ENABLED=TRUE`, `G8_ALL_PROVIDER_HARD_STOP=OPEN`; `C3_LOCAL_SIGNED_INDEX=CRYPTO_PASS`, `C4_OWNER_RISK_ACCEPTANCE=PENDING`, `C5_NPMFREE_REVISION=NOT_DEPLOYED`, `STEP04=HOLD`, `PRODUCTION=NO_GO`. NEVER redo C1/C2/C3/C4 one-shots, source tests, old billing cap screenshot, Grype, upload or signing.


## 21 Nov 2026 — C4 bounded disposition and G4/G8 gated handoff (LATEST)

This is the **reviewer's source-and-evidence-based RECOMMENDATION**, not an owner waiver, qualified third-party certificate, signed VEX, new Grype scan or authorization to activate a cloud service. It is based on the exact owner-observed one-shot C4 result at ~16:51 IST: six `docker cp` checks reported **`NOT_CONFIRMED`**, `C4_EXACT_FROZEN_IMAGE=PASS`, `C4_CONTAINER_STARTED=NO`, receipt saved, cleanup PASS. The original offline Grype snapshot **remains 1 CRITICAL + 5 HIGH + 12 MEDIUM + 2 LOW**.

### Decision matrix — one disposition per existing severe finding

| ID / package | Technical disposition **proposed**, not a scanner rewrite | Mandatory containment / decision trigger |
| --- | --- | --- |
| **CVE-2019-1010022** / glibc 2.43.0-r14 / CRITICAL | **DISPUTED CLASSIFICATION — CONDITIONAL REVIEW ONLY.** Red Hat marked NOTABUG; evidence suggests a stack-canary hardening/post-compromise concern, rather than an established OLDX HTTP attack. Exact BellSoft VEX not present. | Keep scanner CRITICAL visible; restrict to private nonroot default-OFF/503 staging until qualified reviewer and owner **explicitly** record any residual risk acceptance; untrusted native processing or a demonstrated exploit chain = STOP |
| **CVE-2019-1010023** / glibc / HIGH | **CLI PATH REQUIRES UNTRUSTED ELF + `ldd` — NOT PROVEN REACHABLE.** Source test covers 27 first-party JS files; six common `ldd` path probes returned NOT_CONFIRMED, **not ABSENT**. | No untrusted ELF accepted for dependency inspection; no generic subprocess/exec in product-read route; third-party/native paths still unknown. If an actual untrusted-file → `ldd` chain is found, STOP until eliminated |
| **CVE-2026-0861** / glibc / HIGH | **UPSTREAM AFFECTED VERSION RANGE EXCLUDES CURRENT 2.43.0-r14 — STRONG VENDOR-EVIDENCE CANDIDATE.** BellSoft's noted affected range is 2.30–2.42; exact image VEX absent. | Confirm publisher/base lineage is unchanged at frozen digest; do **not** compare fix `-r6` from a different upstream glibc version as if directly ordered against `2.43.0-r14`. If advisory scope changes, review material delta |
| **CVE-2026-19499** / glibc / HIGH | **SAME-STREAM VENDOR FIXED-VERSION MATCH CANDIDATE.** BellSoft reports 2.43.0-r6 fixed; frozen exact installed 2.43.0-r14, not independently image-specific VEX. | Require exact package lineage/immutability and reviewer acknowledgement. If evidence of an exploitable `strfmon*` path or wrong package stream, STOP |
| **CVE-2026-84243** / glibc / HIGH | **EXACT VENDOR FIXED-VERSION MATCH CANDIDATE.** BellSoft lists 2.43.0-r14 as fixed and frozen image reports r14, but no signed image-scoped negative VEX. | Keep nonroot/privilege boundaries verified at target revision; reassess if locale path/trust boundary is exposed or version mapping changes |
| **CVE-2026-119586** / sqlite-libs 3.54.1-r0 / HIGH | **SQLITE CLI PIPELINE EXPOSURE NOT ESTABLISHED.** SQLite describes `.recover` + unsafe second sqlite3 CLI, not core library API; six path probe returned three sqlite3 `NOT_CONFIRMED`, **not CLI ABSENT**. | No untrusted DB → `sqlite3 .recover` → second CLI path; first-party route lacks direct CLI use, transitive/other paths unknown. A reachable CLI chain requires a targeted fix or disabling feature before serving requests |

**No `RESOLVED`, `PATCHED`, `VEX_PASS` or `C4_OWNER_ACCEPTED` status is claimed** for any row. Existing G2 Security Watch tracks only *material newly published vendor evidence*; do not create a duplicate monitor or rerun old scan/build to refresh these dispositions.

### Two distinct acceptance levels — do not conflate them

**Level 1 — one possible future, separately approved, private Cloud Run B1 trial with DEFAULT-OFF/503, owner-supervised.** A *candidate* bounded operational risk acceptance can be considered only when all conditions are verified for the actual revision: 0% main traffic (tagged URL can still be invoked by authorized principals), no public/anonymous caller, min instances 0, bounded max instances, no credential-backed product reads/writes enabled, no new sensitive fixture inputs, exact pinned OCI index digest and local signature-bundle receipt, short rollback/cleanup window, and owner-approved nonzero cost exposure. The previous **G4 limited acceptance** applies only to existing Owner/Editor potential invokers for one OFF-only B1; it **does not** authorize B1 execution nor prove exclusive effective invocation. Private OFF-only B1, if ever authorized and observed, is **not** C4 risk acceptance for enabled traffic or production.

**Level 2 — enabled feature, live user data or production launch.** **NO-GO by this packet.** Before a release, independently review routes, authz/data isolation, abuse/rate limits, third-party/native execution and hard failures; evidence-tie any remaining severe findings to exact deployed digest, version and chosen compensating control, and collect a **separate, dated explicit owner acceptance** of named residual risks. The owner's strategic decision not to wait indefinitely for vendor patches applies at *that future release gate*, not as a present blanket security waiver.

### G4/G8 exact limitation at next Step04 handoff (no live changes)

- **G4 Cloud Run:** The owner already accepted *existing* project Owner/Editor **possible additional authenticated invokers** for **one** future private OFF B1; `G4_EFFECTIVE_EXCLUSIVE_INVOKER=UNVERIFIED/NONEXCLUSIVE`, because basic project roles can also provide `run.routes.invoke`. No roles are added to the former Owner or to any principal, and no existing privileges are removed in this source review. Even a 0% traffic revision can be invoked by authorized principals through tagged URL. **Separate G4 Firestore:** oldx-staging has previously observed only `(default)`; default-DB one-doc source/runtime proof passed, but no actual other-DB negative isolation was performed and no second DB should be provisioned solely for the check. A precise IAM condition doesn't override other unconditional project grants. For OFF-only trial, **do not enable any Firestore-dependent route** until scoped policy evidence is sufficient.
- **G8 spend:** Owner-observed **₹100/month Cloud Run-only** spend cap is *one project + one eligible service*, not all-provider enforcement. Source-only 20-minute review planning bound `maxGrossPaise <= 10000` is a proposal validation, **not billed-spend verification or provider hard kill switch**. Firestore/Auth/Logging/Artifact Registry/network and delayed charges can escape the Cloud Run-only cap. For a future trial, minimize chargeable surface, designate exact owner/operator, hard-stop operationally on usage/error, specify short end time and cleanup, and obtain **explicit approval for unbounded-by-cap side costs** or do not deploy. No all-provider G8 PASS is possible from present evidence; alerts-only budgets do not cap spending.
- **Signature/provenance:** C3 owner-local DSSE signature for `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79` cryptographically verified with exact Yasmin/Google issuer; Registry signature referrer **NOT ATTACHED**; independent trusted builder SLSA **UNVERIFIED**. C5 should verify that *same exact local bundle or an approved attached signature*; it must not silently fall back to a mutable tag or the older V2 image.
- **No repeat:** C1 original single-push journal consumed, C2 passed, C3 signed once and verified, C4 filesystem probe completed. No repeat of passed checks, no new build/scan/signature/Registry write merely to close documentation.

### G4/G8 → C5 single OFF-only staging B1 decision card — SOURCE-ONLY, NOT EXECUTION

**Do not submit B1 from this card.** It describes the **next precisely scoped approval boundary**, based only on prior owner/policy evidence. Mark preimage and live parameters **UNVERIFIED** until an authorized, fresh, read-only staging snapshot is collected; do not assume an old rollback or CI report describes today's live service. Owner standing approval for *public Sigstore signing identity* and the separate G4 nonexclusive-invoker risk does not authorize hosted deployment, new tokens, billed traffic or Registry signature referrer writes.

| Dimension | Proposed one-trial bound (subject to concrete owner approval) | Current evidence / STOP |
| --- | --- | --- |
| Cloud project/service | `oldx-staging` / private Cloud Run `oldx-owner-read` in its **actual verified** region; proposed tag `ownerreadv2` | Confirm service/revision/region and current preimage without changing state; stop if drift |
| Image custody | **Existing immutable private OCI index** `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-npmfree-20261121-a1@sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79` | C1/C2 remote identity and C3 owner-local DSSE signature PASS; exact **local** bundle SHA256 `1ce7427b1d5dbb3b1c13cfd9a97b690d5c94d20f3509516c8014259c933d896`. No Registry signature attached. Do not use older V2 digest/tag; determine how the operator independently validates the local bundle |
| Runtime contract | **DEFAULT-OFF/503** for product feature; no credential-backed product reads, no Firestore/Auth/Storage writes, no guest/real-user usage | Verify actual exact code+env behavior and deny-by-default route before any hosted action; if source and deployed digest differ, STOP |
| Traffic/access | **Private authenticated** service, IAM Invoker check intact, main traffic **0%**, owner-only supervised tagged test URL *with known existing other project Owners/Editor potentially invokable* | G4 has **limited owner acceptance only for this risk in one future OFF B1**; cannot claim exclusively invokable. Tagged URL can be called even with main traffic at 0%; no broadening/anonymous access |
| Resource & duration | Proposed `min instances=0`, `max instances=1`, short **20-minute** supervised observation, bounded one smoke-call sequence; no autonomous follow-up or permanent service | These are proposals, **NOT currently observed settings**. Preimage, health-check policy, concurrency, network/logging and rollback need confirmation |
| Database/identity | Do not enable any Product/Firestore access. Keep expected database `oldx-staging/(default)` explicit and deny-by-default | Actual default-DB one-doc prior proof PASS and consumed; effective other-DB denial **UNVERIFIED**. Do not create second DB to make gate pass. No new IAM or default Compute SA role changes |
| G8 cost | Proposed per-trial review envelope max **₹100 gross**, owner to consider **additional uncovered provider charges**; existing Cloud Run-only monthly ₹100 cap separately observed | No project-wide/Firestore/Logging/Registry hard cap. No 100%-safe cost guarantee, even for a 20-min 0% traffic test. If owner declines uncovered cost or estimates cannot be reasonably bounded, STOP |
| Evidence & rollback | Snapshot actual service config, effective IAM risk, exact digest and original traffic/preimage; separately authorize and demonstrate **R1 remove trial tag** and **R2 restore original config/traffic**, with failure recovery, no old-run repetition | Prior historical B1/R1/R2 success is not automatic authorization nor proof of this newer image's future rollout. No automatic retry on partial action |

**GO for source-only documentation**: yes (this card). **GO for creating B1, IAM/Firestore/Cloud Run changes, billing or production**: **NO — requires fresh exact resource/identity/call/budget approval and a genuinely executable rollback plan**. If qualified reviewer and owner elect to accept the six unresolved scanner severe findings, record precise named risks and controls in the [launch decision register](launch-decision-register-2026-11-07.md) only at the relevant release boundary, not as historical waiver.

**Optimal next operation:** One *new* qualified source-only checklist review is done here; the only remaining evidence that can materially change B1 readiness is **an approved, minimally scoped current live service/preimage/read-only IAM and spend-scope snapshot**. Do **not** ask for a repeat of old C1/C2/C3, C4 scan or prior G4 synthetic one-document proof. If user approves a bounded live read later, prepare a single command/operation and STOP on drift; no deploy inside a read-only approval.


**Decision ledger at this checkpoint:**

```text
C4_SIX_CVE_TECHNICAL_TRIAGE=PREPARED_WITH_CONDITIONAL_DISPOSITIONS
C4_FROZEN_SCAN_COUNTS=1_CRITICAL_5_HIGH_12_MEDIUM_2_LOW_UNCHANGED
C4_OWNER_EXPLICIT_RESIDUAL_RISK_ACCEPTANCE=NOT_GRANTED
C4_ENABLED_RELEASE_CLEARANCE=HOLD
C4_PRIVATE_OFF_B1=ONLY_FUTURE_CANDIDATE_SEPARATE_AUTHORIZATION
G2_PROVENANCE_AND_SECURITY_CLEARANCE=HOLD
G4_NONEXCLUSIVE_OFF_B1_RISK=OWNER_ACCEPTED_LIMITED
G4_OTHER_DATABASE_ISOLATION=UNVERIFIED
G8_CLOUD_RUN_ONLY_CAP=PREVIOUSLY_OBSERVED_100_INR_MONTH
G8_ALL_PROVIDER_FINANCIAL_HARD_STOP=NOT_PROVEN
C5_STAGING_DEPLOYMENT=NOT_AUTHORIZED
STEP04=HOLD
PRODUCTION=NO_GO
```

**Next meaningful task (no new console command required for this source-only checkpoint):** reconcile the *existing* G4/G8 evidence into a single limited B1 approval card with explicit OFF/503, zero traffic, cross-DB exclusion, all-provider expense warning, verification of the exact derived digest and rollback. Do not trigger B1 yet. If this card cannot offer a bounded safe trial, document BLOCK rather than call C4/G2 PASS.


## 21 Nov 2026 ~16:51 IST — C4 frozen npm-free CLI-path ONE-SHOT inspection COMPLETE; 6 paths NOT_CONFIRMED (LATEST)

**Owner actual Windows PowerShell screenshot** of the pinned dedicated C4 one-shot script `scripts/step04-c4-npmfree-cli-presence-once-a1.py`, now run **once** in the correct `PS C:\Users\Yasmin Parmar>` shell:
```text
C4_SOURCE_SHA256=PASS
C4_EXACT_FROZEN_IMAGE=PASS
C4_CONTAINER_STARTED=NO
C4_PATH=/usr/bin/sqlite3 STATE=NOT_CONFIRMED
C4_PATH=/bin/sqlite3 STATE=NOT_CONFIRMED
C4_PATH=/usr/local/bin/sqlite3 STATE=NOT_CONFIRMED
C4_PATH=/usr/bin/ldd STATE=NOT_CONFIRMED
C4_PATH=/bin/ldd STATE=NOT_CONFIRMED
C4_PATH=/usr/local/bin/ldd STATE=NOT_CONFIRMED
C4_LOCAL_RECEIPT_SAVED=YES
C4_CONTAINER_CLEANUP=PASS
C4_PROBE_STATUS=INSPECTION_COMPLETE
C4_CVE_DISPOSITION=STILL_REVIEW_REQUIRED
C4_G2=HOLD
```

**Evidence limitations exactly as script implemented:** The local image identity/config/OCI index descriptor matched the frozen `oldx-bellsoft-npmfree:20261120-a1` and `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`. Docker created **one stopped container** (never started image process), inspected six `sqlite3` and `ldd` absolute paths with `docker cp`, discarded tar bytes, then deleted stopped container. **`NOT_CONFIRMED` deliberately conflates failed `docker cp` with a possibly missing file/other error**, so do NOT promote to `ABSENT`, `UNREACHABLE`, `PATCHED` or `CVE_FIXED`. Unchecked filesystem paths, shell alternatives, native/third-party components and dynamic execution remain outside this focused probe. Exact reason for each `docker cp` failure is not collected (stderr suppressed). Owner-private receipt is **`D:\OLDX\G2\c4-npmfree-cli-presence-20261121-a1.json`**, already saved; preserve. No C1 or C3 repeat, no new build/scan/upload/Registry/Cloud write, no deployment.

**Next source-only C4 disposition using this evidence:** For `CVE-2019-1010023` (`ldd` on malicious ELF) and `CVE-2026-119586` (SQLite CLI unsafe `.recover` pipeline), classify `KNOWN_SIX_CLI_PATHS_NOT_CONFIRMED_AND_FIRST_PARTY_DIRECT_EXEC_PATHS_NOT_SEEN` with **partial exposure-reduction support**, but NOT established absence or unexploitable. Existing official Red Hat/SQLite/BellSoft version/advisory evidence for the other four remains frozen; overall original local one-shot Grype **1 CRITICAL / 5 HIGH** stays unchanged. A **qualified reviewer/owner must expressly decide** six separate risk dispositions/mitigations and whether extra proof is necessary. Do not invent a waiver or blanket C4 PASS.

**Decision/current:** `C4_EXACT_IMAGE_PROBE=INSPECTION_COMPLETE`, `C4_CONTAINER_CLEANUP=PASS`, `C4_QUALIFIED_SIX_CVE_DISPOSITION=PENDING`, `C4_OWNER_RISK_ACCEPTANCE=PENDING`, `C3_LOCAL_DSSE_SIGNATURE=CRYPTOGRAPHICALLY_VERIFIED_PASS`, `C3_REGISTRY_SIGNATURE=NOT_ATTACHED`, `G2=HOLD`, `G4_OTHER_DB=OPEN`, `G8_ALL_PROVIDER_SPEND_STOP=OPEN`, `STEP04=HOLD`, `PRODUCTION=NO_GO`. Stop: never repeat this C4 one-shot; no follow-up shell checks needed just to preserve evidence.

## 21 Nov 2026 — C4 EXACT npm-free CLI-path presence probe PREPARED, NOT YET RUN (LATEST)

**New dedicated script:** [scripts/step04-c4-npmfree-cli-presence-once-a1.py](scripts/step04-c4-npmfree-cli-presence-once-a1.py), frozen initial commit `7cba228f59bcb6903bb64c783231605b2ea3bf16`, Git blob SHA `1bc7941c9cd2434493343d34b01f9d15d53ef3d1`, **SHA256 `270f8978c2b3a7345114f7e2522cbf7228ff6a6169c195437e84e2f56b8cec4e`** (calculated from exact committed source by a SHA256 function that passed the known `abc` test vector). Owner has **not run the script yet**. Do not reuse the older `step04-bellsoft-fs-exposure-once-a1.py` since it targets an older, different image.

**Exact scope:** Safeguard local WSL + Unix Docker context with no remote override; pin existing `oldx-bellsoft-npmfree:20261120-a1` by both local image ID and OCI index `sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79` / media type / 856 bytes; check expected `appuser` + Node entrypoint/CMD. Create a **never-started** local Docker container (`--network none --read-only --cap-drop ALL`), only `docker cp` 6 `sqlite3`/`ldd` path probes with copied file bytes discarded, and remove stopped container in `finally`. Create one exclusive small owner-local receipt `D:\OLDX\G2\c4-npmfree-cli-presence-20261121-a1.json` with status/cleanup. File check responses are `PRESENT` or `NOT_CONFIRMED` (NOT “definitely absent”); cannot establish transitive library execution or prove CVE fixed. Only temporary local Docker container metadata and a tiny private receipt are written; no image execution, build, upload, scan, IAM, cloud, billing or deployment.

**Next owner's exact one-time step:** Download pinned raw script from public GitHub commit into unused `D:\OLDX\G2\c4-npmfree-cli-presence-once-a1.py`; verify its exact SHA256 by PowerShell then `wsl.exe -- python3 /mnt/d/OLDX/G2/c4-npmfree-cli-presence-once-a1.py` ONCE. STOP on mismatch/errors/existing file, no automatic re-runs. Wait for actual owner screenshot before declaring result. All prior C1/C2/C3 checks frozen; C3 local signed bundle crypto PASS; C4 six severe risk acceptance PENDING, G2 HOLD, G4 cross-db OPEN, G8 full-provider spend stop OPEN, Step04 HOLD, production NO-GO.

**Prepared 21 November 2026 after C3 LOCAL signature verification. Source-only; no automatic waiver, deployment, IAM, Registry write, scan or cost approval.**

## C4.1 — 21 Nov 2026 official-vendor and code-path independent source review

**Nature of this checkpoint:** READ-ONLY external official-source research combined with pre-existing review-branch source inspection. **No rebuilt image, no new vulnerability scan, no owner-local private artifacts copied, no new local CLI/filesystem test**, and no assertion that the original full report has been reparsed. This section **does not supersede the frozen Grype counts**, and neither an upstream advisory nor a source-only code inspection certifies the actual deployed image is safe.

### A. Six severe IDs — evidence-specific triage, not blanket dismissal

| CVE / Grype severity | Fresh authoritative evidence actually read (21-Nov-2026) | OLDX-specific exposure gap | Suggested CONDITIONAL C4 disposition |
|---|---|---|---|
| **CVE-2019-1010022 / CRITICAL**, glibc 2.43.0-r14 | Red Hat [bug 1731964](https://bugzilla.redhat.com/show_bug.cgi?id=CVE-2019-1010022) shows **CLOSED NOTABUG** and its security team describes the glibc stack-canary behavior as a post-compromise mitigation concern, not a direct glibc security flaw. [Ubuntu](https://ubuntu.com/security/CVE-2019-1010022) independently records upstream non-security treatment. | Scanner still flags CRITICAL on the frozen APK via generic CPE and no BellSoft subject-bound VEX/explicit owner acceptance obtained. | `DISPUTED_CLASSIFICATION_REVIEW_CANDIDATE`. Qualify/record scanner-versus-upstream conflict; **keep one CRITICAL OPEN** until release reviewer accepts with exact BellSoft image scope |
| **CVE-2019-1010023 / HIGH**, glibc | [Red Hat advisory](https://access.redhat.com/security/cve/cve-2019-1010023) identifies misuse of `ldd` on **untrusted ELF**. For untrusted binary dependency inspection, Red Hat recommends `objdump -p` rather than `ldd`. | No evidence production route shells out to `ldd`, but presence/absence of `ldd` inside **frozen npm-free image** and transitive native modules not proven. | `CONDITIONAL_CLI_PATH_LOW_REACHABILITY_CANDIDATE`; require confirmation no untrusted file → `ldd` path, and keep code/process execution disabled |
| **CVE-2026-0861 / HIGH**, glibc | BellSoft [publisher advisory](https://docs.bell-sw.com/security/cves/CVE-2026-0861) describes upstream affected GNU libc **2.30–2.42** and identifies Hardened Containers Stream fix **2.39.0-r6** on its historical stream line. The frozen new derived image is recorded to have **2.43.0-r14**. | **Do NOT compare only the APK `-r6` vs `-r14` values across different glibc 2.39/2.43 branches.** 2.43 is outside the advisory's listed affected upstream range, but an exact image-specific publisher VEX or source-patch pedigree is not in this packet. | `STRONG_VERSION_OUTSIDE_AFFECTED_RANGE_CANDIDATE`; obtain reviewer’s image-specific rationale rather than assert Grype false positive universally |
| **CVE-2026-19499 / HIGH**, glibc | BellSoft [publisher advisory](https://docs.bell-sw.com/security/cves/CVE-2026-19499/) says **Hardened Containers Stream glibc 2.43.0-r6 FIXED**, while frozen signed base SBOM/images show **2.43.0-r14** (same 2.43.0 stream). Advisory describes `strfmon/strfmon_l` with right-justified padding and a specific buffer arrangement. | No *full transitive/native* proof whether Node/Sharp/Firebase ever invokes the susceptible path; the fixed same-release package version is stronger positive evidence but no exact image-specific VEX. | `VENDOR_FIXED_INSTALLED_VERSION_MATCH_CANDIDATE`, **not** `ZERO_HIGH`; independently document package lineage if accepted |
| **CVE-2026-84243 / HIGH**, glibc | BellSoft [publisher advisory](https://docs.bell-sw.com/security/cves/CVE-2026-84243) marks **Hardened Containers Stream glibc 2.43.0-r14 FIXED**, equal to frozen glibc 2.43.0-r14. Its exploit constraints include a crafted readable locale path and a privileged/trust-boundary scenario. | Specific locale/trust exposure for frozen nonroot/default-OFF OLDX runtime not exhaustively tested. | `VENDOR_FIXED_EXACT_VERSION_MATCH_CANDIDATE`, pending narrow image/package/reviewer decision |
| **CVE-2026-119586 / HIGH**, sqlite-libs 3.54.1-r0 | [Official SQLite CVE list](https://www.sqlite.org/cves.html) explicitly distinguishes the **CLI** scenario: crafted SQLite file, `.recover` dot-command output then passed into a second **sqlite3 CLI without `--safe`**; *not* a core SQLite library flaw. | Frozen image contains `sqlite-libs` package record, but the npm-free image's actual `sqlite3` executable presence and any transitive CLI execution route are **NOT PROVEN**. | `CONDITIONAL_CLI_ONLY_PATH_CANDIDATE`; accept only after scoped runtime image-file inventory or an independent equivalent source/binary proof tied to the exact image |

**Do not classify any of these as `FIXED_IN_OLDX_SCAN`**; retain the original unfiltered scanner output and counts as point-in-time evidence. BellSoft advisory “fixed version” is vendor evidence, not evidence the frozen Grype report has magically changed. Conversely a generic CPE match alone may misclassify a vendor-patched APK. A qualified release decision should cite *both*.

### B. Pre-existing source-only attack path and defense-in-depth evidence

- Inspected `Dockerfile.product-read.bellsoft-npm-free` on `security-hardening-review`: **exact pinned BellSoft base** `sha256:ef00ba8e634402e8dd3b374643fdbc178e876c7a312c9d55e4734efaa1e93d94`, final `USER appuser`, inherited Node entrypoint and explicit runtime JS server command. It strips the bundled npm runtime path at build stage, rather than attempting an OLDX source lock change. Do not rebuild it.
- Inspected `functions/staging-marketplace/product-read-server.mjs`: only health routes and bounded POST API route; **default `enabled=false` gives 503**, request bounds are set, and source header notes **no guest or write routes**. This is a meaningful proposed compensating control at **guarded default-OFF staging** only; actual Cloud Run configuration/identity/policy still separately unverified for future C5.
- Inspected existing `tests/integration/step04-runtime-cli-paths.test.mjs`: the source test enumerates **27 exact first-party runtime JS files from the Dockerfile COPY statements** and rejects direct literals `node:child_process`, `ldd`, `sqlite3`, `.recover` and common subprocess-call forms. **This file is a test specification, NOT a freshly executed test here**, and the author explicitly notes it cannot audit dynamically assembled strings, third-party/native imports, BellSoft base filesystem, or programs outside the final runtime. No conclusion of complete `ldd` or sqlite absence is justified.
- An older `scripts/step04-bellsoft-fs-exposure-once-a1.py` exists, **but pins the PREVIOUS BellSoft derived image** `sha256:161fedc0...`. It does **not** apply to current npm-free index `0844...`. Do not rerun or reuse its result as proof about the new image. A novel **metadata-only** inventory on exact frozen npm-free image might close the sqlite/ldd CLI presence gap, but must be designed with frozen-image guards and without touching the consumed one-shot runner; not necessary to write this source-only packet.

### C. Proposed least-cost C4 decision, **not yet owner release acceptance**

- The strongest candidate for **qualifying upstream scanner mismatch** is `CVE-2019-1010022` (Red Hat NOTABUG); strongest positive **publisher fix version** evidence is `CVE-2026-19499` (fixed 2.43.0-r6, installed r14) and `CVE-2026-84243` (fixed r14, installed r14); `CVE-2026-0861` upstream affected range excludes 2.43; `CVE-2019-1010023` and `CVE-2026-119586` remain CLI-reachability-limited candidates pending exact image/route evidence. No numerical “risk reduction percentage” or guaranteed safety inferred.
- **Suggested release risk posture:** keep `C4_EXACT_SIX_CVE_REVIEW=SOURCE_TRIAGE_PREPARED`, `C4_QUALIFIED_DISPOSITIONS=PENDING`, `C4_OWNER_RISK_ACCEPTANCE=PENDING`. Allow owner, after reviewer review, to explicitly accept **bounded residual risk** if mitigations adequately cover reachable paths; such acceptance is **not equivalent** to software patches or external signed VEX. Keep all six visible in scanner record. If one verified exploitable pathway exists, choose targeted fix/defense and reassess.
- **C3-to-C5 signature transport:** A local cryptographically verified signed bundle is sufficient to **document** one owner-controlled custody check, but **not** automatically discoverable by an external Cloud Run/Registry admission system. Plan a release preflight that uses the same exact local bundle SHA256 + immutable index digest + exact Yasmin identity/issuer and stores *sanitized pass/fail receipt* before staging, **or** obtain separate owner approval for creating an Artifact Registry signature/referrer when the approved architecture actually needs remote discovery. A private repo image existing in Registry is not evidence of attached signature. Avoid uploading as a default.
- **G4/G8 policy remains separate**: G4 effective Firestore IAM protection across databases and G8 full-provider spend control are not fixed by vendor advisories or signing. Guarded C5 default-OFF staging still requires exact configuration/rollback/retention/rate-control decisions, qualified review and a separate staged release authorization; production remains NO-GO. The standing intent to launch when website is ready does not override this risk register now.

**Next genuinely useful NEW check, if qualified reviewer requires CLI-path closure:** read-only inventory of exact npm-free image's `sqlite3`/`ldd` filesystem presence and final runtime routes, using frozen index/config identity guards and **no Docker build/scan/upload, no old script rerun**. First decide whether this evidence changes the C4 decision enough to justify even a small new inspection. Do not spend time building a general testing framework or rerunning 27-source tests only to reconfirm frozen source.

---

## A. Frozen C1→C3 evidence — do not repeat

- Target **private** Artifact Registry OCI **index**, pinned: `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-npmfree-20261121-a1@sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`. Already read-only verified local Docker's `.Descriptor` matches remote OCI index SHA256/mediaType/856B; remote AMD64 manifest and config SHA/size, 10/10 ordered local vs remote RootFS `diff_ids`, ten remote compressed-layer HEAD/advertised-size responses, and pinned runtime user/entrypoint/CMD passed. These checks are frozen and have individual documented limits; full compressed-layer byte hash independently not performed.
- Original C1 single-push script printed `STOP_C1_OUTCOME_POSSIBLY_REMOTE_CHANGED` and its one-shot journal was consumed. Later successful targeted read-only remote reconciliation does **NOT** rewrite that runner's original `STOP` into `SUCCESS`. Never rerun C1 `--execute`, reupload, retag, rebuild or rescan merely to make a green result.
- **C3 local keyless signed custody**: owner already approved public disclosure of Yasmin Google signing identity. Cosign **v3.1.4** ran `sign --upload=false --bundle=<owner-local file> IMAGE@sha256:<index>` once, created the local 6,947-byte **Sigstore v0.3 DSSE** bundle `D:\OLDX\G2\c3-cosign-v3.1.4\oldx-c3-index-20261121-a1.sigstore.json` with SHA256 **`1ce7427b1d5dbb3b1c13cfd9a97b690d5c94d20f3509516c8014259c933d896`**, retained exclusive journal `oldx-c3-sign-20261121-a1.attempt.txt`, and cleaned temporary WSL Docker credentials. Local bundle content has exact single subject index SHA256, Fulcio cert and one tlog entry.
- **21 Nov ~04:30 IST actual owner screenshot:** `cosign verify-blob-attestation --bundle <this exact local bundle> --certificate-identity yasminparmar087@gmail.com --certificate-oidc-issuer https://accounts.google.com --digest 0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79 --digestAlg sha256 --type https://sigstore.dev/cosign/sign/v1` returned **`Verified OK`**. Valid exact certificate identity/issuer, cryptographic DSSE signature, signed subject digest, predicate, transparency verification under default safe Cosign policy. **C3_LOCAL_SIGNED_INDEX_BUNDLE=PASS**, not a Registry-hosted signature.
- **No signature/referrer was uploaded to Artifact Registry** (`--upload=false`). Future C5 verifier must either securely receive this exact local bundle with exact trusted signer policy, or separately obtain owner approval for narrow Registry attachment and associated storage/network cost. No standing permission for OCI attach. No retrospective trusted builder SLSA or complete byte-chain proof is created by signing.

Sources: [C2/C3 packet](OLDX_STEP04_C2_C3_NO_REUPLOAD_RELEASE_GATE_2026-11-21.md), [canonical no-rebuild custody route](OLDX_STEP04_NPMFREE_NO_REBUILD_CUSTODY_ROUTE_2026-11-21.md), [owner's Issue #17 audit](https://github.com/yasminparmar087-ops/oldx-website/issues/17). No secrets, login URLs or authorization codes are stored.

## B. Frozen npm-free image scan: remaining **1 CRITICAL + 5 HIGH** (plus 12 MEDIUM, 2 LOW)

Historical **one-shot** frozen npm-free derived-image Grype scan is `CRITICAL=1; HIGH=5; MEDIUM=12; LOW=2` on offline DB snapshot, not a live scanner view. Its private unfiltered report and local source artifacts remain owner-local **D:**; previously verified report SHA256 `142e52449a4c610d79c2cefd8193f70c671bb58c643710a3fe64a7c85bf03a89`, source SHA `fcc96574b6388dc441a0b5d3eade48e79c7ebb24`, summary SHA256 `e263d56102bc0a5656a704d952eb4e35be8d7b9310ac66f8a53bd3d704125bea`. Existing nonroot / Node / Sharp / Firebase / health-200 / default-off-503 / shutdown local runtime smoke was completed at original one-shot execution. **No new scan or runtime test is authorized or needed merely to prepare this packet.**

The [BellSoft nine-severe evidence tracker](OLDX_BELLSOFT_9_CVE_TRACKER_2026-11-19.md) identifies the following six **remaining** APK `nvd:cpe` matched IDs in the npm-free report after three earlier nested `npm/undici` GHSA findings were removed via npm-free runtime design. The mapping below is a **source-only cross-reference**, not a fresh parsed scan or a new vendor VEX:

| CVE | Package in frozen report | Severity | Known bounded evidence | CURRENT disposition / decision needed |
| --- | --- | --- | --- | --- |
| `CVE-2019-1010022` | glibc `2.43.0-r14` | **CRITICAL** | Earlier Red Hat / Ubuntu notes dispute security classification; still shows as Grype CPE match | **OPEN**; no BellSoft-index-bound signed NON_AFFECTED VEX / independent qualified acceptance. Do not dismiss automatically |
| `CVE-2019-1010023` | glibc `2.43.0-r14` | HIGH | Reported vulnerability is executing `ldd` against crafted ELF; runtime exposure not proven | **OPEN**, path-specific candidate low reachability, not confirmed non-affected |
| `CVE-2026-0861` | glibc `2.43.0-r14` | HIGH | Prior BellSoft advisory/fixed-version evidence notes r14 floor; generic `nvd:cpe` scanner match remains | **OPEN**, require precise vendor version/scope mapping or signed VEX; don't erase report |
| `CVE-2026-19499` | glibc `2.43.0-r14` | HIGH | Same prior BellSoft fixed-version evidence, scanner CPE match | **OPEN**, source-conditional risk review |
| `CVE-2026-84243` | glibc `2.43.0-r14` | HIGH | Same prior BellSoft advisory fixed r14 evidence, scanner CPE match | **OPEN**, source-conditional risk review |
| `CVE-2026-119586` | sqlite-libs `3.54.1-r0` | HIGH | Official SQLite advisory associates exposure with particular CLI `.recover` followed by unsafe second command, not ordinary SQLite library API; `sqlite3` executable presence and reachability unproved | **OPEN**, bounded code-path/CLI availability decision needed |

Source: [BellSoft nine-CVE tracker — latest severe triage](OLDX_BELLSOFT_9_CVE_TRACKER_2026-11-19.md), [one-shot npm-free frozen evidence](OLDX_STEP04_NPMFREE_LOCAL_ONESHOT_2026-11-20.md). The tracker explicitly cautions that `nvd:cpe` matches, fixed-version advisories and application-specific exposure are distinct; absence of a visible exploit path or a publisher advisory alone is **not** proof of universal safety. Do **not** claim six CVEs fixed, zero HIGH, or G2 PASS.

## C. C4 controls and exact next bounded decisions

1. **C4 Risk register:** preserve each exact CVE, detected package, severity, source-specific advisory, version/package mapping, route reachability, compensating controls, owner acceptance or STOP, and reviewer/date. Owner's earlier desire to launch eventually even if vendor patch is unavailable does **not** automatically waive C4, authentication/privacy or live protection checks.
2. **Provenance:** Record separately: `LOCAL_OWNER_WSL_BUILD=KNOWN` and runtime smoke/Grype scan evidence frozen; `INDEPENDENT_TRUSTED_ORIGINAL_BUILDER_SLSA=UNVERIFIED`, `REMOTE_COMPRESSED_LAYER_BYTES_FULL_SHA=NOT_INDEPENDENTLY_CHECKED`, `C3_LOCAL_SIGNED_CUSTODY=VERIFIED`, `C3_REGISTRY_SIGNATURE_ATTACHMENT=NOT_DONE`. Signing cannot retroactively change original build provenance.
3. **Verification transport:** Decide if guarded C5 can verify **the existing local bundle** under an exact owner certificate/issuer allowlist, or whether Registry-hosted signature/referrer is a mandatory operational dependency. **Do not** upload a Registry signature solely because C3 local PASS; separate costs and operator approval would be required.
4. **C4 release decision:** Keep `C4_RISK_ACCEPTANCE=PENDING` until the six severe findings have individual dispositions and practical mitigations tied to exact frozen digest plus qualified reviewer/owner decision. Future new fix is an alternative, not a reason to alter the frozen OCI or rerun existing tests now.
5. **G4/G8 independently:** effective Firestore access limitation on other databases remains OPEN; all-provider financial hard stop not yet proven. A verified signature does not bypass either. C5 private/default-OFF staging (503, min0 etc) must stay non-activated until actual scoped guarded release gate, rollback, spend/retention and explicit approval; production remains NO-GO.

## D. Current milestone and next work

```text
C1_REMOTE_INDEX_CHILD_CONFIG_ROOTFS_BLOB_AVAILABILITY=PASS_WITH_DOCUMENTED_LIMITS
C2_LOCAL_REMOTE_INDEX_DESCRIPTOR_IDENTITY=PASS
C3_OWNER_LOCAL_KEYLESS_SIGNED_INDEX=CRYPTOGRAPHICALLY_VERIFIED_PASS
C3_REGISTRY_SIGNATURE_REFERRER=NOT_ATTACHED
C4_RESIDUAL_CRITICAL_HIGH_RISK_ACCEPTANCE=PENDING
G2_SECURITY_CLEARANCE=HOLD
G4_CROSS_DATABASE_IAM=OPEN
G8_ALL_PROVIDER_SPEND_STOP=OPEN
C5_STAGING_RELEASE=NOT_AUTHORIZED
STEP04=HOLD
PRODUCTION=NO_GO
```

**Next source-only task:** Independent, bounded six-CVE disposition matrix review with exact BellSoft advisories and freeze-safe original Grype locations, then a real scoped owner decision on compensating controls and the necessity of Registry signature attachment. No old C1/C2/C3 operations or scans rerun; don't leak original raw local report into public GitHub. As new official security evidence arrives, evaluate *only material deltas* through the existing scheduled G2 watch, not repeated full research.
