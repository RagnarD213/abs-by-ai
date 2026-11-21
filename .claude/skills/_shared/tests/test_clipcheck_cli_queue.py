"""CLI scheduling checks with isolated, deliberately synthetic metadata fixtures."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "framecheck/clipcheck.py"
sys.path.insert(0, str(SCRIPT.parent))
import clipcheck


class AdmissionReached(Exception):
    pass


class MetadataSchedulingTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="clipcheck-cli-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.clip = self.root / "synthetic-fixture.mp4"
        self.clip.write_bytes(b"NOT A VIDEO: isolated metadata dispatch fixture")
        self.stamp = Path(str(self.clip) + ".clipcheck.json")
        self.stamp.write_text(json.dumps({"clip_version": clipcheck.CLIP_VERSION,
                              "clip_sha256": hashlib.sha256(self.clip.read_bytes()).hexdigest(),
                              "verdict": "PASS", "rows": []}))
        self.report = self.root / "synthetic-review.md"
        self.report.write_text("Synthetic metadata test only.\nVERDICT: PASS\n")
        self.admissions = []
        fake = types.ModuleType("renderq")

        @contextlib.contextmanager
        def slot(*args, **kwargs):
            self.admissions.append((args, kwargs))
            raise AdmissionReached("measurement reached normal admission")
            yield

        fake.slot = slot
        fake.pool_for_media = lambda *args, **kwargs: "quick"
        self.fake_queue = fake

    def cli(self, *args):
        with patch.object(sys, "argv", [str(SCRIPT), str(self.clip), *args]), \
             patch.dict(sys.modules, {"renderq": self.fake_queue}), \
             contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                runpy.run_path(str(SCRIPT), run_name="__main__")
        return result.exception.code

    def test_record_and_verify_need_no_media_admission(self):
        self.assertEqual(self.cli("--review", str(self.report)), 0)
        self.assertEqual(self.cli("--verify"), 0)
        self.assertEqual(self.admissions, [])
        self.assertEqual(json.loads(self.stamp.read_text())["review"]["verdict"], "PASS")

    def test_changed_file_still_refuses_verification(self):
        self.assertEqual(self.cli("--review", str(self.report)), 0)
        self.clip.write_bytes(b"changed synthetic fixture")
        self.assertIn("changed", str(self.cli("--verify")))
        self.assertEqual(self.admissions, [])

    def test_failed_review_still_blocks_verification(self):
        self.report.write_text("Synthetic metadata test only.\nVERDICT: FAIL\n")
        self.assertEqual(self.cli("--review", str(self.report)), 1)
        self.assertIn("FAIL", str(self.cli("--verify")))
        self.assertEqual(self.admissions, [])

    def test_measurement_still_requires_normal_admission(self):
        with self.assertRaises(AdmissionReached):
            self.cli("--spec", str(self.root / "unused-spec.json"))
        self.assertEqual(len(self.admissions), 1)


if __name__ == "__main__":
    unittest.main()
