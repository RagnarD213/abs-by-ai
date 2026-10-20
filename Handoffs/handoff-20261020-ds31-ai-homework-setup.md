CONTENT: AI Homework SFC, approved R2, covers and setup.

Task name: **AI Homework SFC Setup**. Recommended model: **Claude Opus 5.5, high effort** (cover designs and public descriptions). Written October 20, 2026.

**Use the Codex subscription to generate the images.** One Claude task makes five cover choices, shows Dan one review sheet and stops for his pick, then completes organic setup. Worked example of the same job on the same set: DS-28 Meal Prep (`Handoffs/handoff-20261017-ds28-meal-prep-setup.md`, receipt `Docs/DS28_SETUP_RECEIPT_20261017.md`, config `scripts/blotato/configs/ds28-meal-prep.json`). Follow it; differences are below.

## Exact approval and files

Dan finalized the complete R2 film on October 20: "Okay, everything looks good. We'll keep the warm, vivid color, and the intro clip looks good. Let's proceed to set up." State: **finalized, not uploaded**. Approval: `Short-form video content/AI Homework - DS-31/APPROVAL.json` (copy beside the Extreme master), and `round2_approval` in `/Volumes/Extreme/_edit_work/ds31/round2-plan/decisions.json`.

Project delivery folder: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/AI Homework - DS-31/`
- Upload master: `AI Homework SFC R2 - complete Short.mp4`, **94,943,517 bytes**, SHA-256 `69213798dd2c34fe88eace189c869d5169ca990f67e877aafde3c15d7777c2ba`.
- SRT: `AI Homework SFC R2.srt` (101 cues). Last words at 1:00.88-1:01.50: "get in shape." (closing line: "Subscribe for more ways to use AI to get in shape.").
- Matching backup: `/Volumes/Extreme/Short-form video content/AI Homework - DS-31/`. Original delivery and all evidence: `/Volumes/Extreme/_edit_work/ds31/round2/review/` (gate stamps, audit `../audit/ROUND-2-REVIEW.md`, recipe `recipe-DS31-R2/`).

1080x1920 Rec.709 H.264/AAC, 1848 frames at 30000/1001, **61.66 s** (dedicated Short, under the 66 s ceiling). Verify the hash before use; upload this exact master, never the phone proxy or `r2-first-build/`. Organic dedicated Short: no Google Ads, no extra formats, no cutdowns.

## Preserve the final film

Colour C (Warm vivid) on every camera shot; A1 "Homework tower" AI opener at 0:00-0:02.80 with its AI-GENERATED chip; three Soft Blue cards, captions, B-roll, voice all as delivered. **The realistic AI clip (and the AI chat screen at 0:08) make the platform AI flag appropriate: `ai_generated: true`, YouTube altered/synthetic on.** Delivery gate 2.6.1 on this exact file: 35 PASS, 4 FAIL (approved bass-lift tone row, two wide-shot head-size rows, legacy caption-sync row), 3 N/A, 0 NOT MEASURED; independent audit SHIP; two watch-pass judges 0 defects. Do not change the film, thresholds or stamps. Finished transcript (tied to this sha): `/Volumes/Extreme/_edit_work/ds31/round2/finished-asr.json`.

## Topic for covers and copy

College students: let AI do the busy schoolwork (paid Claude plan, run it through AI checkers, fix flags) and put the hours saved into working out every day. Use the approved words and SRT; do not invent personal facts. The A0198 homework-tower clip is library-registered and fine as cover inspiration for an AI option.

## Execute

Steps 1-8 of the DS-28 handoff, with DS-31 names: verify hashes and that no other DS-31 setup owner exists; five unique Codex covers (one real pool photo, one real studio photo, one AI-enhanced or AI-generated Dan, two AI images of Codex's choice; `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`), one numbered sheet, **stop for Dan's pick**; after the pick, Google Drive copy in `gdrive:Short-form video content/AI Homework - DS-31/` set to anyone-with-link and hash-verified; TikTok cover-first copy with the maintained helper; title, description, tags, `https://absbyai.com` link/UTMs and one easy `pinned_comment` question in Dan's voice; config `scripts/blotato/configs/ds31-ai-homework.json` (`"content_type": "organic"`, exact `"source"`, `"ai_generated": true`, cover URLs, pinned question); `ad_guard.py --scan` and `cover_audit.py` before and after; Facebook cover registry; `organic_short_queue.py` dry-run then `--apply` on the next free Tuesday, Thursday or Saturday slot (America/Chicago) for YouTube (account 46963), Facebook, Instagram **@danrosefit** and TikTok; read every post back; if Blotato is full, finish everything and add one `kind: short`, `job: DS-31` entry to `scripts/blotato/video_waitlist.json` (no per-video scheduled task). Receipt `Docs/DS31_SETUP_RECEIPT_<date>.md`. Mark DS-31 `uploaded` with `queue.py` only when all four posts read back (mirror to the Edit Queue artifact db). Read first: `AGENTS.md`, full `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/video-setup/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`, `Docs/PINNED_COMMENTS.md`.

Git: the main folder is jammed (about 99 unpushed commits, merge conflicts owned by other sessions). Push task files from a clean checkout of `origin/main` if `safe-push.sh` stops; never hand-merge others' files.

## Finalization housekeeping already done

Approval recorded (project + Extreme `APPROVAL.json`, decisions.json, regression corpus entry `ds31-r2-approved-20261020`). Master and SRT filed hash-identical in the project folder and on Extreme. `Videos to Review` copy deleted; the :8931 review service retired. Queue state `finalized` (artifact db mirrored). A1 registered as clip library `A0198`. Spend so far $0 (60 Flow credits). No covers, uploads or Drive filing done yet.

## Ready-to-paste starter prompt

CONTENT: Name this chat AI Homework SFC Setup. Read Handoffs/handoff-20261020-ds31-ai-homework-setup.md and use /video-setup for the finalized AI Homework R2 Short. Use the Codex subscription to generate the images. Make five unique cover choices, show me one numbered review sheet and stop for my pick. After my pick, preserve the exact approved film, finish the backups, and set it up through Blotato for YouTube, Facebook, Instagram @danrosefit and TikTok. Verify the covers, saved schedules and pinned question. Use the shared waitlist if full. No extra formats or new edits.
