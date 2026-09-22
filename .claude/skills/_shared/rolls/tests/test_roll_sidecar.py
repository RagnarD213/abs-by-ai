#!/usr/bin/env python3
import json
import io
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
TOOL = HERE.parent / "roll_sidecar.py"
REPO = TOOL.parents[4]
FFMPEG = REPO / "Media" / "video_edit" / "bin" / "ffmpeg"
SPEC = importlib.util.spec_from_file_location("roll_sidecar", TOOL)
ROLL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ROLL)


class GeminiDescriptionRetryTest(unittest.TestCase):
    def test_empty_response_retries_and_records_both_charges(self):
        with tempfile.TemporaryDirectory(prefix="roll-gemini-retry-") as directory:
            contact = Path(directory) / "contact.jpg"
            contact.write_bytes(b"test contact")
            ledger = Path(directory) / "usage.jsonl"
            empty = {"candidates": [], "usageMetadata": {"promptTokenCount": 1000}}
            valid = {"candidates": [{"content": {"parts": [{"text": '{"summary":"camera roll","shots":[]}' }]}}],
                     "usageMetadata": {"promptTokenCount": 1000, "candidatesTokenCount": 100, "thoughtsTokenCount": 50}}
            responses = [io.BytesIO(json.dumps(row).encode("utf-8")) for row in (empty, valid)]
            with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "test-key", "ROLL_USAGE_LEDGER": str(ledger)}), \
                 mock.patch.object(ROLL.urllib.request, "urlopen", side_effect=responses), \
                 mock.patch.object(ROLL.time, "sleep"):
                parsed, usage = ROLL.describe_contact(contact, 5)
            self.assertEqual("camera roll", parsed["summary"])
            self.assertEqual(2, usage["attempts"])
            self.assertEqual(2000, usage["input_tokens"])
            self.assertEqual(50, usage["thinking_tokens"])
            self.assertEqual(0.000725, usage["estimated_actual_usd"])
            rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(2, len(rows))
            self.assertTrue(rows[0]["status"].startswith("invalid-response"))
            self.assertEqual("ok", rows[1]["status"])


    def test_three_malformed_responses_stop_after_bounded_attempts(self):
        with tempfile.TemporaryDirectory(prefix="roll-gemini-retry-") as directory:
            contact = Path(directory) / "contact.jpg"
            contact.write_bytes(b"test contact")
            ledger = Path(directory) / "usage.jsonl"
            malformed = {"candidates": [{"content": {"parts": [{"text": "{"}]}}],
                         "usageMetadata": {"promptTokenCount": 1000}}
            responses = [io.BytesIO(json.dumps(malformed).encode("utf-8")) for _ in range(3)]
            with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "test-key", "ROLL_USAGE_LEDGER": str(ledger)}), \
                 mock.patch.object(ROLL.urllib.request, "urlopen", side_effect=responses), \
                 mock.patch.object(ROLL.time, "sleep"):
                with self.assertRaisesRegex(RuntimeError, "three invalid descriptions"):
                    ROLL.describe_contact(contact, 5)
            self.assertEqual(3, len(ledger.read_text(encoding="utf-8").splitlines()))

    def test_provider_content_block_does_not_retry(self):
        with tempfile.TemporaryDirectory(prefix="roll-gemini-block-") as directory:
            contact = Path(directory) / "contact.jpg"
            contact.write_bytes(b"test contact")
            ledger = Path(directory) / "usage.jsonl"
            blocked = {"promptFeedback": {"blockReason": "PROHIBITED_CONTENT"},
                       "usageMetadata": {"promptTokenCount": 1000}}
            response = io.BytesIO(json.dumps(blocked).encode("utf-8"))
            with mock.patch.dict(os.environ, {"GEMINI_API_KEY": "test-key", "ROLL_USAGE_LEDGER": str(ledger)}), \
                 mock.patch.object(ROLL.urllib.request, "urlopen", return_value=response) as urlopen:
                with self.assertRaisesRegex(RuntimeError, "PROHIBITED_CONTENT"):
                    ROLL.describe_contact(contact, 5)
            self.assertEqual(1, urlopen.call_count)
            row = json.loads(ledger.read_text(encoding="utf-8").strip())
            self.assertEqual("blocked:PROHIBITED_CONTENT", row["status"])


