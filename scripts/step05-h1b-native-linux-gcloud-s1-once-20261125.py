#!/usr/bin/env python3
"""OLDX H1B S1: ONE owner-approved local-only isolated Google Cloud CLI extraction.

This script NEVER executes gcloud, install.sh, login, SDK config, or Cloud API calls.
A first attempt consumes its own marker even if network or validation fails.
"""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import platform
import posixpath
import re
import ssl
import stat
import sys
import tarfile
import time
from datetime import datetime, timezone
from urllib.parse import urlsplit
from urllib.request import build_opener, HTTPSHandler, HTTPRedirectHandler, ProxyHandler, Request

VERSION = '594.0.1'
SHA256 = 'c6fdba4cb1551b0da7c1d744eb0dfaf68b59861238d6a6b5ef6bad1ba596b567'
FILENAME = 'google-cloud-cli-linux-x86_64.tar.gz'
ARCHIVE_URL = 'https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/' + FILENAME
DOC_URL = 'https://docs.cloud.google.com/sdk/docs/downloads-versioned-archives'
INSTALL_URL = 'https://docs.cloud.google.com/sdk/docs/install-sdk'
TOOLS = Path('/root/oldx-tools')
DEST = TOOLS / ('native-gcloud-' + VERSION)
MARKER = Path('/root/.oldx-h1b-native-gcloud-s1-once-20261125')
EVIDENCE_ROOT = Path('/root')
MAX_DOC_BYTES = 2 * 1024 * 1024
MAX_ARCHIVE_BYTES = 130 * 1024 * 1024
MAX_TOTAL_UNPACKED = 2 * 1024 * 1024 * 1024
MAX_MEMBER_BYTES = 512 * 1024 * 1024
MAX_MEMBERS = 45000


