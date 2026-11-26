# OLDX Step05 H2E — Owner actual one-shot STOP_AFTER_MARKER; new two-field GET recovery only

**26 November 2026 ~23:19 IST**, Owner actual Ubuntu WSL screenshot after running pinned `scripts/step05_h2_api_enablement_exact_two_readonly_once_20261126.py` (commit `7b5f4b9ee4d5c745d8ce6bd87b4a43773cd31dec`, original blob `be06d2cda30db0b647efd0ab5ee372389de32a3a`). This record is screenshot/source derived, not independent live Google Cloud access.

## 1. Actual result — do not repeat H2E

```text
OLDX_H2E_RESULT=STOP_AFTER_MARKER
OLDX_H2E_REASON=UNEXPECTED_SERVICE_USAGE_RESPONSE
OLDX_H2E_KMS_API=UNKNOWN_NOT_CHECKED
OLDX_H2E_AUTH_API=UNKNOWN_NOT_CHECKED
OLDX_H2E_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2E_CLOUD_RESOURCE_WRITES=NONE
OLDX_H2E_NO_IAM_KMS_FIREBASE_CHANGES=TRUE
OLDX_H2E_DO_NOT_REPEAT=TRUE
```

**Interpretation:** the H2E one-shot marker `/root/.oldx-step05-h2-exact-api-enablement-get-once-20261126` is consumed. No Cloud resource writes or H2 activation. `UNKNOWN_NOT_CHECKED` reports no *confirmed states*; the script **did make its first Service Usage GET attempt**, but stopped while checking its response and never reached the second state. Do NOT claim either API is disabled, enabled, or absent. Do NOT re-execute H2E or delete/reset the marker.

**Source diagnosis:** H2E `get_state()` raises `UNEXPECTED_SERVICE_USAGE_RESPONSE` only when its HTTP success response fails `status==200 and size <= 65,536 bytes`; its `urllib` handler separately returns `UNKNOWN_HTTP_x` on normal HTTP error status. The likely failure was the **Service Usage v1 GET returning a full `Service` configuration larger than the script's 64 KiB cap**, but the response's exact byte length wasn't retained, so **this is a supported hypothesis, not proven root cause**. Google Service Usage `services.get` returns full Service configuration+state; Google's standard REST partial-response `fields` selector supports reducing the response to `name,state`.

Previous H2P project `testIamPermissions` returned both `cloudkms.keyRings.list` and `firebaseauth.configs.get` at project, while H2R target GETs to KMS and Auth config returned 403; this conflict remains unresolved. No blind grants, no old G1/IAM probe repeats. Previous H2P saved inventory count snapshot: one asia-south1 Cloud Run service, no oldx-c2 service, seven project SAs, one c2-named SA, zero project Storage buckets, exact default Firestore database metadata. No new count inventory necessary.

## 2. NEW H2F recovery source, exactly two minimal field-filtered GETs (prepared, NOT executed)

File `scripts/step05_h2_exact_two_api_states_fields_recovery_once_20261126.py`.

- Immutable pinned source commit `f228b02cfbbbe4dab8d67cd5398615ca2e56408d`
- Exact GitHub blob `362ffb697ab316e7ed3152cb613c3db5e35e8b6c`
- Distinct marker `/root/.oldx-step05-h2-exact-two-states-fields-only-once-20261126`; consumed on actual attempts and NEVER reset or rerun.
- Requires the already CONSUMED original H2E marker with exact `RESULT=STOP_AFTER_MARKER` and `REASON=UNEXPECTED_SERVICE_USAGE_RESPONSE`; existing isolated Owner `yasminparmar087@gmail.com` native WSL SDK/project `oldx-staging`; no new installation/login.
- Two NEW exact HTTPS **GET-only partial-response** URLs (not the original unfiltered GET requests):
  `https://serviceusage.googleapis.com/v1/projects/38472235077/services/cloudkms.googleapis.com?fields=name%2Cstate`
  `https://serviceusage.googleapis.com/v1/projects/38472235077/services/identitytoolkit.googleapis.com?fields=name%2Cstate`
- Only `name` and `state` requested. Exact returned service resource identity must match project number and service name; `state` must be `ENABLED` or `DISABLED`. If permissions HTTP403/other error => `UNKNOWN_HTTP_*`; network error => UNKNOWN; unexpected JSON/size/identity => STOP, no retries. Response bound 8 KiB; no CryptoKeys, service configuration, signing, IAM grants, Auth users, Firebase/Firestore/Storage data, Cloud Run operations or resource writes.
- Saves only local sanitized API state and new one-shot marker under `/root`, `umask 077`, no OAuth or Google raw response uploads.
- Even a genuine `API_ENABLED` for both services does NOT solve the original KMS/Auth 403, select signing keys, or authorize H2; separate narrow error-reason investigation would be needed.

### ONE owner Ubuntu WSL root paste

```bash
umask 077
d=$(mktemp -d /root/oldx-h2f-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2f.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/f228b02cfbbbe4dab8d67cd5398615ca2e56408d/scripts/step05_h2_exact_two_api_states_fields_recovery_once_20261126.py' &&
test "$(git hash-object "$d/h2f.py")" = '362ffb697ab316e7ed3152cb613c3db5e35e8b6c' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2f.py" &&
python3 -B "$d/h2f.py" --h2-two-api-states-fields-only-once
```

Possible completion shape, **NOT an expected fact about states**:
```text
OLDX_H2F_RESULT=EXACT_TWO_API_STATES_FIELDS_ONLY_WITH_LIMITS
OLDX_H2F_KMS_API=API_ENABLED|API_DISABLED|UNKNOWN_...
OLDX_H2F_AUTH_API=API_ENABLED|API_DISABLED|UNKNOWN_...
OLDX_H2F_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2F_CLOUD_RESOURCE_WRITES=NONE
OLDX_H2F_DO_NOT_REPEAT=TRUE
```

On STOP, even if a partial GET may have occurred, preserve H2F marker and report `OLDX_H2F_*` only. Don't upload token, private SDK config, raw Google errors or local evidence. Nothing silently enabled, IAM-granted or changed.

## 3. Broader safety, no-repeat, and next decision

Previous H1B OFF-only Cloud Run four-probe test PASS, service deletion confirmed. One H1B no-key SA UID `115445220422157278526` **disabled, not deleted**, since 26 Nov 2026 22:14:17 IST; earliest separate dependency review 27 Nov 2026 22:14:17 IST, NOT automatic deletion. Older C1A residuals unchanged, H1B OFF image NOT eligible as H2 enabled image.

Full Step05 actual enabled seller/buyer Product lifecycle remains unverified. Three distinct H2 principals, dedicated KMS signing version, default-DB effective IAM/Auth, managed photo provider, durable budget/TTL cleanup, independent approval verifier and new enabled image provenance still need exact provider selection and separate finite pilot consent. `H2/PRODUCTION=NO_GO`.

Source references: https://docs.cloud.google.com/service-usage/docs/reference/rest/v1/services/get and https://docs.cloud.google.com/apis/docs/system-parameters .
