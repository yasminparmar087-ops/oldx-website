#!/usr/bin/env python3
"""OLDX Step05 H1B S3B: independently list only proposed NEW Cloud Run service & SA.

No change to project, auth, IAM or resources. S3 original evidence and marker
are READ-ONLY inputs. Distinct S3B marker is consumed before any Cloud call.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import stat
import subprocess
import sys
from datetime import datetime, timezone

OWNER = 'yasminparmar087@gmail.com'
PROJECT = 'oldx-staging'
PROJECT_NUMBER = '38472235077'
REGION = 'asia-south1'
REGISTRY = 'oldx-staging-images'
NEW_SERVICE = 'oldx-c2-website-mediator'
NEW_SA = 'oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com'
S3_MARKER = '.oldx-h1b-s3-cloudshell-readonly-once-20261125'
S3B_MARKER = '.oldx-h1b-s3b-target-list-once-20261126'
TIMEOUT = 20
MAX_OUTPUT = 512 * 1024

class Stop(Exception):
    pass

def require(ok, code):
    if not ok:
        raise Stop(code)

def private_file(path: Path):
    require(not path.is_symlink() and path.is_file() and path.stat().st_uid == os.geteuid(), 'UNSAFE_EVIDENCE_FILE')
    require(path.stat().st_size <= MAX_OUTPUT, 'EVIDENCE_OVERSIZE')

def verify_prior_evidence(home: Path):
    marker = home / S3_MARKER
    private_file(marker)
    lines = marker.read_text(encoding='utf-8').splitlines()
    require('S3_ATTEMPT_CONSUMED' in lines and 'RESULT=STOP' in lines
            and 'REASON=TARGET_STATUS_UNRESOLVED_STOP' in lines, 'S3_RECEIPT_NOT_EXPECTED')
    paths = [x.partition('=')[2] for x in lines if x.startswith('EVIDENCE=')]
    require(len(paths) == 1, 'S3_EVIDENCE_PATH_AMBIGUOUS')
    d = Path(paths[0])
    require(d.is_absolute() and d.parent == home and not d.is_symlink()
            and d.is_dir() and d.stat().st_uid == os.geteuid()
            and d.name.startswith('oldx-h1b-s3-cloudshell-readonly-'), 'S3_EVIDENCE_DIR_UNSAFE')
    def data(name):
        f = d / name
        private_file(f)
        return json.loads(f.read_text(encoding='utf-8'))
    owner = data('owner.stdout')
    require(isinstance(owner, list) and len([x for x in owner if isinstance(x, dict) and x.get('status') == 'ACTIVE']) == 1
            and any(x.get('account') == OWNER and x.get('status') == 'ACTIVE' for x in owner if isinstance(x, dict)),
            'PREVIOUS_OWNER_MISMATCH')
    project = data('project.stdout')
    require(isinstance(project, dict) and project.get('projectId') == PROJECT
            and str(project.get('projectNumber')) == PROJECT_NUMBER
            and project.get('lifecycleState') == 'ACTIVE', 'PREVIOUS_PROJECT_MISMATCH')
    registry = data('registry.stdout')
    require(isinstance(registry, dict) and registry.get('format') == 'DOCKER'
            and isinstance(registry.get('name'), str)
            and registry['name'].endswith('/locations/' + REGION + '/repositories/' + REGISTRY),
            'PREVIOUS_REGISTRY_MISMATCH')
    summary = data('summary.json')
    require(isinstance(summary, dict) and summary.get('result') == 'STOP'
            and summary.get('reason') == 'TARGET_STATUS_UNRESOLVED_STOP'
            and summary.get('project') == PROJECT and summary.get('region') == REGION,
            'PREVIOUS_SUMMARY_MISMATCH')
    return d

def classify_listing(command: str, rc: int, output: str, err: str):
    """Fail closed on any failed/incomplete list or unexpected schema."""
    if rc != 0:
        return 'UNRESOLVED_CLI_NONZERO'
    if re.search(r'(?i)(permission.denied|unauthenticated|\b403\b|\b401\b|\bpartial\b)', err):
        return 'UNRESOLVED_WARNING'
    try:
        values = json.loads(output)
    except ValueError:
        return 'UNRESOLVED_JSON'
    if not isinstance(values, list) or len(values) > 25000:
        return 'UNRESOLVED_LIST_SCHEMA'
    for entry in values:
        if not isinstance(entry, dict):
            return 'UNRESOLVED_ITEM_SCHEMA'
        if command == 'service':
            meta = entry.get('metadata')
            if meta is not None and not isinstance(meta, dict):
                return 'UNRESOLVED_ITEM_SCHEMA'
            name = (meta or {}).get('name') or entry.get('name')
            if not isinstance(name, str) or not name:
                return 'UNRESOLVED_ITEM_SCHEMA'
            if name.rsplit('/', 1)[-1] == NEW_SERVICE:
                return 'EXISTS_COLLISION_STOP'
        elif command == 'sa':
            email = entry.get('email')
            if not isinstance(email, str) or not email:
                return 'UNRESOLVED_ITEM_SCHEMA'
            if email == NEW_SA:
                return 'EXISTS_COLLISION_STOP'
        else:
            return 'INVALID_LIST_KIND'
    return 'ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS'

def run_list(gcloud: str, args: list[str], evidence: Path, stem: str, env: dict):
    # Each type queried at most once; exactly scoped CLI flag set.
    stdout_path = evidence / (stem + '.stdout')
    stderr_path = evidence / (stem + '.stderr')
    cmd = [gcloud, '--quiet', '--account=' + OWNER, '--project=' + PROJECT, *args, '--format=json']
    with stdout_path.open('xb') as out, stderr_path.open('xb') as err:
        proc = subprocess.Popen(cmd, stdout=out, stderr=err, stdin=subprocess.DEVNULL,
                                start_new_session=True, cwd=str(evidence.parent),
                                env=env, close_fds=True)
        try:
            rc = proc.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait(timeout=3)
            raise Stop(stem.upper() + '_TIMEOUT_NO_RETRY')
    require(stdout_path.stat().st_size <= MAX_OUTPUT and stderr_path.stat().st_size <= MAX_OUTPUT,
            stem.upper() + '_OUTPUT_LIMIT')
    (evidence / (stem + '.exit')).write_text(str(rc) + '\n', encoding='utf-8')
    return classify_listing(stem, rc, stdout_path.read_text(encoding='utf-8', errors='replace'),
                            stderr_path.read_text(encoding='utf-8', errors='replace'))

def main():
    os.umask(0o077)
    if sys.argv[1:] != ['--new-target-lists-once']:
        print('S3B_RESULT=STOP_FLAG_REQUIRED')
        return 2
    home = Path.home()
    try:
        require(platform.system() == 'Linux' and 'microsoft' not in platform.release().lower()
                and os.geteuid() != 0 and home.is_dir(), 'CLOUD_SHELL_NONROOT_REQUIRED')
        gcloud = shutil.which('gcloud')
        require(gcloud is not None and not gcloud.startswith('/mnt/') and Path(gcloud).is_file(), 'GCLOUD_NOT_FOUND')
        verify_prior_evidence(home)  # reads original S3 files, never reissues S3 requests
        marker = home / S3B_MARKER
        require(not marker.exists() and not marker.is_symlink(), 'S3B_MARKER_ALREADY_CONSUMED')
        evidence = home / ('oldx-h1b-s3b-new-targets-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
        require(not evidence.exists() and not evidence.is_symlink(), 'S3B_EVIDENCE_COLLISION')
    except (Stop, OSError, ValueError, json.JSONDecodeError) as exc:
        print('S3B_RESULT=STOP_PREFLIGHT')
        print('S3B_REASON=' + (str(exc) if isinstance(exc, Stop) else type(exc).__name__))
        return 2
    evidence.mkdir(mode=0o700)
    fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as fp:
        fp.write('S3B_ATTEMPT_CONSUMED\nEVIDENCE=' + str(evidence) + '\n')
    env = dict(os.environ)
    env.update({'CLOUDSDK_CORE_DISABLE_PROMPTS': '1',
                'CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK': '1',
                'CLOUDSDK_CORE_DISABLE_USAGE_REPORTING': '1'})
    service_state = sa_state = 'NOT_QUERIED'
    result = 'STOP'
    reason = 'UNDETERMINED'
    try:
        service_state = run_list(gcloud, ['run', 'services', 'list', '--region=' + REGION],
                                 evidence, 'service', env)
        if service_state == 'ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS':
            sa_state = run_list(gcloud, ['iam', 'service-accounts', 'list'], evidence, 'sa', env)
            if sa_state == 'ABSENT_FROM_SUCCESSFUL_LIST_WITH_LIMITS':
                result = 'READ_ONLY_PASS_WITH_LIMITS'
                reason = 'BOTH_TARGETS_ABSENT_IN_SUCCESSFUL_SCOPED_LISTS'
            elif sa_state == 'EXISTS_COLLISION_STOP':
                reason = 'NEW_SA_COLLISION'
            else:
                reason = 'NEW_SA_LIST_UNRESOLVED'
        elif service_state == 'EXISTS_COLLISION_STOP':
            reason = 'NEW_SERVICE_COLLISION'
        else:
            reason = 'NEW_SERVICE_LIST_UNRESOLVED'
    except (Stop, OSError, subprocess.SubprocessError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
    finally:
        with marker.open('a', encoding='utf-8') as fp:
            fp.write('RESULT=' + result + '\nREASON=' + reason + '\n')
        summary = {'result': result, 'reason': reason, 'service': service_state, 'sa': sa_state,
                   'scope': 'READ_ONLY_TARGET_LISTS', 'project': PROJECT, 'region': REGION,
                   'cloud_writes_requested': False}
        (evidence / 'summary.json').write_text(json.dumps(summary, sort_keys=True) + '\n', encoding='utf-8')
    print('S3B_SERVICE=' + service_state)
    print('S3B_SA=' + sa_state)
    print('S3B_RESULT=' + result)
    print('S3B_REASON=' + reason)
    print('S3B_CLOUD_WRITES=NONE')
    return 0 if result == 'READ_ONLY_PASS_WITH_LIMITS' else 2

if __name__ == '__main__':
    sys.exit(main())
