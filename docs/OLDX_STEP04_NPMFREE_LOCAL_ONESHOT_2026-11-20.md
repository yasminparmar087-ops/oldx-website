# OLDX Step 04 — one NEW npm-free local image assessment (prepared, never executed)

**State:** Source-only runner prepared on 20 Nov 2026. `G2 HOLD`; existing scanned image remains CRITICAL 1/HIGH 8. This is **not** authorization or a claim that the image was rebuilt, scanned or published.

## Exact boundaries

- Build **one new** BellSoft npm-free OLDX image from clean, pinned source commit `fcc96574b6388dc441a0b5d3eade48e79c7ebb24` on **owner's local Windows D:-backed WSL Linux Docker**, never hosted Cloud Shell, Vercel or production.
- Entrypoint `scripts/step04-npmfree-local-one-shot-a1.py`, anchored GitHub commit `f46eba4a3c19ac3f6870b7974fdda59b96c7dd9a`, blob SHA1 `5ce4b93f5f906f4a475a328fd0a51383df62cfc1`. Do **not** download an unpinned branch/latest script.
- It checks clean source, repo ownership, exact Git blob identities, immutable publisher-signed BellSoft glibc-r14 base, platform, local unix-socket Docker context, 12 GiB free D:, previously imported **unchanged offline Grype** 0.121.3 DB SHA256 `303ba44739343769e0e15bd0d50af62e142491b256bb533a8cfaf13ab00ca1b7`, and absence of prior one-shot attempt.
- `--preflight` only reads local metadata and emits `NPMFREE_PREFLIGHT=PASS` or `STOP_PREFLIGHT=...`. It creates no evidence, image or container. `--execute` performs **one** local build with cache allowed but no registry push; one nonroot, no-network/read-only Node/Sharp/Firebase/health 200/default-OFF 503/SIGTERM check; **one** new-image unfiltered Grype scan using existing offline DB. The old image, old scan, B1/R1/R2, G4 and CI are never rerun.
- Journal created **before build** at `D:\OLDX\G2\oldx-bellsoft-npmfree-20261120-a1\summary.json`; the directory's presence blocks another attempt, even after failure. New full Grype report and build log are private on owner's D:. Never upload raw private report, tokens or cloud credentials. No remote/cloud writes, IAM, Rules, service traffic, DNS, deployment or billing changes.
- Build uses `--platform linux/amd64 --pull=false` with public pinned bases. Docker may fetch missing public layers or npm tarballs during the **single local build**; there is no guarantee of strictly offline construction, but the scan database is offline. No implicit cloud-billing charges from this local operation, though owner's network/data/storage usage applies.
- **STOP does not mean retry:** leave the image and receipt alone for review. All vulnerability findings remain open unless the **new image-specific** full report and runtime evidence support a narrowed disposition. OCI whiteout does not erase original inherited base-layer bytes, and npm-free does not fix glibc/G4/G8/provenance.

## One-time setup and read-only preflight (inside owner's WSL terminal, not Windows CMD or hosted Cloud Shell)

```bash
set -e
SRC=/mnt/d/OLDX/G2/oldx-npmfree-source-a1
RUNNER=/mnt/d/OLDX/G2/oldx-npmfree-runner-a1.py
test ! -e "$SRC" && test ! -e "$RUNNER"
git clone -q --branch security-hardening-review --single-branch https://github.com/yasminparmar087-ops/oldx-website.git "$SRC"
git -C "$SRC" checkout --detach fcc96574b6388dc441a0b5d3eade48e79c7ebb24
curl --fail --location --silent --show-error --output "$RUNNER" https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/f46eba4a3c19ac3f6870b7974fdda59b96c7dd9a/scripts/step04-npmfree-local-one-shot-a1.py
test "$(git hash-object "$RUNNER")" = 5ce4b93f5f906f4a475a328fd0a51383df62cfc1
python3 "$RUNNER" --preflight --source "$SRC"
```

Only after `NPMFREE_PREFLIGHT=PASS` and exact bounded owner execution decision, use the same pinned local file (no re-clone or re-download):

```bash
python3 /mnt/d/OLDX/G2/oldx-npmfree-runner-a1.py --execute --source /mnt/d/OLDX/G2/oldx-npmfree-source-a1
```

Provide only the concise terminal status and sanitized `summary.json` outputs for review. **Do not repeat any old proof.** A failed preflight may be investigated read-only, but a started build/scan must not be blindly rerun.
