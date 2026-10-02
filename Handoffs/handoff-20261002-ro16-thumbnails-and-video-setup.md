# RO-16 "If I Had Belly Fat, Here's How I'd Lose It In 90 Days": thumbnails, then upload and setup

**Written 2026-10-02 by Claude (Opus 5.5).** Job RO-16 on the Edit Queue, state `finalized`. One Claude task does everything:
five thumbnail choices (made by Codex in the command line), stop for Dan's pick, then `/video-setup`.
**Model:** Claude Opus 5.5, medium. **Sidebar name:** `If I Had Belly Fat LFC Setup`.
**Use the Codex subscription to generate the images.**

## 1. What is approved
Dan, 2026-10-02, after watching the round-3 review copy: *"All right, this is approved."* The film is locked; do not re-edit it.
It is an ORGANIC content video. It ends: "If you got something out of this video, subscribe to the channel and I'll see you in
the next one." No "tap the button below". Still run the skill's Step 0 classification and
`python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.

## 2. Files (all local, no download step)
Folder: `claude edited long form content/09 - If I Had Belly Fat, Here's How I'd Lose It In 90 Days/`
- Master: `If I Had Belly Fat, Here's How I'd Lose It In 90 Days | claude round 3 | 16x9 | RO-16.mp4`, 3.99 GB, 12:09.33,
  1920x1080 29.97 fps, sha256 `c535ab4cfe881fc95796c9f5a191535c87aa2d2bb61d3588a4f850da02643b09`. Re-hash it first.
- Subtitles `... RO-16.srt` (218 cues, sidecar) and `... RO-16.chapters.txt` (10 chapters, use as-is).
- Build record: `notes-RO16.md` (round-3 section at the bottom), `ROUND-3-REVIEW.md`.

Facts for the packaging:
- **The film contains realistic AI footage** with the on-screen AI-GENERATED label (the mirror opener at 0:00, the kitchen dad
  at 1:25, the office scene at 1:57, the pizza refusal at 3:34, the gym deadlift at 9:12, the two closing scenes at 11:59). So
  `ai_generated: true` in the Blotato config and the AI flag on YouTube.
- Organic videos may name the drug (VIDEO-RULES.md): the title and description may say Zepbound and GLP-1.
- Dan says to talk to your doctor on camera; put "Not medical advice. Talk to your doctor before you start." in the description.
- **The delivery gate stamp reads FAIL (gate 2.4.0), known and reported to Dan before he approved:** the same four rows as
  round 2 (a 30.5 s static stretch inside the approved first minute, the deliberate framing cuts, and two caption rows that
  misread sidecar subtitles and Soft Blue cards). Independent review said SHIP. Do not rebuild or re-gate; if a setup script
  refuses the stamp, tell Dan what it refused and stop there.

## 3. Thumbnails first (Dan's new standard, 2026-10-02)
Read `.claude/skills/_shared/VIDEO-RULES.md` (first section) and `.claude/skills/_shared/IMAGE-GENERATION.md`, then
`/youtube-packaging` for the photo, crop and text-clearance rules. Dan: *"one from the pool shoot, one from the studio shoot,
and three unique AI-generated images, three unique designs of Codex's choice."*
1. **Pool:** one real pool-shoot photo of Dan (cutout from `photos/finalized social media photos/_cutouts/`), abs visible, not
   a frowning photo, Speedo crop rule applied.
2. **Studio:** one real studio-shoot photo, same rules.
3. **to 5. AI-generated:** three different designs of Codex's choice that sell this topic (losing belly fat in 90 days). Let
   Codex pick the concept for each; ask for three that differ from each other in subject and layout, not three takes on one.
- Every image call: `.claude/skills/_shared/codex-image.sh --prompt-file p.txt --out <file> --model gpt-6.1-sol --effort high`.
  No Gemini or any other outside model. For the two real photos Codex makes the background only; Dan's real cutout and the type
  are layered in code. For the three AI designs, set the shipping type in code too.
- Same copy on all five unless Dan asks for alternatives. Text never touches his face or hair. No AbsByAI.com and no
  real-photo label on a thumbnail. 1280x720 JPEG under 2 MB.
- Build in `social media graphics/youtube/thumbnails/If I Had Belly Fat/_build-2026-10-02/`. State the image count before the
  batch (about 5, no spares). Send Dan one review sheet with the five numbered, say in plain words what each is, and **STOP
  for his pick.** Export `If I Had Belly Fat - thumbnail FINAL.jpg` after he picks.

## 4. Then upload and setup (per `/video-setup`)
1. **Board + queue:** add one RO-16 ACTIVE entry while you work. Queue stays `finalized` until Blotato is verified.
2. **Backups:** master and .srt to the Extreme drive and Google Drive per the skill's three-copies rule (Drive: anyone with
   the link).
3. **Packaging:** searchable title with no hype claims; description with the UTM link (`utm_content=ro16-belly-fat-90-days`),
   the 10 chapters, a short summary of the 8 steps, the not-medical-advice line, subscribe CTA, 3 to 5 hashtags. No em dashes.
4. **YouTube goes through Blotato only** (VIDEO-RULES.md, 2026-10-01): no upload of our own, no native scheduling, never Public
   by our hand. Title, description, thumbnail and AI flag travel in the Blotato YouTube target.
5. **Blotato:** the 3.99 GB master is far over the 400 MB cap. Encode a platform copy under 400 MB (1080p H.264, about 4 Mbps
   video, audio copied) with `Media/video_edit/bin/ffmpeg` (`nice -n 20` + VideoToolbox), check duration and loudness against
   the master, upload it and the thumbnail with `blotato_create_presigned_upload_url`, hash-check each, write
   `scripts/blotato/configs/ro16-belly-fat-90-days.json` (`content_type: organic`, `source` = the master's path), dry-run
   `scripts/blotato/longform_queue.py`, then `--apply`. Accounts: YouTube, Facebook, Instagram @danrosefit, TikTok. Never
   @abs.by.ai. The film is 12:09: confirm each platform takes that length; if one refuses, queue the others and tell Dan.
6. **Release slot:** 9 AM CT on the first Sunday with no other long-form. Taken at writing: Oct 4, 11, 18, 25. Read
   `BLOTATO_QUEUE_PROGRESS.md` and the live Blotato schedule for anything newer and record the slot there.
7. **Verify** every schedule on a fresh pull, write `Docs/RO16_SETUP_RECEIPT_<date>.md`, set the queue to `uploaded`, mirror
   the row to the Edit Queue artifact, update the board and `Handoffs/README.md`, and push with `scripts/git/safe-push.sh`.

## 5. Owed from the edit job (do at the end, small)
- Clip library: register the A01 opener and the new stock inserts that are in the film
  (`.claude/skills/_shared/cliplib/clip_library.py add ... --status used-final --used-in "RO-16"`, then `sheet`). Sources and
  IDs: `recipe-RO-16/plan_resolved.json` in the delivery folder.
- `roll_sidecar.py mark-used` for every C1710 range in `recipe-RO-16/edl.json`.

## 6. Traps
- Machine cap: two video builds at once; the platform encode runs anyway at lowest priority on the hardware encoder.
- YouTube engagement ads fire automatically for new videos; leave that routine alone.
- Swearing on camera stays ("that advice is bullshit" at 0:47); never flag it.
- A Blotato "failed" on a big video may be live (memory `blotato-false-failure-large-video`): verify before retrying.

## Starter prompt
> Read `Handoffs/handoff-20261002-ro16-thumbnails-and-video-setup.md` and do the RO-16 thumbnails, then upload and setup. Use
> the Codex subscription to generate the images (GPT-6.1 Sol, high effort): one pool-shoot photo, one studio-shoot photo and
> three AI-generated designs of Codex's choice. Show me the five and stop for my pick, then queue the video on all platforms
> through Blotato. Name this session `If I Had Belly Fat LFC Setup`.
