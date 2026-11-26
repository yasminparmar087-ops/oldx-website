# OLDX Step05 H1B — Owner W3V actual PASS, one-session private OFF Cloud Run + guarded service cleanup

**26 November 2026, owner screenshot ~22:00 IST.** Repository `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. Latest new stage here; old G1/G2A/G2B/W0/W1 and W3V one-shots MUST NOT repeat.

## Actual latest screenshot (W3V)

Owner launched commit-pinned `scripts/step05_h1b_w3_off_private_validate_only_once_20261126.py`, initial commit `8679d110ea36b9706129a00c742676afa5f46ce7`, source blob `62ca63d02167c3b8988759cc4cf6891d0213326e`.

```text
H1B_W3V_NEW_SA_UID=FROZEN_MATCH
H1B_W3V_NEW_SERVICE=ABSENT_404_BEFORE_VALIDATE
H1B_W3V_IMAGE=FROZEN_REMOTE_G2B_DIGEST
H1B_W3V_RESULT=VALIDATE_ONLY_ACCEPTED_WITH_LIMITS
H1B_W3V_REASON=NEW_PRIVATE_OFF_CLOUD_RUN_CONFIG_VALIDATED_NO_CREATION
H1B_W3V_CLOUD_RESOURCE_WRITES=NONE
H1B_W3V_NEW_CLOUD_RUN_SERVICE=NOT_CREATED
H1B_W3V_DO_NOT_REPEAT=TRUE
```

**Interpretation:** Google's `create?validateOnly=true` accepted the proposed private compiled-OFF service configuration but created **NO Cloud Run service**. This does not verify successful future deployment, invoker/IAM policies, runtime health or cleanup. W3V marker `/root/.oldx-h1b-w3-private-validate-only-once-20261126` is **CONSUMED**. The NEW no-key runtime SA already actually exists from W1 with immutable UID `115445220422157278526`. Frozen image already in Mumbai Registry after ONE owner G2B push, `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`.

## W3/W4/W5/W6 owner consent already explicitly granted; new one-session script prepared

Owner `ha manjuri chhe` approved ONE supervised private/OFF/no-real-user-data staging experiment covering one NEW Cloud Run service in `oldx-staging/asia-south1`, optional **Yasmin-only** service-level invoker, up to 4 specific H1B-only HTTP probes, same-session **new-only** guarded cleanup and no risk of changes to old resources. Known H1A 12 HIGH CVE risk accepted ONLY for this private OFF experiment of less than 24h, not production/H2. No Firebase/Auth/Firestore/media/provider data, default-deny Rules unchanged, no older C1A image/SA or `oldx-owner-read` changes, no shareable public access.

New SOURCE-ONLY file, **not executed on owner WSL**:
`scripts/step05_h1b_w3_w6_new_only_one_session_20261126.py`.
- **Pinned final source commit:** `9c6484836fbdd720ffe18659bc4b31ffd2264596`
- **Exact verified Git blob SHA:** `cb588678a1756fbc36cbd0b6a036c62b68f87858`
- One-shot marker: `/root/.oldx-h1b-w3w6-private-off-once-20261126`. Used once if a new service CREATE is attempted, never clear/re-run on failure or success.
- Requires original isolated Yasmin OAuth principal, `oldx-staging`, exact W1 SA UID and success marker, W3V validateOnly marker and frozen G2B digest; rechecks exact NEW service 404 just before create, SA uniqueId, project Run create/delete/get/setIamPolicy and resource-level SA actAs/delete. No re-run of broad old IAM scans or old image tests.
- Generates a fresh high-entropy session label `oldx-session`; creates exactly ONE NEW private Cloud Run service `oldx-c2-website-mediator` with the previously validated template, immutable remote image, identity `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com`, min0/max1, CPU1/512Mi, timeout5s, concurrency1, port8080, IAM check enabled. `ingress=INGRESS_TRAFFIC_ALL` permits supervised external HTTP probes **but is not public IAM access**.
- Handles long-running create Operation with bounded same-session GET polling; exact service `uid`, `etag`, session label, runtime SA, image and settings must match. Reads initial new-service direct IAM: must have **no bindings**. Grants just `roles/run.invoker` to `user:yasminparmar087@gmail.com` on the **NEW service only** and independently reads back the exact single binding; never project-wide roles and never `allUsers` or `allAuthenticatedUsers`.
- Up to **four** new-service-only HTTP probes, no retry: anonymous GET `/health` must 403, owner ID-token GET `/health` must 200, owner POST `/api/staging/marketplace/owner` must 503, owner GET `/unmatched-oldx-h1b-path` must 404. If actual Owner ID token not available or HTTP status differs, service cleanup still attempted. No real or synthetic user/data calls.
- **Finally SAME SESSION**: attempts one exact NEW-service-only `DELETE ?etag=<fresh-etag>` after validating new service UID/label/image/SA/direct IAM, waits for operation, confirms GET 404. Even if create response was partial, it may safely recover only if its unpredictable session label and exact returned UID/creator/properties prove the new service belongs to this attempt; never delete on name alone. Uncertain identity, IAM, auth, network, operation or etag => `STOP_MANUAL_RECOVERY`, resource might remain; preserve private evidence and DO NOT retry this one-shot. Execution is synchronous, **no autonomous timer or guaranteed cleanup if owner closes WSL/session or connection fails**.
- **New W1 SA is retained after service cleanup** until its use in other services/regions and references can be separately verified; immediate SA deletion is not unconditionally safe even if the service is gone. Existing G2B image remains in existing shared Registry as is; no second push, no image deletion. W6 final SA cleanup remains separate, dependent on exact resource-reference checks. A successful same-session service cleanup is **not** complete Step05 closure unless SA residual is addressed.
- Private WSL evidence `/root/oldx-h1b-w3w6-<session>` and consumed marker persist. Script does not upload tokens or IAM credentials to GitHub. Source was verified by GitHub readback and static safety invariant checks; **actual Python parsing and Cloud behavior in Owner WSL remain unverified until execution**. Operator bootstrap uses `ast.parse` before invoking. No assistant-issued Cloud writes.

## ONE owner paste — same existing Ubuntu WSL root prompt, no heredoc

```bash
umask 077
d=$(mktemp -d /root/oldx-h1b-w3w6-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/w3w6.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/9c6484836fbdd720ffe18659bc4b31ffd2264596/scripts/step05_h1b_w3_w6_new_only_one_session_20261126.py' &&
test "$(git hash-object "$d/w3w6.py")" = 'cb588678a1756fbc36cbd0b6a036c62b68f87858' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/w3w6.py" &&
python3 -B "$d/w3w6.py" --w3-w6-private-off-single-session-once
```

Expected successful outcome if Cloud Run deploy, private IAM/ID token/HTTP and same-session NEW service deletion all work:
```text
H1B_W3W6_SERVICE_CLEANUP=NEW_ONLY_RUN_SERVICE_DELETED_CONFIRMED
H1B_W3W6_HTTP_PROBES_ATTEMPTED=4
H1B_W3W6_SA_CLEANUP=RETAIN_PENDING_DEPENDENCY_GUARDS
H1B_W3W6_RESULT=PASS_PRIVATE_OFF_FOUR_PROBES_AND_SERVICE_DELETED_SA_RETAINED
H1B_W3W6_DO_NOT_REPEAT=TRUE
```

Even with fewer than 4 probes or any failure, examine sanitized `H1B_W3W6_SERVICE_UID`, `SERVICE_CLEANUP`, `RESULT`, `REASON` carefully. **If `STOP_MANUAL_RECOVERY...` or service cleanup not explicitly `NEW_ONLY_RUN_SERVICE_DELETED_CONFIRMED` or `NEW_SERVICE_ABSENT_404_NO_DELETE_NEEDED`, stop immediately and provide sanitized status for new-only guarded manual recovery. NEVER rerun this command, reset marker or blindly delete.** If the service remains running, plan short urgent read-only/guarded deletion; do not assume it was removed or promise 24h automation. The SA is expected to remain.

## Next after real owner output
1. If new Cloud Run service deletion actually confirmed, separately guarded NEW-SA dependency check and eventual removal/disable of exact UID `115445220422157278526`; keep immutable image in shared registry unless exact unreferenced status proven.
2. If any stop after actual create, prioritize safe guarded new-only service readback and cleanup before other OLDX work; no second Cloud Run create.
3. H2/production remains NO-GO; Step05 not yet considered complete solely from dry-run.

Google current official Cloud Run create/delete/operations and IAM documentation:
https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/create
https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/delete
https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.operations/get
https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/getIamPolicy
https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/setIamPolicy
