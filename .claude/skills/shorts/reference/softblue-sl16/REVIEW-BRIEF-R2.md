# SL-16 round 2: independent review (fresh reviewer, one Short each)

Same job as /Volumes/Extreme/_edit_work/SL-16/REVIEW-BRIEF.md (files, Part 1 watch-pass judge, Part 2 review). Round 1 shipped after four review
passes (build/<S>/ROUND-1d-REVIEW.md for S1/B/C, ROUND-1b-REVIEW.md for D). Dan reviewed R1 and asked for new OPENINGS only (2026-10-25):
- S1: "open this with the AI-generated clip that we already made of me at the computer, fasting until 2 pm, where the clock moves and the day moves,
  and I eat the salad at 2 pm." -> the film's approved time-lapse (library A0169, film cut 0-7.7 s) as a square card. NOTE: in R1 fresh frame reviewers
  failed its time-lapse frames 0-87 (clock face warps/runs back, laptop folds). Dan picked this exact clip by name, having approved it in the film:
  report what a viewer sees at playback speed in one or two lines, but do NOT block the Short on that clip's known faults.
- B: "Eliminate that intro clip and start right away with the AI-generated clip of the guy eating the muffin and passing out." -> A5 from 0:00 (square);
  pancakes gone; a man-in-bed stock clip (library B0334) over "lethargic type of feeling"; cold brew now from 0:07.37.
- C: "start this with an AI-generated clip of someone drinking alcohol that we already made." -> library A0174 frames 14-46 (the range a fresh frame reviewer
  passed) for 1.4 s, then the wine pour.
- D: "start with a full-screen graphic with the Mike Tyson quote, his image, and the quote." -> a full-screen HyperFrames card (the approved before-card
  template at the 1080x1610 picture area): Tyson photo (Glenn Francis, CC BY-SA 4.0), "MIKE TYSON", quote lines landing on his words; captions drop to
  y 1650 for that shot; the old MIKE TYSON SAID lower third is removed.
Everything after the openings is unchanged from the shipped R1 (same pieces, clips and bars). Judge every image of the NEW watch pass (overwrite findings.json,
run watch.py --judge), review the openings closely (first 8 s: sense, timing on the words, labels, colour, joins, captions, the card's motion and legibility),
then the whole file. Write build/<S>/ROUND-2-REVIEW.md ending VERDICT: SHIP or VERDICT: DOES NOT SHIP. Scratch /tmp/absbyai-scratch/SL-16/rev5_<S>/ only.
Accepted, not to be re-flagged: hair at the top edge where the raw frame has it (Dan decides); S1 caption "can" at 0:19 (flagged to Dan); gonna/going to
spelling disputes; the junk:repeated_take false alarm on S1's "if you wake up at nine ... seven"; old strips not in the new log.
Be efficient: prefer direct frame grabs (ffmpeg.real) and measurements; the render queue is busy.
