import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILE = ROOT / "scripts" / "step04-npmfree-c0-local-metadata-a1.py"
spec = importlib.util.spec_from_file_location("oldx_c0_local", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def valid():
    daemon = {"OSType": "linux", "OperatingSystem": "Docker Desktop"}
    image = [{"Id": mod.IMAGE_ID, "RepoTags": [mod.IMAGE],
              "Os": "linux", "Architecture": "amd64", "Size": 170 * 1024 ** 2,
              "Config": {"User": "appuser", "Entrypoint": ["/usr/bin/node"],
                         "Cmd": ["functions/staging-marketplace/product-read-server.mjs"]}}]
    return ["Linux 6.0 Microsoft WSL2", {}, "default", "unix:///var/run/docker.sock", daemon, image]

class TestC0LocalMetadata(unittest.TestCase):
    def test_valid_local_snapshot_reports_size_not_cost(self):
        result = mod.review(*valid())
        self.assertEqual(result["local_bytes"], 170 * 1024 ** 2)
        self.assertEqual(result["local_mib"], 170.0)
        self.assertNotIn("registry_cost", result)

    def test_reject_nonlocal_or_overridden_docker(self):
        for pos, update in [(0, "Linux without WSL"), (1, {"DOCKER_HOST":"tcp://example:2376"}),
                            (2, "remote"), (3, "tcp://127.0.0.1:2376")]:
            args = valid()
            args[pos] = update
            with self.assertRaises(mod.Stop, msg=f"at {pos}"):
                mod.review(*args)

    def test_reject_wrong_daemon_and_platform(self):
        args=valid();args[4]["OSType"]="windows"
        with self.assertRaises(mod.Stop): mod.review(*args)
        args=valid();args[5][0]["Architecture"]="arm64"
        with self.assertRaises(mod.Stop): mod.review(*args)

    def test_reject_wrong_image_id_tag_and_unsafe_runtime(self):
        for key, value in [("Id", "sha256:"+"0"*64), ("RepoTags", ["old-version"]),
                           ("Size", -1), ("Size", 9*1024**3), ("Size", True)]:
            args=valid();args[5][0][key]=value
            with self.assertRaises(mod.Stop, msg=key): mod.review(*args)
        for key, value in [("User", "root"), ("Entrypoint", ["/bin/sh"]),
                           ("Cmd", ["/bin/bash"])]:
            args=valid();args[5][0]["Config"][key]=value
            with self.assertRaises(mod.Stop, msg=key): mod.review(*args)

    def test_readonly_cli_scope(self):
        source=FILE.read_text("utf-8")
        for command in ("docker\", \"build", "docker\", \"push",
                        "docker\", \"run", "docker\", \"tag",
                        "gcloud\",", "grype\",", "curl\","):
            self.assertNotIn(command, source)
        self.assertIn('"docker", "image", "inspect", IMAGE', source)

if __name__ == "__main__":
    unittest.main()
