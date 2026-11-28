# BAJUTO Step05 H2AP STOP — confirmed invalid 66-hex H2AO frozen H2AM-summary pin; source-only H2AQ continuation

**2026-11-29 ~01:40 IST, owner WSL root actual screenshot.** Branch `security-hardening-review`. This is a **source transcription error**, NOT evidence of an H2AM receipt mutation. Do not re-run consumed attempts or delete old receipts/markers.

## Screenshot-grounded facts

The exact H2AM private summary `/root/oldx-h2am-selective-20261128T183527Z-2ae92ca2/summary.json` is reported as:

- `H2AM_ACTUAL_SHA256=99a455c5bedd435c0f72b0c9aadcb96d8949db9cb1d2bff518416ca1b18e958f` (**64 hex digits**).
- `H2AM_SIZE=443`, `H2AM_MTIME_UTC=2026-11-28T18:35:29.133144+00:00`, `H2AM_EXPECTED_MATCH=False` against the copied incorrect 66-character expectation.
- `H2AM_OUTCOME=STOP_PARTIAL_NO_AUTOMATIC_RETRY`, `H2AM_FAILURE=MEDIATOR_HISTORIC_LOCAL_CONFIG_MISMATCH`, `MEDIATOR_STAGE=IMAGE_BINDING`; Gateway/Backend/Reader `NOT_ATTEMPTED`.
- `H2AM_MARKER_PRESENT=True`: H2AM permanently consumed, must NEVER rerun or reset.
- Previous owner screenshot of exact H2AP summary: `OUTCOME=STOP_NO_AUTOMATIC_RETRY`, `FAILURE_CODE=PRIOR_H2AM_SUMMARY_SHA_DRIFT`, `H2AO_HANDOFF=NOT_ATTEMPTED`, four roles `NOT_ATTEMPTED`, zero proofs present, all five H2AP/H2AO/new preflight/GET/global markers `NOT_FOUND`. No fresh registry GET/runtime/scan observed.

## Root cause independently verified against immutable GitHub source

Immutable H2AO source `scripts/step05_h2ao_selective_continuation_once_20261129.py` at commit `92a4529d3fe4de641898f9195634dfd2e9b8144e` contains:

```python
# INCORRECT (66 hex digits; impossible SHA256)
AM_SUMMARY_SHA="99a455c5bedd435c0f72b0c9aacadcb96d8949db9cb1d2bff518416ca1b18e958f"
# CORRECT (64 hex digits; matches owner actual file)
AM_SUMMARY_SHA="99a455c5bedd435c0f72b0c9aadcb96d8949db9cb1d2bff518416ca1b18e958f"
```

Exact difference is extra `ca` in `...c9aacadcb...` versus `...c9aadcb...`. A GitHub connector read confirmed frozen length=66 and owner visible actual=64; replacing that single erroneous substring yields the owner actual checksum. H2AO `history()` does `fail(sha256(summary_raw)==AM_SUMMARY_SHA, "PRIOR_H2AM_SUMMARY_SHA_DRIFT")`; as written it **can never pass** for any SHA256 since its constant has length66. H2AP invokes H2AO history **before** its four-manifest request marker or token retrieval. This explains the actual prewrite STOP.

The old H2AM receipt is semantically consistent with its historical actual checkpoint and frozen H2AM SHA in `docs/OLDX_STEP05_H2AN_OWNER_THREE_PRELOADS_PASS_H2AM_PARTIAL_READONLY_TRIAGE_2026-11-29.md`. This is not independent proof of every old ledger byte; all other H2AO history/identity checks remain mandatory in a corrected path.

## Scope of next SOURCE-ONLY task (one consolidated Codex prompt)

Continue fast on `yasminparmar087-ops/oldx-website`, `security-hardening-review` ONLY. Read `AGENTS.md`, the first current Handoff sections, this source-fault receipt, prior H2AP/H2AO source receipts, and exact original frozen source; do not redo previous tests/CI/builds/Grype/cloud. Reuse existing tested modules.

1. Create an ADDITIVE fresh **H2AQ** correction path, not a replay or mutation of consumed old H2AM/H2AN/H2AJ/H2AK or original frozen H2AO/H2AP. Fix only the invalid 66-digit `AM_SUMMARY_SHA` to the exact 64-digit old owner checksum in a separately versioned H2AO runner. Keep strict schema/marker/identity/history/OCI/nonroot/signed-scans/bounds/replay protection; never bypass digest checks to force PASS. Preserve all unrelated fixed original source and immutable pins.
2. Introduce an H2AQ wrapper which uses the exact newly Git-blob-pinned corrected runner and other unchanged H2AO dependencies, verifies their hashes in an immutable source commit, provides fresh H2AQ-exclusive attempt/evidence markers and checks **both original and new marker/ledger namespaces** to prevent replay. It must NOT invoke old H2AP/H2AO entrypoints or old scans. Old H2AP pre-marker failed evidence remains untouched; new step requires **new action-specific owner consent** before its first registry GET or local runtime. Secure cached-token helper is reused unchanged. No refresh/login or SDK credential-store mutation; no token argv/env/disk/log. Default OFF. Frozen original H2AP/H2AO sources must remain intact. Prefer a concise new wrapper instead of broad refactor.
3. Add focused NEW offline mock cases for: exact64-byte historical SHA pin versus impossible66-byte pin, old receipt semantic verification, old and new consumed-marker STOP, fresh H2AQ default-OFF, four-proof SHA/OCI/descriptor preservation, Mediator report reuse/no scan, unconditional STOP on auth/manifest/identity failure and only ONE H2AO handoff once all four proofs pass. No old 21/26/19 or broader CI repeat. Test exact new executable code and report errors honestly.
4. **DO NOT execute** external registry GETs, Docker containers, Grype scanners, OAuth SDK, gcloud, Cloud Run, IAM, Firebase, KMS, billing or production. No new owner terminal commands until source is reviewed/tested. Update `AGENTS.md`, current Handoff, new receipt and Issue #17 with short exact HEAD/tests/remaining gates. Preserve owner dirty local `Handoff`/`.firebaserc` if encountered, no reset/force push.
5. Return one exact owner approval packet and ONE hash/Git-blob-verified WSL-root command only for **future separately approved execution**, using a new consumed-once marker. On unknown old receipt/marker/identity or missing token, STOP, never auto-retry. Keep Step05 ACTIVE, G2/G4/G8/hosted/security HOLD, production OFF/NO-GO. No unverified CVE/security PASS claims.

No source fix is yet implemented by this checkpoint; this is diagnostic evidence plus a safe next engineering scope. **No old marker/receipt should be edited even to “fix a hash”.**
