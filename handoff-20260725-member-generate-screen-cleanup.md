# Handoff: Hide the marketing hero + proof banner for logged-in members on the generate screen

**Date:** 2026-07-25
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** App adoption (member retention / usability), and it unblocks a Google Play compliance test that gates the Android launch.

## Objective

When a logged-in member taps **Generate New Image** on the member hub, they currently land at the top of the acquisition marketing page — the "Visualize Yourself With Abs" headline and the before/after proof banner — with the actual "Add your photo" upload card pushed to or past the bottom of the screen. Members read this as "the button did nothing / it bounced me back to the home screen." Fix it by hiding the two marketing blocks for logged-in members with active access, so a member lands directly on the upload card, while logged-out visitors keep the full sales page exactly as it is today.

This is web-only (`public/index.html`). Both native wrappers load the live site, so one Railway deploy fixes the Android app, the iOS app, and the website together.

## Current State

**The Android app is live on Google Play's internal testing track** (published 2026-07-25 3:49 PM, v1/1.0, `com.absbyai.app`). Dan installed it and verified two of three acceptance checks:

- ✅ Opens full-screen, no address bar (the `assetlinks.json` fix shipped today, commit `448ca32`)
- ✅ Photo upload + generation works
- ⬜ **No buy buttons on credits/membership** — *partially* verified. The membership upsell on the member hub correctly hides its buy buttons. The **credits paywall was never reached**, because Dan tried to exhaust his credits by tapping "Generate New Image" and hit the bug this handoff fixes. This is the last open item on the Android acceptance checklist.

**Poster/Stripe checkout is correct and must not be touched.** Google requires *digital* goods to use Play Billing; *physical* goods (printed posters/canvas) must use a normal processor. Dan flagged the Stripe option on posters as a possible issue — it is not. See `public/index.html:2708`.

### The bug, with measurements

`openHubFeature('generate')` → `showScreen('form')` (`public/index.html:4457`). `showScreen` swaps section visibility and calls `window.scrollTo({top: 0})` (`public/index.html:3195`). It never resets or repositions the form. The top of `#formSection` is the marketing hero.

Reproduced on production at 375×812 using the Apple-reviewer demo account (a comp member with a saved transformation — the same state Dan is in):

| Proof banner state | Proof banner height | `#uploadCard` top | Result |
|---|---|---|---|
| Expanded (fresh session) | 268px | **475px** (card bottom 841px) | Card bottoms out **past the 812px fold** |
| Collapsed (after one auto-rotation) | 50px | 249px | Card visible |

The proof banner only shrinks to the slim "See examples" strip *after* it has auto-rotated through every slide once, and that state lives in `sessionStorage` (`absbyai_proof_strip_collapsed` / `absbyai_proof_strip_seen`). **A fresh app launch always gets the tall version**, which is why Dan hit it reliably on the phone and why it can look fine on a warm desktop tab.

**This is not Android-specific.** It reproduces identically in a desktop browser for any logged-in member.

## Key Decisions Already Made

