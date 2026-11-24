# OLDX Step 05 — H1B NEW private OFF-only mediator: image risk, provenance and owner decision packet

**Prepared 25 November 2026 IST — SOURCE-ONLY DECISION PACKET. No H1B execution authorization.**

Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review` ONLY. This packet consumes the actual ONE local H1A result at verified remote commit `2579c2998ff2ef250f579dec5a86e84a60b86d26`. Grounding: [canonical H1A exact execution receipt](OLDX_STEP05_MAXIMUM_SAFE_SOURCE_EXECUTION_RECEIPT_2026-11-25.md) and [Issue #17 H1A outcome](https://github.com/yasminparmar087-ops/oldx-website/issues/17#issuecomment-7143018758). Existing [G1 H1/H2 architecture boundary](OLDX_STEP05_C2_G1_MEDIATOR_OFF_HTTP_AND_SCOPED_HOST_DECISION_2026-11-25.md) remains relevant but contains older H1A-pending language; **this packet and the canonical H1A receipt supersede that older status**.

**Unambiguous overall status:** `H1A=PASS_WITH_LIMITS`, `H1A_APPROVAL_AND_BUILD_MARKER=CONSUMED`, `H1B=HOLD_NOT_AUTHORIZED`, `H2=NOT_AUTHORIZED`, `C2_LIVE=HOLD`, `STEP05=NOT_DONE`, `PRODUCTION=NO_GO`. **Do not rebuild, rescan, repull, rerun runtime, push, provision, activate or delete any resource** under this source-only decision task.

## 1. Frozen NEW image identity and local evidence

| Evidence | Actual H1A observed value / limitation |
|---|---|
| Immutable original base | `gcr.io/distroless/nodejs24-debian13:nonroot@sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec`; old Docker CLI verification error remains unexplained; separate raw-byte SHA matched and BuildKit accepted same pin |
| NEW image local build | ONE `linux/amd64` Docker build PASS with three hash-approved sources, restrictive context, no app providers. Size 214,841,702 bytes; built under owner-local WSL |
| **Local Docker inspect image ID / OCI index** | `sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e` — **NOT** a pushed registry manifest digest |
| BuildKit-export child manifest | `sha256:2e555bd98424d29b32a7bb3409a45e2c257569ff632085e4ff0e3a9ab4413b5f` — local reported child, **NOT** independently verified registry resolution |
| BuildKit-export image config | `sha256:c71c7268e08f9ed91a92fd4e82e499a7331c3a071985cebcede7d76efbdf5b71`; Syft source metadata imageID matched this config, not the OCI index |
| Local image tag | `oldx-h1a-c2-mediator-off:local-20261124t195244z`; retained in owner WSL; no `docker push` or exported remote immutable URL |
| Syft | v1.57.1, one full new-image squashed SBOM PASS, **15 cataloged packages**; completeness relative to all possible bundled binary code is not proven |
| Grype | v0.121.3, one scan of exact saved SBOM, **55 vulnerability/package matches, ignored=0**; database valid, schema v6.1.10 built `2026-11-24T06:22:05Z` |
| Runtime | Node major 24, UID/GID 65532, readonly FS, cap-drop ALL, no-new-privileges, local loopback, CPU/memory/PID limits PASS; health 200; Product API 503; forged proof 403; no CORS grant; SIGTERM exit0 in 0.507s. Seven synthetic local requests only |
| Auth/Publisher | **No real hosted invoker/IAM, Firebase, Firestore, KMS, app intent signer, remote publisher signature, SLSA or separately verified provenance** |
| Private evidence | WSL `/root/oldx-h1a-evidence-20261124T195244Z`, receipt SHA256 `9be77e292585d30aa859c50cf1bc5112c631c615c89697e4928604171283a560`, full SBOM SHA256 `09159b10490fe3ba072c0f53dadc49c428e8a4c1e0a940de1d939a8c4a2c235a`, Grype JSON SHA256 `2fbfc099009a6e1153f438e77f9724dff5e81884ba326953ae1a5fa2cdc0680a` |
| One-shot custody | BUILD marker `/root/.oldx-h1a-c2-mediator-once-20261125` is CONSUMED. Test container removed; local image + private reports RETAINED; never delete marker or repeat local image work |

**Provenance chain to require for H1B:** original Git-approved three file blobs → immutable base manifest pinned and independently raw-sha validated → BuildKit linux/amd64 result → reported local OCI index/child/config identities → Syft saved image config linkage → Grype saved SBOM receipt. This is **local build custody only**, not verified remote registry content or a supply-chain signature. An eventual separately approved `docker push` can yield a different OCI index or child digest; H1B must capture and verify the ACTUAL pushed immutable `linux/amd64` image manifest and inspect parent/config/layer/source linkage before referencing it in a Cloud Run revision. Never treat local image ID, local child manifest, config digest and future registry manifest as interchangeable.

## 2. All twelve distinct HIGH CVE findings — no blanket acceptance

Actual report severity: Critical **0 distinct CVEs / 0 matches**; High **12 distinct CVE IDs / 18 matches**; Medium **11 / 20**; Low **3 / 6**; Negligible **8 / 11**. Total **55 matches**, not 55 unique CVEs. Fix state below is **Grype saved output**, not independently adjudicated exploitation/patch/exposure; not-fixed/wont-fix statuses are **not** compensating controls.

| Family / actual installed version | Exact HIGH IDs | Report interpretation | Risk decision |
|---|---|---|---|
| gcc-14-base, libgcc-s1, libgomp1, libstdc++6 `14.2.0-19` | `CVE-2026-95619`, `CVE-2026-102010` | 8 package matches, `wont-fix`, `versions:[]` | **UNACCEPTED**; must assess actual runtime use/exposure and upstream distro disposition |
| libssl3t64 `3.5.9-1~deb13u1` | `CVE-2026-124709`, `CVE-2026-95692`, `CVE-2026-107496`, `CVE-2026-107494`, `CVE-2026-121482`, `CVE-2026-95691`, `CVE-2026-88823`, `CVE-2026-84786`, `CVE-2026-107493` | 9 package matches, `not-fixed`, `versions:[]` | **UNACCEPTED**; don't infer compiled-OFF Node has no SSL call path |
| libc6 `2.41-12+deb13u5` | `CVE-2026-84243` | 1 match, `wont-fix`, `versions:[]` | **UNACCEPTED**; call-path and available security updates not independently settled |

**External official tracker sample check (not an OLDX rescan, and NOT an exhaustive 12-CVE adjudication):** Debian 13/trixie source-package trackers reviewed 25 November 2026 show `CVE-2026-124709` on OpenSSL 3.5.9-1~deb13u1 vulnerable; `gcc-14` trixie `CVE-2026-95619`/`CVE-2026-102010` vulnerable; `glibc` trixie `CVE-2026-84243` vulnerable. Sources: https://security-tracker.debian.org/tracker/CVE-2026-124709 ; https://security-tracker.debian.org/tracker/source-package/gcc-14 ; https://security-tracker.debian.org/tracker/source-package/glibc . These tracker package entries do NOT establish exploitability of this exact OFF server image, and do NOT prove a working fix exists for this exact base. The other nine IDs require separate official status review if the owner considers security-risk acceptance.

**H1B residual-risk minimum:** identify each ID's affected call path or explain unknown; current official source status/fixed build; external reachability; relevant attack prerequisites; controls and remaining exposure under the exact private/off deployment; explicit time-boxed exception expiration, independent rollback and cleanup, named approver and evidence. Do NOT mark 12HIGH automatically accepted because prior C1A had 12HIGH or because H1A local health returned200. Original Step04/A8 15 severe and existing C1A 12HIGH concern different images; no fabricated `15+12+12` unique count.

## 3. Proposed H1B PRIVATE OFF-only experiment — still NO authorization

**Purpose only:** one NEW IAM-private, nonroot OFF-only staging mediator deployment to verify **infrastructure/image/identity isolation**, not C2 Product enablement or public website API. This is a *candidate* if the owner explicitly decides a short-lived residual-risk exception after package/call-path disposition. **There is no H1B GO now.**

Proposed bounded NEW-only resources, all existence and operator access currently UNKNOWN:
- Project `oldx-staging`, project number **38472235077**, region `asia-south1` (must be read back, not guessed from historic command context).
- NEW proposed service account `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, no generated downloadable keys, no project-wide data/auth/KMS roles. Verify new uniqueId and exact effective/inherited permissions before use.
- NEW proposed Cloud Run service `oldx-c2-website-mediator` with a new immutable **registry** image identity recorded only AFTER a separate authorized push. Collision status, service UID, revision, URL, principal, manifest and effective IAM currently **NOT VERIFIED**.
- Require IAM Invoker authentication, forbid `allUsers`/`allAuthenticatedUsers`, no public browser access, no staging domain routing, no Product traffic, no new IAM bindings to existing `oldx-step05-gateway`. Explicit owner Invoker if positive hosted probe is separately approved. Keep ingress minimally accessible subject to *actual* owner-to-service test path; never assume internal ingress is reachable from arbitrary laptop. No Firebase/Firestore/Auth/KMS/Admin SDK, no signing provider, no new backend data.
- Candidate min instances0/max1, 1 vCPU/512MiB, concurrency1, bounded 5s request timeouts, disabled default/OFF-only binary returning API503. Any environment flag claiming Product enabled is an error; H1 image has **no H2 enabled code**. No deployed enabled backend, no traffic migration or tag revision of existing resources.
- Suggested **time limit at most 24 hours**, zero synthetic Auth/Documents/media, and one short human-supervised verification window; separate explicit owner consent must set exact start/end, allowed GET/POST count, machine operator/principal, gross maximum costs across new Cloud Run, Artifact Registry/storage, request/logging/egress/network and tax/FX, retention and guarded CLEANUP deadline. **Metered cost is possible even with min instances0**; no ₹0 guarantee/free-tier assumption.
- Before ANY cloud write: fresh exact resource-collision reads with NOT_FOUND vs403/error distinguished, permissions/effective inherited/SA UID, protected service C1A and `oldx-owner-read` snapshots in the existing evidence, exact registry repository/tag/digest target, remaining CVE decision, provenance chain and rollback. No broad project IAM audit repeat, no billing form exercise, no previous C1A/B probes replay. If source/identity differs from frozen receipts: STOP.

