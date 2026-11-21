---
name: index-html-screen-nesting
description: "public/index.html is one page of ~25 stacked .screen divs; an unclosed div in one screen silently nests every later screen inside it and they render blank (happened 2026-09-08, fixed 10eda3b)"
metadata: 
  node_type: memory
  type: project
  originSessionId: f6290172-b341-4d83-8d42-ab0bc897ab24
  modified: 2026-09-09T15:40:39.132Z
---

`public/index.html` is a single page of ~25 sibling `<div class="screen">` sections that `renderScreen()` shows one at a time by
setting `display`. On 2026-09-08 the new analysis page (85d81c1) ended with its footer line and never closed its section div, so
every screen after it in the file — hub, macro tracker, trainer, program, nutrition, membership, quiz — became a CHILD of the hidden
analysis section and rendered blank for logged-in members until 2026-09-09 10:36 CT (`10eda3b`). Nothing in the build or the
deploy catches it; the browser parser just nests.

**Why:** a member-facing blackout that lasted ~18 hours and was only found by accident, while capturing the Trainer for a video.

**How to apply:** after ANY edit that adds or restructures a `.screen` in `public/index.html`, run the 10-second check before
pushing: strip `<script>` blocks, count `<div`/`</div>` up to each `id="…Section"` — every screen must sit at div depth 2.
Or in Playwright: `while (e=e.parentElement)` from the new section must reach `.app` in one step. Related: [[deploy-drops-locked-holds]].
