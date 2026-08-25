# Handoff: Finish YouTube channel setup (Shorts metadata/scheduling + long-form thumbnails)

**Date:** 2026-08-11
**Project:** Abs By AI
**Business goal this serves:** Marketing performance → app adoption. The whole back catalogue
(7 long-form + 28 Shorts) is uploaded but most of it is sitting in draft with no titles, no
descriptions, no tags and no publish dates. Every day it stays unconfigured is a day the
channel produces zero traffic to absbyai.com.

## Objective

Finish configuring the Abs By AI YouTube channel. 11 of 28 Shorts are fully set up and
scheduled; 16 remain (plus 1 blocked on a copyright claim). Two of five unpublished long-form
videos have their thumbnail A/B tests set; three still need thumbnails built and installed.
Plus four small cleanup items. **All the copy is already written** — this is execution, not
authoring.

## Current State

### Uploads — verified complete, nothing to re-upload
- **Long-form 7/7 uploaded.** Titles, descriptions (with `utm_source=youtube&utm_medium=video`
  links) and chapters were already done on all seven before this session. Sunday cadence already
  in place.
- **Short-form 28/28 uploaded.** Mapping from local file → YouTube id is **certain**, not
  inferred: every Short's edit page shows its source filename, and all 28 were confirmed
  individually or by an exact duration match (+1s YouTube rounding).

### Long-form publish calendar (already correct — do not change)
| File | YouTube id | Title | Publishes |
|---|---|---|---|
| V1 | `UghqHEH8yho` | Welcome to Abs by AI! | Published Aug 4 |
| V2 | `0zspIJVrv08` | Use AI To Get REAL Six Pack Abs – 6 Strategies That Work | Published Aug 7 |
| V4 | `Sv5wZha_a8c` | 1 Minute Ab Workout That Hits All 4 Ab Muscle Groups (At Home) | Aug 11 |
| V3 | `2T4LrQrmz9s` | My Top 10 Tips For Getting Six Pack Abs (At 40 Years Old) | Sun Aug 16 |
| V5 | `8BaCYcGhRPY` | The Ultimate 1 Minute Ab Workout – Follow Along (No Talking) | Sun Aug 23 |
| V6 | `hKmttAhgLfQ` | 3 Minute Total Body Home Workout (Almost No Equipment) | Sun Aug 30 |
| V7 | `27vZC4xVkms` | 3 Minute Total Body Home Workout – Follow Along (No Talking) | Sun Sep 6 |

### Shorts — 11 DONE and verified in the Studio content list
All have an individual title, a description with the parent-video link + `utm_medium=short`
UTM, video-specific tags added on top of the 15 inherited channel tags, made-for-kids
answered, and a schedule at **5:00 PM Central**.

