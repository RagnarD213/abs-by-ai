#!/usr/bin/env python3
"""THE BOUNDS. Every number in this file names the video it was measured on and the date.

⚠ THIS IS THE ONLY PLACE A BOUND MAY LIVE. The seventeen gates this module replaces each carried
their own copy, so a fix landed in one of six pipelines and the other five kept the bug -- which is
exactly what happened on 2026-09-09, when the spray-tan pipeline kept a forked `work/dereverb.py`
and the same-day shared fix never reached it (memory `shared-fix-may-not-reach-the-pipeline`).

⚠ NEVER RAISE A THRESHOLD TO MAKE A BUILD PASS (memory `audio-never-over-strip`). If a corpus entry
fails a bound, that IS the finding. Report it; do not tune it away.

⚠ NEVER "SIMPLIFY" A BOUND WHILE MERGING. Every constant here traces to a file Dan approved or
rejected. Carry the provenance comment with the number or the number becomes a taste call again.

⚠ A ROW THAT IS NEITHER CONFIGURED NOR DECLARED NOT-APPLICABLE FAILS AS UNCONFIGURED. That is
deliberate: adding a row forces every format to make a decision about it, in writing, here, where a
reader can audit it. Silence is what let `full-bleed/qc.js` ship with no caption-sync and no
loudness check at all.

------------------------------------------------------------------------------------------------
THE CALIBRATION TABLE -- measured 2026-09-11 by re-running the picture rows over the whole regression
corpus. Decode settings are fixed in checks/picture.py; change them and this table is void.

  file                              verdict     cov   static  chg/min  uncov/min
  FINAL_abwheel (the 8/20 cut)      REJECTED     9%    79.2s      2.1       2.2
  FINAL_spraytan_PRE_REBUILD        REJECTED    28%    22.7s     10.8       3.2
  website rev 4                     approved    37%    12.2s     12.0       1.0
  website rev 5                     approved    32%    13.5s     11.7       0.8
  website rev 6 (his final)         approved    31%    10.8s     12.5       1.8
  muhammad ad 1 16x9                reference   44%    16.8s     12.1       0.8
  muhammad ad 2 16x9                reference   38%    19.7s      9.8       1.3
  zeeshan ad 1 16x9                 approved    45%    18.0s      9.6       1.7
  ad 1 | claude | 9x16              approved    45%    17.0s     13.7       0.8
  ad 2 | claude | 9x16              approved    56%    25.7s      8.3       0.2
------------------------------------------------------------------------------------------------
"""

# Every row this module knows how to run. A format must answer for each one.
ALL_ROWS = (
    "container:size", "container:fps", "container:codec", "container:duration", "container:frames",
    "audio:stamp", "audio:stream_integrity", "audio:lipsync", "audio:click_at_joins",
    "style:coverage", "style:static_run", "style:change_rate",
    "cut:uncovered_joins", "cut:black_frames", "cut:min_segment", "cut:jump_cut",
    "cut:splice_visibility",
    "captions:graphic_clearance", "captions:card_collision", "captions:burned",
    "captions:within_runtime", "captions:sync",
    "compliance:banned_screen", "compliance:labels", "compliance:drug_names",
    "compliance:negative_events", "compliance:script_fidelity",
    "watch:pass", "srt:present", "srt:shape",
)

# ---------------------------------------------------------------------------- shared fragments
# These are not "defaults" in the sense of a fallback -- a format still has to reference them, so
# the choice stays visible at the format. They exist so one number has one home.

_DRUGS = r"\b(zepbound|tirzepatide|semaglutide|ozempic|mounjaro|wegovy)\b"
# Dan's rule, ad-edit Step 9.3: "weight loss medication" only, never a brand name.

_BLACK = dict(max_luma=6.0, allow_lead_s=0.0, allow_tail_s=0.0)
# 6.0 of 255: a frame this dark is a hole, not a grade. Ported from shorts/*/qc.js, which fails on
# ANY black frame; the lead/tail allowances exist for formats that legitimately fade from or to
# black and each one sets them itself.

_LIPSYNC = dict(tolerance_ms=1.0, checkpoints=5)
# 1.0 ms: the defect this catches is EXACTLY 219 samples = 4.966 ms at 44.1 kHz (alimiter attack=5,
# measured on V4 2026-08-28, correlation 1.0000 at three checkpoints). The fix renders 0.000 ms, so
# 1 ms is five times the noise floor of the measurement and a fifth of the defect.

