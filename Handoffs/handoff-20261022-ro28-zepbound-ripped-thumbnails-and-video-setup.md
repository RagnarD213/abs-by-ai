# CONTENT, long-form: Zepbound Even If Ripped LFC Setup

Written 2026-10-22 by Claude (Opus 5.5) at the end of round 3. Sidebar name: **Zepbound Even If Ripped LFC Setup**.
**Recommended model:** Claude Opus 5.5, high effort (the film started on Claude). **Use the Codex subscription to generate the images.**
Every generated still uses `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.

"Why Zepbound Improves Your Health Even If You're Ripped" (RO-28), 10/15 studio roll C1771. **Fire only after Dan approves round 4**
(review page http://127.0.0.1:8931/). Record his words and set the queue to `finalized` first.

## Exact file (never edit it; re-hash before setup)
- `claude edited long form content/23 - Why Zepbound Improves Your Health Even If You're Ripped/Why Zepbound Improves Your Health Even
  If You're Ripped | claude round 4 | 16x9 | RO-28.mp4` sha256 `86f7fbece5aada923fff6702053dbbab16a3fc05eaccd8e8c88b399974b29b8f`, 6:26.0, ~848 MB (over the 400 MB Blotato
  cap: make an upload derivative per `/video-setup`). Same folder: `.srt` (upload, never burn in), `.chapters.txt`, gate stamps,
  `recipe-RO-28-r4/ROUND-4-REVIEW.md`. No edit sheet (the writer demands a label on real moving footage of Dan, which the film rightly lacks).
- Gate: 36 pass; 3 known fails (warm-bass tone, two caption false positives), as RO-14 shipped.
- AI footage, each labelled AI-GENERATED: pharmacist double take (0:00), doctor says no (0:38), gym sit-up (1:32), barbecue (1:50),
  doctor visit (4:06). R4: ab wheel at 4:03 removed (Dan on camera); pool clips 2:22 and 6:12 re-graded (Dan 10-23: never raw footage). YouTube altered/synthetic disclosure and the TikTok AI flag apply. Organic: Zepbound may be named.
- Chapters: 0:00 Why I think ripped men should take Zepbound, 1:04 What losing weight does for you, 1:34 Reason 1: You're probably not
  at your ideal weight, 2:26 Reason 2: Health benefits beyond weight loss, 4:29 Why I'm staying on it for life, 5:31 How I take it.
- Ending (organic): subscribe + "go to SixPackAbs.com to get all my newest videos". Confirm with setup Step 0.

## Read before work
Live `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` (thumbnails, release cadence, pinned comment, never Public),
`.claude/skills/video-setup/SKILL.md`, `.claude/skills/youtube-packaging/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`,
`Docs/LONGFORM_RELEASE_CALENDAR.md` (RO-28 sits on the 2027 tentative list), memory `cover-picks-ai-dan-acting-topic`.

## Five thumbnail choices, then STOP for Dan's pick
VIDEO-RULES "Thumbnails: the five": one real pool-shoot photo, one real studio-shoot photo, one AI-enhanced or AI-generated Dan, two
AI images of Codex's choice; each its own design. Real photos never redrawn. No claims, no frowning Dan, text off face and hair.
Strongest pictures: the pharmacist's double take at a ripped customer (`round2/motion/veo/veo/A1d-flow-t3.mp4`, frames 0-93), the
doctor holding up her hand for no (`A2-flow-t1.mp4`). Show all five on one sheet, stop.

## After the pick
`/video-setup`: title, description with chapters and UTM link, tags, pinned question comment, AI disclosure, SRT. Schedule per the
calendar and the live Blotato queue (`scripts/blotato/longform_queue.py`); full Blotato goes on `scripts/blotato/video_waitlist.json`.
Shorts from this film (3) are a separate `/shorts` job (SFL).

## Starter prompt
> CONTENT (LFC). Rename this task `Zepbound Even If Ripped LFC Setup`. Read `Handoffs/handoff-20261022-ro28-zepbound-ripped-thumbnails-and-video-setup.md` and set up "Why Zepbound Improves Your Health Even If You're Ripped" (RO-28). Use the Codex subscription to generate the images. Opus 5.5, high effort.
