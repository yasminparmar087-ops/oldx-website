# OLDX Step 05 H2 — exact provider bindings and safe metadata-only readiness gate

**26 Nov 2026, after Codex consolidated G2–G6 source batch.** Repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. This packet is the **next genuinely new work** following source-only completion, not a claim that H2 has been activated.

## 1. Actual starting point (verified current GitHub)

Remote branch HEAD after Codex `45f20e8ba0dcc84e4106c998060f4639cbe3ce5e`. The [canonical technical receipt](OLDX_STEP05_C2_SOURCE_ONLY_ENABLED_SLICE_GAP_AND_ONE_PASS_IMPLEMENTATION_PACKET_2026-11-24.md) shows **11 distinct NEW focused groups verified in aggregate** on Windows Node v26.13; initial focused failures corrected. Not one final 11-case test suite, and no live Google/Firebase/KMS or hosted product acceptance. Current source:
- `scripts/c2-enabled-release-control.mjs`: new **default-OFF** synthetic scope requires exactly 3 distinct run SAs and 3 distinct, **not OLD OFF** immutable images, 6 evidence hashes, 2 synthetic actors, max1 Product +1 reviewed photo, max20 requests/20 minutes, independently trusted `verifyApproval` and durable `consumeRunBudget`.
- `scripts/c2-cloud-run-metadata-identity.mjs` and `scripts/c2-kms-request-signing.mjs`: source-only identity/managed asymmetric signing contracts, no actual current runtime identities, key ring/version or secret provisioned by this new source.
- `functions/staging-marketplace/secure-product-pipeline.mjs`: original backend remains **publication-OFF**. New C2 enabled factory is inactive until independent provider bindings/approvals and actual enabled image.
- Reused Firebase/Media/Firestore/nonce sources and atomic run-budget port plus cleanup DRAFT; local synthetic seller/buyer flow passed, but real managed-media moderation, Firebase IAM/Auth, Firestore TTL, identity, and cleanup proof remain **NOT VERIFIED**.

H1B prior separate OFF-only trial and four probes PASS; its exact new Run service deleted; W1 SA UID `115445220422157278526` was **disabled but not deleted at 26 Nov 22:14:17 IST**. Earliest separate 24-hour dependency review `27 Nov 22:14:17 IST`; not an automatic deletion. Never rerun old H1A/G1/G2A/G2B/W0/W1/W3V/W3–W6/W6SA or C2 G1 origin 1/0 test, build/scan/re-push, or touch old C1A resources.

## 2. The exact H2 bindings still to choose (NOT assumed already present)

| Gate | Required decision/evidence before any enabled pilot | Current evidence |
| --- | --- | --- |
| G2 — host and signing | Current trusted server-host choice; exact distinct mediator/Gateway/backend SA emails and immutable **new enabled** image digests; each Cloud Run service URI/audience, service Invoker IAM; designated `asia-south1` KMS **ASYMMETRIC_SIGN** CryptoKeyVersion with RSA-SHA256, enabled state, read-back public SPKI pin, signer-only authority for exact host and independent verifier | Source contract only; no selected live H2 identities/key |
| G3 — Firebase | Effective runtime identity not just declared SA; actual `oldx-staging/(default)` Firestore metadata, Firebase Auth Email/Password/revocation, least-privilege database/media roles and 2 synthetic test actors under separate consent | Local fixtures, not hosted data-plane evidence |
| G4 — approved media | Exact one pinned managed photo, ownership, separate moderation approval/provider/byte delivery and reversible publication consent | Local media policy and atomic fixture tested; real provider not bound |
| G5 — durability and cleanup | Real cross-instance atomic run-budget/nonce bindings, TTL configuration and retention, exact-version/UID synthetic cleanup readback and rollback rights | Native-shaped transaction adapter and cleanup draft; cloud bindings not proven |
| G6 — release authority | Independent verifier of owner-approved signed H2 scope + evidence/expiry; enabled-image security/provenance/cost/risk acceptance; exact private-first rollback, no public or real user access unless separately approved | Default-OFF guard source; H2 authority and hosted evidence still missing |

**Never reuse H1B OFF image** `sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e` or old C1A image `sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a` as enabled H2. The compiled-OFF experiment's 12 HIGH CVE acceptance was bounded to that test, not production/H2.

## 3. New one-shot live read-only metadata audit source (PREPARED, NOT RUN)