_NEGEV = dict(min_frames=24)
# 24 frames: one sample every ~10 s of a 4-minute ad. The scan is a person's judgment (see
# checks/compliance.py); this row only enforces that it happened on THIS render and was written down.

_CAPTION_BAND_16x9 = (0.156, 0.861, 0.688, 0.102)
# x, y, w, h as fractions of the frame = crop=1320:110:300:930 at 1920x1080, the band
# longform-edit/qc_style.py has sampled since 2026-08. Keep it in fractions so 4K and 1080p agree.
_CAPTION_BAND_9x16 = (0.10, 0.70, 0.80, 0.14)
# the vertical caption safe area from the /make-ad 1080x1920 spec.


def _common(drop=(), **over):
    """The rows whose bound genuinely does not vary by format.

    `drop` names the ones this format declares NOT APPLICABLE instead -- the audit refuses a format
    that both configures a row and declares it inapplicable, so the two lists cannot drift apart.
    """
    d = {
        "cut:black_frames": dict(_BLACK),
        "audio:lipsync": dict(_LIPSYNC),
        "compliance:drug_names": dict(pattern=_DRUGS),
        "compliance:negative_events": dict(_NEGEV),
        "compliance:script_fidelity": dict(min_ratio=0.95),
        # 0.95: website-video/recipe/qc.py and ad-edit/rev5/qc5.py both landed here independently;
        # below it a dropped half-sentence at a join stops being visible.
        "captions:graphic_clearance": dict(min_px=20),
        # 20 px: website rev 2 inked at y 727-806 over lower thirds at y 757-905 -- 49 px of
        # OVERLAP. 20 px is the clearance rev 4 was built to and Dan approved on 2026-09-08.
        "captions:within_runtime": dict(tolerance_s=0.10),
        "cut:uncovered_joins": dict(max_per_min=2.5),
        # 2.5/min: the rejected spray-tan longform reads 3.2; the highest APPROVED reading in the
        # corpus is website rev 6 at 1.8, then Zeeshan's approved ad 1 at 1.7. Measured 2026-09-11.
        "cut:min_segment": dict(min_seconds=0.20),
        # 0.20 s: website-video/recipe/qc.py check 2 and ad-edit/rev5/qc5.py, unchanged since rev 1.
        "cut:jump_cut": dict(),
        # no bound of its own: two adjacent VISIBLE segments at one framing is a jump cut, full
        # stop (website-video/recipe/qc.py check 2, hardened on rev 4 to ignore covered segments).
        "cut:splice_visibility": dict(ceiling_mult=1.0),
        "audio:click_at_joins": dict(ceiling_mult=1.25),
        # 1.25x the file's OWN natural ceiling: longform-edit/qc_style.check_splices.
    }
    for k in drop:
        d.pop(k, None)
    d.update(over)
    return d


