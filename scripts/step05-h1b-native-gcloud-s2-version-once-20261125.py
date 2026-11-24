#!/usr/bin/env python3
"""OLDX H1B S2: one bounded local native-Linux gcloud --version probe only.

S1/S1R markers stay consumed. No auth list, login, project, IAM, registry,
Cloud API, install/update, Windows SDK path or existing gcloud config access.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import platform
import re
import signal
import stat
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path('/root')
SDK = ROOT / 'oldx-tools/native-gcloud-594.0.1/google-cloud-sdk'
CLI = SDK / 'bin/gcloud'
PYTHON = SDK / 'platform/bundledpythonunix/bin/python3'
S1R_MARKER = ROOT / '.oldx-h1b-native-gcloud-s1r-offline-extract-once-20261125'
MARKER = ROOT / '.oldx-h1b-native-gcloud-s2-version-once-20261125'
CONFIG = ROOT / 'oldx-tools/native-gcloud-594.0.1-s2-isolated-config'
TIMEOUT_SECONDS = 15

class Stop(Exception):
    pass

def require(ok, code):
    if not ok:
        raise Stop(code)

def version_ok(output: str, return_code: int | None) -> bool:
    return (return_code == 0
            and bool(re.search(r'(?m)^Google Cloud SDK 594\.0\.1[ \t]*$', output)))

def preflight():
    require(platform.system() == 'Linux'
            and platform.machine() in ('x86_64', 'amd64')
            and 'microsoft' in platform.release().lower()
            and os.geteuid() == 0, 'OWNER_ROOT_WSL_REQUIRED')
    require(not MARKER.exists() and not MARKER.is_symlink(), 'S2_ALREADY_ATTEMPTED')
    require(not CONFIG.exists() and not CONFIG.is_symlink(), 'S2_CONFIG_COLLISION')
    require(not SDK.is_symlink() and SDK.is_dir()
            and SDK.resolve().is_relative_to(ROOT)
            and SDK.stat().st_uid == 0, 'SDK_DIR_UNVERIFIED')
    require(not S1R_MARKER.is_symlink() and S1R_MARKER.is_file()
            and S1R_MARKER.stat().st_uid == 0, 'S1R_MARKER_MISSING')
    contents = S1R_MARKER.read_text(encoding='utf-8').splitlines()
    require('S1R_ATTEMPT_CONSUMED' in contents
            and 'RESULT=S1R_COMPLETE_NO_CLI_EXECUTION' in contents
            and 'REASON=NONE' in contents, 'S1R_SUCCESS_NOT_CONFIRMED')
    for path in (CLI, PYTHON):
        require(path.is_file()
                and path.resolve().is_relative_to(SDK.resolve())
                and path.stat().st_uid == 0
                and (path.stat().st_mode & stat.S_IXUSR) != 0,
                'SDK_REQUIRED_FILE_UNVERIFIED')
    require(CONFIG.parent == SDK.parent and not CONFIG.parent.is_symlink(),
            'CONFIG_PARENT_UNSAFE')

def run_version():
    env = {
        'HOME': '/root',
        'PATH': '/usr/bin:/bin',
        'LANG': 'C.UTF-8',
        'CLOUDSDK_CONFIG': str(CONFIG),
        'CLOUDSDK_PYTHON': str(PYTHON),
        'CLOUDSDK_CORE_DISABLE_USAGE_REPORTING': 'true',
        'CLOUDSDK_COMPONENT_MANAGER_DISABLE_UPDATE_CHECK': 'true',
        'CLOUDSDK_CORE_CHECK_GCE_METADATA': 'false',
    }
    out_path = CONFIG / 's2-version.stdout'
    err_path = CONFIG / 's2-version.stderr'
    with out_path.open('xb') as stdout, err_path.open('xb') as stderr:
        process = subprocess.Popen(
            [str(CLI), '--version'],
            cwd=str(ROOT), env=env, stdin=subprocess.DEVNULL,
            stdout=stdout, stderr=stderr, start_new_session=True,
            close_fds=True,
        )
        try:
            exit_code = process.wait(timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=3)
            raise Stop('GCLOUD_VERSION_TIMEOUT_15S')
    require(out_path.stat().st_size <= 65536 and err_path.stat().st_size <= 65536,
            'VERSION_OUTPUT_TOO_LARGE')
    output = out_path.read_text(encoding='utf-8', errors='replace')
    require(version_ok(output, exit_code), 'VERSION_NONZERO_OR_UNVERIFIED')
    return exit_code

def main():
    os.umask(0o077)
    if sys.argv[1:] != ['--version-local-once']:
        print('S2_RESULT=STOP_FLAG_REQUIRED')
        return 2
    try:
        preflight()
    except (Stop, OSError) as error:
        print('S2_RESULT=STOP_PREFLIGHT')
        print('S2_REASON=' + (str(error) if isinstance(error, Stop) else type(error).__name__))
        return 2
    fd = os.open(MARKER, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as writer:
        writer.write('S2_ATTEMPT_CONSUMED\n')
    result, reason, code = 'STOP', 'UNDETERMINED', None
    try:
        CONFIG.mkdir(mode=0o700)
        code = run_version()
        result, reason = 'STARTUP_PASS_WITH_LIMITS', 'NONE'
    except (Stop, OSError, subprocess.SubprocessError) as error:
        reason = str(error) if isinstance(error, Stop) else type(error).__name__
    finally:
        with MARKER.open('a', encoding='utf-8') as writer:
            writer.write('RESULT=' + result + '\nREASON=' + reason + '\n')
        try:
            if CONFIG.is_dir():
                (CONFIG / 's2-result.json').write_text(
                    json.dumps({'result': result, 'reason': reason, 'exit_code': code,
                                'version_expected': '594.0.1',
                                'scope': 'LOCAL_VERSION_ONLY',
                                'original_sdk_config_unchanged': True,
                                'cloud_resource_commands_requested': False}) + '\n',
                    encoding='utf-8')
        except OSError:
            pass
    print('S2_RESULT=' + result)
    print('S2_REASON=' + reason)
    print('S2_VERSION_EXPECTED=594.0.1')
    print('S2_NO_AUTH_OR_CLOUD_RESOURCE_COMMANDS=TRUE')
    return 0 if result == 'STARTUP_PASS_WITH_LIMITS' else 2

if __name__ == '__main__':
    sys.exit(main())
