# Alcohol And Abs SFL Setup (SL-10): setup receipt, November 2, 2026

CONTENT (SFL), four Shorts from "Can You Drink Alcohol And Still Have Abs? (My 6 Rules)" (RO-13). **HOLD: shared waitlist.** Blotato was 199/200 (1 free; each Short needs 4), so nothing is scheduled yet. The daily `social-queue-daily-refresh` top-up queues them once the parent RO-13 (waitlisted, Sun Dec 20 9 AM Central) is queued; each entry carries `after` and `parent_config` = RO-13, so no Short posts before the parent. Dry run (`video_topup.py --assume-free 250`) places all four exactly on their slots. Studio set plus clips, no kitchen.

Approval: Dan, 2026-11-01, "All are approved. Go to setup." Covers: Dan's picks below. Round 1 page http://127.0.0.1:9652/ (8 per Short, blind set, picks logged with `blind.py pick`), round 2 http://127.0.0.1:9653/.

| Short | Slot (Central) | Cover | Film SHA-256 |
|---|---|---|---|
| Your Nightly Wine Is Killing Your Abs | Thu Dec 24, 9 AM | D | `3f4a487f4066fabd24c82bfd2feb2f2bb80e270d9f6d14aebc0fc705b50c8021` |
| Your Drinks Should Taste Bad | Thu Dec 24, 6 PM | A | `cf0a7630c904d33d0269a0fb7f084c09591bc9f0c94457cf5fd354cea30974e5` |
| What Killed My Urge To Drink | Fri Dec 25, 9 AM | Q | `aa2b52111159752370ba434e61694c04564d0b9c99b21f372e598e0bde5fdb9c` |
| Stop Drinking 3 Hours Before Bed | Fri Dec 25, 6 PM | L | `1d2458deca68b1b65349a4303451b24e2c3389f05aa9d37a7a7c8ec504d40bee` |

## Covers
- Your Nightly Wine Is Killing Your Abs: round 1 X2, AI Dan pouring red wine down a sink, thumbs up, large bottom title.
- Your Drinks Should Taste Bad: round 1 X5, AI Dan wincing after a vodka soda at a poolside bar, yellow band.
- What Killed My Urge To Drink: round 2 U2, his round 1 X6 (pool party, palm up to a beer) with the white pen from X7 in the other hand, raised so it reads at phone size. Dan, 2026-11-02: "U2 for What Killed My Urge to Drink. Go ahead and install those."
- Stop Drinking 3 Hours Before Bed: round 2 T4, new AI image Dan asked for: AI Dan in a black tank top slapping a beer out of an overweight man's hand while pointing at a pub clock, yellow band. All eight round 1 options rejected.
- His pen note named Drinks Taste Bad and his clock note named What Killed My Urge; the pictures he cited belong to Urge and 3 Hours, so they were applied there and said so in chat before he approved.
- All AI images: Codex gpt-6.1-sol high on the subscription with a real identity reference, faces inspected. Files and hashes: `Short-form video content/covers/approved-sl10/picks.json`. Copies beside the films on Extreme and Drive (`approved covers/`). YouTube JPEGs under 2 MB.

## Media
- Films re-hashed against the handoff before setup. Backups: Extreme `Short-form video content/Alcohol And Abs - SL-10/` (SHA-256 match), [Google Drive](https://drive.google.com/open?id=1t0OUdc4jHBG9grA1vunikZALgqjuaCEZ) (MD5 match, anyone with the link). An over-broad first copy also put the rejected R1 masters, the Y2 comparison and review copies there; all were moved to the Drive trash the same day.
- TikTok cover-first copies in `/Volumes/Expansion/_edit_work/sl10-publish/`: one cover frame prepended, audio packet payloads identical, zero decode errors, frame-zero PSNR 47 to 51 dB, first frames inspected.
- Blotato uploads (master, TikTok copy, Instagram PNG, YouTube JPEG per Short): 16 files, each downloaded back and SHA-256 matched (`/Volumes/Expansion/_edit_work/sl10-publish/uploads.json`). No direct YouTube upload, nothing Public, no native scheduling.

## Configs and checks
Configs `scripts/blotato/configs/sl10-short{1,2,3,4}-*.json`: organic, `ai_generated` true on all four (AI footage in each), description line "Some footage in this video is AI-generated and labeled on screen.", keyword FOOD, UTM campaign alcohol-and-abs, absbyai.com links, "Full video on this channel" line. Copy is Dan's filmed wording. No em dashes. Facebook covers in `scripts/blotato/fb_reel_covers.json` and the live installer copy. ad_guard CLEAN, cover_audit zero issues.

Pinned comments (written directly, not through dan-voice-writer): Wine "How many nights a week do you have a drink?"; Taste Bad "What do you usually order when you go out?"; Urge "How many drinks do you have in a normal week?"; 3 Hours "What time is your last drink on a night out?". Post and pin automatically after release (routine youtube-pinned-comment-daily).

Article: Shorts, nothing at setup; the post-release routine writes or skips.

Calendar: `Docs/SHORTS_RELEASE_CALENDAR.md` Dec 24 and Dec 25 rows = Waitlist. Edit Queue: SL-10 stays `finalized` until the top-up creates and reads back the schedules (same practice as DS-49, RO-04).

Outstanding (existing routines): top-up queues the 16 posts; then public cover tiles on all four platforms, pinned comments, Facebook covers, and YouTube's Related Video link from each Short to the parent once it is public.
