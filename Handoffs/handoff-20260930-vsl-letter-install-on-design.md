# Handoff: install Dan's final sales letter on the approved VSL landing design

Written 2026-09-30 by Claude (Opus 5.5). Not executed. Design-canvas work only: no live-site build in this task.

## 1. Goal

Put Dan's finalized sales letter, word for word, onto the approved Round 2 landing page design, and design every new
section the letter introduces so the whole page reads as one finished mockup. The output is what the later build task
codes into the live page.

## 2. Where everything is

| item | where |
|---|---|
| Design canvas (private) | https://claude.ai/artifact/GM8Han9hMfSHNf625vqtyu, page **Round 2** |
| Version A (no 7-day list) | `project/R2-Letter.dc.html` (390 x 6500) |
| Version B (with "Your First 7 Days") | `project/R2-Letter-Week.dc.html` (390 x 7100) |
| Sound box color options | `project/R2-Sound-Overlay.dc.html` |
| Round 1 (five concepts, reference only) | page **Round 1**, do not edit |
| Dan's final letter | the Google Doc link Dan pastes in the starter prompt. Read it with the Google Docs / Google Drive connector |
| Earlier research | `Handoffs/handoff-20260924-vsl-landing-five-mockups.md` (executed; background only) |

Uploaded images already in the canvas (use these URLs verbatim in `<img src>`):
- logo `/_blob/bf9335dac3fc2f8d33819a110ab2cce3` (black on transparent; `filter: invert(1)` on dark backgrounds)
- video poster `/_blob/818cf8f3f239f5e2a1a071908f085ba2`
- Dan founder photo `/_blob/3af9ad97992abf1b1eae6677f684fbd6`
- Dan avatar `/_blob/28e9f4b3a38a0f85455b0362d64b18e1`
- Dan pool pose `/_blob/f19ece8afa07caa435fed6c33c583618`

## 3. What is locked (do not redesign)

The top of the page, as in Round 2 A and B:
1. Dark top stripe pinned while scrolling: "7-Day Free Trial / $0 today" + green "Start Free Trial" button. No bottom sticky bar.
2. Small logo, eyebrow line, headline (Title Case, red highlight on the payoff phrase).
3. Full-width 16:9 video with the "Your video is playing / Tap to turn on sound" box (yellow is the recommended default;
   the `overlay` tweak switches colors), then "Make sure your sound is on".
4. Offer card right under the video: title, three check lines, green **Start My 7-Day Free Trial** button, terms line.

Change the headline, eyebrow or offer card text only if Dan's doc explicitly gives new text for them.

Design system (keep it): Manrope 500/600/700/800 (Google Fonts); ink `#05070B`; paper `#F6F4F0`; body text `#2B2F36` /
`#3F444C`; red accent `#C9302D` for highlights, eyebrows and check marks only; **green `#15803D` only on buy buttons**
(nothing else on the page is green); yellow `#FFD23F` only on the sound box. Buttons 58 px tall, 12 px radius, 18 px
800 weight. Section padding 32 to 40 px vertical, 20 px side gutters on the phone. Alternate white and paper
backgrounds between sections; one dark (`#05070B`) section at most every few screens, as the 165-hours block does.

Keep the Tweaks on both boards: `cta` (green shades), `overlay` (sound box color), `eyebrow`, `week`.

## 4. The work

1. Read Dan's doc in full. List its sections in order and compare them with the current Round 2 letter
   (story, pull quote, 165 hours grid, "This is for you if", five helpers, cost comparison, before/after,
   first 7 days, FAQ, final button). Mark each doc section as: existing (reuse the block), changed, or **new**.
2. Install the text **verbatim**. Do not rewrite, trim or "improve" Dan's copy. If something will not fit a layout,
   change the layout, not the words. If the doc contains an em dash, keep Dan's text but tell him in chat (house rule:
   no em dashes in new writing).
3. Design each **new** section properly in the system above: pick the layout that suits its content (list, cards, table,
   comparison, quote, timeline, stat row, image plus text). Do not force new content into an old block that doesn't fit.
4. `[VISUAL: ...]` markers in the doc become real assets where one exists in the canvas, otherwise a labelled striped
   placeholder (`.ph` class) naming exactly what goes there. App screenshots and Dan's "before" photo are still
   placeholders.
5. Button repeats: a green button block after every two or three sections, using the short headings Dan's doc gives
   above each button. The final section ends in a button plus the terms line.
6. The 7-day list: if the doc includes it, A stays without it and B has it (the `week` tweak). If the doc leaves it out,
   drop it from B too and say so.
7. Also add one **desktop board (1280 wide) of the full final page**, single centered column about 720 px, on the
   Round 2 page to the right of the existing boards. The build task needs it.
8. Update the Round 2 sticky notes so they describe the new state. Leave Round 1 untouched.

## 5. Canvas mechanics (the traps)

- This is a Design-type artifact. Only files under `project/` are yours. Before editing, `read` `project/canvas.json`
  and each Round 2 board from the artifact (Dan may have edited in the page), save them under one scratch folder at the
  same `project/...` paths, edit there, then publish with `url` = the canvas link, `root` = that folder,
  `file_path` = one changed file, `files` = the other changed files. Send `canvas.json` only when boards are added,
  moved or resized, keeping every other key as read.
- Every board's root element has a **fixed height** that must equal its `h` in `canvas.json` and its `$preview`.
  Estimate generously: content past the height is clipped. The footer has `flex-grow: 1`, so extra height just becomes
  footer. The Round 1 boards had to be raised 10 to 15 percent after the first estimate.
- `{{hole}}` holds a name only, never an expression; compute in `renderVals()`. The 165-hours grid is built from a
  `cells` array there; keep it.
- Before publishing: `grep -c '—' project/*.html` must be 0 on everything you wrote.
- Do not render, screenshot or re-read the canvas to check it unless Dan asks.

## 6. Out of scope

Building the live page, touching `public/start.html` or any site code, changing ad destinations, creating PostHog flags.
That is the next task after Dan approves this canvas.

## 7. Done means

- Round 2 A and B carry the full letter verbatim with every new section designed, plus the full-page desktop board.
- Chat message to Dan: the canvas link, what is new, which sections you redesigned and why, any text that did not fit,
  and the one or two decisions left (7-day list in or out, sound box color if not yet picked).
- Update Dan's decision line for the VSL landing page in `AI_COORDINATION.md`, remove this handoff's line from the
  HANDOFFS section and its row from `Handoffs/README.md`, run `scripts/board-check.sh`, commit and push.

## Starter prompt

> Read `Handoffs/handoff-20260930-vsl-letter-install-on-design.md` in full. My finalized sales letter is here:
> [PASTE GOOGLE DOC LINK]. Install it word for word on the Round 2 design in the canvas
> https://claude.ai/artifact/GM8Han9hMfSHNf625vqtyu, keep the locked top of the page, design every new section the
> letter adds, and add a full-page desktop board. Mockups only: do not touch the live site.

Recommended model: **Claude Opus 5.5, high effort.** The words are final, so this is layout and design judgment, not
writing; Fable is not needed.
