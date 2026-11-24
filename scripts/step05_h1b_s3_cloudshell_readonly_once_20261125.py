#!/usr/bin/env python3
"""OLDX Step05 H1B S3: one supervised Cloud Shell read-only owner and targets check.

S3 uses the logged-in Cloud Shell user, never auth login/config set/impersonation.
No Cloud writes, no deploys, no SDK repair. A separate S3 marker is consumed once.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

EXPECTED_ACCOUNT = 'yasminparmar087@gmail.com'
PROJECT = 'oldx-staging'
PROJECT_NUMBER = '38472235077'
REGION = 'asia-south1'
REGISTRY = 'oldx-staging-images'
SERVICE = 'oldx-c2-website-mediator'
SA = 'oldx-c2-mediator@oldx-staging.iam.gserviceaccount.com'
MARKER_NAME = '.oldx-h1b-s3-cloudshell-readonly-once-20261125'
TIMEOUT_SECONDS = 20

class Stop(Exception):
    pass

def require(condition, code):
    if not condition:
        raise Stop(code)

def active_owner(data):
    require(isinstance(data, list), 'ACTIVE_ACCOUNT_RESPONSE_INVALID')
    active = [x.get('account') for x in data
              if isinstance(x, dict) and x.get('status') == 'ACTIVE']
    require(len(active) == 1 and active[0] == EXPECTED_ACCOUNT,
            'EXPECTED_OWNER_NOT_ACTIVE')
    return True

def project_valid(data):
    require(isinstance(data, dict) and data.get('projectId') == PROJECT
            and str(data.get('projectNumber')) == PROJECT_NUMBER
            and data.get('lifecycleState') == 'ACTIVE',
            'PROJECT_IDENTITY_NOT_VERIFIED')
    return True

def registry_valid(data):
    require(isinstance(data, dict) and data.get('format') == 'DOCKER'
            and isinstance(data.get('name'), str)
            and data['name'].endswith('/locations/' + REGION + '/repositories/' + REGISTRY),
            'EXISTING_REPOSITORY_UNVERIFIED')
    return True

def target_state(returncode, stderr, stdout, kind):
    if returncode == 0:
        try:
            obj = json.loads(stdout)
            if not isinstance(obj, dict):
                return 'UNVERIFIED_RESPONSE'
        except (ValueError, TypeError):
            return 'UNVERIFIED_RESPONSE'
        if kind == 'service':
            name = obj.get('metadata', {}).get('name') if isinstance(obj.get('metadata'), dict) else obj.get('name')
            if isinstance(name, str) and name.split('/')[-1] == SERVICE:
                return 'EXISTS_COLLISION_STOP'
        elif kind == 'sa' and obj.get('email') == SA:
            return 'EXISTS_COLLISION_STOP'
        return 'UNVERIFIED_RESPONSE'
    # A reported 404 is still only negative evidence; masking and IAM remain possible.
    if (re.search(r'\b(?:NOT_FOUND|404)\b', stderr, flags=re.I)
            and not re.search(r'\b(?:PERMISSION_DENIED|403|UNAUTHENTICATED|401)\b', stderr, flags=re.I)):
        return 'API_NOT_FOUND_REPORTED_REVIEW_REQUIRED'
    return 'UNRESOLVED_ERROR_NOT_PROVEN_ABSENT'

def main():
    os.umask(0o077)
    if sys.argv[1:] != ['--s3-cloudshell-readonly-once']:
        print('S3_RESULT=STOP_FLAG_REQUIRED')
        return 2
    home = Path.home()
    try:
        require(platform.system() == 'Linux' and 'microsoft' not in platform.release().lower()
                and os.geteuid() != 0 and home.is_dir() and home != Path('/root'),
                'CLOUD_SHELL_NONROOT_REQUIRED')
        exe = shutil.which('gcloud')
        require(exe and not exe.startswith('/mnt/') and Path(exe).is_file(), 'GCLOUD_NOT_FOUND')
        marker = home / MARKER_NAME
        require(not marker.exists() and not marker.is_symlink(), 'S3_ALREADY_ATTEMPTED')
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        evidence = home / ('oldx-h1b-s3-cloudshell-readonly-' + stamp)
        require(not evidence.exists() and not evidence.is_symlink(), 'EVIDENCE_COLLISION')
    except Stop as err:
        print('S3_RESULT=STOP_PREFLIGHT')
        print('S3_REASON=' + str(err))
        return 2
    evidence.mkdir(mode=0o700)
    marker_fd = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(marker_fd, 'w', encoding='utf-8') as f:
        f.write('S3_ATTEMPT_CONSUMED\nEVIDENCE=' + str(evidence) + '\n')
    env = dict(os.environ)
    env['CLOUDSDK_CORE_DISABLE_PROMPTS'] = '1'
    env['CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK'] = '1'
    env['CLOUDSDK_CORE_DISABLE_USAGE_REPORTING'] = '1'
    env['CLOUDSDK_PYTHON_SITEPACKAGES'] = '0'
    def run(step, args):
        command = [exe, '--quiet', *args]
        try:
            r = subprocess.run(command, capture_output=True, text=True,
                               encoding='utf-8', errors='replace', timeout=TIMEOUT_SECONDS,
                               stdin=subprocess.DEVNULL, env=env, cwd=str(home))
            (evidence / (step + '.stdout')).write_text(r.stdout, encoding='utf-8')
            (evidence / (step + '.stderr')).write_text(r.stderr, encoding='utf-8')
            (evidence / (step + '.exit')).write_text(str(r.returncode) + '\n', encoding='utf-8')
            return r.returncode, r.stdout, r.stderr
        except subprocess.TimeoutExpired:
            raise Stop(step.upper() + '_TIMEOUT_STOP_NO_RETRY')
    result, reason = 'STOP', 'UNKNOWN'
    service_state = sa_state = 'NOT_QUERIED'
    try:
        rc, stdout, stderr = run('owner', ['auth', 'list', '--filter=status:ACTIVE', '--format=json'])
        require(rc == 0, 'ACTIVE_OWNER_READ_FAILED')
        active_owner(json.loads(stdout))
        print('S3_OWNER=EXPECTED_OWNER_ACTIVE')
        rc, stdout, stderr = run('project', ['projects', 'describe', PROJECT, '--format=json'])
        require(rc == 0, 'PROJECT_READ_FAILED')
        project_valid(json.loads(stdout))
        print('S3_PROJECT=EXACT_ID_NUMBER_ACTIVE')
        rc, stdout, stderr = run('registry', ['artifacts', 'repositories', 'describe', REGISTRY,
                                            '--project=' + PROJECT, '--location=' + REGION, '--format=json'])
        require(rc == 0, 'EXISTING_REGISTRY_READ_FAILED')
        registry_valid(json.loads(stdout))
        print('S3_EXISTING_REGISTRY=DOCKER_VERIFIED_READ_ONLY')
        rc, stdout, stderr = run('new-service', ['run', 'services', 'describe', SERVICE,
                                                '--project=' + PROJECT, '--region=' + REGION, '--format=json'])
        service_state = target_state(rc, stderr, stdout, 'service')
        print('S3_NEW_SERVICE=' + service_state)
        rc, stdout, stderr = run('new-sa', ['iam', 'service-accounts', 'describe', SA,
                                           '--project=' + PROJECT, '--format=json'])
        sa_state = target_state(rc, stderr, stdout, 'sa')
        print('S3_NEW_SA=' + sa_state)
        if service_state == 'API_NOT_FOUND_REPORTED_REVIEW_REQUIRED' and sa_state == 'API_NOT_FOUND_REPORTED_REVIEW_REQUIRED':
            result, reason = 'READ_ONLY_PASS_WITH_LIMITS', 'NEGATIVE_LOOKUPS_REQUIRE_INDEPENDENT_REVIEW'
        elif 'EXISTS_COLLISION_STOP' in (service_state, sa_state):
            reason = 'NEW_TARGET_COLLISION_STOP'
        else:
            reason = 'TARGET_STATUS_UNRESOLVED_STOP'
    except (Stop, json.JSONDecodeError, OSError) as error:
        reason = str(error) if isinstance(error, Stop) else type(error).__name__
    finally:
        with marker.open('a', encoding='utf-8') as f:
            f.write('RESULT=' + result + '\nREASON=' + reason + '\n')
        (evidence / 'summary.json').write_text(json.dumps({
            'result': result, 'reason': reason, 'service': service_state, 'sa': sa_state,
            'project': PROJECT, 'region': REGION, 'cloud_writes': False,
            'auth_login_or_account_change': False,
        }, sort_keys=True) + '\n', encoding='utf-8')
    print('S3_RESULT=' + result)
    print('S3_REASON=' + reason)
    print('S3_CLOUD_WRITE=NONE')
    print('S3_EXISTING_S1_S1R_S2_MARKERS=UNTOUCHED')
    return 0 if result == 'READ_ONLY_PASS_WITH_LIMITS' else 2

if __name__ == '__main__':
    sys.exit(main())
