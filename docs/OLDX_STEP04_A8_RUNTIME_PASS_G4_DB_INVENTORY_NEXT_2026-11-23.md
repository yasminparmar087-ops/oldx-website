# OLDX Step04 A8: isolated runtime PASS WITH LIMITS; G4 existing database inventory next

## Actual owner screenshot 23 November 2026 ~21:05 IST

Operator pasted and ran previously SHA256-pinned script `scripts/step04-a8-isolated-runtime-one-shot.sh` from immutable first Git SHA `e6350642530b5b5afdf3a592eaba5f9db2513a2e` in Google Cloud Shell. The terminal returned normally and printed exact:
```text
/tmp/oldx-a8-runtime-source-2506826f.sh: OK
A8_RUNTIME_ONESHOT_ATTEMPT=CREATED
A8_RUNTIME_SUBJECT=EXACT_IMMUTABLE_NEW_DIGEST
A8_RUNTIME_EXACT_DIGEST_PULL=PASS
A8_RUNTIME_REGISTRY_DIGEST=PASS
A8_RUNTIME_CONFIG_USER=APPUSER
A8_RUNTIME_NETWORK=NONE
A8_RUNTIME_ROOTFS=READ_ONLY
A8_RUNTIME_NONROOT=true
A8_RUNTIME_HEALTH_STATUS=200
A8_RUNTIME_DISABLED_OWNER_STATUS=503
A8_RUNTIME_FIREBASE_NETWORK=ISOLATED_NOT_TESTED
A8_RUNTIME_ISOLATED_LOCAL_TEST=PASS_WITH_LIMITS
A8_RUNTIME_REAL_IAM_OTHER_DB=NOT_TESTED
A8_CLOUD_RUN_DEPLOY=NONE
A8_BUILD_SCAN_SLSA_RERUN=NONE
A8_STEP04=HOLD_PENDING_G4_G8_AND_RISK
```

**Decision:** This is the first real local sandbox runtime execution of the EXACT new immutable image digest `sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`; nonroot, network-disabled, read-only rootfs, health 200 and owner API default-OFF 503 all PASS WITH LIMITS. Existing Docker `--rm` and `trap` stop/remove only the test container; one-shot marker retained. **Do NOT rerun this image pull/runtime test or delete marker**. This is NOT hosted Cloud Run or effective Firestore IAM verification. It does not prove that all OpenSSL CVEs are fixed or that production is safe. No new Cloud Run deploy/IAM/Firebase data-plane mutation was made. Pull may incur bandwidth cost, not a zero-cost guarantee.

## G4 after existing evidence reconciliation

Historical ONE successful *corrected* Cloud Asset IAM allow-policy analysis 21 Nov ~19:03 for `oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com` and Firestore GET/CREATE/UPDATE/DELETE: one exact `resource.name == "projects/oldx-staging/databases/(default)"` conditional binding, zero unconditional or other-conditioned matches in query scope. Source-only guard and one synthetic doc operation with DELETE403 already observed. This is not **effective other-database denial**. Existing project no parent metadata and pre-B1 direct service IAM have been reviewed and should not be rerun. A past B1 private 0%-main default-OFF revision was deployed once and R1 tag-only removal completed; don't redeploy/retag or repeat. Historical OFF-only scope owner's financial and CVE acceptances are consumed, not approval to enable Product API.

Distinct minimal next step to discover whether an actual nondefault database resource even exists, without provisioning one: **one read-only Firestore database inventory only**. If no nondefault DB exists, a genuine negative test is not currently possible without separately approved new resource; do not manufacture one. Even if another DB exists, *listing as the owner* is not denial evidence for the runtime SA. Do not impersonate the runtime SA, create/modify documents, or enumerate their contents as part of this inventory.

## One owner Cloud Shell command — PREPARED NOT EXECUTED

```bash
python3 - <<'PY'
import json
import subprocess

cmd = [
    "gcloud", "firestore", "databases", "list",
    "--project=oldx-staging",
    "--account=yasminparmar087@gmail.com",
    "--format=json", "--quiet"
]
try:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        raise ValueError("DATABASE_LIST_READ_FAILED")
    items = json.loads(r.stdout)
    if not isinstance(items, list):
        raise ValueError("DATABASE_LIST_SHAPE_UNEXPECTED")
    names = [str(x.get("name", "")) for x in items if isinstance(x, dict)]
    if len(names) != len(items) or len(set(names)) != len(names):
        raise ValueError("DATABASE_LIST_INCOMPLETE")
    prefix = "projects/oldx-staging/databases/"
    if any(not x.startswith(prefix) or not x[len(prefix):] for x in names):
        raise ValueError("DATABASE_LIST_PROJECT_MISMATCH")
    default = sum(x == prefix + "(default)" for x in names)
    if default != 1:
        raise ValueError("DEFAULT_DB_NOT_RECONCILED")
    print("G4_EXISTING_DATABASE_INVENTORY=READ_ONLY_PASS")
    print("G4_DATABASE_COUNT=" + str(len(names)))
    print("G4_DEFAULT_DB_PRESENT=True")
    print("G4_OTHER_DATABASE_COUNT=" + str(len(names) - default))
    print("G4_EFFECTIVE_OTHER_DB_ACCESS_DENIAL=UNVERIFIED")
    print("G4_NEW_DATABASE_CREATED=NO")
    print("G4_IAM_FIRESTORE_WRITES=NONE")
    print("A8_BUILD_SCAN_SLSA_RUNTIME_RERUN=NONE")
except Exception:
    print("STOP_G4_DATABASE_INVENTORY_NO_RETRY")
    print("G4_DATABASE_INVENTORY=UNVERIFIED")
    print("G4_NEW_DATABASE_CREATED=NO")
    print("G4_IAM_FIRESTORE_WRITES=NONE")
PY
```

Reads only `gcloud firestore databases list` in `oldx-staging`, checks return code/JSON shape/project prefix, requires precisely one `(default)` database consistent with prior reports, prints count of other databases but not their names or contents. No IAM / Firestore resource or data mutation, no Build/Grype/SLSA/runtime reruns. If STOP, report and do not retry automatically. If `G4_OTHER_DATABASE_COUNT=0`, keep effective other-DB deny UNVERIFIED, weigh owner risk pathway vs strict G4-B requirement; never falsely mark G4 PASS. If >0, design separately authorized non-destructive negative test only after exact target and permission model validated. If list operation fails, preserve current state and STOP.

Official references: https://docs.cloud.google.com/sdk/gcloud/reference/firestore/databases/list ; https://docs.cloud.google.com/firestore/docs/reference/rest/v1/projects.databases/list ; https://firebase.google.com/docs/firestore/manage-databases .

**Current gate statuses:** `G2_A8_LOCAL_RUNTIME=PASS_WITH_LIMITS`; `G2_A8_SCAN=ONE_COMPLETE_WITH_CVE_TRIAGE`; `G4_ALLOW_POLICY_AUDIT=PASS_WITH_LIMITS`; `G4_OTHER_DB_EFFECTIVE_DENIAL=UNVERIFIED`; `G4_EXCLUSIVE_INVOKER=NOT_PROVEN`; `G8_PROVIDER_WIDE_HARD_STOP=NOT_PROVEN`; `STEP04=HOLD`; `PRODUCTION=NO_GO`.