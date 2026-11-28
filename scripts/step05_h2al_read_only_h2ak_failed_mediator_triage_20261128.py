#!/usr/bin/env python3
"""H2AL diagnostic: inspect EXISTING H2AK evidence, never scan or modify.

NO Docker pull, run, exec, stop, image removal, registry, gcloud or network
requests. Only root-owned files + local docker ps/image inspect/logs GETs.
The consumed H2AK marker and previous H2AJ artifacts MUST remain untouched.
"""
from __future__ import annotations
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path('/root')
EVID = ROOT / 'oldx-h2ak-images-20261128T160610Z-42e006'
MARK = ROOT / '.oldx-step05-h2ak-four-pinned-image-acceptance-once-20261128'
H2AJ = ROOT / '.oldx-step05-h2aj-four-off-builds-corrected-context-once-20261128'
IMAGE = ('asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/'
         'oldx-c2-mediator-h2ah@sha256:'
         '01b5d063a7836e736dda0d0f7fc32a2a78ee39bcee64d3ef3ccc22de10e6cfbe')

def safe_file(path, maximum=60_000_000):
    if not path.is_file() or path.is_symlink():
        return None
    st=path.stat()
    if st.st_uid!=0 or st.st_size<1 or st.st_size>maximum:
        return None
    return path

def read_json(path):
    if safe_file(path):
        try:
            with path.open('r', encoding='utf-8') as stream:
                return json.load(stream)
        except (OSError, UnicodeError, ValueError):
            return None
    return None

def cmd(args,timeout=12):
    # Whitelisted local Docker READ-ONLY commands. Never call the Docker API
    # to create/stop/delete/extract image, start a scan or fetch from registry.
    valid=(args[:2]==['docker','ps'] and '--all' in args
           and '--format' in args and '--filter' in args
          ) or (args[:3]==['docker','image','inspect'] and IMAGE in args
           and '--format' in args) or (
            args[:2]==['docker','logs'] and len(args)==5
            and args[2:4]==['--tail','25']
            and re.fullmatch(r'[a-f0-9]{12,64}',args[4]) is not None
           ) or (
            args[:2]==['docker','events'] and
            args[2:]==['--since','2026-11-28T16:06:00Z',
                        '--until','2026-11-28T16:13:30Z',
                        '--filter','type=container','--format',
                        '{{.Action}}|{{.Actor.Attributes.name}}|{{.Actor.Attributes.exitCode}}']
           )
    if not valid:
        return ['DENIED_NON_READ_ONLY_COMMAND']
    try:
        r=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
             stdin=subprocess.DEVNULL,timeout=timeout,check=False)
        if r.returncode!=0:
            return ['READ_ONLY_DOCKER_ERROR_EXIT_'+str(r.returncode)]
        bytes_out=r.stdout+(b'\n'+r.stderr if args[1]=='logs' else b'')
        return bytes_out.decode('utf-8','replace').splitlines()[:65]
    except (OSError, subprocess.TimeoutExpired):
        return ['DOCKER_READ_ONLY_UNAVAILABLE']

def lines(path):
    p=safe_file(path,30000)
    return p.read_text(encoding='utf-8',errors='replace').splitlines() if p else []

