"""DS-43 R2 reel for the panel behind Dan's reply and his physique lines (Dan: "play the horizontal clips of Terry Crews looking jacked
above me, shirtless and jacked", "a few more clips ... flexing and looking jacked ... when I talk about how he's got a good physique").
Eleven clean shots, 29.97 fps, 1080x608, BT.709, silent; hard cuts between them. Sources in /Volumes/Expansion/_edit_work/DS-43/src/flex/:
ZD = Muscle & Fitness "Behind The Scenes: Terry Crews is More Ripped Than Ever at 49" (ZDgGriH6Vx4), Hq = "All of the Terry Crews Old Spice
Commercials" (Hq2SlCja3zo), S9 = Old Spice Muscle Music (S9iKC7vb-Ts, dropped: Old Spice sign in frame), rr = America's Got Talent Pec Popping 101 (rrsbh6Sks0I).
Writes src/flex_reel.npy (frames, 608, 1080, 3)."""
import subprocess, numpy as np
from pathlib import Path
W = Path(__file__).resolve().parents[1]; F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'; D = '/Volumes/Expansion/_edit_work/DS-43/src/flex/'
FPS = 30000/1001
Z, H, S, R = 'ZDgGriH6Vx4', 'Hq2SlCja3zo', 'S9iKC7vb-Ts', 'rrsbh6Sks0I'
#        source  in s    frames    what (R2 independent review: no monitors, screens or signs; every cut lands with or well clear of Dan's cuts)
REEL = [(Z,      62.50,  97),  # A shirtless in the gym ring, flexes toward the camera   (reply starts, film 15.72)
        (Z,     150.90,  97),  # C walks to the lens, pecs and arms
        (Z,     118.98,  47),  # B abs and chest beside the heavy bag; ends on Dan's cut at 23.76
        (Z,      58.62,  33),  # I close, chest and arm, pointing at the lens
        (Z,      84.02,  23),  # flexed back on the pull-up bar, close
        (Z,     134.16,  19, 1.0, 'crop=iw*0.82:ih*0.82:iw*0.18:ih*0.09,'),  # boxing gloves, glistening; 134.15-134.78 is the clean window (a dissolve follows; 39.34 is mid-dissolve, never use it); crop drops a monitor strip at left
        (Z,      27.15,  45, 1.30),  # shirtless profile, same;  ends on Dan's cut at 27.76
        (R,      44.60,  72),  # E pec pops, shirtless                                   ("great physique")
        (R,      47.85,  30),  # shirtless, front on (the bathroom ad shot showed a readable can: never use it)
        (H,     338.10,  68)]  # skyscraper: pose into double biceps, one continuous source shot (it ends 340.40; the 16 Hour logo card follows, never use it)
N = None
if __name__ == '__main__':
    tot = []
    for s, a, n, *g in REEL:
        d = n/FPS; lift = f'eq=gamma={g[0]},' if g and g[0] != 1.0 else ''; crop = g[1] if len(g) > 1 else ''
        raw = subprocess.check_output([F, '-nostdin', '-v', 'error', '-ss', f'{a - 1:.3f}', '-i', D + s + '.mkv', '-ss', '1', '-t', f'{d + 0.2:.3f}', '-an', '-vf',
            'fps=30000/1001,' + crop + 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc:w=1080:h=608:flags=area,' + lift + 'format=rgb24', '-f', 'rawvideo', '-'])
        a_ = np.frombuffer(raw, np.uint8).reshape(-1, 608, 1080, 3)
        assert len(a_) >= n, (s, a, len(a_), n); tot.append(a_[:n]); print(s[:2], a, n, flush=True)
    r = np.concatenate(tot); np.save(W/'src/flex_reel.npy', r); print('REEL', r.shape, round(len(r)/FPS, 3), 's')
