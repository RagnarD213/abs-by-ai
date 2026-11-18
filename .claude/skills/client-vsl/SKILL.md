---
name: client-vsl
description: Edit a CLIENT's long-form direct-response VSL (front-end or upsell/OTO) for the Social Response Marketing agency from the client's spokesperson footage, voice-over and master script, to the Joint Vigor standard Dan approved 2026-11-18. Covers the whole job: $5 trial lead, style-options page, key-visuals and script-cuts page, full uncut build with parallel block agents, recommended-cut split-test render, upsells and the mobile vertical, plus the review gates that took Joint Vigor to SHIP and the numbers for quoting. Use it whenever anyone mentions a client VSL, an agency, Upwork or SRM video edit, a sales video for a client's product, a trial edit of a lead, a style-options or key-visuals page for a client, a client upsell or OTO video, or any Goldenroots / Joint Vigor round, even without "/client-vsl". Not for Dan-on-camera Abs By AI work (/ad-edit, /website-video, /longform-edit); sales copy is /dan-copywriting.
---

# Client VSL edit (Social Response Marketing)

The method that produced the Joint Vigor VSL (Goldenroots Naturals, client Eric, Upwork): 59:35 at 1.1x, uncut master
script, Fable review F = SHIP, Dan approved 2026-11-18. Every future client VSL meets that bar. The finished masters are
the reference: [reference/QUALITY-BAR.md](reference/QUALITY-BAR.md).

**Category: AD (client VSL).** Write it on the first line of the task, every handoff and every receipt. Task names:
`<Product> VSL AD R<round>` (for example `Joint Vigor VSL AD R4`). These are agency jobs: the Abs By AI release
calendars, Blotato, YouTube, thumbnails, setup handoff and "no new Abs By AI ads" rule do not apply. The client owns
publishing.

## Read first, every job
1. This file, then the reference file for the round you are on (table at the bottom).
2. The job folder's `STYLE-LOCK.md` (from round 4 on) and `STATUS.md`. Job notes live in the private SRM repo:
   `~/Projects/Claude/Projects/Social Response Marketing/clients/<client>/<job>/`. Media and builds live in
   `renderq.py workdir` (Joint Vigor: `/Volumes/Extreme/_edit_work/SRM-goldenroots-jointvigor/`).
3. `.claude/skills/_shared/VIDEO-RULES.md` sections: B-roll correction in the finished film, AI clip filing, Google
   subscription first, AI start/end frames, AI imagery disclosure, review pages and Full screen, silent checks, render
   queue, edit cap, two Macs. `_shared/PRE-RENDER-APPROVAL.md` for the round method.

