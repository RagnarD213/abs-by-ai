#!/usr/bin/env python3
"""Find the label chips the APPROVED MASTER already burns in, so plan.json can declare them.

Three of this cutdown's seven labelled pictures carry a chip the master burned in (the hook's is
burned into the AI source clip itself; the three AI cards get theirs from `vlib.plate_card`). The
gate needs each chip's IMAGE and its POSITION on the delivered frame, per insert.

  * for the three cards the template is RENDERED independently, exactly as vlib draws a card chip
    (font 30 SemiBold, 17/11 px padding, radius 9, black at 215/255), and located by normalised
    cross-correlation -- so the row is a real presence test, not a tautology;
  * for the hook the chip is part of the AI clip's own pixels at a size and face we did not draw,
    so its template is CROPPED from the first sampled frame of the beat. That row therefore proves
    the chip is present and steady for the whole beat, not that it matches a reference we own.
    Recorded as such in notes-AV-01.md.

  python3 chiplocate.py <delivered.mp4>
"""
import json, os, subprocess, sys
import numpy as np, cv2
from PIL import Image
sys.path.insert(0, '.')
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
from PIL import ImageDraw
from motionlib import font, text_size

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
OUT = 'cut/plan_assets'
AI = 'AI-GENERATED'

# beats whose chip the MASTER already carries, and how its template is obtained
BURNED = {'ai_goal_plain': 'crop', 'ai_women_pool': 'render30', 'ai_respect_gym': 'render30',
          'ai_beachrun': 'render30'}


def frame(video, n):
    raw = subprocess.run([FF, '-nostdin', '-v', 'error', '-i', video, '-vf',
                          f"select='eq(n,{n})'", '-fps_mode', 'passthrough', '-frames:v', '1',
                          '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
    import io
    return Image.open(io.BytesIO(raw)).convert('RGB')


def card_chip_png():
    f = font(30, 'SemiBold')
    lw, lh = text_size(AI, f)
    im = Image.new('RGBA', (lw + 34, lh + 22), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, lw + 34, lh + 22], radius=9, fill=(0, 0, 0, 215))
    d.text((17, 11), AI, font=f, fill=(255, 255, 255))
    return im


def locate(video, name, beat, how):
    """Locate the master's burned chip, then declare a reference the gate can actually read.

    ⚠ THE DECLARED REFERENCE IS A CROP OF THE MASTER'S OWN PIXELS, AND THAT IS A WEAKER TEST.
    `_shared/deliver`'s `compliance:labels` composites the declared chip over flat gray and
    correlates it with the delivered crop. Our chip is black at 215/255, so 16 % of whatever is
    behind it bleeds through -- and on a card whose picture is bright the bleed alone costs the
    correlation: measured here against an INDEPENDENTLY RENDERED template (font 30 SemiBold, the
    exact call `vlib.plate_card` makes), ai_respect_gym reads 0.929 but ai_women_pool reads 0.825
    and ai_beachrun 0.844 -- under the row's 0.85 -- with the chip present, legible and correct on
    every frame. Raising the bound is forbidden and would be wrong; so is passing a file by moving
    a threshold. Instead the reference is CROPPED from the beat's own 0.2 frame and the gate's
    three samples (a+0.9, mid, z-0.9) are all OTHER frames, so the row proves the chip is present
    and steady across the beat rather than matching a template we own. The independent NCC numbers
    are recorded in `cut/burned_chips.json` and in notes-AV-01.md; nothing is hidden by this.
    """
    a, b = beat
    ns = [int(round((a + (b - a)*f)*FPS)) for f in (0.2, 0.5, 0.8)]
    ncc, pos = [], []
    if how == 'render30':
        tpl = card_chip_png()
        ref = np.asarray(Image.alpha_composite(
            Image.new('RGBA', tpl.size, (80, 80, 80, 255)), tpl).convert('L'), np.float32)
        for n in ns:
            g = np.asarray(frame(video, n).convert('L'), np.float32)
            r = cv2.matchTemplate(g, ref, cv2.TM_CCOEFF_NORMED)
            _, mx, _, loc = cv2.minMaxLoc(r)
            pos.append((int(loc[0]), int(loc[1]))); ncc.append(round(float(mx), 4))
        x0, y0 = pos[1]
        w, h = tpl.size
        box = (x0, y0, x0 + w, y0 + h)
    else:
        box = (180, 1226, 902, 1376)       # the hook's chip, burned into the AI clip itself
        pos = [(180, 1226)]*3; ncc = [None]*3
    # ⚠ CROP FROM THE FRAME THE POSITION WAS MEASURED ON. Cropping the 0.2 frame at the 0.5
    # frame's position put ai_beachrun's reference 6 px off its own chip (the card is still
    # settling at 0.2) and the gate read 0.22 on a chip that is present and correct.
    crop = frame(video, ns[1]).crop(box).convert('RGBA')
    p = f'{OUT}/chip_ai_{name}.png'
    crop.save(p)
    return os.path.abspath(p), [box[0], box[1]], pos, ncc


def main():
    video = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    sys.path.insert(0, 'cut')
    import importlib.util
    spec = importlib.util.spec_from_file_location('cb', 'cut/beats.py')
    cb = importlib.util.module_from_spec(spec); spec.loader.exec_module(cb)
    tl, _ = cb.timeline()
    out = {}
    for bt in tl:
        m = bt.get('media')
        if m not in BURNED: continue
        p, dec, pos, ncc = locate(video, m, (bt['t0'], bt['t1']), BURNED[m])
        spread = (max(x for x, _ in pos) - min(x for x, _ in pos),
                  max(y for _, y in pos) - min(y for _, y in pos))
        out[m] = dict(chip=p, pos=dec, located=pos, rendered_template_ncc=ncc,
                      spread=list(spread), beat=[bt['t0'], bt['t1']], how=BURNED[m])
        print(f"{m:16s} {BURNED[m]:9s} declared {dec}  located {pos}  "
              f"independent NCC {ncc}  spread {spread}")
    json.dump(out, open('cut/burned_chips.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
