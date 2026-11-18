import hashlib
import importlib.util
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
s = importlib.util.spec_from_file_location('g2_attest', ROOT/'scripts'/'step04-g2-attestation-readonly.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)

def obj(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()

def digest(b):
    return hashlib.sha256(b).hexdigest()

def fixture(path, *, mismatch_subject=False, corrupt_statement=False, bad_annotation=False):
    child = obj({'schemaVersion':2, 'mediaType':'application/vnd.oci.image.manifest.v1+json'})
    ci = digest(child)
    statement = obj({'_type':'https://in-toto.io/Statement/v1',
        'subject':[{'name':'test','digest':{'sha256':ci}}],
        'predicateType':'https://slsa.dev/provenance/v1',
        'predicate':{'runDetails':{'builder':{'id':'test-builder'}},
                     'buildDefinition':{'resolvedDependencies':[{'digest':{'gitCommit':m.SOURCE_RECEIPT}}]}}})
    si = digest(statement)
    annotation = 'https://spdx.dev/Document' if bad_annotation else 'https://slsa.dev/provenance/v1'
    att = obj({'schemaVersion':2, 'mediaType':'application/vnd.oci.image.manifest.v1+json',
        'artifactType':m.ARTIFACT,
        'subject':{'digest':'sha256:'+('0'*64 if mismatch_subject else ci)},
        'layers':[{'mediaType':m.INTOTO, 'digest':'sha256:'+si,
                   'size':len(statement),'annotations':{'in-toto.io/predicate-type':annotation}}]})
    ai = digest(att)
    index = obj({'schemaVersion':2, 'manifests':[
        {'digest':'sha256:'+ci},{'digest':'sha256:'+ai}]})
    ii=digest(index)
    members=[(ii,index),(ci,child),(ai,att),(si,statement)]
    with tarfile.open(path,'w') as tar:
        for i,(sha,payload) in enumerate(members):
            if corrupt_statement and i==3:
                payload=b'Z'+payload[1:]
            t=tarfile.TarInfo('./blobs/sha256/'+sha)
            t.size=len(payload);tar.addfile(t,io.BytesIO(payload))
    return ii,ci,ai

class OfflineAttestation(unittest.TestCase):
    def check(self, kwargs, expectation):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp)/'oci.tar'
            ii,ci,ai=fixture(archive,**kwargs)
            old=m.INDEX,m.AMD64,m.ATTESTATION
            try:
                m.INDEX,m.AMD64,m.ATTESTATION=ii,ci,ai
                if expectation=='PASS':
                    counts,n=m.inspect(archive)
                    self.assertEqual(n,1)
                    self.assertEqual(counts['slsa'],1)
                    self.assertEqual(counts['spdx'],0)
                    self.assertEqual(counts['matching_subject'],1)
                    self.assertEqual(counts['source_sha_mentioned'],1)
                    self.assertEqual(counts['builder_id_present'],1)
                else:
                    with self.assertRaisesRegex(m.Stop,expectation):
                        m.inspect(archive)
            finally:
                m.INDEX,m.AMD64,m.ATTESTATION=old

    def test_valid_original_subject_and_untrusted_claims(self):
        self.check({},'PASS')
    def test_attestation_subject_mismatch_stops(self):
        self.check({'mismatch_subject':True},'ATTESTATION_SUBJECT_MISMATCH')
    def test_corrupted_in_toto_statement_stops(self):
        self.check({'corrupt_statement':True},'BLOB_SHA_MISMATCH')
    def test_predicate_annotation_mismatch_stops(self):
        self.check({'bad_annotation':True},'ANNOTATED_PREDICATE_MISMATCH')

if __name__ == '__main__':
    unittest.main()
