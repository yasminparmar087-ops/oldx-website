# BAJUTO / OLDX Step05 H2W — Owner-approved ONE new internal-only Cloud Run H2 Gateway OFF service

**27 November 2026, after H2V actual PASS. Branch `security-hardening-review`.** The owner said **"ha manjuri chhe"** to creating **one new private/default-OFF Cloud Run staging service**, verifying exact service identity and IAM, and optionally adding exactly one Owner Invoker binding. This is a NEW approval; it does **not** cover KMS, Firestore, public access or Production.

## Accepted predecessor H2V — NEVER REPEAT

- One new H2U image was successfully built locally, verified Node24.22.3 UID65532 HTTP 200 OFF/503 Disabled/404, then pushed **once** to existing private Artifact Registry `oldx-staging-images` in `asia-south1`.
- Owner H2V output: `H2V_RESULT=PASS_REMOTE_FROZEN_DIGEST_VERIFIED`, `H2V_PUSH_ATTEMPTED=TRUE`, exact immutable OCI index `sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2`, amd64 child `sha256:c165e671e2b231b5b6210f867dacc085d4a53b69fae2998a712019d9b6575243`, config `sha256:56b7a9601702e80286c80089e33fe13049b6fa7d3fbbcb98e4f775c9d31ace25`. Tag `h2v-off-20261127-793639b6b8d15e55ea4a` is not a deployment selector. [Canonical Owner H2V upload PASS](OLDX_STEP05_H2V_ONE_PRIVATE_REGISTRY_PUSH_ACTUAL_PASS_2026-11-27.md).
- All prior one-shot source tests/import/ESM, base Cosign, local build, H2V upload, H2S/H2T/H2N/H2R and H1B experiments are **consumed**; don't rerun, reset markers, rebuild, repush, rescan unrelated images or repeat old IAM inventories.

## Exactly approved H2W target and boundaries

| Property | Exact new deployment scope |
| --- | --- |
| Project/region | `oldx-staging` / `asia-south1` |
| NEW Cloud Run service name | `oldx-c2-h2-private-gateway` (must be fresh GET 404 before first write) |
| Service account | `oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com` |
| Verified expected SA UID | `107238619872767759560` (must freshly match IAM API) |
| NEW service-only image | `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-h2-gateway-off@sha256:4b1bd8a5cba33e96969f8f92ebd73b73f281b6ca5279fd2b14d3be8e9a5391f2` |
| Cloud Run ingress | **`INGRESS_TRAFFIC_INTERNAL_ONLY`**; never internet-all or external load-balancer ingress |
| Authentication | `invokerIamDisabled=false` (IAM Invoker check enabled), exactly one **new-service-only direct** `roles/run.invoker` binding to `user:yasminparmar087@gmail.com` after create |
| Limits | min instances 0; max 1; concurrency 1; 1 vCPU, 512 MiB; timeout 5s; port 8080; CPU idle, no startup boost |
| Runtime | OFF-only H2 gateway; `OLDX_H2U_MODE=OFF`, `NODE_ENV=production`, no secrets/KMS/Firestore provider enablement |
| No other actions | No second image build/push, registry writes, old Cloud Run update, other IAM modifications, SA/keys, Firebase, Firestore, KMS or Production |