`scripts/step05_h2_provider_readonly_inventory_once_20261126.py`
- **Pinned final source commit:** `a97d83e57824f168bc2e2c978cc545aeb885d68b`
- **Verified Git blob:** `490095ca85821b22b5f2f4b4270b41986a08eb81`
- Uses existing **isolated** native WSL Google SDK and active Yasmin identity; `oldx-staging` project number from previously proven W0 identity. No new login, browser, Docker, image, install or auth-file change.
- Exactly 7 fixed **HTTPS GET-only** Google metadata endpoints plus at most 3 bounded CryptoKey *metadata-list* GETs (only if <=3 key rings in `asia-south1`). Lists are first-page bounded: pagination, unreachable regions, 401/403/5xx/timeout, ambiguous metadata => **PARTIAL/UNKNOWN**, never "absent". IAM SA listing and Cloud Run listing are **inventory**, not IAM policy verification or public exposure testing. Only one region `asia-south1`; other regions/projects never inferred absent.
- Examines project, regional Cloud Run service count/c2 name candidates, project SA count/c2 count, KMS key ring and `ASYMMETRIC_SIGN` CryptoKey **metadata counts only** (NO versions or private/public bytes), Firestore `(default)` DB metadata, Firebase Identity Toolkit Auth configuration, and project Storage bucket metadata count.
- No IAM policies read/written, no `testIamPermissions`, no privileged service invocation, no KMS asymmetric sign, no IAM change, no Cloud Run deployment, no Firestore documents, no Auth user list, no Storage object access or deletion, no re-probing prior disabled H1B SA. Bearer token kept inside Python memory only, no stdout/token files.
- Stores a **sanitized local-only** JSON metadata result under `/root/oldx-h2-provider-readonly-<UTC>/` with `umask 077`. GitHub stores **only script/source plan**, never auth tokens or unreviewed live metadata.
- New one-shot marker `/root/.oldx-step05-h2-provider-readonly-inventory-once-20261126` is distinct and consumed after local owner/project authentication. Do not delete/reset it or rerun on STOP; preserve evidence and choose only new read-only recovery if warranted. One response cannot justify an enabled deployment.
- Static source read back and safety guards inspected; **the Python file has not been executed by the Owner or assistant against Google APIs**. AST precheck is in the owner one-paste below.

### One paste — current Ubuntu WSL root shell (not Google Cloud Shell)

```bash
umask 077
d=$(mktemp -d /root/oldx-h2-readiness-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2read.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/a97d83e57824f168bc2e2c978cc545aeb885d68b/scripts/step05_h2_provider_readonly_inventory_once_20261126.py' &&
test "$(git hash-object "$d/h2read.py")" = '490095ca85821b22b5f2f4b4270b41986a08eb81' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2read.py" &&
python3 -B "$d/h2read.py" --h2-provider-metadata-readonly-once
```

Possible *limited* successful status:
```text
OLDX_H2R_RESULT=READ_ONLY_METADATA_WITH_LIMITS
OLDX_H2R_H2_BINDINGS=NOT_SELECTED_OR_INDEPENDENTLY_VERIFIED
OLDX_H2R_APPROVAL_VERIFIER=NOT_BOUND_OR_INDEPENDENTLY_VERIFIED
OLDX_H2R_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2R_SA_KMS_DB_STORAGE_WRITES=NONE
OLDX_H2R_DO_NOT_REPEAT=TRUE
```
Other printed `OLDX_H2R_*` lines summarize whether each metadata endpoint was visible. An all-200 inventory **does not mean H2 ready**. If `STOP`, DO NOT REPEAT; provide only sanitized `OLDX_H2R_*` lines, not OAuth codes, tokens, account configs or private raw HTTP responses.

## 4. Next decision after *actual* owner output

Convert this bounded metadata inventory into one **exact H2 provider binding selection**: choose only verified available principals/host, KMS signing version and independently pinned public key, real Firebase/media provider roles, separate owner approval verifier, durable/TTL/cleanup authority and enabled-image provenance. A new private-only synthetic H2 pilot would then need its own finite operational consent and fail-closed execution plan. If any provider missing, choose a safe creation or alternate-host path **after** precise owner consent, not as an implicit step of this read-only audit.

**Current:** `G2–G6=SOURCE_IMPLEMENTED_LOCAL_11_DISTINCT_GROUPS`, `H2_METADATA_AUDIT=SOURCE_READY_NOT_OWNER_RUN`, `H2_PROVIDER_BINDINGS=UNSELECTED`, `HOSTED_PRODUCT_SLICE=NOT_VERIFIED`, `H2/PRODUCTION=NO_GO`.

### Official API contracts checked

- Cloud Run regional services.list: https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/list
- IAM serviceAccounts.list: https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/list
- KMS keyRings/cryptoKeys.list: https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings/list and https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys/list
- Firestore default database.get: https://docs.cloud.google.com/firestore/docs/reference/rest/v1/projects.databases/get
- Firebase Identity Toolkit projects.getConfig: https://docs.cloud.google.com/identity-platform/docs/reference/rest/v2/projects/getConfig
- Cloud Storage buckets listing: https://docs.cloud.google.com/storage/docs/listing-buckets
