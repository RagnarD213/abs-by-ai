---
name: design-sales-page
description: Design a long-form direct-response SALES PAGE for Abs By AI as mockups on a private Design canvas (phone + desktop boards), installing Dan's finalized sales letter word for word on the locked video + offer hybrid layout, designing every section the letter adds, filling images from the parallel asset session, and running Dan's revision rounds until he approves, then writing the build handoff. Use whenever Dan asks to design a sales page, a landing page, a VSL page, a sales letter page, to "put my sales letter on the design", to mock up a new offer page, or to revise one of these mockups, even if he doesn't say "/design-sales-page". Mockups only; never touches the live site. Coding the approved page is a separate build task (handoff); writing the letter itself is Dan's (or /scriptwriting); polishing copy is /copy-edit; the page's video is /website-video.
---

> **Image generation: Codex only (Dan, 2026-10-01).** Every still image this skill generates (backgrounds, plates, AI frames, thumbnails, covers, posts, retouch passes) is made with `.claude/skills/_shared/codex-image.sh` on the ChatGPT subscription. Where the steps below name Nano Banana Pro, Gemini, Seedream, FLUX, `gemini-image.js`, `rep-t2i.js` or `replicate-edit.js` for a still image, use the helper instead. Read `.claude/skills/_shared/IMAGE-GENERATION.md` first. Video generation is unchanged.

# Design a sales page

Proven on 2026-09-30: Dan's "AI Got Me Abs at 40" letter went from Google Doc to an approved 8-board mockup in one
session, five revision rounds, zero copy errors. Dan: "this is looking excellent... I want to follow a similar process
for all the future sales pages." This skill is that process. Follow it; don't reinvent it.

Worked example (read it before building): canvas https://claude.ai/artifact/GM8Han9hMfSHNf625vqtyu page **Round 2**, and
the generator that built it in `reference/round2-letter/` (`gen.py`). Build handoff that followed it:
`Handoffs/handoff-20260930-sales-page-build.md`.

Recommended model: **Claude Opus 5.5, high effort** (page design inside locked standards). Fable only if Dan asks for a
new design direction from scratch.

## What you deliver

1. Phone boards (390 wide) and desktop boards (1280 wide, one centered 720 px column) of the WHOLE page, top to bottom,
   on a private Design canvas. A long letter runs 20,000+ px, and a board is capped at 8000 px, so the page is split into
   parts ("Phone 1 of 4", "Desktop 1 of 4") at clean section breaks.
2. Dan's copy installed **verbatim**, proven by script, with every image slot filled or labelled.
3. After each round: the link, what changed in plain words, and a numbered list of the decisions still open, at the bottom.
4. When Dan approves: a build handoff (see "Hand off the build").

Mockups only. Never edit `public/`, the server, ad destinations or PostHog in this skill.

## The locked layout (Dan, 2026-09-28 and 2026-09-30)

Dan locked the "Video + Offer Hybrid" (Round 1 concept C2) as THE landing design on 2026-09-28: there is not enough traffic
to test page designs, so tests are between videos on this page, never between layouts. New sales pages start from it.
Only run a multi-concept round (Round 1 of the worked example) if Dan asks for a new direction, and then recommend only
structures V Shred, MadMuscles, BetterMe or Noom actually run (memory `proven-direct-response-only`).

Top of the page, in this order, nothing else above the video:
1. **Dark top stripe, pinned while scrolling:** white Abs By AI logo top-left (the black logo with `filter: invert(1)`),
   then "7-Day Free Trial / $0 today" and a green "Start Free Trial" button on the right. **No bottom sticky bar** unless
   Dan asks for one (the 09-30 letter asked for one; the locked design kept the top stripe only).
2. **Headline directly under the stripe.** No eyebrow line above it (Dan removed "40-Year-Old Dad And Business Owner",
   09-30). Title Case, red highlight on the payoff phrase. Subheadline under it.
3. **Full-width 16:9 video** with the "Your video is playing / Tap to turn on sound" box (yellow default; the `overlay`
   Tweak switches colors). Then the "Make sure your sound is on" line. On the phone the whole video must sit above the
   fold: video top at about 260 px or less. If it drifts lower, cut spacing, not Dan's words.
