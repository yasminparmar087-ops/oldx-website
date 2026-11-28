# BAJUTO / OLDX Step05 — H2AM actual Docker-containerd vs Grype image identity error; H2AO new source-only repair, do not repeat attempts

Date: 2026-11-29 ~00:14 IST. Repo `yasminparmar087-ops/oldx-website`, **ONLY** branch `security-hardening-review`. Owner WSL-root screenshot; no new scan/cloud/Docker mutation in the identity audit.

## EXACT OWNER READ-ONLY EVIDENCE, most current

```text
OLD_GRYPE_IMAGE_ID=sha256:44c8657a5aad46d7aa1192e73af0a338200c61720f47b0ebe8d19faa3613f1e2
OLD_GRYPE_MANIFEST=sha256:31285b477845b9e10f76c4b7df425d200fa15db0e615b0cb4b639e4c3fc7aae4
OLD_GRYPE_REF_MATCH=True
OLD_SCAN_SHA256=e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92
LOCAL_DOCKER_IMAGE_ID=sha256:01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe
TWO_IMAGE_IDS_MATCH=False
PINNED_REPODIGEST_PRESENT=True
PLATFORM=linux/amd64
H2AM_SUMMARY_SHA256=99a455c5bedd435c0f72b0c9aacadcb96d8949db9cb1d2bff518416ca1b18e958f
AUDIT_COMPLETE=NO_SCAN_NO_WRITES
```

**Exact frozen approved Mediator child manifest ref**:
`asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-h2ah@sha256:01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe`.

H2AM existing actual failed stage `MEDIATOR_HISTORIC_LOCAL_CONFIG_MISMATCH`, **Mediator IMAGE_BINDING**, BEFORE runtime start. Old Grype scan is COMPLETE (**57 matches, 18 HIGH, 0 Critical**) and verified against exact pinned SHA. Gateway/Backend/Reader scans NOT attempted. H2AN successfully pulled 3 exact existing private image digests; all 4 locally present. **H2AN and H2AM one-time markers BOTH CONSUMED.** Do not rerun either; H2AJ/H2AK and H2AG markers also untouched. No image build, push, new pull, scan, Docker run/exec/stop/cleanup, Cloud Run/IAM/KMS/Firebase/production call here.

## Root cause — cross-store ID semantics, not proof of tampering

The H2AM source unconditionally does:

```python
# scripts/step05_h2am_selective_acceptance_once_20261128.py
image_id=self.local_image("mediator")   # Docker image inspect .Id
fail(image_id==historic["imageId"],"MEDIATOR_HISTORIC_LOCAL_CONFIG_MISMATCH")
```

`historic["imageId"]` is Grype's `source.target.imageID` from a Grype scan of **the exact immutable child reference**. Local Docker `.Id` is **exactly the approved child manifest digest** (confirmed by screenshot), not the Grype imageID. Docker with the containerd image store may report the manifest/index digest in `image inspect .Id` rather than legacy image config digest. Thus comparing the two different identifiers as if they had the same semantics is a **confirmed incorrect source assumption**. This outcome is consistent with a containerd store and is not by itself evidence the image content changed. **Do not weaken the gate to always-true or claim equivalence merely from different labels.**

Authoritative references (verify any future implementation against actual source and contract):
- Docker CLI maintainers explicitly note: containerd image store targets images by manifest/index rather than image config: https://github.com/docker/cli/issues/5526
- containerd/nerdctl documents `IMAGE ID` as target index/manifest, matching Docker containerd store, differing from legacy config digest: https://github.com/containerd/nerdctl/blob/main/docs/command-reference.md
- OCI image-spec no longer defines one universal ImageID implementation; previously config SHA256, now implementations vary: https://github.com/opencontainers/image-spec/blob/main/config.md
- OCI image manifest REQUIRED `config.digest` provides the **cryptographic binding between manifest digest and image config digest**: https://github.com/opencontainers/image-spec/blob/main/manifest.md

**Key uncertainty:** Screenshot does **NOT** prove the OCI child manifest's `config.digest` equals historic Grype `sha256:44c8657a...`, because the immutable child OCI manifest bytes / config descriptor have not yet been compared. The old Grype `manifestDigest` value `sha256:31285b...` is DIFFERENT from approved registry child digest and must not be silently substituted for it. To definitively bind identifiers, compare the exact pinned child manifest's authenticated, digest-hash-verified raw JSON `config.digest` with historic Grype imageID, using an existing trusted saved source or **one separately authorized minimal read-only OCI manifest request**, NOT a new scan/build/pull. Any unexpected mismatch means STOP.

