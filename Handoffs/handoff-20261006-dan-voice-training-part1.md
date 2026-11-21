# Handoff: train Claude to write in Dan's voice (Part 1, voice corpus and guide)

Written 2026-10-06. Replaces `handoff-20261006-dan-voice-corpus-from-drive.md` (merged in here, Dan's call: this is
the only voice handoff he runs). Task name: `Dan Voice Training P1`.

**Model: Claude Opus 5.5, high effort. Built to run in a CLOUD session** (Dan's choice, to save local tokens).
No metered spend: Drive reads, Dropbox downloads and yt-dlp listing only. Use subagents for the reading so the main
context stays small.

## Goal

Every writing skill (`/scriptwriting`, `/scriptfromoutline`, `/shorts-scripting`, `/shortsideas`, `/ad-copy`,
`/ad-outlines`, `/copy-edit`, `/youtube-packaging`) writes in Dan's real voice, so he edits nothing. Build one voice
guide plus a small set of real example passages the skills read before writing. Both cloud and local sessions get it,
because it lives in the repo.

You cannot retrain the model. "Training" here means: read everything once, measure how Dan writes, pick the best
real passages by job, and write that down where every writing skill loads it. Dumping whole books and scripts into
the skills is the wrong answer: it costs tokens on every job and buries the good parts.

Part 2 (a checker script that flags AI tells before delivery) is a separate task. This handoff only produces the
numbers Part 2 needs (step 6). Do not build the checker here.

## What Dan decided (2026-10-06)

- **Ads, top priority source:** his biggest client's top 10 all-time ad creatives, sheet
  `1RtcUMgsJAdOHu5VKKaMOhhVXNvGi8DvfZ8XU3CCrKtw` ("Top 10 All Time HBI Ad Creatives"; columns: name, script link,
  YouTube link, lifetime spend, lifetime CPA, creative producer). Rows marked **Social Response Marketing are Dan's
  own writing** (Tier A). Rows marked **Keith** or **Wes** are by outside copywriters Dan rates highly: learn their
  techniques and label them as borrowed, never call them Dan's voice. Spend and CPA tell you which ones won hardest;
  weight by that. Spend runs $855k to $5.96M per ad.
- **Ads, second source:** Dan's other past ad scripts on Drive (HBI, Spy Briefing, CPA offers, Physio Tru, Darren
  Fujiyama, 2019 to 2025). Social Response Marketing is Dan's agency, so finalized scripts from it count as his.
  "Scripts for Mike / Jason / Martin" were written for other on-camera talent: still his writing. **Skip any doc
  titled DRAFT, DO NOT USE or NOT READY.** Sample the finalized ones; do not read all 40.
- **Content:** Dan says every Abs By AI / Daniel Rose Fitness content script was written by him. ⚠ The repo shows many
  of them started as Claude drafts that Dan then edited (for example `Docs/SCRIPTS_923_SHOOT_LONGFORM_DAN_EDITED_20260921.md`).
  So treat each FINISHED doc as Dan-approved words, and wherever the original Claude draft exists (repo, git history,
  `Handoffs/`, skill references) diff the two: the changes are the purest evidence of his voice. See the tiers below.
- **Content, which ones:** start from his most-viewed YouTube videos (list below), then the rest.
- **Not voice models:** the V2 long-form "Use AI To Get REAL Six Pack Abs - 6 Strategies That Work" and the AI ad
  "The Upload" (`ad-factory/the-upload/script.md`). Dan: not his best work. Already removed from the skills.
- **Out unless Dan says otherwise:** 2022 Gundry MD scripts.
- **Book (Tier A, required):** Dan's manuscript "15 Steps to Profitable YouTube Advertising", FINAL MANUSCRIPT,
  Google Doc `12wKH4OUzxbcNGv40YbnBx2DBUFXuRgcW1W19OsPewdk` (2019 to 2020). It is the longest pure sample of Dan's own
  writing: personal story openers ("Nine Years Ago on This Day... I was overdrawn, again"), fear then payoff, direct
  address to the reader. Read all of it through subagents (it is long). Three traps:
  - **The manuscript uses em dashes. Do not learn them.** The no-em-dash rule stands for everything written now.
    Quote book excerpts in the repo with each em dash rewritten as a comma, colon or period, and say so in the guide.
  - **It is a marketing book.** Learn the voice (story, rhythm, how he persuades), never the persona: on the page Dan
    is never a marketer or agency owner (WRITING-RULES section 2).
  - **Old personal facts.** Its life details are from 2019. Current facts come from memory
    `dan-personal-facts-for-scripts` only; never lift a fact from the book into a script.
  Dan has written other books too. If the starter prompt names more titles, read them the same way. Otherwise do a
  quick Drive search (`title contains 'manuscript'`, `fullText contains 'Chapter 1'`, `owner = 'me'`) and list any
  others found in the report without stalling on them.

