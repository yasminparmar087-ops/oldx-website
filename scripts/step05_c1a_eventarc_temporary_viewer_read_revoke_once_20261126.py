#!/usr/bin/env python3
"""OLDX C1A: approved temporary Eventarc Viewer grant/read/revoke, one-shot.

Project-only IAM time-conditional grant; always attempt exact revocation.
NO Cloud Run deletion and no other Cloud writes. Local safeguards fail closed.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import sys
from datetime import datetime, timedelta, timezone

PROJECT = 'oldx-staging'
OWNER = 'yasminparmar087@gmail.com'
MEMBER = 'user:' + OWNER
ROLE = 'roles/eventarc.viewer'
C1A = 'oldx-step05-gateway'
PRIOR = '.oldx-step05-c1a-cli-read-failure-diagnostic-once-20261126'
MARKER = '.oldx-step05-c1a-eventarc-temp-viewer-grant-list-revoke-once-20261126'
MAX_DATA = 1024 * 1024
TTL_MINUTES = 25

class Halt(Exception):
    pass

def need(cond, reason):
    if not cond:
        raise Halt(reason)

def safe_file(p, home):
    need(p.parent == home and p.is_file() and not p.is_symlink()
         and p.stat().st_uid == os.geteuid() and p.stat().st_size < 16384,
         'PREVIOUS_C1A_MARKER_UNSAFE')

def check_prior(home):
    p = home / PRIOR
    safe_file(p, home)
    lines = p.read_text(encoding='utf-8').splitlines()
    need({'ATTEMPT_CONSUMED', 'RESULT=STOP',
          'REASON=IAM_OR_EVENTARC_DIAG_NEEDS_REVIEW'}.issubset(set(lines)),
         'PREVIOUS_C1A_CLI_DIAG_NOT_STOP')
    dirs = [r.partition('=')[2] for r in lines if r.startswith('EVIDENCE=')]
    need(len(dirs) == 1, 'PREVIOUS_EVIDENCE_PATH_INVALID')
    root = Path(dirs[0])
    need(root.parent == home and root.name.startswith('oldx-c1a-cli-read-diagnostic-')
         and root.is_dir() and not root.is_symlink() and root.stat().st_uid == os.geteuid(),
         'PREVIOUS_EVIDENCE_DIR_UNSAFE')
    summary = root / 'summary.json'
    need(summary.is_file() and not summary.is_symlink() and summary.stat().st_size < 16384,
         'PREVIOUS_EVIDENCE_SUMMARY_UNSAFE')
    data = json.loads(summary.read_text(encoding='utf-8'))
    need(isinstance(data, dict) and data.get('result') == 'STOP'
         and data.get('iam') == 'NO_DIRECT_BINDINGS'
         and data.get('eventarc') == 'PERMISSION_DENIED'
         and data.get('writes_attempted') is False
         and data.get('deleted') is False,
         'PREVIOUS_EVIDENCE_VALUES_UNEXPECTED')

def parse_policy(obj):
    need(isinstance(obj, dict) and isinstance(obj.get('bindings', []), list),
         'PROJECT_IAM_POLICY_SCHEMA_UNKNOWN')
    for b in obj.get('bindings', []):
        need(isinstance(b, dict) and isinstance(b.get('role'), str)
             and isinstance(b.get('members'), list), 'PROJECT_IAM_BINDING_SCHEMA_UNKNOWN')
    return obj['bindings'] if 'bindings' in obj else []

def own_bindings(policy):
    return [b for b in parse_policy(policy)
            if b['role'] == ROLE and MEMBER in b['members']]

def precise_binding(policy, title, expression):
    matched = [b for b in parse_policy(policy) if b['role'] == ROLE
               and isinstance(b.get('condition'), dict)
               and b['condition'].get('title') == title
               and b['condition'].get('expression') == expression]
    return matched

def trigger_inspection(payload):
    need(isinstance(payload, list), 'EVENTARC_ALL_LOCATIONS_LIST_NOT_ARRAY')
    count = 0
    for obj in payload:
        need(isinstance(obj, dict) and isinstance(obj.get('name'), str)
             and obj['name'].startswith('projects/' + PROJECT + '/locations/')
             and '/triggers/' in obj['name'], 'EVENTARC_TRIGGER_SCHEMA_UNKNOWN')
        dest = obj.get('destination')
        need(isinstance(dest, dict), 'EVENTARC_DESTINATION_MISSING')
        cloud = dest.get('cloudRun', dest.get('cloud_run'))
        if cloud is not None:
            need(isinstance(cloud, dict) and isinstance(cloud.get('service'), str)
                 and bool(cloud['service']), 'EVENTARC_CLOUDRUN_DESTINATION_UNVERIFIED')
            if cloud['service'].rstrip('/').split('/')[-1] == C1A:
                return 'C1A_DEPENDENCY_EXISTS_STOP', len(payload)
        else:
            # Explicit, recognized non-Cloud-Run destinations only.
            need(any(k in dest for k in ('workflow', 'gke', 'httpEndpoint', 'http_endpoint')),
                 'EVENTARC_UNRECOGNIZED_DESTINATION')
        count += 1
    return 'NO_C1A_TRIGGER_IN_SUCCESSFUL_ALL_LOCATION_LIST_WITH_LIMITS', count

class CLI:
    def __init__(self, exe, home, evidence):
        self.exe, self.home, self.evidence = exe, home, evidence
        self.env = dict(os.environ)
        self.env.update(CLOUDSDK_CORE_DISABLE_PROMPTS='1',
                        CLOUDSDK_CORE_DISABLE_USAGE_REPORTING='1',
                        CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK='1')
    def run(self, name, args, timeout=40):
        args = [self.exe, '--quiet', '--account=' + OWNER, '--project=' + PROJECT, *args]
        try:
            r = subprocess.run(args, capture_output=True, timeout=timeout,
                               stdin=subprocess.DEVNULL, cwd=str(self.home), env=self.env)
        except subprocess.TimeoutExpired:
            return None, 'TIMEOUT', None
        if len(r.stdout) > MAX_DATA or len(r.stderr) > MAX_DATA:
            return None, 'OUTPUT_TOO_LARGE', None
        (self.evidence / (name+'.exit')).write_text(str(r.returncode)+'\n')
        (self.evidence / (name+'.stdout')).write_bytes(r.stdout)
        (self.evidence / (name+'.stderr')).write_bytes(r.stderr)
        if r.returncode != 0:
            return r.returncode, 'NONZERO', None
        return r.returncode, 'OK', r.stdout
    def json(self, name, args, timeout=40):
        _, code, output = self.run(name, args+['--format=json'], timeout)
        need(code == 'OK', name.upper() + '_' + code)
        try: return json.loads(output)
        except (TypeError,ValueError,UnicodeError): raise Halt(name.upper()+'_INVALID_JSON')


def assert_owner(accounts):
    need(isinstance(accounts, list), 'OWNER_AUTH_RESPONSE_INVALID')
    active = [x.get('account') for x in accounts
              if isinstance(x, dict) and x.get('status') == 'ACTIVE']
    need(active == [OWNER], 'EXPECTED_OWNER_NOT_SOLE_ACTIVE_ACCOUNT')


def one_shot_main():
    os.umask(0o077)
    if sys.argv[1:] != ['--temporary-eventarc-viewer-once']:
        print('C1A_EVENTARC_GRANT_RESULT=STOP_FLAG_REQUIRED')
        return 2
    home = Path.home()
    try:
        need(platform.system() == 'Linux' and 'microsoft' not in platform.release().lower()
             and os.geteuid() != 0 and home.is_dir() and not home.is_symlink(),
             'OWNER_CLOUD_SHELL_REQUIRED')
        check_prior(home)
        exe = shutil.which('gcloud')
        need(exe and Path(exe).is_file() and not exe.startswith('/mnt/'), 'GCLOUD_NOT_FOUND')
        marker = home / MARKER
        need(not marker.exists() and not marker.is_symlink(), 'ONESHOT_CONSUMED')
        evidence = home / ('oldx-c1a-eventarc-temp-viewer-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
        need(not evidence.exists() and not evidence.is_symlink(), 'EVIDENCE_COLLISION')
    except (Halt, OSError, ValueError, TypeError) as e:
        print('C1A_EVENTARC_GRANT_RESULT=STOP_PREFLIGHT')
        print('C1A_EVENTARC_REASON='+ (str(e) if isinstance(e, Halt) else type(e).__name__))
        return 2
    evidence.mkdir(mode=0o700)
    fd = os.open(marker, os.O_CREAT|os.O_EXCL|os.O_WRONLY|getattr(os,'O_NOFOLLOW',0), 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write('ATTEMPT_CONSUMED\nEVIDENCE='+str(evidence)+'\n')
    cli = CLI(exe, home, evidence)
    granted = False
    grant_attempted = False
    initial_verified = False
    list_result = 'NOT_QUERIED'
    revoke_result = 'NOT_NEEDED'
    reason = 'UNKNOWN'
    expiry = ''
    condition = ''
    title = 'OLDX_C1A_EVTARC_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    def interruption(_sig, _frame):
        raise Halt('INTERRUPTED_CLEANUP_REQUIRED')
    signal.signal(signal.SIGTERM, interruption)
    try:
        assert_owner(cli.json('active-owner', ['auth','list','--filter=status:ACTIVE']))
        initial = cli.json('iam-before', ['projects','get-iam-policy',PROJECT])
        parse_policy(initial)
        need(not own_bindings(initial), 'PREEXISTING_EVENTARC_VIEWER_BINDING_STOP')
        need(not any(b.get('condition',{}).get('title') == title
                     for b in parse_policy(initial) if isinstance(b.get('condition'),dict)),
             'CONDITION_TITLE_ALREADY_EXISTS')
        initial_verified = True
        expiry = (datetime.now(timezone.utc)+timedelta(minutes=TTL_MINUTES)).strftime('%Y-%m-%dT%H:%M:%SZ')
        expression = 'request.time < timestamp("' + expiry + '")'
        condition='expression='+expression+',title='+title
        (evidence/'grant-scope.json').write_text(json.dumps({
           'project':PROJECT,'member':MEMBER,'role':ROLE,'title':title,
           'expiration_utc':expiry,'condition_expression':expression},sort_keys=True)+'\n')
        grant_attempted = True
        _,code,_ = cli.run('iam-add', ['projects','add-iam-policy-binding',PROJECT,
                          '--member='+MEMBER,'--role='+ROLE,'--condition='+condition], timeout=45)
        need(code == 'OK','IAM_ADD_'+code)
        after_add = cli.json('iam-after-add', ['projects','get-iam-policy',PROJECT])
        b = precise_binding(after_add,title,expression)
        need(len(b)==1 and b[0].get('members') == [MEMBER], 'IAM_NEW_BINDING_UNVERIFIED')
        granted = True
        # The permission is temporary and conditionally time-bound even on process failure.
        rows = cli.json('eventarc-all-locations',
                        ['eventarc','triggers','list','--location=-'], timeout=75)
        list_result, count = trigger_inspection(rows)
        (evidence/'eventarc-classification.json').write_text(
            json.dumps({'classification':list_result,'trigger_count':count,
                        'project':PROJECT}, sort_keys=True)+'\n')
        need(list_result=='NO_C1A_TRIGGER_IN_SUCCESSFUL_ALL_LOCATION_LIST_WITH_LIMITS',
             list_result)
        reason = 'EVENTARC_LIST_COMPLETE_NEEDS_REVOKE'
    except (Halt, OSError, ValueError, TypeError, UnicodeError, subprocess.SubprocessError) as e:
        reason = str(e) if isinstance(e,Halt) else type(e).__name__
    except KeyboardInterrupt:
        reason = 'INTERRUPTED_CLEANUP_REQUIRED'
    finally:
        if grant_attempted and condition:
            try:
                expression = 'request.time < timestamp("' + expiry + '")'
                after = cli.json('iam-before-revoke',['projects','get-iam-policy',PROJECT])
                matching = precise_binding(after,title,expression)
                if not matching:
                    revoke_result = 'BINDING_NOT_PRESENT_VERIFIED'
                elif len(matching)==1 and matching[0].get('members')==[MEMBER]:
                    _,code,_=cli.run('iam-remove',['projects','remove-iam-policy-binding',PROJECT,
                                   '--member='+MEMBER,'--role='+ROLE,'--condition='+condition],timeout=45)
                    if code!='OK':
                        revoke_result = 'REMOVE_FAILED_OR_TIMEOUT'
                    else:
                        check = cli.json('iam-after-revoke',['projects','get-iam-policy',PROJECT])
                        revoke_result = ('REMOVED_AND_VERIFIED'
                                         if not precise_binding(check,title,expression)
                                         else 'STILL_PRESENT_AFTER_REMOVE')
                else:
                    revoke_result = 'UNEXPECTED_BINDING_MEMBERS_STOP_MANUAL'
            except (Halt, OSError,ValueError,TypeError,UnicodeError,subprocess.SubprocessError) as e:
                revoke_result = 'REVOKE_UNVERIFIED_' + (str(e) if isinstance(e,Halt) else type(e).__name__)
        if revoke_result in ('REMOVED_AND_VERIFIED','BINDING_NOT_PRESENT_VERIFIED'):
            result = ('READ_ONLY_PASS_WITH_LIMITS' if list_result==
                      'NO_C1A_TRIGGER_IN_SUCCESSFUL_ALL_LOCATION_LIST_WITH_LIMITS'
                      else 'STOP_WITH_REVOKE_VERIFIED')
        elif grant_attempted:
            result='STOP_IAM_REVOCATION_NOT_VERIFIED'
        else:
            result='STOP_NO_ROLE_ADDED'
        (evidence/'summary.json').write_text(json.dumps({
            'result':result,'reason':reason,'list_result':list_result,
            'grant_attempted':grant_attempted,'grant_verified':granted,
            'revoke_result':revoke_result,'expires_utc':expiry,
            'cloud_run_deleted':False,'service_account_deleted':False,
            'registry_image_deleted':False},sort_keys=True)+'\n')
        with marker.open('a',encoding='utf-8') as f:
            f.write('RESULT='+result+'\nREASON='+reason+'\nREVOKE='+revoke_result+'\n')
    print('C1A_EVENTARC_GRANTED='+str(granted).upper())
    print('C1A_EVENTARC_LIST='+list_result)
    print('C1A_EVENTARC_REVOKE='+revoke_result)
    print('C1A_EVENTARC_TEMP_EXPIRES_UTC='+expiry)
    print('C1A_EVENTARC_RESULT='+result)
    print('C1A_EVENTARC_REASON='+reason)
    print('C1A_CLOUD_RUN_DELETED=NO')
    print('C1A_SERVICE_ACCOUNT_DELETED=NO')
    print('C1A_REGISTRY_IMAGE_DELETED=NO')
    if result=='STOP_IAM_REVOCATION_NOT_VERIFIED':
        print('C1A_URGENT_MANUAL_IAM_REVOKE=REQUIRED')
    return 0 if result=='READ_ONLY_PASS_WITH_LIMITS' else 2

if __name__ == '__main__':
    sys.exit(one_shot_main())