**Security nuance:** Cloud Run Internal-only ingress and IAM are distinct layers. A desktop WSL client on public internet is not an allowed internal source, **even if Owner-authenticated**. Therefore this command does **NOT** probe HTTP from WSL and does not claim 403/200/503/404 hosted requests. Instead it verifies service/revision template and its **direct IAM policy readback only**. Inherited project/folder/org-level Invoker grants are **not exhaustively verified**; internal ingress still prevents direct public internet traffic. Official Google [Cloud Run ingress](https://docs.cloud.google.com/run/docs/securing/ingress) and [Service IAM](https://docs.cloud.google.com/run/docs/securing/managing-access).

## NEW source-only H2W runner, NOT EXECUTED

`scripts/step05_h2w_one_new_internal_off_gateway_cloudrun_owner_once_20261127.py`
- **Git creation commit:** `d11f5c29c98b3e051bba77e117a0369a587fabe1`
- **Verified source Git blob SHA1:** `32f0422b0bd451753f1560a91c63938bec2b1a1c`
- Built from the **previously proven** H1B W3–W6 bounded REST/Owner login/operation machinery, with **new separate target**, **new marker**, strict allowlist (POST only new Cloud Run create, project `testIamPermissions`, SA `testIamPermissions`, and new service `setIamPolicy`; GET exact SA/service, IAM policy and this region's operation). **No DELETE/PATCH/PUT, no HTTP probe or prior script execution.**
- Root Ubuntu WSL with existing separate native SDK + isolated Owner auth only. Preflight: expected Owner active, project correct; prior H2V successful one-shot receipt matching **exact tag**; no old script re-execution; Gateway SA IAM GET exactly email/UID/enabled; target service GET **exact 404**; project run.services.create/get/delete/setIamPolicy/getIamPolicy rights and exact SA `actAs`. Missing/unknown gives STOP **before marker or Cloud write**. Right before first create, a second **same target GET 404** guards collision.
- Creates distinct durable marker `/root/.oldx-step05-h2w-new-internal-off-cloudrun-service-once-20261127` and private evidence first. Then **one** create attempt for exactly `oldx-c2-h2-private-gateway`, immutable image by DIGEST. Polls this new operation, GET checks service full name, UID, session label, internal-only ingress, IAM enforcement, SA identity, exact image, OFF env, limits and etag. If the default direct service IAM has unknown bindings, **STOP without granting**.
- Exactly one optional (approved) Owner-only **direct** IAM `setIamPolicy` guarded by initial etag. Confirms new-service-only policy exactly one `roles/run.invoker` binding to Yasmin, no `allUsers`/allAuthenticatedUsers direct; readback service must preserve all constraints and UID. **Do not claim this is full inherited IAM audit.**
- Retains the new service for subsequent staging; records `uid`, `etag`, session label and operation in root-private evidence for later UID/etag-guarded rollback. **No automatic delete on failure or success** (partial creation can be ambiguous). Stop after marker/any create/write requires fresh read-only reconciliation, not retry or blind deletion.

### ONE NEW Owner WSL root command (only once)

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2w-private-run-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/deploy.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/d11f5c29c98b3e051bba77e117a0369a587fabe1/scripts/step05_h2w_one_new_internal_off_gateway_cloudrun_owner_once_20261127.py' &&
test "$(git hash-object "$d/deploy.py")" = '32f0422b0bd451753f1560a91c63938bec2b1a1c' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/deploy.py" &&
python3 -B "$d/deploy.py" --h2w-owner-approved-one-internal-off-gateway-service-create-once
~~~

**Result expectations only after Owner execution:**

~~~text
H2W_CREATE_ATTEMPTED=TRUE
H2W_IAM_WRITE_ATTEMPTED=TRUE
H2W_OWNER_INVOKER=EXACT_OWNER_ONLY_DIRECT_BINDING_VERIFIED
H2W_INGRESS=INTERNAL_ONLY
H2W_HTTP_PROBES=NOT_ATTEMPTED_INTERNAL_ONLY
H2W_RESULT=PASS_NEW_INTERNAL_OFF_SERVICE_AND_OWNER_DIRECT_INVOKER_WITH_LIMITS
H2W_H2_PRODUCTION=NO_GO
H2W_DO_NOT_REPEAT=TRUE
~~~

The script prints exact new service UID and root-private receipt path. **Do not claim PASS now**, no Cloud Run deployment yet observed. If `H2W_RESULT=STOP_BEFORE_CLOUD_WRITES`, no create happened. After `H2W_CREATE_ATTEMPTED=TRUE` or new marker exists, **never rerun**, even if IAM step fails, because partial service could remain. Never share OAuth tokens or auth config.

## Next H2 after a real H2W PASS

Preserve fresh service UID+etag and readback. A new **private network-origin** HTTP test (not WSL public internet), inherited IAM review, Cloud Run service agent access and future new provider wiring, with separate approvals, remain. KMS status reader, atomic Firestore one-sign budget/no TTL, single bounded synthetic KMS sign and derived image risk acceptance do **not** become done by Cloud Run default-OFF service creation. Any later cleanup/rollback must target only this newly created UID/session/etag and requires a separately reviewed command, no shared/old resource deletion.

**Checkpoint:** `H2V_REGISTRY_PUSH=ACTUAL_PASS_CONSUMED`; `H2W_INTERNAL_OFF_CLOUD_RUN=OWNER_APPROVED_SOURCE_READY_NOT_EXECUTED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.

## 27 Nov 2026 ~23:13 IST — First H2W source superseded
Owner first run STOP_BEFORE_CLOUD_WRITES because the 19-hex predecessor H2V tag was mistranscribed; no Cloud Run create or IAM write. The corrected and ONLY permitted next source is `scripts/step05_h2w_one_new_internal_off_gateway_cloudrun_receipt_tag_fix_once_20261127.py`, commit `e55857f4600f2a152a93fdc3ac1bec201bed7cad`, blob `a6986708b2fe0ac67aa214b544ca977244cf131d`. Actual predecessor H2V tag is the corrected 20-hex tag above. **Never rerun the original H2W script.** Follow [canonical STOP/fix and one command](OLDX_STEP05_H2W_PREBUILD_H2V_RECEIPT_TAG_TYPO_STOP_FIX_2026-11-27.md). One H2W owner-approved Cloud create attempt remains unused.