## Tiers: whose words are they?

Most Abs By AI docs since July 2026 began as Claude drafts. Learning from Claude text teaches Claude to copy itself.
Sort every source into a tier before learning anything from it.

- **Tier A, Dan's own writing:** Social Response Marketing ad scripts; his outlines (for example "Abs By AI ad outlines -
  batch 1"); his shorts idea lists; his own drafts; the book manuscript; anything written before Claude worked on the project;
  doc comments and suggestions by danroseconsulting@gmail.com (`read_file_content` with `includeComments: true`).
  Highest weight.
- **Tier B, Dan's edits to a Claude draft:** before/after pairs. Second highest weight, and the best evidence for "what
  Claude writes that Dan cuts". The 2026-09-21 work is the model: `Docs/SCRIPTS_923_SHOOT_LONGFORM_DAN_EDITED_20260921.md`,
  `.claude/skills/scriptfromoutline/references/dan-edits-2026-09-21.md`, `dan-edits-2026-09-21-calories-pair.md`.
- **Tier K, borrowed technique (Keith, Wes):** structures and moves to copy. Never quoted as Dan's voice.
- **Tier C, Claude text Dan approved unchanged:** weak evidence; only confirms patterns from A and B.
  `.claude/skills/scriptwriting/references/finalized-ad-scripts.md` is probably here or B.
- **Exclude:** AI-generated ads, the ruled-out material above, docs written to editors about edits (covered by memory
  `revision-docs-in-dans-voice`).

Signals: em dashes, "Today we're talking about" openers and tidy three-item lists point to Claude. Wispr Flow
dictation quirks, his real numbers and run-on spoken phrasing point to Dan. If authorship is unclear, say so in the
inventory rather than guess.

## Top-viewed YouTube (@danrosefit, pulled 2026-10-06 with yt-dlp)

Views are small and some videos got paid traffic, so treat this as a hint about what landed, not proof.

- Long-form: My Top 10 Tips For Getting Six Pack Abs (At 40) `2T4LrQrmz9s` 13k; Ab Wheel: Most Underrated Ab Exercise
  `bkzT-3ENpoU` 2.6k; Your Belly Fat Is an Emergency `v2R4QpnURqA`. Skip the "Follow Along (No Talking)" and
  "Do It With Me" workouts: no script.
- Shorts: Jump Rope Without Tripping `LTkjlBr_3tg` 5k; 2 Minute Arm Pump `qDvrtKbuhf4` 4.4k; Toe Touch `I_IpdKpT2-0`
  2.7k; You Have 4 Ab Muscles `A8_uiK0D8nc` 2.6k; Supplements Are Only 3% `P9VUGyWeNtY` 2.3k; Never Start Your Day
  With Carbs `_Ep_hVPZYzE` 1.7k; Why I Skip Breakfast `UFga137pseM` 1.4k; Why Bodybuilders Suck Their Stomach In
  `QuswpGj635A`; Your Protein Shake Might Be Stopping Your Abs `B6Oku5GjrLs`; Milk Is Not A Health Food `YvfQfo9Qh4s`;
  Stop Doing Ab Exercises Until You Can See Your Abs `GVNzvm5sUbk`.
- Re-pull fresh: `pip install yt-dlp`, then
  `yt-dlp --flat-playlist --print "%(view_count)s|%(id)s|%(title)s" https://www.youtube.com/@danrosefit/shorts`
  (and `/videos`), sort by the first field.

Find each one's script doc on Drive by title. Early videos were filmed off the cuff with no script; for those the
voice is in what he said, not a doc.