| file | ytId | scheduled |
|---|---|---|
| short1_4-ab-muscles | `A8_uiK0D8nc` | Aug 13 |
| short2_toe-touches | `I_IpdKpT2-0` | Aug 15 |
| short3_v-sit-twists | `glHfVQsmqfI` | Aug 18 |
| short4_spiderman-planks | `KThvfTo4xMo` | Aug 20 |
| v2-short1_sugar-free-gum-trick | `y0XIbNoA2Xo` | Aug 22 |
| ~~v2-short2_sean-ray-vision-board~~ | `DiwFRZT4JUI` | **PULLED — set to Private 2026-08-25** (shows Mike Chang; Dan's call). Do not reschedule. |
| v2-short3_supplements-3-percent | `P9VUGyWeNtY` | Aug 27 |
| v2-short4_macro-tracking-obsolete | `VOlZHV1ibmU` | Aug 29 |
| v6-short4_towel-row-karate-chop | `qH9YRoH2PpM` | Oct 10 |
| v6-short5_you-always-have-three-minutes | `jImEPfu_Jak` | Oct 13 |
| v2-short5_ask-ai-to-interview-you | `rqyK5IDsxX0` | Sep 1 |

### Thumbnails — 2 of 5 unpublished videos DONE
- **V4**: A/B test SET and saved using the pre-existing on-spec pair
  (`thumb-A-medball-v2-FINAL.jpg` + `thumb-B-toetouch-FINAL.jpg`).
- **V3**: NEW full-bleed pair built, installed as primary, A/B test SET and **verified**
  (reopening the dialog warns "your current test will be deleted", which is the proof):
  - `thumb-A-flex-v2-FINAL.jpg` — photo-122, front double-biceps, bright poolside
  - `thumb-B-poolstand-v2-FINAL.jpg` — photo-180, standing at the pool, full body

## Key Decisions Already Made

- **Shorts cadence is Tue / Thu / Sat at 5:00 PM Central.** Dan's choice.
- **Shorts are gated behind their parent long-form** — a Short never publishes before the
  video it was cut from. This produced the slot order: V4's 5 Shorts → V2's 7 → V3's 11 →
  V6's 5.
- **V4 was left publishing Tuesday Aug 11** rather than moved to a Sunday. Dan's choice —
  only V4 is off-pattern and it gets the library moving sooner.
- **Thumbnail rebuild scope is the 5 unpublished videos only.** V1 and V2 keep their live
  thumbnails even though V1's pair uses the rejected Arial-Black style and V2's are 68–71%
  black. Dan's explicit choice.
- **Use the `plank()` full-bleed layout, never `scene()`.** `scene()` is what produces the
  black left slab and the pushed-to-the-side subject Dan rejected. `plank()` is what his
  approved V4-B toetouch uses.
- **The `®` comes out of every title.** It's the same false-registration claim that got the
  Google Ads account suspended on 2026-08-09, and YouTube is the same company. Already
  stripped from the 11 done Shorts.
- **`v2-short2` is titled "The Vision Board Trick That Built My Six Pack"** — deliberately
  does NOT name Mike Chang, per the contract-derived copy constraint recorded in
  `AI_COORDINATION.md`. The short's audio still references him; only the title/tags were
  controlled. Do not "improve" this title by adding his name.
- **Tags are ADDED, never replaced.** Every Short inherits 15 channel tags from the previous
  upload (`abs`, `six pack abs`, `sixpackabs`, `abs by ai`, `lose belly fat`, …). Adding 5–6
  video-specific tags lands around 290–380 of the 500-character limit.
- **`short5_1-minute-workout` is left unscheduled**, not scheduled-and-hoped. It is blocked
  globally and scheduling it would fail silently.

## Detailed Plan

### Step 1 — Remaining 16 Shorts (the bulk of the work)

Copy for every one is already written in
`YouTube Long Form Video Content/SHORTS_UPLOAD_PLAN.json` — title, description body, tag list,
slot number and date, keyed by source filename. **Use it verbatim; do not re-author.**

| file | ytId | date (5:00 PM CT) |
|---|---|---|
| v2-short6_hire-a-maid-not-a-trainer | `LvOMn7IpuCI` | Sep 3 |
| v2-short7_chicken-soup-trick | `broQqQ7We4k` | Sep 5 |
| v3-short1_no-abs-until-you-see-abs | `GVNzvm5sUbk` | Sep 8 |
| v3-short2_whey-protein-insulin | `B6Oku5GjrLs` | Sep 10 |
| v3-short3_liquid-calories-milk | `YvfQfo9Qh4s` | Sep 12 |
| v3-short4_train-abs-every-day | `sY5T9_sl8gk` | Sep 15 |
| v3-short5_jelly-bean-vs-soda | `JuLnoU9NV28` | Sep 17 |
| v3-short6_vacuum-exercises | `1AnxJ5JCLa0` | Sep 19 |
| v3-short7_fast-until-2pm | `7_dRh8Zhscs` | Sep 22 |
| v3-short8_weigh-yourself-every-day | `tqURi3qdrIc` | Sep 24 |
| v3-short9_break-fast-low-carb | `qpJnLUevrJ8` | Sep 26 |
| v3-short10_eight-hours-is-not-sleep | `o1v3wPkNI2I` | Sep 29 |
| v3-short11_bubble-gut-vacuums | `USLrZHrajGQ` | Oct 1 |
| v6-short1_gained-muscle-in-quarantine | `78pojxcmNeg` | Oct 3 |
| v6-short2_knee-yourself-in-the-face | `4e9jrnSq_pk` | Oct 6 |
| v6-short3_look-at-the-sky-deadlift | `kX6opGeaBtA` | Oct 8 |

Per video, at `https://studio.youtube.com/video/<id>/edit`:

1. **Confirm identity first.** Read the `Filename` field on the page and look the metadata up
   by that filename. Do not trust position in the content list.
2. **Set title + description** on the two `#textbox` contenteditables via
   `document.execCommand('insertText', …)` after selecting their contents — the framework only
   reacts to real input events.
3. **Answer "Is this video made for kids?" → No.** This is unanswered on every draft and
   **blocks Save entirely** until answered.
4. **Click `Show more`**, then add the video-specific tags: focus the Tags input, clear it,
   then per tag `execCommand('insertText', tag)` followed by a synthetic `keydown` **and**
   `keyup` for `,`. Clear the input again afterward.
5. **Save.**
6. **`Edit draft` → `Next` ×3 → Visibility → expand `Schedule`.** Drafts have no Visibility box
   on the details page; scheduling is only reachable through the wizard.
7. **Set the DATE first**: real click on the date field's dropdown **chevron** (not the text),
   which opens the calendar and focuses its text input, then `cmd+a`, type e.g. `Sep 8, 2026`,
   `Return`.
8. **Then set the TIME**: real click on the time field to open its list, then click the
   `tp-yt-paper-item` whose text is `5:00 PM` (index 68).
9. **Verify date AND time on screen**, then click `Schedule`, then read the confirmation
   ("Your video will be set to public on …").

The working helper functions from this session are documented in
`YouTube Long Form Video Content/SHORTS_UPLOAD_PROGRESS.md`. Stashing them in
`sessionStorage.__ALL` lets them survive same-tab navigation, which saves a lot of tokens.

**Keep a CDP call under ~45 seconds** — a single JS call that does metadata + save + open
wizard + advance will time out and leave the page mid-flight.

### Step 2 — Thumbnails for V5, V6, V7

Build with `plank()` from
`YouTube Long Form Video Content/batch2-transcripts/build-thumbs.py`, sourcing from the **18
landscape** photos (4096×2747) in `photos/finalized social media photos/`. `pany=0.10–0.14`
buys headroom for the top-left headline block.

- **V5** `8BaCYcGhRPY` — has **no thumbnails at all**. Build a fresh pair. Headline
  `["1 MINUTE AB","WORKOUT"]` (it's the follow-along cut of V4). Since it's a workout video, one
  variant should show Dan actually doing an ab exercise — **toe touches with the medicine ball
  are the approved look; a plank/push-up shape is rejected outright.**
- **V6** `hKmttAhgLfQ` — rebuild both. `thumb-A-towelrow` is 60% dark with Dan pushed right;
  `thumb-B-fists` also uses the `scene` layout. Headline `["3 MINUTE TOTAL","BODY WORKOUT"]`.
- **V7** `27vZC4xVkms` — rebuild both. `thumb-B-flex` is 78% dark; `thumb-A-seated` has the
  headline touching his shoulder. Same headline as V6.

Finals go in `social media graphics/youtube/thumbnails/<Video Name>/`.

Install + A/B test per video:
1. Primary: put the JPEG on the macOS clipboard with
   `osascript -e 'set the clipboard to (read (POSIX file "…") as «class JPEG»)'`, register a
   capture-phase `paste` listener that assigns `ev.clipboardData.files[0]` to
   `input[type=file]` **index 0** via `DataTransfer` + `change`, then click a **non-editable**
   area (empty space right of the panels, ~1330,420) and send `cmd+v`.
2. A/B test: `A/B Testing` → click the `Thumbnail only` chip's `#chip-container` → re-arm the
   listener targeting `input[type=file]` **index 2** → click the dialog heading → `cmd+v` →
   `Set test` → **Save**. The test only starts once the page is saved.
3. Verify by reopening the dialog — "Your current test will be deleted" is the proof it saved.

**OPEN (executor's call, low stakes):** whether V6 and V7 should share one thumbnail pair since
they're the same workout (narrated vs follow-along). Recommendation: give them *different*
photos so the two don't look like duplicate uploads in a viewer's feed.

### Step 3 — Copyright block on `short5_1-minute-workout` (`I_trw1PaMhc`)

Blocked globally; audio claim on **"Hard Rap Beat" by Artiss**, baked in from the V4/V5 source.
Not a strike, no channel impact. Options in order of preference:
1. Studio's own remove-claimed-content tools (Claims → Take action → replace/mute song). Only
   acceptable if it doesn't gut the workout audio — check what the segment actually sounds like
   first.
2. Re-render the Short locally with royalty-free music using the pipeline in
   `YouTube Long Form Video Content/v4-1min-ab-workout/`, then re-upload. Dan has to do the
   actual file upload (a browser can't be handed a local video file).

Its slot is deliberately empty; if fixed, append it to the end of the calendar (Oct 15) rather
than reshuffling everything.

### Step 4 — Two small cleanups

- **Strip the `®` from the two unlisted "The Upload" ad creatives** (`QkAFUHVyx28`,
  `uFPEbEm6ps4`), currently titled `Abs By AI ® - The Upload - Mike Tells His Story`. Note the
  second one is the `1.2x` variant. Same suspension-trigger reasoning as the Shorts.
- **V3's description names "Zepbound / Retatrutide"** in the Tip 8 chapter line. That breaks
  Dan's standing rule (never name a weight-loss drug — always "weight loss medication"), and
  it's the same tip he deliberately refused to cut into a Short for exactly that reason. V3
  publishes Sun Aug 16, so fix before then. **This is Dan's own copy — show him the replacement
  line before saving it.** Suggested: `14:33 Tip 8 — Consider weight loss medication`.

### Step 5 — Final verification

Load the Shorts content list and confirm all 27 schedulable Shorts show `Scheduled` with the
right dates, and that **zero** rows still read `Abs By AI ®`. Then spot-check two Shorts' times
via the Visibility panel — the content list shows the date but not the time, and a silent
12:00 AM is the single most likely defect.

## Things to Avoid / Lessons Learned

- **Typing into the schedule TIME field silently reverts to 12:00 AM.** It looks like it took.
  One video was scheduled at midnight this way. Click the real dropdown option instead.
- **Setting the date with a JS `.click()` on the trigger silently keeps the DEFAULT date.** One
  video got scheduled for *tomorrow* instead of six weeks out. Only a real click on the chevron
  opens the calendar properly. **Always read the confirmation dialog.**
- **`offsetParent` is `null` for the fixed-position time dropdown**, so filtering candidate
  options by visibility silently returns zero items. Match on text across all
  `tp-yt-paper-item` with no visibility filter.
- **`div.calendar-month` is not always reachable via `document.querySelectorAll`** — inside the
  upload wizard it needs a shadow-DOM-piercing query, and sometimes isn't reachable at all. Fall
  back to typing the date into the calendar's focused text input.
- **Dispatching only `keydown` for the tag comma silently accumulates raw text into one giant
  garbage tag** (`ab musclesrectus abdominisobliques…`). Needs `keyup` too. This happened once
  and had to be deleted by hand.
- **Do NOT force-navigate away while Studio reports unsaved changes** — it discards a
  configured-but-unsaved A/B test. This cost one rebuild. If a native "Leave site?" dialog
  appears, script injection times out and force-navigating is the only recovery, so avoid
  getting there.
- **Dark-pixel percentage is a bad proxy for "too much black."** A legitimately dark evening
  photograph scores the same as a black overlay panel. Judge visually.
- **Rejected thumbnail sources:** `photo-63` (push-up shape — Dan rejects push-ups as an ab
  exercise), `photo-118 / 189 / 212` (raised arm collides with the headline block).
- **Claude cannot upload video files.** Long-form files are 0.4–3 GB and Chrome's native file
  picker isn't drivable. Any re-upload is Dan's ~30 seconds.
- **An unanswered AI-disclosure question was noticed and left alone.** Studio asks "Was AI used
  to generate or edit your content…" on these Shorts. It does not block scheduling. These are
  cuts of Dan's real footage, so the honest answer is likely No — but it is a formal disclosure,
  so **ask Dan rather than self-certifying**, same rule as the Play Store content rating.

## Relevant Files & Locations

- `YouTube Long Form Video Content/SHORTS_UPLOAD_PLAN.json` — **the source of truth.** Title,
  description, tags, slot, date for all 28 Shorts, keyed by source filename, plus parent video
  ids.
- `YouTube Long Form Video Content/SHORTS_UPLOAD_PROGRESS.md` — what's done, the working Studio
  automation recipe, both silent-failure modes, the thumbnail install method.
- `YouTube Long Form Video Content/batch2-transcripts/build-thumbs.py` — `plank()` and `scene()`
  builders, per-video specs for V3/V6/V7.
- `photos/finalized social media photos/` — 125 finals; the 18 landscape ones are the thumbnail
  sources.
- `social media graphics/youtube/thumbnails/<Video Name>/` — where finals go.
- `Short-form video content/` — the 28 rendered Shorts (git-ignored).
- Per-video Shorts records: `YouTube Long Form Video Content/{six-ways-ai-abs,v3-top10-tips,
  v6-3min-home-workout}/SHORTS.md` — segment choices, editorial decisions, bleeps.
- Channel: `https://studio.youtube.com/channel/UC236gjadarHAhEhOMYNGJ9g`
- `.claude/skills/youtube-packaging/SKILL.md` — thumbnail rules and Studio gotchas. **Worth
  updating with the schedule-field failure modes from this session.**

## Model & Effort Recommendation

**Capability constraint that overrides the usual cost preference: this work cannot go to Codex.**
Every remaining step requires driving YouTube Studio through a live browser session (and the
macOS clipboard for thumbnail installs). Codex has no browser control, so it can't do Steps 1–4
at all. This isn't a quality judgement — it's a tooling one.

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Sonnet 5, standard thinking.** The copy is pre-written and the recipe is documented, so this is careful mechanical execution, not problem-solving. Sonnet is the right cost/capability point. |
| **If Claude usage is high / approaching a limit** | **Still Claude Sonnet 5** — Codex can't drive the browser. Instead reduce scope per session: do Step 2 (thumbnails for V5, which publishes Aug 23) and Step 4 (the V3 drug-name fix, which publishes Aug 16) **first**, since those are the only date-critical items. The 16 Shorts don't start until Sep 3 and can wait for a fresh window. |

Do **not** reach for Opus here — nothing in this task is architecturally hard or expensive to
unwind, and every failure mode is already documented. The one place to escalate is if Studio's UI
has visibly changed since 2026-08-11 and the documented selectors no longer match; then a single
Opus session to re-derive the recipe is worth it, after which drop back to Sonnet.

## Starter Prompt for the Next Task

> Finish the Abs By AI YouTube channel setup. Read
> `Handoffs/handoff-20260811-youtube-channel-setup-finish.md` first, then
> `YouTube Long Form Video Content/SHORTS_UPLOAD_PROGRESS.md` for the working YouTube Studio
> automation recipe — it documents two silent failure modes (the schedule time reverting to
> 12:00 AM, and the date silently keeping its default) that you must guard against by reading
> the confirmation dialog every time.
>
> Do the two date-critical items first, in this order:
> 1. V3 (`2T4LrQrmz9s`) publishes Sunday Aug 16 and its description names "Zepbound /
>    Retatrutide", which breaks Dan's standing rule against naming weight-loss drugs. Show Dan
>    the replacement chapter line, then fix it.
> 2. Build and install a thumbnail A/B pair for V5 (`8BaCYcGhRPY`, publishes Aug 23) — it has no
>    thumbnails at all. Use the `plank()` full-bleed builder and landscape source photos, never
>    `scene()`.
>
> Then work through the remaining 16 Shorts listed in the handoff, taking title/description/tags
> verbatim from `SHORTS_UPLOAD_PLAN.json` and scheduling each at 5:00 PM Central on its listed
> date. Confirm each video's identity by the `Filename` field on its edit page before writing
> anything to it. Finish with the V6/V7 thumbnail rebuilds, the `®` on the two unlisted ad
> creatives, and the final content-list verification.
