# Handoff — Website conversion video: upload to YouTube (unlisted) and install on the analysis page + /start

**Written 2026-09-09, after Dan finalized rev 6 ("you nailed it, this is perfect, this video is finalized"). Not executed.**

## What exists

The finalized master is **rev 6, version A (tan-corrected)** — Dan's approval did not name A or B; A is the version
that carries everything he asked for and it passed every gate, so it was finalized as A with B kept as `_ALT`. If he
ever says "B", swap the two files and re-run this doc's install step with the other upload.

| | path |
|---|---|
| **the file to upload** | `Website Videos/Website Conversion Video (post-generation)/website_video_16x9.mp4` |
| same file, working delivery folder | `claude edited long form content/06 - Website Conversion Video (post-generation)/website_video_16x9.mp4` |
| spec | 1920×1080, 29.97 fps, H.264 High, CRF-14 export (~18 Mbps), AAC 320k, **captions burned in**, 3:50.23, ~400 MB |
| alternate (cheek as-is) | `…/website_video_16x9_ALT.mp4` — do NOT upload unless Dan switches |
| notes on what is in it | `…/notes.md` (rev 6), per-revision history `notes_REV*.md` |
| poster frame | `public/img/video-poster.jpg` (65 KB, already in the repo and referenced by `site-video.js`) |

Both pages already have the player wired and hidden:

- `public/site-video.js` — **the one place**: `window.ABS_SITE_VIDEO = { youtubeId: '', mp4: '', poster: '/img/video-poster.jpg' }`.
- `public/index.html` — the post-lock-in "Your analysis" page reads it as `ANALYSIS_VIDEO` (~line 4823) and renders a
  `youtube-nocookie.com/embed/<id>` iframe into `#analysisVideoFrame` when `youtubeId` is set; hidden for real users
  until then (`?vp=1` shows a placeholder card so the layout can be checked).
- `public/start.html` — the `/start` ad landing page (both A/B variants) reads the same object (~line 489).

So the whole install is: **paste the 11-character id into `youtubeId`, push, verify.**

## Step 1 — upload to YouTube as UNLISTED (the only step that needs a human or a new token)

Claude cannot do the upload the obvious way: the Chrome extension's `file_upload` is capped at **10 MB** against a
~400 MB file (`AI_COORDINATION.md`, the longforms 02/03 entry), and the stored `GOOGLE_REFRESH_TOKEN` in
`~/.absbyai-secrets.env` is **calendar-scoped only** — it cannot call the YouTube Data API. Two ways, pick one:

**(a) Dan uploads — 2 minutes, recommended if he is at the keyboard.** YouTube Studio → Create → Upload videos → drag the
file above. Settings: title `Abs by AI — what happens after your photo`; description one line + `https://absbyai.com`;
**Visibility: Unlisted**; audience: not made for kids; no playlist, no cards, no end screen (it plays inside our page);
tags optional. The captions are burned in, so skip YouTube's caption step. Copy the id from the URL (`watch?v=<id>`).

**(b) Claude uploads through the YouTube Data API v3** — needs a token with `https://www.googleapis.com/auth/youtube.upload`.
The existing `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` in `~/.absbyai-secrets.env` are a Google OAuth client; mint a
NEW refresh token with the YouTube scope (do not overwrite the calendar one — store it as `YOUTUBE_REFRESH_TOKEN`):
1. Run a local loopback OAuth flow (a 20-line Node/Python script: open the consent URL with `access_type=offline`,
   `prompt=consent`, scope `youtube.upload`, redirect `http://127.0.0.1:<port>`), open the URL in Dan's Chrome, and
   **ask Dan in chat before clicking Allow** (granting OAuth permission is an explicit-permission action; Dan signs in
   himself if Google asks — Claude never types credentials). The YouTube Data API must be enabled on that Google Cloud
   project (Cloud Console → APIs & Services → Enable APIs → YouTube Data API v3); if the OAuth client is in "Testing"
   mode, Dan's account must be a listed test user, else the token expires in 7 days.
2. Resumable upload: `POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status`
   with `{snippet:{title,description,categoryId:"26"}, status:{privacyStatus:"unlisted", selfDeclaredMadeForKids:false}}`,
   then PUT the bytes to the returned Location in 8 MB chunks. Save the token to `~/.absbyai-secrets.env` (0600) and
   the video id to `Docs/VSL_LANDING.md`.
