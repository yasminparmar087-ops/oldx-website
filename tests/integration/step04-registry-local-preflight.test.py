import hashlib
import importlib.util
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('preflight', Path(__file__).resolve().parents[2] / 'scripts' / 'step04-registry-local-preflight.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def payload(value):
    return json.dumps(value, separators=(',', ':'), sort_keys=True).encode()

def dig(blob):
    return 'sha256:' + hashlib.sha256(blob).hexdigest()

def make_tar(tar_path, *, mutate_blob=False, directories=False, dot_prefix=False, extra_entry=None):
    config = payload({'rootfs': {'diff_ids': ['sha256:' + 'f'*64 for _ in range(30)]}})
    manifest = payload({'schemaVersion': 2,
        'config': {'digest': dig(config), 'size': len(config)}, 'layers': []})
    index = payload({'schemaVersion': 2, 'manifests': [
        {'digest': dig(manifest), 'size': len(manifest),
         'platform': {'os': 'linux', 'architecture': 'amd64'}}]})
    root = payload({'schemaVersion': 2, 'manifests': [
        {'digest': dig(index), 'size': len(index)}]})
    blobs = {dig(b): b for b in [config,manifest,index]}
    for i in range(34):
        blob = b'unit-test-filler:' + str(i).encode()
        blobs[dig(blob)] = blob
    assert len(blobs) == 37
    with tarfile.open(tar_path, 'w') as arc:
        if directories:
            for name in ('./', './blobs/', './blobs/sha256/'):
                ti=tarfile.TarInfo(name);ti.type=tarfile.DIRTYPE;arc.addfile(ti)
        prefix = './' if dot_prefix else ''
        for name,data in [('index.json', root), ('oci-layout', b'{"imageLayoutVersion":"1.0.0"}')]:
            ti=tarfile.TarInfo(prefix+name);ti.size=len(data);arc.addfile(ti,io.BytesIO(data))
        for i,(sha,data) in enumerate(blobs.items()):
            ti=tarfile.TarInfo(prefix+'blobs/sha256/'+sha[7:]);ti.size=len(data)
            arc.addfile(ti,io.BytesIO(data if not mutate_blob or i else b'X'+data[1:]))
        if extra_entry:
            ti=tarfile.TarInfo(extra_entry)
            ti.size=0;arc.addfile(ti,io.BytesIO(b''))
    return dig(index),dig(manifest),dig(config)

class TestReadOnlyRegistryPreflight(unittest.TestCase):
    def test_valid_manifest_graph_and_sha(self):
        with tempfile.TemporaryDirectory() as root:
            tar=Path(root)/'test.oci.tar';index,child,config=make_tar(tar)
            old=(mod.INDEX,mod.AMD64,mod.CONFIG,mod.EXPECTED_ARCHIVE_BYTES)
            try:
                mod.INDEX,mod.AMD64,mod.CONFIG=index,child,config
                mod.EXPECTED_ARCHIVE_BYTES=tar.stat().st_size
                self.assertEqual(mod.verify(tar),hashlib.sha256(tar.read_bytes()).hexdigest())
            finally:
                mod.INDEX,mod.AMD64,mod.CONFIG,mod.EXPECTED_ARCHIVE_BYTES=old

    def test_common_directory_headers_and_dot_prefixed_paths_pass(self):
        with tempfile.TemporaryDirectory() as root:
            for dotted in (True, False):
                tar=Path(root)/'directory-layout.oci.tar'
                index,child,config=make_tar(tar, directories=True, dot_prefix=dotted)
                old=(mod.INDEX,mod.AMD64,mod.CONFIG,mod.EXPECTED_ARCHIVE_BYTES)
                try:
                    mod.INDEX,mod.AMD64,mod.CONFIG=index,child,config
                    mod.EXPECTED_ARCHIVE_BYTES=tar.stat().st_size
                    self.assertEqual(mod.verify(tar),
                                     hashlib.sha256(tar.read_bytes()).hexdigest())
                finally:
                    mod.INDEX,mod.AMD64,mod.CONFIG,mod.EXPECTED_ARCHIVE_BYTES=old

    def test_extra_path_and_traversal_still_fail_closed(self):
        with tempfile.TemporaryDirectory() as root:
            for name in ('unexpected.txt', '../escape'):
                tar=Path(root)/'bad-entry.oci.tar'
                index,child,config=make_tar(tar,directories=True, dot_prefix=True,
                                            extra_entry=name)
                old=(mod.INDEX,mod.AMD64,mod.CONFIG,mod.EXPECTED_ARCHIVE_BYTES)
                try:
                    mod.INDEX,mod.AMD64,mod.CONFIG=index,child,config
                    mod.EXPECTED_ARCHIVE_BYTES=tar.stat().st_size
                    with self.assertRaisesRegex(mod.Stop,'UNEXPECTED_ARCHIVE_ENTRY'):
                        mod.verify(tar)
                finally:
                    mod.INDEX,mod.AMD64,mod.CONFIG,mod.EXPECTED_ARCHIVE_BYTES=old

    def test_detect_corrupt_blob(self):
        with tempfile.TemporaryDirectory() as root:
            tar=Path(root)/'bad.oci.tar';index,child,config=make_tar(tar,mutate_blob=True)
            old=(mod.INDEX,mod.AMD64,mod.CONFIG,mod.EXPECTED_ARCHIVE_BYTES)
            try:
                mod.INDEX,mod.AMD64,mod.CONFIG=index,child,config
                mod.EXPECTED_ARCHIVE_BYTES=tar.stat().st_size
                with self.assertRaisesRegex(mod.Stop,'BLOB_SHA256_MISMATCH'):
                    mod.verify(tar)
            finally:
                mod.INDEX,mod.AMD64,mod.CONFIG,mod.EXPECTED_ARCHIVE_BYTES=old

    def test_wrong_oci_index_denied(self):
        with tempfile.TemporaryDirectory() as root:
            tar=Path(root)/'test.oci.tar';index,child,config=make_tar(tar)
            old=(mod.INDEX,mod.AMD64,mod.CONFIG,mod.EXPECTED_ARCHIVE_BYTES)
            try:
                mod.INDEX,mod.AMD64,mod.CONFIG='sha256:'+'a'*64,child,config
                mod.EXPECTED_ARCHIVE_BYTES=tar.stat().st_size
                with self.assertRaisesRegex(mod.Stop,'SELECTED_INDEX_NOT_ROOT_REFERENCED'):
                    mod.verify(tar)
            finally:
                mod.INDEX,mod.AMD64,mod.CONFIG,mod.EXPECTED_ARCHIVE_BYTES=old

if __name__ == '__main__':
    unittest.main()
