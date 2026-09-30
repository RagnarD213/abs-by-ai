# Handoff: move the morning brief to the OpenAI dot (Codex sets it up)

Written 2026-09-30 by Claude (Fable 5.1). **Executor: a Codex session (GPT-6 Sol, high), then the dot runs
it daily.** Read `handoff-20260930-codex-dot-00-shared-setup.md` first.

## Goal

Dan gets a morning brief at 6:30 AM Central every day that changes what he does that morning, produced and
delivered by his dot at zero allowance cost during the launch month, and cheaply after. The Claude routine
`abs-by-ai-morning-brief` (disabled since mid-September) is not revived.

## What the brief IS (the part that must survive the move)

The Claude prompt lives at `~/.claude/scheduled-tasks/abs-by-ai-morning-brief/SKILL.md` (about 7,500
words). Read it once for the reasoning, then carry over only these rules:

1. **The one test.** Every sentence must answer "what would make Dan act differently this morning?" A short
   brief is a correct brief. It is not a status report.
2. **Rank by who is blocking, not by importance.** Bucket A = blocked on Dan (a decision, a verdict on finished
   work, a real-world act). Bucket B = something an agent could run (at most one line). Bucket C = everything
   else, which does not appear.
3. **Exactly one thing at the top**, with its consequence or deadline in the headline. Never a numbered plan
   of three.
4. **Memory and escalation.** Yesterday's ask is stored; this morning opens with "You said you'd <ask>. Did it
   go?" If the same item was the ask before, say which morning it is and raise the stakes. Every "Still on
   you" row carries a day count; anything past 14 days becomes "decide or drop" with the two real answers
   named.
5. **Standing sections that print every morning:** calendar (today plus what is imminent in the next 10 days),
   editor deliveries waiting on a verdict, "From your saves" (2 videos to watch, 2 actions, from the watch
   history review, phrased as recommendations, never "you liked this").
6. **Deleted on purpose, do not restore:** markets, AI news as a section, the fuel quote. AI news appears
   only as an interrupt that changes a tool or cost decision.
