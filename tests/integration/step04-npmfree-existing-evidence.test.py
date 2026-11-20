import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[2] / "scripts" / "step04-npmfree-existing-evidence-a1.py"
spec = importlib.util.spec_from_file_location("oldx_local_image_check", PATH)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def fake(root):
    severe = [{"vulnerability": {"severity": severity, "id": identifier},
               "artifact": {"name": pkg, "version": version}}
              for identifier, (severity, pkg, version) in m.SEVERE.items()]
    matches = severe + [
        {"vulnerability": {"severity": "MEDIUM", "id": "TEST-MED-" + str(i)},
         "artifact": {"name": "test", "version": "0"}} for i in range(12)]
    matches += [
        {"vulnerability": {"severity": "LOW", "id": "TEST-LOW-" + str(i)},
         "artifact": {"name": "test", "version": "0"}} for i in range(2)]
    report = json.dumps({"source": {"type": "image"}, "matches": matches},
                        sort_keys=True).encode()
    (root / "new-image-grype-full.json").write_bytes(report)
    digest = hashlib.sha256(report).hexdigest()
    summary = {
        "source_sha": m.SOURCE,
        "base_index": m.BASE_INDEX,
        "base_amd64_child": m.BASE_AMD64,
        "scanner_db_sha256": m.SCANNER_DB,
        "planned_image": m.IMAGE,
        "stage": "COMPLETE_REVIEW_REQUIRED",
        "outcome": "DONE_NOT_SECURITY_CLEARANCE",
        "execution": "one_new_image_only",
        "image_id": "sha256:" + "a" * 64,
        "runtime": {"uid": 1000, "node": "24.12.0", "npm_path_absent": True,
                    "sharp": "PASS", "firebase_admin_imports": "PASS",
                    "health_200": "PASS", "default_off_503": "PASS"},
        "new_image_scan": {
            "conclusion": "REVIEW_REQUIRED_NOT_G2_PASS",
            "db_sha256": m.SCANNER_DB,
            "full_report_sha256": digest,
            "full_report_local_only": str(root / "new-image-grype-full.json"),
            "bundled_undici_high_remaining": [],
            "severity_counts": dict(m.COUNTS),
            "match_count": 20,
            "severe_ids": sorted(m.SEVERE),
        },
    }
    (root / "summary.json").write_text(json.dumps(summary, sort_keys=True))
    return summary

class TestExistingLocalEvidence(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.summary = fake(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def write(self):
        (self.root / "summary.json").write_text(json.dumps(self.summary, sort_keys=True))

    def stop(self, label):
        with self.assertRaises(m.Stop, msg=label):
            m.verify(self.root)

    def test_exact_frozen_snapshot_integrity_pass_not_provenance(self):
        proof = m.verify(self.root)
        self.assertEqual(proof["source_sha"], m.SOURCE)
        self.assertEqual(proof["image_id"], self.summary["image_id"])
        self.assertEqual(len(proof["report_sha256"]), 64)

    def test_tampered_report_sha_rejected(self):
        path = self.root / "new-image-grype-full.json"
        path.write_bytes(path.read_bytes() + b" ")
        self.stop("scan altered after journal")

    def test_wrong_source_and_image_rejected(self):
        for key, replacement in (("source_sha", "f" * 40),
                                 ("planned_image", "oldx-other"),
                                 ("image_id", "not-a-digest")):
            previous = self.summary[key]
            self.summary[key] = replacement
            self.write()
            self.stop(key)
            self.summary[key] = previous
        self.write()

    def test_missing_or_incomplete_journal_rejected(self):
        self.summary["stage"] = "STOP"
        self.write()
        self.stop("incomplete")
        (self.root / "summary.json").unlink()
        self.stop("missing")

    def test_forged_report_in_sync_but_different_severe_match_rejected(self):
        path = self.root / "new-image-grype-full.json"
        report = json.loads(path.read_bytes())
        report["matches"][0]["vulnerability"]["id"] = "CVE-OTHER"
        raw = json.dumps(report, sort_keys=True).encode()
        path.write_bytes(raw)
        self.summary["new_image_scan"]["full_report_sha256"] = hashlib.sha256(raw).hexdigest()
        self.write()
        self.stop("new hashes but wrong severe result")

    def test_runtime_and_scan_receipt_drift_rejected(self):
        self.summary["runtime"]["npm_path_absent"] = False
        self.write()
        self.stop("npm")
        self.summary["runtime"]["npm_path_absent"] = True
        self.summary["new_image_scan"]["bundled_undici_high_remaining"] = ["GHSA-qrxm-fqhp-jwvm"]
        self.write()
        self.stop("undici")

    def test_symlink_summary_refused(self):
        original = self.root / "summary.json"
        target = self.root / "summary-backup.json"
        original.rename(target)
        original.symlink_to(target)
        self.stop("symlink")

if __name__ == "__main__":
    unittest.main()
