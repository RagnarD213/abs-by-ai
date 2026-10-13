#!/usr/bin/env python3
"""Synthetic proof for audio:click_at_joins; decodes no media.

No corpus file was rejected for a click at a join, so the corpus cannot say whether this row sees one. This
fixture can: speech-like bursts with pauses, joins placed in the pauses, and a hard step cut in where a test
needs a click. It also holds the row to the fault it had on RO-19 round 4 (2026-10-13): the verdict may not
depend on a 2.1 s change in the file's length.
"""
import os, sys, unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, SKILLS)
from _shared.deliver import common as C                      # noqa: E402
from _shared.deliver import formats as F                     # noqa: E402
from _shared.deliver.checks import audio as A                # noqa: E402

SR = 48000
CFG = F.FORMATS["longform"]["rows"]["audio:click_at_joins"]


def film(seconds=120, seed=3):
    """Bursts of band-limited noise (0.6 to 1.6 s, uneven level) with 0.25 to 0.6 s pauses between them.
    Returns (samples, pause centres, burst centres)."""
    rng = np.random.default_rng(seed)
    a = np.zeros(seconds * SR)
    pauses, bursts, t = [], [], 0.5
    while t < seconds - 3:
        n = int(rng.uniform(0.6, 1.6) * SR)
        x = np.convolve(rng.standard_normal(n + 15), np.hanning(16) / 8, mode="valid")[:n]
        x *= rng.uniform(0.05, 0.22) * np.hanning(n) ** 0.3 / (np.abs(x).max() + 1e-9) * 3
        i = int(t * SR)
        a[i:i + n] = np.clip(x, -0.95, 0.95)
        bursts.append(t + n / SR / 2)
        gap = rng.uniform(0.25, 0.6)
        pauses.append(t + n / SR + gap / 2)
        t += n / SR + gap
    return a, pauses, bursts


def run(samples, plan):
    real = C.pcm
    C.pcm = lambda *_a, **_k: samples
    try:
        return A.click_at_joins("audio:click_at_joins", None, CFG, plan, "fixture.mp4")
    finally:
        C.pcm = real


def click(samples, t, step=0.9):
    """A hard splice: everything from t on is shifted by `step` for 3 ms, the way an unfaded cut lands."""
    out = samples.copy()
    i = int(t * SR)
    out[i:i + 144] += step
    return out


class ClickAtJoins(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a, cls.pauses, cls.bursts = film()
        cls.joins = [round(t, 3) for t in cls.pauses if 6 < t < 114]

    def test_clean_joins_in_pauses_pass(self):
        r = run(self.a, dict(joins=self.joins))
        self.assertIs(r.ok, True, r.detail)
        self.assertEqual(r.value["source"], "joins")

    def test_a_click_at_a_join_fails_and_is_named(self):
        t = self.joins[7]
        r = run(click(self.a, t), dict(joins=self.joins))
        self.assertIs(r.ok, False, r.detail)
        self.assertEqual([b[0] for b in r.value["bad"]], [round(t, 2)])

    def test_clicks_at_every_join_do_not_set_their_own_bar(self):
        a = self.a
        for t in self.joins:
            a = click(a, t)
        r = run(a, dict(joins=self.joins))
        self.assertIs(r.ok, False, r.detail)
        self.assertEqual(len(r.value["bad"]), min(30, len(self.joins)))
        self.assertAlmostEqual(r.value["ceiling"], run(self.a, dict(joins=self.joins)).value["ceiling"], delta=0.02)

    def test_a_shorter_film_gets_the_same_bar(self):
        """RO-19 round 4: 2.1 s came out of the film, the bar fell from 0.4244 to 0.1802, the row flipped."""
        cut0, cut1 = int(60.0 * SR), int(62.1 * SR)
        shorter = np.concatenate([self.a[:cut0], self.a[cut1:]])
        moved = [t for t in self.joins if t < 59.9] + [round(t - 2.1, 3) for t in self.joins if t > 62.2]
        full, short = run(self.a, dict(joins=self.joins)), run(shorter, dict(joins=moved))
        self.assertIs(short.ok, full.ok)
        self.assertLess(abs(short.value["ceiling"] / full.value["ceiling"] - 1), 0.03,
                        f"{full.value['ceiling']} against {short.value['ceiling']}")

    def test_same_file_same_answer(self):
        self.assertEqual(run(self.a, dict(joins=self.joins)).value, run(self.a, dict(joins=self.joins)).value)

    def test_audio_joins_is_the_list_graded_when_declared(self):
        # a picture cut on the loudest instant of the film, over continuous sound, with the audio joined elsewhere
        d = np.abs(np.diff(self.a[6 * SR:114 * SR]))
        loud = round(6 + int(d.argmax()) / SR, 3)
        picture = sorted(self.joins + [loud])
        self.assertIs(run(self.a, dict(joins=picture)).ok, False)
        r = run(self.a, dict(joins=picture, audio_joins=self.joins))
        self.assertIs(r.ok, True, r.detail)
        self.assertEqual(r.value["source"], "audio_joins")
        self.assertEqual(r.value["joins"], len(self.joins))

    def test_a_click_at_an_audio_join_still_fails_when_declared(self):
        t = self.joins[3]
        r = run(click(self.a, t), dict(joins=self.joins + [50.0], audio_joins=self.joins))
        self.assertIs(r.ok, False, r.detail)

    def test_no_joins_is_not_measured(self):
        self.assertIsNone(run(self.a, dict()).ok)
        self.assertIsNone(run(self.a, dict(joins=[], audio_joins=[])).ok)

    def test_the_bound_is_the_recorded_one(self):
        self.assertEqual(CFG, dict(ceiling_mult=1.25, control_quantile=0.9954))


if __name__ == "__main__":
    unittest.main(verbosity=1)
