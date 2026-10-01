# Follow-up: graphics inventory for a replacement kit

Dan does not like Muhammad's graphic style (blue glass title bar, black chips with olive tab). We are going to BUILD
every graphic for him ourselves in our Soft Blue Light style, as transparent 1080x1920 overlays he drops on top of his
cut, and link them in the doc. I need from you, for YOUR video only, the complete list of graphics the FINISHED video
should carry AFTER the revisions in your section are applied (so: his existing titles / numbered chips / info chips
that stay, with corrected wording; the key points your section adds or rewrites; labels; the AbsByAI.com mark).
Do not include captions.

Write `/Volumes/Extreme/_edit_work/revisions-20261001/muhammad/out/<NAME>.graphics.json`: a JSON list, play order, of

  {"id": "g01",                       # g01, g02 ...
   "kind": "title" | "section" | "keypoint" | "chip" | "label_ai" | "label_real" | "mark",
   "t0": 0.0, "t1": 3.2,              # seconds in the CURRENT cut where it should be on screen (full precision you have)
   "eyebrow": "REASON 1 OF 3",        # small caps line. title: a 1-3 word category; section: e.g. "REASON 1 OF 3", "WAY 2 OF 3",
                                      # "NUMBER 3"; keypoint: always "KEY POINT"; chip: a short category or ""
   "text": "It's RARER",              # main line, Title Capitalization, the 1-2 punch words in FULL CAPS. For a title, the
                                      # video's real title. Keep under about 45 characters where possible (2 lines max at
                                      # roughly 24 characters per line). Fix his typos / wrong words here.
   "his_text": "IT IS RARER",         # what his graphic says now, verbatim ("" if this graphic is new)
   "under": "camera" | "picture" | "clip" | "app",   # what is on screen under it
   "hair_top_px": 340,                # camera scenes only: lowest-numbered y (px from the top, 1080x1920) of Dan's hair
                                      # top during t0..t1, so a top graphic can be placed above his head; null otherwise
   "note": ""}                        # anything the builder must know (e.g. "AI clip: label for the whole clip, clear of face")

Rules: one entry per on-screen graphic span. A numbered section title that just echoes the spoken sentence becomes a
short signpost (eyebrow "REASON 2 OF 3", text the 2-4 word name of the point). Every AI picture or AI clip gets a
"label_ai" entry for its full span (text "AI-GENERATED"); every real physique photo of Dan gets a "label_real" entry
(text "Real Picture Of Me, Not AI-Generated"); say in "note" where on the frame the label is clear of faces and abs
(e.g. "top left", "top center"). Percentages, food names and number chips are kind "chip". The AbsByAI.com mark is
kind "mark" with text "AbsByAI.com", from the script's cue to the end. Follow your own section's decisions (items you
told him to remove are NOT in the list). Measure hair_top_px on full-resolution frames (2-3 samples per span, take the
smallest y). No em dashes. Reply with the path and the count only.