## Cloud access, tested 2026-10-06

- **Works:** Google Drive connector (search, read Docs, Sheets, PDF, Word); Dropbox share links (swap `dl=0` for `dl=1`,
  `curl -L`, read the .docx with `python-docx`, already installed); yt-dlp channel listings with view counts.
- **Blocked:** YouTube captions and video downloads ("sign in to confirm you're not a bot"). So for the HBI ads and any
  off-the-cuff video, use the script doc, not a transcript. Also try Drive for `.srt` / `.vtt` files with the video's
  title. If a top video has neither, list it in the report as "needs a local transcript" and move on.
- **Drive sharing:** a cloud session can only share to an email address, so docs it creates stay private in Dan's Drive.
  That is fine here.

## Steps

1. **Read first:** `.claude/skills/_shared/WRITING-RULES.md`, memory entries (`Docs/memory/<name>.md`)
   `script-zero-edit-lessons`, `video-outline-style`, `dan-personal-facts-for-scripts`, `ad-copy-headline-voice`,
   `no-em-dashes`, and the "WHAT DAN CHANGED" section of `.claude/skills/scriptfromoutline/SKILL.md`. Do not re-learn
   what is already written down; extend it.
2. **Collect the sources.**
   - HBI sheet: read it, then fetch all 11 rows' scripts (Google Docs through the connector, Dropbox through curl).
     Rows 1 and 8 / 11 share docs; read each doc once.
   - Older ad scripts: Drive `search_files`, owner `me`, titles containing `ad scripts`, `ad outlines`, `vsl script`,
     `sales letter`. Pick about 8 finalized Social Response Marketing docs across years and products.
   - Abs By AI docs: queries on title and full text for `Abs By AI`, `Dan Rose Fitness`, `script`, `outline`,
     `teleprompter`, `shorts`, `VSL`, `sales letter`, `shoot`, `long form`, `hook`, 2025 on. Known starting points:
     `1r3Jmuihyryq0qv2Y3A--D_yaerF9B_ZqAb-QvOuAwjg` (ads batch 1 with filming notes),
     `1bpEndCcM-imeOWS0tp86l7Ud0bGyxLQ-MWZVAwcacgA` (batch 1 teleprompter only),
     `1AVRvxiINZ0EDkoFv77piXbg5xGuizHGuHE7vRVWXRKk` and `1n1FIVgNaBZZ6j0aJsEyqLAE8oT82SQQNJ_pGrCLVVwg` (Ads 2 to 15),
     `1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA` (/start VSL scripts),
     `1zCLn6pIuxGv4H1hkyieCk2T4NoYAQBnaNKMEFMcYV9o` (sales letter final copy),
     `1tTPTksuG_YwifjMWohtmXpelrjTFdo8KzjfxyuVvxq4` (9/23 shoot scripts), the ad outlines doc, each shoot's outline doc.
   - Book: `12wKH4OUzxbcNGv40YbnBx2DBUFXuRgcW1W19OsPewdk`, per the decision above.
   - Never edit any source doc.
3. **Read with subagents.** Big docs overflow context (batch 1 is 85k characters). Hand batches to subagents that
   return, per source: id, title, date, writer (Dan / Keith / Wes / Claude draft / unclear), format (ad, long-form,
   short, VSL, sales letter, outline, idea list, book), tier with reason, spend and CPA or views if known, and the
   Tier A, B and K passages verbatim (spoken words only, no cues or links).
