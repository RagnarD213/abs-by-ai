#!/usr/bin/env python3
"""Junk-footage rows, measured on the DELIVERED file's own audio.

Both rows are the delivery-time end of `_shared/cut/junk.py` (the pre-render junk report). The
report is where a cut is fixed; these rows are what stops a cut that was not.

  junk:repeated_take   a CONFIRMED restart shipped: a repeated phrase delivered with a measured
                       hesitation, a stretched word that hides extra words, or speech Whisper
                       dropped -- each re-transcribed alone before it counts. The spray-tan
                       longform's rejection ("junk footage and repeated takes were kept in here").
  junk:dead_air        a measured silence inside the speech longer than the format's bound.
                       Dan flagged 1.21 s on the spray-tan rev 0 ("slight pause here, cut this").

Both rows need words. They take the plan's `speech_words` when its evidence is delivered-audio ASR
bound to this file's sha256 (evidence contract v2), and otherwise transcribe the delivered audio
themselves through the chunked runner -- cached by sha256, so a re-gate is free and a re-render
is not. That is deliberate: a NOT MEASURED here would be a row every pipeline could skip.

⚠ Runtime: the first gate run on a new render transcribes it (small model, ~0.2x realtime on
this Mac) and verifies each candidate with medium.en. Budget minutes, not seconds, for a longform.
"""
import os

from .. import common as C
from ..common import Row, unmeasured

SKILLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _cut():
    import sys
    if SKILLS not in sys.path:
        sys.path.insert(0, SKILLS)
    from _shared.cut import junk as J
    from _shared.cut import speech as S
    return J, S


def _words(plan, video, cfg):
    """The delivered file's words: plan speech_words bound to this sha, else our own transcript."""
    J, S = _cut()
    if plan.get("_junk_words") is not None:
        return plan["_junk_words"], plan["_junk_words_src"]
    sw = plan.get("speech_words")
    ev = plan.get("speech_words_evidence") or {}
    if sw and ev.get("method") == "delivered_asr" and ev.get("video_sha256") == plan.get("_sha256"):
        words, src = S.load_words(sw), "plan:speech_words (delivered_asr)"
    else:
        words, src = S.transcribe(video, cfg.get("model", "small"), quiet=True)
    plan["_junk_words"], plan["_junk_words_src"] = words, src
    return words, src


def repeated_take(key, pr, cfg, plan, video, work):
    """junk:repeated_take -- no confirmed restart, hidden restart or dropped take in the delivered audio."""
    if not pr.get("has_audio"):
        return unmeasured(key, "the file has no audio stream")
    J, S = _cut()
    import tempfile
    words, src = _words(plan, video, cfg)
    if not words:
        return unmeasured(key, f"the transcript is empty ({src}) -- nothing was said, or the audio is not speech")
    with tempfile.TemporaryDirectory(prefix="gate-junk-") as tmp:
        wav = S.wav16k(video, os.path.join(tmp, "a.wav"))
        db = S.envelope(S.pcm(wav))
        gaps = S.gaps_from_envelope(db)
        _, fixed = J.detect_swallowed(words, gaps)
        cands = J.detect_stretched(words) + J.detect_repeats(fixed, gaps) + J.detect_orphans(db, fixed)
        J.verify(cands, wav, fixed, cfg.get("verify_model", "medium.en"), quiet=True)
    confirmed = [c for c in cands if c["verified"] == "confirmed" and
                 (c["cls"] != "REPEAT" or c["measure"].get("kind") == "RESTART")]
    listen = [c for c in cands if c["cls"] == "REPEAT" and c["measure"].get("kind") == "REINTRO"]
    where = "; ".join(f"{c['cls']} @ {C.mmss(c['t'])} {c['measure'].get('gram') or c['measure'].get('word') or ''}".strip()
                      for c in confirmed[:5])
    return Row(key, not confirmed,
               f"{len(confirmed)} confirmed restart(s) in {len(words)} words ({src}); "
               f"{sum(1 for c in cands if c['cls'] == 'REPEAT' and c['measure'].get('kind') == 'ANAPHORA')} "
               f"deliberate repeat(s) kept, {len(listen)} fluent re-said phrase(s) for a listen"
               f"{': ' + where if where else ''}",
               dict(confirmed=[dict(cls=c["cls"], t=c["t"], end=c["end"], measure=c["measure"])
                               for c in confirmed[:20]],
                    listen=[dict(t=c["t"], gram=c["measure"].get("gram")) for c in listen[:20]],
                    candidates=len(cands), words=len(words), words_source=src))


def dead_air(key, pr, cfg, plan, video, work):
    """junk:dead_air -- no measured silence inside the speech longer than the format's bound."""
    if not pr.get("has_audio"):
        return unmeasured(key, "the file has no audio stream")
    J, S = _cut()
    words, src = _words(plan, video, cfg)
    if not words:
        return unmeasured(key, f"the transcript is empty ({src})")
    db = S.envelope(S.pcm(video))
    gaps = S.gaps_from_envelope(db)
    t0, t1 = words[0]["t"], words[-1]["e"]
    inner = [(g0, g1) for g0, g1 in gaps if g0 >= t0 and g1 <= t1]
    bound = cfg["max_gap_s"]
    bad = sorted([(round(g0, 2), round(g1 - g0, 2)) for g0, g1 in inner if g1 - g0 >= bound],
                 key=lambda x: -x[1])
    longest = max((g1 - g0 for g0, g1 in inner), default=0.0)
    return Row(key, not bad,
               f"longest silence inside the speech {longest:.2f} s (max {bound:.2f} s); "
               f"{len(bad)} over the bound{': ' + ', '.join(f'{C.mmss(t)} ({L} s)' for t, L in bad[:6]) if bad else ''}; "
               f"threshold {S.gap_threshold(db):.1f} dBFS against speech at {S.speech_level(db):.1f}",
               dict(longest=round(longest, 2), bound=bound, over=bad[:30], gaps=len(inner)))
