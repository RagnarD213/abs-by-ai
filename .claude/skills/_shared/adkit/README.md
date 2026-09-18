# `_shared/adkit` — the card kit Dan approved on RA-01 (2026-09-18)

Dan, approving "The AI Trick That Got Me Abs": *"I think this was a template for future videos… I especially like this
graphic that you made with the things to lose body fat and gain muscle. Let's make this something that we reuse in
future videos… I think that illustrated it better than we did in past videos."*

| file | what |
|---|---|
| `analysis_card.py` | **the analysis card**: subject picture + scan line + BODY FAT / FAT TO LOSE / MUSCLE TO GAIN bars + YOUR WORKOUT PLAN band. 9:16 and 16:9. CLI and `build()`. Refuses printed numbers; places its label chip by person mask. |
| `cardlib.py` | geometry per aspect (caption line, chip safe band, card rectangle), the one chip style, measured chip placement, the J2AD field, fitted photo layers, Ken Burns drift, hard-cut entries, the h264 card encoder. |

```bash
python3 .claude/skills/_shared/adkit/analysis_card.py --image "Media/example pictures/dan by pool.png" \
    --aspect 9x16 --dur 5.2 --label ai --out /Volumes/Extreme/_edit_work/<job>/cards/analysis_9x16
```

**When to use it:** any line that says the app analyses the picture and turns it into a plan ("AI analyzed it and
figured out how much fat I had to lose and where I had to gain muscle"). 4–6 s. Cut it in and out on hard cuts; keep
captions running under it; put the emitted `chip_png` / `chip_pos` / `card_rect` into the delivery-gate plan.

**Do not** add numbers to the rows, show it for a different person than the video's before/after, or fade it in.
Extend the kit here (a 1:1 `Aspect`, more cards) rather than forking it into a per-video recipe; measure any new
geometry on a gated render first. Worked example with every other card (photo cards, end card, CTA pill, phone
clip): `Claude Ad Videos/the ai trick that got me abs - RA-01/recipe-RA-01/`.
