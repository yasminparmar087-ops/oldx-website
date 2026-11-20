import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

script = Path(__file__).resolve().parents[2] / "scripts" / "step04-npmfree-c1-single-push-a1.py"
spec = importlib.util.spec_from_file_location("c1single", script)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

def image():
    return [{"Id": c.SOURCE_ID, "RepoTags": [c.SOURCE],
             "Os": "linux", "Architecture": "amd64",
             "Size": 316232711,
             "Config": {"User": "appuser", "Entrypoint": ["/usr/bin/node"],
                        "Cmd": ["functions/staging-marketplace/product-read-server.mjs"]}}]

def repo(state="SCANNING_DISABLED"):
    return {"name": f"projects/{c.PROJECT}/locations/{c.LOCATION}/repositories/{c.REPOSITORY}",
            "format": "DOCKER", "mode": "STANDARD_REPOSITORY",
            "vulnerabilityScanningConfig": {"enablementState": state}}

class TestOnePush(unittest.TestCase):
    def test_local_pin_valid_and_rejects_mismatched_source_or_remote_context(self):
        value=c.review_local(image(), "default", "unix:///var/run/docker.sock", {})
        self.assertEqual(value, 316232711)
        for bad in ("sha256:" + "f"*64, "nondigest"):
            v=image();v[0]["Id"]=bad
            with self.assertRaises(c.Stop): c.review_local(v,"default","unix:///var/run/docker.sock",{})
        with self.assertRaises(c.Stop):
            c.review_local(image(), "remote", "tcp://untrusted:2376", {})

    def test_prewrite_repo_requires_scanning_disabled_and_target_absent(self):
        c.validate_repo(repo(), None, "(unset)")
        for broken,package,impersonation in [
            (repo("SCANNING_ACTIVE"), None, "(unset)"),
            (repo(), "exists", "(unset)"),
            (repo(), None, "unsafe@example.com"),
        ]:
            with self.assertRaises(c.Stop): c.validate_repo(broken,package,impersonation)

    def test_wrong_repository_and_missing_scanner_rejected(self):
        v=repo();v["name"]="projects/other/locations/asia-south1/repositories/no"
        with self.assertRaises(c.Stop): c.validate_repo(v,None,"(unset)")
        v=repo();v.pop("vulnerabilityScanningConfig")
        with self.assertRaises(c.Stop): c.validate_repo(v,None,"(unset)")

    def test_remote_digest_validates_frozen_config_and_layers(self):
        descriptor={"digest":"sha256:"+"a"*64,"size":512}
        payload={"schemaVersion":2, "config":{"digest":c.SOURCE_ID}, "layers":[descriptor]}
        self.assertEqual(c.inspect_remote(payload,"sha256:"+"b"*64),1)
        payload["config"]["digest"]="sha256:"+"c"*64
        with self.assertRaises(c.Stop): c.inspect_remote(payload,"sha256:"+"b"*64)
        payload["config"]["digest"]=c.SOURCE_ID
        payload["manifests"]=[descriptor]
        with self.assertRaises(c.Stop): c.inspect_remote(payload,"sha256:"+"b"*64)

    def test_journal_created_once_and_prevents_reexecution(self):
        with tempfile.TemporaryDirectory() as tmp:
            new=Path(tmp)/"c1.json"
            with patch.object(c, "JOURNAL", new):
                c.start_journal()
                self.assertEqual(json.loads(new.read_text())["stage"], "ONE_PUSH_STARTED_DO_NOT_RETRY")
                with self.assertRaises(c.Stop): c.start_journal()
                c.update_journal("ONE_PUSH_REMOTE_MANIFEST_VERIFIED", "sha256:"+"a"*64)
                self.assertEqual(json.loads(new.read_text())["registry_manifest_digest"],
                                 "sha256:"+"a"*64)

    def test_source_has_no_build_scan_cloud_run_or_iam_mutations(self):
        s=script.read_text()
        for text in ('"build"', '"buildx"', '"grype"', '"deploy"', '"set-iam-policy"', '"services", "enable"'):
            self.assertNotIn(text,s)
        self.assertIn('"push", TARGET',s)
        self.assertIn('gcloud("artifacts", "packages", "describe"',s)
        self.assertIn('TemporaryDirectory',s)

if __name__ == "__main__":
    unittest.main()
