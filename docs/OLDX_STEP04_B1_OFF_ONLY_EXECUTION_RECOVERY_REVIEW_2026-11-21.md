# OLDX Step 04 — B1 OFF-only deploy and recovery operator review (SOURCE-ONLY)

## 21 Nov 2026 — OWNER R1 + R2 narrow conditional execution approvals RECORDED (NEW LATEST)

User expressly replied `ha manjuri chhe` to **two separate specific rollback scopes**: **R1** remove *only* future `ownerreadv2` tag after it is created, leaving `healthcheck` and `step3rc14` intact; **R2** restore original `oldx-owner-read-00001-8kr=100%` main only if unexpected traffic drift is established and a fresh exact-state safety review permits it; R2 is **NO-OP** when old 100% main/tags remain. [Owner R1/R2 consent packet](docs/OLDX_STEP04_R1_R2_OWNER_CONDITIONAL_APPROVAL_2026-11-21.md). `R1_OWNER_CONDITIONAL_CONSENT=YES`, `R2_OWNER_CONDITIONAL_CONSENT=YES`, prior `B1_OWNER_CONDITIONAL_CONSENT=YES`. **Still NOT permission for immediate blind cloud execution**: fresh immediate pre-write service-state guard, exact final B1 CLI flags, environment/identity/secret diff, inherited IAM scope review, no public invocation, source digest, post-state/recovery plan needed. R1 tag removal does **not** revert latest template/revision. G4-A three GET snapshot ~17:48 `PASS_WITH_LIMITS` **consumed; do not rerun for status**. C4/G8 OFF-only risk accepted with limits; G2 independent builder provenance UNKNOWN, G4 other-db/exclusive invocation NOT PROVEN. `B1_R1_R2_EXECUTED=NO`, `STEP04=HOLD`, production NO-GO.


Date: 21 Nov 2026. **DO NOT EXECUTE THIS AS A SCRIPT.** The owner gave conditional B1 scope consent, C4 narrow risk acceptance, G8 narrow financial risk acceptance; a fresh G4-A three-GET check just **PASSED WITH LIMITS** at ~17:48 IST. Its single read-only run is **CONSUMED**. See [sanitized G4-A receipt](OLDX_STEP04_G4A_PREFLIGHT_OBSERVED_PASS_2026-11-21.md).

## Exact target and immutable checkpoint

- Existing private Cloud Run service: `oldx-owner-read`, project `oldx-staging`, region `asia-south1`, one existing runtime service account from the approved G4-A snapshot.
- Proposed new npm-free OCI index: `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-npmfree-20261121-a1@sha256:0844b637cf1bfedef60caa6a54ad515ebf9c0a937453b409101ad0d2ff254f79`, private existing Artifact Registry. C1/C2 index identity and C3 local digest-bound signed receipt already verified. No build, push, scan or re-sign.
- One new **revision/tag** `ownerreadv2` with **0% untagged main traffic**. Existing main `00001-8kr=100%`, `00002-tid=healthcheck`, `00003-nus=step3rc14` **exactly preserved** (the historical step3 tag has no hyphen). Unknown revision suffix of new revision must be obtained only *after* new create.
- Candidate target **1 CPU, 512Mi, 1 concurrency, timeout 30 seconds, minimum instances 0, maximum instances 1**, request-based pricing, private IAM check on, both activation flags EXACT `false`, no hosted API calls, no Firestore/Auth/Storage operation, no network/test request, no public access, short supervised review window.
- Must **not** send real user data or make enabled Product route accessible. `--no-traffic` alone does NOT prevent invocation via the tagged URL; IAM must stay enforced. Both exact FALSE flags are a second independent guard. Existing IAM Owner/Editor and parent/inherited unknown means *not exclusive-owner*.

## Provider syntax independently checked (documentation, NOT yet deployed)

