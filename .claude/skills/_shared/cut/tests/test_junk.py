#!/usr/bin/env python3
"""The junk detectors' own fixture. No Whisper, no media: every case is synthetic words + a
synthetic envelope, so the classifier is proven on the shapes it claims to separate before the
corpus asks it about a real file. Run by `qc_corpus/run.py` as step 0c.

Cases, each one a shape Dan has judged:
  * RESTART   "then this if[0.7 s] you[1.6 s] have someone who can help you" (spray-tan 4:00 junk)
  * RESTART   "If you are super pale. now,[0.7 s] if you are super pale" (rev 2's kept stumble)
  * ANAPHORA  "He's trying to avoid cancer. He's trying to avoid skin damage." (fluent, kept)
  * ANAPHORA  a list with a breath: "...better and[0.86 s] I was a little bit leaner" (kept)
  * REINTRO   the same sentence said again after other content (a listen, never a gate fail)
  * PAUSE     0.60 s is breath (low), 0.80 s medium, 1.20 s high; a gap at a piece edge is not a pause
  * SWALLOWED a 0.95 s gap inside "you're" (Dan's "junk footage in the beginning at 0:01")
  * ORPHAN    speech-level energy no word covers, on a synthetic envelope
  * gaps      the envelope's silencedetect equivalent finds exactly the planted gaps
  * timelines ranges -> pieces/joins, words mapped onto the cut's timeline
  * takes     later fluent take wins; a later take with a restart loses; the noisy take loses;
              an abandoned attempt never wins on fluency alone
"""
import os
import sys
import unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, SKILLS)

from _shared.cut import junk as J        # noqa: E402
from _shared.cut import speech as S      # noqa: E402
from _shared.cut import takes as T       # noqa: E402


def W(text, t0=0.0, dur=0.25, gap=0.05, stretch=None):
    """Words at a steady cadence. `stretch` = {index: seconds} lengthens a word (a folded pause)."""
    out, t = [], t0
    for i, w in enumerate(text.split()):
        d = (stretch or {}).get(i, dur)
        out.append(dict(w=" " + w, t=round(t, 3), e=round(t + d, 3), p=0.9))
        t += d + gap
    return out


def kinds(cands):
    return [c["measure"]["kind"] for c in cands if c["cls"] == "REPEAT"]


class Repeats(unittest.TestCase):
    def test_restart_with_stretched_words_is_junk(self):
        # "...someone who can get your back, then this if[0.7] you[1.6] have someone who can help you apply the tan"
        text = ("if you have someone who can help you do it lets say someone who can get your back "
                "then this if you have someone who can help you apply the tan someone who can spray")
        words = W(text, stretch={19: 0.7, 20: 1.6})
        c = J.detect_repeats(words, gaps=[])
        self.assertIn("RESTART", kinds(c), c)
        r = [x for x in c if x["measure"]["kind"] == "RESTART"][0]
        self.assertEqual(r["confidence"], "high")

    def test_restart_after_a_gap_is_junk(self):
        # "If you are super pale. [0.74 s] Now if you are super pale, just keep in mind"
        a = W("you have to get a spray tan if you are super pale.", 0.0)
        b = W("Now if you are super pale just keep in mind that you do not need a tan that much", a[-1]["e"] + 0.74)
        c = J.detect_repeats(a + b, gaps=[(a[-1]["e"], a[-1]["e"] + 0.74)])
        self.assertIn("RESTART", kinds(c), c)

    def test_anaphora_is_kept(self):
        words = W("this is the reason why. He's trying to avoid cancer. He's trying to avoid skin damage. "
                  "And that's the reason why he only goes out at night")
        c = J.detect_repeats(words, gaps=[])
        self.assertTrue(c, "the repeat must be seen")
        self.assertNotIn("RESTART", kinds(c), c)
        self.assertNotIn("REINTRO", kinds(c), c)

    def test_list_with_a_breath_is_kept(self):
        # "the lighting was a little bit better. The camera was a little bit better. The photographer
        #  was a little bit better and[0.86] I was a little bit leaner"
        text = ("the lighting was a little bit better. The camera was a little bit better. The photographer "
                "was a little bit better and I was a little bit leaner for the second shoot.")
        words = W(text, stretch={21: 0.86})                                 # word 21 is "and"
        c = J.detect_repeats(words, gaps=[])
        self.assertNotIn("RESTART", kinds(c), c)

    def test_reintro_is_a_listen_not_a_fail(self):
        text = ("i use an oura ring to track my sleep every night. it tells me my readiness. "
                "the other thing i do is glycine before bed. i use an oura ring to track my sleep every night "
                "and it scores the night")
        c = J.detect_repeats(W(text), gaps=[])
        self.assertIn("REINTRO", kinds(c), c)
        r = [x for x in c if x["measure"]["kind"] == "REINTRO"][0]
        self.assertEqual(r["confidence"], "low")

    def test_no_repeat_no_row(self):
        self.assertEqual(J.detect_repeats(W("one two three four five six seven eight nine ten"), []), [])


