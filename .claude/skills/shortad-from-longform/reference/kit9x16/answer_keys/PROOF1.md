# Proof 1: the automatic content sheet against the two answer keys (2026-09-28)

`auto_content.py` with Gemini leftover calls; tolerance 0.2 s. Ad 10 ran from `kit_recover.py`'s own recovery (no
hand-recovered input anywhere); Ad 1 from the approved build's recovered EDL and grade (its key is a revised,
approved vertical, so its sheet was never going to be reproducible from the master alone).

| | Ad 10 (AV-07 key) | Ad 1 (approved-vertical key) |
|---|---|---|
| beats found / expected (paired) | 31 / 31 (31), 0 extra | 34 / 35 (30) |
| lower thirds | 6 / 6 | 7 / 7 |
| CTA pills | 3 / 3 (2 his, 1 by the kit's grammar) | 3 / 3 |
| kinds correct | 39 / 39 | 26 / 40 |
| t0 and t1 within 0.2 s | 30 / 39 | 24 / 40 |
| text, exact / ignoring case and punctuation | 10 / 12, 12 / 12 | 7 / 13, 12 / 13 |
| media: same file, or the same picture in another file | 20 / 25 | 2 / 24 |
| label_kind equal | 21 / 25 | 20 / 24 |
| **real vs AI swapped on the same picture** | **0** | **0** |
| escalations | 0 | 2, both correct (the email-capture screen at 74.9 s and "Meet the new you" at 197.9 s in his master) |
| AI calls / cost (one clean run) | 11 / $0.005 | 8 / $0.004 |

## Every Ad 10 difference, explained

* **Timing (9 rows)**: all lower-third and CTA rows are the key's hand-rounded times; the master's frames were
  read for 68.8 (on screen 68.9-74.3 s: auto 69.0-74.3, key 68.8-73.1), 141.3 (typing at 142.4, gone by 144.0: auto
  142.3-143.7, key 141.3-144.6), 108.6 (pill sliding in at 108.6: auto 108.58, key 109.0), 178.3 (no pill at 178.3,
  in at 178.45: auto 178.61, key 178.28). 151.6 / 156.6: his food shot ends at 155.72 and the bullet panel is
  already sliding in at 155.8; the key held the food card to 156.6 on purpose (a stretched hold asset).
* **Media (5)**: 106.2 s the key uses photo-10, but his master shows **photo-74** (jump rope), which the auto sheet
  found: a key error. 63.1 / 65.1 the auto sheet found the clean originals (`fatdad_ride.jpg`,
  `fatdad_standing.jpg`) where the key lifted his frame. 93.2 the key used one still frame of his phone clip, the
  auto sheet the moving clip. 151.6 the key built a stretched hold, the auto sheet lifts his clip.
* **Labels (4)**: the two family snapshots (clothed) and the two app form screens: key `real`, auto no chip.
  Neither is a physique picture; no label is swapped.
* **CTA**: his master has two pills; the kit's measured range wants three. The key added one at 74.1 s, the auto
  sheet at 80.4 s (his Ad 1 position, 0.43 of the runtime, on a sentence start in plain talk).

## Ad 1: what the key carries that his master does not

Dan's own revisions of the approved vertical (all in the key's `deviations`): the hook as an inset graphic (0-2.95),
the three "today" photos held 1.55 s longer (11.45-14.3), a different model photo (47.95), the after-reveal cards
he asked for (73.6, 197.3), ten stock clips swapped in for Muhammad's b-roll (81.2, 113.95, 116.3, 136.3, 152.45,
153.75, 155.1, 208.1, 216.3; natively vertical, so `bleed` where the auto sheet lifts his 16:9 into a card), stills
of the AI clips whose hands melt (101.5, 106.25), and his cropped dad photos in place of the busy-dad AI clip
(132.4-136.3). The auto sheet reproduces what his master shows there (it labels the busy-dad clip AI, correctly for
that picture). Its own limits on Ad 1: a dissolve inside one card (the 200 lb photo into the AI "heavier Dan with
the phone" clip, 2.8-6.9 s) is not split, so the lifted card keeps his labelling; the key's lower-third and CTA
times are hand-set (the 118.6 lower third is gone by 123.0 in his master: auto ends at 123.7, key 126.4).
