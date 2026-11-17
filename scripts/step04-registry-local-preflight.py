#!/usr/bin/env python3
"""OLDX Step04: read-only, offline verifier of ONE existing OCI tar.

No cloud calls, registry credentials, shell commands, image rebuild, extraction,
file writes or upload. It checks the already-attested local image identities.
Passing this tool is *not* a provider publish, vulnerability waiver or signed
supply-chain custody proof. Python 3.9+ standard library only.
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
import tarfile
from pathlib import Path

EXPECTED_FILE = Path('/mnt/d/OLDX/G2/g2-image-proof-d13818-a1/candidate.oci.tar')
EXPECTED_ARCHIVE_BYTES = 88_515_072
EXPECTED_BLOB_COUNT = 37
EXPECTED_DIFF_IDS = 30
INDEX = 'sha256:93b70b8b09255194974bc46c7e5942c81531261b81224bd80fa575330f7572e4'
AMD64 = 'sha256:fde6b74beb8a62678fdc9df4598e5ef1affc2c8be0d89d3502938d4daac4fd68'
CONFIG = 'sha256:a1564f402a24e80b42df6a7c2b6fbfa8e9938b1ea1619771532d578d19c01fa2'
SOURCE_SHA = 'd13818acc66e1ffcca5e72209658e24129a1061d'
DIGEST = re.compile(r'^sha256:[0-9a-f]{64}$')
BLOB = re.compile(r'^blobs/sha256/[0-9a-f]{64}$')
JSON_LIMIT = 1_048_576

class Stop(Exception):
    pass

def need(ok, reason):
    if not ok:
        raise Stop(reason)

def json_bytes(payload, label):
    need(len(payload) <= JSON_LIMIT, f'{label}_TOO_LARGE')
    try:
        value = json.loads(payload)
    except (ValueError, UnicodeDecodeError):
        raise Stop(f'{label}_NOT_JSON') from None
    need(isinstance(value, dict), f'{label}_NOT_OBJECT')
    return value

def canonical_tar_members(tar):
    members = {}
    directories = set()
    for member in tar:
        raw = member.name
        # OCI exporters often include the harmless ./, blobs/ and
        # blobs/sha256/ directory headers, and may prefix paths with ./.
        # Accept ONLY these three directories; never extract anything.
        need(isinstance(raw, str) and raw and not raw.startswith('/') and
             "\\" not in raw, 'UNEXPECTED_ARCHIVE_ENTRY')
        name = raw[2:] if raw.startswith('./') else raw
        if member.isdir():
            directory = name.rstrip('/')
            need(directory in ('', '.', 'blobs', 'blobs/sha256') and
                 member.size == 0, 'UNEXPECTED_ARCHIVE_ENTRY')
            # Treat . and ./ as the same single root directory.
            directory = '.' if directory == '' else directory
            need(directory not in directories, 'DUPLICATE_ARCHIVE_ENTRY')
            directories.add(directory)
            continue
        # Only normal files in the OCI layout, no links, devices, extra data,
        # traversal, or duplicate names after optional ./ normalization.
        need(member.isfile() and
             (name in ('oci-layout', 'index.json') or BLOB.fullmatch(name)) and
             all(part not in ('', '.', '..') for part in name.split('/')),
             'UNEXPECTED_ARCHIVE_ENTRY')
        need(name not in members, 'DUPLICATE_ARCHIVE_ENTRY')
        members[name] = member
    need('oci-layout' in members and 'index.json' in members, 'NOT_OCI_LAYOUT')
    blobs = [name for name in members if BLOB.fullmatch(name)]
    need(len(blobs) == EXPECTED_BLOB_COUNT and len(members) == EXPECTED_BLOB_COUNT + 2,
         'UNEXPECTED_BLOB_SET')
    return members

def read_member(tar, member, cap):
    need(member.size <= cap, 'METADATA_TOO_LARGE')
    stream = tar.extractfile(member)
    need(stream is not None, 'ARCHIVE_READ_FAILED')
    with stream:
        return stream.read()

def verify(path=EXPECTED_FILE):
    path = Path(path)
    need(path.is_file(), 'ARCHIVE_MISSING')
    need(path.stat().st_size == EXPECTED_ARCHIVE_BYTES, 'ARCHIVE_SIZE_CHANGED')
    with tarfile.open(path, 'r:') as tar:
        members = canonical_tar_members(tar)
        # Hash every blob by streaming, so layer data are never held in memory.
        for name, member in members.items():
            if not BLOB.fullmatch(name):
                continue
            stream = tar.extractfile(member)
            need(stream is not None, 'ARCHIVE_BLOB_READ_FAILED')
            h = hashlib.sha256()
            with stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(block)
            need(h.hexdigest() == name.rsplit('/', 1)[1], 'BLOB_SHA256_MISMATCH')

        def load(ref, label):
            need(isinstance(ref, str) and DIGEST.fullmatch(ref), f'{label}_INVALID_DIGEST')
            key = f'blobs/sha256/{ref[7:]}'
            need(key in members, f'{label}_MISSING_BLOB')
            return json_bytes(read_member(tar, members[key], JSON_LIMIT), label)

        root = json_bytes(read_member(tar, members['index.json'], JSON_LIMIT), 'ROOT_INDEX')
        layout = json_bytes(read_member(tar, members['oci-layout'], JSON_LIMIT), 'OCI_LAYOUT')
        need(layout.get('imageLayoutVersion') == '1.0.0', 'UNSUPPORTED_LAYOUT')
        need(root.get('schemaVersion') == 2 and isinstance(root.get('manifests'), list),
             'ROOT_INDEX_INVALID')
        root_refs = [x.get('digest') for x in root['manifests'] if isinstance(x, dict)]
        need(INDEX in root_refs, 'SELECTED_INDEX_NOT_ROOT_REFERENCED')
        inner = load(INDEX, 'SELECTED_INDEX')
        need(inner.get('schemaVersion') == 2 and isinstance(inner.get('manifests'), list),
             'SELECTED_INDEX_INVALID')
        amd64_descriptors = [d for d in inner['manifests']
                             if isinstance(d, dict) and d.get('digest') == AMD64]
        need(len(amd64_descriptors) == 1, 'AMD64_CHILD_NOT_UNIQUE')
        platform = amd64_descriptors[0].get('platform') or {}
        need(isinstance(platform, dict) and platform.get('os') == 'linux' and
             platform.get('architecture') == 'amd64',
             'WRONG_CHILD_PLATFORM')
        manifest = load(AMD64, 'AMD64_MANIFEST')
        need(manifest.get('schemaVersion') == 2 and
             isinstance(manifest.get('config'), dict) and
             manifest['config'].get('digest') == CONFIG,
             'CONFIG_IDENTITY_CHANGED')
        config = load(CONFIG, 'IMAGE_CONFIG')
        rootfs = config.get('rootfs')
        need(isinstance(rootfs, dict), 'ROOTFS_MISSING')
        diffids = rootfs.get('diff_ids')
        need(isinstance(diffids, list) and len(diffids) == EXPECTED_DIFF_IDS and
             all(isinstance(x, str) and DIGEST.fullmatch(x) for x in diffids),
             'ROOTFS_DIFFID_COUNT_CHANGED')
        # Full member SHA was checked above; verify all immediate index/manifest
        # descriptor identities and sizes but do NOT purport to attest signatures.
        for d in [*root['manifests'], *inner['manifests'], manifest['config'],
                  *(manifest.get('layers') or [])]:
            need(isinstance(d, dict) and DIGEST.fullmatch(str(d.get('digest', ''))),
                 'DESCRIPTOR_INVALID')
            key = 'blobs/sha256/' + d['digest'][7:]
            need(key in members and isinstance(d.get('size'), int) and
                 d['size'] == members[key].size, 'DESCRIPTOR_SIZE_OR_BLOB_MISMATCH')
    archive_hash = hashlib.sha256()
    with path.open('rb') as inp:
        for block in iter(lambda: inp.read(1024 * 1024), b''):
            archive_hash.update(block)
    return archive_hash.hexdigest()

def main():
    try:
        result = verify()
    except (Stop, OSError, tarfile.TarError) as exc:
        code = exc.args[0] if isinstance(exc, Stop) else 'LOCAL_IO_OR_TAR_ERROR'
        print(f'STOP_REGISTRY_LOCAL_PREFLIGHT: {code}')
        return 2
    print('PASS_LOCAL_OCI_LAYOUT_AND_BLOB_SHA256')
    print('PINNED_SOURCE_SHA_PRIOR_RECEIPT_ONLY=' + SOURCE_SHA)
    print('IMAGE_INDEX=' + INDEX)
    print('AMD64_MANIFEST=' + AMD64)
    print('IMAGE_CONFIG=' + CONFIG)
    print('ARCHIVE_SHA256=' + result)
    print('REGISTRY_PUBLICATION=NOT_DONE')
    print('CVE_RISK=9_HIGH_UNRESOLVED')
    print('G4_IAM=UNVERIFIED; G8_COST_STOP=BLOCKED')
    return 0

if __name__ == '__main__':
    sys.exit(main())
