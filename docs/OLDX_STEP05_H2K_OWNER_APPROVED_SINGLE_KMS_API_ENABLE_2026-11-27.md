# OLDX Step05 H2K — exact OWNER APPROVAL to enable ONLY Cloud KMS API in oldx-staging

**27 Nov 2026 IST.** Owner's actual reply: `ha manjuri chhe` to the explicit question **"શું તમે માત્ર Cloud KMS API ચાલુ કરવાની મંજૂરી આપો છો?"** This authorization is scoped **only** to activating `cloudkms.googleapis.com` in `oldx-staging`, project number `38472235077`. No approval to create key rings, keys, versions, IAM grants, sign data, build/deploy Cloud Run, enable H2, change Auth/Firestore/Storage/billing or production. Source and operation must fail closed and preserve previous evidence.

## Evidence before authorization (DO NOT REPEAT)

Owner's actual H2F screenshot from 26 Nov ~23:24 IST:
```text
OLDX_H2F_RESULT=EXACT_TWO_API_STATES_FIELDS_ONLY_WITH_LIMITS
OLDX_H2F_KMS_API=API_DISABLED
OLDX_H2F_AUTH_API=API_ENABLED
OLDX_H2F_CLOUD_RESOURCE_WRITES=NONE
OLDX_H2F_DO_NOT_REPEAT=TRUE
```

This was two `?fields=name,state` Service Usage GETs, not a resource write. All H2F/H2E/H2P/H2R one-shot markers are CONSUMED; never reset or re-run them, nor prior H1A/G1/G2A/G2B/W0/W1/W3V/W3–W6/W6SA/C2 Origin/Codex tests. Exact H2F prior marker: `/root/.oldx-step05-h2-exact-two-states-fields-only-once-20261126`. Prior sanitized H2F local evidence contains the project and both API states, is NOT uploaded to GitHub. The new script validates it before touching the Cloud.

## New H2K source — SOURCE READY; NOT EXECUTED BY OWNER

`scripts/step05_h2_kms_api_enable_one_approved_once_20261127.py`

- Pinned source commit: **`85b9cfd8991c15d719959f6cfcf223c84bec778d`**
- GitHub-readback exact blob SHA: **`3104edcca5fa81943186da72d58be95b8c81e426`**
- NEW one-shot marker: `/root/.oldx-step05-h2-kms-api-enable-owner-once-20261127`. Never delete/reset/retry if consumed.
- The script checks existing isolated native `OLDX-Ubuntu-24.04` WSL Owner `yasminparmar087@gmail.com`, exact Cloud SDK and project `oldx-staging` before any write. Reads original H2F **successful** marker and sanitized local proof KMS `API_DISABLED`, Identity Toolkit `API_ENABLED`, WITHOUT rerunning old two GETs.
- It makes one fresh **KMS-only** read-only `Service Usage GET .../projects/38472235077/services/cloudkms.googleapis.com?fields=name%2Cstate` to prevent stale-state/race risk. If KMS is already ENABLED, prints `ALREADY_ENABLED_NO_WRITE` and stops without POST. If KMS remains DISABLED, **one** Owner-authorized `POST .../services/cloudkms.googleapis.com:enable` with EMPTY body, no other APIs specified; first writes a separate immutable one-shot marker to local disk.
- If API responds with a long-running operation, script validates exact `operations/*` name, performs bounded **GET-only** polling (max 12 × 3 seconds delay) and a single exact filtered readback GET to confirm `API_ENABLED`. No automatic retry on timeout or ambiguous post-write error, no attempted rollback by disabling. Successful readback state is necessary for PASS.
- Local sanitized log and marker retained under `/root/oldx-h2k-kms-api-owner-enable-<UTC>/` with `umask 077`; OAuth token stays in Python memory, no raw API responses or key material uploaded to GitHub.
- New source statically inspected: target exact KMS, project number and owner/previous marker gates, one POST site, only operation/known-URL GETs, no IAM key/deployment branch, no H2 activation. Actual Python AST parse and external API operation have **NOT BEEN EXECUTED** by assistant. No claim of successful API enablement until Owner's screenshot.
- Google official REST `services.enable` requires `serviceusage.services.enable` and returns a long-running `Operation`. Source: https://docs.cloud.google.com/service-usage/docs/reference/rest/v1/services/enable . `operations.get`: https://docs.cloud.google.com/service-usage/docs/reference/rest/v1/operations/get . Enabling APIs can enable subsequent billable API usage under existing billing, even though no actual CryptoKey is created by this script: https://docs.cloud.google.com/service-usage/docs/enabled-service .

## ONE exact Owner WSL root paste

```bash
umask 077
d=$(mktemp -d /root/oldx-h2k-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2k.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/85b9cfd8991c15d719959f6cfcf223c84bec778d/scripts/step05_h2_kms_api_enable_one_approved_once_20261127.py' &&
test "$(git hash-object "$d/h2k.py")" = '3104edcca5fa81943186da72d58be95b8c81e426' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2k.py" &&
python3 -B "$d/h2k.py" --approved-single-kms-api-enable-once
```

Potential confirmed successful status:
```text
OLDX_H2K_PROJECT=oldx-staging
OLDX_H2K_SERVICE=cloudkms.googleapis.com
OLDX_H2K_ENABLE_ATTEMPTED=TRUE
OLDX_H2K_RESULT=PASS_KMS_API_ENABLED_EXACT_PROJECT_VERIFIED
OLDX_H2K_FINAL_KMS_API_STATE=ENABLED
OLDX_H2K_OTHER_RESOURCES_IAM_KEYS=NOT_CHANGED_BY_SCRIPT
OLDX_H2K_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2K_DO_NOT_REPEAT=TRUE
```
This is a **prediction of output shape**, not measured. If API already ENABLED, no actual enable POST will be attempted (`ALREADY_ENABLED_NO_WRITE`). A `STOP` after a POST can mean the API enable eventually succeeds; NEVER rerun this one-shot, clear its marker or manually send an unguarded second enable. Share only `OLDX_H2K_*` sanitized lines. The new step is a real API service activation (a project write), not a source-only test.

## Separate next gates after actual result

Only after genuine exact KMS enabled readback, choose a **new** KMS key ring/ASYMMETRIC_SIGN version metadata inventory, with explicit scope and permission/identity review; `identitytoolkit.googleapis.com` already enabled and earlier Auth config GET HTTP403 still needs a separate narrow diagnosis. Distinct runtime principals, approved moderated media, durable nonce/TTL cleanup, independent owner approval verifier, new enabled image security/rollback and true hosted Product seller/buyer acceptance remain OPEN. No H2/production live GO.

H1B old trial runtime SA UID `115445220422157278526` remains DISABLED NOT DELETED since 26 Nov 22:14:17 IST. Earliest separate post-24-hour dependency review 27 Nov 22:14:17 IST, not a deletion instruction. Do NOT touch it as part of this enable.

**State now:** `OWNER_H2K_ENABLE_CONSENT=GRANTED_EXACT_ONE_API`; `H2K_SCRIPT=SOURCE_READY_NOT_OWNER_RUN`; `CLOUD_KMS_API=DISABLED_AT_LAST_VERIFIED_H2F_SNAPSHOT`; `IDENTITY_TOOLKIT_API=ENABLED_AT_LAST_H2F`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
