# ManyChat comment-to-DM: per-topic keywords

Built 2026-09-08. Replaces the single `ABS` keyword that every one of the ~60 queued CTA
posts shared, which made per-post attribution impossible and sent every commenter the same
generic DM.

ManyChat account `fb5531746`, Instagram @danrosefit only. Every automation uses the same
shape as the original: trigger = comment on **any post or reel** containing the keyword →
rotating public reply → opening DM with a `[Send me the link]` button → link DM with a
`[Get my free preview]` button. The two-beat DM is mandatory (Instagram blocks a bare link
in the first automated message).

| Keyword | Topic | Queued posts | utm_campaign | Automation |
|---|---|---|---|---|
| `ABS`   | ab training & anatomy               | 13 | `comment-abs`   | `content20250805163853_256330` (the original) |
| `FOOD`  | nutrition, eating windows, alcohol  | 13 | `comment-food`  | `content20260908153327_557281` |
| `TRAIN` | non-ab workouts, mobility, back     |  8 | `comment-train` | `content20260908153321_400271` |
| `TRACK` | scale, mirror, progress photos      |  5 | `comment-track` | `content20260908153309_310866` |
| `SLEEP` | sleep & recovery                    |  4 | `comment-sleep` | `content20260908153303_162369` |
| `COACH` | AI plan / macros / preview tips     |  4 | `comment-coach` | `content20260908153247_216144` |

Link is always `https://absbyai.com/?utm_source=instagram&utm_medium=dm&utm_campaign=<campaign>`.

## Why these six words and not the obvious ones

ManyChat matches **contains**, not equals, so a keyword that is a substring of a common
comment cross-wires the DMs. Rejected for that reason:

- **`EAT`** — fires on "great", the single most common comment on the account. Use `FOOD`.
- **`AI`** — fires inside "train", "again", "wait", "said", "fail". Use `COACH`.

None of the six chosen words is a substring of another, and the only English words that
contain them ("training", "tracking", "asleep", "planks") stay on their own topic.

## Editing these in the browser

The easy builder's fields are React-controlled: synthetic typing **drops characters**
(measured: "uncovers" → "ncovers", "seconds" → "sconds"). Set them with the native value
setter plus an `input` event instead. The link URL lives behind the 🔗 icon next to the
button label and has its own Save, separate from the automation's Update.

ManyChat's SPA also wedges the Claude-in-Chrome extension's script injection after a
handful of page loads — every tool call then times out, including on unrelated sites.
Recovery is to close the ManyChat tabs and bring Chrome to the front.

## Post captions

`scripts/manychat/keyword_split.py` rewrites the CTA line in the queued Blotato captions
(`Comment ABS …` → `Comment <KEYWORD> …`). Dry run by default; the topic of every post is
pinned by schedule id so nothing is guessed at run time.
