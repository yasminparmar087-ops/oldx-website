# BAJUTO / OLDX Step05 — ACTUAL H2AM historical-vs-local config mismatch; no runtime or scans

Date 29 November 2026 ~00:11 IST, Owner WSL root screenshot. GitHub branch `security-hardening-review`.

## Exact actual receipt values (not inference)

```text
=== H2AM FAILURE ===
Outcome: STOP_PARTIAL_NO_AUTOMATIC_RETRY
Failure code: MEDIATOR_HISTORIC_LOCAL_CONFIG_MISMATCH
Primary failure: UNKNOWN

=== ROLE STATUS ===
mediator {'stage': 'IMAGE_BINDING'}
  Scan receipt: COMPLETE
gateway {}
backend {}
reader {}

=== MARKERS ===
H2AN CONSUMED
H2AM CONSUMED
READ_ONLY_DIAGNOSTIC=COMPLETE
```

H2AN had previously pulled Gateway, Backend, Reader exact verified child images successfully and checked four local image references. H2AM imported the historic Mediator Grype report **57 matches, 18 HIGH, 0 Critical** with a COMPLETE scan receipt; no new scan was attempted. This H2AM failure happened at **Mediator IMAGE_BINDING**, before Mediator OFF-runtime Docker container invocation, so **no current runtime logs exist**. All three other role scans and runtime checks remain unattempted. H2AJ images in registry and local Docker unchanged. H2AN/H2AM one-time markers consumed: NEVER rerun or remove marker.

## Review of frozen exact source

Existing `scripts/step05_h2am_selective_acceptance_once_20261128.py` blob `3adfb06ca66d6175f089ea797df21ca767779cca`:

```python
# image_info result verifies local RepoDigests includes exact pinned H2AJ
# Linux/AMD64, nonroot 65532:65532, entrypoint and expected /app Command.
image_id=self.local_image('mediator')
fail(image_id==historic['imageId'],'MEDIATOR_HISTORIC_LOCAL_CONFIG_MISMATCH')
```

Existing `scripts/step05_h2am_acceptance_support.py` blob `b9b57daa9a5b5f0304afc9cfc758630793454c07` takes `historic['imageId']` from Grype `source.target.imageID` (or `imageId`) and independently pins `source.target.userInput/repoDigests/manifestDigest` to approved child ref. The older source receipt claimed the historic Grype imageID is `sha256:44c8657a5aad46d7aa1192e73af0a338200c61720f47b0ebe8d19faa3613f1e2`. **Actual current Docker `image inspect .Id` was NOT printed in the screenshot; not known yet.** Difference could be actual config mismatch or scanner-vs-Docker identifier semantics; do not weaken identity checks or infer a bug without reading the actual two IDs.

The previous consumed H2AK's original scan is validated by pinned raw SHA256 `e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92`; H2AM source receipt already has a pinned approved immutable linux/amd64 child manifest ref `asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-h2ah@sha256:01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe`.

## One exact READ-ONLY WSL root identity audit — no Docker writes, scans or Grype runs

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib,json,re,subprocess
root=Path('/root')
e=root/'oldx-h2am-selective-20261128T183527Z-2ae92ca2'
historic=root/'oldx-h2ak-images-20261128T160610Z-42e006/mediator-grype.json'
expected='e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92'
ref='asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/oldx-c2-mediator-h2ah@sha256:01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe'
print('AUDIT=READ_ONLY_NO_SCAN_NO_PULL_NO_RUNTIME')
for n,path in [('H2AN',root/'.oldx-step05-h2an-three-pinned-preloads-once-20261128'),('H2AM',root/'.oldx-step05-h2am-selective-off-runtime-three-scans-once-20261128')]:
 print(n+'_MARKER='+('CONSUMED' if path.is_file() else 'NOT_FOUND'))
