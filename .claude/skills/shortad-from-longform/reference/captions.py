#!/usr/bin/env python3
"""Word-timed burned captions, rendered with PIL so the typography matches the graphics.

Not libass: Manrope ships as a VARIABLE font and libass takes the default instance, so
ASS captions come out Regular while every graphic in the build is ExtraBold. Rendering
them the same way the plates are rendered keeps one type system.

Captions are SUPPRESSED wherever a graphic carries its own words (bullets, title cards,
statements, the CTA pill). Two competing text systems in a 1080-wide frame is unreadable,
and the bullets paraphrase the very sentence being spoken.
"""
import json, os, re, subprocess, sys
sys.path.insert(0, '.')
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
from PIL import Image, ImageDraw, ImageFilter
import vlib, beats as BT
from motionlib import font, text_size

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
VW, VH = 1080, 1920
CAP_Y  = vlib.CAP_Y
F      = font(64, "ExtraBold")
MAXW   = VW - 150
GROUP_MAX = 22          # characters; ~3 words -- a phone reads a short chunk, not a line

# Whisper mis-heard three words in this roll. They are HIS words on screen, so a
# mis-transcription burned into the captions is a spelling mistake in the ad.
FIX = {('six','back','abs.'): ('six','pack','abs.'),
       ('a','gold','picture'): ('a','goal','picture'),
       ('WuWu','stuff.'): ('Woo-woo','stuff.')}

def load_words():
    d = json.load(open('m.whisper.json'))
    out = []
    for s in d['segments']:
        for w in s.get('words', []):
            t = w['word'].strip()
            if t: out.append((t, float(w['start']), float(w['end'])))
    n = 0
    for i in range(len(out)):
        for src, dst in FIX.items():
            k = len(src)
            if tuple(x[0] for x in out[i:i+k]) == src:
                for j, word in enumerate(dst):
                    out[i+j] = (word, out[i+j][1], out[i+j][2])
                n += 1
    print(f'transcription fixes applied: {n}')
    return out

def suppressed():
    """Where captions must not run: graphics that carry their own words, plus any beat
    explicitly flagged caps=False (a card with a kicker or a caption)."""
    tl, ov = BT.timeline()
    # Lower thirds print the very sentence being spoken, so they mute the captions for
    # their duration exactly as the bullet screens do.
    return [(b['t0'], b['t1']) for b in tl + ov
            if b['kind'] in BT.NO_CAPS_KINDS or b['kind'] == 'lt' or b.get('caps') is False]

def groups(words, mute):
    def muted(t): return any(a - 0.15 <= t <= b + 0.05 for a, b in mute)
    gs, cur = [], []
    for w in words:
        if muted(w[1]):
            if cur: gs.append(cur); cur = []
            continue
        # never carry a group across a full stop: "life. You're more" reads as a mistake
        if cur and cur[-1][0].rstrip().endswith(('.', '?', '!')):
            gs.append(cur); cur = [w]; continue
        cand = cur + [w]
        if len(' '.join(x[0] for x in cand)) > GROUP_MAX and cur:
            gs.append(cur); cur = [w]
        elif cur and w[1] - cur[-1][2] > 0.55:
            gs.append(cur); cur = [w]
        else:
            cur = cand
    if cur: gs.append(cur)
    return gs

def render(gs, out='captions.mov', capdir='cap'):
    os.makedirs(capdir, exist_ok=True)
    blank = f'{capdir}/_blank.png'
    if not os.path.exists(blank):
        Image.new("RGBA", (VW, VH), (0, 0, 0, 0)).save(blank)
    entries, n, t = [], 0, 0.0
    for g in gs:
        txt = ' '.join(x[0] for x in g)
        if g[0][1] - t > 0.02:
            entries.append((blank, g[0][1] - t)); t = g[0][1]
        for k, (w, ws, we) in enumerate(g):
            p = f'{capdir}/c{n:05d}.png'; n += 1
            if not os.path.exists(p):
                im = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
                d = ImageDraw.Draw(im)
                tw = text_size(txt, F)[0]
                x = (VW - tw) // 2
                # shadow first, so the caption survives a bright b-roll frame
                sh = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
                ImageDraw.Draw(sh).text((x, CAP_Y), txt, font=F, fill=(0, 0, 0, 235), anchor="lt")
                im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
                im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
                cx = x
                for j, (ww, _, _) in enumerate(g):
                    col = vlib.OLIVE if j == k else (255, 255, 255)
                    d.text((cx, CAP_Y), ww, font=F, fill=col + (255,), anchor="lt")
                    cx += text_size(ww + ' ', F)[0]
                im.save(p)
            end = we if k == len(g) - 1 else g[k + 1][1]
            entries.append((p, max(0.04, end - max(ws, t)))); t = max(end, t)
    with open(f'{capdir}/list.txt', 'w') as f:
        for p, d in entries:
            f.write(f"file '{os.path.abspath(p)}'\nduration {d:.4f}\n")
        f.write(f"file '{os.path.abspath(entries[-1][0])}'\n")
    subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{capdir}/list.txt',
                    '-r', '30000/1001', '-c:v', 'qtrle', '-pix_fmt', 'argb', out], check=True)
    print(f'{len(gs)} groups, {n} word states -> {out}')

if __name__ == '__main__':
    ws = load_words(); mute = suppressed()
    gs = groups(ws, mute)
    kept = sum(len(g) for g in gs)
    print(f'words {len(ws)}  captioned {kept}  suppressed {len(ws)-kept} under graphics')
    render(gs)
