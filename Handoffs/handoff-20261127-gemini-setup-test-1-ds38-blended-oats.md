CONTENT · organic dedicated Short (SFC) · DS-38 · Gemini audition, live setup

# Gemini Setup Test 1 (live): TikTok Says Blended Oats Work Like Ozempic. They Don't. (DS-38)

**OPEN. Written by Claude 2026-11-27 for Gemini. This is a real setup of a real approved video. For this one job it replaces the Codex owner named in `handoff-20261114-ds38-blended-oats-off-the-cuff-setup.md`; do not fire that one too.**

Dan is deciding whether Gemini takes over video setup from Codex. This is audition 1 of 2. You are graded on the scorecard at the bottom. Do the whole job yourself. Codex is used for the five Codex cover pictures only, through the image script; zero Claude, zero paid API.

**Changed 2026-11-27 after this test had started (Dan: "Let's continue using Codex images as normal in addition to Gemini").** The blind cover mix stays: five Codex designs plus three Google options, shuffled and unlabeled. The run already in progress made a Gemini-only set first; before Dan picks, add the five Codex designs, keep your best three as the Google options, and rebuild the page blind.

## Where to run it (decided, tested today)

- **Antigravity CLI (`agy`) in Terminal on the M6, started from the project folder.** Model `gemini-4-neon-high`.
- **Not Gemini Desktop Task Mode.** On Nov 27 it was denied writing into `Handoffs/`, and the keys, `~/bin/rclone` and `~/.absbyai/` sit outside its two connected folders.
- Claude tested headless `agy` on this Mac on Nov 27: it wrote files, could read `~/.absbyai-secrets.env`, ran `~/bin/rclone` (v1.75.1), hashed the DS-38 master correctly and made a 9:16 picture with the built-in image generator (768x1376). All passed.
- Trap seen in that test: `agy` wrote its files into the `--add-dir` folder, not the folder it was started in. Start it from the project folder and always write to full absolute paths.

## Travel traps (Dan is in Massachusetts; the Austin machines are off)

- `/Volumes/Expansion` (Seagate) and the M2 (`ssh m2`, 10.66.0.2) are unreachable. Never wait on them.
- In the project, `Short-form video content` and `Videos to Review` are links to the Seagate and are **broken today**. Do not use, repair, replace or write through them. The old handoff's delivery path under that link does not work.
- `ffprobe` is not on PATH. Use `Media/video_edit/bin/ffprobe`.
- Disk space: internal drive has about 9 GB free, the Extreme about 46 GB. Work in `/Volumes/Extreme/_edit_work/DS-38-setup/` and keep it under 5 GB.
- `agy` has no connectors (`agy mcp list` is empty). Use the project's scripts and the REST calls below, not a Blotato connector.

## Verified inputs (checked by Claude on the M6, 2026-11-27)

| | |
|---|---|
| Approved master | `/Users/danrrose/Library/Application Support/AbsByAI Reviews/9600/page/media/off-the-cuff.mp4` |
| | 97,793,680 bytes, 64.83 s, 1080x1920, 30000/1001 fps, H.264 + AAC |
| | SHA-256 `eba0879d4f9cb9b9c557b70f6c6ca2c233dbf45afb56afe3141d0d7e4b2eb787` (matches the approval record) |
| Captions file | same folder, `off.srt`, 4,024 bytes, SHA-256 `1d655a09a3b95aaec73dad95c33d8766a9cb78413779e66b8f52d872ef94ff2e` |
| Approval | Dan chose "Off the cuff" on Nov 14, 2026: `Docs/DS38_FINALIZATION_20261114.md` |
| Set | 10/15 studio green screen reaction Short. Not kitchen, not gym. |
| Existing setup state | None. No config in `scripts/blotato/configs/`, no entry in `scripts/blotato/video_waitlist.json`, no receipt. Recheck before creating anything. |

Captions are already burned into the film. Never burn a second layer. The film is final: no re-encode of the master, no trims, no audio work. `scripted.mp4` in the same folder was not chosen; ignore it.

Organic, not an ad. The film ends "Thanks for watching and subscribe to the channel for more videos." Title stays exactly **TikTok Says Blended Oats Work Like Ozempic. They Don't.** Under this title the video is not eligible for an engagement ad (Nov 18 drug-terms rule); say so in the receipt. No needles, pens, vials or pharmacy imagery on any cover.

## Read first

