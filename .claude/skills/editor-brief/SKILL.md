---
name: editor-brief
description: Write the job briefing document Dan sends to a freelance video editor for a BATCH of videos — the offer and terms, links to every raw roll, the asset inventory, the scripts document, the quality standard stated as measurements, and the compliance rules. Use whenever Dan asks for a job brief, a project brief, an editor briefing, a "document for the editor", or to brief out the rest of a shoot — even if he doesn't say "/editor-brief". For reviewing a cut an editor has already delivered use /revisions; for cutting the video ourselves use /ad-edit or /longform-edit.
---

# /editor-brief — the job briefing document for a freelance editor

The deliverable is **one or two Google Docs in Dan's Drive**, written for the editor but
**delivered to Dan as a draft**. Dan reads it, shares the files, and sends it himself.
**Never contact an editor directly and never set link sharing on his behalf** — tell him
which docs and folders need to be opened up before he sends.

This skill was written from the 2026-08-27 brief for Muhammad A's 12-ad batch, which was
itself modelled on the 2026-08-20 PAID TEST PROJECT BRIEF (`1U9T4j9xbFlKNLgF95GnXlLYvblAN8eLbgr0Zr-TULmA`).
Read that one before writing a new brief — it is the format Dan already approved.

---

## THE RULE THAT MATTERS MOST: never tell an editor he is beating the others

**Do not reference another editor's work in a brief unless that other editor did the job
BETTER than the one you are writing to, and you are pointing at their video as the target
to match.**

If the other editors did *worse* — if the editor reading this is the best one Dan has —
say nothing about them at all. Not as praise, not as context, not as a war story, and not
buried inside a technical explanation.

The reason is commercial: **an editor who learns he is the best one on the roster asks for
more money.** Dan is negotiating the rate in the same document.

This is easy to violate accidentally, because the honest way to explain a source-footage
fault is to say who else tripped over it. On 2026-08-27 the audio section of the Muhammad
brief ended with *"Two editors before you delivered cuts that failed on exactly this, in
two different ways."* True, useful-sounding, and it handed him the knowledge that he is
the one who got it right. Dan deleted it himself.

**Write the fault as a property of the equipment, full stop.** "The rolls carry two
microphones hard-panned against each other. Use the right channel only." No history, no
comparison, no "unlike others". The instruction is exactly as actionable without it.

The one legitimate direction to reference another editor: **when their cut IS the standard**
— which is the normal case when Dan asks a new editor to match an approved reference. Then
name it, link it, and measure it.

---

## What goes in the document

Sections, in this order. Skip a section only if it genuinely does not apply.

### 1. Framing paragraph
What this batch is, and — if he has worked for Dan before — that his own earlier video is
the standard. One paragraph. Tell him to work only from this doc and the script doc it
links, so nothing gets pulled from the wrong folder.

### 2. The offer
Per-video rate, batch total, and the bonus if there is one, with its **exact date** and its
**exact quality condition**. State whether the bonus is all-or-nothing on the batch. State
how many revision rounds are included, and **whether revision rounds count against a bonus
deadline** — if they don't, say so explicitly, or a cautious editor will sandbag the last
delivery. Tell him to deliver one at a time rather than holding the batch: the same note
then does not repeat across twelve videos.

### 3. What you are delivering, per video
Container, resolution, aspect ratio, captions, colour, audio, music.

**State the aspect ratio as an exclusion, not just a request** — "16:9 only, do not build
vertical versions; we make the 9:16 ourselves from your finished file." Otherwise a
conscientious editor doubles his own work and then wants paying for it.

### 4. The standard, as measurements
Link the reference cut. Then give the numbers, because "make it as good as the last one" is
not a specification and cannot be argued about at delivery. Measure the reference and quote:
pacing / dead air, insert-and-graphic coverage as a % of runtime, punch-in count and the
interval between framing changes, what graphics exist, music tempo, and the audio master
(LUFS and true peak). See /ad-edit and /longform-edit for how these get measured.

### 5. Raw footage table
One row per video: number, title, roll id, raw length, script word count, **expected finished
runtime**, and a direct Drive link.

- **Derive the roll→video mapping from evidence, not from a handoff table.** Transcribe a
  probe of each roll (`probes.json` from `probe_identify.py` already exists for the 8/14
  shoot) and read the slates. Handoff tables get copied forward and go stale.
