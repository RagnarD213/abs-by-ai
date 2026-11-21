#!/usr/bin/env python3
"""Voice + music bed + SFX for the 9:16 cut.

VOICE IS THE RIGHT CHANNEL ONLY, AS MONO. C1591 is not a stereo recording: it carries two
different microphones ~7.8 ms apart with the far one polarity-inverted. Summing them is a
comb filter no EQ can undo. Right = the lav. The voice is then EQ-fitted band by band to
MUHAMMAD'S FINISHED MIX, because his cut is the one Dan approved.

TWO THINGS CHANGED AFTER ATTEMPT 1, both from measurement:

  MUSIC. Attempt 1 reused `rev5/music/acoustic_bg.mp3`, a bed a previous session had
  picked by spectral shape against a DIFFERENT, older reference. Dan: "the music is
  sleepy... it kind of puts me to sleep." His bed measures a 0.480 s beat -- 125 BPM --
  with the pulse carried in a 6-14 kHz hat pattern and a 30-150 Hz kick.
  `music/funk_break.mp3` measures 0.480 s exactly, the closest band profile of nineteen
  candidates and the flattest energy over four minutes. Pixabay Content Licence: commercial
  use, NO attribution (Werq matched the tempo exactly too but is Kevin MacLeod CC-BY, which
  needs perpetual credit and is heavily Content-ID fingerprinted).

  SFX. Attempt 1 fired 83 events -- one every 2.8 s -- programmatically on every beat
  boundary including plain b-roll cuts. Dan: "weird swishing, swiping side effect appearing
  at random points." His cut was then measured: a high-band transient detector over 48
  candidate graphic moments found 21 above the p90 baseline, one every 11 s, and ZERO on
  his ten white-flash transitions or on footage-to-footage cuts. HIS_SFX below is that
  list, mapped to our matching beat. Nothing is added mechanically.
"""
import json, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
import sfxlib

FF  = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = ("/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, "
       "outdoor workout content | jeff chagrin | dan rose/C1591.MP4")
HIS = "ref_audit/his.wav"
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio'); from common import load_source
LAV = load_source(SRC)   # pick_lav.py decides which track is the lav on THIS roll; never a channel number
MUSIC = "music/funk_break.mp3"
FPS = 30000/1001; SR = 48000
BANDS = [(80,150),(150,250),(250,400),(400,700),(700,1200),(1200,2000),
         (2000,3200),(3200,5000),(5000,8000),(8000,10500)]
MUSIC_DB = -19.0

# (our time, class) -- one per SFX HE actually plays, at our matching beat.
HIS_SFX = [
  ( 2.95, 'whoosh'),   # card in (his 2.80)
  ( 4.95, 'whoosh'),   # second half of the sequential hook card (his 4.40 kicker)
  (12.30, 'whoosh'),   # "today" photo montage
  (12.80, 'pop'),      # third photo (his 13.05)
  (14.70, 'pop'),      # bullet 1
  (23.50, 'pop'),      # bullet 3
  (36.90, 'whoosh'),   # lower third
  (47.95, 'whoosh'),   # fitness-model card
  (61.45, 'whoosh'),   # photoshop gag, full frame
  (68.45, 'whoosh'),   # product screen + Dan
  (86.90, 'whoosh'),   # lower third
  (101.50,'whoosh'),   # first AI clip
  (111.00,'whoosh'),   # lower third
  (126.40,'whoosh'),   # 200-lb card
  (137.90,'whoosh'),   # phone-in-hand card
  (171.80,'whoosh'),   # statement
  (183.00,'whoosh'),   # lower third
  (187.30,'whoosh'),   # full-frame product screen
  (200.00,'whoosh'),   # lower third
  (213.20,'whoosh'),   # lower third
  (222.80,'pop'),      # last bullet
]

