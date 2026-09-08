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
FPS = 30000/1001; VW = 1080
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
frames = [max(int(round(s * FPS)) + 1, int(round((s + 0.4 * (e - s)) * FPS))) for (_, s, e, _, _) in items]
uniq = sorted(set(frames))
sel = '+'.join(f'eq(n,{n})' for n in uniq)
open('/tmp/_cs_sel.txt', 'w').write(f"select='{sel}',crop=1080:110:0:1385,scale=540:55")
raw = subprocess.run([FF,'-v','error','-i',V,'-filter_script:v','/tmp/_cs_sel.txt','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'],
                     capture_output=True).stdout
A = np.frombuffer(raw, np.uint8).reshape(-1, 55, 540, 3).astype(np.int16)
assert len(A) == len(uniq), (len(A), len(uniq))
band = dict(zip(uniq, A))
def olive_x(im):
    r, g, b = im[...,0], im[...,1], im[...,2]
    m = (g > r + 6) & (g > b + 30) & (g > 90) & (r > 70)
    if m.sum() < 12: return None
    xs = np.nonzero(m.any(0))[0]
    return float(xs.mean()) * 2.0, float(xs.min()) * 2.0, float(xs.max()) * 2.0     # back to 1080 px
hits, miss = 0, []
for (w, s, e, lo, hi), n in zip(items, frames):
    o = olive_x(band[n])
    tol = max(40.0, 0.6 * (hi - lo))
    ok = o is not None and (lo - tol) <= o[0] <= (hi + tol)
    if ok: hits += 1
    else: miss.append((round(s, 2), w, None if o is None else round(o[0]), round((lo+hi)/2)))
n_items = len(items); frac = hits / max(1, n_items)
runs = 0; cur = 0; ms = set(m[0] for m in miss)
for (w, s, e, lo, hi) in items:
    cur = cur + 1 if round(s, 2) in ms else 0; runs = max(runs, cur)
# --- B. silence
subprocess.run([FF,'-v','error','-y','-i',V,'-vn','-ac','1','-ar','16000','-af','highpass=f=200,lowpass=f=3500','-c:a','pcm_s16le','/tmp/_cs.wav'], check=True)
a = np.frombuffer(wave.open('/tmp/_cs.wav').readframes(10**9), dtype='<i2').astype(np.float32)/32768
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