1. `AGENTS.md` in full (your session hook loads the part past the 24 KB cap; if it did not, read from line 110 to the end).
2. `.claude/skills/_shared/VIDEO-RULES.md`: "Thumbnails: the five", the cover, publishing and AI-disclosure sections.
3. `.claude/skills/video-setup/SKILL.md` and `Docs/PINNED_COMMENTS.md` **as they are on disk today**. Both carry uncommitted edits from another live session: `engagement_prompt` replaces `pinned_comment`, and the ManyChat keyword field is gone. Read them. Never edit, stage or commit them.
4. `.claude/skills/coverimage/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`.
5. `.claude/skills/_shared/WRITING-RULES.md`, `.claude/skills/_shared/DAN-VOICE.md`.
6. Worked example, same shoot and same reaction format, all on this Mac: Kevin James Tried One Cheat Day A Week. It Wrecked His Diet. (DS-41): `Docs/DS41_SETUP_RECEIPT_20261115.md`, `scripts/blotato/configs/ds41-kevin-james-cheat-day.json`, `~/Projects/_edit_work/DS-41-setup/` (`design-plan.md`, `prompts/`, `layout-manifest.json`, `final/uploads.json`, `final/tiktok-verification.json`). Cover builder example: `~/Projects/_edit_work/DS-34-covers-r3/build.py`. Upload example: `/Volumes/Extreme/_edit_work/DS-108-setup/publishing/upload_assets.py`.

You are the setup owner where a skill says "Codex owns setup". For the five Codex cover designs you call `.claude/skills/_shared/codex-image.sh` yourself, with the model and effort the image rules name, exactly as a Claude setup owner does. Everything else in the skills applies as written.

## Phase A: up to Dan's cover pick

1. Run `agy` `/usage` and save the percentages (start reading). Note the start time.
2. Verify both hashes above. Recheck that no DS-38 config, waitlist entry or receipt exists.
3. **Eight cover options (five Codex designs plus three Google options of yours), each as a pair: Instagram/Facebook Reels 1080x1920 and YouTube Shorts 1080x1920.** The five Codex designs follow the mix below; your three are extra designs following the same guidance, not copies.
   - Two different AI pictures of Dan acting out the topic. Identity reference: `social media graphics/youtube/thumbnails/I'm 41. Here Are The 10 Exercises I Do Every Week/_build-20261113/identity-reference.jpg`. Look at every generated face before using it. Lean and shredded, not bulky. No frowning by default.
   - One real photo of Dan, original person pixels, from `photos/finalized social media photos/_cutouts/` (pool or studio), on a generated background.
   - Two concepts guided by what Dan actually picked recently: look at `/Volumes/Extreme/Short-form video content/covers/approved-*` and the last five setup receipts in `Docs/`.
   - Follow "Reaction cover composition" in the setup skill.
   - The five Codex designs come from `codex-image.sh` on the ChatGPT subscription (state the image count first, make no spares). Your three Google options come from your built-in image generation. **Zero paid API** (`GEMINI_API_KEY`, `GOOGLE_API_KEY` and `ALLOW_API_IMAGE` stay unset).
   - The blind test is on. Use `.claude/skills/_shared/blind-image/blind.py` (`add`, `build`, `pick`): neutral labels X1 to X8, no source named anywhere Dan can see, pick logged.
   - Your own pictures come back around 768x1376; Codex pictures around 941x1672. Headlines are set in code (Pillow), never generated. Upscale locally to 1080x1920 (no paid upscaler) and say which method you used.
   - If the image model refuses a picture (shirtless Dan is the likely case), record the refusal, do not reword around the filter, and make a different concept for that slot.
   - Every word on a cover starts with a capital letter. Run the layout checks the cover skill requires and keep the output.
4. Build a phone-first review page with `.claude/skills/_shared/review_server.py`: all eight options, both layouts each, blind labels X1 to X8. Give Dan the `http://127.0.0.1:PORT/` link.
5. While the page is up, prepare without waiting: copy master and captions to `/Volumes/Extreme/Short-form video content/Blended Oats - DS-38/` under the names `Blended Oats SFC R3 - off the cuff.mp4` / `.srt`, verify SHA-256, back up to Google Drive with `~/bin/rclone` (anyone-with-the-link, byte check). Draft title, platform captions, YouTube description, hashtags and the `engagement_prompt` from the actual words in `off.srt`, in Dan's voice. No long dashes in any outward-facing file: run the dash count check from AGENTS.md ("No em dashes in outward-facing writing") on each one; it must print 0.
6. **STOP. Show Dan the page, the proposed captions and the proposed release slot. Wait for his pick.** A revised cover needs his OK on the exact revised pair before it is installed.

