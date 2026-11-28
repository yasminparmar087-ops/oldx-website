# BAJUTO / OLDX Step05 — H2AN actual 3 PRELOAD PASS; H2AM actual PARTIAL STOP: READ EXISTING EVIDENCE ONLY

Date: 2026-11-29 ~00:06 IST, Owner WSL root screenshot. Branch `security-hardening-review`.

## Actual results from screenshot

```text
GRYPE_OWNER_BEFORE=1001:1001
GRYPE_OWNER_AFTER=0:0
H2AN_PREFLIGHT=OWNER_DOCKER_GRYPE_DB_HISTORY_PASS
H2AN_MISSING=gateway,backend,reader
H2AN_SOURCE_BLOBS=ALL_THREE_VERIFIED
H2AN_PRELOAD_MARKER=CONSUMED_NO_REPEAT
H2AN_PULL_START=gateway
H2AN_PULL_PASS=gateway
H2AN_PULL_START=backend
H2AN_PULL_PASS=backend
H2AN_PULL_START=reader
H2AN_PULL_PASS=reader
H2AN_FOUR_LOCAL_CHILDREN=VERIFIED
H2AN_H2AM=START_ONE_APPROVED_SELECTIVE_ATTEMPT
H2AM_OUTCOME=STOP_PARTIAL_NO_AUTOMATIC_RETRY
H2AM_SUMMARY_SHA256=99a455c5bedd435c0f72b0c9aacadcb96d8949db9cb1d2bff518416ca1b18e958f
H2AM_PRIVATE_EVIDENCE=/root/oldx-h2am-selective-20261128T183527Z-2ae92ca2
H2AM_MEDIATOR_SCAN=IMPORTED_NOT_RESCANNED
H2AM_CLOUD_KMS_FIREBASE_DEPLOYMENT=NONE_PRODUCTION_NO_GO
H2AN_RESULT=STOP_AFTER_PRELOAD_MARKER
H2AN_REASON=H2AM_COMPLETED_WITH_STOP_STATUS_2
H2AN_H2AM_STARTED=TRUE
H2AN_EVIDENCE=/root/oldx-h2an-preload-20261128T183341Z-13cf10
H2AN_OLD_MARKERS_UNTOUCHED=TRUE
H2AN_BUILD_PUSH_CLOUD_IAM_KMS_FIREBASE=NONE
H2AN_DO_NOT_REPEAT_AFTER_MARKER=TRUE
```

**Verified true progress:** three precise already-built child images were each pulled ONCE and inspected locally, four local child images now VERIFIED, old H2AJ registry pushes not repeated, old Mediator Grype report (57 findings, 18 HIGH, 0 Critical) was imported rather than rescanned. Grype original archive extract ownership was actually 1001:1001; changed only Grype binary owner to 0:0. Prior prewrite missing-grype failure resolved.

**Critical stop:** H2AN preload one-shot marker CONSUMED, H2AM selective one-shot started and its marker may be consumed. The observed H2AM status is `STOP_PARTIAL_NO_AUTOMATIC_RETRY` and **does not prove whether Mediator runtime or Gateway/Backend/Reader scans were reached**. Do not claim a specific role/stage passed or failed until exact existing private summary and receipts are read. Do not rerun, clear markers, pull more images, run scan, start/stop containers, or assume which Grype JSON files exist. No Cloud Run, IAM, KMS, Firebase or production writes in this screenshot.

## Next only read-only receipt inspection, no Docker invocation or mutation

Run **ONE** direct Python snippet in the same WSL root. It reads the exact existing H2AM private receipt and marker files, printing only status and safe structured failure codes, NEVER raw log stderr/stdout/auth tokens/Env:

```bash
python3 - <<'PY'
from pathlib import Path
import json
p=Path('/root/oldx-h2am-selective-20261128T183527Z-2ae92ca2')
root=Path('/root')
def read(name):
    f=p/name
    if f.is_symlink() or not f.is_file() or f.stat().st_size>2000000:
        return None
    try:
        v=json.loads(f.read_text(encoding='utf-8'))
        return v if isinstance(v,dict) else None
    except (ValueError,OSError,UnicodeError):
        return None
def small(value):
    return str(value)[:120] if value is not None else 'UNKNOWN'
print('=== H2AM EXISTING RECEIPTS ONLY ===')
for label,name in [('H2AN','three-pinned-preloads'),('H2AM','selective-off-runtime-three-scans')]:
    prefix='.oldx-step05-h2a'+('n' if label=='H2AN' else 'm')
    relevant=(root/'.oldx-step05-h2an-three-pinned-preloads-once-20261128') if label=='H2AN' else (root/'.oldx-step05-h2am-selective-off-runtime-three-scans-once-20261128')
    print(label+'_MARKER='+('CONSUMED' if relevant.is_file() else 'NOT_FOUND'))
summary=read('summary.json')
if summary:
    print('OUTCOME='+small(summary.get('outcome')))
    fail=summary.get('failure') or {}
    print('FAILURE_CODE='+small(fail.get('code')))
    detail=fail.get('detail') if isinstance(fail.get('detail'),dict) else {}
    for key in ('stage','exitCode','timedOut','reason','role'):
        if key in detail:print('FAILURE_'+key.upper()+'='+small(detail[key]))
    roles=summary.get('roles') or {}
    for role in ('mediator','gateway','backend','reader'):
        x=roles.get(role)
        print('SUMMARY_'+role+'='+small({k:v for k,v in x.items() if k in ('stage','scan','runtime')} if isinstance(x,dict) else x))
else:print('SUMMARY=NOT_READABLE')
for role in ('mediator','gateway','backend','reader'):
    for stage in ('scan','runtime'):
        x=read(role+'-'+stage+'.json')
        if x is None:continue
        print('RECEIPT_'+role+'_'+stage+'='+small(x.get('status')))
        if stage=='runtime':
            first=x.get('primaryFailure') or {}
            clean=x.get('cleanup') or {}
            state=x.get('state') or {}
            print('RUNTIME_'+role+'_PRIMARY='+small(first.get('code')))
            print('RUNTIME_'+role+'_CLEANUP='+small(clean.get('status')))
            print('RUNTIME_'+role+'_OOM='+small(x.get('oomEvidence')))
            for field in ('ExitCode','OOMKilled','Running'):
                if field in state:print('RUNTIME_'+role+'_'+field.upper()+'='+small(state[field]))
            d=first.get('detail') if isinstance(first.get('detail'),dict) else {}
            for field in ('stage','exitCode','timedOut'):
                if field in d:print('RUNTIME_'+role+'_FAIL_'+field.upper()+'='+small(d[field]))
print('=== READ_ONLY COMPLETE / NO RETRIES ===')
PY
```

No Docker, Grype, registry or gcloud command; no mutation. Return output/screenshot; then reconcile actual role/stage errors and choose one safe minimal fresh approval for only unattempted stages if justified. **Consumed attempts must never be silently replayed, even if failed.**

Checkpoint: `H2AJ=4_IMAGES_PRIVATE_REGISTRY_PASS`; `H2AN=3_EXACT_PRELOADS_PASS_MARKER_CONSUMED`; `LOCAL_FOUR=VERIFIED`; `H2AM=PARTIAL_STOP_MARKER_PRESUMED_CONSUMED`; `MEDIATOR_OLD_GRYPE=IMPORTED_NO_RESCAN`; `H2AM_ACTUAL_FAILED_STAGE=NEEDS_PRIVATE_SUMMARY`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`.
