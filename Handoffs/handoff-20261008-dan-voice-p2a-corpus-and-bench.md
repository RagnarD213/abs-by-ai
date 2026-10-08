# Handoff: Dan Voice Training P2A (real corpus, test bench, baseline)

Written 2026-10-08. Task name: `Dan Voice P2A Corpus + Bench`. **Run as a LOCAL task. Claude Opus 5.5, high effort.**
Use subagents for all reading and transcribing so the main context stays small. Spend: transcription a few dollars
(Replicate Whisper), Gemini judging up to $5. Nothing else metered.

This is Phase A of `handoff-20261008-dan-voice-training-part2-plan.md` (read its "What the research says" and "The
design" sections first; Phases B to D are there). It also carries the leftovers of
`handoff-20261006-dan-voice-training-part1-finish.md`.

If context reaches about half before the bench exists, stop after step 4, report, and hand off steps 5 to 7.

## Goal

1. Rebuild the voice corpus from material that is really Dan talking to an audience, sorted into his four types of
   writing.
2. Build a blind test bench and score today's guide on it, so every later change has a number.

## Dan's decisions (2026-10-08). Follow them exactly

- **Four types of writing, each trained on its own material:**
  1. **Content.** YouTube and every other platform; he says it is much the same across them.
  2. **Ads.**
  3. **Website conversion videos**, such as the VSL (the /start sales letter sits here too). Close to ads, but more
     important and he puts more time into them, so they are trained separately.
  4. **Products.** What the customer gets: The Sex God Method, The 15 Steps To Profitable YouTube Marketing, his Social
     Response Marketing product videos. Not VSLs, not the /start letter.
- **Never a source:** his dictation or prompts to Claude or any AI, and business email.
- **The Sex God Method** is, in his words, one of the best examples of how he communicates and of his writing style. It is
  how he talks to a regular consumer; 15 Steps is for a business audience. Of the two, The Sex God Method is the more
  relevant for products and for content.
- **Travel Like a Boss podcast** (his guest appearance): a very good example of him speaking off the cuff.
- **Old Six Pack Shortcuts videos with him in them:** usable, but long ago and a little dated.
- **Old channel** youtube.com/@danielrose-socialresponse7768: how he speaks off the cuff; the subject is business and
  marketing, so the topic differs.
- **Ad results:** HBI was the top account. He will send more numbers if asked.

Claude's standing rule on top: **text Claude drafted is never his voice, whatever he changed in it.** Only the lines he
changed are kept, as before/after pairs. Baseline numbers for a type come only from that type's Tier 1.

## Read first

`.claude/skills/_shared/DAN-VOICE.md` and every file in `_shared/voice/`; `Docs/VOICE_CORPUS_INVENTORY.md`;
`_shared/WRITING-RULES.md` section 3; memory `voice-corpus-sources`, `dan-voice-guide`, `swearing-never-cut-never-ask`,
`script-zero-edit-lessons`, `dan-personal-facts-for-scripts`.

## Step 1: leftovers from 10-06

Run steps 1, 2 and 4 of `handoff-20261006-dan-voice-training-part1-finish.md` as written (more ad scripts, the swearing
and controversy pass into `_shared/voice/profanity-and-controversy.md`, the seven raw copies the cloud refused, the
swearing contradiction between memory `swearing-never-cut-never-ask` and `WRITING-RULES.md` section 3, copying
`Docs/memory/dan-voice-guide.md` into the local memory folder). Skip its step 3. Two changes:

- **RO-14 is released from hold-out.** It is a Claude draft he edited, so it cannot stand as "real Dan" in a blind test.
  Its swearing lines may be quoted now. The HBI "Five Foods To Avoid" section stays held out, as an Ads item.
- The old channel's opinion videos (step 2) are prime evidence for the swearing and controversy pass. Read them for it.

## Step 2: build the corpus, one pile per type

| type | Tier 1 (the baseline) | Tier 2 (supporting) | Tier 3 (dated, lowest weight) |
|---|---|---|---|
| **Content** | (a) Abs By AI videos filmed from outlines with no script, finished cuts and raw rolls. (b) Old channel solo videos. (c) Travel Like a Boss episode 252, his side only. | His half of the Dan & Dani podcast. The Sex God Method. His own outlines. | Six Pack Shortcuts videos with him on camera. 15 Steps. |
| **Ads** | Ads he wrote and performed as himself: Abs By AI Ads 1 and 3, his typed lines in the other batch-1 ads, any ads he ran for his own book, course or agency, as filmed. | Ads he wrote for other presenters (HBI, Spy Briefing, CPA offers, Physio Tru), weighted by spend and CPA: structure and persuasion, not voice numbers. | |
| **Website conversion videos** | His own sales videos and letters: the 2019 consulting sales video, the 2019 DR marketing website VSL, the Black Belt sales video outline and cart page script, his Abs By AI VSL outline, his own sections of the /start letter, the book funnel copy and pre-order video outline. | The 2025 Fujiyama VSL (written for another presenter): structure only. | |
| **Products** | The Sex God Method (lead example). His Social Response Marketing product videos (the Black Belt course). | 15 Steps (business audience). | |

Where things are:

- **Outline-filmed Abs By AI videos.** SRTs already in the project: `claude edited long form content/01 - My First Spray
  Tan/FINAL_spraytan.srt`, `02 - My Honest Zepbound Update/FINAL_zepbound.srt`, `03 - The Supplements I Actually
  Take/FINAL_supplements.srt`, `04 - Why You Should Invest More In Your Health/FINAL_invest_health.srt` (20,800 words
  together), plus `Media/codex-video-trial/03-organic-abwheel/FULL_AB_WHEEL_v4b.srt`. Still to transcribe or convert:
  Top 10 Tips `2T4LrQrmz9s`, the ten shorts listed at the end of the inventory, the Oura review SRT, and the Stop
  Deadlifting and Keep Your Muscle SRTs on Drive. For each video confirm from its shoot doc that it was filmed from an
  outline; anything read from a teleprompter script is out. Raw rolls: 902 word-level transcripts in the project and on
  `/Volumes/Extreme`.
- **Old channel.** 42 videos from about 2020 to 2021, 12,800 subscribers. Of the 30 counted: 23 solo (about 380 minutes,
  roughly 60,000 words) and 7 Dan & Dani podcast episodes (about 260 minutes; needs speaker separation, keep only him).
  Use YouTube's captions where they exist, otherwise download the audio and run the project's Whisper path
  (`/youtube-packaging` step 1, or `.claude/skills/_shared/whisper-to-scribe.py`). The installed `yt_dlp` (2025.10.14)
  listed the channel but failed on single videos on 10-08: `pip install -U yt-dlp` first.
- **Travel Like a Boss, episode 252,** "Daniel Rose (Internet Marketing Multi-Millionaire)", 2020-07-06, 1 h 18 min:
  `podcasts.apple.com/us/podcast/ep-252-daniel-rose-internet-marketing-multi-millionaire/id727446851?i=1000482873048`.
  A second guest spot turned up in search ("Scaling Your Business Through YouTube Advertising with Daniel Rose", on
  Audible); confirm it is him before using it.
- **The Sex God Method:** PDF on Drive `1KVRHZ04oGliUoQd9EISUl0DySIVTu-C3`. A second file, `sgm.pdf`
  `1NlsoD4c-ieqB-alkjHI38d6HnQj21rni`, is unread: find out what it is (if it is the book's sales page, it belongs under
  website conversion). It is an old book: learn how he explains, motivates and talks to the reader, not its punctuation
  or its dated facts. For the example files in the repo, pick passages on mindset, method and motivation and skip the
  explicit ones, which do nothing for fitness writing.
- **15 Steps:** final manuscript `12wKH4OUzxbcNGv40YbnBx2DBUFXuRgcW1W19OsPewdk` (already copied, see inventory).
- **Product videos:** Drive folder "Black Belt Videos - Send To Customers Until Site Is Fixed"
  `1X9dliVnqj9TNCDIwvCPrmTJvUXcSnlhv`, plus loose files "EXPLORATION DRILLING STRATEGY"
  `1LAhluCuztp49pPiFbUlZzS_emy-AyrEv`, "VIDEO 6 - LTV" `11TjBBJzzJ253hAoK3H-R8CwPXqra0xnD` and "Welcome to Ad
  Management Black Belt" `1HfhP0rNoHqHNJOvttcjnHi-MBbIdYKdv`. Transcribe at least four. Dan's dictated note about these
  was garbled ("I might actually just delete those"): **delete nothing**; confirm in the report that these are the
  product videos he meant.
- **Conversion and ad documents:** ids are in `Docs/VOICE_CORPUS_INVENTORY.md` and in step 1 of the 10-06 handoff. The
  /start VSL scripts doc and VSL Version A and B are Claude's writing: pairs only, never voice.
- **Six Pack Shortcuts:** find up to five videos with him on camera (YouTube search). Ten minutes at most; if nothing,
  ask him for links in the report. Keep a pattern from these only if it also shows up in 2026 material.
- **Unconfirmed:** "YouTube Ad Scripts Portfolio For Daniel Rose" `1QAEr2M07HapKXT5vnj6n4ZxspN9Q42KXNmIvqMLBjBU` (owned
  by someone else). Ask him whether the scripts in it are his before using it.

Rules for every pile:

- Tag each source with type, tier, year, spoken or written, and audience (consumer or business).
- Old-channel and Black Belt business vocabulary is filtered out of the word lists. Sentence shape, small words,
  transitions, openers and how he states an opinion count in full.
- Weight 2026 material highest. An older pattern is kept only if it also shows up in 2026.
- **Free pairs:** for every teleprompter video, diff the script against what he said on camera. Each line he changed
  while reading is a correction. Store them with the edit pairs.
- If Dan records off-the-cuff takes at the 10/17 shoot before reading Claude's scripts for the same outlines, those
  become the core of the Content hold-out. Optional; he has not committed to it.
- Raw text stays out of the public repo: local folder `voice-corpus/` (add it to `.gitignore`), mirrored to the Drive
  folder `Dan voice corpus (raw) 2026-10` (`1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`). Update the inventory with every
  source, its type and tier.

## Step 3: re-measure

Rebuild `_shared/voice/STATS.md` with one baseline per type, from that type's Tier 1 only. Add to
`scripts/voice/voice_stats.py`, or a sibling script:

- small everyday words per 1,000 ("actually", "really", "very", "kind of", "stuff", "things", "going to", "which",
  "because"). A first pass on 10-08 found Claude-drafted scripts carry almost 3 times his "actually" and half or less
  of his "really", "very", "kind of", "stuff" and "things";
- a function-word fingerprint (Burrows' Delta, `pip install faststylometry`, pooled samples of 2,500+ words);
- one style embedding (LUAR, `rrivera1849/LUAR-MUD`).

Always report a ceiling (Dan against Dan, the pile split in half) and a floor (Dan against cold Claude, and against one
other fitness creator's transcript).

## Step 4: update the example files (light touch)

Add real passages from the new sources to `_shared/voice/` so the current skills gain at once: a file each for content,
ads, conversion and products, whole passages of 150 to 500 words, labelled with source and tier. Do not rewrite
`DAN-VOICE.md` beyond the swearing section; the rebuild is Phase B.

## Step 5: hold-out set

40 passages of pure Dan, 150 to 450 words, never quoted in any guide or example file: about 16 content (10 long-form,
6 shorts), 10 ads, 6 conversion, 8 products; fewer where the material is thin, and say so. List them in
`_shared/voice/HELD-OUT.md` by source and position, not by text. Write `scripts/voice/heldout_guard.py`: it fails if any
file under `_shared/` contains an 8-word run from a held-out passage. For each passage write a content-only brief: the
facts and the point in neutral words, none of his phrasing.

## Step 6: the bench

`scripts/voice/bench.py`:

1. A fresh subagent writes each brief under a named setup (it sees only what that setup allows).
2. Each judge, a fresh Claude subagent and Gemini (`GEMINI_API_KEY` is in `~/.absbyai-secrets.env`), sees 8 real
   reference passages of the same type that are not held out, plus one real/generated pair in random order. It picks
   the AI one and says why.
3. At least 80 trials per setup. Output to `Docs/voice-bench/<date>-<setup>.md`: judge accuracy overall and per type,
   the reasons tallied by cue, Delta and LUAR against ceiling and floor, the stats gaps.

## Step 7: baseline and Dan's blind page

Score two setups: cold Claude with no guide, and today's guide. Then build a private page with 20 pairs (8 content, 5
ads, 3 conversion, 4 products) where Dan clicks which one is his and can say why, with votes saved, shareable to two or
three people who know him. The answer key goes in the chat report only.

## Finish

- Update `Docs/VOICE_CORPUS_INVENTORY.md`, memory `dan-voice-guide` (local, then `scripts/sync-memory-to-repo.sh`) and
  `Handoffs/README.md`. Re-read `AI_COORDINATION.md` from disk, swap this handoff's line for the Phase B line, run
  `scripts/board-check.sh`.
- Zero em dashes in every new or edited file. Push each shared file with `scripts/git/safe-push.sh` as it is edited.
- Check every path the guide and skills mention exists in the repo.

## Report to Dan

Plain words: words collected per type and tier, and where each type is thin; the swearing rules in five lines with one
real quote each; the two baseline scores (what Part 1 bought over cold Claude) with the top five reasons the judges
gave; the blind page link; the open questions (the product videos, `sgm.pdf`, the scripts portfolio, Six Pack Shortcuts
links, the three authorship questions from the 10-06 handoff); the starter prompt for Phase B.

## Starter prompt

> Run `Handoffs/handoff-20261008-dan-voice-p2a-corpus-and-bench.md`. Name this task `Dan Voice P2A Corpus + Bench`. Use
> subagents for the reading and transcribing. Extra ads, results numbers or recordings from me: [links or "none"]. End
> with the baseline scores and my blind test page.
