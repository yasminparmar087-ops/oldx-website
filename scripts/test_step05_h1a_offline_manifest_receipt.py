import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from step05_h1a_offline_manifest_receipt import verify_recorded_base, SOURCES, MEDIA

class OfflineEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.folder = root / 'diagnostic'
        self.folder.mkdir(mode=0o700)
        self.marker = root / 'once'
        self.raw = json.dumps({'schemaVersion': 2, 'mediaType': MEDIA,
            'config': {'mediaType':'application/vnd.oci.image.config.v1+json', 'digest':'sha256:'+'0'*64, 'size':1},
            'layers': [{'mediaType': 'application/vnd.oci.image.layer.v1.tar+gzip', 'digest':'sha256:'+'1'*64,'size':1}]},sort_keys=True).encode()
        self.pin = 'sha256:' + hashlib.sha256(self.raw).hexdigest()
        self.url = 'https://gcr.io/v2/distroless/nodejs24-debian13/manifests/' + self.pin
        self.receipt = {'mode': 'one_public_raw_manifest_GET_only', 'status':'RAW_SHA256_MATCH',
            'http_code':200,'requested_digest':self.pin,'requested_reference':self.url,
            'source_git_blobs':SOURCES, 'raw_sha256':self.pin, 'raw_matches_pin':True,
            'header_matches_pin':True, 'raw_bytes':len(self.raw),
            'response_headers':{'Content-Type':MEDIA,'Content-Length':str(len(self.raw)),
                'Docker-Content-Digest':self.pin, 'Content-Encoding':''},
            'build':'NOT_RUN','sbom':'NOT_RUN','grype':'NOT_RUN','runtime':'NOT_RUN'}
        self.write_files()
    def write_files(self):
        (self.folder / 'raw-manifest.bin').write_bytes(self.raw)
        self.receipt_bytes = (json.dumps(self.receipt)+'\n').encode()
        (self.folder / 'receipt.json').write_bytes(self.receipt_bytes)
        self.marker.write_text(json.dumps({'evidence':str(self.folder),'url':self.url})+'\n')
        for file in [self.folder / 'receipt.json',self.folder / 'raw-manifest.bin',self.marker]:
            os.chmod(file,0o600)
    def check(self):
        return verify_recorded_base(self.folder,marker_path=self.marker,expected_pin=self.pin,
            expected_receipt_sha=hashlib.sha256(self.receipt_bytes).hexdigest(),
            expected_size=len(self.raw),expected_url=self.url)
    def test_verified_consistent_offline_receipt_passes_without_network(self):
        got = self.check()
        self.assertEqual(got['status'],'LOCAL_RAW_MANIFEST_INTEGRITY_MATCH_ONLY')
        self.assertFalse(got['h1aBuildAuthorizedToResume'])
        self.assertEqual(got['platform'],'UNVERIFIED_REQUIRES_BUILD_OR_CONFIG')
    def test_mutated_raw_manifest_denied(self):
        p=self.folder/'raw-manifest.bin'; data=p.read_bytes();p.write_bytes(data[:-1]+b' ')
        with self.assertRaisesRegex(ValueError,'H1A_RAW_MANIFEST_PIN_MISMATCH'):self.check()
    def test_receipt_sha_change_denied(self):
        (self.folder/'receipt.json').write_bytes(self.receipt_bytes+b' ')
        with self.assertRaisesRegex(ValueError,'H1A_DIAGNOSTIC_RECEIPT_SHA_MISMATCH'):self.check()
    def test_false_digest_header_denied(self):
        self.receipt['response_headers']['Docker-Content-Digest']='sha256:'+'f'*64
        self.write_files()
        with self.assertRaisesRegex(ValueError,'H1A_DIAGNOSTIC_RECEIPT_CONTENT_MISMATCH'):self.check()
    def test_marker_mismatch_denied(self):
        self.marker.write_text(json.dumps({'evidence': '/tmp/not-expected','url':self.url}));os.chmod(self.marker,0o600)
        with self.assertRaisesRegex(ValueError,'H1A_DIAGNOSTIC_MARKER_MISMATCH'):self.check()
    def test_insecure_permissions_denied(self):
        os.chmod(self.folder/'receipt.json',0o644)
        with self.assertRaisesRegex(ValueError,'H1A_EVIDENCE_PERMISSION_TOO_BROAD'):self.check()
    def test_missing_manifest_structure_denied(self):
        self.raw=b'{"schemaVersion":2,"mediaType":"'+MEDIA.encode()+b'"}'
        self.pin='sha256:'+hashlib.sha256(self.raw).hexdigest()
        self.url='https://gcr.io/v2/distroless/nodejs24-debian13/manifests/'+self.pin
        self.receipt.update(raw_sha256=self.pin,requested_digest=self.pin,requested_reference=self.url,raw_bytes=len(self.raw))
        self.receipt['response_headers'].update({'Content-Length':str(len(self.raw)),'Docker-Content-Digest':self.pin})
        self.write_files()
        with self.assertRaisesRegex(ValueError,'H1A_OCI_MANIFEST_STRUCTURE_UNVERIFIED'):self.check()
    def test_missing_marker_denied(self):
        self.marker.unlink()
        with self.assertRaisesRegex(ValueError,'H1A_EVIDENCE_MISSING_OR_SYMLINK'):self.check()

if __name__=='__main__': unittest.main()
