CONTENT | SL-06 | Top 5 Zepbound Tips SFL R3

# SL-06 round 3: AI flex intro on all six, real thigh-injection clips in C, rebuild, gate, review

Written 2026-10-17 by Claude (Opus 5.5), from the round-2 task after Dan's reply. **Recommended: Claude Opus 5.5, high
effort.** (New AI frames and motion with retakes, sourced third-party footage, six re-renders and the full gate chain.)

## Dan's reply (2026-10-17, verbatim copy)

`/Volumes/Extreme/_edit_work/sl06/round2/DAN_R2_NOTES.md`. Read it in full; the summary below is the editor's reading.

## What Dan approved

- **D is approved except one change** (the new intro). For A: "everything else in that is approved". Read as approval of
  every round-2 decision as built: **GLP-1 Tips** title band, the title copy, one step at a time in C and E, B's long
  pickup wording, pickup sound A (the fitted EQ), the key-point copy. Record this in `/Volumes/Extreme/_edit_work/sl06/decisions.json`
  (create it) with his words.
- Round 2's C AI frames (thigh injection) and E roof gag were not approved: C's opening becomes the flex intro below; E keeps
  its staircase ending. Put E's ending in one line on the R3 page, not as a decision.

## The work

### 1. An AI flex intro clip on all six (start and end frames first, then motion)

Each intro covers the opening line: A to E their recorded pickup (A 0 to 4.14 s, B 0 to 4.61, C 0 to 2.84, D 0 to 3.27,
E 0 to 3.15); F its first line (0 to 2.5 s, replacing the sliced-chicken clip). Every intro: AI-generated Dan (his
likeness from real reference photos, lean and shredded, not bulky, same face; check the face reads as him), shirtless or
in his usual tank as the references show, a tiny Zepbound vial held between thumb and index finger, a poster behind him
with the exact text, the poster legible in the 9:16 frame. AI-GENERATED chip on every intro (placed off face and body).

| | Pose | Background | Poster text (exact) |
|---|---|---|---|
| D | Front double biceps, a tiny Zepbound vial in EACH hand between thumb and index finger | a calendar with every Thursday circled on one side, the poster on the other | Inject Zepbound Thursday evening |
| A | One arm flexed, vial between thumb and forefinger; the other hand (not flexing) points at the poster | poster behind him | Start at 1 mg, not 2.5 mg |
| B | One bicep flexed holding the vial; other hand points at the poster | poster | Use a needle, not a KwikPen |
| C | One bicep flexed holding the vial; other hand points at the poster | poster | How to inject Zepbound |
| E | One bicep flexed in the foreground holding the vial; (point at the poster as in A to C) | poster | Come off Zepbound without regaining fat |
| F | One bicep flexed in the foreground holding the vial; (point at the poster as in A to C) | poster | How much protein do you need on a GLP-1? |

- Dan's own wording for A reads "with my other hand... I'm holding the Zepbound vial. I point at the poster": the flexing
  hand holds the vial and the other hand points. Use that for A to C; E and F say only "one bicep flex with the Zepbound",
  so the pointing hand is the editor's reading (keep it consistent across the batch).
- **The title band comes off during the intro clip and returns on the first film frame** (Dan's words for D; the poster
  carries the title). Apply it to all six and say so in "What I decided". Captions and the disclaimer stay.
- Frames: Codex on the subscription (`_shared/codex-image.sh --model gpt-6.1-sol --effort high`, `_shared/IMAGE-GENERATION.md`),
  real Dan photos as reference only (`photos/finalized social media photos/`, cutouts in `_cutouts/`; no frowning photo).
  End frame: the same scene a beat later (the flex squeezes, the pointing hand lands on the poster); motion about 3 to 4.6 s,
  matching each head length. Generate in 9:16 with the poster and the vial in the middle band (title band y 0 to 310 is
  hidden during the intro, captions from y 1412 stay).
- Every pair: frame spec, `_shared/framecheck/gate.py`, a fresh `frame-reviewer` agent per pair and per retry; the page
  refuses pairs without both (`gate.py --verify`). Check: vial size real (a small single-dose vial, readable as Zepbound
  without inventing a fake logo), fingers, the poster text spelled exactly, the calendar's Thursdays (D).
- **Stop for Dan's frame approval before any motion** (VIDEO-RULES: frames before motion). Put the six pairs on the R3 page
  with the round-2 shorts. After his yes: motion on the Google Flow subscription through the `flow-veo` agent
  (`_shared/veo/README.md`, `veo.py add`), motion gate (`clipcheck.py`) and a fresh reviewer per take, then build.

