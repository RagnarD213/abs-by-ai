---
name: dan-voice
description: >
  Write, assemble or check anything that goes out under Dan Rose's name so it reads as his and not as AI. Three
  modes. WRITE: turn a content plan (an outline, a brief, a list of points) into finished words in his voice through
  the dan-voice-writer agent. ASSEMBLE: Dan dictates a 3 to 5 minute take and this orders and cuts it into a script,
  letter or post with at least 80% of the sentences left as he said them. CHECK: score a draft against his numbers
  and have the critic agent mark what gives it away. Use whenever Dan says "write this in my voice", "make this sound
  like me", "this sounds like AI", "assemble my take", "here's my dictation, turn it into a script", "check this
  draft", or invokes "/dan-voice". The writing skills (/scriptwriting, /scriptfromoutline, /shorts-scripting,
  /ad-copy, /copy-edit, /ad-outlines, /shortsideas, /youtube-packaging) decide WHAT a piece says; this skill and its
  agents decide how it sounds.
---

# /dan-voice

Built 2026-10-10 (Dan Voice P2B). The method and its scores: `.claude/skills/_shared/DAN-VOICE.md` and
`Docs/voice-bench/`. Everything here is in the repo, so it works the same in a cloud session.

**The three lanes (research, 2026-10-08).** Text a person wrote and AI only arranged is hard to tell from human
text; text AI generated is not. So the lane depends on what is at stake:

| lane | use it for | mode |
|---|---|---|
| 1. His words first | website sales videos and letters, personal posts, anything read by people who know him | ASSEMBLE |
| 2. Continue from his text | scripts, descriptions, captions, editor messages | WRITE |
| 3. Check | any draft from either lane, or one Dan pastes in | CHECK |

If a Lane 1 piece arrives with no take from Dan, ask him for one (one line: what to talk about, 3 to 5 minutes,
talking to the viewer and not to Claude). Do not quietly fall back to WRITE for those pieces.

## Mode WRITE

1. Settle the content first, with the skill that owns the piece. The content plan is: what it is, who it is for, the
   points in order, every fact and number, the ask. His own outline wording goes in word for word: it is the seed.
2. Missing take or number? Look in `_shared/voice/POSITIONS.md`. Not there: one question to Dan or a `[DAN: ...]` gap.
   Never invent an opinion, a story or a number for him.
3. Hand the plan to the **dan-voice-writer** agent with the type and format (table in `DAN-VOICE.md`). It loads the
   real passages, drafts, runs the checker and the critic, and returns the piece with a short report.
4. Read the report. A hard fail or a score over the line that the writer could not fix is said to Dan in one line
   with the draft, not hidden.
5. Save the delivered draft to `voice-corpus/drafts/<date>-<slug>.md` if the folder exists (local sessions). When Dan
   finalizes it, the difference between the two is how the method learns (Phase D).

## Mode ASSEMBLE (Lane 1)

Dan talks; Claude is the editor, not the writer.

1. **Get the take.** A Wispr Flow dictation pasted in chat, a voice memo, or a raw roll transcript. It must be him
   talking to the viewer. His instructions to Claude ("make this punchier") are not part of the take: set them aside
   as directions.
2. **Clean, do not rewrite.** Remove filler sounds, false starts he corrected, and exact accidental repeats. Fix a
   word the transcriber plainly misheard. Nothing else changes inside a sentence.
3. **Order and cut.** Pick the order (hook, then his points, then the ask), cut what repeats or wanders, and set
   line breaks for a teleprompter or paragraphs for a letter. Moving and cutting whole sentences is the job.
4. **The 80% rule.** At least 80% of the sentences in the result are his sentences as he said them (after step 2).
   Count it: `python3 scripts/voice/assemble_check.py take.txt assembled.txt`. Under 80%: put his sentences back.
5. **Anything Claude adds is marked.** A bridge between two of his points, a hook he did not say, a call to action
   from `WRITING-RULES.md`: wrap each in `[+ ... +]` so his eye lands on it. Keep additions short and plain, and
   take their wording from his own sentences nearby wherever possible.
6. **Hard rules still apply** (`python3 scripts/voice/voice_check.py --hard assembled.txt`): no em or en dash.
   His swearing stays (memory `swearing-never-cut-never-ask`).
7. Deliver the assembled piece, the count ("31 of 36 sentences are yours as said; 5 additions marked"), and a list of
   what was cut in one line each, so he can ask for any of it back.

## Mode CHECK

1. `python3 scripts/voice/voice_check.py draft.txt --type <type> --format <format>`: hard fails, the score against
   the format's line, the measures outside his band, the lines to look at.
2. Hand the draft alone to the **dan-voice-critic** agent (it fetches its own 8 real pieces). It returns marks
   tagged WRONG, OVERSTATED and MISSING.
3. Report to Dan in plain words: would it pass, the three biggest giveaways with the line each sits on, and the
   fix for each. Change the draft only if he asked for a fix, and then only the marked spans.

## Rules that hold in every mode

- Never an em dash or an en dash. Never a phrase on the hard list (`voice_check.py`).
- Bands, not bans: no habit of his is ever required in a piece, and none is used more than his own pieces use it.
- A script is not a transcript (Dan, 2026-10-10): take his wording, his small words and his bluntness; give it order
  and line breaks. Instruction first, caveat after and short, or not at all.
- His personal facts go in only where the paragraph needs them (memory `personal-facts-only-when-relevant`).
- Nothing Claude drafted counts as his voice later, even after he edits it. Only his own text goes in the bank.
- The test of any change to this method is the bench (`python3 scripts/voice/bench.py run --setup <name>`), and a
  change that does not move the number is dropped.
