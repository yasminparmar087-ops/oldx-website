# OLDX Step05 H2 — owner actual metadata PASS/403, next exact two-permission check from saved evidence

**26 Nov 2026 ~23:07 IST.** Real owner screenshot of `OLDX_H2R_RESULT=READ_ONLY_METADATA_WITH_LIMITS` on isolated WSL. `KMS_KEY_RINGS=UNKNOWN_HTTP_403`, `AUTH_CONFIG=UNKNOWN_HTTP_403`; Cloud Run/SAs/Storage lists `FIRST_PAGE_COMPLETE`, exact `(default)` Firestore DB metadata visible, project identity ACTIVE. H2 bindings and approval verifier not selected. H2/production NO-GO.

[Full actual screenshot receipt](OLDX_STEP05_H2_OWNER_METADATA_READONLY_ACTUAL_RESULT_2026-11-26.md). **Do NOT rerun old H2R GET script or previous G1/W6SA/H1B tests or cloud operations**. HTTP403 does **not** prove KMS key absent or Auth sign-in disabled. Documentation: Google KMS keyRings.list permission is `cloudkms.keyRings.list`; Firebase Identity Toolkit `projects.getConfig` requires `firebaseauth.configs.get`. The 403 could be insufficient permission or another provider/config constraint; exact effective access is not yet proven.

## Fastest next single no-resource-write operator command

New `scripts/step05_h2_two_permission_and_saved_receipt_once_20261126.py`, **source PREPARED but not owner-executed**. Uses existing isolated native Google SDK Owner login, does NOT replay the completed API listing.

- Immutable pinned initial commit `6aba3e75c4493611fea5a51c00fd8c6b5093a7d9`.
- GitHub verified exact blob `bf11763e14ceb778990616d17e9e0475ea3679c2`.
- Reads only the previous H2R one-shot marker `/root/.oldx-step05-h2-provider-readonly-inventory-once-20261126` and its locally saved `sanitized-h2-metadata.json` (no upload), printing bounded previously recorded **Cloud Run service count**, **C2 service candidate names**, **project SA count/C2 candidate count**, and **Storage bucket count** if fully present. Does not query those APIs again. No full SA/bucket list exposed in stdout.
- Then performs exactly ONE additional **read-only permission test** as POST to Google Cloud Resource Manager `projects/oldx-staging:testIamPermissions` for only `cloudkms.keyRings.list` and `firebaseauth.configs.get`. **This POST requests effective permission information, not an IAM binding update, KMS signing, Cloud Run operation or Firebase data access.** Values `RETURNED_AT_PROJECT`, `NOT_RETURNED_AT_PROJECT` or `UNKNOWN_HTTP_403` are **project-level hints only**, not proof of resource-level or org-policy/API-service access. Any missing result is not proof of key/account absence. Not a repeat of broad old G1 test, because two new permissions specifically address the observed KMS/Auth 403.
- One new marker `/root/.oldx-step05-h2-two-permission-readonly-once-20261126`, consumed upon actual Google permission request. No retries, no token logging, no changes to IAM, KMS, Firebase Auth, Cloud Run, Storage, old H1B SA, Registry or production.
- Private sanitized JSON output only under `/root/oldx-h2-two-permission-readonly-<UTC>/`. Do NOT put credentials/raw account inventories in GitHub.
- If missing local evidence or identity wrong, STOP BEFORE request; if network/unknown after request, STOP, do not repeat/reset marker.

### ONE paste, same native Ubuntu WSL root terminal

```bash
umask 077
d=$(mktemp -d /root/oldx-h2-permissions-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2perm.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/6aba3e75c4493611fea5a51c00fd8c6b5093a7d9/scripts/step05_h2_two_permission_and_saved_receipt_once_20261126.py' &&
test "$(git hash-object "$d/h2perm.py")" = 'bf11763e14ceb778990616d17e9e0475ea3679c2' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2perm.py" &&
python3 -B "$d/h2perm.py" --saved-h2-and-two-permissions-once
```

Possible limited success: `OLDX_H2P_RESULT=LOCAL_EVIDENCE_AND_TWO_PERMISSION_HINTS_WITH_LIMITS`, plus separate `OLDX_H2P_KMS_LIST_PERMISSION` and `OLDX_H2P_AUTH_CONFIG_PERMISSION` result; actual values **NOT YET KNOWN**. If permission test returns 403, script may succeed with `UNKNOWN_HTTP_403` and still NO-GO. If STOP, never rerun a consumed one-shot. Owner should share only `OLDX_H2P_*` lines.

## After actual two-permission result

- If both permissions missing at project: propose **minimum scoped read-only** role changes (KMS Viewer; Firebase Authentication Viewer as appropriate) and seek separate explicit IAM write consent **before changing any grant**; never broaden old `paniruddhsinh` principal.
- If both returned yet data API still 403: don't grant random extra roles; focus on service enablement, conditional policy/org constraints and exact requested resource using newly justified independent diagnosis.
- If KMS ring/key metadata eventually visible, must still select distinct H2 signing key version/public pin and 3 fresh runtime SAs/new enabled image; real media, budget/TTL/cleanup and approval verifier are still needed.
- H1B W6SA disabled exact test SA UID `115445220422157278526` at 26 Nov 22:14:17 IST, NOT deleted; earliest separate dependency review 27 Nov 22:14:17 IST. No automatic deletion or H2 reuse of OFF resources.

**Current:** `H2R=ACTUAL_READ_ONLY_METADATA_PASS_WITH_LIMITS_CONSUMED`; `H2P=SOURCE_READY_NOT_RUN`; `KMS/Auth=403_UNKNOWN`; `G2–G6_SOURCE=IMPLEMENTED_LOCAL_PASS`; `H2/PRODUCTION=NO_GO`.

Official references: https://docs.cloud.google.com/kms/docs/reference/permissions-and-roles ; https://docs.cloud.google.com/identity-platform/docs/reference/rest/v2/projects/getConfig ; https://docs.cloud.google.com/iam/docs/roles-permissions/firebaseauth .
