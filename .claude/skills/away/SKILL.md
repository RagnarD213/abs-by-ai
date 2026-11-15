---
name: away
description: Dan is leaving his Mac now. Give video edits the full away core budget at once (M6: 10 cores instead of 6) instead of waiting 30 idle minutes. Use when Dan types /away, says he is stepping away, going out, going to bed, or asks edits to use all the cores; "/away off" or "I'm back" turns it off.
---

# /away: use all the cores while Dan is gone

Run on the Mac Dan is sitting at (the M6):

```bash
python3 .claude/skills/_shared/editroute/away.py on        # optional: --hours 3 (default 8)
```

Then tell him, in one or two plain sentences, what the command printed (cores for edits now) and that it switches
itself off the moment he touches the keyboard or mouse again, after a 2 minute grace to walk away. Nothing else to do:
the render queue reads the new budget on its next admission, so waiting steps start by themselves. Do not restart,
reorder or cancel any job.

- `away.py off`: Dan is back and wants the Mac responsive now (touching the Mac does the same thing).
- `away.py status`: is it on, and how many cores edits have.
- It only changes how many cores the render queue hands out on this Mac (`hostcfg.presence`). Edit slots, the M2,
  spending and approvals are untouched. Numbers live in `editroute/hosts.json` (`cores_present`, `cores_away`).
- If Dan asks from a chat running on the M2, run it on the M6: `ssh m6 'cd "<M6 repo>" && python3 .claude/skills/_shared/editroute/away.py on'`.
