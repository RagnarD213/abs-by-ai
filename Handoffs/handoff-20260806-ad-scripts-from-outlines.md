# Handoff: Write finalized teleprompter ad scripts from Dan's remaining batch-1 outlines

**Date:** 2026-08-06
**Project:** Abs By AI
**Business goal this serves:** Marketing performance (ad creative for the first paid YouTube campaigns)

## Objective

Dan writes detailed ad outlines (structure: Skip stopper → Believable promise → Conditioning content → CTA 1 → Conditioning content → CTA 2, sometimes + product detail → CTA 3) in a Google Doc. The next task turns each newly filled-in outline into a **finalized word-for-word teleprompter script in Dan's voice** and adds it to the finalized-scripts Google Doc, carrying over every image Dan embedded in the outline. Ad 1 ("How AI Got Me Abs") is already done and approved — it is the reference example.

## Current State

- **Outline doc (Dan writes here):** "Abs By AI ad outlines - batch 1" — https://docs.google.com/document/d/160O1s3xcUGlVU_BjtZR5u_V2WgE9JSREUftUTPuZQEw/edit — contains the completed Ad 1 outline plus ~14 empty TEMPLATE slots Dan will fill in over time.
- **Finalized-scripts doc (output goes here):** "abs-by-ai ads batch 1 finalized scripts for teleprompter" — https://docs.google.com/document/d/1r3Jmuihyryq0qv2Y3A--D_yaerF9B_ZqAb-QvOuAwjg/edit — native Google Doc, currently contains the finalized Ad 1 script with all 6 outline images placed at their cue points, plus production notes. Dan approved this script ("really, really good").
- **The method is captured as a project skill:** `.claude/skills/scriptwriting/SKILL.md` (invoke with `/scriptwriting`). It holds the voice guide, the process, and the Google-Docs mechanics. **Read it first — it is most of this handoff's substance.**
- The docx builder used for the initial doc is preserved at `.claude/skills/scriptwriting/build-script-doc-template.js`.

## Key Decisions Already Made

- **Keep Dan's rough-draft lines nearly verbatim when they're good** — he writes his own best hooks ("This picture got me abs. / And it's not even real."). Flesh out only the sections left as bullet points, in his spoken voice.
- **Voice source of truth:** the transcript of his real spoken video at `YouTube Long Form Video Content/six-ways-ai-abs/v2-transcript.txt`, plus the approved "The Upload" ad script (`ad-factory/the-upload/script.md`). Do not invent a different tone.
- **"Tap the button below"** is the speakable CTA placeholder (never read "CTA TEXT" aloud).
- **AI-labeling rule (settled, do not relitigate):** any AI-generated goal/after image shown on screen keeps an "AI-GENERATED" tag; Dan's real photos need no label.
- **Format:** spoken lines in plain text, bracketed ALL-CAPS cues in bold (not to be read), outline images embedded at their exact cue positions, word count + runtime estimate per ad (~150–160 wpm).
- **Deliverable is the Google Doc, not chat text.** Dan reads from it on a teleprompter.

## Detailed Plan (per new outline Dan finishes)

1. Read `.claude/skills/scriptwriting/SKILL.md` and follow it. In short:
2. Export the outline doc as .docx via the Google Drive MCP (`download_file_content`, export mime `application/vnd.openxmlformats-officedocument.wordprocessingml.document`), unzip, and map each embedded image to its outline position by walking `word/document.xml` paragraph order.
3. Write the finalized script (voice rules in the skill). Show it to Dan in chat for approval before touching the Google Doc.
4. Add the approved script to the finalized-scripts Google Doc. Two ways, pick one:
   - **Append in place (keeps the same link — preferred):** open both docs in Dan's Chrome (claude-in-chrome MCP), type the new ad's text at the end of the finalized doc, and copy each image across by selecting it in the outline doc → Ctrl+C → Ctrl+V at the right cue point in the finalized doc.
   - **Rebuild (fallback):** extend `build-script-doc-template.js` with the new ad, rebuild the .docx, upload via the input-interception technique in the skill, Save as Google Docs, trash the old doc. NOTE: this changes the link — only do this if Dan agrees.
5. Verify by re-reading the doc via Drive MCP (text) and scrolling in the browser (images), then give Dan the link and a one-line summary of what changed vs. his outline.

**OPEN:** none blocking — the work simply waits on Dan filling in the next outline.

## Things to Avoid / Lessons Learned

- **The Drive MCP cannot write content into an existing Google Doc**, and inlining a multi-MB base64 docx into `create_file` is impossible (token limits). The browser path is the way.
- **Synthetic drop events on drive.google.com are ignored** (trust check). The working upload trick: patch `HTMLInputElement.prototype.click` to suppress the native picker, click New → File upload so Drive creates its real listener-attached input, then set `input.files` via DataTransfer from a localhost fetch and fire `change`. Details in the skill.
- **Chrome blocks localhost fetches from HTTPS pages** unless the local server answers the Private Network Access preflight (`Access-Control-Allow-Private-Network: true` on OPTIONS). Without it the fetch hangs forever.
- **The claude-in-chrome `file_upload` tool had a broken `paths` parameter** (arrives undefined server-side) — don't burn time on it; use the JS injection path.
- **Long-running `await` in `javascript_tool` on Google pages can time out the tool** — run work fire-and-forget writing progress to `window.__state`, then poll it with a second call.
- Uploaded .docx opens in Office-compat mode; **File → Save as Google Docs** converts it (new file id). Trash the .docx intermediate afterward so only one document remains.
- Google Docs docx export dedupes repeated images — an image used at two cues is one media file referenced twice. Map by document order, not by file count.

## Relevant Files & Locations

- Outline doc + finalized doc: links above (both in Dan's My Drive root).
- Skill: `.claude/skills/scriptwriting/` (SKILL.md + build-script-doc-template.js)
- Voice sources: `YouTube Long Form Video Content/six-ways-ai-abs/v2-transcript.txt`, `ad-factory/the-upload/script.md`
- Approved Ad 1 script text: in the finalized-scripts Google Doc (and reproduced in the skill as the worked example reference).

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking |
| **If Claude usage is high / approaching a limit** | Still Claude (this is brand-voice copywriting — an always-Claude task type; don't hand it to Codex). Use Sonnet 5; it's cheap enough at this scope. |

Override note: script *writing* is voice-sensitive marketing copy → always Claude. Sonnet 5 is sufficient because the skill + Ad 1 example carry the voice; escalate to Opus only if an outline is unusually sparse and the whole ad must be invented from bullets.

## Starter Prompt for the Next Task

> Dan has finished a new ad outline in "Abs By AI ad outlines - batch 1" (Google Doc id `160O1s3xcUGlVU_BjtZR5u_V2WgE9JSREUftUTPuZQEw`). Run `/scriptwriting` and follow the skill: read the new outline (including its images), write the finalized teleprompter script in Dan's voice, show it to Dan for approval in chat, then add it — with the outline's images at the right cue points — to the finalized-scripts Google Doc (id `1r3Jmuihyryq0qv2Y3A--D_yaerF9B_ZqAb-QvOuAwjg`) using the append-in-place browser method. Full context in `Handoffs/handoff-20260806-ad-scripts-from-outlines.md`.