Google Cloud official [rollouts guide](https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration) explicitly demonstrates `gcloud run deploy SERVICE --image IMAGE_URL --no-traffic --tag TAG_NAME`. [Current CLI reference](https://docs.cloud.google.com/sdk/gcloud/reference/run/deploy) documents the flag family `--tag`, `--no-traffic`, `--service-account`, `--cpu`, `--memory`, `--concurrency`, `--timeout`, `--min-instances`, `--max-instances`, `--set-env-vars` and identity/ingress controls. [Traffic reference](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/update-traffic) includes `--remove-tags` and `--to-revisions`.

**No pastable deploy command is authorized or issued in this source-only packet.** A precise final command must be dry-reviewed for the actual installed `gcloud.cmd` version and entire service template before use. Particular STOP hazards:
- `--set-env-vars` replaces the set of env variables; `--update-env-vars` can inadvertently retain old/unexpected environment values. Decide exact new revision env allowlist explicitly. Do not echo secret values in public documents.
- The new revision changes the service's **latest template/latestReady revision even at zero main traffic**. Removing only its tag is NOT a full rollback of template, revision existence, or ongoing costs. R2 no-op pertains only to root traffic/tags, NOT a claim old template restored. Any template restoration is a *different* approved transaction and may itself create a revision.
- `--no-allow-unauthenticated`, IAM grants, `--set-iam-policy`, `--to-latest`, `--clear-tags`, `--to-revisions` and broad YAML `replace` can change active access/traffic/config; none is part of ordinary B1 OFF-only write.
- Do not deploy if public principal, invoker IAM check disabled, unknown IAM inheritance risk inconsistent with owner-approved OFF-only scope, tag conflict, revision preimage drift, unexpected env secret or service template side effect, missing local sign/identity receipt, or any inability to perform safe recovery.

## Minimal operator one-try sequence when explicitly released

1. **Before** any mutation: same-window *fresh* source receipt and exact immutable digest; one live service-state/traffic direct-IAM preimage (do not replay C5 revision-only GET set). If the verified 17:48 read has gone stale, refresh only what is needed to guard drift, never repeat entire G4-A suite for status alone.
2. Verify `ownerreadv2` does not already exist and there is no concurrent operator. Verify no root traffic/old tag edits, no IAM/public access change, no unintended env changes; fail closed.
3. Require **specific recorded approvals** for R1 tag-only removal and R2 conditional emergency traffic restoration **before creating** B1. Also require source-approved exact final flags and new revision target.
4. At most one supervised B1 deployment attempt; no automatic retries or guesswork after unknown state. Collect minimal sanitized post-operation receipt: new revision identity, target image digest, flags, resources, tag, old 100%-main/tag invariants; do NOT invoke tagged URLs or upload raw service/IAM JSON.
5. R1 if trial must end: remove **only** `ownerreadv2` tag with fresh exact-state guard and separately recorded owner approval. Verify original main/root and tags again; this does not erase the revision. R2 **NO-OP** while original main + tags match; if unexpected traffic drift, **STOP** and follow an incident-specific, freshly authorized restore plan, not a generic past command.
6. Record real observed result in `AGENTS.md`, `OLDX_CURRENT_HANDOFF.md` once; old evidence/history immutable. Do not call `B1_PASS` on flags/source alone. No production rollout.

## Remaining explicit STOPs

- `G4A_FRESH_DIRECT_POLICY_PREFLIGHT=PASS_WITH_LIMITS` observed ~17:48; `G4_PARENT_INHERITED_IAM=NOT_VERIFIED`; `G4_OTHER_DB_DENIAL=NOT_VERIFIED`; `G4_EXCLUSIVE_INVOCATION=NOT_PROVEN`.
- `C4_OWNER_OFF_ONLY_RISK=ACCEPTED_WITH_LIMITS`, original 1 CRITICAL/5 HIGH Grype unchanged.
- `G8_OWNER_OFF_ONLY_FINANCIAL_RISK=ACCEPTED_WITH_LIMITS`, no provider-wide hard max guarantee.
- `B1_OWNER_CONDITIONAL_SCOPE_CONSENT=YES`; `B1_EXACT_EXECUTION_RELEASE=NOT_YET`; `R1_R2_OWNER_EXECUTION_CONSENT=NOT_RECORDED`.
- `B1_DEPLOYMENT=NOT_STARTED`; `R1_EXECUTED=NO`; `R2_EXECUTED=NO`; `STEP04=HOLD`; `PRODUCTION=NO_GO`.

**Next request:** Explicit owner authorization, strictly scoped to *R1 remove only the new tag if created* and *R2 restore the exact main 00001=100% only upon an incident, after a fresh guarded preimage*, with neither permission allowing IAM, billing, Firebase, image, build, data-plane activation or production changes. Then finalize/install-version-check the exact B1 command and safe single-use operator sequence before action. 
