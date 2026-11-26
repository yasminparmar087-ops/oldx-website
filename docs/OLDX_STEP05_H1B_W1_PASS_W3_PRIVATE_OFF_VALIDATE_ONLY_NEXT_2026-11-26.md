# OLDX Step05 H1B — actual W1 SA UID PASS; W3 Cloud Run private OFF validateOnly source

**26 Nov 2026 IST**. Repo `yasminparmar087-ops/oldx-website`, branch `security-hardening-review`. This is the latest owner handoff and supersedes older records that said W1 is pending.

## Actual Owner W1 checkpoint — do not repeat
Owner Windows/Ubuntu WSL screenshot contains:
```text
H1B_W1_STAGE=ONE_APPROVED_NEW_SA_CREATE_ATTEMPT
H1B_W1_SA_UID=115445220422157278526
H1B_W1_SA_CREATE_ATTEMPTED=TRUE
H1B_W1_RESULT=NEW_NO_KEY_SA_CREATED_RIGHTS_PASS_WITH_LIMITS
H1B_W1_REASON=SA_UID_READBACK_AND_ACTAS_DELETE_PASS
H1B_W1_CLOUD_RUN_DEPLOY=NOT_ATTEMPTED
H1B_W1_IAM_BINDINGS_AND_KEYS=NONE_CREATED_BY_THIS_SCRIPT
H1B_W1_DO_NOT_REPEAT=TRUE
```
One new user-managed no-key runtime Service Account `oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com` was actually created and read back; **frozen numeric uniqueId 115445220422157278526**. The W1 code did not create any custom keys, IAM bindings, Cloud Run revision or endpoint. Its one-shot marker remains consumed. Detailed [actual W1 proof](OLDX_STEP05_H1B_W1_OWNER_ACTUAL_PASS_SA_UID_AND_NEXT_W3_W6_2026-11-26.md).

Earlier verified G2B remote immutable image:
`asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-off@sha256:576a1faa599459ed9b1cdeccc01a3adc2076dffff617bec42f38df7d3a75663e`.
The former image build, SBOM/Grype, local smoke, one Registry push, G1/G2A, W0 and W1 are consumed and MUST NOT be repeated. Existing C1A old service removed; C1A leftover SA/image, shared Registry, Firebase, old owner-read and production untouched.

## Owner approved W1–W6 scope

Owner already granted `ha manjuri chhe` for one finite supervised private IAM-protected compiled-OFF/no-user-data H1B experiment in `oldx-staging` `asia-south1`, new SA and service only; optional owner-only service-level Invoker, up to 4 new-service HTTP probes and same-session UID-guarded NEW-only cleanup. Known 12 HIGH CVE accepted only for private/OFF/test max24h. No public roles, real data, Firebase Rules, H2 or production.

## Why W3 validateOnly before real deployment

Google's official Cloud Run v2 create endpoint supports `?validateOnly=true`: server validates the proposed Service and supplies defaults **without persisting any Service or creating resources**. This new check is not a re-run of W0 or W1; it verifies the exact NEW Cloud Run template and fresh new-SA identity before a billable deployment. Cloud Run actual create/delete are long-running operations; guarded same-session cleanup needs exact new `uid` and `etag`. Official: https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/create and https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services/delete . Cloud Run IAM must remain enforced: https://docs.cloud.google.com/run/docs/securing/managing-access .

## New W3V source-only runner — NOT executed on Owner WSL

`scripts/step05_h1b_w3_off_private_validate_only_once_20261126.py`

- Pinned initial commit: `8679d110ea36b9706129a00c742676afa5f46ce7`
- Exact GitHub-readback blob SHA: `62ca63d02167c3b8988759cc4cf6891d0213326e`
- Distinct one-shot marker: `/root/.oldx-h1b-w3-private-validate-only-once-20261126` (never reset/rerun after a real validation attempt).
- Only existing native `OLDX-Ubuntu-24.04` root and isolated Yasmin `gcloud` OAuth config. Requires success markers from existing frozen W1 UID and G2B digest. No fresh SDK install, login, Docker build, Registry push, old service probes, global IAM change.
- Performs SA exact-UID GET, new Run service absence GET 404, scoped Run create/delete/get/setIamPolicy `testIamPermissions` (read-only HTTP POST). These are **new W3 safety checks**, not rerun of W0/G1.
- Posts **only** to `https://run.googleapis.com/v2/projects/oldx-staging/locations/asia-south1/services?serviceId=oldx-c2-website-mediator&validateOnly=true` with immutable remote image and new SA identity. Payload: `ingress=INGRESS_TRAFFIC_ALL` (network reachability needed for supervised probes, **NOT public IAM**), `invokerIamDisabled=false`, min0/max1, cpu1/memory512Mi, request CPU idle, concurrency1, timeout5s, port8080, gen2; compiled OFF image. No owner keys/env/providers/Firebase/Firestore data, no real service creation.
- A 200 validation response without `error` leads to `H1B_W3V_RESULT=VALIDATE_ONLY_ACCEPTED_WITH_LIMITS`; this does **not** prove deployment readiness, runtime health, IAM effectiveness or cleanup success. Any status 403/unknown/HTTP failure STOP; no automatic retries. Saves only proposed request to private Owner WSL evidence directory; no sensitive credentials printed or uploaded.
- A real Cloud Run service, IAM grant, hosted probes and cleanup are all still **NOT EXECUTED** at this checkpoint, and need the actual validateOnly owner result to assemble a tested guarded W3–W6 execution packet. No new extra owner approval is required within the existing explicit bounded consent.

### ONE paste in current Ubuntu WSL root prompt (not Cloud Shell)
```bash
umask 077
d=$(mktemp -d /root/oldx-h1b-w3v-source.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/w3v.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/8679d110ea36b9706129a00c742676afa5f46ce7/scripts/step05_h1b_w3_off_private_validate_only_once_20261126.py' &&
test "$(git hash-object "$d/w3v.py")" = '62ca63d02167c3b8988759cc4cf6891d0213326e' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/w3v.py" &&
python3 -B "$d/w3v.py" --w3-off-private-validate-only-once
```

Expected successful limited status:
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

If `STOP_PREFLIGHT`, no validate request attempted; if `STOP_VALIDATE_WITH_LIMITS`, validation request may have occurred but **validateOnly cannot persist resources**. Never remove consumed marker or retry script. Share `H1B_W3V_*` status only.

**Next after actual W3V PASS:** prepare one exact-new-service W3 create -> optional W4 invoker -> at most four W5 probes -> same-session guarded W6 delete by `uid`/`etag`, then only UID-and-dependency-confirmed new-SA cleanup; stop if deletion safety uncertain; do not delete existing old services, C1A SA/image, shared Registry or real data.

**CURRENT**: W1 `ACTUAL_PASS_UID_115445220422157278526`; G2B `ACTUAL_PASS_REMOTE_DIGEST`; W3V `SOURCE_READY_OWNER_NOT_EXECUTED`; W3–W6 `NOT_EXECUTED`; Step05 `IN_PROGRESS`; H2/production `NO_GO`.
