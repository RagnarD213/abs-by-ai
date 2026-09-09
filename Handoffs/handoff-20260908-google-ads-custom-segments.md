# Handoff — Google Ads custom segments for the Abs By AI Demand Gen launch (10 segments + a members exclusion list)

**Written:** 2026-09-08 (Claude Code, Fable 5.1), from the live keyword lists in `Business/google-ads-bulk/`
(gitignored, local only), the 8/13 campaign build doc (`Business/google-ads-campaign-build-20260813.md`) and the
8/31 ads audit in `AI_COORDINATION_ARCHIVE.md`. Every website below was fetched on 09-08 and returned 200; the
Google Play package ids were read from Play search results the same day.
**Status:** PARTIALLY EXECUTED 2026-09-08 — segments 1–6, 8, 9, 10 built and verified (see Execution notes at the bottom); 7a/7b/7c, the members list and Phase 2 remain.
**Fire when:** Dan has said which segments to build (default: all ten). Before the new Demand Gen app campaign is
switched on. ~1.5–2.5 h of driving Google Ads in Dan's Chrome, $0 AI spend, no code, no native retest.
**Not on the dashboard** — Dan's 09-08 rule; add a row only if he asks.

---

## WHAT THIS IS FOR, IN PLAIN TERMS

Dan is building a new Demand Gen campaign for the app itself (09-08 screenshot: the "New audience" dialog with the
Custom segments panel open, an audience draft named `MU 25-54…`). A **custom segment** is a description of a kind of
person, built from search terms, interests, website addresses and app names. Google finds people who match it on
YouTube, Discover and Gmail. These ten segments are the audiences the campaign's ad groups will target. Dan asked for
mirrors of the two search campaigns, AI-for-fitness audiences, app-based audiences by category, plus my own ideas.

**Dan's top-three pick order (09-08):** #2 AI abs preview tool, #5 competitor apps, #9 get abs / belly fat. Build
those first so they exist even if the session dies.

## FOUR FACTS ABOUT CUSTOM SEGMENTS THAT SHAPE THE BUILD

1. **Two segment types, chosen by a radio button, cannot be mixed in one segment.** "People with any of these
   interests or purchase intentions" (the default) or "People who searched for any of these terms on Google". The
   search type only works on Google properties — Demand Gen runs on YouTube, Discover and Gmail, so it is the right
   type for the intent segments. Websites and apps can be added to either type via the two blue links under
   "Expand segment by also including".
2. **Websites and apps mean "people who use sites and apps LIKE these", not visitors of those sites.** Google reads
   the list as a description. Entering madmuscles.com does not retarget MadMuscles' visitors.
3. **The app picker only knows Google Play.** App-based signal is therefore mostly Android. Fine for a web product,
   but do not expect the app lists to reach iPhone users on their own.
4. **No minimum size.** The ~1,000-member floor applies to remarketing lists ("Your data"), not custom segments.
   The insights panel on the right shows an estimate; record it, do not act on it.

**Sensitive terms: keep every prescription / drug term OUT** — Zepbound, Ozempic, Wegovy, Mounjaro, GLP-1,
semaglutide. The dialog's own banner says sensitive keywords serve contextually only or not at all, and on a
reinstated account (2026-08-11) a flagged segment is not worth the risk. If Google shows a warning chip on any
term, remove that term and note it in the results table; do not fight it.

## WHERE TO BUILD

- Account **342-717-0837** = `ocid=8444849202`. Build from **Tools → Shared library → Audience manager → Custom
  segments tab** (probable direct URL `https://ads.google.com/aw/audiences/custom?ocid=8444849202`; if it does
  not render, go through Tools). This keeps the build out of Dan's half-finished campaign draft. Segments built
  here appear in the campaign's "New audience → Custom segments" search box.
- Names follow Dan's existing `type | what` convention (his lists are `website | visited absbyai.com | 30 day`,
  `youtube | watched any video | 30 day`).

