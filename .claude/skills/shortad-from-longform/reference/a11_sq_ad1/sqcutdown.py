#!/usr/bin/env python3
"""The <=0:59 SQUARE cutdown: intervals SELECTED out of the finished square master.

  python3 sqcutdown.py            # plan only, prints the transcript to read as prose
  python3 sqcutdown.py --build    # cut the picture + his mix, rebuild the captions, mux

Selecting from the approved master rather than re-cutting from source carries every
decision through unchanged -- take choice, grade, graphics, framing, labels. The RANGES are
`cutdown.py`'s, i.e. the ones the approved vertical's cutdown used, expressed as PHRASE
ANCHORS so they land on the same words even though the beat sheet moved under them since.

⚠ THE AUDIO IS THE APPROVED MASTER'S MIX, CUT AND NOTHING ELSE. No bed rebuild, no
loudnorm, no limiter: `his_mix.wav` (the vertical's own decoded stream) is cut at the
seams with 4 ms raised-cosine joins and encoded straight to AAC 320k. The vertical's
`cutdown.py` rebuilt the bed and ran two-pass loudnorm, which is the class of thing Dan
rejected on 2026-09-10 ("Use Zishan's audio") and Step 4 now forbids.
"""
import json, math, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, '.')
import beats as BT

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
FPS = 30000/1001
SR = 48000
# ⚠ THE RANGE EDGES COME FROM THE CTC ALIGNMENT, NOT FROM WHISPER (audit 2, 2026-09-12).
# `beats.at/end` read m.whisper.json, whose word starts run ~130 ms early and whose word ends
# truncate. On a beat sheet that is harmless -- a beat edge is a picture decision. On a CUTDOWN
# SEAM it is a defect twice over: the 33.63 s seam opened 35 ms INSIDE the onset of "You're"
# (already at -23.5 dBFS), so the audio clipped the word AND the caption mapper dropped it, and
# the caption after the seam read "more attractive to" while the audio said "You're more
# attractive to women"; and range ends cut word tails ("changes." 118 ms early with the sibilant
# still at -25 dBFS). words_ctc.json is the alignment the CAPTIONS are built from, so taking the
# seams from it makes the picture, the audio and the captions agree by construction.
_CTC = [(BT._n(w['word']), float(w['start']), float(w['end']))
        for w in json.load(open('words_ctc.json')) if BT._n(w['word'])]

def _seq_ctc(phrase, after=0.0):
    toks = [BT._n(x) for x in phrase.split() if BT._n(x)]
    for i in range(len(_CTC)):
        if _CTC[i][1] < after: continue
        if [w[0] for w in _CTC[i:i+len(toks)]] == toks: return i, len(toks)
    raise SystemExit(f'phrase not found in words_ctc.json: {phrase!r}')

def at(phrase, after=0.0):
    i, _ = _seq_ctc(phrase, after); return _CTC[i][1]

def end(phrase, after=0.0):
    i, n = _seq_ctc(phrase, after); return _CTC[i+n-1][2]

# Dan's settled shorts-ad doctrine: sell the GENERATION almost exclusively, give the
# trainer/nutritionist exactly one beat near the end, say the CTA twice.
RANGES = [
 (0.0,                                                   end('and its not even real')),
 (at('i generated this picture'),                        end('when i was 200 pounds')),
 (at('i made it my phone lock screen'),                  end('and this is where im at today')),
 (at('with ai you can create a picture'),                end('youve always wanted')),
 (at('and once you see yourself with abs'),              end('everything changes')),
 # ⚠ NOT 'and right now you can generate' (91.02): that opens INSIDE his lower third
 # 86.90-91.85, whose sentence is cut away -- so the cutdown printed "If you saw yourself
 # with abs, you'd be MOTIVATED" over "And right now, you can generate..." (lesson A6.15,
 # live in the first build). 91.85 is the lower third's end AND the bullets screen's start,
 # and the bullets print these very words. Costs "And right now," (0.83 s).
 (at('you can generate an ai image of yourself with ripped'), end('to see yourself with abs')),
 (at('youre more attractive to women'),                  end('you feel better')),
 (at('generating an image of yourself with abs is just'), end('helps you make it real')),
 (at('to start losing your belly fat'),                  BT.DUR),
]

EDGES = sorted({0.0, BT.DUR} | {x for b in BT.timeline()[0] for x in (b['t0'], b['t1'])})

