# BAJUTO / OLDX Step05 — H2AK PREWRITE STOP: missing native Linux Grype; verified release install and resume
Date: 28 November 2026, ~21:29 IST; user WSL-root screenshot. Branch security-hardening-review.

## Exact screenshot evidence

After the previous *prewrite* marker-prefix bug was fixed in `scripts/step05_h2ak_four_pinned_new_images_scan_offhealth_once_20261128.py` and the runner verified its immutable source hash, the user's second execution printed:

```text
H2AK_RESULT=STOP_BEFORE_IMAGE_READ
H2AK_REASON=MISSING_LINUX_GRYPE
```

This confirms the earlier H2AJ marker false-negative was resolved; the H2AK preflight got as far as the missing native `grype` binary check. **No H2AK one-time marker was consumed**. No image pull, Grype scan or local container was started; no Cloud/IAM/KMS/Firestore/deploy or image build/push was requested. Previous H2AJ FOUR new private image pushes remain ACTUAL PASS. Do NOT repeat H2AJ, H2AI, H2AG or old tests.

## Verified official Grype release source

Official Anchore GitHub release `v0.122.1`, released 2026-11-18 14:14 UTC:
- `https://github.com/anchore/grype/releases/download/v0.122.1/grype_0.122.1_linux_amd64.tar.gz`
- **Published GitHub release asset SHA256:** `f1ba7e2917ee1395618de20a98da0aa7c0fb1788927797651047c50502a37538`.
- Authoritative GitHub API `https://api.github.com/repos/anchore/grype/releases/tags/v0.122.1` returned identical filename and `digest:sha256:f1ba7e29...`. Checksums are not equivalent to verifying the Sigstore attestation; do not claim signature verified.

Local-only install into `/root/oldx-tools/grype-v0.122.1`, SHA256 before extraction, inject that path into the current execution shell. No global `apt`, `sudo`, Windows Node/SDK or Cloud changes. Keep installed binary for later security audits; no need to reinstall it again.

## ONE WSL root command — native verified Linux Grype then corrected unchanged H2AK

```bash
(
set -euo pipefail
test -f /root/.oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128
test ! -e /root/.oldx-step05-h2ak-four-pinned-image-acceptance-once-20261128
GRYPE_DIR=/root/oldx-tools/grype-v0.122.1
if [ ! -x "$GRYPE_DIR/grype" ]; then
  tmp=$(mktemp -d /root/oldx-grype-install.XXXXXXXX)
  curl --fail --location --silent --show-error --retry 0 --max-time 180 --output "$tmp/grype.tar.gz" 'https://github.com/anchore/grype/releases/download/v0.122.1/grype_0.122.1_linux_amd64.tar.gz'
  printf '%s  %s\n' 'f1ba7e2917ee1395618de20a98da0aa7c0fb1788927797651047c50502a37538' "$tmp/grype.tar.gz" | sha256sum --check -
  mkdir -p "$GRYPE_DIR"
  tar -xzf "$tmp/grype.tar.gz" -C "$GRYPE_DIR" grype
  chmod 0755 "$GRYPE_DIR/grype"
fi
export PATH="$GRYPE_DIR:$PATH"
test -x "$GRYPE_DIR/grype"
"$GRYPE_DIR/grype" version
d=$(mktemp -d /root/oldx-h2ak-grype-ready.XXXXXXXX)
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ak.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/809197dc24e5aa389106dea715fa82fa6ffbb549/scripts/step05_h2ak_four_pinned_new_images_scan_offhealth_once_20261128.py'
test "$(git hash-object "$d/h2ak.py")" = 'f9b6f2f15cd1c5a59405d33f09e158434b7c2773'
python3 -B "$d/h2ak.py" --h2ak-four-h2aj-images-scan-offhealth-local-only-once
)
```

This command will use the **same exact H2AK source that just STOPped before marker**, not rerun prior Node/Grype scans. Scanner setup is local-only and not a Cloud write. The previously approved H2AK only pulls four exact digest-pinned private new images read-only, scans once per image and checks nonroot/default-OFF HTTP inside `docker run --network none`. If `H2AK_MARKER=CONSUMED_NO_REPEAT` is printed, do not rerun under any circumstance; collect exact output/receipt. If Grype installation or binary verification fails, that occurs before H2AK marker or any scan.

## Strict current truth

`H2AJ=FOUR_PRIVATE_IMAGES_ACTUAL_PASS`; `H2AK=PREWRITE_STOP_MISSING_LINUX_GRYPE`; `H2AK_MARKER=NOT_CONSUMED_AS_SCREENSHOT`; `GRYPE_INSTALL=PROPOSED_NOT_YET_EXECUTED`; `FOUR_NEW_IMAGE_SCANS=NOT_YET_STARTED`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
