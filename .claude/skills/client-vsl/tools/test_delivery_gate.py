"""Regressions for the client delivery gate. Uses no real client files or paid calls."""
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

import delivery_gate

from delivery_gate import CHECKS, VERSION, blind_review, fingerprint, receipt_path, require_receipt, verify_rows, write_json
from delivery_sync import caption_alignment, check_source_ranges
from review_publish import checked_review, stage_media


class DeliveryGateTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.job = Path(scratch.name)
        self.video = self.job / "review.mp4"
        self.video.write_bytes(b"checked media")
        self.rows = self.job / "rows.json"
        self.captions = self.job / "review.srt"
        self.captions.write_text("1\n00:00:01,000 --> 00:00:02,000\nHere is the line.\n")
        self.words = [("here", 1.05, 1.22), ("is", 1.23, 1.34),
                      ("the", 1.35, 1.49), ("line", 1.50, 1.88)]
        self.row = {"id": "L1", "words": 'On "here is the line", show the label.',
                    "spoken_quote": "here is the line", "fix": "Added the label.", "verdict": "Done", "t": 1.01}
        self.verification = {"result": "PASS", "client_words": self.row["words"], "fix": self.row["fix"],
                             "observed": "Label is readable throughout the line.",
                             "spoken_quote": "Here is the line.", "t": 1.08}
        self.review = {"verifications": {"L1": self.verification}}

    def test_caption_timing_and_missing_words(self):
        self.assertEqual(caption_alignment(self.captions, self.words, 4, 30)["result"], "PASS")
        for change in ([], [(word, t + 0.3, end + 0.3) for word, t, end in self.words],
                       [(word, t + 2, end + 2) for word, t, end in self.words]):
            with self.subTest(words=change):
                self.assertEqual(caption_alignment(self.captions, change, 4, 30)["result"], "FAIL")

    def test_source_map_checks_sources_and_one_frame_drift(self):
        picture = {"source": "camera A", "in_s": 2, "out_s": 5}
        audio = picture.copy()
        segment = {"kind": "speaker", "start_s": 0, "end_s": 3, "source_fps": 30,
                   "picture": picture, "audio": audio}
        data = {"duration_s": 3, "segments": [segment]}
        for result, changes in (("PASS", {"out_s": 5 + 1 / 30}), ("FAIL", {"out_s": 5.04}),
                                ("FAIL", {"out_s": 5, "source": "other VO"})):
            with self.subTest(changes=changes):
                audio.update(changes)
                self.assertEqual(check_source_ranges(data, 3, 30)["result"], result)
        segment["start_s"] = 1
        with self.assertRaisesRegex(ValueError, "gap"):
            check_source_ranges(data, 3, 30)

    def test_rows_require_same_quote_fix_and_exact_transcript_time(self):
        result = verify_rows({"asked": [self.row]}, self.review, self.words, 4)
        self.assertEqual(result["verified"]["L1"]["t"], 1.05)
        for change in ({"t": 2.0}, {"fix": "Said it was finished."}, {"spoken_quote": "another line"}):
            with self.subTest(change=change):
                result = verify_rows({"asked": [{**self.row, **change}]}, self.review, self.words, 4)
                self.assertEqual(result["result"], "FAIL")
        self.assertEqual(verify_rows({"asked": [self.row]}, {}, self.words, 4)["result"], "FAIL")

    def test_blind_review_rejects_silent_partial_or_editor_attestations(self):
        path = self.job / "blind-review.json"
        report = {"sha256": "a" * 64, "reviewer": "Other Reviewer", "reviewer_session": "A1",
                  "reviewed_at": "2026-11-20T16:00:00Z", "method": "Played full export with sound.",
                  "blind": True, "audio": True, "moving_video": True, "whole_film": True,
                  "reviewed_duration_s": 4, "verdict": "PASS", "findings": [],
                  "row_verifications": {"L1": self.verification}}
        for change in ({}, {"audio": False}, {"reviewer": "Editor"}, {"reviewed_duration_s": 2},
                       {"findings": [{"t": 1.1, "result": "FAIL"}]}, {"sha256": "b" * 64}):
            with self.subTest(change=change):
                write_json(path, {**report, **change})
                if change:
                    with self.assertRaises(ValueError):
                        blind_review(path, report["sha256"], "Editor", 4)
                else:
                    self.assertEqual(blind_review(path, report["sha256"], "Editor", 4)["result"], "PASS")

    def passing_receipt_fixture(self):
        data = {"asked": [self.row, {**self.row, "id": "L2", "verdict": "OPEN"}]}
        write_json(self.rows, data)
        evidence = self.job / "sample.json"
        write_json(evidence, {})
        inputs = {name: fingerprint(evidence) for name in ("manifest", "source_map", "blind_review", "transcript", "gemini")}
        inputs.update(rows=fingerprint(self.rows), captions=fingerprint(self.captions))
        checks = {check: {"result": "PASS"} for check in CHECKS}
        checks["rows"] = verify_rows(data, self.review, self.words, 4)
        receipt = {"version": VERSION, "result": "PASS", "sha256": fingerprint(self.video)["sha256"],
                   "job": str(self.job.resolve()), "inputs": inputs, "checks": checks}
        write_json(receipt_path(self.video), receipt)
        return receipt

    def test_consumers_render_verified_rows_and_replace_same_size_wrong_media(self):
        self.passing_receipt_fixture()
        receipt, render_rows = checked_review(self.video, self.captions, self.rows, self.job)
        first, second = render_rows["asked"]
        self.assertEqual((first["verdict"], first["t"]), ("Done", 1.05))
        self.assertEqual((second["verdict"], second["t"], second["fix"]), ("not yet", None, ""))
        out = self.job / "review"
        video_name, _ = stage_media(self.video, self.captions, out, receipt)
        published = out / "media" / video_name
        published.write_bytes(b"X" * self.video.stat().st_size)
        stage_media(self.video, self.captions, out, receipt)
        self.assertEqual(published.read_bytes(), self.video.read_bytes())
        self.video.write_bytes(b"X" * self.video.stat().st_size)
        with self.assertRaisesRegex(ValueError, "video bytes differ"):
            require_receipt(self.video, self.rows, self.job)

    def test_receipt_rejects_changed_rows_and_any_failed_check(self):
        receipt = self.passing_receipt_fixture()
        self.rows.write_text('{"asked":[]}')
        with self.assertRaisesRegex(ValueError, "rows changed"):
            require_receipt(self.video, self.rows)
        receipt["checks"]["gemini"]["result"] = "FAIL"
        write_json(receipt_path(self.video), receipt)
        with self.assertRaisesRegex(ValueError, "required check"):
            require_receipt(self.video, self.rows)

    def test_run_gate_issues_receipt_that_both_consumers_can_reopen(self):
        digest = fingerprint(self.video)["sha256"]
        evidence = delivery_gate.evidence_dir(self.job, digest)
        evidence.mkdir(parents=True)
        source = evidence / "source.json"
        write_json(source, {"kind": "source_ranges", "duration_s": 4,
                            "segments": [{"kind": "cover", "start_s": 0, "end_s": 4, "reason": "Narrated image."}]})
        write_json(evidence / "inputs.json",
                   {"sha256": digest, "editor": "Editor", "captions": str(self.captions),
                    "captions_sha256": fingerprint(self.captions)["sha256"], "source_map": source.name,
                    "source_map_sha256": fingerprint(source)["sha256"]})
        write_json(evidence / "blind-review.json",
                   {"sha256": digest, "reviewer": "Reviewer", "reviewer_session": "A1",
                    "reviewed_at": "2026-11-20T16:00:00Z", "method": "Played the export with sound.",
                    "blind": True, "audio": True, "moving_video": True, "whole_film": True,
                    "reviewed_duration_s": 4, "verdict": "PASS", "findings": [],
                    "row_verifications": {"L1": self.verification}})
        write_json(self.rows, {"asked": [self.row]})
        words = [{"w": word, "t": start, "e": end} for word, start, end in self.words]
        speech = Mock(FP="ffprobe", FF="ffmpeg", transcribe=Mock(return_value=(words, "test transcript")))
        shared = types.ModuleType("_shared")
        cut = types.ModuleType("_shared.cut")
        cut.speech = speech
        with patch.dict(sys.modules, {"_shared": shared, "_shared.cut": cut}), \
                patch.object(delivery_gate, "probe", return_value=(4, 30)), \
                patch.object(delivery_gate, "gemini_review", return_value={"result": "PASS", "parts": []}):
            self.assertEqual(delivery_gate.run_gate(self.video, self.job.resolve(), self.rows), 0)
        self.assertEqual(require_receipt(self.video, self.rows, self.job)[0]["result"], "PASS")
        self.assertEqual(checked_review(self.video, self.captions, self.rows, self.job)[1]["asked"][0]["t"], 1.05)

    def test_ledger_rejects_missing_file_and_failed_receipt(self):
        ledger = Path(__file__).with_name("client_ledger.py")
        write_json(self.job / "CLIENT-LEDGER.json", {"sources": [], "items": [], "sweeps": []})
        command = [sys.executable, str(ledger), "gate", str(self.job), "--stage", "deliver"]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("delivery needs --file", result.stdout)
        self.passing_receipt_fixture()
        receipt_path(self.video).unlink()
        result = subprocess.run(command + ["--file", str(self.video), "--rows", str(self.rows)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Delivery blocked", result.stdout)


if __name__ == "__main__":
    unittest.main()
