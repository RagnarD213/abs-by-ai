# Handoff — /start hero revisions: drop the video caption, move the subtitle under the button, push the trust copy to the footer

**Written 2026-09-10 (Dan's revisions after seeing Muhammad's Ad 1 live on `/start`). NOT EXECUTED.**

## What Dan asked for, in his words (dictated, 2026-09-10 2:46 PM)

1. "Remove my small circular avatar image and 'Dan Rose, founder · this picture got me abs · 3:53'. Remove that from below the video."
2. "The text 'Upload one photo. In about 20 seconds…' (that whole paragraph): move that below the button."
3. "Remove the text 'Free to try · About 20 seconds · No sign-up to see it' and 'Your photo is sent securely to our AI partners…'."
4. "Move this text to the bottom of the page. Keep the privacy policy link here, though."

He was looking at **variant A (`?v=a`, `control`) at phone width** (Chrome device toolbar, 379 px wide). Reading of 3 + 4:
both lines leave the spot under the button and reappear at the bottom of the page; a bare **Privacy Policy** link stays under
the button. (The two asks were dictated as one thought — the "this text" of 4 is the text removed in 3.)

## The page today — `public/start.html`

Everything is in ONE file; the video config lives in `public/site-video.js` (`ABS_START_VIDEO`, do not touch).

| # | Element | Where | Notes |
|---|---|---|---|
| 1 | `<div class="video-cap">` (avatar `img` + `<span id="heroVideoCap">`) | line ~293, inside `#heroVideoBlock` | CSS `.video-cap` / `.video-cap img` lines ~136–137. The inline script writes `heroVideoCap` when `ABS_START_VIDEO` has an id — it is already null-guarded (`const cap = $('heroVideoCap'); if (cap) …`), so deleting the markup is safe; delete the dead write + the `.video-cap` CSS too. |
| 2 | `<p class="sub only-control">Upload one photo. In about 20 seconds…</p>` | line ~268, directly under the `<h1>` | Variant B has its own `<p class="sub only-analysis">` at line ~272. On phones `#heroVisualMobile` (line ~274, where the video lands) sits between the subtitle and `#ctaBlock` (line ~276). |
| 3 | `<div class="cta-note">` (three chips) + `<div class="cta-legal">` (privacy sentence + link) | lines ~283–284, inside `#ctaBlock` under the button | CSS `.cta-note`, `.cta-note span + span::before`, `.cta-legal`, `.cta-legal a` at lines ~171–174. |
| 4 | Bottom of the page | `<div class="legal">` (line ~456) then `<div class="footer-links">` (line ~458), then the sticky CTA | The sticky mobile CTA `#stickyCta` is separate — leave it. |

## The change (one commit)

1. **Delete** the `.video-cap` div, its two CSS rules, and the `heroVideoCap` write in the script. Keep `#heroVideoFrame` and the
   `title`/`lengthLabel` fields in `site-video.js` (variant B's `#sectionVideoH` still uses `title`).
2. **Move the subtitle under the button.** Cut both `<p class="sub …>` paragraphs (control AND analysis — keep the A/B layouts
   identical so the test is not confounded; note this default in the report) and place them inside `#ctaBlock` **after** the
   `<button>`. Give `.sub` a `margin-top` (≈12 px) instead of `margin-bottom`, and centre it to match the button
   (`text-align:center`) — check the desktop layout too, where the copy column sits beside the visual.
   Resulting phone order, variant A: `h1 → video → button → subtitle → Privacy Policy`. Variant B: `h1 → phone mock → button → subtitle → Privacy Policy`.
3. **Under the button, replace** `.cta-note` + `.cta-legal` with a single `<div class="cta-legal"><a href="/privacy">Privacy Policy</a></div>`.
4. **At the bottom**, immediately above `<div class="footer-links">`, add the removed copy back: the three chips
   (`Free to try · About 20 seconds · No sign-up to see it`) and the full sentence "Your photo is sent securely to our AI partners
   (Anthropic, Google, Replicate) to create your result — never sold, delete anytime." with its Privacy Policy link. Reuse the
   `.cta-note` / `.cta-legal` classes so nothing new is styled; give the block a little top margin so it does not run into `.legal`.
5. Don't touch: the `<meta>` description/og tags (they carry the same sentence for search/social and are not on-page copy), the
   FAQ answer that repeats the privacy sentence, `#stickyCta`, the PostHog `vsl_*` events, `ABS_START_VIDEO`.

## Verify

- Local first (`preview_start` name `abs-by-ai`), then live after the deploy: `absbyai.com/start?v=a` and `?v=b`, **phone width
  (375) and desktop**. Confirm: no avatar/caption under the video; subtitle sits under the button; only "Privacy Policy" under
  it; chips + privacy sentence sit above the footer links; the sticky CTA still appears once the hero button scrolls out;
  variant B's video section still renders its heading; no console errors; `git diff` touches only `public/start.html`.
- Screenshot both variants at phone width and send them with the report.
- `/start` is **web-only** → no native retest. One push (a push wipes in-memory locked holds — memory `deploy-drops-locked-holds`).

## Close out

Remove this doc from `AI_COORDINATION.md` (HANDOFFS) and `Handoffs/README.md` (Open table). No dashboard row exists for it
(Dan's 09-08 rule); nothing to check off. Delete the coordination entry "/start video — INTERIM AD 1 LIVE" if Dan has seen the page.

## Recommended model and starter prompt

Opus 5, medium effort — one HTML/CSS file, well specified, plus a live check. (Fable is not needed for this.)

```
Execute Handoffs/handoff-20260910-start-hero-copy-revisions.md: apply Dan's four /start hero revisions to
public/start.html exactly as the doc specifies (drop the video caption + avatar, subtitle under the button, only a Privacy
Policy link under the button, the chips + privacy sentence moved above the footer links), verify locally then live in both
variants at phone width and desktop, send screenshots, commit + push, and close the doc out of the coordination file and
Handoffs/README.md.
```