## THE TEN SEGMENTS

Model / effort is per segment. **Executor for everything is Fable 5.1** (it is in Dan's Max plan; the cost is
allowance, not dollars, and the Google Ads UI wedges enough that a weaker model burns more retries than it saves).
Effort is what varies: **medium** for a segment that is pure typing, **high** where the picker or a policy
judgment is involved. Cheaper fallback if the Fable allowance is tight: Sonnet 5 at high for the six search-term
segments only.

### Search-term type ("People who searched for any of these terms on Google")

| # | Name | Terms (paste comma-separated, then Enter; verify chip count) | Model / effort |
|---|---|---|---|
| 1 | `custom \| search \| brand` | abs by ai, absbyai, absbyai.com, abs by ai app, abs by ai reviews, abs by ai login, sixpackabs, sixpackabs.com, six pack abs com, sixpackabs app | Fable 5.1 / medium |
| 2 | `custom \| search \| AI abs preview tool` | ai abs generator, ai six pack generator, ai muscle generator, ai abs maker, ai six pack maker, add abs to photo, add six pack to photo, add muscles to photo, put abs on a photo, six pack photo editor, abs photo editor, ai abs photo editor, ai abs filter, six pack filter, muscle filter ai, abs filter app | Fable 5.1 / medium |
| 3 | `custom \| search \| what would I look like` | what would i look like with abs, what would i look like with a six pack, what would i look like with muscles, what would i look like ripped, what would i look like lean, what would i look like if i lost weight, see myself with abs, body transformation simulator, ai body transformation app, ai body transformation generator, ai before and after body, ai fitness visualization | Fable 5.1 / medium |
| 4 | `custom \| search \| AI fitness` | ai fitness app, best ai fitness app, ai personal trainer, ai workout plan, ai workout generator, chatgpt workout plan, ai meal plan, chatgpt meal plan, ai nutritionist, ai diet plan, ai calorie counter, ai body scan, ai body fat calculator, ai fitness coach, ai gym app | Fable 5.1 / medium |
| 5 | `custom \| search \| competitor apps` | madmuscles, mad muscles app, madmuscles reviews, is madmuscles legit, madmuscles alternative, muscle booster app, muscle booster reviews, betterme app, betterme reviews, zing coach, zing coach review, fitbod, freeletics, caliber app, fitnessai, centr app, gigabody, cal ai app, macrofactor, carbon diet coach, rp diet app | Fable 5.1 / medium |
| 9 | `custom \| search \| get abs belly fat` | how to get abs, how to get a six pack, how to get visible abs, how to lose belly fat, lose belly fat fast, lower belly fat, love handles, how to get rid of belly fat men, six pack diet, abs diet, calorie deficit for abs, body fat percentage for abs, how long does it take to get abs, how to get lean, cutting diet, abs after 40, best ab workout, ab workout at home, six pack workout | Fable 5.1 / **high** (policy judgment: drop any term Google flags; never add drug terms) |

Segment 2 and 3 are the non-brand search campaign's six ad groups, deduplicated and split by what the person wants:
2 wants a tool, 3 wants to see a future self. Segment 9 is the family the search campaign deliberately excludes as
negatives (workout, diet, how to get…) — wasteful at $2 a search click, but on Demand Gen views cost cents and
these are the trainer's, nutritionist's and tracker's real customer.

### Interest type ("People with any of these interests or purchase intentions") + websites + apps

