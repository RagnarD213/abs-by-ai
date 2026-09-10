#!/usr/bin/env python3
"""Word-timed burned captions, rendered with PIL so the typography matches the graphics.

Not libass: Manrope ships as a VARIABLE font and libass takes the default instance, so
ASS captions come out Regular while every graphic in the build is ExtraBold. Rendering
them the same way the plates are rendered keeps one type system.

Captions are SUPPRESSED wherever a graphic carries its own words (bullets, title cards,
statements, the CTA pill). Two competing text systems in a 1080-wide frame is unreadable,
and the bullets paraphrase the very sentence being spoken.
"""
import hashlib, json, os, re, subprocess, sys
sys.path.insert(0, '.')
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
from PIL import Image, ImageDraw, ImageFilter
import zgfx as vlib, beats as BT
from motionlib import font, text_size

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
VW, VH = 1080, 1920
CAP_Y  = vlib.CAP_Y
F      = font(64, "ExtraBold")
MAXW   = VW - 150
GROUP_MAX = 22          # characters; ~3 words -- a phone reads a short chunk, not a line

# Whisper mis-heard these on Zeeshan's Ad 1 mix (2026-09-10). They are HIS words on screen, so a
# mis-transcription burned into the captions is a spelling mistake in the ad.
FIX = {('gold','picture'):          ('goal','picture'),
       ('six','back','abs,'):        ('six','pack','abs,'),
       ('woo','-woo'):               ('woo-woo',''),
       ('chat','GPT'):               ('ChatGPT',''),
       ('body','builders'):          ('bodybuilders','')}

def load_words(source='words_ctc.json'):
    """Caption words with their timings. ⚠ WHISPER'S OWN WORD TIMESTAMPS ARE ~130 ms EARLY ON THIS MIX
    (sd 150, p90 +295 ms against a CTC forced alignment; 289 of 875 words off by more than 150 ms) --
    that is the 'highlighted word does not match what is said' Dan rejected 2026-09-08. The timings
    now come from align_ctc.py (wav2vec2 CTC forced alignment of the same words to his mix); the
    Whisper JSON is only the source of the WORDS."""
    import os
    if source and os.path.exists(source):
        d = json.load(open(source))
        out = [(w['word'].strip(), float(w['start']), float(w['end'])) for w in d if w['word'].strip()]
        n = 0   # the FIX map was applied before alignment, so no re-application here
        print(f'caption timings: {source} ({len(out)} words, CTC forced alignment)')
        return out
    d = json.load(open('ref.whisper.json'))
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
    out = [w for w in out if w[0]]
    print(f'transcription fixes applied: {n}')
    return out

def suppressed():
    """Where captions must not run: graphics that carry their own words, plus any beat
    explicitly flagged caps=False (a card with a kicker or a caption)."""
    # His persistent CTA bar sits ABOVE the caption band (zgfx.CTA_BOX), so it does not mute them; every
    # graphic that prints the spoken sentence, and the white app screens, do (beats.muted_ranges).
    return BT.muted_ranges()

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
    # HARD STOPS: a line's last word is held up to 0.8 s, and that hold must never run into a graphic that mutes the
    # captions nor across a cutdown seam (seen 2026-09-10: "is where I'm at today." sat on the app screen after the
    # cutdown's first seam, "everything changes." ran into the next range).
    STOPS = sorted(set([a_ for a_, b_ in suppressed()] + list(getattr(BT, 'SEAMS', []))))
    next_start = {id(g): (gs[i+1][0][1] if i + 1 < len(gs) else None) for i, g in enumerate(gs)}
    for g in gs:
        txt = ' '.join(x[0] for x in g)
        if g[0][1] - t > 0.02:
            entries.append((blank, g[0][1] - t)); t = g[0][1]
        for k, (w, ws, we) in enumerate(g):
            # The file name carries the state's CONTENT (line text + lit word), not just its sequence number: a changed
            # grouping renumbers every state, and a name keyed on the number alone silently reused the previous run's
            # pictures -- "I was 200 pounds." burned over "I generated this picture" (2026-09-10, caught in stills).
            p = f"{capdir}/c{n:05d}_{hashlib.md5(f'{txt}|{k}|{CAP_Y}'.encode()).hexdigest()[:10]}.png"; n += 1
            if not os.path.exists(p):
                im = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
                d = ImageDraw.Draw(im)
                # ⚠ BASELINE, NOT TOP. PIL's "t" anchor is the ascender line OF THE STRING
                # IT IS GIVEN, so drawing one word at a time aligns each by its own top:
                # every word without an ascender drops below its neighbours and the line
                # reads as broken. And the advance must be getlength(), which counts the
                # trailing space -- getbbox() ignores it, so the words crowd and drift left
                # of their own shadow. Both faults shipped in an earlier attempt.
                BASE = CAP_Y + F.getmetrics()[0]
                tw = F.getlength(txt)
                x = int((VW - tw) // 2)
                sh = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
                ImageDraw.Draw(sh).text((x, BASE), txt, font=F, fill=(0, 0, 0, 235), anchor="ls")
                im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
                im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
                cx = float(x)
                for j, (ww, _, _) in enumerate(g):
                    col = vlib.LIME if j == k else (255, 255, 255)
                    d.text((int(cx), BASE), ww, font=F, fill=col + (255,), anchor="ls")
                    cx += F.getlength(ww + ' ')
                im.save(p)
            if k == len(g) - 1:
                # The LAST word of a line stays lit until the next line starts (or 0.8 s, whichever is
                # sooner) instead of dropping at its own acoustic end: a 40 ms 'on' used to flash for one
                # frame and vanish, which reads as the highlight skipping the word (Dan, 2026-09-08).
                nxt = next_start.get(id(g))
                hold = max(we, ws + 0.12)                       # at least 120 ms on screen
                end = min(nxt, max(hold, min(nxt, we + 0.8))) if nxt is not None else we + 0.3
                end = max(end, ws + 1.0/24)                  # never zero, never past the next line
                stop = next((s_ for s_ in STOPS if s_ > ws + 1e-3), None)
                if stop is not None: end = max(min(end, stop), ws + 1.0/24)
            else:
                end = g[k + 1][1]
            entries.append((p, max(0.04, end - max(ws, t)))); t = max(end, t)
    with open(f'{capdir}/list.txt', 'w') as f:
        for p, d in entries:
            f.write(f"file '{os.path.abspath(p)}'\nduration {d:.4f}\n")
        f.write(f"file '{os.path.abspath(entries[-1][0])}'\n")
    subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{capdir}/list.txt',
                    '-r', '24', '-c:v', 'qtrle', '-pix_fmt', 'argb', out], check=True)
    print(f'{len(gs)} groups, {n} word states -> {out}')

if __name__ == '__main__':
    ws = load_words(); mute = suppressed()
    gs = groups(ws, mute)
    kept = sum(len(g) for g in gs)
    print(f'words {len(ws)}  captioned {kept}  suppressed {len(ws)-kept} under graphics')
    render(gs)
