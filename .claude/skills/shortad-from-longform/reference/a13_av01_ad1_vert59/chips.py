#!/usr/bin/env python3
"""The two label chips at 9:16, drawn exactly as the build draws them.

Ported verbatim from the square's `sqlib.chip_at/chip_dims` (the placement Dan reviewed on
2026-09-13) with VW/VH at the vertical's 1080x1920 and the vertical's own INK. Same padding
(17 px sides, 11 px top/bottom), same radius 9, same 215/255 black -- so a chip added by this
cutdown is indistinguishable from the chips the approved vertical already burns on its AI cards.

AGENTS.md, Dan 2026-09-11 / 2026-09-12:
  'AI-GENERATED'                            on every AI image or clip
  'Real picture of me - not AI-generated'   on every real after picture of Dan
  never over his face and never over his abs -- measured on the rendered frame, never a fixed y.
"""
import sys
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
from PIL import Image, ImageDraw
from motionlib import font, text_size

VW, VH = 1080, 1920
INK = (255, 255, 255)
REAL_LABEL = "Real picture of me — not AI-generated"
AI_LABEL   = "AI-GENERATED"
REAL_LINES  = ("Real picture of me —", "not AI-generated")
REAL_LINES3 = ("Real picture", "of me — not", "AI-generated")


def _parts(label, lines):
    if lines == 1 or label != REAL_LABEL: return [label]
    return list(REAL_LINES if lines == 2 else REAL_LINES3)


def chip_dims(label, lines=1, size=34):
    f = font(size, "SemiBold")
    parts = _parts(label, lines)
    lh = int(size*1.18)
    tw = max(text_size(p, f)[0] for p in parts)
    th = text_size(parts[0], f)[1] if len(parts) == 1 else lh*len(parts) - (lh - size)
    return tw + 34, th + 22


def chip_at(label, x, y, lines=1, size=34):
    f = font(size, "SemiBold")
    parts = _parts(label, lines)
    w, h = chip_dims(label, lines, size)
    lay = Image.new("RGBA", (VW, VH), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x, y, x+w, y+h], radius=9, fill=(0, 0, 0, 215))
    if len(parts) == 1:
        d.text((x+17, y+11), parts[0], font=f, fill=INK, anchor="lt")
    else:
        lh = int(size*1.18); asc = f.getmetrics()[0]
        for i, p in enumerate(parts):
            d.text((x + (w - text_size(p, f)[0])//2, y + 11 + i*lh + asc), p, font=f,
                   fill=INK, anchor="ls")
    return lay
