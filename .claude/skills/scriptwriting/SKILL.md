---
name: scriptwriting
description: >
  Turn one of Dan's ad or video OUTLINES (usually a Google Doc with images) into a
  finalized word-for-word teleprompter script in Dan's own spoken voice, and deliver
  it into a Google Doc with the outline's images placed at the right cue points.
  Use whenever Dan asks to write, finalize, or "flesh out" a script from an outline,
  or to add a newly finished outline to the finalized-scripts doc — even if he
  doesn't say "/scriptwriting". This is for scripts DAN reads on camera; for
  AI-generated video ads use /make-ad instead.
---

# Scriptwriting: Outline → Finalized Teleprompter Script

**STATUS: v1 — created 2026-08-06 after the approved Ad 1 script ("How AI Got Me
Abs"). Dan's verdict: "really, really good, excellent work."**

## The job

Dan writes outlines with a mix of (a) fully-drafted lines, (b) bare bullet points,
and (c) bracketed visual cues like `[SHOW BEFORE PICTURE ON SCREEN]`, with images
embedded under the cues. The output is a script he reads verbatim on a teleprompter:
spoken words in plain text, cues in **bold bracketed ALL-CAPS** (never read aloud),
images carried over at their exact cue positions, and a word count + runtime
estimate (~150–160 wpm) at the top of each ad.

## Voice rules (derived from his real transcripts — do not drift)

Ground truth: `YouTube Long Form Video Content/six-ways-ai-abs/v2-transcript.txt`
(38 minutes of Dan actually talking) and the approved ad script
`ad-factory/the-upload/script.md`. The finalized Ad 1 in the scripts doc (link
below) is the worked example. Voice traits:

- Direct, conversational second person: "Listen —", "Let's be honest", "here's the
  truth", occasional "you guys".
- Doubled intensifiers: "really, really hard", "far, far better", "so, so".
- Short declarative sentences. One idea per sentence. Em-dash pivots.
- Personal specifics over generalities (200 pounds, 38-year-old dad, lockscreen for
  a year, meal prep, tracking calories). Never replace his specifics with generic ones.
- Core phrase pair: "lose your belly fat" + "six-pack abs" — used constantly, keep it.
- Honest, no-hype framing. He'll say "reasonably accurate", he won't overpromise.
- Numbers written out for the teleprompter ("two hundred pounds", "thirty-eight").

## The process

1. **Use Dan's drafted lines nearly verbatim when they're good.** He writes his own
   best hooks. Only rewrite a drafted line if it's clearly weaker than his usual
   voice — and be ready to say what you changed and why. Flesh out bullet-point
   sections fully in his voice.
2. Small connective additions that set up a reveal are welcome (Ad 1 added "it
   looked ridiculous — deep down, you knew that wasn't really you" after the crude
   photoshop cue), but keep them short.
3. **CTAs:** the outline says "tap CTA TEXT below" — write "tap the button below"
   (speakable, button-text-agnostic).
4. **Compliance (settled decisions, don't relitigate):** every AI-generated
   goal/after image shown on screen keeps an "AI-GENERATED" label; Dan's real photos
   need none. Keep claims positive-framed (aspiration, not body-shaming) for ad
   policy safety. Add a short "Production notes" block for anything the editor needs.
5. **Show the script in chat for Dan's approval BEFORE putting it in the Google Doc**
   (first time each ad). Then deliver into the doc.

## Ad outline structure (his template)

Skip stopper → Believable promise → Conditioning content → CTA 1 → Conditioning
content → CTA 2 (+ optional product-detail section → CTA 3). The skip stopper is
the first 5 seconds; the believable promise sets up "in today's episode…" so the ad
feels like content (MadMuscles-style).

## Google Docs mechanics (all proven 2026-08-06 — don't re-derive)

**Docs in play:** outlines = "Abs By AI ad outlines - batch 1"
(`160O1s3xcUGlVU_BjtZR5u_V2WgE9JSREUftUTPuZQEw`); output = "abs-by-ai ads batch 1
finalized scripts for teleprompter"
(`1r3Jmuihyryq0qv2Y3A--D_yaerF9B_ZqAb-QvOuAwjg`).

- **Getting the outline + images:** Drive MCP `download_file_content` with export
  mime `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  (result lands on disk as JSON with base64 `content`), unzip, then walk
  `word/document.xml` paragraphs in order, resolving `r:embed` rIds through
  `word/_rels/document.xml.rels`, to map each image to its cue. Note: the export
  DEDUPES images — one file can be referenced at two cues.
- **The Drive MCP cannot edit an existing Google Doc, and `create_file` can't carry
  multi-MB base64** (token limits). Adding content to Docs goes through the browser
  (claude-in-chrome, Dan's logged-in Chrome).
- **Appending a new ad to the existing doc (preferred — keeps the link):** type the
  text at the end of the finalized doc in Chrome; copy images across by selecting
  each in the outline doc → Ctrl+C → Ctrl+V at the cue point.
- **Creating a doc from scratch (what built v1):** extend
  `build-script-doc-template.js` (in this skill folder; needs `npm install docx`),
  build the .docx, then upload to Drive with the input-interception trick:
  1. Serve the file on localhost with CORS **plus Private Network Access headers**
     (`Access-Control-Allow-Private-Network: true` on OPTIONS) — without PNA the
     page's fetch hangs forever.
  2. In the Drive tab: patch `HTMLInputElement.prototype.click` to capture file
     inputs instead of opening the native picker, click New → File upload, then set
     the captured input's `.files` from a `DataTransfer` built from the localhost
     fetch and dispatch `change`. (Synthetic *drop* events are ignored by Drive —
     trust check. The claude-in-chrome `file_upload` tool's `paths` param was broken.)
  3. Open the uploaded .docx at `docs.google.com/document/d/<id>/edit` → File →
     **Save as Google Docs** (converts; new file id) → trash the .docx intermediate.
  4. Restore the click patch; kill the localhost server.
- **`javascript_tool` gotcha on Google pages:** long awaits time out the tool. Run
  work fire-and-forget writing progress to `window.__state`, poll with a second call.
- **Verify** by re-reading the finished doc through the Drive MCP (text) and
  scrolling it in the browser (images), before giving Dan the link.

## Doc formatting spec (match Ad 1)

- H1 doc title, H2 per ad ("AD N — <Title>"), italic gray usage note up top.
- Cues: bold, small, gold-ish (`#7A6A2E`), e.g. `[CTA 1]`, `[SHOW BEFORE PICTURE ON
  SCREEN]`. Spoken text: 14pt Arial, relaxed line spacing (teleprompter-readable).
- Images centered, ~300px display width (340px for landscape), directly under their cue.
- Per-ad note line: "~N spoken words ≈ M:SS at normal pace."
- End with a "Production notes" section (CTA button wording, AI-label reminder,
  anything editor-facing).

## Lessons

- Dan says "ads"/"abs" interchangeably via dictation — "How AI Got Me Ads" meant
  "Abs". Check phonetics before acting literally (Wispr Flow rule).
- His outline bullets under a cue that look empty in a text export are IMAGES —
  always pull the .docx export to find them.
- Runtime math: his relaxed narration is ~2.3–2.5 words/sec; a ~600-word ad reads
  3:45–4:15.
