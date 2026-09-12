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
# Whisper mis-heard six things on this roll. They are HIS words on screen, so a
# mis-transcription burned into the captions is a spelling mistake in the ad.
FIX = {('your','gold','picture'):    ('your','goal','picture'),
       ('hit','your','golden.'):     ('hit','your','goal.'),
       ('number','of','a','chart,'): ('number','on','a','chart,'),
       ('time','of','debt,'):        ('time','of','day,'),
       ('in','Seconds'):             ('in','seconds.'),
       ('6packabs','.com'):          ('6PackAbs.com',''),
       ('nutritionist','and','diet'):('nutritionists','and','diet')}

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
    explicitly flagged caps=False (a card with a kicker or a caption).

    ⚠ IN A CUTDOWN THIS LIST IS READ FROM `mute.json`, WRITTEN BY THE CUTDOWN BUILDER (2026-09-12).
    The builder maps the MASTER's spans through the range plan; the generated cut beat sheet maps
    the BEATS. Those two agree to within a few milliseconds -- and a few milliseconds is enough,
    because groups() treats a word starting within 0.15 s of a span as muted. On this cutdown the
    card beat read 2.936 in the generated sheet against 2.950 in the builder, which muted one extra
    word: the render burned 103 caption states and `caption_sync_check.py`, re-deriving the
    grouping from THIS function, graded 104 and reported three "misses" on captions that are
    correct on the frame. One file, written once, read by both."""
    import os as _os, json as _json
    _m = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'mute.json')
    if _os.path.exists(_m):
        return [tuple(x) for x in _json.load(open(_m))]
    tl, ov = BT.timeline()
    # Lower thirds AND CTA pills print words of their own, so they mute the captions for
    # their duration exactly as the bullet screens do. Missing 'cta' here ran the captions
    # straight through all three pills -- "With Abs" overprinted by "to generate an image".
    return [(b['t0'], b['t1']) for b in tl + ov
            if b['kind'] in BT.NO_CAPS_KINDS or b['kind'] in ('lt','cta') or b.get('caps') is False]

def groups(words, mute):
    # ⚠ THE MUTE SLACK MUST NOT REACH ACROSS A CUTDOWN SEAM (2026-09-12, Ad 1 square audit 2).
    # A word is treated as muted if it starts within [a - 0.15, b + 0.05] of a suppressed span --
    # slack that stops a caption flashing on the first or last frames of a graphic. At a SEAM the
    # graphic is not there any anymore: the next range's picture is a different part of the film.
    # Measured on this cutdown: the first CTA pill's mute ends exactly on the 34.10 s seam and its
    # +0.05 swallowed "You're" at 34.133, so the line read "more attractive to" while the audio
    # said "You're more attractive to women". SEAMS is [] on a master, so nothing outside a
    # cutdown changes. It lives HERE, not in the cutdown builder, because caption_sync_check.py
    # re-derives the grouping from this same function -- a fix applied in only one of the two
    # makes the gate grade a grouping the render never had (it read 99.0 % on correct captions).
    _seams = sorted(getattr(BT, 'SEAMS', []) or [])

    def muted(t):
        for a, b in mute:
            lo, hi = a - 0.15, b + 0.05
            # ⚠ COMPARE WITH A TOLERANCE. A span clamped to a range edge and the seam itself are
            # computed by two different sums (dst0 + (a1 - src0) vs the next range's dst0) and came
            # out 1e-5 apart on this cut -- so an exact `s >= b` never matched, the slack stayed at
            # b + 0.05, and "You're" was muted again after the rule moved here. 1 ms is far below
            # the 50 ms slack this is clamping and far above the float noise.
            EPS = 1e-3
            for s in _seams:
                if s >= b - EPS: hi = min(hi, s); break
            for s in reversed(_seams):
                if s <= a + EPS: lo = max(lo, s); break
            if lo <= t <= hi: return True
        return False
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
    # HARD STOPS (2026-09-10, lesson A6.14): a line's last word is held up to 0.8 s, and that hold must never run into a
    # graphic that mutes the captions nor across a cutdown seam (beats.SEAMS, when the build defines it).
    STOPS = sorted(set([a_ for a_, b_ in suppressed()] + list(getattr(BT, 'SEAMS', []))))
    next_start = {id(g): (gs[i+1][0][1] if i + 1 < len(gs) else None) for i, g in enumerate(gs)}
    for g in gs:
        txt = ' '.join(x[0] for x in g)
        if g[0][1] - t > 0.02:
            entries.append((blank, g[0][1] - t)); t = g[0][1]
        for k, (w, ws, we) in enumerate(g):
            # The file name carries the state's CONTENT (line text + lit word), not just its sequence number: a changed
            # grouping renumbers every state, and a name keyed on the number alone silently reused the previous run's
            # pictures -- wrong words burned over correct timings (lesson A6.24, caught in stills 2026-09-10).
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
                    col = vlib.OLIVE if j == k else (255, 255, 255)
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
                end = max(end, ws + 1.0/29.97)                  # never zero, never past the next line
                stop = next((s_ for s_ in STOPS if s_ > ws + 1e-3), None)
                if stop is not None: end = max(min(end, stop), ws + 1.0/29.97)
            else:
                end = g[k + 1][1]
            entries.append((p, max(0.04, end - max(ws, t)))); t = max(end, t)
    with open(f'{capdir}/list.txt', 'w') as f:
        for p, d in entries:
            f.write(f"file '{os.path.abspath(p)}'\nduration {d:.4f}\n")
        # ⚠ THE TRAILING `file` LINE IS RENDERED, AND IT MUST BE THE BLANK (skill [S1].6).
        # The concat demuxer needs one more `file` after the last `duration`, and writing the
        # last caption STATE there re-showed its lit word past its own planned end: measured on
        # this build, "six pack abs," printed across the closing CTA pill's "With Abs" for 7
        # frames (master f6936-6942, 231.43-231.63 s) -- in the master AND in the cutdown, whose
        # caption stream ends at the same pill. The plan was right (cap/list.txt ends at 231.400,
        # the pill's own mute start); only the trailing repeat was wrong. The lesson was written
        # up on the Ad 2 square and never applied in code. A blank, held, then repeated.
        f.write(f"file '{os.path.abspath(blank)}'\nduration 0.5000\n")
        f.write(f"file '{os.path.abspath(blank)}'\n")
    subprocess.run([FF, '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{capdir}/list.txt',
                    '-r', '30000/1001', '-c:v', 'qtrle', '-pix_fmt', 'argb', out], check=True)
    print(f'{len(gs)} groups, {n} word states -> {out}')

if __name__ == '__main__':
    ws = load_words(); mute = suppressed()
    gs = groups(ws, mute)
    kept = sum(len(g) for g in gs)
    print(f'words {len(ws)}  captioned {kept}  suppressed {len(ws)-kept} under graphics')
    render(gs)
