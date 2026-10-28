"""RO-24 round 4 audio repairs on the round 4 voice (film_voice_r4.wav -> film_voice_r4b.wav, same length), from the second
independent review (ROUND-4-REVIEW-2 items 5 and 6):
- five sharp clicks (0.3-1 ms spikes, up to -1.7 dBFS, far above the 20 ms around them): the spike samples only are replaced
  by a straight line between their neighbours, so no word or breath around them changes;
- Meghan Trainor's clip exit: her music bed fell about 15 dB in 0.2 s at the insert's end; a 0.30 s cosine fade now starts
  right after her last word ("pregnancy.", film 311.73) so it eases out under the cut."""
import json, wave, pathlib, numpy as np
R4 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round4'); SR = 48000
CLICKS = [274.9588, 345.5946, 502.2023, 350.9296, 364.8294]
MEGHAN_FADE = (311.75, 312.05)
with wave.open(str(R4 / 'audio/film_voice_r4.wav')) as r:
    p = r.getparams(); raw = r.readframes(p.nframes)
dt = {2: np.int16, 4: np.int32}[p.sampwidth]; full = float(np.iinfo(dt).max)
a = np.frombuffer(raw, dt).reshape(-1, p.nchannels).astype(np.float64) / full
log = []
for t in CLICKS:
    c = int(round(t * SR)); lo, hi = c - int(0.003 * SR), c + int(0.003 * SR)
    ctx = np.r_[a[c - int(0.025 * SR):lo, 0], a[hi:c + int(0.025 * SR), 0]]
    thr = max(4 * np.sqrt((ctx ** 2).mean()), 1e-4)
    bad = np.nonzero(np.abs(a[lo:hi, 0]) > thr)[0]
    if not len(bad): log.append(dict(t=t, fixed=0)); continue
    s0, s1 = lo + bad[0] - int(0.0003 * SR), lo + bad[-1] + int(0.0003 * SR) + 1
    before = 20 * np.log10(np.abs(a[s0:s1, 0]).max() + 1e-12)
    for ch in range(p.nchannels):
        a[s0:s1, ch] = np.linspace(a[s0 - 1, ch], a[s1, ch], s1 - s0)
    log.append(dict(t=t, samples=int(s1 - s0), ms=round((s1 - s0) / SR * 1000, 2), peak_before_dbfs=round(before, 1),
                    peak_after_dbfs=round(20 * np.log10(np.abs(a[s0:s1, 0]).max() + 1e-12), 1), context_thr_dbfs=round(20 * np.log10(thr), 1)))
# lip smacks in pauses (review 3): the smack's few ms replaced by room tone from just before it, 3 ms crossfades each side
SMACKS = [(364.672, 364.737, 364.55), (170.712, 170.737, 170.62)]
for t0, t1, src in SMACKS:
    s0, s1, r0 = int(t0 * SR), int(t1 * SR), int(src * SR); n = s1 - s0; x = int(0.003 * SR)
    rt = a[r0:r0 + n].copy(); ramp = np.linspace(0, 1, x)[:, None]
    rt[:x] = a[s0:s0 + x] * (1 - ramp) + rt[:x] * ramp; rt[-x:] = rt[-x:] * (1 - ramp) + a[s1 - x:s1] * ramp
    a[s0:s1] = rt
    log.append(dict(t=t0, smack_ms=round(n / SR * 1000, 1), room_tone_from=src))
# Tracy Morgan's exit (review 4): the audience reaction after "I gained 40 pounds." was cut in 80 ms; ease it out over the
# 0.28 s between his last word (film 404.553) and the insert's end (404.837)
t0, t1 = int(404.56 * SR), int(404.837 * SR)
a[t0:t1] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, t1 - t0)))[:, None]
log.append(dict(tracy_fade=[404.56, 404.837]))
f0, f1 = (int(x * SR) for x in MEGHAN_FADE)
a[f0:f1] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, f1 - f0)))[:, None]
a[f1:f1 + int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))[:, None] * 0 + np.clip(np.linspace(0, 1, int(0.02 * SR)), 0, 1)[:, None]
out = np.clip(np.round(a * full), np.iinfo(dt).min, np.iinfo(dt).max).astype(dt)
with wave.open(str(R4 / 'audio/film_voice_r4b.wav'), 'w') as w:
    w.setparams(p); w.writeframes(out.tobytes())
json.dump(dict(clicks=log, meghan_fade=MEGHAN_FADE), open(R4 / 'audio/audiofix_r4.json', 'w'), indent=1)
print(json.dumps(log, indent=1))
