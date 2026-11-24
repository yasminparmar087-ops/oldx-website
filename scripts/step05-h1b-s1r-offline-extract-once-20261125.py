#!/usr/bin/env python3
"""OLDX H1B S1R: offline-only, one-shot recovery of previously verified archive.

Never downloads, executes SDK, changes SDK config, authenticates or calls Cloud APIs.
Original failed S1 marker and evidence are read-only; S1R uses a distinct marker.
"""
import hashlib
import json
import os
from pathlib import Path
import platform
import posixpath
import stat
import sys
import tarfile
from datetime import datetime, timezone

SHA = 'c6fdba4cb1551b0da7c1d744eb0dfaf68b59861238d6a6b5ef6bad1ba596b567'
OLD = Path('/root/.oldx-h1b-native-gcloud-s1-once-20261125')
NEW = Path('/root/.oldx-h1b-native-gcloud-s1r-offline-extract-once-20261125')
TOOLS = Path('/root/oldx-tools')
DEST = TOOLS / 'native-gcloud-594.0.1'
FILENAME = 'google-cloud-cli-linux-x86_64.tar.gz'
EXPECTED_IMPLICIT = {
  'google-cloud-sdk/platform/gsutil/third_party/requests/tests/certs/mtls/client/ca':
  'google-cloud-sdk/platform/gsutil/third_party/requests/tests/certs/expired/ca',
  'google-cloud-sdk/platform/gsutil/third_party/requests/tests/certs/valid/ca':
  'google-cloud-sdk/platform/gsutil/third_party/requests/tests/certs/expired/ca',
}

class Halt(Exception): pass

def require(test, message):
    if not test: raise Halt(message)

def real_private_file(p):
    require(not p.is_symlink() and p.is_file(), 'MISSING_OR_SYMLINK_FILE')
    s = p.stat()
    require(s.st_uid == 0 and stat.S_ISREG(s.st_mode), 'FOREIGN_FILE')

def source_path():
    real_private_file(OLD)
    text = OLD.read_text(encoding='utf-8')
    require('S1_ATTEMPT_CONSUMED' in text.splitlines() and 'RESULT=STOP' in text.splitlines() and
            'DETAIL=ARCHIVE_DANGLING_LINK' in text.splitlines(), 'ORIGINAL_NOT_EXPECTED_STOP')
    rows = [v.partition('=')[2] for v in text.splitlines() if v.startswith('EVIDENCE=')]
    require(len(rows) == 1, 'EVIDENCE_MARKER')
    e = Path(rows[0])
    require(e.parent == Path('/root') and e.name.startswith('oldx-h1b-native-gcloud-s1-') and
            not e.is_symlink() and e.is_dir() and e.stat().st_uid == 0, 'EVIDENCE_DIR')
    receipt = e / 'receipt.json'
    real_private_file(receipt)
    d = json.loads(receipt.read_text(encoding='utf-8'))
    require(d.get('state') == 'STOP' and d.get('stop_reason') == 'ARCHIVE_DANGLING_LINK' and
            d.get('sha_expected') == SHA and d.get('sha_actual') == SHA and
            d.get('gcloud_invoked') is False and d.get('cloud_api_invoked') is False,
            'ORIGINAL_RECEIPT_MISMATCH')
    archive = e / FILENAME
    real_private_file(archive)
    require(0 < archive.stat().st_size <= 130 * 1024 * 1024, 'ARCHIVE_SIZE')
    return archive

def inspect_archive(tf, *, expected_count=36776, expected_implicit=EXPECTED_IMPLICIT):
    """Only the two hash-frozen implicit directory targets may lack tar headers."""
    require(hasattr(tarfile, 'data_filter'), 'DATA_FILTER_UNAVAILABLE')
    entries, links, implicit, total = {}, {}, set(), 0
    for m in tf:
        name = m.name
        bits = name.rstrip('/').split('/')
        require(name and len(name) <= 512 and not name.startswith('/') and '\\' not in name and
                ':' not in name and '\x00' not in name and all(x not in ('', '.', '..') for x in bits),
                'UNSAFE_MEMBER_NAME')
        name = '/'.join(bits)
        require(name == 'google-cloud-sdk' or name.startswith('google-cloud-sdk/'), 'OUTSIDE_ROOT')
        require(name not in entries, 'DUPLICATE_MEMBER')
        entries[name] = m
        for i in range(1, len(bits)): implicit.add('/'.join(bits[:i]))
        if m.isfile():
            require(0 <= m.size <= 512 * 1024 * 1024, 'FILE_SIZE')
            total += m.size
            require(total <= 2 * 1024 * 1024 * 1024, 'EXPANDED_SIZE')
        elif not (m.isdir() or m.issym() or m.islnk()): raise Halt('SPECIAL_MEMBER')
        if m.issym() or m.islnk():
            link = m.linkname
            require(link and len(link) <= 512 and not link.startswith('/') and
                    '\\' not in link and ':' not in link and '\x00' not in link, 'UNSAFE_LINK')
            target = posixpath.normpath(posixpath.join(posixpath.dirname(name) if m.issym() else '', link))
            require(target.startswith('google-cloud-sdk/') and target != name, 'ESCAPING_LINK')
            links[name] = target
        require(len(entries) <= 45000, 'ENTRY_CAP')
    require(len(entries) == expected_count, 'EXPECTED_MEMBER_COUNT_DRIFT')
    require('google-cloud-sdk/bin/gcloud' in entries and
            'google-cloud-sdk/platform/bundledpythonunix/bin/python3' in entries, 'REQUIRED_SDK_MISSING')
    unseen = {}
    for name, target in links.items():
        visited = set()
        while target in links:
            require(target not in visited, 'LINK_CYCLE')
            visited.add(target)
            target = links[target]
        if target not in entries:
            require(name in expected_implicit and expected_implicit[name] == target and
                    target in implicit, 'UNAPPROVED_DANGLING_LINK')
            unseen[name] = target
    require(unseen == expected_implicit, 'EXPECTED_IMPLICIT_LINK_SET_DRIFT')
    # Prevent a link or regular file appearing as a path prefix of a later member.
    for name in entries:
        parts = name.split('/')
        for i in range(1, len(parts)):
            parent = '/'.join(parts[:i])
            if parent in entries:
                require(entries[parent].isdir(), 'SYMLINK_OR_FILE_PARENT')
    return {'members': len(entries), 'implicit_dir_links': len(unseen), 'expanded_bytes': total}

