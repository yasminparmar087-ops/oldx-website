# BAJUTO / OLDX Step05 H2AD4 — owner explicitly approved ONE existing-probe Invoker correction

## Owner decision, 28 Nov 2026

After H2AD3 Owner actual Google Cloud audit log finding `H2AD3_MATCH_1_CODE=3`, `H2AD3_MATCH_1_CATEGORY=PROBE_SERVICE_ACCOUNT_PRINCIPAL_REJECTED`, and the separately scoped question about exactly **one** corrective service-only Invoker IAM write, Owner answered **"ha manjuri chhe"**. This is explicit permission for ONE guarded attempt **only**, not indefinite retries, broad project policy, a new Service Account, KMS, Firebase/Firestore, production enable, Cloud Run ingress change, Scheduler job create or actual HTTP dispatch.

Frozen actual prior checkpoints (NO REPEAT):
- H2AD1 Owner created one dedicated SA, `oldx-h2ad-probe-20261128@oldx-staging.iam.gserviceaccount.com`, then the one Gateway `:setIamPolicy` attempt HTTP400. H2AD1 marker consumed.
- H2AD2 Owner actual read-only: SA exists and enabled, unique numeric SA UID `110217058111344002447`; exact private Cloud Run service UID `2d87153f-155e-409f-a418-463c785d8467` still `INTERNAL_ONLY` and default `OFF`; direct Invoker policy **Owner-only**. H2AD2 marker consumed.
- H2AD3 Owner actual bounded audit log read: one target entry with code3 and sanitized classification `PROBE_SERVICE_ACCOUNT_PRINCIPAL_REJECTED` (diagnostic hint, not proof of exact 400 cause). H2AD3 marker consumed.
- H2AD0 known original `run.app` host, exact job-name absence; H2AC Scheduler API already ENABLED; existing H2U/H2V/H2W verified image/private Gateway. Never re-run consumed image builds, registry pushes, Cloud Run creates or old tests.

## Single frozen H2AD4 script, now explicitly owner-approved but NOT YET EXECUTED

- File: `scripts/step05_h2ad4_owner_approved_existing_probe_exact_iam_correction_once_20261128.py`
- Source creation commit: `e25c84e22c718b3cdb5e4e2a1dc113e955889605`
- Verified again after approval: Git blob `1406253ede3e24ea1034985b3e625354f32115ea`.
- Existing isolated Ubuntu WSL root Owner configuration. Preflight all H2AD1/H2AD2/H2AD3 exact root-owned consumed markers with fixed identity; fresh existing SA UID read, exact Cloud Run service UID/internal ingress/auth/OFF/pinned image read, fresh direct service IAM Owner-only read with ETag. No new SA created. If direct Owner+probe already present, stop without IAM write.
- If still Owner-only, write unique one-shot local marker `/root/.oldx-step05-h2ad4-one-corrective-exact-invoker-once-20261128` before the **single corrective `POST ...:setIamPolicy`**, setting only target-service direct `roles/run.invoker` with current Owner and exact existing probe SA; no IAM project/folder grants. Must read back just those two members. Any timeout, 400, unexpected status or IAM drift => STOP; **do not rerun, clear marker, retry or auto-clean up**. Printed error category sanitized; never paste full IAM, bearer tokens or raw error responses.
- No job created/run, no Cloud Run ingress change, no KMS sign, Firestore or Product writes; H2/prod NO-GO.

### Approved exactly one root Ubuntu WSL paste

```bash
umask 077
d=$(mktemp -d /root/oldx-h2ad4-approval.XXXXXXXX) &&
curl --fail --silent --show-error --retry 0 --max-redirs 0 --max-time 40 --proto '=https' --output "$d/h2ad4.py" 'https://raw.githubusercontent.com/yasminparmar087-ops/oldx-website/e25c84e22c718b3cdb5e4e2a1dc113e955889605/scripts/step05_h2ad4_owner_approved_existing_probe_exact_iam_correction_once_20261128.py' &&
test "$(git hash-object "$d/h2ad4.py")" = '1406253ede3e24ea1034985b3e625354f32115ea' &&
python3 -B -c 'import ast,sys; ast.parse(open(sys.argv[1],encoding="utf-8").read())' "$d/h2ad4.py" &&
python3 -B "$d/h2ad4.py" --h2ad4-owner-approved-one-existing-probe-invoker-correction-once
```

Expected *only if successful*: `H2AD4_RESULT=PASS_ONE_CORRECTIVE_EXACT_INVOKER_WITH_LIMITS`, `H2AD4_GATEWAY_IAM=OWNER_PLUS_EXACT_PROBE_ONLY`. If already bound, `H2AD4_RESULT=ALREADY_GRANTED_NO_CLOUD_WRITE`. **Do not predict success**; status 400 could recur. An unsuccessful result is not permission to dispatch a Scheduler job. Next, only after actual successful readback, create *one* bounded paused/future Scheduled OFF `GET /healthz` job, manually dispatch one time, separately verify HTTP delivery, and clean up exact new resources after delivery is reconciled.

**Current checkpoint:** `H2AD4=OWNER_APPROVED_SOURCE_PINNED_NOT_EXECUTED`; `H2AD1=PARTIAL_SA_CREATE_HTTP400_CONSUMED`; `H2AD2=OWNER_ONLY_CONSUMED`; `H2AD3=AUDIT_HINT_CONSUMED`; `STEP05=ACTIVE`; `H2_HOSTED_HTTP=NOT_TESTED`; `PRODUCTION=NO_GO`.