class PausesAndWords(unittest.TestCase):
    def test_pause_grades(self):
        gaps = [[1.0, 1.60], [3.0, 3.80], [5.0, 6.20], [9.95, 10.60]]
        pieces = [dict(a=0.0, b=10.0, off=0.0, name="p")]
        c = J.detect_pauses(gaps, pieces, 10.0)
        by = {round(x["t"], 2): x["confidence"] for x in c}
        self.assertEqual(by, {1.0: "low", 3.0: "medium", 5.0: "high"})   # the edge gap is not a pause
        self.assertIn("breathing", [x for x in c if x["t"] == 1.0][0]["action"])

    def test_swallowed_pause_inside_a_word(self):
        # "you're" timed 1046.94-1048.82 swallowing a 0.95 s hesitation
        words = [dict(w=" so", t=1046.5, e=1046.9, p=0.9), dict(w=" you're", t=1046.94, e=1048.82, p=0.9),
                 dict(w=" going", t=1048.85, e=1049.1, p=0.9)]
        gaps = [[1047.1, 1048.05]]
        sw, fixed = J.detect_swallowed(words, gaps)
        self.assertEqual(len(sw), 1)
        self.assertEqual(sw[0]["confidence"], "high")
        self.assertAlmostEqual(fixed[1]["t"], 1048.05, places=2)          # the word's real onset
        self.assertTrue(all(w["e"] > w["t"] for w in fixed))              # no word inverts

    def test_stretched(self):
        words = W("a b c", stretch={1: 0.9})
        s = J.detect_stretched(words)
        self.assertEqual([x["measure"]["word"] for x in s], ["b"])

    def test_head(self):
        pieces = [dict(a=100.0, b=110.0, off=0.0, name="short-A")]
        self.assertEqual(J.detect_head(W("hi there", 0.9), pieces)[0]["cls"], "HEAD")
        self.assertEqual(J.detect_head(W("hi there", 0.2), pieces), [])


class Envelope(unittest.TestCase):
    def _signal(self):
        rng = np.random.default_rng(3)
        sr = S.SR
        n = int(6.0 * sr)
        a = rng.normal(0, 0.0005, n)                                     # room tone ≈ -66 dBFS
        def burst(t0, t1, amp=0.1):
            i0, i1 = int(t0 * sr), int(t1 * sr)
            a[i0:i1] += rng.normal(0, amp, i1 - i0)
        burst(0.5, 1.5); burst(2.7, 3.5); burst(4.0, 5.5)                # speech-level runs
        return a

    def test_gaps_found_where_planted(self):
        db = S.envelope(self._signal())
        gaps = S.gaps_from_envelope(db)
        inner = [(round(g0, 1), round(g1, 1)) for g0, g1 in gaps if 0.4 < g0 and g1 < 5.6]
        self.assertEqual(inner, [(1.5, 2.7), (3.5, 4.0)])

    def test_orphan_run(self):
        db = S.envelope(self._signal())
        words = W("hello there friend", 0.55) + W("and again now", 4.05, dur=0.4)   # nothing covers 2.7-3.5
        o = J.detect_orphans(db, words)
        self.assertEqual(len(o), 1, o)
        self.assertAlmostEqual(o[0]["t"], 2.7, delta=0.15)
        self.assertAlmostEqual(o[0]["end"], 3.5, delta=0.15)


