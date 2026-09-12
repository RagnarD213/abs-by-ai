#!/usr/bin/env python3
"""THE SUBTITLE GATE (Dan, 2026-09-08): "the highlighted word in the subtitles matches what's actually
being said, never desynchronised." Measured on the DELIVERED file, per word, end to end:

  A. WORD-BY-WORD: at the instant the forced alignment says a word starts (+60 ms), the frame is pulled from
     the delivered file, the olive (karaoke) highlight in the caption band is located, and its x is compared
     with where THAT word sits in its caption line (same font metrics as captions.py). A miss = a different
     word is lit while this one is spoken. PASS: >= 97 % of words hit and no run of 3+ consecutive misses.
  B. SILENCE: a highlighted word must sit inside speech -- some frame within +-150 ms of the word's centre
     is >= 10 dB above the floor in the speech band. (Soft function words are quiet; they are not silent.)
  C. INFO: the aligned starts vs an independent Whisper-medium transcription (mean/sd), to catch a broken
     alignment -- if two Whispers agree with each other and not with the alignment, the alignment is wrong.
Usage: python3 caption_sync_check.py <delivered.mp4>"""
import json, os, subprocess, sys, wave
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
V = sys.argv[1] if len(sys.argv) > 1 else 'ad2v2h_vertical_9x16.mp4'
VW = 1080
# The frame rate is the DELIVERED file's, probed, never assumed: every sample below is pulled by frame index, and
# a 24 fps master read at 29.97 samples the caption band 25 % too late by the end (Zeeshan's Ad 1, 2026-09-10).
_fr = subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-select_streams', 'v', '-show_entries',
                      'stream=r_frame_rate', '-of', 'csv=p=0', V], capture_output=True, text=True).stdout.strip().split('\n')[0]
_n, _d = (_fr.split('/') + ['1'])[:2]; FPS = int(_n) / int(_d)
# ⚠ PER-PROCESS TEMP FILES. These were the fixed paths _CS_WAV and _CS_SEL: with two builds
# running at once the OTHER session's extraction overwrote the wav between this one's write and its read, and test B
# graded THIS file's word list against THAT file's audio -- 8 "words lit outside speech" on a file whose audio had not
# changed by a byte (Ad 5 round 2, 2026-09-11). A gate that measured the wrong file is worse than one that failed
# (skill A6.25). Re-applied after a concurrent edit dropped it; keep it.
import atexit, shutil, tempfile
_CSTMP = tempfile.mkdtemp(prefix='capsync_')
atexit.register(shutil.rmtree, _CSTMP, True)
_CS_WAV, _CS_SEL = os.path.join(_CSTMP, 'cs.wav'), os.path.join(_CSTMP, 'sel.txt')
sys.path.insert(0, '.'); import captions as C
words = C.load_words(); mute = C.suppressed(); gs = C.groups(words, mute)
F = C.F
# expected x-range of every shown word, exactly as captions.py lays the line out
items = []   # (word, start, end, x_lo, x_hi)
for g in gs:
    txt = ' '.join(x[0] for x in g); x0 = (VW - F.getlength(txt)) // 2; cx = float(x0)
    for (w, s, e) in g:
        wl = F.getlength(w); items.append((w, s, e, cx, cx + wl)); cx += F.getlength(w + ' ')
# --- A. pull the caption band at each word's frame (start + 60 ms), one ffmpeg pass
# sample INSIDE the spoken word: 40 % into it, at least one frame after its start (a 40 ms 'on' is one frame long)
# ⚠ THE BAND'S POSITION COMES FROM THE BUILD'S OWN CAP_Y, NEVER A CONSTANT. It was hard-coded at
# y=1385 for the 9:16 frame (CAP_Y 1400 minus 15), which on the 1:1 square build (CAP_Y 880) reads
# 505 px BELOW the captions and finds no highlight at all -- a gate measuring empty field would have
# failed a correct build, the mirror of the 24 fps index bug this file already carries (2026-09-11).
# ⚠ SAMPLE INSIDE THE WORD'S OWN SPAN. `round(s*FPS)+1` lands PAST a word shorter than two
# frames, so the gate graded the NEXT word and reported four false misses on 20-60 ms
# function words ('a', 'of', 'and') -- audit finding F2, 2026-09-11.
frames = [min(max(int(round(s * FPS)) + 1, int(round((s + 0.4 * (e - s)) * FPS))),
              max(int(round(s * FPS)), int(round(e * FPS)) - 1)) for (_, s, e, _, _) in items]