class Stop(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class OfficialRows(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows: list[tuple[str, tuple[str, ...]]] = []
        self.headings: list[str] = []
        self._in_row = False
        self._in_heading = False
        self._parts: list[str] = []
        self._links: list[str] = []
        self._hparts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            if self._in_row:
                raise Stop('OFFICIAL_DOC_NESTED_ROW')
            self._in_row, self._parts, self._links = True, [], []
        elif tag in ('h1', 'h2', 'h3'):
            self._in_heading, self._hparts = True, []
        elif tag == 'a' and self._in_row:
            self._links.extend(v for k, v in attrs if k == 'href' and v is not None)

    def handle_endtag(self, tag):
        if tag == 'tr' and self._in_row:
            self.rows.append((' '.join(self._parts), tuple(self._links)))
            self._in_row = False
        elif tag in ('h1', 'h2', 'h3') and self._in_heading:
            self.headings.append(' '.join(self._hparts))
            self._in_heading = False

    def handle_data(self, data):
        if self._in_row:
            self._parts.append(data)
        if self._in_heading:
            self._hparts.append(data)


def validate_official_pages(installed_html: bytes, archive_html: bytes) -> None:
    """Require matching current release heading AND a single matching official row."""
    for page in (installed_html, archive_html):
        if len(page) > MAX_DOC_BYTES:
            raise Stop('OFFICIAL_DOC_TOO_LARGE')
    installed, archive = OfficialRows(), OfficialRows()
    try:
        installed.feed(installed_html.decode('utf-8'))
        archive.feed(archive_html.decode('utf-8'))
    except (UnicodeError, ValueError) as exc:
        raise Stop('OFFICIAL_DOC_PARSE') from exc
    headings = [' '.join(h.split()).lower() for h in installed.headings]
    if ('install gcloud cli version ' + VERSION).lower() not in headings:
        raise Stop('OFFICIAL_VERSION_DRIFT')
    matched = [(text, links) for text, links in archive.rows if FILENAME in text]
    if len(matched) != 1:
        raise Stop('OFFICIAL_ARCHIVE_ROW_UNVERIFIED')
    text, links = matched[0]
    checksums = re.findall(r'\b[0-9a-fA-F]{64}\b', text)
    if checksums != [SHA256]:
        raise Stop('OFFICIAL_ARCHIVE_SHA_DRIFT')
    if links.count(ARCHIVE_URL) != 1:
        raise Stop('OFFICIAL_ARCHIVE_URL_DRIFT')
    # The official current-version page must independently contain this precise artifact.
    if not any(FILENAME in text and SHA256 in text for text, _ in installed.rows):
        raise Stop('OFFICIAL_INSTALL_PAGE_MISMATCH')


def validate_archive_member(member: tarfile.TarInfo) -> tuple[str, str | None]:
    """All extraction paths and link targets must remain in the dedicated SDK tree."""
    name = member.name
    parts = name.rstrip('/').split('/')
    if (not name or len(name) > 512 or name.startswith('/') or '\\' in name or '\x00' in name
            or ':' in name or any(bit in ('', '.', '..') for bit in parts) or
            (name.endswith('/') and not member.isdir())):
        raise Stop('ARCHIVE_UNSAFE_NAME')
    norm = posixpath.normpath(name)
    if norm != 'google-cloud-sdk' and not norm.startswith('google-cloud-sdk/'):
        raise Stop('ARCHIVE_OUTSIDE_ROOT')
    if member.isdir():
        pass
    elif member.isfile():
        if member.size < 0 or member.size > MAX_MEMBER_BYTES:
            raise Stop('ARCHIVE_FILE_SIZE')
    elif not (member.issym() or member.islnk()):
        raise Stop('ARCHIVE_SPECIAL_MEMBER')
    target = None
    if member.issym() or member.islnk():
        link = member.linkname
        if not link or len(link) > 512 or link.startswith('/') or '\\' in link or '\x00' in link or ':' in link:
            raise Stop('ARCHIVE_UNSAFE_LINK')
        target = posixpath.normpath(posixpath.join(posixpath.dirname(norm) if member.issym() else '', link))
        if target == 'google-cloud-sdk' or not target.startswith('google-cloud-sdk/'):
            raise Stop('ARCHIVE_ESCAPING_LINK')
    return norm, target


def inspect_archive(path: Path) -> dict[str, int]:
    if not hasattr(tarfile, 'data_filter'):
        raise Stop('PYTHON_TAR_DATA_FILTER_REQUIRED')
    seen: set[str] = set()
    total = 0
    count = 0
    links: dict[str, str] = {}
    try:
        with tarfile.open(path, 'r:gz') as archive:
            for m in archive:
                count += 1
                if count > MAX_MEMBERS:
                    raise Stop('ARCHIVE_MEMBER_CAP')
                name, target = validate_archive_member(m)
                if name in seen:
                    raise Stop('ARCHIVE_DUPLICATE_NAME')
                seen.add(name)
                if m.isfile():
                    total += m.size
                    if total > MAX_TOTAL_UNPACKED:
                        raise Stop('ARCHIVE_EXPANDED_CAP')
                if target:
                    links[name] = target
            if 'google-cloud-sdk/bin/gcloud' not in seen:
                raise Stop('ARCHIVE_MISSING_CLI')
            # Forbid links to missing archive members or symlink cycles, not just ../ escapes.
            for path_name in links:
                cursor = path_name
                visited: set[str] = set()
                while cursor in links:
                    if cursor in visited:
                        raise Stop('ARCHIVE_LINK_CYCLE')
                    visited.add(cursor)
                    cursor = links[cursor]
                if cursor not in seen:
                    raise Stop('ARCHIVE_DANGLING_LINK')
    except (tarfile.TarError, OSError, EOFError) as exc:
        raise Stop('ARCHIVE_UNREADABLE') from exc
    return {'members': count, 'unpacked_bytes': total}


def open_official(url: str, *, max_size: int, deadline_seconds: float, output: Path | None = None) -> tuple[bytes | None, str, int]:
    parts = urlsplit(url)
    if parts.scheme != 'https' or parts.username or parts.password or parts.fragment or parts.query or parts.hostname not in ('dl.google.com', 'docs.cloud.google.com'):
        raise Stop('OFFICIAL_URL_REJECTED')
    if url not in (DOC_URL, INSTALL_URL, ARCHIVE_URL):
        raise Stop('OFFICIAL_URL_UNEXPECTED')
    opener = build_opener(ProxyHandler({}), HTTPSHandler(context=ssl.create_default_context()), NoRedirect())
    request = Request(url, headers={'Accept-Encoding': 'identity', 'User-Agent': 'OLDX-H1B-S1-integrity/1.0'}, method='GET')
    start = time.monotonic()
    sha = hashlib.sha256()
    count = 0
    chunks = []
    try:
        with opener.open(request, timeout=18) as response:
            if response.status != 200 or response.geturl() != url:
                raise Stop('OFFICIAL_HTTP_STATUS_OR_REDIRECT')
            if response.headers.get('Content-Encoding', 'identity').lower() != 'identity':
                raise Stop('OFFICIAL_CONTENT_ENCODING')
            length = response.headers.get('Content-Length')
            if length is not None and (not length.isascii() or not length.isdecimal() or int(length) > max_size):
                raise Stop('OFFICIAL_CONTENT_LENGTH')
            stream = output.open('xb') if output else None
            try:
                while True:
                    if time.monotonic() - start > deadline_seconds:
                        raise Stop('OFFICIAL_DOWNLOAD_DEADLINE')
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    count += len(block)
                    if count > max_size:
                        raise Stop('OFFICIAL_SIZE_LIMIT')
                    sha.update(block)
                    if stream:
                        stream.write(block)
                    else:
                        chunks.append(block)
                if length is not None and count != int(length):
                    raise Stop('OFFICIAL_TRUNCATED_DOWNLOAD')
            finally:
                if stream:
                    stream.close()
    except Stop:
        raise
    except Exception as exc:
        raise Stop('OFFICIAL_NETWORK_OR_TLS_STOP_' + type(exc).__name__) from exc
    if count == 0:
        raise Stop('OFFICIAL_EMPTY_DOWNLOAD')
    return (None if output else b''.join(chunks)), sha.hexdigest(), count


def wsl_preflight() -> None:
    if platform.system() != 'Linux' or platform.machine() not in ('x86_64', 'amd64'):
        raise Stop('NOT_LINUX_X86_64')
    if 'microsoft' not in platform.release().lower() or os.geteuid() != 0:
        raise Stop('NOT_OWNER_ROOT_WSL')
    if sys.version_info < (3, 12) or not hasattr(tarfile, 'data_filter'):
        raise Stop('PYTHON312_REQUIRED')
    if Path('/root').is_symlink() or Path('/root').resolve() != Path('/root'):
        raise Stop('ROOT_SYMLINK_OR_MOUNT')
    if not Path('/root').is_dir() or Path('/root').stat().st_uid != 0:
        raise Stop('INVALID_LINUX_HOME')
    if DEST.exists() or DEST.is_symlink() or MARKER.exists() or MARKER.is_symlink():
        raise Stop('S1_MARKER_OR_DEST_ALREADY_EXISTS')
    if TOOLS.is_symlink() or (TOOLS.exists() and (not TOOLS.is_dir() or TOOLS.stat().st_uid != 0)):
        raise Stop('TOOLS_PARENT_UNSAFE')
    mount_lines = Path('/proc/self/mountinfo').read_text(encoding='utf-8').splitlines()
    mounts = []
    for line in mount_lines:
        before, sep, after = line.partition(' - ')
        if sep:
            fields = before.split()
            backend = after.split()
            if len(fields) >= 5 and backend:
                mounts.append((fields[4].replace('\\040', ' '), backend[0]))
    relevant = [(len(mp), fstype) for mp, fstype in mounts if '/root' == mp or '/root'.startswith(mp.rstrip('/') + '/') or mp == '/']
    if not relevant or max(relevant)[1].lower() in ('9p', 'drvfs', 'fuseblk', 'fuse', 'ntfs', 'cifs', 'vfat', 'exfat'):
        raise Stop('NOT_NATIVE_LINUX_STORAGE')
    disk = os.statvfs('/root')
    if disk.f_bavail * disk.f_frsize < 2 * 1024 * 1024 * 1024:
        raise Stop('S1_FREE_SPACE_BELOW_2GIB')


def installed_paths(stage: Path) -> dict[str, str]:
    sdk = stage / 'google-cloud-sdk'
    gcloud = sdk / 'bin/gcloud'
    bundled = sdk / 'platform/bundledpythonunix/bin/python3'
    for path in (gcloud, bundled):
        if not path.is_file() or not path.resolve().is_relative_to(sdk.resolve()):
            raise Stop('SDK_REQUIRED_FILE_MISSING')
    if not (gcloud.stat().st_mode & stat.S_IXUSR) or not (bundled.stat().st_mode & stat.S_IXUSR):
        raise Stop('SDK_FILE_NOT_EXECUTABLE')
    return {'cli': 'google-cloud-sdk/bin/gcloud', 'bundled_python': 'google-cloud-sdk/platform/bundledpythonunix/bin/python3'}


def main() -> int:
    os.umask(0o077)
    if sys.argv[1:] != ['--setup-local-once']:
        print('S1_RESULT=STOP_FLAG_REQUIRED')
        return 2
    try:
        wsl_preflight()
    except Stop as exc:
        print('S1_RESULT=STOP_' + str(exc))
        return 2
    evidence = EVIDENCE_ROOT / ('oldx-h1b-native-gcloud-s1-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    stage = TOOLS / ('.native-gcloud-' + VERSION + '-s1-incomplete-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    if evidence.exists() or stage.exists() or evidence.is_symlink() or stage.is_symlink():
        print('S1_RESULT=STOP_S1_SESSION_COLLISION')
        return 2
    marker_fd = os.open(MARKER, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(marker_fd, 'w', encoding='utf-8') as m:
        m.write('S1_ATTEMPT_CONSUMED\nEVIDENCE=' + str(evidence) + '\n')
    result = {'scope': 'S1_LOCAL_ONLY', 'state': 'STOP', 'version': VERSION, 'sha_expected': SHA256,
              'download_url': ARCHIVE_URL, 'gcloud_invoked': False, 'cloud_api_invoked': False}
    try:
        evidence.mkdir(mode=0o700)
        TOOLS.mkdir(mode=0o700, exist_ok=True)
        if TOOLS.is_symlink() or TOOLS.stat().st_uid != 0:
            raise Stop('TOOLS_PARENT_CHANGED')
        docs, _, _ = open_official(DOC_URL, max_size=MAX_DOC_BYTES, deadline_seconds=40)
        install, _, _ = open_official(INSTALL_URL, max_size=MAX_DOC_BYTES, deadline_seconds=40)
        validate_official_pages(install or b'', docs or b'')
        result['official_pages_consistent'] = True
        archive_path = evidence / FILENAME
        _, actual_sha, downloaded = open_official(ARCHIVE_URL, max_size=MAX_ARCHIVE_BYTES,
                                                    deadline_seconds=300, output=archive_path)
        result['download_bytes'] = downloaded
        result['sha_actual'] = actual_sha
        if actual_sha != SHA256:
            raise Stop('ARCHIVE_SHA256_MISMATCH')
        structure = inspect_archive(archive_path)
        result['archive_structure'] = structure
        stage.mkdir(mode=0o700)
        with tarfile.open(archive_path, 'r:gz') as archive:
            archive.extractall(stage, filter='data')
        result.update(installed_paths(stage))
        if DEST.exists() or DEST.is_symlink():
            raise Stop('DEST_COLLISION_AFTER_DOWNLOAD')
        stage.rename(DEST)
        result['state'] = 'S1_COMPLETE_NO_CLI_EXECUTION'
        result['installed_at'] = str(DEST)
    except Stop as exc:
        result['stop_reason'] = str(exc)
    except Exception as exc:
        result['stop_reason'] = 'UNEXPECTED_' + type(exc).__name__
    finally:
        if evidence.is_dir():
            receipt = evidence / 'receipt.json'
            receipt.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8')
        with MARKER.open('a', encoding='utf-8') as m:
            m.write('RESULT=' + result['state'] + '\n')
            m.write('DETAIL=' + str(result.get('stop_reason', 'SUCCESS')) + '\n')
        print('S1_RESULT=' + result['state'])
        print('S1_STOP_REASON=' + str(result.get('stop_reason', 'NONE')))
        print('S1_VERSION=' + VERSION)
        print('S1_EXPECTED_SHA256=' + SHA256)
        print('S1_EVIDENCE=' + str(evidence))
        print('S1_CLOUD_OR_GCLOUD_ACTION=NONE')
    return 0 if result['state'] == 'S1_COMPLETE_NO_CLI_EXECUTION' else 2


if __name__ == '__main__':
    sys.exit(main())
