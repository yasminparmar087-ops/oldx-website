# OLDX Step04 G2 A8 — Cloud Shell first on-demand scan submission STOP; local-only log reconciliation

Actual user screenshot 23 Nov 2026 approximately 00:32 IST, Google Cloud Shell (Linux), project `oldx-staging`, actor preflight passed, running one owner-approved `gcloud artifacts docker images scan` attempt against **immutable** A8 image `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`.

Exact bottom output:
```text
A8_SCAN_ONE_ATTEMPT_MARKER=CREATED
A8_SCAN_TARGET=APPROVED_IMMUTABLE_DIGEST
STOP_A8_SCAN_SUBMIT_FAILED_OR_AMBIGUOUS
A8_SCAN_STATE=RECONCILE_BEFORE_ANY_NEW_WRITE
A8_PRIVATE_SCAN_LOG=SAVED_IN_CLOUD_SHELL_HOME
A8_BUILD_OR_VERIFIER_RERUN=NONE
A8_SCAN_RETRY=PROHIBITED
```

This proves the one-time marker was made and scan-command branch did not return CLI exit-zero. It **does not establish whether a Google long-running operation was created** before command failure. Do not claim a scan happened or that it did not. Do not repeat the submitted scan, delete marker, enable APIs, IAM/write, build, push, or rerun SLSA verifier. The original private Cloud Shell file `$HOME/oldx-a8-on-demand-scan-2506826f.log` must be inspected **locally only**, not pasted/uploaded raw. Cloud Shell `$HOME/.oldx-a8-on-demand-scan-2506826f-attempted` is the no-repeat marker. The scan attempt might incur charges if operation was created; do not assert zero cost from CLI failure. Prior signed Git SHA, output digest, SLSA and Build PASS remain consumed. Scan findings and G2 security clearance still UNKNOWN; G4/G8 outstanding, Step04 HOLD, production NO_GO.

## Next exactly ONE local-only Linux Cloud Shell read — prepared, NOT run

The following command does NOT call `gcloud`, make network calls, start a new scan, or mutate any file. It reads the previous private log and marker, prints limited redacted error diagnostics and any exact project/region operation names. It checks common classes including the Google `local-extract` component, flags, auth/permission, API, quota, network. Regex classifications are **hints**, not authoritative root cause. If an operation name appears, inspect that ONE operation in a later separate read-only command before any further action. If an operation does not appear, that alone does NOT prove no operation was submitted.

```bash
python3 - <<'PY'
from pathlib import Path
import re

log=Path.home()/"oldx-a8-on-demand-scan-2506826f.log"
marker=Path.home()/".oldx-a8-on-demand-scan-2506826f-attempted"
print("A8_ONE_ATTEMPT_MARKER_PRESENT="+str(marker.is_dir()))
if not log.is_file():
    print("STOP_A8_PRIVATE_SCAN_LOG_MISSING")
else:
    raw=log.read_text(encoding="utf-8",errors="replace")
    print("A8_PRIVATE_LOG_READ=PASS")
    print("A8_PRIVATE_LOG_BYTES="+str(log.stat().st_size))
    operations=list(dict.fromkeys(re.findall(
        r"projects/oldx-staging/locations/(?:asia|us|europe)/operations/[A-Za-z0-9-]+",raw)))
    print("A8_RECORDED_OPERATION_COUNT="+str(len(operations)))
    for op in operations[:2]:
        print("A8_RECORDED_OPERATION="+op)
    checks=[
      ("COMPONENT_OR_LOCAL_EXTRACT",r"local.extract|component manager|components install|component.+not installed"),
      ("PERMISSION_DENIED",r"permission.denied|permission denied|insufficient permissions|\b403\b"),
      ("INVALID_FLAG_OR_ARGUMENT",r"unrecognized arguments|unrecognized flag|invalid choice|invalid argument|unknown flag"),
      ("API_DISABLED",r"has not been used|is disabled|api.not.enabled|enable.*api"),
      ("IMAGE_NOT_FOUND",r"image.not.found|not found|\b404\b"),
      ("QUOTA_OR_RATE_LIMIT",r"quota|rate.limit|\b429\b"),
      ("AUTHENTICATION",r"unauthenticated|invalid credentials|login required|authentication failed"),
      ("NETWORK_OR_TIMEOUT",r"timed out|connection reset|network|ssl|certificate verify"),
    ]
    found=[name for name,pattern in checks if re.search(pattern,raw,re.I)]
    print("A8_ERROR_CATEGORIES="+(",".join(found) if found else "UNCLASSIFIED"))
    selected=[line for line in raw.splitlines()
      if re.search(r"error|failed|denied|component|invalid|not found|quota|permission|warning|traceback",line,re.I)]
    for line in selected[-5:]:
        line=re.sub(r"(?i)Bearer\s+\S+","Bearer [REDACTED]",line)
        line=re.sub(r"ya29\.[A-Za-z0-9._-]+","[TOKEN]",line)
        line=re.sub(r"[\w.+-]+@[\w.-]+","[EMAIL]",line)
        line=re.sub(r"https?://\S+","[URL]",line)
        print("A8_REDACTED_DIAGNOSTIC="+line[:200])
print("A8_NEW_SCAN_SUBMITTED_BY_THIS_CHECK=NO")
print("A8_IAM_API_REGISTRY_CHANGES=NONE")
print("A8_ORIGINAL_SCAN_COMMAND_RETRY=PROHIBITED")
PY
```

Document official support for CLI flags: https://docs.cloud.google.com/sdk/gcloud/reference/artifacts/docker/images/scan ; Google setup mentions `local-extract` dependency and owner accounts: https://docs.cloud.google.com/artifact-analysis/docs/scan-os-on-demand .

After user returns only sanitized terminal screenshot, diagnose exact failure and choose the least-change next distinct action. NEVER re-run scan submission under the first consumed marker automatically. No second paid scan without reconciling provider state and bounded owner action.