7. **The two packaged long-forms reminder** (Zepbound + Supplements, on hold by Dan's call since 09-08): the
   rule in the Claude prompt says whoever closes that decision deletes the block. It is still open, so the
   dot carries one pinned row, "Upload ours today" or "Wait for Muhammad", counting days since 2026-09-02.

## Inputs and where the dot gets them

| input | source for the dot | notes |
|---|---|---|
| Today's calendar, next 10 days | Google Calendar connector, all calendars | an error is "calendar could not be read", never an empty day |
| Board: what is blocked on Dan | `AI_COORDINATION.md` via the GitHub connector (public repo) | read for facts, throw the prose away |
| Handoffs to fire, assistant queue, task checks | `absbyai.com/api/todos` and `/api/task-checks` with `X-Dash-Key` | key comes from the Mac's secrets file; see "the local helper" below |
| Editor deliveries pending | `.claude/skills/editor-deliveries/state.json` (GitHub connector) | written by handoff 02's routine before 6:30 |
| Ads digest | `brief-ads.json` at the repo root | written by the local helper, below |
| Ad-in-organic-queue guard | `ad_guard` result inside the same helper output | any hit is bucket A: "delete schedule <id>" |
| Watch picks | the dot's own Sunday watch review (handoff 03) | 2 watch, 2 actions, carried forward until watched |
| Business pulse | PostHog project 458833, yesterday vs same window 7 days ago | via the local helper (API key on the Mac) or the dot's browser |
| Gmail digest | Gmail connector, business labels only (contact form, Stripe) | never the general inbox |
| Last night's plan | `next-day-plan.json` in the Claude routine folder, only if `forDate` is today | the local helper copies it into the inputs file |

### The local helper (the only Mac-side piece)

The measured, $0 inputs already exist as scripts in the repo. The Codex session writes one wrapper,
`scripts/brief/collect_inputs.py`, that runs at 6:05 AM as a **Codex automation** (lowest model that works) or
directly on the dot's linked Mac, and produces one file the dot can read from GitHub:

- runs `node scripts/ads/ads-digest.js` (writes `brief-ads.json`; always exits 0),
- runs `python3 scripts/blotato/ad_guard.py --scan` and records CLEAN or the hits,
- curls `/api/todos` and `/api/task-checks` with the key and stores the JSON,
- copies `next-day-plan.json` if `forDate` is today,
- queries PostHog for the two windows (event counts grouped by event, uniques, signups, memberships),
- writes `brief-inputs.json` at the repo root and commits + pushes it (pull --rebase first).

No secret ever lands in the file. The file holds numbers and ids only. If a step fails, the file says which
step failed; the dot then reports "could not read X", never a clean result.

## Output and delivery

Phase 1 (do this first): the dot delivers the brief as a message in the dot chat at 6:30 AM CT, and by text if
Dan turns on the texting beta. Same eight elements, same order, plain text with light bold.

Phase 2 (only after a week of good briefs): publish the HTML page to `absbyai.com/morningbrief` as the Claude
routine did. That means writing `morningbrief.html` to the **repo root** (never `public/`, the page is gated),
plus `brief-ask.json` and `gmail-digest.json`, and pushing to main through the GitHub connector with approval.
The locked visual format is in the Claude prompt, Step 3. Do not start Phase 2 until Dan asks.

## The dot assignment (paste-ready, the Codex session finalizes it)

> Every weekday and weekend at 6:30 AM Central, build my Abs By AI morning brief. Read `brief-inputs.json`,
> `AI_COORDINATION.md` and `.claude/skills/editor-deliveries/state.json` from GitHub `RagnarD213/abs-by-ai`,
> my Google Calendar for today and the next 10 days, and Gmail only under the contact-form and Stripe labels.
> Sort everything into: blocked on me, agent-executable, everything else. Show me ONE thing at the top with
> its consequence or deadline. Open with yesterday's ask and ask whether it happened. List what is still on
> me with a day count; anything over 14 days becomes "decide or drop" with the two real answers. Include the
> calendar, editor files waiting on my verdict, and this week's 2 videos and 2 actions from your Sunday watch
> review. No markets, no news section, no quotes. If an input could not be read, say so; never show a failed
> check as clean. Keep it short. Never use an em dash.

## Steps for the Codex session

1. Read the Claude prompt in full once. Read `Docs/BOARD_MORNING_MAINTENANCE.md`.
2. Write `scripts/brief/collect_inputs.py` as described; run it by hand; check `brief-inputs.json` has no
   secrets; commit and push.
3. Create the 6:05 AM Codex automation that runs it (or a launchd job if Dan prefers no automation cost; note
   the choice).
4. Finalize the dot assignment text above with the exact file paths and hand it to Dan to paste into the dot,
   with the connector list (Calendar, Gmail, GitHub) and the schedule.
5. Prove one run by hand: ask the dot to build today's brief now; compare it against the one test. Fix the
   assignment wording, not the dot's output.
6. Record in `Docs/ROUTINES.md`. Tell Dan the Claude routine stays disabled (it already is).

## Traps

- The board maintenance step (aging, weekly archive) that the Claude routine performed edits the repo. Leave
  it out of the dot version for now; it needs a session with the board rules loaded. Note it as open.
- `absbyai.com/api/*` without the key returns 401 or the marketing page. Both look like "nothing there".
- A stale `next-day-plan.json` must never print. Check `forDate` equals today in America/Chicago.
- The brief goes to a public repo only in Phase 2. Personal calendar names never go in the headline.

## Done means

`brief-inputs.json` is produced every morning at 6:05, the dot delivers a brief at 6:30 that passes the one
test for three consecutive mornings, `Docs/ROUTINES.md` lists it, and Dan has read one brief and said it is
useful.

## Starter prompt

```
Read Handoffs/handoff-20260930-codex-dot-00-shared-setup.md, then execute Handoffs/handoff-20260930-codex-dot-01-morning-brief.md in full. Build the local inputs helper, prove one dot run, record the routine, commit and push. Report in plain language.
```

Model: GPT-6 Sol, high effort.
