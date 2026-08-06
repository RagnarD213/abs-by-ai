---
name: ad-outlines
description: >
  Write a NEW ad/video outline as a variation of one Dan already wrote, and insert
  it into his Google Doc "Abs By AI ad outlines - batch 1" in the right place. Use
  whenever Dan asks for another outline "like" an existing one, a variation on a
  theme (swap trainers → nutritionists, coaches, meal-plan services, supplements),
  or to add a new outline to the outlines doc — even if he doesn't say
  "/ad-outlines". For turning a FINISHED outline into a word-for-word teleprompter
  script, use /scriptwriting instead. For AI-generated video ads, use /make-ad.
---

# Ad outlines: write a variation of Dan's existing outline

**STATUS: v1 — created 2026-08-06 from the approved "Stop Paying Human
Nutritionists! Use AI Instead" outline, written as a variation of Dan's "Stop
Paying Human Trainers!" outline. Dan's verdict: "This outline looks excellent.
Great work… I want you to do it exactly like this."**

## The job

Dan writes an outline he likes, then asks for the same outline aimed at a different
target ("same thing but about nutritionists"). The deliverable is a new outline in
his doc, indistinguishable in structure and voice from the one he wrote, placed
**directly below the source outline and above the blank TEMPLATE blocks** unless he
says otherwise.

## Method — mirror the source beat-for-beat, then upgrade one section

This is the part that made v1 land. Do all four:

1. **Read the source outline in full first** (Drive MCP `read_file_content` on
   `160O1s3xcUGlVU_BjtZR5u_V2WgE9JSREUftUTPuZQEw`). Never write from the theme alone.
2. **Keep the source's skeleton exactly** — same section headers (Skip stopper →
   Believable promise → Conditioning content → CTA 1 → Conditioning content → CTA 2),
   same bullet nesting depth, same number of arguments in the same order, same
   bracketed cue points at the same beats. If the source has 4 "why AI wins"
   arguments, the variation has 4, in the same sequence (cost → generic vs
   personalized → bro-science vs science → always-with-you).
3. **Swap the noun, keep Dan's credentials true.** Trainer → nutritionist means his
   credential line changes ("I've written nutrition programs for hundreds of
   thousands of people") but the SixPackAbs.com channel proof and the Six Pack
   Shortcuts clip cue stay. Never invent a credential he doesn't have.
4. **Upgrade the one section where the new angle is genuinely stronger,** and leave
   the rest parallel. In v1 that was "too expensive to be with you at every meal" —
   photo-logging a plate, ordering off a menu, GLP-1 adjustments — because the app's
   real nutrition features are more concrete than the training ones. One added
   personal line is welcome if it sharpens the angle ("I knew exactly what to eat,
   and I still ate like garbage"). Don't pad other sections to match its length.

## Voice

Same rules as `/scriptwriting` (read that skill's Voice section — it's derived from
Dan's real transcripts). For outlines specifically:

- Outlines are half-drafted prose, half shorthand. Match the source's register: some
  bullets are full spoken sentences, some are directions to himself.
- Keep his phrases: "lose your belly fat", "six pack abs", "Listen -", "a 38 year old
  Dad running a successful ad agency", "stubborn stomach fat".
- Cues in ALL CAPS inside square brackets, matching the source's wording style
  (`[SHOW BEFORE PICTURE]`, `[SHOW 3-5 BEST SHOTS FROM PHOTO SHOOT]`).
- Em-dash asides are fine; keep sentences short.

## Settled compliance calls (don't relitigate)

- **GLP-1 stays generic** — "if you're on a GLP-1 medication", never naming Dan's own
  use, unless he asks for it.
- **Supplement language stays softened** — "which ones aren't worth your money", NOT
  "which ones you should stop taking" (the Google Ads pre-review wording shipped on
  the site, commit `59e943b`).
- Positive/aspirational framing, no body-shaming, no medical claims.

## Delivery into the Google Doc — the exact mechanics that work

**Doc:** "Abs By AI ad outlines - batch 1" —
`160O1s3xcUGlVU_BjtZR5u_V2WgE9JSREUftUTPuZQEw`.

The Drive MCP **cannot edit an existing Google Doc**, so delivery goes through Dan's
logged-in Chrome (`claude-in-chrome`). Typing nested bullets key-by-key is slow and
error-prone. Paste formatted HTML instead:

1. **Write the outline as an HTML file** to the scratchpad: `<p><b>Title</b></p>`
   then nested `<ul>` matching the source's indent depth. Set
   `font-family: Arial; font-size: 11pt` on the body so it matches the doc. Use
   `&rsquo;`/`&mdash;` entities. End the file with a `<p>&ndash;</p>` separator so the
   new section closes the way the others do. Keep real links as `<a href>` (the
   SixPackAbs.com line).
2. **Put it on the macOS clipboard with the HTML flavor** — this is the load-bearing
   step:
   ```bash
   python3 -c "
   import subprocess
   h=open('outline.html','rb').read().hex()
   subprocess.run(['osascript','-e','set the clipboard to «data HTML'+h+'»'],check=True)"
   ```
   Verify with `osascript -e 'clipboard info'` → should report `«class HTML», <bytes>`.
3. **In Chrome:** open the doc, `cmd+f`, type a unique phrase from the END of the
   source outline (e.g. "let your AI trainer help you make it a reality"), Enter,
   Escape. Screenshot to find the `–` separator line below it.
4. **Click on that `–` line** → `cmd+Right` (end of line) → `Return` → `cmd+v`.
   Screenshot to confirm.
5. **Verify** by re-reading the doc through the Drive MCP and confirming the new
   outline sits between the source outline and the first `TEMPLATE`, with the source
   outline unchanged.
6. Close the tab; stop any local server.

### Gotchas that cost time in v1 — do not re-derive

- **`cmd+c` driven through the browser extension does NOT populate the macOS
  clipboard.** It silently leaves whatever was there before, so `cmd+v` pastes
  something unrelated (in v1 it pasted an old Google Docs URL into the doc). The
  `osascript` HTML-flavor write above is the reliable path. Serving the HTML on
  localhost and copying from the rendered page is NOT needed.
- **Recovery is easy and safe:** `Escape` (dismiss any smart-chip popup) then
  `cmd+z` ×2 restores the doc. Screenshot to confirm before retrying.
- **The find box swallows the first typed string** if you type immediately after
  `cmd+f`. Screenshot, click into the field, then type.
- **`scroll_amount` on the Chrome computer tool maxes at 10.**
- Paste into the plain `–` paragraph, never into a bullet — pasting inside a list
  makes the new content inherit the list level.

## Checklist before telling Dan it's done

- [ ] New outline reads as a sibling of the source, not a rewrite of it
- [ ] Same section headers, same order, same nesting depth
- [ ] Cues present at the same beats as the source
- [ ] Compliance calls above honored
- [ ] Placed below the source outline, above the first TEMPLATE
- [ ] Source outline verified unchanged (Drive MCP re-read)
- [ ] Summary in chat names the beats mirrored and flags any judgment calls
