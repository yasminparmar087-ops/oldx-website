# BAJUTO / OLDX Step05 H2X — new service hosted readiness read-only after H2W actual PASS

## 27 November 2026 late IST — source-only next action, NOT EXECUTED

[Canonical owner actual H2W new Cloud Run OFF Gateway creation and direct Owner-only IAM binding PASS](OLDX_STEP05_H2W_PRIVATE_GATEWAY_NEW_SERVICE_ACTUAL_PASS_2026-11-27.md). Owner screenshot showed new service `projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway`, **service UID** `2d87153f-155e-409f-a418-463c785d8467`, separate **runtime service-account numeric UID** `107238619872767759560`, new Owner direct Invoker policy PASS, `INGRESS=INTERNAL_ONLY`, `HTTP_PROBES=NOT_ATTEMPTED_INTERNAL_ONLY`, no other Cloud writes, H2 Production NO_GO.

**Do not repeat the consumed H2W service create/Owner IAM write**, or the former H2V image push, H2U build, signed base verification, prior Product/ESM tests, older H1B probes, Cloud inventories, etc. Do not delete/reset markers.

## One distinct NEW factual check: Hosted Ready revision, generation and active traffic (only ONE GET)

GitHub source `scripts/step05_h2x_new_h2w_hosted_revision_readiness_readonly_once_20261127.py`
- **Immutable creation commit** `9913908772a301583c6921a9ef0a778264d69f9d`;
- **Git blob SHA-1** `e4c053baae63340bc721821899db667572d0ed8b`, GitHub fetched and static-scoped, not yet executed on Owner WSL;
- Requires existing H2W one-shot marker with **actual PASS**, exact new service UID and frozen H2U image; root WSL with Owner's previously established isolated native Google Cloud SDK credentials; rejects any unexpected/missing prerequisite.
- Acquires a short-lived Owner OAuth access token in memory using the existing isolated config; only queries `GET https://run.googleapis.com/v2/projects/oldx-staging/locations/asia-south1/services/oldx-c2-h2-private-gateway`. The exact service **name+UID+internal ingress+IAM enforced+runtime SA+image digest+OFF env** must still match the H2W receipt.
- **New, not previously recorded facts:** `generation`, `observedGeneration`, `latestCreatedRevision`, `latestReadyRevision`, `reconciling`, `terminalCondition.state`, `trafficStatuses`. Requires generation observed match, latest ready==created, `reconciling=false`, terminal state `CONDITION_SUCCEEDED`, and 100% traffic status. If status is transient, incomplete or differs, prints `STOP_NEW_REVISION_READY_NOT_VERIFIED`; no automatic rerun or changes.
- **Read-only only**: no IAM GET or write, no Cloud Run mutation or new deployment, no host HTTP GET, no public exposure, no source build/push, no KMS/Firestore.
- Even a readiness PASS does **not** constitute a hosted HTTP check or an inherited IAM permission audit; it only establishes the latest revision is reconciled and serving per the Google Cloud control plane at the time of the read.

Google official semantics: [Cloud Run V2 Service revision readiness/reconciling/traffic](https://docs.cloud.google.com/run/docs/reference/rest/v2/projects.locations.services) and [internal ingress origin rules](https://docs.cloud.google.com/run/docs/securing/private-networking).

### Exactly one new Owner Ubuntu WSL root command

~~~bash
umask 077
d=$(mktemp -d /root/oldx-h2x-readiness-launch.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/readiness.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/9913908772a301583c6921a9ef0a778264d69f9d/scripts/step05_h2x_new_h2w_hosted_revision_readiness_readonly_once_20261127.py' &&
test "$(git hash-object "$d/readiness.py")" = 'e4c053baae63340bc721821899db667572d0ed8b' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/readiness.py" &&
python3 -B "$d/readiness.py" --h2x-new-h2w-service-readiness-readonly-once
~~~

**Expected if actually Ready (NOT claimed in advance):**

~~~text
H2X_NEW_HOSTED_REVISION_READY=VERIFIED
H2X_CLOUD_READ=ONE_EXACT_SERVICE_GET
H2X_RESULT=READ_ONLY_NEW_REVISION_READY_PASS_WITH_LIMITS
H2X_INHERITED_IAM=NOT_AUDITED
H2X_HOSTED_HTTP=NOT_TESTED
H2X_CLOUD_WRITES=NONE
H2X_H2_PRODUCTION=NO_GO
~~~

If `STOP`, do not repeat previous H2W create/Owner IAM grant, and do not rush to update security policy: read the reason and decide next distinct targeted diagnostics. Keep service/private OFF unchanged.

## Next after H2X

With readiness confirmed, determine supported private network origin for **one bounded real authenticated OFF-only HTTP probe**. A Cloud Run Job or new probe service without configured internal routing cannot be assumed to reach an internal-only service. New network/job/service resources or IAM require **separate Owner approval**. Independent actual KeyVersion public-status reader, Firestore one-sign durable tombstone, bounded synthetic KMS sign and derived-image security/provenance are still pending. Public Production remains NO_GO.

**Checkpoint:** `H2W_NEW_PRIVATE_SERVICE_AND_OWNER_DIRECT_INVOKER=ACTUAL_PASS`; `H2X_READ_ONLY_NEW_HOSTED_READY=SOURCE_READY_NOT_EXECUTED`; `STEP05=ACTIVE`; `H2/PRODUCTION=NO_GO`.
