# RX-01 — Audit the raw footage nobody has mapped yet

**List 1 · housekeeping · READY · low effort, no editing.** Read `00-RULES.md` §1 (the machine cap applies to Whisper).

## Why
On 2026-09-16 the master list was built by transcribing every 8/28 talking/workout roll in full, plus the 7/8 rolls
C1482–C1486 and C1489. That found 41 filmed scripts the old maps had missed. These rolls are still **unmapped**, so there may
be more finished-script footage we don't know about, or nothing at all.

| shoot | rolls | what's known |
|---|---|---|
| welcome-video first shoot (camera date 06-18) | C0223–C0238, ~2 h 40 m (C0236 58:12, C0238 30:02) | nothing. Probably the source of V2 "Use AI To Get Real Six Pack Abs" (38:25), unverified. ⚠ Its only copy is on this drive (board: 114 GB upload undecided). |
| 7/8 | C1481, C1490–C1499 (short clips), GoPro GH01/02/03/040268, GH010269/GH020269 | C1483 = V1 intro, C1484–85 = RO-07, C1486 = RO-08, C1487–88 = Zeeshan's Deadlifting, C1489 = V3 |
| 8/3 | C1515–C1531 (17 clips, 9–23 s), GoPro 1 GOPR0040/0041 (~72 min), GoPro 2 GH0x0270–272 | probably b-roll/alt angles; GoPro 2 GH0x0268/269 look like duplicates of the 7/8 files |
| 8/14 | C1615 (0:19), C1627 (0:40) inside the Vacuum range | false starts? |
| 8/28 card leftovers | C1457–C1480 (May), C1500–C1509 (Jul–Aug), C1634–C1645 (Aug tests); C1476–80 (~53 min) and C1639/C1643 unmapped | |
| 8/28 b-roll | C1678, C1684 unchecked; 360 GoPro (3 files); regular GoPro 1/2 (unset clock) | DS-25 (M100s) needs to know whether M100 moves exist anywhere |

Existing transcripts: `/Volumes/Extreme/_edit_work/_transcripts-828-full/` (25 rolls), `_edit_work/tx/probes.json` (8/3),
`_edit_work/ad1-8-14/tx/probes.json` (8/14), `_edit_work/website-video-828/tx/probes.json` (8/28 first 100 s).

## Do
1. Talking rolls: Whisper `base.en` over the full roll (read-only on the source; extract one mono track to a temp WAV,
   then delete it). Write `<roll>.txt` with timestamps into `_transcripts-828-full/` (keep the dir name; it's the shared transcript home).
2. Silent/b-roll clips: a 3×3 contact sheet per clip (ffmpeg thumbnails) instead of transcription.
3. Match each roll against every script doc: Shoot 5 `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k`, Shoot 4
   `1uDAWvxoAjXUaawZctgdSDj_9JPa5mfk5MMM2Sh8L7yE`, Shoot 3 `1VeNXATtvHBVe_Y5S3fxmSjllZxva0zwgo5NghW-G_bU`, Second Shoot
   `15gg6GP_Huy93ZBfTpbQuUtHGDrgHL-bs6Op-nN2UBr8`, and the published V-videos (match V2 by content).
4. Write `Docs/RAW_FOOTAGE_MAP.md`: one table per shoot, roll → content → used by (published video / job ID / unused).
5. **Any filmed video that isn't in `00-MASTER.md`** gets a new row and a job doc in the same format as its siblings.
   Anything that is only b-roll goes in the map, not the master list.

No renders, no spend. Report to Dan in a few lines: what was found and what was added to the list.

## Starter prompts
**Claude (Opus 5, medium):**
> Read `Handoffs/video-editing/00-RULES.md` §1, then execute `Handoffs/video-editing/RX-01-unmapped-footage-audit.md`: transcribe or contact-sheet every unmapped roll, match them to the script docs, write `Docs/RAW_FOOTAGE_MAP.md`, and add any filmed-but-unlisted video to the master list with its own job doc. Report what you found.

**Codex (GPT-5.6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` §1 and §3, then execute `Handoffs/video-editing/RX-01-unmapped-footage-audit.md`. Write the footage map, add any missing videos to `00-MASTER.md` with job docs, report to Dan.
