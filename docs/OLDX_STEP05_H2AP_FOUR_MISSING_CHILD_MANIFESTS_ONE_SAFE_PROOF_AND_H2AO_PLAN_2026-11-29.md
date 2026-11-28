# BAJUTO / OLDX Step05 — H2AP: four raw OCI child manifests absent from saved evidence; one source-only proof acquisition + H2AO continuation

**Date:** 29 November 2026 ~00:52 IST. **Repo:** `yasminparmar087-ops/oldx-website`. **Branch:** `security-hardening-review`.

## New actual OWNER read-only proof inventory (NOT a scan)

User WSL-root screenshot of ONE existing-filesystem-only scan over `/root/oldx-h2a{i,j,k,l,m,n,o}*` evidence directories (the exact prefixes included ai/aj/ak/an/am/ao and perhaps others). No Docker/Grype/network/registry/Cloud or file writes.

```text
=== H2AO READ-ONLY MANIFEST INVENTORY ===
H2AO_MARKER= NOT_CONSUMED
MEDIATOR=NOT_FOUND_IN_SEARCH_SCOPE
GATEWAY=NOT_FOUND_IN_SEARCH_SCOPE
BACKEND=NOT_FOUND_IN_SEARCH_SCOPE
READER=NOT_FOUND_IN_SEARCH_SCOPE
FILES_CHECKED= 188
READ_ONLY=COMPLETE_NO_SCAN_NO_NETWORK_NO_WRITES
```

**Important caveat:** This means none of the **188 eligible files in the bounded searched evidence folders** matched the SHA256 of an original exact raw child manifest. It does **not** prove no other copy exists in the whole filesystem, nor that any private registry image is missing. Previously owner ACTUALLY built/pushed all four immutable private child image refs (H2AJ PASS); preloaded verified four local Docker image refs (H2AN PASS); H2AK complete historic Mediator Grype report 57 findings / 18 HIGH / 0 Critical; H2AM marker consumed and stopped **before runtime or any new scan** at a mistaken Docker containerd manifest-vs-Grype config ID equality, since corrected SOURCE-ONLY in H2AO (26 new distinct offline PASS evidence). No old artifacts or markers may be reset or replayed.

Immutable H2AO source-only commit **`92a4529d3fe4de641898f9195634dfd2e9b8144e`** (verified branch HEAD when checked). H2AO identity verifier blob `b7f7eb42ba4a72fb6959ca06e52cff55b3b30ae5`, selective runner blob `5db17708caad89f0c49502eb343c71f3120b1260`. H2AO requires **ALL** existing raw role child manifests in a private `--manifest-directory` named `mediator-child-manifest.json`, `gateway-child-manifest.json`, `backend-child-manifest.json`, `reader-child-manifest.json`; it contains an OPTIONAL read-only GET helper for **Mediator only**, and explicitly STOPs for absent other three proofs before its preflight/runtime markers. DO NOT run it now.

**Exactly pinned immutable Linux/AMD64 CHILD manifest refs:**

| Role | Private artifact | Child manifest digest |
| --- | --- | --- |
| Mediator | `oldx-c2-mediator-h2ah` | `sha256:01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe` |
| Gateway | `oldx-c2-gateway-h2ah` | `sha256:921fbf4ff71b918c479e4a786868368640a494c16da08e54192f25e14dc1ec4d` |
| Backend | `oldx-c2-backend-h2ah` | `sha256:01ae540aa88ad0e3a6888994dd41b6b02b9d934a7a1d2e455f44b194f033b941` |
| KMS Reader | `oldx-c2-kms-reader` | `sha256:822e2592b1010bfa94a1fe5bc75003712485abae0369f5252ece3863723eb077` |

Project `oldx-staging`, region `asia-south1`, registry host `asia-south1-docker.pkg.dev`, repository `oldx-staging-images`. Exact containerd-vs-Grype ID issue: local Docker `.Id` may be the child digest while Grype historic `imageID` is config digest `sha256:44c8657a5aad46d7aa1192e73af0a338200c61720f47b0ebe8d19faa3613f1e2`. Historic Grype config raw base64 decoded bytes SHA256 matches Grype config ID, BUT child manifest `config.digest` still NOT checked. Absolutely no bypass of binding allowed.

## NEXT, ONE CONSOLIDATED H2AP CODEX SOURCE-ONLY TASK (NO Cloud/Docker action)

Implement complete new **H2AP proof acquisition and safe H2AO handoff**, not merely docs. Prefer the simplest *new* source-only one-shot wrapper or a narrowly reviewed new role-aware helper; **do NOT edit old consumed H2AM/H2AN/H2AJ/H2AK scripts/markers or rebuild images**.