4. **Save the raw text to Drive, not the repo.** The GitHub repo is still public and the HBI scripts are the client's.
   Create one Drive folder `Dan voice corpus (raw) 2026-10` with one Google Doc per source, so a later run never has
   to re-collect. The repo gets only analysis and short excerpts (about 150 words or less per HBI or Keith/Wes passage;
   Dan's own Abs By AI words can be longer, as `finalized-ad-scripts.md` already is).
5. **Write the inventory:** `Docs/VOICE_CORPUS_INVENTORY.md`, one row per source with the step 3 fields plus its Drive
   raw-copy id.
6. **Measure the baseline (feeds Part 2).** Write `scripts/voice/voice_stats.py`: given text files, report per 100
   words: "and" count, three-item lists ("X, Y and Z" / "X, Y, and Z"), questions, "you", contractions, swear words;
   plus average and spread of sentence length, words per paragraph, and how often paragraphs end on a one-line punch.
   Run it on five piles: Dan Tier A ads, Dan Tier A/B content, the book, Keith/Wes, and recent Claude drafts (Tier C plus the
   "before" side of Tier B). Save `.claude/skills/_shared/voice/STATS.md` with the table and the five biggest
   Dan-versus-Claude gaps. This is where Dan's sense that Claude says "and" too much gets proven or disproven with
   numbers.
7. **Write the example files:** `.claude/skills/_shared/voice/` with
   `ads.md` (hooks, problem, mechanism, proof and testimonials, offer, close; each excerpt labelled source, writer,
   spend/CPA), `content-longform.md`, `content-shorts.md`, `sales.md`, `outlines.md`, `book.md` (story openers, transitions, persuasion passages), `borrowed-keith-wes.md`
   (techniques with short excerpts, labelled borrowed), and `dan-edits-<date>.md` for each new before/after set.
   Words only, each passage labelled with its source id. Pick the best 15 to 25 passages overall, not everything.
8. **Write the guide:** `.claude/skills/_shared/DAN-VOICE.md`, at most about 1,500 words. Patterns ranked by evidence,
   each with two or three real quotes and the source. Sections: openers and hooks, sentence shape (with the STATS
   numbers), pet phrases, how he uses numbers and his own story, how he builds a mechanism, how he sells and closes,
   what to borrow from Keith and Wes, and "what Claude writes that Dan cuts". Mark anything backed only by Tier C as
   weak. Note the HBI audience (older, back and joint pain) differs from Abs By AI (men 35+ who want abs): copy the
   persuasion moves, not the topic or the age framing.
9. **Wire it in:** WRITING-RULES section 1, "Anything in Dan's voice" row points at `DAN-VOICE.md` first, and the
   ad scripts row's voice references line lists the corpus files that earned a place. Point the "Voice rules"
   sections of `scriptwriting`, `scriptfromoutline`, `shorts-scripting` and the voice parts of `ad-copy`,
   `ad-outlines`, `shortsideas`, `copy-edit` at the guide. Rewrite any voice trait the evidence contradicts (for
   example scriptwriting still lists "Listen", "Let's be honest", "here's the truth"; keep them only if Dan's own
   text uses them). Drop `finalized-ad-scripts.md` from the voice references if it lands in Tier C. Replace the
   pointer in `scriptwriting/SKILL.md` that names the old corpus handoff with one naming `DAN-VOICE.md`.
   Add memory entry `Docs/memory/dan-voice-guide.md` (what exists, where, when to read it) and its line in
   `Docs/memory/MEMORY.md`.
10. **Prove it, blind.** Hold out two real pieces the guide does not quote: one Social Response Marketing HBI ad and one
    Abs By AI content script (Tier A or B). Give a fresh subagent only the topic or outline plus the guide and examples,
    have it write each piece, and run `voice_stats.py` on both versions. Fix the guide once based on the gaps. Then
    put the real and generated versions of the Abs By AI piece in one Drive doc, unlabelled as A and B, with the
    answer key in the report only, so Dan can say whether he can tell which is his.
11. **Push.** Every new file: the em dash count (`grep -c` for the character) must be 0 (quoted old Claude text may keep its punctuation; the guide says
    never copy it). Cloud: plain git to `main` (clean checkout; `git pull --no-rebase origin main` first if behind).
    Local: `scripts/git/safe-push.sh -m "..." -- <files>`.
12. **Close out:** delete this handoff's row in `Handoffs/README.md` and its line in the HANDOFFS section of
    `AI_COORDINATION.md` (re-read the board from disk first; run `scripts/board-check.sh`).

## Report to Dan

In plain words: how many sources were found and how many were truly his; whether any other books turned up; the five
strongest voice patterns, one quote each; the three most useful Keith/Wes techniques; the STATS gaps between him and
Claude (including the "and" number); the blind test doc link; top videos that still need a local transcript; and any
source where authorship was unclear and his call would change the guide. Stop there. Part 2 (the AI-tell checker) is
its own task.
