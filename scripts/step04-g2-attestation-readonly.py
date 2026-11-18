#!/usr/bin/env python3
"""OLDX G2: bounded OFFLINE attestation statement inspection (not signature verification).

Reads existing immutable OCI TAR, never extracts or writes, never uses network,
never prints raw provenance, builder identity, private source URLs or credentials.
Python 3.9+ standard library only. A PASS establishes structure, NOT SLSA trust.
"""
import hashlib
import json
import re
import sys
import tarfile
from pathlib import Path

ARCHIVE = Path('/mnt/d/OLDX/G2/g2-image-proof-d13818-a1/candidate.oci.tar')
INDEX = '93b70b8b09255194974bc46c7e5942c81531261b81224bd80fa575330f7572e4'
AMD64 = 'fde6b74beb8a62678fdc9df4598e5ef1affc2c8be0d89d3502938d4daac4fd68'
ATTESTATION = '04251bbb6dc180c81d8d7d6f47c8be5bb94bc291652571ea6db12799db46fff8'
SOURCE_RECEIPT = 'd13818acc66e1ffcca5e72209658e24129a1061d'
DIGEST = re.compile(r'^sha256:([a-f0-9]{64})$')
INTOTO = 'application/vnd.in-toto+json'
ARTIFACT = 'application/vnd.docker.attestation.manifest.v1+json'
MAX_METADATA = 2 * 1024 * 1024
MAX_STATEMENT = 8 * 1024 * 1024

class Stop(Exception):
    pass

def require(cond, reason):
    if not cond:
        raise Stop(reason)

def inspect(path=ARCHIVE):
    require(path.is_file(), 'ARCHIVE_NOT_FOUND')
    with tarfile.open(path, 'r:') as archive:
        # Paths only; no archive extraction and no writing.
        entries = {}
        for member in archive:
            raw = member.name
            require(raw and not raw.startswith('/') and '\\' not in raw,
                    'UNEXPECTED_TAR_PATH')
            name = raw[2:] if raw.startswith('./') else raw
            if not member.isfile():
                continue
            require(name not in entries, 'DUPLICATE_TAR_PATH')
            entries[name] = member

        def blob(sha, limit):
            require(bool(re.fullmatch('[a-f0-9]{64}', sha)), 'BAD_DIGEST')
            key = 'blobs/sha256/' + sha
            require(key in entries, 'PINNED_BLOB_MISSING')
            member = entries[key]
            require(0 < member.size <= limit, 'BLOB_SIZE_OUT_OF_SCOPE')
            stream = archive.extractfile(member)
            require(stream is not None, 'BLOB_NOT_READABLE')
            with stream:
                payload = stream.read(limit + 1)
            require(len(payload) == member.size, 'BLOB_LENGTH_MISMATCH')
            require(hashlib.sha256(payload).hexdigest() == sha, 'BLOB_SHA_MISMATCH')
            return payload

        def object_for(sha, limit):
            try:
                doc = json.loads(blob(sha, limit))
            except (ValueError, UnicodeDecodeError):
                raise Stop('MALFORMED_JSON') from None
            require(isinstance(doc, dict), 'JSON_NOT_OBJECT')
            return doc

        index = object_for(INDEX, MAX_METADATA)
        descriptors = index.get('manifests')
        require(isinstance(descriptors, list), 'INDEX_DESCRIPTORS_MISSING')
        ids = [d.get('digest') for d in descriptors if isinstance(d, dict)]
        require('sha256:' + AMD64 in ids and 'sha256:' + ATTESTATION in ids,
                'ATT_AND_AMD64_NOT_IN_SAME_INDEX')
        doc = object_for(ATTESTATION, MAX_METADATA)
        require(doc.get('artifactType') == ARTIFACT, 'NOT_EXPECTED_ATTESTATION')
        subject = doc.get('subject')
        require(isinstance(subject, dict) and subject.get('digest') == 'sha256:' + AMD64,
                'ATTESTATION_SUBJECT_MISMATCH')
        layers = doc.get('layers')
        require(isinstance(layers, list) and 1 <= len(layers) <= 10,
                'ATTESTATION_LAYER_COUNT_UNEXPECTED')
        counts = {'slsa': 0, 'spdx': 0, 'other': 0, 'matching_subject': 0,
                  'source_sha_mentioned': 0, 'builder_id_present': 0}
        for layer in layers:
            require(isinstance(layer, dict), 'INVALID_LAYER_DESCRIPTOR')
            require(layer.get('mediaType') == INTOTO, 'UNEXPECTED_LAYER_MEDIA_TYPE')
            match = DIGEST.fullmatch(str(layer.get('digest', '')))
            require(match is not None, 'LAYER_DIGEST_INVALID')
            expected_size = layer.get('size')
            require(isinstance(expected_size, int) and 0 < expected_size <= MAX_STATEMENT,
                    'LAYER_SIZE_NOT_ALLOWED')
            key = 'blobs/sha256/' + match.group(1)
            require(key in entries and entries[key].size == expected_size,
                    'LAYER_DESCRIPTOR_SIZE_MISMATCH')
            stmt = json.loads(blob(match.group(1), MAX_STATEMENT))
            require(isinstance(stmt, dict) and stmt.get('_type') in
                    ('https://in-toto.io/Statement/v1', 'https://in-toto.io/Statement/v0.1'),
                    'NOT_IN_TOTO_STATEMENT')
            predicate = stmt.get('predicateType')
            require(isinstance(predicate, str) and 0 < len(predicate) <= 256,
                    'PREDICATE_TYPE_INVALID')
            declared = (layer.get('annotations') or {}).get('in-toto.io/predicate-type')
            require(declared is None or declared == predicate,
                    'ANNOTATED_PREDICATE_MISMATCH')
            kind = ('slsa' if predicate.startswith('https://slsa.dev/provenance/') else
                    'spdx' if predicate == 'https://spdx.dev/Document' else 'other')
            counts[kind] += 1
            subjects = stmt.get('subject')
            require(isinstance(subjects, list), 'STATEMENT_SUBJECT_NOT_ARRAY')
            if any(isinstance(item, dict) and
                   isinstance(item.get('digest'), dict) and
                   item['digest'].get('sha256') == AMD64 for item in subjects):
                counts['matching_subject'] += 1
            if SOURCE_RECEIPT in json.dumps(stmt, separators=(',', ':')):
                counts['source_sha_mentioned'] += 1
            p = stmt.get('predicate')
            if kind == 'slsa' and isinstance(p, dict):
                run_details = p.get('runDetails') or {}
                builder = (run_details.get('builder') if isinstance(run_details, dict)
                           else None) or p.get('builder')
                if isinstance(builder, dict) and isinstance(builder.get('id'), str) and builder['id']:
                    counts['builder_id_present'] += 1
        return counts, len(layers)