## Phase B: after Dan picks

7. Build the TikTok cover-first copy with `scripts/blotato/tiktok_cover.py`. Check frame count, duration and audio against the master.
8. Upload master, TikTok copy and both chosen covers to Blotato media storage by REST: `POST /media/uploads` then PUT to the returned presigned URL (key file `Business/blotato-api-key.txt`, helper `call()` in `scripts/blotato/danrosefit_migration.py`). Download each file back and compare SHA-256. This is media hosting only, not a post.
9. Write `scripts/blotato/configs/ds38-blended-oats.json`, modeled on the DS-41 config, with `engagement_prompt`.
10. Dry run only: `python3 scripts/blotato/organic_short_queue.py scripts/blotato/configs/ds38-blended-oats.json`. **Never `--apply` in this test.**
11. Pick the slot from `Docs/SHORTS_RELEASE_CALENDAR.md` and `scripts/blotato/release_phases.py` (next open slot is in late January). Add exactly one entry for DS-38 to `scripts/blotato/video_waitlist.json`, same fields as the DS-41 entry, and mark the slot on the calendar. Waitlist only, even if the queue has room.
12. Run `scripts/blotato/cover_audit.py` and `scripts/blotato/ad_guard.py --scan`; keep the output.
13. Write `Docs/DS38_SETUP_RECEIPT_20261127.md` (list below). Push only your own files with `scripts/git/safe-push.sh -m "DS-38 setup (Gemini test 1)" -- <your files>`. If it stops on other sessions' files, leave your commit local and say so.

## Stop lines

- No live scheduling, no `--apply`, no edits or deletions of any Blotato post or schedule.
- No native YouTube upload of any kind.
- Do not touch: `AI_COORDINATION.md`, `BLOTATO_QUEUE_PROGRESS.md`, `.claude/skills/video-setup/SKILL.md`, `Docs/PINNED_COMMENTS.md`, `Handoffs/README.md`, anything under `SRM-goldenroots-jointvigor` or any Joint Vigor file. A client deadline is running on this Mac until Saturday 9 AM ET.
- Do not update the Edit Queue (its page sync is a Claude-only step) and do not write the sixpackabs.com article. List both as owed in the receipt.
- No `editcap.py acquire`: setup does not use an edit slot.
- Never say uploaded, scheduled or complete for anything you did not read back.

## Receipt must include

Hashes and byte counts, Drive link, cover pick and file hashes, every uploaded URL with its read-back hash, the config path, the waitlist read-back, the chosen slot, the two owed items (Edit Queue note, Seagate/M2 archive copy when Dan is back in Austin), plus the audition numbers: `/usage` before and after, pictures generated, refusals, wall-clock time, and every time Dan had to step in and why. Score yourself on the card below; Claude scores it again afterward.

## Scorecard (pass needs all five)

| # | Area | Pass |
|---|---|---|
| 1 | Copy and voice | Title unchanged. Captions, description and `engagement_prompt` read like Dan, use the film's real words, no long dashes, zero AI stock phrases, prompt under 180 characters. Dan edits at most one line. |
| 2 | Cover package | Five Codex designs plus three Google options, all clearly different, in both layouts, blind, exact 1080x1920, recognizable Dan in the AI pictures, clean cutout edge on the real photo, readable on a phone, layout checks pass. Dan picks one without asking for a full redo. |
| 3 | Technical accuracy | Valid config, uploaded files hash-match on download, one clean waitlist entry, correct slot for the phase rules, audits clean, receipt truthful. |
| 4 | Small Codex footprint | Codex used only for the five cover pictures (count reported), no Claude calls, no paid API charge, Gemini weekly usage drop reported. |
| 5 | Ran on its own | Finished in one session with no path, link or permission rescue from Dan, and none of the stop lines crossed. |

## Starter prompt

```bash
cd "/Users/danrrose/Projects/Claude/Projects/Abs By AI" && agy --model gemini-4-neon-high --dangerously-skip-permissions -i "Start Blended Oats SFC Setup (Gemini setup test 1). Read and execute Handoffs/handoff-20261127-gemini-setup-test-1-ds38-blended-oats.md exactly. Dan approved the Off-the-cuff R3 film on November 14; do not ask about the film again. Do the whole job yourself: Codex only for the five Codex cover pictures through the image script, zero Claude, zero paid API. Stop at the cover pick and wait for Dan."
```