# ⚠ A WORD MAY BE UNREADABLE ON THE ONE FRAME WE HAPPEN TO SAMPLE, AND READABLE ON THE NEXT.
# The caption image is IDENTICAL across a word's own span -- same line, same lit word -- so any frame in that span
# measures the same thing. But an editor's light-leak strobe washes the band toward white for a few frames at a time:
# measured on Ad 5's cutdown, "when" (frames 212-215, inside Muhammad's 209-220 leak) carries 96 qualifying pixels at
# 212 and 0 at 214-215, and the 40 %-into-the-word heuristic landed on a washed one. That is the INSTRUMENT failing,
# not the build: reported as a miss it took a correct cutdown to 96.1 % and failed it.
# So each word gets up to CAND candidates spread across its own span, tried LEAST-WASHED FIRST (lowest band luma),
# and the first that yields a detection is the one graded. This is a strictly better measurement of the same word --
# never a looser bound: a word that is lit wrongly is lit wrongly on every frame of its span, and a word readable on
# no frame of its span is still a miss.
CAND = 5
def _cands(s, e, n0):
    a, b = int(round(s * FPS)), max(int(round(s * FPS)), int(round(e * FPS)) - 1)
    if b <= a: return [n0]
    step = max(1, (b - a) // (CAND - 1))
    return sorted({n0} | {x for x in range(a, b + 1, step)} | {b})
cands = [_cands(s, e, n) for (_, s, e, _, _), n in zip(items, frames)]
uniq = sorted({x for c in cands for x in c})
sel = '+'.join(f'eq(n,{n})' for n in uniq)
CAP_Y = getattr(C, 'CAP_Y', 1400)
BAND_Y, BAND_H = max(0, int(CAP_Y) - 15), 110
# ⚠ FULL RESOLUTION. At half resolution the downscale averages the highlight's core with
# whatever is behind it, and the ABSOLUTE thresholds below then depend on the background
# being bright: measured on a build with a dark bed behind the caption band, a short word
# fell from 48-56 qualifying pixels to 0-10, under the 12-pixel floor, and the gate reported
# "no highlight" on nine words that were lit correctly (audit F2). The band is 110 rows;
# reading it at full width costs nothing.
open(_CS_SEL, 'w').write(f"select='{sel}',crop={VW}:{BAND_H}:0:{BAND_Y}")
raw = subprocess.run([FF,'-v','error','-i',V,'-filter_script:v',_CS_SEL,'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],
                     capture_output=True).stdout
A = np.frombuffer(raw, np.uint8).reshape(-1, BAND_H, VW, 3).astype(np.int16)
assert len(A) == len(uniq), (len(A), len(uniq))
band = dict(zip(uniq, A))
# The karaoke highlight is drawn at the build's OWN colour, at full opacity, on top of
# whatever sits behind it -- so matching THAT colour is a strictly more specific test than
# "greenish and bright enough", not a looser one. The generic test stays as the fallback for
# a build that does not expose one.
# ⚠⚠ MEASURED REGRESSION ON OLIVE-GRADED MATERIAL (Ad 2 square, 2026-09-11) -- NOT YET FIXED,
# RECORDED HERE SO IT IS NOT REDISCOVERED. The full-resolution + exact-highlight-colour pair above
# is strictly better on a build with a dark bed behind the captions. It is WORSE on a build whose
# GRADE sits inside the tolerance of its own accent colour: Muhammad's room tone is within +-22 of
# his olive (140,153,91), so on the Ad 2 square the exact mask matched 13,347 pixels on frame 6882
# where the lit word is ~1,200, and the heaviest contiguous column run landed on the background at
# x 128-238 instead of the word at 358. Twelve words were reported as misses; ALL TWELVE were pulled
# at full resolution and are the correct word, lit in the correct place, legible -- and the caption
# PLAN is correct at every one of those samples. The same captions scored 99.0 % on the half-
# resolution instrument an hour earlier and 98.2 % after.
# DO NOT "fix" this by loosening the tolerance or reverting to half resolution -- half resolution
# has its own documented failure (audit F2). The two candidate real fixes, neither taken yet:
#   (a) require the winning run to be DENSE in the caption's own row band (glyph rows), which the
#       background blob is not -- a strictly more specific test, not a looser one;
#   (b) the picture-side fix the skill already sanctions ([A6].17): a scrim behind the caption band,
#       which puts the background under both the eye's and the detector's threshold.
# Whoever picks this up: the corpus must pass, and a build whose captions are correct must not be
# failing this gate.
HL = tuple(getattr(getattr(C, 'vlib', None), 'OLIVE', (140, 153, 91)))

def olive_x(im):
    r, g, b = im[...,0], im[...,1], im[...,2]
    m = ((np.abs(r - HL[0]) <= 22) & (np.abs(g - HL[1]) <= 22) & (np.abs(b - HL[2]) <= 28))
    if m.sum() < 40:                                   # fallback: the generic green test
        m = (g > r + 6) & (g > b + 30) & (g > 90) & (r > 70)
    if m.sum() < 12: return None
    # ⚠ THE CENTROID OF EVERY MATCHING PIXEL IS NOT THE WORD. A background that survives the
    # colour test (neon-green shorts, broccoli) drags the mean off the word by 100+ px. The
    # highlight is a DENSE blob; take the heaviest contiguous run of columns.
    col = m.sum(0).astype(float)
    on = col > max(1.0, 0.12 * col.max())
    runs, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]: j += 1
            runs.append((i, j)); i = j
        else: i += 1
    if not runs: return None
    a_, b_ = max(runs, key=lambda q: col[q[0]:q[1]].sum())
    w_ = col[a_:b_]
    cx = float((np.arange(a_, b_) * w_).sum() / max(w_.sum(), 1e-9))
    return cx, float(a_), float(b_ - 1)
hits, miss = 0, []
for (w, s, e, lo, hi), n, cs_ in zip(items, frames, cands):
    tol = max(40.0, 0.6 * (hi - lo))
    o = None
    for c_ in sorted(cs_, key=lambda x: float(band[x].mean())):     # least-washed frame first
        o = olive_x(band[c_])
        if o is not None: n = c_; break
    ok = o is not None and (lo - tol) <= o[0] <= (hi + tol)
    if ok: hits += 1
    else: miss.append((round(s, 2), w, None if o is None else round(o[0]), round((lo+hi)/2)))
n_items = len(items); frac = hits / max(1, n_items)
runs = 0; cur = 0; ms = set(m[0] for m in miss)
for (w, s, e, lo, hi) in items:
    cur = cur + 1 if round(s, 2) in ms else 0; runs = max(runs, cur)
# --- B. silence
subprocess.run([FF,'-v','error','-y','-i',V,'-vn','-ac','1','-ar','16000','-af','highpass=f=200,lowpass=f=3500','-c:a','pcm_s16le',_CS_WAV], check=True)
a = np.frombuffer(wave.open(_CS_WAV).readframes(10**9), dtype='<i2').astype(np.float32)/32768
hop = 160; env = np.array([20*np.log10(np.sqrt((a[i:i+320]**2).mean()) + 1e-9) for i in range(0, len(a)-320, hop)])
floor = np.percentile(env, 10)
def speech_near(t, r=0.15):
    i0 = max(0, int((t-r)*16000/hop)); i1 = min(len(env), int((t+r)*16000/hop)+1)
    return env[i0:i1].max() >= floor + 10 if i1 > i0 else False
silent = [(w, round(s,2)) for (w, s, e, lo, hi) in items if not speech_near((s+e)/2)]
# --- C. info
info = ''
if os.path.exists('ref_medium.whisper.json'):
    import difflib
    med = [(w['word'].strip().lower().strip('.,!?'), w['start']) for s_ in json.load(open('ref_medium.whisper.json'))['segments'] for w in s_.get('words',[])]
    Aw = [w[0].lower().strip('.,!?') for w in words]; Bw = [m[0] for m in med]
    sm = difflib.SequenceMatcher(a=Aw, b=Bw, autojunk=False); d = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for i, j in zip(range(i1, i2), range(j1, j2)): d.append(med[j][1] - words[i][1])
    d = np.array(d); info = f'Whisper-medium minus aligned start on {len(d)} words: mean {d.mean()*1000:+.0f} ms, sd {d.std()*1000:.0f}'
ok = frac >= 0.97 and runs < 3 and len(silent) == 0
print(f'caption sync on {V}: {n_items} highlighted words')
print(f'  A. the word being said is the word lit: {hits}/{n_items} = {100*frac:.1f} %  (longest run of misses {runs}); misses: {miss[:10]}')
print(f'  B. words lit outside speech: {len(silent)} {silent[:6]}')
if info: print(f'  C. info: {info}')
print('CAPTION SYNC ' + ('PASS' if ok else 'FAIL'))
os.makedirs('logs', exist_ok=True)
json.dump(dict(video=V, words=n_items, hit_fraction=frac, longest_miss_run=runs, misses=miss, silent=silent, info=info, ok=bool(ok)), open('logs/caption_sync.json','w'), indent=1)
sys.exit(0 if ok else 1)