def main():
    try:
        counts, n = inspect()
    except (Stop, OSError, tarfile.TarError, ValueError, UnicodeDecodeError) as exc:
        reason = str(exc) if isinstance(exc, Stop) else 'LOCAL_PARSE_OR_IO_ERROR'
        print('STOP_OFFLINE_ATTESTATION_' + reason)
        return 2
    print('ATTESTATION_INDEX_AND_MANIFEST_SHA256=PASS')
    print('ATTESTATION_MANIFEST_SUBJECT_AMD64=PASS')
    print('IN_TOTO_LAYERS_SHA256=PASS')
    print('IN_TOTO_LAYER_COUNT=' + str(n))
    print('SLSA_PREDICATE_COUNT=' + str(counts['slsa']))
    print('SPDX_PREDICATE_COUNT=' + str(counts['spdx']))
    print('OTHER_PREDICATE_COUNT=' + str(counts['other']))
    print('MATCHING_STATEMENT_SUBJECT_COUNT=' + str(counts['matching_subject']))
    print('PRIOR_SOURCE_SHA_MENTION_COUNT_UNTRUSTED=' + str(counts['source_sha_mentioned']))
    print('SLSA_BUILDER_ID_PRESENT_COUNT_UNTRUSTED=' + str(counts['builder_id_present']))
    print('INDEPENDENT_SIGNATURE_VERIFICATION=NOT_PERFORMED')
    print('SLSA_BUILD_LEVEL=UNKNOWN')
    print('G2_RELEASE=HOLD_NOT_DEPLOYABLE')
    print('REGISTRY_AND_PRODUCTION=NOT_CHANGED')
    return 0

if __name__ == '__main__':
    sys.exit(main())
