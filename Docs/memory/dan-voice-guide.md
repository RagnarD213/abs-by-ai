---
name: dan-voice-guide
description: 2026-10-06 voice guide built from Dan's own ads (HBI $5.96M), book, outlines and edits; read .claude/skills/_shared/DAN-VOICE.md before writing anything in his voice
metadata:
  type: reference
---

On 2026-10-06 (Dan Voice Training P1) Claude read Dan's real writing and built a voice guide that every writing skill
now points at:

- `.claude/skills/_shared/DAN-VOICE.md`: the guide (about 1,500 words), ranked patterns with real quotes.
- `.claude/skills/_shared/voice/`: real passages by job (`ads.md`, `content-longform.md`, `content-shorts.md`,
  `sales.md`, `outlines.md`, `book.md`), outside writers (`borrowed-keith-wes.md`), Dan's edits to Claude drafts
  (`dan-edits-2026-10-06.md`), and the numbers (`STATS.md`).
- `scripts/voice/voice_stats.py`: measures a draft ("and" per 100 words, kicker endings, em dashes, sentence length).
- `Docs/VOICE_CORPUS_INVENTORY.md`: every source, its tier, and its raw copy in Drive folder
  `1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`.

**Why:** Dan wants drafts he does not need to edit. The numbers proved his hunch: Claude uses "and" about 45 percent
more than he does, ends paragraphs on short kickers 2.5 to 6 times as often, and writes shorter, more even sentences.

**How to apply:** read `DAN-VOICE.md` before writing any script, outline, ad copy, letter or description in his voice,
then the matching `voice/` file. Run `voice_stats.py` on the draft before delivering. "Let's be honest" and "really,
really" are Claude's, not his. The blind test (step 10) was not run yet; how to run it is at the end of the inventory.
Part 2 (an AI-tell checker built on `STATS.md`) is a separate task. Related: [[script-zero-edit-lessons]],
[[dan-personal-facts-for-scripts]], [[no-em-dashes]].
