CONTENT (SFC), organic. Setup task name: `Self-Driving Car SFC Setup`.

# Make Time For Exercise With A Self-Driving Car: setup of the approved Short (DS-30), 2026-11-16

**Owner: Codex (setup owner by default, Dan 2026-11-07). Model: newest supported stable Sol, high (GPT-6.1 Sol as of 2026-10-20; verify the
catalog).** Do not start a second owner if a setup chat for DS-30 already exists.

Goal: take the approved film all the way to queued: covers, Dan's pick, backups, organic metadata, Blotato on the four platforms (or the
shared waitlist when full), pinned question, Edit Queue, receipt. Read `.claude/skills/video-setup/SKILL.md`,
`.claude/skills/_shared/VIDEO-RULES.md` (thumbnails: the five; Google subscription first for images), `.claude/skills/coverimage/SKILL.md`,
`.claude/skills/_shared/IMAGE-GENERATION.md` (blind Google test) and `Docs/PINNED_COMMENTS.md` first.

## Exact approved film (do not re-render, re-mix or re-cut)

- Folder (shared Seagate, same project path on both Macs): `Short-form video content/Self-Driving Car - DS-30/`
  (`/Volumes/Expansion/_internal-offload-20261031/Short-form video content/Self-Driving Car - DS-30/`).
- Master `Self-Driving Car SFC R1 - complete Short.mp4`, SHA256 `31dcb750b089c33e01622da845c9bf15281a932b6132e3cb10f66f6f957dc4fc`,
  1080x1920, 30000/1001 fps, 1857 frames, 61.962 s, AAC 48 kHz. Captions burned in; `Self-Driving Car SFC R1.srt` beside it.
- Stamps beside it: audio gate (all pass except `tone`, the standard +3 dB bass lift); delivery gate 2.6.3, 35 pass / 4 known gate-vs-rule
  rows (tone; `framing:no_wide_level` and `framing:push_coverage` because the wide is the camera's original frame per Dan's 2026-11-15 rule;
  `captions:sync` legacy energy method; sentence starts measured at median -5 ms). Independent review `ROUND-1-REVIEW.md`: SHIP. Do not change gates or the film.
- Approval `APPROVAL.json`. Dan, 2026-11-16: *"All right, let's keep color C and voice V1. Proceed to setup if there is nothing else left to do
  here. Give me a handoff or setup, actually. For Codex"*. Colour C (Warm vivid) and voice V1 are what the file already contains.
- QA limit Dan accepted: nobody did an audible listening pass before approval (all audio checks were measurements).
- Other files there (`audio AB.mp4`, `notes-R1.json`) are review material, not setup media. Edit history: `/Volumes/Extreme/_edit_work/DS-30/` on the M2.

## What the Short says (for covers, title and description)

Working title: **Make Time For Exercise With A Self-Driving Car**. Dan on the 9/23 studio set (dark backdrop, lamp; not kitchen; check by frame):
too busy to work out? Trade your car in for a cheaper one that drives itself. The average American spends about an hour a day in the car,
7 hours a week staring at the road. Once the car drives, take work calls, make reservations, talk to AI so it's working before you reach the office.
The Tesla checks you're watching the road but you can look away for long stretches. A Tesla isn't a rich guy's car: Kelley Blue Book puts the
5-year cost on a base Model 3 at about $47,000 all in, a base Camry about $48,000. Somewhere with robotaxis, like Austin, you might not need a car
at all. You'll be shocked how much focus and energy you have left once you stop wasting it on driving. Subscribe for more ways to use AI to get in shape.

B-roll is all Pexels stock (library B0757 to B0763): a Tesla on self-driving (NOT Dan's car), freeway traffic, a work call, a laptop in a car,
a Zoox robotaxi, Austin skyline. Full-screen Soft Blue cost card (Tesla Model 3 vs Toyota Camry, Kelley Blue Book). **No AI imagery:**
`ai_generated` / synthetic-content disclosure = false on every platform (unless a cover itself is AI; covers follow their own label rule).

## Still to do (in order)

1. Covers: the standard five (two distinct AI images of Dan acting out the topic, e.g. Dan relaxed in the driver's seat working on a laptop or
   lifting while the car drives; one real photo from the pool OR studio shoot; two history-guided choices), Google subscription attempt first,
   required Codex comparison choices, plus the three unlabeled Google options for the blind test. Real identity reference and inspect every AI
   Dan face; real-photo choice keeps original person pixels. Both Instagram and YouTube layouts; every word capitalized. Learn from recent
   `covers/approved-*/picks.json` first. **Stop for Dan's pick.** No Tesla logo claims or prices on the cover (no-claims rule).
2. Backups: master + SRT to the Extreme and Google Drive (anyone with the link can view), checksums verified against the SHA above.
3. Organic classification (content, not an ad; ad_guard), title/description/tags in Dan's voice (no em dashes in anything public), pinned
   question (`"pinned_comment"` in the Blotato config), SixPackAbs link per the description rules. Dedicated Short: no parent long-form, no Related Video link.
4. Placement per `Docs/SHORTS_RELEASE_CALENDAR.md` and `scripts/blotato/release_phases.py`: studio set, not kitchen, so phases 1 and 3 are
   allowed; take the next free dedicated-Short slot. Inspect the live Blotato queue; if full, the shared waitlist (`scripts/blotato/video_waitlist.json`,
   `kitchen: false`), never a new per-video routine. YouTube never Public at upload, never native scheduling. Read every schedule back.
5. Edit Queue: `uploaded` only after the upload's visibility is read back (`scripts/edit-queue/queue.py set DS-30 uploaded`, mirror to the page).
   Setup receipt `Docs/DS30_SETUP_RECEIPT_<date>.md`; one short board line while it waits on Dan's cover pick; mark this entry executed in `Handoffs/README.md`.

Articles: handled after release by `sixpackabs-article-gap-daily`.

## Starter prompt

> CONTENT (SFC). Name this chat "Self-Driving Car SFC Setup". Execute `Handoffs/handoff-20261116-ds30-self-driving-car-setup.md`: set up Dan's
> approved Short "Make Time For Exercise With A Self-Driving Car" (DS-30, exact master SHA256 31dcb750...957dc4fc, in
> `Short-form video content/Self-Driving Car - DS-30/`). Five covers plus the three blind Google options (Google subscription first), both
> Instagram and YouTube layouts, stop for Dan's pick, then backups, metadata, pinned question, Blotato or the shared waitlist with readbacks,
> Edit Queue and a setup receipt. No AI imagery in the film. Do not re-render the film.
