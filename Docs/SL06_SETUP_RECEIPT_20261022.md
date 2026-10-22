# SL-06 Top 5 Zepbound Tips shorts: setup receipt (2026-10-22)

Task `Top 5 Zepbound Tips SFL Setup`, Claude Opus 5.5. Handoff `Handoffs/handoff-20261022-sl06-zepbound-tips-shorts-covers-and-setup.md`.

## Checks before any write
- Masters re-hashed: SHA-256 prefixes match the handoff (0ebf77cf, ad578fa5, 56ed1071, 0458bf1d, f11bfee8, e9b58ad3). Not re-edited.
- Classification: all six ORGANIC (delivered ASR closing words match the handoff; no "tap the button"). `ad_guard.py --scan` CLEAN before (158 posts) and after (182).
- Parent RO-12 "Top 5 Zepbound Tips To Lose Fat And Keep Your Muscle": YouTube schedule `5046550` Sun Nov 8 2026 15:00Z (read live 2026-10-22); socials Mon Nov 9 noon. Every short follows it. RO-12's config still says Oct 25; the live queue is the authority.

## Covers
Round 1: five per short (A pool, B studio on a Codex scene, C AI image of Dan, D and E Codex designs), 25 Codex GPT-6.1 Sol high images on the subscription (short 5 C regenerated once: tight stretched grin), 60/60 measured checks. Dan, 2026-10-22: "For short one, let's go with C, but change the text to 'reduce GLP-1 side effects'. Short two: let's go with C. Change the text to 'Why I don't use the KwikPen'. Short 3: Change the title to 'How to Inject Zepbound', and let's go with Design A. Short 4: Let's go with Design C. Change the text to 'Take Weight Loss Meds Thursday Evening'. Short 5: Change the title to 'How to Avoid Rebound Weight Gain'. Short 6: Let's go with C." Short 5 had no letter: C used. The revised covers were queued before he saw them (a miss; now a standing rule in VIDEO-RULES); he then reviewed all six on one sheet and approved: "Okay, everything is approved. No revisions needed" (2026-10-22), short 5 C included. His new text is the cover headline AND the YouTube title; the burned-in on-screen titles are unchanged. Short 3 names Zepbound on the cover at his request. Rebuilt covers 60/60 checks. Builder, prompts, checks, upload and config scripts: `scripts/covers/sl06-20261022/`. Exports and full hashes: `Short-form video content/covers/approved-sl06/picks.json`.

## Queued (Blotato, 9 AM Central, all four platforms)
Order of ids: Facebook / Instagram / TikTok / YouTube.

| short | title | slot | cover | AI flag | master / TikTok sha256 | IG PNG / YT JPG sha256 | schedule ids | config |
|---|---|---|---|---|---|---|---|---|
| 1 | Reduce GLP-1 Side Effects | Mon Nov 9 9 AM (2026-11-09T15:00Z) | C | yes | `0ebf77cf` / `e32ecf13` | `b7243f36` / `7e0d428b` | 5909999 / 5910000 / 5910001 / 5910003 | `sl06-short1-reduce-glp1-side-effects.json` |
| 2 | Why I Don't Use The KwikPen | Sat Nov 21 9 AM (2026-11-21T15:00Z) | C | yes | `ad578fa5` / `d099fa07` | `7d19ad69` / `72c403d0` | 5910004 / 5910006 / 5910007 / 5910008 | `sl06-short2-why-i-dont-use-the-kwikpen.json` |
| 3 | How To Inject Zepbound | Sat Nov 28 9 AM (2026-11-28T15:00Z) | A | yes | `56ed1071` / `cec4ab48` | `412384ed` / `ce293561` | 5910010 / 5910011 / 5910012 / 5910013 | `sl06-short3-how-to-inject-zepbound.json` |
| 4 | Take Weight Loss Meds Thursday Evening | Tue Dec 1 9 AM (2026-12-01T15:00Z) | C | yes | `0458bf1d` / `7bf88e5f` | `92fbdf09` / `9662511c` | 5910016 / 5910017 / 5910018 / 5910019 | `sl06-short4-take-weight-loss-meds-thursday-evening.json` |
| 5 | How To Avoid Rebound Weight Gain | Sat Dec 5 9 AM (2026-12-05T15:00Z) | C | yes | `f11bfee8` / `cf57a6c5` | `49a1314b` / `bca0398e` | 5910021 / 5910022 / 5910023 / 5910024 | `sl06-short5-how-to-avoid-rebound-weight-gain.json` |
| 6 | How Much Protein You Need On A GLP-1 | Tue Dec 8 9 AM (2026-12-08T15:00Z) | C | yes | `e9b58ad3` / `3fb96a53` | `c1005c8e` / `72597c27` | 5910026 / 5910027 / 5910028 / 5910029 | `sl06-short6-how-much-protein-you-need-on-a-glp1.json` |

- All 24 uploads downloaded back from their public URLs and SHA-256 matched (`/Volumes/Expansion/_edit_work/sl06-publish/uploads.json`).
- Read back on a fresh pull: times, Instagram and YouTube cover URLs, YouTube title, public status and AI flag, TikTok `videoCoverTimestamp: 0` and AI flag: 24/24 as configured.
- TikTok copies: `tiktok_cover.build()` with the Instagram cover as frame 0 (video +1 frame, audio packets identical, frame 0 PSNR 35.4 to 38.4 dB). In `/Volumes/Expansion/_edit_work/sl06-publish/`.
- Facebook covers (YouTube layout JPEG) registered in `scripts/blotato/fb_reel_covers.json` and the live installer `~/.absbyai/fb-reel-covers/`, matched on each caption's first line. `cover_audit.py`: no issues.
- Keyword FOOD (as the parent), campaign `zepbound-tips`, `utm_content=sl06-short<N>`. Captions from Dan's own words in each short, ending "Not medical advice. Talk to your doctor." YouTube descriptions name the full video by title and carry the AI-clips line; short 3 credits "Seattle Children's and SynergenX on YouTube".

## Pinned comments (dan-voice-writer)
- Short 1: Most of the side effects are the jump, not the drug. What dose did you start Zepbound at?
- Short 2: I use a needle and vial instead of the pen so I can adjust my dose precisely. Are you using the pen or a vial?
- Short 3: A good stick takes about 10 seconds and is nearly painless. Where do you usually inject?
- Short 4: Weekends are where diets die. What day of the week do you take your shot?
- Short 5: Lower half a mg a week while you're at or below goal weight. Have you ever gone off a GLP-1 and gained the weight back?
- Short 6: Your snacks should not be carbs. What's your favorite protein snack?
Posts and pins automatically after release (routine youtube-pinned-comment-daily).

## Copies
- Extreme: `/Volumes/Extreme/Short-form video content/zepbound-tips SL-06/` (six masters md5-matched, twelve covers, picks.json).
- Google Drive: `Short-form video content/zepbound-tips SL-06/`, anyone with the link: https://drive.google.com/open?id=1n71G1zJfus-gQZtTe45XjpIsHVnPYmhv (six masters md5-matched, twelve covers, picks.json).

## After release
- Captions are burned in; no SRT. Articles: written by the routine after release.
- After each YouTube release, check the public Shorts tile shows the approved cover (`/video-setup`, "YouTube Shorts cover verification"); the cover monitor checks all four platforms.
