"""RO-18: the picture for 'AI editing videos for this channel, including probably this one' (P02): nine of THIS video's own
graphics and clips, 3 x 3, from review/stills. Re-run after the stills whenever one of the nine changes, then re-run stills.py P02."""
from PIL import Image
W = "/Volumes/Extreme/_edit_work/RO-18/round1"
IDS = ["T1", "C01", "G08", "G04", "G01", "G16", "T5", "G19", "G27"]
TW, TH, GAP = 600, 338, 18
im = Image.new("RGB", (GAP + 3 * (TW + GAP), GAP + 3 * (TH + GAP)), (8, 18, 33))
for k, i in enumerate(IDS):
    t = Image.open(f"{W}/review/stills/{i}.jpg").convert("RGB").resize((TW, TH), Image.Resampling.LANCZOS)
    im.paste(t, (GAP + (k % 3) * (TW + GAP), GAP + (k // 3) * (TH + GAP)))
im.save(f"{W}/assets/screens/ro18_graphics_grid.png"); print("grid", im.size)
