# Handoff — install DS-04 "The Only Ab Exercise That Shrinks Your Belly Fat" (2026-09-18)

**Fire when Dan says the review copy is finalized.** This handoff only publishes a short that is already
built, gated and reviewed. It changes no frames.

## The file

```
Short-form video content/ds-04_only-ab-exercise-that-shrinks-belly-fat.mp4
sha256  3e2a51b76ccf87aed6b02a002c84ccaf9013baf39466fb0345eeff8090df67b9
        70,119,789 bytes · 1080x1920 · 30000/1001 · 50.117 s · h264/AAC · BT.709 tagged
```

Beside it: `.audio_gate.json`, `.deliver_gate.json`, `.audio_untreated.json`, `ds-04_notes.md`,
`REVIEW_540p_…mp4`, `AB_ref-vs-ours_…mp4`, and `ds-04_recipe/` (plan.json, captions.srt, ROUND-3-REVIEW.md,
frame_diff_vs_round2.json, the full s01–s39 pipeline). **Verify the sha before doing anything** — if it does not
match, Dan asked for another change and this handoff is stale.

⚠ **The delivery gate's stamp reads FAIL and that is correct.** 36 rows pass; the one failure is `audio:stamp`,
which fails because `audio_gate`'s `artifacts` row fails on this roll's untreated outdoor lav (0.088 against a
0.079 limit; the untreated source is 0.101). Dan has listened and accepted the sound. **Do not "fix" the audio,
do not touch the threshold, do not re-render.** Publish the file as it is.

## Step 0 — claim it

1. `Handoffs/video-editing/00-MASTER.md` → DS-04 row; `AI_COORDINATION.md` → the DS-04 entry. If either says a
   session already owns the install, stop.
2. `python3 scripts/edit-queue/queue.py set DS-04 in_progress --by <Claude|Codex>`; add one ≤3-line ACTIVE entry
   to `AI_COORDINATION.md`; run `scripts/board-check.sh`.
3. ffmpeg is not on PATH — use `Media/video_edit/bin/ffmpeg` / `ffprobe`.

## Step 1 — read the skill, then follow it

**Invoke `/video-setup` and follow it.** Do not work these endpoints from memory. This is an **organic
dedicated short**, not an ad, so the whole skill applies with these DS-04 specifics:

* **Steps 1 and 2 are already done.** The file is filed and there is nothing to download. **Do not build
  thumbnail variations** — Dan moved cover images to Codex (his call, 2026-09-18) and there is no cover for
  DS-04 yet. See the cover warning below.
* **Model the packaging on DS-17**, the last dedicated short through this path:
  `scripts/blotato/configs/ds17-how-to-jump-rope.json`. Copy its shape exactly — `content_type: "organic"`,
  a `source` path, hook / body / close in Dan's voice, `ai_generated: false` (this cut contains no AI imagery;
  `plan.json` declares `ai_inserts` and `real_photos` both empty, and the gate's `compliance:labels` row is n/a
  for that reason), and a `youtube_description` with a UTM'd absbyai.com root link.
* **ManyChat keyword: `ABS`** (ab content — the table is `Docs/MANYCHAT_KEYWORDS.md`). ⚠ That account shows
  TRIAL on the board; if the keyword is dead, say so rather than inventing a different one.
* **YouTube: Private, and leave it Private.** `--privacy private`, `--synthetic false`, no `publishAt`, no
  Studio scheduling. Read the record back and require `privacyStatus: private`. Blotato owns the release.
* **Organic links go to the absbyai.com root**, never `/start` — that keeps organic out of the `/start` A/B test.
* Run `python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.

## Step 2 — ⚠ the TikTok cover is a hard gate on the schedule

TikTok's API takes no cover image, only a timestamp, so **a post queued without a cover falls back to frame 0 of
the video.** Frame 0 of DS-04 is Dan looking down and to the side with his eyes nearly closed (the reviewer
called this out as the platform still) — a bad permanent cover. A posted video's cover can only be changed
**within 7 days, from the phone** (`Docs/TIKTOK_COVERS.md`, memory `tiktok-cover-frame-0`), and two shorts have
already been stranded that way.

**So: do not queue TikTok until DS-04 has a cover.** Covers are Codex's now. Either
(a) a cover exists → `python3 scripts/blotato/tiktok_cover.py --build` then `--apply`, which prepends it as
frame 0 losslessly and sets `videoCoverTimestamp: 0`; or
(b) no cover exists → queue the other accounts, leave TikTok out, and tell Dan in one line that TikTok is
waiting on a cover from Codex. Do not queue TikTok "for now and fix it later" — later does not exist.

## Step 3 — close out

* Verify every schedule on a fresh pull before reporting success; record ids in `BLOTATO_QUEUE_PROGRESS.md`.
* `python3 scripts/edit-queue/queue.py set DS-04 uploaded --by <who>`, mirror to the artifact db
  (`ArtifactData` → `set`, url `https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs`, collection `jobs`,
  doc_id `DS-04`, with `if_version` from a read), and `mark-synced`.
* Check the task off on the Victory Dashboard (`/dashboard-tasks`) — **only if a DS-04 row exists**; do not
  create one for this handoff (Dan's rule, 2026-09-08).
* Delete the DS-04 entry from `AI_COORDINATION.md`, this handoff's row in `Handoffs/README.md`, and its line in
  the board's HANDOFFS section. Commit docs and configs only — never media; the repo is public.

## Context a fresh session will want

* **What this revision was.** Dan rejected the round-2 opening ("it looks like I'm standing there"), then
  rejected four real-footage candidates AND an AI-generated vacuum clip ("It looks like an AI morph. My face
  looks like 20 years older"), and chose candidate C — C1677 at 136.60 s. Only the opening beat, two caption
  chunks and one undeclared join changed; the audio is bit-identical to the cut he approved. Full account:
  `Short-form video content/ds-04_notes.md`, "Revision 1".
* **Known minors already accepted by Dan, do not re-open:** his eyes squint into the sun for the first ~2 s of
  the opening; the draw-in reads moderate at phone size because cue 1 is a full-body crop (that crop is what
  keeps the caption clear of his stomach); a 0.24 s caption chunk at 0:28.36; his mouth open on the last four
  profile frames at 0:29.30. The last two are frame-identical to the round-2 cut he approved.
* **Do not upload the AI experiment.** `/Volumes/Extreme/_edit_work/ds04/rev1/ai/` holds a generated vacuum clip
  and its keyframes. Dan rejected them. They exist only as a record.

## Starter prompt

> Read `Handoffs/handoff-20260918-ds04-install-vacuum-short.md` and install DS-04, the vacuum short. Verify the
> sha256 first, then invoke `/video-setup` and follow it: the file is already built, gated and reviewed, so skip
> the download and the thumbnail step. YouTube goes up Private and stays Private; Blotato owns the release.
> Do NOT queue TikTok unless DS-04 has a cover image — if it doesn't, queue the other accounts and tell me
> TikTok is waiting on Codex. The delivery gate's one FAIL row (`audio:stamp`) is my accepted exception — publish
> as is, don't touch the audio.

**Recommended model:** Codex **GPT-6 Astra, high** (Claude's video work is frozen to 2026-09-24, and this is an
ops job the Codex column covers). Claude alternative: **Sonnet 5, medium** — the file is finished; this is
upload and queue work, not editing.