def snap(t, tol=0.35):
    """Pull a range edge onto the nearest beat boundary. A range that starts 80 ms inside a
    card shows that card already half-open, which reads as a dropped frame.

    Returns (time, snapped?). The flag matters at the frame step: a start that was snapped onto
    a beat edge must be CEILed, because a boundary at time T means frame ceil(T*FPS) is the first
    frame that belongs to the new beat -- flooring it re-opens the range 25 ms inside the graphic
    the snap existed to clear (it fired the A6.15 orphan-overlay assert on the first run of this
    fix). A start that was NOT snapped is floored, so it contains the word it opens on."""
    n = min(EDGES, key=lambda e: abs(e-t))
    return (n, True) if abs(n-t) <= tol else (t, False)


MASTER_FRAMES = 6976            # Muhammad's count; the square master is asserted to it


# ⚠⚠ A CTC WORD END TRUNCATES A FRICATIVE. CEILING IT BY ONE FRAME IS NOT ENOUGH (audit 3, 2026-09-12).
# The 34.10 s seam ended range 5 on "...six pack abs." and cut the "s" AT ITS LOUDEST POINT: measured in
# 5 ms bins on his mix, the sibilant (high-frequency ratio 0.93-0.99) runs from -45 ms to +70 ms around
# the cut and is still RISING at -20.9 dBFS on the cut frame, while CTC had ended the word 14 ms earlier.
# It played as "with ab-" into silence. Ceiling the end (the audit-2 fix) bought one frame of it; the
# word needs its DECAY. So a range end that is not pinned to a beat boundary is carried forward while
# the mix is still loud, stopping at the first quiet frame -- never into the next word, and never more
# than TAIL_MAX. Same class as the in-point clip audit 2 found, mirrored onto the out-point.
TAIL_DB, TAIL_MAX, TAIL_GAP = -35.0, 0.30, 0.04


