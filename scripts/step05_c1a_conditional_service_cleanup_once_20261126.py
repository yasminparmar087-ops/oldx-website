#!/usr/bin/env python3
"""OLDX C1A: ONE service-only Cloud Run conditional deletion with exact UID + etag.

Preconditions: actual owner-approved original C1A cleanup preflight PASS and
previous private evidence intact. Does NOT delete service account, image,
Artifact Registry repository, H1B, or any other Cloud Run service.
Every API call is bounded. No retry if a write has been attempted.
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
from urllib import error, parse, request

OWNER='yasminparmar087@gmail.com'
PROJECT='oldx-staging'
REGION='asia-south1'
SERVICE='oldx-step05-gateway'
FULL=f'projects/{PROJECT}/locations/{REGION}/services/{SERVICE}'
UID='bf441d37-e39b-4afd-b4c8-0e6edee7269b'
REV='oldx-step05-gateway-00001-thd'
SA='oldx-step05-gateway@oldx-staging.iam.gserviceaccount.com'
SA_UID='102194769236111252832'
IMAGE=('asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/'
       'oldx-step05-gateway-off@sha256:612f3c02806a93d991127f87e34391646edf9bad251bb22b8aace90a434bc30a')
PREFLIGHT_MARKER='.oldx-step05-c1a-cleanup-readonly-once-20261126'
DELETE_MARKER='.oldx-step05-c1a-conditional-service-delete-once-20261126'
BASE='https://run.googleapis.com/v2/'
MAX_BODY=256*1024

class Stop(Exception): pass

def need(ok, reason):
    if not ok: raise Stop(reason)

def private_file(file, uid):
    need(file.is_file() and not file.is_symlink() and file.stat().st_uid==uid
         and file.stat().st_size<=MAX_BODY, 'PRIVATE_EVIDENCE_FILE_UNSAFE')

def validate_preflight(home:Path):
    marker=home/PREFLIGHT_MARKER
    private_file(marker,os.geteuid())
    rows=marker.read_text().splitlines()
    need({'ATTEMPT_CONSUMED', 'RESULT=READ_ONLY_PASS_WITH_LIMITS',
          'REASON=EXACT_HISTORIC_C1A_IDENTIFIERS_MATCH'}.issubset(set(rows)),
         'ORIGINAL_C1A_PREFLIGHT_NOT_PASS')
    dirs=[r.partition('=')[2] for r in rows if r.startswith('EVIDENCE=')]
    need(len(dirs)==1,'ORIGINAL_C1A_EVIDENCE_AMBIGUOUS')
    folder=Path(dirs[0])
    need(folder.parent==home and folder.is_dir() and not folder.is_symlink()
         and folder.name.startswith('oldx-c1a-cleanup-preflight-')
         and folder.stat().st_uid==os.geteuid(),'ORIGINAL_C1A_EVIDENCE_UNSAFE')
    def load(name):
        f=folder/name
        private_file(f,os.geteuid())
        return json.loads(f.read_text())
    summary=load('summary.json')
    need(summary.get('result')=='READ_ONLY_PASS_WITH_LIMITS'
         and summary.get('reason')=='EXACT_HISTORIC_C1A_IDENTIFIERS_MATCH'
         and summary.get('passed')==['service','service_iam','revisions','runtime_sa']
         and summary.get('read_only') is True
         and summary.get('cleaned_or_deleted') is False,'C1A_PRIOR_SUMMARY_MISMATCH')
    # Preserve previous exact successful v1 findings; the new v2 GET below
    # independently checks the resource's CURRENT UID + etag before deletion.
    v1=load('service.json')
    need(v1.get('metadata',{}).get('uid')==UID
         and v1.get('metadata',{}).get('name')==SERVICE
         and v1.get('status',{}).get('latestReadyRevisionName')==REV,
         'C1A_PRIOR_SERVICE_MISMATCH')
    need(not load('service_iam.json').get('bindings'),'C1A_PRIOR_DIRECT_IAM_MISMATCH')
    revisions=load('revisions.json')
    need(isinstance(revisions,list) and len(revisions)==1
         and revisions[0].get('metadata',{}).get('name')==REV,
         'C1A_PRIOR_REVISIONS_MISMATCH')
    sa=load('runtime_sa.json')
    need(sa.get('email')==SA and str(sa.get('uniqueId'))==SA_UID,
         'C1A_PRIOR_SA_MISMATCH')
    return True

def inspect_current(service):
    need(isinstance(service,dict) and service.get('name')==FULL
         and service.get('uid')==UID, 'C1A_V2_UID_CHANGED')
    etag=service.get('etag')
    need(isinstance(etag,str) and 1<=len(etag)<=256, 'C1A_ETAG_MISSING')
    need(service.get('reconciling') is False,'C1A_RECONCILING_OR_UNKNOWN')
    need(not service.get('deleteTime'),'C1A_ALREADY_DELETING')
    need(service.get('invokerIamDisabled') is not True, 'C1A_IAM_CHECK_DISABLED')
    need(str(service.get('generation'))==str(service.get('observedGeneration'))
         and service.get('generation') is not None, 'C1A_GENERATION_MISMATCH')
    def rev(v):
        return isinstance(v,str) and v.rsplit('/',1)[-1]==REV
    need(rev(service.get('latestReadyRevision')) and rev(service.get('latestCreatedRevision')),
         'C1A_V2_REVISION_CHANGED')
    template=service.get('template')
    need(isinstance(template,dict) and template.get('serviceAccount')==SA,
         'C1A_V2_SA_CHANGED')
    containers=template.get('containers')
    need(isinstance(containers,list) and len(containers)==1
         and isinstance(containers[0],dict) and containers[0].get('image')==IMAGE,
         'C1A_V2_IMAGE_CHANGED')
    need(not containers[0].get('env') and not template.get('volumes'),
         'C1A_V2_ENV_OR_VOLUME_CHANGED')
    targets=service.get('trafficStatuses')
    need(isinstance(targets,list) and len(targets)==1
         and isinstance(targets[0],dict) and targets[0].get('percent')==100
         and rev(targets[0].get('revision')) and not targets[0].get('tag'),
         'C1A_V2_TRAFFIC_STATUS_CHANGED')
    desired=service.get('traffic')
    need(isinstance(desired,list) and len(desired)==1
         and desired[0].get('percent')==100 and not desired[0].get('tag'),
         'C1A_V2_DESIRED_TRAFFIC_CHANGED')
    return etag

def service_iam_ok(p):
    need(isinstance(p,dict) and not p.get('bindings'), 'C1A_DIRECT_IAM_NOW_CHANGED')

def eventarc_ok(items):
    need(isinstance(items,list), 'C1A_EVENTARC_LIST_UNVERIFIED')
    for trigger in items:
        need(isinstance(trigger,dict),'C1A_EVENTARC_ITEM_INVALID')
        dest=trigger.get('destination')
        need(isinstance(dest,dict),'C1A_EVENTARC_DESTINATION_UNKNOWN')
        run=dest.get('cloudRun') or dest.get('cloud_run')
        if isinstance(run,dict):
            need(run.get('service')!=SERVICE,'C1A_EVENTARC_TRIGGER_DEPENDENCY')
        elif run is not None:
            raise Stop('C1A_EVENTARC_DESTINATION_UNKNOWN')
    return True

class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def http_json(token,method,path,params=None):
    url=BASE+path
    if params: url+='?'+parse.urlencode(params)
    req=request.Request(url,headers={'Authorization':'Bearer '+token,
                    'Accept':'application/json','User-Agent':'OLDX-C1A-guarded-service-cleanup/1'},
                    method=method)
    opener=request.build_opener(request.ProxyHandler({}),
            request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())
    try:
        with opener.open(req,timeout=20) as response:
            status=response.status
            raw=response.read(MAX_BODY+1)
    except error.HTTPError as exc:
        raise Stop(method+'_HTTP_'+str(exc.code)) from None
    except (error.URLError,TimeoutError) as exc:
        raise Stop(method+'_NETWORK_UNCERTAIN_'+type(exc).__name__) from None
    need(len(raw)<=MAX_BODY,method+'_HTTP_RESPONSE_TOO_LARGE')
    need(status==200,'HTTP_UNEXPECTED_STATUS_'+str(status))
    try:return json.loads(raw)
    except (ValueError,UnicodeError):raise Stop(method+'_INVALID_RESPONSE_JSON')

def cli_json(gcloud,args):
    cmd=[gcloud,'--quiet','--account='+OWNER,'--project='+PROJECT,*args,'--format=json']
    r=subprocess.run(cmd,capture_output=True,timeout=20,stdin=subprocess.DEVNULL)
    need(r.returncode==0 and len(r.stdout)<=MAX_BODY and len(r.stderr)<=MAX_BODY,
         'C1A_LIVE_CLI_READ_FAILED')
    try:return json.loads(r.stdout)
    except (UnicodeError,ValueError):raise Stop('C1A_LIVE_CLI_JSON_INVALID')

def get_token(gcloud):
    p=subprocess.run([gcloud,'--quiet','--account='+OWNER,'auth','print-access-token'],
                     stdin=subprocess.DEVNULL,capture_output=True,timeout=20)
    need(p.returncode==0,'C1A_OWNER_TOKEN_UNAVAILABLE')
    s=p.stdout.decode('ascii','strict').strip()
    need(bool(re.fullmatch(r'[A-Za-z0-9._~-]{40,4096}',s)),'C1A_OWNER_TOKEN_INVALID')
    return s

def main():
    os.umask(0o077)
    if sys.argv[1:]!=['--delete-only-c1a-service-once']:
        print('C1A_SERVICE_DELETE_RESULT=STOP_FLAG_REQUIRED')
        return 2
    home=Path.home()
    try:
        need(platform.system()=='Linux' and 'microsoft' not in platform.release().lower()
             and os.geteuid()!=0 and not home.is_symlink(),'CLOUD_SHELL_REQUIRED')
        gcloud=shutil.which('gcloud')
        need(gcloud and Path(gcloud).is_file() and not gcloud.startswith('/mnt/'),
             'GCLOUD_NOT_FOUND')
        validate_preflight(home)
        marker=home/DELETE_MARKER
        need(not marker.exists() and not marker.is_symlink(),'DELETE_ONESHOT_ALREADY_CONSUMED')
        evidence=home/('oldx-c1a-service-delete-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
        need(not evidence.exists() and not evidence.is_symlink(),'EVIDENCE_COLLISION')
    except (Stop,OSError,ValueError,TypeError) as exc:
        print('C1A_SERVICE_DELETE_RESULT=STOP_PREFLIGHT')
        print('C1A_REASON='+str(exc) if isinstance(exc,Stop) else 'C1A_REASON=INVALID_EVIDENCE')
        return 2
    evidence.mkdir(mode=0o700)
    fd=os.open(marker,os.O_EXCL|os.O_CREAT|os.O_WRONLY|getattr(os,'O_NOFOLLOW',0),0o600)
    with os.fdopen(fd,'w') as fh:
        fh.write('ATTEMPT_CONSUMED\nEVIDENCE='+str(evidence)+'\n')
    state,reason='STOP','UNDETERMINED'
    write_sent=False
    etag_verified=False
    try:
        token=get_token(gcloud)
        live=http_json(token,'GET',FULL)
        etag=inspect_current(live)
        # Do not save access token or raw private API payload in GitHub or stdout.
        (evidence/'current-service-redacted.json').write_text(json.dumps({
            'uid_match':True,'etag_sha256':__import__('hashlib').sha256(etag.encode()).hexdigest(),
            'revision':REV,'image_digest':IMAGE.rsplit('@',1)[-1],
            'iam_check_enabled':True},sort_keys=True)+'\n')
        policy=cli_json(gcloud,['run','services','get-iam-policy',SERVICE,'--region='+REGION])
        service_iam_ok(policy)
        # If Eventarc not readable/disabled, do not infer zero triggers.
        eventarc=cli_json(gcloud,['eventarc','triggers','list','--location='+REGION])
        eventarc_ok(eventarc)
        # API v2 validation with SAME etag; no deletion yet.
        probe=http_json(token,'DELETE',FULL,{'etag':etag,'validateOnly':'true'})
        need(isinstance(probe,dict) and isinstance(probe.get('name'),str)
             and probe['name'].startswith(f'projects/{PROJECT}/locations/{REGION}/operations/'),
             'C1A_DELETE_VALIDATION_RESPONSE_UNVERIFIED')
        etag_verified=True
        # ONE real etag-conditional DELETE attempt; after this line, error can mean
        # unknown write outcome. Do not blindly retry.
        write_sent=True
        op=http_json(token,'DELETE',FULL,{'etag':etag})
        need(isinstance(op,dict) and isinstance(op.get('name'),str)
             and op['name'].startswith(f'projects/{PROJECT}/locations/{REGION}/operations/'),
             'C1A_DELETE_OPERATION_UNVERIFIED')
        (evidence/'operation.json').write_text(json.dumps({
            'name':op['name'], 'done':bool(op.get('done',False)),
            'has_error':bool(op.get('error'))
        },sort_keys=True)+'\n')
        if op.get('error'):
            reason='DELETE_OPERATION_REPORTED_ERROR'
        elif op.get('done') is True:
            state,reason='DELETE_OPERATION_DONE_NEEDS_READBACK','AWAIT_INDEPENDENT_SERVICE_ABSENCE_CHECK'
        else:
            state,reason='DELETE_ACCEPTED_PENDING_COMPLETION','AWAIT_INDEPENDENT_OPERATION_AND_SERVICE_CHECK'
    except (Stop,OSError,ValueError,TypeError,subprocess.TimeoutExpired) as exc:
        reason=str(exc) if isinstance(exc,Stop) else type(exc).__name__
        if write_sent: state='WRITE_OUTCOME_UNKNOWN_STOP'
    finally:
        with marker.open('a') as fh:
            fh.write('RESULT='+state+'\nREASON='+reason+'\nWRITE_ATTEMPTED='+str(write_sent)+'\n')
        (evidence/'summary.json').write_text(json.dumps({
            'result':state,'reason':reason,
            'etag_checked_and_validate_only_passed':etag_verified,
            'delete_attempted':write_sent,'service':SERVICE,
            'sa_deleted':False,'image_deleted':False,'repo_deleted':False
        },sort_keys=True)+'\n')
    print('C1A_SERVICE_DELETE_RESULT='+state)
    print('C1A_REASON='+reason)
    print('C1A_WRITE_ATTEMPTED='+str(write_sent).upper())
    print('C1A_SERVICE_ACCOUNT_DELETED=NO')
    print('C1A_REGISTRY_IMAGE_DELETED=NO')
    print('C1A_UNRELATED_RESOURCES_CHANGED=NONE_REQUESTED')
    return 0 if state.startswith('DELETE_') else 2

if __name__=='__main__':
    sys.exit(main())
