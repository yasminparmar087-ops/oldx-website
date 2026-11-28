#!/usr/bin/env python3
"""BAJUTO Step05 H2AG: ONE approved SA create + ONE exact CryptoKey IAM update.

Scope strictly oldx-staging, read-only KMS reader, no keys or signing.
One-shot marker BEFORE first mutation. Never replay on STOP/partial result.
This script cannot prove inherited IAM grants or hosted runtime identity.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import ssl
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error

ROOT = Path('/root')
PROJECT = 'oldx-staging'
OWNER = 'yasminparmar087@gmail.com'
READER_ID = 'oldx-c2-kms-reader'
READER = READER_ID + '@oldx-staging.iam.gserviceaccount.com'
DISPLAY = 'BAJUTO C2 KMS metadata reader'
SIGNER = 'oldx-c2-private-gateway@oldx-staging.iam.gserviceaccount.com'
SIGNER_MEMBER = 'serviceAccount:' + SIGNER
READER_MEMBER = 'serviceAccount:' + READER
GATEWAY_UID = '107238619872767759560'
OLD_UIDS = frozenset({
    '100779414920484819274', GATEWAY_UID,
    '106984791114720194680', '110217058111344002447',
})
KEY = ('projects/oldx-staging/locations/asia-south1/keyRings/'
       'oldx-c2-h2-signing/cryptoKeys/oldx-c2-attestation-rs256')
IAM_ROOT = 'https://iam.googleapis.com/v1/projects/' + PROJECT + '/serviceAccounts'
SA_URL = IAM_ROOT + '/' + READER
KMS_ROOT = 'https://cloudkms.googleapis.com/v1/' + KEY
POLICY_GET = KMS_ROOT + ':getIamPolicy?options.requestedPolicyVersion=3'
POLICY_SET = KMS_ROOT + ':setIamPolicy'
ROLES = ('roles/cloudkms.viewer', 'roles/cloudkms.publicKeyViewer')
H2R = ROOT / '.oldx-step05-h2r-gateway-single-key-signer-grant-once-20261127'
MARK = ROOT / '.oldx-step05-h2ag-one-reader-sa-two-key-only-roles-once-20261128'
SDK = ROOT / 'oldx-tools/native-gcloud-594.0.1/google-cloud-sdk'
CLI = SDK / 'bin/gcloud'
PY = SDK / 'platform/bundledpythonunix/bin/python3'
CONFIG = ROOT / 'oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config'
FLAG = '--h2ag-owner-approved-one-kms-reader-sa-and-two-key-only-read-roles-once'
UID_RE = re.compile(r'[0-9]{10,32}\Z')
TOKEN_RE = re.compile(r'[A-Za-z0-9._~+\-]{40,4096}\Z')

class Stop(Exception):
    pass

def need(cond, reason):
    if not cond:
        raise Stop(reason)

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None

OPENER = request.build_opener(
    request.ProxyHandler({}),
    request.HTTPSHandler(context=ssl.create_default_context()),
    NoRedirect(),
)

def old_marker():
    need(H2R.is_file() and not H2R.is_symlink() and H2R.stat().st_uid == 0
         and H2R.stat().st_size <= 4096, 'H2R_PRIOR_MARKER_NOT_TRUSTED')
    lines = H2R.read_text(encoding='utf-8').splitlines()
    for x in ('ATTEMPT_CONSUMED=TRUE', 'PROJECT=' + PROJECT, 'KEY=' + KEY,
              'RESULT=PASS_EXACT_ONE_CRYPTOKEY_GATEWAY_SIGNER_BINDING_VERIFIED'):
        need(x in lines, 'H2R_PRIOR_SIGNER_PASS_NOT_CONFIRMED')

def owner_token():
    need(sys.argv[1:] == [FLAG], 'EXACT_H2AG_OWNER_APPROVAL_FLAG_REQUIRED')
    need(platform.system() == 'Linux' and os.geteuid() == 0
         and 'microsoft' in platform.release().lower(), 'ROOT_WSL_REQUIRED')
    need(not MARK.exists() and not MARK.is_symlink(), 'H2AG_ONE_SHOT_ALREADY_CONSUMED')
    old_marker()
    need(SDK.is_dir() and not SDK.is_symlink() and SDK.stat().st_uid == 0,
         'NATIVE_SDK_UNTRUSTED')
    need(CLI.is_file() and not CLI.is_symlink() and CLI.stat().st_uid == 0
         and os.access(CLI, os.X_OK), 'NATIVE_CLI_UNTRUSTED')
    resolved_py = PY.resolve(strict=True)
    need(resolved_py.is_relative_to(SDK.resolve(strict=True))
         and resolved_py.is_file() and resolved_py.stat().st_uid == 0
         and os.access(resolved_py, os.X_OK), 'NATIVE_PYTHON_UNTRUSTED')
    need(CONFIG.is_dir() and not CONFIG.is_symlink()
         and CONFIG.stat().st_uid == 0, 'ISOLATED_CONFIG_UNTRUSTED')
    env = dict(os.environ)
    env.update({'HOME': str(ROOT), 'PATH': str(SDK / 'bin') + ':/usr/bin:/bin',
                'CLOUDSDK_CONFIG': str(CONFIG), 'CLOUDSDK_PYTHON': str(PY),
                'CLOUDSDK_CORE_DISABLE_USAGE_REPORTING': '1',
                'CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK': '1',
                'CLOUDSDK_CORE_CHECK_GCE_METADATA': 'false'})
    env.pop('GOOGLE_APPLICATION_CREDENTIALS', None)
    env.pop('CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE', None)

    def cli(args):
        try:
            p = subprocess.run([str(CLI), *args], env=env,
                               stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               timeout=28, check=False)
        except subprocess.TimeoutExpired:
            raise Stop('OWNER_GCLOUD_TIMEOUT') from None
        need(p.returncode == 0, 'OWNER_GCLOUD_FAILED')
        return p.stdout.decode('utf-8', 'strict').strip()

    need(cli(['auth', 'list', '--filter=status:ACTIVE',
              '--format=value(account)']) == OWNER, 'WRONG_OWNER_ACCOUNT')
    need(cli(['config', 'get-value', 'project']) == PROJECT, 'WRONG_PROJECT')
    token = cli(['--quiet', '--account=' + OWNER,
                 'auth', 'print-access-token'])
    need(TOKEN_RE.fullmatch(token) is not None, 'OWNER_TOKEN_UNAVAILABLE')
    return token

def exact_policy(p, include_reader=False):
    need(type(p) is dict and set(p).issubset({'version','etag','bindings'})
         and p.get('version', 1) in (1, 3)
         and type(p.get('version', 1)) is int
         and isinstance(p.get('etag'), str)
         and 0 < len(p['etag']) <= 512
         and isinstance(p.get('bindings'), list),
         'CRYPTOKEY_POLICY_SCHEMA_OR_ETAG_DRIFT')
    expected = [('roles/cloudkms.signer', (SIGNER_MEMBER,))]
    if include_reader:
        expected += [(role, (READER_MEMBER,)) for role in ROLES]
    actual = []
    for b in p['bindings']:
        need(type(b) is dict and set(b) == {'role', 'members'}
             and isinstance(b['role'], str)
             and type(b['members']) is list
             and len(b['members']) == 1 and isinstance(b['members'][0], str),
             'CRYPTOKEY_POLICY_EXTRA_BINDING_OR_CONDITION')
        actual.append((b['role'], tuple(b['members'])))
    need(len(actual) == len(expected) and set(actual) == set(expected),
         'CRYPTOKEY_SIGNER_OR_READER_BINDING_DRIFT')
    return p['etag']

def identity(sa, expected_uid=None):
    need(type(sa) is dict and sa.get('email') == READER
         and isinstance(sa.get('uniqueId'), str)
         and UID_RE.fullmatch(sa['uniqueId']) is not None
         and sa['uniqueId'] not in OLD_UIDS
         and type(sa.get('disabled', False)) is bool
         and sa.get('disabled', False) is False,
         'READER_EMAIL_UID_OR_DISABLED_STATE_INVALID')
    need(sa.get('projectId', PROJECT) == PROJECT,
         'READER_PROJECT_DRIFT')
    if sa.get('name') is not None:
        need(sa['name'] in (
            'projects/' + PROJECT + '/serviceAccounts/' + READER,
            'projects/' + PROJECT + '/serviceAccounts/' + sa['uniqueId']),
            'READER_CANONICAL_NAME_DRIFT')
    if expected_uid is not None:
        need(sa['uniqueId'] == expected_uid, 'READER_NUMERIC_UID_DRIFT')
    return sa['uniqueId']

def payload_create():
    return {'accountId': READER_ID,
            'serviceAccount': {'displayName': DISPLAY}}

def payload_set(policy):
    old_etag = exact_policy(policy)
    return {'policy': {'version': policy.get('version', 1), 'etag': old_etag,
                       'bindings': [
                           {'role': 'roles/cloudkms.signer',
                            'members': [SIGNER_MEMBER]},
                           {'role': ROLES[0], 'members': [READER_MEMBER]},
                           {'role': ROLES[1], 'members': [READER_MEMBER]},
                       ]}, 'updateMask': 'bindings,etag'}

def api(method, url, token, body=None, allowed_numeric_uid=None):
    permitted = (
        (method == 'GET' and body is None and url in (SA_URL, POLICY_GET)) or
        (method == 'GET' and body is None
         and isinstance(allowed_numeric_uid, str)
         and UID_RE.fullmatch(allowed_numeric_uid) is not None
         and allowed_numeric_uid not in OLD_UIDS
         and url == IAM_ROOT + '/' + allowed_numeric_uid) or
        (method == 'POST' and url == IAM_ROOT and body == payload_create()) or
        (method == 'POST' and url == POLICY_SET and type(body) is dict
         and set(body) == {'policy','updateMask'}
         and body.get('updateMask') == 'bindings,etag'
         and type(body.get('policy')) is dict
         and exact_policy(body['policy'], include_reader=True))
    )
    need(permitted, 'CLOUD_API_METHOD_OR_PAYLOAD_OUTSIDE_H2AG_SCOPE')
    raw = json.dumps(body, sort_keys=True, separators=(',',':')).encode('utf-8') if body is not None else None
    req = request.Request(url, method=method, data=raw, headers={
        'Authorization': 'Bearer ' + token, 'Accept': 'application/json',
        'User-Agent': 'BAJUTO-H2AG-one-SA-two-key-only-reader-roles/1',
        **({'Content-Type': 'application/json'} if raw is not None else {})})
    try:
        with OPENER.open(req, timeout=35) as resp:
            raw_resp = resp.read(65537)
            need(len(raw_resp) <= 65536, 'H2AG_API_RESPONSE_TOO_LARGE')
            need(resp.status == 200, 'H2AG_UNEXPECTED_HTTP_STATUS')
            parsed = json.loads(raw_resp)
            need(type(parsed) is dict, 'H2AG_API_RESPONSE_NOT_JSON_OBJECT')
            return 200, parsed
    except error.HTTPError as e:
        code = e.code
        e.close()
        return code, {}
    except (error.URLError, ssl.SSLError, TimeoutError):
        raise Stop('H2AG_API_NETWORK_OR_TIMEOUT_UNKNOWN_NO_RETRY') from None

def append(stage):
    # Never print tokens, full policies, PII or policy ETags.
    with MARK.open('a', encoding='utf-8') as out:
        out.write(stage + '\n')

def main():
    os.umask(0o077)
    try:
        token = owner_token()
        # Check ONLY the new SA and existing exact CryptoKey, before any write.
        code, _ = api('GET', SA_URL, token)
        need(code == 404, 'READER_ACCOUNT_ALREADY_EXISTS_OR_NOT_PROVEN_ABSENT_HTTP_' + str(code))
        code, before = api('GET', POLICY_GET, token)
        need(code == 200, 'EXACT_KEY_IAM_PREIMAGE_HTTP_' + str(code))
        etag = exact_policy(before)
    except (Stop, OSError, TypeError, ValueError, UnicodeError) as e:
        print('H2AG_RESULT=STOP_BEFORE_CLOUD_WRITE')
        print('H2AG_REASON=' + (str(e) if isinstance(e, Stop) else type(e).__name__))
        print('H2AG_CLOUD_WRITES=NONE')
        print('H2AG_H2_PRODUCTION=NO_GO')
        return 2

    evidence = ROOT / ('oldx-h2ag-reader-key-only-' +
        datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    try:
        evidence.mkdir(mode=0o700)
        fd = os.open(str(MARK), os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                     getattr(os,'O_NOFOLLOW',0), 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write('ATTEMPT_CONSUMED=TRUE\nPROJECT=' + PROJECT + '\n')
            f.write('KEY=' + KEY + '\nREADER_EMAIL=' + READER + '\n')
            f.write('H2R_SIGNER_UID=' + GATEWAY_UID + '\nEVIDENCE=' + str(evidence) + '\n')
            f.write('PREWRITE_ETAG_SHA256=' + hashlib.sha256(etag.encode('utf-8')).hexdigest() + '\n')
    except OSError:
        print('H2AG_RESULT=STOP_MARKER_CREATION')
        print('H2AG_H2_PRODUCTION=NO_GO')
        return 2

    print('H2AG_MARKER=CONSUMED_NO_REPEAT', flush=True)
    result, reason = 'STOP_AFTER_MARKER_POSSIBLE_PARTIAL_CLOUD_WRITE', 'UNKNOWN'
    sa_create = False
    key_write = False
    verified_sa = False
    verified_key = False
    uid = 'NOT_VERIFIED'
    try:
        append('STAGE=CREATE_EXACT_ONE_KMS_READER_SA_ABOUT_TO_SEND')
        sa_create = True
        code, created = api('POST', IAM_ROOT, token, payload_create())
        need(code == 200, 'READER_CREATE_HTTP_' + str(code))
        uid = identity(created)
        print('H2AG_READER_CREATED_UID=' + uid, flush=True)
        # Google IAM service account visibility can lag one successful create.
        # Read only by immutable numeric UID; no create attempt is repeated.
        for delay in (0, 1, 2, 4):
            if delay:
                time.sleep(delay)
            append('STAGE=READ_EXACT_SA_NUMERIC_UID')
            code, observed = api('GET', IAM_ROOT + '/' + uid, token,
                                 allowed_numeric_uid=uid)
            if code == 404:
                continue
            need(code == 200, 'READER_READBACK_HTTP_' + str(code))
            identity(observed, uid)
            verified_sa = True
            break
        need(verified_sa, 'READER_UID_READBACK_NOT_VISIBLE')
        print('H2AG_READER_SA_UID_ENABLED=VERIFIED', flush=True)

        # Protect the original signer; exact fresh policy MUST remain identical
        # to the one seen before SA creation, including unchanged ETag.
        append('STAGE=FRESH_KEY_POLICY_PREWRITE_READ')
        code, current = api('GET', POLICY_GET, token)
        need(code == 200 and current == before, 'CRYPTO_KEY_IAM_CHANGED_SINCE_PREFLIGHT')
        body = payload_set(current)
        append('STAGE=ONE_EXACT_KEY_IAM_SET_ABOUT_TO_SEND')
        key_write = True
        code, updated = api('POST', POLICY_SET, token, body)
        need(code == 200, 'TWO_READER_ROLE_KEY_IAM_HTTP_' + str(code))
        after_etag = exact_policy(updated, include_reader=True)
        need(after_etag != etag, 'KEY_POLICY_ETAG_DID_NOT_ADVANCE')
        print('H2AG_READER_READ_ONLY_KEY_ROLES_POST=VERIFIED', flush=True)
        append('STAGE=ONE_POST_WRITE_KEY_POLICY_READBACK')
        code, actual = api('GET', POLICY_GET, token)
        need(code == 200 and exact_policy(actual, include_reader=True) == after_etag,
             'KMS_KEY_ROLE_READBACK_MISMATCH')
        verified_key = True
        result, reason = 'ONE_READER_SA_TWO_KEY_READ_ONLY_ROLES_PASS', 'UID_AND_EXACT_ETAG_POLICY_READBACK_VERIFIED'
    except (Stop, OSError, ValueError, TypeError, UnicodeError, KeyError) as e:
        reason = str(e) if isinstance(e, Stop) else type(e).__name__
    finally:
        try:
            sanitized = {
                'project': PROJECT, 'cryptoKey': KEY, 'readerEmail': READER,
                'readerUid': uid, 'signerUid': GATEWAY_UID,
                'prewriteEtagSha256': hashlib.sha256(etag.encode('utf-8')).hexdigest(),
                'saCreateAttempted': sa_create, 'readerUidVerified': verified_sa,
                'keyPolicyWriteAttempted': key_write, 'keyPolicyReadbackVerified': verified_key,
                'result': result, 'reason': reason, 'otherIAMProjectRingRoleChanges': False,
                'kmsSigning': False, 'newKeys': False, 'firebaseRunProductWrites': False,
                'h2': 'NO_GO', 'production': 'NO_GO',
            }
            (evidence / 'sanitized-h2ag-receipt.json').write_text(
                json.dumps(sanitized, sort_keys=True, indent=2) + '\n', encoding='utf-8')
            append('RESULT=' + result)
            append('REASON=' + reason)
        except OSError:
            result = 'STOP_EVIDENCE_WRITE'
        print('H2AG_READER_SA=' + (uid if verified_sa else 'NOT_VERIFIED'))
        print('H2AG_SA_CREATE_ATTEMPTED=' + str(sa_create).upper())
        print('H2AG_ONE_KEY_IAM_WRITE_ATTEMPTED=' + str(key_write).upper())
        print('H2AG_KEY_READER_ROLES_READBACK=' + ('VERIFIED' if verified_key else 'NOT_VERIFIED'))
        print('H2AG_EXISTING_GATEWAY_SIGNER=' + ('PRESERVED_VERIFIED' if verified_key else 'UNKNOWN_NO_ASSUMPTIONS'))
        print('H2AG_OLD_H2R_H2AF_MARKERS=UNTOUCHED')
        print('H2AG_OTHER_IAM_KMS_SIGN_FIRESTORE_RUN_WRITES=NONE')
        print('H2AG_H2_PRODUCTION=NO_GO')
        print('H2AG_DO_NOT_REPEAT=TRUE')
        print('H2AG_RESULT=' + result)
        print('H2AG_REASON=' + reason)
    return 0 if result == 'ONE_READER_SA_TWO_KEY_READ_ONLY_ROLES_PASS' else 2

if __name__ == '__main__':
    sys.exit(main())
