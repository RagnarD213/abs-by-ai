# Handoff: build Dan's voice corpus from his Google Drive

Written 2026-10-06. Recommended model: **Claude Opus 5.5, high effort.** No metered spend (Drive reads only).
Runs fine in a cloud session or locally. Task name: `Dan Voice Corpus`.

## Goal

Every script skill (`/scriptwriting`, `/scriptfromoutline`, `/shorts-scripting`, `/ad-copy`, `/ad-outlines`) should
write in Dan's real voice so he edits nothing. Today the voice references are thin and partly wrong. Find every
Abs By AI script and content document in Dan's Google Drive, work out which words are actually Dan's, and turn
them into one voice guide plus a reference corpus the skills read before writing.

## What Dan decided (2026-10-06)

- **Not voice models:** the V2 long-form transcript ("Use AI To Get Real Six Pack Abs - 6 Strategies That Work")
  and the AI-generated ad "The Upload" (`ad-factory/the-upload/script.md`). Dan: the ad was AI-generated and not
  good, and the video was not that good. Do not use either. They were removed from the skills on 2026-10-06.
- **Scope is Abs By AI documents.** His 2022 Gundry MD scripts and other client work are out unless he says so.

## The hard part: whose words are they?

Most Abs By AI docs since July 2026 were drafted by Claude. Learning from those teaches Claude to copy itself.
Sort every doc into a tier before learning anything from it:

- **Tier A, Dan's own writing.** Docs he wrote himself: his outlines (for example "Abs By AI ad outlines - batch 1"),
  his shorts ideas lists, his own drafts, anything created before Claude worked on the project, typed notes.
  Highest weight.
- **Tier B, Dan's edits to a Claude draft.** Where an as-delivered Claude copy exists (in `Docs/`, `Handoffs/`,
  skill references, or git history) and the Drive doc now differs, the difference is Dan's voice. Extract
  before/after pairs. Second-highest weight, and the most useful for "what Claude does that Dan cuts".
  The 2026-09-21 work is the model: `Docs/SCRIPTS_923_SHOOT_LONGFORM_DAN_EDITED_20260921.md`,
  `.claude/skills/scriptfromoutline/references/dan-edits-2026-09-21.md`, `dan-edits-2026-09-21-calories-pair.md`.
- **Tier C, Claude text Dan approved without edits.** Weak evidence. Use only to confirm patterns from A and B.
  `.claude/skills/scriptwriting/references/finalized-ad-scripts.md` (ads batch 1) is probably here or B.
- **Exclude:** AI-generated ads, Dan-ruled-out material above, docs written for editors about edits (those are
  covered by memory `revision-docs-in-dans-voice`).

Signals that help: em dashes and "Today we're talking about" style openers point to Claude; Wispr Flow
dictation quirks, his real numbers and run-on spoken phrasing point to Dan. Doc comments and suggestions by
danroseconsulting@gmail.com are Dan's (`read_file_content` with `includeComments: true`). If authorship is unclear,
say so in the inventory rather than guess.

## Steps

1. **Read first:** `.claude/skills/_shared/WRITING-RULES.md`, memory entries `script-zero-edit-lessons`,
   `video-outline-style`, `dan-personal-facts-for-scripts`, `ad-copy-headline-voice`, `no-em-dashes`, and the
   "WHAT DAN CHANGED" section of `.claude/skills/scriptfromoutline/SKILL.md`. Do not re-learn what is already there;
   extend it.
2. **Find the docs.** Google Drive MCP `search_files`, owner `me`, Google Docs mime type, many queries: title and
   full text for "Abs By AI", "abs by ai", "script", "outline", "teleprompter", "shorts", "VSL", "sales letter",
   "shoot", "long form", "longform", "ad", "hook", "SixPackAbs" (only the Abs By AI era, 2025 on). Page through
   every result. Known starting points: `1r3Jmuihyryq0qv2Y3A--D_yaerF9B_ZqAb-QvOuAwjg` (ads batch 1 with filming
   notes), `1bpEndCcM-imeOWS0tp86l7Ud0bGyxLQ-MWZVAwcacgA` (batch 1 teleprompter only, Aug 11),
   `1AVRvxiINZ0EDkoFv77piXbg5xGuizHGuHE7vRVWXRKk` and `1n1FIVgNaBZZ6j0aJsEyqLAE8oT82SQQNJ_pGrCLVVwg` (Ads 2 to 15),
   `1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA` (/start VSL scripts), the ad outlines doc, each shoot's outline doc.
3. **Read with subagents.** Big docs overflow context (the batch 1 doc is 85k characters). Send batches of docs to
   subagents that return, per doc: id, title, dates, type (ad, long-form, short, VSL, sales letter, outline, idea
   list), tier with the reason, and the Tier A or B passages verbatim (spoken words only, no cues or links).
   Never edit any Drive doc.
4. **Write the inventory:** `Docs/VOICE_CORPUS_INVENTORY.md`, one row per doc with the fields above.
5. **Write the corpus:** `.claude/skills/_shared/voice/` with Tier A passages grouped by format
   (`ads.md`, `longform.md`, `shorts.md`, `sales.md`, `outlines.md`) and Tier B before/after pairs in
   `dan-edits-<date>.md` files. Words only, headings kept, each passage labelled with its source doc id.
6. **Write the guide:** `.claude/skills/_shared/DAN-VOICE.md`, at most about 1,500 words. Patterns ranked by how
   much evidence backs them, each with two or three real quotes and its source. Sections: openers, sentence shape,
   pet phrases, how he uses numbers and his own story, how he sells, how he closes, and "what Claude writes that Dan
   cuts". Mark anything backed only by Tier C as weak.
7. **Wire it in:** WRITING-RULES section 1 "Anything in Dan's voice" row points at `DAN-VOICE.md`; replace the
   ad scripts row's voice references line with the corpus files that actually earned a place. Point the "Voice
   rules" sections of `scriptwriting`, `scriptfromoutline`, `shorts-scripting` and the voice parts of `ad-copy` at
   the guide, and rewrite any voice trait the evidence contradicts (for example "Em-dash pivots" was removed
   2026-10-06). Drop `finalized-ad-scripts.md` from the voice references if it lands in Tier C.
8. **Prove it:** pick one Tier A or B passage the guide did not quote, give a fresh subagent only its outline or
   topic plus the guide, have it write the passage, and compare side by side with Dan's real version. Report what
   still differs and fix the guide once.
9. **Push** every changed file with `scripts/git/safe-push.sh` (locally) or plain git to `main` (cloud clean checkout).
   An em dash count (`grep -c` for the character) on every new file you wrote must be 0; quoted Tier C Claude text may keep its old punctuation but
   the guide must say never to copy it.
10. **Close out:** delete this handoff's row in `Handoffs/README.md` and its line in `AI_COORDINATION.md` if one
    was added.

## Report to Dan

In plain words: how many docs were found, how many were truly his writing, the five strongest voice patterns with
one quote each, the side-by-side test result, and any docs where authorship was unclear and his call would change
the guide. Stop there.