1. Read `AGENTS.md`, current Handoff, this actual screenshot checkpoint, `docs/OLDX_STEP05_H2AO_OCI_IDENTITY_SOURCE_RECEIPT_2026-11-29.md`, original H2AO identity/runner, frozen image proposal and actual prior H2AN/H2AM/H2AK receipts. Maintain exact approved code/source pins. Before implementation explicitly distinguish local evidence not found versus registry absent. No further broad directory sweeps or old CI/tests/scans.
2. Implement a **new default-OFF H2AP manifest-acquisition runner** that accepts a separate exact future Owner approval flag. It first verifies OWNER native WSL root, frozen `oldx-staging` project/account, existing H2AJ success and consumed H2AN/H2AM markers + their exact prior evidence, no H2AO marker, 4 exact SHA-pinned refs, Grype historic report SHA and non-sensitive native tool requirements, 4 existing local Docker refs when read-only inspect is useful. A private clean output dir must be root-owned 0700 and proof files 0600.
3. Before any new H2AP marker, obtain a **short-lived Owner OAuth credential safely** from the already-installed native isolated gcloud SDK ONLY if separately approved at execution; do not print or write its value, put it in argv or environment, persist it in Docker config, or modify account/SDK/IAM. A token in temporary process memory is acceptable. Validate native account/project from read-only local config and reject wrong account/project. No elevated IAM or service-account key.
4. **At most one pinned authenticated HTTPS GET for EACH of these exact four child digests**, no mutable tags, HEAD, image pulls, scans, new builds or pushes. Fixed `https://asia-south1-docker.pkg.dev/v2/oldx-staging/oldx-staging-images/<fixed-role-name>/manifests/sha256:<frozen-child>` endpoints ONLY. One exclusive new H2AP attempt marker **before the first request**, with per-role durable ATTEMPTED/COMPLETE/FAIL receipts; separate exact tokenless per-role audit fields. No automatic retry after a request starts, no redirects, no proxies/insecure TLS, bounded deadlines and max 512 KiB raw response per role. Require HTTP 200, exact accepted Docker/OCI media type, identity content-encoding, expected or missing matching `Docker-Content-Digest` header.
5. Hash the **unaltered raw bytes**, SHA256 == frozen child manifest digest (not JSON reserialized), and pass the existing H2AO `manifest_config(raw, exact_ref)` verifier: OCI/Docker schema-2 **child** only, no index, valid config descriptor and layers. File is privately persisted with exact filename `<role>-child-manifest.json` and file SHA, fsync, before being marked COMPLETE. If any GET/auth/TLS/header/hash/config fails, STOP permanently for this one-shot, preserve successful prior proof files/attempt logs and DO NOT start H2AO. Do not delete a partial or run another HTTP request after failure. Never invent missing bytes or downgrade verification. Any need for another scope after ambiguity needs separate explicit Owner approval.
6. For Mediator, require `config.digest == sha256:44c8657a5aad46d7aa1192e73af0a338200c61720f47b0ebe8d19faa3613f1e2` and config.size == actual decoded historical Grype config byte length (32372), with immutable historic raw report SHA `e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92`. If mismatch STOP before any H2AO marker. Additional role scan config binding is performed by H2AO when scanning each role.
7. Only after all four proofs are complete, independently rehash them and verify exact frozen H2AO source files (runner blob `5db17708caad89f0c49502eb343c71f3120b1260`, identity `b7f7eb42ba4a72fb6959ca06e52cff55b3b30ae5`, immutable H2AM helpers `b9b57daa9a5b5f0304afc9cfc758630793454c07` and `3adfb06ca66d6175f089ea797df21ca767779cca`, frozen proposal `c1cfcfa2f224e9a47dd6e896730c73e927b9b483`). Download them read-only to a fresh isolated source tree if necessary. No silent source drift, global config mutation, or copies of Grype/credentials. Hand off to the **unchanged, already-tested H2AO one-shot runner** with `--manifest-directory <private-proof-dir> --execute-h2ao-once --owner-approved-selective-off-only` and WITHOUT any `--allow-one-mediator-manifest-get` or token-FD argument: all four proofs already exist.
8. H2AO's existing strict gates must determine whether its own preflight or runtime marker can be consumed. If proof mismatch or identity uncertainty, it MUST stop before runtime marker. If all PASS, only one Mediator OFF runtime (NEVER re-run 57-finding Grype scan), then only after its PASS one new Grype scan+OFF runtime each Gateway/Backend/Reader; no automatic retry, no premature PASS/GO. All new H2AP/H2AO markers durable and never reset. Private receipts include exact safe progress so one future chat can avoid re-running complete stages. No global IAM/KMS/Firebase/Cloud Run/production changes; only 4 authenticated Artifact Registry **read** requests and separately-approved local runtime and three new scans.
9. Create **new focused OFFLINE tests only** for mocked token retrieval+no leakage, fixed four URLs/one GET each, every partial failure STOP/no retry, false media type/redirect/TLS/401/body oversize/hash/manifest malformed/config mismatch, marker consumed boundaries, private file permissions, retention after failures, all 4 proof PASS before H2AO call, H2AO-only-once call under separate approval and no mediator Grype rerun. No actual new registry calls or Docker/scans during tests. Do NOT rerun previous 26 H2AO/19 H2AM or old CI.
10. Commit/push new source/tests/receipt, update `AGENTS.md` newest handoff and `docs/OLDX_CURRENT_HANDOFF.md`, add Issue #17 comment. Return verified SHA, new focused tests, exact future **ONE Owner approval packet** and ONE hash-verified WSL-root command to be supplied **only after that approval**. Do not consume any marker now.

## Current owner permission boundary (NOT yet approved)

User has NOT approved these four new authenticated manifest GETs. Earlier permission was for exact local H2AN three image pulls and old H2AM selective execution only; both consumed. H2AO future execution was proposed but not approved, and its optional single Mediator GET did not authorize other three. This H2AP document authorizes **source-only work**, not any network/Cloud action. Ask separately for ONE combined approval after source/NEW offline tests pass.

**Strict status:** H2AJ all four new private registry image PASS; H2AN three missing local pulls PASS and four local images VERIFIED; H2AK Mediator scan COMPLETE 57 matches /18 HIGH /0 Critical, do not rescan; H2AM consumed at Mediator image-ID binding with NO current-runtime or other three scans. H2AO source-only 26 distinct new offline PASS; H2AO marker NOT CONSUMED. H2AP source-only task NOW, no new live GET/scan/runtime, security HOLD, production NO-GO, Step05 ACTIVE.
