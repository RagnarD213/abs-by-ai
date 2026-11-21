"""RO-24 take selection for the whole film (prep for round 2; the first-minute pieces are the round-1 EDL, unchanged).
Each beat is (first words, approx start s, last words, approx end s, why) on the medium.en source transcript; edges are then
placed on the measured lav envelope: in = speech onset - 0.12 s (onset = first 10 ms frame over -38 dB after >= 50 ms under
-44 dB), out = last frame over -38 dB + 0.08 s (followed by >= 60 ms under -44 dB). Prints each piece's head and tail words so
every edge can be read. Writes edl_full_takes.json."""
import json, numpy as np, subprocess
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'; FPS = 30000 / 1001
W = '/Volumes/Expansion/_edit_work/RO-24/round1'
x = np.frombuffer(subprocess.check_output([FF, '-v', 'error', '-i', f'{W}/audio/lav_full.wav', '-f', 'f32le', '-ac', '1', '-']), np.float32)
n = 480; L = 20 * np.log10(np.sqrt(np.mean(x[:len(x) // n * n].reshape(-1, n) ** 2, 1)) + 1e-9)    # 10 ms frames
WS = json.load(open(f'{W}/audio/words_src.json'))
def onset(t):
    i0, i1 = int((t - .45) * 100), int((t + .35) * 100)
    for i in range(i0, i1):
        if L[i] > -38 and (L[i - 5:i] < -44).all(): return i / 100
    return None
def offset(t):
    i0, i1 = int((t - .35) * 100), int((t + .45) * 100)
    for i in range(i1, i0, -1):
        if L[i] > -38 and (L[i + 1:i + 7] < -44).all(): return (i + 1) / 100
    return None
# (start s, end s, note): starts and ends are the word times of the chosen take on the medium.en transcript
BEATS = [
 (536.62, 563.02, 'hook, last take (536); earlier take 495 is clean too'),
 (570.18, 587.46, 'Sharon retake after the aborted "She went under a one"'),
 (590.32, 593.54, '"Your face looks deflated..." retake (the 587.5 one is cut off)'),
 (598.93, 666.56, '"Sharon\'s Ozempic face..." retake after the 594 restart, through "not a serious risk"'),
 (671.50, 738.90, 'Fat Joe, second take of the intro line ("did it the right way")'),
 (766.14, 807.96, 'Amy Schumer retake of "Next up" (the 741 one has a 17 s gap), through "lost about 33"'),
 (811.88, 823.72, 'second "and only about half as many people quit Zepbound because of stomach side effects"'),
 (824.42, 844.72, 'Meghan Trainor, through the first clean "I\'m proof of it"'),
 (848.28, 869.30, 'skips "I\'m actually, I\'m proof of it"'),
 (872.92, 876.54, 'second "if you can\'t do these things, you shouldn\'t even start taking the drug"'),
 (882.86, 892.56, 'third "do a short weightlifting workout every day..." through "at every meal"'),
 (893.48, 984.24, 'Oprah, Tracy Morgan, the trial, microdose, stepping down'),
 (1000.70, 1008.14, 'recap, "Number one"'),
 (1012.18, 1021.20, 'second "Number two" through "for life"'),
 (1027.52, 1031.48, 'second "If you can\'t do that..."'),
 (1052.66, 1066.42, 'last take of "Do these four things" and the close'),
]
pieces = []
for a, b, note in BEATS:
    on = onset(a); off = offset(b)
    tin = (on - .12) if on else a - .12; tout = (off + .08) if off else b + .08
    words = [w for w in WS if tin <= (w['t0'] + w['t1']) / 2 <= tout]
    pieces.append(dict(f0=int(round(tin * FPS)), f1=int(round(tout * FPS)), t_in=round(tin, 3), t_out=round(tout, 3), onset_found=on is not None,
                       offset_found=off is not None, head=' '.join(w['w'] for w in words[:6]), tail=' '.join(w['w'] for w in words[-6:]), note=note))
    print(f"{tin:8.2f} {tout:8.2f} {'' if on else 'ON?'}{'' if off else 'OFF?'} | {pieces[-1]['head']} ... {pieces[-1]['tail']}")
tot = sum(p['f1'] - p['f0'] for p in pieces) / FPS
print('total', round(tot, 1), 's =', f'{int(tot // 60)}:{tot % 60:04.1f}')
json.dump(dict(note='round-2 prep: best take of every line; pauses inside pieces still to be capped', pieces=pieces, seconds=round(tot, 2)),
          open(f'{W}/edl_full_takes.json', 'w'), indent=1)