| # | Name | Interests | Websites ("People who browse types of websites") | Apps ("People who use types of apps") | Model / effort |
|---|---|---|---|---|---|
| 6 | `custom \| interest \| AI fitness sites` | ai fitness app, ai personal trainer, ai workout plan, ai meal planner, ai calorie counter | madmuscles.com, betterme.world, zing.coach, fitbod.me, freeletics.com, caliberstrong.com, fitnessai.com, centr.com, gigabody.com, calai.app, macrofactor.com, joincarbon.com, rpstrength.com | none | Fable 5.1 / high |
| 7a | `custom \| apps \| AI coaching and workout` | ai fitness app, workout app | none | MadMuscles, Muscle Booster, BetterMe, Zing Coach, Fitbod, Freeletics, Caliber, FitnessAI, Centr, Fitify, Ladder, Juggernaut AI, Alpha Progression, Hevy, Strong, JEFIT, Nike Training Club | Fable 5.1 / **high** (picker ambiguity, see ids below) |
| 7b | `custom \| apps \| nutrition and calorie` | calorie counter, macro tracker | none | MyFitnessPal, Cal AI, Lose It!, MacroFactor, Carbon Diet Coach, RP Diet Coach, Cronometer, Noom, Yazio, Lifesum | Fable 5.1 / high |
| 7c | `custom \| apps \| body photo editing` | ai body editor, ai muscle editor | none | Gigabody, Manly, AI Muscle Generator, Facetune, RetouchMe, YouCam Perfect, BodyTune, Peachy, Body Editor, AirBrush, Remini, PicsArt, Fotor | Fable 5.1 / high |
| 8 | `custom \| interest \| AI body photo editing sites` | ai body editor, ai muscle editor, body photo editor, photo body reshaping | fotor.com, insmind.com, pixelbin.io, clipfly.ai, media.io, goenhance.ai, seaart.ai, perfectcorp.com, retouchme.com, picsart.com, facetune.com, remini.ai, gigabody.com | none | Fable 5.1 / high |
| 10 | `custom \| interest \| transformation content` | body transformation, 30 day transformation, before and after abs, dad bod, get shredded, body recomposition | athleanx.com, builtwithscience.com, jeffnippard.com, bodybuilding.com, menshealth.com, muscleandfitness.com, t-nation.com | none | Fable 5.1 / high |

Dan may say 7 is one segment instead of three; if so, name it `custom | apps | fitness and body editing` and put all
three app lists in it. Segment 8 is the search campaign's negative list (fotor, insmind, pixelbin…) turned into an
audience seed: those tools' users are the generator's exact buyer.

**Google Play package ids, read from Play search on 09-08** — use them to pick the right result when two apps share
a name (the picker searches by title; confirm the developer line matches):

| App | Package id |
|---|---|
| MadMuscles | `com.amomedia.madmuscles` |
| Muscle Booster | `musclebooster.workout.home.gym.abs.loseweight` |
| Zing Coach | `coach.zing.fitness` (NOT `com.zingwellbeing.app`) |
| FitnessAI | `com.fitnessai.android` |
| Caliber | `com.caliberfitness.app` |
| Juggernaut AI | `com.jtsstrength.juggernautai` |
| Alpha Progression | `com.alphaprogression.alphaprogression` |
| Nike Training Club | `com.nike.ntc` |
| Cal AI | `com.viraldevelopment.calai` |
| Carbon Diet Coach | `com.joincarbon.nutrition` |
| RP Diet Coach | `com.rp.rpdiet` |
| Cronometer | `com.cronometer.android.gold` |
| Gigabody | `com.howoo.jang.expofirebase` (first Play result for "Gigabody"; confirm the title in the picker) |
| Manly | `manmusclemaker.absbody.bicepenhancer` |
| AI Muscle Generator | `com.bodyphotoeditor.aimusclegenerator` |
| Peachy | `peachy.bodyeditor.faceapp` |
| BodyTune | `net.braincake.bodytune` (two other "BodyTune" apps exist; this is the body editor) |
| AirBrush | `com.magicv.airbrush` |
| PicsArt | `com.picsart.studio` |

An app the picker cannot find is skipped and listed in the results table — never substituted with a guess.

## THE MEMBERS EXCLUSION LIST ("Your data") — Fable 5.1 / medium

The campaign must not pay to show ads to people who already pay. The 15 remarketing lists built 08-17 are plain
page visits, so a members list does not exist yet.

