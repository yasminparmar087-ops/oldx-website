# OLDX Step05 — LATEST one-free-local-image-evidence handoff (24 Nov 2026)

**OWNER APPROVAL (ACTUAL):** "ha manjuri chhe" in direct response to "one limited, cost-free NEW OFF-only Gateway image build, SBOM/security scan and Linux Node24 smoke, with NO cloud deployment, Registry upload, IAM change or paid resource." C1A deploy, C1B hosted requests and C2 enabled use are **NOT approved**.

**Previously verified remote HEAD:** `e74082d7a216550a54cebfc61ead8ea931966459`; last 84 DISTINCT focused synthetic/offline PASS receipts remain historical. Neither 84 cases nor old A8 image builds/scans/Cloud/Vercel/IAM investigations were rerun.

**Actual work THIS turn:** Created and updated source-only `scripts/step05-gateway-off-local-one-shot.sh` on `security-hardening-review`, with pinned Git blobs of ONLY the new Gateway OFF-server/Dockerfile/deny-all Docker context. The script performs a single local Docker Linux/AMD64 Node24 nonroot readonly network-none build/smoke, one SHA256-verified official Syft1.57.1 CycloneDX SBOM, and one SHA256-verified official Grype0.121.3 vulnerability scan, computing distinct HIGH/CRITICAL IDs. No automatic retries, source drift or duplicate build; a HOME one-shot marker is set only after preflight and before local build; exact new local container/image and binaries are cleaned up, small reports retained.

**Blocked runtime:** assistant container has no Docker, Podman, Buildah, daemon or gcr.io DNS. No actual new image was built. Bash syntax of a corresponding locally authored draft PASSED; the GitHub script itself was not executed in Linux/Docker here. Do not claim SBOM/Grype/Linux Node24 smoke passed. GitHub public standard runners would be free but adding a push-triggered workflow would automatically repeat old unconditional Safety CI; deliberately NOT done. No GitHub CI or cloud service was invoked.

**One owner Cloud Shell action, only if existing FREE Cloud Shell has Docker and >=4GiB scratch (script checks both):**
```bash
d=$(mktemp -d /tmp/oldx-step05-build.XXXXXX) && git clone --quiet --depth 1 --single-branch --branch security-hardening-review https://github.com/yasminparmar087-ops/oldx-website.git "$d" && cd "$d" && bash scripts/step05-gateway-off-local-one-shot.sh
```

Share only the final `summary.txt` and, if failed, one concise STOP reason. Do not repeat an attempted build after a failure without an explicit scoped decision; do not reveal tokens or upload raw secrets.

**Technical note:** `docs/OLDX_CURRENT_HANDOFF.md` has grown beyond GitHub Contents API's supported content retrieval size and is returned empty by the connector in this turn. It was **NOT overwritten or truncated**. This small checkpoint is the authoritative newer pointer, linked from Step05's single master-plan row and the canonical [C1A owner manifest](OLDX_STEP05_OWNER_SELECTED_OPTION_C_C0_AND_MINIMAL_C1A_MANIFEST_2026-11-24.md).

**Security/launch HOLD:** new image local build/SBOM/scan/Node24 execution UNVERIFIED; even if passed, publisher signature, exact derived image immutable registry digest, C1A operator/tester/ingress and finite INR cost/cleanup, effective IAM, Step04 enabled 15 CVEs and media remain unresolved. `OPTION_C=C0_OWNER_SELECTED`, `STEP05_LOCAL_IMAGE_EVIDENCE=OWNER_APPROVED_ONE_ATTEMPT_NOT_RUN`, `STEP05_HOSTED=BLOCKED`, `STEP05=NOT_DONE`, `PRODUCTION=NO_GO`.


## 24 Nov 2026 — Owner Cloud Shell first one-shot ATTEMPT PARTIAL PASS, STOP at Syft SBOM

**This replaces the earlier “NOT RUN” state for the exact one-shot build.** Owner provided Cloud Shell screenshot for the already-approved local script. Exact transcript visible:

- `HEAD=10a486e27a75fa79d0c90fbea7c7017cfb15a020` (the previous review-branch source checkpoint).
- `EVIDENCE=/home/yasminparmar087/oldx-step05-gateway-evidence-20261124T111007Z`.
- `LINUX_NODE24_NONROOT_READONLY=PASS`.
- `OFF_ONLY_LINUX_CONTAINER=PASS`.
- `LINUX_SIGTERM_EXIT=PASS`.
- SHA256 of the downloaded `syft_1.57.1_linux_amd64.tar.gz` reported `OK`.
- Final line: `STOP: New image SBOM failed`, shell returned to prompt.

**Evidence interpretation:** A NEW derived Gateway image WAS locally built (necessary for those real container smoke checks), Linux Node24/nonroot/read-only, disabled API/health and Linux SIGTERM checks passed. The image was NOT uploaded or deployed. Syft extraction and SBOM operation were reached but the scan command returned nonzero; screenshot alone does NOT establish why (source mismatch, image deleted before scan, Syft error, timeout, disk, etc. not yet diagnosed). **No valid SBOM or Grype CVE scan PASS**; Grype was not reached. Script trap cleans only its new temporary container/image and scan scratch and retains the evidence directory; the one-time marker is consumed. Do **NOT** rerun the build or any old 84 offline tests / Step04 A8 scans under this spent approval. A new build needs a distinct scoped decision. New test-case count unchanged at 84; Linux container smoke results are reported separately, not automatically added to historical Node offline totals.

**Next action: read-only evidence inspection, no repeated build/scan** from existing Cloud Shell (exact known evidence path):

```bash
OUT="$HOME/oldx-step05-gateway-evidence-20261124T111007Z"
printf '\n=== SUMMARY ===\n'; cat "$OUT/summary.txt"
printf '\n=== FILES ===\n'; ls -lh "$OUT"
printf '\n=== SBOM BYTES ===\n'; wc -c "$OUT/sbom.cdx.json" 2>/dev/null || true
printf '\n=== BUILD ERRORS (IF ANY) ===\n'; grep -Ei 'error|fail|warning' "$OUT/build.log" | tail -n 12 || true
```

Inspect output before any new action or download. Note that the original Syft stderr was not explicitly redirected to a retained log in the one-shot script, so the exact exit reason might be unavailable; do not infer it. Preserve `summary.txt`, `node24-runtime.txt`, `off-scenario.txt`, `shutdown.txt`, `build.log` and any partial SBOM without exposing credentials. **Next consent scope:** if evidence cannot resolve failure, propose a minimal scan-only recovery or distinct one-time new build based on whether an immutable locally accessible image remains. No Cloud Build, Registry push or deploy automatically.

**Status:** `C1A_LOCAL_NEW_IMAGE_BUILD=PASS_WITH_LIMITS`; `LINUX_NODE24_OFF_SMOKE=PASS`; `SYFT_SBOM=FAILED`; `GRYPE_NOT_RUN`; `C1A_IMAGE_SECURITY=BLOCKED`; `STEP05_HOSTED=BLOCKED`; `PRODUCTION=NO_GO`.
