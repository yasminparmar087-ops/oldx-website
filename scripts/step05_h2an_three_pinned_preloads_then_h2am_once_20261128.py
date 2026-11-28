#!/usr/bin/env python3
"""H2AN: ONE approved 3-image private preload then ONE old H2AM selective OFF run.

No build/push, Cloud Run deploy, IAM/KMS/Firebase, old scan replay, or retries.
H2AN preload has its own exclusive marker and never clears prior markers.
"""
from __future__ import annotations
import hashlib, json, os, platform, re, secrets, shutil, subprocess, sys
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path('/root')
SDK=ROOT/'oldx-tools/native-gcloud-594.0.1/google-cloud-sdk'
GCLOUD=SDK/'bin/gcloud'
GCLOUD_PY=SDK/'platform/bundledpythonunix/bin/python3'
CONFIG=ROOT/'oldx-tools/oldx-h1b-g2-20261126-cloudsdk-config'
GRYPE=ROOT/'oldx-tools/grype-v0.122.1/grype'
DB=ROOT/'.cache/grype/db'
REGISTRY='asia-south1-docker.pkg.dev'
OWNER='yasminparmar087@gmail.com'
PROJECT='oldx-staging'
REPO='yasminparmar087-ops/oldx-website'
SOURCE='8f5df51075d6cc42f0d32ad0c730b14611c03f87'
FLAG='--owner-approved-exact-three-preloads-then-one-h2am-off-only'
PRELOAD_MARK=ROOT/'.oldx-step05-h2an-three-pinned-preloads-once-20261128'
H2AM_MARK=ROOT/'.oldx-step05-h2am-selective-off-runtime-three-scans-once-20261128'
H2AJ_MARK=ROOT/'.oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128'
H2AK_MARK=ROOT/'.oldx-step05-h2ak-four-pinned-image-acceptance-once-20261128'
REPORT=ROOT/'oldx-h2ak-images-20261128T160610Z-42e006/mediator-grype.json'
REPORT_SHA='e89c68fb7838173cbcca4ac3c365584e63a370480867961ac866065bbe6e3f92'
BLOBS={
 'scripts/step05_h2am_selective_acceptance_once_20261128.py':'3adfb06ca66d6175f089ea797df21ca767779cca',
 'scripts/step05_h2am_acceptance_support.py':'b9b57daa9a5b5f0304afc9cfc758630793454c07',
 'deployment/four-role/h2aj-four-immutable-images-pinned-proposal.json':'c1cfcfa2f224e9a47dd6e896730c73e927b9b483'}
IMAGES={
 'mediator':('oldx-c2-mediator-h2ah','01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe'),
 'gateway':('oldx-c2-gateway-h2ah','921fbf4ff71b918c479e4a786868368640a494c16da08e54192f25e14dc1ec4d'),
 'backend':('oldx-c2-backend-h2ah','01ae540aa88ad0e3a6888994dd41b6b02b9d934a7a1d2e455f44b194f033b941'),
 'reader':('oldx-c2-kms-reader','822e2592b1010bfa94a1fe5bc75003712485abae0369f5252ece3863723eb077')}
REFS={r:f'{REGISTRY}/{PROJECT}/oldx-staging-images/{n}@sha256:{d}' for r,(n,d) in IMAGES.items()}
class Stop(Exception):pass
def require(ok,why):
 if not ok:raise Stop(why)