**Protected existing resources:** `oldx-owner-read` and all old revisions/tags/traffic/IAM; existing C1A `oldx-step05-gateway` service UID `bf441d37-e39b-4afd-b4c8-0e6edee7269b`, OFF-only `/api/*=503`, existing runtime SA `oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com`, historic image/tag and Artifact Registry repository are not targets of this new-only proposal. **C1A retention expires 28 Nov 2026 at 23:19 IST; that approval does NOT automatically retain newly proposed H1B resources.** No timer or automatic cleanup is active.

**Guarded rollback/cleanup if later explicitly authorized:** record exact *NEW* service UID/revision/config/IAM before+after and SA uniqueId and NEW immutable registry digest before deployment. On anomaly STOP traffic/probes, prevent new invocation through independently approved means, rollback to the pre-H1B empty/new OFF state or safely disable the exact new revision/service only. Do not mutate old services/tags or delete the shared artifact repository, never sweep all tags/SA. Remove only exact NEW service, exact newly created SA, exact pushed image when no other digest/tag/subject references and freshly verified UID/dependencies match. Shared registry/old data stay. If any dependence/collision or UID mismatch: `STOP_MANUAL_RECOVERY`. Source-only packet does not execute or schedule cleanup.

## 4. Two owner decisions MUST remain separate