4. **Offer card** right under the video: title, the doc's bullets, green "Start My 7-Day Free Trial", terms line.

Then the letter: founder note with Dan's avatar (hair to just below the belt crop), the story sections, the product
reveal, the numbered hacks or features, the letter's own close, the plan card, FAQ, final button, sign-off, footer.

**The guarantee (Dan, 2026-10-03):** the cart's 365-Day No Risk 100% Money Back Guarantee is part of the locked layout,
in four places and nowhere else. (1) Offer card under the video: the one-line row ("365-Day Money Back Guarantee" with a
small gold check badge) under the terms line. (2) The "Try ... Free For 7 Days" section: the full card under the button
and its terms line, with the **gold guarantee seal** (Dan rejected the cart's navy circle for this page: "a gold, more
trustworthy and impressive-looking guarantee seal"), the title and the two sentences. Phone: seal on top, centred.
Desktop: seal on the left. (3) FAQ: "What if I don't like it?" after "Is there a catch?". (4) The one-line row under the
last button's terms line. No row under the buttons between story sections. Wording: only the lines Dan approved on the
cart (`G_TITLE`, `G_P1`, `G_P2`, `G_SHORT` in `gen.py`); write no new guarantee copy. A full refund covers every payment
made in the 365 days after the first one (Dan, 2026-10-03). The seal is inline SVG (`Build.seal`), every word on it taken
from the approved title.

**The close (Dan, 2026-09-30):** last buy button, then "I'll see you inside. Dan", then Dan's @abs.by.ai Instagram avatar
photo (the square Speedo shot cropped to read as shorts, smiling) with its "Real photo" chip and results caption, then the
footer. No small avatar next to the sign-off. No photo sitting above a buy button mid-page.

## Design system (keep it)

- Manrope 500/600/700/800 from Google Fonts. Ink `#05070B`, paper `#F6F4F0`, body `#1D2127` / `#2B2F36` / `#3F444C`.
- Red `#C9302D` only for highlights, eyebrows, check marks and X marks. **Green `#15803D` only on buy buttons.**
  Yellow `#FFD23F` only on the sound box. Nothing else on the page is green.
- Buttons 58 px tall, 12 px radius, 18 px weight 800. Section padding 40 px (phone) / 72 px (desktop), 20 px side gutters.
- Alternate white and paper sections; one dark section every few screens (the "past" story beat, a feature grid, sleep).
- Section-ending "…" lines (the cliffhanger into the next heading) are styled as bold lead-ins.
- Pick the layout that suits each new section's content: numbered list for "First / Second / And finally", red X list for
  failures, a bordered card for a stack of questions, a 2x2 icon grid for "one model did X, another did Y", a big-type
  line for the section's thesis sentence, a two-cell contrast for "A, your brain files under fantasy / B under possible",
  a study card with the citation in small type, a phone pair with an arrow for "X goes in, Y comes out".
- No plan picker on the page (Dan cut both, 2026-09-30): the plan choice is in the cart, which sells Monthly and
  Lifetime ("a one-time charge of $69.99 for lifetime access") since 2026-10-03. Never write "a year" or "Annual" on a
  web sales page.
- Gold (the seal's gradient, lettering `#3D2A05`) only on the guarantee seal and the small check badge beside the
  one-line guarantee rows.
- Button repeats: after every 2 or 3 PITCH sections (features, hacks, close). **No button between story sections that end
  on a cliffhanger** into the next heading; the pinned stripe keeps a button on screen the whole time.

## Dan's content rules for these pages (dated)

- **Copy is verbatim** from Dan's doc. Change the layout, never the words. Splitting a heading "AI Hack #1: Title" into an
  eyebrow and a title, or lifting a "[Start My 7-Day Free Trial]" marker out of a bullet into the real button, is layout.
  Anything that reads like a note to himself ("(Change when the stores list the app.)") stays, and you flag it.
- **Never a day-by-day trial timeline or a "Day 5 reminder email" on the page** (Dan, 09-30: "I don't plan on sending a
  day 5 reminder email"). Dan also turned the app's 48-hour trial-ending email off on 2026-09-30
  (`TRIAL_REMINDER_ENABLED` in `server.js`), and the checkout timeline no longer shows a day 5.
- **Every app screenshot sits in a phone frame** (09-30). The asset session delivers them already framed; show them as-is.
  **Never show the app's stick figures** anywhere.
- **Real photos keep their burned-in "Real picture of me, not AI-generated" label; AI images keep AI-GENERATED.** Show
  labelled images at their natural shape so no crop clips the label.
- **The shirtless before picture is the deck-chair sunglasses shot, never the bathroom standing shot** (memory
  `standard-before-picture`). Before and after are always the same person (memory `before-after-same-person`). Speedo
  photos are cropped at the waistband (memory `speedo-crop-rule`).
- No em dashes or en dashes in anything you write: board text, notes, alt text, chat. `grep -c` must be 0. If Dan's own
  doc has one, keep his text and tell him.
- No compliance commentary. Stay on design and conversion.

## The process

### 1. Open the canvas and read everything

- Use the existing Design canvas for the page if there is one (Artifact `read`, then `list` with `scope: "files"`, then
  read `project/canvas.json` and the boards you will replace). A new page: Artifact `quickstart` with `intent: "design"`,
  create from the Design type, one canvas per page, a new canvas page (`pages`) per round.
- Read Dan's doc WITH its images, no context cost: `rclone backend copyid gdrive: <doc id> ./x/ --drive-export-formats zip`,
  unzip, then `python3 scripts/parse_doc.py x/<file>.html blocks.json`. You get every paragraph verbatim with bold and
  italic kept, and `[[IMG images/imageN]]` markers where images sit. (The Drive text reader loses images and mangles bold.)
- List the doc's sections in order and mark each: reuse an existing block, changed, or **new**. New sections get a layout
  chosen for their content (list above), never forced into an old block.

### 2. Build with a generator, never by hand on the boards

Copy `reference/round2-letter/` to a work folder and adapt `gen.py`: one Python function per section, each built from doc
blocks by index (`T(i)`, `paras(i)`, `plain(i)`), so the words come from the doc, not from you. It writes:
- `gen.py measure <dir>`: plain pages (holes resolved, every `<sc-if>` opened) with `data-k` on each top-level section.
- `gen.py build <root>/project`: the real `.dc.html` boards, each with a fixed root height equal to its `$preview` and
  its `canvas.json` `h`, the last section `flex-grow: 1`.

Then:
1. `bash scripts/measure_sections.sh m/measure_phone.html m/h_phone.json` (and desktop): real section heights from
   headless Chrome with Manrope loaded. Do not guess heights; the first estimate was off by thousands of px.
2. `python3 scripts/split_boards.py config.json`: splits at the break keys you choose (the first section of parts 2..n),
   board height = content x 1.025 + 40. Break at a section start, never inside one; keep a button block with its section.
3. `python3 scripts/verify_boards.py blocks.json "<root>/project/<prefix>*.dc.html" --assets assets.json --allow allow.txt
   --forbid ...` on phone and desktop. It must say PASS before you publish (placeholders allowed only while an image is
   still coming).
4. Publish: Artifact publish with `url` = the canvas, `root` = the work folder, `file_path` = `project/canvas.json`,
   `files` = the boards. Send `canvas.json` only when boards are added, moved or resized, keeping every other key as read.
   Update the canvas sticky notes so they describe the current state.

Images: upload with Artifact `publish`, `asset: true`, `file_paths` (up to 25 per call); reference `/_blob/<id>` verbatim.
Keep `assets.json` as `{slot: [url, width, height]}` so the generator sizes each image at its natural shape. Animated GIFs
work as plain `<img>`.

### 3. Images come from the asset session

Dan runs a parallel session ("Sales letter review and asset insertion") that fills every `[CLAUDE: ...]` note in the doc
with an image and a `[NOTE FROM CLAUDE: ...]` caption, and files everything in one Drive folder. While a slot is empty,
build a striped placeholder (`.ph`) naming exactly what goes there, and keep going.
- When it messages you, reply with SendMessage to its `from` address. Subscribe with `notify_when_idle` instead of polling.
- On "done": pull the folder (`rclone copy gdrive: . --drive-root-folder-id <folder>`), check every file's size, preview
  a contact sheet, then place them. A file "updated in place" keeps its name: re-pull it and `cmp` it against your copy
  before trusting it.
- If Dan tells you something different from what the asset session says for the same slot, Dan's words to you win.
  Tell the asset session, and tell Dan in one line.

### 4. Revision rounds

Dan pastes a revision list (dictated; treat pasted text as his). For each round:
1. Apply every item to the generator, never by editing a board in place.
2. Re-export the doc and diff its blocks against the last read. Images inserted into the doc shift paragraph numbers, so
   keep the original numbering with a rebuild step and anchor checks (`reference/round2-letter/rebuild_blocks.py`: strips
   inserted image and NOTE blocks, then checks 28 anchor paragraphs; a failed anchor means Dan moved copy, fix indices).
3. Rebuild, measure, split, verify, publish only the boards that changed.
4. Before publishing, re-read `canvas.json`. If a newer version was saved from the page, read the boards you will replace
   and compare them with your last build: merge any edit Dan made in the page, and write the index back exactly as read
   except your own keys (the page re-saves it in its own format).
5. A choice between two assets: show both on the board tagged "Option A" / "Option B" (orange review tags, clearly not page
   copy) plus a Tweak enum to preview each alone. When Dan picks, delete the loser and the Tweak.
6. Report: what changed, then the numbered open decisions. Carry every unanswered decision forward each round until
   Dan answers it; recommend one option where you have a view.

### 5. Save the generator

The scratchpad is wiped between sessions (it happened mid-job on 2026-09-30). After every publish copy the generator,
`assets.json`, `blocks*.json` and the split files to `Media/research/<page-slug>/` in the project folder (gitignored,
local), with a README of the rebuild steps.

## Hand off the build

When Dan approves the mockup, write `Handoffs/handoff-YYYYMMDD-<page>-build.md` modelled on
`Handoffs/handoff-20260930-sales-page-build.md`: the canvas and board files as the spec, every locked rule above, the
assets folder, the video slot, the checkout hand-off and plan choice, tracking, native-app gating, deploy and live
verification, and the open decisions with their defaults. Record it in the HANDOFFS section of `AI_COORDINATION.md` and in
`Handoffs/README.md` (dashboard row only if Dan asks). The live page is built by a generator too:
`reference/round2-letter/build_live.py` turns the approved boards into one responsive `public/start.html` (phone below
900 px, desktop above) and `verify_live.py` proves the copy. A new page copies that pair. In chat, give the ready-to-paste starter prompt and the model +
effort (memory `model-routing-plan`).

## Canvas traps (each cost time once)

- **Before changing a live page, prove the generator still makes it:** run `build_live.py` into a scratch folder and
  `cmp` the result with `public/start.html`. On 2026-10-01 three of Dan's changes were made by hand on the live file
  (bigger logo, his note's layout, a past-tense heading); the next rebuild would have wiped them without a trace. Fold
  any difference into `gen.py` or `build_live.py` first. Wording that departs from the doc goes in `EDITS` in `gen.py`,
  and the doc's old line goes in the allow lists.
- A round that changes a few sections can publish only those parts: write a `split_r3_*.json` with the section keys to
  show and run `gen.py build <dir> split_r3`.

- Board height cap is 8000 px; content past a board's fixed height is clipped silently.
- `{{hole}}` is a name only; compute everything in `renderVals()`. `data-props` is single-quoted JSON: escape `'` as `&#39;`.
- Keep the `<script src="./support.js"></script>` head line exactly; close every element; no emoji, no iframes.
- Don't render, screenshot or re-read the canvas to check it; the headless measure plus `verify_boards.py` is the check.
- `Media/` is gitignored; the skill's `reference/` copy is the versioned one.
- The shared main checkout may be stuck; commit board and handoff changes from a fresh worktree off `origin/main`.