def main():
    print('H2AL_MODE=READ_ONLY_NO_SCAN_NO_DOCKER_WRITES')
    print('H2AL_H2AK_MARKER='+('CONSUMED' if safe_file(MARK,15000) else 'MISSING_OR_UNTRUSTED'))
    print('H2AL_H2AJ_MARKER='+('EXISTS_UNTOUCHED' if safe_file(H2AJ,15000) else 'MISSING_OR_UNTRUSTED'))
    status=lines(MARK)
    print('H2AL_MARKER_ROLES='+','.join(x for x in status
        if re.fullmatch(r'ROLE=(mediator|gateway|backend|reader) (?:ABOUT_TO_CHECK|PASS)',x)))
    print('H2AL_MARKER_RESULT='+next((x for x in status if x.startswith('RESULT=')),'UNKNOWN'))
    summary=read_json(EVID/'sanitized-h2ak-summary.json')
    if isinstance(summary,dict):
        print('H2AL_RECORDED_OUTCOME='+str(summary.get('outcome','UNKNOWN'))[:100])
        print('H2AL_RECORDED_REASON='+str(summary.get('reason','UNKNOWN'))[:100])
        print('H2AL_SUMMARY_ROLES='+','.join(summary.get('roles',{}).keys()))
    else:
        print('H2AL_SUMMARY=NOT_READABLE')
    scanned=read_json(EVID/'mediator-grype.json')
    if isinstance(scanned,dict) and isinstance(scanned.get('matches'),list):
        matches=scanned['matches']
        severities=Counter(str(m.get('vulnerability',{}).get('severity','Unknown'))
            for m in matches if isinstance(m,dict))
        print('H2AL_MEDIATOR_GRYPE_JSON=EXISTS_COMPLETE_JSON')
        print('H2AL_MEDIATOR_GRYPE_MATCHES='+str(len(matches)))
        print('H2AL_MEDIATOR_SEVERITIES='+
              ','.join(k+':'+str(v) for k,v in sorted(severities.items())))
        print('H2AL_MEDIATOR_GRYPE_DB_CHECKSUM_OR_AGE=NOT_INFERRED')
    else:
        print('H2AL_MEDIATOR_GRYPE_JSON=ABSENT_OR_INVALID')
    for role in ['gateway','backend','reader']:
        present=(EVID/(role+'-grype.json')).exists()
        print('H2AL_'+role.upper()+'_GRYPE_JSON='+('EXISTS' if present else 'ABSENT'))
    print('H2AL_DOCKER_PS_BEGIN')
    retained=[]
    for line in cmd(['docker','ps','--all','--filter','name=oldx-h2ak-',
                     '--format','{{.Names}}|{{.Status}}|{{.ID}}']):
        if line.startswith('oldx-h2ak-'):
            print('H2AL_CONTAINER='+line[:240])
            parts=line.split('|')
            if len(parts)==3 and parts[0].startswith('oldx-h2ak-mediator-') and re.fullmatch(r'[a-f0-9]{12,64}',parts[2]):
                retained.append(parts[2])
    print('H2AL_DOCKER_PS_END')
    for cid in retained[:2]:
        print('H2AL_RETAINED_CONTAINER_LOG_BEGIN')
        for line in cmd(['docker','logs','--tail','25',cid]):
            line=re.sub(r'(?i)bearer\s+\S+', '[REDACTED_BEARER]', line)
            line=re.sub(r'(?i)(?:token|password|secret|authorization)\s*[:=]\s*\S+', '[REDACTED_SECRET]', line)
            print('H2AL_LOG='+line[:350])
        print('H2AL_RETAINED_CONTAINER_LOG_END')
    print('H2AL_DOCKER_EVENTS_BEGIN')
    for line in cmd(['docker','events','--since','2026-11-28T16:06:00Z',
            '--until','2026-11-28T16:13:30Z','--filter','type=container',
            '--format','{{.Action}}|{{.Actor.Attributes.name}}|{{.Actor.Attributes.exitCode}}'],timeout=15):
        if 'oldx-h2ak-' in line:
            print('H2AL_EVENT='+line[:350])
    print('H2AL_DOCKER_EVENTS_END')
    print('H2AL_MEDIATOR_LOCAL_IMAGE_INSPECT_BEGIN')
    for line in cmd(['docker','image','inspect',IMAGE,'--format',
        'User={{.Config.User}}|Entrypoint={{json .Config.Entrypoint}}|Cmd={{json .Config.Cmd}}|WorkingDir={{.Config.WorkingDir}}|OS={{.Os}}|Arch={{.Architecture}}']):
        print('H2AL_IMAGE='+line[:500])
    print('H2AL_MEDIATOR_LOCAL_IMAGE_INSPECT_END')
    print('H2AL_DO_NOT_RERUN_H2AK=TRUE')
    print('H2AL_DOCKER_BUILD_PUSH_EXEC_STOP_RM_SCAN=NONE')
    print('H2AL_CLOUD_IAM_KMS_FIREBASE_WRITES=NONE')

if __name__ == '__main__':
    main()