- **Option 2 chosen over Option 1.** Option 1 was "leave the page alone but auto-scroll the member down to the upload card." Dan chose Option 2 — actually hide the marketing blocks for members — because a paying member should get a tool, not an ad. Do not relitigate; build Option 2. (Option 1's scroll-to-top behavior is still the underlying mechanism: once the marketing is hidden, `scrollTo(0)` naturally lands on the upload card.)
- **Logged-out visitors must keep the full sales page unchanged.** That hero is the conversion asset for new traffic. This is the single biggest risk in the task.
- **Gate on membership, not merely on being logged in.** Use the existing `hasMemberAccess()` helper (`public/index.html:4441`), which returns true for `memberState.active` or `status === 'comp'`. A logged-in but *inactive* user is still in the funnel and should keep seeing the sales page — this matches `isHubPreviewMode()` (`public/index.html:4445`), which already treats logged-in-without-access as preview mode.
- **Do not touch the poster/Stripe checkout path.** Verified correct; changing it would create the violation, not fix one.

## Detailed Plan

1. **Add stable hooks to the two marketing blocks** in `#formSection`:
   - `public/index.html:1464` — `<div class="hero-h1">Visualize Yourself With Abs</div>`
   - `public/index.html:1465` — `<div class="hero-sub">See how good you'd look with abs…</div>`
   - `public/index.html:1467` — `<section id="proofStrip" …>`

   Preferred approach: wrap the hero h1 + sub in a single container (e.g. `<div id="formMarketingHero">`) rather than tagging each. `#proofStrip` already has an id.

   ⚠️ **Do NOT write a bare `.hero-h1 { display:none }` rule.** `.hero-h1` and `.hero-sub` are reused on at least three other screens — the result screen (`:1675`), the chooser (`:1804`), and the email-capture screen (`:1853`). Any selector must be scoped to `#formSection`.

2. **Add a body/root class toggle**, following the pattern already proven by `IS_NATIVE_APP` → `document.documentElement.classList.add('native-app')` (`public/index.html:2718`) and its CSS at `:1216–1219`. Suggested: add/remove a `member-mode` class on `<html>` whenever membership state is resolved.

3. **Drive the toggle from the places membership changes**, not just page load. At minimum: `refreshMembership()`, `restoreSession()` (`:4305`), post-login (`:4390`+), and post-checkout. A membership state that resolves *after* first paint must still hide the hero — otherwise the member sees a flash of marketing.

4. **CSS:** `.member-mode #formSection #formMarketingHero, .member-mode #formSection #proofStrip { display: none; }`

5. **Verify `initProofStrip()` degrades safely.** It queries `#proofStrip` and attaches an `IntersectionObserver`, rotation timers, and swipe handlers (`public/index.html:~3208`+). With the element `display:none` it will never intersect, so rotation should simply never start — confirm no console errors and no runaway timers. If it throws, guard the init with an early return when the strip is hidden.

6. **Test matrix** (all at 375×812, and spot-check desktop):
   - Logged-out visitor → full sales page, hero + proof banner present, unchanged
   - Logged-in **without** active membership → full sales page (still in the funnel)
   - Logged-in **comp/active member** → `#uploadCard` top is near 0 and fully above the fold; no hero, no proof banner
   - Member on a **fresh session** (clear `sessionStorage` first — this is the state that actually broke)
   - Result screen, chooser screen, email-capture screen → their own `.hero-h1`/`.hero-sub` still render (regression check for step 1's warning)
   - No console errors on any of the above

7. **Ship it:** commit, push to `main`, confirm the Railway deploy, and verify on live `absbyai.com` — per `AGENTS.md` these are required parts of the change, not follow-ups.

8. **Then close out the Android checklist.** On the phone, in the Play-installed app: tap Generate New Image, confirm you land on the upload card, burn the remaining credits, and confirm the **credits paywall shows no buy buttons and displays the "not available for purchase in the app" note**. Check off the dashboard key task `money::Android app: confirm NO buy buttons on the credits and membership screens` via `POST /api/task-checks`.

**OPEN (minor, decide while building):** whether a member should still be able to reach the examples. Recommendation: no — they have their own transformations in My Transformations. Don't build a toggle unless it falls out for free.

## Things to Avoid / Lessons Learned

- **`.hero-h1` / `.hero-sub` are shared classes across four screens.** Scope every selector to `#formSection`. This is the most likely way to break something unrelated.
- **`showScreen()` never resets form state.** It only flips `display` and scrolls to top. Don't assume entering the form clears the previously uploaded photo.
- **The proof banner's collapsed state is per-session, not persistent.** Always clear `sessionStorage` before testing, or you'll test the wrong (working) state and conclude there's no bug.
- **Two agents in one browser fight.** A scheduled task (`submit-android-app-after-org-wait`) fired mid-session today and drove the same Chrome window Dan and Claude were using, silently creating Play Console records. If a scheduled task may be active, check before driving the browser.
- **Claude cannot upload local files through the browser tools** (`file_upload` rejects paths outside the session folder), and **Gmail blocks `.apk` attachments** — neither is a workaround worth retrying.
- **Railway watch paths** exclude the eight `*-data.json` files, so writing todos/task-checks does not trigger a redeploy. Editing `public/index.html` does.

## Relevant Files & Locations

| Item | Location |
|---|---|
| The file being changed | `public/index.html` |
| Hero h1 / sub (form screen) | `public/index.html:1464–1465` |
| Proof banner | `public/index.html:1467` (`#proofStrip`) |
| Upload card | `public/index.html:1526` (`#uploadCard`) |
| `showScreen()` | `public/index.html:3195` |
| `hasMemberAccess()` / `isHubPreviewMode()` | `public/index.html:4441` / `:4445` |
| `openHubFeature()` — generate route | `public/index.html:4457` |
| `restoreSession()` | `public/index.html:4305` |
| Native-app class pattern to copy | `public/index.html:2705–2718`, CSS `:1216–1219` |
| Shared `.hero-*` reuse (regression risk) | `public/index.html:1675`, `:1804`, `:1853` |
| Repo | `RagnarD213/abs-by-ai`, deploys to absbyai.com via Railway on push to `main` |
| Demo member account for testing | `danroseconsulting+applereview@gmail.com` — password in `app-store-assets/LISTING_COPY.md` (comp member, has a saved transformation) |
| Dashboard task to check off afterward | `POST /api/task-checks`, id `money::Android app: confirm NO buy buttons on the credits and membership screens` |

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Sonnet 5, standard thinking.** Single-file, well-specified change with an explicit test matrix. Sonnet handles this comfortably — no need for Opus. |
| **If Claude usage is high / approaching a limit** | **Codex (current flagship), medium effort.** The plan above is concrete enough that Codex can execute it without design judgment. Drop to a mini-tier model at low effort only if you want to save further — the change is small, but the shared-CSS-class trap is a real one and medium effort is worth the insurance. |

No always-Claude override applies: this is routine UI work, not brand copy, architecture, or Anthropic API integration code. Don't over-provision — the ambiguity here is low because the diagnosis is already done and measured.

## Starter Prompt for the Next Task

> Read `handoff-20260725-member-generate-screen-cleanup.md` in the Abs By AI project root and execute it.
>
> Short version: logged-in members who tap "Generate New Image" on the member hub land on the marketing hero ("Visualize Yourself With Abs") plus the before/after proof banner, which pushes the "Add your photo" upload card past the bottom of the screen on a phone — measured at 475px top on a 812px viewport with a fresh session. Members think the button is broken. Fix: hide the hero and the proof banner on the `#formSection` screen for logged-in users with active membership (use the existing `hasMemberAccess()` helper), so members land directly on the upload card. Logged-out visitors and logged-in-but-inactive users must keep the full sales page exactly as it is today.
>
> Critical trap: `.hero-h1` and `.hero-sub` are reused on the result, chooser, and email-capture screens — scope every selector to `#formSection` or you'll break them. Follow the existing `IS_NATIVE_APP` → `.native-app` class pattern at `public/index.html:2705–2718` for the toggle.
>
> First concrete action: open `public/index.html`, wrap lines 1464–1465 (the hero h1 + sub inside `#formSection`) in a container with a stable id, then add the member-gated class toggle and the scoped CSS.
>
> Test at 375×812 with `sessionStorage` cleared, using the comp demo account in `app-store-assets/LISTING_COPY.md`. Then commit, push to `main`, confirm the Railway deploy, and verify live on absbyai.com — that's required, not optional. Finally, tell Dan to finish the last Android check: burn his remaining credits in the Play-installed app and confirm the credits paywall shows no buy buttons.
