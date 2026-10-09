"""Regression checks for delivered website sidecar captions, 2026-10-09."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

P = Path(__file__).resolve().parents[1] / "gate.py"
S = importlib.util.spec_from_file_location("caption_gate", P)
G = importlib.util.module_from_spec(S)
S.loader.exec_module(G)


class CaptionPlanRouting(unittest.TestCase):
    def test_run_reads_plan_before_selecting_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "plan.json"
            plan.write_text(json.dumps({"caption_mode": "srt"}))
            video = Path(tmp) / "candidate.mp4"
            video.write_bytes(b"test")
            probe = {"vdur": 10, "fps": 30, "width": 1920, "height": 1080}
            with patch.object(G.C, "probe", return_value=probe), \
                 patch.object(G.PIC, "Picture"), \
                 patch.object(G.FMT, "config_for", wraps=G.FMT.config_for) as routing:
                _, _, rows = G.run(str(video), "website", str(plan),
                                   only=["captions:card_collision"])
            routing.assert_called_once_with("website", "srt")
            self.assertTrue(rows[0].na_reason)

    def test_sidecar_mode_changes_only_caption_requirements(self):
        original = G.FMT.config_for("website")
        sidecar = G.FMT.config_for("website", "srt")
        caption_keys = {"captions:burned", "captions:sync", "captions:graphic_clearance",
                        "captions:card_collision", "srt:present", "srt:shape"}
        for group in ("rows", "not_applicable"):
            self.assertEqual({k: v for k, v in original[group].items() if k not in caption_keys},
                             {k: v for k, v in sidecar[group].items() if k not in caption_keys})
        self.assertTrue(sidecar["rows"]["srt:present"]["required"])
        self.assertFalse(sidecar["rows"]["captions:burned"]["present"])
        self.assertEqual(set(G.FMT.ALL_ROWS), set(sidecar["rows"]) | set(sidecar["not_applicable"]))

    def test_stamp_records_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            video = Path(tmp) / "candidate.mp4"
            video.write_bytes(b"test")
            pr = {"size": "1920x1080", "fps_str": "30000/1001", "vdur": 10}
            stamp = G.stamp(str(video), "website", [], "PASS", pr, "srt")
            self.assertEqual(json.loads(Path(stamp).read_text())["caption_mode"], "srt")


if __name__ == "__main__":
    unittest.main()
