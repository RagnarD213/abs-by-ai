# SP-05: SRM top ad "How Men Over 40 Can Burn Belly Fat" (SixPackAbs.com): portfolio re-edit, 16:9

**AD (Social Response Marketing portfolio, not Abs By AI). List 1 · READY · fired by hand only (Dan, 2026-11-02: "We'll fire the edits individually").** Read `00-RULES.md` first. The `SP` group is outside the overnight queue's unattended pilot, so the dispatcher never launches it.

## Why this job exists
This is one of the 8 top ads on https://socialresponsemarketing.com (Dan's own brand (part of $103M lifetime spend); 16.7M views on the site). It sits on a YouTube channel Dan no longer controls (SixPackAbs.com), and Dan expects the owners may take it down once they see the site. So Dan wants SRM's own re-edited copy of each ad (Dan, 2026-11-02). Where the copy is hosted, and the rights question for client ads, are open in the SRM repo's `DECISIONS.md`. Neither blocks the edit.

## Source (downloaded 2026-11-02, YouTube's highest quality)
* Video: `Media/srm-portfolio-ads/05-spa-men-over-40-belly-fat/tq96OGXAJfA.mp4`: 1920x1080, 23.976 fps, h264 at about 2449 kbps, audio opus, **4:59**. This finished ad is the only source. No raw takes exist on this machine.
* Original: https://www.youtube.com/watch?v=tq96OGXAJfA (uploaded 20170321).
* Same folder: `SOURCE.json` (these facts), `transcript-youtube-auto.txt` (YouTube's auto captions, 805 words. Use it to find your way around, but re-transcribe with the shared Whisper tools before cutting on words), `contact-sheet.jpg` (16 frames across the ad), the `.info.json` (title, description, chapters), the thumbnail and the caption `.vtt` files.
* Treat the folder as raw footage: read-only. Work in `/Volumes/Extreme/_edit_work/SP-05/`.

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
`spa-men-over-40-belly-fat | claude or codex | 16x9 | srm portfolio.mp4` (1920x1080 or the source's size if smaller), a REVIEW 540p copy and `notes.md` (the plan Dan approved, the removals with timestamps, gate results) into `Media/srm-portfolio-ads/05-spa-men-over-40-belly-fat/deliver/`. Send Dan the review copy. Update the master list (`queue.py set SP-05 delivered`).

## Starter prompts
**Claude (Opus 5.5, high):**
> Name this chat "How Men Over 40 Can Burn Belly Fat SRM Portfolio AD R1". Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SP-05-spa-men-over-40-belly-fat.md`: re-edit SixPackAbs.com's ad "How Men Over 40 Can Burn Belly Fat" from the downloaded YouTube master as an SRM portfolio copy. Watch it, write the re-edit plan and stop for my OK before rendering. Then build it with /ad-edit's finishing standards, every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6.1 Sol, high):**
> Name this chat "How Men Over 40 Can Burn Belly Fat SRM Portfolio AD R1". Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SP-05-spa-men-over-40-belly-fat.md`: watch the downloaded ad, write the re-edit plan and stop for Dan's OK, then build it using `.claude/skills/ad-edit/SKILL.md` finishing standards. Deliver, send Dan the review copy, update `00-MASTER.md`.
