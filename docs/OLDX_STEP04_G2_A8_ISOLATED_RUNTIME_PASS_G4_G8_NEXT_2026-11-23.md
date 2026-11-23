# OLDX Step04 A8 — one-off isolated immutable new image runtime PASS WITH LIMITS; G4/G8 next

## Actual owner Google Cloud Shell screenshot — 23 Nov 2026 ~21:05 IST

Owner executed the already prepared SHA256-checked one-shot source from immutable Git commit `e6350642530b5b5afdf3a592eaba5f9db2513a2e`, source script `scripts/step04-a8-isolated-runtime-one-shot.sh`. Original source SHA256 printed `/tmp/oldx-a8-runtime-source-2506826f.sh: OK`. The ONLY subject was previously built immutable BellSoft Registry image `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`.

Actual terminal result:
```text
/tmp/oldx-a8-runtime-source-2506826f.sh: OK
A8_RUNTIME_ONESHOT_ATTEMPT=CREATED
A8_RUNTIME_SUBJECT=EXACT_IMMUTABLE_NEW_DIGEST
A8_RUNTIME_EXACT_DIGEST_PULL=PASS
A8_RUNTIME_REGISTRY_DIGEST=PASS
A8_RUNTIME_CONFIG_USER=APPUSER
A8_RUNTIME_NETWORK=NONE
A8_RUNTIME_ROOTFS=READ_ONLY
A8_RUNTIME_NONROOT=true
A8_RUNTIME_HEALTH_STATUS=200
A8_RUNTIME_DISABLED_OWNER_STATUS=503
A8_RUNTIME_FIREBASE_NETWORK=ISOLATED_NOT_TESTED
A8_RUNTIME_ISOLATED_LOCAL_TEST=PASS_WITH_LIMITS
A8_RUNTIME_REAL_IAM_OTHER_DB=NOT_TESTED
A8_CLOUD_RUN_DEPLOY=NONE
A8_BUILD_SCAN_SLSA_RERUN=NONE
A8_STEP04=HOLD_PENDING_G4_G8_AND_RISK
```

Conclusion: **G2 exact A8 new-digest local default-OFF sandbox runtime gate PASS WITH LIMITS**. The exact downloaded image RepoDigest and Docker-config user `appuser` were checked. Container ran with no outbound network (`--network none`), read-only rootfs, cap-drop all, no-new-privileges, temporary /tmp, no host ports/mounts/ADC/Firestore credentials, feature flags explicitly FALSE. In-container Node loopback request checked 200 `/healthz` and 503 `/api/staging/marketplace/owner`; UID >0. The script's exit trap stops/removes the container. The one-shot local marker and private working logs remain for provenance. This is **real local runtime evidence**, stronger than source or emulator only, but NOT hosted Cloud Run revision, tested Firebase IAM or multi-database denial, enabled Product API, proof any CVE is fixed, new SLSA trust for a future build, or production authorization. Do not rerun the one-shot: marker consumed.

## Gate reconciliation — use CONSUMED older observations, not stale future-plan text

**G2:** one trusted Google Cloud Build on 22 Nov SUCCESS, signed exact Git source commit/subject/builder and SLSA verifier PASS; ONE Grype scan of this NEW digest completed 46 package-vulnerability matches (1 CRITICAL, 23 HIGH, 19 MEDIUM, 3 LOW), 15 unique severe CVE IDs. Seven BellSoft fixed-version candidates (PURLs in new image identify namespace `bellsoft-hardened-containers`, scanner metadata only, no vendor APK signature), two disputed glibc, one SQLite CLI workflow and five potentially exposed OpenSSL contexts need final vendor/backport and threat mitigation disposition. Current local default-OFF runtime **PASS WITH LIMITS**. Does not turn 46 matches into zero.

**G4 historic work ALREADY DONE, do not repeat:** The single corrective Cloud Asset IAM allow-policy query dated 21 Nov ~19:03 returned exactly ONE selected-principal Firestore GET/CREATE/UPDATE/DELETE allow binding with exact `resource.name == "projects/oldx-staging/databases/(default)"`, **zero** unconditional/other-conditioned matches *within this query*, nested/outer fullyExplored true. Older direct Cloud Run service/project IAM snapshot included project Owner=2/Editor=1 and a named invoker; **exclusive invocation NOT proven**. Project parent metadata `NO_PARENT_REPORTED`, not a guarantee no other effective access. Previous default-DB one-document positive and DELETE403 completed. Cross-db actual deny remains **UNVERIFIED** without a distinct approved resource/negative test; Cloud Asset allow-policy alone is not cross-db denial. Earlier private default-OFF B1 revision `oldx-owner-read-00010-zud` one-shot deployment completed and R1 tag-only removal (preserving root 100% and prior tags) completed; DO NOT redeploy, retag or repeat B1/R1. All past OFF-only trial scope risk acceptances were for that **consumed** trial only, not enabled API/production.

**G8:** owner historically accepted limited exposure to side-provider billing for that one OFF-only private trial; not a guaranteed provider-wide INR hard ceiling. Cloud Run spend caps are service-scoped with reporting/enforcement lag; provider-wide cost stop remains **NOT_PROVEN**. Do not repeat old billing snapshots or update caps/billing; do not transfer that scope acceptance to enabled API/production.

## Next meaningful action after this checkpoint

Stop repeating G2/G4/G8 historic tests. Distinguish two decision paths:

1. **Keep default-OFF project-private behavior** while resolving remaining work via source-only risk ledger and planning. No enabled Product/Firestore data path or production. No new Cloud Run deploy and no repeat scan/build. This path is currently backed by local runtime PASS with limits plus previous one-time OFF-only trial, but not a formal Step04 full GO.
2. **Enabled Product API/website launch:** remains a separate G4-B effective multi-DB denial/authorization requirement, direct invoker controls, sufficient non-exploitable or formally accepted CVE risk, realistic gross cost/rollback plan, additional P0 tests and a fresh explicit owner GO. A new enabled-test scope (if needed) requires specifically approved resources and rollback; do not create a second Firestore database, change IAM, enable ADC or API without a separate approval.

Existing source plan: `docs/OLDX_STEP04_G4_AFTER_R1_DISTINCT_ALLOW_ANALYZER_GATE_2026-11-21.md`, `docs/OLDX_STEP04_G8_SERVICE_CAP_AND_OFF_ONLY_DECISION_2026-11-21.md` and `docs/OLDX_SINGLE_EXECUTION_PLAN_2026-11-13.md`. The old historical docs' 'B1 not yet executed' paragraphs are **superseded** by observed R1 completion. Next may prepare a **distinct narrow, read-only list of existing Firestore database names** to establish if any non-default database exists, before even considering a safe negative test; this is a planning check only and not proof of denial. No new resources may be created as a shortcut.

**Latest status:** `G2_A8_LOCAL_RUNTIME=PASS_WITH_LIMITS`; `G2_A8_SCAN=COMPLETE_FINDINGS_TRIAGE`; `G4_ALLOW_ANALYSIS=PASS_WITH_LIMITS`; `G4_OTHER_DB_DENY=UNVERIFIED`; `G4_EXCLUSIVE_INVOKER=NOT_PROVEN`; `G8_PROVIDER_WIDE_HARD_STOP=NOT_PROVEN`; `STEP04=HOLD`, `PRODUCTION=NO_GO`. All previous artifacts remain preserved in GitHub/owner private Cloud Shell HOME.