def sh(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit(1)
    return r

# ---------------------------------------------------------------- 1. conform voice
def conform():
    if os.path.exists('voice_raw.wav'): return
    S = json.load(open('edl_frames.json'))
    os.makedirs('aud', exist_ok=True)
    with open('aud/list.txt','w') as f:
        for s in S:
            o = f'aud/a{s["i"]:03d}.wav'
            n = int(round(s['frames']*SR*1001/30000))
            if not os.path.exists(o):
                sh([FF,'-v','error','-y','-ss',f'{s["src_in"]:.4f}','-i',SRC,
                    '-map', LAV['map'], '-af', f"{LAV['filter']},atrim=end_sample={n},asetpts=N/SR/TB",
                    '-ar',str(SR),'-ac','1','-c:a','pcm_s16le',o])
            f.write(f"file a{s['i']:03d}.wav\n")
    sh([FF,'-v','error','-y','-f','concat','-safe','0','-i','aud/list.txt','-c','copy','voice_raw.wav'])

# ---------------------------------------------------------------- 2. EQ fit to his voice
def spec_of(path, af, wins):
    parts = []
    for i, (ss, d) in enumerate(wins):
        p = f'_s{i}.wav'
        sh([FF,'-v','error','-y','-ss',str(ss),'-t',str(d),'-i',path,'-af',af,
            '-ac','1','-ar','22050','-c:a','pcm_s16le',p]); parts.append(p)
    a = np.concatenate([np.frombuffer(wave.open(p).readframes(10**9), dtype='<i2').astype(float)/32768
                        for p in parts])
    N = 2048
    fr = np.array([a[i:i+N]*np.hanning(N) for i in range(0, len(a)-N, 512)])
    S = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(N, 1/22050)
    rms = np.sqrt((fr**2).mean(1)); keep = rms > np.percentile(rms, 55)
    m = S[keep].mean(0) + 1e-12
    return f, 20*np.log10(m/m.sum()*len(m))

WINS = [(30.0,4),(60.0,4),(95.0,4),(145.0,4),(200.0,4)]
def fit_eq():
    if os.path.exists('eq.json'): return json.load(open('eq.json'))
    F, H = spec_of(HIS, 'pan=mono|c0=0.5*c0+0.5*c1', WINS)
    _, O = spec_of('voice_raw.wav', 'anull', WINS)
    errs = [float(H[(F>=lo)&(F<hi)].mean() - O[(F>=lo)&(F<hi)].mean()) for lo, hi in BANDS]
    json.dump(errs, open('eq.json','w'))
    print('band error before fit (his - ours), dB:', ' '.join(f'{e:+.1f}' for e in errs))
    return errs

def eq_chain(errs):
    out = []
    for (lo, hi), g in zip(BANDS, errs):
        fc = (lo*hi)**0.5; w = hi/lo
        g = max(-9.0, min(6.0, g))   # capping the top: the raw fit wants +8.8 dB at 9 kHz,
        if abs(g) < 0.35: continue   # which lifts lav hiss along with the air
        out.append(f'equalizer=f={fc:.0f}:t=q:w={1.6/np.log2(w):.2f}:g={g:.2f}')
    return ','.join(out)

# ---------------------------------------------------------------- 3. SFX bed
def sfx_bed(dur):
    if os.path.exists('sfx.wav'): return
    y = np.zeros(int(dur*SR)+SR, dtype=np.float32)
    def put(t, s, g):
        i = int(t*SR)
        if i < 0 or i >= len(y): return
        n = min(len(s), len(y)-i); y[i:i+n] += s[:n].astype(np.float32)*g
    wh, pp = sfxlib.whoosh(0.40), sfxlib.pop()
    for t, kind in HIS_SFX:
        if kind == 'whoosh': put(t-0.10, wh, 0.26)
        else:                put(t-0.04, pp, 0.16)
    sfxlib.save('sfx.wav', y[:int(dur*SR)], stereo=False)
    print(f'{len(HIS_SFX)} SFX events = one every {dur/len(HIS_SFX):.1f}s '
          f'(his: 21, one every 11.1s; attempt 1: 83, one every 2.8s)')

# ---------------------------------------------------------------- 4. mix
def main():
    conform()
    dur = sum(s['frames'] for s in json.load(open('edl_frames.json')))/FPS
    errs = fit_eq(); eq = eq_chain(errs)
    print('EQ:', eq or '(flat)')
    sfx_bed(dur)
    voice = ('agate=threshold=0.010:ratio=3:attack=6:release=180,' + (eq+',' if eq else '') +
             'acompressor=threshold=0.10:ratio=3:attack=8:release=180:makeup=2,'
             'alimiter=limit=0.95')
    fc = (f'[0:a]{voice},aformat=channel_layouts=mono,asplit=2[v][vsc];'
          f'[1:a]aformat=channel_layouts=stereo,volume={MUSIC_DB}dB,'
          f'afade=t=in:st=0:d=1.2,afade=t=out:st={dur-2.2:.2f}:d=2.0[mus];'
          f'[mus][vsc]sidechaincompress=threshold=0.030:ratio=6:attack=8:release=320[musd];'
          f'[2:a]volume=-4dB[sfx];'
          f'[v][musd][sfx]amix=inputs=3:duration=first:normalize=0[mx];'
          f'[mx]loudnorm=I=-14:TP=-1.5:LRA=9[out]')
    sh([FF,'-v','error','-y','-i','voice_raw.wav','-stream_loop','-1','-i',MUSIC,'-i','sfx.wav',
        '-filter_complex',fc,'-map','[out]','-t',f'{dur:.4f}',
        '-ar',str(SR),'-ac','2','-c:a','pcm_s24le','audio.wav'])
    r = subprocess.run([FF,'-nostats','-hide_banner','-i','audio.wav','-af',
                        'loudnorm=print_format=summary','-f','null','-'],
                       capture_output=True, text=True).stderr
    print('\n'.join(l for l in r.split('\n') if 'Input' in l))

if __name__ == '__main__':
    main()