| Choice | Meaning | What it **does not** authorize |
|---|---|---|
| **A — HOLD (recommended default)** | Do not deploy this 12HIGH candidate; first finish official CVE/call-path disposition, publisher/provenance and exact future operator/cost scope, or evaluate a patched immutable replacement in a **new separately authorized** build cycle | No image rebuild/pull/scan automatically; no C1A extension; no H1B write |
| **B — BOUNDED PRIVATE OFF-only risk exception** | Owner explicitly accepts **exact 12 HIGH unresolved CVEs plus unverified remote signature/SLSA** for **only one newly named private default-OFF staging mediator** and a specified finite time window, with no data, zero public Invoker, IAM isolation, rollback and cost stop conditions | A **risk decision only**; still NO registry push/new SA/IAM/service creation until SECOND exact H1B operational authorization |
| **C — REVISE candidate** | Owner favors later rebuilt patched/source-reduced alternative under independent digest/status, image packaging and NEW security evidence | No repin, no Docker build or Grype repeat under consumed H1A approval; H1B stays HOLD |

**Recommended action at this source-only checkpoint:** choose **A/HOLD** while 12HIGH risk and actual publisher/provenance remain unresolved. It is legitimate to choose B only after deliberate, documented, **OFF-only** bounded risk acceptance, never as an implicit result of H1A PASS. The higher-risk H2 enabled/public Product path MUST undergo independent full risk disposition and fresh build/permissions before it can be considered, regardless of any H1B decision.

