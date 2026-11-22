# OLDX Step04 G2 A8 — Cloud Shell Grype preflight observed only 39 MiB HOME free; scratch+registry check next

## 23 Nov 2026 ~00:38 IST — owner screenshot (actual)
```text
A8_TOOL_grype=ABSENT
A8_TOOL_syft=ABSENT
A8_TOOL_docker-credential-gcloud=AVAILABLE
A8_TOOL_docker-credential-gcr=AVAILABLE
A8_TOOL_curl=AVAILABLE
A8_TOOL_tar=AVAILABLE
A8_DOCKER_AUTH_CONFIG=EXISTS
A8_HOME_FS_FREE_MIB=39
A8_GOOGLE_ON_DEMAND_SCANNER=UNSUPPORTED_BELLSOFT_OS
A8_NEW_GRYPE_SCAN=NOT_STARTED
A8_CLOUD_MUTATIONS=NONE
A8_GOOGLE_SCAN_RETRY=PROHIBITED
```

**Interpretation:** With only 39MiB in `$HOME` filesystem, installing scanner+DB/image there is inappropriate and may corrupt existing HOME. However this screenshot does NOT independently show free space on `/tmp`, which can be a distinct filesystem; do not infer the latter. Earlier Cloud Shell one-shot full build required 14GiB scratch, but one image-only Grype scan may require substantially less; no new build is proposed. The local owner D:-backed Windows WSL, per historical `docs/OLDX_STEP04_NPMFREE_LOCAL_ONESHOT_2026-11-20.md` and `scripts/step04-npmfree-local-one-shot-a1.py`, ALREADY used pinned Grype version 0.121.3 at `/root/.oldx-g2-tools/grype` and existing offline DB under `/root/.oldx-g2-tools/db-cache-raw`, but they have NOT been checked at this turn. Their historical older image was a **different image**, and its Grype report MUST NOT be carried forward as new A8 image findings.

Goal: one read-only decision probe INSIDE CURRENT CLOUD SHELL first, then decide between `/tmp` ephemeral scratch with credentials already available versus previously used local WSL + D:. Avoid duplicate network downloads, source rebuilds, scan reruns and broad IAM changes. NO unsafe `gcloud artifacts docker images scan` retry: BellSoft OS unsupported. Proposed subject stays the existing private immutable A8 image `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-step04-g2-cloudbuild-20261122-a1@sha256:6ecd02bdd409a40673e28560f9fa77a642fee898a038d0133aea6f3a6a31cacc`.

## One next owner-run read-only Python command in same Cloud Shell — PREPARED NOT RUN

Prints HOME and TMP MiB available and device IDs, exact `asia-south1-docker.pkg.dev` Docker credential helper configured (boolean only, never prints content/credentials), and whether helper executable is present. No network, no gcloud, no files created, no scan, no auth, no IAM/API/billing/Cloud Run action.

```bash
python3 - <<'PY'
from pathlib import Path
import json, os, shutil
for name, path in [('HOME',Path.home()), ('TMP',Path('/tmp'))]:
    try:
        s=os.statvfs(path)
        print(f"A8_{name}_FREE_MIB={s.f_bavail*s.f_frsize//(1024*1024)}")
        print(f"A8_{name}_FILESYSTEM_ID={os.stat(path).st_dev}")
    except OSError:
        print(f"A8_{name}_FS=UNVERIFIED")
cfg=Path.home()/'.docker/config.json'
if cfg.is_file():
    try:
        data=json.loads(cfg.read_text(encoding='utf-8'))
        helper=str(data.get('credHelpers',{}).get('asia-south1-docker.pkg.dev',''))
        print("A8_REGISTRY_HELPER_CONFIGURED="+str(helper in ('gcloud','gcr')))
        print("A8_CONFIGURED_HELPER_EXISTS="+str(bool(shutil.which('docker-credential-'+helper)) if helper else False))
    except Exception:
        print("A8_REGISTRY_HELPER_CONFIGURED=UNVERIFIED")
else:
    print("A8_REGISTRY_HELPER_CONFIGURED=FALSE")
print("A8_CLOUD_SHELL_GRYPE_INSTALLED="+str(bool(shutil.which('grype'))))
print("A8_NEW_SCAN_STARTED=NO")
print("A8_CLOUD_ACTIONS=NONE")
print("A8_BUILD_AND_SLSA_RERUN=NONE")
PY
```

If TMP is a different FS with several GiB free and registry helper recognized, prepare an exact SHA256-pinned Grype+DB in `/tmp` without changing HOME (with ephemeral output backed up privately). If TMP is too small or helper unavailable, prefer confirmed existing root WSL Grype tools on D:-backed Windows and perform separate minimal local preflight; scan one *new digest* only. On success preserve secure JSON receipt + DB timestamp/scan coverage to avoid false clearance; do not claim zero vulnerabilities from unsupported Google scanner or empty scan discovery. G2 runtime/default DB guard, G4 cross-DB invoker and G8 total costs remain OPEN. `STEP04=HOLD`, `PRODUCTION=NO_GO`.

References: https://oss.anchore.com/docs/guides/private-registries/ ; https://oss.anchore.com/docs/reference/grype/configuration/ ; https://github.com/anchore/grype/security/advisories/GHSA-6gxw-85q2-q646 (older versions can leak credentials in report, keep all raw reports private).