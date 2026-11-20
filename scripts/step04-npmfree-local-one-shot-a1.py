#!/usr/bin/env python3
"""OLDX Step04 - ONE NEW, local-only BellSoft npm-free derived image assessment.

Run from a clean OLDX review-branch git checkout on owner's D:-mounted WSL,
using --preflight (no writes) or --execute (exactly one new local build, offline
runtime smoke and ONE unfiltered offline-DB Grype scan). No cloud, deployment,
registry push, IAM, Firebase, billing, previous image or old Grype rechecks.
An attempted run gets an exclusive journal and must NOT be blindly retried.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

REPO = 'yasminparmar087-ops/oldx-website'
BRANCH = 'security-hardening-review'
SOURCE_SHA = 'fcc96574b6388dc441a0b5d3eade48e79c7ebb24'  # focused source CI PASS
ROOT = Path('/mnt/d/OLDX/G2/oldx-bellsoft-npmfree-20261120-a1')
IMAGE = 'oldx-bellsoft-npmfree:20261120-a1'
CONTAINER = 'oldx-bellsoft-npmfree-runtime-20261120-a1'
PINNED = {
    'Dockerfile.product-read.bellsoft-npm-free': 'c833e8372324cbdf80f6497bf3968ac421cadfc4',
    'Dockerfile.product-read.bellsoft-npm-free.dockerignore': 'c70b39451363a89f81c99738c60bd2c5b92621f0',
    'package.json': '441d7165b7cf49fae16dfcc6952e986663bd4b36',
    'package-lock.json': '26b039f82887ff63ccdd2e163b68d5bf5d6726db',
}
BASE_INDEX = 'sha256:ef00ba8e634402e8dd3b374643fdbc178e876c7a312c9d55e4734efaa1e93d94'
BASE_AMD64 = 'sha256:3862d478c2737d8386911b777d713e56a26e182f7c107e702be23a7b1cfe4799'
GRYPE = Path('/root/.oldx-g2-tools/grype')
DB_CACHE = Path('/root/.oldx-g2-tools/db-cache-raw')
DB = DB_CACHE / '6/vulnerability.db'
DB_SHA = '303ba44739343769e0e15bd0d50af62e142491b256bb533a8cfaf13ab00ca1b7'
UNDICI_IDS = {'GHSA-2m5v-pch6-74hx', 'GHSA-qrxm-fqhp-jwvm', 'GHSA-xjj6-f33q-929c'}

class Stop(Exception):
    pass

def require(ok, reason):
    if not ok:
        raise Stop(reason)

def run(args, *, cwd=None, timeout=45, check=True, env=None):
    try:
        p = subprocess.run(args, cwd=cwd, timeout=timeout, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Stop('SUBPROCESS_UNAVAILABLE_OR_TIMEOUT_' + str(args[0])) from exc
    if check and p.returncode != 0:
        raise Stop('COMMAND_REJECTED_' + str(args[0]) + '_' + str(args[1] if len(args)>1 else ''))
    return p

def sha256_file(file):
    h = hashlib.sha256()
    with file.open('rb') as f:
        for buf in iter(lambda:f.read(1048576),b''):
            h.update(buf)
    return h.hexdigest()

def git(repo,*args):
    return run(['git','-C',str(repo),*args]).stdout.strip()

def preflight(source):
    require(Path('/mnt/d').is_dir(), 'OWNER_D_DRIVE_NOT_MOUNTED')
    require('microsoft' in Path('/proc/version').read_text('utf-8').lower(), 'WSL_REQUIRED_NOT_CLOUD')
    require(source.is_dir() and (source/'.git').exists(), 'GIT_CHECKOUT_REQUIRED')
    current_branch=git(source,'branch','--show-current')
    require(current_branch in ('',BRANCH), 'WRONG_BRANCH')
    require(not git(source,'status','--porcelain'), 'DIRTY_SOURCE')
    origin=git(source,'remote','get-url','origin')
    require(bool(re.fullmatch(r'(?:https://github\.com/|git@github\.com:)'+re.escape(REPO)+r'(?:\.git)?', origin)), 'WRONG_REPOSITORY')
    sha=git(source,'rev-parse','HEAD')
    require(sha==SOURCE_SHA, 'SOURCE_COMMIT_DRIFT')
    for name,expected in PINNED.items():
        require(git(source,'hash-object',name)==expected, 'SOURCE_BLOB_DRIFT_'+name)
    dockerfile=(source/'Dockerfile.product-read.bellsoft-npm-free').read_text('utf-8')
    require(dockerfile.count('docker.io/bellsoft/hardened-nodejs@'+BASE_INDEX)==1, 'BASE_PIN_DRIFT')
    require(dockerfile.count('USER 0\nRUN [')==1 and dockerfile.count('\nUSER appuser\n')==1, 'RECIPE_ROOT_GUARD_DRIFT')
    require(not ROOT.exists() and not ROOT.is_symlink(), 'ONESHOT_JOURNAL_ALREADY_EXISTS_DO_NOT_RETRY')
    require(shutil.which('docker') is not None, 'LOCAL_DOCKER_REQUIRED')
    require(not any(os.environ.get(k) for k in ('DOCKER_HOST','DOCKER_CONTEXT','DOCKER_CERT_PATH','DOCKER_TLS_VERIFY')),
            'DOCKER_REMOTE_ENV_OVERRIDE_PRESENT')
    context=run(['docker','context','show']).stdout.strip()
    require(context in ('default','desktop-linux'), 'UNAPPROVED_DOCKER_CONTEXT')
    endpoint=run(['docker','context','inspect','--format','{{json .Endpoints.docker.Host}}']).stdout.strip()
    require(endpoint.startswith('"unix://'), 'DOCKER_REMOTE_ENDPOINT_NOT_ALLOWED')
    info=json.loads(run(['docker','info','--format','{{json .}}'],timeout=20).stdout)
    require(info.get('OSType')=='linux', 'LINUX_DOCKER_ENGINE_REQUIRED')
    require('desktop' in str(info.get('OperatingSystem','')).lower() or
            'wsl' in str(info.get('OperatingSystem','')).lower() or
            'ubuntu' in str(info.get('OperatingSystem','')).lower(), 'DOCKER_HOST_IDENTITY_UNVERIFIED')
    require(run(['docker','image','inspect',IMAGE],check=False).returncode!=0, 'NEW_IMAGE_TAG_ALREADY_EXISTS')
    require(run(['docker','container','inspect',CONTAINER],check=False).returncode!=0,'CONTAINER_ALREADY_EXISTS')
    require(GRYPE.is_file() and os.access(GRYPE,os.X_OK) and DB.is_file(), 'PINNED_OFFLINE_SCANNER_DB_REQUIRED')
    require(sha256_file(DB)==DB_SHA, 'OFFLINE_DB_DRIFT')
    require('0.121.3' in run([str(GRYPE),'version'],timeout=20).stdout, 'GRYPE_VERSION_DRIFT')
    space=os.statvfs('/mnt/d')
    require(space.f_bavail*space.f_frsize>=12*1024**3, 'D_FREE_BELOW_12_GIB')
    return {'source_sha':sha,'docker_context':context,'base_index':BASE_INDEX,
            'base_amd64_child':BASE_AMD64,'scanner_db_sha256':DB_SHA,
            'planned_image':IMAGE, 'planned_d_drive_receipt':str(ROOT)}

def persist(data):
    temp=ROOT/'summary.tmp'
    with temp.open('x',encoding='utf-8') as fp:
        json.dump(data,fp,indent=2,sort_keys=True)
        fp.write('\n');fp.flush();os.fsync(fp.fileno())
    temp.replace(ROOT/'summary.json')

def info_for_image():
    return json.loads(run(['docker','image','inspect',IMAGE],timeout=25).stdout)[0]

def image_checks():
    item=info_for_image()
    config=item.get('Config') or {}
    require(item.get('Os')=='linux' and item.get('Architecture')=='amd64', 'IMAGE_PLATFORM_MISMATCH')
    require(config.get('User')=='appuser', 'IMAGE_FINAL_USER_MISMATCH')
    require(config.get('Entrypoint')==['/usr/bin/node'], 'NODE_ENTRYPOINT_DRIFT')
    require(config.get('Cmd')==['functions/staging-marketplace/product-read-server.mjs'],'CMD_DRIFT')
    require(IMAGE in (item.get('RepoTags') or []), 'IMAGE_TAG_NOT_LOCAL')
    require(bool(re.fullmatch('sha256:[a-f0-9]{64}',str(item.get('Id')))), 'IMAGE_ID_INVALID')
    return item['Id']

JS_RUNTIME = r'''
import fs from 'node:fs';
import sharp from 'sharp';
await import('firebase-admin/app');
await import('firebase-admin/auth');
await import('firebase-admin/firestore');
const version = process.versions.node.split('.').map(Number);
if(version[0]!==24||version[1]<12)throw Error('NODE_VERSION');
if(!Number.isInteger(process.getuid?.())||process.getuid()===0)throw Error('NONROOT');
if(fs.existsSync('/usr/lib/node_modules/npm'))throw Error('BUNDLED_NPM_STILL_PRESENT');
const png=await sharp({create:{width:2,height:2,channels:4,background:'#c44'}}).png().toBuffer();
const image=await sharp(png).metadata();
if(image.width!==2||image.height!==2||image.format!=='png')throw Error('SHARP');
const health=await fetch('http://127.0.0.1:8080/healthz',{signal:AbortSignal.timeout(5000)});
if(health.status!==200||(await health.json())?.ok!==true)throw Error('HEALTH_200');
const off=await fetch('http://127.0.0.1:8080/api/staging/marketplace/owner',
  {method:'POST',headers:{'content-type':'application/json'},body:'{}',
   signal:AbortSignal.timeout(5000)});
if(off.status!==503||(await off.json())?.error?.code!=='ENFORCEMENT_UNAVAILABLE')throw Error('OFF_503');
console.log(JSON.stringify({uid:process.getuid(),node:process.versions.node,
  npm_path_absent:true,sharp:'PASS',firebase_admin_imports:'PASS',health_200:'PASS',default_off_503:'PASS'}));
'''

def smoke():
    cmd=['docker','run','--detach','--name',CONTAINER,'--network','none',
         '--read-only','--tmpfs','/tmp:rw,nosuid,size=64m','--cap-drop','ALL',
         '--security-opt','no-new-privileges','--pids-limit','128',
         '--memory','768m','--cpus','1',IMAGE]
    started=False
    try:
        run(cmd,timeout=70)
        started=True
        time.sleep(2)
        out=run(['docker','exec',CONTAINER,'/usr/bin/node','--input-type=module',
                '--eval',JS_RUNTIME],timeout=75).stdout
        result=json.loads(out.strip().splitlines()[-1])
        require(result.get('npm_path_absent') is True and
                all(result.get(k)=='PASS' for k in
                    ('sharp','firebase_admin_imports','health_200','default_off_503')),
                'RUNTIME_RESULT_FAILED')
        run(['docker','stop','--time','12',CONTAINER],timeout=35)
        code=run(['docker','inspect','--format','{{.State.ExitCode}}',CONTAINER]).stdout.strip()
        require(code=='0','SIGTERM_EXIT_NOT_ZERO')
        return result
    finally:
        if started:
            removed=run(['docker','rm','--force',CONTAINER],timeout=30,check=False)
            if removed.returncode!=0:
                raise Stop('CONTAINER_CLEANUP_UNVERIFIED')

def offline_scan(data):
    env={k:v for k,v in os.environ.items() if not k.startswith(('GRYPE_','SYFT_'))}
    env.update({'GRYPE_DB_CACHE_DIR':str(DB_CACHE), 'GRYPE_DB_AUTO_UPDATE':'false',
                'GRYPE_CHECK_FOR_APP_UPDATE':'false'})
    config=ROOT/'grype-empty.yaml'
    config.write_text('{}\n','utf-8')
    report=ROOT/'new-image-grype-full.json'
    stderr=ROOT/'new-image-grype.stderr'
    args=[str(GRYPE),'--config',str(config),'docker:'+IMAGE,'--scope','squashed','--output','json']
    data['stage']='NEW_IMAGE_SCAN_START';persist(data)
    with report.open('xb') as out,stderr.open('xb') as err:
        p=subprocess.Popen(args,stdout=out,stderr=err,env=env)
        try:
            rc=p.wait(timeout=480)
        except subprocess.TimeoutExpired:
            p.terminate()
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:p.kill();p.wait()
            raise Stop('NEW_IMAGE_SCAN_TIMEOUT_DO_NOT_RETRY')
    require(rc==0,'SCANNER_EXIT_NONZERO_DO_NOT_RETRY')
    require(report.stat().st_size>50,'SCANNER_REPORT_EMPTY')
    result=json.loads(report.read_text('utf-8'))
    require(isinstance(result.get('matches'),list) and isinstance(result.get('source'),dict),
            'SCANNER_SCHEMA_NOT_VERIFIED')
    counts=Counter(str((m.get('vulnerability') or {}).get('severity','Unknown')).upper()
                   for m in result['matches'])
    severe=sorted({str((m.get('vulnerability') or {}).get('id',''))
                   for m in result['matches']
                   if str((m.get('vulnerability') or {}).get('severity','')).upper() in ('CRITICAL','HIGH')})
    targets=sorted(UNDICI_IDS.intersection(severe))
    return {'match_count':len(result['matches']),'severity_counts':dict(counts),
            'severe_ids':severe,'bundled_undici_high_remaining':targets,
            'full_report_sha256':sha256_file(report),'db_sha256':DB_SHA,
            'full_report_local_only':str(report),'conclusion':'REVIEW_REQUIRED_NOT_G2_PASS'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    choices=parser.add_mutually_exclusive_group(required=True)
    choices.add_argument('--preflight',action='store_true',help='Read-only checks, no build or journal')
    choices.add_argument('--execute',action='store_true',help='One new local build, runtime smoke, offline scan')
    parser.add_argument('--source',type=Path,default=Path.cwd(),help='clean OLDX review-branch git checkout')
    args=parser.parse_args()
    try:
        data=preflight(args.source.resolve())
    except Exception as e:
        print('STOP_PREFLIGHT='+str(e) if isinstance(e,Stop) else 'STOP_PREFLIGHT='+type(e).__name__,flush=True)
        return 2
    print('NPMFREE_PREFLIGHT=PASS',flush=True)
    print('SOURCE_SHA='+data['source_sha'],flush=True)
    if args.preflight:
        print('EXECUTION=NOT_STARTED',flush=True)
        return 0
    # START of one and only one new image attempt. An uncertain result is STOP;
    # the existing journal blocks all automatic retries of the same scope.
    try:
        ROOT.mkdir(mode=0o700,parents=False,exist_ok=False)
        data.update({'stage':'BUILD_START','outcome':'INCOMPLETE','execution':'one_new_image_only'})
        persist(data)
        print('ONE_NEW_NPMFREE_IMAGE_BUILD_START',flush=True)
        env=dict(os.environ,DOCKER_BUILDKIT='1',BUILDKIT_PROGRESS='plain')
        # Existing pinned public builder/base layers may be reused. No registry push.
        with (ROOT/'build.log').open('x',encoding='utf-8') as log:
            p=subprocess.Popen(['docker','build','--platform','linux/amd64','--pull=false',
                '--file','Dockerfile.product-read.bellsoft-npm-free','--tag',IMAGE,'.'],
                cwd=args.source,stdout=log,stderr=subprocess.STDOUT,env=env)
            try: code=p.wait(timeout=900)
            except subprocess.TimeoutExpired:
                p.terminate()
                try:p.wait(timeout=10)
                except subprocess.TimeoutExpired:p.kill();p.wait()
                raise Stop('NEW_BUILD_TIMEOUT_DO_NOT_RETRY')
        require(code==0,'NEW_BUILD_FAILED_DO_NOT_RETRY')
        data['image_id']=image_checks()
        data['stage']='IMAGE_BUILT';persist(data)
        print('ONE_NEW_NPMFREE_IMAGE_BUILT=PASS',flush=True)
        data['runtime']=smoke()
        data['stage']='RUNTIME_PASS';persist(data)
        print('ONE_OFFLINE_RUNTIME_AND_CLEANUP=PASS',flush=True)
        data['new_image_scan']=offline_scan(data)
        data['stage']='COMPLETE_REVIEW_REQUIRED';data['outcome']='DONE_NOT_SECURITY_CLEARANCE'
        persist(data)
        print('ONE_NEW_NPMFREE_IMAGE_SCAN=COMPLETE_REVIEW_REQUIRED',flush=True)
        print('SEVERITY_COUNTS='+json.dumps(data['new_image_scan']['severity_counts'],sort_keys=True),flush=True)
        print('UNDICI_HIGH_REMAINING='+str(len(data['new_image_scan']['bundled_undici_high_remaining'])),flush=True)
        print('SUMMARY='+str(ROOT/'summary.json'),flush=True)
        return 0
    except Exception as e:
        data['stage']='STOP';data['outcome']='STOP_DO_NOT_RETRY'
        data['stop_reason']=str(e) if isinstance(e,Stop) else type(e).__name__
        try:persist(data)
        except Exception:pass
        print('STOP_NEW_NPMFREE='+data['stop_reason'],flush=True)
        print('DO_NOT_RETRY_OR_DELETE_LOCAL_EVIDENCE',flush=True)
        return 2

if __name__=='__main__':
    sys.exit(main())