### 2. C: real thigh-injection clips from YouTube, credited

- At "Inject into your thigh on the outer front part" (C about 0:06, film 167.6 on; currently Dan on camera with Step 1),
  a real clip of someone pinching the thigh and injecting into it (preparation, pinch, needle in). Credit the source
  (channel name, "YouTube") small in the lower right-hand corner for the whole clip, clear of the captions.
- "In the beginning", several different real Zepbound thigh-injection clips, each credited the same way. Editor's reading:
  the intro flex clip keeps 0 to 2.84; the montage covers "This takes about 10 seconds once you know what you are doing"
  (2.84 to 5.77, replacing the hand drawing from a vial), then the pinch-and-inject clip runs into "Inject into your thigh".
  Prefer needle-and-vial or insulin-syringe injections (the short teaches a needle); pen injections into the thigh are
  acceptable for the montage if few needle clips exist. No belly injections.
- Find them with YouTube search (in-app browser), download with `python3 -m yt_dlp` (installed), cut only the seconds used,
  colour correct to sit with Dan, keep full height in a card if horizontal (VIDEO-RULES), and record the source URL,
  channel and timestamps in `clips/youtube_sources.json` and on the page. Dan's explicit pick: execute it as asked.
- Re-check C's B-roll share and caption-on-cut behaviour after the change.

### 3. Rebuild, gate, review, page

- Build on round 2 (`/Volumes/Extreme/_edit_work/sl06/`, tooling and lessons in `.claude/skills/shorts/reference/softblue-sl06/README.md`,
  "Round 2" section: render_queue.sh, deliver_watch.sh, gate_queue.sh, make_joins.py, page_r2.py). New folder `round3/`;
  never overwrite `round2/`. `batch.py` needs: covers that hide the title band (a cover flag such as `noband=True`, used by
  `finish`), and the credit line for the YouTube clips (a small Soft Blue chip, lower right, above the disclaimer).
- Each changed short: render, `deliver_watch.sh`, a fresh watch judge (Sonnet), `gate.py --format short` (39 rows), then one
  fresh `ra-reviewer` on all six. Watch the AI label rows: every short now carries an AI clip (`ai_inserts` + chip box in the
  gate plan); all six get the AI flag at setup.
- R3 page on a new port (8819 is round 2's; keep it until Dan finalizes): the six intro frame pairs first (stage 1), then
  after motion the six finished shorts, the C injection clips with their credits, "What I decided", checks, one reply box.
  Copy finished shorts to `Videos to Review/` as `Top 5 Zepbound Tips SFL R3 - short <S> - <title>.mp4` and delete the R2
  copies of that short when its R3 copy lands. Later-round rule: list each change with its timestamp and a watch range.

## State at handoff

- Round 2 delivered and gated (all six PASS at 2.6.1; re-review: A to E ship, F's curls clip fixed after). Files:
  `Short-form video content/zepbound-tips-short1..6_*.mp4`, notes `notes-SL06.md`, recipe `recipe-SL06/`. Page
  http://127.0.0.1:8819/. Queue SL-06 `delivered` (set to `in_progress` when R3 starts).
- Two local commits from round 2 (b1e35a1, 2a22a47, plus the board note 016500c) wait on main: safe-push was blocked by
  other sessions' live edits. Run `scripts/git/safe-push.sh` with this task's files; it carries them.
- Spend so far about $0.10 (Gemini listens). AI motion goes on the Flow subscription, not paid.

## Open risks

- Dan's likeness: Codex redraws people; check the face against a real photo before the page, and regenerate if it does not
  read as him (thumbnail option 3 precedent, VIDEO-RULES 2026-10-13).
- Poster and vial text: image models misspell. Check every letter; regenerate rather than patching text by hand.
- YouTube rate limits (reaction-clips SKILL, line 152). Keep downloads few and short.
- E is 58.0 s; its intro replaces the scale clip at the same length, so the length does not change.

## Starter prompt

> Name this task "Top 5 Zepbound Tips SFL R3". This is CONTENT. Read `Handoffs/handoff-20261017-sl06-round3-flex-intros-and-thigh-injection-clips.md` and `/Volumes/Extreme/_edit_work/sl06/round2/DAN_R2_NOTES.md`, then execute it: make the six AI flex intro frame pairs (Codex subscription for the images), gate and review them, and put them on a new review page for my approval; source and credit the real thigh-injection clips for short C. After I approve the frames, make the motion on my Google Flow subscription, rebuild the six shorts with the title band off during the intro, run the gates and an independent review, and give me one page. No covers, no upload.
