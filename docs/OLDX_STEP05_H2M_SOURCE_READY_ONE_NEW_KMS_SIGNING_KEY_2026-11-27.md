# BAJUTO / OLDX — Step05 H2M guarded signing-key creation SOURCE READY (not run)

**27 Nov 2026 IST.** Owner Task 27 H2L actual result (complete empty key-ring list for oldx-staging/asia-south1) remains authoritative: [H2L receipt](OLDX_STEP05_H2L_ACTUAL_ZERO_KMS_RINGS_H2M_APPROVAL_2026-11-27.md). Previous API activation H2K actual PASS; H2R/H2P/H2E/H2F/H2K/H2L are consumed; **never rerun**.

## New SOURCE-ONLY deliverable

- Exact file: scripts/step05_h2m_one_new_kms_signing_key_owner_approved_once_20261127.py
- Source commit (final code): dbe9de386f865d828aeb81d0ba61791d54f956dd
- Git blob readback: c6939b54eb54412bc4e23fdc2411cf962dcdb949
- **Prepared and GitHub-readback confirmed; NOT run in owner WSL, no cloud key resources created, no cloud resource write performed by this preparation.** No Python AST parse or Google KMS live verification claimed. Local static method allowlist checked; only two proposed POSTs.
- Owner WSL guards: exact Yasmin OAuth, root native WSL SDK in isolated config, exact oldx-staging project, H2K success marker + H2L root-owned saved metadata showing a complete zero-ring list. Fresh exact ring GET must return **404**; 403/other statuses STOP.
- **After separate explicit approval only:** exactly one new projects/oldx-staging/locations/asia-south1/keyRings/oldx-c2-h2-signing; exactly one cryptoKeys/oldx-c2-attestation-rs256 created with purpose ASYMMETRIC_SIGN, SOFTWARE, RSA_SIGN_PKCS1_2048_SHA256, single initial version.
- Exclusive /root/.oldx-step05-h2m-new-ring-key-one-create-once-20261127 marker created **before** first write; one POST ring + readback, then one POST key + key/version readback. On PENDING_GENERATION, bounded 12 GET-only checks; no extra version create; if still pending STOP and separately reconcile read-only, not retry.
- Local sanitized receipt (no credentials), fail-closed on unexpected identity, token, response, metadata, state, missing ring or partial result. Marker consumed even on partial write; never automatically delete/recreate.
- **Explicit non-scope:** no IAM grant/role, no signing, no public/private key fetch, no Run image/service, Firebase/Auth/Firestore/Storage, DNS, billing settings, H2 enablement, or production changes. H1B trial SA UID 115445220422157278526 remains disabled/not deleted.

## Owner exact H2M approval RECEIVED — execution still not attempted

This creation is NEW and billable, distinct from prior KMS API-only consent. One active SOFTWARE key version costs about **US$0.06/month plus key operations** (USD list; currency/taxes may differ). Keys/rings cannot simply be renamed. Owner explicitly replied **“ha manjuri chhe”** on 27 Nov 2026 to the proposal for exactly ONE new ring and ONE new key with ONE initial SOFTWARE RSA signing version in oldx-staging/asia-south1. This is the separate H2M consent that was previously missing; no further approval is required for these two exact creation requests and bounded verification, provided all source guards pass. The approval does NOT cover IAM, sign, deployment, activation, production or further key versions. Generic “continue” never widens this scope. Official docs: https://cloud.google.com/kms/pricing ; https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings/create ; https://docs.cloud.google.com/kms/docs/reference/rest/v1/projects.locations.keyRings.cryptoKeys/create ; https://docs.cloud.google.com/kms/docs/create-key .

**ONE paste under the now-explicit owner H2M approval** in existing owner Ubuntu WSL root prompt (not Windows SDK Shell; no new SDK install, Docker image or Cloud Shell work):

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2m-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2m.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/dbe9de386f865d828aeb81d0ba61791d54f956dd/scripts/step05_h2m_one_new_kms_signing_key_owner_approved_once_20261127.py' &&
test "$(git hash-object "$d/h2m.py")" = 'c6939b54eb54412bc4e23fdc2411cf962dcdb949' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2m.py" &&
python3 -B "$d/h2m.py" --owner-explicitly-approved-one-new-h2m-ring-and-key
~~~

Never repeat after marker, STOP, error, hang or ambiguous response. Preserve private WSL receipt; share only summarized OLDX_H2M_* output, not OAuth token or raw Google errors. A creation PASS does not imply successful KMS signing or hosted H2 acceptance.

## Remaining critical path

After actual verified H2M key creation, new read-only version/public SPKI pin followed by separately consented signer-only IAM, Firebase Auth config 403 resolution, distinct H2 runtime principals/Invoker/audiences, managed photo, durable nonce/budget + TTL, independent release approval, enabled image provenance, real hosted seller→buyer→edit→withdraw and rollback. Do not repeat 11 previous focused test groups or H1B frozen OFF image.

**Checkpoint:** H2M=OWNER_APPROVED_SOURCE_READY_NOT_EXECUTED; H2/PRODUCTION=NO_GO; branch=security-hardening-review; public brand=BAJUTO, internal IDs=OLDX; bajuto.in purchase not yet confirmed.
