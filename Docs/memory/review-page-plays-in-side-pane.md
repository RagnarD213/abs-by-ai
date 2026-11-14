---
name: review-page-plays-in-side-pane
description: "Review pages must play in the Claude app's side browser pane (about 800-1150 px wide), with a video already loaded in the player"
metadata:
  node_type: memory
  type: feedback
  originSessionId: ec46c0f2-9c38-4b9e-901e-ab9ba9671c5a
  modified: 2026-11-14T18:56:53.758Z
---

Dan opens review pages in the Claude app's built-in browser pane beside the chat, not only in full-screen Chrome. On 2026-11-14 (Great Again T VSL round 1, port 9760) he wrote "I can't play the video on the review page. Fix that." The page's shared player only became a side panel at 1500 px or wider; in the pane it was a tall, EMPTY sticky box at the top (no video loaded until a Play button far down the page was clicked), so pressing play did nothing and the box covered most of the pane.

**Why:** the wide-monitor layout was the only one tested (headless Chrome at 1920 px). My interpretation: the fault was layout and an empty player, not a broken file; playback itself worked once a source was set.

**How to apply:** on every review page, (1) load the first or most important video into the shared player at page load (`src` plus poster, `preload="none"`), so the native play button works at once; (2) make the player a fixed side panel from about 760 px up (300 px wide is enough for a vertical video), and only stack it on top below that, capped near a third of the screen height; (3) test at about 800 and 1150 px wide in the in-app pane as well as at 1920 px, with a real play and seek in silent check mode, before sending the link. Related: [[review-page-must-seek]], [[review-page-what-i-decided]].
