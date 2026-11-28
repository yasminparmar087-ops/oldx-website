# BAJUTO / OLDX Step05 H2AI — Owner FIRST build invocation failed; one-shot marker CONSUMED

Date: 2026-11-28 IST (~20:45 local). Evidence: Owner WSL root screenshot.

## Exact observed terminal values

```text
H2AI_PREFLIGHT=OWNER_PROJECT_REPOSITORY_NODE_DOCKER_DISK_PASS
H2AI_SOURCE_BUNDLES=FOUR_READY_EXACT_APPROVED_SOURCE
H2AI_MARKER=CONSUMED_NO_REPEAT
H2AI_BUILD_PUSH_START=mediator
H2AI_RESULT=STOP_AFTER_MARKER_POSSIBLE_PARTIAL_REGISTRY_WRITES
H2AI_SOURCE_REVISION=d05a0603296e7685c58fec83f5f7aa12a278a839
H2AI_PRIVATE_EVIDENCE=/root/oldx-h2ai-four-builds-20261128T151519Z-09e4fd
H2AI_DOCKER_CONFIG=TEMPORARY_NOT_GLOBAL
H2AI_CLOUD_RUN_IAM_KMS_FIRESTORE_DEPLOYMENT=NONE
H2AI_H2_PRODUCTION=NO_GO
H2AI_DO_NOT_REPEAT=TRUE
H2AI_REASON=APPROVED_COMMAND_FAILED_NO_RETRY
```

This is **NOT** the earlier missing Node or builder-pin prewrite STOP: the corrected runner passed Owner/native SDK, Node24, Buildx and provenance/source-bundle preflight, **created its EXCLUSIVE marker**, then launched the FIRST `docker buildx build --push` for **Mediator only**. The subprocess returned non-zero; whether any registry write occurred is **UNKNOWN/POSSIBLE PARTIAL** until the actual private log/metadata and at most read-only registry inspection confirm. **Gateway, Backend and Reader were NOT attempted**; do not infer any image/digest or PASS. The generated source-bundle revision is a documentation-only descendant of approved source `5d5a621d7a9d9015b5068077b914fef3d6fb9925`, with unchanged Dockerfiles/locks per runner prewrite check.

**MANDATORY STOP**: do NOT rerun H2AI, DO NOT clear or alter `/root/.oldx-step05-h2ai-four-off-build-push-once-20261128`, DO NOT run build/push for remaining roles under consumed approval, DO NOT delete partially pushed image or receipts. Owner approval allowed **at most ONE build/push attempt per role** and the exact runner stops the entire batch on first ambiguous failure. A separate exact one-time reconciliation and new authorization are required before any additional registry mutation.

## One READ-ONLY local evidence command

In the existing WSL root terminal, print only sanitized recent Mediator build errors and stage receipt. This does not rerun tests, builds, authentication or any Cloud request:

```bash
python3 - <<'PY'
from pathlib import Path
import json,re
p=Path('/root/oldx-h2ai-four-builds-20261128T151519Z-09e4fd')
print('=== SANITIZED SUMMARY ===')
f=p/'sanitized-h2ai-summary.json'
if f.is_file():
    r=json.loads(f.read_text())
    print(json.dumps({'outcome':r.get('outcome'),
      'reason':r.get('reason'),'sourceRevision':r.get('sourceRevision'),
      'roles':{k:{'buildPushAttempted':v.get('buildPushAttempted'),
          'readbackVerified':v.get('readbackVerified'),
          'registryIndexDigest':v.get('registryIndexDigest'),
          'linuxAmd64ChildDigest':v.get('linuxAmd64ChildDigest')}
        for k,v in r.get('roles',{}).items()}},indent=2))
else: print('RECEIPT_NOT_FOUND')
print('=== MEDIATOR BUILD LOG LAST 55 LINES (REDACTED) ===')
log=p/'private-build-mediator.log'
if log.is_file():
    lines=log.read_text(errors='replace').splitlines()[-55:]
    for x in lines:
        x=re.sub(r'(?i)(Bearer\\s+)[A-Za-z0-9._~+/-]+',r'\\1[REDACTED]',x)
        x=re.sub(r'(oauth2accesstoken[:=])[^\\s]+',r'\\1[REDACTED]',x,flags=re.I)
        print(x[:500])
else: print('MEDIATOR_LOG_NOT_FOUND')
print('=== MARKER ===')
print('CONSUMED' if Path('/root/.oldx-step05-h2ai-four-off-build-push-once-20261128').is_file() else 'NOT_FOUND_VERIFY_BEFORE_ANY_ACTION')
PY
```

If the log includes any credential/token/password or private data, redact it before sharing screenshot. Do NOT paste full auth tokens, Docker config or secrets. After evaluating actual error, use read-only evidence to determine whether the Mediator artifact tag/index exists. Only then propose **one minimal fresh Owner approval** tailored to the precise failed role + remaining unattempted roles; do not assume another build is allowed or necessary.

**Checkpoint:** `H2AI_MARKER=CONSUMED`; `MEDIATOR_BUILD_PUSH=FAILED_UNKNOWN_PARTIAL`; `GATEWAY_BACKEND_READER=NOT_STARTED`; `CLOUD_RUN_IAM_KMS_FIRESTORE=UNCHANGED`; `STEP05=ACTIVE`; `PRODUCTION=OFF_NO_GO`. Earlier six H2AI safety tests PASS; do not rerun. H2AG Reader/IAM PASS stays consumed.
