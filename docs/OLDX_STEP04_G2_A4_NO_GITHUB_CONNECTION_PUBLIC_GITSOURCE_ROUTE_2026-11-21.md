# OLDX Step04 G2 A4 — public GitSource without Cloud Build GitHub connection (SOURCE-ONLY)

21 Nov 2026 after actual A3 owner screenshot, `security-hardening-review`, repo `yasminparmar087-ops/oldx-website`.

## 1. New actual A3 evidence: complete, never rerun

The owner-supervised **one** A3 Windows PowerShell command actually returned (without STOP):

```text
G2_A3_CONNECTION_COUNT_ASIA_SOUTH1=0
G2_A3_GITHUB_CONNECTION_COUNT_ASIA_SOUTH1=0
G2_A3_GITHUB_REPOSITORY_OLDX_LINKED=UNVERIFIED
G2_A3_OTHER_REGIONS=NOT_CHECKED
G2_A3_BUILD_SERVICE_ACCOUNT=NOT_CHECKED
G2_A3_BUILD_REGISTRY_DEPLOY_WRITES=NONE
G2_A3_REGION_ONLY_READ=COMPLETE_WITH_LIMITS
```

As of that screenshot, there were **no Cloud Build v2 Connections returned in asia-south1**. Nothing in this limited result proves no connections elsewhere; in particular, absence from the one region does not mean Google Cloud Build cannot build from OLDX's **public** GitHub repository. [Actual A3 record](OLDX_STEP04_G2_A3_CONNECTED_SOURCE_REGION_READ_ONLY_2026-11-21.md) is consumed. Previous A2 Cloud Build API enable `ENABLED_VERIFIED` is also complete. **NO more A1/A2/A3 queries.**

## 2. More efficient documented source lane (NEW; no GitHub OAuth/Secret Manager required for public URL)

Official Google Cloud CLI reference explicitly supports:

```text
gcloud builds submit "https://github.com/owner/repo" --git-source-revision=<branch|tag|commit SHA> --config=config.yaml
```

The Cloud Build V1 `GitSource` schema says `url` can be any **accessible** Git remote and `revision` can be a **commit SHA**; Cloud Build uses `git fetch`. This **does not require a Cloud Build v2 connection resource** to be created. The actual OLDX repo is currently public (GitHub REST repo metadata previously checked), so a read-only **direct HTTPS GitSource with immutable full commit SHA** is the **preferred candidate for one future independently attested source-to-image build**, avoiding connection creation, broad GitHub app authorization, Secret Manager credentials and cross-region searches.

**This is a documented supported path, NOT proof of execution or source access by Cloud Build at this time.** Git fetch for an exact SHA, build-agent network rules, selected GitHub commit availability and source provenance record content must be verified at a separately approved *new* build. If an exact SHA cannot be fetched, STOP rather than silently falling back to mutable `main` or `security-hardening-review`. No Docker/build/Registry action is authorized here.

Official:
- https://docs.cloud.google.com/sdk/gcloud/reference/builds/submit (source URL, `--git-source-revision`, `--region`, `--disk-size`, `--service-account`)
- https://docs.cloud.google.com/build/docs/api/reference/rest/v1/projects.builds (GitSource, revision can be commit SHA)
- https://docs.cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance (`images`, `requestedVerifyOption: VERIFIED`, SLSA verifier source + builder checks)

## 3. What a *future* separately approved ONE Cloud Build must freeze

**Source:** use `https://github.com/yasminparmar087-ops/oldx-website` and an **owner-approved 40-hex Git commit SHA captured at execution approval time on `security-hardening-review`**. Never default to `main`, mutable branch head or working directory upload. Existing `Dockerfile.product-read.bellsoft-npm-free` has exactly two immutable base digests: `node:24-bookworm-slim@sha256:dc26ae92c9fb15cf6b1d63e20f0944b2efe0f115b20e00be48fb23fceb061c54` and `docker.io/bellsoft/hardened-nodejs@sha256:ef00ba8e634402e8dd3b374643fdbc178e876c7a312c9d55e4734efaa1e93d94`. Keep reviewed Dockerfile-specific allowlist; source-only check before build must detect relevant drift. Do not put tokens, keys, local files or unpublished receipts into the public Git history or image.

