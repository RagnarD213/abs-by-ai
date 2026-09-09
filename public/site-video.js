// The website conversion video, in ONE place. Both the ad landing page (/start)
// and the post-lock-in "Your analysis" page (index.html, ANALYSIS_VIDEO) read it.
//
// The master is `claude edited long form content/06 - Website Conversion Video
// (post-generation)/website_video_16x9.mp4` (rev 5, 3:50, 1920x1080). It is
// 315 MB, far past anything that belongs in this public repo, so it is hosted
// on YouTube as an UNLISTED upload. Paste the 11-character video id below
// (the part after `watch?v=`) and both pages light up on the next deploy.
// `mp4` is an alternative for a self-hosted file; `poster` is the frame shown
// before play (and the landing page's share image).
//
// Every push redeploys and wipes in-memory locked holds (memory:
// deploy-drops-locked-holds) — set this alongside other code changes when possible.
window.ABS_SITE_VIDEO = { youtubeId: '', mp4: '', poster: '/img/video-poster.jpg' };
