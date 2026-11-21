---
name: audio-joins-smooth-before-ship
description: "Dan 2026-10-20 (RO-25): every audio join is measured (seamscan.py) and blind-listened twice before any review copy; stumbles from the word map; a failing audio row is fixed, never carried as accepted"
metadata:
  type: feedback
---
Dan, after watching the published "I'm 41. I Wasted My Life." (RO-25, Codex R7): a solid edit, but a few awkward audio starts, places where the audio was not smooth, and a stumble left in. He wants all the audio fixed and smooth before anything like that ships again.

**Why:** the delivery gate's `audio:click_at_joins` row measures only clicks; it passed six of the seven faults a listener heard (chopped "Right." at 1:46.5, a hard start at 4:53.6, a room jump at 5:14.2, a DC thump at 5:55.2, a clipped "And" at 8:40.9, the "productive" restart at 1:18.2, a click at 4:01.0). One join the gate did flag (2:53.6) the listener called clean. The editor had dropped 1:46.5 from its join list as "a contiguous camera boundary". Known failing rows were carried into the final as "accepted".

**How to apply:** every round that delivers a review copy or a final, Claude and Codex: list every seam from the audio assembly map, run `.claude/skills/_shared/audio/seamscan.py` on mono PCM of the exact file, cut 5 s clips around every flag plus controls, blind-listen twice with shuffled letters (Gemini), scan the word map for repeats, long short words, gaps and fragments, then FIX (cut into the pause at a zero crossing, keep the whole word, 20 to 40 ms crossfade, or the clean take). The reviewer repeats it. Rule text: `.claude/skills/_shared/VIDEO-RULES.md`, "Audio joins are smooth before anything ships". Related: [[editor-audio-untouched]], [[audio-never-over-strip]], [[gate-the-harm-not-just-the-fix]].
