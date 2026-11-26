# OLDX Step05 H2K ACTUAL PASS — next exact KMS signing-key metadata inventory (GET-only)

**27 Nov 2026 ~00:14 IST actual owner screenshot.** Repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Current authorized action was exactly one activation of `cloudkms.googleapis.com` on `oldx-staging`, project number `38472235077`.

## 1. H2K actual result — DONE, NEVER REPEAT

```text
OLDX_H2K_STAGE=ONE_OWNER_APPROVED_KMS_API_ENABLE_ATTEMPT
OLDX_H2K_PROJECT=oldx-staging
OLDX_H2K_SERVICE=cloudkms.googleapis.com
OLDX_H2K_ENABLE_ATTEMPTED=TRUE
OLDX_H2K_RESULT=PASS_KMS_API_ENABLED_EXACT_PROJECT_VERIFIED
OLDX_H2K_REASON=ONE_ENABLE_OPERATION_DONE_AND_KMS_ONLY_READBACK_ENABLED
OLDX_H2K_FINAL_KMS_API_STATE=ENABLED
OLDX_H2K_OTHER_RESOURCES_IAM_KEYS=NOT_CHANGED_BY_SCRIPT
OLDX_H2K_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2K_DO_NOT_REPEAT=TRUE
```

Full exact owner receipt: [H2K enabled actual PASS](OLDX_STEP05_H2K_ACTUAL_KMS_API_ENABLED_2026-11-27.md). H2K one-shot marker `/root/.oldx-step05-h2-kms-api-enable-owner-once-20261127` is consumed. Do **not** rerun Service Usage enable, H2F/H2E/H2P/H2R, earlier W6SA/H1A/H1B/old G1/Registry or Codex old tests.

## 2. New H2L read-only post-enable metadata — SOURCE READY, NOT OWNER EXECUTED

Prior KMS `keyRings.list` HTTP403 occurred while the **KMS API was disabled**. This changed materially upon Owner H2K activation, so a NEW bounded KMS metadata inventory is justified without repeating the old H2R one-shot.

New script `scripts/step05_h2_kms_post_enable_ring_key_metadata_once_20261127.py`.

- **Pinned commit**: `f9ea10cfd8c5fcde89c02ed7d6c704de5f990ce0`
- **Verified Git blob**: `e95594640a4b71d8fd9390d6684d77f004d4ef97`
- Existing isolated native Owner WSL / `oldx-staging`; requires exact consumed successful H2K marker (not a repeat API state query). New one-shot marker `/root/.oldx-step05-h2-postenable-kms-rings-keys-readonly-once-20261127`.
- **Only GET**: one `cloudkms.googleapis.com/v1/projects/oldx-staging/locations/asia-south1/keyRings?pageSize=100`; on a complete visible, unpaginated response with **up to 3 rings**, perform one `cryptoKeys?pageSize=25` metadata GET per exact ring. Reports ring names, counts and `purpose=ASYMMETRIC_SIGN` key names if complete.
- Strict URL, project and region scope, key ring/key name validation, HTTPS, bounded response size/network timeout, no redirects/retries, no resource writes.
- `HTTP403/other error`, network timeout or pagination = **UNKNOWN/PARTIAL**, never "no keys". >3 rings is a bounded intentional partial scope and no key listing; keys beyond a first page of 25 cannot be counted as absent.
- Does NOT list CryptoKeyVersions or inspect key states/algorithms beyond `purpose`. Does NOT sign, fetch public/private key material, create key rings/keys/versions, change IAM, invoke Firebase/Auth/Cloud Run, change billing, or enable H2. A ring/key name listed is only a candidate, NOT permission to use it.
- Privately stores sanitized metadata in `/root/oldx-h2-kms-metadata-<UTC>/`, with `umask 077`; no OAuth tokens or raw Google error messages sent to GitHub. GitHub contains source and owner-supplied sanitized results only.
- Script read back from GitHub, static guard inspection passed; **Python AST parse/runtime API call NOT YET VERIFIED**. A single Owner paste below runs syntax check then exact new one-shot.

### One owner paste in existing Ubuntu WSL root prompt

```bash
umask 077
d=$(mktemp -d /root/oldx-h2l-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2l.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/f9ea10cfd8c5fcde89c02ed7d6c704de5f990ce0/scripts/step05_h2_kms_post_enable_ring_key_metadata_once_20261127.py' &&
test "$(git hash-object "$d/h2l.py")" = 'e95594640a4b71d8fd9390d6684d77f004d4ef97' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2l.py" &&
python3 -B "$d/h2l.py" --h2-postenable-kms-rings-and-signing-key-metadata-once
```

Illustrative output **shape only, not a live claim**:
```text
OLDX_H2L_RESULT=KMS_POST_ENABLE_METADATA_READ_WITH_LIMITS
OLDX_H2L_RING_LIST=COMPLETE_VISIBLE_PAGE|PARTIAL_PAGINATED|UNKNOWN_HTTP_...
OLDX_H2L_RING_COUNT=...                # only if complete
OLDX_H2L_RING_NAMES=...                # only if complete
OLDX_H2L_KMS_KEY_OR_VERSION_CREATED=FALSE
OLDX_H2L_RESOURCE_WRITES=NONE
OLDX_H2L_H2_ENABLED=NOT_ATTEMPTED
OLDX_H2L_DO_NOT_REPEAT=TRUE
```

On `STOP` or `UNKNOWN`, DO NOT re-execute H2L or clear any marker. If a complete list is empty in exactly `asia-south1`, propose one dedicated H2 signing ring/key with **new explicit owner approval**. If an `ASYMMETRIC_SIGN` candidate appears, next NEW stage needs version/algorithm/status plus independent public-key pin and least-privilege signer-only authority, still no key use yet. When KMS list shows 403 after enable, diagnose sanitized IAM policy/error reason before any permission request.

## 3. Separate open gates / no accidental GO

Identity Toolkit API was already ENABLED; Firebase Auth config GET403 remains unresolved, independent of KMS. Media Storage listing previously returned zero project buckets but no globally exhaustive provider proof. No new runtime identities, live KMS managed signing, Firebase least-privilege acceptance, durable atomic budget/nonce TTL cleanup, approval verifier or enabled-image provenance. **H2 and production stay NO-GO.**

H1B old trial SA UID `115445220422157278526` remains disabled not deleted; 24h post-disable review starts 27 Nov 2026 22:14:17 IST, not automatic SA deletion.

Official GET-only KMS docs: https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings/list ; https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys/list .