def run(argv,env=None,timeout=50,stdin=None):
 try:
  p=subprocess.run(argv,env=env,timeout=timeout,input=stdin,
        stdin=None if stdin is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
 except subprocess.TimeoutExpired:raise Stop('TIMEOUT_AMBIGUOUS_NO_RETRY') from None
 except OSError:raise Stop('COMMAND_NOT_AVAILABLE') from None
 require(p.returncode==0,'FAILED_'+Path(argv[0]).name+'_EXIT_'+str(p.returncode))
 require(len(p.stdout)<1000000,'COMMAND_OUTPUT_TOO_LARGE')
 return p.stdout.decode('utf-8','strict').strip()
def blob(data):
 return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def logmark(message):
 with PRELOAD_MARK.open('a',encoding='utf-8') as f:
  f.write(message+'\n');f.flush();os.fsync(f.fileno())
def inspect(ref,env):
 # Returns None only on a positively established missing local image.
 p=subprocess.run(['docker','image','inspect',ref],stdin=subprocess.DEVNULL,
          stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,timeout=40)
 if p.returncode:
  require(re.search(rb'No such image|No such object|not found',p.stderr,re.I),
          'LOCAL_INSPECT_UNKNOWN_NOT_ABSENT')
  return None
 rows=json.loads(p.stdout)
 require(isinstance(rows,list) and len(rows)==1,'LOCAL_IMAGE_SCHEMA')
 x=rows[0];c=x.get('Config') or {}
 require(x.get('Os')=='linux' and x.get('Architecture')=='amd64'
     and c.get('User')=='65532:65532'
     and c.get('WorkingDir')=='/app'
     and c.get('Entrypoint')==['/nodejs/bin/node']
     and re.fullmatch(r'sha256:[a-f0-9]{64}',x.get('Id',''))
     and ref in x.get('RepoDigests',[]),'LOCAL_IMAGE_DIGEST_OR_NONROOT_DRIFT')
 return x['Id']
def preflight():
 require(sys.argv[1:]==[FLAG],'EXACT_OWNER_APPROVAL_FLAG')
 require(os.geteuid()==0 and platform.system()=='Linux' and
         'microsoft' in platform.release().lower(),'NATIVE_WSL_ROOT_REQUIRED')
 for p in (PRELOAD_MARK,H2AM_MARK):
  require(not p.exists() and not p.is_symlink(),'NEW_ATTEMPT_MARKER_ALREADY_CONSUMED')
 for p in (H2AJ_MARK,H2AK_MARK):
  require(p.is_file() and not p.is_symlink() and p.stat().st_uid==0,
          'PREVIOUS_MARKER_MISSING')
 require(SDK.is_dir() and GCLOUD.is_file() and GCLOUD_PY.is_file()
         and CONFIG.is_dir(),'ISOLATED_NATIVE_GCLOUD_MISSING')
 require(GRYPE.is_file() and os.access(GRYPE,os.X_OK)
         and GRYPE.stat().st_uid==0,'NATIVE_GRYPE_MISSING')
 require(DB.is_dir() and not DB.is_symlink() and DB.stat().st_uid==0,
         'EXISTING_PRIVATE_GRYPE_DB_MISSING')
 require(shutil.disk_usage(ROOT).free>=4*1024**3,'PRIVATE_DISK_BELOW_FOUR_GIB')
 require(REPORT.is_file() and not REPORT.is_symlink() and REPORT.stat().st_uid==0,
         'HISTORIC_MEDIATOR_SCAN_MISSING')
 require(hashlib.sha256(REPORT.read_bytes()).hexdigest()==REPORT_SHA,
         'HISTORIC_MEDIATOR_SCAN_CHANGED_NO_RESCAN')
 env=dict(os.environ)
 env.update({'HOME':str(ROOT),'CLOUDSDK_CONFIG':str(CONFIG),
      'CLOUDSDK_PYTHON':str(GCLOUD_PY),'CLOUDSDK_CORE_DISABLE_USAGE_REPORTING':'1',
      'CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK':'1',
      'CLOUDSDK_CORE_CHECK_GCE_METADATA':'false',
      'GRYPE_CHECK_FOR_APP_UPDATE':'false','GRYPE_DB_AUTO_UPDATE':'false',
      'GRYPE_DB_CACHE_DIR':str(DB),
      'PATH':str(GRYPE.parent)+':'+env.get('PATH','/usr/local/bin:/usr/bin:/bin')})
 env.pop('GOOGLE_APPLICATION_CREDENTIALS',None)
 env.pop('CLOUDSDK_AUTH_CREDENTIAL_FILE_OVERRIDE',None)
 def cloud(args):return run([str(GCLOUD),'--quiet',*args],env=env)
 require(cloud(['auth','list','--filter=status:ACTIVE','--format=value(account)'])==OWNER,
         'WRONG_OWNER_ACCOUNT')
 require(cloud(['config','get-value','project'])==PROJECT,'WRONG_STAGING_PROJECT')
 require(run(['docker','info','--format','{{.OSType}}'],env)=='linux',
         'LINUX_DOCKER_REQUIRED')
 db=run([str(GRYPE),'db','status','-o','json'],env,timeout=40)
 require(db.startswith('{') and isinstance(json.loads(db),dict),
         'CACHED_GRYPE_DB_STATUS_UNKNOWN')
 return env,cloud
def bundle(parent,env):
 target=parent/'source'
 for rel,expected in BLOBS.items():
  f=target/rel;f.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
  url=f'https://raw.githubusercontent.com/{REPO}/{SOURCE}/{rel}'
  run(['curl','--fail','--silent','--show-error','--retry','0',
        '--max-redirs','0','--max-time','40','--proto','=https',
        '--output',str(f),url],env,timeout=45)
  require(f.is_file() and f.stat().st_size<100000,'FROZEN_SOURCE_MISSING')
  require(blob(f.read_bytes())==expected,'FROZEN_SOURCE_GIT_BLOB_DRIFT')
  if rel.endswith('.py'):compile(f.read_bytes(),rel,'exec')
 p=json.loads((target/'deployment/four-role/h2aj-four-immutable-images-pinned-proposal.json').read_text())
 require(p.get('executionAllowed') is False and p.get('project')==PROJECT
         and p.get('imageBuildSourceRevision')=='f567aa6ccef7a71b6032dc1bdb9f2bcf0a8587d4'
         and set(p.get('roles',{}))==set(IMAGES),'IMMUTABLE_PROPOSAL_DRIFT')
 for role,ref in REFS.items():
  require(p['roles'][role]['image']==ref and p['roles'][role]['enabled'] is False,
          'IMMUTABLE_ROLE_IMAGE_DRIFT')
 return target
def main():
 os.umask(0o077)
 try:
  env,cloud=preflight()
  print('H2AN_PREFLIGHT=OWNER_DOCKER_GRYPE_DB_HISTORY_PASS',flush=True)
 except (Stop,OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired) as err:
  print('H2AN_RESULT=STOP_BEFORE_ANY_PRELOAD')
  print('H2AN_REASON='+str(err)[:140]);return 2
 evidence=ROOT/('oldx-h2an-preload-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+secrets.token_hex(3))
 private=evidence/'private-docker-config'
 consumed=False;started=False
 try:
  evidence.mkdir(mode=0o700);private.mkdir(mode=0o700)
  source=bundle(evidence,env)
  local={role:inspect(ref,env) for role,ref in REFS.items()}
  require(local['mediator'] is not None,'MEDIATOR_LOCAL_IMAGE_NOT_VERIFIED')
  missing=[r for r in ('gateway','backend','reader') if local[r] is None]
  print('H2AN_MISSING='+','.join(missing),flush=True)
  print('H2AN_SOURCE_BLOBS=ALL_THREE_VERIFIED',flush=True)
  if missing:
   auth_env=dict(env,DOCKER_CONFIG=str(private),DOCKER_DEFAULT_PLATFORM='linux/amd64')
   token=cloud(['--account='+OWNER,'--project='+PROJECT,'auth','print-access-token'])
   require(re.fullmatch(r'[A-Za-z0-9._~+\-]{40,4096}',token) is not None,
           'OWNER_OAUTH_TOKEN_FORMAT_INVALID')
   run(['docker','login','--username','oauth2accesstoken','--password-stdin',
        'https://'+REGISTRY],auth_env,stdin=(token+'\n').encode())
   del token
   fd=os.open(str(PRELOAD_MARK),os.O_CREAT|os.O_EXCL|os.O_WRONLY|getattr(os,'O_NOFOLLOW',0),0o600)
   with os.fdopen(fd,'w',encoding='utf-8') as f:
    f.write('ATTEMPT_CONSUMED=TRUE\nSOURCE='+SOURCE+'\nEVIDENCE='+str(evidence)+'\n')
    f.flush();os.fsync(f.fileno())
   consumed=True
   print('H2AN_PRELOAD_MARKER=CONSUMED_NO_REPEAT',flush=True)
   for role in missing:
    logmark('ROLE='+role+' PULL_ATTEMPT_STARTED')
    print('H2AN_PULL_START='+role,flush=True)
    run(['docker','pull','--platform','linux/amd64',REFS[role]],auth_env,timeout=600)
    identity=inspect(REFS[role],auth_env)
    require(identity is not None,'EXACT_CHILD_NOT_VISIBLE_AFTER_PULL')
    logmark('ROLE='+role+' VERIFIED_IMAGE_ID='+identity)
    print('H2AN_PULL_PASS='+role,flush=True)
  for role,ref in REFS.items():
   require(inspect(ref,env) is not None,'FOUR_LOCAL_CHILDREN_NOT_PRESENT')
  print('H2AN_FOUR_LOCAL_CHILDREN=VERIFIED',flush=True)
  if consumed:logmark('ALL_FOUR_CHILDREN_VERIFIED')
  shutil.rmtree(private)
  require(not H2AM_MARK.exists() and not H2AM_MARK.is_symlink(),'H2AM_ALREADY_STARTED')
  started=True
  print('H2AN_H2AM=START_ONE_APPROVED_SELECTIVE_ATTEMPT',flush=True)
  approved=os.environ.copy()
  approved['PATH']=str(GRYPE.parent)+':'+approved.get('PATH','')
  approved['GRYPE_CHECK_FOR_APP_UPDATE']='false'
  approved['GRYPE_DB_AUTO_UPDATE']='false'
  approved['GRYPE_DB_CACHE_DIR']=str(DB)
  p=subprocess.run([sys.executable,'-B',
       str(source/'scripts/step05_h2am_selective_acceptance_once_20261128.py'),
       '--execute-h2am-once','--owner-approved-selective-off-only',
       '--grype-db-cache',str(DB)],env=approved,check=False)
  require(p.returncode==0,'H2AM_COMPLETED_WITH_STOP_STATUS_'+str(p.returncode))
  print('H2AN_RESULT=PRELOAD_AND_H2AM_COMPLETE',flush=True)
  return 0
 except (Stop,OSError,ValueError,KeyError,TypeError) as err:
  print('H2AN_RESULT='+('STOP_AFTER_PRELOAD_MARKER' if consumed else 'STOP_BEFORE_PRELOAD_MARKER'),flush=True)
  print('H2AN_REASON='+(str(err) if isinstance(err,Stop) else type(err).__name__)[:150],flush=True)
  print('H2AN_H2AM_STARTED='+str(started).upper(),flush=True)
  return 2
 finally:
  if private.exists():shutil.rmtree(private,ignore_errors=True)
  print('H2AN_EVIDENCE='+str(evidence),flush=True)
  print('H2AN_OLD_MARKERS_UNTOUCHED=TRUE',flush=True)
  print('H2AN_BUILD_PUSH_CLOUD_IAM_KMS_FIREBASE=NONE',flush=True)
  print('H2AN_DO_NOT_REPEAT_AFTER_MARKER=TRUE',flush=True)
if __name__=='__main__':sys.exit(main())
