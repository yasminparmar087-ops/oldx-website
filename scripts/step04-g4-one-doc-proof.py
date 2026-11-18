#!/usr/bin/env python3
"""OLDX Step 04: exact-scope, owner-supervised Firestore one-document IAM proof.

Requires separately recorded Yasmin consent. This is NOT a hosted B1 deploy,
Firestore Rules validation, or cross-database isolation test. Run ONCE only.
No auth users, roles, keys, services, IAM, billing or production changes.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

PROJECT = 'oldx-staging'
ACCOUNT = 'yasminparmar087@gmail.com'
RUNTIME = 'oldx-product-read-staging@oldx-staging.iam.gserviceaccount.com'
COLLECTION = 'oldxG4IamProof_v1'
DB_ROOT = 'projects/oldx-staging/databases/(default)'
BASE = 'https://firestore.googleapis.com/v1/' + DB_ROOT + '/documents/'
TOKEN_URL = 'https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/' + RUNTIME + ':generateAccessToken'
JOURNAL_DIRNAME = '.oldx-g4-one-document-v1'
TOKEN_PATTERN = re.compile(r'^[A-Za-z0-9._~+/\-]{20,8192}={0,2}$')
TIME_PATTERN = re.compile(r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,9})?Z$')
PERFORM_WORD = 'YASMIN_APPROVED_ONE_SYNTHETIC_G4_DOC_20261118'
REQUEST_CAP = 12

class Stop(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code

class HttpResult:
    def __init__(self, status, body):
        self.status, self.body = status, body

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

OPENER = urllib.request.build_opener(NoRedirect())

def request(method, url, token, payload=None):
    # Only exact Google API host prefixes constructed by this fixed script.
    if not (url.startswith(BASE + COLLECTION + '/') or
            url.startswith(BASE + COLLECTION + '?') or url == TOKEN_URL):
        raise Stop('UNEXPECTED_ENDPOINT')
    if not TOKEN_PATTERN.fullmatch(token):
        raise Stop('INVALID_TOKEN_SHAPE')
    body = None if payload is None else json.dumps(payload, separators=(',', ':')).encode('utf-8')
    req = urllib.request.Request(url, data=body, method=method, headers={
        'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json',
        'Accept': 'application/json', 'User-Agent': 'oldx-g4-one-doc-evidence/1',
    })
    try:
        with OPENER.open(req, timeout=12) as response:
            raw = response.read(32769)
            if len(raw) > 32768:
                raise Stop('OVERSIZE_RESPONSE')
            return HttpResult(response.status, _json(raw))
    except urllib.error.HTTPError as exc:
        # Error bodies are not printed, only a sanitized error status.
        raw = exc.read(32769)
        if len(raw) > 32768:
            raise Stop('OVERSIZE_ERROR')
        return HttpResult(exc.code, _json(raw))
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise Stop('NETWORK_OUTCOME_UNCERTAIN') from None

def _json(data):
    if not data:
        return {}
    try:
        value = json.loads(data)
        if isinstance(value, dict):
            return value
    except (ValueError, UnicodeDecodeError):
        pass
    raise Stop('INVALID_JSON_RESPONSE')

def _cli(*args):
    try:
        result = subprocess.run(['gcloud', *args], capture_output=True, text=True,
                                check=False, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        raise Stop('GCLOUD_UNAVAILABLE') from None
    if result.returncode != 0:
        raise Stop('GCLOUD_REJECTED')
    return result.stdout.strip()

def guard_operator():
    if _cli('config', 'get-value', 'project') != PROJECT:
        raise Stop('WRONG_PROJECT')
    if _cli('auth', 'list', '--filter=status:ACTIVE', '--format=value(account)') != ACCOUNT:
        raise Stop('WRONG_OPERATOR')
    try:
        p = json.loads(_cli('projects', 'get-iam-policy', PROJECT, '--format=json',
                            '--account=' + ACCOUNT))
    except (ValueError, KeyError):
        raise Stop('OWNER_POLICY_UNVERIFIED') from None
    bindings = p.get('bindings', [])
    matching = [b for b in bindings if b.get('role') == 'roles/owner' and
                'user:' + ACCOUNT in b.get('members', []) and 'condition' not in b]
    if len(matching) != 1:
        raise Stop('OPERATOR_CLEANUP_ROLE_UNVERIFIED')
    # Owner grant is configuration, NOT verified effective DELETE (deny/PAB may apply).
    return _cli('auth', 'print-access-token', '--account=' + ACCOUNT, '--quiet')

def runtime_credential(operator_token):
    r = request('POST', TOKEN_URL, operator_token, {'scope': [
        'https://www.googleapis.com/auth/datastore'], 'lifetime': '300s'})
    if r.status != 200:
        raise Stop('RUNTIME_TOKEN_DENIED')
    token = r.body.get('accessToken')
    expiry = r.body.get('expireTime')
    if not isinstance(token, str) or not TOKEN_PATTERN.fullmatch(token) or token == operator_token:
        raise Stop('RUNTIME_TOKEN_UNVERIFIED')
    try:
        exp = dt.datetime.fromisoformat(expiry.replace('Z', '+00:00'))
        left = (exp - dt.datetime.now(dt.timezone.utc)).total_seconds()
    except (ValueError, AttributeError):
        raise Stop('RUNTIME_TOKEN_EXPIRY_UNVERIFIED') from None
    if not 70 < left <= 305:
        raise Stop('RUNTIME_TOKEN_EXPIRY_UNVERIFIED')
    return token

def fields(marker, revision):
    return {'purpose': {'stringValue': 'OLDX_G4_EXACT_IAM_PROOF_ONLY'},
            'marker': {'stringValue': marker},
            'revision': {'integerValue': str(revision)}}

def valid_document(body, name, marker, revision, created=None):
    f = body.get('fields', {})
    if (body.get('name') != name or
        f.get('purpose', {}).get('stringValue') != 'OLDX_G4_EXACT_IAM_PROOF_ONLY' or
        f.get('marker', {}).get('stringValue') != marker or
        f.get('revision', {}).get('integerValue') != str(revision)):
        raise Stop('PROVENANCE_MISMATCH')
    ct, ut = body.get('createTime'), body.get('updateTime')
    if not isinstance(ct, str) or not TIME_PATTERN.fullmatch(ct) or not isinstance(ut, str) or not TIME_PATTERN.fullmatch(ut):
        raise Stop('TIMESTAMP_UNVERIFIED')
    if created is not None and ct != created:
        raise Stop('CREATION_TIME_DRIFT')
    return ct, ut

def get_exact(token, url, caller=request):
    r = caller('GET', url, token)
    if r.status == 404:
        return None
    if r.status != 200:
        raise Stop('DOCUMENT_GET_UNVERIFIED')
    return r.body

def journal_path():
    return Path.home() / JOURNAL_DIRNAME

def durable_record(directory, record, *, first=False):
    path = directory / 'journal.json'
    raw = (json.dumps(record, sort_keys=True, indent=2) + '\n').encode('utf-8')
    if first:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, 'O_NOFOLLOW'):
            flags |= os.O_NOFOLLOW
        fd = os.open(path, flags, 0o600)
        with os.fdopen(fd, 'wb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
    else:
        tmp = directory / ('journal-' + secrets.token_hex(8) + '.tmp')
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, 'O_NOFOLLOW'):
            flags |= os.O_NOFOLLOW
        fd = os.open(tmp, flags, 0o600)
        with os.fdopen(fd, 'wb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    dfd = os.open(directory, os.O_RDONLY)
    try: os.fsync(dfd)
    finally: os.close(dfd)

def update(directory, record, state, **values):
    record.update(values)
    record['state'] = state
    durable_record(directory, record)
    print('G4_STAGE=' + state, flush=True)

def report_status():
    p = journal_path()
    try:
        if p.is_symlink() or (p.stat().st_mode & 0o077) != 0:
            raise Stop('JOURNAL_NOT_PRIVATE')
        obj = json.loads((p / 'journal.json').read_text('utf-8'))
    except (FileNotFoundError, ValueError, OSError):
        raise Stop('JOURNAL_UNAVAILABLE') from None
    print('G4_PROJECT=' + str(obj.get('project', 'UNKNOWN')))
    print('G4_STATE=' + str(obj.get('state', 'UNKNOWN')))
    print('G4_DOCUMENT_PATH=' + str(obj.get('document', 'UNKNOWN')))
    print('G4_CLOUD_ACTION=NONE_IN_STATUS')

def run_once():
    if os.name != 'posix':
        raise Stop('LINUX_WSL_REQUIRED')
    directory = journal_path()
    if directory.exists() or directory.is_symlink():
        raise Stop('EXISTING_JOURNAL_REQUIRES_REVIEW')
    oldmask = os.umask(0o077)
    try:
        directory.mkdir(mode=0o700)
    finally:
        os.umask(oldmask)
    marker = secrets.token_hex(20)
    docid = 'g4-proof-' + secrets.token_hex(12)
    document = COLLECTION + '/' + docid
    name = DB_ROOT + '/documents/' + document
    url = BASE + document
    record = {'project': PROJECT, 'database': '(default)', 'document': document,
              'marker': marker, 'state': 'INITIALIZED', 'createTime': None,
              'updateTime': None, 'runtimeDeleteStatus': 'UNVERIFIED',
              'operatorCleanupStatus': 'NOT_ATTEMPTED'}
    durable_record(directory, record, first=True)
    print('G4_SCOPE=oldx-staging/(default)/' + document, flush=True)
    print('G4_JOURNAL=PRIVATE_LOCAL_PERSISTED', flush=True)
    operator_token = None
    runtime_token = None
    calls = 0
    def limited(method, link, token, payload=None):
        nonlocal calls
        calls += 1
        if calls > REQUEST_CAP:
            raise Stop('REQUEST_BUDGET_EXCEEDED')
        return request(method, link, token, payload)
    try:
        operator_token = guard_operator()
        if not TOKEN_PATTERN.fullmatch(operator_token):
            raise Stop('OPERATOR_TOKEN_INVALID')
        update(directory, record, 'OPERATOR_ROLE_CONFIGURED_NOT_EFFECTIVE')
        runtime_token = runtime_credential(operator_token)
        update(directory, record, 'RUNTIME_TOKEN_READY')
        # One fresh collision check, same exact ID and BOTH identities, before write.
        if get_exact(operator_token, url, limited) is not None or get_exact(runtime_token, url, limited) is not None:
            raise Stop('COLLISION_OR_UNEXPECTED_DOCUMENT')
        update(directory, record, 'EXACT_ABSENCE_VERIFIED')
        # One create attempt. Any uncertain outcome stays in private journal, no blind retry.
        update(directory, record, 'CREATE_UNKNOWN')
        resp = limited('POST', BASE + COLLECTION + '?documentId=' + docid,
                       runtime_token, {'fields': fields(marker, 1)})
        if resp.status != 200:
            raise Stop('CREATE_DENIED_OR_FAILED')
        ct, ut = valid_document(resp.body, name, marker, 1)
        update(directory, record, 'CREATED_VERIFIED', createTime=ct, updateTime=ut)
        # Conditional UPDATE of only revision field; preserve immutable marker.
        query = urllib.parse.urlencode({'updateMask.fieldPaths': 'revision',
                                        'currentDocument.updateTime': ut})
        update(directory, record, 'UPDATE_UNKNOWN')
        resp = limited('PATCH', url + '?' + query, runtime_token,
                       {'name': name, 'fields': {'revision': {'integerValue': '2'}}})
        if resp.status != 200:
            raise Stop('UPDATE_DENIED_OR_FAILED')
        ct2, ut2 = valid_document(resp.body, name, marker, 2, ct)
        if ut2 == ut:
            raise Stop('UPDATE_TIME_NOT_ADVANCED')
        update(directory, record, 'UPDATED_VERIFIED', updateTime=ut2)
        # Exactly ONE runtime DELETE-denial attempt with updateTime precondition.
        update(directory, record, 'RUNTIME_DELETE_OUTCOME_UNKNOWN')
        resp = limited('DELETE', url + '?' + urllib.parse.urlencode({
            'currentDocument.updateTime': ut2}), runtime_token)
        if resp.status != 403 or resp.body.get('error', {}).get('status') != 'PERMISSION_DENIED':
            update(directory, record, 'RUNTIME_DELETE_UNEXPECTED', runtimeDeleteStatus=str(resp.status))
            raise Stop('RUNTIME_DELETE_NOT_PROVEN_DENIED')
        update(directory, record, 'RUNTIME_DELETE_DENIED_VERIFIED', runtimeDeleteStatus='403_PERMISSION_DENIED')
        # Verify document still exists and unchanged BEFORE cleanup with distinct operator OAuth.
        existing = get_exact(operator_token, url, limited)
        if existing is None:
            raise Stop('DOC_MISSING_AFTER_DENIED_DELETE')
        ct3, ut3 = valid_document(existing, name, marker, 2, ct)
        if ut3 != ut2:
            raise Stop('UPDATE_TIME_DRIFT')
        update(directory, record, 'OPERATOR_CLEANUP_OUTCOME_UNKNOWN')
        resp = limited('DELETE', url + '?' + urllib.parse.urlencode({
            'currentDocument.updateTime': ut3}), operator_token)
        if resp.status not in (200, 204):
            raise Stop('OPERATOR_CLEANUP_FAILED')
        # One read-only empty check after exact conditional delete.
        if get_exact(operator_token, url, limited) is not None:
            raise Stop('DOC_STILL_PRESENT_AFTER_CLEANUP')
        update(directory, record, 'CLEANUP_VERIFIED', operatorCleanupStatus='PASS')
        print('G4_RUNTIME_CREATE=PASS')
        print('G4_RUNTIME_UPDATE=PASS')
        print('G4_RUNTIME_DELETE=DENIED_403_PERMISSION_DENIED')
        print('G4_OPERATOR_EXACT_CLEANUP=PASS')
        print('G4_CROSS_DATABASE=UNVERIFIED')
        print('G4_HOSTED_STAGING=NOT_CHANGED')
        print('G4_RESULT=ONE_DOC_PROOF_PASS_WITH_CLEANUP')
    except Stop as ex:
        # Never mask an uncertain mutation by retrying or automated bulk cleanup.
        # Owner can inspect this exact private journal for a separately reviewed recovery.
        print('G4_STOP=' + ex.code)
        print('G4_FINAL_STATE=' + record['state'])
        print('G4_PRIVATE_JOURNAL=' + str(directory))
        if record['state'] in ('INITIALIZED', 'OPERATOR_ROLE_CONFIGURED_NOT_EFFECTIVE',
                               'RUNTIME_TOKEN_READY', 'EXACT_ABSENCE_VERIFIED'):
            print('G4_NEW_DOCUMENT=NOT_YET_ATTEMPTED')
        else:
            print('G4_NEW_DOCUMENT=MAY_REMAIN_REQUIRES_EXACT_MANUAL_REVIEW')
        print('G4_B1_PRODUCTION=NOT_CHANGED')
        raise

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--status', action='store_true')
    p.add_argument('--execute', action='store_true')
    p.add_argument('--approved-once', default='')
    args = p.parse_args()
    if args.status and not args.execute and args.approved_once == '':
        report_status(); return 0
    if args.execute and not args.status and args.approved_once == PERFORM_WORD:
        run_once(); return 0
    raise Stop('EXACT_ONE_SHOT_APPROVAL_ARGUMENT_REQUIRED')

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Stop as e:
        # Error messages or raw API exception payloads are never disclosed.
        print('STOP: ' + e.code)
        sys.exit(2)
    except (KeyboardInterrupt, Exception):
        print('STOP: INTERRUPTED_OR_UNEXPECTED_ERROR_CHECK_PRIVATE_JOURNAL')
        sys.exit(2)
