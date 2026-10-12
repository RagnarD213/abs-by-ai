# The data file `page.py` reads

One JSON file per shoot or batch. A full, real example: `Docs/shoot-1017-shorts-ideas/ideas.json`.

```json
{
  "title": "10/17 Shoot: Reaction Clips, Round 3",
  "sub": "One line under the title: what this page is and the date.",
  "port": 8881,
  "decisions": ["<b>Bold lead.</b> One decision per line. Simple HTML is allowed here only."],
  "sections": [
    {
      "id": "new",
      "heading": "New reaction clips",
      "sub": "Press play and the clip starts on the line you react to.",
      "label": "New reaction",
      "pick": true,
      "reply_label": "NEW REACTIONS",
      "items": [
        {
          "t": "Bill Maher Says Fat Shaming Should Come Back. He's Right.",
          "v": "right",
          "id": "Dm4TAdiEFn0",
          "segs": [[353, 370]],
          "src": "Real Time with Bill Maher, \"New Rule: The Fudge Report\"",
          "views": "2.1M views",
          "words": "Starts on \"fat shaming doesn't need to end\". Ends on \"shame is the first step in reform\".",
          "what": "One or two sentences: who is speaking, where, and what they claim.",
          "pts": ["Hook: ...", "My take: ...", "Lesson: ...", "Bottom line: ..."],
          "note": "Optional. Anything Dan must check by eye, or anything that is your guess."
        }
      ]
    },
    {
      "id": "locked", "heading": "Locked reactions", "label": "Reaction", "locked": true,
      "items": []
    },
    {
      "id": "outdoor", "heading": "Locked outdoor shorts", "label": "Outdoor", "locked": true,
      "items": [{"t": "How To Do Towel Rows", "pts": ["..."], "br": "Pool shot 3.", "note": "Optional."}]
    }
  ],
  "reply_title": "10/17 REACTION CLIPS, ROUND 3",
  "reply_help": "Tap Kill on any clip you don't want. Everything else counts as a keep.",
  "reply_lines": ["Optional extra question lines for the reply box, one per line"]
}
```

Rules:

- `v` is `right`, `wrong`, or `plain` (shown as MY SPIN, for a clip Dan builds on without a verdict).
- `segs` is a list of `[start, end]` pairs in seconds, played in order. One pair for a normal clip. The total
  must be 25 seconds or less; aim for 15.
- An item with no `id` is an idea card (title, bullets, `br` for B-roll): no player.
- A section with `"pick": true` gets Kill buttons and a line in the reply box, and needs `reply_label`.
  A section with `"locked": true` shows a LOCKED tag and no buttons.
- One bullet in `pts` must start with `Lesson:` or `Do this`. `page.py` refuses a clip card without one.
- `noembed` is set by `page.py` when the owner has turned off embedding. Do not write it by hand.
- Use straight quotes escaped as `\"` inside strings. No em dash and no en dash: `page.py` refuses them.
