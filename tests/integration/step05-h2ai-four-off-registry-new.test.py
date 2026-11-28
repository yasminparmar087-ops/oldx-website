#!/usr/bin/env python3
"""NEW H2AI pure local tests only. No Docker, network, cloud or registry mutation."""
from __future__ import annotations
import ast
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

here=Path(__file__).resolve()
if here.name=="test_runner.py":
    runner=here.with_name("runner.py")
else:
    runner=here.parents[2]/"scripts/step05_h2ai_four_off_images_build_push_once_20261128.py"
source=runner.read_text(encoding="utf-8")
ast.parse(source,filename=str(runner))
spec=importlib.util.spec_from_file_location("h2ai_build_once",runner)
h=importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

class NewH2AIOffline(unittest.TestCase):
    def test_01_approved_four_exact_private_refs_no_old_image(self):
        self.assertEqual(set(h.ROLES),{"mediator","gateway","backend","reader"})
        self.assertEqual(set(h.ROLES.values()),
          {"oldx-c2-mediator-h2ah","oldx-c2-gateway-h2ah",
           "oldx-c2-backend-h2ah","oldx-c2-kms-reader"})
        self.assertEqual(len(set(h.IMAGES.values())),4)
        self.assertTrue(all(x.startswith("asia-south1-docker.pkg.dev/oldx-staging/oldx-staging-images/")
                            for x in h.IMAGES.values()))
        self.assertEqual(h.BRANCH,"security-hardening-review")
        self.assertEqual(h.APPROVED_SOURCE,"5d5a621d7a9d9015b5068077b914fef3d6fb9925")
        self.assertTrue(all(len(x)==64 for x in h.OLD_OFF))
    def test_02_registry_index_accepts_one_linux_amd64_child_only(self):
        child="sha256:"+"a"*64
        raw=json.dumps({"schemaVersion":2,"mediaType":"application/vnd.oci.image.index.v1+json",
          "manifests":[{"digest":child,"platform":{"os":"linux","architecture":"amd64"}},
            {"digest":"sha256:"+"b"*64,"platform":{"os":"unknown","architecture":"unknown"}}]})
        with patch.object(h,"command",return_value=raw) as command:
            observed,sha=h.describe_pushed_image("example.example/image:tag",{})
        self.assertEqual(observed,child)
        self.assertEqual(sha,hashlib.sha256(raw.encode()).hexdigest())
        self.assertIn("--raw",command.call_args.args[0])
    def test_03_registry_multiple_child_or_arm_only_stops_no_pretend_pass(self):
        for platform in [
          [{"os":"linux","architecture":"amd64"},{"os":"linux","architecture":"amd64"}],
          [{"os":"linux","architecture":"arm64"}],
          [{"os":"windows","architecture":"amd64"}]]:
            raw=json.dumps({"manifests":[
              {"digest":"sha256:"+str(i+1)*64,"platform":p}
              for i,p in enumerate(platform)]})
            with patch.object(h,"command",return_value=raw):
                with self.assertRaises(h.Stop):
                    h.describe_pushed_image("example.example/image:tag",{})
    def test_04_root_wsl_gate_rejects_other_os_before_cloud_auth(self):
        with patch.object(h.platform,"system",return_value="Windows"),\
             patch.object(h.os,"geteuid",return_value=0):
            with self.assertRaises(h.Stop):
                h.isolated_owner_env()
    def test_05_subprocess_failure_cannot_be_accepted_as_success(self):
        failure=subprocess.CompletedProcess(["noop"],1,b"",b"")
        with patch.object(h.subprocess,"run",return_value=failure):
            with self.assertRaises(h.Stop):
                h.command(["noop"],timeout=1)
    def test_06_only_one_build_push_invocation_and_no_run_kms_firestorm(self):
        self.assertEqual(source.count('["docker","buildx","build"'),1)
        self.assertIn('"--platform","linux/amd64"',source)
        self.assertIn('"--provenance=true","--sbom=true"',source)
        self.assertIn('"--push"',source)
        self.assertIn('O_EXCL',source)
        self.assertIn('H2AI_DO_NOT_REPEAT=TRUE',source)
        self.assertNotIn('gcloud run deploy',source)
        self.assertNotIn(':asymmetricSign',source)
        self.assertNotIn('setIamPolicy',source)

if __name__=="__main__":
    unittest.main(verbosity=2)
