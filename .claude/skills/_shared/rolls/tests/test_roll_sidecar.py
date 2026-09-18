#!/usr/bin/env python3
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
TOOL = HERE.parent / "roll_sidecar.py"
REPO = TOOL.parents[4]
FFMPEG = REPO / "Media" / "video_edit" / "bin" / "ffmpeg"


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


if __name__ == "__main__":
    unittest.main()
