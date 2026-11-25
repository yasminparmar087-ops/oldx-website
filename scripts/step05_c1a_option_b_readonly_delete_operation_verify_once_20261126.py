#!/usr/bin/env python3
"""OLDX C1A Option B: one independent read-only Cloud Run delete confirmation.

No DELETE/retry, IAM writes, API enablement, image or SA operations.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import re
import shutil
import ssl
import subprocess
import sys
from datetime import datetime, timezone
from urllib import error, request

OWNER = 'yasminparmar087@gmail.com'
PROJECT = 'oldx-staging'
REGION = 'asia-south1'
SERVICE = 'oldx-step05-gateway'
FULL = f'projects/{PROJECT}/locations/{REGION}/services/{SERVICE}'
UID = 'bf441d37-e39b-4afd-b4c8-0e6edee7269b'
ORIGINAL = '.oldx-step05-c1a-option-b-conditional-service-delete-once-20261126'
ONCE = '.oldx-step05-c1a-option-b-service-delete-readback-once-20261126'
MAX_BYTES = 131072

class Stop(Exception):
    pass

def need(value, reason):
    if not value:
        raise Stop(reason)

def private_file(path):
    need(path.is_file() and not path.is_symlink()
         and path.stat().st_uid == os.geteuid()
         and 0 < path.stat().st_size <= MAX_BYTES, 'PRIVATE_RECEIPT_INVALID')

def prior_receipt(home):
    marker = home / ORIGINAL
    private_file(marker)
    rows = marker.read_text(encoding='utf-8').splitlines()
    need({'ATTEMPT_CONSUMED','RESULT=DELETE_ACCEPTED_PENDING_COMPLETION',
          'REASON=AWAIT_INDEPENDENT_OPERATION_AND_SERVICE_CHECK',
          'WRITE_ATTEMPTED=True'}.issubset(set(rows)),
         'ACTUAL_C1A_DELETE_RECEIPT_NOT_MATCHED')
    entries = [x.partition('=')[2] for x in rows if x.startswith('EVIDENCE=')]
    need(len(entries) == 1, 'EVIDENCE_PATH_AMBIGUOUS')
    folder = Path(entries[0])
    need(folder.parent == home and folder.name.startswith('oldx-c1a-service-delete-')
         and folder.is_dir() and not folder.is_symlink()
         and folder.stat().st_uid == os.geteuid(), 'EVIDENCE_FOLDER_INVALID')
    def load(name):
        file = folder / name
        private_file(file)
        return json.loads(file.read_text(encoding='utf-8'))
    summary = load('summary.json')
    need(isinstance(summary,dict)
         and summary.get('result') == 'DELETE_ACCEPTED_PENDING_COMPLETION'
         and summary.get('delete_attempted') is True
         and summary.get('service') == SERVICE
         and summary.get('sa_deleted') is False
         and summary.get('image_deleted') is False,
         'C1A_SAVED_SUMMARY_MISMATCH')
    op = load('operation.json')
    need(isinstance(op, dict) and isinstance(op.get('name'), str),
         'C1A_OPERATION_RECEIPT_INVALID')
    prefix = f'projects/{PROJECT}/locations/{REGION}/operations/'
    suffix = op['name'][len(prefix):] if op['name'].startswith(prefix) else ''
    need(bool(re.fullmatch(r'[A-Za-z0-9_.-]{1,200}',suffix)),
         'C1A_OPERATION_OUTSIDE_EXACT_SCOPE')
    need(op.get('done') is False and op.get('has_error') is False,
         'C1A_ORIGINAL_OPERATION_RECEIPT_CHANGED')
    return op['name']

def token_for_owner(gcloud):
    res = subprocess.run([gcloud,'--quiet','--account='+OWNER,'auth',
                          'print-access-token'],stdin=subprocess.DEVNULL,
                         capture_output=True,timeout=20)
    need(res.returncode == 0, 'OWNER_ACCESS_TOKEN_UNAVAILABLE')
    token = res.stdout.decode('ascii','strict').strip()
    need(bool(re.fullmatch(r'[A-Za-z0-9._~-]{40,4096}',token)),
         'OWNER_ACCESS_TOKEN_INVALID')
    return token

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def safe_get(token, name, allow_404=False):
    url = 'https://run.googleapis.com/v2/' + name
    req = request.Request(url,method='GET',headers={
        'Authorization':'Bearer '+token,'Accept':'application/json',
        'User-Agent':'OLDX-C1A-readonly-final-operation-check/1'})
    opener = request.build_opener(request.ProxyHandler({}),
        request.HTTPSHandler(context=ssl.create_default_context()), NoRedirect())
    try:
        with opener.open(req,timeout=20) as response:
            status = response.status
            data = response.read(MAX_BYTES+1)
    except error.HTTPError as exc:
        if exc.code == 404 and allow_404:
            return 404, None
        raise Stop('READ_ONLY_GET_HTTP_'+str(exc.code)) from None
    except (error.URLError,TimeoutError):
        raise Stop('READ_ONLY_GET_NETWORK_UNVERIFIED') from None
    need(status == 200 and len(data) <= MAX_BYTES,
         'READ_ONLY_GET_INVALID_RESPONSE')
    try:
        return 200,json.loads(data)
    except (ValueError,UnicodeError):
        raise Stop('READ_ONLY_GET_JSON_INVALID')

def interpret(operation_name, op, svc_status, svc):
    need(isinstance(op,dict) and op.get('name') == operation_name,
         'OPERATION_ID_CHANGED')
    metadata = op.get('metadata')
    if isinstance(metadata,dict) and metadata.get('target'):
        need(metadata['target'] == FULL,'OPERATION_TARGET_NOT_C1A')
    done = op.get('done') is True
    if op.get('error'):
        op_state = 'DONE_WITH_ERROR' if done else 'ERROR_PRESENT_UNEXPECTED'
    elif done:
        op_state = 'DONE_NO_ERROR'
    elif op.get('done') in (False,None):
        op_state = 'PENDING_OR_NOT_DONE'
    else:
        op_state = 'DONE_FIELD_INVALID'
    if svc_status == 404:
        svc_state = '404_NOT_FOUND'
    else:
        need(isinstance(svc,dict), 'SERVICE_GET_SCHEMA_UNKNOWN')
        if svc.get('name') != FULL or svc.get('uid') != UID:
            svc_state = 'PRESENT_IDENTITY_CHANGED_STOP'
        elif svc.get('deleteTime'):
            svc_state = 'PRESENT_DELETION_IN_PROGRESS'
        else:
            svc_state = 'PRESENT_SAME_UID'
    result = ('CONFIRMED_REMOVED' if op_state=='DONE_NO_ERROR'
              and svc_state=='404_NOT_FOUND' else
              'STOP_IDENTITY_CHANGED' if svc_state=='PRESENT_IDENTITY_CHANGED_STOP'
              else 'NOT_YET_CONFIRMED')
    return op_state,svc_state,result

def main():
    os.umask(0o077)
    if sys.argv[1:] != ['--verify-c1a-option-b-delete-readonly-once']:
        print('C1A_READBACK_RESULT=STOP_FLAG_REQUIRED')
        return 2
    home = Path.home()
    try:
        need(platform.system()=='Linux' and 'microsoft' not in platform.release().lower()
             and os.geteuid()!=0 and home.is_dir() and not home.is_symlink(),
             'OWNER_CLOUD_SHELL_REQUIRED')
        name = prior_receipt(home)
        gcloud = shutil.which('gcloud')
        need(gcloud and Path(gcloud).is_file() and not gcloud.startswith('/mnt/'),
             'GCLOUD_NOT_FOUND')
        marker = home / ONCE
        need(not marker.exists() and not marker.is_symlink(),
             'READBACK_ONESHOT_ALREADY_CONSUMED')
        folder = home / ('oldx-c1a-option-b-delete-readback-'+
               datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
        need(not folder.exists() and not folder.is_symlink(), 'EVIDENCE_COLLISION')
    except (Stop,OSError,UnicodeError,ValueError,TypeError) as exc:
        print('C1A_READBACK_RESULT=STOP_PREFLIGHT')
        print('C1A_REASON='+str(exc) if isinstance(exc,Stop)
              else 'C1A_REASON=LOCAL_PREFLIGHT_INVALID')
        return 2
    folder.mkdir(mode=0o700)
    fd = os.open(marker, os.O_EXCL|os.O_CREAT|os.O_WRONLY|
                 getattr(os,'O_NOFOLLOW',0),0o600)
    with os.fdopen(fd,'w') as f:
        f.write('ATTEMPT_CONSUMED\nEVIDENCE='+str(folder)+'\n')
    op_status='UNKNOWN'
    svc_status='UNKNOWN'
    result='STOP_UNVERIFIED'
    reason='UNDETERMINED'
    try:
        token = token_for_owner(gcloud)
        _,op = safe_get(token,name)
        _,svc = None,None
        service_http,svc = safe_get(token,FULL,allow_404=True)
        op_status,svc_status,result = interpret(name,op,service_http,svc)
        reason = ('OPERATION_SUCCESS_AND_C1A_SERVICE_404' if result=='CONFIRMED_REMOVED'
                  else 'READ_ONLY_STATE_REQUIRES_FOLLOWUP')
    except (Stop,OSError,ValueError,UnicodeError,TypeError,subprocess.TimeoutExpired) as exc:
        reason = str(exc) if isinstance(exc,Stop) else type(exc).__name__
    finally:
        (folder/'summary.json').write_text(json.dumps({
            'result':result,'reason':reason,'op_state':op_status,
            'service_state':svc_status,'cloud_writes':False,
            'sa_or_image_deleted':False},sort_keys=True)+'\n')
        with marker.open('a') as f:
            f.write('RESULT='+result+'\nREASON='+reason+'\n')
    print('C1A_OPERATION_STATE='+op_status)
    print('C1A_SERVICE_STATE='+svc_status)
    print('C1A_READBACK_RESULT='+result)
    print('C1A_REASON='+reason)
    print('C1A_CLOUD_WRITES=NONE')
    print('C1A_SERVICE_ACCOUNT_DELETED=NO')
    print('C1A_REGISTRY_IMAGE_DELETED=NO')
    return 0 if result=='CONFIRMED_REMOVED' else 2

if __name__ == '__main__':
    sys.exit(main())
