# BAJUTO / OLDX Step05 — H2AG exact Owner approval, new guarded WSL runner READY (NOT EXECUTED)

Date: 28 Nov 2026, `security-hardening-review`.

## Owner's actual permission

After receiving proposal [H2AG exact reader identity and two read-only CryptoKey roles](OLDX_STEP05_H2AG_ONE_READER_IDENTITY_KEY_ONLY_IAM_OWNER_DECISION_2026-11-28.md), Owner replied **"ha manjuri chhe"**. Approval is **only** (1) ONE new `oldx-c2-kms-reader@oldx-staging.iam.gserviceaccount.com` SA, (2) `roles/cloudkms.viewer` and `roles/cloudkms.publicKeyViewer` ONLY on the already existing `projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256`, preserving the ONE existing signer `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com`, (3) exact readbacks/one-shot evidence. No other Cloud writes, signing, SA keys, production enable, media/Firebase/Run/Registry change, new key/version or project/ring IAM.

Direct current GCP execution is not available from this assistant, so one safe **owner WSL root** execution is required; NOT yet performed. Do not confuse GitHub push or local unit test with IAM grant PASS.

## Tested one-shot runner

- New `scripts/step05_h2ag_exact_reader_sa_two_key_roles_once_20261128.py`.
- Immutable creation commit `4cce529f8319eb415f9b3e4eeb378a70423b6774`; **Git blob `9ea97a0d0638962813a5d03b2942eac752a8cbf4`**.
- New `tests/integration/step05-h2ag-exact-reader-sa-two-key-roles-new.test.py` — Git blob `e9f3f0f33f2cb955deeb3a5e06ffc17fb7ea17da`.
- **7 NEW isolated Python offline tests PASS / 0 FAIL** on the exact local source byte copies: signer-only policy/version1+3, unexpected other roles/conditions/members rejected, two reader-only role payload preserving signer, omitted ProtoJSON disabled=false and UID drift, out-of-scope REST URL/method no network, full mocked one-create/one-IAM set & UID/ETag readbacks, post-marker create HTTP409 STOP with no IAM write. These are not actual Cloud tests. GitHub readback source + test SHA matched exact tested local Git hashes.
- Actual source has strict method/path/body allowlist. Owner-specific isolated Linux WSL gcloud SDK/config and prior successful H2R root-owned marker required. Read-only exact reader-account GET **404** + CryptoKey direct policy with exactly one signer-only binding and ETag required **BEFORE first mutation**. Root one-shot marker `/root/.oldx-step05-h2ag-one-reader-sa-two-key-only-roles-once-20261128` created with `O_EXCL|O_NOFOLLOW` before CREATE.
- Exactly one REST POST ServiceAccounts.create; require brand-new email, returned different 10–32 digit UID, disabled false (omitted default accepted), up to four bounded **GET by numeric UID** readback attempts (no create retry). Re-read ONLY exact CryptoKey IAM, demand unchanged preimage/ETag; one ETag-guarded key `:setIamPolicy` POST preserving existing signer and adding only the two new reader-only bindings, one fresh GET readback; retain private root evidence and sanitized receipt. No IAM write at project or ring.
- If account collision, conditional/other IAM policy binding, 403, 409, etag drift, network ambiguity or partial result: STOP. No automatic re-POST, rollback, delete, marker clear or rerun. If already-created account but IAM not granted, inspect exact UID/stage before separately authorized reconciliation. Production remains OFF.
- Official REST references: https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts/create ; https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys/setIamPolicy ; https://docs.cloud.google.com/iam/docs/roles-permissions/cloudkms.

## One owner WSL root command — execute exactly ONCE

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ag-approved.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ag.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/4cce529f8319eb415f9b3e4eeb378a70423b6774/scripts/step05_h2ag_exact_reader_sa_two_key_roles_once_20261128.py' &&
test "$(git hash-object "$d/h2ag.py")" = '9ea97a0d0638962813a5d03b2942eac752a8cbf4' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ag.py" &&
python3 -B "$d/h2ag.py" --h2ag-owner-approved-one-kms-reader-sa-and-two-key-only-read-roles-once
```

**Expected *only if Cloud succeeds*:**
```text
H2AG_MARKER=CONSUMED_NO_REPEAT
H2AG_READER_SA_UID_ENABLED=VERIFIED
H2AG_READER_READ_ONLY_KEY_ROLES_POST=VERIFIED
H2AG_KEY_READER_ROLES_READBACK=VERIFIED
H2AG_EXISTING_GATEWAY_SIGNER=PRESERVED_VERIFIED
H2AG_DO_NOT_REPEAT=TRUE
H2AG_RESULT=ONE_READER_SA_TWO_KEY_READ_ONLY_ROLES_PASS
```

As of this document: **OWNER_APPROVED / SCRIPT_PUSHED_AND_OFFLINE_TESTED / CLOUD_EXECUTION_NOT_YET_OBSERVED**. Await exact terminal screenshot; do not assert KMS GET/PEM working just because key-level IAM role write succeeded. Attached runtime reader workload, signed approval, immutable enabled images, Firebase/media/Firestore and authenticated hosted Seller–Buyer flow remain future independent gates. Step05 ACTIVE / Production OFF, NO-GO.