def native_preflight():
    require(platform.system() == 'Linux' and platform.machine() in ('x86_64', 'amd64') and
            'microsoft' in platform.release().lower() and os.geteuid() == 0 and
            sys.version_info >= (3, 12), 'ROOT_WSL_PYTHON312_REQUIRED')
    require(not DEST.exists() and not DEST.is_symlink() and not NEW.exists() and not NEW.is_symlink(), 'ALREADY_ATTEMPTED_OR_INSTALLED')
    require(not TOOLS.is_symlink() and (not TOOLS.exists() or
            TOOLS.is_dir() and TOOLS.stat().st_uid == 0), 'TOOLS_PARENT_UNSAFE')
    require(os.statvfs('/root').f_bavail * os.statvfs('/root').f_frsize >= 2 * 1024**3, 'INSUFFICIENT_LINUX_SPACE')
    mounts = []
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        before, delim, after = line.partition(' - ')
        if delim:
            b, a = before.split(), after.split()
            if len(b) >= 5 and a and ('/root' == b[4] or '/root'.startswith(b[4].rstrip('/') + '/') or b[4] == '/'):
                mounts.append((len(b[4]), a[0]))
    require(mounts and max(mounts)[1].lower() not in ('9p', 'drvfs', 'ntfs', 'fuseblk', 'cifs', 'vfat', 'exfat'), 'NOT_LINUX_FILESYSTEM')

def main():
    os.umask(0o077)
    if sys.argv[1:] != ['--recover-existing-archive-once']:
        print('S1R_RESULT=STOP_FLAG_REQUIRED'); return 2
    try:
        native_preflight()
        archive = source_path()
    except (Halt, ValueError, OSError, json.JSONDecodeError) as e:
        print('S1R_RESULT=STOP_PREFLIGHT_' + (str(e) if isinstance(e, Halt) else type(e).__name__)); return 2
    marker_fd = os.open(NEW, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(marker_fd, 'w') as fd: fd.write('S1R_ATTEMPT_CONSUMED\n')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    stage = TOOLS / ('.native-gcloud-594.0.1-s1r-incomplete-' + stamp)
    result = 'STOP'; reason = 'UNKNOWN'
    try:
        require(not stage.exists() and not stage.is_symlink(), 'STAGE_COLLISION')
        h = hashlib.sha256()
        with archive.open('rb') as f:
            for block in iter(lambda: f.read(1048576), b''): h.update(block)
            require(h.hexdigest() == SHA, 'ARCHIVE_SHA256_MISMATCH')
            f.seek(0)
            with tarfile.open(fileobj=f, mode='r:gz') as tf: evidence = inspect_archive(tf)
            f.seek(0)
            stage.mkdir(mode=0o700)
            with tarfile.open(fileobj=f, mode='r:gz') as tf: tf.extractall(stage, filter='data')
        cli = stage / 'google-cloud-sdk/bin/gcloud'
        python = stage / 'google-cloud-sdk/platform/bundledpythonunix/bin/python3'
        sdk = stage / 'google-cloud-sdk'
        for item in (cli, python):
            require(item.is_file() and item.resolve().is_relative_to(sdk.resolve()) and
                    item.stat().st_mode & stat.S_IXUSR, 'EXTRACTED_EXECUTABLE_MISSING')
        require(not DEST.exists() and not DEST.is_symlink(), 'DEST_COLLISION')
        stage.rename(DEST)
        result, reason = 'S1R_COMPLETE_NO_CLI_EXECUTION', 'NONE'
    except (Halt, OSError, tarfile.TarError, ValueError) as e:
        reason = str(e) if isinstance(e, Halt) else type(e).__name__
    with NEW.open('a') as fd: fd.write('RESULT=' + result + '\nREASON=' + reason + '\n')
    print('S1R_RESULT=' + result)
    print('S1R_STOP_REASON=' + reason)
    print('S1R_NO_DOWNLOAD_NO_GCLOUD_NO_CLOUD=TRUE')
    return 0 if result == 'S1R_COMPLETE_NO_CLI_EXECUTION' else 2

if __name__ == '__main__': sys.exit(main())
