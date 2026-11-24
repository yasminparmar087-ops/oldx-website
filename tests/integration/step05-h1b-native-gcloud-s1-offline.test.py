import io, os, sys, tarfile, tempfile, unittest, pathlib, importlib.util
src = pathlib.Path(__file__).resolve().parents[2] / 'scripts/step05-h1b-native-linux-gcloud-s1-once-20261125.py'
spec = importlib.util.spec_from_file_location('s1', src)
s1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s1)

def html_for(release='594.0.1', digest=s1.SHA256, target=s1.ARCHIVE_URL):
  row=f'<tr><td>Linux 64-bit (x86_64)</td><td><a href="{target}">{s1.FILENAME}</a></td><td>94.8 MB</td><td>{digest}</td></tr>'
  return f'<html><h2>Install gcloud CLI version {release}</h2><table>{row}</table></html>'.encode()

def make_tar(path, escape=False, link=False):
  with tarfile.open(path, 'w:gz') as tar:
    root=tarfile.TarInfo('google-cloud-sdk/');root.type=tarfile.DIRTYPE;tar.addfile(root)
    for name in ('google-cloud-sdk/bin/gcloud','google-cloud-sdk/platform/bundledpythonunix/bin/python3'):
      t=tarfile.TarInfo(name);t.size=4;t.mode=0o755;tar.addfile(t,io.BytesIO(b'pass'))
    if escape:
      t=tarfile.TarInfo('google-cloud-sdk/../../oops');t.size=1;tar.addfile(t,io.BytesIO(b'x'))
    if link:
      t=tarfile.TarInfo('google-cloud-sdk/link');t.type=tarfile.SYMTYPE;t.linkname='../../etc/passwd';tar.addfile(t)

class TestS1(unittest.TestCase):
  def test_verified_official_html_and_drift(self):
    s1.validate_official_pages(html_for(),html_for())
    for badinstall,badarchive in [(html_for(release='594.0.2'),html_for()),(html_for(),html_for(digest='0'*64)),(html_for(),html_for(target='https://evil.test/cli.tar.gz'))]:
      with self.assertRaises(s1.Stop): s1.validate_official_pages(badinstall,badarchive)
  def test_archive_safety_positive(self):
    with tempfile.TemporaryDirectory() as tmp:
      p=pathlib.Path(tmp)/'good.tgz';make_tar(p)
      self.assertEqual(s1.inspect_archive(p)['members'],3)
      with tarfile.open(p) as t:t.extractall(tmp,filter='data')
      self.assertTrue((pathlib.Path(tmp)/'google-cloud-sdk/bin/gcloud').exists())
  def test_archive_traversal_denied(self):
    with tempfile.TemporaryDirectory() as tmp:
      p=pathlib.Path(tmp)/'bad.tgz';make_tar(p,escape=True)
      with self.assertRaises(s1.Stop):s1.inspect_archive(p)
  def test_archive_escaping_symlink_denied(self):
    with tempfile.TemporaryDirectory() as tmp:
      p=pathlib.Path(tmp)/'bad.tgz';make_tar(p,link=True)
      with self.assertRaises(s1.Stop):s1.inspect_archive(p)
  def test_gate_does_not_execute_or_write(self):
    import subprocess
    r=subprocess.run([sys.executable, str(src)],capture_output=True,text=True)
    self.assertEqual(r.returncode,2)
    self.assertIn('S1_RESULT=STOP_FLAG_REQUIRED',r.stdout)

if __name__=='__main__': unittest.main(verbosity=2)