# ---------------------------------------------------------------------------- the formats
FORMATS = {

    # ------------------------------------------------------------------ 9:16 vertical ad
    "ad9x16": dict(
        note="A vertical ad cut from a finished long-form master. The approved examples are the "
             "Ad 1 and Ad 2 verticals cut from Muhammad's masters (2026-09-10).",
        rows=_common(
            **{
                "container:size": dict(size="1080x1920"),
                "container:fps": dict(fps="30000/1001"),
                "container:codec": dict(vcodec="h264", acodec="aac", asr=48000, achannels=2),
                "container:duration": dict(tolerance_s=0.10),
                "container:frames": dict(),
                "audio:stamp": dict(),
                "audio:stream_integrity": dict(length_tolerance_s=0.15, silent_second_dbfs=-50.0),
                "style:coverage": dict(min=0.38),
                # lowest APPROVED vertical is Ad 1 at 45%, Ad 2 at 56%. 0.38 keeps 7 points of
                # margin under the tighter of the two. shortad's own qc.json used his cut's 39%.
                "style:static_run": dict(max=31.6),
                # 31.6 s is Muhammad's own longest talking stretch (shortad-from-longform qc.json).
                # Our approved verticals read 17.0 and 25.7.
                "style:change_rate": dict(min_per_min=7.0),
                # approved verticals read 13.7 and 8.3; his 16x9 masters 12.1 and 9.8.
                "captions:burned": dict(present=True, min_frac=0.45, band=_CAPTION_BAND_9x16),
                "captions:card_collision": dict(),
                "captions:sync": dict(tolerance_ms=120, silence_before_s=0.30, min_samples=5),
                # Dan, 2026-09-08: the highlighted word must be the word being said.
                "compliance:banned_screen": dict(max_ncc=0.72, grid_w=192),
                # 0.72 is shortad-from-longform/reference/qc.py check 10's bound, unchanged.
                "compliance:labels": dict(min_corr=0.85),
                # 0.85: website-video/recipe/qc_frame.ai_tags, measured over its AI inserts.
                "watch:pass": dict(required=True),
                # the one format where the watch pass is already a hard gate (qc.py check 15).
            }),
        not_applicable={
            "srt:present": "a vertical ad burns its captions; there is no sidecar deliverable",
            "srt:shape": "no sidecar -- see srt:present",
        },
    ),

    # ------------------------------------------------------------------ 16:9 ad master
    "ad16x9": dict(
        note="A filmed ad in landscape. References: Muhammad's Ad 1 and Ad 2 masters and Zeeshan's "
             "approved Ad 1.",
        rows=_common(
            **{
                "container:size": dict(size="1920x1080"),
                "container:fps": dict(fps="30000/1001"),
                "container:codec": dict(vcodec="h264", acodec="aac", asr=48000, achannels=2),
                "container:duration": dict(tolerance_s=0.10),
                "container:frames": dict(),
                "audio:stamp": dict(),
                "audio:stream_integrity": dict(length_tolerance_s=0.15, silent_second_dbfs=-50.0),
                "style:coverage": dict(min=0.35),
                # lowest reading among the three 16:9 references is Muhammad's Ad 2 at 38%.
                "style:static_run": dict(max=25.0),
                # ad-edit/rev5/qc5.py's own bound; the three references read 16.8, 19.7 and 18.0.
                "style:change_rate": dict(min_per_min=8.0),
                # the three references read 12.1, 9.8 and 9.6.
                "captions:burned": dict(present=True, min_frac=0.45, band=_CAPTION_BAND_16x9),
                "captions:card_collision": dict(),
                "captions:sync": dict(tolerance_ms=120, silence_before_s=0.30, min_samples=5),
                "compliance:banned_screen": dict(max_ncc=0.72, grid_w=192),
                "compliance:labels": dict(min_corr=0.85),
                "watch:pass": dict(required=False,
                                   pending="Phase 3 of handoff-20260911-video-quality-engine.md "
                                           "turns the watch pass on for /ad-edit (2026-09-11)"),
            }),
        not_applicable={
            "srt:present": "a 16:9 ad burns its captions; there is no sidecar deliverable",
            "srt:shape": "no sidecar -- see srt:present",
        },
    ),

    # ------------------------------------------------------------------ 1:1 square ad
    "ad1x1": dict(
        note="The square re-layout of an approved vertical, for Demand Gen in-feed / Discover / "
             "Gmail. Same EDL, same grade, same beats, same audio bit for bit.",
        rows=_common(
            **{
                "container:size": dict(size="1080x1080"),
                "container:fps": dict(fps="30000/1001"),
                "container:codec": dict(vcodec="h264", acodec="aac", asr=48000, achannels=2),
                "container:duration": dict(tolerance_s=0.10),
                "container:frames": dict(),
                "audio:stamp": dict(),
                "audio:stream_integrity": dict(length_tolerance_s=0.15, silent_second_dbfs=-50.0),
                "style:coverage": dict(min=0.38),
                "style:static_run": dict(max=31.6),
                "style:change_rate": dict(min_per_min=7.0),
                # a square build is a re-layout of an approved vertical, so it inherits the
                # vertical's bounds: the EDL, the beats and the coverage are the same cut.
                "captions:burned": dict(present=True, min_frac=0.45, band=(0.08, 0.72, 0.84, 0.16)),
                "captions:card_collision": dict(),
                "captions:sync": dict(tolerance_ms=120, silence_before_s=0.30, min_samples=5),
                "compliance:banned_screen": dict(max_ncc=0.72, grid_w=192),
                "compliance:labels": dict(min_corr=0.85),
                "watch:pass": dict(required=True),
                # a square build is delivered to an ad platform; it gets the vertical's hard gate.
            }),
        not_applicable={
            "srt:present": "a square ad burns its captions; there is no sidecar deliverable",
            "srt:shape": "no sidecar -- see srt:present",
        },
    ),

    # ------------------------------------------------------------------ organic YouTube long-form
    "longform": dict(
        note="An organic YouTube video. ⚠ ITS CAPTION RULE IS THE OPPOSITE OF EVERY AD FORMAT'S: "
             "Dan, 2026-08-27 -- organic longforms carry NO burned captions and no watermark; the "
             ".srt sidecar is the deliverable.",
        rows=_common(
            drop=("captions:graphic_clearance",),
            **{
                "container:size": dict(size="1920x1080"),
                "container:fps": dict(fps="30000/1001"),
                "container:codec": dict(vcodec="h264", acodec="aac", asr=48000, achannels=2),
                "container:duration": dict(tolerance_s=1.50),
                # 1.5 s: longform-edit/qc_generic.py and qc_with_inserts.py. A longform's target is
                # the plan's total, which floats by a frame per beat over a 20-minute programme.
                "container:frames": dict(),
                "audio:stamp": dict(),
                "audio:stream_integrity": dict(length_tolerance_s=0.15, silent_second_dbfs=-50.0),
                "style:coverage": dict(min=0.40),
                # longform-edit/qc_style.MIN_COVERAGE, unchanged. Its provenance: the outside
                # editor's 6:58 ab-wheel cut 64.6%, our rebuild 58.2%, the 8/20 cut Dan rejected
                # 8.7% -- and re-measured 2026-09-11 at 9%.
                "style:static_run": dict(max=30.0),
                # Dan's own written rule, 2026-08-21 (spray-tan rev 1). The rejected ab-wheel cut
                # sits still for 79.2 s.
                "style:change_rate": dict(min_per_min=4.0),
                # qc_style.MIN_SCENES_PER_MIN. The reference cut runs 7.7/min; the rejected ab-wheel
                # cut 2.1.
                "captions:burned": dict(present=False, max_frac=0.10, band=_CAPTION_BAND_16x9),
                # the INVERTED rule. See the note above.
                "captions:card_collision": dict(),
                "compliance:banned_screen": dict(max_ncc=0.72, grid_w=192),
                # the row that was missing here: the app's before/after screen reached the delivered
                # spray-tan longform for 5.6 s at 18:04 because only /ad-edit template-scanned.
                "compliance:labels": dict(min_corr=0.85),
                "watch:pass": dict(required=False,
                                   pending="Phase 3 of handoff-20260911-video-quality-engine.md "
                                           "turns the watch pass on for /longform-edit (2026-09-11)"),
                "srt:present": dict(required=True),
                "srt:shape": dict(max_line_chars=48, max_lines=2,
                                  banned_spellings=["GOP", "Zepbound", "Ozempic"]),
                # 48 chars / 2 lines: longform-edit/cutdown_final_gate.py. "GOP" is Whisper's
                # mis-hearing of "GLP"; it has come back three times.
            }),
        not_applicable={
            "captions:sync": "an organic longform burns no captions, so there is no on-screen "
                             "highlight to synchronise; srt:shape covers the sidecar",
            "captions:graphic_clearance": "no burned captions -- nothing to clear a graphic by",
        },
    ),

    # ------------------------------------------------------------------ vertical Short / Reel
    "short": dict(
        note="A vertical Short cut out of a video we ourselves rendered.",
        rows=_common(
            **{
                "container:size": dict(size="1080x1920"),
                "container:fps": dict(fps="30000/1001"),
                "container:codec": dict(vcodec="h264", acodec="aac", asr=48000, achannels=2),
                "container:duration": dict(tolerance_s=0.25),
                # 0.25 s: all four shorts/qc.js forks. A Short's target is its own beat sheet.
                "container:frames": dict(),
                "audio:stamp": dict(),
                "audio:stream_integrity": dict(length_tolerance_s=0.15, silent_second_dbfs=-50.0),
                # shorts/*/qc.js already failed on any second under -50 dBFS; kept exactly.
                "style:coverage": dict(min=0.30),
                # a Short is one continuous passage of a longer cut, so it inherits less coverage
                # than a built ad. 0.30 is the lowest APPROVED longform-family reading (website
                # rev 6, 31%) rounded down one point. ⚠ Not measured on the approved Shorts
                # themselves -- the five ab-wheel Shorts Dan approved are cut from Muhammad's
                # master and have not been re-gated. Re-measure when they are.
                "style:static_run": dict(max=30.0),
                "style:change_rate": dict(min_per_min=4.0),
                "captions:burned": dict(present=True, min_frac=0.45, band=_CAPTION_BAND_9x16),
                "captions:card_collision": dict(),
                "captions:sync": dict(tolerance_ms=120, silence_before_s=0.30, min_samples=4),
                # the row two of the four shorts gates did not have at all: full-bleed/qc.js and
                # scored-source/qc.js cannot see a desynced caption.
                "compliance:banned_screen": dict(max_ncc=0.72, grid_w=192),
                "compliance:labels": dict(min_corr=0.85),
                "watch:pass": dict(required=False,
                                   pending="Phase 3 of handoff-20260911-video-quality-engine.md "
                                           "turns the watch pass on for /shorts, which mentions it "
                                           "zero times today (2026-09-11)"),
            }),
        not_applicable={
            "srt:present": "a Short burns its captions; there is no sidecar deliverable",
            "srt:shape": "no sidecar -- see srt:present",
        },
    ),

    # ------------------------------------------------------------------ absbyai.com conversion video
    "website": dict(
        note="The trust video on the analysis page / /start. Six rounds over seven days; rev 4 is "
             "where Dan locked the framing and rev 6 is his final.",
        rows=_common(
            **{
                "container:size": dict(size="1920x1080"),
                "container:fps": dict(fps="30000/1001"),
                "container:codec": dict(vcodec="h264", acodec="aac", asr=48000, achannels=2),
                "container:duration": dict(tolerance_s=0.50),
                "container:frames": dict(),
                "audio:stamp": dict(),
                "audio:stream_integrity": dict(length_tolerance_s=0.15, silent_second_dbfs=-50.0),
                "style:coverage": dict(min=0.28),
                # the three APPROVED revs read 37%, 32% and 31%. 0.28 sits three points under the
                # lowest one Dan accepted. ⚠ This is NOT the longform 0.40: a trust video holds on
                # Dan's face on purpose, and grading it against the ab-wheel number would block the
                # cut he approved. Per-format config is the answer, not a widened bound.
                "style:static_run": dict(max=25.0),
                # website-video/recipe/qc.py check 3, unchanged. The approved revs read 12.2, 13.5
                # and 10.8.
                "style:change_rate": dict(min_per_min=8.0),
                # the approved revs read 12.0, 11.7 and 12.5.
                "captions:burned": dict(present=True, min_frac=0.45, band=_CAPTION_BAND_16x9),
                "captions:card_collision": dict(),
                "captions:sync": dict(tolerance_ms=120, silence_before_s=0.30, min_samples=5),
                "compliance:banned_screen": dict(max_ncc=0.72, grid_w=192),
                # measured on rev 4 2026-09-11: best NCC 0.484 over 6,900 frames, nothing over 0.72.
                "compliance:labels": dict(min_corr=0.85),
                "watch:pass": dict(required=False,
                                   pending="Phase 3 of handoff-20260911-video-quality-engine.md "
                                           "turns the watch pass on for /website-video (2026-09-11)"),
            }),
        not_applicable={
            "srt:present": "the website player carries no sidecar; captions are burned",
            "srt:shape": "no sidecar -- see srt:present",
        },
    ),

    # ------------------------------------------------------------------ AI exercise demo
    "exercise-demo": dict(
        note="An AI-Dan exercise demo for the Trainer: a narrated form cue over a seamless looping "
             "rep. ⚠ ITS SHAPE IS NOT A DEFECT. The narration ends and the rep keeps looping, so "
             "the picture legitimately outruns the audio -- which is why 88 of these failed the "
             "`silence` and `length` rows in Docs/VQC_baseline_20260909.md. The allowance below is "
             "MEASURED off the files Dan approved, not widened until they passed.",
        rows=_common(
            drop=("audio:lipsync", "audio:click_at_joins", "cut:min_segment", "cut:jump_cut",
                  "cut:splice_visibility", "captions:graphic_clearance", "captions:within_runtime",
                  "compliance:drug_names", "compliance:negative_events",
                  "compliance:script_fidelity"),
            **{
                "container:size": dict(size="960x540"),
                "container:fps": dict(fps="24/1"),
                "container:codec": dict(vcodec="h264", acodec="aac", asr=32000, achannels=1),
                # measured 2026-09-11 over the 33 shipped demos in public/exercise-demos: every one
                # is 960x540 @ 24 fps with mono 32 kHz aac. ⚠ EXCEPT plank.mp4, which is 960x536 --
                # a real finding this gate would have caught, reported rather than accommodated.
                "container:duration": dict(tolerance_s=0.25),
                "container:frames": dict(),
                "audio:stamp": dict(),
                "audio:stream_integrity": dict(length_tolerance_s=0.15, max_audio_short_s=6.5,
                                               silent_second_dbfs=-50.0, allow_silent_lead_s=1),
                # Measured 2026-09-11 across the 33 shipped demos in public/exercise-demos:
                #   picture minus narration   +0.49 s .. +5.59 s  (max: pike-pushup)  -> 6.5 s
                #   leading silent seconds    exactly 1 on 32 of 33, never 2          -> 1
                #   trailing silent seconds   0 on all 33                             -> unchanged
                # The lead allowance is the measurement, with no margin added: a demo that opens
                # with two silent seconds is not like the ones Dan approved and should fail.
                "cut:uncovered_joins": dict(max_per_min=99.0),
                # a seamless loop is one continuous rep repeated: the loop point is a picture
                # discontinuity by construction and there is nothing to cover it with. Effectively
                # off, and stated rather than silently absent.
            }),
        not_applicable={
            "style:coverage": "there is nothing to cut away TO: the deliverable is one looping rep "
                              "of one movement, by design (exercisegeneration/SKILL.md)",
            "style:static_run": "same: the shot is the demo, and it is 15-28 s long",
            "style:change_rate": "same",
            "cut:min_segment": "a single generated loop has no framing segments",
            "cut:jump_cut": "a single generated loop has no framing segments",
            "cut:splice_visibility": "a single generated loop has no joins",
            "audio:click_at_joins": "a single generated loop has no joins",
            "audio:lipsync": "the narration is a cloned-voice read laid over a generated loop; it "
                             "was never cut against a source mix, so there is no alignment to hold",
            "captions:burned": "an exercise demo plays muted-first inside the app with no captions",
            "captions:graphic_clearance": "no captions and no graphics",
            "captions:card_collision": "no captions and no cards",
            "captions:within_runtime": "no captions",
            "captions:sync": "no captions",
            "compliance:banned_screen": "no app UI appears in a generated exercise demo",
            "compliance:labels": "AI-Dan is not a picture of Dan's physique making a before/after "
                                 "claim; the demos carry the app's own AI disclosure in the UI",
            "compliance:drug_names": "the narration is the movement's form cues only",
            "compliance:script_fidelity": "the form cues are generated with the clip, not cut to a "
                                          "script",
            "compliance:negative_events": "a demo of a movement shows no body-shame imagery",
            "srt:present": "the demos play inside the app with no sidecar",
            "srt:shape": "no sidecar -- see srt:present",
            "watch:pass": "delivered in batches of 9-15 and reviewed as a batch by Dan before "
                          "install; Phase 3 decides whether a per-file watch pass is worth it",
        },
    ),
}


def config_for(fmt):
    if fmt not in FORMATS:
        raise SystemExit(f"unknown format {fmt!r}; known: {', '.join(sorted(FORMATS))}")
    return FORMATS[fmt]


def audit():
    """Every format answers for every row, or this returns what is missing."""
    holes = {}
    for name, f in FORMATS.items():
        missing = [r for r in ALL_ROWS
                   if r not in f["rows"] and r not in f.get("not_applicable", {})]
        both = [r for r in ALL_ROWS
                if r in f["rows"] and r in f.get("not_applicable", {})]
        if missing or both:
            holes[name] = dict(unconfigured=missing, contradictory=both)
    return holes