## Hard rules for every client VSL
- **Nothing goes to the client without Dan's approval in his own words.** Draft every client message in
  `CLIENT-MESSAGE-<round>-DRAFT.md`, mark it SENT with the story id after Dan says to send. No calls. Dan's voice:
  short, plain, first name sign-off "Dan", no em or en dashes ([reference/ROUNDS.md](reference/ROUNDS.md), "Client
  messages").
- **The client's script is the copy.** Every figure, price, date, study and quote on screen comes from the master
  script (prices checked against the client's live order page). Never reword, never add a claim. Cuts are verbatim
  deletions on sentence boundaries. Flag spoken differences; do not fix them with captions that disagree with the audio.
- **The client's casting rule is a gate**, written into `STYLE-LOCK.md` and audited over the whole film before every
  review (Joint Vigor: Caucasian seniors everywhere, Japanese people and settings only where the script mentions Japan
  or Okinawa).
- **Every AI picture of a person carries the "Dramatization" chip** top left, clear of faces, on every frame it shows,
  including crops and client-supplied AI images. Product, ingredient, study and illustration shots do not.
- **No em or en dashes in any on-screen text, page copy or client message.** Page builders assert it.
- **Generation:** Google Flow on Dan's subscription first (Nano Banana Pro stills 0 credits, Veo 3.1 Fast 10 credits a
  take), Codex image subscription as the alternative, paid API only after a recorded subscription failure. Stock
  (Pexels, Pixabay, free licences) before AI. Every AI take is filed in the clip library before the job closes.
- **Silent checks only** for sound; say plainly that nobody has listened. Dan's review page is handed over paused with
  sound ready.
- **One owner.** The orchestrator session owns the job; helpers and block agents write only inside their own folder.

## Before the first production step
```bash
python3 .claude/skills/_shared/editroute/editroute.py pick <JOB> --kind VSL --round <N>
python3 .claude/skills/_shared/editcap/editcap.py acquire <JOB> --title "<Product> VSL" --type AD
python3 .claude/skills/_shared/renderq/renderq.py workdir <JOB> --need <GB>
```
Dan calls it a priority: use `/priority-edit` (dedicated Mac, `priority.py reserve`). Honest `--need`: the 4K green-screen
key of a 60-minute film is about 190 GB. Heavy steps go through `renderq.py run --group <JOB> --heavy -- CMD`. Release
the slot with `editcap.py release <JOB> --review` whenever the job waits on Dan or the client. The M2 holds the Extreme
and Seagate drives; when the M6 edits there, run the keepalive and throttle big copies (memory `m6-network-drive-drops`).

## The rounds (detail: [reference/ROUNDS.md](reference/ROUNDS.md))
| Round | What the client sees | Lock written |
|---|---|---|
| 0 Intake | One short message asking only for what is missing | `PLAN.md` |
| 1 Trial | The finished first ~5 minutes (the lead), captioned + clean + SRT, for the $5 milestone | approved lead = visual vocabulary |
| 2 Style options | A page with one pick per area: opening, set/framing, pace, music, callouts, mechanism animation | picks |
| 3 Key visuals + script cuts | Replacement options for anything he asked to change, 10 to 15 key-visual stills, cut options as tracked-change Docs | `STYLE-LOCK.md` (first step of R4) |
| 4 Full build | The whole uncut film (or the version he names), captioned + clean + SRT, VTurb reveal time | |
| 5 Split-test cut | The same edit with the approved cuts lifted out, its own reveal time | |
| 6 Upsells, vertical | Each upsell/OTO version; the mobile vertical from the version he names | |

Internal reviews by Dan come before every client round. Two revision rounds per film are included in the agency offer;
anything beyond is a new quote.

## The full build (detail: [reference/PIPELINE.md](reference/PIPELINE.md))
1. `STYLE-LOCK.md` written from the picks before anything renders.
2. Opening rebuilt from the original layers with the picked clips.
3. House chroma key over the whole spokesperson roll (start it first; it is the longest machine step).
4. Dialogue foundation: master-order EDL, last clean complete take, film-time words at 1x, `MAP.md` with blocks, VO
   passages needing cover, key-visual times, reveal time at each pace, cut-version projections.
5. Captions: script-corrected ASR words, then forced alignment.
6. Four block planners in parallel from one shared `BLOCKS-BRIEF.md`, each writing `plan_bN.json` + `SOURCES.md` +
   contact sheet + receipt. The orchestrator appends every decision, timestamped, to the brief.
7. Stock first; AI needs listed with a stock fallback and queued to ONE Flow agent (frame gate + fresh frame-reviewer,
   take review, grade to the film, deliver, file).
8. Cards built in code in the approved card style, contain-fitted above the caption band.
9. Render chunks picture-only (captioned and clean in one pass, frame exact), assemble with the timing shifts, finish
   once: 1.1x pace, music laid over the whole film in one pass and ducked to the measured targets, -13.5 LUFS.
10. Gates, receipt, Dan's review page, fresh Fable review. Fix, re-finish once, repeat until SHIP.
11. Deliver captioned + clean + SRT (Drive folder, public link, hashes checked) with the VTurb reveal time.

## Quality gates (detail and the defect list: [reference/GATES.md](reference/GATES.md))
Run every one of these on the delivered masters BEFORE the reviewer sees them. Each exists because a Joint Vigor review
found its defect class:
- frame counts and video = audio length at 1x and paced; loudness; seam scan on every EDL join; music dropouts;
- per-frame luma (isolated dark frames, dark runs, one-frame flashes) and black/freeze detection;
- **BT.709 decode check after any patch round** (patch tools that decode as BT.601 darken the film 2 to 3% per round);
- patch-boundary check (first and last frame of every patch range, plus one either side, rendered fresh and compared);
- plan lint: stills held over 5 s in VO, reuse of a source within 90 s (keyed by file NAME), missing assets;
- card keep-out (no card text in the caption band), duplicate caption words, SRT = burned words, caption onsets on
  speech, no dash characters in burned text;
- VTurb reveal: first product frame lands on the spoken product word and nothing shows the product before it;
- **whole-film casting audit** of every stock, clip and photo shot against the client's casting rule, read by eye;
- **Dramatization chip sweep** at native size on the first and last frame of every AI shot of people;
- doctor colour across the whole film (camera white-balance steps) and one-frame pose jumps at cuts;
- story-scene read: one location and one cast per narrative scene, beats in script order;
- every B-roll insert colour corrected and checked as a frame pulled from the final master.

**Reviewer:** a fresh Claude Fable 5.2 high-effort agent (`Agent`, `model: "fable"`) on the WHOLE film every round
until it returns SHIP, given only the delivered files, the master script, `STYLE-LOCK.md`, the visual rules and the
previous review. Never the editor's receipts. Brief: [reference/REVIEWER-BRIEF.md](reference/REVIEWER-BRIEF.md). Dan sees
the film only after a SHIP (or with the open items listed).

## Dan's review page
`_shared/review_server.py <PORT> <DIR>` (byte-range seeking, silent-check and owner hand-off injected, Full screen opens
the file in VLC through `/__fullscreen`). The page has a button whose text is exactly `Full screen`, chapter links to
every changed spot and cut point, the revision list at paced film time, and "For a human ear" (what nobody has heard).
Builder model: Joint Vigor `asm/make_review_r2.py` (kit copy in the job folder, see PIPELINE.md). Test it at 800 and
1150 px in the side pane, hand over with `beginChecks()` then `handoff()`.

## Quoting the next job
Actual hours, credits and render time for Joint Vigor: [reference/QUOTING.md](reference/QUOTING.md). Log Dan's own minutes
on the next job; Joint Vigor did not.

## Reference files
| File | Use it for |
|---|---|
| [reference/ROUNDS.md](reference/ROUNDS.md) | Client round structure, review-page building and hosting on review.socialresponsemarketing.com, client message rules |
| [reference/STYLE-LOCK-TEMPLATE.md](reference/STYLE-LOCK-TEMPLATE.md) | The per-job lock file |
| [reference/PIPELINE.md](reference/PIPELINE.md) | Every build step with the tool that does it (Joint Vigor kit paths) |
| [reference/BLOCKS-BRIEF-TEMPLATE.md](reference/BLOCKS-BRIEF-TEMPLATE.md) | The shared brief for parallel block planners |
| [reference/GATES.md](reference/GATES.md) | Every gate, and every defect class reviews A to F found with the check that now catches it |
| [reference/REVIEWER-BRIEF.md](reference/REVIEWER-BRIEF.md) | The fresh Fable reviewer prompt |
| [reference/QUOTING.md](reference/QUOTING.md) | Hours, AI credits, render time, storage |
| [reference/QUALITY-BAR.md](reference/QUALITY-BAR.md) | The approved Joint Vigor R4 masters, paths and sha256 |

This repo is public. Keep client contract numbers, Upwork room and story ids, Drive folder ids, review-page slugs and
prices out of this skill; they live in the private SRM job folder.
