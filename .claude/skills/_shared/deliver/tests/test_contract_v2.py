#!/usr/bin/env python3
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, ROOT)

from _shared.deliver import contract as CT  # noqa: E402
from _shared.deliver import gate as GATE  # noqa: E402
from _shared.deliver.common import Row  # noqa: E402
from _shared.deliver.checks import captions as CAP  # noqa: E402
from _shared.deliver.checks import compliance as COMP  # noqa: E402
from _shared.deliver.checks import framing as FR  # noqa: E402


class ContractV2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.png = os.path.join(self.tmp.name, "state.png")
        im = Image.new("RGBA", (100, 40), (0, 0, 0, 0))
        ImageDraw.Draw(im).rectangle((10, 8, 90, 32), fill=(255, 255, 255, 255))
        im.save(self.png)
        self.sha = CT.file_sha256(self.png)

    def tearDown(self):
        self.tmp.cleanup()

    def plan(self, **extra):
        p = dict(evidence_contract=dict(version=2, video_sha256="video"))
        p.update(extra)
        p["_sha256"] = "video"
        p["_contract_error"] = CT.validate(p, "video")
        return p

    def test_stale_geometry_fails_closed(self):
        p = dict(evidence_contract=dict(version=2, video_sha256="old"),
                 caption_states=[dict(beat=[0, 1], image=self.png, image_sha256=self.sha)])
        self.assertIn("stale", CT.validate(p, "new"))

    def test_missing_and_changed_assets_fail_closed(self):
        p = self.plan(caption_states=[dict(beat=[0, 1], image=self.png,
                                                  image_sha256="0" * 64)])
        self.assertIn("hash changed", CT.validate(p, "video"))

    def test_delivered_pixel_fixture_finds_present_and_missing_state(self):
        import cv2
        asset = os.path.join(self.tmp.name, "pattern.png")
        rgba = np.zeros((10, 18, 4), np.uint8)
        rgba[..., 3] = 255
        rgba[:, :6, :3] = (250, 20, 20)
        rgba[:, 6:12, :3] = (20, 250, 20)
        rgba[:, 12:, :3] = (20, 20, 250)
        Image.fromarray(rgba).save(asset)
        video = os.path.join(self.tmp.name, "fixture.avi")
        writer = cv2.VideoWriter(video, cv2.VideoWriter_fourcc(*"MJPG"), 10, (64, 64))
        for _ in range(8):
            frame = np.zeros((64, 64, 3), np.uint8)
            frame[30:40, 20:38] = rgba[..., :3][..., ::-1]
            writer.write(frame)
        writer.release()
        present = dict(image=asset, pos=[20, 30])
        missing = dict(image=asset, pos=[2, 2])
        cache = {}
        CT.pixel_correlations(video, [("present", present, .3, "image"),
                                      ("missing", missing, .3, "image")], cache)
        self.assertGreater(cache[CT.correlation_key(present, .3)], .95)
        self.assertLess(cache[CT.correlation_key(missing, .3)], .3)

    def test_square_and_vertical_composite_windows(self):
        sq = CT.rect_at([dict(beat=[0, 2], rect=[450, 34, 630, 996], motion="fixed-wide")],
                        1.0, 1080, 1080)
        vert = CT.rect_at([dict(beat=[0, 2], rect=[0, 60, 1080, 1000], motion="tracking")],
                          1.0, 1080, 1920)
        self.assertEqual(sq[:4], (450, 34, 630, 996))
        self.assertEqual(vert[:4], (0, 60, 1080, 1000))
        self.assertIsNone(CT.rect_at([dict(beat=[0, 2], rect=[900, 0, 300, 300])],
                                     1.0, 1080, 1080))

    def test_png_alpha_bbox_and_collision(self):
        state = dict(name="word", word="word", beat=[0, 1], image=self.png,
                     image_sha256=self.sha, pos=[100, 700])
        self.assertEqual(CAP._png_bbox(state), (110, 708, 190, 732))
        scaled = dict(state, rect=[100, 700, 200, 80])
        self.assertEqual(CAP._png_bbox(scaled), (120, 716, 281, 765))
        plan = self.plan(caption_states=[state],
                         graphic_regions=[dict(name="lower", beat=[0, 1], rect=[0, 720, 1080, 200])])
        def fill(_video, jobs, cache):
            for _i, item, t, key in jobs:
                cache[CT.correlation_key(item, t, key)] = .95
            return cache
        with mock.patch.object(CT, "pixel_correlations", side_effect=fill):
            row = CAP._new_graphic_clearance("captions:graphic_clearance",
                                             dict(width=1080, height=1080),
                                             dict(min_px=20, min_state_corr=0.60), plan, "unused.mp4")
        self.assertFalse(row.ok)
        self.assertTrue(row.value["bad"])

    def test_png_clearance_positive_with_no_simultaneous_obstacle(self):
        state = dict(name="word", word="word", beat=[0, 1], image=self.png,
                     image_sha256=self.sha, pos=[100, 700])
        plan = self.plan(caption_states=[state],
                         graphic_regions=[dict(name="card", beat=[1, 2], rect=[0, 0, 1080, 1080])])
        def fill(_video, jobs, cache):
            for _i, item, t, key in jobs:
                cache[CT.correlation_key(item, t, key)] = .95
            return cache
        with mock.patch.object(CT, "pixel_correlations", side_effect=fill):
            row = CAP._new_graphic_clearance("captions:graphic_clearance",
                                             dict(width=1080, height=1080),
                                             dict(min_px=20, min_state_corr=0.60), plan, "unused.mp4")
        self.assertTrue(row.ok)

    def test_continuous_speech_alignment_detects_early_and_late(self):
        states = [dict(word=w, beat=[t, t + .10]) for w, t in (("one", 0), ("two", .2), ("three", .4))]
        speech = [dict(w=w, t=t, e=t + .10) for w, t in (("one", 0), ("two", .2), ("three", .4))]
        pairs, nc, ns = CT.timed_word_pairs(states, speech)
        self.assertEqual((len(pairs), nc, ns), (3, 3, 3))
        self.assertLess(max(abs(x[0]) for x in pairs), 1e-9)
        speech[1]["t"], speech[1]["e"] = .5, .6
        pairs, _, _ = CT.timed_word_pairs(states, speech)
        self.assertGreater(abs(pairs[1][0]), .12)

    def test_sync_row_uses_delivered_audio_evidence(self):
        states = [dict(word=w, beat=[t, t + .1], speech=[t, t + .1], image=self.png,
                       image_sha256=self.sha, pos=[0, 0])
                  for w, t in (("one", 0), ("two", .2), ("three", .4))]
        speech = [dict(w=w, t=t, e=t + .1) for w, t in (("one", 0), ("two", .2), ("three", .4))]
        plan = self.plan(caption_states=states, speech_words=speech,
                         speech_words_evidence=dict(method="delivered_asr", video_sha256="video"))
        cfg = dict(tolerance_ms=120, min_state_corr=.6, min_word_match_frac=.95)
        def fill(_video, jobs, cache):
            for _i, item, t, key in jobs:
                cache[CT.correlation_key(item, t, key)] = .95
            return cache
        with mock.patch.object(CT, "pixel_correlations", side_effect=fill):
            self.assertTrue(CAP.sync("captions:sync", {}, cfg, plan, "unused", ".").ok)
            plan["speech_words"][1].update(t=.5, e=.6)
            self.assertFalse(CAP.sync("captions:sync", {}, cfg, plan, "unused", ".").ok)

    def test_fixed_wide_is_not_a_tracking_error(self):
        samples = [dict(t=x / 4, valid=True, motion="fixed-wide", cx_off_frac=.19,
                        top1080=130, mo=x * .02)
                   for x in range(5)]
        tr = FR.Track(samples, 1080, 1080, 4, len(samples))
        with mock.patch.object(FR, "track_of", return_value=tr), \
             mock.patch.object(FR, "holds", return_value=[samples]):
            row = FR.centering("framing:centering", object(), dict(max_off_frac=.06), {})
        self.assertTrue(row.ok)
        self.assertIn("fixed-wide", row.detail)
        with mock.patch.object(FR, "track_of", return_value=tr), \
             mock.patch.object(FR, "talk_holds", return_value=[samples]):
            row = FR.headroom("framing:headroom", object(),
                              dict(seg_min_px=20, seg_max_px=70, median_max_px=75), {})
        self.assertTrue(row.ok)
        self.assertIn("fixed-wide", row.detail)

    def test_clipped_hair_inside_declared_window_fails(self):
        samples = [dict(t=x / 4, valid=True, top1080=5, edge_m=.5)
                   for x in range(3)]
        tr = FR.Track(samples, 1080, 1080, 4, len(samples))
        with mock.patch.object(FR, "track_of", return_value=tr):
            row = FR.hair_top("framing:hair_top", object(),
                              dict(min_px=20, edge_frac=.2), {})
        self.assertFalse(row.ok)
        self.assertTrue(row.value["cut"])
        self.assertTrue(row.value["edge"])

    def test_label_track_reports_missing_wrong_and_partial_separately(self):
        tracks = [dict(name="ai", kind="ai", beat=[0, 1], image=self.png,
                       image_sha256=self.sha, wrong_image=self.png,
                       wrong_image_sha256=self.sha, pos=[0, 0]),
                  dict(name="transition", kind="ai", beat=[1, 1.1], image=self.png,
                       image_sha256=self.sha, pos=[0, 0], visibility="partial")]
        p = self.plan(label_tracks=tracks,
                      label_clearance=dict(sha256="video", obstructions=[], checked=3))
        def fill(_video, jobs, cache):
            for _i, item, t, key in jobs:
                cache[CT.correlation_key(item, t, key)] = .9
            return cache
        with mock.patch.object(CT, "pixel_correlations", side_effect=fill):
            row = COMP._tracked_labels("compliance:labels",
                                       dict(min_track_corr=.6, wrong_margin=.03, max_search_px=4,
                                            clearance_px=8),
                                       p, "unused.mp4")
        self.assertFalse(row.ok)
        self.assertEqual(len(row.value["wrong"]), 3)
        self.assertEqual(len(row.value["partial"]), 1)

    def test_label_track_fails_body_obstruction(self):
        track = dict(name="real", kind="real", beat=[0, 1], image=self.png,
                     image_sha256=self.sha, pos=[0, 0], sample_times=[.5])
        p = self.plan(label_tracks=[track])
        def fill(_video, jobs, cache):
            for _i, item, t, key in jobs:
                cache[CT.correlation_key(item, t, key)] = .9
            return cache
        with mock.patch.object(CT, "pixel_correlations", side_effect=fill), \
             mock.patch.object(COMP, "_measure_label_clearance",
                               return_value=([("real", .5, 42)], 1, None)):
            row = COMP._tracked_labels("compliance:labels",
                                       dict(min_track_corr=.6, wrong_margin=.03, max_search_px=4,
                                            clearance_px=8),
                                       p, "unused.mp4")
        self.assertFalse(row.ok)
        self.assertEqual(row.value["obstructions"], [("real", .5, 42)])

    def test_negative_events_has_four_distinct_outcomes(self):
        base = dict(_sha256="video")
        cfg = dict(min_frames=10)
        def row(findings):
            p = dict(base, negative_events_scan=dict(sha256="video", when="now",
                                                     frames_checked=10, findings=findings))
            return COMP.negative_events("compliance:negative_events", {}, cfg, p, "v", ".")
        self.assertTrue(row([]).ok)
        self.assertFalse(row([dict(disposition="confirmed_violation")]).ok)
        self.assertIsNone(row([dict(disposition="needs_review")]).ok)
        self.assertIsNotNone(row([dict(disposition="needs_review")]).review_reason)
        malformed = row([dict(description="no disposition")])
        self.assertIsNone(malformed.ok)
        self.assertIn("NOT MEASURED", malformed.detail)

    def test_review_and_pending_both_block_total_pass(self):
        self.assertEqual(GATE.verdict([Row.review("policy", "decide")])[0], "FAIL")
        self.assertEqual(GATE.verdict([Row("watch", None, "PENDING -- not implemented")])[0],
                         "FAIL")
        self.assertEqual(GATE.verdict([Row("measured", True, "good")])[0], "PASS")

    def test_legacy_ass_parser_still_works(self):
        path = os.path.join(self.tmp.name, "x.ass")
        with open(path, "w") as f:
            f.write("Dialogue: 0,0:00:01.00,0:00:02.00,Default,,0,0,0,,hello\n")
        self.assertEqual(CAP.read_cues(path), [(1.0, 2.0, "hello")])

    def test_legacy_ass_clearance_path_still_grades_ink(self):
        ass = os.path.join(self.tmp.name, "x.ass")
        mov = os.path.join(self.tmp.name, "graphic.mov")
        with open(ass, "w") as f:
            f.write("[Script Info]\nDialogue: 0,0:00:01.00,0:00:02.00,Default,,0,0,0,,hello\n")
        open(mov, "wb").close()
        plan = dict(captions_ass=ass,
                    graphics=[dict(name="lower", beat=[1, 2], mov=mov)])
        with mock.patch.object(CAP, "_ass_ink_bbox", return_value=(100, 700, 500, 760)), \
             mock.patch.object(CAP, "_alpha_bbox", return_value=(0, 750, 1080, 900)):
            row = CAP.graphic_clearance("captions:graphic_clearance",
                                        dict(width=1080, height=1080), dict(min_px=20),
                                        plan, "unused.mp4", self.tmp.name)
        self.assertFalse(row.ok)
        self.assertEqual(row.value["tightest"], -10)


if __name__ == "__main__":
    unittest.main()