Quota: one upload costs ~1,600 units of the 10,000/day default — fine.

Either way, **confirm the video processes to 1080p on YouTube before installing** (Studio shows "SD" for a few minutes
after upload; the embed serves whatever is processed). Open the unlisted URL once, logged out, and check it plays.

## Step 2 — install (one line, one deploy)

1. `public/site-video.js`: `youtubeId: '<id>'`. Leave `mp4` empty and `poster` as is. Update the comment's "rev 5, 315 MB"
   to "rev 6 (final), ~400 MB".
2. **Batch it with any other pending code change if one exists** — every push redeploys and wipes the in-memory locked
   holds and the analysis cache (memory `deploy-drops-locked-holds`); a visitor mid-funnel at that moment loses their held
   image. Deploy in a quiet minute (check PostHog live events), not right after a `generation_started`.
3. Commit, push, confirm the Railway deploy (`~/.npm-global/bin/railway deployment list --service abs-by-ai --json`).

## Step 3 — verify LIVE, both pages

- `curl -s https://absbyai.com/site-video.js` shows the id.
- `/start`: load `https://absbyai.com/start?v=a` and `?v=b` in the Browser pane; assert the iframe `src` contains
  `youtube-nocookie.com/embed/<id>`, that it renders above the fold on a 390-px viewport (`resize_window` mobile), and
  that the sticky CTA still works below it. Take one screenshot of each.
- Analysis page: the real page only renders after a lock-in, so use the local funnel recipe (memory
  `local-funnel-test-recipe`: live-key launch config, seed a before/after, lock in) with the same `site-video.js`, and
  check `#analysisVideoBlock` is visible with the iframe; then on LIVE confirm at least that `?vp=1` no longer shows the
  placeholder text but the real embed (the block reads the same object). Screenshot both.
- **Native retest flag:** the analysis page renders inside the iOS/Android apps too. A `youtube-nocookie` iframe plays in
  WKWebView and in the TWA, but say so explicitly in the delivery — Dan must open the analysis page once on each phone.
  (Rule: memory `cross-platform-retest-rule`.)

## Step 4 — housekeeping

- `AI_COORDINATION.md`: the `/start` entry's step (1) ("upload the rev-5 website video … paste the id") and the
  analysis-page entry's "video block is hidden until `youtubeId` …" sentence are DONE — edit those two entries (only
  those; other sessions own the rest of them). The rev-6 delivery entry: on Dan's confirmation the winner is already
  renamed, so delete it once the install is live.
- `Docs/VSL_LANDING.md`: record the video id, the upload date, unlisted, and where the master lives.
- No dashboard row unless Dan asks (his 2026-09-08 rule). Remove this doc from the HANDOFFS list in
  `AI_COORDINATION.md` and from `Handoffs/README.md` in the session that runs it.
- The `Website Videos/` folder is git-ignored (`.gitignore`, 2026-09-09) — nothing from it may be committed; the repo is
  public.

## Starter Prompt

> Execute `Handoffs/handoff-20260909-website-video-youtube-install.md`: upload the finalized website conversion video
> (`Website Videos/Website Conversion Video (post-generation)/website_video_16x9.mp4`, rev 6 version A, ~400 MB) to
> YouTube as **Unlisted**, then install its id in `youtubeId` in `public/site-video.js` so the post-lock-in analysis page
> and `/start` both show it, deploy, and verify live on both pages (and the analysis page via the local funnel recipe).
> The Chrome extension cannot upload a file that size and the stored Google token is calendar-only, so either ask me to
> drag it into YouTube Studio or mint a YouTube-scoped token through a local OAuth flow (ask before clicking Allow) and
> upload through the Data API. Batch the one-line change with any other pending code edit (a deploy wipes locked holds),
> flag the native retest, update the two coordination entries and `Docs/VSL_LANDING.md`, and retire this handoff.

**Model:** Fable 5.1, effort **medium** — short, but it touches production and the OAuth path has traps worth the
standing model (memory `astra-vs-fable-verdict`). If Dan does the upload himself, this is a 15-minute session.
