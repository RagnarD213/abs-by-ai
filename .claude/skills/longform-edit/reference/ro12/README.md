# RO-12 "Top 5 Zepbound Tips" (9/23 C1706): recipe and traps (Claude Opus 5.5, 2026-09-30)

First organic long-form on the 9/23 studio set. Independent review SHIP on round 3; delivered to
`claude edited long form content/09 - Top 5 Zepbound Tips/`. Work dir `/Volumes/Extreme/_edit_work/ro12/`.

Recipe: `edl.py` (kept source ranges snapped to measured speech islands, `vad.py`), `plan.py` (every graphic and insert anchored
to Dan's words with `words.at()`), `build.py timeline | stills | picture | audio`, `finish.py` (SRT from the delivered audio's own
transcript, chapters, gate plan incl. label chips and banned-screen source), `rebuild_r2.sh` (whole chain), `deliver.sh`.

## Traps this build paid for
1. **Whisper merges restarts.** Five abandoned attempts on C1706 were invisible in the Whisper words ("it@372.98-375.54" swallowed
   "If you bled, or if it ac-"). A verbatim Gemini listen of the lav in 3-minute chunks (`gemini_listen.py`, about $0.10 per chunk)
   listed every one; the cut points then come from the lav's speech islands, not the word times.
2. **Pick the intro take by ear.** Takes 1 and 2 said "zap bound" / "set bound"; only take 3 said Zepbound. The text is identical.
3. **The 9/23 lav is quiet (-28 to -30 LUFS), the chain lifts it +18.6 dB, and the bed goes up with it.** RO-05's bed level failed
   the floor row (20.8 vs Muhammad 27.6); 10 dB lower passed. Treat the bed level as a ceiling and read the floor row.
4. **A fitted EQ belongs to its recording.** WV-01's fitted curve (same set, same mic) failed the tone row on C1706 (80 Hz +3.6,
   5.5 kHz -4.5). Re-fit on the roll (`voice_chain.py` without `--eq`), then add the approved extras (audio B's +0.9 dB at 150 Hz).
5. **Presenter slivers.** Any gap under ~0.67 s between two covering pieces, or between a piece and a camera cut, flashes Dan on
   screen. Close them in the timeline (stretch the piece or move the cut onto its edge), never by eye afterwards.
6. **Side layouts (3A card, phone) are their own wide shot.** `shift_presenter` applied only while the card shows makes Dan jump
   320 px mid-shot; put shot boundaries on the card's first and last frame so the shift enters and leaves on a cut. Then fix W/T
   parity per run of free shots (a run between two forced-W shots needs an odd count; split its longest shot).
7. **Check every insert slot against its source length.** An 8.4 s stock clip in a 10 s slot froze for 1.8 s.
8. **Stock can contradict the instruction.** Every free injection clip shows a pen in the belly; Dan teaches syringe in the outer
   thigh. The steps card beside Dan was right; the "thigh" stock (back of a leg) was a blocker.
9. **Negative-imagery scan:** a stock close-up of a soft belly under "you are smaller, but soft" is exactly the pattern; remove it
   yourself. A heavier man eating a burger (not a close-up) stays and goes to Dan as needs-review.
10. **Gate rows that cannot pass on a Zepbound video:** `compliance:drug_names` and `srt:shape` (banned spelling "Zepbound") both
    carry the ad rule into organic long-form; `captions:burned` / `captions:card_collision` read Soft Blue lower thirds and cards as
    burned captions (same as RO-05 round 4). Reported to Dan, not tuned.
