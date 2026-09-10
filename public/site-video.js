// The website conversion video, in ONE place. Both the ad landing page (/start)
// and the post-lock-in "Your analysis" page (index.html, ANALYSIS_VIDEO) read it.
//
// The master is `claude edited long form content/06 - Website Conversion Video
// (post-generation)/website_video_16x9.mp4` (rev 6 version A — Dan's final, 3:50,
// 1920x1080; identical to the copy in `Website Videos/`). It is ~424 MB, far past
// anything that belongs in this public repo, so it is hosted
// on YouTube as an UNLISTED upload. Paste the 11-character video id below
// (the part after `watch?v=`) and both pages light up on the next deploy.
// `mp4` is an alternative for a self-hosted file; `poster` is the frame shown
// before play (and the landing page's share image).
//
// Every push redeploys and wipes in-memory locked holds (memory:
// deploy-drops-locked-holds) — set this alongside other code changes when possible.
// Uploaded 2026-09-09 by scripts/youtube/upload.js (unlisted, embeddable, on the
// "Abs by AI" channel): https://www.youtube.com/watch?v=CwEGFxpIM-E
window.ABS_SITE_VIDEO = { youtubeId: 'CwEGFxpIM-E', mp4: '', poster: '/img/video-poster.jpg' };

// The short video INSIDE the web cart (the pay-first checkout, 2026-09-10).
// Placeholder until Dan has the file: with both fields empty the slot is hidden
// for real visitors and a labelled placeholder shows on localhost, ?vp=1 and
// /?demo=checkout. Fill `youtubeId` (unlisted upload) or `mp4` (a hosted file —
// better here, a YouTube embed carries a "Watch on YouTube" exit).
window.ABS_CART_VIDEO = { youtubeId: '', mp4: '', poster: '' };
