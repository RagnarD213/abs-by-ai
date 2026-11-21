---
name: voice-bass-standard
description: Dan's voice standard for every video we mix ourselves is a subtle bass lift (+3 dB wide at 120 Hz), set 2026-10-12 on RO-19
metadata:
  type: feedback
---

Dan, 2026-10-12, picking the RO-19 "My First Spray Tan" voice from seven options: "For the voice, let's go with B2 with more bass. Let's make a subtle addition of bass to my voice the standard for all Claude and Codex video editing skills. I like that better than the default, just the echo removed."

B2 = the warm fixed tone shape + light dereverb + no expander + a wide +3 dB lift at 120 Hz (`equalizer=f=120:t=q:w=0.8:g=+3.0`). +1.5 dB was not his pick; +4.5 dB measured close to boomy.

**Why:** he hears the bass version as more authoritative than echo removal alone.

**How to apply:** on every new voice we mix (never an editor's finished mix), start from the +3 dB lift at 120 Hz on top of the film's tone, keep the 70 Hz high-pass, check for boom. Less on a room that already reads full (my reading of "subtle"). Full rule: `.claude/skills/_shared/VIDEO-RULES.md`, top section. Related: [[audio-never-over-strip]], [[editor-audio-untouched]].