if historic.is_file() and not historic.is_symlink():
 data=historic.read_bytes()
 print('HISTORIC_REPORT_SHA256='+hashlib.sha256(data).hexdigest())
 print('HISTORIC_REPORT_SHA_PIN_MATCH='+str(hashlib.sha256(data).hexdigest()==expected))
 old=json.loads(data)
 t=old.get('source',{}).get('target',{})
 print('GRYPE_IMAGE_ID='+str(t.get('imageID') or t.get('imageId')))
 print('GRYPE_MANIFEST_DIGEST='+str(t.get('manifestDigest')))
 print('GRYPE_USER_INPUT_MATCHES_CHILD='+str(t.get('userInput') in (ref,'docker:'+ref)))
 print('GRYPE_REPODIGEST_CONTAINS_CHILD='+str(ref in (t.get('repoDigests') or [])))
else:print('HISTORIC_REPORT=MISSING')
f=e/'summary.json'
if f.is_file():
 raw=f.read_bytes()
 print('H2AM_SUMMARY_SHA256='+hashlib.sha256(raw).hexdigest())
 print('H2AM_FAILURE_CODE='+str(json.loads(raw).get('failure',{}).get('code')))
img=e/'mediator-image.json'
if img.is_file():
 a=json.loads(img.read_text())
 print('H2AM_SAVED_DOCKER_IMAGE_ID='+str(a.get('imageId')))
print('DOCKER_LOCAL_INSPECT_BEGIN')
try:
 p=subprocess.run(['docker','image','inspect',ref,'--format',
    '{{.Id}}|{{json .RepoDigests}}|{{.Os}}|{{.Architecture}}|{{.Config.User}}'],
    timeout=20,check=False,capture_output=True,text=True)
 if p.returncode==0:
  a=p.stdout.strip().split('|')
  if len(a)==5:
   print('DOCKER_CONFIG_ID='+a[0])
   refs=json.loads(a[1])
   print('DOCKER_REPODIGEST_PIN_PRESENT='+str(ref in refs))
   print('DOCKER_OS='+a[2])
   print('DOCKER_ARCH='+a[3])
   print('DOCKER_USER='+a[4])
  else:print('INSPECT_SCHEMA_UNKNOWN')
 else:print('INSPECT_ERROR_EXIT='+str(p.returncode))
except (OSError,ValueError,subprocess.TimeoutExpired):
 print('DOCKER_LOCAL_INSPECT_UNAVAILABLE')
print('AUDIT_FINISHED=NO_WRITES')
PY
```

The command above only reads existing private root files and runs local `docker image inspect` with a restricted `--format`; prints no Docker Env/secret/whole Grype JSON. Do not upload the full Grype report, auth config or private runtime logs. It does not invoke Docker pull, container run/exec/stop/rm, Grype, gcloud or any Cloud operation.

## Next ONLY after exact identity evidence

- If Docker config ID equals Grype source target imageID but the H2AM error occurred, inspect the source/receipt type/sanitization logic for a source-only bug and prepare a new reviewed one-time selective continuation, NEVER resetting old markers.
- If IDs differ but same immutable child digest bound, inspect whether Grype's `imageID` refers to OCI config vs layer vs SBOM abstraction and whether old Grype scan was actually of the intended local built image. Do not simply remove the equality check. Establish trustworthy equivalence with independent metadata before making any source correction.
- Existing Mediator scan must not be repeated. Global H2AM per-stage scan receipt is COMPLETE; new source should reuse it, only attempt as-yet-unattempted runtime and the other three scans after explicit bounded new Owner approval.
- If genuine identity tampering/drift, STOP, do not authorize continuation.

**Current:** `H2AJ=FOUR_PRIVATE_REGISTRY_PASS`, `H2AN=THREE_PRELOADS_PASS_MARKER_CONSUMED`, `H2AM=CONSUMED_PARTIAL_AT_MEDIATOR_IMAGE_BINDING`, `MEDIATOR_GRYPE_HISTORIC=COMPLETE_NO_RESCAN`, `MEDIATOR_RUNTIME=NOT_STARTED`, `GATEWAY_BACKEND_READER_SCANS=NOT_STARTED`, `STEP05=ACTIVE`, `PRODUCTION=OFF_NO_GO`.
