# Kevin James Cheat SFC Setup: approved off the cuff R2 (DS-41)

CONTENT, dedicated Short (SFC). **Start now.** One Codex setup owner, newest stable Sol at high effort (GPT-6.1 Sol on 2026-11-14; verify the current newest), following `.claude/skills/video-setup/SKILL.md`. Read `.claude/skills/_shared/VIDEO-RULES.md` first. Do not render a new edit, re-encode the film or add another layer of captions.

Video: "Kevin James Tried One Cheat Day A Week. It Wrecked His Diet." Reaction Short in the locked format (Bill Maher Codex R5), edited by Claude on the M2.

## What Dan approved

- Round 1 (2026-11-13) showed scripted and off the cuff side by side. Dan took off the cuff forward and on 2026-11-14 asked for two cuts and a speed-up: "Okay, let's cut. Subscribe to my channel for more workout and nutrition tips. At the end, let's cut to Do Cut A: 'Guys, this concept of a cheat meal does not work mathematically.' Then accelerate as much as necessary to get it under the 60-second limit there."
- Round 2 was delivered the same day on http://127.0.0.1:9800/ and Dan replied: **"Approved"** (2026-11-14). The scripted version was not selected; do not set it up.
- Approved film: `Kevin James Cheat SFC R2 - off the cuff.mp4`, 1080x1920, 29.97 fps, 59.46 s, burned captions.
  - MP4 sha256 `06001f612394d929e464a185ba26c8199d220e7181541fb8ed257e1e735c02bc`
  - SRT sha256 `b5da1e4f0b15440a541e53f5fb90e6fe0a69c4f3b64ece9a20840bea70bbc013`
- Where: `Short-form video content/Kevin James Cheat - DS-41/` in the project folder on both Macs (same hashes), with the stamps, the independent review, `notes-kevin-james-cheat-sfc-r2.md` and `recipe-r2/`. Work folder (M2): `/Volumes/Expansion/_edit_work/DS-41/r2/` (its `RESUME.md` has the build facts). Verify the hash before using the file. The Expansion drive has corrupted copies before: checksum every copy you make.

## Edit choices to preserve

- Dan's reply runs at 1.15x with pitch kept; Kevin James's clip (JRE Clips, "Kevin James on Cheat Days and Losing 60lbs After Fasting for 41 Days") plays at normal speed. The film ends on "and still track when you cheat." There is no subscribe line or end card by Dan's choice.
- Two AI cutaways carry the AI-GENERATED label (library clips A0197 scale, A0242 drive-thru). The setup's AI disclosure should reflect that the film contains AI-generated clips.
- The caption at 0:48 reads "while you're going hog wild" (he says "going to hog wild"); Dan approved the file with it.

## Honest QA limits

- Independent review: SHIP (`Kevin James Cheat SFC R2 - off the cuff - independent review.md`). Delivery gate 2.6.3: 35 passed; three rows stay red as on every Short in this format, each measured by the reviewer as not a real fault (full-mix tone because the podcast clip is in the window, voice alone passes; hair overlapping the panel by design; the zoom cut at 55.92 s); caption sync not measurable by the tool, measured by hand by the reviewer.
- No AI listening pass was possible. Dan reviewed and approved the file himself.
- No edit fixes are pending.

## What exists and what does not

- Edit Queue: DS-41 is `finalized`. Nothing is uploaded, no covers exist, no Blotato config, no Drive backup of the R2 master, no calendar slot (`Docs/SHORTS_RELEASE_CALENDAR.md` has no DS-41 row). Check for any existing platform, config or Drive records before creating anything.
- Filmed on the 10/15 studio green screen (not kitchen), topic fat loss and dieting: eligible for any phase, including the January blitz.

## The job

1. Verify the MP4 and SRT hashes, then make the verified backups the setup skill requires (Extreme and Google Drive, Drive set to anyone with the link).
2. Covers: five distinct concepts under the current rules (two AI images of Dan acting out the topic, one real pool or studio photo, two history-guided choices), Google subscription attempt first, the required Codex subscription choices and the blind Google options, in both the Instagram and YouTube layouts. Run the frame and face checks. **Stop for Dan's pick.**
3. Metadata from the approved take: title options led by "Kevin James Tried One Cheat Day A Week. It Wrecked His Diet.", description, tags, the pinned question comment (`"pinned_comment"` in the Blotato config), captions from the SRT where a platform takes them, YouTube Related Video only if a public parent applies (this is a dedicated Short: none).
4. After his pick: install the cover, upload non-public per the YouTube rule, and place all four platforms (YouTube, Facebook, Instagram @danrosefit, TikTok) in the next allowed Short slot for the dated phase, or on the shared waitlist (`scripts/blotato/video_waitlist.json`, flags `kitchen: false`, `gym: false`) if Blotato is full. Inspect the live queue first. Never create a per-video routine.
5. Verify every saved entry by reading it back, write `Docs/DS41_SETUP_RECEIPT_<date>.md`, set the Edit Queue to `uploaded` only under the verified setup-completion rule, update this handoff's top line and its `Handoffs/README.md` entry, and keep the status board entry short.

Report finalized, cover-approved, uploaded, queued or waitlisted and scheduled as separate states. Name the video by its title when talking to Dan.

## Starter prompt

```
Read Handoffs/handoff-20261114-ds41-kevin-james-cheat-approved-film-setup.md and execute it now with /video-setup: set up the approved dedicated Short "Kevin James Tried One Cheat Day A Week. It Wrecked His Diet." (DS-41, off the cuff R2, sha256 06001f61...). Dan approved the film on 2026-11-14; do not re-edit it. Verify the hashes, make the backups, build the five cover choices plus the blind Google options, and stop for my pick. After my pick, finish metadata, uploads (never Public), queue or shared waitlist placement, read everything back and write the setup receipt. Name the task "Kevin James Cheat SFC Setup".
```

Recommended: Codex, newest stable Sol (GPT-6.1 Sol), high effort.