## ONE concentrated H2AO Codex source-only repair BEFORE any new execution

User priorities: SPEED, no repeated completed tests, and fix root causes *before* scan. Do full implementation in one Codex run:

1. Read `AGENTS.md`, `docs/OLDX_CURRENT_HANDOFF.md`, this actual checkpoint, `docs/OLDX_STEP05_H2AM_SELECTIVE_RUNTIME_SOURCE_RECEIPT_2026-11-28.md`, consumed H2AM source+support+existing new tests, `deployment/four-role/h2aj-four-immutable-images-pinned-proposal.json`, and actual H2AN owner receipt. Do NOT change original consumed H2AM/H2AN scripts, markers, image digests, registry images, cloud resources, older tests, or Grype report. Source branch ONLY `security-hardening-review`.
2. Add a **new H2AO source-only canonical identity verifier** that understands the **OCI child manifest digest vs OCI config digest vs Docker containerd `.Id`** distinctions, rejecting mismatched refs/digests/platform/nonroot/cross-role lineage. Bind historic Grype report's pinned SHA, source.target.userInput/ref, recorded `imageID` and 57 severity results to the original image. Require an authenticated, hash-verified manifest config descriptor match to historic Grype imageID when that evidence is obtainable; otherwise **STOP with a precise reason before the new one-shot runtime marker**. Never treat arbitrary distinct image IDs as equivalent. If additional read-only private manifest fetch is truly required, add it as a separately described **one GET** under a future single exact Owner approval, with temporary isolated OAuth and no access token printed or retained.
3. Create one **new H2AO selective continuation runner** (new unique marker, new evidence path), not a patch that encourages re-running consumed H2AM. It must verify previous H2AM/AN markers and exact previous H2AM summary failure at `IMAGE_BINDING`, Mediator scan COMPLETE/no runtime attempts, Gateway/Backend/Reader scan+runtime NOT attempted, old Mediator Grype original report pinned; verify all four image refs already locally present, valid Grype DB, Owner/project scope and approved OCI identity BEFORE new marker.
4. Once *later separately approved*, execution may perform **only** Mediator OFF-health local runtime (NEVER Mediator Grype), then only after Mediator PASS, exactly one fresh Grype scan+OFF health each Gateway, Backend and Reader. Persist scan results independently of runtime and retain primary error, Docker `State.OOMKilled`, logs before cleanup; no `--rm` masking; no automatic retry or repeated scan. Run `--network none`, nonroot, read-only, no host port. Stop on ambiguity. Old H2AM/H2AN marker and evidence untouched; no build, push, Cloud Run/IAM/KMS/Firebase actions.
5. Add NEW focused offline tests for both **legacy Docker config-ID** and **containerd manifest-ID** identities, OCI manifest `sha256`/config digest match, wrong child SHA, wrong config SHA, wrong Grype ref/scan SHA, missing OCI proof, tampered prior receipt, old consumed markers preserved, Mediator scan import without repeat, no Docker operations before approval/preflight, selective scans only 3, and failure-path log/cleanup preservation. Test without Docker, Cloud or Grype execution. Do not rerun 19 H2AM focused tests or previous OLDX groups.
6. Commit and push source, NEW tests, consolidated new receipt, `AGENTS.md` latest checkpoint, handoff and Issue #17. Return remote verified SHA, test outcomes, exact remaining unknowns and **one narrowly scoped future Owner approval** for optional one read-only OCI manifest GET and one new **H2AO** local selective execution. No code/run now is owner-authorized by this document.

## Current security and launch posture

`H2AJ=FOUR_NEW_PRIVATE_IMAGES_REGISTRY_PASS`
`H2AN=THREE_LOCAL_PULLS_PASS_CONSUMED`
`H2AM=CONSUMED_PARTIAL_AT_IMAGE_BINDING`
`MEDIATOR_OLD_GRYPE=COMPLETE_57_WITH_18_HIGH_0_CRITICAL_DO_NOT_RESCAN`
`MEDIATOR_RUNTIME=NOT_ATTEMPTED`
`GATEWAY_BACKEND_READER_SCANS=NOT_ATTEMPTED`
`H2AO=SOURCE_ONLY_NEXT_NOT_EXECUTED`
`STEP05=ACTIVE`; `SECURITY=HOLD`; `PRODUCTION=OFF_NO_GO`.
