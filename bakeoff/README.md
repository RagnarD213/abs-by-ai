# Model bake-off harness (v2)

Test-only tooling for `handoff-20260724-model-bakeoff-v2.md`. **Nothing here runs in production** — it is never imported by `server.js` or `public/index.html`, and it is not served over HTTP (the server only serves `public/`).

## What it does

Builds the *real* production prompt for a test case, then sends it to six image models directly and saves every candidate, so a human can compare them side by side.

- `prompts.js` — extracts the live `SYSTEM_PROMPT` / `goalSystemPrompt()` straight out of `public/index.html` (read-only) and drives prod `/api/generate-prompt`, exactly as the browser does. Also carries production's `condenseForKontext` logic as the "condensed" prompt variant.
- `cases.js` — the round-1 grid: 6 photos × 2 intensities.
- `adapters.js` — one adapter per model, all returning the same shape.
- `runner.js` — runs a single case × model × prompt-variant cell and caches it on disk, so a rerun never re-spends.
- `build-prompts.js` / `phase1.js` / `phase2.js` — build prompts, verify adapters, run the grid.
- `build-gallery.js` — renders the blind labeling gallery (letters shuffled per case, model names hidden).
- `stats.js` — per-model success/block rate, latency, nominal spend.

## Running it

Needs `bakeoff/.env` (gitignored) with `GEMINI_API_KEY` and `REPLICATE_API_TOKEN`. Pull them from Railway:

```bash
railway variables --service abs-by-ai --kv | grep -E '^(GEMINI_API_KEY|REPLICATE_API_TOKEN)=' > bakeoff/.env
```

Then, from `bakeoff/`:

```bash
node build-prompts.js && node phase1.js && node phase2.js && node stats.js && PART=1 node build-gallery.js && PART=2 node build-gallery.js
```

**Never add a `deviceId` to a test request** — that spends real credits and commits a data file. The harness deliberately omits it.

## Round 1 results

`round1/results.json` — one record per cell (ok/blocked/error, latency, nominal cost).
`round1/key.json` — the blind key: `"<caseId>:<letter>" → model`. Do not reveal until labels are in.
`round1/run-log.txt` — the batch log.

The generated images and source photos are gitignored (55 MB) and live at `round1/images/` and `round1/photos/` on the machine that ran the batch.
