# Handoff: finish Dan Voice Training Part 1 (swearing pass, more sources, blind test)

Written 2026-10-06. Task name: `Dan Voice Training P1 Finish`. **Run as a LOCAL task** (Dan's choice, after his limit
resets). **Model: Claude Opus 5.5, high effort.** Use subagents for the reading so the main context stays small.
Spend: Drive reads are free. Transcribing videos may use Replicate Whisper (a few dollars at most, inside the $25
session cap). No other metered spend.

## Goal

Part 1 built the voice guide in the cloud (`.claude/skills/_shared/DAN-VOICE.md`, examples in `_shared/voice/`, numbers
in `_shared/voice/STATS.md`, sources in `Docs/VOICE_CORPUS_INVENTORY.md`, memory `dan-voice-guide`). This task finishes
it:

1. **A swearing and controversy pass.** Dan (2026-10-06): swearing is good in his videos, but Claude imitates it
   clumsily. Learn exactly how he uses profanity and offensive or controversial language, and teach that.
2. **More source material.** Dan has many more scripts and content videos than Part 1 read.
3. **The blind test** Part 1 skipped to save cloud credit.
4. **Train BOTH cloud and local sessions** (Dan's explicit requirement). See "Cloud and local" below.

## Cloud and local: where everything must land

Cloud sessions see only what is committed to the repo; local sessions also load the local auto-memory folder. So:

- Every rule, example and number goes in **repo files**: `DAN-VOICE.md`, `_shared/voice/*.md`, the skills, `Docs/`.
  Never only in local memory, `~/.claude`, the scratchpad or chat.
- Memory entries: write or update them in the **local** auto-memory folder, then run `scripts/sync-memory-to-repo.sh`
  so `Docs/memory/` matches. Also copy `Docs/memory/dan-voice-guide.md` (written in the cloud) **into the local memory
  folder** and add its index line there, since the sync script only copies local to repo, never back.
- Raw source text and new transcripts go to the Drive folder `Dan voice corpus (raw) 2026-10`
  (`1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`), set to anyone-with-link view (memory `drive-always-public`), not to the
  repo (it is public, and the HBI scripts are the client's) and not only to the Mac.
- Before finishing, check that every path the guide or the skills mention exists in the repo:
  `grep -o '[A-Za-z_./-]*\.md' .claude/skills/_shared/DAN-VOICE.md | sort -u` and `ls` each one.
- Push with `scripts/git/safe-push.sh -m "..." -- <files>` (local rule). Push each shared file the moment it is
  edited (AGENTS.md, 2026-10-05).

## Read first

`DAN-VOICE.md` and every file in `_shared/voice/`; `Docs/VOICE_CORPUS_INVENTORY.md`; `_shared/WRITING-RULES.md`
section 3; memory `swearing-never-cut-never-ask`, `script-zero-edit-lessons`, `video-outline-style`,
`dan-personal-facts-for-scripts`; in `.claude/skills/scriptfromoutline/SKILL.md` the sections WHAT DAN CHANGED (G and
H), "BE CONTROVERSIAL. SWEAR." and "Dating & relationship advice register"; the swearing and bluntness lessons in
`.claude/skills/shorts-scripting/SKILL.md`. Do not re-learn what is written down; extend it.

## Step 1: collect more source material

Ask Dan once, at the start, for any folders or doc links he wants included (the starter prompt has a slot). Then,
without waiting:

- **Content he wrote or said, most valuable for swearing:** off-the-cuff videos. Transcribe the top videos Part 1
  could not read (list at the end of the inventory: Top 10 Tips `2T4LrQrmz9s`, Ab Wheel `bkzT-3ENpoU`, and 10 shorts)
  from the local video files in the project folder or the Extreme drive, with the project's Whisper path (see
  `/youtube-packaging` step 1, or `.claude/skills/_shared/whisper-to-scribe.py`). Also convert the two SRTs already on
  Drive (Stop Deadlifting `1NeSaKftqqXs3VlZwoY6iz0stOghaOrBm`, Keep Your Muscle `176MKh1QPa83ziaDAoEFqF0xZiNfjcXu3`).
  Any other finished Abs By AI or Daniel Rose Fitness video with Dan talking unscripted counts as Tier A spoken.
- **More ad scripts:** Part 1 read 10 of about 115 Social Response Marketing docs. Read 8 to 12 more finalized ones,
  starting with: Spy Briefing Aug 2024 FINALIZED `1NHm51ndaKaNFiTM0kgNAZ4QSvrJr6I_s9Q91Nj0XnRY`, HBI scripts adapted
  from emails 2024 `1Jvr7oaoyJ1I1J2eLP7C4I6qaPT2ulutHrtNbpP35cLc`, Dennys UGC HBI 2025
  `1x0v6ESe367gORqO_-LfhNsydEkYfpRZ4ClmxqrOpCqw`, Black Belt cart page script `1HyLS5nVGxi_I34AAD9BR3hAiGi6lpeJoeAVhVK_09fo`,
  DR marketing website VSL 2019 `1qvU-4gQUQG0OW88MxSy104lsNe7EH1z4biCEw_Dcf3I`, Dan's VSL outline
  `1y4ZrYoehmh54IQf0Hayv_krkG1K0NZjVVN8ZNrADX8w`, "Dedicated Shorts Ads Scripts" `1huBqiKl2jJr0DgeFiEXU31kL3DU1JYeNVl-1OoYWs6M`
  and "Approach #2" `1mqgnFYHDugEYDErNXqzWcPxUVRPStmxiXPU0HgNETS0`. Same skip rules as Part 1 (DRAFT, DO NOT USE,
  NOT READY, Gundry 2022, Keith/Wes as Dan).
- **Tier everything** with the Part 1 method (inventory, "How to tell Dan's lines from Claude's": curly apostrophes =
  Dan typed it; his typos; spaced hyphen). Add rows to `Docs/VOICE_CORPUS_INVENTORY.md`.
- **Make the seven raw copies the cloud session's permission check refused** (listed as "denied" in the inventory) into
  the Drive folder, and fill in their ids.
- **Keep the two blind-test pieces out of everything you write until step 3 is done:** the HBI "Five Foods To Avoid"
  section of `1nCn7t0bF3aC0GrJZiG04UD26TRl86EhWCCR4EY_XAUQ` and the RO-14 "Why You're Not Losing Weight" final in
  `1tTPTksuG_YwifjMWohtmXpelrjTFdo8KzjfxyuVvxq4`. RO-14 has some of his best profanity ("bullshit story", "fat wife"),
  which is exactly why it makes a good test: do not quote it in the swearing file until the test has run.

## Step 2: the swearing and controversy pass

**What Part 1 measured:** Claude swears MORE than Dan, not less (Claude content 0.08 swears per 100 words; Dan's
edited finals 0.05; his own Tier A content 0.03). The problem is placement and aim, not volume.

**What is already known (extend, don't repeat):** a swear survives when it is aimed at mainstream advice or an
institution inside a full sentence ("that advice is bullshit", "useless bullshit anyways", "half-ass this for years",
"stressed out as hell"). A swear bolted on as its own sentence or punchline gets cut ("It's bullshit.", "Glycine is not
going to do shit for you."). Swears aim at advice, never at a group of people (memory `script-zero-edit-lessons`).
He softens insults aimed at the viewer and hardens claims aimed at the problem (`voice/dan-edits-2026-10-06.md`).
Older agency ads used milder words ("lying ass dating experts", "dieting sucks"); the book says "piss a lot of people
off", "save your ass", "shitty".

**Do this:**

1. Have subagents pull EVERY swear and every offensive or controversial line from all Tier A and B sources (old and
   new), plus every swear in Claude drafts with what Dan did to it (kept, cut, changed). Record for each: the line,
   source, tier, format (long-form, short, paid ad, organic ad, letter), and:
   - **word and strength** (mild: hell, ass, sucks, crap; strong: shit, bullshit, fuck);
   - **target** (bad advice, an industry or institution, experts, an excuse or habit, the viewer, a group of people,
     himself, a thing);
   - **position** (inside a full sentence, end of sentence, standalone sentence, opener);
   - **job** (contempt for advice, emphasis on a stake, self-deprecation, honesty signal, humor);
   - **controversial claims:** the stance, how he states it (flat, no apology, no "I know how that sounds"), and how he
     backs it (his own fact, a consequence, a number).
2. Measure rates per 1,000 words by format and by tier (extend `scripts/voice/voice_stats.py` with a per-target
   breakdown only if it is simple; otherwise tally by hand).
3. Write `.claude/skills/_shared/voice/profanity-and-controversy.md`: the rules ranked by evidence, the real lines
   that show each (labelled), the Claude lines he cut beside what he wrote instead, the rates per format as targets, and
   a short "where a swear belongs in a script" checklist. Paid ads stay clean (Google reviews them).
4. Rewrite `DAN-VOICE.md` so it carries a short swearing and controversy section pointing at the new file (keep the
   guide at about 1,700 words or less), and update the "BE CONTROVERSIAL. SWEAR." section of `scriptfromoutline` and
   the shorts-scripting swearing lessons to match.
5. **Fix a contradiction on record:** memory `swearing-never-cut-never-ask` says "the separate scripting guidance on not
   writing profanity into new scripts is unchanged", while `WRITING-RULES.md` section 3 says to write swears where he
   would in organic content. Dan's 2026-10-06 instruction settles it: swearing belongs in organic scripts, done his
   way. Update the memory entry's last line and WRITING-RULES section 3 to say so.

## Step 3: the blind test

Run it after steps 1 and 2, so it tests the finished guide.

1. Confirm the guide and every `voice/` file quote neither held-out piece (grep for distinctive lines).
2. Give a FRESH subagent only `DAN-VOICE.md`, `_shared/voice/`, `WRITING-RULES.md` and memory
   `dan-personal-facts-for-scripts`, plus (a) a brief for the HBI ad: "Five Foods To Avoid If You Have Arthritis", read
   by Jesse Cannone (owner of HealthAndWellnessTools.com), reveal tomatoes and solanine, hold back four, free
   presentation normally $49.95, "Watch Now", about 500 words; and (b) Dan's outline "5. Why You're Not Losing Weight"
   from `1ND_BTQKfIIBdfBC_WJGhxc_SZHtQFh32HI3ksD_dIVo` (bullet outline only, not Claude's 09-19 script). It writes
   both pieces.
3. Run `voice_stats.py` on real and generated versions of both, and compare the swears line by line for RO-14. Fix the
   guide once from the gaps.
4. Put the real and generated RO-14 scripts in one Google Doc as "Version A" and "Version B" in random order, no labels,
   anyone-with-link view. The answer key goes in the chat report only.
5. Once the test is done, RO-14 may be quoted: add its best swearing and controversy lines to the new file.

## Step 4: finish up

- Re-run `STATS.md` with the bigger corpus (same piles, new sources added) and update the five gaps if they moved.
- Update memory `dan-voice-guide` (local, then sync), the inventory, and `Handoffs/README.md`; delete this handoff's
  line in the HANDOFFS section of `AI_COORDINATION.md` (re-read it from disk first; run `scripts/board-check.sh`).
- Zero em dashes in every new or edited file (grep -c for the em dash character; must be 0).

## Open questions from Part 1 to put to Dan in the report (don't block on them)

- Is HBI row 11 ("Five Foods To Never Eat If You Have Arthritis | MARK", $48.14 CPA) the "Seniors having fun" section
  of the Mark doc? Part 1 matched it by inference.
- Did Dan write the Make Time shorts hooks ("No time to work out? I'm going to solve that problem for you")? If yes,
  `_shared/HOOKS.md` should list problem-plus-promise as a first-class hook beside its surprising-claim hooks.
- Was the "What Five Leading Specialists" section of the Mark doc his?

## Report to Dan

Plain words: how many new sources, how many truly his; the swearing rules in five lines with one real quote each, and
how Claude's swearing differed; the blind test doc link and which version was his; the STATS changes; confirmation that
the repo files, `Docs/memory/` and the local memory folder all carry the new material; the open questions above.
