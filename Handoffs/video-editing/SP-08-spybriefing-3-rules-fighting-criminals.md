# SP-08: SRM top ad "The 3 Rules Of Fighting Criminals" (Spy Briefing): portfolio re-edit, 16:9

**AD (Social Response Marketing portfolio, not Abs By AI). List 1 · READY · fired by hand only (Dan, 2026-11-02: "We'll fire the edits individually").** Read `00-RULES.md` first. The `SP` group is outside the overnight queue's unattended pilot, so the dispatcher never launches it.

## Why this job exists
This is one of the 8 top ads on https://socialresponsemarketing.com ($3M+ total ad spend; 4.8M views on the site). It sits on a YouTube channel Dan no longer controls (Jason Hanson), and Dan expects the owners may take it down once they see the site. So Dan wants SRM's own re-edited copy of each ad (Dan, 2026-11-02). Where the copy is hosted, and the rights question for client ads, are open in the SRM repo's `DECISIONS.md`. Neither blocks the edit.

## Source (downloaded 2026-11-02, YouTube's highest quality)
* Video: `Media/srm-portfolio-ads/08-spybriefing-3-rules-fighting-criminals/sruniCtkIo0.mp4`: 1920x1080, 23.976 fps, vp9 at about 2631 kbps, audio aac, **5:16**. This finished ad is the only source. No raw takes exist on this machine.
* Original: https://www.youtube.com/watch?v=sruniCtkIo0 (uploaded 20221019).
* Same folder: `SOURCE.json` (these facts), `transcript-youtube-auto.txt` (YouTube's auto captions, 1054 words. Use it to find your way around, but re-transcribe with the shared Whisper tools before cutting on words), `contact-sheet.jpg` (16 frames across the ad), the `.info.json` (title, description, chapters), the thumbnail and the caption `.vtt` files.
* Treat the folder as raw footage: read-only. Work in `/Volumes/Extreme/_edit_work/SP-08/`.

## Build
1. **Watch the whole ad first, then write a 5 to 8 line re-edit plan and stop for Dan's OK.** Default plan, unless Dan changes it:
   * Keep the ad's script, story order, voice and runtime. No new claims, no rewritten lines, no new on-camera promises.
   * Remove what no longer works for a portfolio copy: dead offer end screens, old URLs, phone numbers, prices and "click below" calls to action for products SRM doesn't sell. Note each removal with its timestamp. Text burned into the picture (for example the Spy Briefing ad's "Click 'Claim Book' Now" over most shots) can't be lifted out of a finished ad. Per shot, propose keep, cover with a rebuilt neutral band, or a gentle reframe, and let Dan choose in the plan.
   * Fix the finish where the 1080p source allows it: colour (decode as BT.709, per `00-RULES.md`), soft or cramped on-screen text rebuilt cleanly at the same timing, no loudness change to the original mix (`--verbatim`).
   * End on a 3-second Social Response Marketing end card: the white SRM logo `~/Projects/Claude/Projects/Social Response Marketing/brand/logo/svg/srm-logo-white.svg` on black, plus the line "Written and produced by Dan Rose". No URL, no call to book anything.
2. Build with `/ad-edit`'s finishing standards where they apply. The cut, graphics and audio gates still run. The S-Log, lav and take-selection steps don't apply, because the source is a finished ad.
3. Never claim on screen that no AI was used. Keep every health disclaimer the original carries.
4. All gates at the current version, independent audit.

## Deliver
`spybriefing-3-rules-fighting-criminals | claude or codex | 16x9 | srm portfolio.mp4` (1920x1080 or the source's size if smaller), a REVIEW 540p copy and `notes.md` (the plan Dan approved, the removals with timestamps, gate results) into `Media/srm-portfolio-ads/08-spybriefing-3-rules-fighting-criminals/deliver/`. Send Dan the review copy. Update the master list (`queue.py set SP-08 delivered`).

## Starter prompts
**Claude (Opus 5.5, high):**
> Name this chat "The 3 Rules Of Fighting Criminals SRM Portfolio AD R1". Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SP-08-spybriefing-3-rules-fighting-criminals.md`: re-edit Spy Briefing's ad "The 3 Rules Of Fighting Criminals" from the downloaded YouTube master as an SRM portfolio copy. Watch it, write the re-edit plan and stop for my OK before rendering. Then build it with /ad-edit's finishing standards, every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6.1 Sol, high):**
> Name this chat "The 3 Rules Of Fighting Criminals SRM Portfolio AD R1". Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SP-08-spybriefing-3-rules-fighting-criminals.md`: watch the downloaded ad, write the re-edit plan and stop for Dan's OK, then build it using `.claude/skills/ad-edit/SKILL.md` finishing standards. Deliver, send Dan the review copy, update `00-MASTER.md`.
