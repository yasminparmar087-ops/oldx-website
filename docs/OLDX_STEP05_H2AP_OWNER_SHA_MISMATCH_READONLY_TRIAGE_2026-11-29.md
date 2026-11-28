# BAJUTO Step05 H2AP — owner read-only screenshot: summary hash mismatch; stage UNKNOWN

29 November 2026 ~01:33 IST. Evidence source: owner-provided Windows CMD/WSL-root screenshot following Task29's read-only summary inspector. This note documents *observed output*, not a verified local filesystem inspection by the assistant.

Prior source-only H2AP receipt: `docs/OLDX_STEP05_H2AP_FOUR_PROOF_SOURCE_RECEIPT_2026-11-29.md`. Prior owner run checkpoint: `docs/OLDX_STEP05_H2AP_OWNER_ACTUAL_SUMMARY_WRITTEN_RESULT_NOT_YET_READ_2026-11-29.md`. Immutable H2AP script source commit `1b643487824739290839124269195c32fa7c850d`, wrapper Git blob `cfbb37d59603dd6cab1abe44a266380f4df00aa6`. Review-branch HEAD before this note: `ec16ef9f3a18e1018fe2fb2450d4bb6491633b8e`.

## Screenshot-only observed output

- Private evidence directory: `/root/oldx-h2ap-proofs-20261128T195645Z-9b92c299`
- Previously printed expected summary SHA256: `b3993a77c66ce016f83ee5c574fe2688957603a318f2973ee10785ecc0f52859`
- Owner read-only inspection: `SUMMARY_SHA256_MATCH= False`; `H2AP_MARKER= NOT_FOUND`; `H2AO_MARKER= NOT_FOUND`; `READ_ONLY=COMPLETE_NO_NETWORK_NO_SCANS_NO_WRITES`
- Last inspector only printed outcome/role/handoff fields when checksum matched, so **actual outcome, failureCode, current summary checksum and role statuses remain UNKNOWN**. Neither current summary contents nor absence of two markers proves no prior requests or authorizes replay.

## Source-level interpretation and next move

Original H2AP source puts the H2AP marker in `/root/.oldx-step05-h2ap-four-child-manifests-and-h2ao-once-20261129` **after** frozen-source, native environment, old receipts, tool, disk and cached-token preflight; failures before this point can write `summary.json` without an H2AP marker. This is a plausible explanation, not verified cause. Original source prints summary SHA in its `finally` block, so the apparent mismatch between the earlier printed SHA and later read requires a bounded read-only reconciliation before relying on the summary. No assumptions of tampering or automatic refresh.

**Next only:** ONE read-only, no-network WSL inspection of the exact private summary file: verify lstat/owner/type/mode/size, print computed actual SHA256 and compare expected, parse only allowlisted `outcome`, `failureCode`, `handoff.status`, `roles[*].status/httpStatus/failureCode`, and check presence of all five exact H2AP/H2AO attempt/preflight/global markers plus four proof files. No raw manifest bodies, tokens, SDK credential files or unfiltered logs printed. If file inaccessible/unsafe/malformed, STOP with UNKNOWN; don't reset/replay old action.

**Hard NO-REPEAT:** no rerun of H2AP/H2AO/H2AM/H2AN/H2AJ/H2AK; no token refresh/login; no registry GET, Grype/Docker scan/runtime, builds/pulls, Cloud changes, IAM, KMS, Firebase, production. Preserve original receipts and all markers. H2AP/H2AO actual PASS UNKNOWN; Step05 ACTIVE, security/hosted HOLD, production OFF/NO-GO. Need owner-side result to determine the smallest next distinct action.