def _mix():
    """His mix, mono float, at SR. Decoded with the tool that wrote it (skill S1.11: `wave` raises on
    ffmpeg's pcm_s24le and reads a float WAV silently wrong)."""
    if not hasattr(_mix, 'a'):
        raw = subprocess.run([FF, '-nostdin', '-v', 'error', '-i', 'his_mix.wav', '-map', '0:a',
                              '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                             capture_output=True).stdout
        _mix.a = np.frombuffer(raw, '<i2').astype(np.float32) / 32768
    return _mix.a


def pad_tail(b, snapped):
    """Carry a range end past the CTC word end until the sound it belongs to has decayed."""
    if snapped: return b
    a = _mix()
    nxt = min([w[1] for w in _CTC if w[1] > b + 1e-3] or [b + TAIL_MAX + 1.0])
    lim = min(b + TAIL_MAX, nxt - TAIL_GAP)
    t = b
    while t < lim:
        seg = a[int(t*SR):int((t + 0.005)*SR)]
        if len(seg) == 0: break
        if 20*np.log10(float(np.sqrt((seg**2).mean())) + 1e-12) < TAIL_DB: break
        t += 0.005
    return t

def plan():
    """⚠ THE PLAN IS IN FRAMES, NOT SECONDS. A range expressed in seconds can ask for one
    frame more than the master holds (the last range's src1 is beats.DUR = 232.768 s, while
    6,976 frames is 232.7659 s), and the selection then comes out a frame short with every
    duration check still green. Each range takes exactly the frames that exist between its
    two frame indices."""
    out, prev = [], 0
    for (a, a_snapped), (b, b_snapped) in [(snap(a), snap(b)) for a, b in RANGES]:
        assert b > a, (a, b)
        # ⚠ FLOOR THE START, CEIL THE END. A range must CONTAIN every word it carries: rounding
        # to the nearest frame can start half a frame after a word's onset (which clips it and
        # makes the caption mapper drop it) or end half a frame before its tail. The exception
        # is an edge that snap() put ON a beat boundary: there it is ROUNDED, because a boundary
        # is ONE frame index and the previous range's exclusive end must be the same number as the
        # next range's start -- ceil/floor there opens a one-frame hole or a one-frame overlap, and
        # on this cut it leaked the first frame of `today_flag` between the trees photo and the app
        # recording (the flicker audit 2 found) and turned a contiguous join into a real seam.
        n0 = max(0, int(round(a*FPS) if a_snapped else math.floor(a*FPS)))
        b = pad_tail(b, b_snapped)
        n1 = min(int(round(b*FPS) if b_snapped else math.ceil(b*FPS)), MASTER_FRAMES)
        assert n1 > n0, (a, b, n0, n1)
        out.append(dict(src0=round(n0/FPS, 5), src1=round(n1/FPS, 5), frames=n1-n0, n0=n0,
                        dst0=round(prev/FPS, 5), dst1=round((prev+n1-n0)/FPS, 5)))
        prev += n1-n0
    return out, prev


def assert_no_orphan_overlay(P):
    """⚠ NO RANGE MAY OPEN ON THE TAIL OF A BURNED OVERLAY WHOSE START WAS CUT AWAY.

    The cutdown is a SELECTION out of the finished master, so his lower thirds and CTA pills
    are already in the pixels. A range that begins part-way through one inherits words that
    belong to a sentence the cutdown no longer contains (lesson A6.15). This is structural:
    it cannot be seen in the beat sheet, because the generated cut beat sheet correctly drops
    the overlay -- only the picture still has it."""
    bad = []
    for p in P:
        for o in BT.LOWER_THIRDS + BT.CTAS:
            starts_inside = o['t0'] < p['src0'] - 1e-6 < o['t1']
            dropped = not any(q['src0'] <= o['t0'] <= q['src1'] for q in P)
            if starts_inside and dropped:
                bad.append((round(p['src0'], 3), o['kind'], round(o['t0'], 2), round(o['t1'], 2),
                            (o.get('lines') or [o.get('big', '')])[0][:44]))
    for b in bad:
        print(f'  ORPHAN OVERLAY: range opens at {b[0]}s inside {b[1]} {b[2]}-{b[3]} "{b[4]}"')
    assert not bad, 'a range opens on the tail of an overlay whose start was cut away (A6.15)'
    print(f'no range opens on an orphaned overlay ({len(BT.LOWER_THIRDS)+len(BT.CTAS)} checked)')


def transcript(P):
    """⚠ READ THIS AS PROSE BEFORE MAPPING ANY RANGES. Attempt 1 selected by topic doctrine,
    never read the result, and Dan's verdict was 'the cutdown makes no sense at all'. Every
    seam has to be a sentence boundary AND a thought boundary."""
    import captions as CAP
    words = CAP.load_words()
    lines = []
    for p in P:
        ws = [w for w, s, e in words if p['src0'] - 0.05 <= s <= p['src1']]
        lines.append(' '.join(ws))
    return lines


def raised_cosine(n):
    return 0.5*(1 - np.cos(np.pi*np.arange(n)/max(1, n-1)))


def decode(path):
    """Decode to float64 stereo with ffmpeg. ⚠ NOT `wave`: ffmpeg's pcm_s24le writes
    WAVE_FORMAT_EXTENSIBLE (tag 65534), which the stdlib refuses outright -- and a float
    WAV it would read SILENTLY WRONG (skill A8.14). Decode with the same tool that wrote it."""
    raw = subprocess.run([FF, '-nostdin', '-v', 'error', '-i', path, '-f', 'f32le',
                          '-ac', '2', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype='<f4').reshape(-1, 2).astype(np.float64)


def cut_his_mix(P, src='his_mix.wav', out='cut/his_mix.wav', join_ms=4.0):
    """His mix, CUT. Nothing else happens to it: no gain, no limiter, no loudnorm, no
    mono sum -- only the seams get a 4 ms raised-cosine join so a splice does not click."""
    a = decode(src)
    j = int(SR*join_ms/1000)
    parts = []
    for p in P:
        ns = int(round(p['frames']*SR*1001/30000))
        s0 = int(round(p['src0']*SR))
        seg = a[s0:s0+ns].copy()
        if len(seg) < ns: seg = np.vstack([seg, np.zeros((ns-len(seg), 2))])
        r = raised_cosine(j)[:, None]
        seg[:j] *= r; seg[-j:] *= r[::-1]
        parts.append(seg)
    y = np.vstack(parts)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR),
                    '-ac', '2', '-i', '-', '-c:a', 'pcm_s24le', out],
                   input=np.clip(y, -1, 1).astype('<f4').tobytes(), check=True)
    return y.shape[0]


