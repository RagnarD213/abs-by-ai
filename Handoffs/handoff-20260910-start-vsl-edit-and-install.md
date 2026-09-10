# Handoff — /start VSL: edit the recording, then install it on /start

**Written 2026-09-10. NOT EXECUTED. Fire only after Dan has recorded the script.**

## What this is

Dan asked for a video sales letter for `absbyai.com/start` whose single job is getting a cold visitor to upload a
photo (90% of visitors leave without uploading — `Docs/VSL_LANDING.md`). The script is written and lives in a Google
Doc: **https://docs.google.com/document/d/1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA/edit** (Drive title
"Abs By AI — /start VSL scripts (hero + full) — WITH FILMING NOTES"; id `1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA`).
If Dan edited the doc before recording, his version is the script of record — re-read it. It contains:

- **HERO CUT** (about 260 words, ≈1:15 at Dan's measured 203 wpm, demo-first: Dan uploads his own before photo on camera). The default video.
- **FULL CUT** (about 660 words, ≈3:15, story-first on the "This picture got me abs" hook). The test arm; also usable as a YouTube ad.
- Four hook takes that each end on "I'll go first" (so any hook splices onto the hero body), three pickups, a shot list,
  a B-roll table (B1–B13) with exact asset paths, the research summary, the compliance rules, and a teleprompter appendix.

Read the doc's sections 4, 5, 7 and 8 before touching footage — they are the edit spec.

## The job, in order

1. **Find the footage.** Ask Dan where the rolls are (expected: the 8/28 kitchen set, 4K S-Log3, four mono tracks —
   memory `shoot-828-slog3-format`). Probe every roll with `_shared/audio/pick_lav.py`; never assume a channel.
2. **Edit with `/website-video`** — the whole skill applies (audio chain gated against Muhammad, hair-anchored
   NEAR/FAR/PIP framing, real app screens as phone PiPs, AI clips regenerated until perfect, the full QC suite).
   Deliverables: the hero in **four versions** (hooks 1–4), and the full cut. Script fidelity is checked against the doc.
   - **B1 (the real upload flow)** is new: capture the current `/start` → photo picker → "Where you are now" →
     Subtle/Ripped → Generate → loader → result → "Lock in this goal" → analysis page, on the fixture server
     (stage 5 of the runbook), using Dan's before photo as the input. Measure the real generation wait; the hero's
     on-screen "REAL TIME: N SECONDS" uses that measured number. Never a real account, never the email screen.
   - **B6 / B7** are two new Veo clips (the same man as the website video, `ai/prompts/MAN.txt`): a mirror photo
     with the shirt off, and a glance at the lock screen then lacing shoes. Budget ≈ $3–6 inside the $25 cap.
   - Every AI image/clip tagged AI-GENERATED; Dan's photo-shoot stills carry "Dan's own result. Results vary."
     (or the longer variant if Dan chose it in the doc's section 7); before photo under 2 s; never side by side.
   - The trial sentence in the full cut needs the terms card (B10) on screen for 4 s.
   - End card holds to the last frame on both cuts.
3. **Dan reviews** (540p copies + the audio A/B). On approval, finalize per `/website-video` "Delivery layout".
4. **Upload unlisted** with `scripts/youtube/upload.js` (memory `youtube-upload-capability` — the brand-account
   trap). Custom thumbnail: Dan holding the phone with his AI goal image, "SEE YOURS IN 20 SECONDS". The embed shows
   the title and thumbnail before anyone taps play, so write the title for a visitor, not for search.
5. **Give /start its own video slot.** Today `public/site-video.js` (`window.ABS_SITE_VIDEO`) feeds BOTH `/start`
   and the post-lock-in analysis page (`ANALYSIS_VIDEO` in `index.html`). The analysis page must keep the finalized
   post-generation video `CwEGFxpIM-E`. Add a separate `/start` config (e.g. `window.ABS_START_VIDEO =
   { youtubeId, poster, lengthLabel }`) that `public/start.html` reads first, falling back to `ABS_SITE_VIDEO`.
   Update the copy that still describes the old video: the hero caption ("what happens after your photo · 3:50",
   `start.html` line ~293) and variant B's section heading + description ("…3 min 50 s", line ~357–358).
6. **Verify live** on `absbyai.com/start?v=a` and `?v=b` at phone width: the video renders in each variant's slot,
   the caption shows the new length, and the analysis page still plays `CwEGFxpIM-E`. Open the embed in a fresh
   profile and check for a **pre-roll ad** (YouTube can run ads on channels outside its Partner Program). If one
   plays, switch `/start` to a self-hosted mp4 (`site-video.js` already supports `mp4`) and tell Dan what hosting
   it needs.
7. **Measure on uploads, not plays:** `vsl_photo_chosen ÷ vsl_landing_seen`, broken down by `landing_variant`.
   Test order in the doc: hero vs no video → hero vs full → hook 1 vs hooks 2–4. Each arm needs a few hundred
   visitors before it reads.
8. **Close out:** remove this handoff from `AI_COORDINATION.md` (HANDOFFS) and `Handoffs/README.md` (Open table),
   and delete the coordination entry about the VSL script. Then check off the Victory Dashboard row
   `money::Write and record a video sales letter (VSL) for /start — cold-traffic version` (fetch the exact text from
   `/api/todos` first — `/dashboard-tasks`). It was deliberately left unchecked on 2026-09-10 because only the
   script was done.

## Traps

- A push redeploys and wipes in-memory locked holds (memory `deploy-drops-locked-holds`) — batch the `/start` code
  change into one commit.
- `/start` is web-only, so the slot change needs no native retest; the analysis page is shared with the iOS/Android
  wrappers — if it is touched at all, flag the native retest.
- Don't reuse the post-generation video's "thousands of guys" lines anywhere — the real count of people who have
  completed a generation was 75 on 2026-09-10.

## Recommended model and starter prompt

Fable 5.1, high effort (video pipeline + a small code change + live verification).

```
Execute Handoffs/handoff-20260910-start-vsl-edit-and-install.md. Dan has recorded the /start VSL — the rolls are
in <FOLDER DAN GIVES YOU>. Edit the hero cut (four hook versions) and the full cut with /website-video against the
script doc linked in the handoff, deliver review copies for my approval, then after I approve: upload unlisted,
give /start its own video slot (the analysis page keeps CwEGFxpIM-E), verify live, and report.
```