**Risk acceptance form, presently UNSIGNED / NOT ACCEPTED:** exact twelve IDs and three package families above; image identity local index `sha256:576a1faa...` (not registry digest); exposure `NEW_PRIVATE_OFF_ONLY_NO_DATA`; remaining risks `12HIGH + unpublished/unsigned derived image + inherited IAM unknown + metered cost`; proposed expiry within 24h of actual H1B activation; named owner/operation executor; collision+rollback+new-only cleanup guard; explicit approve/reject state. Leave all dates/UIDs/amounts as **UNVERIFIED** until separately resolved—never fabricate them.

## 5. G1–G6 and future handoff

- **G1:** new H1 image local PASS_WITH_LIMITS, not pushed/deployed, future host/SA/URL/guest quota not bound.
- **G2:** default-OFF metadata + KMS DI source contracts exist, but no live key/version or separately signed intent/website identity. No Cloud signer permission.
- **G3:** actual runtime `(default)` DB least-privilege identity and Firebase Auth revocation positive/negative not tested. H1B OFF-only would intentionally have no data permissions.
- **G4:** approved managed media/publication remains disabled (`publicationEnabled:false`); H1B cannot enable any Product.
- **G5:** numeric `expiresAtMs` is not Firestore Timestamp TTL; source-only one Product/photo cleanup draft not executable, shared nonce/rate rows remain unresolved.
- **G6:** H1A full-image scan12 HIGH + provenance/owner decision, private hosted rollback/cost unknown; H2 enabled scope risk not decided.

**ONE next owner action:** make an explicit **H1B CVE/provenance risk disposition**: `A = maintain HOLD and investigate/remediate`, `B = accept ONLY tightly bounded PRIVATE/OFF/no-data candidate risk as documented (no cloud write yet)`, or `C = authorize planning a different image candidate without executing a build`. Absent a recorded owner choice, **A/HOLD is the default**.

**No-repeat marker:** H1A build/Syft/Grype/runtime finished and consumed; existing C1A/B and Step04 receipts consumed. This packet created no Docker/registry/Cloud/Firebase/IAM actions, no test reruns, no scanner refresh, no cost. Future H1B physical provisioning needs **separate exact approval AFTER risk disposition**. Website/H2/Product/production remain HOLD.