- absbyai.com is a single-page app whose URL never changes; every screen reports a synthetic address to Google
  Ads through `fireAdVirtualPageview('/vp/' + name)` in `renderScreen()` (`public/index.html`, ~line 4198), so
  the member hub already fires `/vp/hub` every time it renders. **No code change is needed.** Verify once on
  production before building the list: sign in as a member, open the hub, and confirm a Google ad-network
  request carrying `/vp/hub` (the 08-17 check saw four `/vp/` hits after `showScreen('hub')`).
- **Step 1 (Audience manager → Your data):** rule-based website list `website | member hub | 540 day`, rule
  "URL contains `/vp/hub`", membership 540 days. It will read "Too small to serve" for weeks — expected. The
  08-17 session built 15 such lists programmatically; the routine is in the archive under that date.
- **Step 2:** in the campaign, exclude `website | member hub | 540 day` AND the built-in `All converters`.

## PHASE 2 — WIRE THE SEGMENTS INTO DAN'S NEW CAMPAIGN (Fable 5.1 / high)

Do this in the same session **only if** Dan's Demand Gen app campaign draft exists in the account (Campaigns →
filter to Draft/Paused). Do not create a campaign from scratch, and **never switch the campaign on — Dan presses
the switch** (the convention since the 08-17 search build). If the draft is not there, stop after the segments and
say so.

| Ad group | Segments | Creative the ad group should carry |
|---|---|---|
| A — intent | 1, 2, 4, 5 | the product demo (upload a photo, see the abs, then the plan) |
| B — problem-aware | 3, 9, 10 | Dan's transformation story and tips, then the app |
| C — tool and app users | 6, 7a, 7b, 7c, 8 | the upload-your-photo hook |

Per ad group: **Optimized targeting OFF** for the first two weeks (Google would otherwise expand using its only
conversion history, which is email captures — see the 8/31 audit); the exclusions above; Dan's own geo and
demographic settings from his draft (US, men 25–54) left as he set them. Note in the results what each ad group's
estimated weekly reach reads.

Optional control group Dan can add himself in the same dialog: Google's Health & Fitness affinity segment, the
Fitness in-market segment, and the "getting married soon" life event. Lookalikes are on hold — the only seed list
near 1,000 people is the YouTube-viewer list, which is full of tier-2 subscribers and would model the wrong person.

## DRIVING GOOGLE ADS FROM CLAUDE — READ BEFORE THE FIRST CLICK

Memory `google-ads-ui-automation` and the 08-17 audience build (archive) hold the traps; the short version:

- Use the Chrome extension (`mcp__claude-in-chrome__*`), not the Browser pane. Check `list_connected_browsers`
  first: **two connected extension instances made Google Ads stop rendering on 08-17.** Warn Dan before taking
  the browser; he cannot use Chrome while it runs.
- **No coordinate clicks in the main Ads app** — the viewport is ~2111 px against a ~1558 px screenshot and clicks
  land on "Ask Advisor". Use `find` → `ref` clicks and `javascript_tool`.
- Text fields accept the native value setter + `input`/`change` events. AngularDart `material-select-item` and
  `material-dropdown-select` ignore `.click()`; dispatch `pointerdown → mousedown → pointerup → mouseup → click`
  on the inner `[buttondecorator]`. Menus close between tool calls, so open-and-select must happen in one call.
  Long JS times out at ~45 s over CDP; split into fill and submit.
- The term box takes a comma-separated paste followed by Enter. **After every save, reopen the segment and count
  the chips** against the table; Google silently drops a term it dislikes.
- Google Ads sometimes refuses to render in an extension-driven tab (08-17). If the page is all spinners after a
  hard reload and a fresh tab, stop and report; do not burn the session clicking.

## DONE MEANS

1. Audience manager → Custom segments shows every built segment under the exact names above; each was reopened
   and its chip count matches the table (or the drop is recorded).
2. A results table in the coordination entry: segment, chips entered / kept, estimated size from the insights
   panel, anything Google flagged, any app the picker could not find.