**Build/output:** build a **NEW** isolated immutable candidate into a unique **private** `oldx-staging` Artifact Registry target, not overwrite the deployed `0844...` image/tag. Build must publish through top-level `images` with `requestedVerifyOption: VERIFIED`; do not treat an explicit Docker push step as equivalent. No automatic build trigger, multi-run retry or automatic Cloud Run deployment. Assign project/region, max build timeout and disk-size only after grounded cost/capacity review; earlier Cloud Shell 14 GiB conservative scratch does **not** establish actual Cloud Build disk capacity. Google's pricing for Cloud Build, possible extra SSD charges and Registry storage/logging/egress cannot be assumed free or under whole-project cap. Keep owner ₹2,000/month hard preference but require separate one-shot build cost envelope.

**Identity:** the build service account currently used/default is **UNVERIFIED** (A3 did not check). Do not silently use a broad default identity. Google recommends user-managed least privilege; using it requires a separately reviewed `iam.serviceAccounts.actAs` authorization and configured Cloud Logging or user-owned storage for logs. This task does not approve creating SA, roles, logs buckets, or enabling more APIs. A focused future read-only identity preflight can use Google's supported `gcloud builds get-default-service-account --project=oldx-staging --region=asia-south1` but it is *not executed* here and default SA discovery does not imply permission to build with it.

**Proof:** after the **new** image exists, verify actual image digest and `sourceProvenance.resolvedGitSource` (if present), signed builder ID, source URI, exact commit SHA/materials and in-toto provenance using supported verifier; no claim of SLSA level until observed. If this direct Git-source route fails to produce verifiable source/builder attribution, mark `G2_TRUSTED_BUILDER=NOT_ESTABLISHED` and STOP; a v2 connectedRepository route could later be separately approved as fallback. Reconcile 1 CRITICAL/5 HIGH in frozen previous scan against **new** image's focused assessment—never rewrite or suppress old scanner report; old C4 owner acceptance was for the completed *private default-OFF B1* only.

## 4. Correct next operator/owner boundary

- **Now** source-only A4 evaluation complete; do NOT install/connect a new GitHub App, create GitHub OAuth/PAT/Secret Manager, list more regions, enable another API or rerun old G2 scans just because A3 count was zero.
- **Next useful genuinely different task (read-only)**: inspect which default Cloud Build service account Google would use and whether any narrowly designated nonlegacy builder already exists; separate consent before any IAM write/build submission. Minimize reads to those needed for identity decision, avoid a broad repeat of prior project IAM auditing.
- **Then separate exact owner approval** for one source-pinned new *private, nondeployed* build with output provenance/cost/time/disk/log restrictions. The A2 owner approval was **one API enable only**, and cannot be generalized.
- **State**: `G2_A3=COMPLETE_ZERO_CONNECTIONS_ASIA_SOUTH1`, `G2_A4_DIRECT_GITSOURCE_ROUTE=SOURCE_ONLY_SUPPORTED_NOT_RUN`, `G2_BUILD_ACCOUNT=UNVERIFIED`, `G2_NEW_ATTESTED_IMAGE=NOT_BUILT`, `G2_SIX_SEVERE_CVE=OPEN`, `G4_EFFECTIVE_OTHER_DB_DENY=UNVERIFIED`, `STEP04=HOLD`, `PRODUCTION=NO_GO`.
- No future agent should re-run C1–C5, original local image build, Grype, old cosign, B1/R1/R2, G4 one-doc/allow analyzer, Cloud Build A1/A2/A3, billing or CI for reassurance. Existing G2 Security Watch handles new official CVE releases; don't duplicate it.

**No Google Cloud call or GitHub Actions/Build execution performed by this source-only document.**
