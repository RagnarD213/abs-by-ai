#!/usr/bin/env python3
"""The watch scan's own fixture: a broken scanner must not be able to make the corpus green.

No corpus file carries a frozen run, a black frame or a naked splice ON PURPOSE, so the scan half of
the watch pass is proven here on two clips it builds itself:

  * SYNTHETIC -- a textured static background with one moving subject block, drawn frame by frame,
    encoded once clean and once with exactly three defects injected: ten duplicated frames (a
    frozen run), one black frame, and one same-scene jump (the subject displaced 40 px between two
    consecutive frames). A scene cut (background palette changes) and a push (a 10 % scale step of
    the whole frame) are ALSO injected and must NOT read as naked splices.
  * REAL FOOTAGE -- the corpus excerpt `qc_corpus/excerpts/website-rev4.mp4` (approved, regenerable
    with `run.py --extract`) with the same three defects cut in with ffmpeg. If the excerpt is not on
    disk the test FAILS and says so: a check that did not run is not a pass.

Run by `qc_corpus/run.py` as step 0b, and by `python3 -m unittest discover -s _shared/deliver/tests`.
"""
import os
import subprocess
import sys
import tempfile
import unittest

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, ROOT)

from _shared.deliver import common as C      # noqa: E402
from _shared.deliver import watch as W       # noqa: E402

EXCERPT = os.path.join(ROOT, "_shared", "qc_corpus", "excerpts", "website-rev4.mp4")
FPS = 30
W_, H_ = 640, 360


def _bg(rng):
    """A textured, static background (so a still block reads as still and a moved one as moved)."""
    y, x = np.mgrid[0:H_, 0:W_]
    base = (90 + 40 * np.sin(x / 23.0) + 30 * np.cos(y / 17.0)).astype(np.float32)
    noise = rng.normal(0, 6, (H_, W_)).astype(np.float32)
    g = np.clip(base + noise, 0, 255)
    return np.stack([g * 0.9, g, g * 1.1], axis=2).clip(0, 255).astype(np.uint8)


_NOISE = np.random.default_rng(11)


def _frame(bg, subj_x, subj_y, shade=(200, 170, 140)):
    """One frame: the subject block on the background, plus SENSOR NOISE. Real footage never
    repeats a frame exactly, so without per-frame noise the sway's integer positions would hold
    still for a few frames at each turn and read as a frozen run (that is a fixture artifact,
    not a finding). A duplicated frame stays byte-identical and still reads as frozen."""
    f = bg.astype(np.int16)
    f[subj_y:subj_y + 120, subj_x:subj_x + 80] = shade
    f[subj_y + 20:subj_y + 40, subj_x + 15:subj_x + 65] = (40, 30, 30)       # a "face" band
    f = f + _NOISE.integers(-3, 4, f.shape, dtype=np.int16)
    return np.clip(f, 0, 255).astype(np.uint8)


def _encode(frames, path):
    # ⚠ lossless (-qp 0). The synthetic frames carry heavy per-pixel noise that a lossy encode
    # cannot reproduce, so a lossy encoder keeps REFINING byte-identical input frames against its
    # imperfect reference and the decoded duplicates stop being identical -- the frozen run
    # vanished at crf 16 (2026-09-16). Real footage's noise is already codec-shaped and does not
    # do this; the real-footage fixture below encodes lossy on purpose.
    p = subprocess.Popen([C.FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W_}x{H_}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                          "-preset", "veryfast", "-qp", "0", "-pix_fmt", "yuv420p", path],
                         stdin=subprocess.PIPE)
    for f in frames:
        p.stdin.write(np.ascontiguousarray(f).tobytes())
    p.stdin.close()
    p.wait()


def _synthetic(with_defects):
    rng = np.random.default_rng(7)
    bg = _bg(rng)
    frames = []
    n = 12 * FPS
    sx, sy = 260, 110
    for i in range(n):
        # a gentle sway, one pixel per few frames, like a person talking
        x = sx + int(6 * np.sin(i / 11.0))
        y = sy + int(3 * np.cos(i / 13.0))
        frames.append(_frame(bg, x, y))
    if not with_defects:
        return frames
    # 1. a frozen run: frames 60..69 are frame 60 repeated
    for i in range(61, 70):
        frames[i] = frames[60]
    # 2. a black frame at 4.0 s
    frames[120] = np.zeros_like(frames[120])
    # 3. a naked splice at 6.0 s: the subject jumps 40 px between two consecutive frames and stays
    for i in range(180, n):
        x = sx + 40 + int(6 * np.sin(i / 11.0))
        y = sy + int(3 * np.cos(i / 13.0))
        frames[i] = _frame(bg, x, y)
    # 4. a SCENE CUT at 8.0 s: a different background palette -- covered, must not count
    bg2 = (_bg(np.random.default_rng(3)).astype(np.float32) * np.array([1.3, 0.7, 0.6])).clip(0, 255).astype(np.uint8)
    for i in range(240, n):
        x = sx + 40 + int(6 * np.sin(i / 11.0))
        y = sy + int(3 * np.cos(i / 13.0))
        frames[i] = _frame(bg2, x, y)
    # 5. a PUSH at 10.0 s: the whole frame scaled 10 % about its centre -- a deliberate reframe
    from PIL import Image
    for i in range(300, n):
        im = Image.fromarray(frames[i]).resize((int(W_ * 1.10), int(H_ * 1.10)), Image.BILINEAR)
        a = np.asarray(im)
        oy, ox = (a.shape[0] - H_) // 2, (a.shape[1] - W_) // 2
        frames[i] = np.ascontiguousarray(a[oy:oy + H_, ox:ox + W_])
    return frames


class WatchScanSynthetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.clean = os.path.join(cls.tmp.name, "clean.mp4")
        cls.bad = os.path.join(cls.tmp.name, "defects.mp4")
        _encode(_synthetic(False), cls.clean)
        _encode(_synthetic(True), cls.bad)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def _run(self, path):
        pr = C.probe(path)
        sc = W.scan(path, pr["fps"], pr["width"], pr["height"])
        rep = W.analyse(sc, [], [])
        naked, cands = W.naked_splices(path, sc, [], pr["fps"])
        return sc, rep, naked, cands

    def test_clean_clip_reports_nothing(self):
        sc, rep, naked, cands = self._run(self.clean)
        self.assertEqual(rep["frozen"], [], rep["frozen"])
        self.assertEqual(rep["black"], [], rep["black"])
        self.assertEqual(naked, [], naked)

    def test_defects_are_found_and_only_the_defects(self):
        sc, rep, naked, cands = self._run(self.bad)
        # the frozen run: starts at frame 61 (the first duplicate), ten frames
        self.assertTrue(any(abs(f["t"] - 61 / FPS) < 0.05 and 0.25 <= f["seconds"] <= 0.40
                            for f in rep["frozen"]), rep["frozen"])
        # the one black frame at 4.0 s, and only that one
        self.assertEqual(len(rep["black"]), 1, rep["black"])
        self.assertAlmostEqual(rep["black"][0], 120 / FPS, delta=0.02)
        # the naked splice at 6.0 s ...
        ts = [c["t"] for c in naked]
        self.assertTrue(any(abs(t - 180 / FPS) < 0.05 for t in ts), (ts, cands))
        # ... and NOT the scene cut at 8.0 s, NOT the push at 10.0 s
        self.assertFalse(any(abs(t - 240 / FPS) < 0.10 for t in ts), ("scene cut counted", ts))
        self.assertFalse(any(abs(t - 300 / FPS) < 0.10 for t in ts), ("push counted", ts))
        self.assertEqual(len(naked), 1, naked)

    def test_grab_is_frame_exact(self):
        pr = C.probe(self.bad)
        sc = W.scan(self.bad, pr["fps"], pr["width"], pr["height"])
        sw, sh = sc["grid"][:2]
        g = W.grab(self.bad, 118, 5, pr["fps"], sw, sh, "rgb24")
        self.assertEqual(len(g), 5)
        lum = [float((0.299 * f[:, :, 0] + 0.587 * f[:, :, 1] + 0.114 * f[:, :, 2]).mean()) for f in g]
        # frame 120 is the black one: index 2 of the grab
        self.assertLess(lum[2], 3.0, lum)
        self.assertGreater(lum[1], 40.0, lum)
        self.assertGreater(lum[3], 40.0, lum)


class WatchScanRealFootage(unittest.TestCase):
    """The same three defects cut into 12 s of approved real footage (website rev 4)."""

    def test_real_footage_excerpt_with_injected_defects(self):
        self.assertTrue(os.path.exists(EXCERPT),
                        f"corpus excerpt not on disk: {EXCERPT} -- run `qc_corpus/run.py --extract`. "
                        f"A check that did not run is a FAILURE, not a pass.")
        with tempfile.TemporaryDirectory() as tmp:
            pr = C.probe(EXCERPT)
            fps, w, h = pr["fps"], pr["width"], pr["height"]
            # decode 12 s at half size (the excerpt is 1080p; the defects are injected in RGB)
            hw, hh = w // 2, h // 2
            frames = [f.copy() for k, f in W.stream_frames(EXCERPT, hw, hh, "rgb24") if k < int(12 * fps)]
            self.assertGreater(len(frames), 300)
            n = len(frames)
            for i in range(61, 70):
                frames[i] = frames[60]
            frames[120] = np.zeros_like(frames[120])
            # the naked splice: from 6.0 s on, the SUBJECT band (the central 40 % of columns, where
            # Dan sits in rev 4) is displaced 30 px; the background either side does not move. A
            # whole-frame shift would be a pan, which the instrument rightly refuses to call a jump.
            c0, c1 = int(hw * 0.30), int(hw * 0.70)
            for i in range(180, n):
                f = frames[i].copy()
                f[:, c0:c1] = np.roll(frames[i][:, c0:c1], 30, axis=1)
                frames[i] = np.ascontiguousarray(f)
            out = os.path.join(tmp, "rev4_defects.mp4")
            p = subprocess.Popen([C.FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                  "-s", f"{hw}x{hh}", "-r", pr["fps_str"], "-i", "-", "-c:v", "libx264",
                                  "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", out],
                                 stdin=subprocess.PIPE)
            for f in frames:
                p.stdin.write(f.tobytes())
            p.stdin.close()
            p.wait()
            pr2 = C.probe(out)
            sc = W.scan(out, pr2["fps"], pr2["width"], pr2["height"])
            rep = W.analyse(sc, [], [])
            naked, cands = W.naked_splices(out, sc, [], pr2["fps"])
            self.assertTrue(any(abs(f["t"] - 61 / fps) < 0.05 for f in rep["frozen"]), rep["frozen"])
            self.assertEqual(len(rep["black"]), 1, rep["black"])
            self.assertTrue(any(abs(c["t"] - 180 / fps) < 0.05 for c in naked), (naked, cands))


if __name__ == "__main__":
    unittest.main()
