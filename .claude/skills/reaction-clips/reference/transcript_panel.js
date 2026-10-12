// Read a YouTube video's transcript, with times, from the page itself. Use when yt.py answers NO TRANSCRIPT
// because YouTube is rate-limiting caption downloads (HTTP 429).
//
// How: open https://www.youtube.com/watch?v=ID in the built-in browser, wait 4 seconds, then run this whole file
// with the browser's javascript tool, ending with one of the calls at the bottom. Several videos fit in one
// browser_batch (navigate, wait, run; navigate, wait, run).
//
// T(null, 0, 2500)                    the first 2,500 characters of the transcript
// T(/soda|pounds|calorie/i, 1, 2500)  only lines that match, plus 1 line either side (use this on long videos)
//
// Traps this handles: the video is paused and muted first; a video with chapters opens the panel on a
// "Timeline" tab, so the "Transcript" tab is clicked when no lines appear; lines are
// <transcript-segment-view-model> elements, not the older ytd-transcript-segment-renderer.
// A result of "0 ::" means YouTube showed no transcript for that video: try once more, then pick the second by eye
// (seek the video with document.querySelector('video').currentTime = N and take a screenshot).
const T = async (rx, ctx, max) => {
  const v = document.querySelector('video'); if (v) { v.pause(); v.muted = true; }
  const seg = () => document.querySelectorAll('transcript-segment-view-model').length;
  const w = ms => new Promise(r => setTimeout(r, ms));
  const btn = re => [...document.querySelectorAll('button')].find(x => re.test((x.textContent || '').trim()) && x.offsetParent);
  document.querySelector('#description #expand, tp-yt-paper-button#expand')?.click();
  await w(1500);
  btn(/^show transcript$/i)?.click();
  for (let i = 0; i < 8 && !seg(); i++) await w(600);
  if (!seg()) { btn(/^transcript$/i)?.click(); for (let i = 0; i < 10 && !seg(); i++) await w(600); }
  await w(1200);
  const s = [...document.querySelectorAll('transcript-segment-view-model')].map(e => e.innerText.replace(/\s+/g, ' ').trim()
    .replace(/^(\S+) (?:\d+ hours?, )?(?:\d+ minutes?, )?\d+ seconds? /, '$1 '));
  if (!rx) return s.length + ' :: ' + s.join(' | ').slice(0, max);
  const keep = new Set();
  s.forEach((x, i) => { if (rx.test(x)) for (let j = i - ctx; j <= i + ctx; j++) keep.add(j); });
  return s.length + ' :: ' + s.filter((x, i) => keep.has(i)).join(' | ').slice(0, max);
};
await T(null, 0, 2500)
