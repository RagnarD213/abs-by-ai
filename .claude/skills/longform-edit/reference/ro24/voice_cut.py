"""Cut the voice for an EDL from the lav in one pass, sample-exact to the frame grid (frame f starts at f*1601.6 samples at
48 kHz), 15 ms raised-cosine fades at every piece edge (every edge sits in measured silence). Writes a mono 24-bit WAV and the
audio join times (film seconds) for plan.json's audio_joins."""
import sys, json, numpy as np, subprocess, wave
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'; SPF = 48000 * 1001 / 30000
edl, out = sys.argv[1], sys.argv[2]
E = json.load(open(edl))
raw = subprocess.check_output([FF, '-v', 'error', '-i', '/Volumes/Expansion/_edit_work/RO-24/round1/audio/lav_full.wav', '-f', 'f32le', '-ac', '1', '-'])
x = np.frombuffer(raw, np.float32)
parts = []; joins = []; g = 0; fade = int(.015 * 48000); ramp = .5 - .5 * np.cos(np.linspace(0, np.pi, fade))
for i, p in enumerate(E['pieces']):
    a, b = int(round(p['f0'] * SPF)), int(round(p['f1'] * SPF))
    n = int(round((g + p['f1'] - p['f0']) * SPF)) - int(round(g * SPF))      # keep the cumulative length on the frame grid
    seg = x[a:a + n].copy(); seg[:fade] *= ramp; seg[-fade:] *= ramp[::-1]
    parts.append(seg)
    if i: joins.append(round(g * 1001 / 30000, 4))
    g += p['f1'] - p['f0']
y = np.concatenate(parts)
w = wave.open(out, 'w'); w.setnchannels(1); w.setsampwidth(3); w.setframerate(48000)
i32 = (np.clip(y, -1, 1) * 8388607).astype('<i4'); w.writeframes(b''.join(int(v).to_bytes(3, 'little', signed=True) for v in i32[:0]) or (i32.view(np.uint8).reshape(-1, 4)[:, :3].tobytes())); w.close()
json.dump(dict(frames=g, seconds=g * 1001 / 30000, samples=len(y), audio_joins=joins), open(out + '.json', 'w'), indent=1)
print('voice', out, len(y) / 48000, 'frames', g, 'joins', joins)