def sh(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: print(' '.join(str(x) for x in c[:40]), '\n', r.stderr[-1800:]); raise SystemExit(1)
    return r


def nframes(path):
    j = json.loads(subprocess.run([FP, '-v', 'error', '-select_streams', 'v', '-count_frames',
        '-show_entries', 'stream=nb_read_frames', '-of', 'json', path],
        capture_output=True, text=True).stdout)['streams'][0]
    return int(j['nb_read_frames'])


def _gray(path, n, size=270):
    """One frame of `path`, by INDEX, as a small gray array. Index, never time: a time seek
    lands on the wrong frame on these masters (skill A7.12)."""
    raw = subprocess.run([FF, '-nostdin', '-v', 'error', '-i', path, '-vf',
                          f"select='eq(n,{n})',scale={size}:{size},format=gray",
                          '-fps_mode', 'passthrough', '-frames:v', '1', '-f', 'rawvideo', '-'],
                         capture_output=True).stdout
    assert len(raw) >= size*size, f'{path}: no frame {n}'
    return np.frombuffer(raw[:size*size], np.uint8).astype(np.float32)


def assert_range_lands(v, p):
    """⚠ PROVE EVERY RANGE'S FIRST AND LAST FRAME AGAINST THE MASTER, ON THE PIXELS.
    The seek above is correct by construction; this is what would have caught it when it was
    not. Encoder noise between a crf-16 re-encode and the master runs well under 1.0 mean gray
    level; a one-frame slip on this cut measures 1.4-122."""
    for k, n in ((0, p['n0']), (p['frames']-1, p['n0']+p['frames']-1)):
        d = float(np.abs(_gray(v, k) - _gray('picture.mp4', n)).mean())
        assert d < 1.0, (f"{v} frame {k} is NOT master frame {n} (mean gray diff {d:.2f}) -- "
                         f"the selection has slipped; do not ship this cutdown")


def main():
    P, total = plan()
    assert_no_orphan_overlay(P)
    dur = total/FPS
    print(f'{len(P)} ranges, {total} frames = {dur:.3f}s')
    for p, line in zip(P, transcript(P)):
        print(f"  {p['src0']:8.3f}-{p['src1']:8.3f} ({p['frames']:4d}f)  {line[:96]}")
    print('\n--- the cutdown read as prose ---')
    print(' / '.join(transcript(P)))
    assert dur <= 59.0, f'CUTDOWN IS {dur:.2f}s -- shorts ads must never exceed 0:59'
    json.dump(dict(ranges=P, frames=total, seconds=dur),
              open('cut_plan.json', 'w'), indent=1)
    if '--build' not in sys.argv:
        print('\n(plan only; run with --build to cut)'); return

    os.makedirs('cut', exist_ok=True)
    # ---- picture: frame-exact selection out of the finished square master ----
    names = []
    for i, p in enumerate(P):
        v = f'cut/v{i:02d}.mp4'
        if not os.path.exists(v) or nframes(v) != p['frames']:
            # ⚠⚠ SEEK HALF A FRAME EARLY, NEVER TO THE FRAME'S OWN TIME (audit 2, 2026-09-12).
            # This read `-ss f"{src0:.4f}"`, and whenever the 4-decimal rounding landed ABOVE the
            # frame's pts ffmpeg dropped that frame and the range started ONE FRAME LATE: 4 of 9
            # ranges were off by one. It cost a single-frame flash of the flag photo at the 13.35 s
            # seam (master f400 leaking in between the trees photo and the app recording), dropped
            # the peak frame of Muhammad's light leak at 75.81, and ran the picture 33 ms ahead of
            # the audio over 23.6 s of the 49 s. Seeking to (n0 - 0.5)/FPS lands between frames
            # n0-1 and n0, so the first decoded frame is always n0 -- and the assert below PROVES
            # it on the actual pixels rather than trusting the seek.
            sh([FF, '-nostdin', '-v', 'error', '-y', '-ss', f"{(p['n0'] - 0.5)/FPS:.6f}",
                '-i', 'picture.mp4',
                '-frames:v', str(p['frames']), '-r', '30000/1001', '-c:v', 'libx264',
                '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p',
                '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-an', v])
            assert nframes(v) == p['frames'], (v, nframes(v), p['frames'])
        assert_range_lands(v, p)
        names.append(os.path.basename(v))
    open('cut/vlist.txt', 'w').write(''.join(f'file {n}\n' for n in names))
    sh([FF, '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'cut/vlist.txt',
        '-c', 'copy', 'cut/picture.mp4'])
    assert nframes('cut/picture.mp4') == total

    # ---- audio: HIS MIX, CUT ------------------------------------------------
    n = cut_his_mix(P)
    print(f'cut/his_mix.wav {n} samples = {n/SR:.3f}s  (picture {total/FPS:.3f}s)')

    # ---- captions, re-timed through the range map ---------------------------
    import captions as CAP
    def m(t):
        for p in P:
            if p['src0'] <= t <= p['src1']: return p['dst0'] + (t - p['src0'])
        return None

    def mspan(a, b):
        """⚠ MAP A SPAN TO ITS INTERSECTIONS, CLAMPED -- NEVER ALL-OR-NOTHING. Mapping the
        two ends independently and dropping the span when either falls outside a range threw
        away BOTH CTA pills' caption mutes (each pill starts inside a kept range and ends
        just past it), and the delivered cutdown printed 'below to see yourself' straight
        over 'With Abs'. That is the A4.7 defect, reintroduced by a range-map helper."""
        out = []
        for p in P:
            a0, a1 = max(a, p['src0']), min(b, p['src1'])
            if a1 - a0 > 0.02:
                out.append((p['dst0'] + (a0 - p['src0']), p['dst0'] + (a1 - p['src0'])))
        return out

    def mword(s, e):
        """⚠ A WORD THAT STRADDLES A SEAM IS CLAMPED, NOT DROPPED (audit 2, 2026-09-12).
        Mapping the two ends independently and dropping the word when either fell outside a
        range deleted "You're" from the cutdown's captions -- its CTC start was 35 ms before the
        seam -- so the line read "more attractive to" while the audio said "You're more
        attractive to women". Same class as the mute-span bug in mspan() one function below."""
        best = None
        for p in P:
            a0, a1 = max(s, p['src0']), min(e, p['src1'])
            if a1 > a0 and (best is None or a1 - a0 > best[1] - best[0]):
                best = (p['dst0'] + (a0 - p['src0']), p['dst0'] + (a1 - p['src0']))
        return best

    words = [(w,) + (mword(s, e) or (None, None)) for w, s, e in CAP.load_words()]
    words = [w for w in words if w[1] is not None and w[2] is not None]
    mute = [x for a, b in CAP.suppressed() for x in mspan(a, b)]
    print(f'{len(mute)} caption mutes carried into the cutdown from '
          f'{len(CAP.suppressed())} in the master')
    # ⚠ ONLY THE REAL SEAMS. Four of this plan's eight joins are CONTIGUOUS in the source
    # (range 1 starts exactly where range 0 ends), so there is no cut there at all -- and
    # treating one as a seam would truncate a legitimate held word and capitalise a word in
    # the middle of a sentence ("I / generated this picture" -> "Generated this picture").
    real = [p['dst0'] for p, q in zip(P[1:], P[:-1]) if abs(p['src0'] - q['src1']) > 1e-3]
    BT.SEAMS = real
    print(f'{len(real)} real seams of {len(P)-1} joins: ' +
          ', '.join(f'{t:.2f}s' for t in real))
    # (The mute slack is kept off the seams by captions.groups() itself, which is also
    # what caption_sync_check.py re-derives its grouping from -- one implementation.)
    # ⚠ THE ONE MUTE LIST AND THE ONE WORD LIST FOR THIS CUTDOWN, written here and read by both the
    # render below and caption_sync_check.py. They used to be derived twice -- once here from the
    # master's spans through the in-memory plan, once by sqcut_build.py from cut_plan.json, whose
    # numbers are rounded to 5 decimals. The two agreed to a few milliseconds, and a few milliseconds
    # is enough: groups() mutes a word starting within 0.15 s of a span, so one word fell on opposite
    # sides of that line. The render burned 103 caption states, the gate re-derived 104 and reported
    # three misses on captions that are correct on the frame (2026-09-12).
    json.dump([[round(a, 4), round(b, 4)] for a, b in mute], open('cut/mute.json', 'w'))
    json.dump([dict(word=w, start=round(a, 4), end=round(b, 4)) for w, a, b in words],
              open('cut/words_ctc.json', 'w'), indent=0)
    gs = CAP.groups(words, mute)
    # a range that opens mid-sentence capitalises its first word (lesson A8.14)
    for g in gs:
        if any(abs(g[0][1] - s) < 0.08 for s in real):
            g[0] = (g[0][0][:1].upper() + g[0][0][1:], g[0][1], g[0][2])
    CAP.render(gs, out='cut/captions.mov', capdir='cut/cap',
               stops=[a for a, b in mute] + real)

    # ---- mux: his cut mix, AAC 320k, no filter of any kind ------------------
    sh([FF, '-nostdin', '-v', 'error', '-y', '-i', 'cut/picture.mp4', '-i', 'cut/captions.mov',
        '-i', 'cut/his_mix.wav',
        '-filter_complex', '[0:v][1:v]overlay=0:0:eof_action=pass[v]', '-map', '[v]', '-map', '2:a',
        '-frames:v', str(total), '-r', '30000/1001',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p',
        '-profile:v', 'high', '-level', '4.2',
        '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
        '-c:a', 'aac', '-b:a', '320k', '-ar', '48000', '-ac', '2',
        '-movflags', '+faststart', 'ad1_square_59s.mp4'])
    got = nframes('ad1_square_59s.mp4')
    assert got == total, f'cutdown is {got} frames, plan is {total}'
    print(f'ad1_square_59s.mp4 done -- {got} frames, {got/FPS:.2f}s')


if __name__ == '__main__':
    main()
