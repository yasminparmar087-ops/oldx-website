#!/usr/bin/env python3
"""OLDX Step05 C1A cleanup: guarded READ-ONLY preflight in Owner Cloud Shell.

Does NOT delete/update any Cloud resource. Only supports one later,
separately guarded cleanup of the historical C1A resources.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone

OWNER = 'yasminparmar087@gmail.com'
PROJECT = 'oldx-staging'
REGION = 'asia-south1'
SERVICE = 'oldx-step05-gateway'
SERVICE_UID = 'bf441d37-e39b-4afd-b4c8-0e6edee7269b'
REVISION = 'oldx-step05-gateway-00001-thd'
SA = 'oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com'
SA_UID = '102194769236111252832'
REMOTE_IMAGE = ('asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/'
                'oldx-step05-gateway-off@sha256:'
                '612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a')
MARKER = '.oldx-step05-c1a-cleanup-readonly-once-20261126'
TIMEOUT = 20
MAX_BYTES = 256 * 1024

class Stop(Exception):
    pass

def need(cond, message):
    if not cond:
        raise Stop(message)

def object_dict(obj):
    return obj if isinstance(obj, dict) else {}

def inspect_service(data):
    need(isinstance(data, dict), 'SERVICE_JSON_NOT_OBJECT')
    meta = object_dict(data.get('metadata'))
    status = object_dict(data.get('status'))
    spec = object_dict(data.get('spec'))
    template = object_dict(spec.get('template'))
    template_spec = object_dict(template.get('spec'))
    # CLI defaults to Cloud Run v1 Service resource; never guess v2 field semantics.
    need(data.get('apiVersion') == 'serving.knative.dev/v1', 'SERVICE_API_SCHEMA_NOT_V1')
    need(meta.get('name') == SERVICE and meta.get('uid') == SERVICE_UID, 'SERVICE_UID_OR_NAME_CHANGED')
    need(status.get('latestReadyRevisionName') == REVISION
         and status.get('latestCreatedRevisionName') == REVISION,
         'SERVICE_REVISION_CHANGED')
    traffic = status.get('traffic')
    need(isinstance(traffic, list) and len(traffic) == 1
         and traffic[0].get('revisionName') == REVISION
         and traffic[0].get('percent') == 100
         and not traffic[0].get('tag'), 'SERVICE_TRAFFIC_OR_TAG_CHANGED')
    need(template_spec.get('serviceAccountName') == SA, 'SERVICE_SA_CHANGED')
    containers = template_spec.get('containers')
    need(isinstance(containers, list) and len(containers) == 1
         and object_dict(containers[0]).get('image') == REMOTE_IMAGE,
         'SERVICE_IMAGE_CHANGED')
    need(not containers[0].get('env'), 'SERVICE_HAS_ENV')
    need(not containers[0].get('volumeMounts') and not template_spec.get('volumes'),
         'SERVICE_HAS_VOLUMES')
    annotations = object_dict(meta.get('annotations'))
    need(annotations.get('run.googleapis.com/invoker-iam-disabled') != 'true',
         'INVOCATION_IAM_BYPASS')
    return True

def inspect_policy(data):
    need(isinstance(data, dict), 'IAM_NOT_OBJECT')
    need(not data.get('bindings'), 'DIRECT_IAM_BINDINGS_CHANGED')
    need(not data.get('auditConfigs'), 'DIRECT_IAM_AUDIT_CONFIGS_CHANGED')
    return True

def inspect_revisions(data):
    need(isinstance(data, list) and len(data) == 1, 'REVISION_LIST_CHANGED')
    need(object_dict(data[0].get('metadata')).get('name') == REVISION,
         'REVISION_ID_CHANGED')
    return True

def inspect_sa(data):
    need(isinstance(data, dict) and data.get('email') == SA
         and str(data.get('uniqueId')) == SA_UID
         and data.get('disabled') is not True, 'SA_IDENTITY_CHANGED')
    return True

def main():
    os.umask(0o077)
    if sys.argv[1:] != ['--c1a-cleanup-preflight-once']:
        print('C1A_CLEANUP_PREFLIGHT=STOP_FLAG_REQUIRED')
        return 2
    home = Path.home()
    try:
        need(platform.system() == 'Linux' and 'microsoft' not in platform.release().lower()
             and os.geteuid() != 0, 'OWNER_CLOUD_SHELL_NONROOT_REQUIRED')
        need(home.is_dir() and not home.is_symlink(), 'HOME_UNSAFE')
        gcloud = shutil.which('gcloud')
        need(gcloud and Path(gcloud).is_file() and not gcloud.startswith('/mnt/'),
             'GCLOUD_NOT_FOUND')
        marker = home / MARKER
        need(not marker.exists() and not marker.is_symlink(), 'PREFLIGHT_MARKER_CONSUMED')
        dest = home / ('oldx-c1a-cleanup-preflight-' +
                       datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
        need(not dest.exists() and not dest.is_symlink(), 'EVIDENCE_COLLISION')
    except Stop as e:
        print('C1A_CLEANUP_PREFLIGHT=STOP_PREFLIGHT')
        print('C1A_REASON=' + str(e))
        return 2
    dest.mkdir(mode=0o700)
    fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY
                 | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(fd, 'w') as f:
        f.write('ATTEMPT_CONSUMED\nEVIDENCE=' + str(dest) + '\n')
    env = dict(os.environ)
    env.update({'CLOUDSDK_CORE_DISABLE_PROMPTS': '1',
                'CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK': '1',
                'CLOUDSDK_CORE_DISABLE_USAGE_REPORTING': '1'})
    def read(label, args, verifier):
        cmd = [gcloud, '--quiet', '--account=' + OWNER, '--project=' + PROJECT,
               *args, '--format=json']
        result = subprocess.run(cmd, cwd=str(home), env=env,
                                stdin=subprocess.DEVNULL, capture_output=True,
                                timeout=TIMEOUT)
        need(len(result.stdout) <= MAX_BYTES and len(result.stderr) <= MAX_BYTES,
             label + '_OUTPUT_TOO_BIG')
        (dest / (label + '.json')).write_bytes(result.stdout)
        (dest / (label + '.stderr')).write_bytes(result.stderr)
        (dest / (label + '.exit')).write_text(str(result.returncode))
        need(result.returncode == 0, label + '_READ_FAILED')
        try:
            parsed = json.loads(result.stdout)
        except (ValueError, UnicodeError):
            raise Stop(label + '_INVALID_JSON')
        verifier(parsed)
        return True
    passed = []
    reason, state = 'UNKNOWN', 'STOP'
    try:
        steps = [
            ('service',
             ['run', 'services', 'describe', SERVICE, '--region=' + REGION], inspect_service),
            ('service_iam',
             ['run', 'services', 'get-iam-policy', SERVICE, '--region=' + REGION], inspect_policy),
            ('revisions',
             ['run', 'revisions', 'list', '--service=' + SERVICE, '--region=' + REGION], inspect_revisions),
            ('runtime_sa',
             ['iam', 'service-accounts', 'describe', SA], inspect_sa),
        ]
        for name, args, verifier in steps:
            read(name, args, verifier)
            passed.append(name)
        state, reason = 'READ_ONLY_PASS_WITH_LIMITS', 'EXACT_HISTORIC_C1A_IDENTIFIERS_MATCH'
    except subprocess.TimeoutExpired:
        reason = 'GCLOUD_READ_TIMEOUT_STOP'
    except (Stop, OSError, subprocess.SubprocessError) as e:
        reason = str(e) if isinstance(e, Stop) else type(e).__name__
    finally:
        with marker.open('a') as f:
            f.write('RESULT=' + state + '\nREASON=' + reason + '\n')
        (dest / 'summary.json').write_text(json.dumps({
            'result': state, 'reason': reason,
            'passed': passed, 'read_only': True,
            'service': SERVICE, 'project': PROJECT,
            'cleaned_or_deleted': False,
        }, sort_keys=True) + '\n')
    print('C1A_VERIFIED_STAGES=' + ','.join(passed))
    print('C1A_CLEANUP_PREFLIGHT=' + state)
    print('C1A_REASON=' + reason)
    print('C1A_CLOUD_WRITES=NONE')
    print('C1A_RESOURCE_DELETED=NO')
    return 0 if state == 'READ_ONLY_PASS_WITH_LIMITS' else 2

if __name__ == '__main__':
    sys.exit(main())