- Get raw durations with `ffprobe` on the local rolls, not from Drive metadata.
- Get Drive file ids with the Drive MCP: `search_files` with `parentId = '<shootFolderId>'`.
- **Compute expected runtime from the reference's OWN ratio**, not from a generic wpm figure:
  the reference ad was 610 script words finishing at 3:52.8, so ≈157 words per finished
  minute *including* its inserts and holds. Label it a guide, not a target.
- Say plainly that every roll contains repeated takes, slates, resets and director chatter,
  and that picking the take is the first job. Add: **the slated take is not automatically the
  right one** — on Ad 1 take 1 beat the slated take 2.

### 6. The scripts document
Link it, and explain how to read it: regular text is spoken, bracketed lines are visual cues
and are not spoken, the image under a cue shows the intended asset, and where a real file
exists its link is printed under the image.

### 7. Assets — three sub-sections, and the third is the important one
1. **The core folder**, file by file, each with a direct link, what it is, the rule attached
   to it (AI label / no AI label / "Results are not guaranteed." / never beside the before
   picture), and **which video numbers call for it**. That last column is what turns a folder
   into a work plan.
2. **Extra clips and photos.**
3. **⚠ Assets that do not exist yet.** Walk every bracketed cue in every script and list what
   nobody has generated or shot. Instruct him to **flag the timecode rather than substitute
   stock**, and to never screenshot a concept illustration out of the script doc and use it as
   a finished asset. Missing assets are usually the thing that actually blocks a batch — surface
   them to Dan in chat too, because generating them is a separate session's work that has to
   happen before the editor reaches those videos.

### 8. Source-footage faults
Anything wrong with the rolls themselves that the editor cannot be expected to know. For every
Jeff shoot that is the **two-mic fault** — but the wiring differs per shoot, so **generate this
paragraph from measurement, not memory**: run `.claude/skills/_shared/audio/pick_lav.py` on two or
three of that shoot's rolls and write what it reports. 8/3 and 8/14 rolls: one 2-channel stream,
right = close lav, left = a room mic 7.5–8.2 ms behind it, polarity-inverted and clipped on the ad
rolls → "use the right channel only, as mono, discard the left." 8/28 rolls: FOUR mono tracks,
lav on track 2 (`a:1`), far mic on track 1, tracks 3–4 silent → "use audio track 2 only, as mono."
Summing them combs the voice and costs ~4 dB on any phone speaker.

Then the spec line, stated as the measurement it is: **"the finished audio must pass
`.claude/skills/_shared/audio/audio_gate.py` against Muhammad's reference"** — ≈ −14 LUFS,
≤ −1 dBTP, one centred voice, no comb, room ≤ 80 ms early decay, tone within 1.2 dB of the
reference. Link the gate's A/B clip (his three sentences, then ours) so the editor can hear the
target rather than read it.

Written as equipment background. **No editor history.** (See the rule at the top.)

