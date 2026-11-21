"""Cut the voice for an EDL from the lav in one pass, sample-exact to the frame grid (frame f starts at f*1601.6 samples at
48 kHz). Round 2: every join is a 40 ms equal-power CROSSFADE centred on the cut (each side runs 20 ms past it), so the room
sound runs straight through; round 1 faded each side to zero, which left a 30 ms hole in the room tone that a listener hears as a
cut breath or a click. Every edge still sits in measured silence; the film length is unchanged. Writes a mono 24-bit WAV and the
audio join times (film seconds) for plan.json's audio_joins."""
import sys, json, numpy as np, subprocess, wave
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'; SPF = 48000 * 1001 / 30000
edl, out = sys.argv[1], sys.argv[2]
E = json.load(open(edl))
raw = subprocess.check_output([FF, '-v', 'error', '-i', '/Volumes/Expansion/_edit_work/RO-24/round1/audio/lav_full.wav', '-f', 'f32le', '-ac', '1', '-'])
x = np.frombuffer(raw, np.float32)
XF = int(.020 * 48000)                       # half crossfade, samples
th = np.linspace(0, np.pi / 2, 2 * XF)
fin, fout = np.sin(th), np.cos(th)          # equal power (uncorrelated room tone on the two sides)
y = np.zeros(int(round(sum(p['f1'] - p['f0'] for p in E['pieces']) * SPF)) + 2 * XF, np.float32)
joins = []; g = 0
for i, p in enumerate(E['pieces']):
    a = int(round(p['f0'] * SPF)); o0 = int(round(g * SPF))
    n = int(round((g + p['f1'] - p['f0']) * SPF)) - o0      # keep the cumulative length on the frame grid
    first, last = i == 0, i == len(E['pieces']) - 1
    lo = 0 if first else XF; hi = 0 if last else XF            # run 20 ms past each inner cut
    seg = x[a - lo:a + n + hi].copy()
    if not first: seg[:2 * XF] *= fin                         # fade in across the cut
    if not last: seg[-2 * XF:] *= fout                        # fade out across the cut
    y[o0 - lo:o0 + n + hi] += seg
    if i: joins.append(round(g * 1001 / 30000, 4))
    g += p['f1'] - p['f0']
y = y[:int(round(g * SPF))]

w = wave.open(out, 'w'); w.setnchannels(1); w.setsampwidth(3); w.setframerate(48000)
i32 = (np.clip(y, -1, 1) * 8388607).astype('<i4'); w.writeframes(b''.join(int(v).to_bytes(3, 'little', signed=True) for v in i32[:0]) or (i32.view(np.uint8).reshape(-1, 4)[:, :3].tobytes())); w.close()
json.dump(dict(frames=g, seconds=g * 1001 / 30000, samples=len(y), audio_joins=joins, join='40 ms equal-power crossfade'), open(out + '.json', 'w'), indent=1)
print('voice', out, len(y) / 48000, 'frames', g, 'joins', joins)
