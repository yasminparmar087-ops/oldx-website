"""Offline evidence gate for the *already consumed* H1A raw OCI manifest diagnostic.

No network, Docker, scanner, or build operations. Passing this gate does NOT
establish architecture, layer integrity, publisher signatures or build readiness.
"""
import hashlib
import json
from pathlib import Path

PIN = 'sha256:49559f4ee6632a11a13a7e198183efee1226de7a8f437df83c180b01bd8253ec'
RECEIPT_SHA = 'f301f77236a1af5ac5ee14ef426e3ff1226aa49ec0955fc33d7cea622203b704'
SIZE = 4639
MEDIA = 'application/vnd.oci.image.manifest.v1+json'
URL = 'https://gcr.io/v2/distroless/nodejs24-debian13/manifests/' + PIN
EVIDENCE_FOLDER = 'oldx-h1a-base-manifest-diagnostic-20261124T194159Z'
MARKER_NAME = '.oldx-h1a-base-raw-manifest-once-20261125'
SOURCES = {
    'functions/staging-marketplace/Dockerfile.c2-mediator-off': 'ec36707fce197150e3f5f1b4bd1d0f30d8cbf7fa',
    'functions/staging-marketplace/Dockerfile.c2-mediator-off.dockerignore': 'fc1944d7165bccc1bef5c06901841792724f751d',
    'functions/staging-marketplace/c2-mediator-off-server.mjs': '68e65e2e1cdce5994780a5588c8a02da3e1f4be7',
}

def _read_owned(path, *, ceiling):
    if path.is_symlink() or not path.is_file():
        raise ValueError('H1A_EVIDENCE_MISSING_OR_SYMLINK')
    if path.stat().st_mode & 0o077:
        raise ValueError('H1A_EVIDENCE_PERMISSION_TOO_BROAD')
    with path.open('rb') as file:
        data = file.read(ceiling + 1)
    if len(data) > ceiling:
        raise ValueError('H1A_EVIDENCE_OVERSIZE')
    return data


def verify_recorded_base(evidence_dir, *, marker_path=None, expected_pin=PIN,
                         expected_receipt_sha=RECEIPT_SHA, expected_size=SIZE,
                         expected_url=URL):
    """Verify pinned private evidence off-line; overrides only for synthetic tests.

    Never use caller-provided overrides in the H1A execution runner.
    """
    directory = Path(evidence_dir)
    if directory.is_symlink() or not directory.is_dir() or directory.stat().st_mode & 0o077:
        raise ValueError('H1A_EVIDENCE_DIRECTORY_UNTRUSTED')
    marker = Path(marker_path) if marker_path is not None else Path.home() / MARKER_NAME
    marker_data = json.loads(_read_owned(marker, ceiling=1024))
    if marker_data.get('evidence') != str(directory) or marker_data.get('url') != expected_url:
        raise ValueError('H1A_DIAGNOSTIC_MARKER_MISMATCH')
    receipt_bytes = _read_owned(directory / 'receipt.json', ceiling=16384)
    if hashlib.sha256(receipt_bytes).hexdigest() != expected_receipt_sha:
        raise ValueError('H1A_DIAGNOSTIC_RECEIPT_SHA_MISMATCH')
    receipt = json.loads(receipt_bytes)
    h = receipt.get('response_headers')
    if not isinstance(h, dict) or any([
        receipt.get('mode') != 'one_public_raw_manifest_GET_only',
        receipt.get('status') != 'RAW_SHA256_MATCH',
        receipt.get('http_code') != 200,
        receipt.get('requested_digest') != expected_pin,
        receipt.get('requested_reference') != expected_url,
        receipt.get('source_git_blobs') != SOURCES,
        receipt.get('raw_sha256') != expected_pin,
        receipt.get('raw_matches_pin') is not True,
        receipt.get('header_matches_pin') is not True,
        receipt.get('raw_bytes') != expected_size,
        h.get('Content-Type') != MEDIA,
        h.get('Content-Length') != str(expected_size),
        h.get('Docker-Content-Digest') != expected_pin,
        h.get('Content-Encoding') not in ('', 'identity'),
        receipt.get('build') != 'NOT_RUN',
        receipt.get('sbom') != 'NOT_RUN',
        receipt.get('grype') != 'NOT_RUN',
        receipt.get('runtime') != 'NOT_RUN',
    ]):
        raise ValueError('H1A_DIAGNOSTIC_RECEIPT_CONTENT_MISMATCH')
    raw = _read_owned(directory / 'raw-manifest.bin', ceiling=1024 * 1024)
    if len(raw) != expected_size or 'sha256:' + hashlib.sha256(raw).hexdigest() != expected_pin:
        raise ValueError('H1A_RAW_MANIFEST_PIN_MISMATCH')
    try:
        manifest = json.loads(raw)
        if (manifest.get('schemaVersion') != 2 or
            manifest.get('mediaType') != MEDIA or
            not isinstance(manifest.get('config'), dict) or
            not isinstance(manifest.get('layers'), list) or not manifest['layers']):
            raise ValueError('H1A_OCI_MANIFEST_STRUCTURE_UNVERIFIED')
    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError) as error:
        raise ValueError('H1A_OCI_MANIFEST_STRUCTURE_UNVERIFIED') from error
    return {'status': 'LOCAL_RAW_MANIFEST_INTEGRITY_MATCH_ONLY',
            'manifestSha256': expected_pin,
            'receiptSha256': expected_receipt_sha,
            'rawBytes': expected_size,
            'platform': 'UNVERIFIED_REQUIRES_BUILD_OR_CONFIG',
            'layers': 'UNVERIFIED_REQUIRES_BUILD',
            'dockerManifestCliError': 'UNEXPLAINED',
            'h1aBuildAuthorizedToResume': False}
