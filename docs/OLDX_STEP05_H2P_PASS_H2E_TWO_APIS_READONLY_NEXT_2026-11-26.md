# OLDX Step05 — H2P actual PASS, both permission hints granted, exact H2E API enablement next

**26 Nov 2026 ~23:14 IST.** Owner WSL actual screenshot. GitHub repo `yasminparmar087-ops/oldx-website` / `security-hardening-review`. No Cloud changes from the read-only project permission check.

## 1. Actual H2P source result: DONE / CONSUMED

```text
OLDX_H2P_RESULT=LOCAL_EVIDENCE_AND_TWO_PERMISSION_HINTS_WITH_LIMITS
OLDX_H2P_REASON=NO_RESOURCE_OR_IAM_CHANGE
OLDX_H2P_AUTH_CONFIG=UNKNOWN_HTTP_403_FROM_PRIOR_RUN
OLDX_H2P_C2_SERVICE_ACCOUNT_COUNT=1
OLDX_H2P_C2_SERVICE_CANDIDATES=NONE
OLDX_H2P_CLOUD_RUN_COUNT=1
OLDX_H2P_CLOUD_RUN_LIST=FIRST_PAGE_COMPLETE
OLDX_H2P_FIRESTORE_DB=METADATA_VISIBLE_EXACT_FROM_PRIOR_RUN
OLDX_H2P_KMS_RING_LIST=UNKNOWN_HTTP_403_FROM_PRIOR_RUN
OLDX_H2P_SERVICE_ACCOUNTS_COUNT=7
OLDX_H2P_SERVICE_ACCOUNTS_LIST=FIRST_PAGE_COMPLETE
OLDX_H2P_STORAGE_BUCKETS_COUNT=0
OLDX_H2P_STORAGE_BUCKETS_LIST=FIRST_PAGE_COMPLETE
OLDX_H2P_PROJECT_PERMISSION_TEST=PROJECT_TEST_200_WITH_LIMITS
OLDX_H2P_KMS_LIST_PERMISSION=RETURNED_AT_PROJECT
OLDX_H2P_AUTH_CONFIG_PERMISSION=RETURNED_AT_PROJECT
OLDX_H2P_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2P_CLOUD_RESOURCE_WRITES=NONE
OLDX_H2P_DO_NOT_REPEAT=TRUE
```

Script/source proof pinned original commit `6aba3e75c4493611fea5a51c00fd8c6b5093a7d9`, blob `bf11763e14ceb778990616d17e9e0475ea3679c2`. Canonical [verbatim screenshot and interpretation](OLDX_STEP05_H2P_ACTUAL_TWO_PERMISSIONS_RETURNED_BOTH_APIS_403_2026-11-26.md).

**Meaning:** `cloudkms.keyRings.list` and `firebaseauth.configs.get` **both RETURNED at PROJECT** in a real `testIamPermissions` response, yet previous exact target metadata calls both returned 403 and their failure reason wasn't recorded. Project permission hints do NOT prove API enabled, target resource-level effective access, current org constraint, or existence/absence of KMS key. **DO NOT grant roles on this evidence or rerun broad IAM/G1/H2P/H2R.** Actual source snapshot: 1 regional Cloud Run service, no `oldx-c2` candidate service, 7 project SAs (1 contains c2), 0 project buckets, default Firestore DB metadata visible; counts are first-page complete within the exact listed scope, not all-region audit. No H2 selected runtime identities, managed signing key, media provider or independent approval verifier.

## 2. New precise H2E (API enablement metadata only) — SOURCE PREPARED, NOT OWNER RUN

New script `scripts/step05_h2_api_enablement_exact_two_readonly_once_20261126.py`.