class RollSidecarTest(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="roll-sidecar-test-"))
        self.shoot = self.temp / "Synthetic Shoot"
        self.shoot.mkdir()
        self.clip = self.shoot / "CTEST.MP4"
        self.edit_work = self.temp / "edit-work"
        self.edit_work.mkdir()
        self.mirror = self.temp / "mirror"
        subprocess.run([
            str(FFMPEG), "-nostdin", "-v", "error", "-y",
            "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=10",
            "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=10",
            "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-shortest", str(self.clip),
        ], check=True)
        transcript = {
            "segments": [{
                "start": 0.2,
                "end": 9.6,
                "text": " The synthetic test says dramatic vacuum from the front twice.",
                "words": [
                    {"word": " The", "start": 0.2, "end": 0.6},
                    {"word": " synthetic", "start": 0.6, "end": 1.2},
                    {"word": " test", "start": 1.2, "end": 1.7},
                    {"word": " says", "start": 1.7, "end": 2.2},
                    {"word": " dramatic", "start": 2.2, "end": 3.1},
                    {"word": " vacuum", "start": 3.1, "end": 4.0},
                    {"word": " from", "start": 4.0, "end": 4.5},
                    {"word": " the", "start": 4.5, "end": 4.9},
                    {"word": " front", "start": 4.9, "end": 5.7},
                    {"word": " twice.", "start": 8.8, "end": 9.6},
                ],
            }]
        }
        (self.edit_work / "CTEST.whisper.json").write_text(json.dumps(transcript), encoding="utf-8")
        self.env = os.environ.copy()
        self.env["ROLL_MIRROR_ROOT"] = str(self.mirror)
        self.env["ROLL_EDIT_WORK_ROOT"] = str(self.edit_work)

    def tearDown(self):
        shutil.rmtree(self.temp)

    def run_tool(self, *args, check=True):
        result = subprocess.run(
            [os.environ.get("PYTHON", "python3"), str(TOOL)] + list(args),
            env=self.env,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if check and result.returncode:
            self.fail("tool failed\nstdout:\n{}\nstderr:\n{}".format(result.stdout, result.stderr))
        return result

    def build(self):
        result = self.run_tool("build", str(self.clip), "--no-describe")
        self.assertIn('"harvested": 1', result.stdout)
        sidecar = self.clip.with_name("CTEST.roll.json")
        self.assertTrue(sidecar.exists())
        self.assertTrue(self.clip.with_name("CTEST.roll").joinpath("contact.jpg").exists())
        self.assertFalse(any(self.mirror.rglob("*.jpg")))
        return sidecar

    def test_ten_second_clip_identity_survives_rename(self):
        sidecar = self.build()
        original = json.loads(sidecar.read_text(encoding="utf-8"))["identity"]["content_key"]
        renamed = self.clip.with_name("RENAMED.MP4")
        self.clip.rename(renamed)
        shown = self.run_tool("show", str(renamed))
        self.assertIn(original, shown.stdout)
        self.assertIn("harvested:", shown.stdout)

    def test_locked_fields_survive_force(self):
        sidecar = self.build()
        data = json.loads(sidecar.read_text(encoding="utf-8"))
        data["grade"] = {"value": "human correction", "locked": True}
        rendered = json.dumps(data, indent=2) + "\n"
        sidecar.write_text(rendered, encoding="utf-8")
        mirror_json = next(self.mirror.glob("*/*.roll.json"))
        mirror_json.write_text(rendered, encoding="utf-8")
        self.run_tool("build", str(self.clip), "--no-describe", "--force")
        rebuilt = json.loads(sidecar.read_text(encoding="utf-8"))
        self.assertEqual({"value": "human correction", "locked": True}, rebuilt["grade"])

    def test_find_works_from_mirror_when_source_is_offline(self):
        self.build()
        offline = self.temp / "offline.MP4"
        self.clip.rename(offline)
        found = self.run_tool("find", "dramatic vacuum")
        self.assertIn("CTEST.MP4", found.stdout)
        self.assertIn("drive unplugged", found.stdout)

    def test_find_hides_finished_exports_by_default(self):
        self.build()
        mirror_json = next(self.mirror.glob("*/*.roll.json"))
        data = json.loads(mirror_json.read_text(encoding="utf-8"))
        data["identity"]["current_path"] = str(self.shoot / "EDITED LONGFORM 8-20-26" / "CTEST.MP4")
        mirror_json.write_text(json.dumps(data), encoding="utf-8")
        hidden = self.run_tool("find", "dramatic vacuum", check=False)
        self.assertEqual(1, hidden.returncode)
        self.assertIn("No matches", hidden.stdout)
        shown = self.run_tool("find", "dramatic vacuum", "--include-edited")
        self.assertIn("CTEST.MP4", shown.stdout)


if __name__ == "__main__":
    unittest.main()