class Timelines(unittest.TestCase):
    def test_pieces_and_joins(self):
        pieces, joins = J.pieces_from_ranges([(10.0, 15.0, "a"), (20.0, 22.5, "b"), (30.0, 31.0)])
        self.assertEqual(joins, [5.0, 7.5])
        self.assertEqual(pieces[2]["name"], "30.00-31.00")

    def test_words_mapped_and_clipped(self):
        pieces, _ = J.pieces_from_ranges([(10.0, 12.0, "a"), (20.0, 21.0, "b")])
        words = [dict(w=" x", t=9.9, e=10.3, p=1), dict(w=" y", t=11.0, e=11.4, p=1),
                 dict(w=" z", t=15.0, e=15.3, p=1), dict(w=" q", t=20.2, e=20.6, p=1)]
        m = J.map_words_to_output(words, pieces)
        self.assertEqual([w["w"].strip() for w in m], ["x", "y", "q"])
        self.assertAlmostEqual(m[0]["t"], 0.0)                            # clipped to the cut
        self.assertAlmostEqual(m[2]["t"], 2.2)                            # 2.0 offset + 0.2

    def test_to_source(self):
        pieces, _ = J.pieces_from_ranges([(10.0, 12.0, "a"), (20.0, 21.0, "b")])
        self.assertEqual(J.to_source(2.5, pieces), (20.5, "b"))


class Takes(unittest.TestCase):
    def _take(self, n, start, text, floor=-48.0, low=-60.0, restarts=(), gaps=(), words=None):
        return dict(take=n, group=1, start=start, end=start + 20.0, text=text, tokens=text.split(),
                    _words=[], measure=dict(seconds=20.0, words=words or len(text.split()),
                                            floor_db=floor, low_floor_db=low, long_gaps=list(gaps),
                                            swallowed=[], stretched=[], restarts=list(restarts),
                                            reintro=[], anaphora=[], ends_sentence=True,
                                            defects=len(restarts) + len(gaps),
                                            fluent=not restarts and not gaps))

    def test_later_fluent_take_wins(self):
        g = [self._take(1, 0, "a b c d e f g h"), self._take(2, 30, "a b c d e f g h")]
        T.mark_noise(g)
        pick, why, _ = T.choose(g)
        self.assertEqual(pick["take"], 2)

    def test_later_take_with_a_restart_loses(self):
        g = [self._take(1, 0, "a b c d e f g h"),
             self._take(2, 30, "a b c d e f g h", restarts=[dict(t=31, second=33, kind="RESTART", gram="a b c d")])]
        T.mark_noise(g)
        pick, why, _ = T.choose(g)
        self.assertEqual(pick["take"], 1)
        self.assertIn("not fluent", why)

    def test_noisy_take_loses(self):
        g = [self._take(1, 0, "a b c d e f g h"), self._take(2, 30, "a b c d e f g h", floor=-40.0),
             self._take(3, 60, "a b c d e f g h")]
        T.mark_noise(g)
        self.assertTrue(g[1]["measure"]["noisy"])
        pick, why, flags = T.choose(g)
        self.assertEqual(pick["take"], 3)

    def test_abandoned_attempt_never_wins(self):
        g = [self._take(1, 0, "a b c d e f g h i j k l"),
             self._take(2, 30, "a b c", words=3, gaps=[])]                 # 25 % of the group's longest
        g[1]["measure"]["fluent"] = True
        T.mark_noise(g)
        pick, why, _ = T.choose(g)
        self.assertEqual(pick["take"], 1)
        self.assertIn("abandoned", why)

    def test_retake_grouping_by_head(self):
        words = W("so the first thing you want to do is", 0.0) + \
                W("so the first thing you want to do is take a picture of yourself and upload it", 8.0)
        takes = T.split_takes(words)
        self.assertEqual(len(takes), 2)
        groups = T.group_retakes(takes)
        self.assertEqual(len(groups), 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