### 9. Hard rules — compliance
Numbered, with the consequence stated once at the top ("breaking these gets the ad account
suspended, so an ad that breaks one has to be recut"). The standing set:
no side-by-side before/after in any frame (cut sequentially instead); never show the app's
email-capture form; never show the in-app before/after screen; AI-GENERATED label on every AI
visual, large, upper-left, **never over Dan's face**; "Results are not guaranteed." on the real
physique photographs; no drug or medication brand names in any graphic even if Dan says one
aloud; nothing fake — no mocked-up app screens or third-party apps standing in for ours.

### 10. Delivery and questions
Folder, filename convention (`ad<number>_16x9.mp4`), a 720p review copy alongside each master
so Dan can watch on his phone, and one line per video on any deviation and why.
Close with "ask before you guess" — a missing asset costs one message, a wrong one costs a
revision round.

---

## Write goals, not tool steps

Same rule as /revisions: Dan's editors work with AI editing tools, not a fixed NLE. Never
prescribe a menu path. State the outcome and leave the method to them.

## Tone

Direct, concrete, no flattery and no filler. Every claim about the standard is a number.
Every asset is a link. **Never write anything that reads as an assessment of the editor's
standing relative to anyone else.**

---

## Mechanics

**Count the videos yourself from the script document — do not trust the number in the ask.**
Dan asked for "the 14 scripts remaining"; the batch-1 doc has 13 ad scripts (Ads 1–10, 13, 14,
15 — **11 and 12 do not exist**) and one was already edited, so it was 12. The number drives the
money, so correct it before writing anything and confirm the new total with him.

**Build the scripts doc by COPYING and deleting, never by rebuilding from text.** The scripts
carry embedded cue images, and a text export loses every one of them.
1. Drive MCP `copy_file` with the new title.
2. Open the copy in **Dan's real Chrome** (`mcp__claude-in-chrome__*`) — the in-app browser is
   not signed into Google.
3. Click at the start of the heading to remove, scroll (do **not** click the outline pane —
   that moves the cursor and loses the anchor), then **shift+click at the start of the next
   ad's heading** and press Delete.
4. Retitle the document's top heading with a triple-click and retype.
5. Verify from the outline pane that exactly the intended sections remain.

**Create the brief with Drive MCP `create_file`, `contentMimeType: text/html`.** HTML converts
cleanly to a Doc including tables, `rowspan`, links and nested lists. Use `text/markdown` only
when the doc has no tables — markdown tables do not survive.
- Keep the footage table to **five or six columns**. Seven made the title column wrap to six
  lines per row and spill across pages.
- `update_file` is **metadata-only** and cannot rewrite a body: to fix a doc, `create_file`
  again and `trash_file` the first.

**Verify in the browser before reporting** — open the doc and check the tables and the rowspan
cells actually rendered.

**Sharing is Dan's.** The new docs and the shoot folder are private to his Drive on creation.
Tell him to open all of them to the editor before sending, or every link in the brief 404s.

---

## Lessons

1. **Never state or imply that other editors did worse.** 2026-08-27: the audio section ended
   with "two editors before you delivered cuts that failed on exactly this" and Dan deleted it —
   *"I want to avoid giving away that he did a better job than the other editors… to avoid giving
   away that he can ask for more money."* Reference another editor **only** when their cut is the
   standard being matched. The full rule is at the top of this file.
2. **Count the scripts, don't take the count on faith.** The ask said 14; it was 12. Ads 11 and 12
   were never written and Ad 1 was already delivered.
3. **Copy the scripts doc, don't rebuild it** — the embedded cue images are half its value and a
   text export drops all of them.
4. **The in-app browser pane is not signed into Google.** Docs editing has to go through Claude in
   Chrome. Discovering this costs a round trip if you start in the wrong browser.
5. **Clicking the Docs outline pane moves the text cursor**, which destroys a selection anchor you
   were about to shift+click against. Scroll with the mouse instead.
6. **The asset gap is usually the real blocker and it is invisible until you read every cue.** Five
   of the twelve ads called for AI gag clips that have never been generated. A brief that only
   lists what exists reads as complete and then stalls the editor mid-batch. Walk the cues, list
   the holes, and tell Dan in chat as well as in the doc.
7. **State a bonus deadline against FIRST delivery and say so.** Otherwise revision rounds silently
   put the bonus out of reach and the editor stops trusting the offer.
8. **Say which aspect ratios NOT to build.** Our vertical comes free from `/shortad-from-longform`;
   paying an editor to also cut 9:16 buys a style Dan has not approved, from burned-in graphics that
   cannot be reframed back to wide.

---

## Posting the job on Upwork

Dan often wants an Upwork job posted from the same brief, and the editor invited to it.

**Never paste the Drive links or the brief itself into the job posting.** A public Upwork post
publishes the raw footage, the asset library and the scripts to anyone browsing. Summarise the
work and the terms, and say the full brief is shared on acceptance. Dan sends the docs directly.

**Check for an existing contract first.** If the editor already has an active contract with a
"fund a new milestone" prompt on the dashboard, adding a milestone there is less friction than a
new job — no proposal step, relationship and history intact. Say so in one sentence, then do what
Dan asked.

The flow is 6 steps: title → description → skills → scope → location → budget → review →
finalize. Settings that fit a batch like this: **Short term project**, scope **Medium**,
**1 to 3 months**, **Expert level**, not contract-to-hire, **Worldwide**, **Fixed price** at the
batch total (the bonus lives in the description, not the budget field), and
**"Post as standard for free"** — the **$29.99 Featured** upsell buys reach that is pointless when
you are inviting one named person, and it is a purchase.

To invite: job → **View proposals** → **INVITE FREELANCERS** → **My Hires** tab → *Invite to Job*.
Replace Upwork's default "Hello! I'd like to invite you..." with a real note naming the terms.

⚠ **Upwork's job-post SPA ignores coordinate clicks.** Every button, radio and label has to be
clicked by `ref` from `find`/`read_page`. Radios often need the **label text** element
(`generic "Medium"`), not the `radio` element, and a radio can read `checked:false` in JavaScript
immediately after a successful click because the step re-renders — trust the next screenshot, not
the DOM probe. `form_input` silently no-ops on the budget field; click it and type instead.