3. Members list built after the `/vp/hub` beacon was seen live (or the reason it was skipped).
4. Phase 2 done or explicitly reported as not done and why. **Campaign left OFF.**
5. This doc's Status line updated to EXECUTED; the entry removed from `AI_COORDINATION.md` HANDOFFS and from
   `Handoffs/README.md`'s Open table. No dashboard row exists for this handoff unless Dan added one.
6. Screenshot of the Custom segments list sent to Dan.

---

## STARTER PROMPT (paste into a fresh session — Fable 5.1, effort HIGH)

> Execute `Handoffs/handoff-20260908-google-ads-custom-segments.md` in the Abs By AI project root. Build the
> Google Ads custom segments exactly as specified there, in this order: 2, 5, 9, then 1, 3, 4, then 6, 8, 10,
> then 7a/7b/7c, using Dan's Chrome via the extension (warn him first, check for a second connected instance,
> find→ref clicks only, never coordinate clicks). Paste each term list comma-separated, save, reopen and count the
> chips. Then confirm `/vp/hub` fires live and build the `website | member hub | 540 day` exclusion list. Then, only if my
> Demand Gen app campaign draft already exists, wire ad groups A/B/C per Phase 2 with optimized targeting OFF and
> leave the campaign switched off. Report a results table with chip counts and estimated sizes, and update the
> coordination file and Handoffs/README.md when done.

**Model / effort recommendation:** Fable 5.1 at **high** for the whole session. Medium would do for segments 1–5
alone, but 9, the app pickers and Phase 2 all need judgment, and one session is cheaper than a
split. If the Fable allowance is short, Sonnet 5 at high can build the six search-term segments first and hand
the rest to Fable.


---

## EXECUTION NOTES (2026-09-08, Fable 5.1)

**Built and reopen-verified:** 2 (16/16), 5 (21/21), 9 (19/19, nothing flagged), 1 (10/10), 3 (12/12), 4 (15/15),
6 (5 + 13), 8 (4 + 13), 10 (6 + 7). All "Under review". `/vp/hub` verified live (1p-user-list 200).
**Remaining:** 7a, 7b, 7c, `website | member hub | 540 day`, Phase 2 (draft existence not yet checked).

**Recipe that worked (Chrome extension, tab on `/aw/audiences/management/customaudience?ocid=8444849202`):**
- The plus button is `find` → "Create custom audience". The dialog's fields: `input[aria-label="Segment name"]`
  (native setter + input/change + blur works), the two `material-radio`s (`.click()` does nothing — dispatch
  pointerdown→mousedown→pointerup→mouseup→click on the element whose text contains "searched for"; the chips already
  entered survive the switch), the term box `input[aria-label="Add interests or purchase intentions"]` /
  `"Add Google search terms"` (focus it with JS, then `computer type` the comma-separated list + Return — every chip
  lands at once, no per-term Enter needed).
- Websites: the link is `span.add-url` (not a button); clicking it adds `input[aria-label="Add URLs"]`, which takes
  the same comma-separated paste. Apps: `span.add-app` → `input[aria-label="Add apps"]`; typing a title shows a row
  "Title / package.id - Developer" — match the id against the table above.
- Chips are `material-chip`; count them per section by which `input[aria-label^="Add "]` follows each chip in DOM order.
- Save/Cancel are `material-button`s with text "Save"/"Cancel" — the pointer-event sequence works on them. The saved
  row's name cell is not a native button; reopen with `find` → "custom | … segment name link".
- **Do not** dispatch pointer events on a `material-list-item` in the app picker, and do not `await` inside a
  `javascript_tool` call while the insights panel is refreshing — both hung the renderer for good (needed a new tab).
  Use `find` → ref click on the picker row, or keyboard Down + Return, and verify the chip afterwards.
- Google Ads will not finish loading in an extension-driven tab while the Mac's load average is above ~40.