- Immutable **pinned source commit**: `7b5f4b9ee4d5c745d8ce6bd87b4a43773cd31dec`
- Exact **verified GitHub blob SHA**: `be06d2cda30db0b647efd0ab5ee372389de32a3a`
- Fresh separate one-shot marker: `/root/.oldx-step05-h2-exact-api-enablement-get-once-20261126`.
- Uses already-isolated native owner WSL gcloud identity `yasminparmar087@gmail.com`, project `oldx-staging`. Requires actual consumed H2P receipt; does not replay its permission POST, earlier 7-GET inventory or any previous cloud probe.
- Exactly TWO **Service Usage v1 services.get HTTPS GET** on existing project number `38472235077`: `projects/38472235077/services/cloudkms.googleapis.com` and `projects/38472235077/services/identitytoolkit.googleapis.com`. Only service config **state** and exact returned name are checked; no Auth users/config or CryptoKey metadata, IAM/Invoker/Storage/Firestore requests, KMS signing, Cloud Run actions or resource creation. No automatic API service enablement. No credential or raw response body printed.
- If HTTP200 and matching name: `API_ENABLED` or `API_DISABLED` from exact `state`. If 401/403/404/5xx/network error: `UNKNOWN_...`, **not** proof disabled or absent. `Service Usage services.get` itself may require permission; 403 there does not justify increasing roles automatically. No pagination.
- Writes local-only sanitized status JSON and marker under `/root` with `umask 077`. No private OAuth tokens, IAM bindings or resource details committed to GitHub.
- Earlier H1B OFF-only Cloud Run service deletion confirmed, its test SA UID `115445220422157278526` disabled (NOT deleted) on 26 Nov 22:14:17 IST. Earliest separate dependency review 27 Nov 22:14:17 IST; no deletion/reenabling from H2E. No old H1A/G2B image rebuild/scan/push.
- **H2 and production remain NO-GO regardless of H2E state**; enabled APIs alone do not establish managed signing key, trusted host, three fresh runtime principals, Firebase Auth acceptance, approved moderated photo, durable budget/nonce cleanup, enabled image provenance or independent approval.

### One-paste exact command — current Owner Ubuntu WSL root prompt

```bash
umask 077
d=$(mktemp -d /root/oldx-h2e-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2e.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/7b5f4b9ee4d5c745d8ce6bd87b4a43773cd31dec/scripts/step05_h2_api_enablement_exact_two_readonly_once_20261126.py' &&
test "$(git hash-object "$d/h2e.py")" = 'be06d2cda30db0b647efd0ab5ee372389de32a3a' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2e.py" &&
python3 -B "$d/h2e.py" --h2-two-api-states-readonly-once
```

Expected *shape* (values NOT KNOWN yet):
```text
OLDX_H2E_RESULT=EXACT_TWO_API_STATES_READ_WITH_LIMITS
OLDX_H2E_KMS_API=API_ENABLED|API_DISABLED|UNKNOWN_...
OLDX_H2E_AUTH_API=API_ENABLED|API_DISABLED|UNKNOWN_...
OLDX_H2E_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2E_CLOUD_RESOURCE_WRITES=NONE
OLDX_H2E_DO_NOT_REPEAT=TRUE
```

Any `STOP` or `UNKNOWN` means no automatic rerun or role addition. Send `OLDX_H2E_*` summary only; do not share private gcloud config, token or Google raw error message.

## 3. Decision after actual H2E

- If API `DISABLED`: record fact, propose separate explicit owner permission to enable **only that API** (activation is a Cloud project change); no automatic enable as part of read-only script.
- If API `ENABLED` but direct KMS/Auth GET 403 remains from H2R: next NEW narrowly scoped sanitized per-API 403 reason diagnosis (not blind IAM grant) with bounded GETs only if necessary; preserve `status.details[].reason` and service/consumer only, no raw confidential message.
- If Service Usage GET `UNKNOWN`: stop and narrow Service Usage permission/access or use an independently approved alternative diagnostic, without guessing availability.
- Regardless of case: H2 future actual bound providers/approval and separately authorized enabled pilot remain OPEN.

**Current:** `H2P=ACTUAL_PASS_CONSUMED`; `H2E=SOURCE_PREPARED_NOT_OWNER_RUN`; `KMS/Auth_TARGET_GET=403_UNKNOWN_CAUSE`; `PROJECT_BOTH_PERMISSIONS=RETURNED`; `STEP05=IN_PROGRESS`; `H2/PRODUCTION=NO_GO`.

Official docs: https://docs.cloud.google.com/service-usage/docs/reference/rest/v1/services/get ; https://docs.cloud.google.com/iam/docs/testing-permissions .
