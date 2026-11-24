import importlib.util
import io
import pathlib
import subprocess
import sys
import tarfile
import tempfile
import unittest

SOURCE=pathlib.Path(__file__).resolve().parents[2]/'scripts/step05-h1b-s1r-offline-extract-once-20261125.py'
spec=importlib.util.spec_from_file_location('oldx_s1r',SOURCE)
s1r=importlib.util.module_from_spec(spec)
spec.loader.exec_module(s1r)
ROOT='google-cloud-sdk'


def tar_with(link_to='../expired/ca',escape=False,include_file=True,link_type=tarfile.SYMTYPE):
    tmp=tempfile.TemporaryDirectory()
    p=pathlib.Path(tmp.name)/'a.tar.gz'
    with tarfile.open(p,'w:gz') as tf:
        def entry(name, content=None, typ=tarfile.REGTYPE, target=None):
            member=tarfile.TarInfo(name)
            member.mode=0o755
            member.type=typ
            if target is not None: member.linkname=target
            if content is not None:
                member.size=len(content)
                tf.addfile(member,io.BytesIO(content))
            else: tf.addfile(member)
        entry(ROOT+'/',typ=tarfile.DIRTYPE)
        entry(ROOT+'/bin/gcloud',b'ok')
        entry(ROOT+'/platform/bundledpythonunix/bin/python3',b'py')
        if include_file:
            entry(ROOT+'/tests/expired/ca/fixture.pem',b'cert')
        entry(ROOT+'/tests/valid/ca',typ=link_type,target=link_to)
        if escape: entry(ROOT+'/../../escape.txt',b'NO')
    return tmp,p

class Suite(unittest.TestCase):
    def test_approved_implicit_parent(self):
        tmp,p=tar_with()
        with tmp,tarfile.open(p,'r:gz') as tf:
            got=s1r.inspect_archive(tf,expected_count=5,expected_implicit={ROOT+'/tests/valid/ca':ROOT+'/tests/expired/ca'})
            self.assertEqual(got['implicit_dir_links'],1)
    def test_off_tree_symlink(self):
        tmp,p=tar_with(link_to='../../../../etc/passwd')
        with tmp,tarfile.open(p,'r:gz') as tf:
            with self.assertRaises(s1r.Halt):s1r.inspect_archive(tf,expected_count=5,expected_implicit={ROOT+'/tests/valid/ca':ROOT+'/tests/expired/ca'})
    def test_target_missing(self):
        tmp,p=tar_with(include_file=False)
        with tmp,tarfile.open(p,'r:gz') as tf:
            with self.assertRaises(s1r.Halt):s1r.inspect_archive(tf,expected_count=4,expected_implicit={ROOT+'/tests/valid/ca':ROOT+'/tests/expired/ca'})
    def test_unapproved_implicit_link(self):
        tmp,p=tar_with()
        with tmp,tarfile.open(p,'r:gz') as tf:
            with self.assertRaises(s1r.Halt):s1r.inspect_archive(tf,expected_count=5,expected_implicit={})
    def test_parent_path_traversal(self):
        tmp,p=tar_with(escape=True)
        with tmp,tarfile.open(p,'r:gz') as tf:
            with self.assertRaises(s1r.Halt):s1r.inspect_archive(tf,expected_count=6,expected_implicit={})
    def test_no_argument_does_not_attempt(self):
        r=subprocess.run([sys.executable,'-B',str(SOURCE)],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)
        self.assertIn('STOP_FLAG_REQUIRED',r.stdout)

if __name__=='__main__':unittest.main(verbosity=2)
