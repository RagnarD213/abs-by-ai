CONTENT (SFC). Setup task name: `Metabolism Not The Reason Setup`.

# Your Metabolism Is Not The Reason You're Fat: setup of the approved Short (DS-107), 2026-11-15

**OPEN. Start now. Owner: Codex (setup owner by default, Dan 2026-11-07). Model: newest supported stable Sol, high (GPT-6.1 Sol as of
2026-10-20; verify the catalog).** Do not start a second owner if a setup chat for DS-107 already exists.

Goal: take the approved film all the way to queued: covers, backups, organic metadata, Blotato on the four platforms (or the shared
waitlist when full), pinned question, receipt. Read `.claude/skills/video-setup/SKILL.md`, `.claude/skills/_shared/VIDEO-RULES.md`
(thumbnails: the five; Google subscription first for images; revised covers need Dan's look before install), `.claude/skills/coverimage/SKILL.md`,
`.claude/skills/_shared/IMAGE-GENERATION.md` (blind Google test) and `Docs/PINNED_COMMENTS.md` first.

## Exact approved film (do not re-render, re-mix or re-cut)

- Folder (shared Seagate, same path on both Macs; the M6 sees it through its SMB mount of the M2's Expansion drive):
  `Short-form video content/Metabolism Not The Reason - DS-107/` in the project folder
  (`/Volumes/Expansion/_internal-offload-20261031/Short-form video content/Metabolism Not The Reason - DS-107/`).
- Master `Metabolism Not The Reason SFC R2.mp4`, SHA256 `173a329050ec95f84e80db82e4ed32f929630bc4143aec5411171d5d6b2d8c78`,
  1080x1920, 30000/1001 fps, 1916 frames, 63.931 s, AAC 48 kHz. Captions are burned in; `Metabolism Not The Reason SFC R2.srt` beside it.
- Stamps beside it: audio gate PASS; delivery gate 2.6.3 38/39 (the one FAIL, captions:sync, is the energy method misreading four
  mid-sentence cues; two independent reviews measured them on time, see the review files). Do not change gates or the film.
- Approval record `dan-approval-20261115.json` (Dan's exact words, R1 picks and R2 approval). Dan on R2: *"This looks great ... This clip is
  attention-getting. This is approved. Go ahead and make that note for future edits and finalize this video. Proceed to set up."*
- Editor notes `notes-DS-107-R2.md`; reviews `... - independent review.md` (R1 and R2, both SHIP); recipe `recipe-R2/`; `ROUTING-PROOF.md`
  (two-Mac proof record; not setup material).
- Work folder (edit history, not for setup): `/Volumes/Extreme/_edit_work/DS-107/` on the M2.

## What the Short says (for covers, title and description)

Title: **Your Metabolism Is Not The Reason You're Fat**. Dan, keyed on the Soft Blue field: your metabolism at 45 is the same as at 25;
Science 2021 (Pontzer et al., 6,421 people, 29 countries): calories burned, adjusted for body size, stay flat from 20 to 60 and drop less
than 1 % a year after 60. What changed since 25 is four things that hit after 40: more stress (career, mortgage, kids), worse food without
realizing it (fast food between meetings, whatever your wife cooks), moving less, sleeping worse. Fix 1, food first: decide what you eat
before you're hungry, protein first, order for protein at fast food. Fix 2: 15 minutes of exercise first thing every morning. Bottom line:
it's not your age, which means you can fix it. Subscribe and go to SixPackAbs.com. It opens on Dan's real jump rope clip (shirtless, 1.25x)
and shows his real before photo (deck chair, about 200 lb) and a real pool photo of him today.

## Still to do (in order)

1. Covers: the standard five (two distinct AI images of Dan acting out the topic, one real photo from the pool OR studio shoot, two
   history-guided choices), Google subscription attempt first and the required Codex comparison choices, plus the three unlabeled Google
   options for the blind test; both Instagram and YouTube layouts; title capitalization on every word; stop for Dan's pick. Learn from
   recent `covers/approved-*/picks.json` first. Real-photo choice keeps original person pixels.
2. Backups: master + SRT to the Extreme and Google Drive (anyone with the link can view), checksums verified.
3. Organic classification (content, not an ad; ad_guard), metadata in Dan's voice (no em dashes in anything public), tags, pinned question
   (`"pinned_comment"` in the Blotato config), SixPackAbs link per the description rules.
4. Placement per `Docs/SHORTS_RELEASE_CALENDAR.md` and `scripts/blotato/release_phases.py` (green screen, not kitchen): inspect the live
   Blotato queue; if full, the shared waitlist (`scripts/blotato/video_waitlist.json`), never a new per-video routine. YouTube never Public at
   upload and never native scheduling. Read every schedule back.
5. Edit Queue: set `uploaded` only after the upload's visibility is read back (`scripts/edit-queue/queue.py set DS-107 uploaded`, then mirror
   to the queue page). Setup receipt `Docs/DS107_SETUP_RECEIPT_<date>.md`; one board entry while it waits on Dan's cover pick; list it here.

Articles: handled after release by `sixpackabs-article-gap-daily`.

## Starter prompt

> CONTENT (SFC). Name this chat "Metabolism Not The Reason Setup". Execute `Handoffs/handoff-20261115-ds107-metabolism-approved-film-setup.md`:
> set up Dan's approved Short "Your Metabolism Is Not The Reason You're Fat" (DS-107, exact master SHA256 173a3290...8c78 in
> `Short-form video content/Metabolism Not The Reason - DS-107/`). Five covers plus the blind Google options, stop for Dan's pick, then
> backups, metadata, pinned question, Blotato or the shared waitlist with readbacks, Edit Queue and a setup receipt. Do not re-render the film.
